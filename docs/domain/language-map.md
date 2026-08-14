<!-- LIFEOS-CANONICAL-SPLIT document="language-map.md" part="1" total="5" -->
> **Canonical document split — Part 1 of 5.** Parts 1–5 together form one authoritative document; this is a physical split only, not a summary/reference hierarchy. The payload preserves the full pre-compaction baseline first and later downstream amendments in sequence; later explicit amendments override stale status/deferral wording without deleting the earlier rationale. Navigation: **Part 1** · [Part 2](language-map-part-2.md) · [Part 3](language-map-part-3.md) · [Part 4](language-map-part-4.md) · [Part 5](language-map-part-5.md)

<!-- LIFEOS-CANONICAL-PAYLOAD -->
# LifeOS Domain & Product Language Map

**Status:** Canonical terminology reference for the active Domain Atlas  
**Established:** 2026-08-11  
**Current revision:** 2026-08-12 — Participation v0 PASS WITH HARDENING; intended/response involvement separated from Actual Participation  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

This is the fast canonical reference for LifeOS vocabulary.

It keeps four distinct languages aligned without forcing a one-to-one mapping:

```text
DOMAIN LANGUAGE
what the concept means canonically
        ↓
PRODUCT LANGUAGE
how LifeOS packages/presents it
        ↓
UI LANGUAGE
what users actually read/manipulate
        ↓
IMPLEMENTATION LANGUAGE
API / schema / code names once designed
```

Canonical rule:

> **A domain concept does not require a dedicated visible UI object, and a visible product/UI term does not automatically justify a separate domain primitive.**

Detailed lifecycle, invariants, history, evidence and validation remain in the concept specs/checkpoints.

---

# 1. Terminology authority and precedence

When terminology conflicts, use this order:

1. accepted Domain Atlas concept specification;
2. this Domain & Product Language Map;
3. current Domain Atlas checkpoint / cross-cutting guardrail;
4. active workstream handoff;
5. current V1 product behavior documents;
6. historical product glossaries/planning documents;
7. conversation history.

The old `docs/product/v1-core-domain-glossary.md` remains useful product-history evidence but is not authoritative where the current Domain Atlas differs.

This map records decisions; it does not create primitives.

---

# 2. Term status classes

## CANONICAL

Accepted Domain Atlas concept/capability/value/role/relation semantics with stable current semantics.

```text
Goal
Plan
Activity
Event
Routine
Milestone
Occurrence
Schedule
Session
Temporal Constraint
Recurrence
Availability
Capacity
Actual
Outcome
Observation
Confirmation
Evidence
Provenance
Quantity
Subject (semantic role, not entity)
Person (native human entity)
Actor (semantic agency role/capability, not entity)
Asset (current scoped native physical-object entity)
Resource (semantic planning/execution role/capability, not entity)
Relationship modeling discipline (cross-cutting semantic rule; not entity/root)
Responsibility (specific semantic relation family; not universal entity/root)
Participation (specific semantic relation family; not entity/root)
```

`Account` has an accepted conceptual boundary as platform/access identity but its detailed domain/security model is intentionally deferred; it is therefore not listed as a fully modeled canonical kernel concept yet.

`Asset` is canonical as the **current scoped baseline**. The mandatory terminology-neutral Cluster-4 review has been completed: a universal `ManagedObject` root was rejected under current evidence, the individually tracked physical-object identity need survived, and the exact internal noun `Asset` remains non-semantic/reopenable.

`Relationship` does **not** denote a universal domain entity. The accepted baseline is a modeling discipline: use the most specific truthful relation semantics; keep simple connections direct when semantically complete; introduce a domain-specific qualified relation only when the connection itself has materially relevant state/history/lifecycle/context. See `checkpoints/relationship-v0-validation.md`.

`Responsibility` is canonical as the specific relation answering who is accountable for ensuring a bounded commitment is appropriately handled. It is not requester, expected performer, actual performer, Resource, Authority, Visibility, ownership or coordination Stewardship. See `concepts/responsibility.md` and `checkpoints/responsibility-v0-validation.md`.

`Participation` is canonical as the specific relation family for expected/intended or Actual involvement in a bounded shared occurrence/interaction. Participant is a contextual role over native identity; response/intention and Actual Participation remain distinct. See `concepts/participation.md` and `checkpoints/participation-v0-validation.md`.

## DERIVED

Useful value/state/projection computed from canonical facts rather than a universal primitive.

Examples:

```text
free capacity
overrun
lateness
adherence
streak
query aggregates
needs confirmation
some progress percentages
```

## PRODUCT PROFILE

Recognizable product shape built from canonical concepts without currently requiring a separate kernel primitive.

Examples:

```text
Project
Program
Workout
Study plan
Release plan
saved longitudinal tracker/view
Vehicle profile
Camera profile
Equipment profile
```

A product profile may specialize an Asset experience without creating a new kernel identity concept by default.

## PRODUCT / UI TERM

User/designer vocabulary that maps to canonical or deferred semantics but does not itself define a kernel concept.

Examples:

```text
Task
Repeat
Deadline
Calendar Block
Busy
This time
Inbox
Registra un dato
Register / Registro
Tracker
History / Storico
Progress
User
Gear
Device
Equipment
Inventory
Required equipment
Who's available?
Assigned to
Claim
Hand off
Going / Maybe / Can't go
Attended
```

`User` is deliberately product/implementation language. It must not be used as a universal domain synonym for Person, Actor, Account or Principal.

Terms such as `Gear`, `Equipment`, `Device`, `Things`, or `Inventory` may expose some Asset-backed experiences without redefining Asset semantics.

The word `Resource` itself should usually remain hidden when a more natural label such as Person, Room, Camera, Equipment, Service, or `Who's available?` is clearer.

The word `Relationship` is not a required user-facing noun. UI should normally expose the specific meaning (`Done by`, `Depends on`, `Parent`, `Participant`, `Owner`, `Based on…`) rather than a generic relationship object.

`Assigned to`, `Claim`, and `Hand off` are valid product/action language, but each material action must map to a specific semantic role. The same word must not become a universal kernel object.

`Going`, `Maybe`, `Can't go`, `Attended`, and similar labels may expose Participation response or Actual Participation. UI convenience must not collapse those two semantics.

## PROVISIONAL

Recurring semantic need with meaningful evidence but an unfinished domain boundary.

```text
Stewardship
Authority
Visibility
Acknowledgement
Acceptance / Agreement
Resource Requirement
Allocation / selection
```

## DEFERRED

Demonstrated semantic area intentionally postponed to a later review.

```text
Principal
Trigger
Verification
Decision
Version
Place / Location / Property semantics
living-entity identity beyond Person
Document / Artifact identity model
FinancialAccount specialist model
inventory / supply / consumption semantics
```

Detailed Account/credential/provider/security mechanics are deferred even though the Account != Person != Actor conceptual boundary is already fixed.

A generic Personal Knowledge link layer remains separately deferred. Its future flexibility must not automatically acquire operational, evidentiary, authority, allocation, participation or Actual semantics.

Coordination Stewardship is a demonstrated semantic dimension distinct from Responsibility, but standalone primitive status remains SAFE DEFERRED pending concrete workflows that require explicit independent assignment/transfer/query/history.

## HISTORICAL / SUPERSEDED

Earlier terminology preserved in Git/docs but not authoritative for the current kernel.

- `Register` as a universal kernel container and `RegisterEntry` as a universal semantic record are rejected historical candidates. See `checkpoints/register-v0-validation.md`.
- `Subject` as a universal entity/root/wrapper is rejected. The accepted meaning is a contextual semantic role over native referent identity. See `concepts/subject.md` and `checkpoints/subject-v0-validation.md`.
- universal `Actor` entity/root/wrapper is rejected. Actor is accepted as contextual agency semantics over native referent/system identity. Specific action roles remain preferred over a generic `actor` relation. See `concepts/actor.md`.
- universal `Resource` entity/root/wrapper is rejected. Resource is accepted as contextual planning/execution eligibility/capability over independently justified referent/value/pool/supply/service semantics. See `concepts/resource.md` and `checkpoints/resource-v0-validation.md`.
- universal `User` domain root and `Person = Account` / `Actor = Account` identity models are rejected. See `checkpoints/person-actor-account-v0-validation.md`.
- historical `Asset/Soggetto` language that grouped person, animal, plant, account, document, house and equipment under one generic managed-object umbrella is superseded. Current Asset v0 is narrower; a terminology-neutral cross-domain review rejected a universal `ManagedObject` root under current evidence. See `concepts/asset.md`, `checkpoints/asset-v0-validation.md`, and `checkpoints/data-subjects-v0.md`.
- universal `Relationship` entity/root/supertype and semantic-free `related_to` as kernel truth are rejected. The accepted result is specific relation semantics plus qualification only where the relationship itself materially requires it. See `checkpoints/relationship-v0-validation.md`.
- Assignment, Claim and Hand-off as standalone universal kernel primitives are rejected by Responsibility v0. They remain role-specific establishment/acquisition/transfer operations/workflows. See `checkpoints/responsibility-v0-validation.md`.
- universal Participant/Participation/member/social-graph roots are rejected. Participant is a contextual role and Participation is a specific relation family. Invitation and Attendance are not standalone universal primitives. See `concepts/participation.md` and `checkpoints/participation-v0-validation.md`.

---

# 3. UI exposure classes

- **DIRECT** — natural primary user-facing noun;
- **CONTEXTUAL** — visible under context-specific wording;
- **CONFIGURATION** — primarily rules/settings/actions;
- **ADVANCED** — detail/history/power-user surfaces;
- **HIDDEN** — mostly internal semantics; UI exposes consequences/actions instead.

Kernel sophistication must not force ontology vocabulary into simple UI.

---

# 4. Canonical Intention & Execution concepts

## Goal

**Status:** CANONICAL  
**Source:** `concepts/goal.md`  
**Question:** What outcome/condition/change/pattern is intentionally desired?  
**UI exposure:** DIRECT

```text
Goal != Plan
Goal != Activity
Goal != Milestone
Goal != Evidence
Goal identity != governor/stakeholder/contributor/subject/account
```

Possible UI: Goal, Objective, contextual Target.

## Plan

**Status:** CANONICAL  
**Source:** `concepts/plan.md`  
**Question:** How is a purpose intended to be pursued/organized?  
**UI exposure:** DIRECT / CONTEXTUAL

```text
Plan != Goal
Plan != Activity
Plan != Routine
Plan != Schedule
Plan != Actual
```

Product profiles may include Project, Program, Study plan, Training plan, Release plan, Trip plan and Rehabilitation plan.

## Activity

**Status:** CANONICAL  
**Source:** `concepts/activity.md`  
**Question:** What actionable work/behavior is intended to be performed?  
**UI exposure:** DIRECT / CONTEXTUAL

```text
Activity != Event
Activity != Plan
Activity != Session
Activity != Actual
Activity identity != requester/creator/responsible actor/expected performer/actual performer
```

Responsibility v0 closes the responsibility-family semantics: ordinary responsibility transfer/reassignment preserves Activity identity; Assignment/Claim/Hand-off are role-specific operations/workflows rather than Activity state or standalone universal primitives.

Possible UI: Task, Action, Workout, Study item, Maintenance action, Checklist item.

## Event

**Status:** CANONICAL  
**Source:** `concepts/event.md`  
**Question:** What occurrence-centred thing is expected to happen?  
**UI exposure:** DIRECT

```text
Event != Activity
Event != Schedule
Event != Participation response
Event != Actual Participation / attendance
Event != Milestone
Event identity != participant set/state
```

Participation v0 closes the participant/attendance boundary: invitation/response and Actual Participation are actor-scoped relation semantics around one Event identity.

Possible UI: Meeting, Appointment, Lesson, Exam, Concert, Flight, Shift, Interview, Race.

## Routine

**Status:** CANONICAL  
**Source:** `concepts/routine.md`  
**Question:** What behavioral/execution policy is intentionally expected to repeat?  
**UI exposure:** DIRECT

```text
Routine != Recurrence
Routine != Event series
Routine != Plan
Routine != observed habit
Routine identity != performer
```

## Milestone

**Status:** CANONICAL  
**Source:** `concepts/milestone.md`  
**Question:** What meaningful contextual checkpoint matters inside Goal/Plan?  
**UI exposure:** DIRECT / ADVANCED

```text
Milestone != Goal
Milestone != GoalCriterion
Milestone != Activity
Milestone != Event
Milestone != Outcome
Milestone != Actual
Milestone != Deadline
Milestone != Phase
```

Core hardening: Milestone attainment is Evidence/evaluation-backed checkpoint state; it is not an independent duplicate source of Actual, Outcome, Observation or other underlying reality.

---

# 5. Canonical Time concepts

## Occurrence

**Status:** CANONICAL  
**Source:** `concepts/occurrence.md`  
**Question:** Which expected instance from a recurring/generative source is this?  
**UI exposure:** HIDDEN / ADVANCED

```text
Occurrence != Recurrence
Occurrence != source Routine/Event
Occurrence != Schedule
Occurrence != Session
Occurrence != Actual
```

Typical UI: This time, This workout, This meeting, Only this one, This and future occurrences.

## Schedule

**Status:** CANONICAL  
**Source:** `concepts/schedule.md`  
**Question:** When is this schedulable subject currently accepted/intended/expected to happen?  
**UI exposure:** HIDDEN / CONFIGURATION

```text
Schedule != Temporal Constraint
Schedule != deadline/target
Schedule != Recurrence
Schedule != Availability
Schedule != Capacity claim
Schedule != Session/Actual
Schedule acceptance != Participation response/acceptance
```

## Session

**Status:** CANONICAL  
**Source:** `concepts/session.md`  
**Question:** Which logically continuous bounded episode of actual execution occurred?  
**UI exposure:** CONTEXTUAL / ADVANCED

```text
Session != Schedule
Session != Activity
Session != Occurrence
Session != Participation / Event attendance
Session != broader Actual/Outcome
```

Session identity follows logical execution continuity, not performer or participant count. Attendance does not manufacture one Session per participant.

## Temporal Constraint

**Status:** CANONICAL  
**Source:** `concepts/temporal-constraint.md`  
**Question:** Where/when is placement/duration/temporal relation allowed, required, bounded or preferred?  
**UI exposure:** CONFIGURATION

Possible UI: Deadline, Not before, Not after, Preferred time, Allowed window, Minimum/maximum duration.

`Deadline` is latest-bound Temporal Constraint semantics, not a separate kernel primitive.

## Recurrence

**Status:** CANONICAL  
**Source:** `concepts/recurrence.md`  
**Question:** How does a temporal/generative pattern repeat?  
**UI exposure:** CONFIGURATION

```text
Recurrence != Routine
Recurrence != Occurrence
Recurrence != Schedule
Recurrence != Trigger
Recurrence != responsibility rotation
```

## Availability

**Status:** CANONICAL semantic capability  
**Source:** `concepts/availability-capacity.md`  
**Question:** When may a schedulable Resource's capacity be used?  
**UI exposure:** DIRECT / CONFIGURATION / DERIVED

Availability is Resource-oriented. Subject-specific timing rules remain Temporal Constraints.

## Capacity

**Status:** CANONICAL semantic capability  
**Source:** `concepts/availability-capacity.md`  
**Question:** How much / what kind of compatible commitment can a schedulable Resource sustain?  
**UI exposure:** HIDDEN / DERIVED / ADVANCED

```text
scheduled != capacity consumed
overlap != universal conflict
Capacity != universal busy/free boolean
Capacity != universal scalar percentage
```

Resource v0 clarifies that a schedulable Resource is a provider playing Resource role where time-dependent capacity matters; Resource does not manufacture provider identity.

---

# 6. Canonical Reality & Evidence concepts

## Actual

**Status:** CANONICAL  
**Source:** `concepts/actual.md`  
**Validation:** `checkpoints/actual-v0-validation.md` — PASS WITH HARDENING  
**Question:** How did this specific intention or expectation resolve in reality?  
**UI exposure:** HIDDEN / ADVANCED / CONTEXTUAL

```text
Actual != Schedule
Actual != Session
Actual != Outcome
Actual != Observation
Actual != Evidence
Actual != Confirmation
Actual != Provenance
shared Actual != identical actor-specific Actual Participation
reported/asserted reality != established Actual
```

Core guardrails: contextual rather than universal; absence does not imply failure; passage of time does not establish Actual; conflicting assertions may remain unresolved; shared Actual does not imply identical actor participation.

## Outcome

**Status:** CANONICAL  
**Source:** `concepts/outcome.md`  
**Validation:** `checkpoints/outcome-v0-validation.md` — PASS WITH HARDENING  
**Question:** What result or disposition followed from this realization in the relevant context?  
**UI exposure:** CONTEXTUAL / HIDDEN / ADVANCED

```text
Outcome != Actual
Outcome != lifecycle/operational state
Outcome != Observation
Outcome != artifact/output
Outcome != Milestone
Outcome != Confirmation
Outcome != Provenance
Outcome != Evidence
```

Core guardrails: optional/contextual; no universal Outcome enum; absence does not imply failure; `unconfirmed` is epistemic rather than result semantics.

## Observation

**Status:** CANONICAL  
**Source:** `concepts/observation.md`  
**Validation:** `checkpoints/observation-v0-validation.md` — PASS WITH HARDENING  
**Question:** What was observed, measured, reported, or calculated about this Subject referent, and to what time/context does it apply?  
**UI exposure:** CONTEXTUAL / HIDDEN / ADVANCED

A persistent contextual record of a measured, perceived, reported, or explicitly derived property, state, value, rating, or simple assertion about a Subject referent.

```text
Observation != Actual
Observation != Outcome
Observation != Quantity
Observation != universal RegisterEntry
Observation != Evidence
Observation != Confirmation
Observation != Provenance
```

Core guardrails:

- not a universal fact/blob primitive;
- may exist without prior intention/Actual/Goal/saved tracker;
- effective time/context != recorded/ingested time;
- missing Observation != observed negative != failed measurement;
- subjective/conflicting Observations can coexist;
- query aggregates do not automatically become persisted Observations;
- high-frequency streams do not imply row-per-sample persistence;
- one Observation can appear in zero or many tracker/history/report views without duplication;
- Subject is a role over native identity, not a wrapper entity;
- Person, Actor, Account, Asset and Resource roles remain distinct when relevant.

```text
Quantity      = reusable scalar amount value semantics
Observation   = contextual observed/asserted record
Subject       = native referent's contextual aboutness role
Person        = native human identity
Actor         = contextual agency semantics; specific role preferred
Account       = platform/access identity boundary
Asset         = current scoped physical-object identity
Resource      = contextual planning/execution eligibility role
Tracker/view  = product/query presentation over native records
```

## Confirmation

**Status:** CANONICAL  
**Source:** `concepts/confirmation.md`  
**Validation:** `checkpoints/confirmation-v0-validation.md` — PASS WITH HARDENING  
**Question:** Who or what explicitly affirms this specific version of this target, for which purpose and context?  
**UI exposure:** CONTEXTUAL / HIDDEN / ADVANCED

```text
Confirmation != Actual
Confirmation != Outcome
Confirmation != Observation
Confirmation != Provenance
Confirmation != Evidence
Confirmation != Acknowledgement
Confirmation != Acceptance/Agreement
Confirmation != Verification
Confirmation != Authority
```

Core guardrails:

- contextual and optional;
- no Confirmation != false/rejected/incorrect/not performed;
- target version/context/purpose matters;
- material correction does not inherit prior Confirmation silently;
- `awaiting confirmation` is derived workflow state;
- automation/AI must not fabricate human Confirmation;
- Confirmation by one actor does not imply Confirmation by another.

Typical UI: Confirm, Looks correct, Yes this happened, Review and confirm, Needs confirmation.

