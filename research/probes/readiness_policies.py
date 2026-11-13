"""Read-only official help/fee pages; native public help JSON when HTML is a shell.
Keep short policy excerpts, never account data. Does not test KYC or payouts.
"""
import concurrent.futures
import hashlib
import json
import re
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlparse
import requests
from policy_pages import Text

ROOT=Path(__file__).resolve().parents[2]

def fetch(row):
    out=dict(row,checked_at=datetime.now(timezone.utc).isoformat())
    if row.get('automation_gate')=='manual_owner_review_only' or (urlparse(row['url']).hostname or '').endswith('freelancer.com'):
        return dict(out,status='not_requested',reason='Automated access requires platform permission; manual owner review only')
    try:
        with requests.get(row['url'],stream=True,timeout=(10,25),headers={'User-Agent':'NinjaResearch/0.2 bounded official-policy review'}) as r:
            body=bytearray()
            for b in r.iter_content(8192):
                body.extend(b)
                if len(body)>900_000:break
            out.update(status=r.status_code,bytes=len(body),truncated=len(body)>900_000,sha256=hashlib.sha256(body).hexdigest(),final_url=r.url)
            html=bytes(body[:900_000]).decode(errors='replace')
            if 'api/v2/help_center' in row['url'] and r.ok:
                d=json.loads(html).get('article',{});html=d.get('body','')
                out['article_title']=d.get('title');out['public_article_url']=d.get('html_url')
            parser=Text();parser.feed(html)
            lines=[re.sub(r'\s+',' ',x).strip() for x in ''.join(parser.parts).splitlines() if x.strip()]
            text='\n'.join(lines)
            Path('/tmp/ninja-readiness-policies').mkdir(exist_ok=True)
            Path('/tmp/ninja-readiness-policies',row['id']+'.txt').write_text(text)
            out['excerpts']=[x[:450] for x in lines if re.search(r'Ukraine|Ukrain|Укра|\$|€|%|eligible|countr|вериф|комісі|вивед|профіл|payment|bank|free|approval|discover|review',x,re.I) and not re.search(r'\S+@\S+',x)][:40]
    except (requests.RequestException,ValueError) as e:out['error_type']=type(e).__name__
    return out

def main():
    targets=json.loads((ROOT/'research/probes/readiness_policy_targets.json').read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(fetch,targets))
    (ROOT/'data/readiness_policy_checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    for r in results:print(r['id'],r.get('status',r.get('error_type')),r.get('article_title',''))

if __name__=='__main__':main()
