# 11. Решение владельцу: validation-first service portfolio

**Дата проверки: 2026-11-13 (Europe/Kyiv).** Метки: VERIFIED — первичный документ или воспроизводимый тест; OBSERVED — ограниченная выборка; ESTIMATED — расчёт; ASSUMED — допущение; UNKNOWN — данных недостаточно. HTTP 200 сам по себе не подтверждает API, спрос или право автоматизации.

**Рекомендация (confidence medium для порядка эксперимента, low для продаж): сначала проверить P01 Bot Recovery как узкий пакет, а не строить автономную lead-generation платформу.** Второй shared capability — P04 reliable webhook/replay; P02 WooCommerce только после сравнения с existing free plugin. Нужен отдельный owner approval для публикаций/контактов/оплат; текущий PR — research only.

## Ответы на 17 вопросов

1. **Что строить первым?** Только synthetic recovery demo ≤12–16h и scope/acceptance документацию P01, после отдельного согласования implementation task. Сам работающий bot не менять в этом PR. [06A](06A_TOP_10_PRODUCTS.md)
2. **Почему?** Повторное использование bot expertise, ограниченный delivery8h и понятное доказательство результата. Advertised bot requests существуют, но desired price не доказан. Это более дешёвый learning experiment, чем global registry SaaS. [01](01_REPOSITORY_AUDIT.md), [03](03_OPPORTUNITY_RESEARCH.md)
3. **Какие источники работают?** JSON sample/cursor: Prozorro, GitHub, WP; TED search JSON; GLEIF и UK OCDS useful backups. Не все useful supplier fields/история проверены. Companies House без ключа401, Spending500, часть endpointsHTML/ошибки. [02](02_DATA_SOURCES.md)
4. **Какие площадки доступны?** Подтверждены публичные страницы и отдельные policy facts, а не merchant onboarding. Freelancehunt API показывает buyer requests; Upwork eligibility требует geography/KYC; Contra payoutsUNKNOWN. Полностью проверенных UA payout routes: **0**. [05](05_DISTRIBUTION_CHANNELS.md)
5. **Какие продукты?** P01→P04→conditional P02; P03 gated, P05 только by-product. Не 30 MVP. [06A](06A_TOP_10_PRODUCTS.md)
6. **Первые показы/обращения?** Один buyer-intent listing после approval/eligibility + один полезный English technical demo/tutorial с tracked links и opt-in intake. Ни массовых сообщений, ни «профиль значит трафик». [05A](05A_REGISTRATION_PLAYBOOK.md)
7. **Гипотезы не подтверждены?** Price acceptance$350–600, international buyer exposure, seller trust without reviews, close/lag, repeat/attach/churn, agency interest и поддержка. Payout/admission для большинства каналовUNKNOWN. [07](07_REVENUE_MODEL.md)
8. **Что проверить за1–2дня?** Owner current country/payout/fee status для двух каналов; существующий free workflow на synthetic event; одна restore rehearsal; точное понятное scoped offer; source field-quality10 awarded notices при выборе procurement challenger. Это планы, не уже выполненные customer checks.
9. **Что требует недель?** Достаточный qualified exposure, accepted scopes, реальные payments/delivery/support, partner admission,2 renewals и deployed scheduler reliability. Нельзя заменить их ещё одним API call.
10. **Первые$500?** Illustrative2×$350 jobs=$700gross/$679after refunds; не гарантированный срок. Один$600 replay даёт$582after refunds, если есть buyer. Нужен согласованный paid scope, не автоматическая генерация bid.
11. **$1000?** 3×$350=$1050gross/$1018.50after refunds; после fee10%, direct$9 иfixed$5 около$902.65net. Для$1000net этого мало. [07](07_REVENUE_MODEL.md)
12. **$2000?** 6×$350=$2037after refunds либо5×$500=$2425; 4×$500 дают лишь$1940. Capacity и acquisition проверять вместе. Default optimizer6mixed jobs=$2813after refunds, но demand не доказан. Base conditional day180 chance только~24%. [07](07_REVENUE_MODEL.md), [10](10_PORTFOLIO_STRATEGY.md)
13. **Не работает?** 100targeted visits и0qualified;5qualified discussions и0accepted price/scope; delivery>14–16h; support>2h/client/month; expired leads/payment lag превышает runway. Это ASSUMED stop thresholds, не статистически универсальные benchmarks.
14. **Когда сменить направление?** По evidence: low clicks→позиционирование; clicks без qualified→segment/problem; qualified без sale→trust/price/scope; paid без margin→delivery/support. До изменения продукта измерить достаточный exposure. Два последовательных2-week experiments без improve → challenger P04/agency channel, не ещё10sources.
15. **Бюджет?** Research$0paid API. Demo/validation target$0–5/month software, model fixed$5; platform onboarding/bids/withdrawals may cost extraUNKNOWN. Optional paid infrastructure reserve$25–50/month после revenue и owner approval; это budget scenario, не verified vendor quote. Conservative без продаж даёт loss cash и времени; личный runway неизвестен.
16. **Что reusable?** Recovery fixtures/runbook, signed event adapter, exact-ID ledger/history, approval audit, source claim provenance, minimal inquiry attribution, budget guard. Не копировать client secrets/data в reusable templates. [08](08_TECHNICAL_FEASIBILITY.md)
17. **Что защищает долгосрочно?** Реально измеренные consented failure/repair outcomes, vetted adapter contracts, repeat agency trust, own opt-in channel. Public source volume, generic AI prompts и fabricated lead scores не moat. [10](10_PORTFOLIO_STRATEGY.md)

## Отвергнутые как первый этап идеи

Autonomous cold outreach/auto-bidding; общий реестр всех компаний; новый Zapier; 30 profiles/30 MVP; grants intelligence без budget/customer interview; regulation alerts без legal expert; unattended Mac browser automation при наличии documented bid API; Actions как бесплатный production serverless daemon. Некоторые могут стать полезными позже, но текущего evidence недостаточно и/или есть platform/legal gates.

## Условия перед implementation

Owner: credential rotation/remediation decision; реальный time budget и competence; допустимые country/payout channels; бюджет/цена пилота; permissions на контент и commercial contact; client data/AI policy. Это не просьба повторно одобрить исследование: данный research scope и Draft PR уже разрешены. Merge, cloud publish, registrations и продажи не выполняем.
