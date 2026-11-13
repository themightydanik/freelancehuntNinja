"""Import with synthetic credentials, deny networking; report behavior, no live bot.
Run with application venv, from checkout root. Does not modify the application.
"""
import importlib.util
import json
import os
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]

def main():
    os.environ.update(TELEGRAM_BOT_TOKEN='123456:local-research-placeholder',
                      FREELANCEHUNT_TOKEN='local-research-placeholder',GROQ_API_KEY='',CHAT_ID='0')
    with patch('requests.sessions.Session.request',side_effect=AssertionError('External HTTP forbidden in audit')):
        spec=importlib.util.spec_from_file_location('audited_bot',ROOT/'freelancehuntNinja.py')
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
        mod.flask_app.config['TESTING']=True
        with mod.flask_app.test_client() as client,patch.object(mod.bot,'send_message') as send:
            neutral=client.post('/callback',json={'status':'audit-neutral'})
            assert neutral.status_code==200 and neutral.json=={'status':'ok'}
            assert send.call_count==0
            before=mod.daily_bids
            forged=client.post('/callback',json={'status':'success'})
            assert forged.status_code==200 and mod.daily_bids==before+1 and send.call_count==1
            # This mocked send proves missing callback authorization, not Telegram access.
            result={'synthetic_credentials':True,'outbound_http_denied':True,'neutral_callback_200':True,
                    'unauthenticated_success_callback_mutates_counter':True,
                    'unauthenticated_callback_attempts_mocked_notification':True,
                    'telegram_delivery_or_bidding_validated':False,'mac_server_present_in_repository':False}
    (ROOT/'data/repository_smoke_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
