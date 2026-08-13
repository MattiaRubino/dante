# LifeOS Domain & Product Language Map

**Status:** Canonical terminology reference for the active Domain Atlas  
**Established:** 2026-08-11  
**Current revision:** 2026-08-13 — Representation / on-behalf-of v0 PASS WITH HARDENING; propagation complete, post-write QA pending  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

This is the fast canonical reference for LifeOS vocabulary. Detailed lifecycle, chronology, evidence, benchmark classifications, rejected alternatives, dependency owners/triggers and persistence pressure remain in concept specs and validation checkpoints.

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
API/schema/code names only after logical design
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

# 2. Status classes

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
Asset               — scoped native physical-object entity
Resource            — contextual planning/execution role, not entity/root
Relationship discipline — cross-cutting semantic rule, not entity/root
Responsibility      — specific accountability relation family
Participation       — specific involvement relation family
Authority           — contextual governance relation/capability
Visibility          — contextual information-exposure capability
Acknowledgement     — contextual explicit-taking-notice attestation/relation capability
Decision            — contextual bounded-resolution semantic family/capability
Agreement           — contextual multi-party mutual-assent relation/capability
Consent             — contextual actor-scoped bounded-permission relation/capability
Representation      — contextual action-scoped on-behalf-of relation/capability
```

`Account` has an accepted platform/access identity boundary, while its detailed security model remains deferred.

## DERIVED / PROJECTION

Examples:

```text
free capacity
availability windows derived from constraints/schedules
current status summaries
progress summaries
register/tracker/history views
approval-requirements-satisfied
needs confirmation
needs acknowledgement
```

A projection does not become a new source of truth merely because product UI displays it.

## PRODUCT PROFILE / PRODUCT PACKAGING

Examples:

```text
Project
Program
Area
Calendar Block
Dashboard
Tracker
History
Routine template
```

These may package canonical concepts without becoming new kernel primitives.

## PRODUCT / UI TERMS

Context-sensitive examples:

```text
User
Owner
Member
Assignee
Attendee
Accept
Approve
Agree
Allow
Share
Delegate
Representative
On behalf of
```

The underlying semantic family determines the domain meaning.

## DEFERRED SECURITY / IMPLEMENTATION

```text
Principal
credential/authenticator
session/token
technical Permission
authorization policy/enforcement
impersonation mechanism
```

`Principal` is **not** a LifeOS domain primitive. It is a technical authenticated/authorized request identity to be finalized during security/logical design.

## PROVISIONAL / SAFE DEFERRED

Examples currently include:

```text
Version / material equivalence
Proposal / request reusable identity
Detailed reconciliation / source-precedence policy
Dependency
Coordination Stewardship standalone status
Contribution
GoalCriterion / evaluation relationships
Resource Requirement / Allocation / Reservation / substitution
Verification / comprehension
AI Proposal
focus/context relationships
Trigger / conditional policy
collective/group/quorum semantics
formal legal Contract/signature integration
retention/audit details
native Organization/system/AI identity shapes
```

These are candidate/dependency areas, not a checklist of primitives.

---

# 3. Rejected universal abstractions

Current rejected kernel abstractions include:

```text
universal Register / RegisterEntry root
universal User root
universal Subject root
universal Actor root/entity
universal Resource root/entity
universal ManagedObject root
universal Relationship graph/root
semantic-free related_to kernel relation
universal Participant/member/social-graph root
universal Responsibility/Assignment/Claim/Hand-off root
universal Authority/admin/Permission root
universal Access/Visibility ACL root
universal delivery/read/Acknowledgement state machine
universal cross-domain Acceptance / Assent root
universal Approval root
universal Reconciliation root
universal EffectiveChange / StateTransition root
Decision object for every mutation
universal Agreement / Contract root
universal Consent / Permission root
Principal as a LifeOS domain root
universal Agent / Representative identity root
universal Delegation root
technical impersonation as domain attribution truth
```

Rejected abstractions must not be reintroduced under new names without explicitly reopening the relevant checkpoint with stronger evidence.

---

# 4. Identity and role map

```text
Person
= persistent native human identity

Account
= platform/access identity boundary

Principal
= technical security/request identity — deferred security/implementation

Actor
= contextual semantic agency capability over a native referent/system

Subject
= contextual aboutness role

Resource
= contextual planning/execution eligibility/capability role

Representative
= contextual role of an Actor within a specific Representation/on-behalf-of relation
```

Canonical non-collapse:

```text
Person != Account != Principal
Person != Actor
Actor != Account/Principal
Actor != Subject
Actor != Resource
Actor != Representative identity
represented party != actual Actor by default
represented party != Subject/beneficiary automatically
```

No Account is required for a Person, Actor, participant, representative, Agreement party or Consent-giver to exist in domain reality.

---

# 5. Relationship modeling discipline

```text
universal Relationship entity/root/supertype   REJECTED
semantic-free related_to kernel truth           REJECTED
specific relation semantics                     REQUIRED
specific qualified relation                     ALLOWED WHEN JUSTIFIED
```

Use the most specific truthful semantics.

A connection may remain direct when that fully represents its meaning. When the relation itself has materially relevant state, lifecycle, history, temporal scope, actor-scoped state, Authority, Provenance, privacy/Visibility or invariants, a **specific qualified relation family** may be justified.

```text
qualified relation != independent entity automatically
```

SQL cardinality, row IDs or query frequency do not create domain identity.

---

# 6. Core multi-actor semantic questions

```text
who/what acts?                                  Actor
who is accountable?                             Responsibility
who is involved?                                Participation
who may govern?                                 Authority
what may be exposed?                            Visibility
who explicitly took notice?                     Acknowledgement
what bounded question was resolved?             Decision
which parties mutually assented to terms?       Agreement
who permitted bounded use/action/exposure?      Consent
who actually acted for which distinct party?    Representation / on-behalf-of
what state is now effective?                    affected domain concept
what actually happened?                         Actual
how did this record/action/result arise?         Provenance
```

These questions may coincide in simple personal flows. Their coincidence is convenience, not ontology.

---

# 7. Responsibility and Participation language

## Responsibility

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

Assignment/Claim/Hand-off are not universal primitives.

```text
request != Acknowledgement
!= role-specific response
!= Agreement automatically
!= Approval/Decision where required
!= effective Responsibility transfer
```

## Participation

```text
Participant = contextual role, not identity/root
Invitation = Participation proposal/request
Participation response != Actual Participation
accepted != attended
declined != proved absent
no response != declined
```

`accepted` in Participation remains Participation-response semantics, not generic Acceptance/Agreement.

A response Actor may act on behalf of a different participant; Representation preserves that attribution without rewriting the Actor.

---

# 8. Authority language

**Question:** Who/what may legitimately make which bounded domain effect effective, on what target/scope/basis?

```text
Authority = contextual scoped governance relation/capability
Authority != Actor/Person/Account/Principal
Authority != Responsibility/Participation
Authority != Visibility
Authority != Acknowledgement/Agreement/Consent
Authority != Decision
Authority != truth
Authority != technical Permission
Authority != Representation
```

Delegation means:

```text
bounded establishment / entrustment of a specific Authority
```

not:

```text
delegate everything
```

Canonical guardrails:

```text
Authority to do X != Authority to do Y
domain Authority != technical authorization
current Authority != historical Authority at action time
claimed Authority != established Authority
re-delegation is not implied
Representation claim != established Authority
```

---

# 9. Visibility and Consent language

## Visibility

**Question:** What bounded information may this recipient/access context be exposed to?

```text
Visibility = contextual information-exposure capability
Visibility != Authority
Visibility != technical read Permission
Visibility != actual View/Acknowledgement
Visibility != Consent
```

```text
can see != can change
can see != can re-disclose
can see != can use for every purpose
may see != actually saw
visible target != visible related records
visible projection != visible source
```

## Consent

**Question:** Who explicitly permitted what bounded action/use/exposure concerning what target, for which scope/purpose/context?

```text
Consent = contextual actor-scoped bounded-permission relation/capability
Consent != Visibility
Consent != Authority
Consent != technical Permission
Consent != Agreement
Consent != Decision
Consent != legal-validity/capacity proof
```

Representation does not fabricate represented Consent. A representative action counts for the represented party only where an applicable action-specific Authority/policy/specialist rule permits it.

---

# 10. Common ground / resolution / assent

## Acknowledgement

```text
Acknowledgement
= explicit actor-scoped taking-notice of a specific target/material version/change/request

Acknowledgement != delivery/read/display telemetry
Acknowledgement != understanding
Acknowledgement != Confirmation
Acknowledgement != Participation response
Acknowledgement != Agreement/Consent
Acknowledgement != Authority/Decision/effect
Acknowledgement != Actual
```

A represented Acknowledgement preserves the **actual acknowledging Actor**; it is not silently rewritten as the represented party's personal acknowledgement.

## Decision

```text
Decision
= contextual bounded resolution to a specific result

Decision != Authority
Decision != effective target state
Decision != Actual/truth
Decision != Provenance/rationale
Decision != Evidence/evaluation
Decision != Agreement/Consent
Decision != Representation
```

Approval is scoped Decision/review-result semantics. Reconciliation is a process/pattern. Effective state remains owned by the affected concept.

A represented Decision preserves the actual decision Actor/process and the represented party separately.

## Agreement

```text
Agreement
= contextual multi-party mutual assent to materially same terms/version

Agreement != one Actor's response
Agreement != Acknowledgement
Agreement != Decision
Agreement != Authority
Agreement != Responsibility/resulting state
Agreement != Consent
Agreement != legal Contract
Agreement != Actual
Agreement != Representation
```

Representative assent does not automatically become represented-party Agreement.

---

# 11. Representation / on-behalf-of

**Status:** CANONICAL CANDIDATE — PASS WITH HARDENING; propagation complete, post-write QA pending.  
**Source:** `concepts/representation.md`  
**Validation:** `checkpoints/representation-delegation-principal-v0-validation.md`

**Question:** Who actually acted, and for which distinct party was that action performed or asserted in this bounded context?

```text
Representation / on-behalf-of
= contextual action-scoped relation/capability
  through which an actual Actor acts for a distinct represented party
```

Canonical boundaries:

```text
actual Actor != represented party
Representation != Actor identity
Representation != Subject/beneficiary
Representation != Authority
Representation != Responsibility
Representation != Participation
Representation != Acknowledgement/Confirmation/Decision
Representation != Agreement/Consent
Representation != Provenance
Representation != Principal
technical impersonation != domain attribution truth
```

Critical scope rule:

```text
Authority to schedule for Anna
!= Authority to consent for Anna
!= Authority to agree for Anna
!= Authority to acknowledge for Anna
!= Authority to disclose Anna's private data
!= Authority to re-delegate
```

A `Representative` is contextual role language, not a native Person subtype.

### Principal

```text
Principal
= technical authenticated/authorized request identity
= DEFERRED SECURITY / IMPLEMENTATION

Principal != Person
Principal != Actor
Principal != represented party
Principal != Authority
Principal != Representation
```

### Delegation

```text
Delegation
= bounded Authority-establishment / entrustment pattern
```

not a universal root and not blanket transfer.

### Impersonation

A future security-layer impersonation mechanism may be valid technically, but:

```text
technical impersonation
!= semantic truth about who actually acted
```

Material actual-Actor attribution must survive where known.

---

# 12. Provenance language

```text
Provenance
= bounded contextual origin/evolution lineage

Provenance != Source alone
Provenance != truth
Provenance != Authority
Provenance != Confirmation/Evidence
Provenance != Version
Provenance != Decision/rationale
Provenance != Representation
```

A provenance chain may record:

```text
actual Actor
represented party
Principal/authentication context
Authority/delegation basis
source/process/version/time
```

where material, without collapsing those semantics into Provenance.

---

# 13. Acceptance / Assent disposition

Generic cross-domain `Acceptance` / `Assent` is **not** a canonical standalone primitive.

```text
invitation accepted
→ Participation response

Responsibility hand-off accepted
→ Responsibility-specific response/operation

proposal accepted/applied
→ proposal/effect-specific response/operation

all applicable parties assent to same terms
→ Agreement

actor explicitly permits bounded action/use/exposure
→ Consent
```

A UI label never creates a universal Acceptance/Assent type.

---

# 14. Commonly confused multi-actor semantics

```text
Person != Account != Principal
Actor != Account/Principal
Actor action != Authority
Actor != represented party by default
Representation != Authority
Representation != Responsibility
Representation != Subject/beneficiary
Representation != Provenance
Principal != Actor
technical impersonation != actual Actor
Authority != technical Permission
Visibility != Authority/Consent
Decision != Authority/effect/Actual
Agreement != Decision/Authority/Consent
Consent != Visibility/Authority/technical Permission
Acknowledgement != Agreement/Consent/Decision
Participation response != Agreement automatically
historical actor attribution != current access
```

---

# 15. AI guardrails

```text
AI inference != established identity
AI inference != Actual
AI inference != human Acknowledgement
AI inference != human Agreement
AI inference != human Consent
AI proposal/recommendation != human Decision
AI access/processing != disclosure Visibility
AI can act != AI has Authority
AI Actor != human Actor
AI acting for a user != unlimited Representation
AI acting under policy != human authorship/will
```

If AI/service materially performs a bounded represented action, preserve:

```text
actual AI/service Actor
represented party
applicable policy/Authority basis
Principal/security context where needed
resulting domain effect separately
```

Never launder AI/service behavior into a human action merely because the effect is for that human.

---

# 16. Product / UI mappings

```text
Occurrence          → This time / This workout / This meeting
Temporal Constraint → Deadline / Preferred time / Not before
Actual              → What happened? / Actual time / Performed
Outcome             → Passed / Partial / Result
Observation         → Weight / Mood / Score / Odometer
Quantity            → 66.4 kg / 5 km / 45 min
Subject             → usually hidden; natural referent label
Actor               → Done by / Recorded by / Suggested by / Decided by
Account             → Account / Profile / Login in settings
Principal           → normally hidden; security/admin detail only
Asset               → Car / Camera / Laptop / Bike / Gear
Resource            → Camera / Room / Person / Who's available?
Responsibility      → Responsible / Assigned to / Who's handling this?
Participation       → Going / Maybe / Can't go / Attended
Authority           → normally hidden behind concrete allowed actions/approvals
Visibility          → Private / Shared with… / free-busy only
Acknowledgement     → Got it / Acknowledge / I've seen the change
Decision            → Choose / Keep current / Approve / Reject / Finalize / Resolve
Agreement           → Agree / Agreed terms / We agree
Consent             → Allow / Share for this purpose / Stop sharing
Representation      → On behalf of… / Added by X for Y / Responded by X for Y / Scheduled by assistant
Confirmation        → Confirm / Looks correct / Needs confirmation
Evidence            → Why? / Based on…
Provenance          → Source / Imported from / Corrected by / View history
```

Context-sensitive verbs such as `Accept`, `Apply`, `Approve`, `Agree`, `Allow`, `Delegate`, `Represent`, `Reject` and `Finalize` map to the actual semantic family/effect. They do not create universal primitives.

---

# 17. Implementation-language guardrails

Do not infer final tables/classes/FKs from this map.

In particular:

- no universal `subjects`, `actors`, `resources`, `relationships`, `participants`, `authorities`, `visibility_acl`, `acknowledgements`, `agreements`, `consents`, `representatives`, `delegations`, `principals`, `decisions`, `approvals`, `reconciliations` or `effective_changes` root is pre-approved;
- `Person.id = Account.id` is rejected;
- `Account = Principal` is rejected;
- authenticated Principal must not automatically become semantic Actor;
- represented party must not overwrite actual Actor attribution;
- no universal `user_id` FK as domain identity;
- no generic `on_behalf_of` field on every record is pre-approved;
- no universal authorization/delegation graph is pre-approved;
- technical impersonation must not determine domain authorship;
- direct/qualified relation choices are semantic, not driven by SQL many-to-many pressure;
- provider/source/auth identifiers do not define native identity;
- projection Visibility does not define source Visibility;
- Authority != technical authorization;
- Consent != technical Permission;
- Provenance != Representation;
- arbitrary JSON must not replace typed semantics;
- final logical/physical representation waits for whole-domain gates.

---

# 18. Current cluster status

```text
Intention & Execution v0        PASS
Time v0                         PASS
Observed Reality & Evidence v0  PASS
Data / Subjects v0              PASS WITH HARDENING
Deferred Dependency Closure     PASS
Cross-Cluster Validation v4     PASS WITH HARDENING

Relationships / Reasoning       IN PROGRESS
Relationship v0                 PASS WITH HARDENING
Responsibility v0               PASS WITH HARDENING
Participation v0                PASS WITH HARDENING
Authority v0                    PASS WITH HARDENING
Visibility v0                   PASS WITH HARDENING
Acknowledgement v0              PASS WITH HARDENING
Generic Acceptance / Assent     REJECTED
Decision v0                     PASS WITH HARDENING
Universal Approval              REJECTED
Universal Reconciliation        REJECTED
Universal EffectiveChange       REJECTED
Agreement / Consent v0          PASS WITH HARDENING
Universal Contract              REJECTED
Universal Consent/Permission    REJECTED
Representation v0               PASS WITH HARDENING — POST-WRITE QA PENDING
Principal domain primitive      REJECTED by Representation v0 review
Universal Delegation root       REJECTED by Representation v0 review
Impersonation-as-attribution     REJECTED by Representation v0 review
```

Current structural reopenings: **0**.  
Current unclassified material dependencies: **0**.

Representation is not yet an accepted QA-closed baseline until post-write diff QA completes against its pre-scope commit.

---

# 19. Current next-selection pressure

Do **not** select another candidate until Representation v0 reaches post-write QA PASS.

After QA, perform a fresh re-score of the remaining demonstrated candidate/dependency space. High-pressure areas include, among others:

```text
Version / material equivalence
Detailed reconciliation / source precedence
Proposal / request reusable identity
GoalCriterion / evaluation
Verification / comprehension
Trigger / conditional policy
Resource Requirement / Allocation / Reservation / substitution
collective/group/quorum semantics
Dependency
Coordination Stewardship
Contribution
focus/context relationships
AI Proposal
retention/audit/privacy mechanics
formal specialist signature/Contract integration
```

These remain candidates/dependencies, not pre-approved primitives.

---

# 20. Maintenance rule

This file is semantic navigation, not a duplicate concept specification.

It should answer:

> **What does this term mean, what does it not mean, what status does it have, and what might a user actually see?**

Detailed chronology, external evidence classifications, ADS owners/triggers/tests, rejected alternatives and persistence pressure remain in authoritative concept/checkpoint documents.

Do not rewrite historical evidence merely for terminology uniformity. Close old deferred boundaries through current concept specs, downstream amendments and the active workstream handoff.
