# Доказательства расходов и качество сигналов

[55 evidence records](data/evidence_registry.csv), дата 2026-11-13. Для каждого есть URL, тип, ограничения, independence group. VERIFIED относится только к содержимому первичного источника. OBSERVED — индексированный запрос/отзыв/кейс, не аудит оплаты. Здесь нет заявления, что каждый кандидат имеет три независимых доказательства покупки.

| Кандидат | Сигналы из разных сторон | Что реально подтверждено | Что отсутствует |
|---|---|---|---|
| C01 migration QA | E04 buyer $400; E05 theme buyer; E06 Woo buyer; E02/E03 merchant reviews; E01/E07 substitutes | Существует открыто выраженное намерение оплачивать related audit; люди сообщают оплату migration tool | Сопоставимая собственная принятая цена; invoices; repeat pipeline; отдельный CSV-only scope. E05 смежный, E06 может иметь duplicate listing; три запроса не три оплаты |
| C02 restore proof | E14 $25/hire; E15 $100; E16 $250; E11–13 tools | Несколько запросов на one-off восстановление и конкретные substitutes | Три независимых сигнала **recurring rehearsal** не найдены. Нельзя переносить emergency budgets на subscription |
| C03 MSP change control | E23 platform requirement; E24 $20 audit; E22 vendor MSP case; E17/E20 paid tools | Потребность в auth и предложения управления существуют | Три независимых сигнала оплаты нашего MSP scope не найдены. E22 и E21 зависимы от EasyDMARC. E25 complex outreach scope не target validation |
| C04 payout exceptions | E26 A2X price; E27 MyWorks; E28 Synder; E29 Intuit trigger | Несколько функционально эквивалентных коммерческих tools и миграция | Три независимых buyer signals на exception evidence service не найдены; цены конкурентов не buyers |
| C05 SharePoint | E30 official retirement + official templates + MSP referrals | Trigger и native solution подтверждены | Это один publisher, не три независимых сигнала; наши расходы/заявки UNKNOWN |
| C06 n8n handover | E37 license boundaries; E38 partner program; native runbook alternative | Возможность ограниченной услуги по лицензии, существование интеграторов | Три независимых buyer budget/payment signals не найдены; handover might already be included |

**Лестница доказательств.** Advertised price: E01/E07/E11/E17/E20/E26. Buyer budget: E04/E14–16/E24/E25. Self-reported paid tool: E02; поставщик подтверждает принятие плана в ответе, но оспаривает complaint details. Platform reported hire: E14; не completed contract. Completed sale: UNKNOWN. Collected revenue: UNKNOWN. Наш collected revenue: $0 наблюдённых оплат, поскольку коммерческие действия не проводились; это не доказательство нулевого спроса.

Negative-review audit: billing/cancellation dispute и allegedly incomplete migration/upgrade dispute — два наблюдения. Не называть их доказанной технической ошибкой или high prevalence. Ответы Matrixify указывают на billing cycle и approved refund. Жалоба на metaobjects не противоречит тому, что current price/features уже включают их: поддержка поля и корректность конкретной миграции — разные вопросы. При существующем dry-run/history необходимость отдельной QA must be earned, не предполагается.

Временные конфликты: у E14 relative posting date и indexed title не совпадают — не используем для оценки weekly volume. У региональных Intuit pages различаются 2025/2026 формулировки — не объединяем в единую дату shutdown. A2X banner сообщает повышение 14 ноября 2026; расчёты не должны использовать $79 как вечный benchmark. В реестре собственные цены отдельно от чужих.

Отсутствие трёх независимых сигналов явно снижает gate; недостающие доказательства не заменены большим количеством URL. Отзывы не выгружались массово, контакты/имена частных покупателей не сохранялись. Search snapshots не дают полноту рынка или стабильность страницы.
