#!/usr/bin/env python3
"""Validate the bundled SNS campaign contract without external dependencies.
Structural validation is not factual, policy, permission-provenance or API verification.
"""
import argparse,json,sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo,ZoneInfoNotFoundError

def validate(data,schema=None,require_posts=False):
    if schema is None:
        schema=json.loads((Path(__file__).resolve().parents[1]/'assets/campaign-schema.json').read_text())
    errors=[];warnings=[]
    def err(path,reason):errors.append({'path':path,'reason':reason})
    def matches(value,kind):
        return {'object':isinstance(value,dict),'array':isinstance(value,list),'string':isinstance(value,str),'integer':isinstance(value,int) and not isinstance(value,bool),'number':isinstance(value,(int,float)) and not isinstance(value,bool),'boolean':isinstance(value,bool),'null':value is None}.get(kind,False)
    def walk(value,rule,path):
        kinds=rule.get('type');kinds=[kinds] if isinstance(kinds,str) else kinds
        if kinds and not any(matches(value,k) for k in kinds):err(path,'type must be '+str(kinds));return
        if 'enum' in rule and value not in rule['enum']:err(path,'value outside enum')
        if isinstance(value,str) and len(value)<rule.get('minLength',0):err(path,'empty string')
        if isinstance(value,(int,float)) and not isinstance(value,bool) and value<rule.get('minimum',value):err(path,'below minimum')
        if isinstance(value,dict):
            for key in rule.get('required',[]):
                if key not in value:err(path+'.'+key,'required field missing')
            for key,sub in rule.get('properties',{}).items():
                if key in value:walk(value[key],sub,path+'.'+key)
        if isinstance(value,list):
            for i,item in enumerate(value):walk(item,rule.get('items',{}),path+f'[{i}]')
    walk(data,schema,'$')
    if errors:return {'valid':False,'errors':errors,'warnings':warnings}
    tz=data['timezone']
    try:ZoneInfo(tz)
    except (ZoneInfoNotFoundError,ValueError):err('$.timezone','unknown IANA timezone')
    def indexed(items,key,path):
        result={}
        for i,item in enumerate(items):
            value=item[key]
            if value in result:err(path+f'[{i}].{key}','duplicate identifier')
            result[value]=item
        return result
    resources=indexed(data['resources'],'resource_id','$.resources')
    claims=indexed(data['claim_ledger'],'claim_id','$.claim_ledger')
    atoms=indexed(data['content_atoms'],'atom_id','$.content_atoms')
    posts=indexed(data['posts'],'content_id','$.posts')
    indexed(data['jobs'],'job_id','$.jobs')
    for i,c in enumerate(data['claim_ledger']):
        r=resources.get(c['source_id'])
        if not r:err(f'$.claim_ledger[{i}].source_id','resource does not exist')
        elif c['status']=='verified' and r['access_status']!='observed':err(f'$.claim_ledger[{i}].status','verified claim needs observed source')
    for i,a in enumerate(data['content_atoms']):
        for key in a['evidence_ids']:
            if key not in claims:err(f'$.content_atoms[{i}].evidence_ids','unknown claim '+key)
    for i,j in enumerate(data['jobs']):
        if j['brief_version']!=data['brief_version']:err(f'$.jobs[{i}].brief_version','stale Worker brief')
        for key in j['evidence_ids']:
            if key not in claims:err(f'$.jobs[{i}].evidence_ids','unknown claim '+key)
    def date(value,path):
        if value is None:return
        try:
            d=datetime.fromisoformat(value.replace('Z','+00:00'))
            if d.tzinfo is None:err(path,'timestamp requires UTC offset')
        except ValueError:err(path,'invalid ISO datetime')
    for i,p in enumerate(data['posts']):
        path=f'$.posts[{i}]'
        if p['timezone']!=tz:err(path+'.timezone','different from campaign timezone')
        if p['channel'] not in data['selected_channels']:err(path+'.channel','channel not selected')
        date(p['publish_at'],path+'.publish_at')
        for key in p['claim_ids']:
            if key not in claims:err(path+'.claim_ids','unknown claim '+key)
        for key in p['source_atom_ids']:
            if key not in atoms:err(path+'.source_atom_ids','unknown atom '+key)
        if p['publication_status'] in ('ready','scheduled','published'):
            if p['qa_status']!='passed':err(path+'.qa_status','ready/executed requires QA passed')
            for key in p['claim_ids']:
                if key in claims and claims[key]['status'] in ('unknown','hypothesis'):err(path+'.claim_ids','unresolved claim used in ready post')
            if any(a['status']=='requested' for a in p['asset_specs']):err(path+'.asset_specs','requested asset blocks ready')
            lc=p['length_check']
            if lc['status'] not in ('passed','not_applicable') or not lc['evidence']:err(path+'.length_check','resolved length check and evidence required')
            if p['channel']=='x' and lc['status']!='passed':err(path+'.length_check','X needs passed weighted-length check')
            features={f['name']:f for f in p['feature_checks']}
            for key in ('upload_rules','link_route','rights'):
                f=features.get(key)
                if not f or f['status']=='unverified' or not f['evidence']:err(path+'.feature_checks','resolved '+key+' evidence required')
            if p['link_path'] in ('external_url','profile_link','story_link') and not p['supplied_url']:err(path+'.supplied_url','URL required for this CTA route')
        if p['publication_status'] in ('scheduled','published'):
            receipt=p['execution_receipt']
            if not isinstance(receipt,dict) or not all(receipt.get(k) is not None for k in ('receipt_id','account_id','channel','content_id','revision')):err(path+'.execution_receipt','execution receipt missing');continue
            if not data['permissions']['publish']:err(path+'.publication_status','publishing not authorized')
            if receipt['channel']!=p['channel'] or receipt['content_id']!=p['content_id'] or receipt['revision']!=p['revision']:err(path+'.execution_receipt','receipt version/channel/content mismatch')
            scope=data['permissions']['scope']
            matching=any(s['action']=='publish' and s['account_id']==receipt['account_id'] and s['channel']==p['channel'] and s['content_id']==p['content_id'] and s['revision']==p['revision'] and s['publish_at']==p['publish_at'] for s in scope)
            if not matching:err(path+'.publication_status','no matching account/channel/version/time permission scope')
    if require_posts or data['delivery_stage']=='final':
        if not data['posts']:err('$.posts','complete package requires posts')
        channels={p['channel'] for p in data['posts']}
        for c in data['selected_channels']:
            if c not in channels:err('$.posts','selected channel has no package: '+c)
    if data['delivery_stage']=='bootstrap':warnings.append('Bootstrap is an initial template, not a complete campaign.')
    if any(p['publication_status']=='draft' for p in data['posts']):warnings.append('Draft posts require factual, asset, platform and account review before posting.')
    warnings.append('This check does not verify factual truth, exact X length, policy freshness, rights or actual API execution.')
    return {'valid':not errors,'errors':errors,'warnings':warnings}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('campaign',type=Path);parser.add_argument('--require-posts',action='store_true')
    args=parser.parse_args()
    try:
        data=json.loads(args.campaign.read_text(encoding='utf-8'));result=validate(data,require_posts=args.require_posts)
    except (OSError,ValueError) as e:
        result={'valid':False,'errors':[{'path':'$','reason':str(e)}],'warnings':[]}
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if result['valid'] else 1
if __name__=='__main__':sys.exit(main())
