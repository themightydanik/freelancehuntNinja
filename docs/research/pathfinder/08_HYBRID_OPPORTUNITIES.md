# Пять гибридных возможностей

Два канала дополняют друг друга только если используют один проверенный результат и одну матрицу совместимости. Ниже показана техническая логика возможного дополнения; фактическая экономия поддержки и готовность купить по двум каналам не доказаны. Ни один hybrid не получил статус validated.

| Гибрид | Один продукт / два способа оплаты | Почему могут дополняться | Что может удвоить расходы / критерий отказа |
|---|---|---|---|
| H01 Export Acceptance Kit | Self-service import двух файлов + assisted agency acceptance | Один normalization/contract/report engine; ручной pilot создаёт разрешённые synthetic fixtures для self-service | Два разных формата/гарантии потребуют отдельных adapters; не строить три оболочки; kill если нет повторного agency заказа |
| H02 Woo definitions checker | Бесплатный диагностический report + платная агентская лицензия на повторные согласованные rules | Free report демонстрирует конкретное расхождение; лицензия повторяет те же правила для нескольких клиентских файлов | Free support может превысить оплату; если это обычная настройка exporter, REJECT весь платный слой |
| H03 Shipping fixture kit | Woo read-only tester для merchant + agency scenario library | Одинаковая схема входа и expected outputs; агентство повторно применяет fixtures | Carrier API, themes и checkout engines резко расширяют матрицу; не интегрировать live carriers до оплаты |
| H04 Release evidence | Browser/CLI проверка согласованных redirects + лицензия агентству на отчёт | Один URL-manifest diff и formatter; специалист проверяет, агентство передаёт результат клиенту | Checkbot уже делает отчёты; extension permissions не нужны для file-only mode; kill если бесплатный tool выдаёт тот же output |
| H05 One-template inspection pack | Мобильный local capture + B2B template/export license | Одна offline schema, проверяемый export; B2B оплачивает конкретный шаблон вместо второго backend | Enterprise sync, media audit и права сотрудников превращают продукт в платформу; kill если нужен full SafetyCulture clone |

Источники: G01/G05/G10, X12, M10 и их alternatives в [реестре](data/evidence_registry.csv). Предлагаемые цены не являются тарифами этих источников.

Правило отсутствия двойного счёта: если агентская лицензия покрывает сайты его клиентов, те же sites не считаются retail licenses в модели. [Hybrid calculation](data/financial_thresholds.csv) использует **раздельные группы**: $149/месяц agency + $49/год retail, условно 50/50 gross. Это сценарий, не доказанный оптимальный пакет. При $2 000 target получается 7 агентств + 245 разных retail licenses, а не семь агентств со своими же 245 сайтами, посчитанными второй раз.

Граница расширения: один adapter, одинаковая privacy policy по сути данных, один release train и один формат acceptance. Разработка новой mobile sync системы одновременно с WP plugin не соответствует этому правилу. Из пяти комбинаций сначала проверить только H01 как услугу; recurring license и marketplace wrapper открываются после повторных оплат и измеренного снижения часов.
