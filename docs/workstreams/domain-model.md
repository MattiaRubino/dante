# Workstream — Core Domain Model v0

- Status: **IN PROGRESS — Clusters 1–4 validated together**
- Active branch: `feature/domain-model`
- Current upstream baseline: `main` integrated through `c5120ff463e027c42f4a26fc613d0917596ca738`
- Main-to-domain merge commit: `08595f9526e08db53d9b446b8a7a76cd46adcd55`
- PR: none yet
- Work type: domain modeling / invariants / persistence preparation
- Backend implementation: not started in this branch
- Current next stage: **Relationships / Reasoning**

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
12. [`../domain/checkpoints/multi-actor-evidence-synthesis-v0.md`](../domain/checkpoints/multi-actor-evidence-synthesis-v0.md)

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
- Do not create universal Subject, Actor, Resource, User, ManagedObject, RegisterEntry, or semantic-free graph roots for implementation convenience.
- Prefer specific relationships/roles over generic edges when the semantic distinction matters.
- Do not fabricate historical intention, allocation, identity, authority, or earlier knowledge from later correction/relevance.
- Do not create one table/entity per life topic.
- Do not collapse the domain into arbitrary JSON.
- Do not let AI inference become established identity, Actual, Confirmation, allocation, Authority, or disclosure permission automatically.
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
```

---

# Deferred Dependency Closure — authoritative registry

Normative checkpoint:

- [`Deferred Dependency Closure — Clusters 1–4 v0`](../domain/checkpoints/deferred-dependency-closure-clusters-1-4-v0.md)

Result:

```text
REOPEN                         0
unclassified material items    0
```

Do **not** recreate a parallel watchlist. Use that checkpoint as the source of exact owners, triggers and rerun tests.

High-value SAFE DEFERRED groups entering Relationships / Reasoning include:

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
- AI context/inference/disclosure/Authority;
- retention/deletion/anonymization.

Nothing here is pre-approved as a new primitive.

---

# ACTIVE NEXT STAGE — Relationships / Reasoning

The next stage may begin because Cross-Cluster v4 passed with no structural reopening.

**Do not treat this list as a checklist.** Candidate space currently includes:

```text
Relationship
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

The first task in a new chat should be to determine the **review order**, based on dependency leverage and risk, rather than accepting the list.

A strong likely starting point is the relationship/role foundation around:

```text
Relationship
Responsibility / Participation
Authority / Visibility
```

but the next chat should re-check that ordering against the dependency-closure checkpoint before fixing it.

## Mandatory method from this point

For **every** candidate:

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

- typed/directional relations vs one generic `related_to`;
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

Do not jump directly from Cross-Cluster v4 to SQL/API stabilization.

---

# Git / branch handoff

- active branch: `feature/domain-model`;
- `main` remains at the integrated repository baseline and was not changed by this Cluster-4 closure scope;
- no PR for the domain branch yet;
- backend implementation was not changed here;
- Phase-4 prototype branch was not changed here;
- repository visibility does not change write-scope rules;
- before **any future Git write**, state the exact intended file/branch scope and wait for explicit user approval.

## New-chat handoff

A fresh chat should begin by reading this workstream plus the three latest checkpoints:

1. `data-subjects-v0.md`;
2. `deferred-dependency-closure-clusters-1-4-v0.md`;
3. `cross-cluster-validation-v4.md`.

Then inspect README + Language Map + Methodology v3.

The new chat should **not redo Clusters 1–4 from scratch**. It should use them as the current validated baseline, reopen only on stronger evidence, and begin Relationships / Reasoning by selecting the highest-leverage next candidate/order under the dependency register.
