# DANTE — Temporal Create C1 Final Validation

**Status:** FINAL AUTOMATED VALIDATION — USER MANUAL ACCEPTANCE PENDING  
**Date:** 2026-09-02  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Worktree:** `/home/mattia/projects/dante-timeline`  
**Integration target:** `feature/home-react`  
**Validated implementation / test-harness candidate:** `2b910092ecd70de74338427924666a965938ba9f`  
**Frontend CI:** run `33660540265` / #676 — **FULL PASS**

## 1. Authority of this record

This document is the final automated validation addendum for C1 after the late Planning Tray, all-day rendering, accessible-name and global E2E focus-harness hardening.

It **supersedes only stale candidate SHA, CI-run, measured test-count, architecture-count, bundle-size and current-gate metadata** in older C1 documents. It does not replace or shorten their semantic/product/history content.

Keep reading the detailed authorities:

- `temporal-create-c1-traceability.md`;
- `temporal-create-c1-engineering-checkpoint.md`;
- `temporal-create-c1-scope-amendment.md`;
- `temporal-frontend-roadmap.md`;
- `temporal-create-handoff.md`;
- `temporal-f0-contract.md`;
- `timeline-t1-frozen-contract.md`.

Current operational state is in `temporal-live-status.md`. The one human gate is `temporal-create-c1-manual-acceptance.md`.

## 2. Permanent C1 boundaries remain unchanged

C1 is the maximum useful **manual** Timeline Create capability before backend integration.

```text
manual + / double-click / Shift-drag
→ deterministic structured prefill
→ one Create draft
→ Quick ↔ Expanded ↔ Full
→ normalize / validate / preview
→ explicit user commit
→ F0 application command
→ deterministic local runtime
→ STOP before backend/provider runtime
```

Still permanent:

```text
Activity != Event
Activity repetition → Routine ownership
recurrence specification != generated Occurrence
Schedule != Session != Actual
planned != happened
Context/group membership != appearance override
manual Create != DANTE/AI/NL/voice input
frontend projection id != canonical backend id
ViewModel != application model != DTO != DB row
```

No late hardening in this record changes those rules.

## 3. Final `Da collocare` / Planning Tray behavior

An Activity may be valid planning intent without an accepted exact Timeline slot. That state is now operationally surfaced rather than hidden or fabricated.

Authoritative distinction:

```text
Da collocare
= Activity currently has no accepted exact placement

Collocazione
= UI/application area concerned with placement

Vincolo temporale
= rule constraining how/when the Activity may be placed

Durata prevista
= expected work duration
```

These concepts are intentionally not synonyms.

The Planning Tray now provides a truthful home for unplaced Activities:

- unplaced Activity appears in the tray rather than a fake timed slot;
- searchable list;
- Context/tone/duration/planning-policy summary;
- quick placement by date/time;
- pointer drag from tray into the real Timeline;
- snapped live placement preview;
- Timeline planning/foreground mode while dragging;
- explicit remove/delete confirmation;
- mobile bounded bottom-sheet presentation;
- no fake network/provider/backend state.

Placement is an application mutation of the **same Activity identity**, not delete-and-recreate.

Undo after placement returns that Activity to its prior unplaced state. Undo after explicit tray deletion restores the same unplaced Activity.

Primary automated evidence:

`apps/web/e2e/temporal-create-planning-tray.spec.ts`

The final Chromium suite proves all four contracts:

1. unplaced Activity → tray → quick placement keeps identity → Undo returns it;
2. drag foregrounds Timeline, shows snapped preview, commits once, and Escape cancels without mutation;
3. explicit tray delete → Undo restores the same unplaced Activity;
4. Planning Tray remains bounded as a mobile bottom sheet.

## 4. All-day Event rendering repair

A real product defect was found during CI investigation: the all-day layer still targeted the stale host `.home-timeline-head--production`, while the actual React Timeline mounts `.dante-timeline-header`.

The component now mounts the all-day strip against the real Timeline header. The structural regression contract still requires the strip to live **outside the timed grid**.

Final Chromium evidence proves:

`all-day Event uses a dedicated strip outside the timed grid while unscheduled Activity stays unplaced`

Therefore:

- all-day Event is a date-span surface, not a midnight timed card;
- unscheduled Activity remains a different semantic state;
- the strip is attached to current React DOM architecture rather than legacy markup.

## 5. Accessible naming / product vocabulary repair

CI correctly exposed accessible-name collisions caused by section headings containing labels also owned by real form controls.

The final naming keeps semantic boundaries clear:

- section: `Collocazione`;
- control: `Vincolo temporale`;
- control: `Durata prevista`;
- Activity state: `Da collocare`.

The fix was made in product semantics/accessibility rather than weakening Playwright locators.

## 6. Planning Tray React / TypeScript hardening

The new tray was also hardened to conform to the current React/ESLint/TypeScript contracts:

- pointer gesture state that does not render remains ref-based;
- render-affecting planning/scrim state is explicit React state;
- drag cleanup is a stable callback;
- no effect is used merely to synchronize derivable state;
- optional callback typing is valid under `exactOptionalPropertyTypes`;
- cleanup removes planning mode and transient drag state.

No test or runtime shortcut was added to bypass these checks.

## 7. Global Access E2E harness hardening

After all Timeline/C1 Chromium tests were passing, the global Web E2E gate repeatedly failed in an unrelated Access keyboard test at its **first Tab after navigation**.

The failure reproduced twice on the exact same C1 SHA, so it was not dismissed as a flake.

Inspection showed no demonstrated Access product regression: the locale trigger remains a native button and its ArrowDown/Escape focus behavior is intact. The unstable assumption was the test harness presuming that a fresh browser navigation always provides the same document focus origin.

The final harness now establishes an explicit neutral origin:

```text
body.tabIndex = -1
body.focus()
assert body is activeElement
press Tab
assert locale trigger is focused
```

This does **not** add product autofocus, does not introduce sleeps, does not skip keyboard navigation and does not weaken the tab-order assertion. The first real Tab must still land on the locale trigger, then ArrowDown/Escape/next Tab are tested normally.

A post-write diff audit also caught that the first full-file Contents API rewrite had accidentally dropped one existing password-value assertion. It was restored immediately.

Final compare from `cabd62130601be6c4ed8e9c0e85fbd31041532a5` to `2b910092ecd70de74338427924666a965938ba9f` for this harness hardening:

```text
1 file changed
10 additions
0 deletions
```

Thus the final Access harness change weakens no prior assertion.

## 8. Final automated evidence — CI #676

Validated SHA:

`2b910092ecd70de74338427924666a965938ba9f`

Frontend CI:

- run ID `33660540265`;
- run number `676`;
- conclusion **FULL PASS**.

### Quality — PASS

- frontend pre-production contract drift: PASS;
- active Home format: PASS;
- lint: PASS;
- typecheck: **5 / 5 packages PASS**;
- architecture: **218 modules / 537 dependencies / 0 violations**;
- generated-source drift: PASS;
- web unit: **35 files / 185 tests PASS**;
- `@dante/time`: **5 tests PASS**;
- `@dante/i18n`: **6 tests PASS**;
- production build: PASS;
- diff check: PASS;
- repository mutation check: PASS.

### Mobile — PASS

- Expo dependency compatibility: PASS;
- Android Hermes bundle smoke: PASS.

### Chromium — PASS

Full Web E2E:

```text
96 passed
```

This includes Access, Home structure, all Temporal Create suites, Planning Tray, all-day rendering, recurrence, contextual gestures, mobile Create, Timeline controls/hardening/interactions and World Focus regression coverage.

### Firefox frozen Timeline — PASS

```text
10 passed
```

The frozen Timeline interaction contract remains intact.

### Frontend CI Gate — PASS

All required frontend validation jobs are green.

## 9. Final measured bundle

Production Home route on the validated candidate:

```text
287.61 kB raw
94.69 kB gzip
```

No asynchronous split is introduced merely to reduce gzip. The Create path currently benefits from synchronous draft continuity, validation, focus and recovery. Revisit splitting only from future measured route-growth/performance evidence.

## 10. Backend / external stop line remains unchanged

Still outside C1:

- real API transport;
- PostgreSQL application writes;
- canonical server identities;
- server durable idempotency;
- product Auth/ACL enforcement;
- provider writes/sync/invitations/room booking/conference creation;
- notification delivery;
- authoritative solver;
- recurrence evaluator/checkpoints;
- Occurrence generation;
- Session runtime;
- Actual/outcome runtime;
- multi-device reconciliation;
- AI/NL runtime/input;
- voice runtime/input.

## 11. Current gate

C1 is now:

```text
IMPLEMENTATION COMPLETE
AUTOMATED FULL PASS
FINAL AUTOMATED VALIDATION RECORDED
USER MANUAL ACCEPTANCE PENDING
NOT FROZEN / CLOSED
```

The documentation descendant containing this record must itself pass Frontend CI before the user starts the final manual protocol.

Only explicit user acceptance:

`C1 MANUAL PASS — APPROVED`

allows transition to:

`C1 TEMPORAL CREATE → FROZEN / CLOSED`

Only after that may C2 begin.
