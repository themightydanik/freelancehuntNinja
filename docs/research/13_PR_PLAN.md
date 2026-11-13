# 13. Последовательность будущих PR

**Дата проверки: 2026-11-13 (Europe/Kyiv).** Метки: VERIFIED — первичный документ или воспроизводимый тест; OBSERVED — ограниченная выборка; ESTIMATED — расчёт; ASSUMED — допущение; UNKNOWN — данных недостаточно. HTTP 200 сам по себе не подтверждает API, спрос или право автоматизации.

Ни один production/коммерческий PR ниже не реализован этим research. Цепочка не обязательна целиком: no-go gate останавливает downstream work. Merge текущего Draft PR не означает разрешение на outreach, cloud deployment, paid API, публикации или применение этих plans.

## PR01. Убрать небезопасные defaults и закрыть callbacks

- Точный scope: Owner-managed credential rotation вне Git; env presence fail-closed, token redaction, signed callback+actor ACL; no history rewrite automatically.
- Зависимости: Owner security decision; staging access.
- Ожидаемый результат: Убрать небезопасные defaults и закрыть callbacks, в границах указанного scope; нет обещания продаж.
- Acceptance: Неподписанные/mismatched actor requests rejected; no credential values in logs; existing authorized callback works.
- Сложность: ESTIMATED medium; уточнить после scope/access. Ни одна оценка не включает unknown platform review wait.
- Проверяемая гипотеза: Safe live bot changes achievable before commercial validation.

## PR02. P01 synthetic recovery demonstrator

- Точный scope: Isolated fixture app, reproducible backup/restore/restart, environment-name inventory, English/UA runbook; no production changes.
- Зависимости: None beyond scope approval; no real credentials.
- Ожидаемый результат: P01 synthetic recovery demonstrator, в границах указанного scope; нет обещания продаж.
- Acceptance: Broken fixture restored, executable acceptance, secret-free docs, ≤16h initial build target.
- Сложность: ESTIMATED small-medium; уточнить после scope/access. Ни одна оценка не включает unknown platform review wait.
- Проверяемая гипотеза: Buyer can understand concrete result; delivery technically bounded.

## PR03. Offer/intake/attribution research assets

- Точный scope: One offer page/copy and opt-in minimal intake design; no registration/publication until separately authorized.
- Зависимости: PR02; owner eligibility/fee/payout selection.
- Ожидаемый результат: Offer/intake/attribution research assets, в границах указанного scope; нет обещания продаж.
- Acceptance: Scope/exclusions/price experiment and privacy/measurement review; staged synthetic form only.
- Сложность: ESTIMATED small; уточнить после scope/access. Ни одна оценка не включает unknown platform review wait.
- Проверяемая гипотеза: Two channels can expose qualified buyers at acceptable price.

## PR04. Consent-based commercial validation ledger

- Точный scope: Minimal private cohort/outcome schema and manual approved pilot checklist; no automated outreach.
- Зависимости: Owner commercial authorization; channel rules; PR03.
- Ожидаемый результат: Consent-based commercial validation ledger, в границах указанного scope; нет обещания продаж.
- Acceptance: Payment/outcome fields only actual; no invented exposures; PII outside repo; first2paid cases if market responds.
- Сложность: ESTIMATED small; уточнить после scope/access. Ни одна оценка не включает unknown platform review wait.
- Проверяемая гипотеза: Price acceptance, lag, close, delivery/support unknowns.

## PR05. Reliable event-state primitive

- Точный scope: Record versions, stable semantic identity, checkpoint transaction, outbox lease/retry, reconcile and explicit replay approval.
- Зависимости: Related paid workflow from PR04; current POC only input.
- Ожидаемый результат: Reliable event-state primitive, в границах указанного scope; нет обещания продаж.
- Acceptance: Duplicate/out-of-order/collision/missing-ID/crash tests; no double effect; uncertain state requires review.
- Сложность: ESTIMATED medium; уточнить после scope/access. Ни одна оценка не включает unknown platform review wait.
- Проверяемая гипотеза: Reusable reliability solves observed workflow better than free substitute.

## PR06. P04/P02 adapter for one real scoped integration

- Точный scope: One documented API, signed webhook mapping, redacted synthetic contract tests; client-owned config.
- Зависимости: PR05; client permission and free-tool comparison.
- Ожидаемый результат: P04/P02 adapter for one real scoped integration, в границах указанного scope; нет обещания продаж.
- Acceptance: Agreed end-to-end acceptance; no full-store data copy; rollback; bounded support.
- Сложность: ESTIMATED medium; уточнить после scope/access. Ни одна оценка не включает unknown platform review wait.
- Проверяемая гипотеза: Repeatability across2similar deployments.

## PR07. Bounded cloud scheduler comparison

- Точный scope: Supabase Cron/Edge finite batch vs necessary worker challenger; no current main bot migration; safe run summaries.
- Зависимости: Owner cloud accounts/budget authorization; PR05; actual scheduled job demand.
- Ожидаемый результат: Bounded cloud scheduler comparison, в границах указанного scope; нет обещания продаж.
- Acceptance: 48h observed runs incl retry/restart; stale data alarm; quotas and cost log; no unsupported SLA.
- Сложность: ESTIMATED medium; уточнить после scope/access. Ни одна оценка не включает unknown platform review wait.
- Проверяемая гипотеза: Architecture B is feasible at measured cadence; C only if constraint.

## PR08. Maintenance plan and client regression probes

- Точный scope: Opt-in health check, scope/SLO/support budget, renewal tracking, client-owned alerts; no auto-billing until approved.
- Зависимости: 2accepted deployments; owner commercial/legal approval.
- Ожидаемый результат: Maintenance plan and client regression probes, в границах указанного scope; нет обещания продаж.
- Acceptance: 2actual renewals; measured support cost; manual cancel/export; redacted logs.
- Сложность: ESTIMATED medium; уточнить после scope/access. Ни одна оценка не включает unknown platform review wait.
- Проверяемая гипотеза: Recurring value and margin beyond one-off jobs.

## PR09. Reusable kit/OSS publication candidate

- Точный scope: Extract only own licensed primitives, package/tests/docs; no client data; licensing and marketplace admission review.
- Зависимости: PR02/PR05 evidence; owner publication permission; payment route if paid.
- Ожидаемый результат: Reusable kit/OSS publication candidate, в границах указанного scope; нет обещания продаж.
- Acceptance: Clean-secret/license scan; synthetic install/recovery; manual publication only if authorized.
- Сложность: ESTIMATED small-medium; уточнить после scope/access. Ни одна оценка не включает unknown platform review wait.
- Проверяемая гипотеза: Docs/OSS produce qualified voluntary inquiries or kit purchases.

## PR10. Optional procurement/grant challenger

- Точный scope: One source adapter, max10awarded IT records, exact IDs/provenance, opt-in partner evidence pack; no scraped contacts.
- Зависимости: Source license and owner-approved experiment; ≤4h/week cap.
- Ожидаемый результат: Optional procurement/grant challenger, в границах указанного scope; нет обещания продаж.
- Acceptance: Supplier fields quality measured; false matches=0 in reviewed sample; no demand claims without buyer evidence.
- Сложность: ESTIMATED medium; уточнить после scope/access. Ни одна оценка не включает unknown platform review wait.
- Проверяемая гипотеза: Public data adds unique actionable context, not merely record volume.

## PR11. Revenue model calibration and decision review

- Точный scope: Import anonymized actual cohorts, revise priors with uncertainty, price/time sensitivity and portfolio rerun.
- Зависимости: PR04/PR08 outcomes; privacy aggregation.
- Ожидаемый результат: Revenue model calibration and decision review, в границах указанного scope; нет обещания продаж.
- Acceptance: Reproduce actual monthly accounting within agreed tolerance; show sample size and prior/posterior distinction.
- Сложность: ESTIMATED small-medium; уточнить после scope/access. Ни одна оценка не включает unknown platform review wait.
- Проверяемая гипотеза: Choose scale/pivot based on paid evidence rather than feature output.

## Non-goals для первых PR

Не строить общую CRM, многопользовательский SaaS,30source adapter suite, массовый AI scorer, браузерный bidder, email finder или auto-outreach. Security remediation не должна скрытно переписать историю/отозвать чужие credentials; owner делает это отдельно. P03 security service требует qualification gate и не является default revenue shortcut.

Все implementation changes должны иметь source-specific contract fixtures, synthetic credentials, meaningful negative tests и traceable acceptance. Не добавлять tests, которые просто повторяют constant price assumptions вместо проверки accounting/behavior.
