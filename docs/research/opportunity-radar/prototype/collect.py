"""Opt-in bounded collection: five FTS GETs and one TED search POST.
POST is a read-only search, not publication. Fixed research window: November 2026.
Stops on any HTTP error; no bypass, retry loop, credentials or contact extraction.
Running this replaces the recorded snapshots and collection log; use a separate copy
if preserving the original research evidence. Personal contact fields are discarded.
"""
import urllib.request,json,datetime,hashlib,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
root.joinpath('data').mkdir(exist_ok=True)
root.joinpath('evidence').mkdir(exist_ok=True)
log=[]
def get(url,payload=None):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 req=urllib.request.Request(url,data=json.dumps(payload).encode() if payload else None,headers={'User-Agent':'NinjaOpportunityResearch/0.1 (bounded read-only pilot)','Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=30) as r: raw=r.read(); status=r.status
 log.append({'url':url,'request':payload,'retrieved_at':start,'status':status,'raw_sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
 return json.loads(raw)
# Do not persist personal contact fields or full descriptions. Preserve only task evidence.
fts=[]
u='https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages?limit=100'
for _ in range(5):
 d=get(u)
 for r in d['releases']:
  t=r.get('tender',{});fts.append({'ocid':r['ocid'],'id':r['id'],'date':r['date'],'tag':r.get('tag',[]),'buyer':{'name':r.get('buyer',{}).get('name','')},'tender':{k:t[k] for k in ['title','status','value','tenderPeriod','classification','mainProcurementCategory'] if k in t},'url':'https://www.find-tender.service.gov.uk/Notice/'+r['id'],'data_mode':'live_minimized'})
 u=d.get('links',{}).get('next')
 if not u:break
(root/'data/fts.json').write_text(json.dumps({'license':d.get('license'),'releases':fts},ensure_ascii=False,indent=2))
p={'query':'publication-date >= 20261109 AND (classification-cpv = 72* OR classification-cpv = 7934* OR classification-cpv = 7953*)','fields':['publication-number','publication-date','title-proc','buyer-name','notice-type','deadline-receipt-tender-date-lot','submission-url-lot'],'page':1,'limit':100,'scope':'ALL'}
d=get('https://api.ted.europa.eu/v3/notices/search',p)
notices=[{k:v for k,v in n.items() if k!='links'} for n in d.get('notices',[])]
(root/'data/ted.json').write_text(json.dumps({'notices':notices,'totalNoticeCount':d.get('totalNoticeCount'),'data_mode':'live_minimized'},ensure_ascii=False,indent=2))
(root/'evidence/collection-log.json').write_text(json.dumps(log,indent=2))
print('FTS',len(fts),'TED',len(notices),'total TED',d.get('totalNoticeCount'))
