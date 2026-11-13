# 09. Законность и риски: операционные границы исследования

**Дата проверки: 2026-11-13 (Europe/Kyiv).** Метки: VERIFIED — первичный документ или воспроизводимый тест; OBSERVED — ограниченная выборка; ESTIMATED — расчёт; ASSUMED — допущение; UNKNOWN — данных недостаточно. HTTP 200 сам по себе не подтверждает API, спрос или право автоматизации.

Это risk analysis и список проверок, не профессиональное юридическое заключение. В исследовании не было коммерческих сообщений, контактов, регистраций, сделок, scanning чужих сайтов, отзывов или платежей. Публичные **records** ≠ согласие на маркетинг; разрешение владельца Ninja ≠ согласие получателя и не override platform rules.

## Первичные источники и степень проверки

| Норма/политика | URL | Проверка и confidence |
| --- | --- | --- |
| GDPR Regulation 2016/679 | https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng | Official page HTTP200, byte-truncated; ссылка первичная, не заявление о чтении всей редакции; medium |
| ePrivacy Directive 2002/58/EC | https://eur-lex.europa.eu/eli/dir/2002/58/oj/eng | Official page HTTP200; national transposition/recipient type отдельно; medium |
| Закон Украины о защите ПД 2297-VI | https://zakon.rada.gov.ua/laws/show/2297-17#Text | HTTP503 в этой среде; актуальная редакция UNKNOWN; нужна ручная проверка юристом |
| Закон Украины об электронной коммерции 675-VIII | https://zakon.rada.gov.ua/laws/show/675-19#Text | HTTP503; точные marketing exceptions не подтверждены |
| Постановление open data 835 | https://zakon.rada.gov.ua/laws/show/835-2015-%D0%BF#Text | HTTP503; не утверждаем текущий военный режим доступа к каждому реестру |
| GitHub ToS / Additional terms | https://docs.github.com/en/site-policy/github-terms/github-terms-of-service ; https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features | HTTP200; Actions misuse/hosting restrictions прочитаны; medium-high для зафиксированных пунктов |
| WP plugin guidelines | https://developer.wordpress.org/plugins/wordpress-org/detailed-plugin-guidelines/ | HTTP200; review/license/privacy requirements; product-specific acceptance UNKNOWN |
| EU re-use notice | https://commission.europa.eu/legal-notice_en | HTTP200; dataset/third-party exceptions still need per-resource review |
| Companies House guidelines | https://developer.company-information.service.gov.uk/developer-guidelines/ | HTTP200; rate-limit600/5min и key protection; re-use not blanket consent |
| Upwork eligibility | https://support.upwork.com/hc/en-us/articles/211067778-Eligibility-to-join-and-use-Upwork | HTTP200; residence/restricted territories; actual KYC/payment UNKNOWN |
| n8n commercial/embed policy | https://docs.n8n.io/embed/ | Retrieved body insufficient; old sustainable-use URL became page-not-found; UNKNOWN current license scope |

Evidence timestamps/HTTP/partial pages: [policy_page_checks.json](../../data/policy_page_checks.json). Не цитируем непроверенную текущую формулировку украинских законов как VERIFIED.

## Data protection design before future implementation

Organization-only IDs могут снизить риск, но директор, ФОП, sole trader, личный email, домашний адрес и связка public identifiers могут быть ПД. Публичная доступность не устраняет GDPR purpose limitation, minimization, storage limitation, security и accountability. Для EU recipients определить lawful basis отдельно от ePrivacy requirements для сообщений; legitimate interests не универсальное разрешение unsolicited electronic marketing. В разных странах и для natural persons/corporate subscribers правила различаются. Art13/14 transparency, Art21 objection и suppression, access/deletion workflows нужны там, где применимы; сроки/исключения и international transfers должен проверить специалист.

Предлагаемый minimization: не ingest personal contact fields в opportunity research; purpose-limited pseudonymous lead IDs после добровольного обращения; contacts отдельно с RBAC/retention, not in Git. Retention конкретно согласовать после определения legal basis; произвольное «храним всё навсегда» неприемлемо. Suppression record сам может быть ПД; ограниченный purpose и доступ. AI processor/DPA, region, retention, subprocessors и международные передачи проверить до отправки client descriptions/API payloads; ключ/credential никогда не prompt input.

Dataset license хранить с source/version: CC0/OGL/EU reuse не одинаковы; rights на metadata могут не распространяться на linked files/abstracts/logos. Ограничения publisher/API и запрет resale могут быть отдельными. Company ID matching — explainable, reversible, human review для fuzzy candidates. Ошибочное объединение двух компаний — reputational/business risk, даже если contacts не хранятся.

## Категории действий

| Категория | Действие | Условия/границы |
| --- | --- | --- |
| Разрешено исследованием | Bounded public API GET/search, документированное read-only TED POST; anonymous schema sampling; local synthetic model/tests | Соблюдать limits/TLS/terms, не harvest contacts; no challenge bypass |
| Разрешено с ограничениями | Incremental public data normalization, company-ID diff, repository issue analysis | License/purpose/retention; issue text не согласие на продажи; skip PII |
| Разрешено с ограничениями | AI draft/classification | Redacted facts, schema+source citation, caps, approved provider data terms; no fabricated need |
| Требует отдельного owner authorization | Регистрация/публикация профиля/plugin/package; коммерческое предложение; ставка; отправка сообщения; production deployment/change; paid API | Дополнительно platform admission, recipient lawful basis/consent where required и реальные budget/access rights |
| Требует recipient/client permission | Website/browser tests with side effects, access to CRM/store/DB, production restore, tracking analytics | Scope, staging, no unconsented lead submission; contract/DPA and approvals |
| Требует юридической проверки | Mass company-event intelligence with personal fields, cross-border commercial messaging, legal-deadline offer, grant procurement, processor/international transfer, subcontract IP | Country+recipient+dataset-specific opinion; не universal GDPR boilerplate |
| Неподходящее | Spam/auto-DMs/issue advertising, CAPTCHA/login bypass, review manipulation, fabricated buyers, unauthorized bidding, secret reuse from Git, scraping behind protection | Не входит в scope и не нужно для validation |

## Marketplace и plugin rules

Free profile не право на automation, scraped leads или off-platform circumvention. Каждая площадка имеет своё anti-spam, communication/escrow, identity, country и fee policy. Для WordPress нужен GPL-compatible code review, rights на assets, privacy/telemetry disclosure, support/security handling; коммерческая модель должна соответствовать current directory rules. Chrome extension требует minimal permissions/privacy/store review; не использовать её как обход сайтового scraping запрета. GitHub repository license и API ToS различаются: публичный код не автоматически public domain; issues may include personal information. Не repostить чужие issue bodies или contacts в коммерческий lead list.

## Партнёрство/субподряд

До white-label delivery определить client approval to subcontract, NDA, IP ownership/license chain, data processor obligations, access roles, conflict/no-poach, warranty/scope/acceptance и ответственность за production changes. Агентский lead не даёт автоматического доступа к данным его клиента. В коммерческих материалах не использовать логотипы/имена клиентов без согласия. Trust строится на synthetic proof и принятых deliverables, не fabricated testimonials.

## Матрица рисков

| Риск | Severity | Likelihood | Контроль и gate |
| --- | --- | --- | --- |
| Уже опубликованные credential literals/history | high | Exposure VERIFIED; validity/use UNKNOWN | Owner revoke/rotate отдельно; не выводить значения; remediation PR без использования старых tokens |
| Forged callback / unauthorized Telegram UI action | high | Callback reproduction VERIFIED locally; external reach UNKNOWN | Signature/actor ACL/idempotency; negative tests до production |
| Free-tier pause/data loss | medium-high | Quota rules VERIFIED; live failure rate UNKNOWN | Client-owned backups, export, budget, monitored freshness; no SLA promises |
| No buyers at desired price | high business | UNKNOWN; local budgets challenge target | 2 paid pilots + channel cohort; no platform build first |
| Wrong company merge / overstated AI need | medium-high | UNKNOWN | Exact keys/provenance, facts vs hypotheses, manual decisions |
| API license/marketing violation | high | UNKNOWN per jurisdiction/source | No contacts harvested, consent/ToS review, no commercial action in research |
| Support consumes all capacity | high business | ASSUMED stress case | Support cap/contract, track h/client, priced maintenance only |
| Liability from «RLS audit/compliance» promise | high | UNKNOWN competence | Bounded review wording, expert sign-off, optimizer gate |
| Dependence on one platform/agency | medium-high | UNKNOWN | Exportable fixtures, own opt-in channel, concentration metric |

Точная первая action владельца — отдельно принять решение о credential remediation и разрешить scope коммерческого validation. Этот PR не выполняет эти действия и не публикует историю секретов заново в отчётах.
