# Red team: 15 кандидатов

Отдельный критический проход одного исследователя после отбора. Это не внешний независимый аудит. Во всех строках дополнительно неизвестны фактические KYC/банк, CAC и принятый чек. Рекламный путь для каждой consumer-идеи наследует риск недостаточных DAU/eCPM из [05](05_ADVERTISING_ECONOMICS.md).

| ID | Почему не заплатят / free competition | Канал и сбои автоматизации | Платформы, поддержка и деньги | Условие отказа |
|---|---|---|---|---|
| F01 | Provider уже включает QA; $450 выше observed $400 budget и не принят | Два intake не дают пять покупателей; разные export semantics ломают универсальный compare | PII и спор о scope; partner share и ручная поддержка; PSP/банк UNKNOWN | Нет оплаты или повторного заказа; >8h исполнения; не положительный economic profit |
| F02 | Вендор бесплатно объясняет dates/status/refunds; отдельный tool не нужен | Закрытая support тема не buyer channel; определения отчётов различны | Финансовые данные и риск tax claims; custom mapping support | Native settings/FAQ полностью закрывают вопрос или никто не покупает diagnostic |
| F03 | Shipping plugin/native zones/таблица уже решают | Нет первых users; carriers/rules меняются | Ошибочная цена доставки; широкий checkout matrix | Нет покупателя fixtures сверх купленного shipping tool |
| F04 | CheckView и бесплатный Playwright достаточны | Стабильные тесты требуют много edge cases; каталог не traffic | Тестовые транзакции, secrets, PII; maintenance дорог | Нужен полноценный hosted test platform вместо узкого report |
| F05 | Бесплатный invoice preview и existing templates | Нет канала; local invoice conventions отличаются | Tax/localization liability; annual ARPU низок | Покупатель требует legal invoice certification |
| F06 | Free crawler/ручная проверка и Polylang | Нет install path; dynamic languages создают false positives | Совместимость и translation support; payout отдельно | Бесплатный equivalent даёт полный output за30min |
| F07 | Free calendar/существующий shift app; один bug не рынок | ASO/CPI неизвестны; сложные pay rules | Payroll accuracy/support и mobile release gates | Нет первого100 route или плательщик предпочитает имеющийся app |
| F08 | Низкая годовая цена incumbents и ручной ввод | Слабая привычка/retention, cloud sync не прост | Data-loss support; subscription экономически не подтверждена | Нет paid differentiation/канала; не строить subscription clone |
| F09 | SafetyCulture free tier и обычный PDF | Ни одного industry partner; media/offline edge cases | Business critical evidence, confidential photos, reliability | Для пилота требуют роли/sync/video/full platform |
| F10 | Calendar/spreadsheet/paid-once Bobby | Редкое использование; мало рекламы и recurring value | Financial metadata/sync entitlement support | Не готовы платить регулярно; subscription build REJECT |
| F11 | GoFullPage$12/year + free editor | Миллионы competitor installs не наш channel | Screen PII/CWS review; 2000 payers при$1/mo | Нет преимущества и first100 route; clone REJECT |
| F12 | Native groups/bookmarks и бесплатные extensions | Lost-session trust, migration friction, нулевой organic volume | URL privacy; sync/restore support; checkout UNKNOWN | Native/free покрывают задачу; clone REJECT |
| F13 | Checkbot уже продаёт CSV/PDF reports | No first100 route; crawling/redirect edge cases | Source terms/permissions; не все сайты можно сканировать | Нет нового output сверх existing paid/free tool |
| F14 | Copy/paste/Sheets/free table tools | Layouts хрупки; reviewer paywall anger не спрос | Forbidden scraping/site terms; false confidence in schema | Без отдельного authorized workflow и buyer оплаты — HOLD |
| F15 | Scribe/Tango/ручная инструкция/AI | Нужны enterprise trust и reliable redaction | PII/screenshots и высокая поддержка; broad permissions | Не закрывается одним безопасным schema/scope; нет partner buyer |

Ни одна идея не прошла одновременно проверку оплаты, дистрибуции, экономики с трудом владельца и payout. F01 выбран только для ограниченного ценового эксперимента. F02 — резерв после конкретного buyer evidence, остальные не оправдывают параллельные MVP.
