"""Recheck exact reviewed issue URLs, retaining only topic-marker presence.

The source allegations are NOT reproduced bugs or evidence of payment intent.
"""
import csv
import json
from datetime import datetime,timezone
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parents[2]
MARKERS={
 'GH-supabase-supabase-47206':['spatial_ref_sys','owner','RLS'],
 'GH-supabase-supabase-48382':['TRUNCATE','GRANT'],
 'GH-n8n-io-n8n-42667':['allowed_updates','callback_query'],
 'GH-n8n-io-n8n-37361':['line','rich'],
 'GH-woocommerce-woocommerce-69438':['delivery','second'],
 'GH-woocommerce-woocommerce-69807':['stock_notification','webhook'],
}

def main():
    rows=list(csv.DictReader((ROOT/'data/issue_detail_review.csv').open()))
    results=[]
    for row in rows:
        url=row['url'].replace('https://github.com/','https://api.github.com/repos/')
        result={'evidence_id':row['evidence_id'],'url':url,'checked_at':datetime.now(timezone.utc).isoformat()}
        try:
            r=requests.get(url,timeout=20,headers={'User-Agent':'NinjaResearch/0.1 bounded issue review'})
            result['status']=r.status_code
            if r.ok:
                doc=r.json();text=doc.get('title','')+' '+(doc.get('body') or '')
                result['technical_markers']={key:key.lower() in text.lower() for key in MARKERS[row['evidence_id']]}
                result['scope']='source text only; bug not reproduced; author/contact/body not retained'
        except (requests.RequestException,ValueError) as e:result['error_type']=type(e).__name__
        results.append(result)
    (ROOT/'data/issue_review_verification.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__':main()
