# 02. Реальные источники: 30 кандидатов

**Дата проверки: 2026-11-13 (Europe/Kyiv).** Метки: VERIFIED — первичный документ или воспроизводимый тест; OBSERVED — ограниченная выборка; ESTIMATED — расчёт; ASSUMED — допущение; UNKNOWN — данных недостаточно. HTTP 200 сам по себе не подтверждает API, спрос или право автоматизации.

Полные 15 характеристик каждого источника — [source_registry.csv](../../data/source_registry.csv). ID не меняются между документами. JSON schema examples — [source_probe_results.json](../../data/source_probe_results.json); запросы, задержки, ошибки и pagination — [priority_followup](../../data/priority_followup.json).

## Сводка выполненных проб

| ID | Источник | Наблюдение одной пробы | Ключи сопоставления (наличие в sample не гарантируется) | Приоритет |
| --- | --- | --- | --- | --- |
| S01 | data.gov.ua | 200; json_sample; 1.139s | Набор; иногда ЕДРПОУ внутри ресурса | secondary |
| S02 | Prozorro | 200; json_sample; 0.883s | Tender UUID; supplier scheme+id в awards | shortlist |
| S03 | Spending.gov.ua | 500; http_error; 0.889s | Плательщик/получатель ЕДРПОУ если есть в схеме | secondary |
| S04 | ЄДР Minjust | 503; http_error; 5.236s | ЄДРПОУ; ФОП может быть персональными данными | secondary |
| S05 | ЄДЕССБ | 200; html_only_not_api_validation; 0.94s | ID документа; организация если указана | secondary |
| S06 | NIPO SIS trademarks | 200; html_only_not_api_validation; 1.363s | Номер заявки; владелец не всегда ID компании | secondary |
| S07 | Lviv open data | transport error; transport_error; 0.205s | ID набора; бизнес-ключи по ресурсу | secondary |
| S08 | Kyiv open data | 200; json_sample; 0.409s | ID набора; бизнес-ID по ресурсу | secondary |
| S09 | TED | 200; json_sample; 0.733s | Publication number; national IDs в деталях если есть | shortlist |
| S10 | CORDIS | 200; html_only_not_api_validation; 0.89s | Project grant ID; PIC где доступен | secondary |
| S11 | data.europa.eu | 200; json_sample; 0.489s | Dataset URI; издатель; org keys в ресурсах | secondary |
| S12 | Companies House | 401; http_error; 0.599s | Company number | secondary |
| S13 | GitHub REST | 200; json_sample; 0.546s | Repository node ID; issue number | shortlist |
| S14 | WordPress plugin directory | 200; json_sample; 0.588s | Plugin slug; не company ID | shortlist |
| S15 | World Bank API | transport error; transport_error; 25.096s | ISO country; indicator code | secondary |
| S16 | Eurostat | 200; json_sample; 1.529s | Geo/time/classification codes | secondary |
| S17 | GLEIF | 200; json_sample; 1.51s | LEI; registrationAuthorityEntityID где есть | secondary |
| S18 | UK Contracts Finder | 200; json_sample; 1.372s | OCID; organization identifier scheme | secondary |
| S19 | UK Find a Tender | 200; json_sample; 0.849s | OCID; supplier identifier | secondary |
| S20 | EU Funding and Tenders | transport error; transport_error; 0.207s | Topic ID; grant ID; PIC где есть | secondary |
| S21 | Crossref grants | 200; json_sample; 0.635s | DOI; funder ID; award number | secondary |
| S22 | OpenAlex | 200; html_only_not_api_validation; 0.937s | OpenAlex ID; ROR; DOI | secondary |
| S23 | npm download API | 200; json_sample; 0.162s | Package name; scope не компания | secondary |
| S24 | PyPI | 200; json_sample; 0.167s | Package name; version | secondary |
| S25 | Freelancehunt | 200; json_sample; 0.199s | Project ID; не cross-registry company ID | shortlist |
| S26 | Wikidata | 200; html_only_not_api_validation; 0.556s | QID; LEI/VAT если есть | secondary |
| S27 | US College Scorecard | 403; http_error; 0.555s | UNITID; OPEID | secondary |
| S28 | Energi Data Service DK | 200; json_sample; 0.874s | PriceArea + UTC timestamp | secondary |
| S29 | data.gouv.fr / SIRENE discovery | 200; json_sample; 0.725s | SIREN/SIRET в самом SIRENE; не в metadata sample | secondary |
| S30 | PatentsView | 200; html_only_not_api_validation; 0.603s | Patent ID; assignee disambiguation не legal ID | secondary |

Протокол: 32 начальных HTTP-запроса к 30 target IDs (по две страницы GitHub/WP), до 350 KB на ответ, concurrency 3, connect/read timeout 10/25 s, без retries, credentials, CAPTCHA или обхода защиты. Единственный POST — документированный read-only TED search. `source_probe_results.json` хранит **типизированный обезличенный пример структуры**, не исходные записи. Числа массивов/страниц и наличие полей сохранены, значения имён/контактов нет. Структурный JSON response — ещё не положительный результат бизнес-запроса.

## Что действительно установлено и чего sample не доказывает

- S02: feed вернул 2 записи; next_page принят в отдельном запросе, ещё 2 записи, пересечения ID нет. Detail первой исторической записи не содержит awards. Первичная проба не доказывала supplier awards. Follow-up descending sample n=2 вернул две complete закупки, каждая с одним supplier и UA-EDR identifier + CPV (см. pagination_quality_results). Наличие полей теперь OBSERVED; IT relevance, корректность юрлица и supply-chain buying need **не доказаны**. Нельзя выдавать старые первые записи feed за новых победителей. Следующий эксперимент: за ограниченный date window найти до 10 awarded IT notices, измерить долю supplier identifier+scope.
- S09: TED search вернул 2 notices с publication number/date и ссылками. Search не доказывает удобство supplier joining: eForms детали и award fields надо проверить отдельно. Follow-up по официальному api-v3.yaml проверил PAGE_NUMBER pages1/2 по2 notices: publication IDs не пересекаются, title есть2/2 на каждой, timedOut=false, reported total108069 для publication-date>=20261001. Это notices, не компании/клиенты. PAGE_NUMBER cap15000 documented; ITERATION documented, но не tested. Стабильность во времени UNKNOWN.
- S13: две страницы по 2 items; Link pagination присутствует; endpoint `/issues` может включать PR. Для evidence использован отдельный search `is:issue`. Лимит анонимного REST — 60/h по [GitHub rate documentation](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api); search имеет отдельный лимит. Не масштабировать polling без auth/conditional requests.
- S14: page 1 и page 2, по 2 plugins; metadata сообщает 1 062 результата для поиска telegram и 50 страниц. Это reported search total, не оценка уникальных коммерчески активных конкурентов. Не все optional поля запрошены/присутствуют: `useful_field_presence` фиксирует это. Дата обновления не доказывает abandonment; active installs не платящие пользователи. Follow-up явно запросил fields: slug/last_updated/tested/active_installs/version присутствуют2/2. Changelog/license и реальная совместимость всё ещё требуют ручной проверки.
- S17: GLEIF JSON содержит meta pagination и LEI records. LEI даёт сильный entity key, но покрытие небольших компаний UNKNOWN; не обещать единый мировой реестр SMEs.
- S18/S19: OCDS JSON получен; sample ограничен 2 notices. OCID соединяет releases одного procurement process, а не обязательно организации между странами. Supplier scheme/id нужно проверить на awarded records.
- S25: анонимный public list работает в этой среде; category sample n=6 дал 4 technical keyword matches. Нельзя переносить вывод на authenticated bidding. [Официальная документация](https://apidocs.freelancehunt.com/) требует Bearer для действий аккаунта.
- S01/S08/S11/S29: проверены metadata catalogs. Это не проверка файлов, completeness, свежести самих записей и лицензии каждого dataset. S16 вернул JSON, но выбранная UA statistical cell пуста — не пригодный datapoint. S21 grants filter вернул metadata; relevance компаний надо исследовать.

## Отрицательные результаты и ошибки discovery

S03 HTTP 500 может означать ошибочный endpoint/params или серверный сбой: не объявляем Spending недоступным вообще. S04 HTTP 503 не доказывает юридическое закрытие реестра. S07 transport error требует проверки актуального адреса, а не повторов того же запроса. S12 HTTP 401 — подтверждённый auth gate; официально 600 requests/5 minutes ([developer guidelines](https://developer.company-information.service.gov.uk/developer-guidelines/)); ключ не запрашивался и обход не предпринимался. S15 read timeout — одна проба, не outage. S27 HTTP 403 — без ключа; низкий business fit, не приоритет.

S20: первоначальный discovery URL `hds.healdata.eu` оказался непроверенной ошибочной гипотезой адреса и **не относится к EU Funding & Tenders**. Он сохранён как ошибка процесса, не как тест доступности портала. Официальная [страница Funding & Tenders](https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/topic-search) проверяется отдельно в policy checks; рабочий API не найден. S22/S26/S30 получили HTML вместо ожидаемого JSON: функциональный API не валидирован. Legacy PatentsView нельзя считать current search endpoint. Наличие HTML SIS/ЄДЕССБ не разрешает массовый scraping.

## Выбор 5 источников для следующего короткого эксперимента

1. S25 Freelancehunt — наиболее близкий к явному buyer request; цены и наша win-rate неизвестны.
2. S13 GitHub — pain/reproducibility, полезен для OSS proof; запрещено превращать issues в рекламную рассылку.
3. S14 WordPress — проверка насыщенности/совместимости; не список людей для контакта.
4. S02 Prozorro — проверяемый cursor; сначала качество awards и CPV, затем бизнес-полезность.
5. S09 TED — международные notices; next gate — supplier details, размер контрактов и возможность subcontract.

GLEIF (S17) и UK notices (S18/S19) полезны как supporting sources. Registry events/grants не первый канал продаж: событие организации не подтверждает потребность и свободный бюджет на наш продукт.

## Объём, стоимость и повторяемость

ESTIMATED storage: 10 000 normalized events × 2 KB = 20 MB без indexes/history; 100 000 × 3 versions × 2 KB = 600 MB, уже выше бесплатной DB Supabase 500 MB. Это capacity scenarios, не измеренный размер всего источника. Для каждого dataset хранить `source, id, source_updated_at, retrieved_at, schema_version, normalized_digest, license_ref`; payload allowlist, без контактов. Транзакционно сохранять batch и checkpoint; overlap window + dedupe; deletion/tombstone policy; 429 Retry-After; метрики lag/error. Рабочий алгоритм на synthetic events — [state POC](../../research/probes/state_poc.py), но cloud ingestion не реализован.

Cash budget probes: $0 paid APIs; использованы уже доступные executor/network. Интеграционный труд 2–24h/source — ASSUMED и не входит в оценку простоты готовых APIs. Нет заявления о полном покрытии, rate-limit надёжности, всех pagination modes или разрешении перепродавать данные.

## Финальное уточнение приоритетных источников

[pagination_quality_results.json](../../data/pagination_quality_results.json) и [скрипт](../../research/probes/pagination_quality.py) содержат ещё8bounded reads/search calls: официальный TED Swagger contract, две страницы TED, descending Prozorro feed+2details, WP explicit fields. Request date/latency/bytes сохранены. Первоначальная догадка TED `/v3/api-docs` дала404; корректный schema URL `/api-v3.yaml` найден через официальный Swagger config. Это discovery correction, не authorization bypass. Дополнительный sample не используется для оценки market size, IT procurement share или outage probability.
