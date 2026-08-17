<!-- LIFEOS-CANONICAL-CONTINUATION document="representation-framework-v1.md" follows="representation-framework-v1-part-7.md" -->
> **Canonical continuation of the single Logical Representation Framework v1 document.** Earlier representation roles remain authoritative. This continuation records Slice F — Relationships / Multi-Actor / Governance hardening only.

# Slice F representation hardening

## RF-H01 — LR-03 remains specific semantic association, not universal edge ontology

`LR-03 qualified typed association / relation` may represent multiple accepted semantic owners, including:

```text
Membership
Interpersonal Relationship
Participation
Responsibility
Coordination Stewardship
Contribution
Ownership
Possession
Authority
Consent
Visibility
Representation
Resource Allocation / Capacity Claim from Slice E
```

Canonical rule:

```text
same LR-03 representation role
!= same semantic relation owner
```

Forbidden logical shape:

```text
Relationship
  id
  from
  type
  to
  payload
```

when the generic row becomes the canonical semantic owner or fallback for relations whose stronger meaning is known.

Shared physical edge/reference infrastructure remains possible only if reverse mapping to the specific semantic family stays deterministic and enforceable.

## RF-H02 — No universal RelationRef

Slice F adds no new ReferenceAddress family for relationships.

A simple relation may remain direct and unaddressed as an independent record.

A materially stateful/history-bearing relation may escalate to:

```text
LR-02 dependent/contextual record
+ ScopedRecordRef
+ MaterialStateRef where exact material state is consequential
```

Therefore:

```text
addressable relation
!= RelationRef required

versioned relation
!= relation-native identity hierarchy required
```

`ScopedRecordRef` and `MaterialStateRef` remain sufficient logical abstractions for current relation/governance pressure.

## RF-H03 — Reference Contract gains a relation profile

A Reference Contract may carry relation-profile constraints when it owns or constrains a specific semantic relation family.

Where applicable, the profile may define:

```text
semantic family
endpoint roles
eligible target/reference families
arity / cardinality
direction
inverse semantics
symmetry
transitivity
perspective / actor-scoped meaning
bounded scope / facet
action / governed effect
purpose / context
material-state binding
applicability/effective chronology
establishment / transfer / withdrawal / revocation
unknown/disputed-state rules
Provenance requirements
Visibility surfaces
governance basis
```

This profile is validation/representation metadata, not a new semantic superclass.

## RF-H04 — Direct vs qualified relation is consequence-sensitive

The framework permits two forms without semantic contradiction:

```text
DIRECT TYPED RELATION
when relation meaning is complete and no independent material lifecycle/history is needed
```

and:

```text
QUALIFIED MATERIAL RELATION
when scope/history/governance/provenance/visibility/addressability is material
```

Escalation principle:

```text
simple relation
        ↓ consequence threshold
LR-02 material relation record
+ ScopedRecordRef
+ MaterialStateRef where required
```

No blanket rule forces every M:N relation into a first-class domain record.

## RF-H05 — Same endpoints may bear multiple independent relation families

The framework must allow, simultaneously:

```text
Person Anna -> Membership -> Collective H
Person Anna -> Participation -> Event E
Person Anna -> Responsibility -> Activity A
Person Anna -> Coordination Stewardship -> Context C
Person Anna -> Authority -> bounded effect X
Person Anna -> Visibility -> Projection P
```

without attempting to merge those rows/facts because endpoint pairs happen to repeat.

Canonical rule:

```text
same source/target pair
!= semantic relation equivalence
```

## RF-H06 — Actor remains contextual role/capability

`Actor` does not receive LR-01 identity or a wrapper ReferenceAddress.

Use the most specific actor-role relation where known:

```text
performed_by
requested_by
recorded_by
confirmed_by
proposed_by
```

Generic Actor semantics may support eligibility/common query reasoning but must not erase the concrete relation.

## RF-H07 — Agreement requires n-ary/material-state-aware representation

Agreement pressure exceeds a binary edge model.

Preferred representation:

```text
Agreement
-> LR-02 contextual semantic record
-> ScopedRecordRef

material terms
-> MaterialStateRef

party assent
-> typed relations bound to same terms state
```

Pairwise `agreed_with` edges are insufficient evidence of common assent to one materially specific terms/version state.

Material amendment requires renewed applicable assent; prior state remains reconstructible.

## RF-H08 — Consent uses stronger material binding when consequential

Consent may use LR-03 relation semantics, but consequence can require an LR-02 material record with exact state binding.

Required dimensions where material:

```text
consent-giver
action/use/exposure
target/subject
scope
purpose
context
applicable period
material target/terms state
withdrawal/revocation/supersession
```

A generic boolean `allowed` or a generic permission edge cannot replace these semantics.

## RF-H09 — Authority may be explicit or derived

Authority can appear as:

```text
explicit/material bounded relation
-> LR-03 / LR-02

policy/specification basis
-> LR-05

Effective Authority
-> LR-08
```

The framework must not require materialized per-action permission rows for every derived authority consequence.

However, when a consequential effect occurred, its materially applicable Authority basis must remain reconstructible where required by WD-03.

## RF-H10 — Visibility is projection/relation/source scoped

Visibility is not limited to whole-object ACL semantics.

The representation must permit independent governance of:

```text
object/endpoint representation
relationship existence
relationship kind
relationship current state
relationship history
supporting Evidence / Provenance
derived projection
private source
```

Canonical rules:

```text
Visibility(endpoint A) + Visibility(endpoint B)
!= Visibility(relation A<->B)

Visibility(projection)
!= Visibility(source)
```

The same shared canonical reality therefore does not require per-recipient object duplication.

## RF-H11 — Representation preserves actual Actor and represented party

For action-scoped Representation/on-behalf-of:

```text
actual Actor
represented party
bounded action
applicable Authority/delegation/policy/Consent basis
```

remain independently representable.

```text
represented party
!= actual Actor automatically

Representation
!= Authority automatically
```

Principal/Account runtime identity remains a separate security context.

## RF-H12 — Domain governance and technical authorization are separate representation layers

Canonical domain state may be projected into a technical authorization request/model.

```text
LifeOS semantic governance state
        ↓ projection
Principal + Action + Resource + Context
        ↓
ReBAC / ABAC / capability / policy engine
        ↓
allow / deny
```

The reverse is not identity:

```text
allow != Authority

deny != established absence of Authority

authorization tuple != canonical domain relation automatically
```

Technical authorization artifacts are downstream security representations unless separately justified as domain evidence/history.

## RF-H13 — Authorization projection is replaceable

The Logical Model does not select:

```text
OpenFGA
Zanzibar-derived service
Cedar
OPA/Rego
custom policy engine
capability credentials
```

Any future choice must preserve:

- semantic owner separation;
- Principal != Actor;
- current/historical governance distinction;
- material-state binding;
- selective Visibility;
- no tuple/policy store as universal domain source truth.

## RF-H14 — Delayed effects require governance-time semantics

A technical authorization check cannot float indefinitely with stale governance state.

For consequential delayed/queued effects, representation/runtime must support one of:

```text
revalidation near effect time
OR
explicit immutable authorization/effect binding with valid delayed-execution semantics
```

Exact implementation is Physical Model/runtime work.

The logical invariant is:

```text
authorization decision at T1
!= automatic permanent authority at T2
```

## RF-H15 — Unknown/conflicting relation state is representable

Relation/governance representations must preserve:

```text
unknown
unresolved
conflicting assertion
explicit absence/prohibition
withdrawn/revoked prior state
```

as distinct where materially meaningful.

No generic latest-write/provider/creator/manager/AI-confidence winner is introduced.

## RF-H16 — Technical audit != domain history automatically

Policy-engine decision logs, token claims and authorization tuples may be useful security audit evidence.

They do not automatically replace:

```text
Provenance
MaterialStateRef
historical Authority
Consent state
Agreement terms state
Representation attribution
```

The framework may link security audit evidence to domain history without conflating their semantic ownership.

## Slice F representation verdict

```text
ReferenceAddress                  RETAIN
NativeRef                         RETAIN
ScopedRecordRef                   RETAIN + RELATION USE
MaterialStateRef                  RETAIN + GOVERNANCE USE
Reference Contract                RETAIN + RELATION PROFILE
LR-02 material contextual record  RETAIN
LR-03 qualified typed relation    RETAIN + HARDEN
LR-05 typed policy/specification  RETAIN
LR-08 derived/effective projection RETAIN + GOVERNANCE USE
LR-13 specialist boundary         RETAIN

universal Relationship root       REJECT
universal RelationRef             REJECT
universal Permission root         REJECT
ReBAC tuple ontology              REJECT
ABAC policy ontology              REJECT
universal capability ledger       REJECT
```

No new universal representation role or ReferenceAddress family is introduced by Slice F.