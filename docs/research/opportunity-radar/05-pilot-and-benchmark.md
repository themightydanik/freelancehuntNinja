# Пилот и quality benchmark

## Реальная выборка

Сбор выполнен один раз 13 ноября UTC; точные URL, payload, время, HTTP status, объём и raw body hash — `evidence/collection-log.json`. Отчёт датирован 14 ноября по часовому поясу клиента. `as-of` для воспроизводимых вычислений: `2026-11-14T00:00:00Z`.

| Метрика | Find a Tender | TED |
|---|---:|---:|
| Полученные события | 500 | 100 |
| Страниц/запросов | 5 GET | 1 search POST |
| Первичные notice links | 500/500 (100%) | 100/100 (100%) |
| Даты публикации | 12–13 ноября | 9 ноября |
| Младше 14 дней | 500/500 (100%) | 100/100 (100%) |
| Повторные ID внутри источника | 0 | 0 |
| Кандидаты с rule-based service mapping | 17/500 (3.4%) | 3/100 (3%) |
| Active procurement + service keyword | 3/500 (0.6%) | 0/100 |
| Полностью подтверждённая конкретная услуга, eligibility и scope | 0 | 0 |
| Проверенный законный контактный route | 0/500 | 0/100 |
| Готовые к индивидуальному обращению | 0 | 0 |
| False-positive rate всего источника | Не измерен | Не измерен |
| Фактическое время ручной полной проверки | Не измерено | Не измерено |

**Source-linked не равно independently verified.** Все rows получены прямо из официального API, но это не проверка корректности каждого исходного notice. Web-инструмент не смог открыть страницы четырёх shortlisted FTS notices и FTS docs; API при этом дал штатный 200. Ограничение отмечено, обходов страницы не предпринималось. Для выводов о stage использован официальный JSON, для full eligibility review оснований нет.

FTS — bounded latest-update feed, не все закупки и не весь период. TED запрос: `publication-date >= 20261109 AND (classification-cpv = 72* OR classification-cpv = 7934* OR classification-cpv = 7953*)`, 100 из 1 263 совпадений, без второй страницы; первые записи оказались за 9 ноября. Нет random sample, поэтому нельзя переносить доли на весь поток. Погрешности keyword-правил на других языках существенны: TED не переводится автоматически и вероятные пропуски **не измерены**.

Companies House: 1 synthetic fixture; real events 0; свежесть/precision/contact fractions не считаются. Требуется API key, который не запрашивался. Это проверка pipeline и маркировки, а не живой source benchmark.

## Ручной первичный разбор 20 карточек

`data/cards.json` и `cards.md` содержат все 20 title-matched кандидатов, включая отказы. Это не 20 качественных лидов. Разбор выполнен по title, stage, date, value и доступному deadline, без полной tender документации.

- 15 карточек относятся к завершению/award и не подтверждают открытый заказ. Для прямого pitch заказчику отклонены.
- Ещё 1 active карточка отклонена: Warden Call Equipment / alarms / doors. Слово digital сработало, но предмет — safety-critical оборудование и обслуживание.
- 4 карточки оставлены **hold**: Lumero software procurement (нужны implementation scope/eligibility/deadline), NCG marketing framework (нужны lots/capacity; £29m gross — не доступный нам бюджет), Essex market engagement (ещё не заказ), GeoSphere meteorological software (specialist scope и неизвестный stage).
- **Contact now: 0.** На уровне title/stage screening 16/20 отвергнуты; это observed rejection fraction этой предвзятой выборки, **не** подтверждённая false-positive rate модели или источника.

Ни одной карточке не присвоен выдуманный бюджет услуги. Published procurement value сохранён только как справочное поле. Обращение может заслуживать подготовки лишь после документальной проверки конкретного lot, capacity и route; по доступным фактам ни одна карточка ещё не прошла эти проверки.

## Что умеет прототип

- Получение: opt-in collector, только официальные read-only APIs; HTTP POST TED используется для поиска, не публикации.
- Нормализация: единая event schema, country/channel остаются gate дальнейшего исследования.
- Дедупликация: source+notice ID; conflicting duplicates считаются отдельно. Один OCID с разными notices — намеренно разные события. Cross-source/entity dedup не реализован, возможные дубли TED/FTS **не оценены**.
- Changes: fingerprint минимизированных task fields; baseline/newly observed/changed/unchanged. Изменения полей, которые collector не сохраняет, не обнаруживаются. Исчезновение из ограниченной страницы не трактуется как отмена; removal inference не реализован.
- Classification: четыре класса, простая объяснимая рубрика. Score — ordinal priority, не вероятность сделки. Слабые английские keyword rules служат baseline, а не готовым классификатором.
- Карточки: source URL, событие, гипотеза услуги, evidence gaps, contact gate. Fixture всегда отдельно и неготова к outreach.
- Export: CSV/JSON, state и benchmark; CSV formula prefixes экранируются.

Проверены meaningful invariants: неизменный replay, обнаружение изменения title, дедуп, закрытые/просроченные notices, fixture exclusion, отсутствие contact permission даже при активном спросе. Проверка не доказывает полноту API, юридическую допустимость будущего использования или способность выполнить закупку.

## Следующий честный benchmark

Провести 2 независимых reviewer-сессии по фиксированной новой выборке: сначала manual portal search baseline, затем radar shortlist. Засечь screening и full qualification раздельно; не включать ожидание API в manual time. Зафиксировать scope, eligibility, deadline, route и reason каждого accept/reject. Disagreement разрешать отдельно. По полному labelled sample считать precision; recall требует более полного эталона, его нельзя вывести из shortlist. Считать медиану и p90 времени, стоимость Q и долю route-approved. Назначить заранее лимит работы, например 4 reviewer-hours на cohort; это бюджет эксперимента, не измеренное время одного лида.

Для обнаружения изменений нужны минимум два реальных снимка в разные дни. Сейчас replay и изменённые test fixtures проверяют механику, **но реальная latency и yield изменений не измерены**.
