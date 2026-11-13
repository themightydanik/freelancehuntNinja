"""Bounded, unauthenticated read-only probes; retain structure, not contact data.

Run from checkout: python research/probes/http_probe.py
No source-code credentials, retries, CAPTCHA solving or authenticated writes.
"""
import concurrent.futures
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[2]
LIMIT = 350_000
TARGETS = [
    ("S01", "https://data.gov.ua/api/3/action/package_search?rows=2", None),
    ("S02", "https://public.api.openprocurement.org/api/2.5/tenders?limit=2", None),
    ("S03", "https://api.spending.gov.ua/api/v2/api/transactions/top100?region=26", None),
    ("S04", "https://usr.minjust.gov.ua/", None),
    ("S05", "https://e-construction.gov.ua/", None),
    ("S06", "https://sis.nipo.gov.ua/uk/search/simple/", None),
    ("S07", "https://data.lvivcity.gov.ua/api/3/action/package_search?rows=2", None),
    ("S08", "https://data.kyivcity.gov.ua/api/3/action/package_search?rows=2", None),
    ("S09", "https://api.ted.europa.eu/v3/notices/search", {"query":"publication-date >= 20260101", "limit":2, "fields":["publication-number","publication-date","notice-title"]}),
    ("S10", "https://cordis.europa.eu/about/dataextractions", None),
    ("S11", "https://data.europa.eu/api/hub/search/search?query=energy&limit=2", None),
    ("S12", "https://api.company-information.service.gov.uk/search/companies?q=software&items_per_page=2", None),
    ("S13", "https://api.github.com/repos/supabase/supabase/issues?state=open&per_page=2", None),
    ("S13p2", "https://api.github.com/repos/supabase/supabase/issues?state=open&per_page=2&page=2", None),
    ("S14", "https://api.wordpress.org/plugins/info/1.2/?action=query_plugins&request[search]=telegram&request[per_page]=2&request[page]=1", None),
    ("S14p2", "https://api.wordpress.org/plugins/info/1.2/?action=query_plugins&request[search]=telegram&request[per_page]=2&request[page]=2", None),
    ("S15", "https://api.worldbank.org/v2/country/UA/indicator/IT.NET.USER.ZS?format=json&per_page=2", None),
    ("S16", "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_pjan?geo=UA&time=2023&sex=T&age=TOTAL", None),
    ("S17", "https://api.gleif.org/api/v1/lei-records?page[size]=2&filter[entity.legalAddress.country]=UA", None),
    ("S18", "https://www.contractsfinder.service.gov.uk/Published/Notices/OCDS/Search?limit=2", None),
    ("S19", "https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages?limit=2", None),
    ("S20", "https://hds.healdata.eu/", None),
    ("S21", "https://api.crossref.org/works?filter=type:grant&rows=2", None),
    ("S22", "https://api.openalex.org/works?filter=institutions.country_code:ua&per-page=2", None),
    ("S23", "https://api.npmjs.org/downloads/point/last-week/@supabase/supabase-js", None),
    ("S24", "https://pypi.org/pypi/groq/json", None),
    ("S25", "https://api.freelancehunt.com/v2/projects", None),
    ("S26", "https://www.wikidata.org/wiki/Special:EntityData/Q212.json", None),
    ("S27", "https://api.data.gov/ed/collegescorecard/v1/schools?per_page=1", None),
    ("S28", "https://api.energidataservice.dk/dataset/Elspotprices?limit=2", None),
    ("S29", "https://www.data.gouv.fr/api/1/datasets/?q=sirene&page_size=2", None),
    ("S30", "https://api.patentsview.org/patent/?q=%7B%22patent_id%22:%227861317%22%7D", None),
]

def shape(value, depth=0):
    if depth > 4:
        return type(value).__name__
    if isinstance(value, dict):
        return {str(k): shape(v, depth+1) for k,v in list(value.items())[:40]}
    if isinstance(value, list):
        return {"type":"array", "length":len(value), "item":shape(value[0],depth+1) if value else None}
    return type(value).__name__

def probe(target):
    sid,url,payload = target
    start=time.perf_counter()
    out={"source_id":sid, "url":url, "method":"POST" if payload else "GET",
         "payload":payload, "checked_at":datetime.now(timezone.utc).isoformat(),
         "authentication":"none", "byte_cap":LIMIT}
    try:
        with requests.request(out["method"],url,json=payload,stream=True,timeout=(10,25),
                              headers={"User-Agent":"NinjaResearch/0.1 (bounded read-only feasibility study)", "Accept":"application/json"}) as r:
            body=bytearray()
            for part in r.iter_content(8192):
                body.extend(part)
                if len(body)>LIMIT: break
            clipped=len(body)>LIMIT
            raw=bytes(body[:LIMIT])
            out.update(status=r.status_code,content_type=r.headers.get("Content-Type"),
                       elapsed_seconds=round(time.perf_counter()-start,3),
                       bytes_read=len(body),truncated=clipped,
                       response_sha256=hashlib.sha256(raw).hexdigest(),
                       pagination_header_present=bool(r.headers.get("Link")),
                       retry_after=r.headers.get("Retry-After"),
                       rate_remaining=r.headers.get("X-RateLimit-Remaining"))
            try:
                doc=json.loads(raw)
                out["anonymized_example"]=shape(doc)
                out["valid_json"]=True
                if isinstance(doc,dict):
                    out["pagination_fields"]=[k for k in doc if k.lower() in ("next_page","links","meta","info","pagination","total","count","next")]
                    if sid.startswith("S14"):
                        out["pagination_metadata"]=doc.get("info")
                        out["useful_field_presence"]={k:sum(k in p for p in doc.get("plugins",[])) for k in ("slug","last_updated","tested","active_installs","requires","version")}
                    if sid=="S02":
                        out["page_record_count"]=len(doc.get("data",[]))
                        out["cursor_present"]=bool(doc.get("next_page",{}).get("offset"))
                elif isinstance(doc,list): out["page_record_count"]=len(doc)
            except (ValueError,UnicodeDecodeError):
                out["valid_json"]=False
            out["outcome"]="json_sample" if out["valid_json"] and r.ok else "http_error" if not r.ok else "html_only_not_api_validation"
    except requests.RequestException as e:
        out.update(outcome="transport_error", error_type=type(e).__name__, elapsed_seconds=round(time.perf_counter()-start,3))
    return out

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results=list(pool.map(probe,TARGETS))
    (ROOT/"data/source_probe_results.json").write_text(json.dumps({"scope":"one bounded request per target; two pages only for S13/S14; no retries", "results":results},ensure_ascii=False,indent=2)+"\n")
    for r in results: print(r["source_id"],r.get("status"),r["outcome"],r["elapsed_seconds"])

if __name__=="__main__": main()
