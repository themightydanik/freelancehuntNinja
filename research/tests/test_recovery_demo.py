import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'demos'))
from bot_recovery_demo import new_state,receive,repair,diagnose,rehearse,digest

class RecoveryDemoTests(unittest.TestCase):
    def test_failure_is_observable(self):
        s=new_state();self.assertEqual(receive(s,{'update_id':1,'type':'callback_query'}),'filtered_before_handler')
        self.assertEqual(s['synthetic_effects'],[]);self.assertTrue(diagnose(s)['supported'])
    def test_repair_and_duplicate(self):
        s=new_state();repair(s);u={'update_id':1,'type':'callback_query'}
        self.assertEqual(receive(s,u),'accepted_locally');self.assertEqual(receive(s,u),'duplicate_skipped')
        self.assertEqual(len(s['synthetic_effects']),1)
    def test_rollback_does_not_mutate_snapshot(self):
        s=new_state();snap=copy.deepcopy(s);repair(s)
        self.assertNotEqual(digest(s),digest(snap));self.assertEqual(snap['allowed_updates'],['message'])
    def test_full_rehearsal(self):
        r=rehearse();self.assertTrue(r['rollback_exact'] and r['final_recovered'])
        self.assertEqual(r['real_messages'],0);self.assertEqual(r['network_calls'],0)

if __name__=='__main__':unittest.main()
