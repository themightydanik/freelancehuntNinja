#!/usr/bin/env python3
"""Research-integrity and arithmetic checks, not demand validation."""
from pathlib import Path
import csv,json,re,math
R=Path(__file__).resolve().parents[1];D=R/'data'
def read(n):
 with (D/n).open(newline='') as f:return list(csv.DictReader(f))
e=read('evidence_registry.csv');ids={x['evidence_id'] for x in e};assert len(ids)==len(e)==126
for x in e:
 assert x['url'].startswith('https://') and x['checked_date']=='2026-11-13'
 assert x['type'] and x['limitations'] and x['own_collected_revenue']=='UNKNOWN'
assert len(read('partners.csv'))==22
assert len(read('mobile_niches.csv'))==len(read('extension_ideas.csv'))==len(read('plugin_opportunities.csv'))==15
c=read('candidate_comparison.csv');assert len(c)==15 and sum(x['verdict']=='EXPERIMENT_ONLY' for x in c)==1
for x in c:assert set(x['evidence_ids'].split(';'))<=ids
for x in read('mobile_niches.csv'):assert set(filter(None,x['supporting_evidence_ids'].split(';')))<=ids
for p in R.glob('*.md'):
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if not target.startswith(('http:','https:','#')):assert (p.parent/target.split('#')[0]).exists(),(p,target)
 for id_ in re.findall(r'\b(?:[MPXGRA]\d{2}|S\d{2})\b',p.read_text()):assert id_ in ids,(p,id_)
required=['00_EXECUTIVE_COMPARISON.md','01_PARTNER_DISTRIBUTION.md','02_MOBILE_APPS.md','03_CHROME_EXTENSIONS.md','04_PLUGINS_AND_ECOSYSTEMS.md','05_ADVERTISING_ECONOMICS.md','06_SUBSCRIPTION_ECONOMICS.md','07_DISTRIBUTION_REALITY.md','08_HYBRID_OPPORTUNITIES.md','09_RED_TEAM.md','10_FINALISTS.md','11_FIRST_MARKET_EXPERIMENT.md']
assert all((R/x).exists() for x in required)
f=read('financial_thresholds.csv');assert len(f)==18
for x in f:
 assert float(x['recognized_monthly_gross'])>=int(x['target_gross'])
 assert abs(float(x['contribution'])-float(x['owner_labor'])-float(x['economic_profit_before_tax_fx_acquisition']))<.011
 assert x['actual_collected_revenue']=='UNKNOWN'
choose=lambda model,next_target=2000:next(x for x in f if x['model']==model and int(x['target_gross'])==next_target)
assert int(choose('MOBILE_SUB')['customers_or_active_annual_licenses'])==401
assert int(choose('CHROME_SUB')['customers_or_active_annual_licenses'])==400
assert int(choose('PLUGIN_FREEMIUM')['customers_or_active_annual_licenses'])==490
assert float(choose('B2B_FIXED')['economic_profit_before_tax_fx_acquisition'])==152.55
assert float(choose('PLUGIN_FREEMIUM')['all_customers_billed_now_cash'])>float(choose('PLUGIN_FREEMIUM')['conditional_cash_monthly_equivalent'])*11
ads=read('advertising_thresholds.csv');assert len(ads)==108
for x in ads:
 assert int(x['delivered_impressions_month'])>=float(x['target_publisher_revenue'])*1000/float(x['assumed_net_ecpm'])
 assert int(x['required_mau'])>=int(x['required_dau'])
assert len(read('conversion_thresholds.csv'))==45
assert len(read('retention_sensitivity.csv'))==16
assert len(read('economics_sensitivity.csv'))==72
result=json.loads((D/'demo_result.json').read_text())
assert result['equal_pair']['status']=='PASS'
assert result['omitted_refund']['status']=='FAIL'
assert result['different_definition']['status']=='BLOCKED_DEFINITION'
assert all(result[k]['status']=='BLOCKED_DATA' for k in ['duplicate','mixed_currency','missing_timezone'])
summary=dict(status='PASS',partners=22,mobile=15,extensions=15,plugins=15,evidence_records=126,red_team=15,build_ready_products=0,experiment_candidates=1,financial_models=7,financial_rows=18,ad_sensitivity_rows=108,limitations='Checks verify integrity and arithmetic, not demand, source truth, bank payout or production reliability')
(D/'validation_result.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
