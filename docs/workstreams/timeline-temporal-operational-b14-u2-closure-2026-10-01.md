# B14 + B07 — U2 Quick Authoring Closure

- **Status:** CLOSED / PROVEN — source, persistence, API, generated client and focused local automated proof
- **Closed:** 2026-10-01
- **Branch:** `feature/timeline-temporal-operational`
- **Persistence head:** `20261001_95`
- **Catalog topology:** `196|5|157|100|397|344|503|0|0|0`
- **Generated client checkpoint:** `dd94c6ee876bf5e671a516898b064c37e2d90741`
- **CI:** not used; all reported proof was run locally by the user

## 1. Closed contract

U2 closes the canonical Quick Create authoring path for Activity and Event while preserving the permanent temporal/domain boundaries.

The accepted product contract is:

```text
Activity/Event may exist without a Life Area assignment
absence of Life Area assignment != synthetic category
Life Area remains actor-local product organization
Tag remains secondary many-to-many organization and is outside Quick Create
location is optional for Activity and Event
description is optional canonical authoring metadata
item color override is distinct from Life Area color
new Life Area creation occurs only when the enclosing authoring command is accepted
selected existing Life Area keeps its accepted revision/color unless the user explicitly changes color
explicit Life Area color change is revision-guarded
Quick Create date/time placement maps to canonical Schedule placement
multi-day placement is explicit; no hidden end-time rollover
projection != canonical truth
Activity != Event != Routine
Occurrence != Schedule
Schedule != Session != Actual
```

## 2. Persistence and ACL

`20260930_94` introduced:

- nullable canonical `description`, `location`, `color_code` on `dante.activity_intention`;
- nullable canonical `description`, `location`, `color_code` on `dante.event_expectation`;
- six database CHECK constraints covering descriptor metadata;
- bounded SECURITY DEFINER authoring wrappers:
  - `dante.create_self_activity_authoring(...)`;
  - `dante.create_self_event_authoring(...)`.

`20261001_95` is a forward-only ACL repair restoring the historical runtime read capability on the two descriptor tables after `_94` had revoked it too broadly. Runtime direct INSERT/UPDATE/DELETE remains denied; writes stay behind bounded capabilities.

The reconciled current topology is:

```text
tables            196
views               5
routines           157
triggers           100
physical indexes   397
foreign keys       344
check constraints  503
domain/enum          0
sequence/matview     0
policies             0
```

## 3. Application and API

U2 adds one transactional authoring boundary for each Quick Create root:

```text
POST /api/v1/temporal/authoring/activities
POST /api/v1/temporal/authoring/events
```

The application boundary owns:

- Activity/Event creation;
- optional existing/new Life Area handling;
- revision-guarded Life Area color mutation when explicitly requested;
- optional canonical description/location/item-color metadata;
- optional accepted Schedule placement;
- idempotent replay behavior.

Legacy lower-level B01/B03 helpers remain internal compatibility capabilities; U2 supersedes the old B05 product rule that public creation must always create a primary Life Area assignment.

## 4. Web integration

The compatible Quick Create path uses the U2 authoring endpoint and no longer blocks Activity/Event creation when Life Area is absent.

The U2 draft carries:

- explicit start/end date-time placement state;
- optional Life Area selection or new-name draft;
- accepted Life Area revision/color separately from user-modified color;
- optional item color override when no Life Area is selected;
- optional location;
- optional description.

Quick and Advanced surfaces share the same draft. Advanced intents not yet represented by the U2 DTO remain on the historical runtime path rather than being silently dropped. This fallback is deliberately temporary and belongs to the continuing U3+ UI consolidation work.

## 5. Generated public contract

The OpenAPI and generated TypeScript/Zod client were produced only through repository generation tooling and committed at:

```text
dd94c6ee chore(api-client): regenerate B14 U2 authoring contract [skip ci]
```

The generated contract includes the U2 Activity/Event request/response models and accepted placement response union.

## 6. Local proof reported by the user

The user-run gate reported:

```text
Alembic current                         20261001_95 (head)
focused U2/B05/B03/backend regressions  PASS before catalog reconciliation
U2 API unit contract                    PASS
web typecheck                           PASS
web focused suite                       8 files / 26 tests PASS
api-client typecheck                    PASS
generated:check                         PASS / deterministic
final current catalog pair              8 passed in 30.04s
```

The first catalog run correctly exposed stale `_93` Dictionary/topology expectations. The repository was reconciled to `_95`, including the two new routine entries and six new CHECK constraints, and the focused catalog rerun then passed `8/8`.

No GitHub Actions/CI run is used as closure evidence.

## 7. Superseded statements

Any older workstream/Dictionary prose saying that every newly created Activity/Event must have a primary Life Area is superseded for the U2 Quick Authoring product boundary.

The retained B05 truths are:

```text
Life Area = actor-local primary organization when assigned
Tag = actor-local secondary many-to-many organization
Life Area != Tag != Context
organization != Domain ownership
```

The new truth is:

```text
0..1 primary Life Area assignment for a Quick-authored Activity/Event
0 is a valid accepted state
```

## 8. What remains active

U2 closure does **not** close B14+B07.

The next cursor is U3+ visual/product consolidation:

- finish the fixed two-date + two-time Quick Create presentation and calendar polish;
- finish Life Area/color/location/description visual organization;
- move the broader Advanced configuration into the large shared-draft surface;
- progressively migrate remaining Advanced intents off the historical fallback without losing capability;
- continue Home/Timeline visual and interaction consolidation.

B14+B07 therefore remains ACTIVE while U2 itself is CLOSED / PROVEN.
