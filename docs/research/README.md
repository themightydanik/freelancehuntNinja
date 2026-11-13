# Ninja 2.0 — исследовательский Draft PR

**Дата проверки: 2026-11-13 (Europe/Kyiv).** Метки: VERIFIED — первичный документ или воспроизводимый тест; OBSERVED — ограниченная выборка; ESTIMATED — расчёт; ASSUMED — допущение; UNKNOWN — данных недостаточно. HTTP 200 сам по себе не подтверждает API, спрос или право автоматизации.

Это пакет для принятия решения, а не реализация нового сервиса. Начните с [Executive report](00_EXECUTIVE_DECISION_REPORT.md). Исходный бот и его зависимости не изменены. Реальных сообщений, заявок, регистраций, покупок и развёртываний не выполнялось. Публикация среды также не выполнялась.

## Навигация

| Этап | Материал | Проверяемая основа |
| --- | --- | --- |
| Аудит | [01](01_REPOSITORY_AUDIT.md) | static review, Git history, network-denied smoke |
| Данные | [02](02_DATA_SOURCES.md) | 30 источников, 32 начальных запроса, дополнительные проверки |
| Стратегии | [03](03_OPPORTUNITY_RESEARCH.md) | объявления и issues; ни одной подтверждённой оплаты |
| Альтернативы | [04](04_COMPETITOR_LANDSCAPE.md) | 38 продуктов/услуг, первичные страницы, ограничения извлечения |
| Дистрибуция | [05](05_DISTRIBUTION_CHANNELS.md), [05A](05A_REGISTRATION_PLAYBOOK.md) | 36 каналов-кандидатов; KYC/payout не проверены регистрацией |
| Продукты | [06](06_PRODUCT_CATALOG.md), [06A](06A_TOP_10_PRODUCTS.md) | 30 офферов с явными допущениями |
| Экономика | [07](07_REVENUE_MODEL.md) | seed 20261113, 5000 траекторий на сценарий |
| Технология | [08](08_TECHNICAL_FEASIBILITY.md) | API probes, local state POC; облачный runtime не развёрнут |
| Риски | [09](09_COMPLIANCE_AND_RISKS.md) | законы/политики; не юридическое заключение |
| Портфель | [10](10_PORTFOLIO_STRATEGY.md) | integer enumeration + зависимости |
| Решение | [11](11_FINAL_RECOMMENDATION.md), [12](12_IMPLEMENTATION_ROADMAP.md), [13](13_PR_PLAN.md) | коммерческие и технические gates |

## Воспроизведение

```bash
cd /workspace/freelancehuntNinja
UV_CACHE_DIR=/workspace/.cache/uv uv venv --python /workspace/.venvs/freelancehuntNinja/bin/python /workspace/.venvs/ninja-research
UV_CACHE_DIR=/workspace/.cache/uv uv pip sync --python /workspace/.venvs/ninja-research/bin/python research/requirements.lock.txt
PYTHONDONTWRITEBYTECODE=1 /workspace/.venvs/ninja-research/bin/python -m unittest discover -s research/tests -v
/workspace/.venvs/ninja-research/bin/python research/models/revenue_model.py --runs 5000 --seed 20261113
/workspace/.venvs/ninja-research/bin/python research/models/portfolio_optimizer.py
/workspace/.venvs/ninja-research/bin/python research/probes/state_poc.py
PYTHONDONTWRITEBYTECODE=1 /workspace/.venvs/freelancehuntNinja/bin/python research/probes/repository_smoke.py
python research/probes/audit_secrets.py
# Следующие команды выполняют ограниченные публичные HTTP-чтения и обновляют evidence timestamp:
/workspace/.venvs/ninja-research/bin/python research/probes/http_probe.py
/workspace/.venvs/ninja-research/bin/python research/probes/priority_followup.py
/workspace/.venvs/ninja-research/bin/python research/probes/policy_pages.py
/workspace/.venvs/ninja-research/bin/python research/probes/pagination_quality.py
/workspace/.venvs/ninja-research/bin/python research/probes/verify_issue_reviews.py
python research/probes/verify_artifacts.py
```

Если опубликованное окружение не содержит app venv, создайте его вне checkout и установите неизменённый `requirements.txt`. Для smoke нужны app packages; математическая модель изолирована. Не запускайте `freelancehuntNinja.py` как main: он регистрирует webhook и отправляет сообщения. Все тестовые credentials явно синтетические.

Результаты запросов меняются; seed фиксирует модель только при неизменных версиях кода/NumPy. Полные версии — [research/requirements.lock.txt](../../research/requirements.lock.txt), среда — [run_manifest](../../data/run_manifest.json). Модель не зависит от live API. API-пробы не читают credentials из кода. Некоторые страницы неполные/динамические/блокируются; ошибки сохранены, обхода нет.

## Граница завершённости

Созданы все запрошенные категории артефактов. Не завершены и не имитировались: proof of payment demand, проверка украинских выплат через KYC, закрытые API, юридическое заключение, cloud deployment reliability и новая production архитектура. Поэтому это воспроизводимый **decision checkpoint**, а не доказательство готовой бизнес-модели. Уровень уверенности рекомендации о первом эксперименте — medium; прогноз продаж — low.
