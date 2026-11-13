# 06A. Отбор 10 → 3

**Дата проверки: 2026-11-13 (Europe/Kyiv).** Метки: VERIFIED — первичный документ или воспроизводимый тест; OBSERVED — ограниченная выборка; ESTIMATED — расчёт; ASSUMED — допущение; UNKNOWN — данных недостаточно. HTTP 200 сам по себе не подтверждает API, спрос или право автоматизации.

Не используем arbitrary weighted score. Порядок: (1) concrete evidence proximity, (2) absence of blockers, (3) ≤14h rollout и обратимость, (4) reuse с текущим первым пакетом, (5) channel/payment gate. Это **порядок экспериментов**, не вероятность успеха.

| Порядок | Оффер | Почему в short-list | Обязательный gate |
| --- | --- | --- | --- |
| 1 | P01 | Самый близкий к существующему опыту и sampled bot requests; 8h rollout. Бюджеты UAH не подтверждают $350. | Один scoped paid recovery pilot; measured restore; no secret disclosure. |
| 2 | P04 | Повторяемый primitive для нескольких офферов; webhook issues подтверждают проблему, не оплату. | Один client-approved duplicate/lost event case, paid acceptance и handover. |
| 3 | P02 | Понятный business event и WP ecosystem; бесплатные plugins могут полностью закрыть кейс. | Сначала existing-tool comparison, затем $500 price acceptance и ≤12h delivery. |
| 4 | P10 | Дешёвый bounded вариант P01; основание — audit, внешний buyer спрос UNKNOWN. | Не продавать WSGI import как работающий monitoring; проверить actual workflow. |
| 5 | P23 | Реальные n8n Telegram issues; service лучше ещё одного orchestrator. | Проверить license/owner workflow; credential-free fixture + paid recovery. |
| 6 | P09 | Найден integration request; высокий overlap с P02/P04. | Сузить до одного CRM/API и lawful minimal notification. |
| 7 | P22 | Может увеличить чек и repeat use без новой платформы; agency demand не подтверждён. | Trusted introduction или inbound; scope/NDA/IP; 2 paid sprints. |
| 8 | P03 | Высокий возможный вклад на час, но qualification gate сильнее математики. | Экспертный review и tenant-negative tests; не full security audit; optimizer excludes by default. |
| 9 | P05 | Reusable by-product P01; template acquisition не доказан. | Не отдельный большой build; публиковать только после service proof и payout gate. |
| 10 | P06 | API feed/cursor проверен; готовность agencies платить UNKNOWN, supplier quality не подтверждена. | 10 awarded notices quality test + 5 opt-in users; лишь потом subscription pilot. |

## Первые три кандидата

**P01 Bot Recovery**: первый synthetic demo и fixed-scope offer. Сохранять secret names, не values; staging restore; один deployment path. Price test $250–450, основная модель $350. ≤12h reusable base; delivery ≤8–10h; support ≤1h/month. Самый быстрый кандидат не означает доказанный международный спрос.

**P04 Webhook Replay**: второй, только если первый канал привёл integration demand. Paid primitive: подписанные события, stable event ID, durable delivery states, replay approval, failure dashboard/report. Do not promise exactly-once external side effects. $400–700 price test; model $600; 14h rollout. Common primitive для P02/P09/P23.

**P02 WooCommerce order notification**: третий, **условный**: сначала Make/plugin substitution test. Если existing plugin достаточно, предлагать настройку/восстановление с прозрачной лицензией, а не свой plugin. $350–650 price test; model $500; rollout ≤12h. Reuse P04 только после реальной идентичности workflow.

Для всех: критерий перехода к продукту — минимум 2 похожих paid pilots и измеренная поддержка, а не clicks/likes. P03 математически привлекателен, но не должен попасть в первый портфель без подтверждённой компетенции и ответственности. P08 grants, P18 registry SaaS и P17 browser extension отложены из-за длинного цикла, доступа, review и неподтверждённой дистрибуции.
