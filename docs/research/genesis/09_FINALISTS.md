# Финалисты: 1 для проверки, 0 для разработки

**C01 — independent Shopify migration acceptance. Gate HOLD / EXPERIMENT_ONLY.** Buyer: небольшая ecommerce agency с повторными миграциями или merchant перед конкретным launch. Наш narrow scope: два consented CSV/JSON exports, до 5 000 product variants и 50 000 order rows, одна currency за run, согласованные keys/statuses/totals, список расхождений с воспроизводимыми identifiers. Эти лимиты ASSUMED и проверяются пилотом. Не включать live writes, весь SEO, налоговую корректность, гарантии продаж, миграцию секретов и checkout certification.

Почему выбран для test: buyer budget $400 [E04], смежные buyer requests [E05/E06], существующие платные tools и reported payments [E01/E02], возможность bounded offline результата. Почему не build: наш принятый scope/price, first organic exposure, acquisition cost, recurring agency usage и UA cash path UNKNOWN. Цена $100 diagnostic/$400 full — экспериментальные предложения, не market rate. Три related independent signals существуют, три оплаты **этого** narrow продукта не найдены.

### Buyer-to-Cash Map

`Agency/merchant →[OBSERVED E04–06] migration audit problem →[OBSERVED E02/E04; разные scopes] existing tool spend / audit budget →[ASSUMED; policy VERIFIED E45] discovers our listing →[UNKNOWN] submits qualified exports + scope →[UNKNOWN; payout gate] pays accepted price →[ASSUMED; offline subset VERIFIED] receives accepted reconciliation pack →[UNKNOWN] buys next migration / agency license`

Критические разрывы: discover→qualified action, action→accepted price→cash и repeat. Наличие этих разрывов запрещает рекомендацию полноценной разработки. VERIFIED offline subset: demo проверяет synthetic keys, duplicate IDs, variant quantities и monetary totals с Decimal; оно не доказывает production Shopify/CS-Cart mappings.

### Кандидаты вне финала

C02 WordPress restore proof: интересна recurring agency модель, но E14–16 подтверждают one-off recovery, не subscription. Gate UNVALIDATED. C03 MSP change control: есть requirement/free/paid ecosystem, но наш channel и paid gap не доказаны. Gate UNVALIDATED. C04–06 ещё слабее в доступе/компетенции/свидетельствах, поэтому не расходуем деньги на их прототипы. Все шесть глубоких карточек — [04](04_EXISTING_SPENDING_EVIDENCE.md), [06](06_COMPETITIVE_ALTERNATIVES.md), [scorecard](data/finalist_scorecard.csv).

Взвешенный балл — порядок исследовательских тестов по весам 20/25/15/15/10/10/5, не вероятность успеха. Ни один score не преодолевает hard gate. Числа subjective 0–5; основания и главный риск доступны в scorecard; без подтверждённого канала оценка distribution ≤2.

**Экономический hard gate C01:** базовая самостоятельная услуга $400/10h при 5 продажах — REJECT как бизнес при owner rate $25/h. HOLD относится только к проверке изменённого предложения, а не к обходу gate. При тех же 5 продажах break-even price ≈$423.78 или total client labor ≤9.23h при цене $400 (sales/admin16h отдельно); запас прибыли нужен сверх нулевой границы. Эти пороги не доказывают принятие более высокой цены или меньшие часы. Если пилот не покажет положительный экономический результат, кандидат исключается.

C04/C05/C06 также не проходят baseline economic gate при заложенной цене/нагрузке: их варианты услуг REJECT в текущем виде. Исследовательский HOLD допускает возвращение только с новой принятой ценой, меньшей измеренной трудоёмкостью и buyer evidence. Поле `baseline_economics_gate` отделено от статуса дальнейшего исследования в scorecard.
