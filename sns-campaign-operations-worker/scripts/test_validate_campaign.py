#!/usr/bin/env python3
"""Synthetic regression tests. No network, platform publishing or live approvals."""
import copy,json,unittest
from pathlib import Path
from validate_campaign import validate
BASE=Path(__file__).resolve().parents[1]
EX=json.loads((BASE/'assets/example-campaign.json').read_text())
def sample():return copy.deepcopy(EX)
def ready():
    d=sample()
    for p in d['posts']:
        p['publication_status']='ready';p['qa_status']='passed'
        p['length_check']={'status':'passed','evidence':'Synthetic fixture only; no actual X parser execution.'}
        for a in p['asset_specs']:a['status']='available'
        for f in p['feature_checks']:f.update(status='confirmed',evidence='Synthetic fixture, not live verification.')
    return d
class CampaignTests(unittest.TestCase):
    def test_complete_draft(self):self.assertTrue(validate(sample(),require_posts=True)['valid'])
    def test_bootstrap(self):self.assertTrue(validate(json.loads((BASE/'assets/campaign-template.json').read_text()))['valid'])
    def test_ready_fixture(self):self.assertTrue(validate(ready())['valid'])
    def test_missing_field(self):
        d=sample();del d['posts'][0]['body_or_script'];self.assertFalse(validate(d)['valid'])
    def test_wrong_type(self):
        d=sample();d['posts'][0]['revision']=True;self.assertFalse(validate(d)['valid'])
    def test_dangling_claim(self):
        d=sample();d['posts'][0]['claim_ids']=['absent'];self.assertFalse(validate(d)['valid'])
    def test_dangling_atom(self):
        d=sample();d['posts'][0]['source_atom_ids']=['absent'];self.assertFalse(validate(d)['valid'])
    def test_duplicate_id(self):
        d=sample();d['posts'].append(copy.deepcopy(d['posts'][0]));self.assertFalse(validate(d)['valid'])
    def test_wrong_timezone(self):
        d=sample();d['posts'][0]['timezone']='UTC';self.assertFalse(validate(d)['valid'])
    def test_invalid_timezone(self):
        d=sample();d['timezone']='invalid/tz';self.assertFalse(validate(d)['valid'])
    def test_missing_channel_package(self):
        d=sample();d['posts'].pop();self.assertFalse(validate(d)['valid'])
    def test_stale_brief(self):
        d=sample();d['jobs'][0]['brief_version']=99;self.assertFalse(validate(d)['valid'])
    def test_unobserved_verified_source(self):
        d=sample();d['claim_ledger'][0]['status']='verified';self.assertFalse(validate(d)['valid'])
    def test_ready_unresolved_claim(self):
        d=ready();d['claim_ledger'][0]['status']='unknown';self.assertFalse(validate(d)['valid'])
    def test_ready_missing_asset(self):
        d=ready();d['posts'][0]['asset_specs'][0]['status']='requested';self.assertFalse(validate(d)['valid'])
    def test_ready_x_unverified_length(self):
        d=ready();d['posts'][1]['length_check']['status']='unverified';self.assertFalse(validate(d)['valid'])
    def test_ready_unverified_feature(self):
        d=ready();d['posts'][0]['feature_checks'][0]['status']='unverified';self.assertFalse(validate(d)['valid'])
    def test_missing_execution_receipt(self):
        d=ready();d['posts'][0]['publication_status']='published';self.assertFalse(validate(d)['valid'])
    def test_version_scope_mismatch(self):
        d=ready();p=d['posts'][0];p['publication_status']='published'
        p['execution_receipt']={'receipt_id':'synthetic','account_id':'example','channel':p['channel'],'content_id':p['content_id'],'revision':1}
        d['permissions']['publish']=True;d['permissions']['scope']=[{'action':'publish','account_id':'example','channel':p['channel'],'content_id':p['content_id'],'revision':2,'publish_at':None}]
        self.assertFalse(validate(d)['valid'])
    def test_no_publish_permission(self):
        d=ready();p=d['posts'][0];p['publication_status']='published'
        p['execution_receipt']={'receipt_id':'synthetic','account_id':'example','channel':p['channel'],'content_id':p['content_id'],'revision':1}
        d['permissions']['scope']=[{'action':'publish','account_id':'example','channel':p['channel'],'content_id':p['content_id'],'revision':1,'publish_at':None}]
        self.assertFalse(validate(d)['valid'])
    def test_bad_datetime(self):
        d=sample();d['posts'][0]['publish_at']='tomorrow';self.assertFalse(validate(d)['valid'])
if __name__=='__main__':unittest.main(verbosity=2)
