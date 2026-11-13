"""Bounded read-only active-job sampling, NOT a market census or sales evidence.

30 unfiltered FH pages + up to 5 pages each for Bot/DevOps/Python.
Freelancer collection is disabled: section33 requires written permission.
Active-only survivor bias, keyword-query bias and missing budgets are explicit.
No employer/author/contact/attachment fields retained; no bids or messages sent.
"""
import csv
import hashlib
import json
import re
import time
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parents[2]
ASOF=datetime(2026,11,13,0,0,tzinfo=timezone.utc)
START=datetime(2026,10,14,0,0,tzinfo=timezone.utc)
QUERIES=[]  # Restricted platform queries are deliberately not executed.
TECH=re.compile(r'telegram|телеграм|бот|\bbot\b|webhook|вебхук|\bapi\b|\bpython\b|n8n',re.I)
RECOVERY=re.compile(r'fix|repair|recover|restore|debug|broken|not work|stopped|deploy|migrat|troubleshoot|error|виправ|исправ|віднов|восстанов|помил|ошиб|перен[ео]|розгор|развер|депло|не працю|не работа|доработ|доопрац',re.I)

def safe_text(text):
    text=re.sub(r'<[^>]*>',' ',text or '')
    text=re.sub(r'https?://\S+','[link omitted]',text)
    text=re.sub(r'[\w.+-]+@[\w.-]+|(?<!\w)@[\w_]+','[contact omitted]',text)
    text=re.sub(r'\+?\d[\d ()-]{9,}\d','[number omitted]',text)
    text=re.sub(r'\b[A-Za-z0-9_:/+=-]{35,}\b','[long literal omitted]',text)
    return re.sub(r'\s+',' ',text).strip()

def main():
    log=[];rows={};errors=[]
    scratch=Path('/tmp/ninja-commercial-review');scratch.mkdir(exist_ok=True)
    def read(url,params=None):
        start=time.perf_counter()
        with requests.get(url,params=params,stream=True,timeout=(10,25),
                          headers={'User-Agent':'NinjaResearch/0.2 bounded read-only commercial research'}) as r:
            body=bytearray()
            for b in r.iter_content(8192):
                body.extend(b)
                if len(body)>2_000_000:break
            log.append({'url':r.url,'status':r.status_code,'elapsed_seconds':round(time.perf_counter()-start,3),
                        'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()})
            if len(body)>2_000_000:raise ValueError('response byte cap')
            r.raise_for_status();return json.loads(body)
    def add(platform,project,query):
        p=project.get('attributes',project)
        pid=str(project['id']);key=platform+'-'+pid
        if key in rows:
            rows[key]['query_strata']=','.join(sorted(set(rows[key]['query_strata'].split(','))|{query}));return
        title=p.get('name',p.get('title',''));description=p.get('description') or p.get('preview_description') or ''
        text=title+' '+description
        assert platform=='FH', 'Only documented Freelancehunt public listing reads are enabled'
        stamp=p.get('published_at');date=datetime.fromisoformat(stamp) if stamp else None
        budget=p.get('budget') or {};currency=budget.get('currency')
        if isinstance(currency,dict):currency=currency.get('code')
        low=high=budget.get('amount');fx=None;bids=p.get('bid_count');typ='fixed'
        url='https://api.freelancehunt.com/v2/projects/'+pid
        in_window=bool(date and START<=date<ASOF)
        tech=bool(TECH.search(text));recovery=bool(RECOVERY.search(text))
        # Only technical rows carry a short redacted title in the public sample.
        row={'sample_id':key,'platform':platform,'url':url,'checked_at':datetime.now(timezone.utc).isoformat(),
             'published_at':date.isoformat() if date else '', 'in_window':in_window,'query_strata':query,
             'technical_keyword_match':tech,'recovery_keyword_match':recovery,
             'screening_status':'candidate_manual_review' if tech and recovery and in_window else 'not_selected_by_keyword_rule',
             'technical_title':safe_text(title)[:180] if tech and in_window else '[not retained: outside technical/window screen]',
             'project_type':typ,'budget_min':low,'budget_max':high,'currency':currency,
             'platform_fx_usd_per_unit_unverified':fx,'bids_snapshot':bids,
             'buyer_geography':'UNKNOWN; platform segment is not residence',
             'evidence_level':'advertised open request, not paid sale'}
        rows[key]=row
        if tech and recovery and in_window:
            (scratch/(key+'.txt')).write_text(safe_text(title)+'\n'+safe_text(description)[:6000])
    for page in range(1,31):
        try:
            d=read('https://api.freelancehunt.com/v2/projects',{'page[number]':page})
            for p in d.get('data',[]):add('FH',p,'unfiltered_open')
            if not d.get('links',{}).get('next'):break
        except (requests.RequestException,ValueError,KeyError) as e:
            errors.append({'platform':'FH','page':page,'error':type(e).__name__});break
    for skill in (180,181,22):
        for page in range(1,6):
            try:
                d=read('https://api.freelancehunt.com/v2/projects',{'filter[skill_id]':skill,'page[number]':page})
                for p in d.get('data',[]):add('FH',p,'skill_'+str(skill))
                if not d.get('links',{}).get('next'):break
            except (requests.RequestException,ValueError,KeyError) as e:
                errors.append({'platform':'FH','skill':skill,'page':page,'error':type(e).__name__});break
    records=list(rows.values())
    with (ROOT/'data/commercial_job_sample.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n');w.writeheader();w.writerows(records)
    summary={'window_start_inclusive':START.isoformat(),'window_end_exclusive':ASOF.isoformat(),
             'sampling_frame':'active/open listings only; bounded non-probability sample; no platform census',
             'query_definitions':QUERIES,'fh_skill_strata':[180,181,22],'requests':log,'errors':errors,
             'unique_by_platform':dict(Counter(r['platform'] for r in records)),
             'in_window_by_platform':dict(Counter(r['platform'] for r in records if r['in_window'])),
             'candidate_by_platform':dict(Counter(r['platform'] for r in records if r['screening_status']=='candidate_manual_review')),
             'no_contacts_or_authors_retained':True}
    (ROOT/'data/commercial_sample_manifest.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='requests'},indent=2))

if __name__=='__main__':main()
