"""Offline analysis of retained permitted-source evidence. Never pools currencies.
Freelancer listing records are excluded, not used to estimate demand or prices.
"""
import csv
import json
import statistics
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
RELEVANT={'bounded_deployment_candidate','adjacent_large','bounded_api_candidate','adjacent_hourly'}

def main():
    samples=list(csv.DictReader((ROOT/'data/commercial_job_sample.csv').open()))
    reviews=list(csv.DictReader((ROOT/'data/commercial_job_review.csv').open()))
    byid={r['sample_id']:r for r in samples}
    assert all(r['platform']=='FH' for r in samples),'Restricted listing records must not be retained'
    assert all(r['sample_id'] in byid for r in reviews)
    selected=[r for r in reviews if r['review_label'] in RELEVANT]
    groups={}
    for label in sorted({r['review_label'] for r in reviews}):
        rows=[byid[r['sample_id']] for r in reviews if r['review_label']==label]
        budgets={}
        for row in rows:
            if row['budget_min']:
                budgets.setdefault((row['currency'],row['project_type']),[]).append(float(row['budget_min']))
        bids=[int(r['bids_snapshot']) for r in rows if r['bids_snapshot']]
        groups[label]={'records':len(rows),'missing_budget':sum(not r['budget_min'] for r in rows),
                       'budget_groups':[{'currency':c,'type':t,'n':len(v),'min':min(v),'median':statistics.median(v),'max':max(v)} for (c,t),v in budgets.items()],
                       'bids_snapshot':{'n':len(bids),'min':min(bids),'median':statistics.median(bids),'max':max(bids)} if bids else None}
    bounties=list(csv.DictReader((ROOT/'data/international_bounty_sample.csv').open()))
    rewards=[float(r['advertised_reward_usd']) for r in bounties if r['advertised_reward_usd']]
    out={'retained_FH_unique':len(samples),'retained_FH_window_records':sum(r['in_window']=='True' for r in samples),
         'FH_keyword_candidates_reviewed':len(reviews),'FH_adjacent_existing_repair_deploy_migration_records':len(selected),
         'strict_existing_telegram_recovery_found':sum(r['strict_existing_telegram_recovery'].lower()=='true' for r in reviews),
         'FH_groups':groups,'international_bounty_context':{'sample_size':len(bounties),'one_sponsor_only':True,
            'advertised_USD_reward':{'n':len(rewards),'min':min(rewards),'median':statistics.median(rewards),'max':max(rewards)},
            'state_counts':dict(Counter(r['state'] for r in bounties)),'not_Telegram_recovery':True},
         'restricted_source':'Freelancer listing records removed and not used; see restricted_source_exclusion.json',
         'price_inference':'Bot Recovery accepted-price range UNKNOWN; adjacent budgets and one-sponsor rewards are not comparable transaction prices',
         'limits':['non-random active-only FH sample','single-sponsor international context','keyword false negatives possible',
                   'single manual reviewer, excerpt-limited','different project IDs do not prove independent buyers',
                   'buyer geography UNKNOWN; platform or currency does not establish residence','no sales or account/payout tests']}
    (ROOT/'data/commercial_review_summary.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
