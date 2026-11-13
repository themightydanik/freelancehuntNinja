"""Small follow-up sample: pagination, notice detail, software demand signals.
Retains public record URLs and technical/budget fields; no people/contact fields.
"""
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parents[2]
OUT={"checked_at":datetime.now(timezone.utc).isoformat(),"requests":[],"evidence":[]}

def get(url):
    start=time.perf_counter()
    r=requests.get(url,timeout=20,headers={"User-Agent":"NinjaResearch/0.1 bounded read-only"})
    OUT['requests'].append({'url':url,'status':r.status_code,'elapsed_seconds':round(time.perf_counter()-start,3),'bytes':len(r.content)})
    r.raise_for_status()
    return r.json()

def main():
    # Published documentation collection; never call any of its write endpoints.
    try:
        doc=get('https://apidocs.freelancehunt.com/api/collections/3971751/S1Lzy7WU?segregateAuth=true&versionTag=latest')
        endpoints=[]
        def walk(node):
            if isinstance(node,dict):
                req=node.get('request')
                if isinstance(req,dict):
                    url=req.get('url',{})
                    raw=url.get('raw','') if isinstance(url,dict) else str(url)
                    if 'bid' in raw.lower() or 'bid' in node.get('name','').lower():
                        endpoints.append({'name':node.get('name'),'method':req.get('method'),'url_template':raw})
                for v in node.values(): walk(v)
            elif isinstance(node,list):
                for v in node: walk(v)
        walk(doc)
        OUT['freelancehunt_documented_bid_endpoints']=endpoints
    except (requests.RequestException,ValueError) as e: OUT['fh_docs_error']=type(e).__name__
    # Fresh feed often starts at historical entries: never interpret it as a recent award list.
    try:
        first=get('https://public.api.openprocurement.org/api/2.5/tenders?limit=2')
        cursor=first.get('next_page',{}).get('uri')
        if cursor and cursor.startswith('https://public.api.openprocurement.org/'):
            second=get(cursor)
            OUT['prozorro_pagination']={'first_count':len(first.get('data',[])),'second_count':len(second.get('data',[])),
                'disjoint_ids':not bool({x['id'] for x in first.get('data',[])} & {x['id'] for x in second.get('data',[])})}
        if first.get('data'):
            detail=get('https://public.api.openprocurement.org/api/2.5/tenders/'+first['data'][0]['id']).get('data',{})
            OUT['prozorro_detail']={'fields':sorted(detail),'award_count':len(detail.get('awards',[])),
                'supplier_identifier_schemes':sorted({s.get('identifier',{}).get('scheme','') for a in detail.get('awards',[]) for s in a.get('suppliers',[])}),
                'is_recent_sample':False}
    except (requests.RequestException,ValueError,KeyError) as e: OUT['prozorro_error']=type(e).__name__
    try:
        data=get('https://api.freelancehunt.com/v2/projects?filter[skill_id]=86&page[number]=1')
        for p in data.get('data',[])[:10]:
            a=p.get('attributes',{}); text=(a.get('name','')+' '+a.get('description','')).lower()
            keywords=[k for k in ('telegram','wordpress','woocommerce','api','react','бот','інтеграц','интеграц','автоматиза') if k in text]
            if keywords:
                budget=a.get('budget') or {}
                OUT['evidence'].append({'id':f'FH-{p["id"]}','kind':'advertised_request_not_sale','url':f'https://api.freelancehunt.com/v2/projects/{p["id"]}',
                    'technical_keywords':keywords,'budget_amount':budget.get('amount'),'budget_currency':budget.get('currency'),
                    'published_at':a.get('published_at'),'status':a.get('status',{}).get('name') if isinstance(a.get('status'),dict) else a.get('status')})
        OUT['fh_page_record_count']=len(data.get('data',[]))
    except (requests.RequestException,ValueError,KeyError) as e: OUT['fh_error']=type(e).__name__
    for repo,query in [('supabase/supabase','RLS'),('n8n-io/n8n','telegram'),('woocommerce/woocommerce','webhook')]:
        try:
            doc=get(f'https://api.github.com/search/issues?q=repo:{repo}+is:issue+is:open+{query}&per_page=2')
            for issue in doc.get('items',[]):
                OUT['evidence'].append({'id':f'GH-{repo.replace("/","-")}-{issue["number"]}','kind':'reported_problem_not_buying_intent',
                    'url':issue['html_url'],'technical_keywords':[query],'created_at':issue['created_at'],
                    'comments':issue['comments'],'state':issue['state']})
        except (requests.RequestException,ValueError,KeyError) as e: OUT.setdefault('github_errors',[]).append({'repo':repo,'error':type(e).__name__})
    (ROOT/'data/priority_followup.json').write_text(json.dumps(OUT,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(OUT,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
