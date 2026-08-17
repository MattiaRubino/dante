# Slice F — Relationships / Multi-Actor / Governance v1

**Status:** Local logical candidate — PASS WITH HARDENING, pending remote QA closure  
**Date:** 2026-08-17  
**Workstream:** Logical Model  
**Slice:** F — Relationships / Multi-Actor / Governance

## 1. Scope

This slice maps the accepted Domain semantics around:

- Actor and specific actor roles;
- Collective and Membership;
- Interpersonal Relationship;
- Participation;
- Responsibility;
- Coordination Stewardship;
- Contribution;
- Ownership and Possession boundaries;
- Authority;
- Consent;
- Agreement;
- Visibility;
- Representation / On-Behalf-Of;
- multi-actor shared reality;
- selective disclosure;
- domain governance versus technical authorization.

This slice does not authorize SQL, tables, foreign keys, indexes, migrations, API/backend implementation, AuthN/AuthZ runtime implementation, Principal persistence, OAuth/token implementation, OpenFGA/Cedar/OPA adoption, frontend work, or `main` changes.

## 2. Preferred logical architecture

The preferred candidate is a **Layered Typed Relations & Governance Model**.

```text
ReferenceAddress
        |
        v
SPECIFIC SEMANTIC RELATION FAMILY
        |
        v
Reference Contract
+ relation profile
        |
        +-------------------------------+
        |                               |
        v                               v
DIRECT TYPED RELATION          QUALIFIED MATERIAL RELATION
when semantically complete     when scope/history/governance matters
                                        |
                                        v
                                  LR-02 material record
                                  + ScopedRecordRef
                                  + MaterialStateRef where required
```

Governance remains a separate semantic layer over those relations and records:

```text
Authority / Consent / Visibility / Agreement / Membership / Representation / policy basis
        |
        v
current/effective governance projection
        |
        v
TECHNICAL AUTHORIZATION ADAPTER
Principal + Action + Resource + Context
        |
        v
replaceable enforcement engine
ReBAC / ABAC / capability / policy engine
        |
        v
allow / deny
```

Canonical separation:

```text
DOMAIN GOVERNANCE STATE
!=
TECHNICAL AUTHORIZATION DECISION
```

No authorization engine is accepted as LifeOS ontology authority.

## 3. No universal Relationship root

The following logical shape is rejected:

```text
Relationship
- id
- from
- relation_type
- to
- payload
```

when `relation_type` is expected to own the canonical meaning of every relationship.

LifeOS already has materially distinct relation families whose semantics cannot be recovered safely from one semantic-free edge envelope:

```text
Membership
Participation
Responsibility
Coordination Stewardship
Contribution
Interpersonal Relationship
Ownership
Possession
Authority
Consent
Agreement
Visibility
Representation
```

Canonical rule:

```text
same technical edge shape
!= same semantic relation
```

A physical implementation may reuse edge/reference infrastructure, indexes or storage envelopes, but reverse mapping must always recover the specific semantic owner without relying on an unconstrained `type + payload` escape hatch.

## 4. No RelationRef family

Slice F does not introduce a new universal `RelationRef`.

If a relation is simple and semantically complete, it may remain a direct typed relation.

If the relation itself has material lifecycle, history, scope, governance, provenance, visibility or independent addressability, it may become an LR-02 dependent/contextual record and use the existing addressing contracts:

```text
ScopedRecordRef
MaterialStateRef
```

Therefore:

```text
relation needs addressability
!= RelationRef required

relation needs history
!= universal Relationship entity required
```

This preserves Slice A identity boundaries and Slice D historical state-addressing without creating a second generic identity hierarchy.

## 5. Reference Contract relation profile

The accepted `Reference Contract` is hardened with an optional **relation profile** for specific semantic relation families.

Where applicable, the profile must be able to define:

```text
semantic relation family
endpoint semantic roles
eligible ReferenceAddress families
arity / cardinality
direction
inverse semantics where valid
symmetry where valid
transitivity where valid
perspective / actor-scoped semantics
bounded scope / facet
action / governed effect where relevant
purpose / context where relevant
material-state binding
applicability / effective chronology
establishment / transfer / withdrawal / revocation
unknown / disputed relation semantics
Provenance requirements
Visibility surfaces
governance basis where applicable
current/effective state owner
```

The profile is not a new universal domain superclass. It is validation/representation metadata constraining one already justified semantic relation family.

## 6. Direct versus qualified relation

### Direct typed relation

Use when the semantic fact is complete without independent material relation state.

Example:

```text
Person P17
Membership -> Collective C3
```

may remain compact if no independent scope/history/governance state is material.

### Qualified material relation

Escalate when consequence requires reconstructible relation state.

Conceptually:

```text
Membership M17
- member -> NativeRef(Person P17)
- collective -> NativeRef(Collective C3)
- scope
- applicable/effective period
- provenance
- material state/history
```

Then:

```text
ScopedRecordRef(M17)
MaterialStateRef(M17, S3)
```

may be used where a historical effect must bind to the exact relation state.

Canonical rule:

> Simple cases remain compact; consequential relation state becomes explicitly reconstructible rather than being silently inferred from current endpoints.

## 7. Actor

`Actor` remains contextual agency and does not gain independent identity.

```text
Person may play Actor
Collective may play Actor
system / AI / automation may play Actor where applicable
```

But:

```text
Actor != Person
Actor != Account
Actor != Principal
Actor != Authority
Actor != Responsibility
```

No `ActorRef` wrapper is introduced.

When the concrete action role is known, it remains stronger than generic Actor attribution:

```text
requested_by
performed_by
recorded_by
confirmed_by
proposed_by
approved_by
```

are not replaced by one persisted `actor` edge.

## 8. Collective

Collective remains an accepted scoped native referent and therefore uses Slice A native identity/reference semantics.

```text
Collective -> LR-01 / NativeRef
```

Critical boundaries:

```text
Collective identity != current member set
member action != Collective action automatically
member assent != Collective assent automatically
member Consent != Collective Consent automatically
```

Collective agency, Responsibility, Agreement or other relations require the applicable semantic relation/governance basis; cardinality alone does not manufacture collective state.

## 9. Membership

Logical disposition:

```text
Membership
-> LR-03 specific typed relation
-> LR-02 + ScopedRecordRef when material relation state/history exists
```

`Member` is contextual role language, not native identity.

Mandatory separation:

```text
Membership != Participation
Membership != Responsibility
Membership != Coordination Stewardship
Membership != Authority
Membership != Visibility
Membership != Agreement
Membership != Consent
Membership != technical security-group membership
```

Provider/security group membership may be evidence or a technical projection but is not automatic canonical Membership or Authority.

## 10. Interpersonal Relationship

Logical disposition:

```text
Interpersonal Relationship
-> LR-03 specific Person-to-Person relation family
-> LR-02 + ScopedRecordRef when material state/history/context requires it
```

A bounded relationship vocabulary may include product-relevant kinds such as parent/child, partner, friend, colleague, manager/report, caregiver/cared-for or client/adviser.

The vocabulary is not a universal social-role ontology and does not grant unrelated effects.

```text
mother relation != Visibility
manager relation != Authority
partner relation != Consent
friend relation != Participation
```

No universal symmetry, inverse or transitivity rule is accepted. Those properties belong to the specific relationship kind where justified.

## 11. Participation

Logical disposition:

```text
Participation
-> LR-03
-> LR-02 + ScopedRecordRef when response/history/scope is material
```

Mandatory separation:

```text
invited
!= accepted
!= intended participation
!= Actual participation

Participation
!= Responsibility
!= Contribution
!= Authority
!= Visibility
```

Later Actual participation does not rewrite invitation/response history, and invitation/acceptance does not prove Actual participation.

## 12. Responsibility

Logical disposition:

```text
Responsibility
-> LR-03
-> LR-02 + ScopedRecordRef when transfer/history/scope/governance is material
```

Responsibility owns accountability for ensuring a bounded commitment is handled.

```text
Responsibility
!= requester
!= expected performer
!= Actual performer
!= Coordination Stewardship
!= Authority
!= Visibility
```

A true Collective may bear Responsibility, but several responsible Actors do not automatically form a Collective.

## 13. Coordination Stewardship

Logical disposition:

```text
Coordination Stewardship
-> LR-03
-> LR-02 + ScopedRecordRef when material
```

Stewardship owns the ongoing coordination burden: remembering, monitoring, prompting, synchronizing, escalating and repairing coordination where applicable.

```text
Stewardship
!= Responsibility
!= performer
!= Participation
!= Authority
!= ownership
```

Actual reminder/escalation behavior may be Evidence about Stewardship but does not silently establish or transfer the relation.

## 14. Contribution

Logical disposition:

```text
Contribution
-> LR-03
-> LR-02 + ScopedRecordRef when material attribution/history matters
```

Contribution is materially meaningful **actual** actor input/work in a bounded realized context.

```text
Participation != Contribution
assignment != Contribution
expected performer != Contribution
Provenance != Contribution
credit / merit / ownership != Contribution
```

A contributor may not be the final performer, and attendance/presence alone does not create Contribution.

## 15. Ownership and Possession

Both remain specific contextual relation families and may use the same direct/qualified representation pattern.

```text
Ownership -> LR-03
Possession -> LR-03
```

But:

```text
Ownership != Possession
Ownership != Authority
Ownership != Visibility
Possession != Allocation
Possession != Actual use
```

Shared physical edge infrastructure is allowed; shared semantic ownership is not implied.

## 16. Authority

Authority is a specific governance capability about who/what may legitimately make a bounded domain effect effective for a defined target/scope/action/context/basis.

Logical disposition:

```text
explicit/material Authority relation
-> LR-03
-> LR-02 + ScopedRecordRef where consequential

governing rule/policy/specification
-> LR-05 where applicable

Effective Authority
-> LR-08 derived/effective projection where appropriate
```

No universal materialization of every effective permission is required.

Critical boundaries:

```text
Authority != Actor
Authority != Responsibility
Authority != Visibility
Authority != Consent
Authority != technical authorization
Authority != truth
Authority != Ownership
```

A consequential historical action must be able to reconstruct the Authority basis applicable at action/effect time where consequence requires it.

## 17. Consent

Consent is actor-scoped bounded permission semantics and is more strongly materialized when used as a consequential governance basis.

Preferred disposition:

```text
Consent
-> LR-03 semantic relation
-> LR-02 material contextual record when consequential
-> ScopedRecordRef
-> MaterialStateRef where exact state/version applicability matters
```

The representation must be able to distinguish, where material:

```text
consent-giver
action / use / exposure
target / subject
scope
purpose
context
applicable period
material target / terms state
withdrawal / revocation / supersession
provenance
```

Mandatory separation:

```text
Consent != Visibility
Consent != Authority
Consent != Agreement
Consent != Decision
Consent != technical Permission
```

Withdrawal changes future applicability; it does not silently erase truthful historical consented actions/disclosures.

## 18. Agreement

Agreement is the strongest current pressure against reducing every relation to a binary edge.

A material Agreement is naturally n-ary and terms/version-bound.

Preferred disposition:

```text
Agreement
-> LR-02 contextual n-ary semantic record
-> ScopedRecordRef

terms / materially specific shared proposition
-> MaterialStateRef where material

party assent relations
-> typed relations bound to the same material terms state
```

Conceptually:

```text
Agreement A7
terms -> MaterialStateRef(Terms, T3)
party Anna -> assent to T3
party Luca -> assent to T3
party Marco -> assent to T3
```

Rejected representation:

```text
Anna agreed_with Luca
Anna agreed_with Marco
Luca agreed_with Marco
```

because pairwise edges do not prove that all parties assented to the same materially specific terms/version.

Material change from terms T3 to T4 requires renewed applicable assent; historical Agreement to T3 remains reconstructible.

A Collective may itself be an Agreement party under applicable governance, without rewriting every member as a personal party.

## 19. Visibility

Visibility is bounded information-exposure capability, not object-wide ACL semantics.

Logical disposition:

```text
explicit visibility/share relation
-> LR-03
-> LR-02 where material

visibility policy/specification
-> LR-05

Effective Visibility
-> LR-08
```

Visibility may independently govern:

```text
endpoint existence
representation/projection
relation existence
relation kind
relation current state
relation history
supporting Evidence / Provenance
private source cause
```

Canonical rule:

```text
Visibility(endpoint A)
+
Visibility(endpoint B)
!= Visibility(relation A<->B)
```

Likewise:

```text
Visibility(derived projection)
!= Visibility(private source)
```

This permits one shared reality with actor-scoped/selective disclosure instead of per-user duplication.

## 20. Representation / On-Behalf-Of

Representation is action-scoped attribution preserving actual Actor and represented party separately.

Logical disposition:

```text
Representation
-> LR-03 action-scoped typed relation
-> LR-02 + ScopedRecordRef when consequential/history-bearing
```

Where material, preserve separately:

```text
actual Actor
represented party
bounded action
target / MaterialStateRef
applicable Authority/delegation/policy/Consent basis
Principal / Account context where useful
resulting effect
```

Mandatory separation:

```text
Representation != Authority
Representation != Subject / beneficiary
Representation != Responsibility
Representation != Principal
Representation != represented-party personal will
```

`Luca acted for Anna` must not become `Anna acted`.

## 21. Domain governance versus technical authorization

This boundary is mandatory.

Domain governance answers semantic questions such as:

```text
Who may legitimately make effect E effective?
Who consented to use/exposure U?
What may recipient R be exposed to?
Which parties mutually assented to terms T?
Who currently belongs to Collective C?
Who actually acted for whom?
```

Technical authorization answers a runtime security question such as:

```text
May Principal P perform Action A on Resource R in Context C now?
```

Therefore:

```text
technical ALLOW != proof of Domain Authority
technical DENY != proof that Domain Authority is absent
```

A technical deny may arise from device posture, session policy, emergency lock, account state, security boundary or other runtime constraint while legitimate Domain Authority still exists.

A technical allow may be misconfigured or broader than legitimate Domain Authority and therefore must not manufacture canonical governance truth.

## 22. Authorization adapter / projection

Future runtime authorization may project canonical LifeOS state into a technical enforcement representation.

Possible target mechanisms include:

```text
Zanzibar/OpenFGA-style ReBAC
Cedar-style principal/action/resource/context policy
OPA/Rego
custom hybrid policy engine
bounded capabilities/delegation credentials
```

The adapter may consume:

```text
Principal/security context
NativeRef / ScopedRecordRef target
specific domain relations
effective Authority/Visibility projections
Consent/Agreement applicability
Collective/Membership state
MaterialStateRefs
runtime request context
```

But the policy engine remains replaceable infrastructure.

```text
authorization tuple != canonical Membership automatically
policy decision != canonical Authority
policy cache != source truth
```

## 23. Delayed effect and stale authorization

Consequential delayed/queued operations create a time-of-check/time-of-use pressure:

```text
T1 Authority valid
T2 runtime authorization ALLOW
T3 Authority revoked
T4 queued effect executes
```

LifeOS must not assume the T2 allow remains valid forever.

Logical requirement:

> A delayed consequential effect must either revalidate the materially applicable governance basis immediately before effect or carry an explicitly valid immutable authorization/effect binding whose semantics permit delayed execution.

The Physical Model/runtime chooses the mechanism. Slice F only requires that historical truth and current governance do not collapse.

## 24. Unknown, conflict and correction

For relation/governance families:

```text
unknown relation
!= explicit absence

no applicable grant found
!= explicit prohibition

claimed Authority
!= established Authority

observed behavior
!= canonical relation automatically

newest assertion
!= universal winner
```

Conflicting assertions may remain unresolved and must be reconciled through applicable Evidence/Provenance/Decision/Authority/Reconciliation semantics rather than silent overwrite.

## 25. AI / automation boundary

AI may:

- infer candidate relations as proposals;
- use authorized private context for bounded derived projections;
- evaluate policy/rules;
- propose governance changes;
- act under explicit Representation/Authority where allowed;
- explain decisions using only visible basis.

AI must not:

```text
infer relationship -> silently establish it
infer Membership -> Authority
infer Interpersonal Relationship -> Visibility
ranking/confidence -> Authority
technical credential -> domain legitimacy
private reasoning access -> disclosure permission
```

## 26. Accepted logical dispositions

```text
Actor
-> contextual role, no ActorRef

Collective
-> LR-01 / NativeRef

Membership
-> LR-03
-> LR-02 + ScopedRecordRef when material

Interpersonal Relationship
-> LR-03
-> LR-02 + ScopedRecordRef when material

Participation
-> LR-03
-> LR-02 + ScopedRecordRef when material

Responsibility
-> LR-03
-> LR-02 + ScopedRecordRef when material

Coordination Stewardship
-> LR-03
-> LR-02 + ScopedRecordRef when material

Contribution
-> LR-03
-> LR-02 + ScopedRecordRef when material

Ownership
-> LR-03

Possession
-> LR-03

Authority
-> LR-03 / bounded LR-02
-> LR-05 governing basis where applicable
-> LR-08 Effective Authority

Consent
-> LR-03
-> LR-02 + ScopedRecordRef
-> MaterialStateRef where material

Agreement
-> LR-02 n-ary contextual record
-> party assent typed relations
-> MaterialStateRef for materially specific terms

Visibility
-> LR-03 / bounded LR-02
-> LR-05 policy
-> LR-08 Effective Visibility

Representation
-> LR-03
-> LR-02 + ScopedRecordRef when material

technical authorization representation
-> downstream projection / adapter only
```

## 27. Slice F hardenings

```text
F-H01  No universal semantic Relationship/Edge root.
F-H02  No universal RelationRef; use existing ScopedRecordRef/MaterialStateRef when material.
F-H03  Reference Contract gains relation-profile constraints without becoming ontology.
F-H04  Direct relation vs qualified material relation is consequence-sensitive.
F-H05  Actor remains role/capability; specific actor role wins over generic actor edge.
F-H06  Membership never implies Participation/Authority/Visibility/Consent/Agreement.
F-H07  Interpersonal Relationship does not grant Authority/Visibility/Consent.
F-H08  Responsibility, Stewardship, performer and Participation remain independently representable.
F-H09  Participation != Contribution.
F-H10  Ownership != Possession != Authority/Visibility.
F-H11  Authority may be explicit or derived, but historical action-time basis must be reconstructible where consequential.
F-H12  Consent is scope/purpose/target/time/material-state sensitive.
F-H13  Agreement is materially terms/version-bound and may be n-ary.
F-H14  Collective Agreement/action does not rewrite member personal state.
F-H15  Visibility can govern relation/projection/source independently from endpoint visibility.
F-H16  Representation preserves actual Actor separately from represented party and Authority basis.
F-H17  Domain governance != technical AuthZ allow/deny.
F-H18  ReBAC/ABAC/capability systems are replaceable enforcement/projection candidates, not ontology authority.
F-H19  Delayed consequential effects must not rely indefinitely on stale authorization checks.
F-H20  Unknown/conflicting governance state remains representable; no newest/provider/AI-confidence winner.
```

## 28. Core invariants

1. Specific semantic relation owner beats generic edge convenience.
2. Technical edge reuse does not create semantic inheritance.
3. Same endpoints can participate in multiple independent relation families simultaneously.
4. Relation addressability/history uses existing logical address/state contracts rather than new universal identity.
5. Direct/simple relation representation remains allowed.
6. Material relation state becomes reconstructible at consequence threshold.
7. Collective identity remains independent from exact member set.
8. Membership grants neither Authority nor Visibility automatically.
9. Relationship labels do not manufacture governance powers.
10. Responsibility, Stewardship, Participation, performer and Contribution do not collapse.
11. Authority, Consent, Visibility and Agreement remain different semantic families.
12. Agreement is bound to materially specific shared terms/version.
13. Visibility of endpoints does not imply visibility of their relationship.
14. Visibility of a derived projection does not imply visibility of its private source.
15. Representation does not rewrite actual Actor identity or manufacture Authority.
16. Current governance state does not rewrite historical action-time governance truth.
17. Technical authorization decision does not become canonical domain governance.
18. Runtime policy engine remains replaceable.
19. Delayed effects must handle governance changes between check and effect.
20. No SQL/API/runtime technology is selected by this slice.

## 29. Reverse mapping

The preferred logical candidate maps unambiguously back to accepted Domain semantics:

```text
Collective NativeRef              -> Collective
member-to-Collective relation     -> Membership
Person-to-Person bounded relation -> Interpersonal Relationship
involvement relation              -> Participation
accountability relation           -> Responsibility
coordination-burden relation      -> Coordination Stewardship
actual meaningful input relation  -> Contribution
owner relation                    -> Ownership
physical holder relation          -> Possession
governance-effect capability      -> Authority
bounded actor permission          -> Consent
shared-terms assent record        -> Agreement
information exposure capability   -> Visibility
actual-Actor/represented-party    -> Representation
runtime allow/deny                -> technical authorization only
```

No semantic-free fallback is required.

## 30. Verdict

```text
SLICE F — RELATIONSHIPS / MULTI-ACTOR / GOVERNANCE

PREFERRED
Layered Typed Relations & Governance Model

LOCAL VERDICT
PASS WITH HARDENING

DOMAIN REOPEN REQUIRED        0
NEW DOMAIN OWNER REQUIRED     0
A+B+C+D+E REGRESSION FAILURE  0
LOGICAL STRUCTURAL BLOCKER    0

TECHNOLOGY / MECHANISM
RETAIN + HARDEN

REMOTE QA
PENDING
```

Canonical activation still requires exact remote Git QA and a separately gated closure record.