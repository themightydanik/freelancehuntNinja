# Первый эксперимент: проверить покупку отчёта, не строить платформу

Ниже подготовлен конкретный пакет. Ничего не опубликовано и не отправлено; коммерческий этап требует отдельного разрешения пользователя, как прямо установлено в запросе. Offline demo уже выполнен в рамках исследования.

**Оффер для проверки:** «Для одной согласованной пары WooCommerce/Shopify exports определим, какие показатели должны совпадать, и выдадим воспроизводимый список расхождений. Начальная диагностика одного определения — $100. Отдельная полная приёмка ограниченного export scope — $450. Никаких live store changes, налоговой сертификации, гарантий SEO или продаж». Цены не являются market rate; покупатель должен принять их явно. Не брать дважды оплату за один и тот же результат diagnostic/full pack.

Ограничение первого теста: одна валюта, явный timezone/date-field policy, согласованные statuses, явное представление возвратов; до 5 000 variants / 50 000 order rows — ASSUMED limits для пилота, не протестированный production capacity. Нет доступа к real stores. Если определения различаются, выдавать BLOCKED_DEFINITION, а не утверждать, что миграция неправильна.

План на семь дней, максимум16h подготовки и$0 внешних расходов:

| День | Конкретный результат | Часы |
|---|---|---:|
| 1 | Сопоставить vendor dry-run/support/manual output с нашим scope; отказаться от уже решённой функции | 3 |
| 2 | Прогнать synthetic contract demo; сформулировать failure cases и exclusions | 3 |
| 3 | Собрать sample report и фиксированный acceptance checklist; измерить время | 3 |
| 4 | Проверить подходящий partnership intake и подготовить один адресный текст без отправки | 2 |
| 5 | Зафиксировать bank/KYC/payment prerequisites, не регистрируясь и не выполняя перевод | 2 |
| 6 | Пользователь рассматривает конкретный пакет и отдельно разрешает выбранный контакт/пилот | 1 |
| 7 | Если разрешено — начать проверку; иначе STOP/HOLD с готовыми материалами | 2 |

**Подготовленный текст для P18, не отправлен:**

> We are testing a narrowly scoped, read-only acceptance report for WooCommerce-to-Shopify exports: agreed keys, dates, statuses, currency and refunds, with a reproducible exception list. Does your partnerships team consider independent acceptance work for migrations, or is this already fully covered in-house? If there is a relevant gap, we can scope a paid $100 diagnostic before any implementation. No store access or customer data is needed for the initial scope discussion.

**Отдельный qualification question для SendPulse S28, не отправлен:** «Есть ли сейчас конкретная недостающая интеграция, для которой заранее обсуждаются вознаграждение, критерии приёмки и обещанное размещение/анонс? Какие существующие интеграции исключают дублирование?» Это не оффер нового Woo connector и не основание строить до ответа.

Минимальный успех: независимый покупатель принимает scope и платит за него; работа принята, refund/dispute учтён, зачисление подтверждено. $100 diagnostic может быть learning expense, а не прибыль: при двух часах исполнения плюс квалификации/partner share экономическая маржа мала. Одна оплата не доказывает $2 000/month или retention.

Следующие gates: два похожих full packs по принятой цене с positive economic profit и хотя бы один повторный agency order. Затем оплаченная лицензия и её фактическое повторное использование. Только тогда обсуждать store wrapper; нельзя начинать три MVP для «двух каналов».

ASSUMED stop rules: пять квалифицированных обсуждений без принятия цены/scope → изменить один параметр или остановиться; 14дней без достаточного exposure → INSUFFICIENT EXPOSURE, а не опровержение спроса. Один partnership contact не равен пяти обсуждениям. Условия немедленного отказа: equivalent output бесплатно за≤30min; QA уже включён в услугу; нет безопасных разрешённых exports; actual delivery>8h; требуется legal/tax/live-write guarantee; нет законного payout.

Сейчас можно получить только новые документальные данные: продажи прямо запрещены текущим этапом. Реальные коммерческие доказательства за семь дней возможны после отдельного разрешения и ответа покупателя; обещать их получение нельзя. Все текущие collected revenues UNKNOWN.
