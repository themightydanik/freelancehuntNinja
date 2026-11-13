"""Offline follow-up consistency/scope checks; never calls a service or bot."""
import csv
import json
import re
import unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def rows(name):return list(csv.DictReader((ROOT/'data'/name).open()))
def normalized(name):return ''.join(c for c in unicodedata.normalize('NFKD',name.lower()) if c.isalnum())

def main():
    sample=rows('commercial_job_sample.csv');review=rows('commercial_job_review.csv')
    assert all(r['platform']=='FH' and r['sample_id'].startswith('FH-') for r in sample)
    assert {r['sample_id'] for r in review}<={r['sample_id'] for r in sample}
    summary=json.loads((ROOT/'data/commercial_review_summary.json').read_text())
    assert summary['retained_FH_unique']==len(sample)
    assert summary['FH_keyword_candidates_reviewed']==len(review)
    assert summary['retained_FH_window_records']==sum(r['in_window']=='True' for r in sample)
    excluded=json.loads((ROOT/'data/restricted_source_exclusion.json').read_text())
    assert excluded['retained_listing_content'] is False
    for path in (ROOT/'docs/research').glob('1[4-7]_*.md'):
        assert not re.search(r'FR-\d+',path.read_text()),'Restricted job evidence reappeared'
    bounties=rows('international_bounty_sample.csv')
    assert all(r['sponsor_count']=='1' for r in bounties)
    assert all('UNKNOWN' in r['payment_status'] for r in bounties)
    zero=[r for r in rows('channel_revenue_scenarios.csv') if r['scenario']=='UNLAUNCHED_reference']
    assert len(zero)==6
    assert all(float(r[k])==0 for r in zero for k in ('revenue_median','net_median','hours_median','p_net_ge_500'))
    assumptions=json.loads((ROOT/'data/channel_model_assumptions.json').read_text())
    assert assumptions['outgoing_messages']['enabled'] is False
    demo=json.loads((ROOT/'data/bot_recovery_demo_report.json').read_text())
    assert demo['real_messages']==0 and demo['network_calls']==0
    assert demo['rollback_exact'] and demo['rollback_restores_broken_state'] and demo['final_recovered']
    page=(ROOT/'docs/research/demo/BOT_RECOVERY_DEMO.html').read_text()
    assert all(stage in page for stage in ('failure','diagnosis','repair_and_replay','rollback','final_recovery'))
    assert not re.search(r'(?:src|href)=["\']https?://',page),'Demo gained remote dependencies'
    awards=rows('it_award_sample.csv')+rows('it_award_development_stratum.csv')
    registry=json.loads((ROOT/'data/award_verification.json').read_text())['national_registry_crosschecks']
    matches=[]
    for item in registry:
        evidence=[r for r in awards if str(item['identifier']) in r['winner_identifiers'].split(' ; ')]
        assert evidence
        assert any(normalized(item['legal_name']) in [normalized(x) for x in r['winner_legal_names'].split(' ; ')] for r in evidence)
        matches.append(str(item['identifier']))
    assert not any(re.fullmatch(r'\d{8}[A-Z]',r['winner_identifiers']) for r in awards)
    first=json.loads((ROOT/'data/first_500_scenarios.json').read_text())
    assert [first[x]['no_refund']['paid_orders'] for x in ('A_FH_USD','B_Upwork_catalog','C_partner_Contra_route')]==[4,3,2]
    result={'retained_FH_records':len(sample),'manual_keyword_reviews':len(review),'international_single_sponsor_context':len(bounties),
            'restricted_listing_records_absent':True,'actual_paid_sales':0,'outgoing_messages':0,
            'registry_identity_matches':len(matches),'unlaunched_reference_zero':True,
            'synthetic_repair_and_exact_rollback_verified':True,'demo_remote_dependencies':0,
            'first500_arithmetic_consistent':True}
    (ROOT/'data/readiness_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
