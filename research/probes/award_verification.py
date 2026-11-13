"""Small second IT-services stratum and read-only national-register cross-checks.
Retains legal-entity identity only; no contact/address/officer fields.
"""
import csv
import json
import re
from datetime import datetime,timezone
from pathlib import Path
import requests
from commercial_sample import safe_text

ROOT=Path(__file__).resolve().parents[2]

def main():
    log=[];cases=[]
    payload={'query':'classification-cpv=72262000 AND publication-date >= 20261001 AND notice-type=can-standard',
             'limit':5,'fields':['publication-number','publication-date','notice-title','classification-cpv','winner-name','winner-identifier','total-value','total-value-cur'],
             'onlyLatestVersions':True}
    def read(method,url,**kw):
        r=requests.request(method,url,timeout=20,headers={'User-Agent':'NinjaResearch/0.2 bounded award verification'},**kw)
        log.append({'url':url,'method':method,'status':r.status_code,'bytes':len(r.content)})
        return r
    errors=[];registry=[]
    try:
        r=read('POST','https://api.ted.europa.eu/v3/notices/search',json=payload);r.raise_for_status();doc=r.json()
        for n in doc.get('notices',[]):
            def one(field):
                x=n.get(field,{})
                if isinstance(x,dict):x=x.get('eng') or next(iter(x.values()),'')
                if isinstance(x,list):
                    if field=='winner-identifier':
                        x=['[unverified person-like identifier omitted]' if re.fullmatch(r'\d{8}[A-Z]',str(v)) else str(v) for v in x]
                    return ' ; '.join(str(v) for v in x)
                return str(x)
            cases.append({'notice':n['publication-number'],'url':'https://ted.europa.eu/en/notice/-/detail/'+n['publication-number'],
                'published_at':n.get('publication-date'),'technical_title':safe_text(one('notice-title'))[:700],
                'cpv':','.join(n.get('classification-cpv',[])),'winner_legal_names':one('winner-name'),
                'winner_identifiers':one('winner-identifier'),'value_raw':json.dumps(n.get('total-value')),
                'currency':','.join(n.get('total-value-cur',[])),'checked_at':datetime.now(timezone.utc).isoformat()})
        for ico in ('07241127','26775794','26480981','26284146','07436505'):
            r=read('GET','https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/'+ico)
            if r.ok:
                d=r.json();registry.append({'scheme':'CZ-ICO','identifier':d.get('ico'),'legal_name':d.get('obchodniJmeno'),
                                           'source':r.url,'status':r.status_code})
            else:registry.append({'identifier':ico,'source':r.url,'status':r.status_code})
        # A 202/empty XML response is a blocker, never a successful notice verification.
        r=read('GET','https://ted.europa.eu/en/notice/674368-2026/xml')
        xml_probe={'status':r.status_code,'bytes':len(r.content),'usable_xml':bool(r.content.lstrip().startswith(b'<?xml'))}
    except (requests.RequestException,ValueError) as e:errors.append(type(e).__name__);xml_probe={}
    if cases:
        with (ROOT/'data/it_award_development_stratum.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(cases[0]),lineterminator='\n');w.writeheader();w.writerows(cases)
    out={'checked_at':datetime.now(timezone.utc).isoformat(),'query':payload,'requests':log,
         'national_registry_crosschecks':registry,'notice_xml_probe':xml_probe,'errors':errors,
         'subcontractor_demand':'UNKNOWN; no partnerships, contacts or account actions performed'}
    (ROOT/'data/award_verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
