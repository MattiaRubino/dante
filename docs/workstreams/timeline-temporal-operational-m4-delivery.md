# B14 M4 — Full Inspector, edit and faithful duplicate delivery

Date: 2026-10-08. Branch: `feature/timeline-temporal-operational`.

## Delivery policy

M4 is **one integrated delivery**, not a chain of tiny gates. Do not request a separate local test after each component. Changes must be source-backed, then pass **one complete user-local verification** for backend/catalog/client/Web/UI. No GitHub Actions or CI.

### Prior foundation and M3 handoff

M1 scoped profile and M2 Objective edit/history are user-verified. M3-A `20261008_127` ownership, nullable primary Life Area, planned Session display name and historical retirement veto are green. M3-B Web and negative series-scope safeguards are also green (36/36 focused Vitest and earlier PostgreSQL regression).

**Explicit unfinished feature, not hidden in the word “closed”:** `Questa e le prossime` is not supported for primary Life Area or planned Session labels. It is guarded as instance-only. It remains a separate **B14 source/template parity obligation before final B15**; moving to M4 is a scheduling decision, not a claim that this global behavior exists. M3's already-built owner/editor functionality is otherwise delivered and should not be repeatedly reopened.

### Current M4 candidate, not yet user-test-verified

- `event-duplicate-seed.ts` builds a new Event Create draft using canonical persisted Timeline Schedule placement, Agenda, primary Life Area and expected Participation. It retains date-span exclusive-end semantics, coarse period and supported floating/named-zone local interval. Unsupported absolute-instant Create representation and subminute precision explicitly fail closed; it never copies Event identity, history, Actual, Observation, Evaluation or operation IDs.
- `event-inspector-actions.tsx` loads Event Agenda and current expected participants from owner-scoped APIs, resolves participant Person labels, refuses a missing referent, and invokes the existing Create duplicate request. `timeline-overlays.tsx` routes the accepted Event placement through Inspector, alongside existing Agenda editing.
- Existing Activity `Duplica` is **guarded against silently dropping displayed Sub-Activity content**; a structure that cannot be fully represented is rejected instead of being copied incompletely.
- Focused Vitest: new Event duplicate seeds, Event Inspector asynchronous participation/ownership, Activity child-count refusal and canonical Event life-area read.

### Required M4 completion before acceptance

1. **Full Event Inspector/Edit parity:** persisted title/description/location/color, Life Area, Agenda and expected Participation state; safe current-identity edits with owner, immutable operation/revision, CAS and expected-fact protections as needed; avoid duplicating B03/B09 endpoints.
2. **Activity duplicate fidelity:** ensure persisted hierarchy/children, true plan/occurrence provenance, relevant Objective and policy definitions can be reconstructed, or explicitly block unsupported cases without silent loss; never copy recorded execution, Observation or authority.
3. **Event duplicate fidelity:** source Event/Occurrence distinction; canonical Schedule temporal form, Agenda, participants, Life Area and recurrence policy where supported; no unintentional one-off reduction of a recurring template. Resolve remaining fields and their authoritative reads.
4. **Whole integrated gate**: generated OpenAPI/Orval deterministic, backend/PostgreSQL/Dictionary catalog/ACL, Web typecheck, complete relevant Vitest, real-stack click-through afterwards. User runs tests from `~/projects/dante`, no CI.
5. End-to-end product visual and keyboard acceptance remains M5/B15, not an automatic result of M4 green tests.

**M4 status: in development, unverified.** Do not describe the Event Duplicate candidate as full Inspector/Edit/Duplica parity until the remaining contract is delivered and the user-local integrated gate passes.

### Current M4 added regression

`timeline-authoritative-event-hydration.test.ts` now checks that the Event Inspector receives the **canonical persisted placement** passed from the Timeline projection rather than constructing a new placement from display-minute geometry. The focused M4 test set additionally includes `event-duplicate-seed.test.ts`, `event-inspector-actions.test.tsx`, `activity-inspector-actions.test.tsx`, and `remote-event-agenda-data-source.test.ts`. No results claimed until a single integrated M4 user-local gate.

## 2026-10-08 — M4 whole-block candidate assembled; ONE user-local gate outstanding

The M4 Event post-create edit/duplicate vertical is assembled on the GitHub branch. This entry **supersedes the earlier incomplete-M4 candidate cursor**; no local tests are claimed for the newly added code. New canonical `20261008_128_b14_m4_event_profile.py` (only one Alembic `_128` revision) owns immutable Event metadata revision history, actor/CAS/replay, with an explicit no-unscoped-recurring-source edit veto. The Event read exposes a canonical profile revision. `event_api.py` accepts guarded Event metadata edits. Event Inspector now supports metadata Title/Description/Location/Color, existing B03 Agenda, B05 Life Area and B09 Participation owners without forging replacements for them. One new integration test `test_b14_m4_event_profile.py` covers owner, CAS, replay, history and current read.

Event Duplica uses canonical persisted Schedule placement and per-Event details, Life Area and expected participants. The Event DST disambiguation now retains the resolved earlier/later fold; cross-fold, invalid clock precision and absolute forms without faithful Create representation are rejected, never silently normalized. A new owner-scoped `remote-event-recurrence-guard.ts` checks the authoritative Event Recurrence before Duplicate, and explicitly blocks unfaithful template-to-one-off conversion; unresolved participants likewise block. Activity Duplica checks authoritative persisted child count and occurrence provenance, not just displayed subitems, and refuses structures/series that cannot be fully reconstructed, preserving all existing Actual/Observation/Evaluation/Session history. These refusals are **known capability limits**, not claims of full copying of complex trees or series.

**Canonical DB target _128:** 235 tables, 5 views, 210 routines, 103 triggers, 479 indexes, 416 FKs, 587 CHECK. Dictionary scope/routine/table and exact current catalog expectations are updated. Backend+Web tests added/extended; OpenAPI/Orval generation for the new Event profile endpoint still needs publication from user-local checkout, not a manually authored generated client.

**Single consolidated verification:** user runs `bash tooling/verify-b14-m4-local.sh` in `~/projects/dante`, with PostgreSQL, Ruff, unit, API export/client determinism, TS and relevant Vitest. Logs and concise result codes remain visible; the script conditionally publishes **only** verified generated client files after all gates pass, with no CI/Actions. If red, fix all real failures before another whole-block gate; no micro-gates. M4 is **candidate / awaiting this one local gate**, not green. Then perform M5/B15 real-UI click-through; the separate M3 global `Questa e le prossime` owner-source policy for Life Area and planned Session labels remains an explicit B14 parity debt before B15. No misleading "fully complete" claim.

## First user-local M4 gate and consolidated repair

The user ran the whole gate after pulling `244ecaef`: `PULL=0`, `SYNTAX=0`, `UNIT=0`, `POSTGRES=0`, `GENERATE=0`, `GENERATED_CHECK=0`, `API_TYPECHECK=0`; `RUFF=1`, `WEB_TYPECHECK=2`, `VITEST=1` (66/67). The failures were two import-format violations, invalid Testing Library `exact` options and optional fetch-init access in tests, plus an Event Agenda test tied to one of two existing Italian label variants. The repair changes only these five source/test files and no canonical schema or runtime behavior. Local Ruff and Web typecheck pass; the same 12-file Web selection passes 67/67. The user's generated client remains uncommitted until the **single complete M4 gate** is green on the updated branch; do not count the repair-only local checks as PostgreSQL or visual acceptance.

## M4 integrated technical gate GREEN; M5 visual acceptance next

The user pulled the repair `06e4b7a7` and reran `bash tooling/verify-b14-m4-local.sh` in `~/projects/dante`. All ten gate results were zero: `PULL`, `SYNTAX`, `RUFF`, `UNIT`, `POSTGRES`, `GENERATE`, `GENERATED_CHECK`, `API_TYPECHECK`, `WEB_TYPECHECK`, `VITEST`. Log directory: `/tmp/dante-m4-whole.5cpYvA`. The gate committed and pushed exactly seven generated OpenAPI/Orval client files as `77968de6` (`M4_CLIENT_PUBLISH=OK`). The M4 implemented Event Inspector/edit/duplicate and guarded Activity duplicate **technical scope is user-verified** against `_128` and the generated API client. Do not rerun this technical gate without a concrete regression or code change.

The next pass is one integrated real-app M5 walkthrough: Event Inspector metadata/Agenda/Life Area/expected participants, faithful Event duplicate into a new Create draft, Activity Inspector/edit/duplicate, recurrence scope and explicit unsupported-case refusals, then reload to compare accepted state with Timeline. Check desktop layout, narrow viewport, keyboard close/focus and validation feedback in the same pass. Record visible defects with screenshots before B15. Unsupported complex hierarchy or recurring-template duplication remains a deliberate refusal, and `Questa e le prossime` for primary Life Area and planned Session labels remains an explicit global B14 debt; the green M4 gate does not resolve either.

## 2026-10-09 — M5 Session editor, validation and Objective Inspector repair candidate

User real-app screenshots exposed three defects after the green M4 technical gate: Edit's planned-Session clock controls inherited broad Timeline input/button styling, Create showed an English range paragraph with a misplaced section-wide red outline, and entering a numeric Objective observation in Inspector opened the error boundary. The Web candidate excludes the shared Session clock controls from those broad editor selectors, removes the Edit-only offset, localizes the bounded structure message, and targets the invalid Session's date/time row. Numeric Objective input now snapshots the DOM value before React's deferred state updater. A dedicated Inspector regression records `8 km`; targeted Create validation checks outside-range and reversed Session times, and a form test confirms the inline Italian error and precise invalid row.

Coding-workspace proof: Web typecheck, changed runtime/new-test ESLint and four focused Vitest files (54 tests) pass. The older Create entry test file has pre-existing ESLint violations and was excluded from this lint command; its tests are included. No user WSL run, real-app visual proof, or PostgreSQL proof is claimed for this candidate. Alembic `_129/_130` untimed planned-Session persistence and Docker-assigned acceptance port are already on branch HEAD `ec648022`, but their user-local PostgreSQL/catalog gate remains pending. M4 stays technically green, M5 remains open, and B15 parity debt for `Questa e le prossime` Life Area/planned Session labels remains unchanged. Run one consolidated affected gate after publication; no CI or extra M4 gate.

## 2026-10-09 — User-local M5/untimed acceptance gate, Ruff repair pending

After pulling `b1b74c6d`, the user's WSL gate reported 13/13 PostgreSQL integration and exact-catalog tests passing on `_130`, Web typecheck passing, and 54/54 focused Vitest tests passing. Ruff alone reported four style violations in `test_b14_u2_authoring.py`: literal dict, compound assertion, and two intentionally naive datetimes for floating-local placement. The focused repair preserves test semantics and marks those two datetimes with `DTZ001` exemptions. This repair is not yet user-local Ruff verified; no second PostgreSQL/Web run is needed solely for this test-style change. The Create entry test also emitted an existing React cross-component setState warning while all tests passed; track separately from this blocking Ruff gate. M5 visual acceptance remains open; B14 source-following Life Area/planned Session naming remains guarded.

## 2026-10-09 — M5/untimed focused technical gate GREEN

The user pulled `0754ba1e` in WSL and reran the exact focused Ruff selection; **All checks passed**. The preceding run on `b1b74c6d` had already passed 13/13 PostgreSQL integration and exact-catalog tests, Web typecheck, and 54/54 focused Vitest tests. The intervening commit changed only test lint/syntax and documentation, so this completes the bounded technical gate without repeating green PostgreSQL/Web checks. The React cross-component update warning seen in an existing Create-entry test remains a non-failing follow-up observation. Next: the user inspects planned Session clock layout in Activity Edit, the localized precise range validation in Create, and numeric Objective input/recording in Inspector in the real app. M5 visual acceptance and B14 source-following `Questa e le prossime` parity debt remain open; no CI/Actions.

### 2026-10-09 — Activity Edit planned time and Timeline runtime candidate

The Activity Edit `Orario` switch now adds or withdraws a planned Session time through coordinated preview/apply. A new guarded `_131` placement capability preserves the Schedule identity when timing an unplaced planned row, including after a previous unschedule; the edit snapshot keeps untimed planned rows visible. New planned rows may be saved without a time. Core Edit requests have bounded database and web timeouts with an Italian retry error instead of an endless spinner. Timeline Activity cards show a combined Play/Pausa button and Stop. Workspace web typecheck and 40/40 focused Vitest tests pass; Python syntax and diff checks pass. PostgreSQL/Ruff and real-app acceptance await the user's local gate. No CI/Actions.
