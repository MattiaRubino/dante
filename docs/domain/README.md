# LifeOS Domain Atlas

**Status:** In progress — Clusters 1–4 validated together; Relationships / Reasoning active  
**Started:** 2026-08-10  
**Current revision:** 2026-08-12 — Acknowledgement v0 PASS WITH HARDENING; generic cross-domain Acceptance rejected  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

The Domain Atlas is the current semantic source for LifeOS before broad persistence/API/backend implementation.

Its job is to produce the smallest model that survives real workflows without losing identity, history, truth, multi-actor correctness, privacy, authority, queryability, extensibility or simple-user usability.

Earlier product documents, prototypes, glossaries, simulations, standards and competitor schemas are **evidence inputs, not automatic ontology truth**.

> **Accepted means current best decision, not immutable decision.**

A candidate may be rejected when its useful capability is preserved more cleanly without another primitive.

---

# 1. Mandatory validation method

Every new candidate/family uses **Domain Validation Methodology v3**:

```text
A. Evidence + candidate formation
        ↓
B. Core Semantic Validation Gate
        ↓
C. Multi-Actor Compatibility Gate
        ↓
D. Cross-Concept Consistency Gate
        ↓
E. Adjacent Dependency Sweep
        ↓
Concept verdict
```

Allowed verdicts:

```text
PASS
PASS WITH HARDENING
REOPEN
DEFERRED DEPENDENCY
```

Dependency closure classes:

```text
RESOLVED
SAFE DEFERRED
REOPEN
```

A SAFE DEFERRED item requires:

- why current acceptance is safe;
- future owner/stage;
- exact reopening trigger;
- tests to rerun.

No unnamed `TBD`/`review later` is accepted for a material dependency.

From Relationships / Reasoning onward the Adjacent Dependency Sweep is mandatory **before every concept verdict**.

Canonical method references:

- [`Validation Methodology v3`](validation-methodology-v3.md)
- [`Validation Execution Template v3`](validation-execution-template-v3.md)
- [`Multi-Actor Readiness v1`](multi-actor-readiness-v1.md)
- [`Domain & Product Language Map`](language-map.md)

---

# 2. External evidence rule

External standards/products/APIs are benchmark evidence, not design authorities.

Preferred direction:

```text
LifeOS semantics
        ↓
strong internal model
        ↓
optional adapters/mappings
        ↓
external providers/standards
```

A provider calling something `User`, `Asset`, `Resource`, `Attendee`, `Relationship`, `Role`, `Permission`, `Access`, `Accepted`, etc. does not make that term authoritative for LifeOS.

Benchmark behavior, lifecycle, correction/history, failure modes, authority, privacy, sync and product cost rather than importing nouns.

---

# 3. Completed integrated baselines

```text
Intention & Execution v0        PASS
Time v0                         PASS
Observed Reality & Evidence v0  PASS
Data / Subjects v0              PASS WITH HARDENING
Deferred Dependency Closure     PASS
Cross-Cluster Validation v4     PASS WITH HARDENING

structural reopenings           0
unclassified material debt      0
```

Current transition references:

- [`Intention & Execution v0`](checkpoints/intention-execution-v0.md)
- [`Time v0`](checkpoints/time-v0.md)
- [`Observed Reality & Evidence v0`](checkpoints/observed-reality-evidence-v0.md)
- [`Data / Subjects v0`](checkpoints/data-subjects-v0.md)
- [`Deferred Dependency Closure — Clusters 1–4`](checkpoints/deferred-dependency-closure-clusters-1-4-v0.md)
- [`Cross-Cluster Validation v4`](checkpoints/cross-cluster-validation-v4.md)

---

# 4. Current accepted semantic set

## Intention / execution

```text
Goal
Plan
Activity
Event
Routine
Milestone
```

## Time

```text
Occurrence
Schedule
Session
Temporal Constraint
Recurrence
Availability
Capacity
```

## Reality / evidence

```text
Actual
Outcome
Observation
Confirmation
Evidence
Provenance
```

## Data / native identity / contextual roles

```text
Quantity              value semantics
Subject               aboutness role, not entity/root
Person                native human entity
Actor                 agency capability, not entity/root
Account               accepted platform/access boundary; detailed model deferred
Asset                 current scoped native physical-object entity
Resource              planning/execution role, not entity/root
```

## Relationships / reasoning — accepted so far

```text
Relationship modeling discipline
Responsibility
Participation
Authority
Visibility
Acknowledgement
```

Generic cross-domain `Acceptance` is explicitly **rejected as a standalone kernel primitive**. Useful positive-response semantics remain in the owning family/workflow.

---

# 5. Core non-collapse baseline

```text
Goal != Plan != Activity
Activity != Event
Routine != Recurrence
Occurrence != Schedule != Session != Actual
Schedule != Temporal Constraint / Availability / Capacity

Actual != Outcome / Observation / Confirmation / Evidence / Provenance
Observation != Quantity
Evidence != source information
Provenance != Source / truth / Authority / Visibility / Version / Audit

Subject != Person / Actor / Account / Principal / Asset / Resource
Person != Actor / Account / Principal / Asset
Actor != Account / Principal / Resource / Responsibility / Participation / Authority / Visibility
Asset != Subject / Resource / owner / holder
Resource != Requirement / Allocation / Reservation / actual use

Responsibility != requester / expected performer / actual performer / Resource / Participation / Authority / Visibility
Participation != Responsibility / Performer / Resource / Organizer / Authority / Visibility / Session
Authority != Actor / Account / Principal / Responsibility / Participation / Visibility / ownership / Confirmation / Acknowledgement / truth
Visibility != Authority / Account / Principal / technical read permission / Participation / Responsibility / ownership / actual View / Acknowledgement / Consent

Delivery/read/display telemetry != Acknowledgement
Acknowledgement != understanding
Acknowledgement != Confirmation
Acknowledgement != Participation response
Acknowledgement != Responsibility
Acknowledgement != Authority / Decision / effective change
Acknowledgement != Actual
```

---

# 6. Relationship modeling discipline

Normative checkpoint:

- [`Relationship v0 validation`](checkpoints/relationship-v0-validation.md) — **PASS WITH HARDENING**.

Decision:

```text
universal Relationship entity/root/supertype   REJECTED
semantic-free related_to kernel truth           REJECTED
specific relation semantics                     REQUIRED
specific qualified relation                     ALLOWED WHEN JUSTIFIED
```

Rule:

> Use the most specific truthful relation semantics. Keep a connection direct when that fully represents its meaning. When the relationship itself has materially relevant state, lifecycle, history, temporal scope, actor-scoped state, Authority, Provenance, privacy/Visibility or domain invariants, use a **specific qualified relation family** rather than a universal Relationship wrapper.

Hardening:

- qualified/structured relation != independent entity automatically;
- queryability/cardinality/SQL row ID != domain identity;
- binary representation is not mandatory when it loses naturally n-ary context;
- orientation/symmetry/inverse/transitivity are family-specific;
- generic Personal Knowledge links remain a separate SAFE DEFERRED low-authority layer.

---

# 7. Responsibility v0

Normative references:

- [`Responsibility`](concepts/responsibility.md)
- [`validation`](checkpoints/responsibility-v0-validation.md)

Verdict: **PASS WITH HARDENING**.

```text
Responsibility
= accountability to ensure a bounded commitment is appropriately handled

Assignment
= role-specific establishment/change operation

Claim
= self-initiated role-acquisition operation

Hand-off
= role-specific transfer workflow
```

Assignment/Claim/Hand-off are **not** standalone universal primitives.

Key rules:

```text
Responsibility != requester
Responsibility != expected performer
Responsibility != actual performer
Responsibility != Resource
Responsibility != Participation
Responsibility != Authority
Responsibility != Visibility
Responsibility != coordination Stewardship
unknown holder != explicitly open/unassigned
hand-off request != effective transfer by default
Responsibility transfer != Activity identity change
```

Common-ground closure now adds:

```text
hand-off request
!= Acknowledgement
!= role-specific accepted response
!= effective transfer
```

Coordination Stewardship is semantically distinct but standalone primitive status remains SAFE DEFERRED.

---

# 8. Participation v0

Normative references:

- [`Participation`](concepts/participation.md)
- [`validation`](checkpoints/participation-v0-validation.md)

Verdict: **PASS WITH HARDENING**.

```text
Participation
= expected/intended or Actual involvement in a bounded shared occurrence/interaction

Participant
= contextual role over native identity

Invitation
= proposal/request for intended Participation

Participation response
= actor-scoped intended/response state

Attendance
= Event-facing Actual Participation semantics
```

Participant/Invitation/Attendance are not universal roots/primitives.

Key rules:

```text
Participation response != Actual Participation
accepted != attended
declined != proved absent
no response != declined
no attendance evidence != proved absence
Event identity != participant set/state
shared Actual != identical actor-specific Actual Participation
Participation != Session / Responsibility / Performer / Resource / Authority / Visibility
```

`accepted` is contextual Participation-response semantics, not a generic Acceptance primitive.

Provider attendance telemetry remains Evidence/Provenance until applicable reconciliation establishes current truth.

---

# 9. Authority v0

Normative references:

- [`Authority`](concepts/authority.md)
- [`validation`](checkpoints/authority-v0-validation.md)

Verdict: **PASS WITH HARDENING**.

Definition boundary:

```text
Authority
= contextual governance capability determining who/what may legitimately
  make a bounded domain effect effective for a defined target/scope/action/context
```

Authority is not a native entity/root or generic administrator role.

Key rules:

```text
Authority to do X != Authority to do Y
Actor action != Authority
Account/Principal != Authority
Responsibility/Participation != Authority
Visibility != Authority
Acknowledgement != Authority
ownership != Authority
Confirmation != Authority
Authority != truth
technical permission/authorization != domain Authority
current Authority != historical Authority at action time
claimed Authority != established Authority
revoked/expired Authority != never existed
```

Delegation is a bounded Authority-establishment/entrustment pattern, not a universal root. Re-delegation is not implied.

Approval may exercise Authority but is not Authority itself; Decision/effective-change semantics remain deferred.

AI capability does not manufacture Authority; effective AI Authority cannot silently exceed applicable scope.

---

# 10. Visibility v0

Normative references:

- [`Visibility`](concepts/visibility.md)
- [`validation`](checkpoints/visibility-v0-validation.md)

Verdict: **PASS WITH HARDENING**.

Definition boundary:

```text
Visibility
= contextual information-exposure capability determining what bounded
  representation may be made available to a recipient/access context
```

`Access` is rejected as one domain mega-concept because inspect, change, execute, use, disclose and technical access are different questions.

Key rules:

```text
can see != can change
can see != can re-disclose
can see != can use for every purpose
may see != actually saw
visible target != visible related records
visible endpoints != visible relationship
visible projection != visible source
current Visibility != historical Visibility
revoked Visibility != erased past disclosure/knowledge
not visible != nonexistent
no grant != explicit prohibition semantically
Visibility != technical read permission
Visibility != Acknowledgement
AI may process source != AI may disclose source
```

A private source may produce a safe visible projection without creating a duplicate public source object.

---

# 11. Acknowledgement v0

Normative references:

- [`Acknowledgement`](concepts/acknowledgement.md)
- [`validation`](checkpoints/acknowledgement-v0-validation.md)

Verdict: **PASS WITH HARDENING**.

Definition boundary:

```text
Acknowledgement
= contextual actor-scoped explicit taking-notice of a specific
  target/material version/change/request for a defined context
```

Acknowledgement is a specific common-ground attestation/relation capability, not a native entity/root and not a universal receipt object.

Key rules:

```text
sent/delivered/displayed/read != Acknowledgement
Acknowledgement != understanding/comprehension
Acknowledgement != Confirmation
Acknowledgement != Acceptance/Agreement/Consent
Acknowledgement != Participation response
Acknowledgement != Responsibility
Acknowledgement != Authority/Approval/Decision
Acknowledgement != effective domain change
Acknowledgement != Actual/performance
silence/no response != Acknowledgement
Acknowledgement(v1) != Acknowledgement(v2) after material change
Acknowledgement by one Actor != another/group acknowledgement
AI/provider inference != human Acknowledgement
```

Acknowledgement is optional and consequence-sensitive. Product UX may use `Got it`/`Acknowledge` where common-ground failure materially matters without exposing ontology complexity everywhere.

## Generic Acceptance disposition

The joint review explicitly rejected a universal cross-domain Acceptance/Assent primitive.

```text
invitation accepted
→ Participation response

Responsibility hand-off accepted
→ role-specific response/operation

proposal accepted / applied
→ proposal/effect-specific response/operation
```

Future Agreement, Consent, Decision or other semantics must earn independent identity/lifecycle/invariants under v3 rather than inheriting a generic `Acceptance` supertype.

---

# 12. Cross-concept closure after Acknowledgement v0

The following old deferred boundaries are now semantically closed at current baseline:

```text
Confirmation ↔ Acknowledgement
Visibility ↔ Acknowledgement
Participation ↔ Acknowledgement
Responsibility ↔ Acknowledgement
Authority ↔ Acknowledgement
Participation accepted ↔ generic Acceptance
Responsibility hand-off acceptance ↔ generic Acceptance
```

Current decomposition:

```text
who acts?                Actor
who is accountable?      Responsibility
who is involved?         Participation
who can govern?          Authority
who can see?             Visibility
who explicitly noticed?  Acknowledgement
what actually happened?  Actual
```

This does **not** mean final Agreement/Consent/Decision/Principal/Version/read-audit/security/persistence models are designed.

---

# 13. Multi-actor baseline

LifeOS remains personal-first but structurally multi-actor-ready.

Core rule:

> **Coordinate shared reality among independent actors while preserving each actor's private operating model, Authority boundaries, Visibility, Provenance, historical truth and appropriate level of digital complexity.**

Important consequences:

```text
Person/Actor != Account/Principal
shared canonical fact != actor-scoped state
Visibility != Authority
current access != historical attribution
non-LifeOS people are ordinary domain reality
proposal != Acknowledgement != family-specific response != authoritative effect != Actual
AI Authority/disclosure never exceeds applicable context
```

No collaboration chat/ACL/read-receipt infrastructure is pre-approved merely by these semantic boundaries.

---

# 14. Current semantic topology

```text
INTENTION / STRATEGY
Goal
Plan
Activity / Event / Routine / Milestone

TIME
Recurrence
Occurrence
Temporal Constraint
Availability / Capacity
Schedule

EXECUTION / REALITY
Session
Actual
Outcome
Observation

EPISTEMIC / LINEAGE
Confirmation
Evidence
Provenance

VALUE SEMANTICS
Quantity

NATIVE / CONTEXTUAL REFERENTS
Person
Asset
Subject role
Actor role
Account boundary
Resource role

RELATION DISCIPLINE
specific direct relation
or specific qualified relation when material
(no universal Relationship root)

ACCOUNTABILITY
Responsibility

INVOLVEMENT
Participation

GOVERNANCE
Authority

INFORMATION EXPOSURE
Visibility

COMMON GROUND / EXPLICIT NOTICE
Acknowledgement
```

This is not a parent tree, processing chain or SQL schema.

---

# 15. Product simplicity rule

Kernel sophistication must not force ontology vocabulary into ordinary UI.

Examples:

```text
Responsibility   → Assigned to / Responsible
Participation    → Going / Maybe / Can't go / Attended
Authority        → normally hidden behind concrete allowed actions/approvals
Visibility       → Private / Shared with… / free-busy only
Acknowledgement  → Got it / Acknowledge / I've seen the change
Subject          → usually natural referent name
Actor            → Done by / Recorded by / Suggested by
Resource         → Camera / Room / Person / Who's available?
```

Context-sensitive verbs such as `Accept`, `Apply`, `Use this`, `Agree`, `Allow`, `Approve` map to the real owning semantic family/effect. A UX label never creates a new kernel concept by itself.

---

# 16. Persistence / API guardrails

Do not begin final SQL/API design yet.

Current semantic decisions explicitly reject assumptions such as:

```text
Person.id = Account.id
Account = Principal
one universal users.id FK
one universal subjects table
one universal actors table
one universal resources table
one universal relationships table/graph
one universal participants table/root
one universal responsibilities table/root
one universal authority/permission table as ontology
one universal visibility/ACL object as ontology
one universal acknowledgement/receipt root
one universal acceptance/assent workflow root
shared=true as full privacy model
related_to + metadata as the kernel
arbitrary JSON as primary domain model
```

Logical modeling comes **after Relationships / Reasoning and whole-domain regression**.

---

# 17. Cluster-5 status and next action

Relationships / Reasoning is **IN PROGRESS**.

Completed reviews:

```text
Relationship v0       PASS WITH HARDENING
Responsibility v0     PASS WITH HARDENING
Participation v0      PASS WITH HARDENING
Authority v0          PASS WITH HARDENING
Visibility v0         PASS WITH HARDENING
Acknowledgement v0    PASS WITH HARDENING
Generic Acceptance    REJECTED as standalone primitive
```

Each accepted/current review has:

```text
REOPEN = 0
unclassified material dependencies = 0
```

**Next:** after documentation propagation and Git QA, re-score the remaining candidate/dependency space by dependency leverage. Do not select the next concept merely from historical roadmap order.

Demonstrated remaining areas include:

- Agreement;
- Consent / purpose limitation;
- Decision / reconciliation / Approval effect;
- Principal / delegation / on-behalf-of;
- Dependency;
- Coordination Stewardship standalone question;
- Contribution;
- GoalCriterion / Goal relationships;
- Evidence ↔ Criterion/evaluation;
- Resource Requirement / Allocation / Reservation / substitution;
- Verification;
- Version;
- AI Proposal;
- focus/context relationships;
- Trigger/policy;
- collective/group semantics;
- generic Personal Knowledge links.

These remain **candidates, not a checklist of primitives**.

---

# 18. Before broad implementation

Still mandatory:

```text
finish Relationships / Reasoning candidate reviews
↓
Cluster-5 integration + multi-actor gate
↓
Cluster-5 deferred-dependency closure
↓
whole-domain semantic regression
↓
destructive redundancy test
↓
deep history/correction regression
↓
whole-domain multi-actor/privacy/Authority/AI stress
↓
simple-user regression
↓
specialist-system boundary
↓
logical data model
↓
physical PostgreSQL
↓
API contracts
↓
backend packages / implementation
```

---

# 19. Documentation rule

Concept specs/checkpoints hold detailed evidence and history. This README is the current navigation and integration summary; `language-map.md` is the fast terminology map; `docs/workstreams/domain-model.md` is the operational handoff.

Do not silently rewrite historical checkpoints merely for vocabulary uniformity. New accepted concepts close old deferred boundaries through explicit downstream amendments/current handoff updates.

A `PASS WITH HARDENING` is not treated as accepted merely because it appeared in chat; hardenings, documentation propagation and Git QA are part of the acceptance cycle.
