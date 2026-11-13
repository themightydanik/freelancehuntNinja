# Финалисты

**Полноценная разработка: 0. Коммерческий эксперимент: 1. Подтверждённых recurring продуктов: 0.** Не назначаем ещё два финалиста ради квоты.

### F01 — Export Acceptance Kit

- **Покупатель:** небольшое ecommerce-агентство с повторяющимися миграциями WooCommerce→Shopify; отдельный merchant перед конкретной приёмкой — вторичный сегмент.
- **Проблема:** нельзя согласовать, какие ключи/суммы должны совпадать между двумя exports; разные даты, статусы, refunds и валюты создают ложные расхождения.
- **Альтернативы:** Matrixify dry-run/history [G01], WP All Export, native CSV и spreadsheet; AlgolPlus $30/год [R16] и vendor support для Woo-показателей. LitExtension/другие migration providers могут включать QA, что надо проверить до продажи.
- **Преимущество:** только независимый согласованный контракт приёмки и воспроизводимые исключения. Оно ASSUMED, легко копируется; доверие, разрешённые fixtures и повторные отношения пока отсутствуют. Обычная красивая таблица не дифференциация.
- **Цена теста:** $100 за определение одного показателя/пары файлов, максимум два часа delivery; $450 за ограниченный full pack только при ≤8h исполнения с поддержкой. Квалификация и продажи дополнительно учитываются в модели. Цена и часы не приняты покупателем.
- **Экономика:** [B2B_FIXED](data/financial_thresholds.csv) включает assumed PSP6%+$0.50, partner20%, refunds3%, direct costs и труд$25/h. Улучшение против Genesis зависит от **непроверенных** более высокой цены/меньших часов. При10h вместо8h пять packs теряют ещё$250 economic profit.
- **Канал:** один явный partnership intake P18, затем заказ только при принятии scope. Нет доказательства, что это даёт пять buyers; direct marketplace wrapper пока не строить.
- **Прототип:** [offline demo](scripts/export_contract_demo.py): synthetic rows, dates/statuses/currency/refunds, fail-closed при несовместимых определениях; без API, настоящих файлов клиентов и live writes.
- **Реальная оплата:** после отдельного разрешения на конкретный контакт и пилот — agreed scope, законный доступный payment path, принятая работа и подтверждённое зачисление. Ни положительный ответ, ни funded milestone без release не collected revenue.
- **Отказ:** бесплатный workaround полностью закрывает результат; agency считает QA включённым; нет оплаты; actual labor>8h; payout невозможно настроить; нужен accounting/SEO/live-write guarantee.
- **Развитие при успехе:** два похожих full-price packs, повторная покупка одного агентства, measured positive contribution after labor; затем отдельно проверить $79/месяц license. Только после оплаты лицензии и повторного использования решать о WP adapter/store listing.

Buyer-to-cash: `agency →[OBSERVED related workflow] проблема →[OBSERVED adjacent budget S32, not our sale] существующие расходы →[VERIFIED route P18 / UNKNOWN appetite] intake →[UNKNOWN] согласованный pilot →[UNKNOWN] оплата →[VERIFIED synthetic subset / UNKNOWN real delivery] принятый report →[UNKNOWN] повтор / лицензия`.

Критическая цепочка обрывается на доступе к buyer, принятии цены и cash. Поэтому это кандидат для исследования, а не подтверждённый путь к $2 000.

F02 Woo definitions diagnostic имеет новый конкретный problem signal, но документация может уже решать его. SendPulse funded integration имеет более явный механизм помощи/промо, но нет конкретной недостающей интеграции/quote. Они не объявлены дополнительными финалистами.
