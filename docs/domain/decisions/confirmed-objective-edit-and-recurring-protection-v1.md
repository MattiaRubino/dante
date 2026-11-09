# Confirmed Objective edit, hard removal and recurring protection — v1

**Decision:** approved by product owner, 2026-11-09. **Scope:** Activity and Event; ordinary Edit, recurring `only_this`, recurring structural / selected-and-following Edit. **Status:** normative contract; executable implementation and verification must be recorded separately. This decision supersedes the legacy inline "historic result remains / removal forbidden" editor notice, not the distinctions between Objective definition, Observation and Evaluation.

## 1. Objective UI states

- **No accepted result:** existing editor remains unchanged (name, kind, target / range / unit, per-goal verification, add, reorder, ordinary removal).
- **Accepted result present:** render an **in-place read-only row** in the same ordered Objective list. Show Objective label, authored criterion/target and the **accepted** value according to boolean / quantity / range / qualitative kind. No active name/target/kind/unit/verification fields, reorder arrows or ordinary Objective removal. Avoid a duplicate recorded-results list beneath the editor and the old explanatory paragraph.
- Provide one explicit **Elimina registrazione** action on the recorded row. This is NOT "delete Objective", "correction", or a silent form save.
- The behavior is identical for ordinary Activity/Event Edit and single-occurrence Edit; use one shared presentation/contract, not per-editor forks.
- Preserve the separate **Correggi risultato** capability for a genuine correction without erasing the result. Do not disguise a correction as deletion.

## 2. Irreversible accepted-result removal

- Before deleting, show a real confirmation dialog with **Annulla** and an explicit destructive confirmation. Cancelling changes nothing.
- On confirmation, atomically and permanently remove **every Observation and associated Evaluation/history/replay/input-confirmation fact that belongs to this Objective's recorded result**, including earlier corrected results. No remaining application-accessible result history, "cancelled" record, stale result cache or ghost in Work/Inspector. This is physical deletion, not a soft-delete marker.
- Preserve the Objective definition and its identity, ordering, criterion, verification and other independently recorded Objective/Session facts. Immediately reload canonical Objective read model and show the original editable row.
- A stale expected-result revision, concurrent correction/confirmation, missing ownership or changed objective must fail without partial deletion. Guard all routes with authenticated self-scope, explicit intent and CAS. Never run a browser-only delete of local state or reach privileged tables directly from web.
- Once a result has been **permanently deleted**, its old confirmation cannot silently reappear via idempotent replay or recurrence rematerialization. A new confirmation is a new result.
- Avoid introducing a durable **new** result-removal audit trail in user application data. Independently imposed external infrastructure logs are outside this contract.

## 3. Recurrence protection semantics

An occurrence is **protected** from any series-wide mutation if it has any real Session **running, paused or finished/recorded**, an accepted Objective result, locally edited instance metadata/schedule/structure/Objective, or another existing protected exception. No distinction between running and paused is allowed in this guard.

- If the **selected** occurrence is clean, offer **Questa e le successive** (inclusive) and exclude all protected future occurrences. Preview must show excluded identities/reasons.
- If the **selected** occurrence is protected, **Questa e le successive** must not be offered or accepted. Offer **Dalla successiva** (exclusive); preserve selected and every later protected occurrence.
- **Solo questa** allows individually editing a recorded instance only within the existing legal lifecycle guards; accepted Objective rows stay read-only until explicitly removed, and live Session restrictions continue to apply. No accidental series propagation.
- Removing an accepted result only clears that protection reason. The instance remains protected if it still has any Session, local edit or other fact. Never blindly unprotect a whole occurrence.
- Apply the same protections to ordinary and structural series edits for Activity and Event, preview AND SQL acceptance; stale previews are rejected. No client-only filter or last-writer-wins.
- An Activity with multiple intervals is **one Activity with several valid Schedule/card identities**; it must not be reported as a duplicated Activity.

## 4. Acceptance / quality gates

- Unit/UI: four result kinds rendered accurately; read-only recorded row; no duplicate footer; deletion confirm/cancel/error/refresh; ordinary/recurring Activity and Event. Unknown/stale result stays blocked, not silently editable.
- API/PostgreSQL: confirmed result and one or more corrections, permanent deletion of owned result graph, intact Objective definition, independent Objective/Session isolation, concurrent confirmation/correction conflict, replay cannot resurrect, no user-visible result after reload, no privilege bypass.
- Series tests: running, paused, finished Session; accepted Objective; locally edited exception; mixed clean/protected first/middle/future; selected scope inclusive or from-next exclusive; source and first physical Schedule identity preserved after one-off→recurring conversion.
- Stateful P1/P2/P3 v2 E2E: independent expected state, exact canonical API and durable Timeline readback after each mutation; test first/middle/last edited occurrences (including **the physical first after conversion**) and scan for duplicate native/Occurrence/Schedule identities, while allowing multiple distinct interval cards for one Activity.
- Every bug fix must bring a focused red-to-green regression, then targeted tests, then the 27-group full gate on the same SHA; report candidate vs actually executed results separately. Do not skip/weaken tests or alter DANTE's unrelated behavior to satisfy a driver assumption.

## 5. Migration and implementation requirements

Use forward-only Alembic migration(s) for privileged PostgreSQL deletion capability, dedicated authenticated API, typed web client methods and shared UI. Remove obsolete editable-recorded behavior and explanatory copy throughout the actual edit surfaces. Keep database ACL and dictionary/generated-contract workflows intact; never rewrite an applied migration.
