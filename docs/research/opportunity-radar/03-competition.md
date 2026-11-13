# Конкурентное поле

Проверка официальных страниц 14.11.2026. Заявления поставщика не являются независимым измерением recall, точности или скорости. Неподтверждённые цифры не перенесены из обзоров.

| Класс / сервис | Что уже делает / контакты и персонализация | Скорость / coverage | Цена на дату проверки | Ограничение для нашей задачи |
|---|---|---|---|---|
| Lead database / [Apollo](https://www.apollo.io/pricing), [intent](https://www.apollo.io/product/buying-intent) | Компания, контакты, enrichment, buying intent, sequences | Vendor указывает weekly refresh для intent; не real-time demand, полнота не измерена | Pricing page есть; точная сопоставимая цена с нужными credits не зафиксирована, запросить quote | Company research ≠ утверждённый проект. Контакт из базы не создаёт прав на сообщение; resale требует отдельных условий |
| Technographics / [BuiltWith](https://builtwith.com/plans) | Технологии, retail lists, история, фильтры, export контактов | Vendor заявляет weekly page updates; first seen не launch; coverage не тестировалась | Basic $295/mo, Pro $495/mo, Team $995/mo; monthly USD до налогов, не эквивалент цены API/resale | Уже покрывает tech-based lead-gen; отсутствует доказательство, что конкретный сайт купит миграцию |
| Workflow/enrichment / [Clay](https://www.clay.com/pricing), [signals](https://www.clay.com/signals) | Multi-provider waterfall, job changes, custom signals, персонализация, workflow | Зависит от provider и trigger; SLA не установлен | Usage-based actions/data credits; фактический comparable bill не рассчитан | «Собрать данные и написать AI-текст» уже commodity. Права на каждого provider отдельно |
| Intent / [Bombora](https://bombora.com/intent/) | Topic research на уровне компаний через data cooperative | Frequency/precision по нашему ICP не измерены; coverage зависит от co-op | Сопоставимая публичная цена не установлена; коммерческое предложение | Topic surge не RFP и не конкретный ответственный/бюджет |
| ABM / [6sense](https://6sense.com/pricing) | Объединяет CRM, intent, scoring и sales intelligence | Не измерено; buyer-stage model не первичный коммерческий запрос | Custom quote на официальной странице | Уже предлагает приоритизацию; нужна проверка реальной задачи, не новый intent-score |
| Monitoring / [Visualping](https://visualping.io/pricing) | Page-change detection, ecommerce/regulatory monitoring, summaries, workflows | Интервал конфигурируемый; UI предлагает от monthly до 2 minutes, не SLA обнаружения события | Динамический calculator не вернул числовой тариф в прочитанной версии; не выдумываем | Разрешение на мониторинг целевого сайта остаётся обязанностью пользователя; изменение страницы не покупка |
| Procurement-native / [TED](https://ted.europa.eu/en/help/data-reuse), [Find a Tender](https://www.find-tender.service.gov.uk/Developer/Documentation) | Поиск реальных notices, первоисточник, иногда budget/route | Событие после публикации; наш пилот не измерил лаг | Пилот API: $0 за доступ; труд/хостинг не нулевые | Сильный бесплатный baseline. Много крупных, нерелевантных и завершённых закупок; право исполнения надо проверять |

Обычный поиск уже обнаружил множество специализированных tender агрегаторов на тех же NCG/Lumero notices. Поэтому «ещё один список закупок» также не преимущество. Их платные функции и тарифы здесь не оценивались; не заявляем уникальность.

## Проверяемые способы отличаться без «используем AI»

1. **Scope-fit для маленькой команды:** исключать hardware/safety, лицензии без implementation scope, крупные consortia, закрытые stages. Тест: доля принятых экспертом среди top-20 против CPV+keyword baseline.
2. **Evidence packet:** точный первичный ID, наблюдаемая задача, deadline, lot, явные пробелы и причина отклонения. Тест: время решения bid/no-bid против ручного поиска.
3. **Проверенный route и jurisdiction:** tender portal/opt-in/корпоративный канал с основанием; неизвестный route блокирует обращение. Тест: доля карточек, прошедших legal/channel checklist; не число собранных email.
4. **Версии и отрицательные события:** изменения scope, отмены, истечение deadline, award; stop-лист при закрытии. Тест: false positive rate и число предотвращённых неуместных обращений.
5. **Нишевой delivery playbook:** 50-SKU пакет, migration assessment конкретной версии, accessibility audit с понятными acceptance criteria. Тест: число подтверждённых задач и contribution margin исполненных проектов.
6. **Совместная проверка с владельцем:** merchant opt-in inventory и воспроизведение проблемы. Тест: доля дефектов, подтверждённых владельцем, а не inferred score.
7. **Экономика по исполнению:** показывать стоимость исследования, proposal и delivery, а не только «лиды». Тест: прибыль после фактического труда и возвратов.

Это гипотезы дифференциации, не доказанные moat. Вначале агентская внутренняя утилита; продажа подписки требует отдельной проверки willingness-to-pay, лицензий на перераспространение и support costs.
