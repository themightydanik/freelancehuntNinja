# Минимальные эксперименты и первые деньги

Ничего не отправлено, не опубликовано, не зарегистрировано и не оплачено. Ниже конкретный пакет для отдельного разрешения на коммерческий этап. Offline demo и эта карточка уже подготовлены в разрешённом исследовании.

### Карточка C01 — готовый текст предложения, не опубликован

**Migration data acceptance: know which records differ before you sign off.**

For one agreed source/target export pair, receive a reproducible reconciliation of IDs, counts, quantities and monetary totals, plus an exception list. Start with a $100 diagnostic covering one entity and a mapping/scope decision. A separate $400 acceptance pack covers the agreed full export scope, one revision and seven days of clarification. No live store changes. No tax, SEO ranking or checkout certification. An unsupported mapping produces a clear limitation report, not a claim that the migration is correct. Delivery target: two business days after complete approved inputs for the diagnostic, five for the pack; these are proposed targets to validate.

Цена/лимиты/сроки — ASSUMED. Время diagnostic cap 2h + 1h qualification/admin; при 15% fee и 5% refund planning $100 даёт $80.75 cash after platform до direct/tax/FX. При $25/h и 3h owner времени почти нет economic surplus. Это price discovery, не масштабируемая экономика. $400 full pack не предполагает обязательную доплату после diagnostic: buyer заранее выбирает scope; не двойной счёт за один результат.

### Уже выполненный offline test

`scripts/migration_acceptance_demo.py` создаёт synthetic source/target в памяти и выводит `data/demo_result.json`: duplicate key, missing row и changed amount. Decimal избегает float rounding; никаких реальных магазинов/API/персональных данных. Контрольная равная пара обязана давать PASS. Это демонстрация приёмки ограниченных exports, не MVP платформы. Read-only report; исходные файлы не меняются.

### Семь дней, максимум 16 часов подготовки

| День | Результат | Часы cap | Cash |
|---|---|---:|---:|
| 1 | Уточнить buyer, исключения, scope и личный country/payout checklist; без нового аккаунта | 2 | $0 |
| 2 | Проверить, закрывают ли vendor dry-run/history/manual spreadsheet весь scope; documented comparison | 3 | $0 |
| 3 | Прогнать synthetic exports, проверить false positives и трудозатраты; приложенный demo — старт | 3 | $0 |
| 4 | Подготовить listing с двумя scope/ценами, sample report и intake без контактов клиентов | 3 | $0 |
| 5 | Owner-side account eligibility/payout verification только после отдельного разрешения, без money transfer | 2 | $0 planned |
| 6 | Review конкретной карточки и разрешение на один publication/pilot; здесь не публикуем | 1 | $0 |
| 7 | Зафиксировать go/hold/kill; после разрешения измерять channel exposure 14 дней | 2 | $0 |

Проверка payout без перевода подтверждает только доступный method/KYC status. Реальный collected revenue требует будущего законного paid pilot и фактического зачисления, которое этим исследованием запрещено.

### Успех, отказ, защита от ложного вывода

Минимальный коммерческий success: один независимый buyer принимает scope и платит $100; service принята и деньги доступны/получены после fee/refunds; delivery cap выдержан. Это валидирует одну продажу, не $2k/month. Следующий gate: два похожих paid $400 packs, measured all-in labor ≤10h каждый и повторная покупка от одной agency; затем тест recurring license, а не заранее SaaS.

Порог теста — ASSUMED decision rule: после 5 qualified discussions ноль accepted scope/price → изменить один параметр или STOP; после 100 genuinely targeted visits ноль qualified inquiries → пересмотреть problem/offer. Это не статистически достаточное доказательство отсутствия рынка. Если 14 дней нет 100 visits/5 discussions, gate INSUFFICIENT EXPOSURE: не строить и не считать спрос опровергнутым. Lead volume нельзя добирать неразрешёнными сообщениями.

KILL: manual equivalent ≤30min; provider включает тот же independent output; нет безопасных exports; buyer требует live writes/tax/SEO guarantees; actual full pack >10h два раза; payout нельзя законно настроить. HOLD: есть запрос, но только сложный scope за $400 — не продавать нерентабельное обещание.

C02 conditional cheap test: только после появления агентства и отдельного разрешения на его backup, одна isolated restore rehearsal на non-production clone, planned 4h/$0 tools на инфраструктуре клиента. Success — paid bounded rehearsal и второй paid cycle; kill если 24/7 liability/privileged secrets выходят за scope. Не выполнено.

C03 conditional cheap test: synthetic sender inventory + sample approval/rollback report, planned 3h/$0; позже один consented transactional domain без DNS writes. Success — MSP платит за конкретный change-control outcome сверх free dashboard; kill если нужно обещать inbox placement или есть только demand на cold email evasion. Не выполнено.

Самый дешёвый путь к **подтверждённой оплате**: C01 $100 bounded diagnostic → один доступный, одобренный listing/входящий buyer → agreed scope → funded/completed/accepted → bank receipt. До первого buyer возможны $0 sales сколько угодно дней; минимальный cash budget не равен нулевой стоимости: подготовка 16h×$25=$400 opportunity cost.

**Экономический success gate сверх одной оплаты:** цену $400 использовать только как проверяемый benchmark, не утверждённый прибыльный бизнес. При 5 packs и16h sales/admin нужно ≤9.23h all-in/client либо ≥$423.78/pack для нулевого economic profit до налогов/FX. Для резерва на риски тестировать accepted $450 либо измеренное время ≤8h, не объявляя такое принятие заранее. Paid diagnostic может быть learning expense; нулевая прибыль diagnostic не допускает масштабирования.
