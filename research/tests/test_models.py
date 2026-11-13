import sys
import unittest
from pathlib import Path
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'models'))
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'probes'))
from revenue_model import simulate,net_receipts,summarize
from portfolio_optimizer import optimize
from state_poc import connect,ingest,identity,reserve

class RevenueTests(unittest.TestCase):
    def test_accounting(self):
        revenue,net=net_receipts(1000,.1,.2,30,5)
        self.assertEqual(revenue,900);self.assertEqual(net,685)
    def test_repeatable(self):
        a=simulate('Base',40,7);b=simulate('Base',40,7)
        np.testing.assert_array_equal(a['revenue'],b['revenue'])
    def test_zero_traffic_no_sales(self):
        r=simulate('Base',100,7,{'impressions':0})
        self.assertEqual(float(r['revenue'].sum()),0)
    def test_zero_success_interval_is_not_zero_width(self):
        r=simulate('Base',100,7,{'impressions':0})
        row=summarize('zero',r)[0]
        self.assertEqual(row['p_month_revenue_ge_2000'],0)
        self.assertGreater(row['mc_95_high'],0)
    def test_zero_capacity_no_fulfillment(self):
        r=simulate('Upside',100,7,{'capacity':0})
        self.assertEqual(float(r['completed'].sum()),0)
        self.assertEqual(float(r['revenue'].sum()),0)
    def test_capacity_conservation(self):
        r=simulate('Upside',300,7)
        self.assertTrue(np.all(r['hours']<=r['capacity_hours']+1e-9))
        self.assertTrue(np.all(r['completed']>=0))
        self.assertTrue(np.all(r['backlog']>=0))
    def test_funnel_counts(self):
        r=simulate('Base',100,7)
        for a,b in [('clicks','impressions'),('qualified','clicks'),('negotiations','qualified'),('proposals','negotiations')]:
            self.assertTrue(np.all(r[a]<=r[b]))
    def test_no_sales_first_month(self):
        r=simulate('Upside',100,7,no_first_month=True)
        self.assertTrue(np.all(r['revenue'][:,0]==0))
    def test_fee_does_not_change_revenue(self):
        a=simulate('Base',100,7);b=simulate('Base',100,7,{'fee':2})
        np.testing.assert_array_equal(a['revenue'],b['revenue'])
        self.assertTrue(np.all(b['net']<=a['net']))
    def test_portfolio_constraints(self):
        r=optimize();self.assertLessEqual(r['hours'],120);self.assertLessEqual(r['cash_cost'],10)
        self.assertLessEqual(r['launch_build_hours'],70)
        self.assertEqual(r['units']['P03'],0)
    def test_fee_reduces_optimum(self):
        self.assertLessEqual(optimize(fee=.3)['monthly_contribution'],optimize(fee=.1)['monthly_contribution'])

class StateTests(unittest.TestCase):
    def test_history_and_idempotence(self):
        db=connect();r={'id':'a','status':'new'}
        ingest(db,'x','1',[r,r]);ingest(db,'x','2',[dict(r,status='changed')])
        self.assertEqual(db.execute('SELECT COUNT(*) FROM versions').fetchone()[0],2)
    def test_atomic_checkpoint(self):
        db=connect();ingest(db,'x','1',[{'id':'a'}])
        with self.assertRaises(RuntimeError):ingest(db,'x','2',[{'id':'b'}],True)
        self.assertEqual(db.execute('SELECT COUNT(*) FROM versions').fetchone()[0],1)
        self.assertEqual(db.execute('SELECT cursor FROM checkpoints').fetchone()[0],'1')
    def test_identity_no_fuzzy_merge(self):
        self.assertIsNone(identity(None,'x'));self.assertNotEqual(identity('UA','001'),identity('UK','001'))
        self.assertEqual(identity('ua-edr',' 001 '),'UA-EDR:001')
    def test_budget_cap(self):
        db=connect();self.assertTrue(reserve(db,.75));self.assertFalse(reserve(db,.5))
        with self.assertRaises(ValueError):reserve(db,-1)

if __name__=='__main__':unittest.main()
