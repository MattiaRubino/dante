# DANTE — Temporal Create C1 Traceability

**Status:** ACTIVE TRACEABILITY — AUTOMATED GREEN / MANUAL OPEN  
**Date:** 2026-09-04  
**Branch:** `feature/home-timeline`  
**Code checkpoint:** `1e7b7752b69f006a4b632e2e2d3ef1522d30e95e`  
**CI:** Frontend CI #937 / `33905239085` — FULL GREEN

## 1. Semantic mapping

| Product concept | DANTE ownership | Non-collapse rule |
| --- | --- | --- |
| Activity | native Activity | not Event; not Routine |
| Event | native Event | Event recurrence may be Event-owned |
| Routine | native Routine | owns persistent repeated Activity intent |
| Schedule/placement | temporal placement | planned placement != Actual |
| Occurrence | recurrence output | rule != generated instance |
| Session | execution runtime | Session != Schedule |
| Actual | realization | planned != happened |
| Context | grouping/filter membership | Context != appearance |
| Appearance | presentation override | appearance != ownership |
| Provider intent | authored metadata | intent != provider execution |
| Timeline card | ViewModel/read projection | not DTO/DB row/canonical identity |

## 2. Current requirement → proof map

| Requirement | Current state | Primary executable proof |
| --- | --- | --- |
| title-first base + Activity/Event actionable types | implemented | `apps/web/e2e/temporal-create.spec.ts` |
| normal Activity/Event without wizard tax | implemented | `temporal-create.spec.ts` |
| `Orario + Divisibile` remains placed | implemented | `temporal-create.spec.ts` |
| Event deep intent + Agenda | implemented | `temporal-create.spec.ts` |
| Activity repeat is Routine-backed | implemented | model/runtime/projection tests + Create E2E |
| Event repeat is Event-owned | implemented | model/runtime/projection tests + Create E2E |
| `Personalizzata…` enters deep recurrence | implemented | `temporal-create-manual-hardening.spec.ts`, `temporal-create.spec.ts` |
| all four CP6 recurrence families remain authorable | implemented | recurrence/model tests + `temporal-create.spec.ts` |
| browser does not canonically generate Occurrences | preserved boundary | model/runtime contract + docs |
| Planning Tray anchored/bounded | implemented | `temporal-create-planning-tray.spec.ts` |
| one-card planning drag / no scrim / no duplicate ghost | implemented | `temporal-create-planning-tray.spec.ts` |
| same identity placement + Escape + Undo | implemented | Planning Tray E2E + F0 tests |
| per-day all-day lane before minute zero | implemented | all-day unit/E2E in `temporal-create.spec.ts` |
| simple Create floating/draggable desktop | implemented | `temporal-create-manual-hardening.spec.ts` |
| Timeline remains interactive while Create open | implemented | `temporal-create-manual-hardening.spec.ts` |
| backdrop no longer closes Create | implemented contract | `temporal-create.spec.ts` |
| dirty draft requires explicit discard | implemented | `temporal-create.spec.ts` |
| Advanced larger floating/bounded | implemented | `temporal-create-manual-hardening.spec.ts` |
| mobile Advanced bounded/no horizontal overflow | implemented | `temporal-create.spec.ts` |
| final user acceptance | pending | manual only |

## 3. Recurrence traceability

CP6 families remain exactly:

| Authored family | CP6 family |
| --- | --- |
| calendar/civil recurrence | `calendar_wall_clock` |
| elapsed interval | `elapsed_interval` |
| quota per period | `quota_per_period` |
| cyclic positions | `cyclic_positional` |

Ownership:

```text
Repeated Event → owner Event
Repeated Activity → owner Routine
```

The frontend may author the rule. Canonical future Occurrences remain backend evaluator output.

Known current local behavior: immediate Create materializes the master/first placed projection only. This is an integration boundary, not permission to make browser-generated Occurrences canonical.

## 4. F0 mutation traceability

Placement/removal continue through the F0 operation model:

```text
projection
→ typed command
→ expected revision/idempotent operation
→ TemporalWorkspacePort
→ truthful applied/no-op/rejected/failed result
→ projection update
→ guarded Undo
```

Planning Tray drop mutates placement of the same Activity. It must not create a duplicate identity.

## 5. T1 regression boundary

Create changes may not weaken:

- custom card drag;
- first drag works;
- no browser ghost/text selection;
- deselect-first focus grammar;
- deterministic compact overlap;
- expanded Context header/card alignment;
- continuous window/Now behavior;
- move + Undo;
- time editor;
- reduced motion;
- Firefox critical contract.

Frontend CI #937 passed both normal Chromium E2E and frozen Firefox Timeline regression.

## 6. Manual-only open requirements

Automated green does not decide remaining visual/product quality.

Open process requirement:

- user inspects one Create UX foundation at a time;
- next change is selected by the user;
- no bundled adjacent features;
- final closure requires one coherent manual pass after the user finishes incremental polish.

Possible simple-only left pin/dock is not yet an active requirement.

## 7. Closure state

```text
TRACEABILITY CURRENT
AUTOMATED GREEN
C1 MANUAL UX ITERATION OPEN
C1 NOT FROZEN
C2 BLOCKED
```

Only explicit `C1 MANUAL PASS — APPROVED` closes C1.
