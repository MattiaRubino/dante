# Timeline / Temporal-Operational — B08 Session Runtime Execution Plan

- **Status:** ACTIVE EXECUTION PLAN — B08 NOT STARTED
- **Created:** 2026-09-23
- **Branch:** `feature/timeline-temporal-operational`
- **Starting remote HEAD:** `9bba3db6efb06147891bedcb6e1e084f6ca3d5a5`
- **Starting Alembic frontier:** `20260923_57`
- **Starting proven DB topology:** `145|5|88|92|285|223|408|0|0|0`
- **Parent roadmap:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Live ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **Workstream handoff:** `docs/workstreams/timeline-temporal-operational-handoff.md`
- **Domain authority:** `docs/domain-model/time/session.md`
- **PostgreSQL overlay:** `docs/database/timeline-temporal-operational.md`
- **CI:** no CI/GitHub Actions run is authorized by this plan; local tests are run by the user

This file is the execution authority for B08. It is deliberately detailed enough that a fresh chat can recover the exact semantic boundary, current slice, accepted decisions, proof obligations and next action without relying on conversational memory.

---

# 0. B08 mission

B08 activates the existing canonical **Session** concept inside the bounded Home `+` / Timeline vertical.

The target capability is:

```text
Activity / Occurrence
        │
        │ optional accepted planning
        ↓
     Schedule
        │
════════╪════════════════════════════════ planned vs reality
        ↓
      Session
        │
        ↓
 later Actual / Outcome work in B10
```

B08 owns actual execution-episode runtime. It does **not** collapse planned placement, expected-instance identity or broader happened-reality semantics into Session.

Permanent boundaries:

```text
Activity != Session
Occurrence != Session
Schedule != Session
Session != Actual
Session != Outcome
planned/intended != happened
planned Schedule duration != Session elapsed duration
Session elapsed duration != Session active duration
Session end != Activity completion
Session end != Occurrence completion
```

---

# 1. Authority chain and implementation discipline

Every B08 decision follows:

```text
Product / simulations where applicable
→ Domain
→ Logical
→ Physical
→ current PostgreSQL dictionary / Alembic
→ application boundary
→ API/OpenAPI/client
→ frontend runtime integration
→ automated proof
→ real-stack manual proof
→ documentation reconciliation
```

Rules:

```text
Domain != Logical != Physical != ORM != API DTO != frontend ViewModel
projection != canonical truth
current accepted state != latest row
NativeRef != ScopedRecordRef != MaterialStateRef
idempotency key != Domain identity
provider identity != DANTE identity
```

No migration is assumed in advance. Existing CP6 structures are reused when they already represent the required semantics. New DDL must be forward-only and justified by a specific persistence gap.

---

# 2. Existing substrate that B08 must reconcile before adding anything

The current database already contains the Session family introduced by CP6-M03:

```text
session
session_timing_state
session_timing_absolute
session_timing_elapsed
session_timing_pause
session_timing_current_history
```

B08 must first establish exactly what this substrate already guarantees, including:

```text
stable Session NativeRef
open-ended Session timing
absolute vs elapsed timing representation
pause interval representation
MaterialState identity
current binding/history chronology
retirement continuity
runtime ACLs
current/history integrity triggers
```

B08 must not introduce a parallel `runtime_session`, generic timer table or alternative currentness model.

---

# 3. Frozen baseline intent to verify in B08-A

The following is the proposed bounded vertical contract. B08-A must verify it against current Product/Domain/Logical/Physical authority before implementation freeze.

## 3.1 Execution targets

```text
Activity     candidate baseline target ✅
Occurrence   candidate baseline target ✅
Routine      direct Session target      ❌
Event        ordinary baseline target   ❌
Schedule     Session owner/target       ❌
```

Interpretation:

- an Activity may be actually executed whether scheduled or unscheduled;
- an Occurrence may be actually executed whether expected-only or scheduled;
- Routine is the recurring behavioral intention/policy, not the episode actually executed;
- ordinary Event actual occurrence does not gain a duplicate Session by default;
- Schedule remains optional planning context, never the owner of actual execution.

The exact physical relation used to connect Session to Activity/Occurrence is **not frozen yet**. B08-A must select a typed bounded representation without inventing a universal semantic reference escape hatch.

## 3.2 Spontaneous Session

The Domain permits actual execution without prior Schedule and can permit execution without a pre-existing Activity. The latter remains a valid Domain capability but is **deferred from the B08 vertical baseline** unless authority inspection shows it is required now.

B08 must not architecturally prohibit future spontaneous execution merely because the first product path requires Activity/Occurrence context.

## 3.3 Baseline lifecycle

Candidate lifecycle semantics to verify/freeze:

```text
START
→ Session exists and is running/open

PAUSE
→ same Session remains open

RESUME
→ same Session continues

END
→ Session closes

later START
→ new Session identity
```

No universal inactivity threshold may silently convert pause into end or close a stale Session.

Lifecycle state should be derived from accepted temporal state where possible rather than introducing a broad generic status ontology without need.

## 3.4 Timing semantics

B08 must preserve at least:

```text
elapsed duration
paused duration when pause information exists
active duration only when supported by captured facts
```

Do not fabricate active-time precision when only an elapsed/manual interval is known.

---

# 4. B08 ordered slices

B08 is executed as six ordered slices. Do not opportunistically start a later slice while an earlier slice is semantically or evidentially open.

## B08-A — Authority reconciliation + implementation freeze

**Goal:** prove the exact vertical semantics and persistence boundary before functional implementation.

Checklist:

```text
[ ] inspect current Session Domain authority in full
[ ] inspect relevant Activity / Occurrence / Schedule / Event / Actual distinctions
[ ] inspect Logical Session/reference contracts
[ ] inspect Physical PostgreSQL mapping for Session
[ ] inspect current dictionary for every `session*` object
[ ] inspect current ORM mappings / DB grants / runtime capabilities touching Session
[ ] inspect current Timeline API/frontend boundaries that will host runtime actions
[ ] resolve Session → Activity / Occurrence typed execution-context representation
[ ] resolve exact lifecycle commands and legal transitions
[ ] resolve exact current/history mutation model
[ ] resolve concurrent-open Session policy for the same actor/context
[ ] resolve idempotency and expected-state/CAS requirements
[ ] classify B04 TC-009 reopening and TC-010 deferral
[ ] freeze explicit B08 exclusions
[ ] write B08-A implementation-freeze record
```

Exit gate:

```text
B08-A CLOSED / FROZEN
no unresolved semantic question required to implement B08-B
DDL gap list explicit
API operation inventory explicit
proof matrix explicit
```

No major runtime implementation starts before this gate.

---

## B08-B — Session Start / Read / End core

**Goal:** establish the smallest canonical execution vertical.

Required capability:

```text
Activity → START Session
Occurrence → START Session
read current/open Session state
END Session
reload/re-read from canonical backend truth
new START after END → new SessionRef
```

Backend/persistence obligations:

```text
[ ] governed Session NativeRef creation/reuse semantics
[ ] typed execution-context binding
[ ] initial timing MaterialState
[ ] current binding/history
[ ] end timing revision
[ ] self-scope / fail-closed ownership
[ ] idempotent operations
[ ] materially different replay conflict
[ ] expected-current/CAS where required
[ ] concurrency proof
[ ] no direct broad-table write shortcut if bounded capability is required
```

Forbidden effects:

```text
START does not fabricate Schedule
END does not complete Activity
END does not resolve Occurrence
END does not create Actual
END does not create Outcome
```

Exit gate includes backend/PostgreSQL integration proof plus API/OpenAPI/client compatibility for the accepted B08-B surface.

---

## B08-C — Pause / Resume + truthful runtime duration

**Goal:** one logically continuous execution attempt survives pause/resume without identity fragmentation.

Required capability:

```text
RUNNING → PAUSED → RUNNING → ENDED
```

Checklist:

```text
[ ] PAUSE keeps same SessionRef
[ ] RESUME keeps same SessionRef
[ ] at most one open pause for one Session
[ ] invalid transition conflicts/fails closed
[ ] elapsed duration derived truthfully
[ ] paused duration derived truthfully
[ ] active duration derived only when support exists
[ ] reload while running preserves state
[ ] reload while paused preserves state
[ ] concurrent PAUSE/RESUME is deterministic/conflict-safe
[ ] correction/current-history semantics remain append/current-history coherent
```

No timer value in browser memory is canonical.

---

## B08-D — Timeline runtime integration

**Goal:** make B08 genuinely usable in the real product before visual consolidation in B07.

Required surfaces:

```text
scheduled Activity
unscheduled Activity path where current product surface permits access
expected Occurrence
scheduled Occurrence
```

Required behavior:

```text
[ ] START exposed only for eligible targets
[ ] RUNNING state visible after authoritative read
[ ] PAUSE / RESUME / END controls obey backend state
[ ] live displayed duration derives from canonical start/pause truth + client clock only as presentation
[ ] F5 rehydrates authoritative state
[ ] navigation away/back rehydrates authoritative state
[ ] Schedule remains unchanged when execution differs
[ ] no duplicate Timeline item from Session projection unless explicitly designed
[ ] no fake optimistic completion/outcome
[ ] empty/error/conflict states are usable and truthful
```

The UI may remain intentionally utilitarian. B07 owns final visual/interaction consolidation.

---

## B08-E — Reopen TC-009 Session-duration semantics

**Goal:** activate only the B04 constraint family that becomes semantically anchored by Session.

TC-009 was deferred specifically for contiguous Session duration. B08-E must first define its exact meaning against Session timing rather than reusing planned Schedule duration by convenience.

Checklist:

```text
[ ] define constrained Session fact/facet
[ ] define contiguous-duration semantics
[ ] distinguish elapsed vs active applicability
[ ] define hard vs soft evaluation behavior
[ ] define violation result without automatic mutation
[ ] select typed persistence if existing Temporal Constraint representation cannot express Session target truthfully
[ ] deterministic evaluation API/application path
[ ] catalog/integrity proof
[ ] Timeline/product exposure only if useful for the bounded vertical
```

Explicitly deferred unless new authority requires reopening:

```text
TC-010 spacing/recovery
TC-011 broad relative before/after
```

---

## B08-F — Whole-block closure

**Goal:** prove the completed Session Runtime across persistence, application, API/client, web and real-stack behavior, then reconcile all documentation.

Automated closure dimensions:

```text
[ ] DB catalog/topology/integrity relevant gates
[ ] Session backend integration tests
[ ] cross-user/fail-closed tests
[ ] idempotency/replay tests
[ ] concurrency/CAS tests
[ ] OpenAPI generated-current check
[ ] API-client typecheck
[ ] web typecheck
[ ] focused Session/Timeline Vitest
[ ] regression tests for B01/B02/B04/B06 touched boundaries
```

The user runs local tests. Do not launch CI/GitHub Actions unless separately authorized.

Real-stack manual closure scenario:

```text
1. create/use an Activity
2. START it
3. F5 → same Session remains running
4. PAUSE
5. F5 → same Session remains paused
6. RESUME
7. END
8. verify elapsed/paused/active truth available as designed
9. START same Activity again → new SessionRef
10. START one eligible Occurrence → Session binds to that Occurrence
11. verify original Schedule is unchanged
12. verify END did not manufacture Activity/Occurrence completion
13. verify no Actual/Outcome was fabricated
14. verify no duplicate runtime/session rows appear after repeated reload/navigation
```

Closure documentation:

```text
[ ] B08-F closure record
[ ] live map reconciled
[ ] parent roadmap reconciled
[ ] handoff advances to B09
[ ] DB overlay/dictionary reconciled if persistence changed
[ ] exact Alembic frontier/topology recorded
[ ] exact accepted test/manual evidence recorded
```

Only then may B08 become `CLOSED / PROVEN`.

---

# 5. B08 explicit non-goals

The following do not belong in the B08 baseline unless a discovered authority dependency makes one unavoidable:

```text
Actual / Outcome / Confirmation semantics                         → B10
Activity/Occurrence automatic completion from Session end         → forbidden
ordinary Event actual-occurrence duplication as Session            → excluded baseline
spontaneous context-free Session product flow                      → deferred
Session split / merge UX                                           → deferred
provider/import reconciliation                                     → future provider work
native/mobile background timer                                     → outside vertical
advanced offline/multi-device runtime synchronization              → outside vertical
cross-account shared execution                                     → outside vertical
analytics/productivity statistics                                  → outside vertical
final visual/interaction polish                                    → B07
TC-010 spacing/recovery                                             → later anchor-specific reopening
```

Deferred does not mean semantically prohibited.

---

# 6. B08 persistence rules

Binding implementation rules:

```text
reuse existing CP6 Session family where truthful
forward-only Alembic
never edit already-applied migrations
no generic Entity/Thing table
no generic Relationship(type, from, to, payload) escape hatch
no generic status row as substitute for typed lifecycle truth
no browser-owned canonical timer state
no last-write-wins for consequential transitions
no current-state inference from max UUID/timestamp
```

If a new execution-context relation is required, it must preserve typed target eligibility and stable Session identity. The exact representation is a B08-A decision.

Every same-change persistence modification must reconcile:

```text
Alembic DDL
SQLAlchemy mapping
Database Dictionary
DB overlay / documentation
catalog tests / expected topology
runtime grants/capabilities
```

---

# 7. API and operation governance

Pre-B04 governance remains binding.

For every accepted Session command/query B08-A/B08-B must define:

```text
semantic operation name
HTTP method/path
stable operationId
request DTO
response DTO
error/conflict contract
idempotency semantics
self-scope semantics
OpenAPI generated-client impact
```

Likely command families are conceptually START / PAUSE / RESUME / END, but exact public naming is frozen only after authority/application inspection.

---

# 8. Proof strategy

B08 uses layered proof; no single green unit test closes a slice.

```text
semantic proof
+ schema/catalog proof
+ transaction/integrity proof
+ application/API proof
+ generated-client proof
+ frontend boundary proof
+ real-stack manual proof where user behavior matters
```

Negative proof is mandatory for the dangerous collapses:

```text
Session action must not mutate Schedule implicitly
Session END must not produce completion/outcome implicitly
cross-user Session refs must fail closed
stale/replayed operations must not create duplicate episodes/pause intervals
reload must not create a new Session
```

---

# 9. Documentation and chat-saturation recovery protocol

This section is intentionally operational.

At every meaningful B08 checkpoint:

1. update `timeline-temporal-operational-map.md` checkboxes/status;
2. update this plan if a decision changes scope or ordering;
3. create an immutable dated freeze/closure record for semantic milestones;
4. update `timeline-temporal-operational-handoff.md` with the exact current slice and next action;
5. reconcile DB overlay/dictionary in the same change as schema changes;
6. push documentation/code frequently rather than waiting for the whole block.

A fresh chat should need to read, in order:

```text
1. docs/workstreams/timeline-temporal-operational-handoff.md
2. docs/workstreams/timeline-temporal-operational-map.md
3. docs/workstreams/timeline-temporal-operational-b08-execution-plan.md
4. latest B08-A/B08-B/... dated freeze or closure record
5. docs/database/timeline-temporal-operational.md if persistence is involved
```

The handoff must always contain:

```text
current branch
exact known remote frontier when recorded
current Alembic frontier
current B08 slice
closed/proven slices
open semantic/technical blockers
last accepted local test evidence
next concrete action
explicit statement that CI is not authorized
```

This is the recovery source of truth when conversation context is lost.

---

# 10. Commit/push discipline

During B08:

```text
small coherent commits
frequent remote pushes
no waiting until slice end to preserve work
no CI side effects
no broad unrelated refactors mixed into Session work
```

Recommended commit families:

```text
docs: freeze B08-A ...
db: add bounded B08 ...
feat: add B08 Session ...
test: prove B08 ...
docs: close B08-...
```

The user executes local test commands and reports output. The assistant may prepare patches/remote commits but does not claim proof until the corresponding user-run evidence is received.

---

# 11. Current gate

```text
B08-A Authority reconciliation + implementation freeze   ← NEXT
B08-B Start / Read / End core                             BLOCKED BY A
B08-C Pause / Resume + duration                           BLOCKED BY B
B08-D Timeline runtime integration                        BLOCKED BY C
B08-E TC-009 Session-duration reopening                   BLOCKED BY A-D semantics
B08-F Whole-block closure                                 BLOCKED BY A-E
```

**Next action:** execute B08-A authority reconciliation from remote frontier `9bba3db6efb06147891bedcb6e1e084f6ca3d5a5` / Alembic `_57`, then publish the B08-A implementation freeze before starting B08-B.