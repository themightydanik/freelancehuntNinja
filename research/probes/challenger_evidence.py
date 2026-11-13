"""Read-only IT award and repeated-problem samples. No outreach or transactions.

Issue reporter IDs are compared only in memory; persist per-gap anonymous groups.
These are reports, not reproduced bugs or evidence of willingness to pay.
"""
import csv
import json
import time
from datetime import datetime,timezone
from pathlib import Path
import requests
from commercial_sample import safe_text

ROOT=Path(__file__).resolve().parents[2]
GAPS={
 'G01_telegram_webhook_lifecycle':[('n8n-io/n8n',18754),('n8n-io/n8n',18895),('n8n-io/n8n',13385)],
 'G02_telegram_large_files':[('codingteam/emulsion',181),('irazasyed/telegram-bot-sdk',1129),('chatwoot/chatwoot',16110)],
 'G03_wc_event_semantics':[('woocommerce/woocommerce',69438),('woocommerce/woocommerce',41544)],
 'G04_postgis_advisory':[('supabase/supabase',47206),('supabase/supabase',29122)],
 'G05_stripe_raw_body':[('vercel/next.js',60002),('vercel/next.js',61365),('vercel/next.js',49739)],
}

def main():
    logs=[]
    def read(method,url,**kwargs):
        start=time.perf_counter()
        r=requests.request(method,url,timeout=25,headers={'User-Agent':'NinjaResearch/0.2 bounded challengers'},**kwargs)
        logs.append({'method':method,'url':url,'status':r.status_code,'elapsed_seconds':round(time.perf_counter()-start,3),'bytes':len(r.content)})
        r.raise_for_status();return r
    checked=datetime.now(timezone.utc).isoformat();awards=[];issues=[];gap_counts={};errors=[]
    payload={'query':'classification-cpv=72200000 AND publication-date >= 20261001 AND notice-type=can-standard',
             'limit':5,'fields':['publication-number','publication-date','notice-title','notice-type','classification-cpv',
                                'winner-name','winner-identifier','buyer-name','total-value','total-value-cur'],'onlyLatestVersions':True}
    try:
        doc=read('POST','https://api.ted.europa.eu/v3/notices/search',json=payload).json()
        for n in doc.get('notices',[]):
            def texts(field):
                value=n.get(field,{})
                if isinstance(value,dict):
                    value=value.get('eng') or next(iter(value.values()),'')
                return value if isinstance(value,list) else [value]
            awards.append({'notice':n.get('publication-number'),'url':'https://ted.europa.eu/en/notice/-/detail/'+n['publication-number'],
                'published_at':n.get('publication-date'),'notice_type':n.get('notice-type'),
                'cpv':','.join(sorted(set(n.get('classification-cpv',[])))),
                'technical_title':safe_text(texts('notice-title')[0])[:800],
                'winner_legal_names':' ; '.join(texts('winner-name')),
                'winner_identifiers':' ; '.join(texts('winner-identifier')),
                'buyer_legal_names':' ; '.join(texts('buyer-name')),
                'value_raw':json.dumps(n.get('total-value')),'currency':','.join(n.get('total-value-cur',[])),
                'checked_at':checked,'evidence':'published IT-services contract award; not subcontract buying intent',
                'identity_limit':'Identifiers exposed by TED search; national scheme/website ownership not independently verified'})
    except (requests.RequestException,ValueError,KeyError) as e:errors.append({'phase':'ted','error':type(e).__name__})
    scratch=Path('/tmp/ninja-gap-review');scratch.mkdir(exist_ok=True)
    for gap,cases in GAPS.items():
        reporters={}
        for repo,num in cases:
            try:
                d=read('GET',f'https://api.github.com/repos/{repo}/issues/{num}').json()
                user=(d.get('user') or {}).get('id')
                if user is not None and user not in reporters:reporters[user]=f'reporter_{len(reporters)+1}'
                row={'gap_id':gap,'repo':repo,'issue':num,'url':d['html_url'],'technical_title':safe_text(d.get('title','')),
                     'created_at':d.get('created_at'),'state':d.get('state'),'comments':d.get('comments'),
                     'reporter_group_within_gap':reporters.get(user,'UNKNOWN'),'checked_at':checked,
                     'evidence_level':'OBSERVED report; root cause, independent deployment and payment unverified'}
                issues.append(row)
                (scratch/(repo.replace('/','-')+'-'+str(num)+'.txt')).write_text(safe_text(d.get('title',''))+'\n'+safe_text(d.get('body') or '')[:7000])
            except (requests.RequestException,ValueError,KeyError) as e:errors.append({'phase':gap,'issue':num,'error':type(e).__name__})
        gap_counts[gap]={'distinct_reporter_accounts_in_memory':len(reporters),
                        'independent_organizations':'UNKNOWN; different accounts are not proof of different buyers'}
    for name,records in [('it_award_sample.csv',awards),('integration_gap_reports.csv',issues)]:
        if records:
            with (ROOT/'data'/name).open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n');w.writeheader();w.writerows(records)
    out={'checked_at':checked,'ted_query':payload,'ted_reported_total':doc.get('totalNoticeCount') if 'doc' in locals() else None,
         'requests':logs,'errors':errors,'gap_reporter_counts':gap_counts,
         'discovery_correction':'form-type=can was rejected HTTP400; documented notice-type=can-standard accepted',
         'contacts_retained':False,'outreach_actions':0}
    (ROOT/'data/challenger_probe_manifest.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'award_count':len(awards),'issue_count':len(issues),'reporter_counts':gap_counts,'errors':errors},indent=2))

if __name__=='__main__':main()
