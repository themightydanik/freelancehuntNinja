import sys
import unittest
from pathlib import Path
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'models'))
from channel_revenue_model import CHANNELS,simulate,invoice_net
from first_500 import calculate,CASES

class ChannelModelTests(unittest.TestCase):
    def test_first500_fh_usd(self):
        self.assertAlmostEqual(invoice_net(150,4,.09,payout_flat=5,direct_per_job=1),537)
    def test_first500_upwork_upper_fee(self):
        self.assertAlmostEqual(invoice_net(220,3,.15,payout_flat=.99,direct_per_job=2),554.01)
    def test_first500_white_label_conservative_payer(self):
        self.assertAlmostEqual(invoice_net(300,2,platform_flat=15,payout_rate=.02,payout_flat=3,direct_per_job=2),551.6)
    def test_refund_does_not_erase_nonrefundable_fee(self):
        self.assertAlmostEqual(invoice_net(150,5,.09,payout_flat=5,direct_per_job=1,refund_amount=150),522.5)
    def test_unlaunched_has_no_sales_or_spend(self):
        a,b=simulate('Upside',50,7,launched=False)
        self.assertEqual(float(a['accepted'].sum()),0);self.assertEqual(float(b['revenue'].sum()),0)
        self.assertEqual(float(b['net'].sum()),0);self.assertEqual(float(b['hours'].sum()),0)
    def test_zero_channel_inputs(self):
        a,b=simulate('Upside',50,7,scales=dict.fromkeys(CHANNELS,0))
        self.assertEqual(float(b['revenue'].sum()),0)
    def test_single_owner_capacity(self):
        a,b=simulate('Upside',200,7,capacity=80)
        self.assertTrue(np.all(b['hours']<=80+1e-8))
        self.assertTrue(np.all(a['completed']>=0));self.assertTrue(np.all(a['backlog']>=0))
    def test_small_capacity_has_no_hidden_overhead_clipping(self):
        a,b=simulate('Upside',30,7,capacity=40)
        actual=b['marketing_hours']+b['build_hours']+b['presales_hours']+a['support_hours'].sum(axis=2)+a['delivery_hours'].sum(axis=2)
        np.testing.assert_allclose(actual,b['hours'])
        self.assertTrue(np.all(actual<=40+1e-8))
        with self.assertRaises(ValueError):simulate(capacity=35)
    def test_channel_funnel_conservation(self):
        a,b=simulate('Base',100,7)
        self.assertTrue(np.all(a['clicks'][:,:,:3]<=a['traffic'][:,:,:3]))
        self.assertTrue(np.all(a['qualified'][:,:,:3]<=a['clicks'][:,:,:3]))
        self.assertTrue(np.all(a['proposals']<=a['conversations']))
        self.assertTrue(np.all(a['funded']<=a['accepted']))
    def test_minimum_paid_orders_after_reserve(self):
        self.assertEqual([calculate(CASES[k])['paid_orders'] for k in CASES],[4,3,2])
    def test_refund_stress_needs_one_extra_order(self):
        self.assertEqual([calculate(CASES[k],1)['paid_orders'] for k in CASES],[5,4,3])
    def test_seed_repeatability(self):
        a,b=simulate('Base',20,7);c,d=simulate('Base',20,7)
        np.testing.assert_array_equal(b['net'],d['net'])
    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):simulate(fx_uah_per_usd=0)
        with self.assertRaises(ValueError):simulate(capacity=-1)

if __name__=='__main__':unittest.main()
