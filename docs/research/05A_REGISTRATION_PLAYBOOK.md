# 05A. Playbook регистрации и первых измерений

**Дата проверки: 2026-11-13 (Europe/Kyiv).** Метки: VERIFIED — первичный документ или воспроизводимый тест; OBSERVED — ограниченная выборка; ESTIMATED — расчёт; ASSUMED — допущение; UNKNOWN — данных недостаточно. HTTP 200 сам по себе не подтверждает API, спрос или право автоматизации.

**Только инструкции для будущего owner-approved этапа. Ни одна регистрация или публикация этим исследованием не выполнена.** Не вводить credentials в чат; банковские/ID данные — только в официальном защищённом кабинете. Формальная проверка страны до подготовки app-store продукта экономит недели.

## Общий порядок

1. Выбрать P01 или P04 и максимум два канала из [05](05_DISTRIBUTION_CHANNELS.md). Owner указывает фактическую территорию проживания/налоговый статус и допустимую форму контракта. Не просить документ/номер в research repo.
2. Открыть официальный current eligibility/fees/payout help. Проверить country **residence**, sanctioned territories, bank currency, withdrawal threshold, hold period, refund/chargeback liability, payout fee, currency conversion и необходимость компании. Если ответ неоднозначен — support question вручную, не фиктивный адрес/резидентство.
3. Зафиксировать в приватном checklist лишь `verified/not verified/date/source`, без паспортов, счетов и ключей. Публичный CSV обновлять только safe eligibility outcome.
4. Создать профиль вручную после разрешения. Проверить уникальность существующего аккаунта. Настроить MFA, роли, owner-controlled recovery. Portfolio synthetic: прямо обозначить demo; никакого выдуманного client proof.
5. Проверить listing rules: fixed scope, support window, revisions, prohibited claims, off-platform communication, IP/license and AI disclosure. Опубликовать один согласованный offer; в research PR публикации нет.
6. Configure UTM source и minimal inquiry form/privacy notice; processing purpose и retention. Не отправлять реальные заявки в production form для теста: synthetic staging only.
7. Две недели измерять; не считать profile creation или search indexing равнозначными traffic. По всем комиссиям сохранить calculation example и actual owner-reviewed current rate.

## Сценарии по типу канала

| Тип | Каналы | Материалы | Регистрационный gate | First exposure experiment (ASSUMED) |
| --- | --- | --- | --- | --- |
| Buyer marketplace | D01–D07 | Headline, 90s demo, scope, FAQ, $ price range | KYC/payout, bid fees, off-platform rules | Один listing и разрешённые ручные ответы только после owner approval |
| Vetted talent | D08–D11 | Реальный опыт, assessment, portfolio | Country/admission, interviews, time commitment | Не первым шагом при <2 кейсов; budget max 8h до ясного eligibility |
| Agency directories | D12–D14 | Agency identity, real cases, consented reviews | Company requirement/free tier vs promotion | Один профиль после двух кейсов; 30d tracked views |
| Ecosystem partner | D15–D18 | Два внедрения, docs, support process | Partner acceptance/certification/license | Manual qualification; directory acceptance ≠ referral |
| Packages/templates | D19,D23,D24,D35 | Tested code, license, docs, disclosure | Package policy/security, license | Один minimal reusable primitive; useful docs; no unsolicited issue promotion |
| App/plugin stores | D20–D22,D28 | Working product, readme, privacy, support/version policy | Review; rights; payouts if paid; permissions | Только после confirmed workflow/payer; review delay UNKNOWN |
| Checkout/MoR | D25–D27 | Approved digital product, refund/support/privacy policy | Ukraine payout + business approval + tax | No discovery assumption; bring already measured own traffic |
| Content/launch | D29–D34 | Original tutorial/demo and opt-in CTA | Community/category rules and account eligibility | One permitted useful contribution; measure clicks, not likes |
| Country network | D36 | Residence/legal status and service portfolio | Supported country unresolved | Stop until eligibility clarified |

## Минимальный asset pack

Title: «Recover one Python Telegram bot in an isolated rehearsal»; deliverables: inventory of **variable names**, restart/runbook, synthetic regression checks, backup/restore rehearsal; exclusions: no unknown browser bidding, no production secret extraction, no guarantee beyond scoped RTO. 1 diagram, 1 demo video, 1 executable fixture, 1 acceptance page. Price $350 — ASSUMED test, not verified willingness to pay. For P04 use one signed webhook and duplicate/replay proof.

Отдельно указать, что pre-sales triage не production audit. Free demo не означает free unbounded consulting. Депозит/escrow, refund terms, tax и договор — только владельцем после platform/legal checks.

## Decision rules

Предлагаемые пороги (ASSUMED experiment design, не benchmarks): 100 targeted visits с 0 qualified inquiries → сменить positioning/segment; 5 qualified discussions и 0 accepted paid scope → проверить trust/price/problem; 2 paid pilots ≤14h delivery → повторить тот же пакет; >2h support/client/month → урезать scope/поднять цену до масштабирования. При слишком малом трафике нельзя обвинять продукт: сначала distribution test. Для 0/100 naive независимых trials 95% upper bound conversion около 3%; independence/intent quality в практике не гарантированы.
