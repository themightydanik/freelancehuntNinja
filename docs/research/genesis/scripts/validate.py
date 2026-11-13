#!/usr/bin/env python3
"""Validate research integrity and financial thresholds without network."""
from pathlib import Path
import csv,json,re,math
R=Path(__file__).resolve().parents[1];D=R/'data'
def read(n):
 with (D/n).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
e=read('evidence_registry.csv');ids={r['evidence_id'] for r in e};assert len(ids)==55
for row in e:
 assert row['url'].startswith('https://') and row['checked_date']=='2026-11-13'
 assert row['limitations'] and row['evidence_type'] and row['independence_group']
 assert row['collected_revenue']=='UNKNOWN'
u=read('opportunity_universe.csv');assert len(u)==45 and len({x['mechanism'] for x in u})==15
s=read('finalist_scorecard.csv');assert len(s)==15
assert len([r for r in s if r['stage'] in ['DEEP','EXPERIMENT_ONLY']])==6
assert len([r for r in s if r['stage']=='EXPERIMENT_ONLY'])==1
weights=[.20,.25,.15,.15,.10,.10,.05]
for row in s:
 vs=[int(row[k]) for k in ['spending','distribution','advantage','economics','speed','technical','scale']]
 assert all(0<=v<=5 for v in vs)
 assert abs(float(row['weighted_score'])-sum(a*b for a,b in zip(vs,weights)))<.0051
for filename in ['opportunity_universe.csv','finalist_scorecard.csv','competitor_comparison.csv','distribution_channels.csv']:
 for row in read(filename):
  for key in ['evidence_id','evidence_ids']:
   if key in row:assert set(filter(None,row[key].split(';')))<=ids,(filename,row)
a=read('competitor_comparison.csv')
for cid in ['C01','C02','C03','C04','C05','C06']:assert sum(x['candidate_id']==cid for x in a)>=3
for p in R.glob('*.md'):
 for match in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if not match.startswith(('https://','http://','#')):assert (p.parent/match.split('#')[0]).exists(),(p,match)
 for eid in re.findall(r'\bE\d{2}\b',p.read_text()):assert eid in ids,(p,eid)
for name in ['00_EXECUTIVE_VERDICT.md','01_MONEY_FLOW_MAP.md','02_DISCOVERY_UNIVERSE.md','03_HIDDEN_OPPORTUNITIES.md','04_EXISTING_SPENDING_EVIDENCE.md','05_DISTRIBUTION_REALITY.md','06_COMPETITIVE_ALTERNATIVES.md','07_UNIT_ECONOMICS.md','08_RED_TEAM.md','09_FINALISTS.md','10_FIRST_REVENUE_EXPERIMENTS.md','11_BUILD_OR_KILL_DECISION.md']:assert (R/name).exists()
rows=read('unit_economics.csv');c01=next(x for x in rows if x['candidate_id']=='C01')
assert float(c01['gross_revenue'])==2000
assert float(c01['contribution_after_direct_fixed'])==1554.01
assert float(c01['owner_total_h'])==66
assert float(c01['economic_profit_before_tax_fx'])==-95.99
for r in rows:
 assert abs(float(r['contribution_after_direct_fixed'])-float(r['owner_labor_value'])-float(r['economic_profit_before_tax_fx']))<.011
 assert r['actual_net_after_tax']=='UNKNOWN'
g=read('budget_time_scenarios.csv');assert len(g)==216
assert {(int(x['budget_usd']),int(x['hours_per_month']),int(x['day'])) for x in g}=={(b,h,d) for b in [0,100,300,1000] for h in [40,80,120] for d in [30,90,180]}
assert json.loads((D/'demo_result.json').read_text())['equal_pair_control']=='PASS'
summary={'status':'PASS','evidence':len(e),'discovery':len(u),'categories':15,'red_team_candidates':len(s),'deep_candidates':6,'alternatives':len(a),'budget_time_rows':len(g),'own_payments_observed':0,'build_ready_finalists':0,'experiment_only_finalists':1,'limitations':'Integrity and arithmetic checks; not validation of demand, source truth, account KYC or payout'}
(D/'validation_result.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
