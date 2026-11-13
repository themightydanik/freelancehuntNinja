#!/usr/bin/env python3
"""Offline threshold arithmetic; no conversion, retention or CAC forecasts."""
from pathlib import Path
import csv,json,math
R=Path(__file__).resolve().parents[1];D=R/'data'
def write(name,rows):
 with (D/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
# These inputs describe proposed economics, never an accepted quote or platform guarantee.
models=[
 dict(id='B2B_FIXED',price=450,period=1,build_h=24,entry_cash=0,release='1–2weeks preparation; buyer/acceptance lag UNKNOWN',fee=.06,flat=.5,partner=.20,refund=.03,direct=8,monthly_h_per_customer=8,fixed_h=16,fixed_cash=20),
 dict(id='B2B_LICENSE',price=79,period=1,build_h=80,entry_cash=0,release='3–6weeks at20–30h/week; no distribution proven',fee=.06,flat=.5,partner=.20,refund=.03,direct=2,monthly_h_per_customer=.5,fixed_h=20,fixed_cash=20),
 dict(id='MOBILE_SUB',price=4.99,period=1,build_h=100,entry_cash=25,release='3–5weeks coding at25h/week + review/testing; iOS adds99/year/hardware UNKNOWN',fee=.15,flat=0,partner=0,refund=.03,direct=.10,monthly_h_per_customer=.03,fixed_h=24,fixed_cash=30),
 dict(id='CHROME_SUB',price=5,period=1,build_h=60,entry_cash='UNKNOWN CWS fee',release='2–4weeks at20–30h/week + review; PSP gate',fee=.06,flat=.5,partner=0,refund=.03,direct=.05,monthly_h_per_customer=.03,fixed_h=20,fixed_cash=20),
 dict(id='PLUGIN_FREEMIUM',price=49,period=12,build_h=100,entry_cash=0,release='3–5weeks code + compatibility and directory review UNKNOWN',fee=.06,flat=.5,partner=0,refund=.03,direct=.10,monthly_h_per_customer=.04,fixed_h=24,fixed_cash=20),
]
# Ads modeled separately: rate is publisher revenue per1000delivered impressions, no store IAP fee.
inputs={'date':'2026-11-13','labor_rate':25,'models':models,'hybrid':{'agency_monthly':149,'retail_annual':49,'agency_gross_target_fraction':.5,'build_h':120,'partner_share_on_agency':.20},'notice':'All commercial inputs ASSUMED; tax, actual CAC, conversion, retention, bank payout UNKNOWN. No API calls.'}
(D/'model_inputs.json').write_text(json.dumps(inputs,ensure_ascii=False,indent=2)+'\n')
rows=[]
for m in models:
 for goal in [500,2000,5000]:
  n=math.ceil(goal/(m['price']/m['period']));gross=n*m['price']/m['period']
  collected=gross*(1-m['refund']);fee=collected*m['fee']+n*m['flat']/m['period'];partner=collected*m['partner']
  cash=collected-fee-partner;direct=n*m['direct'];contribution=cash-direct-m['fixed_cash']
  h=m['fixed_h']+n*m['monthly_h_per_customer'];labor=h*25
  rows.append(dict(model=m['id'],target_gross=goal,customers_or_active_annual_licenses=n,unit_price=m['price'],billing_period_months=m['period'],recognized_monthly_gross=round(gross,2),conditional_cash_monthly_equivalent=round(cash,2),all_customers_billed_now_cash=round(cash*m['period'],2),direct_monthly=round(direct,2),fixed_cash=m['fixed_cash'],contribution=round(contribution,2),owner_hours=round(h,2),owner_labor=round(labor,2),economic_profit_before_tax_fx_acquisition=round(contribution-labor,2),initial_build_h=m['build_h'],initial_labor_value=m['build_h']*25,initial_cash=m['entry_cash'],release=m['release'],actual_collected_revenue='UNKNOWN',cac_conversion_retention='UNKNOWN',tax_fx_bank='UNKNOWN',scope='Threshold capacity; not forecast; annual billing timing not MRR bank deposits'))
# Hybrid: one core, two different buyer populations; no double-counting same site/agency.
for goal in [500,2000,5000]:
 na=math.ceil(goal*.5/149);nr=math.ceil(goal*.5/(49/12));gross=na*149+nr*49/12
 collected=gross*.97;psp=collected*.06+na*.5+nr*.5/12;partner=na*149*.97*.20
 cash=collected-psp-partner;direct=na*3+nr*.1;h=24+na*1+nr*.04;contrib=cash-direct-30
 rows.append(dict(model='HYBRID',target_gross=goal,customers_or_active_annual_licenses=f'{na} agencies + {nr} distinct retail licenses',unit_price='149/mo agency +49/year retail',billing_period_months='mixed',recognized_monthly_gross=round(gross,2),conditional_cash_monthly_equivalent=round(cash,2),all_customers_billed_now_cash='UNKNOWN mixed renewal schedule',direct_monthly=round(direct,2),fixed_cash=30,contribution=round(contrib,2),owner_hours=round(h,2),owner_labor=round(h*25,2),economic_profit_before_tax_fx_acquisition=round(contrib-h*25,2),initial_build_h=120,initial_labor_value=3000,initial_cash=0,release='4–6weeks at25–30h/week plus review; not both wrappers at once',actual_collected_revenue='UNKNOWN',cac_conversion_retention='UNKNOWN',tax_fx_bank='UNKNOWN',scope='50/50 gross split arbitrary sensitivity; disjoint buyers; not guaranteed synergy'))
write('financial_thresholds.csv',rows)
ads=[]
for goal in [500,2000,5000]:
 for ecpm in [.2,1,5,10]:
  im=math.ceil(goal*1000/ecpm)
  for perday in [1,2,5]:
   dau=math.ceil(im/(30*perday))
   for sticky in [.1,.2,.4]:
    mau=math.ceil(dau/sticky);h=24+mau*.001 # owner hours/customer illustrative
    ads.append(dict(model='MOBILE_ADS',target_publisher_revenue=goal,assumed_net_ecpm=ecpm,delivered_impressions_month=im,delivered_ads_per_dau_day_assumed=perday,required_dau=dau,dau_mau_ratio_assumed=sticky,required_mau=mau,assumed_infra_monthly=30,owner_hours_assumed=round(h,2),economic_profit_before_tax_fx_acquisition=round(goal-30-h*25,2),initial_build_h_assumed=100,initial_labor_value=2500,entry_cash_android=25,actual_collected_revenue='UNKNOWN',ecpm_status='Sensitivity only; historical benchmark separate; ad-network deductions included only if net definition holds',fees='No store IAP commission on ad revenue; mediation fees/invalid-traffic deductions UNKNOWN'))
write('advertising_thresholds.csv',ads)
funnel=[]
for row in rows:
 if row['model']=='HYBRID':continue
 n=row['customers_or_active_annual_licenses']
 for conv in [.005,.02,.05]:
  funnel.append(dict(model=row['model'],target_gross=row['target_gross'],payers=n,assumed_qualified_or_activated_to_paid=conv,required_qualified_or_activated=math.ceil(n/conv),unit='qualified B2B opportunities' if row['model'].startswith('B2B') else 'activated users',channel_evidence='UNKNOWN volume; no success probability inferred'))
write('conversion_thresholds.csv',funnel)
ret=[]
for n in [100,401,490,26]:
 for churn in [.02,.05,.10,.20]:
  ret.append(dict(active_customers=n,monthly_churn_assumed=churn,expected_replacements=n*churn,whole_replacements=math.ceil(n*churn),retained_after6months_no_new=round(n*(1-churn)**6,2),status='Sensitivity only; not measured retention'))
write('retention_sensitivity.csv',ret)
sens=[]
for row in rows:
 if row['target_gross']!=2000:continue
 for rate in [10,25,40]:
  for acq in [0,100,500,1000]:
   sens.append(dict(model=row['model'],labor_rate=rate,monthly_acquisition_cash_assumed=acq,economic_profit=round(row['contribution']-row['owner_hours']*rate-acq,2),revenue_after_tax='UNKNOWN',status='Acquisition spend sensitivity, no number of sales promised'))
write('economics_sensitivity.csv',sens)
md="""# Подписки и семь финансовых моделей

Все наши цены, часы, конверсии, churn и стоимость привлечения — ASSUMED или UNKNOWN. Цель таблиц — месячная gross revenue, не личный доход. Проверено 13 ноября 2026. Труд владельца $25/час; чувствительность $10/$25/$40. [Параметры](data/model_inputs.json), [расчёты](data/financial_thresholds.csv), [реклама](data/advertising_thresholds.csv).

| Модель | Для $500 gross | Для $2 000 gross | Для $5 000 gross | Создание: часы / стоимость труда |
|---|---:|---:|---:|---|
"""
for m in models:
 ns=[str(math.ceil(g/(m['price']/m['period']))) for g in [500,2000,5000]]
 md+=f"| {m['id']} | {ns[0]} | {ns[1]} | {ns[2]} | {m['build_h']}h / ${m['build_h']*25}; entry {m['entry_cash']} |\n"
md+="""| MOBILE_ADS | 100 000 показов | 400 000 показов | 1 000 000 показов | 100h / $2 500; Android entry $25; assumed net eCPM $5 |
| HYBRID | 2 агентства + 62 retail | 7 агентств + 245 retail | 17 агентств + 613 retail | 120h / $3 000; одно ядро, два непроверенных канала |

B2B_FIXED — количество новых работ по $450, а не подписчиков. B2B_LICENSE — действующие агентства по $79/месяц. MOBILE_SUB — $4.99/месяц; CHROME_SUB — $5/месяц. PLUGIN_FREEMIUM — действующие годовые лицензии по $49: $4.0833 monthly equivalent. Это 490 активных лицензий для $2k, а не 490 новых покупок каждый месяц. Annual cash нельзя называть повторным MRR без истории продлений.

### При цели $2 000 gross

| Модель | Расчётная gross | Cash monthly equivalent после reserve/fees/partner | Contribution после direct/fixed | Часы владельца | Economic profit до налогов/FX/CAC |
|---|---:|---:|---:|---:|---:|
"""
for x in rows:
 if x['target_gross']==2000:
  md+=f"| {x['model']} | {x['recognized_monthly_gross']} | {x['conditional_cash_monthly_equivalent']} | {x['contribution']} | {x['owner_hours']} | {x['economic_profit_before_tax_fx_acquisition']} |\n"
md+="""
Все cash-колонки — условный расчёт поступлений, не наблюдаемые деньги. Actual collected revenue во всех строках UNKNOWN. Formula: recognized gross = n × price / billing months; collected scenario = gross × (1 − refunds); fees = collected × fee + n × flat fee / billing months; partner = collected × partner share; contribution = collected − fees − partner − direct − fixed; economic profit = contribution − all modeled owner hours × hourly rate − acquisition cash.

PSP 6% + $0.50, partner share 20% и reserve возвратов 3% — стрессовые плановые допущения, не договоры. Direct costs $8/job, $2/agency, $0.10/mobile payer, $0.05/Chrome payer, $0.10/active plugin license monthly тоже ASSUMED; actual infrastructure/API bill UNKNOWN. Fixed reserves $20–30/month. Consumer prices предполагаются без VAT/sales tax; если налог включён в $4.99, proceeds ниже. UA FOP/резидентство/ЕСВ неизвестны → actual profit after tax UNKNOWN. Bank/FX, невозвратные комиссии, disputes и неизвестные лицензии могут ухудшить результат.

Стоимость разработки показана отдельно, не списывается повторно каждый месяц. При простой амортизации за шесть месяцев 100h × $25 уменьшают monthly economic profit ещё на $416.67; 120h — на $500. Поэтому положительная steady-state строка не означает возврат первоначального труда.

### Комиссии по каналам

Play [S03]: для обычных auto-renew subscriptions базовая модель 15% соответствует распространённому Play Billing пути. В первичной странице есть региональные изменения 2026 и деление new/existing installs для иных транзакций: не обобщаем 15% на все paid apps/regions. Apple 15% требует qualifying agreement/program; 30% — обязательный стресс-сценарий до подтверждения допуска. В рекламе IAP-комиссия не применяется автоматически к network revenue.

Woo Marketplace [S15] отдаёт vendor 70%; это не external WP checkout. В таблице PLUGIN_FREEMIUM использован **внешний WordPress premium add-on**, а не скрыто выгодная Woo Marketplace ставка. Shopify 2.9% processing и revenue-share eligibility [S16] также отдельны. Перед выбором магазина пересчитать его реальные terms, refunds и taxes. Для сравнения при одном и том же collected обороте увеличение процентной комиссии с6% до30% уменьшит proceeds на24% этого оборота; нельзя сохранить direct-channel margin.

### Труд, поддержка, churn

B2B_FIXED $450 предполагает <=8h delivery/support плюс16h monthly sales/admin. Genesis $400/10h не прошёл экономический gate. Новые цена/часы ещё не приняты: при10h вместо8h пять jobs добавляют $250 труда. Цена стала выше не потому, что покупатель согласился, а чтобы проверить другую экономику.

B2B_LICENSE support0.5h/account/month — steady-state допущение; новое onboarding неизвестно, добавлять1–4h/account для проверки. Неоплаченная поддержка free users не включена в базовую paid-table:10 000 free users ×0.005h/month =50h/$1 250 дополнительного труда. Если это необходимо для freemium, видимая software margin может исчезнуть.

[Удержание](data/retention_sensitivity.csv): при условном monthly churn5% у401 подписчика нужно около21 replacement buyers/month с округлением вверх; без новых покупок через6месяцев остаётся73.5% cohort. Это арифметика постоянного churn, не прогноз. Для annual renewals нужна годовая cohort-модель; нельзя считать monthly churn измерением годовых банковских счетов.

### Воронка и привлечение

[Conversion thresholds](data/conversion_thresholds.csv): mobile401 payers требуют20 050 activated users при условных2%; Chrome400 —20 000; plugin490 —24 500. При B2B close20% для5 работ нужны25 qualified opportunities; для26 agency licenses —130. Ни один найденный канал не доказал такой объём. Конкурентские installs не равны activation, paying или renewed users.

Фактические CAC/CPI UNKNOWN. [Sensitivity](data/economics_sensitivity.csv) вычитает monthly acquisition cash $0/$100/$500/$1 000, не обещая приобретённых покупателей. Для mobile один payer даёт примерно $4.99×.97×.85−.10−.03h×$25 = $3.26 monthly contribution до fixed. При условном churn10% упрощённый undiscounted contribution LTV≈$32.64 до fixed/onboarding/tax; это не validated LTV. При2% activated→paid соответствующий break-even cost/activated user≈$0.65. CPI — ещё другое событие и не может автоматически равняться этому ceiling.

Hybrid: $149/month agency +$49/year retail, условно50/50 gross. Группы покупателей раздельные; сайты, включённые в агентскую лицензию, повторно retail не считаются. Новые каналы могут увеличить поддержку и маркетинг быстрее выручки; synergy не доказана.

### Срок и капитал

2–4недели — приблизительно40–120 часов кода при20–30h/week, а не два опубликованных стабильных приложения. При40h/month100h разработки занимают2.5месяца, при80h —1.25, при120h —0.83 до review/testing. Play $25 [S04] и возможный12-tester/14-day gate [S02]; iOS $99/year плюс фактические hardware/cloud build costs UNKNOWN. CWS registration fee подтверждён, точная retrieved сумма UNKNOWN [S12].

$0 — только offline пакет и проверка доказательств; $100 может почти уйти на Apple membership или частично на Android entry до неизвестного трафика. $300/$1 000 — резерв, не обоснование строить и не гарантированное число установок. При отсутствии продаж revenue=$0, стоимость потерянного времени=actual hours×rate плюс потраченный cash. Первое зачисление UNKNOWN: app-store и AdMob cycles/thresholds [S08/S21/S22] не совпадают с recognized revenue month.
"""
(R/'06_SUBSCRIPTION_ECONOMICS.md').write_text(md)
print(json.dumps({'financial_rows':len(rows),'ad_rows':len(ads),'funnel_rows':len(funnel),'retention_rows':len(ret),'sensitivity_rows':len(sens)}))
