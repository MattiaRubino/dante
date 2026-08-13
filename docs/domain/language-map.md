# LifeOS Domain & Product Language Map

**Status:** Canonical terminology reference for the active Domain Atlas  
**Established:** 2026-08-11  
**Current revision:** 2026-08-13 — Decision v0 PASS WITH HARDENING; Approval scoped; universal Reconciliation/EffectiveChange roots rejected  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

This is the fast canonical reference for LifeOS vocabulary. Detailed lifecycle, test evidence, history, benchmark evidence, rejected alternatives, dependency owners/triggers and persistence pressure remain in the concept specs and checkpoints.

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
```

UI language must map to precise semantics without broadening them.

`Accept` is especially context-sensitive: it maps to the owning semantic family/workflow and is **not** a universal domain primitive.

`Approve`, `Reject`, `Keep current`, `Finalize`, `Resolve`, `Apply` and similar verbs may map to Decision/review semantics, proposal/effect semantics, or direct bounded target mutation depending on the real workflow. The UI label does not create a new primitive.

## PROVISIONAL / SAFE-DEFERRED SEMANTIC AREAS

```text
Coordination Stewardship standalone primitive question
Understanding / comprehension common-ground semantics
Agreement
Consent / purpose limitation
Principal / delegation / on-behalf-of
Resource Requirement
Allocation / selection
Reservation / Capacity Claim
Dependency
Contribution
GoalCriterion / Goal relationships
Evidence ↔ Criterion / evaluation
Version
Verification
Trigger / policy
focus/context relationships
group / collective actor / collective Decision semantics
Proposal / request reusable identity
Detailed reconciliation / source-precedence policy
Personal Knowledge generic link layer
```

These are demonstrated questions, not pre-approved primitives.

## REJECTED AS UNIVERSAL / CROSS-DOMAIN PRIMITIVE

```text
Acceptance / Assent root
Approval root
Reconciliation root
EffectiveChange / universal state-transition root
```

Useful acceptance/approval/reconciliation/effect semantics remain inside the precise family/process/target semantics that give them meaning.

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

Typical UI: This time, This workout, This meeting.

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

`accepted Schedule` means the current canonical temporal assignment under the applicable governing context/policy. It does **not** mean every participant accepted Participation and it does not imply a universal Acceptance primitive.

A material proposal becomes current Schedule only through applicable proposal/Decision/effect + Authority/policy semantics. A Decision about Schedule does not replace Schedule's own current state, and a rejected Decision may leave Schedule unchanged. Authority to change Schedule does not imply Visibility of private sources; free/busy projection may be visible while the underlying Schedule/Event remains private.

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
```

Authority may govern establishment/correction of the current interpretation; Decision/reconciliation may explain how a bounded conflict was resolved; neither creates objective reality. Visibility of a safe consequence does not imply Visibility of the private Actual or its sources.

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

Missing Observation != observed negative != failed measurement.

## Confirmation

**Question:** Who/what explicitly affirms this specific target version, for which purpose/context?

```text
Confirmation != Actual
Confirmation != Outcome/Observation
Confirmation != Evidence/Provenance
Confirmation != Acknowledgement
Confirmation != Acceptance/Agreement
Confirmation != Verification
Confirmation != Authority
Confirmation != Visibility
Confirmation != Decision
```

Target Visibility does not expose Confirmation history automatically.

## Evidence

**Question:** What information materially bears on this evaluation, in what direction/context?

```text
Evidence != source information
Evidence != Observation/Actual/Outcome
Evidence != Confirmation/Provenance
Evidence != GoalCriterion
Evidence != Decision
```

Private Evidence use does not create disclosure permission. Evidence may inform a Decision without becoming the resolution.

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

Creator/source/recorder does not create Authority or Decision. A Decision may have Provenance. Target Visibility does not imply full lineage Visibility.

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

Being Subject does not grant Authority or Visibility. Visible referent != visible Subject relation/all records about it.

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

Use the specific role (`performed_by`, `recorded_by`, `confirmed_by`, `acknowledged_by`, `decided_by`, `responsible_for`, etc.) when known.

## Account boundary

Platform/access identity boundary.

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

Ownership may be a policy basis but does not equal Authority. Visible Asset != every private field/relation/history. Exact noun `Asset` remains renameable/non-semantic.

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

Resource does not manufacture provider identity. Visible free/busy/eligibility projection != visible private source.

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

Generic Personal Knowledge links remain separately SAFE DEFERRED and must not silently acquire operational/evidentiary/governance semantics.

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

None is a standalone universal primitive.

Current common-ground/governance boundary:

```text
hand-off request
!= Acknowledgement
!= role-specific accepted response
!= Decision/Approval where required
!= effective transfer
```

A Decision may resolve a transfer question but does not become Responsibility; the resulting Responsibility state remains owned by Responsibility.

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
no attendance evidence != proved absence
```

`accepted` here is Participation response semantics, not a universal Acceptance primitive.

Provider attendance telemetry is Evidence/Provenance until applicable reconciliation establishes current truth.

## Authority

**Status:** CANONICAL — PASS WITH HARDENING.  
**Source:** `concepts/authority.md`  
**Validation:** `checkpoints/authority-v0-validation.md`

**Question:** Who/what may legitimately make which bounded domain effect effective, on what target/scope/basis?

```text
Authority = contextual scoped governance relation/capability
Authority != Actor/Person/Account/Principal
Authority != Responsibility/Participation
Authority != Visibility/ownership/Confirmation/Acknowledgement/Acceptance
Authority != Decision
Authority != truth
Authority != technical Permission
```

Key rules:

```text
Authority to do X != Authority to do Y
domain Authority != technical authorization
current Authority != historical Authority at action time
claimed Authority != established Authority
revoked/expired != never existed
```

Delegation is a bounded Authority-establishment/entrustment pattern, not a universal root. Approval may exercise Authority but is not Authority itself. Decision answers what was resolved, not who had governance power.

## Visibility

**Status:** CANONICAL — PASS WITH HARDENING.  
**Source:** `concepts/visibility.md`  
**Validation:** `checkpoints/visibility-v0-validation.md`

**Question:** What bounded information may this recipient/access context be exposed to?

```text
Visibility = contextual information-exposure capability
Visibility != Authority
Visibility != Account/Principal/technical read Permission
Visibility != Participation/Responsibility/ownership/Subject/Resource
Visibility != Sharing/Disclosure event
Visibility != actual View/Acknowledgement
Visibility != Consent/arbitrary downstream Use
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
AI may process source != AI may disclose source
```

`Access` is deliberately not one domain mega-concept: inspect, modify, use, execute and disclose are different questions.

## Acknowledgement

**Status:** CANONICAL — PASS WITH HARDENING.  
**Source:** `concepts/acknowledgement.md`  
**Validation:** `checkpoints/acknowledgement-v0-validation.md`

**Question:** Who explicitly took notice of this specific target/version/change in this context?

```text
Acknowledgement
= contextual actor-scoped explicit-taking-notice attestation/relation capability

Acknowledgement != delivery/read/display telemetry
Acknowledgement != understanding
Acknowledgement != Confirmation
Acknowledgement != Acceptance/Agreement/Consent
Acknowledgement != Participation response
Acknowledgement != Responsibility
Acknowledgement != Authority/Approval/Decision
Acknowledgement != effective change
Acknowledgement != Actual
```

Key rules:

```text
silence/no response != Acknowledgement
Acknowledgement(v1) != Acknowledgement(v2) after material change
Acknowledgement by Actor A != Actor B/group acknowledgement
AI/provider inference != human Acknowledgement
future access revocation != erased historical Acknowledgement
```

`Acknowledgement` is optional and consequence-sensitive; LifeOS must not force read-receipt/acknowledgement bureaucracy into ordinary low-risk use.

## Decision

**Status:** CANONICAL — PASS WITH HARDENING.  
**Source:** `concepts/decision.md`  
**Validation:** `checkpoints/decision-v0-validation.md`

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

Key rules:

```text
Decision(target v1) != Decision(target v2) after material change by default
Decision time != effect time != Actual time
Decision may cause zero/one/multiple effects
effective change may occur without a new explicit human Decision under bounded authorized policy
superseded/reversed Decision != never decided
one Actor's Approval/Decision != collective Decision automatically
Decision result Visibility != rationale/Evidence/Provenance Visibility
AI proposal/recommendation != Decision
```

Approval is scoped Decision/review-result semantics whose effect depends on applicable Authority/policy. Reconciliation is a process/pattern that may culminate in Decision but is not universally a Decision. Effective state change remains owned by the affected domain concept.

## Acceptance disposition

Generic cross-domain `Acceptance` is **not** a canonical standalone primitive.

```text
invitation accepted
→ Participation response

Responsibility hand-off accepted
→ Responsibility-specific response/operation

proposal accepted / applied
→ proposal/effect-specific response/operation
```

Future Agreement and Consent semantics remain separately reviewable rather than being collapsed into one Assent/Acceptance root. Decision does not turn those semantics into a generic acceptance type.

---

# 9. Commonly confused multi-actor semantics

```text
Person != Account
Person may exist without Account
Actor != Account/Principal
Account authentication != semantic Actor
Actor action != Authority
Authority != technical permission
Visibility != Authority
Visibility != actual view
Authority != truth
Authority != Decision
Decision != effective target state
Decision != Actual/truth
Decision != Provenance/rationale
Responsibility != Authority/Visibility
Participation != Authority/Visibility
Subject != Authority/Visibility
Asset ownership != Authority/Visibility
Resource candidacy/allocation != Authority/Visibility
Creator != Owner/Governor
Sharing != ownership
```

```text
Assignment != Acceptance by default
Claim != effective Responsibility by default
hand-off request != Acknowledgement
Acknowledgement != role-specific acceptance
role-specific acceptance != Decision/Approval by default
Decision/Approval != effective role transfer by default
Invitation != Participation response
Participation response != Actual Participation
Schedule acceptance != Participation response
Delivery/read/display != Acknowledgement
Acknowledgement != Confirmation
Acknowledgement != Agreement/Consent
Agreement/Consent != Authority
Decision != Agreement/Consent
```

---

# 10. AI guardrails

```text
AI inference != established identity
AI inference != established relationship
AI inference != Actual
AI inference != Confirmation
AI inference != human Acknowledgement
AI proposal != Responsibility transfer
AI participation inference != response/attendance truth
AI Resource match != authoritative Allocation
AI ability to act/reason != Authority
AI proposal/recommendation != Decision
AI system Decision != human Decision
AI source access/processing != disclosure Visibility
AI provenance != disclosure permission
```

AI authority must remain bounded by the applicable Principal/context/policy, and output disclosure must be evaluated independently from input access.

An AI may acknowledge as its own semantic Actor only when that is the real actor/context; it must not manufacture another actor's acknowledgement. An AI/system may participate in a bounded Decision process only under explicit applicable policy/Authority, with correct attribution and without laundering the result into a human Decision.

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
Decision            → Choose / Keep current / Approve / Reject / Finalize / Resolve / Decision history where consequential
Assignment          → Assign / Reassign
Claim               → I'll take it / Claim
Hand-off            → Hand off / Transfer
Confirmation        → Confirm / Looks correct / Needs confirmation
Evidence            → Why? / Based on…
Provenance          → Source / Imported from / Corrected by / View history
```

Context-sensitive UI verbs:

```text
Accept
Apply
Use this
Approve
Agree
Allow
Reject
Keep current
Finalize
Resolve
```

must map to their actual semantic family/effect. They do not create a universal Acceptance/Assent/Approval/Decision-transition type.

> **A UX label does not automatically create or broaden a backend/domain type.**

---

# 12. Implementation-language guardrails

Do not infer final tables/classes/FKs from this map.

In particular:

- no universal `subjects`, `actors`, `resources`, `relationships`, `participants`, `authorities`, `visibility_acl`, `acknowledgements`, `acceptances`, `approvals`, `reconciliations`, `effective_changes`, or universal state-transition root is pre-approved;
- Decision semantics do not pre-approve one row for every mutation or one polymorphic `decisions` table;
- `Person.id = Account.id` is not accepted;
- `Account = Principal` is not accepted by default;
- `User` must not become the universal FK merely because UI uses the word;
- direct/qualified relation decisions are semantic, not driven by SQL many-to-many pressure;
- explicit open Responsibility must remain distinguishable from unknown;
- planned/response Participation and Actual Participation must remain independently representable;
- Acknowledgement must remain distinguishable from provider read/display telemetry;
- generic `accepted=true` or `approved=true` must not become cross-domain workflow fields;
- Authority semantics must remain separate from technical authorization/enforcement;
- Decision semantics must remain separate from Authority, Provenance, target state and Actual;
- the affected domain concept owns its effective state transition;
- Visibility semantics must remain separate from technical read permission and arbitrary data Use;
- target/projection Visibility must not force source disclosure;
- no per-recipient duplicate canonical reality is required;
- provider/source/auth identifiers do not define native identity by default;
- Register/Tracker UI remains a query/projection capability over native records;
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
- `concepts/decision.md` + validation.

---

# 14. Current next-selection pressure

Do not continue by historical roadmap order and do not preselect the next primitive from vocabulary.

The current Relationships / Reasoning decomposition now includes:

```text
who can govern?          Authority        RESOLVED
who can see?             Visibility       RESOLVED
who explicitly noticed?  Acknowledgement  RESOLVED
universal Acceptance?    REJECTED
what bounded question was resolved? Decision RESOLVED
universal Approval?      REJECTED
universal Reconciliation? REJECTED
universal EffectiveChange? REJECTED
```

The next step after Decision v0 propagation/QA is a **fresh re-score of the remaining demonstrated candidate/dependency space by dependency leverage**.

Still-material areas include, among others:

```text
Agreement
Consent / purpose limitation
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
Verification
AI Proposal
focus/context relationships
Trigger / conditional policy
collective/group/collective-Decision semantics
Personal Knowledge generic link layer
```

These remain **candidates, not a checklist of primitives**.

---

# 15. Maintenance rule

This file is semantic navigation, not a duplicate of every concept spec.

It should answer:

> **What does this term mean, what does it not mean, what status does it have, and what might a user actually see?**

Detailed chronology, benchmark evidence, ADS owners/triggers, rejected alternatives and persistence pressure remain in the authoritative concept/checkpoint documents.

Do not rewrite historical evidence merely for terminology uniformity. Close old deferred boundaries through current concept specs, downstream amendments/checkpoints and the active workstream handoff.
