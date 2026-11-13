import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'probes'))
from policy_pages import fetch as fetch_old_policy
from readiness_policies import fetch as fetch_new_policy

class PermissionTests(unittest.TestCase):
    def test_restricted_domain_is_not_requested(self):
        with patch('requests.get',side_effect=AssertionError('No network allowed here')) as get:
            for fetch in (fetch_old_policy,fetch_new_policy):
                r=fetch({'id':'restricted-test','url':'https://www.freelancer.com/feesandcharges'})
                self.assertEqual(r['status'],'not_requested')
            get.assert_not_called()
    def test_manual_only_source_is_not_requested(self):
        with patch('requests.get',side_effect=AssertionError('No network allowed here')) as get:
            r=fetch_new_policy({'id':'manual','url':'https://example.com/policy','automation_gate':'manual_owner_review_only'})
            self.assertEqual(r['status'],'not_requested');get.assert_not_called()

if __name__=='__main__':unittest.main()
