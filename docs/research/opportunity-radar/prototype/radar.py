"""Offline, read-only analysis of minimized official API snapshots (stdlib only).
Network collection is a separate, bounded opt-in command. No outreach capability.
"""
import argparse
import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

SERVICES = [
    (r'\b(website|web design|web development|websites)\b', 'website and accessibility audit'),
    (r'\b(translation|localisation|localization|tłumacze\w*)\b', 'localization'),
    (r'\b(marketing|advertising|campaign|seo)\b', 'marketing and content'),
    (r'\b(catalogue|catalog|e-commerce|ecommerce)\b', 'catalog management'),
    (r'\b(automation|integration|software|digital)\b', 'integration or automation discovery'),
]


def flatten(value):
    if isinstance(value, dict):
        return ' | '.join(flatten(v) for v in value.values())
    if isinstance(value, list):
        return ' | '.join(flatten(v) for v in value)
    return str(value or '')


def date(value):
    # TED date-only values carry a timezone suffix; preserve the calendar date.
    if len(value) > 10 and value[10] in '+-':
        value = value[:10]
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    return result.replace(tzinfo=timezone.utc) if result.tzinfo is None else result


def normalize(source, payload):
    if source == 'fts':
        for r in payload['releases']:
            t = r.get('tender', {})
            yield dict(source=source, id=r['id'], entity_id=r['ocid'], company=r.get('buyer', {}).get('name', ''),
                       title=t.get('title', ''), published_at=r['date'], status=t.get('status', 'unknown'),
                       deadline=t.get('tenderPeriod', {}).get('endDate'), budget=t.get('value'),
                       source_url=r['url'], data_mode=r['data_mode'], notice_type=','.join(r.get('tag', [])))
    elif source == 'ted':
        for n in payload['notices']:
            identifier = n['publication-number']
            yield dict(source=source, id=identifier, entity_id=identifier, company=flatten(n.get('buyer-name')),
                       title=flatten(n.get('title-proc')), published_at=n['publication-date'],
                       status='unknown', deadline=flatten(n.get('deadline-receipt-tender-date-lot')) or None,
                       budget=None, source_url=f'https://ted.europa.eu/en/notice/-/detail/{identifier}',
                       data_mode=payload['data_mode'], notice_type=n.get('notice-type', 'unknown'))
    elif source == 'companies_house':
        if payload.get('data_mode') != 'synthetic_fixture':
            raise ValueError('Companies House live access is not implemented: key required')
        for n in payload['items']:
            yield dict(source=source, id=n['company_number'], entity_id=n['company_number'], company=n['company_name'],
                       title='Company incorporation (synthetic)', published_at=n['date_of_creation'], status='active',
                       deadline=None, budget=None, source_url=None, data_mode='synthetic_fixture', notice_type='incorporation')
    else:
        raise ValueError(source)


def fingerprint(record):
    return hashlib.sha256(json.dumps(record, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def classify(record, now):
    r = dict(record)
    service = next((s for pattern, s in SERVICES if re.search(pattern, r['title'], re.I)), None)
    age = (now - date(r['published_at'])).total_seconds() / 86400
    fixture = r['data_mode'] == 'synthetic_fixture'
    award = 'award' in r['notice_type'].lower() or r['notice_type'].startswith('can-') or r['status'] == 'complete'
    tender = r['status'] == 'active' or r['notice_type'].startswith('cn-')
    expired = False
    if r['deadline']:
        try:
            expired = date(r['deadline']) <= now
        except ValueError:
            r['deadline_requires_review'] = True
    if fixture:
        demand, reason = 'weak_indirect', 'Synthetic incorporation does not establish a business need'
    elif award or expired or r['status'] in ('cancelled', 'unsuccessful', 'withdrawn'):
        demand, reason = 'false_positive', 'Award, closed, cancelled or expired: no open procurement established'
    elif tender and service:
        demand, reason = 'confirmed_demand', 'Official procurement exists; supplier fit and lot scope remain unverified'
    elif service:
        demand, reason = 'probable_need', 'Relevant title only; stage and scope require verification'
    else:
        demand, reason = 'weak_indirect', 'No specific service supported by the title'
    fresh = 0 <= age <= 14
    score = (25 if r['source_url'] else 0) + (15 if fresh else 0) + (20 if service else 0) + (20 if demand == 'confirmed_demand' else 0)
    if fixture or demand == 'false_positive':
        score = 0
    r.update(service=service, demand_class=demand, classification_reason=reason, age_days=round(age, 2),
             quality_score=score, score_is_probability=False, event='incorporation' if fixture else 'procurement_notice',
             contact_channel='not_verified', contact_permission=False, outreach_ready=False,
             verification_required=['scope and lots', 'eligibility and capacity', 'deadline', 'official submission route', 'country/channel rules'])
    return r


def run(inputs, previous, now):
    records, seen, duplicates, conflicts = [], {}, 0, 0
    for source, payload in inputs:
        for record in normalize(source, payload):
            key = source + ':' + record['id']
            digest = fingerprint(record)
            if key in seen:
                duplicates += 1
                conflicts += seen[key] != digest
                continue
            seen[key] = digest
            r = classify(record, now)
            r['change'] = 'baseline_observation' if not previous else ('newly_observed' if key not in previous else ('changed' if previous[key] != digest else 'unchanged'))
            r['snapshot_key'] = key
            records.append(r)
    live = [r for r in records if r['data_mode'] != 'synthetic_fixture']
    metrics = {'records': len(records), 'live_records': len(live), 'synthetic_records': len(records)-len(live),
               'within_snapshot_duplicates': duplicates, 'conflicting_duplicates': conflicts,
               'cross_source_duplicates': 'not measured; no entity resolution',
               'source_link_present': sum(bool(r['source_url']) for r in live),
               'fresh_within_14_days': sum(0 <= r['age_days'] <= 14 for r in live),
               'specific_service_candidates': sum(bool(r['service']) for r in live),
               'confirmed_procurement_candidates': sum(r['demand_class'] == 'confirmed_demand' for r in live),
               'verified_lawful_contact_routes': 0, 'outreach_ready': 0,
               'false_positive_rate': 'not measured; requires independently reviewed ground truth',
               'manual_review_minutes': 'not measured', 'event_detection_latency': 'not measured; one snapshot'}
    return records, seen, metrics


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data', type=Path, default=Path(__file__).resolve().parents[1]/'data')
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--previous', type=Path)
    p.add_argument('--as-of', default=datetime.now(timezone.utc).isoformat())
    args = p.parse_args()
    inputs = [(s, json.loads((args.data/f'{s}.json').read_text())) for s in ('fts', 'ted', 'companies_house')]
    prev = json.loads(args.previous.read_text()) if args.previous else {}
    records, state, metrics = run(inputs, prev, date(args.as_of))
    args.out.mkdir(parents=True, exist_ok=True)
    for name, data in [('events', records), ('state', state), ('benchmark', metrics)]:
        (args.out/f'{name}.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    fields = ['source','id','company','title','published_at','source_url','data_mode','change','demand_class','service','quality_score','contact_channel','outreach_ready']
    with (args.out/'events.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore', lineterminator='\n');writer.writeheader()
        for record in records:
            record = {k: re.sub(r'\s+', ' ', v).strip() if isinstance(v, str) else v for k, v in record.items()}
            # Prevent formula injection when CSV is opened in spreadsheet software.
            writer.writerow({k: "'"+str(v) if isinstance(v, str) and v.startswith(('=', '+', '-', '@')) else v for k,v in record.items() if k in fields})
    print(json.dumps(metrics, indent=2))


if __name__ == '__main__':
    main()
