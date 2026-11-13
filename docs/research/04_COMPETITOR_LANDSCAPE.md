# 04. Альтернативы и конкуренты: 38 предложений

**Дата проверки: 2026-11-13 (Europe/Kyiv).** Метки: VERIFIED — первичный документ или воспроизводимый тест; OBSERVED — ограниченная выборка; ESTIMATED — расчёт; ASSUMED — допущение; UNKNOWN — данных недостаточно. HTTP 200 сам по себе не подтверждает API, спрос или право автоматизации.

Данные — [competitor_registry.csv](../../data/competitor_registry.csv), результаты загрузки официальных страниц — [policy_page_checks.json](../../data/policy_page_checks.json). Цены ниже — текст на странице в дату проверки; валюта/страна/VAT, ежегодная оплата, акции и единицы usage отличаются. Ни один checkout не пройден. Преимущества/пробелы — аналитические гипотезы, не установленные дефекты конкурента. Acquisition подтверждён лишь наличием официальной страницы/каталога, не числом клиентов или трафиком.

| ID | Предложение | Первичный URL | Кому | Что уже решено | Наблюдаемая цена / предел проверки |
| --- | --- | --- | --- | --- | --- |
| C01 | Zapier | https://zapier.com/pricing | SME ops | Connectors; workflows; templates | Free/paid tiers; exact task price UNKNOWN from truncated page |
| C02 | Make | https://www.make.com/en/pricing | SME ops | Scenarios; connectors; scheduling | OBSERVED $0 and $9/$16/$29 displayed; billing/credits must be selected |
| C03 | n8n | https://n8n.io/pricing/ | Developers/ops | Nodes; self-host/cloud; templates | Cloud paid; exact price UNKNOWN; license review unresolved |
| C04 | Pipedream | https://pipedream.com/pricing | Product developers | Connect; workflows; auth tooling | OBSERVED Connect $0 development; Startup $99/month; production not free |
| C05 | Activepieces | https://www.activepieces.com/pricing | SME teams | Flows; connectors; self-host option | OBSERVED Free; Plus $20/month; Team $200/month; credits differ |
| C06 | Uncanny Automator | https://automatorplugin.com/pricing/ | WordPress owners | Recipes; triggers; actions | OBSERVED Lite $0; Basic $20/month or $199/year; Plus $35/month or $349/year; Elite $60/month or $599/year |
| C07 | WP Webhooks | https://wp-webhooks.com/pricing/ | WP developers | Webhook triggers/actions | OBSERVED Starter $149/year; Business $249/year; Agency $499/year; taxes/terms separately |
| C08 | WP Fusion | https://wpfusion.com/pricing/ | Membership/ecommerce | CRM tags; ecommerce sync | OBSERVED Lite $0; Personal $297/year; Plus $427/year; Professional $647/year |
| C09 | WPCode | https://wpcode.com/pricing/ | WP operators | Snippet library; deployment UI | OBSERVED promotional $49/$99/$199/$349 per year; normal/renewal prices differ |
| C10 | Budibase | https://budibase.com/pricing/ | Internal tools teams | Builder; data connectors | OBSERVED self-host Community $0 software; Cloud from $299/month; hosting not included in self-host |
| C11 | Retool | https://retool.com/pricing/ | Business engineering | Admin UI; workflows; DB connectors | OBSERVED Free EUR0 up to 5 users; Team EUR9/builder/month annual billing; internal users separately |
| C12 | Appsmith | https://www.appsmith.com/pricing | Developers | UI builder; APIs; self-host | OBSERVED Free up to 5 users; Business $15/user/month; Enterprise $2500/month |
| C13 | NocoDB | https://nocodb.com/pricing | SME operators | Tables; APIs; permissions | OBSERVED Free up to 3 users; Plus $12/seat/month billed annually; compare API/run caps |
| C14 | Apify | https://apify.com/pricing | Data teams | Actors; schedules; marketplace | UNKNOWN exact current credits |
| C15 | Visualping | https://visualping.io/pricing | Ops/compliance | Visual diff; alerts | UNKNOWN exact plan price |
| C16 | Distill | https://distill.io/pricing/ | Operators | Browser/cloud monitors | UNKNOWN exact plan price |
| C17 | Hexowatch | https://hexowatch.com/ | Agencies | Multiple monitoring types | UNKNOWN current price |
| C18 | Wappalyzer | https://www.wappalyzer.com/pricing/ | Sales/tech teams | Tech detection; lookup | UNKNOWN current credits |
| C19 | BuiltWith | https://builtwith.com/plans | Sales teams | Tech lists; history | UNKNOWN current price |
| C20 | WPScan | https://wpscan.com/pricing/ | Security teams | Vulnerability intelligence | UNKNOWN current API plans |
| C21 | WPMU DEV | https://wpmudev.com/pricing/ | WP agencies | Hosting; plugins; maintenance | UNKNOWN exact current tiers |
| C22 | ManageWP | https://managewp.com/pricing | WP agencies | Updates; backups; monitoring | UNKNOWN current add-on cost |
| C23 | UpdraftPlus | https://updraftplus.com/shop/updraftplus-premium/ | Site owners | Backups; migration | OBSERVED Personal $87.50/year including Denmark VAT in fetched page; geography/tax-specific |
| C24 | Supabase Advisors | https://supabase.com/docs/guides/database/database-advisors | Supabase developers | Built-in advisor checks | Built-in baseline; marginal plan inclusion must be checked |
| C25 | Checkly | https://www.checklyhq.com/pricing/ | Engineering teams | Browser/API tests; alerts | OBSERVED Hobby $0 personal/learning; Starter $24/month billed annually; Team $64/month billed annually |
| C26 | Better Stack | https://betterstack.com/uptime/pricing | DevOps teams | Monitors; on-call; status pages | OBSERVED Free $0 personal projects; responder $34 monthly or $29 annual-equivalent/month |
| C27 | UptimeRobot | https://uptimerobot.com/pricing/ | SME web owners | HTTP checks; notifications | OBSERVED Free EUR0 for personal and commercial projects; paid Solo EUR9/month annual-equivalent; tiers differ |
| C28 | cron-job.org | https://cron-job.org/en/ | Developers | Cron HTTP triggers | Official site markets free service; exact quota UNKNOWN |
| C29 | Coolify | https://coolify.io/pricing/ | Self-hosting developers | Container deploy; TLS; integrations | OBSERVED self-host software free; Cloud $5/month base connects 2 servers plus $3/additional server; actual servers extra |
| C30 | Stotles | https://www.stotles.com/ | Government suppliers | Tender discovery; market signals | UNKNOWN quote |
| C31 | GovTribe | https://govtribe.com/ | US government suppliers | Opportunity and award research | UNKNOWN; page transport failure |
| C32 | OpenOpps | https://openopps.com/ | Procurement suppliers | Opportunity search | UNKNOWN current commercial availability |
| C33 | GrantForward | https://www.grantforward.com/ | Research institutions | Funding search; alerts | UNKNOWN institution quote |
| C34 | Instrumentl | https://www.instrumentl.com/pricing | Nonprofits | Discovery; tracking; reporting | OBSERVED Discover $299/month billed annually or $349 monthly; higher workflow tiers available |
| C35 | Opendatabot | https://opendatabot.ua/open | Ukraine business | Registry intelligence | UNKNOWN; attempted open page 404 |
| C36 | YouControl | https://youcontrol.com.ua/ | Ukraine business | Company reports/analytics | UNKNOWN; page 403 |
| C37 | Codeable | https://www.codeable.io/developers/apply/ | WordPress buyers | Matching; implementation | UNKNOWN; apply URL 404 |
| C38 | Lemon.io | https://lemon.io/for-developers/ | Startups | Vetting; matching | UNKNOWN public quote |

## Free-first substitution test

1. Generic CRM→Telegram: сначала бесплатный connector/Make/n8n/WordPress plugin на fixture. Если workflow корректен и owner может поддерживать сам, собственного продукта не нужно. Можно продать только понятный onboarding/recovery если клиент хочет.
2. RLS audit: Supabase Advisors уже даёт baseline checks. Платная ценность возможна в **конкретных cross-tenant negative authorization tests** и исправлении с owner review, не в перепечатке бесплатных warnings.
3. Backups/deployment: UpdraftPlus/ManageWP/Coolify и простые platform deploys закрывают baseline. P01 должен доказывать восстановление бизнес-сценария и ownership, а не факт наличия backup.
4. Website checks: UptimeRobot fetched page явно допускает free personal/commercial projects; Checkly free positioning — personal/learning. Значит «бесплатно» требует проверки use-case, не только цены $0.
5. Registry/tender tools: открытые порталы + established tools могут быть достаточно хороши. Технический parser без доказанной экономии decision time — слабый платный wrapper.
6. Internal admin: Appsmith/Retool/NocoDB имеют free entry. React CRUD starter сам по себе плохо защищён. Платить могут за domain validation/migration/tenant isolation, но это пока UNKNOWN.

## Незакрытые гипотезы и дифференциация

| ID | Почему конкурент может быть достаточен (analysis) | Возможная дифференциация (не проверена клиентами) | Следующая проверка |
| --- | --- | --- | --- |
| C01 | ASSUMED analytical comparison: Connector breadth | HYPOTHESIS, not competitor defect: Custom Ukrainian edge cases and ownership | Try existing free/core feature before custom build |
| C02 | ASSUMED analytical comparison: Visual graph | HYPOTHESIS, not competitor defect: Idempotent audited delivery and handover | Try existing free/core feature before custom build |
| C03 | ASSUMED analytical comparison: Reusable templates | HYPOTHESIS, not competitor defect: Fixed-scope implementation rather than generic hosting resale | Try existing free/core feature before custom build |
| C04 | ASSUMED analytical comparison: Managed auth integrations | HYPOTHESIS, not competitor defect: Small single-integration offer below platform complexity | Try existing free/core feature before custom build |
| C05 | ASSUMED analytical comparison: Low entry cost | HYPOTHESIS, not competitor defect: Maintenance and client-owned deployment | Try existing free/core feature before custom build |
| C06 | ASSUMED analytical comparison: Native WP ecosystem | HYPOTHESIS, not competitor defect: Local CRM integration with error recovery | Try existing free/core feature before custom build |
| C07 | ASSUMED analytical comparison: Event primitives already packaged | HYPOTHESIS, not competitor defect: Recovery tests rather than another generic webhook plugin | Try existing free/core feature before custom build |
| C08 | ASSUMED analytical comparison: Specialized CRM mapping | HYPOTHESIS, not competitor defect: Unsupported local CRM with fixed acceptance tests | Try existing free/core feature before custom build |
| C09 | ASSUMED analytical comparison: Free/basic alternative | HYPOTHESIS, not competitor defect: Security-reviewed deliverable instead of snippets alone | Try existing free/core feature before custom build |
| C10 | ASSUMED analytical comparison: Fast CRUD | HYPOTHESIS, not competitor defect: Domain workflow and data cleanup | Try existing free/core feature before custom build |
| C11 | ASSUMED analytical comparison: Rich builder | HYPOTHESIS, not competitor defect: Exportable code and no per-seat coupling | Try existing free/core feature before custom build |
| C12 | ASSUMED analytical comparison: Open-source alternative | HYPOTHESIS, not competitor defect: Workflow-specific fixed-price setup | Try existing free/core feature before custom build |
| C13 | ASSUMED analytical comparison: Basic CRUD may already suffice | HYPOTHESIS, not competitor defect: Data validation and migration service | Try existing free/core feature before custom build |
| C14 | ASSUMED analytical comparison: Broad extraction ecosystem | HYPOTHESIS, not competitor defect: Official API-only pipeline with provenance | Try existing free/core feature before custom build |
| C15 | ASSUMED analytical comparison: Generic monitoring already exists | HYPOTHESIS, not competitor defect: Structured event semantics; false-positive reduction | Try existing free/core feature before custom build |
| C16 | ASSUMED analytical comparison: Low-complexity monitor | HYPOTHESIS, not competitor defect: API cursor integrity and audit history | Try existing free/core feature before custom build |
| C17 | ASSUMED analytical comparison: Many monitor modes | HYPOTHESIS, not competitor defect: Functional reproducible proof rather than cosmetic alert | Try existing free/core feature before custom build |
| C18 | ASSUMED analytical comparison: Technology discovery | HYPOTHESIS, not competitor defect: Verified integration failure evidence; avoid contact resale | Try existing free/core feature before custom build |
| C19 | ASSUMED analytical comparison: Extensive stack datasets | HYPOTHESIS, not competitor defect: Narrow implementation offer; stack alone not need | Try existing free/core feature before custom build |
| C20 | ASSUMED analytical comparison: Specialist vulnerability data | HYPOTHESIS, not competitor defect: Remediation plus consented testing; no scanner resale | Try existing free/core feature before custom build |
| C21 | ASSUMED analytical comparison: Bundled managed WP | HYPOTHESIS, not competitor defect: Local integration ownership and acceptance tests | Try existing free/core feature before custom build |
| C22 | ASSUMED analytical comparison: Management baseline | HYPOTHESIS, not competitor defect: Business workflow recovery beyond updates | Try existing free/core feature before custom build |
| C23 | ASSUMED analytical comparison: Mature backup tool | HYPOTHESIS, not competitor defect: Tested restoration and runbook, not backup replacement | Try existing free/core feature before custom build |
| C24 | ASSUMED analytical comparison: Free checks make generic RLS scan weak | HYPOTHESIS, not competitor defect: Tenant-specific negative authorization tests | Try existing free/core feature before custom build |
| C25 | ASSUMED analytical comparison: Executable monitoring | HYPOTHESIS, not competitor defect: Client-specific critical path setup | Try existing free/core feature before custom build |
| C26 | ASSUMED analytical comparison: Integrated incident tooling | HYPOTHESIS, not competitor defect: Bot workflow recovery playbook | Try existing free/core feature before custom build |
| C27 | ASSUMED analytical comparison: Basic uptime commoditized | HYPOTHESIS, not competitor defect: Semantic order-to-notification assertions | Try existing free/core feature before custom build |
| C28 | ASSUMED analytical comparison: Simple free scheduler | HYPOTHESIS, not competitor defect: Durable state and retries still needed | Try existing free/core feature before custom build |
| C29 | ASSUMED analytical comparison: Free software alternative | HYPOTHESIS, not competitor defect: Client pays compute; recovery package | Try existing free/core feature before custom build |
| C30 | ASSUMED analytical comparison: Procurement specialization | HYPOTHESIS, not competitor defect: Micro-agency fixed CPV digest; willingness to pay untested | Try existing free/core feature before custom build |
| C31 | ASSUMED analytical comparison: US procurement focus | HYPOTHESIS, not competitor defect: Ukraine/EU narrow niche; US outside core priority | Try existing free/core feature before custom build |
| C32 | ASSUMED analytical comparison: Aggregated procurement alternative | HYPOTHESIS, not competitor defect: Sector-specific evidence quality | Try existing free/core feature before custom build |
| C33 | ASSUMED analytical comparison: Institution distribution | HYPOTHESIS, not competitor defect: Post-award reporting product instead of grant search | Try existing free/core feature before custom build |
| C34 | ASSUMED analytical comparison: Established grant workflow | HYPOTHESIS, not competitor defect: Small EU consortium deliverable evidence pack | Try existing free/core feature before custom build |
| C35 | ASSUMED analytical comparison: Local identity data | HYPOTHESIS, not competitor defect: Do not rebuild generic company monitor | Try existing free/core feature before custom build |
| C36 | ASSUMED analytical comparison: Local counterparty specialization | HYPOTHESIS, not competitor defect: Permissioned industry workflow; no bulk personal resale | Try existing free/core feature before custom build |
| C37 | ASSUMED analytical comparison: Trust and vetting | HYPOTHESIS, not competitor defect: A narrower demonstrable fixed deliverable | Try existing free/core feature before custom build |
| C38 | ASSUMED analytical comparison: Staffing trust | HYPOTHESIS, not competitor defect: Small scoped package rather than ongoing staffing | Try existing free/core feature before custom build |

Ни одна из гипотез «локальный CRM», «handover» или «лучший retry» не объявляется отсутствующей у всех конкурентов. Перед build запросить/проверить ровно один workflow у existing tool; если решается за 1–2h, использовать его вместо разработки. n8n current license/embed policy требует отдельной проверки: один старый license URL вернул содержательную page-not-found при HTTP 200. Нельзя заключать, что self-hosting разрешает white-label resale.

## Вывод

Рынок generic automation и мониторинга уже имеет бесплатные и платные альтернативы (VERIFIED существование retrieved offers, не paid traction). Защитимый кандидат — tested delivery + client context + reusable fixtures + distribution relationships. Свой общий Zapier/registry aggregator сейчас не имеет доказанного преимущества. Не делаем выводов о выручке, рыночной доле, пользовательской базе или конверсии любого конкурента.
