# Workstream — Core Domain Model v0

- Status: **IN PROGRESS**
- Active branch: `feature/domain-model`
- Base: `main` at `73f0d172de239853e568532535a4739ce77a0877`
- PR: none yet
- Work type: domain modeling / invariants / persistence preparation
- Current execution mode: documentation/modeling slice independent from backend implementation

## Purpose

Turn the LifeOS product vocabulary and requirements into an implementation-ready domain model without prematurely designing every specialist module or every final SQL table.

This pass explicitly revalidates earlier concepts instead of treating prior documentation as automatically correct. Earlier product definitions remain valuable inputs, but a concept can be revised when broader scenario coverage, stronger reasoning, external benchmarks, implementation constraints, or later cross-cluster tests reveal a better model.

## Current decision rule

**Accepted means current best decision, not immutable decision.**

Decisions may be reopened when new evidence, edge cases, contradictions, or better abstractions emerge. Changes must be explicit, reasoned, and preserved in history rather than silently rewriting prior assumptions.

The active modeling method, documentation standard, benchmark/interoperability rule, mandatory concept-review protocol, and Validation Methodology v2 live in the Domain Atlas.

## Required reading

1. [`../PROJECT-STATUS.md`](../PROJECT-STATUS.md)
2. [`../development/operating-rules.md`](../development/operating-rules.md)
3. [`../domain/README.md`](../domain/README.md)
4. [`../domain/validation-methodology-v2.md`](../domain/validation-methodology-v2.md)
5. [`../domain/checkpoints/intention-execution-v0.md`](../domain/checkpoints/intention-execution-v0.md)
6. [`../domain/checkpoints/time-v0.md`](../domain/checkpoints/time-v0.md)
7. [`../domain/checkpoints/cross-cluster-validation-v2.md`](../domain/checkpoints/cross-cluster-validation-v2.md)
8. [`../domain/concepts/goal.md`](../domain/concepts/goal.md)
9. [`../domain/concepts/plan.md`](../domain/concepts/plan.md)
10. [`../domain/concepts/activity.md`](../domain/concepts/activity.md)
11. [`../domain/concepts/event.md`](../domain/concepts/event.md)
12. [`../domain/concepts/routine.md`](../domain/concepts/routine.md)
13. [`../domain/concepts/milestone.md`](../domain/concepts/milestone.md)
14. [`../domain/concepts/occurrence.md`](../domain/concepts/occurrence.md)
15. [`../domain/concepts/schedule.md`](../domain/concepts/schedule.md)
16. [`../domain/concepts/session.md`](../domain/concepts/session.md)
17. [`../domain/concepts/temporal-constraint.md`](../domain/concepts/temporal-constraint.md)
18. [`../domain/concepts/recurrence.md`](../domain/concepts/recurrence.md)
19. [`../domain/concepts/availability-capacity.md`](../domain/concepts/availability-capacity.md)
20. [`../product/v1-core-domain-glossary.md`](../product/v1-core-domain-glossary.md)
21. [`../product/v1-goal-and-program-lifecycle.md`](../product/v1-goal-and-program-lifecycle.md)
22. [`../product/v1-execution-status.md`](../product/v1-execution-status.md)
23. [`../product/v1-confirmation-and-reminders.md`](../product/v1-confirmation-and-reminders.md)
24. [`../product/v1-scheduling-flexibility.md`](../product/v1-scheduling-flexibility.md)
25. [`../product/v1-data-history-and-privacy.md`](../product/v1-data-history-and-privacy.md)
26. [`../product/feature-discovery-simulation-2026-08.md`](../product/feature-discovery-simulation-2026-08.md)
27. [`../architecture/personal-data-ai-integration.md`](../architecture/personal-data-ai-integration.md)
28. [`../decisions/ADR-003-primary-database.md`](../decisions/ADR-003-primary-database.md)
29. [`../decisions/ADR-006-hybrid-personal-data-model.md`](../decisions/ADR-006-hybrid-personal-data-model.md)

## Where to work

The current work is a clearly separated documentation/modeling slice, so it is running on `feature/domain-model` without backend implementation changes.

When persistence mapping and backend package boundaries begin to overlap materially with Backend Foundation, the branches/workstreams must be synchronized deliberately before implementation. Do not run two branches against the same implementation/domain files merely to make the workstreams look separate on paper.

The Domain Model handoff remains separate so decisions and unresolved questions can be resumed independently by another agent.

## Rules

- Revalidate concepts one at a time; do not inherit terminology merely because it already exists.
- Retain every applicable original scenario/boundary/history test and enrich it with Validation Methodology v2 rather than replacing prior validation.
- For every concept, inspect applicable internal documentation/scenarios and perform enough targeted external benchmarking to expose likely missing semantics before acceptance.
- External standards/products are evidence, not compatibility requirements or design authorities; preserve LifeOS semantics first and push provider-specific compromises into adapters when practical.
- Benchmark systems outside the personal-productivity category when they solve a relevant hard problem well; classify findings as borrow/adapt/already-stronger/anti-pattern/not-applicable.
- Canonical Domain Atlas documentation is maintained in English; discussion language does not create a second canonical translation tree.
- Do not model one table per life topic (`english`, `photography`, `farming`, etc.).
- Do not collapse everything into one `entities` table or arbitrary JSON blob.
- Do not treat AI inference as confirmed truth.
- Keep operational policy separate from domain/topic type where behavior differs by user/plan.
- Preserve planned/actual/history distinctions.
- Preserve original intention when later evidence reveals additional relevance; do not rewrite history to make past execution look intentionally linked to a Goal when it was not.
- Prefer progressive formalization: generic first when genuinely unpredictable; promote repeated/query-heavy concepts through reviewed migrations.
- Preserve progressive disclosure: kernel precision must not force simple users to configure or understand the internal ontology.
- Do not reopen an accepted architectural ADR merely because a first implementation mapping is inconvenient; propose an explicit ADR change when new evidence genuinely challenges the architecture.
- Preserve earlier documents while conflicts are being revalidated; propagate replacements deliberately after related concepts are understood.
- Run cluster checkpoints and cross-cluster validation in addition to concept-level reviews; do not defer all cross-model validation until the end.

# Validated baseline — first two clusters

The first two clusters are now individually and jointly validated as current baselines.

```text
Intention & Execution v0 — PASS
Time v0                 — PASS
Cross-cluster v2        — PASS
```

These are current best decisions, not permanent closure.

Any concept may be reopened by future user-led tests, downstream cluster work, persistence mapping, implementation evidence, integration constraints, or stronger external patterns.

---

## Validated cluster — Intention & Execution v0

Status: **PASS — current validated cluster baseline**.

Validated concepts:

- Goal v0;
- Plan v0;
- Activity v0;
- Event v0;
- Routine v0;
- Milestone v0.

Checkpoint:

- [`../domain/checkpoints/intention-execution-v0.md`](../domain/checkpoints/intention-execution-v0.md)

The cluster was subsequently re-tested under Validation Methodology v2 together with the Time cluster and remained valid.

Key conclusions:

- no universal parent/child hierarchy is required;
- Goal remains desired-condition semantics rather than execution strategy;
- Plan remains coordination/strategy rather than an executable Activity;
- Activity remains action-centred;
- Event remains occurrence-centred even when Schedule changes;
- Routine remains recurring behavior/execution policy rather than Recurrence syntax;
- Milestone remains a contextual meaningful checkpoint, with an explicit future re-test against Outcome and GoalCriterion;
- valid later Evidence may become relevant to Goals without rewriting the source execution's historical intention.

Validation Methodology v2 additionally hardened:

### Routine vs Plan progression

Routine can be composite/adaptive, but materially changing long-horizon stages, strategy transitions, milestones, and multiple recurring policies tend toward Plan rather than one mega-Routine.

Record: [`../domain/concepts/routine.md`](../domain/concepts/routine.md)

### Event without current Schedule

Event temporal meaning remains intrinsic, but an Event that is postponed/unresolved can retain identity and historical expectation while temporarily having no current accepted Schedule.

Record: [`../domain/concepts/event.md`](../domain/concepts/event.md)

---

## Validated cluster — Time v0

Status: **PASS — current validated cluster baseline**.

Validated concepts:

- Occurrence v0;
- Schedule v0;
- Session v0;
- Temporal Constraint v0;
- Recurrence v0;
- Availability & Capacity v0.

Checkpoint:

- [`../domain/checkpoints/time-v0.md`](../domain/checkpoints/time-v0.md)

Key combined result:

```text
appears in time
!= accepted Schedule
!= capacity consumed
!= resource unavailable
!= recurring instance identity
!= Temporal Constraint
!= actual execution
```

The Time model remains composable rather than one calendar mega-object.

---

## Occurrence v0 — validated current baseline

`Occurrence` is the stable logical identity of one expected instance produced by a recurring/generative source.

Key decisions:

- identifies **which expected instance**, not when it is currently scheduled;
- distinct from Routine, recurring source/series, Recurrence, Activity, Event, Schedule, Session, and Actual;
- identity does not depend on current start/end or resolved UTC instant;
- rescheduling does not automatically create a new Occurrence;
- skip/cancellation/non-execution may remain historically identifiable;
- one-off Activity and Event normally use their own identity without artificial Occurrence wrappers;
- may exist before exact Schedule placement;
- may later be realized through multiple Sessions;
- future Occurrences may remain virtual/derived until instance-specific history requires persistent reconstruction;
- historical Occurrences retain enough source/version context to prevent later source revisions from rewriting history.

Record: [`../domain/concepts/occurrence.md`](../domain/concepts/occurrence.md)

---

## Schedule v0 — validated current baseline

`Schedule` is the current accepted temporal assignment of a schedulable subject.

Key decisions:

- answers **when execution/occurrence is currently intended or expected**, not what the subject is;
- remains distinct from Activity, Event, Occurrence, Actual, Session, Deadline/Target, Temporal Constraint, Recurrence, Routine, Movement Policy, and Availability/Capacity;
- AI/system suggestion remains proposal until accepted by user authority or authorized policy;
- Activity may exist without Schedule;
- Occurrence may exist before exact Schedule placement;
- Event identity can survive Schedule revision and can temporarily survive with no current Schedule after postponement/unresolved timing;
- Schedule revision preserves subject identity and history;
- Actual deviation does not silently rewrite Schedule;
- precision may remain date-only, coarse, exact, start-only, interval-based, floating local, named-zone local, or absolute-instant;
- one schedulable subject may have multiple accepted planned placements;
- estimated effort, scheduled duration, and actual duration remain distinct;
- Schedule presence does not imply busy/capacity reservation.

Record: [`../domain/concepts/schedule.md`](../domain/concepts/schedule.md)

---

## Session v0 — validated current baseline

`Session` is a persistent record of one bounded episode of actual execution or performed behavior.

Key decisions:

- Session is actual execution, never canonical planned placement;
- distinct from Schedule, Activity, Occurrence, Routine, Event attendance/actual occurrence, and broader Actual/Outcome;
- one Activity/Occurrence may have zero, one, or many Sessions;
- planned placements and Sessions do not require one-to-one mapping;
- Session may exist without prior Schedule;
- spontaneous execution may be captured without fabricating pre-existing intention;
- pause does not automatically create a new Session;
- one Session may contain multiple active intervals;
- elapsed, active, and paused duration remain conceptually distinct;
- explicit end followed by later restart normally creates another Session;
- overlap is not globally forbidden;
- analytics must not naïvely sum overlapping elapsed time;
- Event attendance does not create redundant Session records by default.

Record: [`../domain/concepts/session.md`](../domain/concepts/session.md)

---

## Temporal Constraint v0 — validated current baseline

`Temporal Constraint` restricts or prefers placement, duration, or temporal relationships without becoming Schedule or Actual.

Key decisions:

- answers when execution/occurrence is allowed, required, bounded, or preferred;
- distinct from Schedule, Session/Actual, Recurrence, Availability/Capacity, and movement authority;
- Deadline is a latest-bound Temporal Constraint semantic specialization rather than a separate kernel primitive;
- Window is a range shape whose meaning depends on semantic role;
- target/review dates do not automatically become scheduling constraints;
- hard constraints define planner admissibility while soft constraints guide optimization;
- strength and authority/mutability remain separate;
- Actual that violates a hard rule remains valid history;
- a passed Deadline does not automatically assert `missed`;
- infeasible combinations remain representable and must be surfaced rather than silently violated;
- scoped constraints and Occurrence-specific exceptions do not require destructive source-policy rewrite.

Record: [`../domain/concepts/temporal-constraint.md`](../domain/concepts/temporal-constraint.md)

---

## Recurrence v0 — validated current baseline

`Recurrence` is a structured repeating-pattern capability rather than the recurring source, Occurrence, Schedule, Actual, or a generic automation engine.

Key decisions:

- distinct from Routine and recurring Event semantics;
- distinct from Occurrence, Schedule, Session/Actual, Temporal Constraint, and Trigger;
- supports calendar/wall-clock, elapsed, quota-per-period, completion-relative, anchor-stream-relative, and cyclic families;
- may produce logical expected Occurrences without exact timestamps;
- wall-clock `daily 08:00` is not automatically `every 24 elapsed hours`;
- floating/user-local, named-zone, and absolute/elapsed semantics remain distinguishable;
- pattern anchor and effective range remain separate;
- expected-occurrence count is not successful-completion count;
- completion-relative chains depend on qualifying Actual/fact anchors;
- one-off Occurrence/Schedule exceptions do not mutate future recurrence automatically;
- structural `this and future` change is an effective source/Recurrence revision;
- future purely virtual instances may regenerate, while instance-specific history must be reconciled rather than disappearing;
- natural-language input and provider recurrence syntax are not canonical normalized truth;
- external recurrence formats remain optional adapter targets, not kernel authorities.

Validation Methodology v2 hardening:

- quota-per-period recurrence preserves enough **period-frame semantics** to determine membership/boundaries when calendar/timezone/boundary interpretation can materially change the expected set;
- equivalent logical quota Occurrences do not receive arbitrary first/second/third semantics unless meaningful ordering is explicitly established.

Record: [`../domain/concepts/recurrence.md`](../domain/concepts/recurrence.md)

---

## Availability & Capacity v0 — validated current baseline

`Availability & Capacity` separates resource schedulability from accepted temporal placement.

Key decisions:

- Availability answers when a schedulable resource has capacity that may be used;
- Capacity answers what compatible commitments the resource can sustain;
- Reservation/Claim represents capacity committed, occupied, protected, or held;
- Effective Free Capacity is derived rather than canonical stored empty intervals;
- Schedule and Capacity Reservation remain distinct;
- scheduled does not automatically mean busy;
- Availability is distinct from Temporal Constraint and preference;
- Capacity is not universally binary and not universally one scalar/percentage;
- timestamp overlap alone does not establish conflict;
- overbooking/conflicting reality remains representable;
- recurring Availability may reuse Recurrence without execution Occurrences;
- positive/negative overrides can modify baseline availability temporarily;
- Temporary Mode may later alter capacity/availability without rewriting stable baseline;
- Event participation/all-day placement does not automatically determine capacity impact;
- external free/busy remains imported evidence/provenance;
- Calendar Block is useful UI/product language but not a mandatory kernel primitive.

Record: [`../domain/concepts/availability-capacity.md`](../domain/concepts/availability-capacity.md)

---

# Cross-cluster Validation v2

Status: **PASS — current combined baseline**.

Record:

- [`../domain/checkpoints/cross-cluster-validation-v2.md`](../domain/checkpoints/cross-cluster-validation-v2.md)

The validation applied:

- original scenario/boundary/history tests;
- Real-World Workflow Inversion;
- deep chronological simulation;
- adversarial reductio;
- semantic redundancy/merge-split tests;
- downward composition;
- upward reconstruction;
- lateral propagation;
- orphan/independence testing;
- external cross-domain benchmark and anti-pattern review;
- scale/history stress;
- simple-user versus power-user analysis.

Results:

```text
12 concepts retained
0 justified primitive merges
0 new cross-cluster primitives required
0 forced universal hierarchy
0 historical-intention rewrites required
```

The model supports both top-down planning and bottom-up retrospective capture.

A spontaneous Session can exist without LifeOS fabricating an Activity/Routine/Plan/Goal that did not historically exist.

One Event/Session/fact can later become relevant to multiple Goals/domains without duplicating the source fact.

This lateral behavior confirms a future requirement for typed semantic relationships rather than one universal untyped `related_to` link.

---

# Validation watchlist

The following boundaries are sound now but must be explicitly re-tested when their strongest adjacent concepts are modeled.

## Milestone vs Outcome vs GoalCriterion

Milestone is currently justified as contextual checkpoint identity, but Outcome/GoalCriterion will be its strongest redundancy challenge.

## Plan vs Routine

Current boundary remains deliberately soft. Complex progression/adaptation should continue to challenge it.

## Event participation vs personal commitment

Shift swaps, delegation, attendance, and multi-participant semantics may refine Event/Relationship modeling without changing the Time kernel.

## Completion-relative Recurrence vs Trigger / relative Constraint

Current boundary remains sufficient but should be revisited when Trigger and Actual-anchor qualification are formalized.

## Availability/Capacity vs Resource

Time semantics are sound; resource identity and quantitative dimensions belong to later Resource/Subject modeling.

## Session vs Actual

Session remains justified as bounded execution episode; broader Actual must later avoid duplicating it.

## Relationship typing/direction

Lateral cross-domain tests indicate that `supports`, `conflicts_with`, `prepares_for`, `depends_on`, `evidence_for`, `replaces`, etc. cannot all safely collapse into one semantic-free generic link.

---

# Current task — user-led brainstorming / questions / additional tests

**Do not automatically start the Observed Reality & Evidence cluster.**

The explicitly agreed next step is:

> **User-led architecture/product brainstorming, questions, and additional tests before selecting the next Domain Atlas cluster.**

The next discussion may:

- challenge the current architecture from a higher-level product perspective;
- reopen any accepted concept;
- add new validation methods;
- test other real-world workflows;
- compare LifeOS against additional systems/architectures;
- examine scalability, performance, UX, AI, integration, data ownership, or extensibility;
- decide whether the eventual next cluster should be Observed Reality & Evidence or something else.

No cluster order after this point is automatic.

---

# Current conceptual direction

```text
Goal         -> what is wanted
Plan         -> how it is intended to be pursued or organized
Activity     -> what concrete action is intended
Event        -> what occurrence-centred thing is expected to happen
Routine      -> what recurring behavioral/execution policy is intended
Milestone    -> what meaningful contextual checkpoint is expected/reached
Recurrence   -> how a recurring/generative pattern repeats
Occurrence   -> which individual expected generated instance exists
Constraint   -> where/when execution is allowed, required, or preferred
Availability -> when schedulable capacity may be used
Capacity     -> ability to accept compatible commitments
Schedule     -> when execution/occurrence is currently accepted to happen
Session      -> which actual execution episode happened
Actual       -> broader truth about what happened
Evidence     -> what supports evaluation
```

The following concepts are displayed only to show known downstream semantic space; Actual/Evidence are not yet accepted Domain Atlas concepts.

---

# Important unresolved downstream questions

The first two clusters deliberately leave these areas open:

- Actual / Outcome / Observation / Evidence / Confirmation / Provenance boundaries;
- GoalCriterion persistence/evaluation model;
- semantic Relationship vocabulary and directionality;
- Participant semantics;
- Resource / Asset / Subject model;
- Register / Quantity / movement/balance model;
- Trigger / Reminder / automation boundary;
- Temporary Mode;
- Decision / Version / revision policy;
- exact lifecycle state machines;
- external provider authority/reconciliation;
- recurrence DSL/resolver/materialization storage;
- exact capacity dimensions/reservation persistence;
- persistence/API/logical/physical PostgreSQL model;
- offline/sync conflict resolution;
- AI context/proposal/authority implementation.

These are downstream dependencies, not current failures.

---

# Output expected before broad persistence implementation

Before broad persistence/backend implementation, the full Domain Atlas should eventually establish:

- concise conceptual model;
- entity/value-object boundaries;
- key invariants;
- ownership/context model;
- lifecycle/state distinctions;
- structural relationship map;
- dynamic relationship/provenance rules;
- AI authority/proposal boundaries;
- first logical persistence mapping for the initial vertical slice;
- explicit list of questions intentionally deferred;
- final whole-domain stress-test result.

## First implementation target

The current working implementation target remains conceptually around:

`Workspace → Goal/Plan → Activity/Event/Routine/Milestone → Recurrence/Occurrence/Constraint/Availability/Capacity/Schedule/Session → later Actual/Confirmation`

This is a working direction, not a final persistence schema and not permission to implement the downstream concepts before their review.

---

# Handoff

- Active branch: `feature/domain-model`
- PR: none
- Base main commit: `73f0d172de239853e568532535a4739ce77a0877`
- Intention & Execution Cluster v0: **PASS / validated current baseline**
- Time Cluster v0: **PASS / validated current baseline**
- Cross-Cluster Validation v2: **PASS / validated current combined baseline**
- Validation Methodology v2: active validation standard
- Completed current baselines: `Goal v0`, `Plan v0`, `Activity v0`, `Event v0`, `Routine v0`, `Milestone v0`, `Occurrence v0`, `Schedule v0`, `Session v0`, `Temporal Constraint v0`, `Recurrence v0`, `Availability & Capacity v0`
- Goal concept commit: `084394ef5523517139335b5e5496aa0e4862c737`
- Plan concept commit: `7a5b9962abb503aa9532daf2acf41af23d699060`
- Activity final concept commit: `f2b2db24bd26684bd58aa925478a1623bf2316fc`
- Event original concept commit: `84e460ba31d5b88b1f415d27d8254803358109f4`
- Routine original concept commit: `f0de8c241d7650bbdbaffdf1b8cb102facf713fc`
- Milestone concept commit: `46ddf9d4bdc514fc56a718a93ad0258a2aa34a4b`
- Intention/execution checkpoint commit: `646f41452c357010550f3fa0ab96147518ddaa4c`
- Occurrence concept commit: `a55fa28b2fb27b1967d18f26b318b173972e35ee`
- Schedule original concept commit: `e716e6ad16391f20bd9264c84733dc4f88da4ef8`
- Session concept commit: `fef80394849e38e9215303b3ee6b1813ef3621a0`
- Temporal Constraint concept commit: `de3a6bb8ca78a7c2f429cf2986c65f084592ac64`
- Recurrence original concept commit: `58e2c50bcfac45a7a5ad8b5140b90040038fddae`
- Availability & Capacity concept commit: `87881b5ddd2ae7952e1982a3624d0a1f1b261833`
- Validation Methodology v2 commit: `177e019a07dab46464b22a4a3ae17a3777afd494`
- Time checkpoint commit: `7b07d56a433edb2d955f14a7ae40b0bca33a289c`
- Cross-cluster validation v2 commit: `dd25597819ae7b843da46a15cc9790f3bdff83e6`
- Routine v2-hardening commit: `dc1de46b02efccb646fb4073adf43c196caba048`
- Event v2-hardening commit: `750fa0b7116873e0b9fe9c53118d52a8d6133424`
- Recurrence v2-hardening commit: `f5b75da4dea3bbfcd6b53fc63ab2fdb302e65707`
- Schedule v2-hardening commit: `024c6422d61f2d57819f2f9cd7b702db913b7967`
- Backend implementation: not started in this branch
- Main modified: no
- Phase 4 prototype branch modified: no
- Current task: **user-led brainstorming/questions/additional tests before selecting the next Domain Atlas cluster**
- Known documentation conflicts: older glossary assumes Goal/Program/Project are distinct and uses narrower Activity/Event/Routine/Calendar Block semantics; active Domain Atlas baselines supersede those definitions for this workstream pending deliberate reconciliation after related clusters are stable.
