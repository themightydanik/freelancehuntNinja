# Пятнадцать возможностей плагинов и приложений

[Данные G01–15](data/plugin_opportunities.csv) включают аналоги, тарифы, предполагаемый разрыв, бесплатную замену, агентскую лицензию, правила каталогов, оплату, обнаруживаемость и поддержку. Изучены WordPress/WooCommerce и Shopify; CRM/ERP-каталоги отдельно рассмотрены в партнёрской части.

| ID | Проверяемый продукт | Альтернативы |
|---|---|---|
| G01 | Приёмка Woo→Shopify экспортов | Matrixify, WP All Export, таблицы |
| G02 | Проверка отклоняемых import rows | WebToffee, WP All Import, native importer |
| G03 | Приёмка формы/checkout после релиза | CheckView, Playwright, ручной тест |
| G04 | Проверка invoice template | WP Overnight, бесплатные PDF invoices |
| G05 | Сценарии shipping rules | Flexible Shipping, native zones, таблица |
| G06 | Отсутствующий переведённый контент | Weglot, TranslatePress, ручной просмотр |
| G07 | Связи языковых страниц | Polylang Pro/free, crawler |
| G08 | Сочетания купонов | Advanced Coupons, native coupons |
| G09 | Пороговые скидки | FlyCart и ручная корзина |
| G10 | Определения показателей Analytics/export | AlgolPlus, Woo Analytics, документация |
| G11 | Квитанция согласованных bulk edits | Smart Manager, native bulk edit, snapshots |
| G12 | Custom checkout fields в экспорте | Acowebs, Checkout Blocks |
| G13 | Приёмка spreadsheet import | WP Sheet Editor, WP All Import |
| G14 | Приёмка metaobjects после переноса | Matrixify и native admin |
| G15 | PDF-ссылки в уведомлениях | Order Printer Pro, Shopify Order Printer |

Платные ориентиры: AlgolPlus $30/год [R16], Polylang Pro от €99/год [G07], Acowebs $49/год [G12], CheckView Essentials $35 и Plus $70 в месяц [G03]. Не считать Essentials планом с checkout, пока entitlement не проверен. Advanced Coupons $99.50 — introductory price против обычных $199 [G08]. Большой lifetime package WP All Import не является ценой любого отдельного экспортёра. Где точного сопоставимого quote нет, указан UNKNOWN.

Особый случай G10: конкретный support thread описывает разницу dates/statuses/refunds/taxes. Поставщик просит уточнить отчёт: разные Analytics views имеют разные показатели. Статус not resolved и закрытие темы не доказывают технически неразрешимый дефект или отсутствие private-ticket решения. S30 объясняет фильтры дат/статусов; S31 подтверждает поддержку refund export. Новый exporter может вообще не требоваться. Узкий diagnostic тоже может оказаться обычной бесплатной поддержкой.

WordPress.org [S14]: GPL-compatible бесплатное ядро, запрет trialware; premium add-on можно распространять отдельно. Genuine serviceware регулируется отдельно. Нельзя оправдать загрузку исполняемого кода словом «SaaS». Каталог не является checkout и не гарантирует показы. Бесплатные пользователи создают расходы на поддержку; telemetry и ссылки требуют соблюдения правил/согласия. GPL не делает license key защитой от копирования; ценность должна быть в результате, обновлениях и поддержке.

Woo Marketplace [S15]: vendor получает 70% продаж до применимых иных расходов; нужны application/review и поддержка. Это отличается от direct WordPress checkout и Shopify. Shopify [S16/S17]: $19 registration, 2.9% processing и отдельные правила revenue share/associated accounts, review, Billing/data access и Hyperwallet. Индивидуальные условия выплаты основателю не проверены.

Матрица поддержки включает PHP, WordPress, Woo, HPOS, Checkout Blocks/classic, темы и другие плагины. Read-only normalization core может её сузить, но это пока допущение. Агентская лицензия должна явно ограничивать sites, support и условия клиента; чужой license key нельзя автоматически перепродавать. Не строить одновременно WordPress wrapper, Shopify app и Chrome extension. Ни для одного нового листинга не подтверждён поток первых 100 пользователей → полноценный plugin build остаётся HOLD.
