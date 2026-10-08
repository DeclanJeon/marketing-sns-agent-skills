#!/usr/bin/env python3
"""Discover capability manifests and compile finite worker DAGs. No model calls or publishing."""
import argparse,itertools,json,re,hashlib,math
from pathlib import Path
class PlanningError(ValueError):pass
def read(path):return json.loads(Path(path).read_text())
def names(value):
 if not isinstance(value,list) or any(not isinstance(s,str) or not s.strip() for s in value):raise PlanningError('nonempty string array required')
 if len(set(value))!=len(value):raise PlanningError('duplicate values')
 return value
def validate_manifest(m,name):
 if not isinstance(m,dict) or m.get('schema_version')!='2.0' or m.get('role')!='worker' or m.get('skill_name')!=name:raise PlanningError('worker identity/schema mismatch: '+name)
 for k in ('provides','requires','channels','conflicts_with'):names(m.get(k))
 if not m['provides'] or type(m.get('phase')) is not int or m['phase']<0:raise PlanningError('invalid phase/provides: '+name)
 for c in m['channels']:
  if 'channel_package:'+c not in m['provides']:raise PlanningError('channel capability missing: '+name)
 return m
def discover(root):
 registry={}
 for p in sorted(Path(root).iterdir()):
  if not p.is_dir() or p.name=='uninstalled':continue
  f=p/'SKILL.md'; mf=p/'assets/worker-capability.json'
  if not f.is_file() or not mf.is_file():continue
  text=f.read_text();match=re.search(r'^name:\s*[\"\']?([a-z0-9-]+)[\"\']?\s*$',text,re.M)
  if not match:raise PlanningError('frontmatter name missing: '+str(p))
  name=match.group(1)
  if name in registry:raise PlanningError('duplicate worker name: '+name)
  manifest=read(mf)
  if isinstance(manifest,dict) and manifest.get('role')=='orchestrator':continue
  registry[name]=validate_manifest(manifest,name)
 return registry
def augment(registry,extra,installed_names):
 if not isinstance(extra,dict) or not isinstance(extra.get('workers'),list):raise PlanningError('extra registry requires workers array')
 result=dict(registry)
 for manifest in extra['workers']:
  if not isinstance(manifest,dict):raise PlanningError('extra worker must be object')
  name=manifest.get('skill_name')
  if name not in installed_names:raise PlanningError('extra worker is not installed')
  if name in result:raise PlanningError('extra worker duplicates registered name')
  result[name]=validate_manifest(manifest,name)
 return result
def installed_names(root):
 result=set()
 for p in Path(root).iterdir():
  if not p.is_dir() or p.name=='uninstalled' or not (p/'SKILL.md').is_file():continue
  match=re.search(r'^name:\s*[\"\']?([a-z0-9-]+)[\"\']?\s*$',(p/'SKILL.md').read_text(),re.M)
  if match:result.add(match.group(1))
 return result
def providers(registry,cap,overrides):
 candidates=[n for n,m in registry.items() if cap in m['provides']]
 if cap in overrides:
  chosen=overrides[cap]
  if chosen not in candidates:raise PlanningError('override does not provide: '+cap)
  return chosen
 if len(candidates)!=1:raise PlanningError('missing or ambiguous capability: '+cap+'; candidates='+','.join(sorted(candidates)))
 return candidates[0]
def compile_plan(registry,recipes,job):
 if not isinstance(job,dict):raise PlanningError('job must be object')
 matches=[r for r in recipes['recipes'] if r['id']==job.get('recipe_id')]
 if len(matches)!=1:raise PlanningError('unknown recipe')
 recipe=matches[0]; channels=names(job.get('channels',[])); overrides=job.get('provider_overrides',{})
 if not isinstance(overrides,dict):raise PlanningError('provider_overrides must be object')
 if recipe['channel_mode']=='required' and not channels:raise PlanningError('select channels before compiling')
 if recipe['channel_mode']=='none' and channels:raise PlanningError('use an SNS recipe for channel deliverables')
 cap_inputs=job.get('available_capabilities',{})
 if not isinstance(cap_inputs,dict) or any(not isinstance(k,str) or not isinstance(v,str) or not v.strip() for k,v in cap_inputs.items()):raise PlanningError('available capabilities require artifact IDs')
 # brief/evidence ledger always produced by intake; empty evidence is an explicit draft, not proof.
 external={'brief':'intake:brief','evidence_ledger':'intake:evidence-ledger',**cap_inputs}
 extras=names(job.get('extra_capabilities',[]));flags=job.get('flags',{})
 if not isinstance(flags,dict) or any(type(v) is not bool for v in flags.values()):raise PlanningError('flags must be boolean map')
 required=list(recipe['required_capabilities'])+list(recipe['final_capabilities'])+extras
 for flag,cap in recipe.get('conditional_additions',{}).items():
  if flags.get(flag):required.append(cap)
 if channels:
  required += ['channel_package:'+c for c in channels]+['distribution_plan','channel_quality','campaign_operations','social_measurement']
 selected={};bindings={};visiting=set()
 def resolve(cap):
  if cap in external:
   bindings[cap]={'kind':'reused_input','artifact_id':external[cap]};return None
  if cap=='channel_packages':
   if not channels:raise PlanningError('channel packages need selected channels')
   owners=[resolve('channel_package:'+c) for c in channels]
   bindings[cap]={'kind':'aggregate','members':['channel_package:'+c for c in channels]};return owners
  if cap in bindings:return bindings[cap]['worker']
  if cap in visiting:raise PlanningError('dependency cycle: '+cap)
  visiting.add(cap);owner=providers(registry,cap,overrides);m=registry[owner]
  selected[owner]=m
  for req in m['requires']:resolve(req)
  visiting.remove(cap);bindings[cap]={'kind':'worker_output','worker':owner};return owner
 for cap in dict.fromkeys(required):resolve(cap)
 for n,m in selected.items():
  if set(m['conflicts_with'])&set(selected):raise PlanningError('incompatible workers: '+n)
 # Dependencies reflect input producers; phases lock strategic inputs before channel fan-out.
 deps={n:set() for n in selected}
 def owners(cap):
  b=bindings.get(cap,{})
  if b.get('kind')=='worker_output':return {b['worker']}
  if b.get('kind')=='aggregate':return set().union(*(owners(c) for c in b['members']))
  return set()
 for n,m in selected.items():
  for req in m['requires']:deps[n]|=owners(req)-{n}
  deps[n]|={other for other,o in selected.items() if o['phase']<m['phase']}
 done=set();groups=[]
 while len(done)<len(selected):
  ready=sorted(n for n in selected if n not in done and deps[n]<=done)
  if not ready:raise PlanningError('worker dependency/phase cycle')
  groups.append(ready);done.update(ready)
 statuses=[]
 estimates=job.get('worker_estimates',{})
 if not isinstance(estimates,dict):raise PlanningError('worker_estimates must be object')
 total=0;unknown=[]
 for n in selected:
  est=estimates.get(n,selected[n].get('estimated_minutes'))
  if est is None:unknown.append(n)
  elif type(est) not in (int,float) or not math.isfinite(est) or est<0:raise PlanningError('invalid time estimate')
  else:total+=est
 time_cap=job.get('time_cap_minutes')
 if time_cap is not None and (type(time_cap) not in (int,float) or not math.isfinite(time_cap) or time_cap<0):raise PlanningError('invalid time cap')
 if unknown:statuses.append('time_estimates_missing')
 if time_cap is not None and total>time_cap:statuses.append('known_work_exceeds_time_cap')
 signature=hashlib.sha256(json.dumps({'job':job,'workers':selected,'recipe':recipe},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
 tasks=[{'task_id':'task:'+n,'worker':n,'requires':selected[n]['requires'],'provides':selected[n]['provides'],'depends_on':['task:'+d for d in sorted(deps[n])],'scope':'capability outputs only','acceptance':'complete output, version/evidence binding, unresolved and next owner','execution_status':'not_started'} for group in groups for n in group]
 return {'schema_version':'2.0','plan_id':signature,'recipe_id':recipe['id'],'channels':channels,'planning_status':'planned','execution_status':'not_started','tasks':tasks,'parallel_groups':groups,'capability_bindings':bindings,'known_total_worker_minutes':total,'resource_review':statuses,'unknown_estimate_workers':unknown,'note':'Plan only; no API, creation, publishing or outcome verification. Explicit channels are never silently dropped.'}
def combinations(registry,recipes):
 channels=sorted({c for m in registry.values() for c in m['channels']});counts=[];unique=set();failed=[]
 for recipe in recipes['recipes']:
  subsets=[()] if recipe['channel_mode']=='none' else [s for k in range(1,len(channels)+1) for s in itertools.combinations(channels,k)]
  valid=0
  for subset in subsets:
   try:p=compile_plan(registry,recipes,{'recipe_id':recipe['id'],'channels':list(subset)})
   except PlanningError as e:failed.append({'recipe':recipe['id'],'channels':subset,'reason':str(e)});continue
   valid+=1;unique.add(tuple(sorted(t['worker'] for t in p['tasks'])))
  counts.append({'recipe_id':recipe['id'],'valid_channel_variants':valid})
 return {'channel_families':channels,'recipes':counts,'valid_recipe_channel_variants':sum(c['valid_channel_variants'] for c in counts),'unique_worker_sets':len(unique),'invalid_variants':len(failed),'invalid_examples':failed[:10],'optional_stage_combinations_included':False,'note':'Finite declared recipes × nonempty channel subsets, not all worker subsets, content variants or proven synergies. Budget, permissions, actual fit and tools still require review.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--skills-root',required=True);ap.add_argument('--recipes',required=True);ap.add_argument('--job');ap.add_argument('--extra-registry');ap.add_argument('--count',action='store_true');ap.add_argument('--output');a=ap.parse_args()
 try:
  reg=discover(a.skills_root);rec=read(a.recipes)
  if a.extra_registry:reg=augment(reg,read(a.extra_registry),installed_names(a.skills_root))
  result=combinations(reg,rec) if a.count else compile_plan(reg,rec,read(a.job))
 except (ValueError,TypeError,KeyError,OSError) as e:result={'planning_status':'review','reason':str(e)}
 out=json.dumps(result,ensure_ascii=False,indent=2)
 if a.output:Path(a.output).write_text(out+'\n')
 else:print(out)
 if result.get('planning_status')=='review':raise SystemExit(2)
if __name__=='__main__':main()
