# Timeline / Temporal-Operational — B14 U6 End-to-End implementation gate

- **Status:** APPROVED / READY TO EXECUTE — IMPLEMENTATION NOT YET CLAIMED
- **Date:** 2026-10-02
- **Branch:** `feature/timeline-temporal-operational`
- **Pre-gate HEAD:** `851b95087789fdcf3155b222ae06536b16314d7a`
- **Parent cycle:** B14 + B07 Product/UI consolidation
- **Semantic/product freeze:** `docs/workstreams/timeline-temporal-operational-b14-u5-subactivity-session-scope-2026-10-02.md`
- **Domain decision:** `docs/domain/decisions/activity-subactivity-session-bounded-v1.md`
- **Logical overlay:** `docs/logical-model/slices/activity-subactivity-session-bounded-v1.md`
- **Physical overlay:** `docs/physical-model/activity-subactivity-session-overlay-v1.md`
- **Database contract:** `docs/database/activity-subactivity-session-contract.md`
- **Previous user-proven code checkpoint before U5/U6 docs:** `5e79f556` — web typecheck PASS; 7 focused files / 14 tests PASS
- **CI:** forbidden unless the user explicitly changes the standing rule; user runs local gates

> **READ THIS FIRST AFTER A CONTEXT RESET.** This file is the exact continuation gate for the next implementation turn. Repository HEAD remains source of truth: re-fetch the live branch before any write and do not assume the pre-gate HEAD is still current.

---

## 1. U6 objective

Execute the complete bounded product vertical discussed and frozen in U5, end-to-end rather than as disconnected UI prototypes.

The deliverable is one coherent user path covering:

```text
Advanced Create
  -> Activity root
  -> direct Sub-Activities
  -> future planned execution slices shown naturally as “Sessioni”
  -> explicit Session capture policy
  -> parent/child temporal and completion guards
  -> canonical persistence/readback
  -> post-create Timeline runtime
  -> B08 real Session execution
  -> B10 reality chain
  -> real “Da risolvere” queue
```

The implementation must preserve every existing semantic boundary and must not fake capability in frontend-only state.

---

## 2. Mandatory semantic boundaries

```text
Activity != Event != Routine
Sub-Activity = Activity identity in typed direct-parent relation
Sub-Activity != Plan Step
Sub-Activity != Session
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Reconciliation != generic unresolved state
Session END != Activity completion
planned/intended != happened
projection != canonical truth
proposal != accepted effect
```

### Future “Sessione” in Create

The UI may call a future execution row **Sessione**, but the kernel meaning is:

```text
future planned execution slice = Schedule/planning truth
actual execution episode       = B08 Session truth
```

A future row MUST NOT create a Session record.

A real Session may appear only from truthful capture:

```text
live Start/Play
manual retrospective record
external import
approved inferred capture
```

`Play` is required only for live capture, not for Session semantics generally.

### Time passes with no execution truth

If a planned slice ends and no Session/Actual exists:

```text
keep planning history
execution truth = unknown
```

Do not silently create:

```text
skipped
failed
not done
completed
Actual(false)
Outcome
Confirmation
Reconciliation
```

A configured review/fallback policy may instead create a derived product need that appears in `Da risolvere`.

### Event

Event remains occurrence-centred:

```text
Event -> Schedule -> Actual event occurrence / attendance / outcome
```

Do not add generic Event-owned B08 Session runtime by symmetry.

A Session related to an Event is only valid for a distinct executable episode and is outside this U6 default Event authoring path.

---

## 3. Frozen product shape

### Advanced Activity structure

The target composition is:

```text
Activity root row
├── direct Sub-Activity row(s), depth <= 2 total
├── future planned execution slice row(s) / “Sessione” UI
└── root configuration / policy controls
```

A Sub-Activity is a full Activity identity and may independently carry:

```text
Schedule
planned execution slices
Session capture policy
B10 reality
```

but cannot itself contain another Sub-Activity in bounded v1.

### Create versus runtime

```text
Create/Advanced
= configure future plan, structure, constraints and policies

Timeline/card/detail after creation
= perform actual runtime actions
```

No Play/Pause/Resume/End controls inside Create.

Post-create controls are conditional on explicit execution policy:

```text
disabled
record
live
record_and_live
```

The old inference `session.active_duration exists => Session enabled` is provisional and must be replaced.

### Reality

Root and each child Activity independently use:

```text
Actual -> Outcome -> Confirmation -> Reconciliation
```

No automatic cascade between parent and child.

Direct-child parent guard:

```text
none
confirm
block
```

Each child relation may be `required` or `optional` for this guard.

### Temporal containment

A child accepted placement must fit the canonical parent envelope. The invariant applies both at Create and later mutation/reschedule.

No frontend-only containment and no silent cascade rescheduling.

---

## 4. `Da risolvere` — real product queue, not mock and not a new ontology

The right-rail `Da risolvere` panel shown in the current Home design becomes a real read/action surface.

It is a **derived resolution queue over canonical states**, not a universal Domain entity.

```text
Da risolvere item != B10 Reconciliation
```

B10 Reconciliation is one possible reason among several.

Initial typed reasons may include only cases already supported by the owning vertical or added canonically in this implementation:

```text
realization_review
  explicit policy requires deciding/recording what happened

outcome_required
  an Actual exists and the configured/product flow requires Outcome input/review

confirmation_required
  an attestation/confirmation action is actually required

reconciliation_open
  a real B10 reconciliation is unresolved

planned_execution_review
  a planned execution slice passed and an explicit follow-up policy requires user review

other existing explicit user-decision states
  only when the owning canonical vertical exposes a real action
```

The queue must not infer a negative reality merely from the clock.

Each queue row needs enough typed identity to route its actions without copying UUIDs manually:

```text
reason_code
subject kind/ref
owning canonical target refs where required
relevant accepted MaterialState refs where required
human title/summary
relevant time/context
actions supported for that exact reason
```

Actions dispatch to the owner, never to a generic `resolve=true` mutation.

Examples:

```text
record/confirm realization -> B10 Actual owner
record/revise Outcome       -> B10 Outcome owner
attest/confirm              -> B10 Confirmation owner
resolve conflict            -> B10 Reconciliation owner
record actual execution     -> B08 Session owner when policy allows
reschedule/skip/fallback    -> Schedule/Occurrence/owning policy vertical
```

Production mock rows must be removed. Badge count must reflect real open items. Reload must deterministically reconstruct the same unresolved items from canonical state.

No queue-specific persistence is introduced only to render the panel. If snooze/dismiss/defer later needs independent state, that requires an explicit typed decision rather than arbitrary localStorage or settings JSON.

---

## 5. Execution protocol before first code write

The implementing chat/agent MUST first:

1. fetch current branch HEAD;
2. read current:
   - `timeline-temporal-operational-roadmap.md`;
   - `timeline-temporal-operational-map.md`;
   - `timeline-temporal-operational-handoff.md`;
   - B14 consolidation ledger;
   - this gate and U5 freeze;
   - Domain/Logical/Physical/Database authority listed above;
3. read the repository agent/development operating manual and obey exact-path/write rules;
4. inspect live Alembic head and current database overlay/dictionary before choosing any DDL;
5. inspect existing B04/B08/B10/B12/B13 persistence and APIs actually present at current HEAD;
6. record the exact live implementation checkpoint before migration/code work.

Do not rely on old conversation memory when current repository authority differs.

---

## 6. U6 implementation phases

### Phase A — live persistence discovery

Determine, from current HEAD and current Alembic/database authority:

```text
current Activity identity/state authoring path
current Schedule identity and whether one Activity supports multiple planned placements today
current temporal placement admission path
current B08 Session owner/link/runtime commands
current B10 Activity/Event/Occurrence subject dispatch
current B13 Plan/Step structure
current authoring transaction/idempotency pattern
current Home Timeline read models
current right-rail Cattura/Da risolvere mock implementation
```

No DDL is authorized until this discovery resolves exact table/routine/helper names and proves the smallest compatible representation.

### Phase B — forward-only persistence

Implement the minimum canonical additions required by U5:

```text
Activity direct decomposition relation
parent child-guard policy
explicit Activity Session-capture/execution policy
```

For future planned execution slices, first reuse the canonical Schedule/planning model if it truthfully supports the required multiplicity. Add no `future_session` table and no B08 Session row. If current Schedule persistence cannot represent the accepted semantic target, stop and document the smallest necessary Schedule-side extension before implementing it.

Reconcile:

```text
Alembic forward-only migration
Dictionary
SQLAlchemy mappings
catalog expectations
CHECK/UNIQUE/FK/index inventory
ACL/grants and guarded routines
```

Published migrations are immutable.

### Phase C — guarded backend/domain application

Provide canonical commands/queries for at least:

```text
create root Activity + zero/many direct children
attach/detach/reorder direct child
required/optional relation state
set/revise child-guard mode
set/revise Session capture mode
author/read planned execution slices without Session identity
validate child temporal containment
validate parent temporal mutation against current children
read full bounded Activity structure after reload
```

Authoring root + children + placements/policies must be atomic or deterministically retry-safe with no duplicate partial tree.

### Phase D — B10 integration

Root and child Activity refs independently use existing B10 semantics.

Implement the parent completion guard at the actual admission point, not as a decorative frontend warning.

Prove:

```text
child reality does not write parent reality
parent reality does not write child reality
all children resolved does not auto-create parent Actual
Session END does not auto-create parent/child Actual
confirm mode requires explicit acknowledgement where applicable
block mode rejects the guarded parent action when required children remain unresolved
```

### Phase E — API/OpenAPI/generated client

Expose only the public capabilities necessary for the product path.

Requirements:

```text
typed request/response values
bounded failure ProblemDetails
generated client via repository tooling only
no hand editing generated sources
deterministic generated:check
```

### Phase F — Advanced Create

Implement the approved central Advanced surface using the shared draft.

Target behavior:

```text
root Activity title/config
inline direct Sub-Activities under root
planned execution “Sessione” rows under the correct Activity owner
right-side row configuration
no runtime controls inside Create
same draft survives Quick <-> Advanced transitions
```

The UI must submit all authored fields through canonical paths. No visible editable field may be ignored.

### Phase G — post-create Timeline/card runtime

Replace provisional Session visibility inference with explicit Activity execution policy.

Behavior:

```text
live / record_and_live -> Play available where appropriate
record / record_and_live -> manual recording path available where implemented
disabled -> no Session capture action
```

When live execution starts, create the actual B08 Session. Pause/Resume remain the same Session; End closes the episode but does not complete Activity.

A planned row that was never executed remains planning history, not a ghost Session.

### Phase H — real `Da risolvere`

Replace the production mock list with a real typed derived read model.

Implementation may aggregate existing owner reads in application/backend code, but it must have one deterministic product contract consumed by Home.

At minimum prove real end-to-end items/actions for the subset currently supported, including a B10-based reason and the planned-execution follow-up reason if that policy is implemented in U6.

Every item must be actionable or intentionally detail-only with a truthful reason. No dead buttons.

After successful canonical resolution, the item must disappear/reclassify correctly after fresh reload.

### Phase I — Event verification

Ensure Event create/runtime remains on Event semantics.

Prove that ordinary Event occurrence/attendance does not create or require a B08 Session duplicate. Event B10 reality remains reachable through its own subject path.

### Phase J — cleanup and docs

Remove superseded temporary/mock/provisional paths only after equivalent canonical behavior exists.

Then reconcile:

```text
roadmap
map
handoff
B14 consolidation ledger
DB overlay / Dictionary where changed
U6 closure record
B15 readiness
```

---

## 7. Mandatory PostgreSQL/backend proof matrix

The local backend gate must cover the applicable implemented surface, including:

```text
root Activity without children
one child
multiple ordered children
atomic root + children authoring
idempotent replay
self-parent rejected
duplicate edge rejected
second parent rejected
depth > 2 rejected
foreign/cross-self rejected
required/optional revision
reorder history/current state
detach preserves both Activity identities
stale expected-current rejected
Session capture policy independent of duration constraint
unknown policy mode rejected
planned execution authoring produces no future Session row
planned execution survives canonical reload
exact child temporal containment
boundary equality cases
outside-parent child rejected
all-day/date-span containment
missing parent envelope handled truthfully
parent mutation preserving children accepted
parent mutation invalidating children guarded
root/child B10 independence
Session END != Activity Actual/completion
Event path does not fabricate Session
queue read model returns only real open reasons
queue resolution action changes canonical owner state and read model follows
Dictionary/catalog/ORM/Alembic inventory exact
```

---

## 8. Mandatory web/client proof matrix

At minimum:

```text
web typecheck
api-client typecheck
generated:check deterministic
Advanced Activity root authoring
Sub-Activity add/remove/reorder/config
planned “Sessione” row authoring without runtime Session identity
Quick <-> Advanced draft preservation
reload reconstructs root/children/planned slices/policies
no Play/Pause/End inside Create
post-create live policy shows Play
post-create disabled policy hides Session runtime
Start creates/reads actual Session through B08 path
End does not mark Activity complete
Event UI does not gain generic Session runtime
Da risolvere has no hard-coded production fixture rows
badge/count derives from real items
queue reason rendering is typed
queue action routes to real owner
resolved item disappears/reclassifies after fresh read
no dead or decorative control
```

Existing B04/B08/B10/B12/B13 focused regressions that touch changed contracts must be included.

---

## 9. User-run gate protocol

The assistant may prepare exact complete command blocks, but the user runs the local tests on `~/projects/dante`.

Rules:

```text
NO GitHub Actions / CI
NO claiming tests passed before user reports output
NO editing generated files by hand
NO skipping exact catalog/Dictionary proof after persistence change
```

The final gate must be reported in tiers:

```text
CANDIDATE
  code committed, not yet user-proven

PROVEN
  exact automated local gate reported PASS by user

USER-ACCEPTED
  real-stack visual/behavior walkthrough reported acceptable by user
```

---

## 10. Real-app acceptance checklist

After automated proof, launch the real Access/Auth stack and verify visually/behaviorally:

```text
Advanced Create layout remains compact and aligned
root + direct Sub-Activity structure is understandable
planned “Sessione” rows clearly behave as future plan
no runtime buttons appear inside Create
post-create Play appears only when live capture is enabled
live Session controls work on the actual card/detail
Session End leaves Activity reality independent
Event remains occurrence-centred
Da risolvere badge/list contains real data
real unresolved items expose correct contextual actions
resolved action removes/reclassifies the card after reload
no overflow/regression in the fixed Home skeleton/right rail
```

The existing right rail geometry and Home anti-overflow constraints must be rechecked because `Da risolvere` is becoming live content rather than fixed mock content.

---

## 11. Stop lines

Do not implement any of the following without reopening scope:

```text
recursive arbitrary-depth Sub-Activity tree
Sub-Activity represented as Plan Step
future B08 Session records
Session nesting
automatic Activity completion on Session END
auto-negative Actual because scheduled time passed
universal unresolved/reconciliation entity
generic resolve=true queue mutation
Event-owned Session runtime by symmetry
silent child Schedule cascade
frontend-only canonical validation
queue localStorage as source of truth
notification delivery system beyond the already frozen Reminder configuration scope
```

---

## 12. Completion definition

U6 closes only when all of the following are true:

```text
canonical persistence exists for every editable new capability
full bounded structure reloads from canonical reads
future planned “Sessione” does not create Session truth
actual Session capture works post-create according to explicit policy
root/child B10 truth remains independent and guarded correctly
Event semantics remain clean
Da risolvere is real and contains no production mock fixtures
queue actions use owning canonical verticals
affected generated/backend/web/catalog gates are user-reported green
real-stack walkthrough is user-accepted
roadmap/map/handoff/consolidation docs are reconciled
```

Until then the block is `ACTIVE / CANDIDATE`, never “done” merely because the UI renders.