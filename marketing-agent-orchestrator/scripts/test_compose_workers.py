import copy,json,tempfile,unittest
from pathlib import Path
from compose_workers import discover,compile_plan,combinations,PlanningError,validate_manifest,augment
HERE=Path(__file__).resolve().parents[1]
def worker(name,cap,req=None,phase=0,channels=None):
 return {'schema_version':'2.0','skill_name':name,'role':'worker','provides':[cap],'requires':req or ['brief'],'phase':phase,'channels':channels or [],'conflicts_with':[],'estimated_minutes':None}
class CompositionTests(unittest.TestCase):
 def setUp(self):
  self.reg={'a':worker('a','a'),'b':worker('b','b',['a'],10)}
  self.rec={'recipes':[{'id':'base','required_capabilities':['b'],'final_capabilities':[],'channel_mode':'none'}]}
  self.job={'recipe_id':'base','channels':[]}
 def test_ephemeral_registered_worker(self):
  updated=augment(self.reg,{'workers':[worker('new','new_cap')]},{'a','b','new'});self.assertIn('new',updated);self.assertNotIn('new',self.reg)
 def test_ephemeral_uninstalled_rejected(self):
  with self.assertRaises(PlanningError):augment(self.reg,{'workers':[worker('fake','fake_cap')]},{'a','b'})
 def test_ephemeral_duplicate_name(self):
  with self.assertRaises(PlanningError):augment(self.reg,{'workers':[worker('a','new_cap')]},{'a','b'})
 def test_dependencies(self):
  p=compile_plan(self.reg,self.rec,self.job);self.assertEqual(p['parallel_groups'],[['a'],['b']]);self.assertEqual(p['execution_status'],'not_started')
 def test_missing(self):
  del self.reg['a']
  with self.assertRaises(PlanningError):compile_plan(self.reg,self.rec,self.job)
 def test_ambiguous(self):
  self.reg['alt']=worker('alt','a')
  with self.assertRaises(PlanningError):compile_plan(self.reg,self.rec,self.job)
 def test_override(self):
  self.reg['alt']=worker('alt','a');self.job['provider_overrides']={'a':'alt'}
  self.assertEqual(compile_plan(self.reg,self.rec,self.job)['parallel_groups'][0],['alt'])
 def test_invalid_override(self):
  self.job['provider_overrides']={'a':'b'}
  with self.assertRaises(PlanningError):compile_plan(self.reg,self.rec,self.job)
 def test_reuse(self):
  self.job['available_capabilities']={'a':'artifact-a:2'}
  self.assertEqual(compile_plan(self.reg,self.rec,self.job)['parallel_groups'],[['b']])
 def test_reuse_requires_id(self):
  self.job['available_capabilities']={'a':None}
  with self.assertRaises(PlanningError):compile_plan(self.reg,self.rec,self.job)
 def test_cycle(self):
  self.reg['a']['requires']=['b']
  with self.assertRaises(PlanningError):compile_plan(self.reg,self.rec,self.job)
 def test_phase_cycle(self):
  self.reg['a']['phase']=20
  with self.assertRaises(PlanningError):compile_plan(self.reg,self.rec,self.job)
 def test_conflict(self):
  self.reg['a']['conflicts_with']=['b']
  with self.assertRaises(PlanningError):compile_plan(self.reg,self.rec,self.job)
 def test_new_capability_without_recipe_edit(self):
  self.reg['new']=worker('new','new_cap',phase=10);self.job['extra_capabilities']=['new_cap']
  self.assertIn('new',[t['worker'] for t in compile_plan(self.reg,self.rec,self.job)['tasks']])
 def test_unknown_estimates(self):
  self.assertIn('time_estimates_missing',compile_plan(self.reg,self.rec,self.job)['resource_review'])
 def test_time_cap(self):
  self.job.update(time_cap_minutes=1,worker_estimates={'a':10,'b':10})
  p=compile_plan(self.reg,self.rec,self.job);self.assertEqual(len(p['tasks']),2);self.assertIn('known_work_exceeds_time_cap',p['resource_review'])
 def test_nan_time(self):
  self.job['worker_estimates']={'a':float('nan')}
  with self.assertRaises(PlanningError):compile_plan(self.reg,self.rec,self.job)
 def test_negative_time(self):
  self.job['time_cap_minutes']=-1
  with self.assertRaises(PlanningError):compile_plan(self.reg,self.rec,self.job)
 def test_unknown_recipe(self):
  self.job['recipe_id']='unknown'
  with self.assertRaises(PlanningError):compile_plan(self.reg,self.rec,self.job)
 def test_invalid_role(self):
  with self.assertRaises(PlanningError):validate_manifest(worker('a','a')|{'role':'orchestrator'},'a')
 def test_discovery_named_and_id_folder(self):
  with tempfile.TemporaryDirectory() as td:
   for folder,name in [('a','a'),('skill-id','b')]:
    p=Path(td)/folder;(p/'assets').mkdir(parents=True);(p/'SKILL.md').write_text('---\nname: '+name+'\ndescription: test\n---\n');(p/'assets/worker-capability.json').write_text(json.dumps(worker(name,name)))
   self.assertEqual(set(discover(td)),{'a','b'})
 def test_installed_complete_and_unique(self):
  reg=discover(HERE.parent);rec=json.loads((HERE/'assets/combination-recipes.json').read_text());c=combinations(reg,rec)
  expected=json.loads((HERE/'assets/worker-registry.example.json').read_text())['workers'];self.assertTrue({m['skill_name'] for m in expected}<=set(reg));c=combinations({m['skill_name']:m for m in expected},rec);self.assertEqual(c['invalid_variants'],0);self.assertEqual(c['valid_recipe_channel_variants'],2044)
 def test_channel_group_and_future_channel(self):
  reg={m['skill_name']:m for m in json.loads((HERE/'assets/worker-registry.example.json').read_text())['workers']};rec=json.loads((HERE/'assets/combination-recipes.json').read_text())
  p=compile_plan(reg,rec,{'recipe_id':'developer_launch','channels':['x','youtube']})
  channel_group=[g for g in p['parallel_groups'] if 'sns-x-worker' in g][0];self.assertIn('sns-youtube-worker',channel_group)
  reg['future-worker']=worker('future-worker','channel_package:future',['message_strategy','channel_strategy'],70,['future'])
  c=combinations(reg,rec);self.assertEqual(c['valid_recipe_channel_variants'],4092);self.assertEqual(c['invalid_variants'],0)
 def test_required_channel(self):
  self.rec['recipes'][0]['channel_mode']='required'
  with self.assertRaises(PlanningError):compile_plan(self.reg,self.rec,self.job)
 def test_duplicate_channels(self):
  self.job['channels']=['x','x']
  with self.assertRaises(PlanningError):compile_plan(self.reg,self.rec,self.job)
if __name__=='__main__':unittest.main()
