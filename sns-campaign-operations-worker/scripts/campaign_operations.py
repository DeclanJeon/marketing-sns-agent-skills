#!/usr/bin/env python3
"""Validate operational sidecar and preserve immutable local snapshots. No publishing."""
import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime
from validate_campaign import validate

PAYLOAD_FIELDS = ('content_id','revision','channel','surface','format','hook','body_or_script','caption_or_description','title_cover','alt_text_or_captions','cta','link_path','supplied_url','utm','publish_at','timezone','asset_specs')
CHECKS = {'semantic','channel_fit','accessibility','rights','upload_rules','length','cta_route'}

def canonical(obj):
    return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')

def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()

def payload_hash(post):
    return digest({k:post.get(k) for k in PAYLOAD_FIELDS})

def has_text(value):
    return isinstance(value,str) and bool(value.strip())

def aware_timestamp(value):
    try:
        return has_text(value) and datetime.fromisoformat(value.replace('Z','+00:00')).utcoffset() is not None
    except ValueError:
        return False

def check_operations(campaign,ops,root):
    errors=[]
    def require(test,message):
        if not test: errors.append(message)
    if not isinstance(ops,dict):return ['operations must be an object']
    require(ops.get('operations_version')=='1.0','unsupported operations_version')
    require(ops.get('campaign_id')==campaign.get('campaign_id'),'campaign_id mismatch')
    for key in ('assets','production_tasks','preflight','events','change_requests'):
        require(isinstance(ops.get(key),list),key+' must be an array')
    if errors:return errors
    posts={p['content_id']:p for p in campaign.get('posts',[])}
    def target(row,label):
        if not isinstance(row,dict):errors.append(label+' must be an object');return None
        p=posts.get(row.get('content_id'))
        require(p is not None,label+': unknown content_id')
        if p:require(type(row.get('revision')) is int and row.get('revision')==p['revision'],label+': stale revision')
        return p
    assets={}; post_assets={k:{} for k in posts}
    for a in ops['assets']:
        p=target(a,'asset')
        if not isinstance(a,dict):continue
        aid=a.get('asset_id'); require(has_text(aid),'asset_id required')
        if not has_text(aid):continue
        require(aid not in assets,'duplicate asset_id'); assets[aid]=a
        require(a.get('status') in ('requested','provided','generated','failed'),'asset: invalid status')
        if p and a.get('status') in ('provided','generated'):
            path=a.get('path'); expected=a.get('sha256')
            if not has_text(path):errors.append('asset: path required');continue
            f=Path(path);f=f if f.is_absolute() else root/f
            if not f.is_file():errors.append('asset: file missing');continue
            got=hashlib.sha256(f.read_bytes()).hexdigest()
            require(expected==got,'asset: hash mismatch')
            post_assets[p['content_id']][aid]=got
            if a.get('status')=='generated':require(has_text(a.get('generation_receipt')),'generated asset requires actual receipt locator')
    for task in ops['production_tasks']:
        p=target(task,'production task')
        if not isinstance(task,dict):continue
        require(has_text(task.get('task_id')),'task_id required')
        require(task.get('brief_version')==campaign.get('brief_version'),'production task: stale brief')
        require(task.get('status') in ('planned','in_progress','completed','blocked'),'production task: invalid status')
        require(has_text(task.get('owner_skill')),'owner_skill required')
        refs=task.get('asset_ids',[]);require(isinstance(refs,list),'task asset_ids must be array')
        if not isinstance(refs,list):continue
        for aid in refs:
            a=assets.get(aid);require(a is not None,'task: unknown asset')
            if a:require(a.get('content_id')==task.get('content_id') and a.get('revision')==task.get('revision'),'task: wrong asset binding')
        if task.get('status')=='completed':require(bool(refs) and all(assets.get(i,{}).get('status') in ('provided','generated') for i in refs),'completed task requires actual assets')
    preflights={}
    for pf in ops['preflight']:
        p=target(pf,'preflight')
        if not p:continue
        cid=p['content_id'];require(cid not in preflights,'duplicate preflight for current content');preflights[cid]=pf
        require(pf.get('payload_sha256')==payload_hash(p),'preflight: payload changed')
        require(pf.get('channel')==p['channel'] and pf.get('surface')==p['surface'],'preflight: channel/surface mismatch')
        require(has_text(pf.get('account')),'preflight: account required')
        receipt=p.get('execution_receipt')
        if p.get('publication_status') in ('scheduled','published') and isinstance(receipt,dict):
            require(pf.get('account')==receipt.get('account_id'),'preflight: execution account mismatch')
        require(aware_timestamp(pf.get('checked_at')),'preflight: timestamp must include timezone')
        require(pf.get('asset_hashes')==post_assets[cid],'preflight: assets changed')
        checks=pf.get('checks',[]);require(isinstance(checks,list),'checks must be array')
        if not isinstance(checks,list):continue
        named={}
        for check in checks:
            if not isinstance(check,dict):errors.append('check must be object');continue
            name=check.get('name');require(name in CHECKS,'unknown check name');require(name not in named,'duplicate check');named[name]=check
            require(check.get('status') in ('passed','failed','unknown','not_applicable'),'invalid check status')
            if check.get('status') in ('passed','not_applicable'):
                require(has_text(check.get('evidence')) and has_text(check.get('method')),'resolved check requires evidence and method')
                if check.get('status')=='not_applicable':require(name in {'accessibility','rights','upload_rules'} and has_text(check.get('reason')),'not_applicable not allowed or reason missing')
        if p.get('publication_status') in ('ready','scheduled','published'):
            require(set(named)==CHECKS,'active post requires all seven preflight checks')
            require(all(c.get('status') in ('passed','not_applicable') for c in named.values()),'active post has unresolved preflight')
    for p in posts.values():
        if p.get('publication_status') in ('ready','scheduled','published'):
            require(p['content_id'] in preflights,'active post missing preflight')
            require(len(post_assets[p['content_id']])>=len(p.get('asset_specs',[])),'active post missing actual asset files')
    event_ids=set()
    for ev in ops['events']:
        if not isinstance(ev,dict):errors.append('event must be object');continue
        eid=ev.get('event_id');require(has_text(eid) and eid not in event_ids,'event_id required and unique')
        if has_text(eid):event_ids.add(eid)
        require(has_text(ev.get('content_id')) and type(ev.get('revision')) is int and ev['revision']>0,'event requires content/revision')
        require(ev.get('outcome') in ('planned','succeeded','failed','unknown'),'event: invalid outcome')
        require(aware_timestamp(ev.get('observed_at')),'event: timestamp must include timezone')
        require(has_text(ev.get('action')),'event: action required')
        if ev.get('outcome')=='succeeded':require(has_text(ev.get('receipt_locator')),'successful event requires receipt')
        if ev.get('outcome')=='unknown':require(has_text(ev.get('next_action')),'unknown event requires reconciliation task')
    for change in ops['change_requests']:
        if not isinstance(change,dict):errors.append('change_request must be object');continue
        require(has_text(change.get('content_id')) and type(change.get('from_revision')) is int,'change requires content/from_revision')
        require(change.get('decision') in ('keep','modify','stop','collect_more'),'invalid change decision')
        require(isinstance(change.get('observation_ids'),list),'observation_ids must be array')
        require(has_text(change.get('rationale')) and has_text(change.get('next_owner')),'change requires rationale/next_owner')
        if change.get('decision')=='modify':
            require(has_text(change.get('variable')) and has_text(change.get('decision_rule')) and has_text(change.get('review_window')),'modify requires variable/decision_rule/review_window')
            require(bool(change.get('observation_ids')) or change.get('status')=='planned','unobserved change must be planned')
    return errors

def snapshot(campaign,ops,directory):
    bundle={'campaign':campaign,'operations':ops}
    raw=canonical(bundle);sha=hashlib.sha256(raw).hexdigest()
    directory.mkdir(parents=True,exist_ok=True)
    dest=directory/(sha+'.json')
    try:
        with dest.open('xb') as f:f.write(raw+b'\n')
    except FileExistsError:
        if dest.read_bytes()!=raw+b'\n':raise ValueError('snapshot collision/corruption; refuse overwrite')
    return dest

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command',choices=['validate','snapshot']);ap.add_argument('campaign');ap.add_argument('operations');ap.add_argument('history',nargs='?')
    args=ap.parse_args()
    try:
        cp=Path(args.campaign);op=Path(args.operations)
        campaign=json.loads(cp.read_text());ops=json.loads(op.read_text())
        result=validate(campaign)
        errors=list(result['errors'])+check_operations(campaign,ops,op.parent)
        output={'passed':not errors,'errors':errors,'limitations':'Structure, binding and local file hashes only; no factual, live-platform or receipt authenticity verification.'}
        if not errors and args.command=='snapshot':
            if not args.history:raise ValueError('history directory required')
            output['snapshot']=str(snapshot(campaign,ops,Path(args.history)))
        print(json.dumps(output,ensure_ascii=False,indent=2));return 1 if errors else 0
    except (ValueError,OSError,KeyError,TypeError) as exc:
        print(json.dumps({'passed':False,'errors':[str(exc)]},ensure_ascii=False));return 1
if __name__=='__main__':raise SystemExit(main())
