"""Exhaustive integer portfolio grid with explicit assumed demand caps.
Not a sales forecast; optimize cash contribution, plus opportunity cost report.
"""
import itertools
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PRODUCTS=[
 {'id':'P01','name':'Bot recovery','price':350,'hours':8,'support':1,'build':12,'cash':1,'cap':3,'dependency':'ops'},
 {'id':'P02','name':'WooCommerce connector','price':500,'hours':12,'support':1,'build':20,'cash':2,'cap':3,'dependency':'events'},
 {'id':'P03','name':'RLS review','price':450,'hours':10,'support':.5,'build':10,'cash':0,'cap':2,'dependency':'security'},
 {'id':'P04','name':'Webhook replay','price':600,'hours':14,'support':1,'build':16,'cash':1,'cap':2,'dependency':'events'},
 {'id':'P05','name':'Kit license','price':49,'hours':.25,'support':.25,'build':24,'cash':.5,'cap':10,'dependency':'ops'},
]

def optimize(capacity=120,budget=10,fee=.1,reuse=True,caps=True,security_review_ready=False):
    best=None
    for units in itertools.product(*[range(p['cap']+1 if caps else 11) for p in PRODUCTS]):
        if units[2] and not security_review_ready:
            continue  # Do not sell a security review on unverified competence alone.
        active=[p for p,u in zip(PRODUCTS,units) if u]
        # Shared setup is paid once per primitive, in addition to offer-specific build.
        shared=6*len({p['dependency'] for p in active}) if reuse else 6*len(active)
        build=shared+sum(p['build'] for p in active)
        if build>70: continue  # 6-week launch budget, amortized over 6 months below
        run_hours=sum(u*(p['hours']+p['support']) for p,u in zip(PRODUCTS,units))
        hours=24+build/6+run_hours
        cash=sum(u*p['cash'] for p,u in zip(PRODUCTS,units))+2
        if hours>capacity or cash>budget:continue
        gross=sum(u*p['price'] for p,u in zip(PRODUCTS,units))
        net=gross*.97*(1-fee)-cash
        if best is None or net>best['monthly_contribution']:
            best={'units':dict(zip([p['id'] for p in PRODUCTS],units)),'monthly_gross':gross,
                  'monthly_contribution':round(net,2),'hours':round(hours,2),'cash_cost':cash,
                  'launch_build_hours':build,'economic_profit_at_20_per_hour':round(net-20*hours,2),
                  'contribution_per_hour':round(net/hours,2),'demand_caps_assumed':caps}
    return best

def main():
    results={'status':'ESTIMATED optimization under ASSUMED prices, demand caps, reuse and workload',
             'products':PRODUCTS,'base':optimize(),'no_reuse':optimize(reuse=False),
             'with_security_qualification':optimize(security_review_ready=True),
             'fee20':optimize(fee=.2),'fee30':optimize(fee=.3),'capacity80':optimize(capacity=80),
             'relaxed_demand_caps_warning':optimize(caps=False)}
    (ROOT/'data/portfolio_results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__': main()
