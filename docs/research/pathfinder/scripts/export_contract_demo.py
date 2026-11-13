#!/usr/bin/env python3
"""Synthetic read-only contract reconciliation; no network/client data/store writes."""
from datetime import datetime
from decimal import Decimal
from pathlib import Path
import json

def reconcile(left,right,left_policy,right_policy):
 required={'currency','timezone','date_field','statuses','refunds'}
 if not required<=left_policy.keys() or not required<=right_policy.keys():
  return {'status':'BLOCKED_DEFINITION','reason':'Missing explicit metric policy'}
 if left_policy!=right_policy:
  return {'status':'BLOCKED_DEFINITION','reason':'Policies differ; do not call this a migration failure'}
 if left_policy['refunds']!='signed_lines':
  return {'status':'BLOCKED_DEFINITION','reason':'Only synthetic signed-line refund contract supported'}
 def normalize(records):
  index={};errors=[];total=Decimal('0')
  for row in records:
   if row['currency']!=left_policy['currency']:
    errors.append('mixed currency');continue
   if not row['id'] or row['id'] in index:
    errors.append('empty or duplicate key');continue
   dt=datetime.fromisoformat(row[left_policy['date_field']])
   if dt.utcoffset() is None or left_policy['timezone']!='UTC' or dt.utcoffset().total_seconds()!=0:
    errors.append('unsupported or missing timezone');continue
   if row['status'] not in left_policy['statuses']:continue
   amount=Decimal(row['amount'])
   if not amount.is_finite():errors.append('non-finite amount');continue
   index[row['id']]=amount;total+=amount
  return index,total,errors
 l,lt,le=normalize(left);r,rt,re=normalize(right)
 if le or re:return {'status':'BLOCKED_DATA','errors':le+re}
 missing=sorted(l.keys()-r.keys());extra=sorted(r.keys()-l.keys())
 changed=[k for k in sorted(l.keys()&r.keys()) if l[k]!=r[k]]
 return dict(status='FAIL' if missing or extra or changed or lt!=rt else 'PASS',missing=missing,extra=extra,changed=changed,left_total=str(lt),right_total=str(rt))

def run():
 p=dict(currency='USD',timezone='UTC',date_field='paid_at',statuses=['completed','refund'],refunds='signed_lines')
 base=[dict(id='synthetic-order',currency='USD',status='completed',amount='100.00',paid_at='2026-01-02T00:00:00+00:00'),dict(id='synthetic-refund',currency='USD',status='refund',amount='-20.00',paid_at='2026-01-03T00:00:00+00:00')]
 same=reconcile(base,base,p,p);assert same['status']=='PASS' and same['left_total']=='80.00'
 # Refund omission must not pass just because the order row matches.
 omitted=reconcile(base,base[:1],p,p);assert omitted['status']=='FAIL' and omitted['missing']==['synthetic-refund']
 different=reconcile(base,base,p,dict(p,date_field='created_at'));assert different['status']=='BLOCKED_DEFINITION'
 duplicate=reconcile(base,base+[base[0]],p,p);assert duplicate['status']=='BLOCKED_DATA'
 mixed=reconcile(base,[dict(base[0],currency='EUR')],p,p);assert mixed['status']=='BLOCKED_DATA'
 naive=reconcile([dict(base[0],paid_at='2026-01-02T00:00:00')],base,p,p);assert naive['status']=='BLOCKED_DATA'
 return dict(equal_pair=same,omitted_refund=omitted,different_definition=different,duplicate=duplicate,mixed_currency=mixed,missing_timezone=naive,limitations='Synthetic USD/UTC/signed-lines contract only. No production Shopify/Woo mapping, tax audit, performance test or actual customer evidence.')
if __name__=='__main__':
 result=run();(Path(__file__).resolve().parents[1]/'data/demo_result.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS: equality, refund omission, definitions, duplicates, currency and timezone cases; offline only')
