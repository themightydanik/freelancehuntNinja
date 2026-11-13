# 03. Коммерческие стратегии: независимая проверка

**Дата проверки: 2026-11-13 (Europe/Kyiv).** Метки: VERIFIED — первичный документ или воспроизводимый тест; OBSERVED — ограниченная выборка; ESTIMATED — расчёт; ASSUMED — допущение; UNKNOWN — данных недостаточно. HTTP 200 сам по себе не подтверждает API, спрос или право автоматизации.

## Уровни спроса

Ни одной продажи, интервью, paid pilot или согласия на маркетинг не получено. [opportunity_evidence.csv](../../data/opportunity_evidence.csv) — 4 открытых Freelancehunt объявления с technical keywords (из n=6 в одной категории) и 6 GitHub issues (по 2 из трёх репозиториев). Два объявления содержат 2 000 UAH budget; остальные budget UNKNOWN. Это **advertised intent/request**, не выполненная покупка. GitHub issue — problem evidence, даже при многочисленных комментариях. Подборка удобная, не репрезентативная; не измеряет распространённость и TAM. IDs/URLs/dates доступны, контакты/имена не сохранялись.

Более сильное evidence для следующего этапа: конкретный qualified buyer согласовал fixed scope и цену → перечислил оплату → принял результат → повторил заказ/renewal. Без отдельного разрешения на эти действия мы их не выполняем. Публичные цены конкурентов подтверждают существование оффера, не его продажи и не наш product-market fit.

Следующие оценки времени/чека — ASSUMED engineering estimates для эксперимента, не рыночные средние. Все 12 стратегий конкурируют за одни 120h/month; их расходы нельзя одновременно сложить в unlimited capacity.

## T01. Contract Winner Supply Chain

- Потребность и buyer: Award notice → гипотеза о subcontract demand; buyer: delivery director победившего подрядчика.
- Evidence и предел вывода: S02/S09/S18/S19 API samples; ни один supplier в sample не подтвердил намерение нанять. Initial Prozorro detail awards=0; latest follow-up n=2 содержит supplier+UA-EDR, но IT relevance и subcontract need неизвестны.
- Альтернативы: C30-C32 и штатный business development; контракты могут быть закрыты внутренней командой.
- Почему могут выбрать нас (HYPOTHESIS): Только вручную подтверждённый IT scope + подходящий white-label пакет P22, а не продажа списка email.
- Дистрибуция и первая продажа: D12/D18 или существующий opt-in партнёр; notice → ручная квалификация → permitted introduction → paid pilot.
- Автоматизация/человек: Parse CPV/date/award; source citations; score explainability. Решение о контакте/предложении/ставке — owner.
- Переиспользуемый актив: Award evidence pack + event/ID ledger.
- Экономика/срок: ASSUMED 24–40h setup; 1–3h research/company; 30–90d deal. При $900/20h возможна услуга, не доказанный pipeline.
- Ограничения: Не равнять budget award со свободным software budget; procurement terms, confidentiality, contact privacy.
- Метрика и falsification gate (предложение): Из 10 awarded IT notices ≥5 пригодны для ручной квалификации; минимум 2 добровольных discussions до разработки radar.
- Масштаб: Масштаб ограничен каналом и ролью subcontractor, а не количеством notices.

## T02. Grant-to-Product Radar

- Потребность и buyer: После award появляются reporting/deliverable obligations; buyer: project coordinator/finance lead.
- Evidence и предел вывода: S10 CORDIS extracts page и C33/C34 commercial products; оплаты именно нашего dashboard нет.
- Альтернативы: Существующие spreadsheets, EU portal, Instrumentl; маленький consortium может не покупать software.
- Почему могут выбрать нас (HYPOTHESIS): P08 с конкретным deliverable export, funded from eligible budget only after sponsor confirmation.
- Дистрибуция и первая продажа: D12 или существующий институциональный партнёр; проверить procurement → интервью coordinator → sample report → pilot.
- Автоматизация/человек: Metadata normalization и напоминания; eligibility/legal/budget approval только человеком.
- Переиспользуемый актив: Reporting schema + evidence export.
- Экономика/срок: ASSUMED 40–80h build; 24–40h rollout; 45–120d cycle; не near-$0 first cash route.
- Ограничения: Data controller/processor, grant procurement, sensitive reporting; grant size не подтверждение spend.
- Метрика и falsification gate (предложение): 2 coordinators показывают текущий workflow и согласуют цену; до этого stop.
- Масштаб: Высокая настройка по грантовым правилам; нет доказанной универсальности.

## T03. Registry Business Event Intelligence

- Потребность и buyer: Регистрационное событие может требовать обновления внутренних систем; buyer: owner/compliance ops.
- Evidence и предел вывода: S12 auth gate, S17 LEI sample, S04 failed; событие не покупательский intent.
- Альтернативы: C35/C36, Companies House notifications, бухгалтер; generic monitoring уже закрыт.
- Почему могут выбрать нас (HYPOTHESIS): P18 для собственных разрешённых юрлиц с explainable diff; не продажа персональных списков.
- Дистрибуция и первая продажа: D04/content/partner accountant; сначала клиентский список разрешённых ID и opt-in.
- Автоматизация/человек: Entity ID joins, history diff; правомерность поля и уведомления — человек.
- Переиспользуемый актив: Journal + schema mapping.
- Экономика/срок: ASSUMED 36–60h build; 12h setup; 30–90d cycle; лицензии/ключи могут добавить cost.
- Ограничения: ФОП/директора/домашние адреса ПД; re-use terms; sanctions and registry restrictions.
- Метрика и falsification gate (предложение): 5 entities tracked correctly; хотя бы один оплаченный scoped request перед расширением.
- Масштаб: Coverage и lawful use ограничивают больше, чем ingestion speed.

## T04. Integration Gap Detector

- Потребность и buyer: Конкретный workflow ломается между двумя системами; buyer: owner/agency tech lead.
- Evidence и предел вывода: GH WC webhook и n8n Telegram issues; FH integration request; только problem/request evidence.
- Альтернативы: C01-C08, бесплатные connectors/templates; большинству не нужен новый connector.
- Почему могут выбрать нас (HYPOTHESIS): P04/P02: fixture-backed delivery, retries, owner handover для одного незакрытого кейса.
- Дистрибуция и первая продажа: D01/D04/D18/D19; demo → qualified request → reproduce → fixed quote → paid pilot.
- Автоматизация/человек: Read-only issue clustering и fixtures; scope, pricing, upstream reply и production changes вручную.
- Переиспользуемый актив: Event ledger, API adapter contracts, replay guard.
- Экономика/срок: ASSUMED 16–32h reusable base; 8–14h rollout; 7–30d first deal if qualified lead exists.
- Ограничения: API ToS, credentials and client data; не писать рекламу в issues; n8n license отдельно.
- Метрика и falsification gate (предложение): 3 independent workflows requiring same fix; 2 paid pilots; <2h monthly support/client.
- Масштаб: От service к repeatable adapter после нескольких одинаковых внедрений, не раньше.

## T05. Plugin Abandonment & Migration Radar

- Потребность и buyer: Необновляемый dependency тревожит site owner; buyer: WP owner/agency.
- Evidence и предел вывода: S14 metadata; дата обновления не доказывает vulnerability или abandonment.
- Альтернативы: C20-C23, auto-updates, maintainer support и бесплатная замена.
- Почему могут выбрать нас (HYPOTHESIS): P14 staged migration/recovery с реальной несовместимостью, не scary security report.
- Дистрибуция и первая продажа: D09/D15/D20 или customer opt-in; inventory → reproduce issue → staging demo → quote.
- Автоматизация/человек: Metadata and version compatibility checks; vulnerability claim/exploitation/owner contact не автоматизировать.
- Переиспользуемый актив: Compatibility fixtures + migration checklists.
- Экономика/срок: ASSUMED 20–32h base; 10–20h job; 7–30d after accepted request.
- Ограничения: Не сканировать чужие сайты без согласия; GPL/code license; backups include ПД.
- Метрика и falsification gate (предложение): 1 confirmed functional break + reversible migration on staging; paid acceptance.
- Масштаб: Расход поддержки растёт с числом plugins; отбирать один ecosystem.

## T06. Public Data Micro-SaaS

- Потребность и buyer: Регулярный информационный workflow; buyer: narrowly defined professional user.
- Evidence и предел вывода: S02/S17/S28 usable samples; buyers and recurring value UNKNOWN.
- Альтернативы: C15/C30/C35 и бесплатные порталы/CSV; опасность wrapper without value.
- Почему могут выбрать нас (HYPOTHESIS): P06/P21 только с проверенным decision-saving workflow и точностью/свежестью.
- Дистрибуция и первая продажа: Own content + partner; show digest → opt-in use → renewal interview → paid subscription.
- Автоматизация/человек: Read-only ingest/diff/digest; выводы о клиентах, коммерческие контакты вручную.
- Переиспользуемый актив: Versioned normalized event store.
- Экономика/срок: ASSUMED 28–60h MVP; $0–30/mo infra, $19–49/mo offer; weeks-months sales; no measured churn.
- Ограничения: Dataset license, attribution, ПД and uptime; free tier not SLA.
- Метрика и falsification gate (предложение): 5 recurring opt-in users, 2 paid renewals, weekly active use, true-positive value.
- Масштаб: Data freshness/coverage and support load are moat candidates, not raw public availability.

## T07. Open-Source Service Funnel

- Потребность и buyer: Developer can self-serve code but may pay for integration/recovery; buyer: engineering lead.
- Evidence и предел вывода: S13 issues/S23 npm/S24 package metadata; downloads/stars не buyers.
- Альтернативы: C03-C05/C29 free tools; same OSS users may prefer DIY.
- Почему могут выбрать нас (HYPOTHESIS): Tiny tested P04/P05 primitive + transparent paid scoped setup; most value in proof/handover.
- Дистрибуция и первая продажа: D19/D23/D24/D34; useful sample → docs click → voluntary inquiry → qualification → service.
- Автоматизация/человек: Package/test/docs generation; публикации и community promotion owner-approved.
- Переиспользуемый актив: One primitive shared with services, never separate 100h free product.
- Экономика/срок: ASSUMED ≤16h initial sample; 3h/wk docs maintenance; 14–90d sales, distribution uncertain.
- Ограничения: Code licenses, trademarks, platform self-promotion rules; no issue spam.
- Метрика и falsification gate (предложение): Measured docs→inquiry; 100 targeted visits with zero qualified inquiry triggers repositioning.
- Масштаб: Distribution compounding plausible but unproven; avoid unpaid unlimited support.

## T08. Marketplace Distribution Network

- Потребность и buyer: Buyer already searches for deliverable; owner chooses fixed package.
- Evidence и предел вывода: Public platform rules and FH active requests; reach/our conversion UNKNOWN.
- Альтернативы: Existing rated sellers, C37/C38 agencies and no-code substitutes.
- Почему могут выбрать нас (HYPOTHESIS): One narrow proof-backed offer P01/P02 with clear exclusions and acceptance.
- Дистрибуция и первая продажа: D01 plus one conditional D02/D04/D03; manual listing after eligibility check; quote and paid pilot.
- Автоматизация/человек: Asset reuse, attribution and qualified-lead tracking; registrations/messages/payments manual.
- Переиспользуемый актив: Canonical offer assets, demo, FAQ, scope template.
- Экономика/срок: ASSUMED 8–16h per first two channels; 7–60d to sale not guaranteed; platform fees matter.
- Ограничения: KYC, residence, payout, tax, ToS; zero-review trust hurdle.
- Метрика и falsification gate (предложение): Impressions→clicks→qualified→proposal→paid tracked separately by channel.
- Масштаб: Network of 30 empty profiles is negative ROI; expand only winning channel.

## T09. Website Improvement Engine

- Потребность и buyer: Verified conversion-path failure; buyer: website owner.
- Evidence и предел вывода: C15-C17/C25 existing monitors; no permissioned customer failure found in research.
- Альтернативы: Free uptime/form tools and internal QA; cosmetic score not buying need.
- Почему могут выбрать нас (HYPOTHESIS): P28 with reproducible functional error and fixed-price repair, on authorized scope.
- Дистрибуция и первая продажа: D02/D03/D34; public synthetic demo → inbound consent → no-submit test → accepted repair.
- Автоматизация/человек: Consented synthetic checks; actual form submission, scanning or contact require approval.
- Переиспользуемый актив: Browser fixtures and before/after report.
- Экономика/срок: ASSUMED 18h base; 8–12h repair; 7–30d after inbound inquiry.
- Ограничения: No third-party unconsented crawling/scanning, fake leads, or security exploit claims.
- Метрика и falsification gate (предложение): Buyer confirms actual operational loss and pays for repair; score improvement alone insufficient.
- Масштаб: Niche-specific checks scale better than generic lighthouse reports.

## T10. Agency White-Label Partnerships

- Потребность и buyer: Capacity spikes at agency; buyer: delivery director/technical lead.
- Evidence и предел вывода: C37/C38 alternatives exist; no agency confirmed subcontract demand for us.
- Альтернативы: In-house staff, vetted networks, offshore teams; trust and legal fit decide.
- Почему могут выбрать нас (HYPOTHESIS): P22/P04 fixed acceptance, repo ownership, repeat delivery; no replacement staffing promise.
- Дистрибуция и первая продажа: D04/D12/D18 or existing trusted introductions; case demo → permitted meeting → NDA/scope → pilot.
- Автоматизация/человек: Capability inventory/fixtures; agency outreach, negotiations, contract/IP decisions manual.
- Переиспользуемый актив: Integration base and agency-specific runbook.
- Экономика/срок: ASSUMED 8h collateral; 20h/$900 sprint; 14–60d cycle if eligible channel works.
- Ограничения: IP assignment, NDA, no-poach, subcontract consent and processor agreement.
- Метрика и falsification gate (предложение): 2 paid sprints, lead time, effective hourly margin and repeat order rate.
- Масштаб: Lower acquisition per repeat agency plausible; concentration risk cap one agency share.

## T11. Regulation Deadline Engine

- Потребность и buyer: A legal obligation may require a system change; buyer: responsible officer.
- Evidence и предел вывода: GDPR/ePrivacy primary documents available; specific new deadline/buyer budget NOT identified.
- Альтернативы: Law firms, trade associations, existing compliance tools; generic dates often free.
- Почему могут выбрать нас (HYPOTHESIS): Only narrow lawyer-reviewed checklist plus implementation P25/P29; never AI legal advice.
- Дистрибуция и первая продажа: Partner legal/accounting firm with opt-in audience; verified applicability before proposal.
- Автоматизация/человек: Official-source change detection and citations; applicability/legal interpretation/claim approval manual.
- Переиспользуемый актив: Source-provenance ledger + reviewed rule version.
- Экономика/срок: ASSUMED 40–80h research + paid expert; weeks-months cycle; incompatible with literal $0 legal certainty.
- Ограничения: Jurisdiction, effective dates, exceptions, liability; current UA laws not fetched successfully.
- Метрика и falsification gate (предложение): Written expert approval, affected user segment, paid implementation request.
- Масштаб: Requires ongoing authoritative legal maintenance; defer as first product.

## T12. Recovery Evidence as Agency Handover Asset

- Потребность и buyer: Handover to a new maintainer exposes undocumented dependencies; buyer: agency inheriting client system.
- Evidence и предел вывода: Repo audit shows this exact technical weakness; external willingness to pay UNKNOWN.
- Альтернативы: C22/C23/C29 backups/deployers do parts; no reason to rebuild those.
- Почему могут выбрать нас (HYPOTHESIS): P01/P10 with bounded restore rehearsal, ownership inventory and executable acceptance rather than new platform.
- Дистрибуция и первая продажа: D04/D12/D34; synthetic case study → inherited-system inbound inquiry → access-approved rehearsal → paid handover.
- Автоматизация/человек: Generate inventory names and synthetic recovery checks; secret handling and production restore manual.
- Переиспользуемый актив: One recovery primitive shared with bots, webhook adapters and white-label sprints.
- Экономика/срок: ASSUMED 12–24h reusable base; 6–10h job; $250–450 price experiment; 7–30d after lead.
- Ограничения: Do not read actual secret values into reports; separate access rights and backups retention.
- Метрика и falsification gate (предложение): Recovery achieved within agreed RTO in isolated staging; one paid pilot and measured support.
- Масштаб: Non-obvious combination: due-diligence checklist becomes sales proof plus a reusable acceptance product.

## Приоритет без искусственных баллов

Ранжирование лексикографическое: (1) наличествует конкретный software problem/request, (2) возможно deliver ≤14h без правовых/инфраструктурных блокеров, (3) есть проверяемый demo, (4) reused primitive, (5) может быть достигнут легальный inbound channel. Успех бизнеса не выводится из этого ranking.

TOP-5 для эксперимента: T12 recovery handover, T04 integration reliability, T08 одна площадка+один прямой портфель, T10 white-label при уже доступном контакте, T07 OSS как малый supporting asset. T01 procurement — discovery-only challenger; T02/T03/T06/T11 отложить до спроса/доступа. T09 не требует discovery crawler: тестировать только с inbound consent.

Ключевой конфликт: низкие бюджеты в локальной выборке против желаемой ставки. Решение — не «AI будет выигрывать больше», а отдельно проверить англоязычный/agency сегмент и price acceptance. Если этот канал не даёт квалифицированных запросов, менять оффер/канал, не добавлять 20 источников.

## Детальный разбор issue evidence: корректировки гипотез

Источник: [issue_detail_review.csv](../../data/issue_detail_review.csv), точные URL и date; [recheck](../../data/issue_review_verification.json) проверяет technical markers, не воспроизводит баги.

| Issue ID | Тема | Сообщение автора (OBSERVED текст) | Изменение решения |
| --- | --- | --- | --- |
| GH-supabase-supabase-47206 | Security Advisor false positive on PostGIS-owned spatial_ref_sys | Reported unresolvable RLS warning; no tenant-data leak demonstrated | Weak evidence for selling generic RLS scan; favors bounded expert interpretation |
| GH-supabase-supabase-48382 | RLS docs privilege baseline and TRUNCATE distinction | Reported docs/default-grant mismatch; RLS and object privileges differ | Negative authorization tests must include role privileges, not only RLS toggles |
| GH-n8n-io-n8n-42667 | Telegram approval buttons and inherited allowed_updates | Reported callback_query not delivered when previous webhook setting only allows messages | Recovery needs webhook config inventory and allowed_updates fixture; not a generic new connector |
| GH-n8n-io-n8n-37361 | Telegram rich-message line breaks | Reported formatting problem; plain text mode reportedly preserves breaks | May have free workaround; not evidence for new integration product |
| GH-woocommerce-woocommerce-69438 | Delivery-ID collision for same-second distinct webhook events | Reporter alleges receiver dropped legitimate events when deduping solely on delivery header | Treat transport IDs as untrusted until uniqueness tested; semantic resource/version identity needed |
| GH-woocommerce-woocommerce-69807 | Stock notification webhook resource request | Core feature proposal for vendor-neutral stock event topics; no paid intent | Monitor upstream solution; implementing paid duplicate feature could be wasted effort |

Не переносить reported loss одной установки в market failure-rate. Supabase PostGIS issue ослабляет generic RLS scan offer; n8n formatting issue может иметь бесплатный workaround; stock notification request может быть реализован upstream бесплатно. Поэтому commercial proof остаётся UNKNOWN даже при очень конкретной технической боли.
