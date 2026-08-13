# LifeOS Domain Atlas

**Status:** In progress — Clusters 1–4 validated together; Relationships / Reasoning active  
**Started:** 2026-08-10  
**Current revision:** 2026-08-13 — Agreement / Consent v0 PASS WITH HARDENING; generic Assent/Acceptance and universal Contract/Permission roots rejected  
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

Every new candidate/family uses **Domain Validation Methodology v3**:

```text
candidate selection / dependency re-score
        ↓
evidence + candidate formation
EV-01 internal evidence
EV-02 real-world workflow inversion
EV-03 targeted external benchmark
EV-04 smallest candidate
        ↓
CORE-01..13
        ↓
MA-01..20
        ↓
XCON-01..06
        ↓
Adjacent Dependency Sweep
        ↓
adversarial log
reopening/dependency register
regression additions
        ↓
concept verdict
        ↓
documentation propagation analysis
        ↓
STOP BEFORE GIT WRITE
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

- unresolved question;
- why current acceptance is safe;
- future owner/stage;
- exact reopening trigger;
- exact tests to rerun.

No unnamed `TBD` / `review later` is accepted for a material dependency.

Canonical method references:

- [`Validation Methodology v3`](validation-methodology-v3.md)
- [`Validation Execution Template v3`](validation-execution-template-v3.md)
- [`Multi-Actor Readiness v1`](multi-actor-readiness-v1.md)
- [`Domain & Product Language Map`](language-map.md)

Canonical acceptance rule:

```text
V3 verdict in chat
!= accepted Domain Atlas baseline

accepted baseline
= complete V3
+ hardenings incorporated
+ documentation propagation
+ approved Git write
+ post-write QA PASS
```

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

Benchmark behavior, lifecycle, correction/history, failure modes, Authority, privacy, sync and product cost rather than importing nouns.

External findings must be classified as:

```text
BORROW
ADAPT
ALREADY STRONGER
ANTI-PATTERN
NOT APPLICABLE
```

A mature product feature, standard noun or technically feasible architecture does not prove LifeOS should adopt the same ontology.

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
Decision
Agreement
Consent
```

Rejected universal abstractions include:

```text
Generic cross-domain Acceptance / Assent
Universal Approval
Universal Reconciliation
Universal EffectiveChange / StateTransition
Universal Contract
Universal Consent / Permission root
```

Useful semantics remain in their precise families:

- positive response stays with Participation/Responsibility/proposal workflow;
- Approval is scoped Decision/review-result semantics;
- Reconciliation is a process/pattern;
- effective state belongs to the affected concept;
- Agreement is mutual assent to materially same terms among applicable parties;
- Consent is actor-scoped bounded permission for action/use/exposure under scope/purpose/context.

---

# 5. Core non-collapse baseline

```text
Goal != Plan != Activity
Activity != Event
Routine != Recurrence
Occurrence != Schedule != Session != Actual
Schedule != Temporal Constraint / Availability / Capacity

Actual != Outcome / Observation / Confirmation / Evidence / Provenance / Decision
Observation != Quantity
Evidence != source information / Decision
Provenance != Source / truth / Authority / Visibility / Version / Audit / Decision / rationale

Subject != Person / Actor / Account / Principal / Asset / Resource
Person != Actor / Account / Principal / Asset
Actor != Account / Principal / Resource / Responsibility / Participation / Authority / Visibility
Asset != Subject / Resource / owner / holder
Resource != Requirement / Allocation / Reservation / actual use

Responsibility != requester / expected performer / actual performer / Resource / Participation / Authority / Visibility / Decision
Participation != Responsibility / Performer / Resource / Organizer / Authority / Visibility / Session / Decision
Authority != Actor / Account / Principal / Responsibility / Participation / Visibility / ownership / Confirmation / Acknowledgement / Agreement / Consent / Decision / truth
Visibility != Authority / Account / Principal / technical read permission / Participation / Responsibility / ownership / actual View / Acknowledgement / Consent

Delivery/read/display telemetry != Acknowledgement
Acknowledgement != understanding
Acknowledgement != Confirmation
Acknowledgement != Participation response
Acknowledgement != Agreement / Consent
Acknowledgement != Responsibility
Acknowledgement != Authority / Decision / effective change
Acknowledgement != Actual

Decision != Authority
Decision != effective domain change
Decision != Actual / truth
Decision != Provenance / rationale
Decision != Evidence / evaluation
Decision != Acknowledgement / Confirmation / family-specific Acceptance
Decision != Agreement / Consent

Agreement != one Actor's response
Agreement != Acknowledgement
Agreement != Decision / Authority
Agreement != Responsibility / resulting state
Agreement != Consent
Agreement != legal Contract / enforceability
Agreement != compliance / Actual

Consent != Visibility
Consent != Authority
Consent != technical Permission / authorization
Consent != Agreement
Consent != Decision
Consent != Acknowledgement / Confirmation / family response
Consent != legal-validity/capacity proof
Consent != proof permitted action occurred
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
- generic Personal Knowledge links remain separately SAFE DEFERRED.

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

Key rules:

```text
Responsibility != requester
Responsibility != expected performer
Responsibility != actual performer
Responsibility != Resource
Responsibility != Participation
Responsibility != Authority
Responsibility != Visibility
Responsibility != Decision
Responsibility != coordination Stewardship
unknown holder != explicitly open/unassigned
hand-off request != effective transfer by default
Responsibility transfer != Activity identity change
```

Consequential transfer may follow:

```text
hand-off request
!= Acknowledgement
!= role-specific response
!= Agreement automatically
!= Approval/Decision where required
!= effective transfer
```

The resulting effective Responsibility state remains owned by Responsibility.

---

# 8. Participation v0

Normative references:

- [`Participation`](concepts/participation.md)
- [`validation`](checkpoints/participation-v0-validation.md)

Verdict: **PASS WITH HARDENING**.

```text
Participation
= expected/intended or Actual involvement in a bounded shared occurrence/interaction
```

Key rules:

```text
Participant = contextual role, not identity/root
Invitation = participation proposal/request, not universal primitive
Participation response != Actual Participation
accepted != attended
declined != proved absent
no response != declined
Event identity != participant set/state
shared Actual != identical actor-specific Actual Participation
Participation != Session / Responsibility / Performer / Resource / Authority / Visibility / Decision
Participation accepted != Agreement automatically
```

Provider attendance telemetry remains Evidence/Provenance until applicable reconciliation establishes current truth.

---

# 9. Authority v0

Normative references:

- [`Authority`](concepts/authority.md)
- [`validation`](checkpoints/authority-v0-validation.md)

Verdict: **PASS WITH HARDENING**.

```text
Authority
= contextual governance capability determining who/what may legitimately
  make a bounded domain effect effective for a defined target/scope/action/context
```

Key rules:

```text
Authority to do X != Authority to do Y
Actor action != Authority
Account/Principal != Authority
Responsibility/Participation != Authority
Visibility != Authority
Acknowledgement != Authority
Agreement != Authority
Consent != Authority
Decision != Authority
ownership != Authority
Confirmation != Authority
Authority != truth
technical permission/authorization != domain Authority
current Authority != historical Authority at action time
claimed Authority != established Authority
revoked/expired Authority != never existed
```

Delegation is bounded; re-delegation is not implied. Consent may be one bounded policy basis/constraint without creating general Authority. Agreement may exist without Authority to make an agreed downstream effect effective.

---

# 10. Visibility v0

Normative references:

- [`Visibility`](concepts/visibility.md)
- [`validation`](checkpoints/visibility-v0-validation.md)

Verdict: **PASS WITH HARDENING**.

```text
Visibility
= contextual information-exposure capability determining what bounded
  representation may be made available to a recipient/access context
```

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
Visibility != technical read permission
Visibility != Acknowledgement
Visibility != Consent
AI may process source != AI may disclose source
```

Consent may be one basis/constraint for exposure/use; purpose/use permission belongs to Consent where applicable while technical policy/enforcement remains separate.

---

# 11. Acknowledgement v0

Normative references:

- [`Acknowledgement`](concepts/acknowledgement.md)
- [`validation`](checkpoints/acknowledgement-v0-validation.md)

Verdict: **PASS WITH HARDENING**.

```text
Acknowledgement
= contextual actor-scoped explicit taking-notice of a specific
  target/material version/change/request for a defined context
```

Key rules:

```text
sent/delivered/displayed/read != Acknowledgement
Acknowledgement != understanding/comprehension
Acknowledgement != Confirmation
Acknowledgement != family-specific Acceptance
Acknowledgement != Agreement / Consent
Acknowledgement != Participation response
Acknowledgement != Responsibility
Acknowledgement != Authority/Approval/Decision
Acknowledgement != effective domain change
Acknowledgement != Actual/performance
silence/no response != Acknowledgement
Acknowledgement(v1) != Acknowledgement(v2) after material change
AI/provider inference != human Acknowledgement
```

Generic cross-domain Acceptance/Assent remains rejected.

---

# 12. Decision v0

Normative references:

- [`Decision`](concepts/decision.md)
- [`validation`](checkpoints/decision-v0-validation.md)

Verdict: **PASS WITH HARDENING — post-write QA PASS**.

```text
Decision
= contextual bounded-resolution semantics determining what bounded question
  was resolved to what result, by whom/what, about which target/version/context
```

Key rules:

```text
Decision != Authority
Decision != effective domain state/change
Decision != Actual/objective truth
Decision != Provenance/rationale
Decision != Evidence/evaluation
Decision != Acknowledgement/Confirmation/family-specific Acceptance
Decision != Agreement/Consent
Decision(target v1) != materially changed v2 by default
Decision time != effect time != Actual time
Decision may cause zero/one/multiple effects
effective change may occur without new explicit human Decision under bounded authorized policy
superseded/reversed Decision != never decided
shared Decision != every Actor's Agreement/Consent
AI proposal/recommendation != Decision
```

Approval is scoped Decision/review-result semantics; Reconciliation is a process/pattern; affected concept owns effective state.

---

# 13. Agreement v0

Normative references:

- [`Agreement`](concepts/agreement.md)
- [`Agreement / Consent validation`](checkpoints/agreement-consent-v0-validation.md)

Current milestone verdict: **PASS WITH HARDENING — propagation in progress; post-write QA pending**.

```text
Agreement
= contextual multi-party mutual-assent relation/capability through which
  the applicable party set has assented to materially same terms/version
```

Key rules:

```text
one party assent != Agreement for everyone
silence/no response != Agreement
Acknowledgement != Agreement
family-specific positive response != Agreement automatically
Agreement != Decision
Agreement != Authority
Agreement != Responsibility/resulting state
Agreement != Consent
Agreement != legal Contract/enforceability
Agreement != compliance/Actual
Agreement(v1) != materially changed v2 by default
current no Agreement != never agreed historically
AI inference != human Agreement
```

Agreement may be direct/derived where simple or specifically qualified where party set, terms/version, history, privacy or lifecycle materially matter. No universal Agreement/Contract root is pre-approved from this semantic capability.

---

# 14. Consent v0

Normative references:

- [`Consent`](concepts/consent.md)
- [`Agreement / Consent validation`](checkpoints/agreement-consent-v0-validation.md)

Current milestone verdict: **PASS WITH HARDENING — propagation in progress; post-write QA pending**.

```text
Consent
= contextual actor-scoped permission relation/capability through which an eligible
  actor explicitly permits a bounded action/use/exposure concerning a target
  under a defined scope/purpose/context where Consent is an applicable basis
```

Key rules:

```text
silence/behavior/membership != Consent
Consent to X != Consent to Y
Consent purpose A != materially different purpose B
Consent(v1) != materially changed scope/version v2 by default
Consent != Visibility
Consent != Authority
Consent != technical authorization/Permission
Consent != Agreement
Consent != Decision
Consent != Acknowledgement/Confirmation/family response
Consent != proof of legal validity/capacity
Consent != proof permitted action occurred
withdrawal affects future applicability != erases historical grant/use/disclosure
one Actor's Consent != group Consent automatically
helper action != represented person's Consent automatically
AI inference/access != human Consent or expanded scope
```

Regulated validity/capacity/legal basis remains specialist/product-policy work. Purpose/use technical enforcement remains downstream security/logical work.

---

# 15. Cross-concept closure after Agreement / Consent v0

Current closed semantic boundaries include:

```text
Acknowledgement ↔ Agreement / Consent
Confirmation ↔ Agreement / Consent
Decision ↔ Agreement / Consent
Authority ↔ Agreement / Consent
Visibility ↔ Consent / purpose semantics
Agreement ↔ Responsibility
Agreement ↔ Consent
```

Current decomposition:

```text
who acts?                                  Actor
who is accountable?                       Responsibility
who is involved?                          Participation
who may govern?                           Authority
who may see?                              Visibility
who explicitly noticed?                   Acknowledgement
what bounded question was resolved?       Decision
which parties mutually assented to terms? Agreement
who permitted bounded use/action/exposure? Consent
what state is now effective?              affected domain concept
what actually happened?                   Actual
```

This does **not** mean Principal/delegation, Version, collective/quorum, legal validity, Proposal, policy enforcement, retention or evaluation semantics are finalized.

---

# 16. Multi-actor baseline

LifeOS remains personal-first but structurally multi-actor-ready.

Core rule:

> **Coordinate shared reality among independent actors while preserving each actor's private operating model, Authority boundaries, Visibility, Consent, Provenance, historical truth and appropriate level of digital complexity.**

Important consequences:

```text
Person/Actor != Account/Principal
shared canonical fact != actor-scoped state
Visibility != Authority/Consent
current access != historical attribution
non-LifeOS people are ordinary domain reality
proposal != Acknowledgement != family response != Agreement/Consent != Decision/Approval != effect != Actual
shared Decision != every Actor's stance/Agreement/Consent
one party assent != full Agreement
membership != Consent
AI Authority/disclosure/Consent never exceeds applicable context
```

No collaboration chat/ACL/read-receipt/approval/contract engine is pre-approved merely by these semantics.

---

# 17. Current semantic topology

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

BOUNDED RESOLUTION
Decision

MUTUAL ASSENT
Agreement

BOUNDED ACTOR PERMISSION
Consent
```

This is not a parent tree, processing chain or SQL schema.

---

# 18. Product simplicity rule

Kernel sophistication must not force ontology vocabulary into ordinary UI.

Examples:

```text
Responsibility   → Assigned to / Responsible
Participation    → Going / Maybe / Can't go / Attended
Authority        → normally hidden behind concrete rights/actions
Visibility       → Private / Shared with… / free-busy only
Acknowledgement  → Got it / Acknowledge / I've seen the change
Decision         → Choose / Keep current / Approve / Reject / Finalize / Resolve
Agreement        → We agree / Agree to these terms / Terms agreed
Consent          → Allow / Share for this purpose / Use for… / Stop sharing
Subject          → usually natural referent name
Actor            → Done by / Recorded by / Suggested by / Decided by
Resource         → Camera / Room / Person / Who's available?
```

Context-sensitive verbs such as `Accept`, `Apply`, `Use this`, `Agree`, `Allow`, `Approve`, `Reject`, `Keep current`, `Finalize` map to the real owning semantic family/effect. A UX label never creates a kernel concept by itself.

---

# 19. Persistence / API guardrails

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
one universal agreement/contract root
one universal consent/permission root
one universal approval root
one universal reconciliation root
one universal EffectiveChange/state-transition root
one Decision row for every mutation
generic agreed=true / consented=true / approved=true fields
shared=true as full privacy model
related_to + metadata as kernel
arbitrary JSON as primary domain model
```

A semantic capability name does not pre-approve a universal table. Direct/derived/qualified persistence remains a logical-model decision constrained by the accepted semantics.

Logical modeling comes **after Relationships / Reasoning and whole-domain regression**.

---

# 20. Cluster-5 status and next action

Relationships / Reasoning is **IN PROGRESS**.

Completed / current reviews:

```text
Relationship v0         PASS WITH HARDENING
Responsibility v0       PASS WITH HARDENING
Participation v0        PASS WITH HARDENING
Authority v0            PASS WITH HARDENING
Visibility v0           PASS WITH HARDENING
Acknowledgement v0      PASS WITH HARDENING — QA PASS
Generic Acceptance      REJECTED as standalone primitive
Decision v0             PASS WITH HARDENING — QA PASS
Universal Approval      REJECTED
Universal Reconciliation REJECTED
Universal EffectiveChange REJECTED
Agreement / Consent v0  PASS WITH HARDENING — propagation in progress / QA pending
Generic Assent root     REJECTED
Universal Contract root REJECTED
Universal Consent/Permission root REJECTED
```

Each completed accepted review has:

```text
REOPEN = 0
unclassified material dependencies = 0
```

Agreement/Consent also currently has `REOPEN = 0`, unclassified = 0, but does not become accepted baseline until this approved propagation and post-write QA pass.

**Next after Agreement/Consent QA PASS:** fresh re-score of the remaining candidate/dependency space by dependency leverage. Do not select the next concept merely from historical roadmap order.

Remaining demonstrated areas include:

- Principal / delegation / on-behalf-of;
- Version / material equivalence;
- Proposal / request reusable identity;
- detailed reconciliation / source-precedence policy;
- Dependency;
- Coordination Stewardship standalone question;
- Contribution;
- GoalCriterion / Goal relationships;
- Evidence ↔ Criterion/evaluation;
- Resource Requirement / Allocation / Reservation / substitution;
- Verification / comprehension;
- AI Proposal;
- focus/context relationships;
- Trigger/policy;
- collective/group/quorum semantics;
- Consent legal validity / purpose-use enforcement;
- formal Contract/signature specialist boundary;
- retention/deletion;
- generic Personal Knowledge links.

These remain **candidates/dependencies, not a checklist of primitives**.

---

# 21. Before broad implementation

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

# 22. Documentation rule

Concept specs/checkpoints hold detailed evidence and history. This README is the current navigation and integration summary; `language-map.md` is the fast terminology map; `docs/workstreams/domain-model.md` is the operational handoff.

Do not silently rewrite historical checkpoints merely for vocabulary uniformity. New accepted concepts close old deferred boundaries through explicit downstream amendments/current handoff updates.

A `PASS WITH HARDENING` is not treated as accepted merely because it appeared in chat; hardenings, documentation propagation and Git QA are part of the acceptance cycle.