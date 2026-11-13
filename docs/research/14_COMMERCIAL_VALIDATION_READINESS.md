# 14. Готовность к коммерческой проверке

**Дата проверки: 13 ноября 2026, Europe/Kyiv.** VERIFIED — первичный документ/воспроизводимый тест; OBSERVED — ограниченная выборка; ESTIMATED — расчёт; ASSUMED — допущение; UNKNOWN — недостаточно данных. Никаких продаж, публикаций офферов, регистраций, платежей, rotation или production changes не выполнялось.

## Решение после follow-up

**Bot Recovery как самостоятельный первый массовый оффер не подтверждён.** Следующий разумный эксперимент — платная диагностика **одной** существующей неисправности webhook/бота или готового приложения с последующим ограниченным исправлением, если diagnosis это допускает. Это гипотеза оффера, а не подтверждённый диапазон рыночной цены. Синтетический proof подготовлен; запуск ждёт отдельного owner authorization и account/payout readiness. Создание Ninja2.0 не начато.

Важное изменение к [первому отчёту](00_EXECUTIVE_DECISION_REPORT.md): меньший scope и проверка цены раньше product build. Нельзя выдавать первоначальные$350/8h или новую цену за validated market price.

## Выборка и исправление методики

Окно: `14.10.2026 03:00 ≤ публикация < 13.11.2026 02:00`, Europe/Kyiv; исходные границы в API —00:00 UTC, с учётом смены летнего времени. Взяты 30 нефильтрованных страниц **открытых** Freelancehunt projects и до 5 страниц по каждой из категорий Bot Development180, DevOps181, Python22. После дедупликации 306 project IDs, из них 304 в окне. Keyword screen дал 59 кандидатов; выполнен один ручной проход по названиям и редактированным техническим фрагментам. Это шире шести объявлений одной категории, но **не вероятностная и не репрезентативная для всего рынка выборка**: активные проекты, page cap, keyword false negatives, один reviewer, фрагменты до 6000 символов, неизвестная география buyer. Нельзя оценить все публикации за месяц, заполненные/закрытые заказы и true frequency. Подстроковый screen «бот» также совпадает с некоторыми обычными словами вроде «работа»; это источник ложных кандидатов, а не технического спроса. Поэтому используются ручные решения, а 59 совпадений не названы 59 квалифицированными запросами.

Скрипт [commercial_sample.py](../../research/probes/commercial_sample.py), [manifest](../../data/commercial_sample_manifest.json), [retained sample](../../data/commercial_job_sample.csv), [ручные решения](../../data/commercial_job_review.csv), [offline summary](../../data/commercial_review_summary.json). Contacts/owners не сохраняются. Разные project IDs не обязательно разные покупатели; две алгоритмические задачи похожи и могут быть от одного заказчика.

**Методическая ошибка раскрыта:** при первоначальном чтении публичного Freelancer API условия проверены слишком поздно. Section33 прямо требует express written permission для автоматического доступа, включая API. Дальнейшие обращения прекращены, все 135 job records и их выводы исключены/удалены; сохранены только request metadata и описание исправления. Их бюджеты, тексты и найденные задачи **не используются** в этом отчёте или модели. Новый collector не обращается к Freelancer; policy collectors теперь тоже имеют guard. [exclusion record](../../data/restricted_source_exclusion.json), [условия](https://www.freelancer.com/about/terms). Прозрачность ошибки не заменяет разрешение площадки.

Для международного контекста законного public GitHub чтения добавлены 30 issues из открытой программы Expensify External за то же окно, search reported total319. Все 30 имеют advertised reward$175;29 open/1closed на момент пробы. Это **один sponsor/codebase**, не тридцать независимых покупателей; External/open не доказывает свободное assignment или состоявшуюся оплату. Не Telegram Recovery и не международный marketplace census. [sample](../../data/international_bounty_sample.csv), [manifest](../../data/international_bounty_manifest.json), [официальные правила участия](https://raw.githubusercontent.com/Expensify/App/main/contributingGuides/CONTRIBUTING.md). Там нужен принятый proposal и в основном verified Upwork для оплаты; PR до accepted proposal открывать нельзя. Никаких proposals не отправлялось.

## Что реально найдено

| Сегмент retained evidence | Результат | Что допустимо заключить |
| --- | --- | --- |
| Существующий Telegram-бот, конкретная неисправность, запрос восстановления |0 в выбранных 59 кандидатах | Спрос на узкий пакет не подтверждён; это не доказательство отсутствия спроса |
| Готовое приложение, ограниченный deployment candidate |1 | Есть объявление, но budgetUNKNOWN и scope до диагностики неясен |
| Более крупная миграция/стабилизация существующей системы |3 | Смежный спрос существует, но не обязан помещаться в 6–8 h |
| Новые интеграции |5 | Новая разработка отдельно от восстановления; не включать в recovery count |
| Остальные keyword candidates |50 | Новое строительство/другая работа/недостаточный match, включая восстановление удалённого личного Telegram account |
| Международный one-sponsor bug bounty context |30×$175 advertised | Явное условное денежное предложение за app bugs; не наш transaction-price benchmark |

| ID | Тип | Запрос | Объявленный budget | Bids snapshot |
| --- | --- | --- | --- | --- |
| FH-1664046 | greenfield_adapter | Синхронізація товарів, цін і залишків між Prom.ua та Хорошоп | UNKNOWN | 109 |
| FH-1663924 | greenfield_adapter | Интеграция автоперевода Google API (с SEO и скриптом) + Создание раздела «Блог» на Laravel | UNKNOWN | 99 |
| FH-1663873 | website_migration | Редизайн сайта и перенос с WordPress на HTML | UNKNOWN | 133 |
| FH-1663031 | existing_system_stabilization | Аудит и комплексная доработка алгоритмической системы: скорость, качество решений, стабильность | 3000 EUR | 54 |
| FH-1663026 | python_rust_migration | Ускорение и развитие системы принятия решений в реальном времени (Python → Rust, ML) Описание | 2500 EUR | 47 |
| FH-1662903 | greenfield_adapter | Разработка AI-помощника и сквозной аналитики: Meta Ads + CRM + LLM-ассистент | 1000 EUR | 120 |
| FH-1661893 | greenfield_adapter | Бот: автозагрузка товаров из Telegram-каналов поставщиков на Prom.ua с помощью ИИ | UNKNOWN | 124 |
| FH-1662007 | ready_app_deployment | Размещение готового сайта на Cloudflare Workers | UNKNOWN | 126 |
| FH-1662598 | greenfield_adapter | Автоматизация заказов: существующие группы Viber → ИИ → 1 С | UNKNOWN | 98 |

Прямые URL и причины каждого включения/исключения — CSV. Для четырёх смежных существующих систем: budgets известны лишь у двух, EUR2500и 3000; другие дваUNKNOWN. Это крупный Python/Rust/algorithm scope, не цена маленького bot repair. У единственного bounded deployment126ставок; у новых интеграций 98–124, median109. Bids — snapshot конкуренции, не odds победы и не число квалифицированных предложений. GitHub comments не bids. Между USD/EUR/UAH, fixed/hourly, whole-project/one-bug budgets не считаем общий median.

**Вывод по цене:** достоверный диапазон принятой клиентом цены Bot Recovery — UNKNOWN. В sample нет сопоставимых paid fixes. $175 bounty — один конкретный program и иной код/навыки; EUR2500–3000 — иной scope. Исходный$350 не подтверждён. Для price discovery подготовлены явно ASSUMED tiers: диагностика 1500 UAH/$75 до 2 h; одно исправление 5000 UAH/$150–250 до 6 h после диагностики. Это не «реалистичная средняя», а ограниченный тест, который нужно принять или отклонить по реальным предложениям/оплатам.

## Fixed, hourly и поддержка

| Модель | Когда подходит | Приёмка и границы | Риск и проверка |
| --- | --- | --- | --- |
| Paid diagnostic,1500 UAH/$75 до 2 h (A) | Причина/качество чужого кода неизвестны | Repro или обоснованный UNKNOWN, evidence-backed diagnosis, план/quote, snapshot без secrets | Платят ли за diagnosis отдельно? Проверить первой оплатой, не обещать fix всегда |
| Fixed repair,5000 UAH/$150–250 total (A) | Один воспроизведённый fault и известный доступ | Patch+acceptance+rollback, до 6 h включая оговорённый handover; diagnosis зачтён в total | Не брать whole SaaS/17containers за цену одного бага |
| Hourly с prepaid cap (A: rate согласуется owner) | Неизвестный legacy scope | До 2 hdiscovery, следующий блок только по approval, журнал времени | Budget overrun и доверие; нет comparable accepted hourly rate в retained sample |
| Maintenance, только после успешного исправления | Регулярная проверка одного согласованного workflow | Limit0.5–0.75 h/month, отдельная цена, не 24/7/SLA | Contra$15/transaction делает дешёвый$39 retainer менее маржинальным; renewalsUNKNOWN |

Карточки для review: [украинская](offers/BOT_RECOVERY_UA.md), [английская](offers/BOT_RECOVERY_EN.md). Не опубликованы на площадке. [Офлайн HTML rehearsal](demo/BOT_RECOVERY_DEMO.html) — review artifact, не hosted demo или customer case; [JSON](../../data/bot_recovery_demo_report.json). Сеть запрещена audit hook; реальных Telegram updates нет. Rollback намеренно возвращает **сломанный pre-fix snapshot**, затем repair применяется снова. Это честная проверка обратимости, не утверждение, что rollback сам восстановил сервис.

## Пять площадок: опубликованные механизмы ≠ successful KYC

Полная таблица — [readiness_channels.csv](../../data/readiness_channels.csv); HTTP/даты/quotes/partial pages — [policy checks](../../data/readiness_policy_checks.json). Статусы ниже относятся к публичным условиям, не личному кабинету владельца.

| Площадка | Регистрация/Украина | Получение денег | Комиссии | Fixed service |
| --- | --- | --- | --- | --- |
| Freelancehunt | Published support for Ukrainian BankID/Diia/passport;18+; actual account/KYC UNKNOWN | UAH directly to executor card; foreign bank/card routes; actual owner payout UNKNOWN | Safe UAH: client pays9%; foreign USD/EUR/PLN: executor pays9%; bank USD5/EUR5; card1.5%+EUR1; intermediary FX extra | Fixed-price projects/bids yes; standalone searchable service-card catalog not verified |
| Upwork | Official Ukraine-specific support and eligibility policy; sanctioned territory exceptions;18+; KYC UNKNOWN | Direct to Local Bank published0.99 USD +possible bank fees; owner Ukraine route/currency/limits UNKNOWN | Freelancer Service Fee0-15% per contract; actual fee shown before accepting; Connects0.15 USD each | Project Catalog fixed scope/tier listings reviewed before publication; no ads needed in principle |
| Fiverr | Current retrieved articles do not explicitly establish Ukraine seller eligibility; manual owner country check required | PayPal/bank via Payoneer/Payoneer account; country restrictions depend on provider; UA route UNKNOWN | Seller earns80%; bank via Payoneer withdrawal1USD/min20; Payoneer account3USD/min10; provider FX extra | Gigs: up to3packages and extras; ID verification may be required before publication |
| Contra | Free account path documented; wallet requires Persona verification; exact UA eligibility UNKNOWN | Local bank/PayPal/Payoneer/crypto published; country list points to Notion, returned only shell; no UA payout proof | Free platform fee15USD below500,29 USD from500; payer must be checked. Payoneer3USD+1-2% or country-specific flat up to15; FX extra | Service/project presentation supported by published profile/payment guides; actual seller listing approval UNKNOWN |
| Freelancer | Ukraine-specific admission UNKNOWN; no account created; published generic terms are not successful KYC | Owner route and KYC UNKNOWN; attempted support URLs returned semantic article-not-found despiteHTTP200 | Published fixed10% or5USD minimum; hourly10%; initially6free bids/month; minimum balance required; Express withdrawal1USD plus provider fees | Fixed-budget bidding documented; independent fixed-service catalog not verified |

| Площадка | Новый аккаунт | Без платной рекламы | Материалы | Ограничения |
| --- | --- | --- | --- | --- |
| Freelancehunt | Profile, skills, honest examples; verification improves published ranking; actual bid/access limits in owner account not tested | Projects/bids/profile search, no guaranteed impressions; sample deployment request126 bids | Synthetic demo; one-scope checklist; realistic experience; manual relevant bid only after launch approval | Published SWIFT restrictions for residents of Crimea/Donetsk/Luhansk/Kherson/Zaporizhzhia; other routes must be checked separately |
| Upwork | Identity/tax/payment details; profile; listing review; no assurance of eligibility or first ranking | Catalog and profile search documented; share own demo only when authorized; zero baseline traffic measured | English scope, image/video/PDF, FAQ, acceptance, excluded work, truthful synthetic case | Some new freelancers need qualifying Connects purchase/Plus before ANY marketplace proposal; no blanket free-proposal claim |
| Fiverr | Identity, phone/business information, profile and compliance; no fake reviews or duplicate accounts | Title/tags/search and vendor recommendations for video/sample; no measured new-seller distribution | Clear Gig title,3 tiers, synthetic demo image/video, FAQ, honest delivery/revision limits | New freelancers may need a one-time ID verification fee (amount not established); no guaranteed zero-cost onboarding |
| Contra | Profile/portfolio plus Persona for wallet; honest prior client reviews only if real and consented | Discovery score includes profile, contributions, recommendations, earnings, response and Pro; no guaranteed zero-review traffic | One-liner; real/synthetic-labelled work samples; scoped service; support and payment readiness | Commission-free claim does not eliminate platform/processor fees; holds and4-day clearance; Pro affects ranking/fees |
| Freelancer | Profile, balance, KYC/payout and account limits need manual review; no source job automation | Manual bidding/project matching possible in principle;6 free bids are not a repeatable acquisition engine | Portfolio and relevant manual proposal after owner permission; verify financial/access terms first | Section33 requires EXPRESS WRITTEN PERMISSION for automated access including API; collection stopped and listing records removed |

Ключевые primary references:

- Freelancehunt: [Safe fee](https://help-ua.freelancehunt.com/uk/sieif/komisiia-za-vikoristannia-sieifa), [withdrawals](https://help-ua.freelancehunt.com/uk/finansovi-pitannia/viviediennia-koshtiv-platizhni-instrumienti-ta-komisiia), [verification](https://help-ua.freelancehunt.com/uk/vierifikatsiia/pierievirka-profiliu), [rules](https://freelancehunt.com/legal-center/rules). В UAH9%платит клиент; не вычитать ещё 9%из исполнителя в модели UAH. Для USD/EUR/PLN платит исполнитель. SWIFT geographical restrictions не означают blanket ban всей регистрации/всех выплат Украине. Текст service-card catalog/search не подтверждён: основной путь — manual relevant project proposal после разрешения.
- Upwork: [eligibility](https://support.upwork.com/hc/en-us/articles/211067778-Eligibility-to-join-and-use-Upwork), [fee0–15%](https://support.upwork.com/hc/en-us/articles/211062538-Learn-about-the-Freelancer-Service-Fee), [Catalog](https://support.upwork.com/hc/en-us/articles/360058234233-How-to-get-started-with-Project-Catalog-as-a-freelancer), [Connects](https://support.upwork.com/hc/en-us/articles/211062898-About-Connects-costs-uses-balances-and-expiration), [bank](https://support.upwork.com/hc/en-us/articles/211063888-How-to-withdraw-earnings-with-Direct-to-Local-Bank), [Ukraine support](https://support.upwork.com/hc/en-us/articles/4723031364115-How-expedited-payments-for-freelancers-in-Ukraine-work). Ukraine support подтверждает опубликованную policy path; конкретный банк, территория, KYC/налоги и actual fee нужны от владельца. Accelerated Ukraine hourly payments не распространяются автоматически на fixed-price jobs.
- Fiverr: [80%earnings](https://help.fiverr.com/hc/en-us/articles/9234443621137-Your-earnings-page), [payouts](https://help.fiverr.com/hc/en-us/articles/360010530058-Withdrawing-your-earnings-managing-payout-methods), [new ID verification](https://help.fiverr.com/hc/en-us/articles/6348992414097-Verifying-your-identity-as-a-new-freelancer), [Gig practices](https://help.fiverr.com/hc/en-us/articles/360010452317-Gigs-best-practices). Возможна разовая ID fee для некоторых новых продавцов; размерUNKNOWN. UA route не подтверждён country-specific документом. Нельзя обещать signup+withdrawal за$0.
- Contra: [fees](https://help.contra.com/en/articles/9322934-fees-overview), [payout](https://help.contra.com/en/articles/10008642-payouts), [KYC](https://help.contra.com/en/articles/9322955-how-to-verify-your-identity-on-contra), [first-client guide](https://help.contra.com/en/articles/11853356-how-to-get-your-first-client-on-contra), [discovery score](https://help.contra.com/en/articles/11899394-how-contra-s-discovery-score-works). «Commission-free» не означает отсутствие$15/$29 platform fee, processor/FX fees. Country list открывается как Notion shell, Ukraine routeUNKNOWN; нельзя заменить этим successful wallet setup.
- Freelancer: [fees](https://www.freelancer.com/feesandcharges), [section33](https://www.freelancer.com/about/terms). Fee page прочитана до выявления automation restriction; job evidence удалено. Два support addresses — soft404приHTTP200; не используем их как KYC/payout policy proof. Дальнейшая проверка владельцем вручную или с письменным разрешением площадки.

## Первые обращения без отзывов: что известно

VERIFIED наличие механизмов/инструкций, а **не** конверсия новых продавцов. Upwork показывает reviewed Catalog listings в search и позволяет добавить image/video/PDF. Fiverr рекомендует точный title/tags, демонстрацию и ясные tiers. Contra discovery учитывает profile quality, contributions, earnings, recommendations, response time и Pro; его first-client guide предлагает привести уже существующих клиентов и настоящие прежние отзывы. Для продавца без сети это не бесплатное создание спроса из ничего. FH позволяет ответить на существующий запрос; большая competition требует точного scope и доказательства, не AI mass bid.

Не найдено representative new-seller cohort/verified first-sale histories, позволяющих назначить conversion. Собственный demo без разрешённой публикации имеет 0 измеренного трафика. Materials: synthetic label, 60–90 s walkthrough plan, executable acceptance, exclusions, scope/cap, truthful skills, privacy and response SLA без обещания uptime. Не подделывать reviews и не обещать полную починку до диагностики.

## Рекомендуемый минимальный эксперимент — подготовлен, не запущен

После **отдельного** разрешения owner и подтверждения payout: один язык/пакет, один источник существующих запросов, максимум 5 вручную квалифицированных ситуаций или добровольных inbound conversations. Сначала подтвердить owner-approved access, один конкретный broken/ready deployment workflow, decision maker, budget и timeline. Предложить paid diagnosis с clear acceptance; не отправлять общую карточку на все найденные записи. Если нет 5 подходящих ситуаций в 14 дней, не делать вывод о цене — сначала менять канал/сегмент. Один existing deployment request в sample не даёт достаточного pipeline четырёх repair sales.

Измерять source-attributed inquiries→qualified→quote→accepted→paid→hours→support; минимальные контакты вне Git. После 5 qualified discussions/quotes без принятия цены — проверить проблему/доверие/scope; после 2 похожих paid fixes — повторяемость; после 2 renewals — recurring value. Эти пороги ASSUMED experiment design, не статистический benchmark. Оплаты и contact permissions в этом PR не получены.

## Таблица решений

| Уже подтверждено | Неизвестно | Как проверить после разрешения | Стоимость проверки (A) | Положительный результат | Отрицательный результат |
| --- | --- | --- | --- | --- | --- |
|59 FHкандидатов screened,0 strict bot recovery | Есть ли buyers именно узкого recovery? |5 qualified situations, один scoped paid diagnostic offer |2–4 hподбора +до 2 hdiagnosis; cash$0 до platform gates |2 похожих paid fixes→узкий пакет | Нет eligible situations→не строить bot-recovery продукт |
| Offline fault/diagnosis/fix/rollback воспроизводятся | Платят ли$75/1500UAH за diagnosis? | Один accepted paid scope; не бесплатная работа ради отзыва |Материалы готовы; фактическая fee/KYCотдельно | Сохранить accepted price и actual hours | Price/scope/trust review, не «повысить AI confidence» |
| Published FH/Upwork paths и fees | Личный KYC, территория, банк | Owner manual secure account/payout status, без секретов в чат |0.5–2 h; обязательные feesUNKNOWN | Разрешить один канал в плане | Выбрать другой доступный путь; не обходить ограничения |
| Public IT awards и 5 Czech IDs можно сверить | Разрешён ли subcontract и нужен ли партнёр? | Manual contract/partner-intake review; только consented conversation |2–4 hбез outreach spend | Capability-fit pilot отдельно | Не превращать awards в spam list |
|5 технических pain families,13 reports | Общий продукт лучше бесплатного fix? | Один reproducible client case + free-substitute comparison |1–2 hна family | Повторяемые paid implementations→shared primitive | Бесплатный workaround достаточен→не строить продукт |
| Канальная модель воспроизводима | Traffic,accepted price,close,lag | Собрать actual cohort при разрешённом pilot |≤4 hmeasurement setup | Калибровать priors с uncertainty | СохранитьUNKNOWN; не обещать$2000 |
