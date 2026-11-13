"""Conditional six-month Monte Carlo, not an empirically calibrated forecast.

All funnel priors are ASSUMED. Currency USD, time hours, months 30 days.
Revenue target = monthly receipts after refunds, before platform fees and tax.
Run: python research/models/revenue_model.py --runs 5000 --seed 20261113
"""
import argparse
import csv
import json
import os
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
SCENARIOS={
 'Conservative':{'impressions':(300,700,1400),'growth':(0,0.08,0.2),'ctr':(.008,.018,.03),
  'qualification':(.03,.07,.12),'negotiation':(.35,.5,.65),'proposal':(.4,.6,.75),'close':(.08,.15,.25),
  'ticket':(180,300,500),'delivery':(12,18,28),'delay':(.1,.4,.5)},
 'Base':{'impressions':(1000,2400,4500),'growth':(.05,.18,.35),'ctr':(.015,.03,.05),
  'qualification':(.05,.12,.2),'negotiation':(.5,.7,.85),'proposal':(.55,.75,.9),'close':(.15,.28,.4),
  'ticket':(300,500,800),'delivery':(8,12,20),'delay':(.35,.5,.15)},
 'Upside':{'impressions':(2500,5000,10000),'growth':(.1,.3,.5),'ctr':(.02,.04,.065),
  'qualification':(.08,.16,.25),'negotiation':(.6,.8,.9),'proposal':(.65,.8,.95),'close':(.2,.35,.5),
  'ticket':(400,650,1000),'delivery':(6,10,16),'delay':(.6,.35,.05)},
}

def net_receipts(gross,refund_rate,fee_rate,variable_cost,fixed_cost):
    revenue=gross*(1-refund_rate)
    return revenue, revenue*(1-fee_rate)-variable_cost-fixed_cost

def simulate(name,runs=5000,seed=20261113,scale=None,no_first_month=False):
    rng=np.random.default_rng(seed); cfg=SCENARIOS[name]; scale=scale or {}
    def draw(key):
        x=rng.triangular(*cfg[key],size=runs)*scale.get(key,1)
        return np.clip(x,0,1) if key in ('ctr','qualification','negotiation','proposal','close') else x
    p={key:draw(key) for key in cfg if key!='delay'}
    refund=rng.triangular(0,.03,.1,runs); fee=rng.triangular(.05,.1,.2,runs)*scale.get('fee',1)
    attach=rng.triangular(.05,.15,.3,runs)*scale.get('attach',1)
    churn=rng.triangular(.02,.08,.2,runs)*scale.get('churn',1)
    repeat=rng.triangular(0,.03,.1,runs)
    capacity=np.full(runs,120.*scale.get('capacity',1))
    due=np.zeros((runs,8),dtype=int); backlog=np.zeros(runs,dtype=int)
    clients=np.zeros(runs,dtype=int); subs=np.zeros(runs,dtype=int)
    results={k:np.zeros((runs,6)) for k in ('impressions','clicks','qualified','negotiations','proposals','orders',
      'completed','template_units','revenue','gross','net','hours','support_hours','backlog','mrr','capacity_hours','refund_rate','fee_rate')}
    for m in range(6):
        impressions=rng.poisson(np.minimum(p['impressions']*(1+p['growth'])**m,200000))
        clicks=rng.binomial(impressions,p['ctr'])
        # Service lane gets 80% of traffic. Other 20% is a downloadable kit lane.
        service_clicks=rng.binomial(clicks,.8)
        qualified=rng.binomial(service_clicks,p['qualification'])
        negotiations=rng.binomial(qualified,p['negotiation'])
        # 24h marketing plus bounded 16h presales. Excess negotiations expire.
        negotiations=np.minimum(negotiations,32)
        proposals=rng.binomial(negotiations,p['proposal'])
        orders=rng.binomial(proposals,p['close'])
        orders+=rng.binomial(clients,np.clip(repeat,0,1))
        if no_first_month and m==0: orders[:]=0
        now=rng.binomial(orders,cfg['delay'][0]); remaining=orders-now
        nxt=rng.binomial(remaining,cfg['delay'][1]/(1-cfg['delay'][0]))
        due[:,m]+=now; due[:,m+1]+=nxt; due[:,m+2]+=remaining-nxt
        subs-=rng.binomial(subs,np.clip(churn,0,1))
        support=subs*.5*scale.get('support',1)
        # If support exceeds capacity, cancel accounts beyond serviceable capacity.
        max_subs=np.floor(np.maximum(0,capacity-24)/(.5*scale.get('support',1))).astype(int)
        subs=np.minimum(subs,max_subs); support=subs*.5*scale.get('support',1)
        build=40 if m==0 else 4
        presales=negotiations*.35+proposals*.15
        available=np.maximum(0,capacity-24-build-presales-support)
        backlog+=due[:,m]
        completed=np.minimum(backlog,np.floor(available/p['delivery']).astype(int))
        backlog-=completed
        # Backlog expires after each month with 35% probability; do not count as revenue.
        backlog-=rng.binomial(backlog,.35)
        delivery=completed*p['delivery']; clients+=completed
        kit_rate=rng.triangular(.002,.008,.02,runs)
        template_units=rng.binomial(clicks-service_clicks,kit_rate)
        template_units=np.minimum(template_units,np.floor(np.maximum(0,available-delivery)/.25).astype(int))
        if no_first_month and m==0: template_units[:]=0
        # Subscription attach starts next month; current MRR is existing retained accounts.
        mrr=subs*39.
        gross=completed*p['ticket']+template_units*49.+mrr
        revenue,net=net_receipts(gross,refund,fee,completed*3.+template_units*.5,5.)
        hours=np.minimum(capacity,24+build+presales+support+delivery+template_units*.25)
        for key,value in dict(impressions=impressions,clicks=clicks,qualified=qualified,negotiations=negotiations,
          proposals=proposals,orders=orders,completed=completed,template_units=template_units,revenue=revenue,
          gross=gross,net=net,hours=hours,support_hours=support,backlog=backlog,mrr=mrr,
          capacity_hours=capacity,refund_rate=refund,fee_rate=fee).items(): results[key][:,m]=value
        subs+=rng.binomial(completed,np.clip(attach,0,1))
    return results

def summarize(name,r):
    rows=[]
    for m in range(6):
        revenue=r['revenue'][:,m]; net=r['net'][:,m]; n=len(revenue)
        p=float(np.mean(revenue>=2000))
        # Wilson intervals remain meaningful when zero trajectories succeed.
        z=1.96; denominator=1+z*z/n
        center=(p+z*z/(2*n))/denominator
        half=z*(p*(1-p)/n+z*z/(4*n*n))**.5/denominator
        row={'scenario':name,'day':(m+1)*30,'runs':n,'p_month_revenue_ge_2000':p,
             'mc_95_low':max(0,center-half),'mc_95_high':min(1,center+half),
             'p_reached_by_day':float(np.mean(np.any(r['revenue'][:,:m+1]>=2000,axis=1))),
             'revenue_p10':float(np.quantile(revenue,.1)),'revenue_median':float(np.median(revenue)),
             'revenue_p90':float(np.quantile(revenue,.9)), 'net_median':float(np.median(net)),
             'net_per_hour_median':float(np.median(net/np.maximum(r['hours'][:,m],1))),
             'economic_profit_median_at_20_per_hour':float(np.median(net-20*r['hours'][:,m]))}
        row.update({k+'_median':float(np.median(v[:,m])) for k,v in r.items() if k not in ('net','revenue')})
        rows.append(row)
    return rows

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--runs',type=int,default=5000); parser.add_argument('--seed',type=int,default=20261113)
    args=parser.parse_args(); rows=[]; full={}
    for name in SCENARIOS:
        r=simulate(name,args.runs,args.seed); full[name]=r; rows+=summarize(name,r)
    def write(name,records):
        with (ROOT/'data'/name).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n');w.writeheader();w.writerows(records)
    write('revenue_scenarios.csv',rows)
    sensitivity=[]
    baseline=float(np.mean(full['Base']['revenue'][:,2]>=2000))
    for key in ('impressions','ctr','qualification','negotiation','proposal','close','ticket','delivery','growth','capacity','attach','churn','fee','support'):
        for factor in (.75,1.25):
            r=simulate('Base',args.runs,args.seed,{key:factor})
            sensitivity.append({'parameter':key,'factor':factor,'p_day90':float(np.mean(r['revenue'][:,2]>=2000)),
              'delta_probability':float(np.mean(r['revenue'][:,2]>=2000))-baseline,'revenue_day90_median':float(np.median(r['revenue'][:,2]))})
    write('revenue_sensitivity.csv',sensitivity)
    disrupted=summarize('Base_no_sales_month1',simulate('Base',args.runs,args.seed,no_first_month=True))
    write('revenue_no_sales_month1.csv',disrupted)
    (ROOT/'data/model_assumptions.json').write_text(json.dumps({'seed':args.seed,'runs':args.runs,'status':'ASSUMED; not calibrated to customers',
      'scenarios':SCENARIOS,'common':{'capacity_hours':120,'marketing_hours':24,'build_hours_month1':40,'build_hours_later':4,
      'presales_hours_per_negotiation':.35,'presales_hours_per_proposal':.15,'presales_negotiation_cap':32,
      'service_traffic_share':.8,'refund_triangle':[0,.03,.1],'fee_triangle':[.05,.1,.2],
      'subscription_price':39,'support_hours_per_sub':.5,'attach_triangle':[.05,.15,.3],'monthly_churn_triangle':[.02,.08,.2],
      'repeat_triangle':[0,.03,.1],'template_price':49,'kit_conversion_triangle':[.002,.008,.02],
      'variable_cost_per_job':3,'variable_cost_per_kit':.5,'monthly_cash_cost':5,'backlog_monthly_expiry':.35}},indent=2)+'\n')
    os.environ.setdefault('MPLCONFIGDIR','/tmp/ninja-matplotlib')
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    for name,r in full.items():
        q=np.quantile(r['revenue'],[.1,.5,.9],axis=0); days=np.arange(1,7)*30
        axes[0].plot(days,q[1],label=name); axes[0].fill_between(days,q[0],q[2],alpha=.12)
        axes[1].plot(days,np.mean(r['revenue']>=2000,axis=0),label=name)
    axes[0].axhline(2000,color='black',linestyle='--');axes[0].set(ylabel='Monthly receipts after refunds (USD)',xlabel='Day')
    axes[1].set(ylabel='Conditional P(month receipts >= $2,000)',xlabel='Day',ylim=(0,1))
    for ax in axes:ax.legend();ax.grid(alpha=.2)
    fig.suptitle('ASSUMED priors; bands = simulation p10–p90, NOT market evidence')
    fig.tight_layout(); fig.savefig(ROOT/'data/revenue_scenarios.png',dpi=150);plt.close(fig)
    print(json.dumps([r for r in rows if r['day'] in (30,60,90,180)],indent=2))

if __name__=='__main__': main()
