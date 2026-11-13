# Подписки и семь финансовых моделей

Все наши цены, часы, конверсии, churn и стоимость привлечения — ASSUMED или UNKNOWN. Цель таблиц — месячная gross revenue, не личный доход. Проверено 13 ноября 2026. Труд владельца $25/час; чувствительность $10/$25/$40. [Параметры](data/model_inputs.json), [расчёты](data/financial_thresholds.csv), [реклама](data/advertising_thresholds.csv).

| Модель | Для $500 gross | Для $2 000 gross | Для $5 000 gross | Создание: часы / стоимость труда |
|---|---:|---:|---:|---|
| B2B_FIXED | 2 | 5 | 12 | 24h / $600; entry 0 |
| B2B_LICENSE | 7 | 26 | 64 | 80h / $2000; entry 0 |
| MOBILE_SUB | 101 | 401 | 1003 | 100h / $2500; entry 25 |
| CHROME_SUB | 100 | 400 | 1000 | 60h / $1500; entry UNKNOWN CWS fee |
| PLUGIN_FREEMIUM | 123 | 490 | 1225 | 100h / $2500; entry 0 |
| MOBILE_ADS | 100 000 показов | 400 000 показов | 1 000 000 показов | 100h / $2 500; Android entry $25; assumed net eCPM $5 |
| HYBRID | 2 агентства + 62 retail | 7 агентств + 245 retail | 17 агентств + 613 retail | 120h / $3 000; одно ядро, два непроверенных канала |

B2B_FIXED — количество новых работ по $450, а не подписчиков. B2B_LICENSE — действующие агентства по $79/месяц. MOBILE_SUB — $4.99/месяц; CHROME_SUB — $5/месяц. PLUGIN_FREEMIUM — действующие годовые лицензии по $49: $4.0833 monthly equivalent. Это 490 активных лицензий для $2k, а не 490 новых покупок каждый месяц. Annual cash нельзя называть повторным MRR без истории продлений.

### При цели $2 000 gross

| Модель | Расчётная gross | Cash monthly equivalent после reserve/fees/partner | Contribution после direct/fixed | Часы владельца | Economic profit до налогов/FX/CAC |
|---|---:|---:|---:|---:|---:|
| B2B_FIXED | 2250.0 | 1612.55 | 1552.55 | 56 | 152.55 |
| B2B_LICENSE | 2054.0 | 1461.36 | 1389.36 | 33.0 | 564.36 |
| MOBILE_SUB | 2000.99 | 1649.82 | 1579.72 | 36.03 | 678.97 |
| CHROME_SUB | 2000.0 | 1623.6 | 1583.6 | 32.0 | 783.6 |
| PLUGIN_FREEMIUM | 2000.83 | 1803.94 | 1734.94 | 43.6 | 644.94 |
| HYBRID | 2043.42 | 1647.14 | 1571.64 | 40.8 | 551.64 |

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
