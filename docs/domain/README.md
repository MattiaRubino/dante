# LifeOS Domain Atlas

**Status:** In progress — Clusters 1–4 validated together; Relationships / Reasoning active  
**Started:** 2026-08-10  
**Current revision:** 2026-08-13 — Representation / on-behalf-of v0 PASS WITH HARDENING; propagation complete, post-write QA pending  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

The Domain Atlas is the current semantic source for LifeOS before broad persistence/API/backend implementation.

Its job is to produce the smallest model that survives real workflows without losing identity, history, truth, multi-actor correctness, privacy, Authority, queryability, extensibility or simple-user usability.

Earlier product documents, prototypes, glossaries, simulations, standards and competitor schemas are **evidence inputs, not automatic ontology truth**.

> **Accepted means current best decision, not immutable decision.**

A candidate may be rejected when its useful capability is preserved more cleanly without another primitive.

---

# 1. Mandatory validation method

Every candidate/family uses **Domain Validation Methodology v3**:

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

Every SAFE DEFERRED item requires:

- unresolved question;
- why acceptance remains safe;
- explicit owner/stage;
- exact reopening trigger;
- exact tests/boundaries to rerun.

No material `TBD`/`review later` limbo is accepted.

Canonical references:

- [`Validation Methodology v3`](validation-methodology-v3.md)
- [`Validation Execution Template v3`](validation-execution-template-v3.md)
- [`Multi-Actor Readiness v1`](multi-actor-readiness-v1.md)
- [`Domain & Product Language Map`](language-map.md)

---

# 2. Acceptance cycle

A chat verdict is not enough.

```text
V3 verdict
!= accepted branch baseline

accepted branch baseline
= full V3
+ hardenings incorporated/retested
+ documentation propagation
+ explicit Git write approval
+ post-write QA PASS
```

For every write milestone:

```text
state branch + pre-scope SHA + exact file scope
↓
explicit approval
↓
write only approved scope
↓
QA complete diff against pre-scope SHA
↓
approval consumed
↓
only then fresh re-score
```

Historical checkpoints preserve their original decision and receive explicit downstream closure appendices rather than silent rewriting.

---

# 3. External evidence rule

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

Benchmark behavior, lifecycle, correction/history, failure modes, Authority, privacy, sync, automation and product cost rather than importing nouns.

Every benchmark finding is classified as:

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

## Data / native identity / contextual roles

```text
Quantity              value semantics
Subject               aboutness role, not entity/root
Person                native human identity
Actor                 agency capability, not entity/root
Account               platform/access identity boundary; detailed security model deferred
Asset                 scoped native physical-object identity
Resource              planning/execution role, not entity/root
```

## Relationships / reasoning — QA-closed baseline

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
```

## Current milestone pending QA

```text
Representation / on-behalf-of
```

Representation is semantically PASS WITH HARDENING and propagated, but it is not yet part of the QA-closed baseline until post-write diff QA passes.

---

# 6. Relationship modeling discipline

Normative checkpoint:

- [`Relationship v0 validation`](checkpoints/relationship-v0-validation.md) — **PASS WITH HARDENING**.

```text
universal Relationship entity/root/supertype   REJECTED
semantic-free related_to kernel truth           REJECTED
specific relation semantics                     REQUIRED
specific qualified relation                     ALLOWED WHEN JUSTIFIED
```

Rule:

> Use the most specific truthful relation semantics. Keep a connection direct when that fully represents its meaning. When the relation itself has materially relevant state, lifecycle, history, temporal scope, Actor-scoped state, Authority, Provenance, privacy/Visibility or invariants, use a **specific qualified relation family** rather than a universal Relationship wrapper.

```text
qualified/structured relation != independent entity automatically
queryability/cardinality/row ID != domain identity
```

---

# 7. Current non-collapse baseline

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

Responsibility != expected performer / actual performer / Resource / Participation / Authority / Decision
Participation != Responsibility / Performer / Resource / Authority / Visibility / Session / Decision
Authority != Actor / Account / Principal / Responsibility / Participation / Visibility / Agreement / Consent / Decision / truth
Visibility != Authority / technical read permission / actual View / Acknowledgement / Consent

Acknowledgement != delivery/read/display telemetry
Acknowledgement != understanding / Confirmation / Agreement / Consent / Decision / Actual

Decision != Authority / effective target state / Actual / Provenance / Evidence / Agreement / Consent / Representation

Agreement != one Actor's response / Decision / Authority / Responsibility / Consent / legal Contract / Actual / Representation

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

actual Actor != represented party by default
technical impersonation != domain attribution truth
```

---

# 8. Responsibility v0

Verdict: **PASS WITH HARDENING**.

```text
Responsibility
= accountability to ensure a bounded commitment is appropriately handled
```

Assignment/Claim/Hand-off remain role-specific operations/patterns, not universal primitives.

```text
hand-off request
!= Acknowledgement
!= role-specific response
!= Agreement automatically
!= Approval/Decision where required
!= effective Responsibility transfer
```

The resulting Responsibility state remains owned by Responsibility.

---

# 9. Participation v0

Verdict: **PASS WITH HARDENING**.

```text
Participant = contextual role over native identity
Invitation = Participation proposal/request
Participation response != Actual Participation
accepted != attended
declined != proved absent
no response != declined
```

A represented Participation response preserves:

```text
participant/native referent
actual response Actor
Representation/on-behalf-of context
Principal/security context where material
applicable Authority/basis
```

without rewriting the actual Actor as the participant.

---

# 10. Authority v0

Verdict: **PASS WITH HARDENING**.

```text
Authority
= contextual governance capability determining who/what may legitimately
  make a bounded domain effect effective for a defined target/scope/action/context
```

```text
Authority != Actor
Authority != Account/Principal
Authority != Responsibility/Participation
Authority != Visibility
Authority != Agreement/Consent
Authority != Decision
Authority != Representation
Authority != technical Permission
```

Delegation remains:

```text
bounded Authority-establishment / entrustment pattern
```

not a universal root.

```text
Authority to do X != Authority to do Y
re-delegation is not implied
claim of Representation != established Authority
```

---

# 11. Visibility v0

Verdict: **PASS WITH HARDENING**.

```text
Visibility
= contextual information-exposure capability determining what bounded
  representation may be made available to a recipient/access context
```

```text
can see != can change
can see != can re-disclose
can see != can use for every purpose
may see != actually saw
visible target != visible related records
visible projection != visible source
Visibility != Consent
```

Representation/delegation details may have tighter Visibility than the resulting shared effect.

---

# 12. Acknowledgement v0

Verdict: **PASS WITH HARDENING**.

```text
Acknowledgement
= contextual actor-scoped explicit taking-notice of a specific
  target/material version/change/request
```

A representative can perform an acknowledgement action with represented effect only under an applicable basis, but LifeOS preserves the **actual acknowledging Actor**.

```text
represented Acknowledgement effect
!= represented party personally performed the action
```

Generic cross-domain Acceptance remains rejected.

---

# 13. Decision v0

Verdict: **PASS WITH HARDENING**.

```text
Decision
= contextual bounded-resolution semantics determining what bounded question
  was resolved to what result, by whom/what, about which target/version/context
```

Approval is scoped Decision/review-result semantics. Reconciliation remains a process/pattern. Effective state remains owned by the affected domain concept.

A represented Decision preserves:

```text
actual decision Actor/process
represented party
applicable Authority/delegation basis
Principal/security context where material
```

and never fabricates represented-party Agreement, Consent, Acknowledgement or Confirmation.

---

# 14. Agreement / Consent v0

Verdict: **PASS WITH HARDENING**.

## Agreement

```text
Agreement
= contextual multi-party mutual assent to materially same terms/version
```

## Consent

```text
Consent
= contextual actor-scoped bounded permission for action/use/exposure
  concerning a defined target/scope/purpose/context
```

Representative assent/Consent does not automatically become the represented party's personal Agreement/Consent. It has represented effect only where an applicable action-specific Authority/policy/specialist basis permits that result, with truthful attribution preserved.

LifeOS does not certify universal legal capacity or enforceability.

---

# 15. Representation / on-behalf-of v0 — current milestone

Normative references:

- [`Representation`](concepts/representation.md)
- [`validation`](checkpoints/representation-delegation-principal-v0-validation.md)

Current semantic verdict: **PASS WITH HARDENING — propagation complete; post-write QA pending**.

Definition:

> **Representation is the contextual action-scoped relation/capability through which an actual Actor performs a bounded semantic action while acting for a distinct represented party in a defined context.**

Canonical question:

> **Who actually acted, and for which distinct party was that action performed or asserted in this bounded context?**

Classification:

```text
Representation / on-behalf-of
✅ contextual action-scoped relation/capability
✅ actual Actor preserved
✅ represented party distinct
✅ bounded action/context
✅ may reference applicable Authority/delegation/policy/basis
✅ history-sensitive where material

❌ native entity/root
❌ universal Agent/Representative identity
❌ Principal
❌ Authority
❌ Responsibility
❌ Subject/beneficiary
❌ Provenance
❌ human will/assent by implication
```

Representative:

```text
contextual role
not native Person subtype/root
```

Principal:

```text
technical authenticated/authorized request identity
security/logical model boundary
NOT LifeOS domain primitive
```

Delegation:

```text
bounded Authority-establishment / entrustment pattern
NOT universal primitive/root
NOT blanket transfer
NOT automatic re-delegation
```

Impersonation:

```text
possible technical/security mechanism later
NOT domain attribution truth
```

Critical rule:

```text
Authority to schedule for Anna
!= Authority to consent for Anna
!= Authority to agree for Anna
!= Authority to acknowledge for Anna
!= Authority to disclose Anna's private data
!= Authority to re-delegate
```

---

# 16. Representation chronology baseline

```text
T0 Anna delegates bounded Schedule Authority to Luca
T1 Luca authenticates under his own Account/Principal
T2 Luca changes Anna's Schedule

actual Actor      = Luca
represented party = Anna
Principal         = Luca security context
Authority basis   = bounded delegation
current Schedule  = owned by Schedule

T3 delegation revoked
T4 Luca attempts another represented action
```

The later attempted Representation may remain attributable, but the effect does not become legitimate merely because earlier Representation was valid.

Historical queries must preserve action-time Actor, represented party, basis, security context where material, effect and later revocation/correction.

---

# 17. Multi-actor baseline

LifeOS remains personal-first but structurally multi-actor-ready.

```text
shared canonical fact
!= one account's private model

Person/Actor != Account/Principal
shared fact != actor-scoped state
Visibility != Authority
Representation != Authority
Representation != represented person's will
current access != historical attribution
non-LifeOS people are ordinary domain reality
AI/source access != disclosure permission
```

Representation strengthens assisted/caregiver/manager/AI workflows without creating enterprise delegation infrastructure or universal Party/Agent roots.

---

# 18. Current semantic topology

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

This is not a parent tree, process chain or SQL schema.

---

# 19. Product simplicity rule

Kernel precision must not force ontology vocabulary into ordinary UI.

Examples:

```text
Responsibility   → Responsible / Assigned to
Participation    → Going / Maybe / Can't go / Attended
Authority        → normally hidden behind concrete allowed actions
Visibility       → Private / Shared with… / free-busy only
Acknowledgement  → Got it / I've seen the change
Decision         → Choose / Approve / Reject / Finalize
Agreement        → Agree / Agreed terms
Consent          → Allow / Share for this purpose / Stop sharing
Representation   → On behalf of… / Added by X for Y / Scheduled by assistant
Actor            → Done by / Recorded by / Suggested by / Decided by
Principal        → normally hidden security/admin detail
```

A UX label never creates a domain primitive by itself.

---

# 20. Persistence / API guardrails

Do not begin final SQL/API design yet.

Rejected assumptions include:

```text
Person.id = Account.id
Account = Principal
one universal users.id FK
one universal subjects/actors/resources/relationships table
one universal Participant/Responsibility/Authority/Visibility root
one universal Acknowledgement/Acceptance/Agreement/Consent root
one universal Decision/Approval/Reconciliation/EffectiveChange root
one universal Representative/Agent/Delegation root
one generic on_behalf_of field on every record
one universal authorization/delegation graph
technical impersonation determines semantic Actor
shared=true as full privacy model
related_to + metadata as kernel
arbitrary JSON as primary semantic model
```

Future logical modeling must preserve:

```text
actual Actor
represented party
Account/Principal security context where material
Authority/delegation basis separately
Provenance separately
resulting domain state separately
historical action-time attribution
```

without forcing a universal representation table/root before persistence pressure is evaluated.

---

# 21. Cluster-5 status

Relationships / Reasoning is **IN PROGRESS**.

QA-closed reviews:

```text
Relationship v0       PASS WITH HARDENING
Responsibility v0     PASS WITH HARDENING
Participation v0      PASS WITH HARDENING
Authority v0          PASS WITH HARDENING
Visibility v0         PASS WITH HARDENING
Acknowledgement v0    PASS WITH HARDENING
Generic Acceptance    REJECTED
Decision v0           PASS WITH HARDENING
Universal Approval    REJECTED
Universal Reconciliation REJECTED
Universal EffectiveChange REJECTED
Agreement / Consent v0 PASS WITH HARDENING
Generic Assent        REJECTED
Universal Contract    REJECTED
Universal Consent/Permission REJECTED
```

Current milestone:

```text
Representation / on-behalf-of v0
PASS WITH HARDENING
hardenings incorporated
propagation complete
post-write QA PENDING

Principal domain primitive       REJECTED
Universal Delegation root        REJECTED
Impersonation-as-attribution     REJECTED
```

Current structural reopenings: **0**.  
Current unclassified material dependencies: **0**.

---

# 22. Current next action

Do **not** re-score another candidate until Representation v0 post-write QA passes against its pre-scope baseline.

After QA PASS:

```text
fresh re-score remaining candidate/dependency space
↓
select one highest-leverage demonstrated candidate/family
↓
execute one complete Methodology v3 cycle
↓
propagation analysis
↓
STOP BEFORE NEXT GIT WRITE
```

High-pressure remaining areas include Version/material equivalence, detailed reconciliation/source precedence, Proposal/request identity, GoalCriterion/evaluation, Verification/comprehension, Trigger/policy, Resource allocation/reservation, collective/group semantics and other documented debts. None is preselected.

---

# 23. Before broad implementation

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
backend packages / implementation
```

---

# 24. Documentation rule

Concept specs/checkpoints hold detailed evidence and history. This README is the current navigation/integration summary; `language-map.md` is the fast terminology map; `docs/workstreams/domain-model.md` is the operational save-game.

Do not silently rewrite historical checkpoints merely for vocabulary uniformity. Later accepted concepts close earlier deferred boundaries through explicit downstream amendments/current-doc updates.
