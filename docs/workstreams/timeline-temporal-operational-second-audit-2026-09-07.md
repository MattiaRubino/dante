# Timeline / Temporal-Operational Vertical — Second Completeness Audit

- **Status:** CURRENT REQUIRED COMPANION / SECOND-AUDIT HARDENING
- **Date:** 2026-09-07
- **Branch:** `feature/timeline-temporal-operational`
- **Protected-main anchor:** `981f6cf9ad985d0b811bc4172c12a7529fbc9b15`
- **Primary semantic map:** `docs/workstreams/timeline-temporal-operational-map.md`
- **Purpose:** independently re-check the semantic map after its deep rewrite against current Logical, Physical, PostgreSQL, Product and Frontend authority, identify any stale/current-truth drift or requirements represented too generically, and bind the corrections before roadmap sequencing.

---

# 0. Why this second audit exists

The first deep rewrite intentionally made the temporal-operational map broad enough to prevent forgotten lifecycle pieces. That is necessary but insufficient for DANTE.

A map can still fail in two ways:

1. **semantic omission** — a real accepted requirement has no explicit home;
2. **current-truth drift** — a requirement is semantically correct but a status/topology/version statement is stale relative to current protected `main`.

The second audit therefore re-checks both.

The governing rule is:

```text
complete semantic map
+
current repository truth
+
explicit non-collapse boundaries
+
traceable source ownership
=
roadmap-safe starting point
```

This file is not a roadmap and does not authorize implementation.

It is also not a new ontology document. If it discovers an inconsistency, it classifies the inconsistency against already-accepted authority rather than inventing a new Domain owner.

---

# 1. Authority result — current protected-main database truth hardening

The second audit found one **current-truth presentation issue** in the deep map.

The deep map's persistence section intentionally quoted the historical CP6 concrete-database closure topology:

```text
68 tables
5 views
14 routines
75 triggers
95 indexes
68 FKs
120 CHECKs
Alembic 20260826_08
```

Those numbers remain valid **historical CP6 closure evidence**.

They are **not the current protected-main database topology** after subsequent Recovery, Access/Auth, Email Platform and pre-vertical foundation evolution.

Current authoritative database truth as of the protected-main anchor used by this branch is:

```text
PostgreSQL                    18.6
Alembic protected-main head  20260906_18

89 tables
5 views
18 routines
77 triggers
173 physical indexes
91 foreign keys
272 CHECK constraints
0 enums/domains
0 sequences
0 materialized views
0 partitioned tables
0 RLS policies
```

Therefore the temporal-operational workstream must use the following precedence:

```text
CURRENT DATABASE IMPLEMENTATION TRUTH
= docs/database/README.md
+ current Alembic
+ SQLAlchemy mappings/MetaData
+ Dictionary
+ real PostgreSQL/direct tests

HISTORICAL CP6 CLOSURE TRUTH
= 20260826_08 / 68|5|14|75|95|68|120
= valid historical baseline only
```

## 1.1 Binding correction to the primary map

Where `timeline-temporal-operational-map.md` §28 or its source ledger discusses `68 / 5 / 14 / 75 / 95 / 68 / 120` as the CP6 closure baseline, interpret it as:

```text
HISTORICAL CP6 MATERIALIZATION BASELINE
NOT CURRENT PROTECTED-MAIN TOPOLOGY
```

For **current pre-vertical implementation planning**, the binding baseline is:

```text
20260906_18
89|5|18|77|173|91|272|0|0|0
```

No roadmap step may size schema work, migration work, tests, ACLs, dictionary drift or recovery impact from the historical CP6 counts as though they were current.

## 1.2 Why this does not reopen CP6 or the Physical Model

The correction is a current-state reconciliation, not an architecture change.

The Physical Model remains closed around:

```text
PostgreSQL 18
= sole canonical persistence + material-history authority
```

Later migrations are normal forward evolution.

Current implementation state does not rewrite historical CP6 evidence, and historical CP6 evidence does not override current implementation state.

---

# 2. Logical Model re-check

The Whole Logical Model is closed and classifies all accepted Domain concepts:

```text
57 / 57 Domain concepts classified
15 LR-01 native owners
0 Domain owner gap
0 unclassified
0 new Domain owner required
0 universal root required
```

The native LR-01 owner set remains exactly:

```text
Person
Living Referent
Asset
Place
Content Artifact
Collective
Possibility
Goal
Plan
Activity
Event
Routine
Occurrence
Session
Observation
```

For this temporal-operational vertical the most important exact dispositions are:

```text
Activity             LR-01 native identity-bearing record
Event                LR-01 native identity-bearing record
Routine              LR-01 native identity-bearing record
Occurrence           LR-01 when persistently addressable; lazy derivation allowed before materialization
Session              LR-01 native identity-bearing record

Schedule             LR-02 dependent semantic record; ScopedRecordRef when material/addressable
Actual               LR-06 realization; LR-02 + ScopedRecordRef when material/addressable
Outcome              LR-06 result; LR-02 when materially persistent/addressable

Temporal Constraint  LR-05 typed rule/specification
Recurrence           LR-05 typed rule/specification
Conditional Policy   LR-05 typed policy/specification

Confirmation         LR-03 typed semantic act/relation; ScopedRecordRef where addressed
Acknowledgement      LR-03 typed semantic act/relation; ScopedRecordRef only where independently addressable
Participation        LR-03 specific typed relation
Responsibility       LR-03 specific typed relation

Provenance           LR-07 typed lineage/history
Version              LR-07 material-state/history semantics; no universal Version root
Reconciliation       transient when low consequence; LR-02/LR-07 when material history/rationale/effect matters
```

This confirms that the primary map's TOP-LEVEL / CONTEXTUAL / DERIVED / INTERNAL classification is compatible with the closed Logical Model **only if those labels are understood as work-map/product classes rather than replacements for LR-01..LR-13**.

Canonical guardrail:

```text
work-map TOP-LEVEL
!= Logical LR-01 by definition

work-map CONTEXTUAL
!= one fixed Logical role

product DERIVED
!= canonical Domain identity
```

The Logical model remains the representation authority.

---

# 3. Whole-Logical hardenings explicitly carried into this vertical

The second audit confirms that the roadmap must actively preserve all WL-H01..WL-H12, not merely the temporal noun distinctions.

## WL-H01 — material terms/state ownership

Any consequential agreement/assent/confirmation-like binding to temporal state must target a justified MaterialState, not an ownerless `terms_id`, `version_id` or free-form snapshot.

## WL-H02 — governed operation/effect contract

Consequential operations such as:

- revise Schedule;
- cancel Activity/Event/Occurrence expectation;
- establish/correct Actual;
- establish Outcome;
- apply this-and-future Routine change;
- perform provider-affecting mutation;
- confirm a MaterialState;

must preserve where applicable:

```text
operation family
target owner/facet
material target state
effect semantics
input/context
purpose
preconditions
governance requirements
expected-state requirement
idempotency semantics
```

```text
HTTP route / UI button / AuthZ action
!= canonical governed effect
```

## WL-H03 — projection/disclosure surface

Timeline, Planning Tray, Resolution Queue, Analytics and provider-facing projections may expose a bounded derivation without exposing every source fact.

They need explicit source/material basis and disclosure semantics where consequential.

## WL-H04 — absence != false

Blocking for:

- no Actual;
- no Outcome;
- no Confirmation;
- no Participation evidence;
- no provider update;
- no available Schedule;
- no visible item.

None may be silently converted to a negative semantic value unless the owner-specific rule establishes that value.

## WL-H05 — expected-state concurrency

Consequential edits must reject/reconcile stale bases rather than silently overwrite current accepted material state.

Required especially for:

- Schedule revisions;
- Session pause/resume/end/correction;
- this-occurrence vs future-series edits;
- Actual/Outcome corrections;
- provider/user conflict resolution;
- offline replay.

## WL-H06 — idempotency != identity

Retry keys never become owner IDs, Request IDs, Session IDs or Occurrence IDs.

Same key + materially different operation must conflict/reject.

## WL-H07 — multi-owner atomicity / explicit staged reconciliation

A user-visible one-tap operation may need to atomically establish several semantic effects.

Example:

```text
Fatto
→ establish Actual
→ establish Outcome
→ record Confirmation
```

If all are required to present success, partial success must not be reported as complete success.

Across external provider boundaries where atomicity is impossible, represent explicit staged/partial/reconciliation state.

## WL-H08 — canonical != provider state

Example:

```text
DANTE accepted Schedule = 16:00
provider still           = 15:00
provider apply           = failed
```

This is representable without either side silently overwriting the other.

## WL-H09 — derived freshness

Timeline/Planning Tray/Resolution/Analytics caches are not canonical truth.

Consequential actions originating from a stale projection must revalidate/bind to the relevant material state rather than trust old rendered data.

## WL-H10 — retention/redaction/tombstone integrity

Deletion/privacy must not manufacture historical non-existence.

Where policy allows a minimal retained reference/tombstone:

```text
payload redacted/deleted
!= object never existed
```

This matters directly for:

- corrected Session history;
- deleted false Session versus redacted true history;
- provider tombstones;
- recurrence history;
- Confirmation/Acknowledgement attribution;
- analytics derived from data later deleted;
- relationship continuity.

## WL-H11 — consequential AuthZ provenance

Where material, reconstruct:

- actual Actor;
- represented party;
- Principal/security context;
- Authority basis;
- Consent/Visibility basis;
- MaterialStateRef(s);
- policy/model version;
- allow/deny decision;
- effect produced.

But:

```text
Principal != Actor
AuthZ decision != Authority
technical audit != Domain history automatically
```

## WL-H12 — non-interference/inference leakage

Selective disclosure applies to:

- counts;
- existence/nonexistence;
- Timeline placement;
- free/busy output;
- errors;
- ranking;
- analytics;
- explanations;
- candidate lists;
- conflict output;
- AI-generated summaries.

A safe derived result does not declassify its hidden source.

---

# 4. Calendar / Life Area second-pass hardening

The first deep map correctly gave `Palestra`, `Inglese`, `Lavoro`, etc. a product-organizational home rather than a new temporal kernel owner.

The second audit makes the complete Product behavior explicit.

## 4.1 Supported organizational lifecycle

A Calendar/Life Area capability may need product operations such as:

- create;
- rename;
- reorder;
- archive;
- hide/show;
- choose local visual recognition metadata such as name/icon/color;
- preserve user-selected visibility/order preferences;
- map one or more external calendars into a Life Area without merging source identity.

These operations are **organization management**, not Activity/Event/Routine lifecycle and not Timeline card mutation by default.

## 4.2 Primary organization versus secondary relationships

One planning item may have:

```text
one primary Calendar/Life Area
+
0..N tags
+
0..N Goal/Plan relations
+
Participation/Responsibility relations
+
Place
+
provider source mappings
```

No duplication is required to make the item visible in multiple views/relations.

## 4.3 Shared item local organization

The same canonical shared Event can be:

```text
Actor A local organization = Personal
Actor B local organization = Family
```

without duplicating shared Event identity or shared Actual occurrence.

Therefore local organizational profile may be actor-scoped even where the underlying item is shared.

## 4.4 Global scheduling awareness across hidden/grouped areas

Grouping/filtering is a projection choice, not a scheduling-truth boundary.

DANTE must still detect relevant:

- conflicts;
- workload pressure;
- travel/buffers;
- protected time;
- fixed commitments;
- replanning consequences;

across relevant calendars/life areas even when one group is collapsed or filtered from the current view.

A hidden conflicting item must not cease to exist for the scheduler.

The UI should surface hidden conflict/affected-item information where material rather than silently scheduling through it.

## 4.5 Appearance accessibility

Color can help recognition but cannot be the only carrier of:

- item type;
- sharing;
- priority;
- execution state;
- organization.

This remains a frontend/accessibility requirement, not Domain identity.

## 4.6 Logical placement caution

`LR-12 Product/organizational profile` is the available Whole-Logical role for product organizational profiles, but this audit **does not assert a new physical `life_area` entity/table**.

Before implementation the roadmap must prove the exact accepted Logical/Physical representation for Calendar/Life Area behavior.

If current Logical/Physical coverage is intentionally profile/configuration based, preserve it.

If implementation pressure demonstrates a real missing durable identity/lifecycle, that is a controlled reopen/extension question—not permission to create a new LR-01 owner by convenience.

---

# 5. Recurring meeting continuity hardening

The primary map includes rich Event before/during/after lifecycle. The second audit makes the recurring-meeting continuity requirements explicit so they are not lost inside generic `Event recurrence`.

A recurring meeting series/context may preserve reusable continuity such as:

- continuing purpose;
- recurring participant set/context;
- agenda template;
- previous decisions;
- unresolved items carried forward;
- commitments due before the next Occurrence;
- relevant documents;
- cadence changes;
- ownership/responsibility changes where applicable.

Each Occurrence must still preserve occurrence-specific:

- Schedule/current exception;
- Participation response/Actual attendance;
- agenda progress;
- notes;
- decisions;
- commitments;
- Outcome;
- provider state;
- history.

Before a later Occurrence, DANTE may derive a continuity brief from authorized history.

Canonical boundaries:

```text
series continuity context
!= one Occurrence

previous decision
!= current decision

carried unresolved matter
!= automatically accepted current agenda item

provider-generated recap
!= confirmed DANTE truth automatically
```

The map must therefore preserve recurring Event continuity as an Event/product relation problem, not invent `MeetingSeries` as a new kernel primitive unless later persistence evidence proves distinct identity/lifecycle.

---

# 6. Conditional Policy runtime hardening

The primary map correctly includes Conditional Policy, Reminder and review activation. The second audit preserves four runtime distinctions that must survive roadmap sequencing.

## 6.1 Transition versus persistent state versus repeated observation

These are not equivalent activation semantics:

```text
when value crosses below threshold
!= while value remains below threshold
!= every new qualifying Observation below threshold
```

A policy/runtime representation must preserve the intended behavior where repeated effects matter.

## 6.2 Duplicate Observation/import != duplicate activation

Receiving the same underlying provider fact twice must not automatically create two semantic activations/effects.

Runtime deduplication/idempotency must be based on bounded semantic operation/source identity rather than merely arrival count.

## 6.3 Competing policies

No universal winner is accepted among:

- newest policy;
- most specific policy;
- human policy;
- provider policy;
- AI proposal;
- largest priority number.

Detection and resolution are context/Authority/Decision/policy problems.

## 6.4 Loops/cycles

Policies can form cycles.

DANTE must be able to diagnose/prevent unsafe runtime loops through bounded execution safeguards, but the Domain does not declare policy graphs universally acyclic.

Potential runtime controls such as:

- recursion limits;
- idempotency;
- deduplication;
- debounce;
- retry limits;
- loop detection;
- compensation;

remain runtime concerns, not new Domain roots.

---

# 7. Privacy / retention / deletion hardening for temporal history

The temporal vertical intentionally stores highly reconstructible personal history. Therefore history completeness must not be confused with indefinite raw retention.

## 7.1 Purpose limitation

Each retained temporal category needs a product/system purpose such as:

- calendar operation;
- execution history;
- user-requested analytics/comparison;
- adaptive planning;
- safety/compatibility checks;
- reminder/integration support;
- audit/security/legal obligation.

Do not collect/retain unrelated raw data merely because PostgreSQL can store it.

## 7.2 Retention modes

Product/data governance may support, by category where practical:

- full-detail retention;
- reduced/aggregated history after a defined period;
- automatic deletion after a chosen period;
- manual deletion of records/categories;
- export before deletion;
- account-wide export/deletion.

## 7.3 Derived data after deletion

Deleting raw records must also address derived data still linkable to the user where required by the applicable retention/legal policy.

Analytics materialization cannot be used as a hidden undeletable copy of deleted source history.

## 7.4 Sensitive temporal data

Session/Activity/Event/Observation context may expose health, disability, medical, dietary, rehabilitation, location or other sensitive information.

Visibility, logging, notifications, provider export, AI prompts and analytics must independently respect the applicable privacy/consent boundary.

A safe `busy 18:00–20:00` projection need not reveal `medical appointment`.

## 7.5 Deletion versus semantic correction

Privacy/retention deletion is not semantic correction.

```text
real Session + wrong start
→ correction

false Session
→ invalidation/deletion policy

valid historical Session + user requests data erasure
→ retention/privacy deletion/redaction path
```

These may lead to different tombstone/reference behavior.

---

# 8. C1/F0/T1 exact frontend guard re-check

The vertical roadmap must start from the current frontend state rather than reconstructing old prototype assumptions.

## 8.1 C1 current product status

```text
engineering automated green
manual product acceptance still open
C1 not frozen
C2 blocked
```

The vertical map does not grant `C1 MANUAL PASS — APPROVED`.

## 8.2 Current C1 Simple Create

Desktop:

- floating;
- stable initial position;
- draggable;
- compact/title-first;
- Timeline/Home remains interactive and scrollable behind it;
- no modal dim/freeze;
- backdrop/outside click is not the silent close contract;
- close/Cancel/Escape respect dirty-draft protection.

## 8.3 Current C1 Advanced

Desktop:

- larger floating surface;
- same draft as Simple;
- bounded to viewport;
- internally scrollable;
- actions/back/close remain reachable;
- Timeline remains interactive.

Mobile:

- viewport bounded;
- no horizontal overflow.

Possible simple-only left pin/dock is **not** current authority.

## 8.4 Current Planning Tray behavior

- unplaced Activity lives in Planning Tray;
- anchored desktop popover / mobile bottom sheet;
- one-card carried drag;
- no scrim;
- no duplicate browser/native ghost;
- placement keeps the same Activity identity;
- Escape cancellation;
- supported removal/placement Undo.

## 8.5 Current all-day behavior

All-day is represented in a real per-day lane and participates in Timeline geometry.

Forbidden:

- global detached all-day strip as unrelated surface;
- fake 00:00–24:00 timed occupancy.

## 8.6 Event Agenda

Agenda/internal Event parts may map to Timeline subitems but do not become independent Domain owners automatically.

## 8.7 Current recurrence stop line

C1 authors recurrence specification only.

```text
browser does not generate canonical future Occurrences
```

## 8.8 T1 frozen behavior remains blocking

Do not alter without explicit user approval:

- custom drag grammar;
- first gesture drag;
- deselect-first focus;
- title/time/subitem action regions;
- no native browser drag ghost/text selection;
- deterministic overlap geometry;
- expanded group/header geometry alignment;
- move + Undo;
- anchored time editor;
- Firefox critical regression behavior.

## 8.9 F0 operation semantics remain inherited

- explicit Clock;
- placement semantic forms;
- operationId idempotency;
- idempotency collision rejection;
- expected revision;
- stale mutation rejection;
- `applied / no-op / rejected / failed`;
- `pending != success`;
- guarded Undo;
- monotonic revision after Undo;
- no fake network/storage/server.

---

# 9. Current PostgreSQL / Alembic / same-change guard

Any future temporal persistence change must start from current head:

```text
20260906_18
```

and preserve the existing accepted migration graph. No historical migration may be rewritten, flattened, renumbered or rebased merely to make the vertical simpler.

A real structural change is incomplete until the same reviewed slice aligns, as applicable:

```text
accepted semantic authority
+
forward Alembic
+
SQLAlchemy mapping/MetaData
+
Database Dictionary
+
current human DB reference
+
direct tests
+
real PostgreSQL proof
+
ACL/security proof
+
recovery impact/proof where required
```

The current runtime/migration/owner/observer role separation remains in force.

No temporal feature is allowed to bypass DB ACL/persistence doctrine because it is called `technical`, `sync`, `analytics` or `timeline` data.

---

# 10. Physical target implications rechecked

The accepted Physical target remains:

```text
PostgreSQL 18         canonical truth/material history
PowerSync + encrypted SQLite target
                      bounded local/sync state, noncanonical
PostgreSQL outbox     bounded async
Restate target        durable Class-B runtime when activated
OR-Tools CP-SAT       solver candidate state
OTel/Grafana          operational telemetry
```

For this vertical:

## 10.1 Offline/sync

PowerSync/SQLite target does not imply it is already activated for temporal data.

When activated:

```text
local/synced projection != canonical PostgreSQL truth
```

Consequential offline writes still require governed reconciliation/revalidation.

## 10.2 Durable execution

Long-lived future operations such as provider reconciliation or notification delivery may eventually need durable runtime semantics, but selection/activation of Restate for a concrete workflow must follow the accepted Physical/runtime gate rather than being assumed by the semantic map.

## 10.3 Solver

OR-Tools may produce candidate schedules/replans.

```text
solver candidate != accepted Schedule
```

The candidate must pass current constraints, Authority/policy and expected-state validation before effect.

---

# 11. Source-to-process coverage matrix — second audit

| Source pressure | Required process home | Verdict |
| --- | --- | --- |
| Activity identity/completion/sub-Activity/responsibility | Activity vertical slice | PRESENT |
| Event original/current/Actual + postponed/TBD | Event/Schedule/Actual slices | PRESENT |
| meeting before/during/after lifecycle | Event slice | PRESENT |
| recurring-meeting continuity | Event recurrence + product continuity | HARDENED HERE |
| Routine policy/composite/pause/end/revision | Routine slice | PRESENT |
| six Recurrence semantic families | Recurrence slice | PRESENT |
| four currently materialized CP6 recurrence families | persistence/runtime mapping gate | PRESENT |
| Occurrence virtual/materialized/current/history | Occurrence slice | PRESENT |
| this occurrence vs future | Routine/Event source + Occurrence boundary | PRESENT |
| Schedule accepted vs proposed/current/history | Schedule slice | PRESENT |
| early/late Actual without reschedule | Session/Actual comparison | PRESENT |
| explicit expected-end change during execution | Schedule revision | PRESENT |
| temporal constraints/deadline/window/spacing | Temporal Constraint slice | PRESENT |
| Session open/pause/resume/end | Session runtime | PRESENT |
| manual/timer/import capture | Session runtime/provenance | PRESENT |
| stale timer/split/merge/correction | Session reconciliation | PRESENT |
| web/mobile/offline/device clock | Session sync/runtime | PRESENT |
| Actual unknown vs known non-realization | Actual slice | PRESENT |
| Outcome contextual result | Outcome slice | PRESENT |
| Confirmation exact MaterialState | Confirmation slice | PRESENT |
| Acknowledgement/common ground | Acknowledgement boundary | PRESENT |
| daily/weekly resolution review | Resolution Queue | PRESENT |
| automatic outcomes | Conditional Policy + governed effect | PRESENT |
| reminder intent vs delivery | Conditional Policy + external notification boundary | PRESENT |
| transition/persistent/repeated activation | Conditional runtime | HARDENED HERE |
| duplicate import != duplicate activation | Conditional/runtime idempotency | HARDENED HERE |
| policy conflict/loop | Conditional runtime/reconciliation | HARDENED HERE |
| Calendar/Life Area primary organization | product organization | PRESENT |
| rename/reorder/archive/hide | organization management | HARDENED HERE |
| shared item different local area | product organization + actor scope | HARDENED HERE |
| hidden groups still affect conflicts | range/scheduling projection | HARDENED HERE |
| Context != appearance | frontend/product organization | PRESENT |
| prototype groups != taxonomy | frontend mapping | PRESENT |
| Timeline projection != truth | read model | PRESENT |
| Planning Tray unplaced same identity | derived projection | PRESENT |
| Resolution Queue != notification feed | derived projection | PRESENT |
| analytics/planned-vs-actual/overlap | analytics | PRESENT |
| corrected current truth vs audit | history/analytics | PRESENT |
| Clock/timezone/DST/precision | temporal infrastructure | PRESENT |
| provider id != DANTE id | integration/reconciliation | PRESENT |
| provider state != canonical state | reconciliation | PRESENT |
| F0 idempotency/revision/Undo | application operations | PRESENT |
| T1 frozen behavior | frontend change control | PRESENT |
| C1 manual acceptance remains open | frontend lifecycle gate | PRESENT |
| WL-H01..WL-H12 | every implementation slice | HARDENED HERE |
| retention/redaction/tombstones | cross-cutting data lifecycle | HARDENED HERE |
| sensitive-data disclosure | Visibility/privacy boundary | HARDENED HERE |
| current DB 20260906_18 topology | pre-implementation baseline | CORRECTED HERE |
| current Alembic DAG preservation | persistence gate | HARDENED HERE |
| current Dictionary/SQLAlchemy/live alignment | same-change persistence gate | HARDENED HERE |

---

# 12. Second-audit findings classification

The second audit found **no new Domain owner** and **no need to collapse existing concepts**.

It did find the following hardenings:

```text
SA-01 CURRENT-DB-TRUTH
historical CP6 counts must not be presented as current protected-main topology
→ corrected by this overlay

SA-02 LOGICAL-WHOLE
WL-H01..WL-H12 must be explicit roadmap gates, not background reading only
→ hardened

SA-03 ORGANIZATION-LIFECYCLE
rename/reorder/archive/hide + actor-local organization + hidden-conflict awareness must not be lost
→ hardened

SA-04 RECURRING-MEETING-CONTINUITY
series continuity must not disappear inside generic recurrence
→ hardened

SA-05 CONDITIONAL-RUNTIME
transition/persistent/repeated observation, duplicate activation, policy conflict and loops must remain explicit runtime requirements
→ hardened

SA-06 RETENTION-PRIVACY
temporal-history completeness must coexist with deletion/redaction/sensitive disclosure policy
→ hardened

SA-07 FRONTEND-CURRENT-TRUTH
C1 exact current floating/nonmodal/manual-open behavior, Planning Tray and T1/F0 gates remain binding
→ reverified

SA-08 ALEMBIC-SAME-CHANGE
future temporal schema work starts at 20260906_18 and must align Alembic/SQLAlchemy/Dictionary/docs/tests/live PostgreSQL
→ hardened
```

---

# 13. Roadmap admission gate after second audit

A roadmap may be designed only if it explicitly consumes **both**:

```text
timeline-temporal-operational-map.md
+
timeline-temporal-operational-second-audit-2026-09-07.md
```

and starts from current protected-main repository/database truth.

Roadmap design must therefore answer, for every implementation block:

1. exact semantic owner/capability;
2. relevant `!=` boundaries;
3. Logical LR role(s);
4. current Physical/DB representation already present;
5. whether any new persistence is actually required;
6. exact governing MaterialState/current binding where consequential;
7. expected-state/idempotency/atomicity behavior;
8. historical/provenance/reconciliation behavior;
9. authority/visibility/privacy implications;
10. frontend surface and inherited C1/F0/T1 behavior;
11. range/read-model/analytics implications;
12. provider/offline/runtime implications;
13. exact tests/direct PostgreSQL proof if persistence changes;
14. recovery and migration same-change obligations;
15. manual product acceptance where UX changes.

No block may be implemented merely because it is the next noun in the tree.

Dependencies and semantic foundations determine order.

---

# 14. Current second-audit verdict

```text
SECOND COMPLETENESS AUDIT
COMPLETE

NEW DOMAIN OWNER REQUIRED                    0
SEMANTIC COLLAPSE REQUIRED                   0
REVIEWED CAPABILITY WITHOUT PROCESS HOME     0
REVIEWED GAP UNCLASSIFIED                    0

CURRENT-TRUTH DRIFT FOUND                    1
CURRENT-TRUTH DRIFT CORRECTED                1

ADDITIONAL EXPLICIT HARDENINGS               7

PRIMARY MAP                                  ACTIVE DRAFT / GAP-AUDITED
SECOND-AUDIT COMPANION                       CURRENT REQUIRED COMPANION
ROADMAP ORDER                                NOT YET FIXED
PRODUCT IMPLEMENTATION                       NOT STARTED BY THIS AUDIT
DDL/API AUTHORIZATION                        NONE
MAIN MODIFICATION                            NONE
```

The important result is not `nothing can ever be discovered later`.

The correct result is:

> **Every requirement and implementation pressure explicitly re-reviewed in this checkpoint now has a defined semantic/process home, while the one stale current-database presentation discovered by the independent second pass has been explicitly corrected before roadmap design.**
