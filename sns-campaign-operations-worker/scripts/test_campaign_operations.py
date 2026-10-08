import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from campaign_operations import check_operations,payload_hash,snapshot,CHECKS

class OperationsTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.c=json.loads((Path(__file__).parent.parent/'assets/example-campaign.json').read_text())
        self.o={'operations_version':'1.0','campaign_id':self.c['campaign_id'],'assets':[],'production_tasks':[],'preflight':[],'events':[],'change_requests':[]}
    def tearDown(self):self.temp.cleanup()
    def errors(self):return check_operations(self.c,self.o,self.root)
    def asset(self):
        f=self.root/'card.txt';f.write_text('synthetic test card')
        self.o['assets']=[{'asset_id':'S1','content_id':'P1','revision':1,'status':'provided','path':'card.txt','sha256':hashlib.sha256(f.read_bytes()).hexdigest()}]
    def active(self):
        self.asset();p=self.c['posts'][0];p['publication_status']='ready'
        self.o['preflight']=[{'content_id':'P1','revision':1,'channel':'instagram','surface':'carousel','account':'synthetic-test-only','checked_at':'2026-10-08T12:00:00+09:00','payload_sha256':payload_hash(p),'asset_hashes':{'S1':self.o['assets'][0]['sha256']},'checks':[{'name':n,'status':'passed','evidence':'synthetic unit fixture, not live verification','method':'fixture'} for n in CHECKS]}]
    def test_empty_draft(self):self.assertEqual(self.errors(),[])
    def test_missing_arrays(self):del self.o['events'];self.assertTrue(self.errors())
    def test_wrong_campaign(self):self.o['campaign_id']='other';self.assertTrue(self.errors())
    def test_provided_asset(self):self.asset();self.assertEqual(self.errors(),[])
    def test_file_changed(self):self.asset();(self.root/'card.txt').write_text('changed');self.assertTrue(self.errors())
    def test_missing_file(self):self.asset();(self.root/'card.txt').unlink();self.assertTrue(self.errors())
    def test_generation_receipt(self):self.asset();self.o['assets'][0]['status']='generated';self.assertTrue(self.errors())
    def test_stale_asset_revision(self):self.asset();self.o['assets'][0]['revision']=2;self.assertTrue(self.errors())
    def test_duplicate_asset(self):self.asset();self.o['assets']*=2;self.assertTrue(self.errors())
    def test_ready_missing_preflight(self):self.c['posts'][0]['publication_status']='ready';self.assertTrue(self.errors())
    def test_full_preflight_fixture(self):self.active();self.assertEqual(self.errors(),[])
    def test_changed_copy(self):self.active();self.c['posts'][0]['body_or_script']='changed';self.assertTrue(self.errors())
    def test_changed_account_surface(self):self.active();self.o['preflight'][0]['surface']='reels';self.assertTrue(self.errors())
    def test_wrong_execution_account(self):
        self.active();p=self.c['posts'][0];p['publication_status']='published';p['execution_receipt']={'account_id':'different-account'};self.assertTrue(self.errors())
    def test_unknown_check(self):self.active();self.o['preflight'][0]['checks'][0]['status']='unknown';self.assertTrue(self.errors())
    def test_missing_check(self):self.active();self.o['preflight'][0]['checks'].pop();self.assertTrue(self.errors())
    def test_na_cannot_skip_semantics(self):
        self.active();c=next(x for x in self.o['preflight'][0]['checks'] if x['name']=='semantic');c.update(status='not_applicable',reason='skip');self.assertTrue(self.errors())
    def test_completed_task_without_asset(self):
        self.o['production_tasks']=[{'task_id':'T1','content_id':'P1','revision':1,'brief_version':1,'owner_skill':'imagegen','status':'completed','asset_ids':[]}];self.assertTrue(self.errors())
    def test_unknown_event_needs_followup(self):
        self.o['events']=[{'event_id':'E1','content_id':'P1','revision':1,'action':'publish','outcome':'unknown','observed_at':'2026-10-08T12:00:00+09:00'}];self.assertTrue(self.errors())
    def test_success_event_needs_receipt(self):
        self.o['events']=[{'event_id':'E1','content_id':'P1','revision':1,'action':'publish','outcome':'succeeded','observed_at':'2026-10-08T12:00:00+09:00'}];self.assertTrue(self.errors())
    def test_change_requires_observation_or_plan(self):
        self.o['change_requests']=[{'content_id':'P1','from_revision':1,'observation_ids':[],'decision':'modify','variable':'hook','rationale':'hypothesis','next_owner':'sns-x-worker','decision_rule':'collect actual response','review_window':'7 days'}];self.assertTrue(self.errors());self.o['change_requests'][0]['status']='planned';self.assertEqual(self.errors(),[])
    def test_snapshot_idempotent_and_revision_preserved(self):
        d=self.root/'history';a=snapshot(self.c,self.o,d);self.assertEqual(a,snapshot(self.c,self.o,d));self.c['posts'][0]['revision']=2;b=snapshot(self.c,self.o,d);self.assertNotEqual(a,b);self.assertTrue(a.exists())
    def test_snapshot_refuses_corruption(self):
        d=self.root/'history';a=snapshot(self.c,self.o,d);a.write_text('corrupt');self.assertRaises(ValueError,snapshot,self.c,self.o,d)
if __name__=='__main__':unittest.main()
