# 06. Каталог 30 конкретных офферов

**Дата проверки: 2026-11-13 (Europe/Kyiv).** Метки: VERIFIED — первичный документ или воспроизводимый тест; OBSERVED — ограниченная выборка; ESTIMATED — расчёт; ASSUMED — допущение; UNKNOWN — данных недостаточно. HTTP 200 сам по себе не подтверждает API, спрос или право автоматизации.

Источник всех характеристик — [product_opportunities.csv](../../data/product_opportunities.csv): проблема, buyer, evidence, alternatives, MVP/reuse/demo, разовый чек/подписка, build/rollout/support часы, канал, ограничения, Codex feasibility и first-sale uncertainty. Цены в USD — **ASSUMED price experiments**, не validated market prices. Труд $20/h — opportunity-cost допущение, не наша историческая ставка. Никаких готовых продуктов этим каталогом не создано.

| ID | Оффер | Buyer | Чек $ (A) | Build h (A) | Внедрение h (A) | Support h/month (A) | Subscription $/month (A) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P01 | Telegram Bot Deployment & Recovery | Владелец бота без дежурного DevOps | 350.0 | 12.0 | 8.0 | 1.0 | 39.0 |
| P02 | WooCommerce Order-to-Telegram Connector | Небольшой магазин или WP-агентство | 500.0 | 20.0 | 12.0 | 1.0 | 39.0 |
| P03 | Supabase Tenant Access Test Review | SaaS founder с Supabase | 450.0 | 10.0 | 10.0 | 0.5 | 39.0 |
| P04 | Webhook Delivery & Replay Kit | Агентство с несколькими API | 600.0 | 16.0 | 14.0 | 1.0 | 39.0 |
| P05 | Telegram Recovery Runbook License | Python bot developer | 49.0 | 24.0 | 0.25 | 0.25 | 0.0 |
| P06 | Prozorro CPV Digest for Micro-Agencies | Агентство web/IT | 150.0 | 28.0 | 4.0 | 1.0 | 29.0 |
| P07 | EU Tender Winner Evidence Pack | White-label агентство | 250.0 | 24.0 | 6.0 | 1.0 | 49.0 |
| P08 | Grant Deliverable Evidence Dashboard | Небольшой консорциум | 900.0 | 40.0 | 24.0 | 2.0 | 59.0 |
| P09 | CRM-to-Telegram Lead Acknowledgment | SME sales team | 400.0 | 20.0 | 10.0 | 1.0 | 29.0 |
| P10 | Flask/Gunicorn Deployment Handover | Small Python studio | 250.0 | 8.0 | 6.0 | 0.5 | 29.0 |
| P11 | Supabase Migration Rollback Rehearsal | Early SaaS team | 500.0 | 18.0 | 12.0 | 1.0 | 39.0 |
| P12 | React Admin CSV Import Validator | Ops team | 550.0 | 30.0 | 12.0 | 1.0 | 19.0 |
| P13 | Supabase Auth Email Flow Diagnostic | SaaS founder | 350.0 | 16.0 | 8.0 | 1.0 | 29.0 |
| P14 | WordPress Unsupported Plugin Migration Assessment | WP site owner | 400.0 | 20.0 | 10.0 | 1.0 | 39.0 |
| P15 | WooCommerce Failed Order Notification Rescue | WP agency | 350.0 | 16.0 | 8.0 | 1.0 | 29.0 |
| P16 | OpenAPI Client Migration Toolkit | Developer team | 700.0 | 32.0 | 16.0 | 1.0 | 39.0 |
| P17 | Browser-to-CRM Manual Capture Extension | Small sales team | 800.0 | 40.0 | 20.0 | 2.0 | 39.0 |
| P18 | Company Registry Change Journal | Firm monitoring own entities | 600.0 | 36.0 | 12.0 | 1.0 | 49.0 |
| P19 | Municipal Open Data Quality Report | Local institution/vendor | 450.0 | 24.0 | 12.0 | 1.0 | 39.0 |
| P20 | Public Dataset API Wrapper | Research organization | 650.0 | 30.0 | 16.0 | 1.0 | 49.0 |
| P21 | Energy Price Threshold Telegram Digest | Small energy consultant | 250.0 | 20.0 | 6.0 | 0.5 | 19.0 |
| P22 | Agency White-Label Integration Sprint | Small digital agency | 900.0 | 8.0 | 20.0 | 1.0 | 0.0 |
| P23 | n8n Workflow Handover & Recovery | SME workflow owner | 450.0 | 16.0 | 10.0 | 1.0 | 39.0 |
| P24 | Zapier/Make Task Cost Review | SME automation buyer | 300.0 | 12.0 | 6.0 | 0.5 | 19.0 |
| P25 | Consent-Safe Form-to-CRM Package | European small business | 550.0 | 24.0 | 12.0 | 1.0 | 29.0 |
| P26 | Client Portal Status Dashboard | Small agency | 650.0 | 30.0 | 16.0 | 1.0 | 29.0 |
| P27 | GitHub Release-to-Migration Digest | Maintainer-dependent team | 350.0 | 24.0 | 8.0 | 1.0 | 19.0 |
| P28 | Dead-Link & Critical Form Check | SME website owner | 350.0 | 18.0 | 8.0 | 1.0 | 29.0 |
| P29 | Tenant Data Export/Delete Workflow | SaaS founder | 700.0 | 28.0 | 16.0 | 1.0 | 39.0 |
| P30 | AI Spend Guard & Provenance Ledger | Small AI product team | 550.0 | 24.0 | 12.0 | 1.0 | 39.0 |

## Demand и альтернативы каждого оффера

| ID | Проблема | Evidence и его предел | Каналы-кандидаты | Ограничение |
| --- | --- | --- | --- | --- |
| P01 | Перезапуски и утерянное состояние | FH-1664211; FH-1662753; C26-C29; budget mismatch remains | D01,D02,D04,D34 | Нужны client-owned hosting/secrets; не обещать zero downtime |
| P02 | Потерянные уведомления о заказе | GH-woocommerce-woocommerce-69438; GH-woocommerce-woocommerce-69807; C06-C08 | D01,D03,D15,D19 | Order ПД; merchant permission; free plugins may suffice |
| P03 | Риск cross-tenant чтения/записи | GH-supabase-supabase-47206; GH-supabase-supabase-48382; C24 | D02,D10,D34 | Не сертификация безопасности; нужен экспертный review |
| P04 | Повторные и пропущенные события | GH-woocommerce-woocommerce-69438; GH-n8n-io-n8n-42667; C03-C05 | D04,D18,D19,D23 | Exactly-once внешние эффекты не гарантировать |
| P05 | Нет проверенного шаблона восстановления | Same problem evidence as P01; product purchase intent UNKNOWN; C29 | D24,D25,D29,D34 | Копирование; поддержка сверх license отдельная; нет distribution evidence |
| P06 | Слишком много нерелевантных закупок | S02 API works; buyer demand UNKNOWN; C30-C32 | D01,D04,D34 | API не lead consent; feed historical; качество awards не доказано |
| P07 | Нужен контекст потенциального партнёра | S09/S18/S19 JSON; paid demand UNKNOWN; C30 | D04,D12,D34 | Победитель может не нуждаться в субподряде |
| P08 | Разрозненные артефакты отчётности | S10 official extracts page; C33-C34; paid demand UNKNOWN | D12,D14,D34 | Грантовый бюджет не бюджет ПО; долгий procurement |
| P09 | Заявки без подтверждения | FH-1661880 integration request; C01-C05 | D01,D03,D18 | CRM license/API limits; ПД не слать в group |
| P10 | Бот работает только через __main__ | Repository audit; C29; external buyer intent UNKNOWN | D01,D04,D24 | Не переносить monitoring thread в multiple WSGI workers |
| P11 | Страх необратимой миграции | C24; no direct sampled buyer evidence | D02,D10,D34 | Restore permissions and RPO/RTO must be scoped |
| P12 | Ошибки импорта данных | C10-C13 alternatives; demand UNKNOWN | D02,D25,D34 | Generic admin already free; differentiation per industry |
| P13 | Ломаются invitation/reset flows | C24 ecosystem; sampled RLS issues do not prove this specific problem | D02,D10 | Email deliverability external; scope test account only |
| P14 | Неясна безопасная замена плагина | S14 metadata works; old updated date not abandonment proof; C20-C23 | D09,D15,D20 | Нужны license and owner consent; no vulnerability claim from age |
| P15 | Не видно проваленных webhook sends | Same WC issues as P02; not independent demand evidence | D03,D09,D15 | Отличать payment failure от webhook failure |
| P16 | Breaking API client change | S24 release metadata; no paid migration request sampled | D22,D23,D34 | Generated code review; upstream licenses |
| P17 | Ручной перенос разрешённых данных | C18-C19 alternatives; buyer intent UNKNOWN | D21,D29 | Store review; broad permissions; site terms |
| P18 | Трудно объяснить изменение записей | S12 auth gate; S17 usable; C35-C36 | D04,D34 | ПД entrepreneurs; no opaque name matching |
| P19 | Неизвестна свежесть наборов | S01/S08 metadata; no buyer proof | D12,D34 | Metadata modified time not underlying data freshness |
| P20 | Нестабильные CSV форматы | S29 metadata; exact resource not tested; C14 | D23,D24,D34 | Upstream license/availability; cannot promise real time |
| P21 | Ручная проверка hourly price | S28 JSON; no paid customer evidence | D04,D25,D34 | Legacy dataset recency and country coverage verify |
| P22 | Пик API integration backlog | C37-C38 services exist; intent for us UNKNOWN | D04,D12,D13,D18 | Capacity; IP and no-poaching agreement; manual sale |
| P23 | Сценарий сломан после ухода автора | GH-n8n-io-n8n-42667; GH-n8n-io-n8n-37361; C03 | D18,D19,D34 | License and commercial hosting restrictions unresolved |
| P24 | Неожиданный usage bill | C01-C02 public usage pricing; pain/payment UNKNOWN | D17,D18,D34 | Savings not guaranteed; account consent required |
| P25 | Нет прозрачной обработки заявки | GDPR/EPRIVACY rules; demand UNKNOWN | D02,D04,D34 | Юрист проверяет notices/lawful basis; не compliance certification |
| P26 | Повторяющиеся запросы о ходе работ | C10-C13 free alternatives; buyer intent UNKNOWN | D02,D12,D25 | Commodity; tenancy; scope creep |
| P27 | Breaking changes замечены поздно | S13/S24 release APIs; not buying evidence | D22,D23,D34 | ToS no unsolicited ads; release does not imply breakage |
| P28 | Ключевая форма не отправляет заявки | C15-C17/C25 existing products; demand UNKNOWN | D02,D03,D34 | Нельзя отправлять real forms или scan чужие сайты |
| P29 | Ручные user-data requests | GDPR Art 15/17 workflow; paid demand UNKNOWN | D02,D10,D34 | Legal exceptions; identity verification; no blanket deletion |
| P30 | Нет budget cap и источников claims | Repo lacks spend control; public AI pricing; paid demand UNKNOWN | D22,D23,D34 | Tokenizer/provider discrepancies; AI inference still untrusted |

## Unit economics и честная маржа

Каталог использует одну прозрачную формулу: `cash contribution = price × (1−0.03 refund) × (1−0.10 fee) − $3 direct cost`; `labor-adjusted contribution = cash contribution − $20 × (delivery_hours + support_hours)`. Это первый месяц с одним support cycle; последующие расходы при отсутствии subscription должны быть ограничены договором. Gross margin без труда обманчиво высока; отдельные колонки показывают результат с трудом. Не включены налог, распределённый presales/marketing и build amortization — [07](07_REVENUE_MODEL.md) учитывает их временем и отдельными вычислениями. Конкретный optimizer использует product-specific cash costs, поэтому его net не обязан совпадать с унифицированной conservative catalog formula.

| ID | Cash contribution $ (E) | Cash margin % до труда (E) | После delivery+1 support cycle по $20/h (E) |
| --- | --- | --- | --- |
| P01 | 302.55 | 86.4 | 122.55 |
| P02 | 433.5 | 86.7 | 173.5 |
| P03 | 389.85 | 86.6 | 179.85 |
| P04 | 520.8 | 86.8 | 220.8 |
| P05 | 39.78 | 81.2 | 29.78 |
| P06 | 127.95 | 85.3 | 27.95 |
| P07 | 215.25 | 86.1 | 75.25 |
| P08 | 782.7 | 87.0 | 262.7 |
| P09 | 346.2 | 86.5 | 126.2 |
| P10 | 215.25 | 86.1 | 85.25 |
| P11 | 433.5 | 86.7 | 173.5 |
| P12 | 477.15 | 86.8 | 217.15 |
| P13 | 302.55 | 86.4 | 122.55 |
| P14 | 346.2 | 86.5 | 126.2 |
| P15 | 302.55 | 86.4 | 122.55 |
| P16 | 608.1 | 86.9 | 268.1 |
| P17 | 695.4 | 86.9 | 255.4 |
| P18 | 520.8 | 86.8 | 260.8 |
| P19 | 389.85 | 86.6 | 129.85 |
| P20 | 564.45 | 86.8 | 224.45 |
| P21 | 215.25 | 86.1 | 85.25 |
| P22 | 782.7 | 87.0 | 362.7 |
| P23 | 389.85 | 86.6 | 169.85 |
| P24 | 258.9 | 86.3 | 128.9 |
| P25 | 477.15 | 86.8 | 217.15 |
| P26 | 564.45 | 86.8 | 224.45 |
| P27 | 302.55 | 86.4 | 122.55 |
| P28 | 302.55 | 86.4 | 122.55 |
| P29 | 608.1 | 86.9 | 268.1 |
| P30 | 477.15 | 86.8 | 217.15 |

Разработка Codex: boilerplate, fixtures, contract checks, docs и bounded scripts вероятно выполнимы; оценка не гарантия production correctness. P03/P11/P25/P29 требуют компетентного security/legal/DB review. P17/P20/P06 зависят от разрешений и стабильности внешних источников. Приоритет не означает разрешение выполнять production changes.

## First-sale probability

Для каждого оффера — UNKNOWN. Назначать произвольные 60%/80% по наличию competitor было бы fake validation. Revenue model оценивает условный **портфель**, а не распределяет измеренные odds по продуктам. Чтобы оценивать first sale: фиксировать targeted exposures и qualified inquiries по одному офферу/каналу, затем paid outcomes, интервалы и lag; отдельная гипотеза для каждой страны/цены. Новые идеи P08/P18/P21 не наследуют спрос от найденного заказа на Telegram bot.

## Stop building rule

Один предложенный пакет → synthetic demo ≤12–16h → owner-approved distribution test → минимум один paid scope, лучше два похожих внедрения → reuse. Если бесплатная existing integration закрывает проблему, использовать её. Если 5 qualified buyers не принимают цену/результат, уточнять segment или отложить продукт. Ни 30 строк каталога, ни 38 competitors не являются основанием строить 30 MVP.
