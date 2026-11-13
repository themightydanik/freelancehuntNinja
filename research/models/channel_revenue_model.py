"""Channel/market-separated planning model, NOT a calibrated sales forecast.

Zero-launch reference disables every acquisition channel and outgoing messages.
All traffic, conversions, price, workload and lag priors are ASSUMED. Problem,
issue and award counts are NEVER loaded as commercial funnel inputs.
"""
import argparse
import csv
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
CHANNELS=['UA_marketplace','INT_marketplace','organic_website','qualified_direct_inbound','B2B_partner_conversations']
TRAFFIC={
 'Conservative':[(0,120,500),(0,150,600),(0,40,200),(0,.2,1),(0,.2,1)],
 'Base':[(100,700,1800),(200,1000,2500),(0,150,600),(0,1,3),(0,1,3)],
 'Upside':[(400,1500,3000),(1000,3500,7000),(300,1000,2500),(1,3,6),(1,4,8)],
}
PRICES=[(3000,5000,8000),(150,220,350),(150,220,350),(150,250,400),(250,300,600)]
LAGS=[(.55,.4,.05),(.35,.5,.15),(.3,.5,.2),(.45,.45,.1),(.1,.5,.4)]

def invoice_net(price,units,fee_rate=0,platform_flat=0,payout_rate=0,payout_flat=0,direct_per_job=0,refund_amount=0):
    """Deterministic first-$500 illustration; platform flat charged per invoice.
    Percent fee conservatively remains charged on all invoices after a refund.
    """
    gross=price*units
    earned=gross-refund_amount
    before_payout=earned-gross*fee_rate-platform_flat*units
    return before_payout*(1-payout_rate)-payout_flat-direct_per_job*units

def simulate(scenario='Base',runs=5000,seed=20261113,launched=True,scales=None,fx_uah_per_usd=45,capacity=120,int_fee=.15,lag_shift=0):
    if fx_uah_per_usd<=0:raise ValueError('Positive planning FX required; not a fetched quote')
    if runs<=0 or capacity<0 or not 0<=int_fee<=1 or lag_shift not in (0,1,2):raise ValueError('Invalid simulation limits')
    if launched and capacity<40:raise ValueError('Chosen16h build +24h acquisition plan needs40h; use unlaunched reference or revise plan')
    rng=np.random.default_rng(seed);scales=scales or {};k=len(CHANNELS)
    traffic=np.column_stack([rng.triangular(*x,runs) for x in TRAFFIC[scenario]])
    for i,name in enumerate(CHANNELS):traffic[:,i]*=scales.get(name,1)
    growth=rng.triangular(0,.1,.25,runs)
    price=np.column_stack([rng.triangular(*x,runs) for x in PRICES]);price[:,0]/=fx_uah_per_usd
    price*=scales.get('price',1)
    delivery=rng.triangular(4,6,10,(runs,k))*scales.get('delivery_hours',1)
    ctr=rng.triangular(.01,.03,.05,(runs,3))
    qualify=np.clip(rng.triangular(.04,.1,.18,(runs,3))*scales.get('qualification',1),0,1)
    proposal_rate=rng.triangular(.45,.7,.9,(runs,k))
    close=np.clip(rng.triangular(.08,.2,.35,(runs,k))*scales.get('close',1),0,1)
    funded_rate=np.clip(rng.triangular(.65,.85,.98,(runs,k))*scales.get('accepted_to_funded',1),0,1)
    refund=rng.triangular(0,.02,.1,runs)
    attach=rng.triangular(0,.08,.2,(runs,k));churn=rng.triangular(.02,.08,.2,(runs,k))
    due=np.zeros((runs,10,k),dtype=int);backlog=np.zeros((runs,k),dtype=int)
    clients=np.zeros((runs,k),dtype=int);subs=np.zeros((runs,k),dtype=int)
    names=['traffic','clicks','qualified','conversations','proposals','accepted','funded','completed','gross','revenue','net','support_hours','mrr','delivery_hours','backlog']
    out={name:np.zeros((runs,6,k)) for name in names}
    totals={name:np.zeros((runs,6)) for name in ['revenue','net','hours','presales_hours','marketing_hours','build_hours']}
    for month in range(6):
        exposure=rng.poisson(traffic*(1+growth[:,None])**month) if launched else np.zeros((runs,k),dtype=int)
        clicks=np.zeros((runs,k),dtype=int);qualified=np.zeros_like(clicks)
        clicks[:,:3]=rng.binomial(exposure[:,:3],ctr)
        qualified[:,:3]=rng.binomial(clicks[:,:3],qualify)
        # Last two are source-attributed, consented conversations/inquiries, not visits.
        qualified[:,3:]=exposure[:,3:]
        conversations=qualified.copy()
        # A shared 16-hour presales budget; no five independent owner capacities.
        demand=conversations@np.array([.5,.5,.5,.5,1.])
        build_plan=16 if month==0 else 4
        presales_cap=min(16,max(0,capacity-24-build_plan)) if launched else 0
        ratio=np.minimum(1,presales_cap/np.maximum(1,demand))
        conversations=np.floor(conversations*ratio[:,None]).astype(int)
        proposals=rng.binomial(conversations,proposal_rate)
        presales=conversations@np.array([.5,.5,.5,.5,1.])
        accepted=rng.binomial(proposals,close)
        # Repeats are explicit and small; they do not emerge from detected problems.
        accepted+=rng.binomial(clients,.03)
        funded=rng.binomial(accepted,funded_rate)
        for i in range(k):
            immediate=rng.binomial(funded[:,i],LAGS[i][0]);remaining=funded[:,i]-immediate
            next_month=rng.binomial(remaining,LAGS[i][1]/(1-LAGS[i][0]))
            for delay,units in enumerate((immediate,next_month,remaining-next_month)):
                due[:,month+delay+lag_shift,i]+=units
        subs-=rng.binomial(subs,churn)
        support=subs*.75
        marketing=24 if launched else 0;build=(16 if month==0 else 4) if launched else 0
        # If support cannot fit, explicitly cancel unserviceable accounts rather than hide hours.
        support_capacity=np.maximum(0,capacity-marketing-build-presales)
        capratio=np.minimum(1,support_capacity/np.maximum(1,support.sum(axis=1)))
        subs=np.floor(subs*capratio[:,None]).astype(int);support=subs*.75
        available=np.maximum(0,capacity-marketing-build-presales-support.sum(axis=1))
        backlog+=due[:,month,:]
        required=(backlog*delivery).sum(axis=1)
        ratio=np.minimum(1,available/np.maximum(1,required))
        completed=np.floor(backlog*ratio[:,None]).astype(int)
        remaining_hours=available-(completed*delivery).sum(axis=1)
        # Allocate leftover fractional capacity once in fixed channel order; no hidden extra hours.
        for i in range(k):
            extra=np.minimum(backlog[:,i]-completed[:,i],np.floor(remaining_hours/delivery[:,i]).astype(int))
            completed[:,i]+=extra;remaining_hours-=extra*delivery[:,i]
        backlog-=completed;backlog-=rng.binomial(backlog,.35)
        mrr=subs*np.array([700/fx_uah_per_usd,39,39,39,39])
        gross=completed*price+mrr;revenue=gross*(1-refund[:,None])
        fees=np.zeros_like(gross);fees[:,1]=revenue[:,1]*int_fee
        # Direct channels: ASSUMED independent covers Contra flat fee + 2% payout.
        fees[:,2:]=completed[:,2:]*np.where(price[:,2:]<500,15,29)+subs[:,2:]*15+revenue[:,2:]*.02
        net=revenue-fees-completed*2-subs*.5
        own_payout=(gross[:,2:].sum(axis=1)>0)*3.
        int_payout=(gross[:,1]>0)*.99
        net[:,3]-=own_payout;net[:,1]-=int_payout
        channel_hours=completed*delivery
        hours=marketing+build+presales+support.sum(axis=1)+channel_hours.sum(axis=1)
        # Do not clip reported work to disguise an infeasible acquisition/build plan.
        actual_overhead=marketing+build+presales
        hours=actual_overhead+support.sum(axis=1)+channel_hours.sum(axis=1)
        assert np.all(hours<=capacity+1e-8)
        for name,value in dict(traffic=exposure,clicks=clicks,qualified=qualified,conversations=conversations,
          proposals=proposals,accepted=accepted,funded=funded,completed=completed,gross=gross,revenue=revenue,net=net,
          support_hours=support,mrr=mrr,delivery_hours=channel_hours,backlog=backlog).items():out[name][:,month,:]=value
        totals['revenue'][:,month]=revenue.sum(axis=1)
        totals['net'][:,month]=net.sum(axis=1)-(5 if launched else 0)
        for name,val in [('hours',hours),('presales_hours',presales),('marketing_hours',marketing),('build_hours',build)]:totals[name][:,month]=val
        clients+=completed;subs+=rng.binomial(completed,attach)
    return out,totals

def summarize(scenario,out,total):
    rows=[];channels=[]
    for m in range(6):
        row={'scenario':scenario,'day':30*(m+1),'p_net_ge_500':float(np.mean(total['net'][:,m]>=500)),
             'p_revenue_ge_2000':float(np.mean(total['revenue'][:,m]>=2000)),
             'p_net500_reached_by_day':float(np.mean(np.any(total['net'][:,:m+1]>=500,axis=1)))}
        row.update({key+'_median':float(np.median(v[:,m])) for key,v in total.items()})
        row.update(net_p10=float(np.quantile(total['net'][:,m],.1)),net_p90=float(np.quantile(total['net'][:,m],.9)))
        rows.append(row)
        for i,name in enumerate(CHANNELS):
            c={'scenario':scenario,'day':30*(m+1),'channel':name}
            c.update({key+'_mean':float(np.mean(v[:,m,i])) for key,v in out.items()});channels.append(c)
    return rows,channels

def write_csv(name,rows):
    with (ROOT/'data'/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)

def main():
    p=argparse.ArgumentParser();p.add_argument('--runs',type=int,default=5000);p.add_argument('--seed',type=int,default=20261113)
    p.add_argument('--fx-uah-per-usd',type=float,required=True,help='Explicit ASSUMED planning input, not a verified FX quote')
    args=p.parse_args();rows=[];channels=[]
    for scenario in TRAFFIC:
        a,b=simulate(scenario,args.runs,args.seed,fx_uah_per_usd=args.fx_uah_per_usd)
        rr,cc=summarize(scenario,a,b);rows+=rr;channels+=cc
    a,b=simulate('Base',args.runs,args.seed,launched=False,fx_uah_per_usd=args.fx_uah_per_usd)
    zero,_=summarize('UNLAUNCHED_reference',a,b);rows+=zero
    write_csv('channel_revenue_scenarios.csv',rows);write_csv('channel_funnel_results.csv',channels)
    changes=[(name,f,{name:f},{}) for name in CHANNELS for f in (.5,1.5)]
    changes += [(name,f,{name:f},{}) for name in ('qualification','close','accepted_to_funded','price','delivery_hours') for f in (.75,1.25)]
    changes += [('cash_lag_months',1,{},dict(lag_shift=1)),('capacity_hours',80,{},dict(capacity=80)),
                ('capacity_hours',160,{},dict(capacity=160)),('planning_FX',40,{},dict(fx_uah_per_usd=40)),
                ('planning_FX',50,{},dict(fx_uah_per_usd=50))]
    sensitivity=[]
    baseline=next(x['p_net_ge_500'] for x in rows if x['scenario']=='Base' and x['day']==90)
    for name,value,scale,kw in changes:
        options=dict(fx_uah_per_usd=args.fx_uah_per_usd);options.update(kw)
        a,b=simulate('Base',args.runs,args.seed,scales=scale,**options)
        probability=float(np.mean(b['net'][:,2]>=500))
        sensitivity.append({'parameter':name,'value':value,'p_net500_day90':probability,
                            'delta_probability':probability-baseline,'net_day90_median':float(np.median(b['net'][:,2]))})
    write_csv('channel_sensitivity.csv',sensitivity)
    config={'status':'All acquisition, conversion, price, workload, growth and lag priors ASSUMED; no calibration to paid outcomes',
      'seed':args.seed,'runs':args.runs,'channels':CHANNELS,'traffic_triangles':TRAFFIC,'prices_local_currency_triangles':PRICES,
      'UA_price_currency':'UAH','other_price_currency':'USD','planning_FX_UAH_per_USD':args.fx_uah_per_usd,
      'FX_status':'ASSUMED; NBU request403; bank conversion not verified',
      'lag_month_probabilities':LAGS,'marketplace_ctr_triangle':[.01,.03,.05],'marketplace_qualified_click_triangle':[.04,.1,.18],
      'proposal_per_conversation_triangle':[.45,.7,.9],'accepted_per_proposal_triangle':[.08,.2,.35],
      'funded_per_accepted_triangle':[.65,.85,.98],
      'delivery_hours_triangle':[4,6,10],'refund_triangle':[0,.02,.1],'capacity_hours':120,'presales_cap_hours':16,
      'marketing_hours_shared':24,'build_hours_month1':16,'build_hours_later':4,'int_fee_planning':.15,
      'fee_sources':['FH_FEES: UAH Safe paid by client, not seller','UW_FEES:0-15% per contract; plan uses15%',
                     'CO_FEES:15/29 transaction; payer assumption conservative;2% payout and3flat are planning route'],
      'direct_invoice_flat_fee':[15,29],'direct_payout_rate':.02,'direct_payout_flat_month':3,'int_bank_payout_flat_month':.99,
      'retainer_price':[700,39,39,39,39],'retainer_attach_triangle':[0,.08,.2],'retainer_churn_triangle':[.02,.08,.2],
      'support_hours_per_retainer':.75,'repeat_order_probability_month':.03,'backlog_expiry_month':.35,
      'direct_cost_per_job':2,'direct_cost_per_retainer':.5,'monthly_cash_reserve':5,'growth_triangle':[0,.1,.25],
      'outgoing_messages':{'enabled':False,'count':0,'not_a_source_of_leads':True},
      'launch_gates':'Planning rows assume channel admission, explicit launch authorization, account/payout and distribution; none verified by simulation',
      'no_detected_problem_counts_as_leads':True}
    (ROOT/'data/channel_model_assumptions.json').write_text(json.dumps(config,indent=2)+'\n')
    print(json.dumps([x for x in rows if x['day'] in (30,90,180)],indent=2))

if __name__=='__main__':main()
