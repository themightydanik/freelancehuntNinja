# 17. Security remediation plan — выполнять владельцем в отдельном change

**Дата проверки: 13 ноября 2026, Europe/Kyiv.** VERIFIED — первичный документ/воспроизводимый тест; OBSERVED — ограниченная выборка; ESTIMATED — расчёт; ASSUMED — допущение; UNKNOWN — недостаточно данных. Никаких продаж, публикаций офферов, регистраций, платежей, rotation или production changes не выполнялось.

**Это план, не выполненная rotation/remediation.** Работающий бот, его default literals и история не изменены этим PR. Токены не проверялись на валидность и не использовались. Владелец должен считать опубликованные реальные credential values скомпрометированными независимо от их текущей активности. Ротация нужна для собственных подтверждённых аккаунтов; чужие учётные данные не отзывать.

Основа: [01 аудит](01_REPOSITORY_AUDIT.md), [history scan metadata](../../data/security_audit.json), [network-denied mock smoke](../../data/repository_smoke_results.json). Источник — [freelancehuntNinja.py](../../freelancehuntNinja.py), без цитирования значений. Высокий риск credential exposure и callback authorization остаётся открытым; synthetic demo не закрывает его.

## 0. Подготовка без раскрытия секретов

Owner подтверждает доступ к BotFather/Telegram bot account, Freelancehunt API settings и фактическому production hosting; определяет все consumers и ответственного. Записывает только aliases, version/commit, имена переменных, presence/status и время — **не значения**, headers, полный token-bearing URL, dumps.env или screenshotsссекретами. Проверить реальные опубликованные deployment/CI logs и сохранённые cloud snapshots по согласованной процедуре; не копировать их сюда.

Имена существующих inputs: `TELEGRAM_BOT_TOKEN`, `FREELANCEHUNT_TOKEN`, optional`GROQ_API_KEY`; `CHAT_ID`, `RAILWAY_URL`, `MAC_SERVER_URL` — тоже чувствительный context, но не все являются credential secrets. Новый receiver может потребовать отдельные `TELEGRAM_WEBHOOK_SECRET` и `MAC_CALLBACK_SIGNING_KEY`; они **не созданы и не сохранены** этим research. Проверка environment status не устанавливает доступ к production accounts.

Подготовить **offline** patch/безопасную rollback версию без embedded tokens и token-bearing logs. Она не применена здесь. Если есть подозрение активного использования утекших credentials, owner немедленно останавливает affected consumers и отзывает credentials; не ждать большой архитектурной миграции. Допустим согласованный downtime. Без права/доступа к аккаунту — остановиться и обратиться к его владельцу, не пробовать найденные tokens.

## 1. Остановить опасные действия и закрыть старые входы

В отдельное согласованное maintenance window остановить **все** экземпляры watcher/bot/bid sender, scheduled jobs и старые workers. Поставить outgoing/bidding на pause. Не дать двум deployments одновременно менять webhook. Временно закрыть доступ к старому unauthenticated callback через authenticated reverse proxy/firewall или остановленный service; не принимать unsigned events «для совместимости».

Pending approvals/delivery states сохранить только разрешённым owner способом, минимально и вне Git; исходный bot держит их вRAM, поэтому без специального export точное восстановление не гарантируется. Нельзя считать HTTP200отMac доказательством поданной ставки. Согласовать, что делать с неопределённым статусом внешнего эффекта — manual reconciliation, а не автоматический повтор коммерческой заявки.

## 2. Владелец отзывает старые credentials

1. **Telegram:** владелец нужного бота через официальный BotFather отзывает опубликованный token и получает новый. Исследователь не отправляет команды и не получает значение.
2. **Freelancehunt:** владелец определяет именно опубликованный API credential/app в собственных settings, отзывает его и создаёт минимально необходимую замену. Не использовать token изGit для проверки, какой это аккаунт.
3. **Groq/прочие сервисы:** ротировать только credentials, для которых установлена exposure/небезопасная копия; наличие имениGROQ_API_KEYне доказывает утечку реального Groqkey. Пересмотреть access/usage по secure owner console.
4. При необходимости отдельно сменить webhook/callback signing secrets. Они не должны совпадать с bot/API tokens. Вести журнал `revoked/replaced/consumer updated`, без fingerprints или значений.

Revocation нельзя «откатить» возвратом к старому token. **Rollback кода должен использовать новые безопасные bindings**, а при их неисправности service остаётся fail-closed/stopped. Удаление строки изHEADили закрытие PR не заменяет отзыв.

## 3. Обновить environment bindings и удалить секреты из кода

Новые values вводятся owner только в secure settings/vault фактического hosting/CI. Не передавать в чат/PR, аргументы shell с tracing, public build output, repository files или frontend bundle. `VITE_*`/`REACT_APP_*` переменные не подходят для server tokens. `.env` с real credentials не коммитить; локальный файл только если разрешён, вне checkout/вignored path с ограниченными правами.

В **будущем security PR**, не здесь:

- Убрать непустые credential fallback literals в declarations `API_TOKEN`, `FREELANCEHUNT_TOKEN` и других найденных credentials. Required variables валидировать до создания clients; отсутствие — понятная ошибка без значений и остановка.
- Убрать token из webhook URL и `setup_webhook` logging; redact request headers/URL/errors. Исключить token-bearing route из access logs ещё до запуска новой конфигурации.
- Проверить всех consumers/старые images, localMac/ngrok, CI variables, deployment logs и версии; не оставить старый процесс с embedded fallback. Исключить зашитые customer/chat identifiers из reusable demos.
- Подготовить valid.exampleс**явными** placeholders и required names; тесты на отсутствие env должны failclosed. Source manifests/lockfiles и unrelated code не менять попутно.

Обновить bindings можно до source deploy, но **не запускать старую версию** с новыми values: текущий `setup_webhook` печатает token-bearing URL. Сначала secure release/tests, затем controlled start.

## 4. Защитить Telegram webhook

Будущий route: `/telegram/webhook/<independent-route-id>`; route-id не bot token и не единственная защита. `setWebhook` должен получить отдельный random `secret_token`; receiver до business logic проверяет `X-Telegram-Bot-Api-Secret-Token` constant-time comparison, TLS, допустимый метод, content-type и body-size/schema. Прямой legacy token route закрыт. IP allowlisting — дополнительный контроль, не замена secret header.

Разделить transport authentication и **авторизацию пользователя**: разрешённые `from_user.id` и `chat.id`, project/approval owner, версия draft и action scope. Чужой пользователь даже внутри известной group не получает права на quote, edit, Groq spend или bid submission. Экранировать внешние HTML-поля. Replays/update IDs должны быть durable и scoped, не process-local sets.

Owner controlled registration новой URL после обновления receiver: явно согласованный `allowed_updates` (как минимум используемые message/callback_query), проверка единственного webhook на нужном bot. Для `drop_pending_updates` нужно отдельное решение: quarantine/reconcile или осознанное удаление, без молчаливой потери pending actions. `getWebhookInfo`/живой synthetic update допустимы только в отдельном approved live check, ответы/logs редактируются. Здесь они не выполнялись.

## 5. Защитить callback и канал Mac/worker

Выделенный signing key, HTTPS, HMAC-SHA256над **неизменёнными raw bytes** + timestamp +nonce/event ID; ограниченное окно например 5 min(ASSUMEDconfiguration), constant-time check, durable replay protection, max-body size и schema/status allowlist. Ключ не bot token; auditlog не содержит signature/secret/rawcustomer payload. Для разных producers — разные scopes/keys.

Producer и receiver выпускаются согласованно: подпись нельзя включить только на одной стороне и затем вернуть unsigned fallback. Исходников Macserverв репозитории нет — эта часть зависимости ещё требует владельца/исходников; не обещать end-to-end security без проверки producer. Пока sender не готов, callback остаётся закрытым/paused.

Counter/state меняются только после authentication+authorization+schema+idempotency. Повтор уже обработанного event не создаёт второе notification/increment. Не считать client-provided`status=success`доказательством actual external bid без корреляции job ID/reconciliation. HTTP200иexactly-onceвнешнего эффекта различаются; для неизвестного статуса нужна ручная проверка до replay. Если официальный FreelancehuntbidAPIзаменитMac, это отдельный functional/compliance change, не часть этой rotation.

## 6. Проверить безопасный release и вернуть работу

До запуска — offline/synthetic negative tests с network denied. После secure settings и owner authorization — ограниченный live synthetic check без коммерческого действия; secret values и token URLs не публикуются. Возобновлять watcher отдельно от bidding; monitoring success не разрешает auto-send.

| Проверка будущего security PR | Ожидаемое поведение |
| --- | --- |
| Required token отсутствует | Failclosed до client/startup, без fallback и secret logs |
| Webhook header отсутствует/неверный | Reject до обработки и AI/APIspend |
| Header верный,actor/chat не разрешён | Reject privileged action; нет edit/generate/send |
| Signed callback испорчен/устарел | Reject; counters/outbox не меняются |
| Replay того же event | Один durable effect; возвращается согласованный идемпотентный результат |
| Другой ресурс с совпавшим transport ID | Нет потери легитимного события: source contract/semantic identity tested |
| Crash перед/после commit | Durable state+checkpoint/outbox согласованы; no blind external resend |
| Code rollback | Новые bindings сохраняются; старые revoked values не возвращаются |
| Реальный owner-controlled smoke | Синтетический сценарий доставлен один раз, logs redacted; не коммерческая ставка |

Текущие research tests подтверждают **модель/демо**, а не выполнение этой таблицы на production bot. Не отмечать checklistpassedпо наличию планового текста.

## 7. Предотвратить повторное появление и решить судьбу истории

- Pre-commit иCI secret scanning с pin/checksum-verified инструментом; scan staged/new commits плюс согласованный history audit. Narrow allowlist только на конкретные synthetic fixtures, не глобальное отключение token rules. Не печатать matching lines/values.
- `.gitignore` local secrets, safe examples, code review на secret defaults/token URLs, минимальные роли/права, разделение environments и логов. Branch protection/review и checks зависят от owner account/plan, не объявлены включёнными.
- История/forks/PRdiffs/releases/log artifacts и опубликованные environment snapshots могут сохранять старый material. **После rotation** owner отдельно принимает решение об очистке истории и координации clones/refs. Никаких `filter-repo`, forcepush, удаления чужих refs или повторной публикации среды этим research.
- Даже после history rewrite старые копии могут существовать; безопасность обеспечивает revocation, не обещание полного удаления из интернета. В опубликованной среде не возобновлять старый небезопасный runtime. Обновление reusable snapshot — отдельное явно разрешённое действие, не повтор предыдущего onboarding.

## Gate владельца

| Подтверждено | Неизвестно | Проверка/стоимость(A) | Положительный результат | Отрицательный результат |
| --- | --- | --- | --- | --- |
| Credential literals/history и unsigned callback risks обнаружены | Активны ли старые keys и где их consumers? | Owner secure inventory/usage,0.5–1 h; без проб чужих keys | Stop/revoke/secure bindings | Нет ownership/access→обращение к владельцу, serviceне запускать |
| Offlineдемо исправляет один synthetic filter failure | Реальный productionrootcause/совместимость sender | Separate security implementation+negative tests,ASSUMED4–12 hбез unavailableMacwork | Owner-controlled staged restart | Оставить paused/failclosed; не вернуть insecurefallback |
| Research не менял source/credentials | Можно ли безопасно запускать коммерческий pilot? | Reviewactualremediation+KYC/payout+permissions, не только документов | Один limited pilot по[15](15_FIRST_500_REVENUE_EXPERIMENTS.md) | Сначала закрыть blocker; никаких сообщений/публикаций |
