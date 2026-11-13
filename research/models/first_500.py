"""Exact conditional invoice arithmetic, not acquisition probabilities or sales.
Prices/cost reserves are test inputs; provider fees still require owner route check.
"""
import json
from pathlib import Path
from channel_revenue_model import invoice_net

ROOT=Path(__file__).resolve().parents[2]
CASES={
 'A_FH_USD':{'price':150,'fee_rate':.09,'payout_flat':5,'direct_per_job':1,'cash_reserve':5},
 'B_Upwork_catalog':{'price':220,'fee_rate':.15,'payout_flat':.99,'direct_per_job':2,'cash_reserve':5},
 'C_partner_Contra_route':{'price':300,'platform_flat':15,'payout_rate':.02,'payout_flat':3,'direct_per_job':2,'cash_reserve':5},
}

def calculate(case,refunds=0):
    params=case.copy();reserve=params.pop('cash_reserve');price=params.pop('price')
    for units in range(max(1,refunds),101):
        net=invoice_net(price,units,**params,refund_amount=refunds*price)-reserve
        if net>=500:
            return {'paid_orders':units,'one_time_price':price,'invoiced':units*price,'full_refunds':refunds,
                    'received_after_refunds':(units-refunds)*price,'conditional_cash_after_fees_direct_reserve':round(net,2),
                    'cash_reserve':reserve,'cost_inputs':params}
    raise ValueError('No solution within100orders')

def main():
    results={key:{'no_refund':calculate(value),'one_full_refund_conservative_fee_retained':calculate(value,1)} for key,value in CASES.items()}
    results['status']='Conditional batch cash after chosen fees/direct reserve, BEFORE tax/FX/unknown onboarding fees; prices unvalidated; zero actual sales'
    results['launch']='Not launched; no messages, accounts, proposals, paid actions or public demo deployment'
    (ROOT/'data/first_500_scenarios.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__':main()
