# 01. Аудит репозитория и ресурсов

**Дата проверки: 2026-11-13 (Europe/Kyiv).** Метки: VERIFIED — первичный документ или воспроизводимый тест; OBSERVED — ограниченная выборка; ESTIMATED — расчёт; ASSUMED — допущение; UNKNOWN — данных недостаточно. HTTP 200 сам по себе не подтверждает API, спрос или право автоматизации.

## Область и ограничения

VERIFIED: исходный HEAD `c6acf4ecbb5ef6cee238ef206a6923b4e9a6288e`, 5 отслеживаемых файлов, 64 достижимых коммита до исследования. Изучены весь Python-модуль и четыре конфигурационных файла. README, тестов, CI, схемы БД и исходников Mac-сервера нет. Источник: локальный Git; команды `git ls-files`, `git log`, `git rev-list`, AST и [сканер](../../research/probes/audit_secrets.py). Удалённые удалённые refs, недостижимые объекты и внешние хостинги не исследованы.

## Что существует и что действительно проверено

| Компонент | OBSERVED/VERIFIED поведение | Решение для будущего |
| --- | --- | --- |
| Freelancehunt reader | `get_full_project`, category polling; список API вернул JSON без ключа в этом запуске | Сохранить mapping как adapter, добавить pagination/cursors и контрактные fixtures |
| Telegram UI | inline generate/edit/send/cancel; library импортируется | Сохранить approval UX; привязать actor/chat к разрешённому owner |
| Groq draft generation | UA/RU prompts, JSON extraction, числовые clamps | Переиспользовать язык/тон как editable templates; заменить schema validation и evidence references |
| Sending | HTTP `/webhook/submit` локальному Mac; кода отправителя нет | Не считать рабочей возможность подачи; проверить официальный API отдельно |
| Flask `/callback` | network-denied smoke доказал HTTP 200; поддельный success меняет счётчик и вызывает mock send | Закрыть auth/signature/replay checks в отдельном security PR |
| Flask Telegram webhook | endpoint path содержит bot token; `secret_token` не проверяется | Секретный header + независимый путь; токен не в логах |
| Memory state | sets/dicts для проектов/ставок/счётчиков | Durable storage; unique constraints; event journal |
| Main entrypoint | monitoring thread запускается только под `__main__` | WSGI-import не запускает мониторинг; отдельный scheduler/worker |

[repository_smoke_results](../../data/repository_smoke_results.json): импорт с synthetic credentials, внешний HTTP запрещён mock-барьером. Проверка **не** доказывает доставку Telegram, Groq generation или Mac bidding. Предыдущий onboarding HTTP-smoke подтверждал лишь локальный WSGI сервер.

## Ограничения логики

VERIFIED по коду: 44 category entries, 43 уникальных; дублированная категория. При идеальном периоде 300 s: `44 × 288 = 12 672` list requests/day плюс startup и details, без пагинации. Реальный период длиннее из-за сетевых задержек. Отсутствует чтение следующих страниц: пропускаются проекты при активном потоке. Нет backoff/Retry-After, rate-budget, connection reuse через Session, incremental watermark или freshness SLA.

Проект отмечается seen **до** успешной доставки: ошибка Telegram может потерять уведомление. При перезапуске инициализация считает существующие проекты просмотренными; состояние теряется. `sent_bids_today` не имеет ежедневного reset в модуле; counters для отчётов не являются подтверждённым бухгалтерским журналом. Ставка помечается как отправленная при HTTP 200 от Mac до подтверждения фактической публикации. Несколько WSGI workers имеют разные dict/set; нет межпроцессной консистентности. Долгие synchronous Groq/API вызовы блокируют обработчик; race conditions и retry effects не контролируются.

AI confidence — число из ответа модели, **не** калиброванная вероятность выиграть контракт. Regex JSON и clamps не валидируют типы/порядок min≤max/содержательность. На редактировании используется последний pending project для любого входящего сообщения, без owner/tenant контекста. HTML-строки из внешних данных не экранируются. Цена ограничивается 27 000 грн независимо от фактической оценки; это не проверенная рыночная ценовая модель.

## Официальная подача ставки и зависимость от Mac

VERIFIED по опубликованной [Freelancehunt Postman collection](https://apidocs.freelancehunt.com/api/collections/3971751/S1Lzy7WU?segregateAuth=true&versionTag=latest), дата выше, confidence high **для существования документации**: присутствует `Add bid`, `POST /v2/projects/{project_id}/bids`. Есть list/revoke/restore endpoints. [priority_followup.json](../../data/priority_followup.json) хранит только имена/методы/templates, без account examples или токенов.

UNKNOWN: разрешение конкретного аккаунта, тарифные/платформенные условия подачи, актуальность всех параметров, успешный ответ записи. Никаких POST bids не выполнялось. Вывод: Mac/browser automation **не является доказанной необходимостью**; официальный API — кандидат после owner authorization и проверки условий. Текущий код отправки от Mac полностью зависит; мониторинг/черновики могут работать независимо. Mac health и submit endpoints не имеют auth в вызывающем коде; безопасность отсутствующего сервера UNKNOWN.

## Зависимости и совместимость

VERIFIED: `requirements.txt` содержит telebot, Flask/Gunicorn, requests, dotenv, Groq/httpx, pytz. `pyproject.toml` описывает другой стек aiogram/aiohttp и Python 3.11; `runtime.txt` — Python 3.13.4. `poetry.lock` содержит shell-команды, а не lockfile. На Python 3.13.4 requirements установились, WSGI импорт работает. Транзитивные версии приложения не зафиксированы.

Кандидаты устранения **без изменения в этом PR**: неиспользуемые aiogram/aiohttp декларации; browser/Mac/ngrok после проверки bid API; постоянный Flask-процесс при переходе на scheduled read-only adapter; `pytz` можно заменить stdlib zoneinfo отдельным совместимым изменением. Flask нужен для существующего webhook; Groq — только при генерации. Не объявлять зависимости лишними до тестов поведения.

## Секреты, история, данные

VERIFIED: в текущем коде есть непустые default literals для Telegram и Freelancehunt credentials, а также идентификатор чата и deployment URL. История содержит credential-shaped значения. Ни один literal не включён в исследовательские файлы. Сканер прошёл 64 коммита и 64 уникальных пар blob/path; 87 finding rows — **не число уникальных секретов**. Категории: {'telegram_token_shape': 46, 'credential_literal': 41}. [security_audit.json](../../data/security_audit.json) хранит paths, commit IDs, rules и counts, без строк исходника или value fingerprints. Это эвристика; отсутствие совпадения не доказывает отсутствие секретов.

Высокоприоритетное действие владельца: считать опубликованные credentials скомпрометированными, самостоятельно отозвать/заменить их в соответствующих сервисах; затем убрать fallback literals и провести отдельное согласованное решение об истории. В этом исследовании они не использовались, не отзывались, не заменялись; Git history не переписывалась. Удалить строку только из HEAD недостаточно. Лог `setup_webhook` включает token-bearing URL; будущий access logging должен редактировать paths/headers.

Хранение сейчас process-local; нет retention policy, tenant boundary, encryption model, backup/restore и удаления. Данные заказов/feedback передаются Groq без описанного privacy режима. Не сохранять контактные поля в новом исследовательском датасете; факты и AI-гипотезы должны иметь разные поля и provenance. Источники юридических ограничений — [09](09_COMPLIANCE_AND_RISKS.md).

## Бесплатный перенос: только вывод исследования

Мониторинг должен стать короткими idempotent batches со state/cursor и отдельным outbox, а не бесконечным thread внутри WSGI. Первые кандидаты — Supabase Cron/Edge или Cloudflare Cron; Netlify — опциональный frontend. GitHub Actions годится для CI; использовать его как постоянный коммерческий backend без отдельной проверки ToS нельзя. Детали, квоты и непроверенные cloud parts — [08](08_TECHNICAL_FEASIBILITY.md). Никакой перенос в этом PR не выполнен.
