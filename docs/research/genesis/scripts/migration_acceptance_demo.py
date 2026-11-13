#!/usr/bin/env python3
"""Synthetic, offline, deterministic acceptance subset; no real customer data."""
from decimal import Decimal
from pathlib import Path
import json

def compare(source,target):
 def index(rows):
  result={};duplicates=[]
  for r in rows:
   key=r['id']
   if key in result:duplicates.append(key)
   else:result[key]=r
  return result,duplicates
 s,sd=index(source);t,td=index(target)
 missing=sorted(set(s)-set(t));extra=sorted(set(t)-set(s));changed=[]
 for key in sorted(set(s)&set(t)):
  for field in ['quantity','amount']:
   # Decimal only; accepted unit/currency mapping must be agreed externally.
   if Decimal(str(s[key][field]))!=Decimal(str(t[key][field])):
    changed.append({'id':key,'field':field,'source':s[key][field],'target':t[key][field]})
 sums=lambda rows:{f:str(sum((Decimal(str(r[f])) for r in rows),Decimal(0))) for f in ['quantity','amount']}
 return dict(status='FAIL' if sd or td or missing or extra or changed else 'PASS',source_duplicates=sd,target_duplicates=td,missing=missing,extra=extra,changed=changed,source_raw_totals=sums(source),target_raw_totals=sums(target),limitations='Synthetic IDs and one currency/unit; no production mapping, taxes, PII, URLs or API writes')

def run():
 source=[{'id':'synthetic-1','quantity':'2','amount':'19.90'},{'id':'synthetic-2','quantity':'1','amount':'5.00'}]
 target=[{'id':'synthetic-1','quantity':'2','amount':'19.99'},{'id':'synthetic-1','quantity':'2','amount':'19.99'}]
 result=compare(source,target)
 assert result['status']=='FAIL' and result['missing']==['synthetic-2']
 assert result['target_duplicates']==['synthetic-1']
 assert result['changed']==[{'id':'synthetic-1','field':'amount','source':'19.90','target':'19.99'}]
 assert result['source_raw_totals']['amount']=='24.90'
 assert compare(source,source)['status']=='PASS'
 result['equal_pair_control']='PASS';return result
if __name__=='__main__':
 p=Path(__file__).resolve().parents[1]/'data/demo_result.json';p.write_text(json.dumps(run(),indent=2)+'\n');print('Synthetic failure detected; equal-pair control PASS; no network')
