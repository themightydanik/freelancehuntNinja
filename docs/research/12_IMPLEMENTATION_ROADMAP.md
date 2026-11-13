# 12. Roadmap 30/60/90/180 дней

**Дата проверки: 2026-11-13 (Europe/Kyiv).** Метки: VERIFIED — первичный документ или воспроизводимый тест; OBSERVED — ограниченная выборка; ESTIMATED — расчёт; ASSUMED — допущение; UNKNOWN — данных недостаточно. HTTP 200 сам по себе не подтверждает API, спрос или право автоматизации.

План условный: Day0 = owner decision после этого research, не сегодняшнее обещание launch. 120h/month capacity — ASSUMED; фактическое время владельца неизвестно. Коммерческие действия в таблице **требуют отдельного разрешения**. Не выполнять их автоматически из этого файла. График payment зависит от eligibility и покупателей, не API availability.

| Период | Work budget (A) | Результат | Evidence gate | Revenue objective, не forecast | Stop/adjust |
| --- | --- | --- | --- | --- | --- |
| Day1–2 | 4–8h | Security owner decision; choose one package and 2 channel checks; free-substitute test | Actual payout/fee status and one synthetic workflow | $0 | Closed channel→replace before build |
| Day3–7 | 12–16h demo +4–6h assets | P01 synthetic restore proof; clear scoped offer+acceptance | Recovery test pass, no secret leakage, delivery estimate ≤10h | No assumed sale | Can't demonstrate→reduce scope |
| Day8–30 | ≤24h acquisition, ≤40h total reusable build; rest delivery/learning | Owner-approved one listing+one tutorial; cohort ledger; pilot if buyer exists | Impressions if available, tracked clicks, qualified inquiries and accepted scopes separate | First$500 aspirational via2small jobs or1replay; Base median month1$0 | No exposure→distribution experiment; no qualified→reposition |
| Day31–60 | 24h acquisition,4–12h improvements, capped delivery/support | Repeat same P01 offer; P04 only if related customer demand |2similar paid pilots; effective rate; no unapproved production actions | First$1000month after refunds requires~3×350 |5qualified/no sale→price/trust/problem review |
| Day61–90 | Capacity120h; no >2 core service variants | Repeat agency/marketplace lane; conditional P02; opt-in maintenance |Margin and actual support≤1–2h/client/month; measured lead→paid lag | $2k goal still unproven; Base conditional~7%month90 | Costs/time exceed quote→scope/price; no market signal→stop broad build |
| Day91–180 |24h acquisition +operating load; small≤4h/week challenger | Double down on winning offer/channel; reuse primitive; renewable maintenance |2renewals and retention; low client concentration; quality/restore regression | Base conditional~24%month180; upside not promise | Revenue plateau due leads→channel; capacity→pricing/reuse; no renewals→no SaaS claim |

## Зависимости и бюджет

Security/handover work не обязан блокировать synthetic research demo, но использование live credentials/production bot требует remediation/owner approval. Partner/store approval может занять неизвестное время; не ставить его в critical path первого small service. Frontend dashboard, Supabase multi-tenant SaaS и30source adapters до demand gate не нужны.

Cash floor$0–5/month для demo/probes; research used no paid APIs. Reserve$25–50/month на reliable production/AI после принятого demand — ASSUMED budget, explicit owner spend gate, actual vendor quote separately. Client-owned infrastructure costs оформлять прозрачно. Professional legal/security review может требовать отдельного бюджетаUNKNOWN; не утверждаем полную compliance за$0. Tax/social contributions и личный runway не рассчитаны без данных владельца.

## Weekly decision review

Короткий ledger: `offer/channel/cohort_date/exposures_if_known/clicks/qualified/negotiations/proposals/accepted/paid_at/refund/platform_fee/delivery_h/support_h/repeat`. Contacts хранить отдельно с законным основанием. Делить cohorts по ценам/языку/стране, не смешивать один случай с «высоким спросом». Показать отказ/no-data, не заменять их AI optimism.

После2paid пилотов заменить priors в модели измеренными диапазонами; приnмаленьком uncertainty остаётся широкой. После30/60/90days сравнивать не только revenue, но contribution/hour и time budget. Переоценивать roadmap по наблюдениям; рост источников данных не метрика успеха.

## Возможная архитектурная последовательность

Локальные synthetic fixtures → client-owned single integration → durable state/outbox только когда нужен повторный scheduler → B(Supabase Cron/Edge) bounded cloud PoC по отдельному разрешению → optional Netlify UI → maintenance/product license. C(worker) только при measured constraint B. A(Actions) остаётся CI. Все gates и конкретные PR — [13](13_PR_PLAN.md).
