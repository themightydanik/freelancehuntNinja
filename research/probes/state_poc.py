"""Local synthetic SQLite POC only. No cloud deployment or external effects."""
import hashlib
import json
import sqlite3

def identity(scheme,identifier):
    if not scheme or not identifier:
        return None  # Never join entities on a missing identifier or name similarity.
    return scheme.upper()+':'+identifier.strip().upper()

def connect():
    db=sqlite3.connect(':memory:')
    db.executescript('''
      CREATE TABLE versions(source TEXT,record_id TEXT,digest TEXT,payload TEXT,
        PRIMARY KEY(source,record_id,digest));
      CREATE TABLE checkpoints(source TEXT PRIMARY KEY,cursor TEXT);
      CREATE TABLE budget(id INTEGER PRIMARY KEY CHECK(id=1),remaining REAL CHECK(remaining>=0));
      INSERT INTO budget VALUES(1,1.0);
    ''')
    return db

def ingest(db,source,cursor,records,fail=False):
    with db:
        for record in records:
            payload=json.dumps(record,sort_keys=True,separators=(',',':'))
            digest=hashlib.sha256(payload.encode()).hexdigest()
            db.execute('INSERT OR IGNORE INTO versions VALUES(?,?,?,?)',
                       (source,record['id'],digest,payload))
        if fail: raise RuntimeError('synthetic crash before checkpoint')
        db.execute('INSERT INTO checkpoints VALUES(?,?) ON CONFLICT(source) DO UPDATE SET cursor=excluded.cursor',(source,cursor))

def reserve(db,estimated_cost):
    if estimated_cost<0: raise ValueError('negative reservation')
    with db:
        cur=db.execute('UPDATE budget SET remaining=remaining-? WHERE id=1 AND remaining>=?',(estimated_cost,estimated_cost))
        return cur.rowcount==1

def main():
    db=connect(); records=[{'id':'synthetic-1','organization_id':None,'status':'open'}]
    ingest(db,'fixture','c1',records);ingest(db,'fixture','c1',records)
    assert db.execute('SELECT COUNT(*) FROM versions').fetchone()[0]==1
    ingest(db,'fixture','c2',[dict(records[0],status='changed')])
    assert db.execute('SELECT COUNT(*) FROM versions').fetchone()[0]==2
    try:ingest(db,'fixture','c3',[{'id':'synthetic-2'}],fail=True)
    except RuntimeError:pass
    assert db.execute('SELECT cursor FROM checkpoints').fetchone()[0]=='c2'
    assert db.execute('SELECT COUNT(*) FROM versions').fetchone()[0]==2
    assert identity('ua-edr',' 00001234 ')=='UA-EDR:00001234'
    assert identity('',None) is None
    assert reserve(db,.8) and not reserve(db,.3)
    result={'scope':'local synthetic SQLite; not Supabase/Edge deployment validation',
            'idempotent_replay':True,'history_preserved':True,'checkpoint_rollback':True,
            'missing_identity_not_merged':True,'leading_zero_identifier_preserved':True,
            'budget_reservation_refused_over_cap':True,'real_ai_calls':0}
    from pathlib import Path
    (Path(__file__).resolve().parents[2]/'data/state_poc_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
