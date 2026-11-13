# 15. Первые $500: три точных условных сценария, без запуска

**Дата проверки: 13 ноября 2026, Europe/Kyiv.** VERIFIED — первичный документ/воспроизводимый тест; OBSERVED — ограниченная выборка; ESTIMATED — расчёт; ASSUMED — допущение; UNKNOWN — недостаточно данных. Никаких продаж, публикаций офферов, регистраций, платежей, rotation или production changes не выполнялось.

## Определение цели и границы арифметики

Здесь «первые$500» — накопленные по batch фактически оплаченные и доступные поступления **после выбранных platform/payout fees, direct costs и резерва$5**, до налогов, личного труда, неизвестного FX/дополнительных bank fees/обязательного onboarding. Это не обещание$500 за 30 дней. Цены — **ASSUMED price tests**, поскольку accepted price Bot RecoveryUNKNOWN. [14](14_COMMERCIAL_VALIDATION_READINESS.md) показывает, почему найденные бюджеты не подтверждают ни$350, ни новые цены.

Расчёт [first_500.py](../../research/models/first_500.py), [JSON](../../data/first_500_scenarios.json), invoice arithmetic tests. Диагностика засчитывается в total repair price; нельзя сложить$75 и$220 для одного$220 заказа. Каждая оплаченная работа должна иметь принятую deliverable/приёмку; quote/escrow/проблема в issue сами по себе не деньги.

| Сценарий | Условный чек | Оплаченные заказы без refund | Invoice total | Расчёт остатка | Остаток$ | При одном полном refund и conservative retained fees |
| --- | --- | --- | --- | --- | --- | --- |
| A: только Freelancehunt, USD Safe |150 |4 |600 |600−54 service fee−5 bank payout−4 direct−5 reserve |532.00 |5 orders,1 refund →517.50 |
| B: Upwork Catalog + собственное разрешённое demo |220 |3 |660 |660−99 fee(15%)−0.99 bank−6 direct−5 reserve |549.01 |4 orders,1 refund →514.01 |
| C: B2B white-label, условный Contra payout route |300 |2 |600 |(600−30 platform)×.98−3 payout−4 direct−5 reserve |546.60 |3 orders,1 refund →529.90 |

Refund stress намеренно консервативно сохраняет percent fee на всех invoices. У конкретной площадки fee refund policy может вернуть часть fees; это не утверждение её правил. Contra payer/route — ASSUMED, нуждается в проверке кабинета. Extra bank/FX/onboarding fees не объявлены нулевыми: вычитать после owner route check. Более низкая комиссия не гарантирует order flow.

## A. Только Freelancehunt

**Механизм:** owner-approved ответ на уже существующий релевантный запрос либо добровольное входящее обращение → qualification → paid diagnostic → scoped fixed quote → Safe funding → approved delivery → acceptance → cleared payout. Не auto-bidding, не новый публичный оффер в этом исследовании. Не отвечать на нерелевантные/new-build задачи только ради количества.

Для точного USD-расчёта выбран **USD Safe**, где executor fee9% по [официальной статье](https://help-ua.freelancehunt.com/uk/sieif/komisiia-za-vikoristannia-sieifa), bank payout$5 по [withdrawals](https://help-ua.freelancehunt.com/uk/finansovi-pitannia/viviediennia-koshtiv-platizhni-instrumienti-ta-komisiia). Для UAH9%платит клиент, а не исполнитель; нельзя механически применить 9%к UAH-net. Существование USD route для конкретной территории/банка владельца не проверено. USDprice150в этой таблице не основан на Telegram-recovery transactions — это экспериментальный lower-scope repair quote.

UAH-вариант без выдуманной валютной котировки: при price5000UAH, direct50UAH/job и batch reserve200UAH нужно
`N = ceil((500×F +200)/(5000−50))`, где `F` — **фактический** UAH/USD conversion с учётом доступного маршрута. Stress inputsF40/45/50 дают 5/5/6jobs; это не утверждение текущего курса. Попытка NBUquote дала 403; текущая bank conversionUNKNOWN. В UAHcard route опубликована 0%payout fee; возможные taxes/bank conversion отдельно.

**Воронка/неизвестные:** для 4 paid jobs `Q≥ceil(4/p_quote_to_paid)`. Stressp5/10/20%→80/40/20**квалифицированных** quotes, не найденных объявлений. Qualification rate, funding rate, paid lag и число доступных подходящих requestsUNKNOWN. Единственный bounded deployment в retained sample имел 126 bids и budgetUNKNOWN; pipeline4repairs не доказан. Если за 14 дней нет 5 действительно подходящих ситуаций, менять канал/scope, не строить Bot Recovery SaaS.

**Время(A):**6 h/order→24 hdelivery/ограниченной поддержки;0.5 h/qualified quote→10–40 h;8 hmaterials/channel work и 16 hразовой demo base→58–88 hпервого batch, без ожидания клиентских доступов/оплаты. $532/58–88 h≈$6–9/h до налогов, не устойчивая зарплата. Subsequent reuse сокращает setup только если тот же сценарий действительно повторяется.

**Самая дешёвая проверка:** после country/account gate и отдельного разрешения —5 qualifications, один ясный paid diagnostic offer; не закупать Plus или automation ради статистики до actual outcome. Cash acquisition может быть$0 только если текущие account limits это допускают; limits/платные функции требуют ручной проверки. Никакого запуска сейчас.

## B. Международный marketplace + собственная демонстрация

Выбран **Upwork Project Catalog** как описанный фиксированный оффер с reviewed listing и organic search; actual Ukraine account/payout gate открыт. В таблице используется верхняя опубликованная Freelancer Service Fee15%, а не универсальные 10%. Direct-to-Local-Bank0.99 тоже условен на доступность конкретного метода. [fee](https://support.upwork.com/hc/en-us/articles/211062538-Learn-about-the-Freelancer-Service-Fee), [Catalog](https://support.upwork.com/hc/en-us/articles/360058234233-How-to-get-started-with-Project-Catalog-as-a-freelancer), [payout](https://support.upwork.com/hc/en-us/articles/211063888-How-to-withdraw-earnings-with-Direct-to-Local-Bank). Optional boosts/ads не включены; нужны authorization на публикацию и подтверждение actual eligibility.

**Механизм:** поисковый показ Catalog **или** разрешённый own-content visit → переход к synthetic demo → уникальное source-attributed inquiry → qualification → diagnostic/quote → funding → repair → accepted milestone → payout. Organic website traffic и marketplace inquiry — разные sources, не дважды один lead. Сама HTML-демонстрация без разрешённой публикации имеет 0 измеренного трафика.

3 paid jobs по 220 дают$549.01 после выбранных fees/costs/reserve; время каждого≤6 h — ASSUMEDcap, проверяемый pilot. Если продаётся только$75 diagnostic, при тех же 15%, direct$2/job и reserve/payout нужно **9 paid diagnostics** ($549.76), а не три. Это причина отдельно измерять willingness to pay за diagnosis и repair.

**Воронка:** `Q≥ceil(3/p_quote_to_paid)`. Stressp10/25/40%→30/12/8qualified quotes. До них ещё нужны unknown exposures, CTR, qualified-inquiry rate; в source job count их нет. Опубликованные советы площадки про изображения/keywords не доказывают 1000 показов нового продавца. Начальный denominator — actual listing views/clicks, если доступны; иначе tracked visits/inquiries, без выдуманных impressions.

**Время(A):**18 hdelivery +4–15 hquotes +24 hразового demo/materials→46–57 hпервого batch. При новом аккаунте review/KYC/ожидание payouts добавляют **календарный**, не скрытый рабочий срок. Минимальный cash входUNKNOWN: некоторые новые аккаунты перед proposals требуют qualifying Connects purchase/Plus; Catalog и client purchase не равны гарантированному бесплатному proposal access. Owner не должен платить за ads/Connects без отдельного решения.

**Сильнее competitor pricing, но иной scope:**30 публичных Expensify External bug issues имеют$175 advertised reward и один sponsor. Четыре принятых и оплаченных исправления по 175 при 15%fee,$2 direct/job,$0.99 payout,$5 reserve дали бы$581.01. Но нужны verified Upwork, принятый proposal, знание React Native/конкретной codebase и очередь review; часть issues уже assigned/closed. Это кандидат отдельной skill-gated проверки, **не** бесплатный источник покупателей Bot Recovery. [rules](https://raw.githubusercontent.com/Expensify/App/main/contributingGuides/CONTRIBUTING.md). Ничего не подавалось.

**Дешёвый тест:** owner secure eligibility review + одна карточка/демо(готовы) + разрешённое measured placement; затем 5 qualified conversations/quotes. Нет targeted visits→проверять distribution, а не менять backend. Есть 5 qualifiedно 0 accepted price→scope/price/trust review. Demand stillUNKNOWN при отсутствии traffic.

## C. B2B-партнёрства + white-label

Две согласованные поставки по$300; каждая — **одна** integration/deployment проблема, до 6 h, source/acceptance ownership/IP/доступы согласованы. Клиентское agency NDA, subcontract consent, DPA и invoice/tax форма проверяются до исполнения. Не продавать full cyber-hardening или public-sector bespoke system как маленький replay kit.

**Acquisition:** существующее consented знакомство, добровольный agency inquiry или явно открытый partner-intake → conversation → capability fit → scoped quote → paid sprint → acceptance → optional next sprint. **Исходящие сообщения отключены**, award event не является conversation или согласием. Наличие таких связей у владельцаUNKNOWN; фактических разговоров 0. TED/ARES пока дают контекст, не buyers — [16](16_ALTERNATIVE_STRATEGY_CHALLENGERS.md).

Чисто условный payment route: независимый исполнитель покрывает Contra$15/transaction<500, Payoneer payout2%+$3, direct$2/job,$5 reserve. Итог$546.60. При country-specific payout flat$15 вместо 3 —$534.60; additionalFX/other fees вычитаются отдельно. Published document даёт варианты, actual owner route/кто несёт platform feeUNKNOWN. Не считать слово commission-free нулевой стоимостью.

**Воронка:** `R≥ceil(2/(s_conversation_to_quote×p_quote_to_paid))`. Stresss=.5,p=.25→16**consented** conversations/8quotes, а не 16 award records. Эти параметры не измерены. При 1 h/conversation +0.5 h/quote +12 hdelivery +24 hsetup→56 hпервого batch. Для другой close rate range может быть намного хуже; профессиональная специализация/доверие — отдельный gate.

**Дешёвый тест:** owner проверяет наличие 3 реально доступных consented agency conversations; один capability-fit walkthrough на synthetic demo; один узкий платный diagnostic/sprint. Без такой сети C не «самый быстрый», даже если содержит всего два invoice. Не отправлять письма компаниям-победителям и не заполнять партнёрские формы в исследовании.

## Канальная модель: что изменено

[Новый скрипт](../../research/models/channel_revenue_model.py), [inputs](../../data/channel_model_assumptions.json), [totals](../../data/channel_revenue_scenarios.csv), [per-channel funnels](../../data/channel_funnel_results.csv), [sensitivity](../../data/channel_sensitivity.csv). Старая модель сохранена как исторический stress-test; новая **не** posterior update из реальных продаж и не сопоставима напрямую с первоначальными 24%.

Пять взаимоисключающих источников: UA_marketplace(UAHprice tier), INT_marketplace(Upwork USDprice tier), organic website visits, direct qualified inbound **вне** этих каналов, consented B2Bconversations. Это операционные price/channel segments, а не измеренное гражданство покупателей. Source attribution предотвращает двойной счёт. Количество issues/awards/jobs в модель не загружается.

Фазы: traffic→click→qualified→conversation→proposal→accepted→funded→due after0/1/2months→capacity-limited delivered/paid→refund/payout; repeats и optional retainers отдельно. Outgoing messages=0. 120 hодного owner;24 hобщего acquisition,16 hshared presales cap, build16hmonth1/4hlater; delivery4/6/10htriangle; retainer0.75 h/month. Не пять независимых исполнителей. При заданных бюджетах 16 h demo и 24 h acquisition активный первый месяц требует минимум 40 h; меньшую доступную мощность надо перепланировать, а не скрыто обрезать время. Shared funding/lag, backlog expiry, churn/support, payout и fees учтены. Сумма marketing+support+delivery не превышает capacity; accepted quote ещё не funded sale.

**Все** traffic/conversion/price/workload/lag/renewal priorsASSUMED, включая accepted→funded65/85/98%triangle. CTR1/3/5%, qualification4/10/18%, proposal45/70/90%, accepted8/20/35% — примеры для sensitivity, не рыночные averages. По сценариям различаются starting channel traffic/conversations; published fees используются с явными route assumptions. Повышенный price и более высокийclose не должны трактоваться независимыми в реальности; корреляция/selection bias пока не калиброваны. FX45 — **явно поданный illustrative parameter**, quoteNBU403, не текущий курс; CLI требует назвать input.

| Planning case | Day | Revenue median$ | Cash contribution median$ | P(monthcash≥500) | P(monthrevenue≥2000) | Owner hours median |
| --- | --- | --- | --- | --- | --- | --- |
| Conservative | 30 | 0.0 | -5.0 | 0.04% | 0.00% | 41.5 |
| Conservative | 90 | 0.0 | -5.0 | 1.30% | 0.00% | 30.0 |
| Conservative | 180 | 0.0 | -5.0 | 2.86% | 0.00% | 31.8 |
| Base | 30 | 0.0 | -5.0 | 1.24% | 0.00% | 47.0 |
| Base | 90 | 248.92 | 211.88 | 16.94% | 0.04% | 43.0 |
| Base | 180 | 378.08 | 332.38 | 31.86% | 0.10% | 49.7 |
| Upside | 30 | 178.5 | 149.44 | 7.16% | 0.00% | 59.9 |
| Upside | 90 | 632.9 | 553.86 | 55.92% | 0.86% | 61.0 |
| Upside | 180 | 732.62 | 638.71 | 63.66% | 1.30% | 63.3 |
| UNLAUNCHED_reference | 30 | 0.0 | 0.0 | 0.00% | 0.00% | 0.0 |
| UNLAUNCHED_reference | 90 | 0.0 | 0.0 | 0.00% | 0.00% | 0.0 |
| UNLAUNCHED_reference | 180 | 0.0 | 0.0 | 0.00% | 0.00% | 0.0 |

Reference `UNLAUNCHED` отключает весь acquisition и spending:0 sales,0 fees,0 activity. Planning rows предполагают **уже полученные** permissions/account/payout/distribution и не относятся к текущему состоянию. Goal$2000 — revenue after expected refunds, доfees/tax; goal$500 — contribution after model costs, **до труда/налогов**. Month-end probabilities не cumulative first-sale probability; отдельная колонка reached_by_day есть вCSV. Ноль успехов из 5000 не доказывает невозможность. Отсутствие calibration важнее маленькой MonteCarlo sampling error.

## Sensitivity по тому, что можно измерить ближайшим экспериментом

| Что меняется | Stress input/multiplier | ΔP(net500/day90), conditional |
| --- | --- | --- |
| price | 1.25 | +9.24 п.п. |
| price | 0.75 | -8.92 п.п. |
| close | 1.25 | +8.08 п.п. |
| cash_lag_months | 1 | -6.88 п.п. |
| accepted_to_funded | 1.25 | +6.82 п.п. |
| accepted_to_funded | 0.75 | -6.74 п.п. |
| close | 0.75 | -6.32 п.п. |
| INT_marketplace | 1.5 | +5.94 п.п. |
| qualification | 1.25 | +5.44 п.п. |
| INT_marketplace | 0.5 | -5.12 п.п. |

| Неизвестный input | Ближайшее измерение | Не подменять |
| --- | --- | --- |
| Accepted price | Реальный accepted quote и cleared payment по одному scope | Объявленным budget/ценой конкурента |
| Qualified traffic | Actual views/UTMvisits и unique qualified inquiry; source отдельно | Числом найденных проектов |
| Quote→accepted→funded | Отдельные counters и отказ/неоплата | Одним AI «lead score» |
| Cash lag | Dates inquiry/quote/funded/delivered/released/withdrawn | Instant payout assumption |
| Delivery/support hours | Одно реальное scoped внедрение +7 дней regression window | Synthetic demo duration |
| Payout/fees/FX | Owner secure account route/status и actual statement без secret values | Публичной страницей как successfulKYC |

Рекомендуемый первый decision gate — **одна фактическая оплата diagnosis**, затем два похожих repair outcomes и повторяемый cost. Не путать это с доказанным$500 pipeline; не строить глобальную Ninjaархитектуру ради улучшения красивых simulation outputs.
