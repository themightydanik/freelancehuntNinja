# 08. Техническая реализуемость: сравнение, не выбранная заранее архитектура

**Дата проверки: 2026-11-13 (Europe/Kyiv).** Метки: VERIFIED — первичный документ или воспроизводимый тест; OBSERVED — ограниченная выборка; ESTIMATED — расчёт; ASSUMED — допущение; UNKNOWN — данных недостаточно. HTTP 200 сам по себе не подтверждает API, спрос или право автоматизации.

## Первичные ограничения на дату проверки

| Provider / primary source | VERIFIED документ / OBSERVED лимит | Значение для решения | Что НЕ проверено |
| --- | --- | --- | --- |
| [Netlify pricing](https://www.netlify.com/pricing/) | Free 300 credits/month; production deploy 15 credits; при limit проекты account могут pausing | 20 deploys исчерпают весь budget даже без другого usage; frontend optional | Account plan/legacy pricing, реальный bill, cold starts, regional latency |
| [Netlify scheduled functions](https://docs.netlify.com/build/functions/scheduled-functions/) | Cron UTC, published deploys only, 30s scheduled execution | Bounded lightweight batches, не текущий бесконечный Python thread | Live schedule, delivery frequency/SLA, preview doesn't prove schedule |
| [Supabase pricing](https://supabase.com/pricing) | Free 500MB DB, 1GB storage, 5GB egress + 5GB cached, 50k MAU, 500k edge invocations; 2 active projects; pause after 1 week inactivity | Хорош для bounded prototype; event history быстро съедает DB; free не uptime SLA | Создание проекта, billing region, pause behavior, production restore |
| [Supabase function limits](https://supabase.com/docs/guides/functions/limits) | 256MB memory, 150s free wall-clock, 2s CPU/request, 150s idle timeout | Network-heavy small batches возможны; CPU-heavy parsing/AI вне функции | Live max limits/perf under account, concurrency/error behavior |
| [Supabase Cron](https://supabase.com/docs/guides/cron) | Документированный pg_cron scheduling | State/queue близко к DB; scheduler invocation secret надо защищать | Extension enablement, pg_net/edge auth and live delivery не тестировались |
| [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions) | Current page expresses Free allowance as $12 compute usage plus 500MB artifact storage, Linux 2-core $0.006/min | Не копировать старое «2000 минут» без проверки конкретного runner/account; billing не снимает ToS ограничения | Actual repository plan/usage; account billing |
| [Actions schedule](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows) | Default branch only; high load может delay/drop runs; public inactivity60d disables | Не обещать 5-minute freshness или SLA на основе cron YAML | 30-day uptime/lag distribution |
| [GitHub additional terms](https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features) | Hosted runners ограничены production/testing/deployment/publication repository software; serverless/business misuse restrictions | Production opportunity monitoring не рекомендовать как бесплатный serverless backend | Нужна конкретная legal/platform review для use-case |
| [Cloudflare Workers limits](https://developers.cloudflare.com/workers/platform/limits/) | Free 100k requests/day, 128MB, 10ms CPU including Cron; 5 cron triggers/account; subrequest caps | Кандидат небольшого TS worker; complex parsing может превышать CPU | Deployment, account admission, trigger lag, D1/Queues pricing отдельно |
| [Groq model list](https://console.groq.com/docs/models) | Current doc показывает per-model pricing/rates; исходный qwen/qwen3-32b не подтверждён live models call | Нельзя считать текущую hardcoded model гарантированно доступной | Нет key, generation/retention/latency/account quotas не тестировались |

Страницы и HTTP/truncation outcomes сохранены в [policy_page_checks](../../data/policy_page_checks.json), IDs NETLIFY/SUPABASE/SUPA_LIMIT/SUPA_CRON/GH_*/CF/GROQ_CURRENT. Статус 200 с shell/page-not-found не считается полной проверкой. Не делаем никакого remote deploy в исследовании.

## Сравнение A/B/C/D

| Критерий | A Netlify+Supabase+Actions | B Netlify+Supabase Edge+pg_cron | C Free worker hybrid (CF candidate) | D Service-first, client-owned runtime |
| --- | --- | --- | --- | --- |
| Initial cash | ASSUMED $0 до quotas | ASSUMED $0 до quotas | ASSUMED $0 до worker/DB quotas | Research/demo $0; production client compute not magically free |
| Periodic jobs | Actions только CI/research; production ToS gate | Documented cron → edge small batch | Documented Cron Trigger; 10ms CPU free | Existing client scheduler; new hosting не нужно для исследования |
| Delays/reliability | Delay/drop/inactivity restrictions | Pause/free limit; no demonstrated SLA | No measured trigger SLA; CPU cap | Agreed client RTO; recovery rehearsal |
| Runtime | CI Python подходит probes, не daemon hosting | Deno/TS path; Python monolith не drop-in | Worker TS; Python capabilities/tooling require separate check | Python3.13 app import tested; isolate watcher/webhook later |
| Data/history | Supabase relational store + retention | Same DB + transactional checkpoint | Supabase or separately evaluated D1; extra provider boundary | Minimal per-client data; no global harvesting |
| Queue | DB outbox with lease/attempt/dedupe needed | DB job/outbox; cron must not overlap effects | Durable queue/D1 choice + quota evaluation pending | Small durable ledger; manually recover initially |
| Logs | CI logs public/private caveat; redact secrets | Free log retention limited; persist safe run summaries | Worker logs quota pending; no source payloads | Client-owned logs/redaction/retention |
| Auth | Frontend anon key+RLS; CI secret minimal scope | Edge JWT/signature + vault-protected scheduler auth | Signed trigger/service credentials + scoped DB roles | Owner-approved access; no secrets in handover report |
| Secrets | Never frontend service_role/token; no PR/fork exposure | Vault/config secret; rotate owner workflow | Worker secret binding, not code; signed webhook | Secure client vault; names/status only in docs |
| AI | Offline classifier/draft, no automatic spending | Preflight budget; small bounded requests | External inference, 10ms CPU excludes heavy local model | Optional; manual structured output review |
| Growth expense | Netlify credits + Supabase paid tiers; Actions not backend | Supabase paid floor/compute, Netlify optional | Worker paid plan+DB+queue evaluation; not $0 guarantee | Price service to cover actual client infra |
| Main risk | Platform ToS + scheduler reliability | Free pause, DB budget, edge CPU | More integrations, narrow CPU, no actual cloud proof | Limited scale and manual time, but fewer unvalidated dependencies |
| Verdict | CI/research only; reject default production cron design | Conditional first reusable backend after paid demand | Challenger if measured B limitation; not automatic extra worker | Best first validation path for services |

A/UI unnecessary before first paid pilot. B reduces providers for low-volume stateful read jobs but remains unproven in deployed runtime. C only if a real benchmark shows B cannot meet a known job. D fastest way to test commercial demand without building global radar. Netlify static frontend optional; GitHub Pages also has commercial hosting restrictions in additional terms, so не подменять им free business hosting без проверки.

## POC results и пределы

1. **Official source access:** 32 initial bounded requests + 8 initial follow-ups + 8 pagination/quality follow-ups: see [02](02_DATA_SOURCES.md). Latest Prozorro n=2 содержит supplier+UA-EDR; TED2pages×2notices доступны. IT award relevance, cross-source matching и TED supplier detail quality остаются UNKNOWN. No credentialed Freelancehunt write.
2. **Local state:** [state_poc.py](../../research/probes/state_poc.py) in-memory SQLite: source+record_id+canonical payload hash makes replay idempotent; changed payload adds version; injected crash rolls back records+checkpoint; missing ID not joined; leading zeros retained; budget overspend reservation rejected. [state_poc_results](../../data/state_poc_results.json), 15 overall tests in research suite.
3. **Current application:** synthetic import, network denied; neutral callback 200, forged success vulnerability reproduced via mock. Не live webhook delivery или cloud feasibility.
4. **Economics:** reproducible stochastic/optimization scripts run locally; no paid AI or cloud account created. No browser website audits or real forms submitted.

SQLite proof — концепт transactional semantics, **не** тест pg_cron, Supabase RLS, distributed leases, Deno compatibility или production recoverability. Сейчас нельзя назвать B развёрнутым/надёжным.

## Инкрементальность, история и entity resolution

Proposed schema, not implementation: `source_runs`, `checkpoints`, `source_records`, `record_versions`, `organizations`, `organization_aliases`, `signals`, `outbox`, `approvals`, `usage_reservations`. Сигнал ссылается на конкретную source version и extraction rule/version; `observed_fact` отдельно от `ai_hypothesis`, с confidence и evidence URL. AI не должен придумывать company ID, budget, buyer role или факт потребности.

Exact joins only: `(identifier_scheme, identifier)`; retain country/authority and leading zeros. LEI→registry authority ID only if source provides mapping; VAT не всегда совпадает с company registration ID. Нормализация имени — candidate suggestion для manual review, не automatic merge. Missing ID → separate unresolved entity; не join NULLs. Нужны provenance/de-merge/history, source precedence, stale conflicts, tombstone handling и minimally retained contacts. Дедуп event ID не гарантирует exactly-once external effect: внешнему API нужен idempotency key или reconciliation; unknown external status требует human approval перед replay.

Batches ≤2–10 records до benchmark; finite page budget; checkpoint commit after durable payload/outbox; overlap окно после source_updated_at; retry/backoff с jitter и 429 Retry-After; endpoint allowlist и schema assertions; не advance cursor после parse failure. Хэш payload должен исключать volatile fetched_at/порядок keys. Реальное изменение схемы/нет данных/ошибка/удаление — разные состояния. Измерять freshness P50/P95, processed/skipped/error и oldest unprocessed event, не только «cron вызвался».

## AI cost cap и facts versus hypotheses

Первый этап вообще может обходиться без AI: deterministic keyword/category filter, ручная квалификация, шаблонный draft. Current model pricing retrieved, but no live account evidence. Бюджетный пример **ASSUMED rates**, не quote: 2000 input+500 output tokens при $0.30/$0.60 per1M стоит $0.0009/classification; 1000 = $0.90; retries3× = $2.70. При $0.80/$4.00 (OBSERVED doc row для qwen/qwen3.8-27b) это $0.0036/call и $3.60/1000 before retries. Цена reasoning/output accounting может отличаться; tokenizer/provider actual usage reconcile обязательны. Эти model IDs не замена текущего кода в данном PR.

Control: monthly/daily hard cap с reserved upper bound до вызова, max input/output tokens, per-signal call count, cache by model+prompt+payload digest, concurrency limits, explicit user review на увеличение бюджета. POC проверяет local reservation $0.8 из $1 и отказ $0.3; real billing cutoff не тестировался. AI output schema validation и evidence-linked claim ledger обязательны до коммерческого draft; commercial sending всегда отдельный approval.

## Реальные ресурсы и следующие проверки

Free onboarding machine — environment для research, не production host. В нём Python/requirements работают; public HTTP access unrestricted observed; repository Git read и GitHub API read работают. Нужные service credentials не объявлены/не присутствуют как app variables. Не просим секреты для исследования: независимые пробы завершены без них. Future cloud PoC потребует owner-controlled accounts, permitted secure bindings и ограниченный budget; next PR tests 48h scheduling + restart/retention + source errors до каких-либо обещаний SLA.

## Source-contract edge cases из реальных reports

[WooCommerce69438](https://github.com/woocommerce/woocommerce/issues/69438) сообщает, что same-second deliveries разных ресурсов могут иметь одинаковый transport delivery ID. Это report, не воспроизведённая нами ошибка. Следствие: прежде чем выбрать idempotency key, проверить upstream contract на collisions; не использовать header как единственную identity. Семантический ключ должен различать ресурс/topic/version и legitimate repeated events; payload hash не универсальная замена event identity. Наш local POC предполагает корректный source record ID и этот upstream contract не валидирует.

[n8n42667](https://github.com/n8n-io/n8n/issues/42667) описывает inherited allowed_updates без callback_query; recovery/reconfiguration может требовать явного update-type fixture. [Supabase47206](https://github.com/supabase/supabase/issues/47206) описывает RLS warning для extension-owned lookup table; исправлять все предупреждения автоматически опасно. Эти findings усиливают human review и contract fixtures, а не основание переписывать продукт в research.
