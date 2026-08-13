# LifeOS Domain Atlas

**Status:** In progress — Clusters 1–4 integrated; Relationships / Reasoning active  
**Started:** 2026-08-10  
**Current revision:** 2026-08-13 — Representation / on-behalf-of v0 PASS WITH HARDENING; post-write QA PASS  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

The Domain Atlas is the current semantic source for LifeOS before broad persistence/API/backend implementation.

Its goal is the **smallest model that survives reality** without losing identity, history, truth, multi-actor correctness, privacy, Authority, queryability, extensibility or simple-user usability.

Earlier product documents, prototypes, glossaries, simulations, standards and competitor schemas are evidence inputs, not automatic ontology truth.

> **Accepted means current best decision, not immutable decision.**

A candidate may be rejected when its useful capability is preserved more cleanly without another primitive.

---

# 1. Mandatory validation method

Every candidate/family uses **Domain Validation Methodology v3**:

```text
Evidence + candidate formation
↓
Core Semantic Validation Gate
↓
Multi-Actor Compatibility Gate
↓
Cross-Concept Consistency Gate
↓
Adjacent Dependency Sweep
↓
verdict
↓
documentation propagation analysis
↓
Git write gate
```

Allowed verdicts:

```text
PASS
PASS WITH HARDENING
REOPEN
DEFERRED DEPENDENCY
```

Dependency classifications:

```text
RESOLVED
SAFE DEFERRED
REOPEN
```

Every SAFE DEFERRED item requires:

- unresolved question;
- why current acceptance is safe;
- owner/stage;
- exact reopening trigger;
- tests/boundaries to rerun.

No material `TBD`/`review later` limbo is accepted.

Normative method references:

- [`Validation Methodology v3`](validation-methodology-v3.md)
- [`Validation Execution Template v3`](validation-execution-template-v3.md)
- [`Multi-Actor Readiness v1`](multi-actor-readiness-v1.md)
- [`Domain & Product Language Map`](language-map.md)

---

# 2. Acceptance cycle

```text
V3 verdict in chat
!= accepted branch baseline

accepted branch baseline
= full V3
+ hardenings incorporated/retested
+ documentation propagation
+ explicit Git write approval
+ post-write QA PASS
```

Every write milestone follows:

```text
branch + pre-scope SHA + exact paths
↓
explicit user approval
↓
write only approved scope
↓
QA against pre-scope SHA
↓
approval consumed
↓
fresh re-score only then
```

Historical checkpoints preserve their original state; later reviews close deferred boundaries through explicit downstream amendments.

---

# 3. External evidence rule

External standards/products/APIs are benchmark evidence, never design authority.

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

Benchmark behavior/lifecycle/history/failure/Authority/privacy/sync/automation/product cost rather than nouns.

Findings are classified:

```text
BORROW
ADAPT
ALREADY STRONGER
ANTI-PATTERN
NOT APPLICABLE
```

---

# 4. Completed integrated baselines

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

References:

- [`Intention & Execution v0`](checkpoints/intention-execution-v0.md)
- [`Time v0`](checkpoints/time-v0.md)
- [`Observed Reality & Evidence v0`](checkpoints/observed-reality-evidence-v0.md)
- [`Data / Subjects v0`](checkpoints/data-subjects-v0.md)
- [`Deferred Dependency Closure — Clusters 1–4`](checkpoints/deferred-dependency-closure-clusters-1-4-v0.md)
- [`Cross-Cluster Validation v4`](checkpoints/cross-cluster-validation-v4.md)

---

# 5. Current semantic set

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

## Data / referents / contextual roles

```text
Quantity       value semantics
Subject        aboutness role, not root
Person         native human identity
Actor          agency capability, not root
Account        platform/access identity boundary
Asset          scoped native physical-object identity
Resource       planning/execution role, not root
```

## Relationships / reasoning — QA-closed so far

```text
Relationship modeling discipline
Responsibility
Participation
Authority
Visibility
Acknowledgement
Decision
Agreement
Consent
Representation / on-behalf-of
```

Current rejected abstractions include generic Acceptance/Assent, universal Approval, Reconciliation, EffectiveChange, Contract, Consent/Permission, Principal, Agent/Representative and Delegation roots.

---

# 6. Current non-collapse baseline

```text
Goal != Plan != Activity
Activity != Event
Routine != Recurrence
Occurrence != Schedule != Session != Actual
Schedule != Temporal Constraint / Availability / Capacity

Actual != Outcome / Observation / Confirmation / Evidence / Provenance / Decision
Observation != Quantity
Evidence != source information / Decision
Provenance != Source / truth / Authority / Visibility / Version / Audit / Decision / Representation

Subject != Person / Actor / Account / Principal / Asset / Resource
Person != Actor / Account / Principal / Asset / Resource
Actor != Account / Principal / Subject / Resource / Authority / Responsibility
Account != Principal

Responsibility != performer / Resource / Participation / Authority / Decision
Participation != Responsibility / Performer / Resource / Authority / Visibility / Session / Decision
Authority != Actor / Account / Principal / Responsibility / Participation / Visibility / Agreement / Consent / Decision / Representation / truth
Visibility != Authority / technical read Permission / actual View / Acknowledgement / Consent

Acknowledgement != delivery/read/display / understanding / Confirmation / Agreement / Consent / Decision / Actual
Decision != Authority / effective state / Actual / Provenance / Evidence / Agreement / Consent / Representation
Agreement != response / Decision / Authority / Responsibility / Consent / Contract / Actual / Representation
Consent != Visibility / Authority / technical Permission / Agreement / Decision / Actual / Representation

Representation != Actor identity
Representation != Subject/beneficiary
Representation != Responsibility
Representation != Authority
Representation != Participation
Representation != Acknowledgement/Confirmation/Decision
Representation != Agreement/Consent
Representation != Provenance
Representation != Principal
actual Actor != represented party
technical impersonation != domain attribution truth
```

---

# 7. Relationship modeling discipline

Normative checkpoint:

- [`Relationship v0 validation`](checkpoints/relationship-v0-validation.md)

```text
universal Relationship root           REJECTED
semantic-free related_to              REJECTED
specific relation semantics           REQUIRED
specific qualified relation           ALLOWED WHEN JUSTIFIED
```

Use the most specific truthful relation. Keep it direct when enough; qualify it when lifecycle/history/scope/Authority/Provenance/privacy/invariants justify it.

```text
qualified relation != entity/root automatically
```

---

# 8. Responsibility v0

**PASS WITH HARDENING**.

```text
Responsibility
= accountability to ensure a bounded commitment is appropriately handled
```

Assignment, Claim and Hand-off are role-specific operations/patterns, not universal roots.

```text
hand-off request
!= Acknowledgement
!= role-specific response
!= Agreement automatically
!= Approval/Decision where required
!= effective Responsibility transfer
```

---

# 9. Participation v0

**PASS WITH HARDENING**.

```text
Participant = contextual role
Invitation = Participation proposal/request
Participation response != Actual Participation
accepted != attended
declined != proved absent
no response != declined
```

A represented response preserves participant, actual response Actor, Representation context, Principal where material and applicable Authority/basis independently.

---

# 10. Authority v0

**PASS WITH HARDENING**.

```text
Authority
= contextual governance capability determining who/what may legitimately
  make a bounded effect effective for target/scope/action/context
```

```text
Authority != Actor/Account/Principal
Authority != Responsibility/Participation
Authority != Visibility
Authority != Agreement/Consent
Authority != Decision
Authority != Representation
Authority != technical Permission
```

Delegation remains bounded Authority-establishment/entrustment semantics.

```text
Authority to X != Authority to Y
re-delegation is not implied
claim of Representation != established Authority
```

---

# 11. Visibility v0

**PASS WITH HARDENING**.

```text
Visibility
= contextual information-exposure capability
```

```text
can see != can change
can see != can re-disclose
can see != use for every purpose
may see != actually saw
visible target != visible source
Visibility != Consent
```

Representation/delegation basis may be less visible than the resulting shared effect.

---

# 12. Acknowledgement v0

**PASS WITH HARDENING — QA PASS**.

```text
Acknowledgement
= explicit actor-scoped taking-notice of a specific target/material version/change/request
```

Represented effect does not rewrite the actual acknowledging Actor as the represented party.

Generic cross-domain Acceptance remains rejected.

---

# 13. Decision v0

**PASS WITH HARDENING — QA PASS**.

```text
Decision
= contextual bounded-resolution semantics
```

Approval remains scoped Decision/review-result semantics. Reconciliation remains a process/pattern. Effective state remains owned by the affected concept.

Represented Decision preserves actual decision Actor/process, represented party and Authority/delegation basis separately.

---

# 14. Agreement / Consent v0

**PASS WITH HARDENING — QA PASS**.

```text
Agreement
= multi-party mutual assent to materially same terms/version

Consent
= actor-scoped bounded permission for action/use/exposure
  under target/scope/purpose/context
```

Representative assent/Consent does not automatically become the represented party's personal Agreement/Consent. LifeOS does not certify universal legal capacity/enforceability.

---

# 15. Representation / on-behalf-of v0

Normative references:

- [`Representation`](concepts/representation.md)
- [`validation`](checkpoints/representation-delegation-principal-v0-validation.md)

**PASS WITH HARDENING — hardenings incorporated; post-write QA PASS.**

> **Representation is the contextual action-scoped relation/capability through which an actual Actor performs a bounded semantic action while acting for a distinct represented party in a defined context.**

Canonical question:

> **Who actually acted, and for which distinct party was that action performed or asserted in this bounded context?**

```text
actual Actor != represented party
Representation != Actor identity
Representation != Subject/beneficiary
Representation != Authority
Representation != Responsibility
Representation != Provenance
Representation != Principal
technical impersonation != domain attribution truth
```

### Delegation

```text
bounded Authority-establishment / entrustment pattern
```

No universal root, blanket transfer or automatic re-delegation.

### Principal

```text
technical authenticated/authorized request identity
```

Security/logical-model boundary only; not a domain primitive.

### Action-specific scope

```text
Authority to schedule for Anna
!= Authority to consent for Anna
!= Authority to agree for Anna
!= Authority to acknowledge for Anna
!= Authority to disclose Anna's private data
!= Authority to re-delegate
```

### AI/service

AI/service actor remains attributable as itself and cannot fabricate human authorship, Ack, Confirmation, Agreement, Consent or Decision.

---

# 16. Multi-actor baseline

LifeOS remains personal-first but structurally multi-actor-ready.

> **Coordinate shared reality among independent actors while preserving private personal models, Authority, Visibility, Provenance, history and appropriate product simplicity.**

Important consequences:

```text
Person/Actor != Account/Principal
shared fact != actor-scoped state
Visibility != Authority
current access != historical attribution
non-LifeOS people are ordinary reality
proposal != Ack != response != Agreement/Consent != Decision != effect != Actual
actual Actor != represented party
AI access/agency != Authority/disclosure/human will
```

No collaboration/IAM/ACL/workflow infrastructure is pre-approved merely by these semantics.

---

# 17. Current semantic topology

```text
INTENTION / STRATEGY
Goal · Plan · Activity · Event · Routine · Milestone

TIME
Recurrence · Occurrence · Temporal Constraint · Availability · Capacity · Schedule

EXECUTION / REALITY
Session · Actual · Outcome · Observation

EPISTEMIC / LINEAGE
Confirmation · Evidence · Provenance

NATIVE / CONTEXTUAL REFERENTS
Person · Asset · Subject role · Actor role · Account boundary · Resource role

RELATION DISCIPLINE
specific direct relation or specific qualified relation

ACCOUNTABILITY
Responsibility

INVOLVEMENT
Participation

GOVERNANCE
Authority

INFORMATION EXPOSURE
Visibility

COMMON GROUND
Acknowledgement

BOUNDED RESOLUTION
Decision

MUTUAL ASSENT
Agreement

BOUNDED PERMISSION
Consent

REPRESENTED ACTION
Representation / on-behalf-of
```

This is not a parent tree, processing pipeline or SQL schema.

---

# 18. Product simplicity rule

Kernel precision must not force ontology wording into ordinary UI.

Examples:

```text
Responsibility   → Responsible / Assigned to
Participation    → Going / Maybe / Can't go / Attended
Visibility       → Private / Shared with… / free-busy only
Acknowledgement  → Got it / I've seen the change
Decision         → Choose / Approve / Reject / Resolve
Agreement        → Agree to terms
Consent          → Allow / Permit / Share for…
Representation   → Done by X for Y / On behalf of…
```

A visible label does not create a new kernel type.

---

# 19. Persistence / API guardrails

Do not begin final SQL/API design yet.

Explicitly rejected assumptions include:

```text
Person.id = Account.id
Account = Principal
one universal users.id FK
universal subjects/actors/resources/relationships roots
universal responsibilities/participants/authority/visibility roots
universal Ack/Acceptance/Approval/Decision workflow root
universal Agreement/Contract or Consent/Permission root
universal Principal/Agent/Representative/Delegation root
one actor_id / principal_id / on_behalf_of_id everywhere
shared=true as privacy model
related_to + metadata as kernel
arbitrary JSON as primary semantic model
```

The logical model follows completion of Relationships / Reasoning and whole-domain regression.

---

# 20. Representation v0 post-write QA

Validated against pre-scope:

```text
b6c53ffa40ba7c1c1408f583856617a0e000f31b
```

Result:

```text
approved unique paths changed          25 / 25
new files                                2 / 2
modified files                          23 / 23
out-of-scope paths                       0
structural REOPEN                        0
unclassified material dependencies      0
main baseline                           c5120ff463e027c42f4a26fc613d0917596ca738
branch behind main                       0
```

The write approval is consumed.

---

# 21. Cluster-5 status and next action

Relationships / Reasoning remains **IN PROGRESS**.

QA-closed reviews:

```text
Relationship
Responsibility
Participation
Authority
Visibility
Acknowledgement
Decision
Agreement / Consent
Representation / on-behalf-of
```

The next step is a **fresh re-score** of the remaining demonstrated candidate/dependency space. No candidate is preselected.

Examples of remaining pressure:

```text
Version / material equivalence
Proposal / request reusable identity
Detailed reconciliation / source-precedence policy
Dependency
Coordination Stewardship
Contribution
GoalCriterion / evaluation
Resource Requirement / Allocation / Reservation / substitution
Verification / comprehension
AI Proposal
focus/context relationships
Trigger / conditional policy
collective/group/quorum semantics
Principal/AuthN/AuthZ implementation boundary
legal/specialist representation capacity
retention/audit
Personal Knowledge generic links
```

These are candidates/dependencies, not a checklist of primitives.

---

# 22. Before broad implementation

Still mandatory:

```text
finish Relationships / Reasoning candidate reviews
↓
Cluster-5 integration
↓
Cluster-5 multi-actor stress
↓
Cluster-5 deferred-dependency closure
↓
whole-domain semantic regression
↓
destructive redundancy regression
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
backend implementation
```

---

# 23. Documentation rule

Concept specs/checkpoints hold detailed evidence/history. This README is current navigation/integration summary; `language-map.md` is terminology navigation; `docs/workstreams/domain-model.md` is the operational save-game.

Do not silently rewrite historical checkpoints for vocabulary uniformity. Close earlier deferred boundaries via downstream amendments and current docs.
