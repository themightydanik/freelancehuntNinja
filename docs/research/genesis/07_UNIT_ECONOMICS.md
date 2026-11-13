# Unit economics — пороги, а не прогноз

Все цены наших пакетов, часы, tool allocation и conversions — ASSUMED: [inputs](data/model_inputs.json), [assumptions](data/assumptions.csv). Чужие тарифы — [evidence](data/evidence_registry.csv). Параметры не подгонялись вероятностной симуляцией. Цель здесь $2 000 **месячной gross revenue**, не cumulative и не net owner income.

Стоимость первой версии — только bounded offline preparation: C01 16h/$400 labor; C02 20h/$500; C03 24h/$600; C04 24h/$600; C05 32h/$800; C06 16h/$400 при $25/h. Cash initial $0 предполагает имеющийся компьютер/инструменты и отсутствие paid registration. Infrastructure reserve $20/month и direct allocation $8/$10/$14/$10/$10/$8 per customer — planning assumptions, не vendor quotes. Production/security/SLA и неизвестные лицензии не входят: product build пока не разрешён экономикой. Срок подготовки при 40/80/120h monthly для C01: около 12/6/4 календарных дней при равномерном распределении; это не срок продажи.

Формулы: gross=n×price; collected-reserve=gross×(1−refund); fee=collected×fee_rate; cash-after-platform=collected−fee−withdrawal; contribution=cash−direct−fixed; owner labor=(delivery+support+sales/admin)×rate; economic profit=contribution−labor. Refund reserve здесь консервативно включает noncollection; actual timing UNKNOWN. Cash received на банк **не наблюдался**, строки cash в CSV — рассчитанный сценарий поступления. Fees applied after refunded amount — упрощение; невозвратные комиссии/chargeback fee могут ухудшить результат.

| Candidate | n для ≥$2k | Gross | Cash after platform/withdrawal | Contribution | Owner h | Labor $25/h | Economic profit before tax/FX |
|---|---:|---:|---:|---:|---:|---:|---:|
| C01 | 5 | $2,000 | $1,614.01 | $1,554.01 | 66 | $1,650 | $-95.99 |
| C02 | 8 | $2,000 | $1,614.01 | $1,514.01 | 48 | $1,200 | $314.01 |
| C03 | 10 | $2,000 | $1,614.01 | $1,454.01 | 46 | $1,150 | $304.01 |
| C04 | 4 | $2,000 | $1,614.01 | $1,554.01 | 64 | $1,600 | $-45.99 |
| C05 | 4 | $2,000 | $1,614.01 | $1,554.01 | 72 | $1,800 | $-245.99 |
| C06 | 6 | $2,100 | $1,694.76 | $1,626.76 | 70 | $1,750 | $-123.24 |

Gross margin после прямого исполнения в CSV не включает platform/fixed/labor; contribution включает platform/direct/fixed/один withdrawal. Это не interchangeable margins. Direct tax UNKNOWN; неизвестны FOP group/residency/ЕСВ/VAT и база признания platform revenues. Чистая прибыль после налогов не рассчитана как факт. Для чувствительности, **не как применимый налог**, если условный turnover levy 6% от gross $2k, дополнительно вычесть $120; 10% → $200; fixed social charges/FX/bank отдельно. Cash surplus без owner labor нельзя называть net profit. Экономический profit — after opportunity cost, а бухгалтерская прибыль может учитывать собственный труд иначе.

### Обратная воронка

C01: 5 sales/month → при close 5%/10%/20% нужно 100/50/25 qualified inquiries. При 5% qualified/targeted visit это 2000/1000/500 visits. Числа из [funnel sensitivity](data/funnel_sensitivity.csv), не прогноз. D01 каталог существует, но evidence объёма таких показов/обращений UNKNOWN; D02 newcomer access UNKNOWN. C02: 8 active agency accounts; C03: 10 MSP accounts. При close 10% начальное приобретение потребовало бы 80/100 qualified inquiries, которых канал не доказал. Recurring account не появляется без onboarding.

### 40 / 80 / 120 часов в месяц

| Hours | C01 steady customers/gross capacity | Month 1 after 16h preparation | Может вместить 5 продаж? |
|---|---|---|---|
| 40 | 2 / $800 | 0 / $0 | Нет при базовых часах |
| 80 | 6 / $2400 | 4 / $1600 | Да, steady-state; спрос UNKNOWN |
| 120 | 10 / $4000 | 8 / $3200 | Да, steady-state; спрос UNKNOWN |

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
