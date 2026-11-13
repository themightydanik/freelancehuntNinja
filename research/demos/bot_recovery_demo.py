"""Offline synthetic Telegram-style recovery rehearsal. No bot/API/network client.

Failure: an inherited allowed_updates filter drops callback_query approvals.
Rollback intentionally restores the pre-fix broken snapshot, then fix is reapplied.
"""
import copy
import hashlib
import html
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def digest(state):
    return hashlib.sha256(json.dumps(state,sort_keys=True).encode()).hexdigest()

def new_state():
    return {'allowed_updates':['message'], 'processed_update_ids':[], 'synthetic_effects':[], 'dropped_types':[]}

def receive(state,update):
    if update['type'] not in state['allowed_updates']:
        state['dropped_types'].append(update['type']);return 'filtered_before_handler'
    if update['update_id'] in state['processed_update_ids']:return 'duplicate_skipped'
    state['processed_update_ids'].append(update['update_id'])
    if update['type']=='callback_query':state['synthetic_effects'].append({'action':'record_mock_approval','fixture':'demo-order-1'})
    return 'accepted_locally'

def diagnose(state):
    return {'root_cause':'callback_query excluded by synthetic allowed_updates filter',
            'supported': 'callback_query' not in state['allowed_updates'],
            'required_change':'Include callback_query; verify unique update processing',
            'production_caveat':'A similar symptom can have other causes; no real Telegram incident diagnosed'}

def repair(state):
    state['allowed_updates']=sorted(set(state['allowed_updates'])|{'callback_query'})

def rehearse():
    state=new_state();update={'update_id':2002,'type':'callback_query','payload':'approve synthetic order'}
    failed=receive(state,update)
    assert failed=='filtered_before_handler' and not state['synthetic_effects']
    diagnosis=diagnose(state);assert diagnosis['supported']
    snapshot=copy.deepcopy(state);before=digest(snapshot)
    steps=[{'stage':'failure','expected':'callback filtered; zero effects','observed':failed,'state':copy.deepcopy(state)},
           {'stage':'diagnosis','expected':'missing update type identified','observed':diagnosis,'state':copy.deepcopy(state)}]
    repair(state);assert receive(state,update)=='accepted_locally'
    assert receive(state,update)=='duplicate_skipped' and len(state['synthetic_effects'])==1
    steps.append({'stage':'repair_and_replay','expected':'exactly one LOCAL mock effect','observed':'accepted once; duplicate skipped','state':copy.deepcopy(state)})
    state=copy.deepcopy(snapshot);assert digest(state)==before
    steps.append({'stage':'rollback','expected':'exact pre-fix snapshot, including broken filter','observed':'digest matches; this is NOT a healthy state','state':copy.deepcopy(state)})
    repair(state);assert receive(state,update)=='accepted_locally' and len(state['synthetic_effects'])==1
    steps.append({'stage':'final_recovery','expected':'repair reapplied and acceptance restored','observed':'one local mock approval','state':copy.deepcopy(state)})
    return {'scope':'offline synthetic state machine; no HTTP server, Telegram, deployment or real credentials',
            'fixture_update_id':2002,'network_calls':0,'real_messages':0,'paid_actions':0,
            'fault_reproduced':True,'diagnosis_verified':True,'repair_verified':True,'duplicate_skipped':True,
            'rollback_exact':True,'rollback_restores_broken_state':True,'final_recovered':True,
            'snapshot_digest':before,'steps':steps}

def main():
    import sys
    def no_network(event,args):
        if event.startswith('socket.'):raise RuntimeError('Network forbidden in offline demo')
    sys.addaudithook(no_network)
    result=rehearse()
    (ROOT/'data/bot_recovery_demo_report.json').write_text(json.dumps(result,indent=2)+'\n')
    target=ROOT/'docs/research/demo';target.mkdir(exist_ok=True)
    cards=''.join('<section><h2>'+html.escape(s['stage'])+'</h2><p>'+html.escape(s['expected'])+'</p><p><b>Observed:</b> '+html.escape(str(s['observed']))+'</p><pre>'+html.escape(json.dumps(s['state'],indent=2))+'</pre></section>' for s in result['steps'])
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bot recovery — offline synthetic rehearsal</title><style>body{font:17px system-ui;max-width:900px;margin:40px auto;padding:0 20px;color:#152337;background:#f4f7fb}section{background:white;padding:20px;margin:18px 0;border-radius:12px;border:1px solid #d1dbe7}pre{overflow:auto;font-size:14px}header{padding:20px;background:#dff3eb;border-radius:12px}h1{font-size:30px}</style><header><h1>Bot recovery rehearsal / Відновлення бота</h1><p><b>100% synthetic, offline research artifact; not hosted.</b> No real Telegram account, messages, customer data, secrets or production changes.</p><p>A working-looking bot can silently lose approval clicks. This rehearsal shows a failed update filter, diagnosis, a minimal repair, duplicate handling, an exact rollback, and final recovery.</p></header>'''+cards+'''<section><h2>What a real service would verify</h2><p>One agreed incident, client authorization, staging access, reproducible acceptance, a reversible change and a written handover. This demonstration is not a customer case, a security audit, cloud deployment evidence, or an SLA.</p><p>Rollback here returns to the pre-fix broken snapshot to prove reversibility; final recovery explicitly reapplies the fix. Local idempotency is not an exactly-once guarantee for external APIs.</p></section></html>'''
    (target/'BOT_RECOVERY_DEMO.html').write_text(page+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='steps'},indent=2))

if __name__=='__main__':main()
