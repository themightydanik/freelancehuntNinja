# 16. Два направления Ninja: проверка механизма покупателей

**Дата проверки: 13 ноября 2026, Europe/Kyiv.** VERIFIED — первичный документ/воспроизводимый тест; OBSERVED — ограниченная выборка; ESTIMATED — расчёт; ASSUMED — допущение; UNKNOWN — недостаточно данных. Никаких продаж, публикаций офферов, регистраций, платежей, rotation или production changes не выполнялось.

Оригинальную идею Ninja сохраняем как **объяснимый радар событий и повторяющихся интеграционных проблем**, а не автоматический генератор сообщений. Источник события, technical pain, buyer need и cleared payment — четыре разных уровня evidence. Ни один record ниже не конвертируется в коммерческий lead автоматически.

## A. Contract Winner Supply Chain — реальные IT awards

Два ограниченных TEDsearch: `classification-cpv=72200000` и более узкий`72262000`, `notice-type=can-standard`, publication≥20261001, latest versions, по 5 notices. Первый query reported1646matches, это не число покупателей. `form-type=can` первоначально дал 400; исправлено на документированный notice-type, без обхода защиты. [первый sample](../../data/it_award_sample.csv), [development stratum](../../data/it_award_development_stratum.csv), [manifest](../../data/challenger_probe_manifest.json), [verification](../../data/award_verification.json).

Получены реальные опубликованные значения award/winner, а не общий feed закупок. Все currencies сохраняются раздельно; award amount не наш budget. В двух notices winner поля пусты — они исключены из partner shortlist. Hardware Security Module не выдаём за подходящий software subcontract. Число 5 в каждом query — ограничение пробы, не оценка всего доступного рынка.

| Notice | Опубликованный winner | Релевантность | ARES match | Решение |
| --- | --- | --- | --- | --- |
| 674335-2026 | Esri Polska Sp. z o.o. | GIS requirements/migration planning; Esri-specific specialist skills | no | low_for_initial_offer |
| 674368-2026 | Tekies s.r.o. | IT delivery/consultancy; potential agency capability fit | yes | manual_qualify_only |
| 674561-2026 | Principal engineering s.r.o. | IT delivery/consultancy; potential agency capability fit | yes | manual_qualify_only |
| 674738-2026 | OIXIO IT AS | Hardware Security Module, mixed hardware/software/security | no | reject_initial_scope |
| 674764-2026 | UNKNOWN | Security content/signing maintenance; winner absent in search fields | no | exclude_unresolved_winner |
| 674807-2026 | Perfect System, s.r.o. | Prague Castle cash/ticketing system; product-specific delivery | yes | low_for_initial_offer |
| 675574-2026 | SAYME MONITORIZACIÓN ESTRUCTURAL,S.L. | Access control software adaptation, specialized supplier | no | low_for_initial_offer |
| 676131-2026 | OR-NEXT spol. s r.o. ; OR-NEXT spol. s r.o. | Existing ISEPA software support | yes | low_for_initial_offer |
| 676728-2026 | Bindworks s.r.o. ; Bindworks s.r.o. | Existing zScanner software support | yes | low_for_initial_offer |
| 676994-2026 | UNKNOWN | Enterprise portfolio management installation/support | no | exclude_unresolved_winner |

### Проверка личности поставщика

VERIFIED public registry responses ARES по пяти **строковым** CZ-IČO:07241127 Tekies,26775794 Principal engineering,26480981 Perfect System,26284146 OR-NEXT,07436505 Bindworks. Имена в национальном реестре совпадают с corporate names изTED; leading zero сохранён. Публичные адреса/контакты/директора не сохранялись. Это подтверждение legal-entity mapping, **не** подтверждение желания сотрудничать или ownership любого найденного домена.

Пример национального primary source: [ARES Tekies](https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/07241127); остальные URL/даты/статусы вverificationJSON. Для Esri и испанского supplier — TED-only; непроверенный person-like identifier не сохраняется. Нельзя fuzzy-join имя к LinkedIn/email и считать contact permission установленным.

Notice XML для 674368-2026вернулHTTP202с пустым body. Детальная contract/subcontract документация в этой пробе **не проверена**, gate открыт; никакого обхода браузерной защиты/повторов challenge не делалось. Сведения supplier вTEDsearch не заменяют полный договор или procurement terms. OR-NEXT/Bindworks названия повторяются по lots: это не новые independent partner companies.

### Кто может стать покупателем и как

Кандидаты для **ручной** проверки — Tekies и Principal engineering: ITdelivery/consultancy ближе к внешней engineering capacity, чем поставка HSM или поддержка закрытого продукта. Но конкретная роль buyer, tech stack, возможность subcontract, необходимость внешнего исполнителя и partner-intake channelUNKNOWN. EsriGIS, Perfect Systemticketing, OR-NEXTISEPA, BindworkszScanner имеют domain/incumbency barriers; маленький Telegram package не следует из их контракта.

Проверяемая цепочка: notice→точный company ID→ручной contract/technology/role review→**явно открытый supplier/partner-intake либо существующее consented introduction**→разговор с delivery lead→один scoped white-label pilot. Если такой intake не найден/нет согласия, контакт не выполнять. Сам факт выигранного контракта не разрешает email/DM и не доказывает свободный бюджет; public procurement может ограничивать subcontract.

Сейчас confirmed partner conversations0, proposals0, payments0. Цель следующего owner-approved challenger:≤5 corporate cases, по каждому отметить опубликованный допустимый путь партнёрства/его отсутствие,1–2 consented conversations при наличии такого пути. CostASSUMED2–4 hreview, $0 public data; legal/specialist review и фактический sales cycleUNKNOWN, возможно недели/месяцы. Нет intake/fit→отбрасываем case, не добавляем contacts. Нельзя использовать непроверенную «conversion из 1646 awards» в финансовой модели.

## B. Integration Gap Detector — пять конкретных pain families

13 публичных reports,5 families. Reporter IDs сравнивались только вRAM; сохранены локальные anonymous groups, technical titles/URLs/dates/state, без usernames/emails/body. В каждой family2–3 разных account IDs. Это **разные аккаунты**, не доказательство разных организаций, независимых deployments, одинакового root cause или paying buyers. Часть issues историческая/закрытая и может быть решена в новых версиях. [reportsCSV](../../data/integration_gap_reports.csv), [manifest](../../data/challenger_probe_manifest.json).

### G01_telegram_webhook_lifecycle: Telegram Trigger silently stops delivering updates after activation/test or configuration changes

- Повторяемость: 3 accounts /3reports; shared symptom, different/unknown root causes.
- Реальные reports: [n8n-io/n8n#18754](https://github.com/n8n-io/n8n/issues/18754), [n8n-io/n8n#18895](https://github.com/n8n-io/n8n/issues/18895), [n8n-io/n8n#13385](https://github.com/n8n-io/n8n/issues/13385). State/version/created_at вCSV; текст изучен, upstream defect не воспроизводился.
- Бесплатный путь: n8n common-issues guide: HTTPS WEBHOOK_URL, proxy/WebSocket setup and reset test execution; Telegram getWebhookInfo/setWebhook contract. [guide](https://docs.n8n.io/integrations/builtin/trigger-nodes/n8n-nodes-base.telegramtrigger/common-issues/).
- Возможное коммерческое преимущество(HYPOTHESIS): No new connector required for many configurations; customer-specific diagnosis/recovery/handover may have value.
- Решение/gate: Service candidate only; reproduce exact client fault first; no claim that all reports share one bug.

### G02_telegram_large_files: Telegram cloud getFile rejects files above20MB; downstream integration loses attachment

- Повторяемость: 3 accounts /3repositories.
- Реальные reports: [codingteam/emulsion#181](https://github.com/codingteam/emulsion/issues/181), [irazasyed/telegram-bot-sdk#1129](https://github.com/irazasyed/telegram-bot-sdk/issues/1129), [chatwoot/chatwoot#16110](https://github.com/chatwoot/chatwoot/issues/16110). State/version/created_at вCSV; текст изучен, upstream defect не воспроизводился.
- Бесплатный путь: Official Telegram docs: cloud download20MB; local Bot API server can remove download size limit and support uploads up to2000MB. [API](https://core.telegram.org/bots/api).
- Возможное коммерческое преимущество(HYPOTHESIS): Local server software is free but hosting/operation/privacy are not; official workaround may suffice.
- Решение/gate: Do not build another file relay without a recurring consented media workflow and budget.

### G03_wc_event_semantics: WooCommerce notification semantics create unsafe dedup/duplicate business-effect handling

- Повторяемость: 2 accounts /2reports; ID collision vs create+update are different cases.
- Реальные reports: [woocommerce/woocommerce#69438](https://github.com/woocommerce/woocommerce/issues/69438), [woocommerce/woocommerce#41544](https://github.com/woocommerce/woocommerce/issues/41544). State/version/created_at вCSV; текст изучен, upstream defect не воспроизводился.
- Бесплатный путь: Official webhooks and existing integrations; filter topic/resource/version, test idempotency keys; current core fixes must be checked. [guide](https://woocommerce.com/document/webhooks/).
- Возможное коммерческое преимущество(HYPOTHESIS): Contract fixtures and semantic event ledger can be reused for actual integration delivery; no proof of a new paid product.
- Решение/gate: Strong candidate for small P04primitive only after client reproduction; never trust transport header alone.

### G04_postgis_advisory: Supabase/PostGIS security guidance or warnings cannot be acted on as a simple owner/schema change

- Повторяемость: 2 accounts /2reports; related workflow, not identical security vulnerability.
- Реальные reports: [supabase/supabase#47206](https://github.com/supabase/supabase/issues/47206), [supabase/supabase#29122](https://github.com/supabase/supabase/issues/29122). State/version/created_at вCSV; текст изучен, upstream defect не воспроизводился.
- Бесплатный путь: Built-in free Advisors, current PostGIS guide and vendor issue resolution; review extension ownership and public lookup data. [guide](https://supabase.com/docs/guides/database/extensions/postgis).
- Возможное коммерческое преимущество(HYPOTHESIS): Expert explanation and safe migration rehearsal may help; warning count is not vulnerability severity.
- Решение/gate: Reject generic paid RLS scanner; no universal ALTER/disable-RLS fix, specialist gate.

### G05_stripe_raw_body: Stripe signature verification fails when Next.js body is consumed/parsed before raw verification

- Повторяемость: 3 accounts /3reports, different framework versions.
- Реальные reports: [vercel/next.js#60002](https://github.com/vercel/next.js/issues/60002), [vercel/next.js#61365](https://github.com/vercel/next.js/issues/61365), [vercel/next.js#49739](https://github.com/vercel/next.js/issues/49739). State/version/created_at вCSV; текст изучен, upstream defect не воспроизводился.
- Бесплатный путь: Official Stripe raw-body verification examples: read once; Pages Router bodyParser=false; preserve signed bytes. [guide](https://docs.stripe.com/webhooks/signature).
- Возможное коммерческое преимущество(HYPOTHESIS): One client-specific signed fixture and deployment check can be a small repair service.
- Решение/gate: Free documented fix often sufficient; no case for a standalone webhook SaaS from these reports alone.


### Механизм привлечения, а не счётчик bugs

Рабочая гипотеза для G01/G03/G05: один полезный consent-free synthetic fixture+понятная инструкция на разрешённом канале → добровольный opt-in inquiry от владельца похожей интеграции → reproduction на approved staging → **сначала бесплатный documented substitute** → paid bounded diagnosis/repair только при согласованной дополнительной ценности. Issues не используются для unsolicited advertising/DM; никакие comments/PRs в upstream projects в этом исследовании не публикуются.

Для G02официальный local server может быть полным техническим решением; новизна relay не доказана, hosting ломает обещание«$0». Для G04проблема интерпретации warning не оправдывает новый scanner или универсальный security audit. G01включает разные причины одного symptom; classifier должен оставлять root causeUNKNOWN до диагностики, а не придумывать общий patch.

Самый дешёвый тест 1–2 h/family: один synthetic contract/repro, проверить официальный workaround, затем вопрос **реальному добровольно обратившемуся** owner о value и paid scope. Наш текущий recovery rehearsal покрывает **один** filter failure, не все пять families. Если free fix достаточен и покупатель может применить сам, нового продукта не нужно. Если два похожих paid fixes требуют одинакового primitive и support ограничен — извлекать reusable adapter/tests.

## Как сохранить уникальность Ninja без преждевременного SaaS

Общий актив: source-provenance ledger + exact corporate IDs + классификатор проблем с явноUNKNOWN root cause + versioned contract fixtures + **разрешённые** агрегаты repair outcomes. Уникальность может появиться после повторяющихся внедрений и opt-in partner relationships, а не от копирования публичных issues/реестров. Всё это пока candidate moat, не доказанное преимущество.

| Направление | Что стало сильнее | Что остаётся слабым | Следующий ограниченный gate |
| --- | --- | --- | --- |
| Supply Chain | Real software awards, named corporate winners,5 ARESidentity checks | No partner intake/subcontract need; XML unavailable; доменная специализация |≤5 manual case qualifications; no contact without lawful path/approval |
| Gap Detector |13 reports from distinct accounts,5 defined symptoms and free alternatives | Root cause/version/payment uncertainty; многие fixes уже бесплатны | One actual client reproduction plus free-substitute comparison |
| First cash service | Offline before/after/rollback proof and draft scope | Bot Recovery paid demand/price/trafficUNKNOWN | One authorized paid diagnostic, не platform build |

Не теряем стратегию: сначала понять, кто и за что платит, затем автоматизировать подтверждённый data→decision workflow. Procurement/grant/issue discovery без покупательского механизма не получает выдуманную commercial conversion.
