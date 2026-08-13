# LifeOS Domain & Product Language Map

**Status:** Canonical terminology reference for the active Domain Atlas  
**Established:** 2026-08-11  
**Current revision:** 2026-08-13 — Version / material-equivalence v0 PASS WITH HARDENING; hardenings incorporated; final post-write QA pending  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

This is the fast canonical navigation layer for LifeOS terminology. Detailed lifecycle, chronology, benchmark evidence, adversarial tests, dependency owners/triggers and persistence pressure belong in concept specs/checkpoints.

```text
DOMAIN LANGUAGE
        ↓
PRODUCT LANGUAGE
        ↓
UI LANGUAGE
        ↓
IMPLEMENTATION LANGUAGE
```

> **A domain concept does not require a dedicated UI object, and a visible product/UI noun or verb does not automatically justify a domain primitive.**

---

# 1. Terminology precedence

1. accepted Domain Atlas concept specification;
2. this Language Map;
3. current validation/checkpoint guardrails;
4. active workstream handoff;
5. current durable product behavior docs;
6. historical product docs/glossaries;
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
Subject             — contextual aboutness role, not root
Person              — native human entity
Actor               — contextual agency capability, not root
Asset               — scoped native physical-object entity
Resource            — contextual planning/execution role, not root
Relationship discipline — cross-cutting rule, not root
Responsibility      — specific accountability relation family
Participation       — specific involvement relation family
Authority           — contextual governance capability
Visibility          — contextual information-exposure capability
Acknowledgement     — contextual explicit-taking-notice relation/capability
Decision            — contextual bounded-resolution family/capability
Agreement           — contextual multi-party mutual-assent relation/capability
Consent             — contextual actor-scoped bounded-permission relation/capability
Representation      — contextual action-scoped on-behalf-of relation/capability
Version             — contextual material-state reference capability; not a universal root/table
```

`Account` is an accepted platform/access identity boundary; its detailed security model remains deferred.

## DERIVED / PROJECTION

Examples:

```text
free capacity
availability windows
current status/progress summaries
register/tracker/history views
approval-requirements-satisfied
needs confirmation
needs acknowledgement
```

A projection is not automatically a new source of truth.

## PRODUCT PROFILE / PACKAGING

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

These may package canonical semantics without becoming kernel primitives.

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
Version
Revision
History
```

The owning semantic family determines the meaning.

## DEFERRED SECURITY / IMPLEMENTATION

```text
Principal
credential/authenticator
session/token
technical Permission
authorization policy/enforcement
impersonation mechanism
storage row version
provider revision / ETag / sync token
```

`Principal` means technical authenticated/authorized request identity. It is **not** a LifeOS domain primitive. Technical/provider revision identifiers may support concurrency/lineage but are not semantic Version by themselves.

## PROVISIONAL / SAFE DEFERRED

Current examples:

```text
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
exact Principal/AuthN/AuthZ mechanics
action-specific delegation policy
legal/specialist representation capacity
multi-hop delegation persistence
exact Version persistence / snapshot-delta/event-history strategy
```

Candidates/dependencies are not a checklist of primitives.

---

# 3. Rejected universal abstractions

```text
universal Register/RegisterEntry root
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
universal cross-domain Acceptance/Assent root
universal Approval root
universal Reconciliation root
universal EffectiveChange/StateTransition root
Decision object for every mutation
universal Agreement/Contract root
universal Consent/Permission root
Principal as LifeOS domain root
universal Agent/Representative identity root
universal Delegation root
technical impersonation as domain attribution truth
blanket delegation
automatic re-delegation
universal Version root/entity/table
one global material-equivalence rule
technical/provider/ETag revision as domain Version truth
mandatory event sourcing/version graph for all concepts
```

A rejected abstraction requires explicit reopening with stronger evidence before reintroduction.

---

# 4. Identity / agency / security / representation map

```text
Person
= persistent native human identity

Account
= platform/access identity boundary

Principal
= technical security/request identity

Actor
= contextual semantic agency capability

Subject
= contextual aboutness role

Resource
= contextual planning/execution eligibility/capability role

Representative
= contextual role of an Actor inside a specific Representation/on-behalf-of relation
```

Canonical non-collapse:

```text
Person != Account != Principal
Person != Actor
Actor != Account/Principal
Actor != Subject
Actor != Resource
actual Actor != represented party
represented party != Subject/beneficiary automatically
Representative != native Person subtype
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

A direct relation is sufficient when it fully represents meaning. A specifically qualified relation may be justified where the relation itself has material lifecycle, history, scope, Authority, Provenance, privacy/Visibility or invariants.

```text
qualified relation != independent entity automatically
```

SQL row IDs/cardinality/query frequency do not create domain identity.

---

# 6. Core multi-actor questions

```text
who/what acts?                                  Actor
who is accountable?                             Responsibility
who is involved?                                Participation
who may govern?                                 Authority
what may be exposed?                            Visibility
who explicitly took notice?                     Acknowledgement
what bounded question was resolved?             Decision
which parties mutually assented?                Agreement
who permitted bounded use/action/exposure?      Consent
who actually acted for which distinct party?    Representation / on-behalf-of
which material state is being referenced?       Version
what state is now effective?                    affected domain concept
what actually happened?                         Actual
how did this record/action/result arise?         Provenance
```

Coincidence in simple flows is convenience, not ontology.

---

# 7. Responsibility / Participation

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

No universal Assignment/Claim/Hand-off root.

```text
hand-off request
!= Acknowledgement
!= role-specific response
!= Agreement automatically
!= Approval/Decision where required
!= effective Responsibility transfer
```

## Participation

```text
Participant = contextual role
Invitation = Participation proposal/request
Participation response != Actual Participation
accepted != attended
declined != proved absent
no response != declined
```

A response Actor may act for a different participant; Representation preserves that fact without rewriting the Actor as the participant.

---

# 8. Authority

```text
Authority
= contextual scoped governance capability
```

```text
Authority != Actor/Person/Account/Principal
Authority != Responsibility/Participation
Authority != Visibility
Authority != Acknowledgement/Agreement/Consent
Authority != Decision
Authority != Representation
Authority != Version
Authority != truth
Authority != technical Permission
```

Delegation:

```text
bounded establishment / entrustment of a specific Authority
```

not `delegate everything`.

```text
Authority to X != Authority to Y
current Authority != historical action-time Authority
claimed Authority != established Authority
re-delegation is not implied
Representation claim != established Authority
```

---

# 9. Visibility / Consent

## Visibility

```text
Visibility = contextual information-exposure capability
Visibility != Authority
Visibility != technical read Permission
Visibility != actual View/Acknowledgement
Visibility != Consent
Visibility != Version
```

```text
can see != can change
can see != can re-disclose
can see != can use for every purpose
may see != actually saw
visible target != visible source/related records
visible projection state != source material state automatically
```

## Consent

```text
Consent
= contextual actor-scoped bounded permission for action/use/exposure
  concerning a defined target/scope/purpose/context
```

```text
Consent != Visibility
Consent != Authority
Consent != technical Permission
Consent != Agreement
Consent != Decision
Consent != Representation
Consent != Version
Consent != legal-validity/capacity proof
```

A representative action does not fabricate represented Consent. Effect requires an applicable action-specific basis/policy/specialist rule.

---

# 10. Acknowledgement / Decision / Agreement

## Acknowledgement

```text
Acknowledgement
= explicit actor-scoped taking-notice of a specific target/material version/change/request
```

```text
Acknowledgement != delivery/read/display
Acknowledgement != understanding
Acknowledgement != Confirmation
Acknowledgement != Participation response
Acknowledgement != Agreement/Consent
Acknowledgement != Authority/Decision/effect
Acknowledgement != Actual
```

Represented Acknowledgement preserves the actual Actor. A material target-state change does not silently inherit prior Acknowledgement unless purpose-specific material equivalence preserves the relevant state.

## Decision

```text
Decision
= contextual bounded resolution to a specific result
```

```text
Decision != Authority
decision != effective target state
Decision != Actual/truth
Decision != Provenance/rationale
Decision != Evidence/evaluation
Decision != Agreement/Consent
Decision != Representation
Decision != Version
```

Approval is scoped Decision/review-result semantics. Reconciliation is a process/pattern. Effective target state remains owned by the affected concept. Decision binds to the material state/question actually resolved.

## Agreement

```text
Agreement
= contextual multi-party mutual assent to materially same terms/version
```

```text
Agreement != one Actor's response
Agreement != Acknowledgement
Agreement != Decision
Agreement != Authority
Agreement != Responsibility
Agreement != Consent
Agreement != legal Contract
Agreement != Actual
Agreement != Representation
Agreement != Version
```

Representative assent does not automatically become represented-party Agreement.

---

# 11. Representation / on-behalf-of

**Status:** CANONICAL — PASS WITH HARDENING; post-write QA PASS.  
**Source:** `concepts/representation.md`  
**Validation:** `checkpoints/representation-delegation-principal-v0-validation.md`

> **Representation is the contextual action-scoped relation/capability through which an actual Actor performs a bounded semantic action while acting for a distinct represented party in a defined context.**

Question:

> **Who actually acted, and for which distinct party was that action performed or asserted in this bounded context?**

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

Critical action-specific scope rule:

```text
Authority to schedule for Anna
!= Authority to consent for Anna
!= Authority to agree for Anna
!= Authority to acknowledge for Anna
!= Authority to disclose Anna's private data
!= Authority to re-delegate
```

### Representative

Contextual role only, not native identity/type.

### Principal

```text
Principal = technical authenticated/authorized request identity
Principal != Person/Actor/represented party/Authority/Representation
```

### Delegation

```text
Delegation = bounded Authority-establishment / entrustment pattern
```

No universal root, blanket transfer or implied re-delegation.

### Impersonation

Possible future security mechanism only:

```text
technical impersonation != semantic truth about who actually acted
```

---

# 12. Provenance

```text
Provenance = bounded contextual origin/evolution lineage
Provenance != Source alone
Provenance != truth
Provenance != Authority
Provenance != Confirmation/Evidence
Provenance != Version
Provenance != Decision/rationale
Provenance != Representation
```

Material provenance may record Actor, represented party, Principal/auth context, Authority/delegation basis, source/process/version/time without collapsing those semantics into Provenance.

---

# 13. Acceptance / Assent disposition

Generic cross-domain `Acceptance` / `Assent` is rejected.

```text
invitation accepted
→ Participation response

Responsibility hand-off accepted
→ Responsibility-specific response

proposal accepted/applied
→ proposal/effect-specific response

all applicable parties assent to same terms
→ Agreement

actor permits bounded action/use/exposure
→ Consent
```

A UX label never creates a universal domain type.

---

# 14. AI guardrails

```text
AI inference != established identity
AI inference != Actual
AI inference != human Acknowledgement
AI inference != human Agreement
AI inference != human Consent
AI proposal != human Decision
AI capability != Authority
AI source access != disclosure permission
AI/service action != represented human authorship/will
```

Where AI/service acts for another party, preserve the actual AI/service Actor, represented party and bounded basis where material.

Version hardening adds:

```text
AI proposal/effect binds to a material base state where stale application could matter
material divergence requires re-evaluation rather than silent stale application
Version does not grant AI Authority
```

---

# 15. Product/UI mappings

```text
Occurrence          → This time / This workout / This meeting
Actual              → What happened? / Actual time / Performed
Outcome             → Result / Passed / Partial
Observation         → Weight / Mood / Score / Odometer
Quantity            → 66.4 kg / 5 km / 45 min
Responsibility      → Responsible / Assigned to / Who's handling this?
Participation       → Going / Maybe / Can't go / Attended
Visibility          → Private / Shared with… / free-busy only
Acknowledgement     → Got it / Acknowledge / I've seen the change
Decision            → Choose / Keep / Approve / Reject / Resolve
Agreement           → Agree to terms / Agreed with…
Consent             → Allow / Permit / Share for… / Stop allowing
Representation      → On behalf of… / Done by X for Y / Managed by…
Version             → Version / Revision / Changed since… / Based on version…
Confirmation        → Confirm / Looks correct
Evidence            → Why? / Based on…
Provenance          → Source / Imported from / Corrected by / History
```

`Delegate`, `Represent`, `Approve`, `Accept`, `Agree`, `Allow`, `Share`, `Version`, `Revision` map to the actual owning semantics rather than universal backend types.

---

# 16. Implementation-language guardrails

Do not infer final tables/classes/FKs from this map.

Explicitly not pre-approved:

```text
universal subjects/actors/resources/relationships/participants roots
universal authority/visibility ACL domain roots
universal acknowledgements/acceptances/approvals roots
universal decisions/state-transition root
universal agreements/contracts/consent-permission root
universal representatives/principals/delegations root
universal Version root/table/graph
global material-equivalence enum/rule
mandatory event sourcing/snapshot table for all concepts
one actor_id / principal_id / on_behalf_of_id everywhere
Person.id = Account.id
Account = Principal
User as universal FK
arbitrary JSON replacing typed semantics
```

Domain Authority != technical authorization. Domain Visibility != technical read permission. Domain Representation != authentication impersonation. Domain Version != provider/storage revision. Effective state belongs to the affected concept.

---

# 17. Version / material equivalence

**Status:** CANONICAL — PASS WITH HARDENING; hardenings incorporated; final post-write QA pending.  
**Source:** `concepts/version.md`  
**Validation:** `checkpoints/version-material-equivalence-v0-validation.md`

> **Version is the contextual capability to identify and reference a materially relevant state of a domain target when changes to that state matter for interpretation, applicability, history, concurrency, reconciliation, or downstream action.**

Canonical question:

> **Which materially relevant state of this target is being referred to for this purpose/facet?**

Core separation:

```text
native identity
!= material state
!= Version reference
!= provider/storage revision
```

Canonical hardenings:

```text
materiality is purpose/facet scoped
field/byte/hash change != material change automatically
no field/byte/hash change != semantic equivalence automatically
prior Ack/Confirmation/Decision/Agreement/Consent does not silently carry across material change
non-linear/offline divergent history is valid
Version does not choose canonical truth/current state/winner
Authority/Decision/reconciliation + owning concept establish effective state
AI stale-base proposals/effects require re-evaluation after material divergence
visible projection Version != source Version automatically
historical reconstructibility != indefinite sensitive-payload retention
```

Rejected:

```text
universal Version entity/root/table
global version number semantics
provider ETag/sequence/storage row version as domain truth
mandatory event sourcing
one universal material-equivalence function
```

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
Acknowledgement v0              PASS WITH HARDENING — QA PASS
Generic Acceptance/Assent       REJECTED
Decision v0                     PASS WITH HARDENING — QA PASS
Universal Approval              REJECTED
Universal Reconciliation        REJECTED
Universal EffectiveChange       REJECTED
Agreement / Consent v0          PASS WITH HARDENING — QA PASS
Universal Contract              REJECTED
Universal Consent/Permission    REJECTED
Representation v0               PASS WITH HARDENING — QA PASS
Principal domain primitive      REJECTED
Universal Agent/Representative  REJECTED
Universal Delegation            REJECTED
Impersonation-as-domain-truth    REJECTED
Version v0                      PASS WITH HARDENING — FINAL QA PENDING
Universal Version root/table    REJECTED
```

```text
structural REOPEN              0
unclassified material debt     0
```

---

# 19. Next-selection pressure

Do not continue by roadmap vocabulary order.

After Version post-write QA closure, run a fresh re-score among remaining demonstrated pressure such as:

```text
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
Personal Knowledge generic link layer
```

These are candidates/dependencies, not pre-approved primitives.

---

# 20. Maintenance rule

This file answers:

> **What does the term mean, what does it not mean, what status does it have, and what might a user see?**

Detailed evidence, chronology, ADS owners/triggers, benchmark classifications and persistence pressure remain in concept specs/checkpoints.

Do not rewrite historical evidence for vocabulary uniformity; close old boundaries through downstream amendments and current docs.