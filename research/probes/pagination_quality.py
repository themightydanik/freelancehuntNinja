"""Small priority-source follow-up after reading official contracts.
No raw organizations, contacts or opaque pagination tokens retained.
"""
import hashlib
import json
import time
from datetime import datetime,timezone
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parents[2]

def main():
    result={'checked_at':datetime.now(timezone.utc).isoformat(),'requests':[]}
    def request(method,url,**kwargs):
        start=time.perf_counter()
        r=requests.request(method,url,timeout=20,headers={'User-Agent':'NinjaResearch/0.1 bounded quality followup'},**kwargs)
        result['requests'].append({'method':method,'url':url,'payload':kwargs.get('json'),
            'status':r.status_code,'elapsed_seconds':round(time.perf_counter()-start,3),'bytes':len(r.content)})
        r.raise_for_status();return r
    try:
        # Read the schema linked through official Swagger config, not a guessed API path.
        config=request('GET','https://api.ted.europa.eu/v3/api-docs/swagger-config').json()
        assert any(x.get('url')=='/api-v3.yaml' for x in config.get('urls',[]))
        schema=request('GET','https://api.ted.europa.eu/api-v3.yaml').text
        result['ted_documented_contract']={'url':'https://api.ted.europa.eu/api-v3.yaml',
            'sha256':hashlib.sha256(schema.encode()).hexdigest(),
            'page_number_mode_documented':'PAGE_NUMBER' in schema,'iteration_mode_documented':'ITERATION' in schema,
            'page_number_15000_cap_documented':'15000 notices' in schema}
        pages=[]
        for page in (1,2):
            payload={'query':'publication-date >= 20261001','limit':2,'page':page,'paginationMode':'PAGE_NUMBER',
                     'fields':['publication-number','publication-date','notice-title'],'onlyLatestVersions':True}
            d=request('POST','https://api.ted.europa.eu/v3/notices/search',json=payload).json()
            pages.append(d)
        a,b=pages
        result['ted_page_test']={'counts':[len(d.get('notices',[])) for d in pages],
            'disjoint_publication_numbers':not bool({n.get('publication-number') for n in a.get('notices',[])}&{n.get('publication-number') for n in b.get('notices',[])}),
            'reported_total':[d.get('totalNoticeCount') for d in pages],
            'timed_out':[d.get('timedOut') for d in pages],
            'title_present':[sum(bool(n.get('notice-title')) for n in d.get('notices',[])) for d in pages]}
    except (requests.RequestException,ValueError,AssertionError) as e:result['ted_error']=type(e).__name__
    try:
        url='https://public.api.openprocurement.org/api/2.5/tenders?limit=2&descending=1'
        data=request('GET',url).json().get('data',[])
        summaries=[]
        for item in data[:2]:
            d=request('GET','https://public.api.openprocurement.org/api/2.5/tenders/'+item['id']).json().get('data',{})
            suppliers=[s for a in d.get('awards',[]) for s in a.get('suppliers',[])]
            summaries.append({'status':d.get('status'),'date_modified':d.get('dateModified'),
                'award_count':len(d.get('awards',[])),'supplier_count':len(suppliers),
                'suppliers_with_identifier':sum(bool(s.get('identifier',{}).get('id')) for s in suppliers),
                'identifier_schemes':sorted({s.get('identifier',{}).get('scheme','') for s in suppliers}),
                'has_cpv':any(bool(i.get('classification',{}).get('id')) for i in d.get('items',[]))})
        result['prozorro_descending_sample']=summaries
    except (requests.RequestException,ValueError,KeyError) as e:result['prozorro_error']=type(e).__name__
    try:
        url='https://api.wordpress.org/plugins/info/1.2/?action=query_plugins&request[search]=telegram&request[per_page]=2&request[fields][active_installs]=true&request[fields][last_updated]=true&request[fields][tested]=true'
        doc=request('GET',url).json()
        result['wp_optional_fields']={'sample_size':len(doc.get('plugins',[])),
          'fields_present':{k:sum(k in p and p[k] is not None for p in doc.get('plugins',[])) for k in ('slug','last_updated','tested','active_installs','version')},
          'pagination_metadata':doc.get('info')}
    except (requests.RequestException,ValueError) as e:result['wp_error']=type(e).__name__
    (ROOT/'data/pagination_quality_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
