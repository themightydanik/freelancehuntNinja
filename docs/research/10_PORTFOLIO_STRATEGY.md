# 10. Комбинации и ограниченный портфель

**Дата проверки: 2026-11-13 (Europe/Kyiv).** Метки: VERIFIED — первичный документ или воспроизводимый тест; OBSERVED — ограниченная выборка; ESTIMATED — расчёт; ASSUMED — допущение; UNKNOWN — данных недостаточно. HTTP 200 сам по себе не подтверждает API, спрос или право автоматизации.

## Сравнение синергий

Цена/сроки/маржа ниже — ASSUMED/ESTIMATED, не данные сделок. Workload из комбинаций нельзя суммировать как независимые команды; всё делает один owner. Общие зависимости: event identity/provenance, bounded source adapters, synthetic fixtures, scoped intake, human approvals. У каждой комбинации есть platform/API зависимость, включая own code distribution на GitHub; moat не равен «много публичных данных».

| ID | Комбинация | Launch work estimate | Cash | Первые обращения | Первые деньги |
| --- | --- | --- | --- | --- | --- |
| K01 | P01 recovery + D01 + D34 synthetic tutorial | 12h base + 8–12h assets | $0–5/mo plus actual platform fees | ASSUMED 7–30d; UNKNOWN exposure | ASSUMED 7–60d; no pipeline yet |
| K02 | P04 event replay + P02 Woo service + D19/D18 | 16+20h specific +6h shared event primitive | $0–10/mo plus client hosting | ASSUMED 14–45d; partner approval UNKNOWN | ASSUMED 14–60d |
| K03 | Award notice + agency directory + P22 white-label | 24–40h data/qualification +8h offer | $0 read probes; paid tender access UNKNOWN | ASSUMED 30–90d | ASSUMED 30–120d |
| K04 | GitHub pain + tiny OSS fixture + P04 implementation | ≤16h sample+docs, not new platform | $0 distribution software; hosting quota applies | ASSUMED 14–60d | ASSUMED 14–90d |
| K05 | Grant project + P08 evidence dashboard + agency/legal partner | 40–80h + expert review | $0 metadata; legal/support may require budget | ASSUMED 30–90d | ASSUMED 45–120d |
| K06 | P01/P04 paid deployments + opt-in maintenance39 + P05 kit by-product | Use deployed fixtures; extra template docs ≤8h after cases | $0–10/mo plus processor/client infra | Existing clients; new traffic UNKNOWN | Maintenance next month after completed job; kit timing UNKNOWN |
| K07 | Plugin lifecycle + agency maintainer handover + recovery rehearsal | 20h compatibility+P01 shared base | $0 metadata; staging client-paid | ASSUMED 14–45d | ASSUMED 14–60d |
| K08 | Grant deliverable + procurement award on exact org ID → partner evidence | 40–80h cross-source mapping | $0–10 sample; access/legal may add cost | UNKNOWN; no buyer example | UNKNOWN; likely institutional delay (ASSUMED) |

| ID | Переиспользование | Экономика | Риск/зависимость | Подтверждение до инвестирования |
| --- | --- | --- | --- | --- |
| K01 | Recovery fixture, runbook, minimal intake | $350; catalog $302.55 cash contribution, $122.55 after first delivery/support labor | Local budgets too low; international discoverability untested | One paid pilot at target scope; <10h delivery |
| K02 | Event ledger, source contract fixtures, signed delivery | $500–600; 12–14h delivery plus1h support; see catalog | Free plugin suffices; transport IDs collide; review/license | Same workflow in two paid cases; compare free integration |
| K03 | Source IDs, award context, integration delivery primitives | $900 sprint/20h assumed; no repeat agency validated | Award winner does not need us; contact permission; long cycle | 10 relevant awards yield5 qualified orgs and2 voluntary discussions |
| K04 | One fixture also serves customer acceptance | Service $600; license optional only after traffic evidence | Users DIY, free workaround, upstream fix removes gap; no issue advertising | Tracked docs→qualified inquiry,2 paid scopes |
| K05 | Versioned report artifacts, permissioned client records | $900+ first setup assumption; 24h delivery+2h support | Grant rules, institutional procurement, competitor spreadsheets | Coordinator validates budget and reporting need |
| K06 | Client-specific synthetic regression probes; recovery history | $39/sub,0.5h support assumption; 52 subs≈$2028 gross but26h support plus acquisition | Support cap, no renewal evidence, checkout payouts UNKNOWN | 2 paid renewals; <0.5–1h support/client/month; transparent scope |
| K07 | Migration fixture and restore runbook as same acceptance asset | $400 scoped migration,10h+1h support assumption | Age is not abandonment; liability for restore; licensing | Consented actual break; staging rollback; one paid acceptance |
| K08 | Entity alias provenance; source-version linked facts | No defensible quote or revenue estimate yet | No shared identifiers/false joins; event still not budget; privacy | 5 exact lawful cross-source matches and specific buyer workflow; otherwise stop |

K07 и K08 — дополнительные неочевидные связи: asset восстановления одновременно становится proof продажи и acceptance при передаче обслуживания; cross-grant/procurement graph потенциально выявляет institutional partner, но пока не имеет даже подтверждённого join/покупателя. K08 нельзя включать в revenue forecast. K06 использует maintenance как opt-in service с обязательствами, не «пассивный SaaS доход».

## Четыре выбора

- **Первые деньги:** K01. Самая короткая связь с текущим bot experience и низкая стоимость synthetic proof; цена/международный traffic ещё gate.
- **Долгосрочное преимущество:** K02+K04 — permissioned edge-case fixtures, recovery outcomes, adapter contracts и agency trust. Публичные raw data и generic prompts не уникальны; client data не публиковать без согласия.
- **Повторяющийся доход:** K06 после completed services и measured renewal/support. Recurring revenue нельзя заложить просто переключателем billing; требуется recurring value и affordable support.
- **Общий начальный портфель:** P01 primary, P04 second only after related qualified demand, P02 niche adapter если free alternatives не закрывают кейс; один buyer channel + один content channel, не 30 profiles. Procure/grant/registry — bounded challenger research, ≤4h/week после первых sales, не второй full product.

## Integer capacity optimization

Файл [portfolio_results.json](../../data/portfolio_results.json); [optimizer](../../research/models/portfolio_optimizer.py) exhaustive search по P01–P05. Assumptions: caps P01≤3, P02≤3, P03≤2, P04≤2, P05≤10/month; эти caps **не измерены**. P03 доступен только при явном security qualification flag; default excludes. Cash≤$10/month, capacity120h, acquisition24h, launch build≤70h, product-specific build amortized6 months, shared primitive6h one per dependency. Refund3%, fee10%. Каждый active product требует своего build и общего prerequisite. Нет спорной абстрактной weighted score: objective cash contribution; labor-adjusted result показан отдельно. Это оптимум **только данной маленькой grid**, не глобальная бизнес-оптимальность.

| Case | Monthly units | Gross $ | Contribution $ | Hours | Launch h | После труда20/h $ |
| --- | --- | --- | --- | --- | --- | --- |
| base | {'P01': 2, 'P02': 2, 'P03': 0, 'P04': 2, 'P05': 0} | 2900 | 2521.7 | 108.0 | 60 | 361.7 |
| no_reuse | {'P01': 2, 'P02': 2, 'P03': 0, 'P04': 2, 'P05': 0} | 2900 | 2521.7 | 109.0 | 66 | 341.7 |
| with_security_qualification | {'P01': 3, 'P02': 0, 'P03': 2, 'P04': 2, 'P05': 0} | 3150 | 2742.95 | 111.33 | 56 | 516.28 |
| fee20 | {'P01': 2, 'P02': 2, 'P03': 0, 'P04': 2, 'P05': 0} | 2900 | 2240.4 | 108.0 | 60 | 80.4 |
| fee30 | {'P01': 2, 'P02': 2, 'P03': 0, 'P04': 2, 'P05': 0} | 2900 | 1959.1 | 108.0 | 60 | -200.9 |
| capacity80 | {'P01': 1, 'P02': 0, 'P03': 0, 'P04': 2, 'P05': 10} | 2040 | 1770.92 | 78.67 | 64 | 197.59 |
| relaxed_demand_caps_warning | {'P01': 0, 'P02': 0, 'P03': 0, 'P04': 6, 'P05': 0} | 3600 | 3134.8 | 117.67 | 22 | 781.47 |

Default optimum: 2 recovery +2 Woo +2 replay = $2900 gross; $2813 after refunds; $2521.70 contribution;108h/month including amortized launch+marketing. Это **6 клиентов/month**, получение которых не доказано. Cash cost$10, upfront launch60h (включая shared12h); это один человек, поэтому запуск растянуть по gates, не делать 3 MVP одновременно. Work allocation:24h acquisition,10h amortized build,74h delivery/support. Первый launch month реально требует больше build и не обязан достигнуть steady-state output. Monte Carlo [07](07_REVENUE_MODEL.md) отдельно моделирует demand/lag и именно поэтому даёт намного менее уверенный результат.

No-reuse не меняет оптимальное число sales в этой grid, но launch66h вместо60h и monthly109h вместо108h. Экономия6h не повод заявлять exponentiating scale. Fee30% опускает contribution до $1959.10 при той же выручке: net target не достигнут. Capacity80h optimum зависит от 10 непроверенных kit sales; при отсутствии kit traffic этот результат завышен. With-security-qualification relaxation показывает альтернативу, но не разрешает продавать security audit без компетенции. Relaxed-demand grid (≤10 units/product) специально демонстрирует, как оптимизатор предлагает больше P04 при произвольно снятых demand caps; это warning о assumptions, не рекомендация.

## Откуда может возникнуть moat

Собственные данные здесь — разрешённые агрегаты фактических failure modes, time-to-recover, integration contracts, support workload, anonymized measured customer outcomes и explicit source provenance; не база scraped personal contacts. Продукты используют общие primitives, но должны оставаться exportable/client-owned. Небольшой opt-in content channel и repeat agency relationships снижают зависимость от ranking площадок. Пока ни одна из этих защит не доказана на рынке; в roadmap есть measurable gates.
