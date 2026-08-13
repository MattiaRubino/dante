# LifeOS Domain & Product Language Map

**Status:** Canonical terminology reference for the active Domain Atlas  
**Established:** 2026-08-11  
**Current revision:** 2026-08-13 — Agreement / Consent v0 PASS WITH HARDENING; generic Assent/Acceptance and universal Contract/Permission roots rejected  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

This is the fast canonical reference for LifeOS vocabulary. Detailed lifecycle, chronology, test evidence, benchmark evidence, rejected alternatives, dependency owners/triggers and persistence pressure remain in the concept specs and checkpoints.

```text
DOMAIN LANGUAGE
what the concept means canonically
        ↓
PRODUCT LANGUAGE
how LifeOS packages/presents it
        ↓
UI LANGUAGE
what users read/manipulate
        ↓
IMPLEMENTATION LANGUAGE
API/schema/code names after logical design
```

> **A domain concept does not require a dedicated visible UI object, and a visible product/UI term does not automatically justify a separate domain primitive.**

---

# 1. Terminology precedence

When terminology conflicts, use this order:

1. accepted Domain Atlas concept specification;
2. this Language Map;
3. current validation/checkpoint guardrails;
4. active workstream handoff;
5. current product behavior documents;
6. historical product documents/glossaries;
7. conversation history.

Historical docs remain evidence, not current ontology authority.

---

# 2. Current status classes

## CANONICAL

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
Subject             — contextual aboutness role, not entity/root
Person              — native human entity
Actor               — contextual agency capability, not entity/root
Asset               — current scoped native physical-object entity
Resource            — contextual planning/execution role, not entity/root
Relationship discipline — cross-cutting semantic rule, not entity/root
Responsibility      — specific accountability relation family
Participation       — specific involvement relation family
Authority           — cross-cutting governance relation/capability
Visibility          — cross-cutting information-exposure capability
Acknowledgement     — contextual explicit-taking-notice attestation/relation capability
Decision            — contextual bounded-resolution semantic family/capability
Agreement           — contextual multi-party mutual-assent relation/capability
Consent             — contextual actor-scoped bounded-permission relation/capability
```

`Account` has an accepted platform/access identity boundary but its detailed security model remains deferred.

## DERIVED / PROJECTION

Examples:

```text
free capacity
overrun / lateness
adherence / streak
query aggregates
needs confirmation
free/busy
safe availability projection
some progress percentages
approval requirements satisfied
```

Derived state does not automatically become a new domain source-of-truth object.

## PRODUCT PROFILE

Examples:

```text
Project
Program
Workout
Study plan
Release plan
Vehicle profile
Camera profile
Equipment profile
saved Tracker/History/Progress view
```

Profiles package canonical semantics; they do not automatically create kernel primitives.

## PRODUCT / UI TERM

Examples:

```text
Task
Repeat
Deadline
Calendar Block
Busy / Free
This time
Inbox
Register / Tracker / History / Progress
User
Gear / Device / Equipment / Inventory
Required equipment
Who's available?
Assigned to
Claim
Hand off
Going / Maybe / Can't go
Attended
Private
Shared with…
Free/busy only
Got it / Acknowledge / I've seen the change
Accept / Apply / Use this
Approve / Reject / Keep current / Finalize / Resolve
Agree / We agree / Accept terms
Allow / Share for this purpose / Use for… / Stop sharing
```

UI language must map to precise semantics without broadening them.

`Accept` is context-sensitive and is **not** a universal domain primitive. `Agree` is Agreement only when the applicable parties have mutually assented to materially same terms/version. `Allow`/`Share`/`Use for…` maps to Consent only when the interaction actually records actor-scoped bounded permission; otherwise it may map to Visibility, Authority, proposal or product workflow semantics.

`Approve`, `Reject`, `Keep current`, `Finalize`, `Resolve`, `Apply` and similar verbs may map to Decision/review semantics, proposal/effect semantics, or direct bounded target mutation depending on the real workflow. The UI label does not create a primitive.

## PROVISIONAL / SAFE-DEFERRED SEMANTIC AREAS

```text
Coordination Stewardship standalone primitive question
Understanding / comprehension common-ground semantics
Principal / delegation / on-behalf-of
Resource Requirement
Allocation / selection
Reservation / Capacity Claim
Dependency
Contribution
GoalCriterion / Goal relationships
Evidence ↔ Criterion / evaluation
Version / material equivalence
Verification
Trigger / conditional policy
focus/context relationships
group / collective actor / quorum / collective Decision or Agreement semantics
Proposal / request reusable identity
Detailed reconciliation / source-precedence policy
Consent legal validity / capacity / specialist basis
Consent purpose/use technical enforcement
Formal signature / Contract integration
retention / deletion / anonymization
Personal Knowledge generic link layer
```

These are demonstrated questions, not pre-approved primitives.

## REJECTED AS UNIVERSAL / CROSS-DOMAIN PRIMITIVE

```text
Acceptance / Assent root
Approval root
Reconciliation root
EffectiveChange / universal state-transition root
universal Contract root
universal Consent / Permission root
```

Useful acceptance, approval, agreement, consent, reconciliation and effect semantics remain inside the precise family/process/target semantics that give them meaning.

## DEFERRED SPECIALIST / LOGICAL / SECURITY AREAS

```text
Principal / credential / provider security identity
technical authorization/enforcement
Place / Location / Property
living-entity identity beyond Person
Document / Artifact identity
FinancialAccount specialist model
inventory / supply / consumption
retention / deletion / anonymization
field/facet/projection policy
sensitivity classification
AI Context Builder enforcement
read/view audit persistence
formal legal Contract/signature/witness/enforceability
regulated consent validity/capacity/jurisdiction
```

---

# 3. Historical / rejected kernel candidates

Current rejected abstractions include:

```text
universal Register
universal RegisterEntry
universal Subject entity/root
universal Actor entity/root
universal Resource entity/root
universal User domain root
universal ManagedObject root
universal Relationship entity/root/supertype
semantic-free related_to kernel truth
universal Responsibility entity/root
universal Assignment primitive
universal Claim primitive
universal Hand-off primitive
universal Participant entity/root
universal Participation/member/social-graph root
universal Invitation primitive
universal Attendance primitive
universal Authority entity/root / admin flag
universal Permission object as domain Authority
universal Access mega-concept
universal Visibility/ACL entity/root
universal delivery/read/Acknowledgement mega-state
universal Acceptance / Assent primitive/root
one universal accepted=true status across unrelated workflows
universal Approval primitive/root
universal Reconciliation primitive/root
universal EffectiveChange / StateTransition root
one universal approved=true status across unrelated workflows
Decision record for every mutation
universal Agreement / Contract root
universal Consent / Permission root
membership = consent
agreement = decision
consent = visibility / authority / technical permission
```

Rejected means the useful capability is preserved through smaller, more precise semantics.

---

# 4. Canonical Intention & Execution language

## Goal

**Question:** What outcome/condition/change/pattern is intentionally desired?

```text
Goal != Plan
Goal != Activity
Goal != Milestone
Goal != Evidence
```

Typical UI: Goal, Objective, contextual Target.

## Plan

**Question:** How is a purpose intended to be pursued/organized?

```text
Plan != Goal
Plan != Activity
Plan != Routine
Plan != Schedule
Plan != Actual
```

Typical product profiles: Project, Program, Study plan, Training plan, Trip plan.

## Activity

**Question:** What actionable work/behavior is intended to be performed?

```text
Activity != Event
Activity != Session
Activity != Actual
Activity identity != requester/responsible actor/expected performer/actual performer
Responsibility transfer != Activity identity change
```

Typical UI: Task, Action, Workout, Study item.

## Event

**Question:** What occurrence-centred thing is expected to happen?

```text
Event != Activity
Event != Schedule
Event != Participation response
Event != Actual Participation
Event identity != participant set/state
```

Typical UI: Meeting, Appointment, Lesson, Flight, Concert, Shift.

## Routine

**Question:** What behavioral/execution policy is intentionally expected to repeat?

```text
Routine != Recurrence
Routine != Event series
Routine != observed habit
```

## Milestone

**Question:** What meaningful contextual checkpoint matters inside Goal/Plan?

```text
Milestone != Goal
Milestone != GoalCriterion
Milestone != Activity/Event
Milestone != Outcome/Actual
```

Milestone attainment is evaluation/Evidence-backed state, not duplicate reality storage.

---

# 5. Canonical Time language

## Occurrence

**Question:** Which expected instance from a recurring/generative source is this?

```text
Occurrence != Recurrence
Occurrence != Schedule
Occurrence != Session
Occurrence != Actual
```

## Schedule

**Question:** When is this schedulable subject currently accepted/intended/expected to happen?

```text
Schedule != Temporal Constraint
Schedule != Deadline/target
Schedule != Recurrence
Schedule != Availability/Capacity claim
Schedule != Session/Actual
Schedule proposal != accepted Schedule
```

`accepted Schedule` means current canonical temporal assignment under applicable governance/policy, not universal Acceptance or Agreement by every participant. A material proposal becomes current Schedule through applicable proposal/Decision/effect + Authority/policy semantics; resulting temporal state remains owned by Schedule.

## Session

**Question:** Which logically continuous bounded episode of actual execution occurred?

```text
Session != Schedule
Session != Activity/Occurrence
Session != Event attendance/Participation
Session != broader Actual/Outcome
```

## Temporal Constraint

**Question:** Where/when is placement/duration/temporal relation allowed, required, bounded or preferred?

`Deadline` is latest-bound Temporal Constraint semantics, not a separate kernel primitive.

## Recurrence

**Question:** How does a temporal/generative pattern repeat?

```text
Recurrence != Routine
Recurrence != Occurrence
Recurrence != Schedule
Recurrence != Trigger
```

## Availability / Capacity

```text
Availability
= when a schedulable Resource's capacity may be used

Capacity
= how much / what kind of compatible commitment a schedulable Resource can sustain
```

```text
scheduled != capacity consumed
overlap != universal conflict
Capacity != universal busy/free boolean
```

---

# 6. Canonical Reality / Evidence language

## Actual

**Question:** How did this specific intention/expectation resolve in reality?

```text
Actual != Schedule
Actual != Session
Actual != Outcome
Actual != Observation
Actual != Evidence
Actual != Confirmation
Actual != Provenance
Actual != Decision
shared Actual != identical actor-specific Actual Participation
reported/asserted reality != established Actual
Authority != Actual/truth
Acknowledgement != Actual
Agreement/Consent != Actual
```

## Outcome

**Question:** What result/disposition followed from this realization in context?

```text
Outcome != Actual
Outcome != lifecycle state
Outcome != Observation
Outcome != Confirmation/Evidence/Provenance
```

## Observation

**Question:** What was observed/measured/reported/calculated about this Subject and when/contextually?

```text
Observation != Actual
Observation != Outcome
Observation != Quantity
Observation != universal RegisterEntry
Observation != Evidence/Confirmation/Provenance
```

## Confirmation

**Question:** Who/what explicitly affirms this specific target version, for which purpose/context?

```text
Confirmation != Actual
Confirmation != Outcome/Observation
Confirmation != Evidence/Provenance
Confirmation != Acknowledgement
Confirmation != family-specific Acceptance
Confirmation != Agreement
Confirmation != Consent
Confirmation != Verification
Confirmation != Authority
Confirmation != Visibility
Confirmation != Decision
```

## Evidence

**Question:** What information materially bears on this evaluation, in what direction/context?

```text
Evidence != source information
Evidence != Observation/Actual/Outcome
Evidence != Confirmation/Provenance
Evidence != GoalCriterion
Evidence != Decision
```

## Provenance

**Question:** How did this record/version come to exist/change, and what materially influenced it?

```text
Source != Provenance
Provenance != truth
Provenance != Authority
Provenance != Visibility
Provenance != Confirmation/Evidence/Version/Audit
Provenance != Decision / Decision rationale
```

---

# 7. Data / identity / contextual-role language

## Quantity

Reusable scalar amount value semantics: magnitude + unit semantics sufficient for interpretation.

```text
number != Quantity by default
Quantity != Observation
property/quantity-kind != unit
same unit != semantic equivalence/aggregation permission
Quantity != Range/Threshold/comparator/criterion
```

## Subject

**Question:** Who/what is this descriptive record primarily about?

```text
Subject = contextual aboutness role
Subject entity/root = rejected
Subject != Person/Actor/Account/Principal/Asset/Resource
Subject != observer/recorder/source/Authority/Visibility
```

## Person

Native persistent human identity.

```text
Person != Subject
Person != Actor
Person != Resource
Person != Participant
Person != Account/Principal/User
Person != Asset
non-account Person is ordinary domain reality
```

## Actor

**Question:** Who/what acts semantically in this context?

```text
Actor = contextual agency capability
Actor entity/root = rejected
Actor != Person/Account/Principal
Actor != Resource/Responsibility/Participation
Actor != Authority/Visibility
```

Use the specific role (`performed_by`, `recorded_by`, `confirmed_by`, `acknowledged_by`, `decided_by`, `consented_by`, `responsible_for`, etc.) when known.

## Account boundary

```text
Account != Person
Account != Actor
Account != Subject/Participant
Account != Principal by default
Account != Authority/Visibility
```

Detailed credentials/provider/security model remains deferred.

## Asset

Current scoped native identity for individually tracked non-human physical objects whose distinct identity/history materially matter.

```text
Asset != Person/Subject/Resource
Asset identity != owner/holder/custodian/steward
Asset != every physical thing
Asset != every managed thing
universal ManagedObject = rejected
```

## Resource

**Question:** What could provide what this execution context needs?

```text
Resource = contextual planning/execution eligibility/capability
Resource entity/root = rejected
Resource != Person/Asset/Subject/Actor
Resource != Requirement/candidate set/Allocation/Reservation/actual use
Resource != Responsibility/Performer/Participation
Resource != Authority/Visibility
```

---

# 8. Cluster-5 Relationship / Reasoning language

## Relationship modeling discipline

**Status:** CANONICAL CROSS-CUTTING RULE — PASS WITH HARDENING.

```text
universal Relationship root = rejected
semantic-free related_to = rejected
specific relation meaning > generic edge
qualified relation != entity automatically
queryability/cardinality/row-id != domain identity
orientation/symmetry/transitivity/inverse = relation-family-specific
```

Simple complete semantics may remain direct. Material relation state/history/time/privacy/Authority/provenance may justify a **specific qualified relation family**.

## Responsibility

**Question:** Who is accountable for ensuring this bounded commitment is appropriately handled?

```text
Responsibility != requester
Responsibility != expected performer
Responsibility != actual performer
Responsibility != Participation/Resource
Responsibility != Authority/Visibility
Responsibility != ownership/Stewardship
unknown holder != explicitly open/unassigned
```

```text
Assignment = role-specific establishment/change operation
Claim = self-initiated role-acquisition operation
Hand-off = role-specific transfer workflow
```

Current boundary:

```text
hand-off request
!= Acknowledgement
!= role-specific accepted response
!= Agreement automatically
!= Decision/Approval where required
!= effective transfer
```

## Participation

**Question:** Who is expected/intended to be involved, and separately who actually participated?

```text
Participant = contextual role, not identity/root
Participation != Responsibility/Performer/Resource/Organizer
Participation != Authority/Visibility/Session
Invitation != Participation response/Actual Participation
Participation response != Actual Participation
accepted != attended
declined != proved absent
no response != declined
```

`accepted` is Participation response semantics, not generic Acceptance or Agreement.

## Authority

**Question:** Who/what may legitimately make which bounded domain effect effective, on what target/scope/basis?

```text
Authority = contextual scoped governance relation/capability
Authority != Actor/Person/Account/Principal
Authority != Responsibility/Participation
Authority != Visibility/ownership/Confirmation/Acknowledgement
Authority != Agreement/Consent
Authority != Decision
Authority != truth
Authority != technical Permission
```

Consent may be one bounded basis/constraint under applicable policy; it does not create general Authority. Agreement may exist without Authority to make an agreed effect effective.

## Visibility

**Question:** What bounded information may this recipient/access context be exposed to?

```text
Visibility = contextual information-exposure capability
Visibility != Authority
Visibility != Account/Principal/technical read Permission
Visibility != Participation/Responsibility/ownership/Subject/Resource
Visibility != Sharing/Disclosure event
Visibility != actual View/Acknowledgement
Visibility != Consent
Visibility != arbitrary downstream Use
```

Consent may be one basis/constraint for exposure/use. Purpose/use permission belongs to Consent where applicable; technical enforcement remains separate.

## Acknowledgement

**Question:** Who explicitly took notice of this specific target/version/change in this context?

```text
Acknowledgement
= contextual actor-scoped explicit-taking-notice attestation/relation capability

Acknowledgement != delivery/read/display telemetry
Acknowledgement != understanding
Acknowledgement != Confirmation
Acknowledgement != family-specific Acceptance
Acknowledgement != Agreement/Consent
Acknowledgement != Participation response
Acknowledgement != Responsibility
Acknowledgement != Authority/Approval/Decision
Acknowledgement != effective change
Acknowledgement != Actual
```

## Decision

**Question:** What bounded question was resolved to what result, by whom/what, about which target/version/context?

```text
Decision
= contextual bounded-resolution semantic family/capability

Decision != Authority
Decision != effective domain change
Decision != Actual/truth
Decision != Provenance / rationale
Decision != Evidence/evaluation
Decision != Acknowledgement/Confirmation/family-specific Acceptance
Decision != Agreement/Consent
```

Approval is scoped Decision/review-result semantics. Reconciliation is a process/pattern. Effective state remains owned by the affected concept.

## Agreement

**Status:** CANONICAL — PASS WITH HARDENING.  
**Source:** `concepts/agreement.md`  
**Validation:** `checkpoints/agreement-consent-v0-validation.md`

**Question:** Which parties mutually assented to which materially specific terms, in which bounded context?

```text
Agreement
= contextual multi-party mutual-assent relation/capability

Agreement != one Actor's response
Agreement != Acknowledgement
Agreement != Decision
Agreement != Authority
Agreement != Responsibility/resulting state
Agreement != Consent
Agreement != legal Contract/enforceability
Agreement != compliance/Actual
```

Key rules:

```text
one party assent != Agreement for everyone
silence/no response != Agreement
Agreement(terms v1) != Agreement(materially changed v2) by default
shared Agreement != all surrounding context visible
current no Agreement != never agreed historically
AI inference != human Agreement
```

Agreement may be direct/derived in simple cases or specifically qualified where party set, terms/version, history, privacy or lifecycle materially matter. Qualified does not imply a native root.

## Consent

**Status:** CANONICAL — PASS WITH HARDENING.  
**Source:** `concepts/consent.md`  
**Validation:** `checkpoints/agreement-consent-v0-validation.md`

**Question:** Who explicitly permitted what bounded action/use/exposure concerning what target, for which scope/purpose/context?

```text
Consent
= contextual actor-scoped bounded-permission relation/capability

Consent != Visibility
Consent != Authority
Consent != technical authorization/Permission
Consent != Agreement
Consent != Decision
Consent != Acknowledgement/Confirmation/family response
Consent != proof of legal validity/capacity
Consent != proof permitted action occurred
```

Key rules:

```text
silence/behavior/membership != Consent
Consent to X != Consent to Y
Consent purpose A != materially different purpose B
Consent(scope/version v1) != materially changed v2 by default
withdrawal changes future applicability != erases historical grant/use/disclosure
one Actor's Consent != group Consent automatically
helper action != represented person's Consent automatically
AI inference/access != human Consent or expanded scope
```

LifeOS records bounded permission semantics; regulated legal/clinical validity remains specialist/policy work.

## Acceptance disposition

Generic cross-domain `Acceptance` / `Assent` is **not** a canonical standalone primitive.

```text
invitation accepted
→ Participation response

Responsibility hand-off accepted
→ Responsibility-specific response/operation

proposal accepted / applied
→ proposal/effect-specific response/operation

all applicable parties assent to same terms
→ Agreement

actor explicitly permits bounded action/use/exposure
→ Consent
```

---

# 9. Commonly confused multi-actor semantics

```text
Person != Account
Actor != Account/Principal
Actor action != Authority
Authority != technical permission
Visibility != Authority
Visibility != Consent
Visibility != actual view
Authority != Agreement/Consent
Authority != Decision
Decision != effective target state
Decision != Actual/truth
Decision != Provenance/rationale
Responsibility != Authority/Visibility
Participation != Authority/Visibility
Subject != Authority/Visibility
Asset ownership != Authority/Visibility
Creator != Owner/Governor
```

```text
hand-off request != Acknowledgement
Acknowledgement != role-specific response
role-specific response != Agreement automatically
role-specific response != Decision/Approval by default
Invitation != Participation response
Participation response != Agreement
Participation response != Actual Participation
Delivery/read/display != Acknowledgement
Acknowledgement != Confirmation
Acknowledgement != Agreement/Consent
Agreement != Consent
Agreement != Decision/Authority
Consent != Visibility/Authority/technical Permission
Decision != Agreement/Consent
Agreement/Consent != Actual
```

---

# 10. AI guardrails

```text
AI inference != established identity
AI inference != established relationship
AI inference != Actual
AI inference != Confirmation
AI inference != human Acknowledgement
AI inference != human Agreement
AI inference != human Consent
AI proposal != Responsibility transfer
AI participation inference != response/attendance truth
AI Resource match != authoritative Allocation
AI ability to act/reason != Authority
AI proposal/recommendation != Decision
AI system Decision != human Decision
AI source access/processing != disclosure Visibility
AI access/processing != permission to enlarge Consent purpose/scope
AI provenance != disclosure permission
```

AI authority remains bounded by applicable Principal/context/policy; output disclosure is evaluated independently from input access. AI must not launder recommendation, clickstream or inference into human Agreement/Consent.

---

# 11. Product/UI mappings

```text
Occurrence          → This time / This workout / This meeting
Temporal Constraint → Deadline / Preferred time / Not before
Actual              → What happened? / Actual time / Performed
Outcome             → Passed / Partial / Result
Observation         → Weight / Mood / Score / Odometer / Shutter count
Quantity            → 66.4 kg / 5 km / 45 min
Subject             → usually hidden; natural referent label
Actor               → hidden; expose Done by / Recorded by / Suggested by / Decided by
Account             → Account / Profile / Login in settings
Asset               → Car / Camera / Laptop / Bike / Gear
Resource            → Camera / Room / Person / Service / Who's available?
Relationship        → expose specific verb/role, not generic noun
Responsibility      → Responsible / Assigned to / Who's handling this?
Participation       → Going / Maybe / Can't go / Attended
Authority           → normally hidden; expose specific action/approval rights
Visibility          → Private / Shared with… / free-busy only / visibility settings
Acknowledgement     → Got it / Acknowledge / I've seen the change / Received
Decision            → Choose / Keep current / Approve / Reject / Finalize / Resolve
Agreement           → We agree / Agree to these terms / Terms agreed
Consent             → Allow / Share for this purpose / Use for… / Stop sharing
Assignment          → Assign / Reassign
Claim               → I'll take it / Claim
Hand-off            → Hand off / Transfer
Confirmation        → Confirm / Looks correct / Needs confirmation
Evidence            → Why? / Based on…
Provenance          → Source / Imported from / Corrected by / View history
```

Context-sensitive UI verbs such as `Accept`, `Apply`, `Approve`, `Agree`, `Allow`, `Share`, `Use this`, `Continue`, `Reject`, `Finalize`, `Resolve` must map to their actual semantic family/effect.

> **A UX label does not automatically create or broaden a backend/domain type.**

---

# 12. Implementation-language guardrails

Do not infer final tables/classes/FKs from this map.

In particular:

- no universal `subjects`, `actors`, `resources`, `relationships`, `participants`, `authorities`, `visibility_acl`, `acknowledgements`, `acceptances`, `agreements`, `consents`, `approvals`, `reconciliations`, `effective_changes`, or universal state-transition root is pre-approved merely from semantic capability names;
- Agreement/Consent may justify specific qualified persistence where lifecycle/history require it, but their validation does not pre-approve universal tables or polymorphic target FKs;
- Decision semantics do not pre-approve one row for every mutation;
- `Person.id = Account.id` is not accepted;
- `Account = Principal` is not accepted by default;
- `User` must not become universal FK because UI uses the word;
- direct/qualified relation decisions are semantic, not driven by SQL many-to-many pressure;
- planned/response Participation and Actual Participation remain independently representable;
- Acknowledgement remains distinct from provider read/display telemetry;
- generic `accepted=true`, `agreed=true`, `consented=true`, or `approved=true` must not become cross-domain workflow fields;
- Authority remains separate from technical authorization;
- Consent remains separate from technical Permission/enforcement;
- Decision remains separate from Authority, Provenance, target state and Actual;
- Agreement remains separate from Decision, Authority and resulting Responsibility/state;
- Visibility remains separate from technical read permission and arbitrary downstream use;
- target/projection Visibility must not force source disclosure;
- no per-recipient duplicate canonical reality is required;
- provider/source/auth identifiers do not define native identity by default;
- Register/Tracker UI remains query/projection capability over native records;
- arbitrary JSON must not replace typed semantics.

---

# 13. Current cluster status

```text
Intention & Execution v0        PASS
Time v0                         PASS
Observed Reality & Evidence v0  PASS
Data / Subjects v0              PASS WITH HARDENING
Deferred Dependency Closure     PASS
Cross-Cluster Validation v4     PASS WITH HARDENING

Relationships / Reasoning       IN PROGRESS
Relationship v0 review          PASS WITH HARDENING
Responsibility v0 review        PASS WITH HARDENING
Participation v0 review         PASS WITH HARDENING
Authority v0 review             PASS WITH HARDENING
Visibility v0 review            PASS WITH HARDENING
Acknowledgement v0 review       PASS WITH HARDENING
Generic Acceptance primitive    REJECTED
Decision v0 review              PASS WITH HARDENING
Universal Approval primitive    REJECTED
Universal Reconciliation root   REJECTED
Universal EffectiveChange root  REJECTED
Agreement / Consent v0 review   PASS WITH HARDENING — propagation in progress / QA pending
Generic Assent root             REJECTED
Universal Contract root         REJECTED
Universal Consent/Permission root REJECTED
```

Current structural reopenings: **0**.  
Current unclassified material dependencies: **0**.

Normative Cluster-5 references:

- `checkpoints/relationship-v0-validation.md`;
- `concepts/responsibility.md` + validation;
- `concepts/participation.md` + validation;
- `concepts/authority.md` + validation;
- `concepts/visibility.md` + validation;
- `concepts/acknowledgement.md` + validation;
- `concepts/decision.md` + validation;
- `concepts/agreement.md`;
- `concepts/consent.md`;
- `checkpoints/agreement-consent-v0-validation.md`.

---

# 14. Current next-selection pressure

Do not continue by historical roadmap order and do not preselect the next primitive from vocabulary.

Current resolved Cluster-5 decomposition includes:

```text
who acts?                    Actor
who is accountable?         Responsibility
who is involved?            Participation
who may govern?             Authority
who may see?                Visibility
who explicitly noticed?     Acknowledgement
what was resolved?          Decision
which parties mutually assented to same terms? Agreement
who permitted which bounded use/action/exposure? Consent
what state is effective?    affected domain concept
what actually happened?     Actual
```

The next step **after Agreement/Consent post-write QA PASS** is a fresh re-score of the remaining demonstrated candidate/dependency space by dependency leverage.

Still-material areas include:

```text
Principal / delegation / on-behalf-of
Version / material equivalence
Proposal / request reusable identity
Detailed reconciliation / source-precedence policy
Dependency
Coordination Stewardship standalone question
Contribution
GoalCriterion / Goal relationships
Evidence ↔ Criterion/evaluation
Resource Requirement / Allocation / Reservation / substitution
Verification / comprehension
AI Proposal
focus/context relationships
Trigger / conditional policy
collective/group/quorum semantics
Consent validity / purpose-use enforcement
formal Contract/signature specialist boundary
retention / deletion
Personal Knowledge generic link layer
```

These remain **candidates/dependencies, not a checklist of primitives**.

---

# 15. Maintenance rule

This file is semantic navigation, not a duplicate of every concept spec.

It should answer:

> **What does this term mean, what does it not mean, what status does it have, and what might a user actually see?**

Detailed chronology, benchmark evidence, ADS owners/triggers, rejected alternatives and persistence pressure remain in the authoritative concept/checkpoint documents.

Do not rewrite historical evidence merely for terminology uniformity. Close old deferred boundaries through current concept specs, downstream amendments/checkpoints and the active workstream handoff.