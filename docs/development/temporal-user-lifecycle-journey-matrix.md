## 2026-11-12 — complete browser inventory in two isolated selections

Owner Chromium evidence: A10 alone passed 1/1 in 80.37s. Four concurrent P2 representatives recorded 3/4 PASS in 240.04s: E11, A06 and A10 green; A01 returned HTTP 409 on whole-series DELETE after the single deletion succeeded. A following A01+E11 two-worker run passed 2/2 in 144.93s. The earlier 409 is **intermittent, not resolved**. Its submitted fingerprint matched the series preview, but the compact trace omitted the HTTP problem body. The E2E assertion now captures a bounded response body when a DELETE is rejected; no product fix is claimed.

The governed real-stack runner supports `--grep-invert` with identical selection in discovery and execution. `--verify-partition` must establish full = V2 + legacy for each of Chromium, Firefox and WebKit before a split gate. Execute both halves on **the same clean SHA**: `--workers 3 --v2-workers 2 --grep 'V2-'` for the 102 V2 cases per browser, then `--workers 3 --grep-invert 'V2-'` for every retained legacy test. The legacy half remains one worker per independent stack, preserving outage/recovery isolation. Upload both summaries and automatic diagnostics. A green half cannot certify the other; any 409 or missing test keeps the global E2E gate red. The unfiltered runner remains available as the reference acceptance run.

---

## 2026-11-11 — targeted remediation after expensive 17/40 Chromium P2 run

The 30m56s P2 run supplied enough evidence to avoid another blind full-matrix rerun. New code on `feature/timeline-temporal-operational` addresses **two confirmed repeated races**:
1. Event `Questa e le successive` no longer hydrates the entire independent *local Event editor* before displaying `RecurringSeriesEditor`; after validated scope choice the series editor loads its own versioned source. This removes an unnecessary multi-API prerequisite observed as Inspector busy/disabled in E11/E14/E16/E17 traces. Existing Event inspector test now asserts no local profile/occurrence-patch fetch.
2. Activity/Event destructive confirmation now holds a **same-tab Occurrence inventory lease from all hard-delete previews until acceptance/cancellation/unmount**, mirroring the already accepted series-edit lifecycle. The full-series DELETE is executed inside the lease without re-entering the FIFO; checkpoints are unblocked on completion/failure. The backend SERIALIZABLE/fingerprint CAS remains unchanged; distinct-tab external modifications still legitimately return 409. Inspector acceptance tests and a remote preview→accept regression were updated.

**Activity 11× PUT timeout:** the archived traces did not include a completed/matching PUT response, and cannot distinguish client-side validation, disabled Save, HTTP pending or transport failure. Do NOT invent a SQL fix or increase broad timeouts. The stateful test now asserts Save readiness and reports whether a matching PUT actually started, any failed request, UI alerts, and invalid fields; waits are bounded at 5 s for ready and 12 s for the exact response. Run **one representative A10** after lint/typecheck/Vitest, inspect its diagnostics, then correct the root if still red.

A06/A16 all-day canonical envelope expectation was previously corrected, not yet rerun. Remaining E10/E18/E19/E20 need representative traces after fast-path Event fix; old snapshots do not prove the same cause. P2 suite remains **17/40 on the last full run**, not green on the new SHA.

**Verification gate:** format then run ESLint/typecheck and targeted Vitest (`event-inspector-actions.test.tsx`, `activity-inspector-actions.test.tsx`, `remote-temporal-hard-deletion.test.ts`), then a **small** Chromium subset or individual A10 if needed. Preserve seven local generated OpenAPI modifications; full parallel gate requires a clean checkout and should not run before targeted fixes are validated.

---

## 2026-11-11 — P2 40-case concurrent Chromium matrix: 17 green, 23 red

Artifact supplied by the user: `E2E_DIAGNOSTICS.tar(20261111-182033).gz`; `summary.json` and all 40 `chromium/junit.xml` cases inspected. Chromium, one real-stack, `--v2-workers 2 --grep V2-P2-`: **40 discovered, 40 recorded, 17 passed, 10 assertion failures, 13 errors, zero skips**, wrapper **1860.44 s**, Chromium **1856.19 s**. Sum of JUnit per-case test seconds is ~3601.95, so two active workers account for most wall time: adding a broad rerun without fixing shared causes is wasteful. Prior standalone A01 PASS does NOT imply this concurrent matrix is green; A01 and A02 both get HTTP 409 at the whole-series DELETE assertion.

Observed families (keep every red case; no skips/xfail):
- **11 Activity atomic PUT response timeouts at 15 s**: `A09–A15, A17–A20`, mostly step 3 (local exception), also some step 2B/6. The report does not prove whether the PUT was sent, failed validation or was slow; instrument request-start/response and editor errors before choosing a timeout increase.
- **4 Event life-area color editor missing**: `E11,E14,E16,E17` at step 4. Inspector snapshot shows the original details with disabled controls rather than the expected series editor. Distinguish pending editor hydration, abandoned editor and product failure using trace/request evidence.
- **2 all-day Activity E2E expectation mismatches**: `A06,A16` at step 2. A canonical all-day envelope Schedule exists despite zero *authored* intervals. E2E assertion corrected on branch in `temporal-stateful-personas.spec.ts` to expect one envelope for all-day, retaining exact Schedule ID checks (commit `8c614c833b3232a6ab5efa67c11e9a27cabd54b4`). Await targeted acceptance.
- **2 Activity full-series deletion conflicts**: `A01,A02`, step 8, DELETE returns 409 rather than 200 under two-worker load. The deletion preview/accept race is a candidate requiring trace evidence; do not weaken CAS.
- **4 distinct Event issues**: `E10` missing expected future card at step 8; `E18` missing title textbox at step 6; `E19` delete dialog lacks single-instance choice at step 8; `E20` missing title textbox at step 2B.

Result breakdown: Event `12/20` PASS, Activity `5/20` PASS; `17/40` total. Slowest passing scenarios include `E12` 243.64 s and `E13` 219.88 s. With one stack and two browser workers the full suite is not suited to every fix-loop. **Use minimal representative selections first** (for example `--workers 1 --project chromium --v2-workers 2 --grep 'V2-(P2-E11|P2-A01|P2-A10|P2-A06)'`, accepted by the existing V2 selector policy); run full P2 only after families are corrected. The full parallel gate additionally requires a clean checkout and must not reset unrelated generated OpenAPI files. Do not declare this suite green based on previous individual E2E passes.

---

## 2026-11-11 — V2-P2-A01 accepted on real stack (Chromium)

Observed from the user's uploaded `summary(20261111-171405).json` and compact `E2E_DIAGNOSTICS` JUnit: `V2-P2-A01 native series → local → following` **PASS**, 1/1 discovered and recorded, 0 failures, 0 errors, 0 skips, 0 retries, exit code 0. Test-case duration **129.532 s**, Chromium project **156.57 s**, full wrapper **162.15 s**. The E2E scenario completes the final single-instance deletion, checkpoint and whole-series deletion assertions (the same A01/8 path that previously timed out). Frontend commit reported on GitHub: `66c24559d9f2949f411ebe0b127dd4ee3296971c`.

This closes the known A01 functional regression for this Chromium run; `P2-A03` and `P2-E03` previously passed on their own targeted runs. **Do not infer per-operation SQL performance from aggregate run time**: this compact artifact has no per-step DELETE response timing or query plan. Next step is the broader stateful P2 persona matrix, then the clean-checkout full parallel gate. The parallel gate explicitly rejects any uncommitted generated OpenAPI changes; preserve them until reconciled rather than resetting or staging them incidentally.

---

## 2026-11-11 — P2-A01 advances to deletion; whole-series DELETE exceeds 15-second E2E wait

Chromium diagnostic `20261111-154205` reports `V2-P2-A01` at step **A01/8 Delete single → checkpoint → whole series**, after the earlier 409-prone following-series revisions have completed. `page.waitForResponse` at `temporal-stateful-personas.spec.ts:983` times out at 15 seconds (test `actionTimeout`), with **no HTTP status yet**. Trace confirms the second `DELETE /api/v1/temporal/hard-deletion/{activity}` was *started* at 15:37:32.258Z; its response is absent/incomplete when Chromium tears down. The earlier single-instance DELETE returned HTTP 200. The full-series SQL function `dante.delete_self_temporal_hard` iterates generated Activity roots and invokes `delete_self_activity_lifecycle_graph` separately for each, so the whole-series graph may be substantially heavier; this does **not** yet prove the absence of an SQL lock wait or performance regression.

Targeted containment: `remote-temporal-hard-deletion.ts` now schedules confirmed DELETE under the same in-tab occurrence-inventory checkpoint fence as series editing. `remote-temporal-hard-deletion.test.ts` verifies checkpoint-before-delete, delete-before-checkpoint, and preserved 409/released queue. In the stateful E2E, **only whole-series DELETE** gets a bounded `90_000` ms response wait while the suite's 300-second journey limit remains; it must receive HTTP 200 and subsequent canonical absence checks must still succeed. A second trace showing continued slowness or timeout should trigger SQL/DB lock and lifecycle-graph performance diagnosis, **not** another timeout increase.

Status: code published, **local Prettier/ESLint/typecheck/Vitest/Chromium run is pending**; do not mark A01 green yet. The unrelated local generated OpenAPI changes must be preserved.

---

## 2026-11-11 — P2-A01 second E2E trace: checkpoint AFTER preview, BEFORE accept

Chromium `V2-P2-A01` on `2faca8b14` still fails with 409 at Following-series revision. The **new** 2026-11-11 14:45:25–26 UTC Playwright trace establishes the missing interval: `series-edit-preview` POST begins 14:45:25.983Z and returns 200 with 35 target Occurrences; `occurrences/checkpoint` POST begins 14:45:26.281Z and returns 200 after materializing 37 Occurrences in the requested Timeline window; `series-edit` POST begins 14:45:26.549Z and returns `temporal.recurring_series.stale` 409 (`Series preview changed before acceptance.`). The first FIFO gated each HTTP call but intentionally permitted a checkpoint between the preview and the human confirmation.

**Correction:** a same-tab inventory review lease now spans preview, human confirmation and acceptance. `holdTemporalOccurrenceInventoryReview` reserves the queue slot before CSRF, exposes a one-time idempotent release and permits acceptance inside the held slot. `RecurringSeriesEditor` releases on Back, Cancel, Escape, close/unmount, failed preview or completed acceptance; the preview epoch prevents orphaned leases when an editor closes while preview is pending. A checkpoint enqueued after preview waits for the user's explicit disposition. No PostgreSQL lock is held, no cross-tab changes are silently accepted, the backend SERIALIZABLE/CAS checks remain authoritative, and server 409 handling stays unchanged. Existing `preview()`/`accept()` client APIs continue to use the original per-request fence for non-interactive callers.

Regression test file `temporal-occurrence-inventory-fence.test.ts` extends coverage to a checkpoint requested **between** review and accept, explicit cancellation/release, and rejected preview cleanup. Frontend lint/typecheck/Vitest and Chromium A01 **must be executed locally** before calling this green. E03 and A03 remain the previously recorded passing scenarios. Do not use a broad gate until A01 passes.

---

## 2026-11-11 — P2-A01 real-stack 409: checkpoint overlaps fingerprinted preview

Old Chromium trace `V2-P2-A01` (09:11:24Z–09:11:26Z) shows full Timeline `POST /occurrences/checkpoint` starting at 09:11:24.689Z, then `POST /occurrences/{selected}/series-edit-preview` starting at 09:11:24.914Z before checkpoint completion. The preview returns 200 but the subsequent `/series-edit` returns 409 `temporal.recurring_series.stale` with `Series preview changed before acceptance.` The trace also shows a SQLSTATE 40001 transient serialization abort during an earlier series acceptance, already covered by the server's bounded transaction retry.

**Frontend fix:** shared same-tab FIFO in `temporal-occurrence-inventory-fence.ts` orders checkpoint, series preview and series accept *including CSRF fetch*, and releases the queue after rejection. Both remote data sources use the same gate. It prevents a checkpoint already requested in this tab from changing the occurrence inventory while a preview is being built. Ordinary read-only Timeline fetches still run concurrently. The server source revision, protection, fingerprint and SERIALIZABLE CAS are unchanged: changes from other tabs/devices or after review still correctly produce 409 and require a fresh explicit review; no automatic stale replay, retry or hidden write.

**Regression:** `temporal-occurrence-inventory-fence.test.ts` verifies checkpoint-before-preview, preview-before-checkpoint, failure releases the queue, and HTTP 409 remains an error without silent retry. Test execution and Chromium `V2-P2-A01` on this new SHA are **pending**; do not mark A01 green yet. P2-E03 has already passed both real PostgreSQL and Chromium E2E, and P2-A03 passed Chromium.

---

## 2026-11-11 — E03 all-day monthly following edit: SQL coordinate resolver rejects valid all-day anchor

Focused Chromium `V2-P2-E03` (42.02 s, 0/1 PASS) still reaches the series preview but receives HTTP 422. The request selected a 2026-12-21 all-day third-Monday Occurrence following a local first-instance edit on 2026-11-16; POST `series-edit-preview` is rejected before review. The response is `temporal.recurrence_edit.invalid`. The added Python validation logger is absent from the Playwright bundle because the SQL constraint path is handled separately as `DBAPIError`.

The original PostgreSQL function `dante.occurrence_edit_coordinate_instant` (`20261008_123`) raises `occurrence_edit_unresolved_zone` for every `named_zone` coordinate lacking `resolved_at`, even when `generated_wall_time IS NULL` by design for **all-day** calendar Occurrences. This is a code-level defect explaining why timed E01/E04 series edits proceed and all-day E03 fails. A forward-only `20261111_186` revision now allows a named-zone calendar **date-only** coordinate through the existing DST-checked local-midnight branch, while continuing to reject unresolved **timed** named-zone coordinates. No applied migration is edited and existing self ownership / SQL EXECUTE ACL are preserved.

Added real PostgreSQL regression to the existing recurring Event Life Area suite: three monthly third-Monday all-day Occurrences, first local Event override, civil-midnight self-scoped coordinate read, second selected-and-following series preview, actual atomic acceptance, preserved first override and transactional Life Area creation. This regression and Chromium E03 have **not yet been executed against the new SHA**. Do not claim green until the owner runs targeted PostgreSQL, migration and E03 real-stack checks. P2-A01's 409 remains separate.

---

## 2026-11-11 — P2-E03 preview 422 after ordinal read fixed; targeted internal validation diagnostics

Owner's fresh Chromium smoke `V2-(P2-E03|P2-A03)` on `00acac32536e` recorded **1 PASS** (A03), **1 FAIL** (E03), 0 skips, 85.77 seconds. A03's genuine global Life Area recolor now passes end to end. E03 now loads the monthly ordinal recurrence correctly (GET `/events/{ref}/recurrence` HTTP 200 with `ordinal_weekdays=[{weekday_number:1,ordinal:3}]`), but fails later at its global Life Area color-change review: POST `/occurrences/{selected}/series-edit-preview` returns `422 temporal.recurrence_edit.invalid`. The actual body is for an all-day monthly third-Monday Event, inclusive `this_and_following` starting 2026-12-21 and genuine blue recolor of an existing Life Area. It retains unchanged Agenda, Objectives, participants and the loaded recurrence rule. The review dialog is absent because server preview refuses the proposal, **not** because of a UI selector or timeout.

The public 422 currently hides the exact internal invariant. The backend now emits `temporal.recurring_series.edit_rejected` with `phase`, exception class and constant developer-owned validation reason for both preview and acceptance; unexpected ValueError detail is redacted. Request payloads, SQL, titles, personal data and IDs are not logged. Public problem codes and write safety are unchanged. Added focused logging regression. **Diagnosis only, not a functional fix**: run backend unit and a single real-stack `V2-P2-E03` to capture the precise reason, then fix the specific invariant with PostgreSQL regression before another broad browser gate. Do not weaken the validation, delete tests, or claim green.

---

## 2026-11-11 — Five-case Chromium smoke: positional Recurrence API and Life Area E2E fixture

The 5-case Chromium V2 smoke `V2-(P2-A01|P2-A03|P2-E01|P2-E03|RT-02)` produced 2 PASS (P2-E01, RT-02), 2 FAIL (P2-A01, P2-A03) and 1 ERROR (P2-E03), 0 skips, in 116.7 s.

E03 is a backend HTTP 500: `GET /events/{ref}/recurrence` validates tuple `ordinal_weekdays` via `RecurrenceStateResponse` which expects named objects. The transport-only fix serializes ordinal weekday and annual month/day coordinates as explicit field maps, with offline contract regressions for each. The Domain tuple representation and canonical persistence remain unchanged. Candidate remains unverified on WSL.

A03 is a test-fixture mistake: the `existing` Life Area is already `#FFD600` for case 03, and selecting Giallo again is a no-op. The browser test now deterministically chooses a *different* named color and still asserts the global-change warning and canonical catalog readback; no product warning has been fabricated. Candidate remains unverified on WSL.

A01 is separate and **unresolved**: HTTP 409 `temporal.recurring_series.stale` in the second series acceptance. Its network trace shows `POST /occurrences/checkpoint` beginning before the preview and completing before acceptance. This suggests an inventory/preview interaction but does not yet prove which fingerprint input changed. Do not bypass the fingerprint or silently auto-accept a stale review; isolate with a real-stack single-browser A01 journey and canonical fingerprint diagnostics.

No full green E2E gate is claimed for this commit series. The owner's generated OpenAPI/client changes are not modified by these source/test updates.

---

## 2026-11-11 — P2-A04 Activity local edit: wait for the actual atomic commit

Owner's three-case isolated Chromium smoke `V2-(P2-E04|P2-A04|P3-EFIRST)` produced **2 PASS** (P2-E04, P3-EFIRST) and **1 FAIL** (P2-A04) in 102.13 s. The failing A04 step expected the last finite Activity's locally changed title on 2027-01-11; HTTP 200 canonical Timeline instead retained the original title. The diagnostic trace demonstrates that Activity Edit changed the submit button label from `Salva modifiche` to `Salvataggio…`; the test's `toHaveCount(0)` on the former label passed while the editor was still pending. It immediately navigated Home and no `PUT /activities/{ref}/atomic-edit` had completed or even appeared in the recorded network. This is a **test driver false completion**, not evidence of a rejected Activity edit, a recurrence cardinality defect, or an Event regression.

`localRevision` now waits for the exact Activity atomic PUT response and HTTP 200, then requires the Activity editor form to close before navigation; the existing physical-placement, title and recurrence-boundary checks remain intact. Event confirmation retains its successful UI acknowledgement path. **Candidate committed, not yet re-executed locally:** run single Chromium `--grep 'V2-P2-A04'` first, then representative P2 tests; do not treat this fix as green before a real-stack replay. The separate P2-E04 and P3-EFIRST are observed PASS on the preceding HEAD.

---

## 2026-11-11 — Focused P1-A02/A06 browser confirmation

The owner's newer `V2-(P1-A02|P1-A06)` summary and progress show **2/2 PASS** in Chromium after the all-day untimed named Session duplication fix. Earlier RED evidence remains useful diagnostically but is superseded for these precise cases. This result does not certify all P1 or the full gate.

---

## 2026-11-11 — P1-A06: all-day Activity duplicate must retain unplaced named Sessions

The focused parallel Chromium run `V2-(P1-A02|P1-A06)` recorded 2/2, 1 PASS (P1-A02) and 1 FAIL (P1-A06), after 6 backend unit tests, 1 PostgreSQL regression and the runner's self-test passed. The P1-A06 HTML snapshot proves successful Activity metadata/Objective/Session replacement and Life Area changes, followed by clicking Inspector `Duplica`. No composer appeared because `buildActivityDuplicateSeed` deliberately threw `Le sessioni pianificate richiedono un’attività con orario.` for a `date_span` with named planned Sessions.

This guard contradicted valid all-day Activity canonical structure: unplaced named Sessions are allowed, as confirmed by the real saved state and by `buildTemporalCreateRecurringActivityTemplate` preserving `time_enabled:false` planned slices for all-day Activities. The duplicate seed now retains the original day range (end-exclusive -> inclusive), life area, objectives, placement protection and ordered untimed Sessions, without introducing invented clock times. The existing invalid `date_span`/interval mix rejection remains unchanged.

The new unit regression asserts two out-of-order named Sessions are sorted and copied as untimed, no borrowed time fields, all-day date range preserved, and fresh Objective IDs. Targeted Chromium P1-A06 remains to be rerun; do not mark green before real execution. The separate P1-A02 scenario remains previously observed PASS. Next triage P2 grouped errors after this gate.

---
## 2026-11-10 — Disposable E2E database capacity and interruption durability

The first broad two-worker Chromium V2 run was interrupted near case 89/103. It exhibited repeated `QueuePool limit of size 5 overflow 5 ... timeout 5.00` after ~19 minutes, and did not produce JUnit because the browser process had not completed. The shared stack's `serve-access-auth-stack.py` sets only 5+5/5 seconds regardless of browser concurrency. Only for two-worker E2E execution, the Access/Auth harness now copies `DatabaseSettings` with a bounded 10+10/15-second pool; one-worker tests and production settings retain their original values. This addresses a demonstrated *test harness capacity mismatch*, but is not proof of absence of held connections; continued pool timeouts require further investigation.

For every browser stack, the runner now writes `progress.jsonl` synchronously on each Playwright test completion via a custom reporter, and builds `partial-summary.json` even when SIGINT prevents JUnit finalization. These are explicitly *diagnostic*, `complete:false`, and cannot satisfy the green coverage gate. The compact diagnostic archive includes both. Its `--self-test` verifies two observed records with different outcomes and archive preservation. A full acceptance pass still requires the definitive JUnit exact-inventory check. After targeted green, diagnose remaining P2 scope/placement errors and rerun smaller representative samples before repeating 103 tests.

---
## 2026-11-10 — Full V2 Chromium interrupted at ~89/103: locked Activity named Session regression

The 103-scenario real-stack run was interrupted by Ctrl+C after approximately 30 minutes. A compact partial archive contains 55 failure reports but **no final JUnit**, so do not claim exhaustive PASS/FAIL counts. The 17 HTTP 409 `Unlock the Activity placement before replanning` reports under P1 Activity follow a common payload: the user edits metadata and Objectives, retains all existing Activity interval coordinates unchanged, removes one named planned Session and adds another. Prior `apply_activity_replan_in_session` wrongly regarded `delete_planned_sessions` as an **envelope coordinate revision**, and rejected it when `placement_protected=true`. The envelope is not moved.

The guarded fix excludes pure `delete_planned_sessions` from envelope placement-change detection. It retains the named Session's own placement lock check, the recorded-attempt protection, and all genuine envelope/interval lock checks. PostgreSQL integration regression `test_locked_envelope_allows_atomic_named_session_replacement_but_not_locked_named_delete` exercises real atomic replacement, unchanged locked envelope and interval identities, preserved named identity, single replacement and rejection of a separately locked named Session.

Other REDs remain, notably P2 Event scope/physical placement mismatches and connection exhaustion `QueuePool size 5 overflow 5 timeout 5s` during broad parallelism. Do not dilute functional assertions or treat the interrupt as test successes. Next run targeted P1-A02 and P1-A03 with an isolated stack, then triage P2 and DB pool before the 103-scenario rerun. Full dynamic suite should emit durable partial diagnostics on interruption.

---
## 2026-11-10 — P2 Event serialization retry after confirmed Chromium SQLSTATE 40001

Owner's second focused dynamic E2E: P2-A04 PASS, P2-E04 FAIL. Backend diagnostic tied to the exact 409 request: `failure_stage=life_area_create`, `sqlstate=40001`, `exception_type=OperationalError`, during SERIALIZABLE Event following-series acceptance with new Life Area. SQLSTATE 40001 is a PostgreSQL serialization abort, **not** a stale-source/CAS conflict. The prior PostgreSQL regression passed without contention, which did not prove the real browser case.

Series `accept` now retries only SQLSTATE 40001, with at most 3 full transaction attempts (rollback and new session each time, short bounded delays). It invokes the same existing `_accept_once` command and rechecks owner scope, operation replay receipt, source version, preview fingerprint, selected protection and complete occurrence reconciliation on every attempt. Any actual conflict (wrong version/fingerprint/protected selected), non-40001 SQL error or validation failure never becomes a successful retry. All Life Area, occurrence and series writes remain in one ACID transaction. The PostgreSQL regression injects first-attempt 40001 during Life Area creation after real preview, verifies next attempt accepts, and checks exactly one committed area. Unit tests cover successful retry, exhaustion, stale conflict, and nonretryable SQLSTATE.

Await targeted WSL tests and focused Chromium E04 before declaring green, then all V2 Chromium with `--v2-workers auto`. No test skipped.

---
## 2026-11-10 — Dynamic E2E RED follow-up: canonical empty-window shape and SQLSTATE diagnostic

Owner Chromium six-V2 dynamic smoke returned 3 PASS/3 FAIL; focused follow-up 1 PASS (RT-02), 2 FAIL (P2-E04 HTTP 409 at series accept; P2-A04 `kind:empty` at finite end). Exact E04 trace confirms preview/accept identical recurrence (`expected_count=4`, selected second biweekly date), and error `Series changed during acceptance.` from a generic SQLAlchemy catch, without actual SQLSTATE. Do not claim or fabricate its SQL cause. The native Event focused PostgreSQL regression now establishes 5 instances, edits original first and final locally, changes second-and-following with a new Life Area, title, Agenda, and finite count 4; it must preserve protected exceptions and cardinality. SQL failures in the outer series transaction log safe `failure_stage`, `sqlstate`, and constraint `error_code` only (never bind values or SQL). Keep public 409 unchanged pending actual diagnosis.

P2-A04's `GET /timeline/window?start_date=2027-01-24` returned HTTP 200 with `{"kind":"empty","start_date":"2027-01-24",...}`: that is *correct empty canonical truth*, not missing results. E2E assertion now permits `kind:empty` only when `items` is absent, or `kind:window` only with array items, and still checks all results for unauthorized extra occurrences. No skip, mock, timeout increase or weakening of the finite-boundary invariant.

Next owner action after pull: targeted real PostgreSQL `tests/integration/temporal/test_recurring_series_bounded_event_acceptance.py`, then focused one-browser Chromium `V2-(P2-E04|P2-A04)` if Postgres green. Preserve full archive and exact SQLSTATE if RED. **Candidate not yet verified; do not assert E04 resolved.**

---
## 2026-11-10 — Finite partial-series boundary + Session end response synchronization (candidate)

Owner's dynamic Chromium smoke completed six independent real-stack V2 scenarios using two same-stack workers: 3 PASS (P1-A01, P3-E01, P3-A01), 3 FAIL (P2-E04, P2-A04, RT-02), no skips. Both finite P2 failures prove one extra generated occurrence on 2027-01-24 despite an original fifth/final date of 2027-01-10: partial edits copied `expected_occurrence_count=5` while moving `effective_from` later. Backend now computes the canonical remaining candidate count from the *existing finite recurrence* for inclusive and exclusive selected-date scopes; `series-edit-source` exposes both counts and the editor initializes the correct `expected_occurrence_count`. Explicit user changes to the count remain possible; no default extension. Pure backend regressions cover biweekly, monthly ordinal, two wall times/day, open-series and off-cadence refusals. TS unit regressions verify Event and Routine scopes. Native Event Life Area integration verifies unbounded readback unchanged.

RT-02 dispatched `POST /sessions/{ref}/end` then immediately read `GET /sessions` before commit. The test now waits for the exact POST response, requires success, and polls the canonical session until `open=false` and `ended_at` is set, without skipping or weakening persistence assertions. **Candidate published; targeted WSL unit/PostgreSQL, API codegen/typecheck and dynamic Chromium smoke remain required**. Do not claim green before evidence. In a later phase run all V2 on Chromium with `--v2-workers auto`, leaving cross-browser for stabilization.

---

## 2026-11-10 — Converted first Event series acceptance receipt: explicit preserved identity (candidate)

Owner's focused Vitest RED reproduced the mismatch: preview includes the physical first Occurrence, while backend correctly retains it rather than superseding it. The old frontend incorrectly required `superseded_count == target_occurrence_refs.length` and reported `Conferma della serie non coerente` after HTTP acceptance. Long title and Event Agenda are not the cause.

Fix candidate: return explicit `preserved_occurrence_ref` in backend accepted/replay result and FastAPI response. The client accepts one fewer superseded target only when the preserved Occurrence is exactly the selected converted Event, present once in the reviewed targets, under inclusive `this_and_following`; native Event/Routine and `from_next` return null. Strict owner/scope/count/protected checks remain. No DB migration needed because owner-scoped converted-first seed already exists. PostgreSQL regressions assert real first identity, replay, response serialization and native Event null; the RED Vitest is retained with refusal variants. The final Chromium `V2-P3-EFIRST` assertion also uses exact accessible title rather than visually truncated card text, retaining card cardinality and stale-title absence.

**Status:** committed on feature branch, WSL tests/codegen/Chromium pending; do not claim GREEN or full 27-group gate until same-SHA owner results. Do not edit generated OpenAPI sources by hand.

---

## 2026-11-10 — E2E first local edit: HTTP 200 and canonical Timeline title correct; date virtualization in test

Owner's `E2E_DIAGNOSTICS.tar(8).gz` and `summary(2).json`: Chromium `V2-P3-EFIRST` runs 1, fails 1 in 45.87 s, at `assertCard(..., localTitle)` (test line 1527), 0 DOM cards with the new title after that helper does an unconditional extra `openHome(page, day)` navigation. This is **not** another database rejection: network trace has `POST /occurrences/{first}/event-local-edit` **HTTP 200** (revision 2), plus three successful `GET /timeline/window` reads where the physical original Event/Schedule carries the accepted first-only title; next day retains series title. Browser trace frame around 33490 ms also captures the physical first card rendered **with the exact correct new title** immediately before an extra reload/recycling transition; later virtualized-day frame no longer includes day 15 in its rendered range. A DOM locator on a date that has been recycled outside the viewport cannot prove a failed mutation.

**Test correction:** in this last Only-this step, check the *current edited page* for exactly one first-day card carrying the **exact** local title, and no first-day card carrying the exact stale series title. Keep independent canonical checks of the physical Schedule identity, no duplicate first-day placement, `GET /occurrences/{first}/event-detail` including local Agenda/title, and next-day UI/title untouched through fresh navigation. Do not loosen assertions or increase timeouts. The existing test already exercises full-page reloads during conversion/series edit; the post-local authoritative API read proves durable storage. Later broad navigation/virtualization stability should be tested as its own concern, not masked by a generic `assertCard` helper that navigates on every assertion.

**Status:** E2E assertion updated on branch; re-run Chromium single test. No production backend changes for this run. Local logs belong in gitignored repository `temp/`.

---

## 2026-11-10 — Chromium V2-P3-EFIRST: Only-this API 409 after first-day following edit (replacement candidate, verify WSL)

Owner's `temp/E2E_EVENT_FIRST_20261110-130226.log`: Chromium `1 discovered, 0 passed, 1 error`, global 300 s timeout. The attached `E2E_DIAGNOSTICS.tar(7).gz` shows the full UI conversion, first-day `this_and_following`, edited title and Agenda read from the *effective first Occurrence* API, stable physical first Schedule, no duplicated card and unchanged next-day cardinality **all passed**. The subsequent UI `Solo questa` on the physical first correctly hydrates the effective title and Agenda. After click Save, `POST /api/v1/temporal/occurrences/{first}/event-local-edit` returns **HTTP 409** within 13 ms. The test then blocked for ~270 seconds on `await saved.text()`, so its outer 300 s timeout masked the actual 409 as a browser-close error.

**Root cause:** `accept_event_occurrence_local_edit` compared `get_self_occurrence(...).governing_recurrence_state_ref` (historical state of the physically linked first Event) with `body.expected_recurrence_state_ref` (the **current** source state from `get_self_occurrence_edit_revision`). These are intentionally different after a selected-first series edit, which preserves the original physical Occurrence identity and advances its effective structure pointer. This was not tested at the API layer: the previous regression called the low-level SQL `accept_self_occurrence_profile_edit` directly and therefore missed the precheck.

**Fix candidate:** on a state difference, allow admission *only* when `get_self_event_recurring_first_by_occurrence(:actor,:occurrence)` proves the selected occurrence is that user's converted first Event and its source matches `get_self_occurrence(...).source_native_ref`. All other old-state occurrences still fail. The canonical `accept_self_occurrence_profile_edit` retains its existing atomic expected-current-state and revision CAS under the source lock, so no stale-client bypass. This also supports a first Event whose inherited structure remains at an older version after a future-only series edit.

**Regression:** `test_existing_event_keeps_first_event_and_excludes_duplicate_occurrence[unlocked/protected]` now calls the **real** API `get_occurrence_profile_edit_state`, `accept_event_occurrence_local_edit`, and `get_recurring_event_occurrence_detail` after TWO consecutive first-day following-series edits; asserts historical/current state inequality, no 409, first-only title+Agenda and unchanged next-day values; owner and Schedule boundary tests remain. E2E no longer waits on `response.text()` before checking status so 409 fails promptly and preserves its true diagnosis. Do **not** loosen E2E assertions or raise global timeout.

**Status:** branch source committed. Repeat **only the two PostgreSQL variants**, then Chromium one test when green. All test diagnostics/logs belong in repository `temp/`, which is gitignored; do not write to `$HOME`.

---

## 2026-11-10 — Converted Event first-instance parity with Activity/Routine (candidate, WSL gate pending)

**Owner's binding functional requirement:** converting one ordinary Event through Edit into a daily Event series must make the original physical Event the **first instance of that series**, not preserve it as an independent functional Event. `Solo questa` must edit that one instance, `Questa e le successive` includes the selected first date, `from_next` must not edit it; future instances follow the versioned source. Original physical Event/Schedule/factual identity may remain stored for durable history, but the user-facing Inspector and Timeline must consume *effective Occurrence state*, never an outdated standalone copy.

**Existing RED evidence:** original backend test `test_existing_event_keeps_first_event_and_excludes_duplicate_occurrence` failed 2/2 after a new checkpoint (two first-day cards). The structural exclusion fix previously made the backend recheckpoint and first DOM cardinality green, but Chromium `V2-P3-EFIRST` then failed because its *test queried raw `GET /events/{original}`* and demanded the updated series title. That raw endpoint is the original descriptor and is not the correct effective series view. `GET /occurrences/{first}/event-detail` is the canonical owner-scoped effective read, combining source structure/Agenda with accepted instance patches. Never make raw original Event mutate merely to satisfy this incorrect assertion.

**Parity fix candidate on branch:**
1. `EventInspectorActions` routes `Solo questa` on the converted first Event via the same `openProfileEditor('only_this', firstOccurrenceContext)` as later instances. The loader no longer gates `loadOccurrenceEvent` on the Timeline DOM's `occurrenceRef` prop being non-null, which was `null` for the physical first Event. The editor now hydrates the *effective* title, Agenda, Life Area, and related Occurrence-scoped fields, and its save uses the existing atomic Event-local Occurrence edit contract.
2. New forward-only migration **`20261110_184`** extends `dante.is_self_event_occurrence_schedule`: preserve the later-Occurrence lookup and admit the physical first Event's actual Schedule **only through the owner-scoped `get_self_event_recurring_first_by_occurrence` link**, verifying both original/source Event ownership. No synthetic Schedule created and no unrelated user or Schedule permission.
3. **Superseded implementation (RED, DO NOT REUSE):** writing inherited series structure as an `event_local`/`only_this` patch *after* superseding the first Occurrence caused `Selected current Occurrence unavailable` in PostgreSQL (2/2 failures, 11.06 s). Worse, such a patch would have falsely marked the first instance `local_change`, blocking later series edits. **Replacement:** do not supersede the linked physical first Occurrence. The source-locked series acceptance advances an owner-scoped `effective_structure_state_ref` on `event_recurring_seed` **only when the first is selected with `this_and_following`**, via migration `20261110_185` and its CAS-checked SQL capability. The linked first Event continues to hold its physical Schedule, remains a current editable Occurrence, and derives inherited Agenda/Life Area/participants from the pointed-to versioned structure. Native Event series and from-next/later-scoped edits do not modify first structure. The original historical Event descriptor remains untouched; the new-state structural exclusion continues preventing duplicate generated first-date cards.
4. The E2E `V2-P3-EFIRST` now asserts `GET /recurring/events/{original}/first-occurrence` then `GET /occurrences/{ref}/event-detail` (effective title + Agenda) instead of raw `GET /events/{original}`. The same journey then opens **Solo questa on the physical first**, verifies the editor starts with effective title/Agenda, edits both, asserts Event-local HTTP success, one original Schedule/card and the next day's unchanged values.
5. Targeted PostgreSQL `test_existing_event_keeps_first_event_and_excludes_duplicate_occurrence[unlocked/protected]` now changes the source Agenda in a scoped series edit, verifies the first linked Occurrence is **not superseded or protected**, its effective versioned source snapshot contains the new Agenda, and its owner-scoped physical Schedule capability rejects foreign actor/unrelated schedules. It also checks that a SECOND `this_and_following` edit from first succeeds, followed by a real `Solo questa` update that leaves later instances unaffected; retains repeated-checkpoint first/future Schedule cardinality and identity.

**Latest owner evidence and acceptance:** The previous `event_local` implementation failed 2/2 PostgreSQL variants in 11.06 s, `POSTGRES_EXIT=1`, with `ForeignKeyViolation: Selected current Occurrence unavailable` from `list_self_recurrence_edit_occurrences`. The replacement design is **committed but NOT YET EXECUTED** in the owner's WSL. Run the two PostgreSQL variants first (new DB migration via `migrated_database` fixture), then `pnpm --filter @dante/web typecheck`, then only Chromium `--project chromium --v2-workers 1 --grep 'V2-P3-EFIRST'`. Do not claim all Event series work is finished from this one path: Objective/Reality inheritance, protected history, changed first-day time geometry, Life Area inheritance and later-date scoped edits need their own parity coverage. Do not delete Event history or silently change scope rules. Fix any actual failures under the test's original strict assertions instead of widening timeouts or hiding cards.

---

## 2026-11-10 — Converted first Event duplicate: reproduced RED in PostgreSQL, transaction-level fix candidate

**Owner's authoritative RED on `30c19cb01`:** `test_existing_event_keeps_first_event_and_excludes_duplicate_occurrence` failed **2/2** in 11.90 s, both `[unlocked]` and `[protected]`. The added assertion after `this_and_following` on the physical first Event, followed by a NEW checkpoint, saw exactly **2 first-date Timeline entries instead of 1**. This is confirmed canonical backend duplication, not only a DOM/React issue. The prior test passed because it did not rematerialize the *revised* recurrence.

**Root mechanism:** existing one-off→series conversion correctly links the *physical original Event/Schedule* to a first `Occurrence` in `event_recurring_seed`. `RoutineOccurrenceMaterializationApplication._apply_event_policy` skips policies for that **specific first Occurrence ID**. However, a `RecurringSeriesEditApplication.accept(... requested_scope="this_and_following")` replaces the recurrence state; a subsequent checkpoint can generate a *new occurrence ID* for the original first date, so the ID-only skip no longer protects the physical first Schedule. A second scheduled/expected Event card is introduced by the new state. The original Event must not be deleted or reauthored.

**Fix candidate:** in `RecurringSeriesEditApplication.accept` (same locked SERIALIZABLE, fingerprint/CAS-checked transaction that commits recurrence + structure), when `owner=event` and `get_self_event_recurring_first_by_source(actor,source)` is populated, obtain the existing first occurrence's canonical civil date. Evaluate the new recurrence candidate for that specific date via the existing canonical calendar evaluator. If the new state has a first-date candidate, add an idempotent, owner-scoped **structural exclusion for the new recurrence state** via `OccurrenceApplication.exclude_in_session`, unless the same coordinate is already excluded by the protected matching set. This exclusion prevents *new* first-day materialization under the revised state; original physical Event, original Schedule, previous registered facts and future dates remain unchanged. Native recurring Events and later/from-next revisions (no first-day candidate) are unaffected; no UI hide/dedupe or destructive delete.

**Test strengthening:** existing DB regression still checks the original Event's identity, title, original Schedule and its placement lock. After the new revision, checkpoint 2 days and assert *only one* original or expected/generated first-date item; assert exactly one future scheduled Event with updated title. Checkpoint again using a **different operation ID** and assert first-day cardinality, original Schedule and future Schedule identity remain stable. E2E `V2-P3-EFIRST` uses a separate seeded account, edits `Questa e le successive` on the physical first Event via the real UI, changes title and agenda, then asserts both canonical and DOM first-day cardinality, the *original physical Event's persisted edited Agenda*, and future title. The original Agenda check intentionally prevents a false green if removing the duplicate simply leaves the old first Event with obsolete Agenda contents. **Code and tests are NOT YET EXECUTED** on owner WSL. The first decisive command is the two-case PostgreSQL test; use single-browser Chromium E2E only after it turns green. Preserve branch documentation and all original invariant assertions.

---

## 2026-11-10 — First Event duplicate reported after one-off→series and edit

**Manual visual evidence:** two orange Event cards on **2026-11-10 11:00–11:30** with the same title `asd`, one containing `Scaletta 1` and one without. Treat as a plausible **first-day duplicate**; screenshot alone cannot establish whether the duplication is in canonical SQL-backed Timeline or Web rendering, and provides no Schedule refs. This must not be declared fixed because `V2-P3-E01` passed: that journey edits original first Event using **Solo questa**, then edits the series only from a later date. It does not test **Questa e le successive from the original first Event**.

**Why previous integration missed it:** `test_existing_event_keeps_first_event_and_excludes_duplicate_occurrence` verified that the linked one-off Event's original Schedule identity and updated title survived a `this_and_following` series edit, but **did not checkpoint the revised recurrence again before examining the Timeline**. The first recurring Occurrence is linked to the original Event; replacing recurrence state can yield generated state/placement materialization that is not exercised by a read-only assertion. The exact underlying cause remains unconfirmed until the new test is executed.

**New targeted regressions (NO PRODUCT FIX YET):**
- After series `accept` in the existing PostgreSQL test, call a fresh 2-day `RoutineOccurrenceMaterializationApplication.checkpoint_window`, then assert exactly **one** physical/expected first-date Event row across the original Event and the converted Event source, requiring the original Schedule identity; run for both locked and unlocked original placement.
- Add `V2-P3-EFIRST` Chromium scenario: create one-off Event with agenda, convert from its Edit screen, edit **Questa e le successive on the original first day**, modify title and agenda, accept confirmation, trigger fresh Home checkpoints and full reload; assert one **canonical Schedule and exactly one DOM card** on the first date, no old title, next-day occurrence updated. Distinguishes duplicated persistent data from UI-only duplication.
- Keep `V2-P2-E04` (finite native Event series) as a **separate** case: older 3-browser run showed different failure stages depending on browser, not evidence of the user's screenshot being caused by that scenario.

**Quick diagnostic sequence:** Run only the named existing PostgreSQL test `test_existing_event_keeps_first_event_and_excludes_duplicate_occurrence` with `-m postgres`; if green, run only `V2-P3-EFIRST` on Chromium (`--project chromium --v2-workers 1`). If RED, retain exact failing trace/SQL assertions and repair the affected product vertical, not the expected count. No full 306 test gate until these are green. A manual user test is unnecessary at this stage because the screenshot already reproduces the symptom.

---

## 2026-11-10 — P3-A01 root cause identified: PostgreSQL Objective numeric overload (RED-to-candidate repair)

**Owner's exact failing PostgreSQL evidence:** `test_converted_activity_with_two_intervals_materializes_next_day[area_two_numeric_objectives]` failed in 7.29s (previous `intervals_only` passed). The inner exception is **`psycopg.errors.UndefinedFunction` (SQLSTATE `42883`)** at `routine_occurrence_materialization.py::_create_objectives` during `dante.create_self_temporal_objective(...)`. Psycopg reported argument 10 as **`double precision`**, but the migration `20261006_113_b14_reality_objectives.py` declares `requested_target_value numeric`, `requested_target_min numeric` and `requested_target_max numeric`; PostgreSQL has no matching overload for the supplied positional argument types. The recurrence routine template converts JSON numeric targets to Python `float`. Without an explicit cast the SQL function invocation resolves `double precision` and fails. Existing earlier two-interval checkpoints with NO Objectives never exercised this branch, so they were correctly green but insufficient. The resulting internal `OccurrencePersistenceError` was transported as `HTTP 503 temporal.occurrence.persistence_unavailable`, explaining the E2E and manual Timeline warning despite existing cards remaining interactive.

**Minimal source fix:** both branches of `RoutineOccurrenceMaterializationApplication._create_objectives` (concrete Activity/Event and direct Occurrence) now invoke their canonical DB functions using **`CAST(:target_value AS numeric)`, `CAST(:target_min AS numeric)`, `CAST(:target_max AS numeric)`**. No schema migration, modification of Objective semantics, skipping, exception swallowing, or UI warning suppression. The SQL signatures are explicitly defined in migrations `20261006_113` and `20261006_114`. Preserve atomic checkpoint rollback on failed materialization.

**Permanent diagnosis improvement:** source-owned structured `log_event` with event `temporal.occurrence.objective_materialization_failed` records request-correlated `exception_type`, `sqlstate`, `failure_stage=objective_create`, `subject_kind`, `objective_index` and generic error category/code. The logging formatter's deny-by-default allowlist was extended only for these safe coordinates. It must NEVER log SQL text, bind parameters, Activity/Objective identifiers, labels, raw SQL exception messages, authentication or body content. An observability unit regression proves request correlation and redaction. Public response remains a safe generic 503 with request ID; full internal classification belongs in application logs.

**Regression owners:** the same original failed `[area_two_numeric_objectives]` Postgres test is kept untouched and MUST turn green on the fixed SHA; its `[intervals_only]` counterpart must remain green. An existing recurring Occurrence Objective integration test now supplies `10.0` (JSON/Python float) rather than only integer `10` so the second DB function overload is also exercised without changing business target semantics. Run targeted logging `tests/test_observability_logging.py` too. The repair is **PENDING owner WSL verification**; do not mark this bug closed until those tests and a one-browser `V2-P3-A01` pass. Revisit broader temporal persistence failure diagnostics and other E2E bugs separately, with actual source-owned SQLSTATE evidence rather than repeated 3-browser brute-force runs.

---

## 2026-11-10 — Manual confirmation: Timeline remains interactive while checkpoint is RED

Owner reproduced P3-A01 by creating an Activity with two timed intervals, two planned Sessions, selected Life Area, and two numeric Objectives, then converting through Edit. Screenshot `immagine(20261110-082813).png` shows both original Activity interval cards and the functional Inspector still interactable while a `Timeline non disponibile` warning is displayed. **This is a partial refresh failure, not evidence that the Activity disappeared or that the entire timeline is unusable.** Source `apps/web/src/features/temporal/timeline-runtime-boundary.tsx` intentionally renders `{children}` even when settled runtime state is `error`. It first displays a preliminary canonical window, then a five-day priority checkpoint/read, then a full checkpoint/read. A failed checkpoint turns the boundary status `error` while existing rendered cards can remain interactive. Do not hide the alert or substitute imaginary future occurrences: reproduce the HTTP 503.

**New fast test case:** existing `test_converted_activity_with_two_intervals_materializes_next_day` is parametrized with `intervals_only` (original green path) and `area_two_numeric_objectives`. The second case creates an existing Life Area, two numeric Objective definitions (quantity and range), review_on_end for one Objective, retains two intervals and planned Sessions, converts via the same application, then checkpoints the **exact five-day priority span** and 43-day read/replay. Verify Life Area/Objective/Session persistence on a generated Activity. This is only a regression candidate until WSL confirms PASS/FAIL and chained traceback; no production code was touched. For fast diagnosis, run just `::test_converted_activity_with_two_intervals_materializes_next_day[area_two_numeric_objectives]` with `--tb=long`. If backend passes even here, target the authenticated API/UI request path and compare the failing HTTP request with application logs rather than repeat a long 3-browser suite.

---

## 2026-11-10 — P3-A01 precise HTTP 503 boundary and rapid manual triage

**New user-supplied evidence:** `E2E_DIAGNOSTICS.tar(2)(1).gz` collected 18 browser cases on three disposable stacks in **223.96 s** with two workers/stack: **2 PASS, 10 FAIL, 6 ERROR, 0 skipped**, 6 cases/browser. P3-E01 one-off Event conversion passed Chromium and Firefox. P1-A01 Activity edit failed in all three with an explicit UI validation alert `Un obiettivo è cambiato: riapri Modifica prima di salvare.`, so no atomic PUT was sent. P2-E04 and P2-A04 got through several scoped edits but failed to find an expected finite instance later (Chromium/A04-E04 step 8). RT-02 found one dated Activity card whereas the test expected two: do not assume a product error until the canonical Schedule date/identity and the test's previous-day reference are checked.

**Precisely located P3-A01 failure:** The actual signed-in `POST /api/v1/temporal/recurring/activities/{activity_ref}/start` returns **200** in Chromium/Firefox/WebKit, but the **subsequent POST `/api/v1/temporal/occurrences/checkpoint` returns 503**, `temporal.occurrence.persistence_unavailable`. The failing command is a **five-day priority window `2026-11-13 → 2026-11-18`**, not the 43-day background checkpoint. Chrome trace request ID `01a1c265-5dec-7702-be41-ec0b56892bf6`, Firefox `01a1c265-3e4e-7205-8d49-ae26330a01e5`, WebKit `01a1c264-3fac-74b2-a00f-c17fc04d88eb`. Prior checkpoints on the same clean account returned 200 with zero active recurrence sources. After conversion the five-day checkpoint attempts real materialization and fails; the Home view correctly shows `Timeline non disponibile` rather than synthetic cards. The API error masks the internal database cause; HTTP trace alone cannot identify the violated SQL constraint or code location.

**Why direct backend PASS is insufficient:** owner ran the enhanced `test_converted_activity_with_two_intervals_materializes_next_day` on `dfcaa685`: **1 PASS in 10.97 s**, validating 43 calendar days, 86 interval Schedule IDs, replay and physical first identity. But that backend test has **no persisted Objectives or existing Life Area**, while P3-A01 has two Objectives (quantity/range, one review_on_end), a selected existing area, two Sessions and two intervals. The next minimal DB test must reproduce these fields **and the five-day checkpoint after a successful conversion**, capturing the original exception/SQLSTATE. Do not change product code until reproducible cause or user confirmation; do not rerun all browser projects to investigate a backend 503.

**Fast acceptance process:** a single real manual UI test of normal Activity with two intervals, two planned Sessions, existing Life Area and quantity/range Objectives; convert via Edit to daily recurrence; inspect original and next-day Timeline. If the 503 also occurs manually, record the response request ID and backend log, not another huge E2E archive. Distinguish genuine product errors from faulty browser expectations. Chromium-only E2E `--project chromium --v2-workers 1 --grep 'V2-P3-A01'` is only for after a targeted fix, followed by a broader gate once the functional vertical is stable.

---

## 2026-11-10 — P3-A01: green direct PostgreSQL test is not the failing browser journey

**Observed owner result on `240feebc4`:** `test_converted_activity_with_two_intervals_materializes_next_day` passed 1/1 in 8.93 s. Its exact contract created one Activity directly through `TemporalAuthoringApplication` with two interval Schedules and two named planned Sessions, converted with `RecurringConversionApplication.activity`, checkpointed only 2027-01-02 through 2027-01-04 and read the canonical Timeline; the generated next-day two Schedule rows and Session names matched. The test did **not** invoke the signed-in HTTP route, browser Edit Save, two Objectives, assigned existing Life Area, or the 43-day Home checkpoint. It therefore cannot clear the earlier `V2-P3-A01` **Timeline unavailable** failure.

**Test-only enhancement on `90c07e51`:** retain original and next-day Schedule/source assertions, but first checkpoint a three-day priority window, read it, then checkpoint the whole 43-day Home span and replay with the exact same operation ID, followed by a full-window read. Assert exactly two distinct physical interval Schedules for the original first Activity and the far final date; the far date must reference its own generated Activity, not the original or the first future day. This strengthens the DB/materialization boundary without changing any product logic. It still **does not model** HTTP/SPA or inherited Objectives/Life Area; if green, run Chromium `V2-P3-A01` with automatic diagnostic archive to identify the actual failing HTTP endpoint, status, response body and UI read-state before designing a fuller protocol reproduction. No functional fix is approved or claimed from the first green test.

**Next gate:** run only `uv run --locked pytest -q --no-cov --tb=short -m postgres tests/integration/temporal/test_existing_activity_recurrence.py::test_converted_activity_with_two_intervals_materializes_next_day` after pulling the updated branch; then, only if green, `python3 tooling/testing/run_real_stack_playwright.py --project chromium --v2-workers 1 --grep 'V2-P3-A01'` from repository root. Save automatic `E2E_DIAGNOSTICS.tar.gz`. Avoid 100-case/three-browser reruns until the failing stage is identified.

---

## 2026-11-09 — Docker volume safety and single-browser rapid V2 smoke (NOT RUN)

**Owner requirement:** do not accumulate disposable Docker/PostgreSQL volumes during repeated E2E cycles, and do not force three browsers during each small regression fix. The current stack bootstrap `tooling/serve-access-auth-stack.py` previously launched `docker run` from the PostgreSQL 18 image and used `docker rm --force` during failed startup/finally. `docker rm` without `--volumes` can leave anonymous volumes from the image's `VOLUME` declaration on disk, even after the container is gone. Corrected launch to `docker run --rm --detach`; both unsuccessful-start cleanup and unconditional final cleanup now use `docker rm --force --volumes <ephemeral-name>` (ignore already-removed container). These only target the uniquely named E2E container, not local Compose, other named Docker volumes or unrelated data. A structural `--self-test` guard parses the harness AST to enforce both lifecycle/cleanup commands, with no Docker daemon needed. **Past orphaned anonymous volumes cannot safely be attributed or deleted automatically**; inspect separately without global `docker volume prune`.

**One-browser diagnostic mode:** `tooling/testing/run_real_stack_playwright.py` now has explicit opt-in `--project chromium` (also `firefox`/`webkit`). When set it starts *only one* isolated API/PostgreSQL/HTTP stack and records exactly one browser inventory/JUnit, with optional `--v2-workers auto` or `2` for multiple self-scoped V2 tests on that stack. It still creates the automatic `E2E_DIAGNOSTICS.tar.gz`; summary records `selected_projects` and actual stack/browsers. The *default* without `--project` still enforces all three projects for real-stack acceptance and the 27-group gate. Self-test checks single-project inventory parity and refuses any attempt to treat that subset as a full three-browser PASS.

**Use:** for iterative fixes `python3 tooling/testing/run_real_stack_playwright.py --project chromium --v2-workers auto --grep 'V2-(...)'`; for cross-browser acceptance run without `--project` after stable Chromium. The existing user-launched three-browser run does not automatically adopt these source changes mid-flight. **Docker volume safety, new smoke selection and self-test are candidate changes pending a fresh owner run.**

---

## 2026-11-09 — Phase-boundary smoke: 18 RED, guarded adaptive V2 workers (NOT YET RE-RUN)

**User evidence:** automatic `E2E_DIAGNOSTICS.tar.gz` for `--grep 'V2-(P1-A01|P2-E04|P2-A04|P3-E01|P3-A01|RT-02)'`, on three isolated real-stack browser projects. Inventory/JUnit parity: 6 cases/browser × 3 browsers = **18/18 collected, 0 PASS, 9 FAIL and 9 ERROR, 0 skipped**, wall clock **716.48 seconds**. Chromium approximately 699 s, Firefox approximately 713 s, WebKit approximately 693 s. P2-E04 and P3-E01 each hit a 300-second test deadline while waiting for a missing accessible Objective-add button. The failures are strongly reproducible across browsers; no fake green, new skip or 300-second timeout increase is allowed.

**Six distinct problems, shared across browser engines:**

1. `V2-P1-A01`: E01 Activity atomic Edit received no `PUT /atomic-edit` within 30 seconds. Network shows no target PUT at all; the UI displayed `Salvataggio…` at Save click, and Objective definition GETs returned 200. No evidence yet whether the failure is form validation, asynchronous preprocessing, or product save; report actual UI field alerts and timeout within 15 seconds on the next run without claiming a product fix.
2. `V2-P2-E04` and `V2-P3-E01`: recurring Event series editor renders **`＋ Aggiungi obiettivo`** while the approved other editors and driver use **`+ Obiettivo`**. The last trace action is a click awaiting that missing button. Corrected the actual recurring-series editor copy, preserving the Objective add function and the original full-flow assertions; introduced V2-only bounded 15-second per-action deadlines so any other absent UI target identifies itself promptly.
3. `V2-P2-A04`: one routine-generated Activity passed its actual Timeline placement read (one physical Schedule card) and its Objective/Session assertions, but the test incorrectly demanded one `role_code=interval` in an edit snapshot whose base placement is encoded as an **envelope**. The replacement retains exact physical cardinality and asserts that each Timeline `schedule_ref` is represented exactly by an envelope/interval snapshot Schedule. This is a stronger cross-readback identity check, not acceptance of a missing Schedule.
4. `V2-P3-A01`: after one-off→routine conversion, the UI displayed **`Timeline non disponibile`** and `data-temporal-read-state=ready` was absent, even though a timeline HTTP request had completed with 200. This remains a **real unresolved runtime/readback issue** until the backend read/response and full trace establish why the SPA rejected the state. Improved `openHome` diagnostic includes actual read-state and visible alert text; do not mask it by bypassing UI or replacing the canonical state assertion.
5. `V2-RT-02`: test expected a single card from `ACTIVITY_CASES[0]`, which deliberately has **two physical Activity intervals**. Now assert both distinct Schedule IDs and execute session controls against one card while still requiring exactly one canonical active Session and its pause/resume/stop persistence.

**Throughput/isolation fix:** the user correctly observed that `--workers 3` was **three browser *stacks*** but within each project Playwright still had `--workers=1`. The real-stack wrapper now supports an **opt-in `--v2-workers 2`** or **`--v2-workers auto`** (1 or 2 based on CPU and WSL MemAvailable): enables `--fully-parallel` **only with strictly V2-only `--grep` selection**. V2 tests seed disjoint self-scoped user accounts and do not intentionally stop PostgreSQL; higher parallelism is forbidden for mixed/legacy selections or the serial fallback because other auth tests restart PostgreSQL. Two workers per project × three isolated projects allows **up to six simultaneous V2 tests**, with independent real backend/Postgres per project and unchanged JUnit coverage parity. The automatic archive is preserved; up to six compact network/action traces per browser are included, while **all original traces stay on disk**. Self-test now guards invalid mixed selectors, serial fallback and archive retention. This is **not yet proven faster** on WSL and should be benchmarked on the next owner smoke.

**Owner acceptance:** pull a new SHA, `python3 tooling/testing/run_real_stack_playwright.py --self-test`, web TypeScript typecheck, then `python3 tooling/testing/run_real_stack_playwright.py --workers 3 --v2-workers auto --grep 'V2-(P1-A01|P2-E04|P2-A04|P3-E01|P3-A01|RT-02)'` (or explicit `--v2-workers 2` if resource budget permits). Check `REALSTACK_CONCURRENCY`, summary and all JUnit cases; upload only the generated `REALSTACK_DIAGNOSTICS` path. Do not launch all 306 until the phase smoke is green and the unresolved conversion/API problem is diagnosed.

---

## 2026-11-09 — Second 3-browser smoke: Inspector lifecycle timeout and automatic diagnostics (NOT YET RE-RUN)

**Owner artifact:** `ultimo-e2e-log.tar.gz` from the isolated Playwright shard runner, containing three real-stack browser traces, three error snapshots, JUnit and Playwright logs. The run completed in **342.37 seconds**, collecting 6/6 tests: **3 PASS / 3 ERROR / 0 skipped**; Event Objective RT-01 passes on Chromium, Firefox and WebKit. All three P1-E01 cases reached **E01/7 “Delete original; duplicate survives”** after successful creation, atomic Edit and Life Area persistence, cancel-unsaved Edit and duplication. They timed out after 300,000 ms, not on backend deletion but while trying to find the Delete button.

**Actual driver defect:** `deleteOneOff` first opened the original Event Inspector, clicked Delete, cancelled the confirmation and called `assertCard` to assert original still exists. `assertCard` navigates with `openHome`, **unmounting that Inspector**. The old driver then attempted a second Delete click against the now-absent modal and waited until the 300-second test deadline; Firefox call log explicitly identifies the missing `Elimina Event` locator, and all snapshots show both the original and copied Event still present in the Timeline with no Inspector open. This is a **test-driver lifetime error**; a DANTE functional delete defect has not been established. The fix reopens the current Event/Activity Inspector after the preservation/reload check, checks the modal and Delete button with bounded 10-second visibility, then performs the second explicit destructive confirmation. No product semantics, delete assertion or test case was removed.

**No more manual tar:** `tooling/testing/run_real_stack_playwright.py` now always writes `<run-directory>/E2E_DIAGNOSTICS.tar.gz` and prints `REALSTACK_DIAGNOSTICS=<absolute-path>` even after failed shards. It includes the run `summary.json`, each project's JUnit XML, Playwright/build/inventory log and error-context snapshot; a compact copy of up to **three traces per browser** preserves action and network trace data but omits repetitive screencast JPEG frames. The *original full* `trace.zip` files remain unchanged under each browser's `test-results/` and are listed in `diagnostic-manifest.json`, including omitted entries when the matrix has many failures. This limits upload size without discarding original evidence. New `--self-test` assertions verify that the archive is generated on a simulated failure, contains JUnit/log/context/trace, strips only video frames and caps trace copies without deleting originals.

**Next verification:** `python3 tooling/testing/run_real_stack_playwright.py --self-test`, web typecheck and then **only** `--workers 3 --grep 'V2-P1-E01'` (three independent browser stacks). The next accepted result must be **3/3 PASS** with complete explicit delete/cancel and canonical readback; otherwise upload the automatically produced diagnostics file. RT-01 already passed 3/3 in two previous isolated smokes; no reason to repeat it before repairing P1-E01. Do not launch the full 306 until all phase-boundary smoke tests pass. The new SHA is **NOT YET E2E GREEN**.

---

## 2026-11-09 — 3-browser smoke: Life Area atomic Save readback race (3 PASS, 3 FAIL)

**Artifact:** user-provided `e2e-v2-smoke-diagnostica.tar.gz`, containing three JUnit files, three Playwright logs and traces (Chromium, Firefox, WebKit). The prior candidate `bf279b18` completed `V2-RT-01` on **all 3 browsers**: recorded Event Objective read-only Edit, cancellation, explicit deletion and canonical reload. `V2-P1-E01` reached **step E01/5: Reassign area, reload, cancel an unsaved edit** and failed identically on all 3: newly created Life Area absent in catalog (expected one, received zero). All six tests were collected and reported: **3 PASS / 3 FAIL / 0 skipped**, total wall-clock approximately 50 seconds using three genuinely isolated PostgreSQL stacks. Do not conflate this 3-browser smoke with the unexecuted 306-slot full suite.

**Trace-proven root cause:** the driver clicked `Salva modifiche` and immediately called `serverRead('/api/v1/temporal/life-areas')`. In all three network traces, the premature **GET 200 returned the old catalog before the second Event `PUT /api/v1/temporal/events/{ref}/atomic-edit` even started**. Example Chromium: the earlier step E01/4 had completed its atomic PUT with 200; the second Event PUT started only at 20:41:47.282Z after the catalog read and near failure teardown, so its trace contains status -1/no response. The request body was correct for this intended change: `new_life_area.name`, `color_code=#8E24AA`, `expected_assignment_revision=1`. Firefox and WebKit show the same sequence. This is **driver synchronization error**, not evidence that the product rejected the new area.

**Minimal regression repair:** shared test-only `saveOneOffEditor()` now requires the **exact Event/Activity atomic PUT 200** and the existing UI completion state **before any canonical GET**. Both E01/4 and E01/5 use the same contract; it fails with the actual HTTP result, never a sleep, retry or weakened assertion. The test still requires exactly one new Area, the expected color, persisted assignment, correct Objective and Schedule identities, and cancel/discard behavior. No product files, DB migration, test skips or timeouts changed.

**Validation boundary:** pending user-run `python3 tooling/testing/run_real_stack_playwright.py --workers 3 --grep 'V2-(P1-E01|RT-01)'` on the new SHA. Confirm `6/6 PASS` with JUnit and traces before expanding beyond smoke. Full TypeScript/Vitest verification of this SHA also remains pending; earlier 158/158 Vitest was run on an older commit.

---

## 2026-11-09 — E2E throughput and stale shared Create selector (SMOKE PENDING)

**Observed real-stack failure:** the user ran 306 slots directly under a **single disposable PostgreSQL / HTTP server** with `--workers=2`; both concurrent first cases `V2-P1-E01` and `V2-RT-01` timed out at 300,000 ms. The browserContext.close secondary exception is teardown after a timed-out test, **not an identified root cause**. Browser traces under `apps/web/test-results/**/trace.zip` and `error-context.md` are required for definitive attribution. The test source has `test.describe.configure({ timeout: 300_000 })` so the shared stack should not be subjected to all 306 slots before a smoke passes. No PASS is claimed for this run.

**Concrete test-driver defect found by source inspection:** after the product copy changed to **`+ Obiettivo`**, two source-owned browser helpers still targeted `Aggiungi obiettivo`: the *first* Objective in `temporal-user-journey-support.ts / configureCreate`, and every *additional* Objective in `temporal-stateful-journey-support.ts / setObjective`. Both are used by the timed-out v2 Create scenarios. The selectors now match the real accessible name exactly and assert button visibility within 10 seconds, without weakening the Objective creation or server-truth assertions. These commits are **candidate repairs** pending real browser proof.

**Correct run strategy:** `python3 tooling/testing/run_real_stack_playwright.py --workers 3 --grep 'V2-(P1-E01|RT-01)'` creates three **independent** frontend/API/PostgreSQL stacks (one per browser). On PASS, use `--grep 'V2-'` for all 102 v2 cases per browser, retaining isolated accounts, one frontend build and separate JUnit, logs and traces. Never use two `playwright.auth.config.ts` workers on the same stack as a substitute for isolated parallelism; the existing runner owns the safe topology. The full gate must later run on one pinned clean SHA. If the smoke still fails, inspect its actual trace before altering any product semantics or increasing timeouts.

---

## 2026-11-09 — Statefulness: first, middle, finite last and interval identity (NOT RUN)

**Context:** two user-provided WSL runs at `7c2886e0` and `46a8f3d4` returned four component Vitest failures each (the later run: 134 PASS, 4 FAIL), 5 TypeScript compiler errors, and 4 unregistered test files. These results are historical: none of the new code is marked green without a fresh run on its exact SHA.

**Test-only repairs:** updated the historical `Aggiungi obiettivo` button selectors after the owner-approved compact **`+ Obiettivo`** label in Activity/Event/Advanced Create; switched an obsolete accepted-Objective retirement/undo test to a genuinely **unrecorded** Objective (registered definitions remain locked); matched the current accessible Life Area *button* and checked its RGB swatch instead of querying a removed decorative img; corrected strict optional-prop, request-init, Activity settings and Event-only TS narrowing issues. Four omitted files were registered in the canonical test-case registry, not skipped/deleted.

**Added test path and failure boundaries:** P2's **bounded five-occurrence** personas (five per Event/Activity family) now explicitly read and locally edit the *actual last* occurrence, assert no sixth generated occurrence, then verify the modified last remains protected after edits of the first, an intermediate and the following slice. P3 already edits the original physical first after conversion, then a generated middle and future slice; expanded canonical duplicate scans across the first five displayed days. Assertions use a scoped Timeline API read, exact expected title and exact physical Schedule-ref cardinality; they inspect both flat Activity/Event placements and *nested* `placement` of recurring Event Occurrences. For Activity, **one activity_ref with N distinct interval schedule_ref/card values is correct**; duplicates are extra Schedule identities beyond those N or repeated identities. A smoke failure on first/middle/last must not be fixed by reducing the expected count.

**Evidence requirements:** run `python3 tooling/testing/verify_test_integrity.py`; targeted Vitest/TypeScript/format/lint; then discover browser inventory with `playwright test --list`, run 1 P1 + 1 P2 (finite) + 1 P3 + RT per browser, then all 102 v2 tests × Chromium, Firefox and WebKit on disposable real-stack accounts. Keep test.step traces and server response readbacks. Functional product bugs require owner review, not silently changed DANTE behavior.

---

## 2026-11-09 — Visual QA: unchanged Save and independent recorded-result deletion (UNVERIFIED)

The user reproduced two real UX faults in Activity Edit: **unchanged Save** transmitted a structurally empty atomic request and displayed an English backend 422 string; **Elimina registrazione** was blocked by a separately staged Objective addition and its canonical refresh would have erased that unsaved draft. Fix is narrow: no-op Activity Edit closes without network mutation; the atomic API client rejects empty edits locally and maps HTTP 422 to user-facing Italian text; recorded Objective deletion performs the confirmed backend action independently and merges only the affected Objective's canonical row. All other unsaved fields, new Objectives and staged removals survive; Event Edit follows the same independent-delete behavior.

**Regression coverage added (not yet executed):** jsdom Activity no-op with all four accepted Objective kinds, Event no-op with mixed accepted kinds; Activity/Event deletion-confirm flow while one newly added Objective has an empty name, preserving that draft; atomic client sends zero requests for empty edit and never exposes raw 422 text. Existing PostgreSQL and WSL tests from `035b28bc` remain historical **36 unit + 7 PostgreSQL PASS**, not a new green verdict for these changes. This candidate needs the focused web gate and real-app visual recheck before proceeding to parallel E2E.

**Error presentation rule:** technical backend validation details, raw stack traces, SQL diagnostics, and framework messages must not be shown as end-user text. Domain validation belongs next to the relevant field where that field can be identified; concurrency conflicts should offer a clear recovery action, and unexpected failures a short local-language message. Keep structured diagnostics in developer observability, without leaking sensitive input values. The Activity atomic 422 mapping is a local first repair, not proof that all DANTE error surfaces have been audited.

---

## 2026-11-09 — Recorded Objective Edit and converted-first identity candidate (NOT RUN)

**Normative decision:** [confirmed-objective-edit-and-recurring-protection-v1.md](../domain/decisions/confirmed-objective-edit-and-recurring-protection-v1.md). Owner-approved: recorded Objective rows are immutable/read-only in ordinary and local Edit until explicit, confirmed, permanent deletion of the result (not the Objective). Pending state and ordinary Create remain editable. Corrections remain a separate action. Running, paused and finished Sessions, recorded Objective facts and locally edited occurrences protect future-series scope.

**Implementation candidate (GitHub only, no new local gate):** forward-only migrations `20261109_182` and `20261109_183`; authenticated Objective deletion API and Objective-definition write guard; common recorded Objective row/dialog wired through Activity and Event Edit; explicit selected-instance protection in pure scope selection plus PostgreSQL admission; removal of old editable recorded row and duplicate result footer.

**Regressions added/updated:** PostgreSQL self-owner, other-owner, stale CAS, recorded definition lock, corrected result (two observations), irreversible removal and clean re-edit; UI component cancellation, confirmation and unlock in Activity and Event; v2 RT-01 Event real UI→API→reload; pure recurrence selected/future protected reasons and PostgreSQL direct inclusive refusal; P3 real UI local edit of the **physical first converted instance**, physical first Schedule identity preservation and canonical duplicate scans on initial/middle/future dates. Multiple interval Schedule/card rows for a single Activity remain expected, not duplicates. Existing unrelated scenarios are not skipped or weakened.

**Pre-acceptance requirements:** Run Ruff/format/pytest targeted PostgreSQL, Vitest/TypeScript/ESLint, OpenAPI/client generation and Dictionary/schema drift, followed by browser P1/P2/P3/RT and 27-group full gate on the same SHA. The candidate is **NOT GREEN**, and product defects found during real tests still require owner discussion; do not edit unrelated product behavior to satisfy the suite. Some legacy tests may still expect an editable recorded Objective and require a semantic review, never a silent weakening.

---

## 2026-11-08 — Second Chromium RED and isolated parallel execution

Owner's second real-stack Chromium run on `cea61d37` again exposed seven
RED journeys; the stack and PostgreSQL started correctly. The newly deepened
checks uncovered several **driver expectations that did not match product
semantics**. The Home Timeline renders a multi-day window around the selected
date, so a card still visible when navigating to date+1 is not proof that
the card moved, persisted on that date, or propagated a local change. The
journey assertions now use the canonical card `data-planned-date` (alongside
Schedule identity) to target the actual day of each instance. This also
prevents the test from accidentally selecting an original instance when it
intended to edit a future one. Quick recurrence selector values are `custom`
when the user's interval differs from one (or monthly ordinal is selected);
the submitted canonical frequency and interval remain strictly asserted.

The conversion scenario had a five-minute opaque timeout; it now has a
bounded 120-second test deadline and 35-second response-wait limit so the
next failure identifies an unconfirmed conversion POST instead of consuming
the full suite. This is **diagnostic only**, not evidence of successful
conversion.

**Concurrency:** the seven journeys have distinct synthetic user identities
and no shared fixture mutations. The lifecycle `test.describe` now opts
into `mode: 'parallel'`; launch this suite with **`--workers=2`** to
retain a conservative bound against the shared real-stack Auth rate capacity.
Do **not** raise the global `playwright.auth.config.ts` worker count or
parallelize other auth specs until their accounts and mutating database
fixtures are audited. PostgreSQL targeted checks can remain in a single
`pytest` invocation with shared fixture startup.

**PostgreSQL RED / PASS:** the owner's Session-duration progression test
passed. The new hard-delete safety test failed *before* the deletion under
test: its helper passed a null expected policy state to an already-materialized
recurring Activity. The test now reads the canonical policy and, if needed,
performs the self-scoped CAS update. The owner's later clarification allows deleting an Activity with an
open Session after explicit confirmation. The obsolete rejection test has
been replaced with an accepted-deletion/atomic-cascade regression.

**Quality gate:** Ruff reported unsorted `asyncio` import, a `PT017`
exception assertion and a format issue in the new tests. These source-level
findings were corrected; the subsequent user clarification superseded the
incorrect destructive-guard assertion with an accepted-deletion contract.
All subsequent commits are **NOT RUN** on owner WSL. Re-run the seven
Chromium user lifecycle journeys with two workers, then Ruff check/format
and targeted PostgreSQL tests; inspect any remaining RED at its exact step.

# Temporal user lifecycle — authenticated journey matrix

**Scope:** Activity, Event, recurring authoring, Session, Objectives, Life Area,
B14 Create/Edit, recurring structural edit, duplication and hard deletion.

**Runtime:** Playwright authenticated HTTPS stack and migrated PostgreSQL,
using the existing playwright.auth.config.ts. These are not fixture-only
layout tests. Every scenario has a separate synthetic test account.

## Automated scenarios

| ID | User workflow | Server/persistence checks |
| --- | --- | --- |
| UJ-01 | Create one-off Activity → Edit title → Duplica → cancel delete → confirm delete → reload | Distinct Activity/Schedule identities, changed profile, original 404, duplicate persists |
| UJ-02 | Same one-off lifecycle for Event | Event profile, accepted delete, independent Event/Schedule and retained duplicate |
| UJ-03 | Recurring Activity: daily, every 2 weeks, monthly day, monthly ordinal, yearly, custom every 3 weeks with count=4 | One source per configuration, HTTP recurrence family/range, Routine inventory after reload |
| UJ-04 | Recurring Event: daily, weekly, all-day every 2 months, monthly ordinal, yearly, custom every 2 weeks with count=3 | Source and recurrence HTTP identity, materialized Timeline after reload |
| UJ-05 | Existing one-off Activity and Event → Edit → Ripeti daily → Save → reload first and next day | Exactly one Start POST per item, first identity unchanged, next occurrence materializes |
| UJ-06 | Recurring Activity → local edit → edit selected+following → preview/confirm → delete one instance → delete series | No propagation of local title, correct series revision, deletion scopes and future survival |
| UJ-07 | Same local/following/deletion journey for recurring Event | Own Event identity, scoped revisions, next instance unchanged until series update |

The recurring matrices exercise **12 UI configurations** (six per subject).
The complex Activity includes a new Life Area, placement protection, an
untimed planned Session and an Objective with numeric target and unit.
The complex Event includes a new Life Area, placement protection, a
Scaletta item and a boolean Objective.

Seven tests are executed for Chromium, Firefox and WebKit: **21
isolated real-stack browser executions** in a complete run. E2E seed
accounts 81–101 are reserved for this matrix (Chromium 81–87,
Firefox 88–94, WebKit 95–101); the existing accounts 1–80 are unaffected.
Every title uses a new UUID suffix to avoid false comparisons.

## Evidence and limitations

Successful tests must pass a real sign-in, browser UI actions, authenticated
HTTP acceptance and fresh canonical reads or Timeline reloads. A screenshot
or DOM-only test does not prove persisted behavior. The suite does not mock
fetch, fabricate Occurrences or force successful responses.

The conversion of an already edited item into a recurring source currently
uses two separate backend transactions (Edit, then Start). A green browser
journey does not imply these form a single database transaction.

## Data-consistency checks added after first Chromium run

The first owner execution at `122c6a42` failed 7/7 journeys **before** lifecycle
acceptance, in two shared test-driver assumptions: the actual expanded Create
surface is `advanced` (not `full`) and hard-delete confirmation is a
portaled `alertdialog` with the action `Elimina definitivamente`.
These two test-driver contracts were repaired; no production feature was changed.

The seven existing paths now also check the following invariants across
successive authenticated Timeline loads and backend checkpoints:

| Transition | Consistency assertion |
| --- | --- |
| Cancel one-off hard delete | The original Activity/Event is still persisted in the canonical profile endpoint, not just temporarily shown in a stale card |
| Delete one-off, keep duplicate | Original returns HTTP 404 and is absent after day+1 checkpoint and return to day; duplicate keeps a distinct Schedule and persists unchanged |
| Daily recurring Create | Only one matching future card is materialized; future Schedule identity differs from first when available, is stable after revisiting earlier dates, and the advanced first/future Activity/Event cards retain the same named Life Area |
| Existing one-off → daily recurrence | Physical first Schedule identity survives; day+1/day+2 have distinct future Schedule identities; returning to earlier day does not duplicate or replace either |
| Local edit vs following-series edit | Changed local title does not propagate to day+1/day+2; a later series revision must not retroactively rewrite that local earlier occurrence |
| Delete one recurring instance | The deleted occurrence does not resurrect when materializing later dates and returning; following occurrences remain present until explicit whole-series deletion |

**Time semantics are tested in two distinct ways.** Browser navigation through
`dateAfter(day, 1/2/3)` triggers genuine authenticated backend Timeline reads
and recurrence checkpoints. This models **calendar progression**, but **does
not advance the server's actual wall clock**. The additional PostgreSQL test
`test_live_session_time_progression_is_persisted_and_stops_after_end` starts
a live Session at the real current time, verifies its canonical active
duration increases across elapsed time, then stops it and checks that
duration no longer grows. This test does not mock PostgreSQL time.

**Active-Session deletion contract (clarified by user):**
`test_confirmed_recurring_instance_deletion_removes_open_session_atomically`
materializes two recurring Activity instances and starts a real live Session
on one. A read-only preview leaves the Activity and running Session intact.
After the user-confirmed destructive operation, the Activity and its open
Session graph **must both be deleted**, the technical skip must prevent
regeneration, and the other instance must remain untouched. Active execution
is **not a deletion veto**. The new positive-acceptance regression is not yet
run on PostgreSQL.

**Important not-yet-proven consistency contracts:** full first/future equivalence
for Life Area beyond the named daily Activity/Event pair, protection,
planned Sessions, quantitative Objectives, reminders and Event Scaletta;
a green active-Session **confirmed deletion** cascade and untouched siblings;
survival of other recorded facts after series edits; CAS conflicts and retry
after lost network response; DST transition with shared controllable
browser/backend clock; skip/cancel/delete on long-running routine histories.
These must be separately backed by source and test evidence; current browser
suite does not prove them merely by checking title or Schedule identity.

**Future expansion (explicitly deferred):** multiple realistic long-running
persona simulations (professions, objectives, routines and changing user
requirements) using a single isolated deterministic clock shared between
frontend, backend and database. Do not substitute browser-only `page.clock`
for server time in these scenarios.

**Verification:** all new checks above are candidate assertions pending WSL
execution on their exact branch commit. The first 7/7 failures at
`122c6a42` remain the recorded initial RED; do not label this checkpoint green.

## Important gaps to add in the next iteration

| Gap | Required proof |
| --- | --- |
| Lost reply / retry | Start accepted then transport fails, same operation replay/reopen gives one source and first occurrence |
| Simultaneous clock change + conversion | Fresh Schedule revision and matching recurrence wall time on both subjects, reload |
| Concurrent commands / stale CAS | Only one writer wins; no partial changes on rejected profile, placement or preview |
| DST | Nonexistent and ambiguous local time, earlier/later, original identity, future materialization |
| Recorded facts | Real Session/Actual/Objective facts survive selected/following edits; from-next applied correctly |
| Full combinations | Reminder, minimum Session duration, planned timed Session, overlapping and crossing-midnight intervals, Life Area reassignment |
| Calendar bounds | End date, 999 count, missing monthly dates, Feb 29, multiple selected weekdays and mixed month-day rules |
| Deletion audits | Exact deleted row counts, stale delete preview conflict, protected facts, replay and concurrent delete |
| Recurring duplication | Copy chosen occurrence template, not the source or recorded attempts; no unintended link |
| Draft / unplaced | Draft Vault, canonical unplaced Activity, duplicate into draft, re-placement and deletion with recorded Session |

These are open items, not presented as implemented in this matrix. The
existing unit and PostgreSQL suites remain authoritative for finer
invariants they already test.

## Commands

Focused real-stack Chromium, after pulling the branch:

    cd ~/projects/dante
    git pull --ff-only origin feature/timeline-temporal-operational
    pnpm --filter @dante/web exec playwright test \
      --config playwright.auth.config.ts \
      e2e/auth/temporal-user-lifecycle.spec.ts \
      --project=chromium

Run all three browsers by omitting --project=chromium, then run the full
DANTE gate:

    python3 tooling/testing/run_parallel_gate.py --group-workers 5 --postgres-workers 10 --postgres-jobs-per-worker 4

The full gate already executes WEB_BROWSER_REAL_STACK, which includes all
auth Playwright specs. No second runner, no CI dependency.

**Verification: NOT RUN** at this new SHA. Keep Playwright traces and the
exact HEAD for fixing red scenarios; older green UI-only tests are not
evidence for these user journeys.


---

## 2026-11-09 — Approved stateful user-journey v2 contract (OPEN IMPLEMENTATION)

**Status:** user-approved design, **NOT YET IMPLEMENTED/EXECUTED** as an 80-source E2E suite. The seven prior browser journeys and their later incremental extensions do **not** satisfy this expanded contract. A green current gate cannot be interpreted as v2 coverage. Keep this section as the admission/coverage source of truth; additional fields and edge scenarios may be appended without removing earlier assertions.

### A. Test population and controlled scope

- **Phase 1:** create **20 independent one-off Events and 20 independent one-off Activities**, then perform many sequential mutations on **each**, finishing with faithful duplication, deletion and Draft Vault flows where applicable.
- **Phase 2:** independently create **20 native recurring Events and 20 native recurring Activities**, reusing the diversified phase-1 combinations and adding frequency, range and occurrence-specific changes. Do not replace the creation matrix with a single-feature-per-object series.
- **Phase 3:** take one-off Events/Activities (or equivalent rich new one-offs), activate a recurrence through **Edit**, then reuse phase-2 local/following/exception/duplication/deletion logic. Minimum ten converted sources per kind; expand to the full twenty when the reusable journey engine is proven.
- For each kind, scenarios **01–10 are varied multi-feature** and **11–20 are high-density**, with *several* settings per item. The numbers below indicate starting configuration, not the number of operations or final counts.
- Presently **exclude** incomplete **location**, **reminders** and **participants** from mandatory v2 acceptance. When those verticals are complete, append explicit validated scenarios; never introduce hidden skips to make a feature appear covered.
- Subject terminology: **Event** has agenda parts, not Activity intervals/Activity Sessions; **Activity** has intervals, planned Sessions (timed/untimed), live/recorded sessions and goals. Avoid impossible cross-subject fixture fields.
- Life Area color belongs to the shared Life Area and changing an existing area's color is **global**, including previously linked items. Changing an assignment for selected-and-following occurrences is a different operation from globally recoloring an area.

### B. Deterministic creation inventory

Legend: \`L\` = Life Area (none / existing / new); \`G\` = number of Objectives; \`A\` = number of Event agenda parts; \`I\` = number of Activity intervals; \`S\` = number of planned Sessions (timed + untimed); \`D\` = description; \`P\` = placement protection; \`T\` = timed / all-day. Goals mix boolean/quantity/range and verification settings where supported. Every nonempty set receives stable, unique labels, distinct values and a recorded creation order. The actual composer must author all represented fields via UI; test fixtures **must not bypass the UI with database inserts**.

| Event ID | T | A | G | L | D | P | Additional contrast |
| --- | --- | ---: | ---: | --- | --- | --- | --- |
| E01 | timed | 2 | 1 | existing | yes | no | distinct color |
| E02 | timed | 3 | 2 | new | no | yes | quantitative goal |
| E03 | all-day | 4 | 2 | existing | yes | no | range goal |
| E04 | timed | 1 | 3 | none | yes | yes | three goal kinds |
| E05 | timed | 5 | 1 | new | yes | no | alternate area color |
| E06 | all-day | 2 | 3 | new | yes | yes | varied goal verification |
| E07 | timed | 3 | 2 | existing | no | yes | different time zone |
| E08 | timed | 4 | 3 | none | yes | no | cross-day schedule |
| E09 | all-day | 5 | 2 | existing | yes | yes | multi-day range |
| E10 | timed | 2 | 4 | new | yes | yes | mixed target values |
| E11 | timed | 6 | 4 | existing | yes | yes | high-density baseline |
| E12 | all-day | 7 | 5 | new | yes | yes | high-density date span |
| E13 | timed | 8 | 4 | new | yes | yes | reorder agenda |
| E14 | timed | 5 | 5 | existing | yes | yes | change several goals |
| E15 | timed | 9 | 3 | new | yes | yes | delete middle agenda |
| E16 | all-day | 6 | 4 | existing | yes | yes | remove/reassign area |
| E17 | timed | 7 | 5 | existing | yes | yes | conflicting edit |
| E18 | timed | 8 | 5 | new | yes | yes | repeated save/reopen |
| E19 | all-day | 9 | 5 | new | yes | yes | rejection and retry |
| E20 | timed | 10 | 5 | existing | yes | yes | maximal editable mix |

| Activity ID | T | I | S timed + untimed | G | L | D | P |
| --- | --- | ---: | --- | ---: | --- | --- | --- |
| A01 | timed | 2 | 1 + 1 | 2 | existing | yes | no |
| A02 | timed | 3 | 2 + 0 | 2 | new | no | yes |
| A03 | timed | 2 | 1 + 2 | 3 | existing | yes | yes |
| A04 | timed | 0 | 2 + 1 | 2 | none | yes | no |
| A05 | timed | 4 | 1 + 0 | 3 | new | yes | yes |
| A06 | all-day | 0 | 0 + 2 | 3 | existing | yes | yes |
| A07 | timed | 3 | 3 + 1 | 2 | none | yes | yes |
| A08 | timed | 2 | 0 + 3 | 4 | new | yes | no |
| A09 | timed | 4 | 2 + 2 | 3 | existing | no | yes |
| A10 | timed | 3 | 3 + 2 | 4 | new | yes | yes |
| A11 | timed | 5 | 4 + 2 | 4 | existing | yes | yes |
| A12 | timed | 5 | 3 + 3 | 5 | new | yes | yes |
| A13 | timed | 6 | 4 + 3 | 5 | existing | yes | yes |
| A14 | timed | 4 | 5 + 2 | 5 | new | yes | yes |
| A15 | timed | 6 | 5 + 3 | 4 | existing | yes | yes |
| A16 | all-day | 0 | 0 + 4 | 5 | new | yes | yes |
| A17 | timed | 5 | 4 + 4 | 5 | existing | yes | yes |
| A18 | timed | 6 | 6 + 2 | 5 | new | yes | yes |
| A19 | timed | 7 | 5 + 4 | 5 | existing | yes | yes |
| A20 | timed | 7 | 6 + 4 | 5 | new | yes | yes |

**Fixture validity gate:** Before encoding the numbers as executable tests, verify the actual Create authoring constraints for interval length, session placement/overlap, all-day untimed sessions, goal types and maximum counts. A table entry is a **required scenario to implement or explicitly resolve**, not proof that its proposed configuration is accepted by today's domain. If an entry conflicts with documented invariants, replace it with an equally complex *valid* configuration and record the reason here; never skip it silently.

### C. Mandatory multi-step mutation journey for EACH source

1. Persist creation via real user UI. Read canonical complete snapshot (one-off) or source + selected/neighboring occurrence snapshots (recurring). Compare **exact ordered arrays, values, identities and types** against the independently declared scenario state, not against the POST echo.
2. **ADD:** several new objectives / Event agenda parts / Activity intervals / Activity planned Sessions where applicable, with changing quantities, time values and Life Area assignment. Save; read again.
3. **UPDATE:** change multiple existing values (title, description, amount, objective type/verification, agenda wording, interval bounds, session name/timing, Life Area selection/color, event/activity times, timezone when valid). Save; verify *changed and unchanged* properties.
4. **REMOVE:** delete first/middle/last entries, then add replacements, then change another surviving entry. Verify exact count, order, persistent IDs of surviving entities and the **absence** of every removed element after complete reload.
5. **REORDER:** where supported, move goals/agenda/intervals/Sessions, and check exact saved and rerendered order; no phantom rows or stale duplicate references.
6. **CANCEL:** modify multiple controls then X/Annulla; exercise the discard decision, cancel and confirm paths. No changed authoritative values or hidden unintended writes.
7. **EXECUTE/RECORD:** start/pause/resume/stop Activity Sessions, include registered sessions, inspect blocked replan/drag while active and post-stop edit policy. Confirm Objective outcomes and validate persisted evidence; **a confirmed objective must not reappear as an unrestricted editable target**.
8. **DUPLICATE:** reopen the *final edited* source. Composer is prefilled with exact duplicate-eligible values, not initial values. Persist new source with distinct native/Schedule/objective/session identities. Never duplicate live execution, observations or historical confirmations.
9. **DRAFT / DELETE:** move to Draft Vault where supported; verify non-executable state. Cancel and confirm deletion, prove canonical 404/deletion and that surviving duplicates remain unchanged.
10. Repeat complete assertions after reloading Home, reopening the Inspector/Edit, and returning to the same date after navigating away. **Every mutation updates an independent expected-state model and is checked immediately**, not only at journey end.

The operations above are a **coverage contract**, not a directive to force unavailable edit commands. If policy forbids a mutation (recorded session, protected exception), the required test proves the explicit refusal and zero persisted changes; after permitted resolution, it retries the originally requested mutation and checks success. Some journeys reorder operations (REMOVE→ADD→UPDATE, UPDATE→CANCEL→UPDATE, etc.) so the engine cannot pass by always exercising the same happy path.

### D. Native series (40) and conversion series (at least 20)

- Reuse **all 20 per-subject creation configurations** with a recurrence matrix spanning daily, weekly (multiple weekdays and steps), monthly by day and ordinal weekday, yearly, bounded count, end date and custom intervals. Assert the canonical requested cadence/range and materialization over a bounded but representative series window, including first, middle and later dates.
- For **each** series, exercise local instance changes and a selected-and-following revision. The exact selected occurrence **is included**, earlier clean occurrences remain unchanged, and protected local exceptions stay intact. When the selected instance is already an exception, prove the correct **from-next** boundary rather than silently rewriting it.
- Distribute independent local changes across **first / middle / last** materialized occurrences; combine local exceptions before and after whole/following revisions. Confirm the preview enumerates protected exceptions and stable references. Preserve recorded facts, confirmations and Session policy across lawful changes.
- Test repeated scoped revisions, addition/modification/removal of structural fields, duplicate from clean and locally modified instances, delete one instance, delete multiple at different times, delete whole source. Check that a later checkpoint **does not resurrect hard-deleted or explicitly skipped instances**.
- Convert at least **ten one-off Events + ten one-off Activities** through Edit into distinct recurrence modes; rerun the same scoped/local/deletion/duplication proofs. Original physical identity must survive; no duplicate source/first placement.
- For an existing Life Area, a color change propagates **globally** (including past linked items). For a new area scoped to the future, previous unmodified/exception instances must not inherit that *new assignment*. Distinguish these operations in expected state.

### E. Cross-cutting consistency / fault contracts

| ID | Required independent evidence |
| --- | --- |
| INV-01 | Every command is fully atomic; failure after intermediate DB write rolls back all changed fields, linked rows and newly created Life Areas |
| INV-02 | Exact list equality for named nested elements, counts, order and stable identities of untouched items; no duplicates or deleted ghosts |
| INV-03 | Compare UI + canonical API + relevant PostgreSQL persisted facts, using a separate expected-state model driven by explicit actions |
| INV-04 | No unintended retroactive series propagation; selected boundary inclusive; from-next exclusive; protected exceptions not overwritten |
| INV-05 | Execution and outcome history cannot be copied by Duplicate or silently deleted/changed by an unrelated Edit |
| INV-06 | Different browser sessions editing stale revisions produce a conflict, not last-writer-wins loss; replay of same operation ID is idempotent |
| INV-07 | Clock boundaries include midnight, month/year rollovers, February and DST ambiguous/nonexistent local hours with supported zone semantics |
| INV-08 | An error response or network interruption cannot hide partial writes or permit duplicate resources on retry |
| INV-09 | Move/drag and changes during live/paused/recorded sessions follow the actual documented Edit guard and confirmation contract |
| INV-10 | No disabled, skipped, weakened or conditional-only assertions to turn known product bugs green; preserve original suites in addition to v2 |

### F. Execution strategy and evidence

The matrix must be **materialized into actual executable, named test cases**; checking that a fixture list contains 40 rows does not establish behavior. Split into isolated per-scenario journeys, not one monolithic fail-fast test. Each step logs scenario ID, operation number, seed, prior accepted state and exact expected/actual field diff. Separate browser test data/users and PostgreSQL lifecycle; no shared mutable database across parallel browser workers. Prefer deterministic pairwise coverage plus bounded reproducible adversarial sequences (recorded seed), never an unrepeatable random walk.

Run local small tests and targeted PostgreSQL first, then targeted real-stack flows, then the entire 27-group gate on the **same commit**; record exact PASS/FAIL/SKIP, total inventory and elapsed time. Four previously known WebKit skips are **open inherited coverage gaps**: do not mistake them for the four formerly failing tests or claim 0 SKIP until genuinely exercised.

**Acceptance rule:** each entry in the matrix must have a linked executable scenario, concrete UI/API/DB assertions and a green run on the exact candidate commit. Missing or unrun cells stay OPEN. Future feature additions may extend the matrix without weakening or deleting existing assertions.


## 2026-11-09 — Stateful v2 executable candidate checkpoint (RED allowed, NOT RUN)

**Evidence caution:** The approved matrix above is the requirement, not a green test report. This checkpoint added executable Playwright cases to the existing suite but has **not run typecheck, Prettier, Vitest or real-stack Playwright at this SHA**. A run that has failures is a RED baseline to repair, never evidence of a green product. Do not disable, skip, mark \`test.fail\`, or narrow assertions just because an existing bug is expected.

### Files and current implementation

| Source | Concrete coverage |
| --- | --- |
| \`apps/web/e2e/auth/temporal-stateful-case-matrix.ts\` | Typed 20 Event + 20 Activity initial configurations with multi-feature variation and recurrence families |
| \`apps/web/e2e/auth/temporal-stateful-case-matrix.test.ts\` | Unit guard that population, goal kinds, recurrence families and synthetic user-account partitions cannot silently shrink |
| \`apps/web/e2e/auth/temporal-stateful-journey-support.ts\` | Real UI Create through advanced composer; independent expected-state builders; authenticated Life Area fixture creation; canonical Objectives, Event agenda and Activity plan readback |
| \`apps/web/e2e/auth/temporal-stateful-personas.spec.ts\` | 100 distinct tests per browser: P1 40 rich one-offs, P2 40 rich native series, P3 20 conversions. They chain CREATE, reload, nested edits/add/delete, Life Area, local/following/from-next scoped edits, exception boundaries, duplication and deletion. A subset also covers Draft Vault (Event copy versus Activity move) |
| \`apps/web/e2e/auth/temporal-stateful-runtime.spec.ts\` | Two further tests per browser for confirmed Objective evidence in Edit and a real live Session with Pause/Resume/End and Edit guard |
| \`tooling/run-access-auth-stack.py\` | Increases E2E seeded accounts 101→407: 1–101 untouched, 102–401 reserved for 100 personas × 3 browsers, 402–407 two runtime guards × 3. Never share a mutable account across parallel cases |

The E2E inventory adds **102 tests to each browser project** (306 browser slots). Previously existing test cases are retained. Total discovered slot counts and skip behavior must be verified using \`playwright test --list\` at the exact candidate SHA; the registry count is not a substitute for actual discovery.

### Known RED / diagnosis linking

- **\`V2-RT-01\`**: the user observed a confirmed Objective still presented as a mutable target in Event Edit; the test confirms an actual objective via the Work panel, then requires the original observation to remain and the ordinary Edit name input to be disabled. If the product is still broken, the latter assertion must be RED, with captured screenshot/trace. The same contract must later be generalized to Activity and recurrence outcomes.
- **\`V2-P2-E*\` and \`V2-P2-A*\`**: a native series's following editor must allow writing a new Life Area with color and changing the appearance of a preexisting shared area. UI → acceptance → catalog and future instances are checked. A known broken picker is a real test failure, not an exception.
- **\`V2-P1-*\`**: nested goals/agenda/planned Sessions are added, updated, removed and replaced across real Edit transactions; exact ordered readback, surviving identities, eliminated ghosts and faithful duplication are required. Some rows may be RED due domain gaps or inaccurate test drivers; classify with step-specific browser evidence.
- **\`V2-P2-*\`**: tests must prove selected-and-following includes the selection; locally protected instance must stay unchanged; \`from_next\` excludes its selected boundary. They recheck the canonical source snapshot, neighboring cards and original exception.
- **\`V2-RT-02\`**: timed near-current Activity with live capture must honor Session state/recorded facts, plan guard and Pause/Resume/End history. Do not simulate time progression with a mocked browser clock while the backend uses real time.

The Playwright \`test.step\` path combines **phase + persona ID + operation index**, e.g. \`V2-P1-A13 / 4 Edit, remove and add nested data\`. A RED fix requires the exact SHA, scenario ID, step name, browser, expectation mismatch, canonical HTTP result and trace, and a corresponding focused regression proof. \`testInfo.attach('scenario')\` provides the initial scenario JSON. Do not derive independent expected truth from observed API state: it is derived from the declared actions and updated on each accepted transition.

### Still OPEN and not to be misrepresented as complete

- Full cross-product of **twenty normal-source conversions per kind** (current P3 10 per kind) and different conversion frequencies (candidate P3 uses daily).
- Fully varied **multiple independently verified edits to every one of the 40 entities**. P1 currently has a dense initial create and one substantial mixed edit plus Life Area, cancel, duplication and deletion; the user-approved requirement explicitly calls for more repeated sequences, removals and reorderings per item.
- Recursive variation of **interval resizing and removal**, timed planned Sessions and their clock setting, verification mode mutation, multi-objective recorded history on both subject kinds, physical drag/move protection, full Draft Vault edit/re-authoring and result correction.
- **True concurrent browser writers with stale revision**, mid-write rollback injections (except previously authored specific PostgreSQL integration), lost network reply and replay, full DST/fold/gap/window matrix, protected recorded future instances, late materialization across months/years and all-day edge cases.
- Conversion+local+following target mapping and structural validation on both Event and Activity need real browser execution; the test code is not the proof.

### Local qualification order

First confirm checkout and a clean worktree; then format/lint/typecheck and the small inventory test. Next run one case from every phase plus the two runtime guards with one browser on isolated real-stack, keeping all failures and traces. Repair **test driver only if it mismatches the documented production UI contract**, and repair product code when real UI→API→DB fails; both require a new regression. Repeat focused tests, then the full v2 suite in Chromium/Firefox/WebKit with isolated stacks, then the complete gate on one SHA. No merging until the user has the all-green full gate and visual walkthrough, and no claiming GREEN for unexecuted test steps.

**Do not enable v2-only skips** to keep the older gate green. Every test in \`*.spec.ts\` is included in the normal real-stack Playwright inventory. The extra cost is intentional; schedule/batch with bounded parallelism while isolating backend and PostgreSQL stacks. Keep all reports, durations and original assertions.


## 2026-11-09 — v2 first real-stack smoke baseline (RED; 2289fdbc)

Source: user-supplied \`V2_SMOKE_20261109_180205.tar.gz\` (Playwright JUnit, logs and traces, Chromium/Firefox/WebKit). Exact tested SHA: \`2289fdbc1608193e1d8e7566bcee16746b111101\`. The 27 selected browser tests were discovered and recorded without skips; **6 passed, 18 assertion failures, 3 Playwright errors** (per browser: 2 pass, 6 fail, 1 error). Prettier/TypeScript/ESLint and the five persona inventory Vitest tests passed. The 6 passes are \`V2-P2-E01\` and the preexisting standalone conversion journey, each in all three browser projects.

Do **not** treat 21 red results as 21 different product bugs. Trace-backed classification:

- \`P1-A01\`/\`P3-A01\`: canonical planned Session name is \`display_name\`, not \`name\`. Actual persisted names match the independently declared fixtures. Test-driver issue.
- \`P2-A01\`: precisely two interval Schedules belonging to one Activity on the same date, at 09:10–09:50 and 10:20–11:20. The original test erroneously assumed one physical card per Activity; cardinality must derive from the declared interval count, and their unique Schedule IDs must be verified. Test-driver issue; *not* proof of duplicate creation.
- \`P3-E01\`: conversion preserves the first physical Event while future occurrences use the dedicated recurring Event source, as reported by \`GET /recurring/events/{original}/seed\`. The test incorrectly filtered future canonical occurrences by the original nonrecurring Event ref. Preserve the separate first-Schedule identity assertion.
- \`P1-E01\`: the driver navigated away approximately 75 ms after pressing Save, with no successful Event edit mutation visible in the trace. Await UI's successful save acknowledgement **before** reloading; until rerun, do not attribute this to a product bug.
- \`RT-02\`: malformed checkbox CSS selector prevented exercising any live Session behavior. Test-driver issue.
- Firefox \`RT-01\`: the same Life Area label appeared twice because typing before asynchronous catalog resolution could stage a second new Life Area; explicitly click the existing catalog option in the composer. This is a fixture-driver race; it is **not** evidence of product duplicate-card behavior.
- Chromium/WebKit \`RT-01\`: confirmed Boolean observation persisted, and Inspector showed the registered result and the \`Correggi risultato\` control, **but** the original goal's \`Nome obiettivo\` field remained enabled in Edit. **Open functional/UI decision:** must the entire goal definition be locked after confirmation, or only immutable recorded results shown with explicit correction? Do not change DANTE or weaken the assertion without user agreement.

Technical-only changes following baseline: \`7deb43ee\`, \`bbb444b7\`, \`01bca639\`, \`4ffa40f4\`, \`daa2ea89\`, \`911450df\`, \`616aced1\`. These modify only the two new Playwright helper/spec files; they have **not yet been run through CI or the local real-stack test gate**. Never mark them green based on code inspection alone.

**Distinct undisclosed-to-suite regression:** manual report says that editing the first instance after converting a one-off to a recurrence can create a duplicate card. The initial v2 P3 journey exercises modifications on later instances, not an independent edit of the original first instance. The current run cannot prove that the suite detects the manually described trigger. Preserve the original P3 test as a separate baseline and extend generic first/middle/last identity and materialization checks after the blind baseline is completed; never silently claim it already caught this.
