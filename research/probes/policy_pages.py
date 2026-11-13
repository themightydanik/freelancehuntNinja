"""Fetch bounded official policy/product pages, retain titles and numeric excerpts.

HTTP success proves retrieval only. Read excerpts in context before making claims.
No login, scraping pagination, or challenge bypass. Cached files are local /tmp only.
"""
import concurrent.futures
import hashlib
import json
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
import requests
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[2]

class Text(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style','noscript'): self.skip+=1
        if tag in ('p','div','h1','h2','h3','li','tr','br'): self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag in ('script','style','noscript'): self.skip=max(0,self.skip-1)
    def handle_data(self,data):
        if not self.skip: self.parts.append(data)

def fetch(row):
    result=dict(row,checked_at=datetime.now(timezone.utc).isoformat())
    if (urlparse(row['url']).hostname or '').endswith('freelancer.com'):
        return dict(result,status='not_requested',reason='Section33 requires express written permission; manual review only')
    try:
        with requests.get(row['url'],stream=True,timeout=(10,20),headers={'User-Agent':'NinjaResearch/0.1 bounded official-page review'}) as r:
            body=bytearray()
            for b in r.iter_content(8192):
                body.extend(b)
                if len(body)>600_000: break
            result.update(status=r.status_code,bytes_read=len(body),truncated=len(body)>600_000,
                          final_url=r.url,sha256=hashlib.sha256(body).hexdigest())
            p=Text(); p.feed(bytes(body[:600_000]).decode('utf-8',errors='replace'))
            text='\n'.join(re.sub(r'\s+',' ',x).strip() for x in ''.join(p.parts).splitlines() if x.strip())
            candidates=[line[:500] for line in text.splitlines() if re.search(r'\$|€|%|free|Free|Ukraine|Ukrain|minute|credit|GDPR|licen[cs]e|commercial|rate limit|bid|Bid',line)][:16]
            result['excerpts']=[line for line in candidates if len(line)<=220
                and not re.search(r'@|\b\d{1,3}(?:\.\d{1,3}){3}\b',line)
                and re.search(r'\d|GDPR|license|licence',line,re.I)]
            result['excerpt_policy']='Short quantitative policy/pricing text only; not a full-page validation'
            result['retrieval_only']=True
            Path('/tmp/ninja-policy-pages').mkdir(exist_ok=True)
            Path('/tmp/ninja-policy-pages',row['id']+'.txt').write_text(text)
    except requests.RequestException as e: result['error_type']=type(e).__name__
    return result

def main():
    rows=json.loads((ROOT/'research/probes/policy_targets.json').read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(fetch,rows))
    (ROOT/'data/policy_page_checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    for r in results: print(r['id'],r.get('status',r.get('error_type')),r.get('truncated'))

if __name__=='__main__': main()
