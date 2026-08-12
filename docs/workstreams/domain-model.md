# Workstream — Core Domain Model v0

- Status: **IN PROGRESS — Relationships / Reasoning active after Clusters 1–4 validation**
- Active branch: `feature/domain-model`
- Current upstream baseline: `main` integrated through `c5120ff463e027c42f4a26fc613d0917596ca738`
- Main-to-domain merge commit: `08595f9526e08db53d9b446b8a7a76cd46adcd55`
- PR: none yet
- Work type: domain modeling / invariants / persistence preparation
- Backend implementation: not started in this branch
- Current next review: **Responsibility / Assignment / Claim / Hand-off / Stewardship family**

## Purpose

Turn LifeOS product requirements into an implementation-ready domain model without prematurely fixing specialist modules, collaboration infrastructure, API shapes or final SQL tables.

Earlier product terminology is evidence, not automatic truth. Candidates are revalidated through real-world workflows, mature-product/standard benchmarks, adversarial reduction, history/correction tests, explicit multi-actor stress and cross-concept consistency.

**Accepted means current best decision, not immutable decision.**

A roadmap concept is a candidate to validate, not an object that must survive. Rejection is correct when the capability can be preserved more cleanly without an additional kernel primitive.

---

# Required reading — current handoff

Read these first, in order:

1. [`../domain/README.md`](../domain/README.md)
2. [`../domain/language-map.md`](../domain/language-map.md)
3. [`../domain/validation-methodology-v3.md`](../domain/validation-methodology-v3.md)
4. [`../domain/validation-execution-template-v3.md`](../domain/validation-execution-template-v3.md)
5. [`../domain/multi-actor-readiness-v1.md`](../domain/multi-actor-readiness-v1.md)
6. [`../domain/checkpoints/intention-execution-v0.md`](../domain/checkpoints/intention-execution-v0.md)
7. [`../domain/checkpoints/time-v0.md`](../domain/checkpoints/time-v0.md)
8. [`../domain/checkpoints/observed-reality-evidence-v0.md`](../domain/checkpoints/observed-reality-evidence-v0.md)
9. [`../domain/checkpoints/data-subjects-v0.md`](../domain/checkpoints/data-subjects-v0.md)
10. [`../domain/checkpoints/deferred-dependency-closure-clusters-1-4-v0.md`](../domain/checkpoints/deferred-dependency-closure-clusters-1-4-v0.md)
11. [`../domain/checkpoints/cross-cluster-validation-v4.md`](../domain/checkpoints/cross-cluster-validation-v4.md)
12. [`../domain/checkpoints/relationship-v0-validation.md`](../domain/checkpoints/relationship-v0-validation.md)
13. [`../domain/checkpoints/multi-actor-evidence-synthesis-v0.md`](../domain/checkpoints/multi-actor-evidence-synthesis-v0.md)

Then inspect the concept specs relevant to the immediate question. Do not rely on old product glossaries as current ontology authority.

Validation Methodology v2 and its addendum are historical audit sources only. v3 is mandatory.

---

# Operating rules

- Work one candidate/boundary at a time, then run the required integration gates.
- Use Methodology v3 for every concept and cluster checkpoint.
- From **Relationships / Reasoning onward, the Adjacent Dependency Sweep is mandatory before every concept verdict**.
- Treat mature apps, specialist systems, standards and APIs as evidence, never automatic design authority.
- Benchmark behavior, identity, lifecycle, relationships, product friction and failure modes — not merely vocabulary.
- A competitor calling something `User`, `Actor`, `Asset`, `Resource`, `Item`, `Relationship`, etc. is not an ontology decision for LifeOS.
- Allowed concept/cluster verdicts remain `PASS`, `PASS WITH HARDENING`, `REOPEN`, `DEFERRED DEPENDENCY`.
- Dependency closure classes remain `RESOLVED`, `SAFE DEFERRED`, `REOPEN`.
- `SAFE DEFERRED` requires: why current acceptance is safe, future owner/stage, exact reopening trigger, tests to rerun.
- No `TBD`, unnamed `future`, or generic `review later` for material dependencies.
- Candidate rejection is valid when no distinct identity/lifecycle/authority/invariant/query behavior justifies a primitive.
- Preserve useful product capability even when a historical kernel candidate is rejected.
- Preserve planned/current/actual/history distinctions.
- Preserve source/provenance/confirmation/evidence/authority distinctions.
- Preserve native identity versus contextual-role distinctions.
- Do not build the domain around `users.id`.
- Do not create universal Subject, Actor, Resource, User, ManagedObject, RegisterEntry, Relationship, or semantic-free graph roots for implementation convenience.
- Prefer the most specific truthful relation semantics over generic edges.
- A semantically complete simple connection may remain direct; a materially rich connection may become a **specific qualified relation family**.
- Qualified/structured relation != independent domain entity automatically.
- Queryability, many-to-many cardinality, graph traversal and database row IDs do not create domain identity.
- Relation orientation, symmetry, inverse and transitivity/propagation rules belong to the specific relation family, never to `Relationship` generally.
- Do not fabricate historical intention, allocation, identity, authority, relationship state, or earlier knowledge from later correction/relevance.
- Do not create one table/entity per life topic.
- Do not collapse the domain into arbitrary JSON.
- Do not let AI inference become established identity, Actual, Confirmation, relationship, allocation, Authority, or disclosure permission automatically.
- Preserve progressive disclosure; kernel terminology need not appear in ordinary UI.
- Re-run earlier clusters when Relationships / Reasoning materially pressures accepted boundaries.
- Do not begin final SQL/API design until Relationships / Reasoning plus whole-domain gates have passed.

---

# Current validated baseline

```text
Intention & Execution v0        PASS
Time v0                         PASS
Observed Reality & Evidence v0  PASS
Data / Subjects v0              PASS WITH HARDENING
Deferred Dependency Closure     PASS
Cross-Cluster Validation v4     PASS WITH HARDENING
Relationship v0 review          PASS WITH HARDENING
Multi-Actor Evidence Synthesis  PASS WITH HARDENING
Validation Methodology v3       ACTIVE MANDATORY STANDARD

structural reopenings           0
unclassified material debt      0
```

Current accepted concept/capability set includes:

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
Availability & Capacity
Actual
Outcome
Observation
Confirmation
Evidence
Provenance
Quantity
Subject        — semantic aboutness role
Person         — native human entity
Actor          — semantic agency category/capability
Asset          — current scoped native physical-object entity
Resource       — semantic planning/execution role/capability
Relationship modeling discipline — cross-cutting semantic rule, not entity/root
```

Accepted conceptual boundary, detailed model deferred:

```text
Account != Person != Actor
Principal remains separate and deferred
```

Rejected kernel candidates / roots:

```text
Register
universal RegisterEntry
universal Subject entity/root
universal Actor entity/root
universal Resource entity/root
universal User root
universal ManagedObject root
universal Relationship entity/root/supertype
semantic-free related_to as kernel truth
```

---

# Cluster-4 closure — important final hardenings

## Actor

Actor remains useful as the semantic category of meaningful agency, but:

```text
recorded_by
performed_by
observed_by
confirmed_by
proposed_by
transformed_by
```

are stronger than one generic `actor` edge when the specific role is known.

Therefore:

```text
Actor semantic category ✅
universal Actor entity ❌
generic actor relation replacing precise roles ❌
```

## Resource

Resource is contextual planning/execution eligibility/capability and **does not manufacture provider identity**.

A provider may independently have:

```text
Person identity
Asset identity
future Place/service identity
pool semantics
Quantity / stock / supply semantics
```

Resource role preserves those semantics rather than replacing them.

Example:

```text
Requirement: 500 ml oil
```

may use supply/Quantity semantics and Resource role without giving that 500 ml a synthetic domain identity.

Planning stages remain distinct:

```text
Requirement
→ candidate(s)
→ Allocation
→ Reservation / Capacity Claim
→ Actual use / consumption
```

## Asset

The mandatory terminology-neutral review is **complete**.

It asked how mature systems model things users manage/monitor/use/possess/share/book/consume without beginning from the word `Asset`.

Current result:

```text
universal ManagedObject root  REJECTED
physical-object identity      RETAINED
exact noun `Asset`            NON-SEMANTIC / reopenable
```

Asset v0 remains the current scoped native identity for individually tracked non-human physical objects whose specific identity/history materially matter.

Future Place/Property, living entities, Documents, FinancialAccounts, services/subscriptions remain independent SAFE DEFERRED questions, not pre-approved primitives.

## Register

Longitudinal product capability remains:

```text
native records
→ query/filter/group
→ valid aggregate/trend/comparison
→ Tracker / History / Progress / Register UI
```

No universal RegisterEntry copy/source-truth layer.

---

# Relationship modeling discipline — current Cluster-5 baseline

Normative checkpoint:

- [`Relationship v0 validation`](../domain/checkpoints/relationship-v0-validation.md) — **PASS WITH HARDENING**.

Current decision:

```text
UNIVERSAL Relationship ENTITY / ROOT / SUPERTYPE
REJECTED

semantic-free related_to as kernel truth
REJECTED

specific relation meaning + complete simple semantics
→ direct typed/specific relation

specific relation meaning + materially rich connection
→ candidate specific qualified relation family
```

Key hardenings:

- no forced direction: orientation semantics are relation-specific; symmetric relations remain possible;
- qualified/structured relation does not automatically have independent domain identity;
- query/cardinality/database pressure does not create identity;
- binary source/target representation is not mandatory when it loses naturally n-ary context;
- transitivity, symmetry, inverse semantics and propagation/reasoning are family-specific;
- Subject, Evidence, Confirmation, Provenance, Actor roles, Resource stages and future Responsibility/Participation/Authority semantics must not be flattened into one `type + metadata` graph;
- generic Personal Knowledge links remain separately SAFE DEFERRED and may not silently become operational/evidentiary/authority semantics;
- AI-inferred relationships remain proposals/inferences unless the specific family/context establishes them through valid authority/decision semantics.

This discipline must be re-tested by every material relation-family review.

---

# Canonical identity / role separation

```text
Person
= native human identity

Asset
= current scoped native physical-object identity

Subject
= contextual aboutness role

Actor
= contextual agency category/capability

Resource
= contextual planning/execution eligibility/capability

Account
= platform/access identity boundary

Principal
= deferred security/authorization identity
```

Key non-collapse rules:

```text
Person != Account
Person != Actor
Person != Subject
Person != Resource
Person != Asset

Asset != Subject
Asset != Resource
Asset != owner/holder/steward

Subject != Actor
Subject != Resource

Actor != Resource
Actor != Authority
Actor != Responsibility
Actor != Account/Principal

Resource != Requirement
Resource != Allocation
Resource != Reservation
Resource != actual use
Resource != Responsibility/Performer

Account authentication != semantic Actor
visibility != authority
ownership != visibility

specific relationship != universal Relationship wrapper
relation existence/type != Authority/Visibility/consent by default
```

---

# Current cross-cluster invariants

Retain at least these during Cluster 5:

```text
reported/asserted reality != established Actual
passage of time != completion/Actual
planned != actual
Schedule != Session
Schedule != Capacity Reservation
Milestone attainment != duplicate Actual/Outcome/Observation truth
Observation != Quantity
Observation != RegisterEntry
Evidence != source information
Provenance != truth / Authority / Version / Audit
Confirmation != Authority / Acknowledgement / Acceptance / Verification
Subject != generic related_to
Actor != generic action edge
Resource != provider identity
Account != Person
universal Relationship root = rejected
semantic-free related_to = rejected
qualified relation != entity automatically
queryability/cardinality != domain identity
```

---

# Deferred Dependency Closure — authoritative registry

Normative checkpoint:

- [`Deferred Dependency Closure — Clusters 1–4 v0`](../domain/checkpoints/deferred-dependency-closure-clusters-1-4-v0.md)

Current Relationship-specific closures/triggers:

- [`Relationship v0 validation`](../domain/checkpoints/relationship-v0-validation.md)

Result entering the current review:

```text
REOPEN                         0
unclassified material items    0
```

Do **not** recreate a parallel unnamed watchlist. Use the checkpoints as sources of exact owners, triggers and rerun tests.

High-value SAFE DEFERRED groups entering/remaining in Relationships / Reasoning include:

- Milestone / GoalCriterion / Evidence / Decision;
- Confirmation / Authority / Acknowledgement / Acceptance / Verification;
- Provenance / Version / Decision / Audit / retention;
- Actual establishment / Authority / reconciliation;
- Session/Actual / Participation / actor-scoped consequences;
- Activity / Responsibility / Assignment / Hand-off / Stewardship / Performer;
- Recurrence / Trigger;
- Account / Principal / credentials / delegation;
- Person/Asset reconciliation;
- Subject / focus / Visibility / heterogeneous references;
- Asset / Place / living entities / Document / FinancialAccount / service / type-profile;
- Resource Requirement / eligibility / Allocation / Reservation / actual use / pools / supply / skill;
- Quantity / Money / Scale / Ratio / UnitDefinition / Duration / Range;
- longitudinal materialization / aggregate visibility;
- generic Personal Knowledge links;
- AI context/inference/disclosure/Authority;
- retention/deletion/anonymization.

Nothing here is pre-approved as a new primitive.

---

# ACTIVE STAGE — Relationships / Reasoning

The stage is now **in progress**, not merely next.

Completed review:

```text
Relationship v0
PASS WITH HARDENING

universal Relationship root  REJECTED
specific direct/qualified semantic discipline  ACCEPTED
```

**Do not treat the remaining candidate space as a checklist.** It currently includes:

```text
Dependency
Responsibility / Assignment / Claim / Hand-off
Stewardship / coordination burden
Contribution
Participation
GoalCriterion / Goal relationships
Evidence ↔ Criterion / evaluation relationship
Resource Requirement / Allocation / substitution
Authority
Visibility
Acknowledgement
Acceptance / Agreement
Verification
Decision
Version
AI Proposal
Principal / delegation / on-behalf-of
focus/context relations
```

## NEXT REVIEW — Responsibility family

The next high-leverage review area is:

```text
Responsibility
Assignment
Claim
Hand-off
Stewardship / coordination burden
```

These terms are **not pre-accepted as five separate concepts**. The review must determine whether they are:

- distinct concepts;
- states/roles/actions within one smaller relation family;
- product/UI vocabulary;
- redundant candidates;
- safe deferrals.

Mandatory representative chronology includes at least:

```text
open/unassigned work
→ assigned
→ claimable / claimed
→ accepted or refused
→ responsibility transfer requested
→ hand-off pending
→ hand-off accepted/effective
→ fallback responsibility
→ substitute
→ actual performer differs
→ completion/failure
→ later historical query
```

It must separately stress:

- requester vs responsible actor vs expected performer vs actual performer;
- assignment vs acceptance;
- responsibility vs Resource eligibility;
- responsibility vs Authority/Visibility;
- responsibility transfer vs Activity identity;
- coordination stewardship/mental load vs execution responsibility;
- Accountless/external Person;
- temporary substitution;
- refusal/silence/conflict;
- unequal-power/caregiver/manager contexts;
- AI proposal vs authoritative assignment/hand-off;
- private constraints and selective disclosure;
- current responsibility vs historical attribution.

The Relationship v0 direct-vs-qualified rule must be treated as a candidate rule under stress, not as something that future reviews are forbidden to reopen.

## Mandatory method

For **every** candidate/family:

```text
Evidence + candidate
→ Core Gate
→ Multi-Actor Gate
→ Cross-Concept Gate
→ Adjacent Dependency Sweep
→ verdict
```

No concept verdict may be saved with an unclassified material adjacent dependency.

---

# Required Cluster-5 pressure

Relationships / Reasoning must explicitly pressure:

- specific relation semantics vs one generic `related_to`;
- direct vs qualified relation threshold;
- symmetric/asymmetric/n-ary relation semantics where relevant;
- Responsibility vs performer vs Resource eligibility;
- open/claimable responsibility;
- hand-off request vs acceptance vs effective responsibility change;
- stewardship/coordination burden vs execution assignment;
- Participation response vs Actual participation;
- Authority vs Visibility;
- Confirmation vs Acknowledgement / Acceptance / Verification;
- canonical-change Authority vs asserted reality / Confirmation / Provenance;
- Account/Principal/delegation/on-behalf-of;
- shared fact vs actor-scoped overlay;
- selective disclosure and inference privacy;
- Evidence/Criterion/Decision semantics;
- Provenance vs Version/Decision/Audit;
- Milestone attainment evaluation;
- Resource Requirement/Allocation/Reservation/history;
- Subject focus/context relations;
- AI proposal/action/authority boundaries;
- historical attribution after Account/relationship changes;
- deletion/revocation/retention implications.

---

# Before broad persistence/backend implementation

Still required after Relationships / Reasoning:

```text
whole-domain semantic regression
↓
whole-domain destructive redundancy test
↓
deep historical reconstruction
↓
whole-domain multi-actor stress
↓
privacy / authority stress
↓
AI stress
↓
simple-user regression
↓
specialist-system boundary
↓
logical data model
↓
physical PostgreSQL model
↓
API contracts
↓
backend package architecture
↓
implementation / vertical slices / frontend integration
```

Do not jump directly from the current Cluster-5 work to SQL/API stabilization.

---

# Git / branch handoff

- active branch: `feature/domain-model`;
- `main` remains at the integrated repository baseline and was not changed by the Relationship review scope;
- no PR for the domain branch yet;
- backend implementation was not changed here;
- Phase-4 prototype branch was not changed here;
- repository visibility does not change write-scope rules;
- before **any future Git write**, state the exact intended file/branch scope and wait for explicit user approval.

## New-chat / continuation handoff

A continuing or fresh chat should begin by reading this workstream plus:

1. `data-subjects-v0.md`;
2. `deferred-dependency-closure-clusters-1-4-v0.md`;
3. `cross-cluster-validation-v4.md`;
4. `relationship-v0-validation.md`.

Then inspect README + Language Map + Methodology v3 and the concept specs pressured by the current review.

Do **not** redo Clusters 1–4 or Relationship v0 from scratch unless stronger evidence exposes a real contradiction. The current next task is the Responsibility / Assignment / Claim / Hand-off / Stewardship review family under Methodology v3, with the Relationship direct-vs-qualified discipline explicitly re-tested rather than assumed infallible.
