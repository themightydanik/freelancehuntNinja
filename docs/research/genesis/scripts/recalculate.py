#!/usr/bin/env python3
"""Offline threshold model. Inputs are assumptions, not measured forecasts."""
from pathlib import Path
import csv,json,math
R=Path(__file__).resolve().parents[1];D=R/'data'
cfg=json.loads((D/'model_inputs.json').read_text())
def write(name,rows):
 with (D/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=rows[0],lineterminator="\n");w.writeheader();w.writerows(rows)
def calc(c,n,refund=None,fee=None,labor=None):
 refund=cfg['refund'] if refund is None else refund;fee=cfg['fee'] if fee is None else fee;labor=cfg['labor_rate'] if labor is None else labor
 gross=n*c['price'];collected=gross*(1-refund);platform=collected*fee
 direct=n*c['direct_per_customer'];cash=collected-platform-cfg['withdrawal']
 contribution=cash-direct-cfg['fixed_monthly'];hours=cfg['sales_hours']+n*(c['delivery_h']+c['support_h'])
 return dict(candidate_id=c['id'],customers=n,price_assumed=c['price'],gross_revenue=round(gross,2),refund_or_noncollection_reserve=round(gross-collected,2),collected_before_fees_assumed=round(collected,2),platform_fee=round(platform,2),cash_after_platform_and_withdrawal=round(cash,2),direct_cash=direct,fixed_cash=cfg['fixed_monthly'],contribution_after_direct_fixed=round(contribution,2),gross_margin_after_direct_fraction=round((collected-direct)/collected,4) if collected else 0,contribution_margin_fraction=round(contribution/gross,4) if gross else 0,owner_delivery_h=n*c['delivery_h'],owner_support_h=n*c['support_h'],owner_sales_admin_h=cfg['sales_hours'],owner_total_h=hours,owner_labor_value=round(hours*labor,2),economic_profit_before_tax_fx=round(contribution-hours*labor,2),actual_tax='UNKNOWN',actual_net_after_tax='UNKNOWN',time_to_bank_cash='UNKNOWN; approval/security lag plus withdrawal',status='ASSUMED threshold; no observed own revenue')
rows=[calc(c,math.ceil(cfg['target_gross']/c['price'])) for c in cfg['candidates']];write('unit_economics.csv',rows)
funnel=[]
for c in cfg['candidates']:
 n=math.ceil(2000/c['price'])
 for close in [.05,.10,.20]:
  q=math.ceil(n/close)
  for qv in [.01,.05,.10]:
   funnel.append(dict(candidate_id=c['id'],sales_required=n,qualified_close_assumed=close,qualified_inquiries_required=q,qualified_per_visit_assumed=qv,targeted_visits_required=math.ceil(q/qv),channel_volume_evidence='UNKNOWN; no channel proven to supply required volume'))
write('funnel_sensitivity.csv',funnel)
sens=[]
for c in cfg['candidates']:
 for refund in [0,.05,.15]:
  for fee in [0,.10,.15]:
   for labor in [10,25,40]:
    r=calc(c,math.ceil(2000/c['price']),refund,fee,labor);sens.append(dict(candidate_id=c['id'],refund=refund,fee=fee,labor_rate=labor,economic_profit_before_tax_fx=r['economic_profit_before_tax_fx']))
write('economics_sensitivity.csv',sens)
grid=[]
for c in cfg['candidates']:
 for budget in [0,100,300,1000]:
  for h in [40,80,120]:
   for day in [30,90,180]:
    months=day//30;start=c['initial_h'] if day==30 else 0
    maxn=max(0,math.floor((h-start-cfg['sales_hours'])/(c['delivery_h']+c['support_h'])))
    need=math.ceil(2000/c['price']);no_sales_cash=months*cfg['fixed_monthly']+c['initial_cash']
    grid.append(dict(candidate_id=c['id'],budget_usd=budget,hours_per_month=h,day=day,initial_hours=c['initial_h'],initial_labor_value=c['initial_h']*cfg['labor_rate'],monthly_capacity_customers=maxn,capacity_gross=maxn*c['price'],target_customers=need,target_capacity_pass=maxn>=need,no_sales_cash_burn=no_sales_cash,planned_no_sales_runway_pass=budget>=no_sales_cash,free_preparation_possible=True,acquisition_or_revenue_forecast='UNKNOWN; capacity only',recurring_cohort='UNKNOWN; not assumed to exist',zero_budget_limit='No paid infrastructure before funded scope; optional free mode not a verified production plan'))
write('budget_time_scenarios.csv',grid)
churn=[]
for c in cfg['candidates']:
 if c['recurring']:
  n=math.ceil(2000/c['price'])
  for x in [0,.05,.10,.20]:
   churn.append(dict(candidate_id=c['id'],active_customers=n,churn=x,expected_replacements_per_month=n*x,whole_customer_replacement_planning=math.ceil(n*x),mrr_lost_if_no_replacement=round(n*x*c['price'],2),six_month_retained_fraction_no_acquisition=round((1-x)**6,4),new_customer_onboarding_hours='UNKNOWN; extra to steady-state delivery hours'))
write('churn_sensitivity.csv',churn)
md='''# Unit economics — пороги, а не прогноз

Все цены наших пакетов, часы, tool allocation и conversions — ASSUMED: [inputs](data/model_inputs.json), [assumptions](data/assumptions.csv). Чужие тарифы — [evidence](data/evidence_registry.csv). Параметры не подгонялись вероятностной симуляцией. Цель здесь $2 000 **месячной gross revenue**, не cumulative и не net owner income.

Стоимость первой версии — только bounded offline preparation: C01 16h/$400 labor; C02 20h/$500; C03 24h/$600; C04 24h/$600; C05 32h/$800; C06 16h/$400 при $25/h. Cash initial $0 предполагает имеющийся компьютер/инструменты и отсутствие paid registration. Infrastructure reserve $20/month и direct allocation $8/$10/$14/$10/$10/$8 per customer — planning assumptions, не vendor quotes. Production/security/SLA и неизвестные лицензии не входят: product build пока не разрешён экономикой. Срок подготовки при 40/80/120h monthly для C01: около 12/6/4 календарных дней при равномерном распределении; это не срок продажи.

Формулы: gross=n×price; collected-reserve=gross×(1−refund); fee=collected×fee_rate; cash-after-platform=collected−fee−withdrawal; contribution=cash−direct−fixed; owner labor=(delivery+support+sales/admin)×rate; economic profit=contribution−labor. Refund reserve здесь консервативно включает noncollection; actual timing UNKNOWN. Cash received на банк **не наблюдался**, строки cash в CSV — рассчитанный сценарий поступления. Fees applied after refunded amount — упрощение; невозвратные комиссии/chargeback fee могут ухудшить результат.

| Candidate | n для ≥$2k | Gross | Cash after platform/withdrawal | Contribution | Owner h | Labor $25/h | Economic profit before tax/FX |
|---|---:|---:|---:|---:|---:|---:|---:|
'''
for r in rows:md+=f"| {r['candidate_id']} | {r['customers']} | ${r['gross_revenue']:,.0f} | ${r['cash_after_platform_and_withdrawal']:,.2f} | ${r['contribution_after_direct_fixed']:,.2f} | {r['owner_total_h']} | ${r['owner_labor_value']:,.0f} | ${r['economic_profit_before_tax_fx']:,.2f} |\n"
md+='''
Gross margin после прямого исполнения в CSV не включает platform/fixed/labor; contribution включает platform/direct/fixed/один withdrawal. Это не interchangeable margins. Direct tax UNKNOWN; неизвестны FOP group/residency/ЕСВ/VAT и база признания platform revenues. Чистая прибыль после налогов не рассчитана как факт. Для чувствительности, **не как применимый налог**, если условный turnover levy 6% от gross $2k, дополнительно вычесть $120; 10% → $200; fixed social charges/FX/bank отдельно. Cash surplus без owner labor нельзя называть net profit. Экономический profit — after opportunity cost, а бухгалтерская прибыль может учитывать собственный труд иначе.

### Обратная воронка

C01: 5 sales/month → при close 5%/10%/20% нужно 100/50/25 qualified inquiries. При 5% qualified/targeted visit это 2000/1000/500 visits. Числа из [funnel sensitivity](data/funnel_sensitivity.csv), не прогноз. D01 каталог существует, но evidence объёма таких показов/обращений UNKNOWN; D02 newcomer access UNKNOWN. C02: 8 active agency accounts; C03: 10 MSP accounts. При close 10% начальное приобретение потребовало бы 80/100 qualified inquiries, которых канал не доказал. Recurring account не появляется без onboarding.

### 40 / 80 / 120 часов в месяц

| Hours | C01 steady customers/gross capacity | Month 1 after 16h preparation | Может вместить 5 продаж? |
|---|---|---|---|
'''
for h in [40,80,120]:
 cap=max(0,(h-16)//10);first=max(0,(h-32)//10)
 md+=f'| {h} | {cap} / ${cap*400} | {first} / ${first*400} | {"Да, steady-state; спрос UNKNOWN" if cap>=5 else "Нет при базовых часах"} |\n'
md+='''
Sales/admin base 16h monthly ограничивает capacity, но не гарантирует требуемый lead volume. При 32h sales/admin C01 target требует 82h; при delivery+support 15h вместо 10h требует 91h при 16h sales. Удвоение сложности легко срывает 80h сценарий. Первая версия/новый recurring onboarding consume часы сверх steady-state; сроки contract approval нельзя сжать дополнительными часами.

### Капитал × горизонт: без продаж

| Cash budget | 30d planned $20 burn | 90d $60 burn | 180d $120 burn | Действие |
|---|---|---|---|---|
| $0 | Не покрыт | Не покрыт | Не покрыт | Только free offline подготовка; paid tools только после funding, cash timing UNKNOWN |
| $100 | Покрыт | Покрыт | Не покрыт | Один эксперимент, без рекламы/годовых лицензий |
| $300 | Покрыт | Покрыт | Покрыт | Reserve; не тратить автоматически; labor runway отдельно |
| $1000 | Покрыт | Покрыт | Покрыт | Не покупать build до buyer evidence; остаток не CAC forecast |

[budget_time_scenarios.csv](data/budget_time_scenarios.csv) содержит все 4×3×3=36 комбинаций **для каждого** из 6 кандидатов: 216 строк. Day30 subtract initial hours; day90/180 показывают capacity целевого месяца после завершения подготовки, не ramp forecast. Target-capacity pass не подтверждает продажи или накопленную cohort. При отсутствии продаж и полном использовании времени 40/80/120h owner opportunity cost=$1000/$2000/$3000 в месяц; за 180d=$6000/$12000/$18000. Cash budget $1000 не оплачивает шесть месяцев жизни владельца.

### Первые $100 / $500 / $2000 / $5000+

$100 gross: один diagnostic; $500 gross: diagnostic + один $400 pack; это два разных результата/сделки без двойного счёта. При базовом stress после 5% reserve/15% fee/одного withdrawal $100 → $79.76 до direct/fixed/labor; чтобы получить $100 cash after platform/withdrawal, нужен gross ≥$125.07 до direct/FX/tax. Чтобы получить $500 cash after platform/withdrawal, gross ≥$620.42. Два $400 pack = $800 gross и $645.01 cash after platform/withdrawal. Первые $500 **оплаты** нельзя обещать из $500 advertised scope.

C01 $2k gross =5 packs; $2k cash after platform/withdrawal требует ≥7 packs=$2800 gross, не 5, и 86h baseline до новых onboarding или более сложных cases. $5k gross требует13×$400=$5200 и146h/month, больше120h. Нужен принятый более высокий чек, существенно меньше трудозатраты либо recurring license; ни одно не доказано. C02 $5k=20 agencies и96h steady-state; C03 $5k=25 MSPs и91h, но initial acquisition/onboarding/channel и retention делают эти арифметические возможности **не масштабируемой доказанной моделью**.

### Отказы, возвраты, отток и задержки

[economics_sensitivity.csv](data/economics_sensitivity.csv): fee 0/10/15%, refunds/noncollection0/5/15%, owner rate10/25/40. Доля возвратов и невозвратные fee неизвестны. [churn_sensitivity.csv](data/churn_sensitivity.csv): при 10% churn на8 agency/10 MSP нужно в ожидании0.8/1 replacement monthly и upfront acquisition time; за6 месяцев без новых клиентов сохраняется≈53.1% cohort. Это deterministic retention при assumed constant churn, не вероятность успешного бизнеса. Даже один lost agency меняет выручку C02 на12.5%; fractional averages не реальные доли клиента.

Time-to-cash: acceptance/security hold UNKNOWN + documented withdrawal timing E47; стресс lag14/30/60d означает необходимость покрывать fixed $20/$20/$40 до первых денег, если работа начинается до cash; фактические сроки площадки и поддержка/refund окна отдельно. No-sales scenario всегда включает $0 revenue; отсутствие observed traffic не заменяется условной вероятностью успеха.
'''
(R/'07_UNIT_ECONOMICS.md').write_text(md)
print(json.dumps({'unit_rows':len(rows),'grid_rows':len(grid),'funnel_rows':len(funnel),'sensitivity_rows':len(sens),'churn_rows':len(churn)}))
