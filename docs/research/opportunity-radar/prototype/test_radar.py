import unittest
from datetime import datetime, timezone
from radar import run

NOW = datetime(2026, 11, 14, tzinfo=timezone.utc)

def payload(status='active', deadline='2026-12-01T00:00:00Z'):
    return {'releases':[{'id':'1','ocid':'a','date':'2026-11-12T12:00:00Z','tag':['tender'], 'buyer':{'name':'Example'},'tender':{'title':'Website development','status':status,'tenderPeriod':{'endDate':deadline}},'url':'https://example.org/notice/1','data_mode':'live_minimized'}]}

class RadarTests(unittest.TestCase):
    def test_baseline_and_idempotent_replay(self):
        data=payload(); records,state,_=run([('fts',data)],{},NOW)
        self.assertEqual(records[0]['change'],'baseline_observation')
        records,_,_=run([('fts',data)],state,NOW)
        self.assertEqual(records[0]['change'],'unchanged')
        data['releases'][0]['tender']['title']='Website redesign'
        self.assertEqual(run([('fts',data)],state,NOW)[0][0]['change'],'changed')
    def test_duplicate_and_conflict(self):
        data=payload(); data['releases']*=2
        self.assertEqual(run([('fts',data)],{},NOW)[2]['within_snapshot_duplicates'],1)
        import copy
        conflicting = copy.deepcopy(data['releases'][0])
        conflicting['tender']['title'] = 'Different website scope'
        data['releases'].append(conflicting)
        self.assertEqual(run([('fts',data)],{},NOW)[2]['conflicting_duplicates'],1)
    def test_newly_observed_does_not_mean_new_business(self):
        data = payload()
        _, state, _ = run([('fts', data)], {}, NOW)
        data['releases'][0]['id'] = '2'
        r = run([('fts', data)], state, NOW)[0][0]
        self.assertEqual(r['change'], 'newly_observed')
        self.assertEqual(r['event'], 'procurement_notice')
        self.assertFalse(r['outreach_ready'])
    def test_closed_and_expired_not_ready(self):
        for data in [payload('complete'),payload(deadline='2026-11-01T00:00:00Z')]:
            r=run([('fts',data)],{},NOW)[0][0]
            self.assertEqual(r['demand_class'],'false_positive')
            self.assertFalse(r['outreach_ready'])
    def test_fixture_is_never_live(self):
        data={'data_mode':'synthetic_fixture','items':[{'company_number':'X','company_name':'SYNTHETIC','date_of_creation':'2026-11-12'}]}
        r,_,m=run([('companies_house',data)],{},NOW)
        self.assertEqual(m['live_records'],0)
        self.assertEqual(r[0]['quality_score'],0)
    def test_notice_is_not_contact_permission(self):
        r=run([('fts',payload())],{},NOW)[0][0]
        self.assertEqual(r['demand_class'],'confirmed_demand')
        self.assertFalse(r['contact_permission'])
        self.assertFalse(r['outreach_ready'])

if __name__=='__main__':unittest.main()
