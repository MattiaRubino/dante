# Workstream — Core Domain Model v0

- Status: **IN PROGRESS — Relationships / Reasoning active after Clusters 1–4 validation**
- Active branch: `feature/domain-model`
- Current upstream baseline: `main` integrated through `c5120ff463e027c42f4a26fc613d0917596ca738`
- Main-to-domain merge commit: `08595f9526e08db53d9b446b8a7a76cd46adcd55`
- PR: none yet
- Work type: domain modeling / invariants / persistence preparation
- Backend implementation: not started in this branch
- Current next review: **reselect by dependency leverage after Participation; strongest current pressure area is Authority / Visibility / Acceptance-Acknowledgement / delegation**

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
13. [`../domain/concepts/responsibility.md`](../domain/concepts/responsibility.md)
14. [`../domain/checkpoints/responsibility-v0-validation.md`](../domain/checkpoints/responsibility-v0-validation.md)
15. [`../domain/concepts/participation.md`](../domain/concepts/participation.md)
16. [`../domain/checkpoints/participation-v0-validation.md`](../domain/checkpoints/participation-v0-validation.md)
17. [`../domain/checkpoints/multi-actor-evidence-synthesis-v0.md`](../domain/checkpoints/multi-actor-evidence-synthesis-v0.md)

Then inspect the concept specs relevant to the immediate question. Do not rely on old product glossaries as current ontology authority.

Validation Methodology v2 and its addendum are historical audit sources only. v3 is mandatory.

---

# Operating rules

- Work one candidate/boundary at a time, then run the required integration gates.
- Use Methodology v3 for every concept and cluster checkpoint.
- From **Relationships / Reasoning onward, the Adjacent Dependency Sweep is mandatory before every concept verdict**.
- Treat mature apps, specialist systems, standards and APIs as evidence, never automatic design authority.
- Benchmark behavior, identity, lifecycle, relationships, product friction and failure modes — not merely vocabulary.
- A competitor calling something `User`, `Actor`, `Asset`, `Resource`, `Item`, `Relationship`, `Assignment`, `Participant`, etc. is not an ontology decision for LifeOS.
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
- Do not create universal Subject, Actor, Resource, User, ManagedObject, RegisterEntry, Relationship, Responsibility, Participant/Participation, or semantic-free graph roots for implementation convenience.
- Prefer the most specific truthful relation semantics over generic edges.
- A semantically complete simple connection may remain direct; a materially rich connection may become a **specific qualified relation family**.
- Qualified/structured relation != independent domain entity automatically.
- Queryability, many-to-many cardinality, graph traversal and database row IDs do not create domain identity.
- Relation orientation, symmetry, inverse and transitivity/propagation rules belong to the specific relation family, never to `Relationship` generally.
- Assignment/Claim/Hand-off are not generic objects: every material operation must identify the specific semantic role being established/acquired/transferred.
- Unknown Responsibility holder != explicitly open/unassigned/claimable Responsibility.
- Assignment != Acceptance by default; hand-off request != effective transfer by default.
- Responsibility != requester / expected performer / actual performer / Participation / Resource / Authority / Visibility / coordination Stewardship.
- Participant is contextual involvement over native identity, not a Person/Actor/Account subtype/root.
- Invitation is a Participation proposal/request, not Acceptance or Actual Participation.
- Participation response != Actual Participation; `accepted != attended`, `declined != proved absent`, `no response != declined`, `no attendance evidence != proved absence`.
- Participation != Session / Responsibility / Performer / Resource / Organizer / Authority / Visibility.
- Shared Actual != identical actor-specific Actual Participation.
- Provider attendance telemetry remains Evidence/Provenance until applicable reconciliation/Authority semantics establish current Participation truth.
- Do not fabricate historical intention, allocation, identity, authority, relationship/responsibility/participation state, or earlier knowledge from later correction/relevance.
- Do not create one table/entity per life topic.
- Do not collapse the domain into arbitrary JSON.
- Do not let AI inference become established identity, Actual, Confirmation, relationship, Responsibility, Participation, allocation, Authority, or disclosure permission automatically.
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
Responsibility v0 review        PASS WITH HARDENING
Participation v0 review         PASS WITH HARDENING
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
Responsibility — specific semantic accountability relation family, not entity/root
Participation — specific semantic involvement relation family, not entity/root
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
universal Responsibility entity/root
universal Assignment primitive
universal Claim primitive
universal Hand-off primitive
universal Participant entity/root
universal Participation/member/social-graph root
universal Invitation primitive
universal Attendance primitive
```

---

# Cluster-4 closure — important final hardenings

## Actor

Actor remains useful as the semantic category of meaningful agency, but specific roles such as:

```text
recorded_by
performed_by
observed_by
confirmed_by
proposed_by
transformed_by
responsible_for
participant / Participation
```

are stronger than one generic `actor` edge when the specific role is known.

## Resource

Resource is contextual planning/execution eligibility/capability and **does not manufacture provider identity, Responsibility or Participation**.

A provider may independently have Person identity, Asset identity, future Place/service identity, pool semantics, or Quantity/stock/supply semantics.

Planning stages remain distinct:

```text
Requirement
→ candidate(s)
→ Allocation
→ Reservation / Capacity Claim
→ Actual use / consumption
```

None of these stages automatically establishes Responsibility or Participation.

## Asset

The mandatory terminology-neutral review is complete:

```text
universal ManagedObject root  REJECTED
physical-object identity      RETAINED
exact noun `Asset`            NON-SEMANTIC / reopenable
```

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
- Subject, Evidence, Confirmation, Provenance, Actor roles, Resource stages, Responsibility, Participation and future Authority semantics must not be flattened into one `type + metadata` graph;
- generic Personal Knowledge links remain separately SAFE DEFERRED and may not silently become operational/evidentiary/authority semantics;
- AI-inferred relationships remain proposals/inferences unless the specific family/context establishes them through valid authority/decision semantics.

This discipline must be re-tested by every material relation-family review.

---

# Responsibility v0 — current Cluster-5 baseline

Normative references:

- [`Responsibility v0`](../domain/concepts/responsibility.md);
- [`Responsibility v0 validation`](../domain/checkpoints/responsibility-v0-validation.md) — **PASS WITH HARDENING**.

Canonical question:

> **Who is accountable for ensuring this bounded commitment is appropriately handled in this context?**

Current decision:

```text
RESPONSIBILITY
specific semantic relation family
simple direct or specifically qualified when justified
NOT universal entity/root

ASSIGNMENT
role-specific establishment/change operation
NOT standalone universal primitive

CLAIM
self-initiated role-acquisition operation
NOT standalone universal primitive

HAND-OFF
role-specific transfer workflow/pattern
NOT standalone universal primitive

COORDINATION STEWARDSHIP
distinct semantic dimension
standalone primitive SAFE DEFERRED
```

Key non-collapse rules:

```text
Responsibility != requester
Responsibility != expected performer
Responsibility != actual performer
Responsibility != Participation
Responsibility != Resource
Responsibility != Authority
Responsibility != Visibility
Responsibility != ownership/custody
Responsibility != coordination Stewardship
unknown holder != explicitly open/unassigned
```

Important operational rules:

- every Assignment/Claim/Hand-off must name the role it changes;
- Assignment does not universally require Acceptance and does not universally make Responsibility effective immediately;
- Claim effect is policy-dependent;
- hand-off request does not universally equal effective transfer;
- transfer of Responsibility does not silently transfer expected performer, Stewardship, Participation, Authority, Visibility or any other role;
- ordinary Responsibility change preserves the underlying Activity identity;
- eventual actual performer/participant does not rewrite historical Responsibility;
- Accountless Person may bear Responsibility;
- AI may propose but does not establish/transfer Responsibility without the required policy/Authority.

Responsibility v0 confirmed the Relationship direct-vs-specific-qualified discipline; it produced no structural reopening.

---

# Participation v0 — current Cluster-5 baseline

Normative references:

- [`Participation v0`](../domain/concepts/participation.md);
- [`Participation v0 validation`](../domain/checkpoints/participation-v0-validation.md) — **PASS WITH HARDENING**.

Canonical questions:

> **Who is expected/intended to be involved in this bounded shared occurrence/interaction?**

and, independently:

> **Who actually participated, and in what way/interval where that matters?**

Current decision:

```text
PARTICIPATION
specific semantic relation family
intended/response and Actual involvement facets remain distinct
simple direct or specifically qualified when justified
NOT entity/root
NOT universal membership/social graph

PARTICIPANT
contextual role over native identity
NOT entity/root

INVITATION
participation proposal/request semantics
NOT standalone universal primitive

PARTICIPATION RESPONSE
actor-scoped intended/response state
NOT Actual Participation

ATTENDANCE
Event-facing Actual Participation semantics
NOT standalone universal primitive
```

Key non-collapse rules:

```text
Event identity != participant set/state
Participation response != Actual Participation
accepted != attended
declined != proved absent
no response != declined
no attendance evidence != proved absence
Participation != Session
Participation != Responsibility
Participation != Performer
Participation != Resource
Participation != Organizer/requester
Participation != Authority/Visibility
shared Actual != identical actor-specific Actual Participation
```

Important operational rules:

- later Actual Participation does not rewrite earlier response history;
- declined may later attend; accepted may later be absent; uninvited participation is representable without fabricated history;
- actual participation may be partial or represented by multiple intervals without creating duplicate Event/Person identity;
- provider attendance telemetry is supporting Evidence/Provenance rather than automatic canonical human Participation;
- participant identity may differ from the Actor/Account/Principal that submits a response;
- Resource reservation/allocation does not establish Participation;
- Accountless Person may participate;
- AI may propose/infer but does not establish response, Actual Participation, Authority or disclosure permission.

Participation v0 is the second major successful stress of Relationship v0 and confirms its direct-vs-specific-qualified discipline.

Still SAFE DEFERRED around Participation:

- Authority/Visibility;
- Acceptance/Acknowledgement;
- participant role taxonomy;
- group/collective Participation;
- delegation/on-behalf-of response;
- recurring-series Participation inheritance/override;
- provider attendance reconciliation/evidence threshold;
- retention/deletion;
- exact qualified Participation identity/cardinality/persistence.

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

Responsibility
= contextual accountability relation family

Participation
= contextual involvement relation family

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
Person != Participant
Person != Asset

Asset != Subject
Asset != Resource
Asset != owner/holder/steward

Subject != Actor
Subject != Resource

Actor != Resource
Actor != Authority
Actor != Responsibility
Actor != Participation
Actor != Account/Principal

Resource != Requirement
Resource != Allocation
Resource != Reservation
Resource != actual use
Resource != Responsibility/Performer/Participation

Responsibility != requester
Responsibility != expected performer
Responsibility != actual performer
Responsibility != Participation
Responsibility != Authority/Visibility/Stewardship

Participation != Session
Participation != Performer
Participation != Resource
Participation != Organizer
Participation != Authority/Visibility

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
Responsibility != requester/expected performer/actual performer/Participation
unknown Responsibility != explicitly open/unassigned
Assignment/Claim/Hand-off must name the role they change
hand-off request != effective transfer by default
Responsibility transfer != Activity identity change
Participant != identity/root
Invitation != Acceptance/Actual Participation
Participation response != Actual Participation
accepted != attended
declined != proved absent
no response != declined
no attendance evidence != proved absence
Participation != Session/Responsibility/Performer/Resource/Authority/Visibility
shared Actual != identical actor-specific Actual Participation
```

---

# Deferred Dependency Closure — authoritative registries

Clusters 1–4 normative checkpoint:

- [`Deferred Dependency Closure — Clusters 1–4 v0`](../domain/checkpoints/deferred-dependency-closure-clusters-1-4-v0.md)

Cluster-5 current checkpoints:

- [`Relationship v0 validation`](../domain/checkpoints/relationship-v0-validation.md)
- [`Responsibility v0 validation`](../domain/checkpoints/responsibility-v0-validation.md)
- [`Participation v0 validation`](../domain/checkpoints/participation-v0-validation.md)

Current result:

```text
REOPEN                         0
unclassified material items    0
```

Do **not** recreate a parallel unnamed watchlist. Use the checkpoints as sources of exact owners, triggers and rerun tests.

The old broad Activity ↔ Responsibility/Assignment/Hand-off deferred dependency is resolved at the semantic level by Responsibility v0.

The old Event/Session/Actual ↔ Participation deferred pressure is resolved at the semantic level by Participation v0.

Remaining high-value SAFE DEFERRED groups include:

- Responsibility / Authority / Acceptance / Visibility / delegation;
- Participation / Authority / Visibility / Acceptance-Acknowledgement / delegation / reconciliation;
- standalone coordination Stewardship;
- collective/joint/fallback Responsibility;
- participant role taxonomy / group Participation / recurrence override;
- Milestone / GoalCriterion / Evidence / Decision;
- Confirmation / Authority / Acknowledgement / Acceptance / Verification;
- Provenance / Version / Decision / Audit / retention;
- Actual establishment / Authority / reconciliation;
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

The stage is in progress.

Completed reviews:

```text
Relationship v0
PASS WITH HARDENING

Responsibility v0
PASS WITH HARDENING

Participation v0
PASS WITH HARDENING
```

**Do not treat the remaining candidate space as a checklist.** It currently includes:

```text
Authority
Visibility
Acknowledgement
Acceptance / Agreement
Principal / delegation / on-behalf-of
Decision / reconciliation
Dependency
Stewardship standalone primitive question
Contribution
GoalCriterion / Goal relationships
Evidence ↔ Criterion / evaluation relationship
Resource Requirement / Allocation / substitution
Verification
Version
AI Proposal
focus/context relations
Trigger / conditional policy
collective/group semantics
```

## NEXT-CANDIDATE SELECTION

Do not continue merely because a roadmap item is next in the old list. Re-score dependency leverage after Participation v0.

Current strongest pressure area is **common-ground / governance semantics**:

```text
Authority
Visibility
Acceptance / Acknowledgement
Delegation / on-behalf-of
Decision / reconciliation
```

Why this area now has high leverage:

- Responsibility role changes depend on policy/Authority/Acceptance without absorbing them;
- Participation invitation/response and on-behalf-of cases expose the same boundary;
- Confirmation already requires separation from Acceptance/Acknowledgement/Authority;
- Actual reconciliation and conflicting assertions depend on who may establish/override current truth;
- Visibility and relation visibility are repeatedly distinct across Subject, Resource, Responsibility and Participation;
- AI must not launder information access into disclosure or action Authority;
- Account/Principal semantics remain intentionally separate.

This is an **area to score**, not a pre-accepted list of primitives. Candidate formation must determine whether Authority and Visibility should be reviewed together or separately, whether Acceptance/Acknowledgement are distinct concepts/operations/states, and which dependencies must precede the others.

## Mandatory method

For every candidate/family:

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
- Responsibility vs expected/actual performer vs Resource eligibility vs Participation;
- open/claimable responsibility;
- hand-off request vs Acceptance vs effective responsibility change;
- stewardship/coordination burden vs execution responsibility;
- Participation response vs Actual Participation;
- Invitation vs Acceptance/Acknowledgement;
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
- `main` remains at the integrated repository baseline and was not changed by the current semantic-review scopes;
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
4. `relationship-v0-validation.md`;
5. `responsibility.md`;
6. `responsibility-v0-validation.md`;
7. `participation.md`;
8. `participation-v0-validation.md`.

Then inspect README + Language Map + Methodology v3 and the concept specs pressured by the next review.

Do **not** redo Clusters 1–4, Relationship v0, Responsibility v0 or Participation v0 from scratch unless stronger evidence exposes a real contradiction. Re-select the next Relationships / Reasoning candidate by dependency leverage, with common-ground/governance semantics now the strongest pressure area rather than a pre-accepted next primitive.