"""Public GitHub commissioned-bug sample, not a freelance-market census.
One sponsor/program; title price is an advertised reward, never a payment.
"""
import csv
import hashlib
import json
import re
from datetime import datetime,timezone
from pathlib import Path
import requests
from commercial_sample import safe_text

ROOT=Path(__file__).resolve().parents[2]
QUERY='repo:Expensify/App is:issue label:External created:2026-10-14..2026-11-12'

def main():
    url='https://api.github.com/search/issues'
    r=requests.get(url,params={'q':QUERY,'per_page':30},timeout=20,headers={'User-Agent':'NinjaResearch/0.2 public commissioned-issues review'})
    r.raise_for_status();doc=r.json();rows=[]
    for issue in doc.get('items',[]):
        title=issue.get('title','');match=re.match(r'^\[\$(\d[\d,]*(?:\.\d+)?)\]',title)
        rows.append({'sample_id':'EXP-'+str(issue['number']),'source':'GitHub/Expensify External program',
            'url':issue['html_url'],'created_at':issue.get('created_at'),'state':issue.get('state'),
            'technical_title':safe_text(title),'advertised_reward_usd':float(match.group(1).replace(',','')) if match else '',
            'comments_not_bids':issue.get('comments'),'sponsor_count':1,
            'scope':'existing application bug; NOT Telegram Bot Recovery; API root cause not established',
            'payment_status':'UNKNOWN; no acceptance, assignment or payment verified',
            'checked_at':datetime.now(timezone.utc).isoformat()})
    with (ROOT/'data/international_bounty_sample.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    rules='https://raw.githubusercontent.com/Expensify/App/main/contributingGuides/CONTRIBUTING.md'
    rr=requests.get(rules,timeout=20)
    if rr.ok:
        Path('/tmp/ninja-expensify-contributing.txt').write_text(rr.text)
    out={'query':QUERY,'search_url':r.url,'status':r.status_code,'response_sha256':hashlib.sha256(r.content).hexdigest(),
        'reported_total':doc.get('total_count'),'sample_size':len(rows),'one_sponsor_only':True,
        'rules_url':rules,'rules_status':rr.status_code,'rules_sha256':hashlib.sha256(rr.content).hexdigest(),
        'limits':['non-random sample','one established codebase/program','not representative of international freelance buyers',
                  'External label does not establish unassigned/available job','rewards not paid transaction prices'],
        'checked_at':datetime.now(timezone.utc).isoformat()}
    (ROOT/'data/international_bounty_manifest.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
