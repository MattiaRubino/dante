# LifeOS Logical Model — Slice A Identity / Reference v1

**Status:** Accepted candidate — activation conditional on Slice-A remote QA  
**Date:** 2026-08-17  
**Slice:** A — Identity / Reference  
**Scope:** logical identity/addressability/reference contract only; no SQL/API/runtime implementation

---

## 1. Decision summary

LifeOS adopts a **Layered Typed Identity & Reference Model** for the Logical Model.

This is a LifeOS-specific synthesis, not a copy of any external product model.

Canonical logical separation:

```text
NATIVE IDENTITY
!= TECHNICAL ADDRESS / REFERENCE
!= CONTEXTUAL ROLE / RELATION MEANING
!= PROVIDER / EXTERNAL IDENTITY
!= ACCOUNT / PRINCIPAL IDENTITY
!= IDENTITY RECONCILIATION STATE
!= MATERIAL VERSION / STATE REFERENCE
!= DISCLOSURE / PUBLIC HANDLE
```

The model exists to let independently meaningful native referents participate in shared cross-domain references without creating a universal semantic `Entity`, `Thing`, `Party`, `Subject`, `Actor` or `Resource` root.

---

## 2. In-scope Domain owners and boundaries

Primary native identity pressure:

```text
Person
Living Referent
Asset
Place
Content Artifact
Collective
```

Contextual-role pressure:

```text
Actor
Subject
Resource
```

External/security pressure:

```text
Account
Principal
provider/source identities
external records/IDs
```

Carried-forward invariants include:

```text
Person != Account != Actor
Person != Subject
Person != Resource
Person != Living Referent != Asset
Asset != Resource
Place != Asset
Collective != current member set
Content Artifact != file/blob/provider representation
provider ID != LifeOS canonical identity
technical registry != semantic Entity / Thing root
technical reference != universal semantic Relationship
correction != silent overwrite
current != historical
unknown/unresolved != false/absent
```

---

## 3. Core logical vocabulary

### 3.1 Native identity

A **native identity** is the stable logical identity of an independently justified Domain referent.

Examples under current Domain Atlas:

```text
Person P17
Asset A9
Place PL4
Living Referent L2
Content Artifact C8
Collective C3
```

Native identity belongs to the Domain owner, not to the technical reference mechanism.

Canonical rule:

> A shared reference mechanism never creates native identity for a concept that does not independently justify it.

---

### 3.2 NativeRef

`NativeRef` is the logical concept of **technical addressability of an already justified native identity**.

Conceptual shape only:

```text
NativeRef
- owner kind / native identity family
- opaque native identity key
```

The shape above is logical, not a mandated serialized/SQL representation.

Canonical rules:

```text
NativeRef != Entity
NativeRef != Thing
NativeRef != Domain superclass
NativeRef != Actor
NativeRef != Subject
NativeRef != Resource
NativeRef != Relationship
NativeRef != Account
NativeRef != Principal
NativeRef != ExternalRef
NativeRef != Version
```

`NativeRef` answers only:

> Which independently justified LifeOS native identity is being addressed?

It does **not** answer:

> Why is this referent present in this context?

That meaning belongs to the containing Reference Contract / typed relation.

---

### 3.3 Reference Contract

Every material reference slot or relation family carries a **Reference Contract**.

A Reference Contract defines at least, where applicable:

```text
semantic meaning / role
eligible target families
cardinality
source/target direction or role
whether unresolved target is allowed
history/materiality requirements
visibility/authority implications owned elsewhere
specialist/extension target rules
```

Example:

```text
Observation.subject
semantic meaning: Subject aboutness
allowed targets: native referents eligible to be Subject in this containing concept
value: NativeRef(Person, P17)
```

This means:

```text
referent identity = Person P17
contextual semantic = Subject
```

It does **not** mean:

```text
Person = Subject
```

Another example:

```text
Activity.expected_performer
semantic meaning: expected performer
eligible targets: actor-capable native/system identities allowed by Activity semantics
value: NativeRef(Person, P17)
```

The exact typed relation remains more precise than a generic Actor edge.

---

### 3.4 Role-target references do not manufacture wrapper identity

Canonical rule:

```text
Person P17 as Subject
!= Subject S99 -> Person P17

Person P17 as Actor/recorder
!= Actor A99 -> Person P17

Asset A9 as Resource candidate
!= Resource R99 -> Asset A9
```

Actor, Subject and Resource retain their accepted role/capability semantics.

No wrapper identity is created solely to make references uniform.

---

### 3.5 Not every valid role target must be a NativeRef

This is a critical hardening.

Some role/capability semantics may validly target things that do not independently justify native kernel identity.

Resource pressure includes potential cases such as:

```text
service
pool
fungible supply
capacity
specialist provider representation
```

Therefore:

```text
role target eligibility
!= universal requirement for NativeRef
```

Conceptual target space may be:

```text
RoleTarget
= NativeRef
OR bounded dependent/value/service/pool/specialist representation
```

according to the containing Reference Contract.

This prevents `everything that can be referenced -> native Entity` inflation.

---

## 4. Native identity properties

### 4.1 Stable logical identity

For a continuing native referent, ordinary changes do not manufacture new native identity.

Examples:

```text
Person changes Account/provider/contact representation
-> same Person

Asset changes owner/possessor/location
-> same Asset

Living Referent changes caregiver/location/name
-> same Living Referent

Place address/coordinates corrected
-> same Place if spatial referent is unchanged

Collective ordinary membership changes
-> same Collective where continuity remains truthful

Content Artifact moves provider/storage
-> may remain same Artifact where artifact identity is materially continuous
```

---

### 4.2 Opaque identity key

Consumers must treat the native identity key as opaque.

Forbidden:

```text
parse prefix to determine semantic owner
infer creation time from encoded bits unless separately contracted
infer tenant/person/provider semantics from raw key format
couple logic to current serialization
```

Owner/type must be deterministically recoverable by the logical reference contract/representation, not by undocumented parsing convention.

---

### 4.3 Non-reuse

Once a native identity key has represented one native referent, it must not later be reassigned to a different native referent.

This applies even if the earlier identity becomes inactive, merged, superseded, deleted from ordinary product surfaces or retained only for historical/legal reasons.

Retention/anonymization policy may change what information remains, but must not make one historical identity key silently mean a different referent.

---

### 4.4 Alias/name/provider ID are not native identity

```text
name
email
phone
username
provider object ID
provider URL
serial/VIN/microchip
address/coordinates
file ID
calendar ID
contact resource name
```

may be important identifiers/evidence but do not automatically become LifeOS native identity.

---

## 5. Account / Principal / Person boundary

Logical model preserves:

```text
Person
!= Account
!= Principal
!= provider security identity
```

Conceptual shape:

```text
Person P17
    ↓ explicit linkage/reconciliation
Account A4
    ↓ authentication/security binding
Principal / provider identities
```

A Person may:

- exist before any Account;
- never have an Account;
- have Account/provider representation changed;
- remain historically attributable after access changes where policy permits.

Account creation does not automatically create a new Person if the represented human already exists.

Account deletion/provider migration does not automatically delete/replace Person identity.

---

## 6. ExternalRef — provider/source identity

External/provider identities are represented logically in a separate scoped identity space.

Conceptual minimum:

```text
ExternalRef
- provider / source system
- source realm / tenant / account / integration instance where material
- provider object/resource type where material
- opaque external identifier
- provider version/revision when identity mapping depends on it
```

Canonical rule:

```text
ExternalRef != NativeRef
```

A safe external uniqueness scope is established from the provider contract; LifeOS must not assume `provider + external_id` is globally sufficient if tenant/account/source scope is material.

Examples:

```text
OIDC issuer + subject
SCIM service provider + id
Google source type + source id
cloud account/tenant/resource scope
calendar account + event id
```

Exact adapter fields remain provider-specific.

---

## 7. Provider mapping / reconciliation

Provider/source mappings are explicit logical state.

Conceptual relation:

```text
ExternalRef
    ↓ Mapping / Reconciliation
NativeRef
```

Mapping may carry, where material:

```text
candidate / proposed / accepted / rejected / superseded state
confidence or evidence basis
Provenance
actor/authority attribution
recorded/accepted/effective time
correction/revocation history
```

No universal latest-write/provider/confidence winner is accepted.

### 7.1 Unresolved mapping is valid

```text
external record exists
+
LifeOS native target uncertain
```

may remain unresolved.

LifeOS must not manufacture:

```text
current user as default Person
same-email automatic Person merge
generic Entity target
provider object as canonical identity
```

simply to obtain a non-null target.

---

## 8. Identity reconciliation: merge / split / correction

Identity reconciliation is distinct from native identity itself.

### 8.1 Duplicate recognition

Example:

```text
Person P17
Person P32
```

Later evidence supports:

```text
P17 and P32 represent the same human
```

The logical result is not required to destroy P32 or rewrite every historical reference as if P32 never existed.

Preferred logical semantics:

```text
Identity Reconciliation R1
- source identities: P17, P32
- current resolution/canonical target: P17
- basis / Evidence / Provenance
- accepted at T
- authority/decision basis where material
- correction/revocation state
```

Current resolution may make queries treat P32 as redirected/resolved to P17 where appropriate while preserving historical addressability.

### 8.2 Wrong merge / unmerge

If later evidence shows R1 was wrong:

```text
R1 corrected/revoked
```

Historical records can again distinguish the original referents without reconstructing meaning from destructive bulk rewrites.

Canonical requirement:

> A materially consequential identity merge must be correctable without pretending LifeOS always knew the final identity resolution.

### 8.3 Split / conflation

One prior native identity may later be discovered to have conflated multiple real referents.

The logical model must preserve:

- prior historical attribution;
- correction basis;
- newly separated native identities where justified;
- unresolved assignment where old records cannot be truthfully redistributed.

No silent rewriting of uncertain history is permitted.

---

## 9. Identity vs material Version/state

Native identity answers:

> Which continuing referent is this?

Version/material-state reference answers:

> Which materially relevant state/version of that referent is being addressed?

Therefore:

```text
NativeRef != VersionRef / material state reference
```

A Decision/Evidence/Provenance chain may need to reference the state known at T without creating a new native identity for every state change.

Exact version-addressing mechanism belongs primarily to Slice D, but Slice A reserves the distinction.

---

## 10. Identity vs alias / human-friendly handle

Human-friendly names/keys may change or be reused while native identity remains stable.

Possible future/API constructs may include:

```text
alias
slug
short key
external handle
context-scoped display reference
redirect
```

None automatically replaces NativeRef identity.

The Logical Model does not require users to see native IDs.

---

## 11. Privacy / selective correlation

Identity linkage itself may be sensitive.

Canonical rules:

```text
referenceability != Visibility
identity equality != disclosure permission
internal canonical identity != universal public/API correlation handle
seeing both referents != seeing their identity-linkage/relation automatically
AI ability to resolve identity != permission to expose linkage
```

LifeOS may internally know that two contexts concern Person P17 while authorized product/API surfaces expose context-scoped handles or omit the linkage entirely.

This does not create duplicate Person identity.

Exact policy/enforcement remains Slice F / security-stage work.

---

## 12. Shared reality / multi-actor

One shared native referent should not normally be duplicated per actor merely because several actors have different views, access, notes or provider representations.

Conceptual pattern:

```text
Native Person P17

Actor A private contact source
Actor B shared Event participant context
Actor C caregiver context
```

Possible actor-scoped state/visibility does not create P17-A, P17-B and P17-C canonical Person copies.

At the same time, identity resolution across those contexts remains visibility-sensitive.

---

## 13. Specialist and product boundaries

The common reference contract does not promote every product/specialist object to a kernel native referent.

Examples:

```text
financial Transaction
inventory Movement
clinical specialist record
Project / Program profile
Inbox item
provider-specific object
```

may have application/specialist identity and still participate in bounded references without changing Domain Atlas native-owner classification.

A later slice may prove additional native identity under its own evidence; Slice A must permit extension without rewriting existing native identities.

---

## 14. Candidate comparison

### Candidate A — universal generic object/entity reference

Shape:

```text
Object/Entity
- id
- type
- properties

any relation -> any Object
```

**Strength:** operationally flexible.

**Failure:** creates semantic universal root, weakens eligibility, encourages generic relations/property fallback, blurs native/product/provider identity.

**Verdict:** `REJECTED LOGICAL CANDIDATE`.

---

### Candidate B — only role/owner-specific reference families

Shape:

```text
PersonRef
AssetRef
PlaceRef
...
SubjectTarget union
ActorTarget union
ResourceTarget union
...
```

**Strengths:** strongest direct referential semantics; natural owner-specific constraints; no universal root.

**Costs/pressure:** repeated heterogeneous-addressability logic; repeated provider/provenance/reconciliation handling; expansion of unions/reference families as native owners grow; cross-domain infrastructure must repeatedly rediscover common addressability.

**Verdict:** `VIABLE STRONG ALTERNATIVE`, not selected.

Candidate B remains a valid physical implementation ingredient and a reopen/retest comparator if the shared logical address layer later proves harmful.

---

### Candidate C — mandatory global identity registry as logical root

Shape:

```text
IdentityRegistry row
-> every object/referent
```

**Strength:** uniform FK/addressability/history hooks.

**Failure if made logically mandatory:** risks converting representation convenience into universal semantic object identity and forcing native identity onto role/value/dependent/provider objects.

**Verdict:** `REJECTED AS LOGICAL REQUIREMENT`.

A narrow technical anchor/registry remains a **physical candidate** if it preserves the Slice-A contract.

---

### Candidate D — Layered Typed Identity & Reference Model

Shape:

```text
native owner identity
        ↓
logical NativeRef addressability
        ↓
slot/relation-specific Reference Contract

ExternalRef / Account / Principal
remain separate scoped identity spaces

Reconciliation/history
links identities without destructive semantic collapse
```

**Strengths:** preserves Domain ownership, supports cross-domain referencing, allows typed target constraints, supports provider migration/reconciliation/history, keeps privacy distinction, permits multiple physical implementations.

**Hardening:** NativeRef is addressability only; not all role targets require NativeRef; identity key is opaque/non-reused; reconciliation is separate/reversible; identity vs Version/public handle remains distinct.

**Verdict:** `SELECTED — PASS WITH HARDENING`, activation conditional on remote Slice-A QA.

---

## 15. Mutation / destructive tests

```text
MUT-A01 remove owner/type information
-> FAIL: reference target semantics cannot be recovered reliably

MUT-A02 remove Reference Contract
-> FAIL: heterogeneous target becomes unconstrained any-object relation

MUT-A03 treat NativeRef as Entity/Thing
-> FAIL: violates Domain/ADR-007 universal-root prohibition

MUT-A04 provider ID becomes NativeRef
-> FAIL: scoped/mutable/provider identity contaminates canonical identity

MUT-A05 Person ID = Account ID
-> FAIL: external/non-account Person and account lifecycle break

MUT-A06 delete obsolete identity on merge
-> FAIL: wrong-merge recovery/history/external references break

MUT-A07 rewrite all historical references after reconciliation
-> FAIL: fabricates that final identity resolution was always known

MUT-A08 infer type from encoded ID prefix only
-> FAIL: format migration becomes semantic migration

MUT-A09 wrapper Actor/Subject/Resource identities
-> FAIL: duplicate identity and synchronization without domain truth

MUT-A10 duplicate native referent per user
-> FAIL: shared canonical reality lost

MUT-A11 expose internal identity globally
-> FAIL: privacy/correlation boundary lost

MUT-A12 force every Resource provider to NativeRef
-> FAIL: supply/pool/service/value cases become false native identities
```

Mutation verdict: **PASS** for selected candidate with listed hardenings.

---

## 16. Counterfactual tests

Selected candidate distinguishes:

```text
existing Person gains Account
!= new Person

same Asset changes possessor
!= replacement Asset

same Living Referent changes caregiver
!= replacement organism

same Content Artifact provider migration
!= independent fork/new artifact identity

same Place address correction
!= genuinely different Place

provider record correction
!= new provider object

possible duplicate
!= accepted duplicate/equivalence

accepted duplicate/equivalence
!= historically always one representation

identity equality internally known
!= authorization to disclose linkage

Subject = Person P17
!= Actor = Person P17

Resource candidate
!= allocation
!= actual use
```

Counterfactual verdict: **PASS**.

---

## 17. Product Reality pressure

### Photography / equipment / external event

```text
Asset camera/lens/filter identities
+
external astronomical event
+
Possibility
+
Activity Resource Requirements
+
typed candidate references
```

No Resource wrapper/native-identity inflation is required.

### Persistent health-relevant context -> later diet request

```text
Person P1
+
health/specialist records where authorized
+
Subject/reference contracts
+
cross-domain retrieval
```

The information can follow the same Person identity without becoming an untyped `Person.properties` bag.

### Books / reviews / later recommendation

Slice A requires that whatever later domain/product representation is justified can be addressed and related without introducing a universal Entity. Slice A does **not** prematurely classify Book as a new kernel native owner.

Product Reality verdict: **PASS / capability-stage work remains**.

---

## 18. High-value queries / operations

Slice A must support logically:

1. resolve a typed reference to its exact native owner without semantic `Entity` inheritance;
2. list current/historical ExternalRefs mapped to one NativeRef;
3. explain why an ExternalRef is mapped, unresolved, rejected or superseded;
4. determine whether two provider representations are currently considered the same native referent without deleting their source identities;
5. reconstruct the identity-resolution state accepted at time T;
6. correct/revoke a mistaken merge/link while preserving prior attribution;
7. distinguish Person from linked Account/Principal/provider identities;
8. reference one Person as Subject in one context and Actor in another without wrapper identity;
9. determine allowed target families for a Reference Contract;
10. reject an invalid target family before treating the relation as canonical;
11. resolve current redirects/identity reconciliation without rewriting the original historical reference automatically;
12. use one native referent across multiple authorized life domains without exposing private cross-context linkage;
13. add a future native referent family without changing the meaning of existing NativeRefs;
14. identify a material Version/state separately from native identity.

---

## 19. Reverse mapping

### LOGICAL REPRESENTATION

```text
Native identity owner record/state
NativeRef logical address
Reference Contract
ExternalRef
identity Mapping/Reconciliation
Version/material-state reference boundary
context-scoped disclosure possibility
```

### DOMAIN OWNERS

```text
Person / Living Referent / Asset / Place / Content Artifact / Collective
Actor / Subject / Resource roles without wrapper identity
Account boundary
Reconciliation / Version / Provenance integration pressure
```

### NOT REPRESENTED AS

```text
universal Entity / Thing
universal Actor / Subject / Resource entity
provider object as native truth
Account as Person
one generic Relationship
one global property bag
```

### IDENTITY RULE

Native identity remains with its Domain owner; ordinary role/provider/name/state changes do not replace it.

### HISTORY RULE

Material identity mapping/reconciliation/correction is historized; final resolution does not silently rewrite what was previously known.

### SOURCE RULE

External/source identity remains scoped and distinct from NativeRef.

### MULTI-ACTOR RULE

Shared referent identity does not imply shared Visibility/Authority or public cross-context correlation.

### DERIVED RULE

Current resolved/redirected identity views may be projections over canonical identity + Reconciliation history.

### SPECIALIST RULE

Specialist/application identities may remain bounded and do not become native kernel identities merely to participate in references.

Reverse-mapping verdict: **PASS**.

---

## 20. Physical-stage freedom

Slice A intentionally does not decide whether the future physical model uses:

```text
technical native-reference anchor/registry
owner-specific foreign keys
composite typed references
separate relation tables
partitioned structures
hybrid combinations
UUID / integer / other key form
public/API handles
GraphQL Node-like API
```

Physical implementation must preserve:

- deterministic owner/type recovery;
- referential integrity appropriate to each reference contract;
- native identity non-reuse;
- provider/source scope;
- correction/reconciliation history;
- no false semantic inheritance;
- viable current and historical queries.

PostgreSQL inheritance is specifically **not** assumed to solve universal PK/FK integrity.

---

## 21. Regression impact

Selected Slice-A model is classified:

```text
R3 — WHOLE-LOGICAL
```

Reason: identity/addressability/reference infrastructure will be reused or pressure-tested by every later slice.

Therefore every later slice that changes NativeRef, Reference Contracts, ExternalRef, reconciliation or identity-history semantics must replay affected Slice-A tests.

---

## 22. Deferred obligations

Safe stage-bound obligations:

```text
Slice D
exact Version / Reconciliation / Provenance historical representation
full WD-03 discharge

Slice F
full Authority / Visibility / consent / delegation implications

Final Whole-Logical
integrated WD-05 persistence/API pressure
clean-room reconstruction

Physical Model
registry vs FK vs composite/hybrid implementation
key technology
constraints/indexes/partitioning

API/security stage
public/context-scoped handles
Principal/runtime authorization enforcement
```

These deferrals do not leave Slice-A identity meaning unresolved.

---

## 23. Reopen triggers

Reopen Slice A logically if later evidence shows that:

1. a native Domain owner cannot be addressed without semantic collapse under the Reference Contract model;
2. a valid role/relation target cannot be represented without forcing false native identity;
3. provider/security identity must become native identity to preserve truthful continuity;
4. identity merge/split/correction cannot remain historically reconstructible without changing Domain semantics;
5. privacy requirements make one shared native identity logically impossible rather than merely requiring scoped disclosure handles;
6. physical feasibility demonstrates that every sound implementation of the logical contract loses required referential integrity or queryability;
7. a later Domain change introduces a referent class incompatible with the current separation.

Physical inconvenience, ORM preference, table count or vendor schema mismatch are not sufficient.

---

## 24. Conditional acceptance

Slice A becomes the active accepted logical baseline only when its approved remote write scope passes exact Git QA:

```text
3 CREATE
5 UPDATE
0 DELETE
0 unexpected
all approved payloads fetched/read
main unchanged
```

When satisfied:

```text
SLICE A — IDENTITY / REFERENCE
PASS WITH HARDENING
REMOTE QA PASS
ACTIVE

DOMAIN REOPEN REQUIRED 0
LOGICAL STRUCTURAL BLOCKER 0

NEXT
SLICE B — INTENTION / EXECUTION
NOT AUTOMATICALLY STARTED BY THIS WRITE
```

---

## 25. Integrated A+B hardening — ReferenceAddress family

The cumulative A+B checkpoint found that Slice A's native/reference contract remained correct but incomplete for persistently addressable **non-native** semantic records introduced by Slice B.

### 25.1 ReferenceAddress is a representation family

Accepted integrated mechanism:

```text
ReferenceAddress
=
  NativeRef
  OR ScopedRecordRef
  OR MaterialStateRef
  OR ExternalRef
  OR another later explicitly accepted bounded address variant
```

This is not a Domain superclass.

```text
ReferenceAddress != Entity
ReferenceAddress != Thing
ReferenceAddress != Object root
ReferenceAddress != Relationship
```

### 25.2 ScopedRecordRef

`ScopedRecordRef` gives stable addressability to a materialized semantic record whose identity/history matters but whose identity remains dependent/contextual rather than native-referent identity.

Current pressure includes:

```text
Milestone
materialized Proposal
materialized Request
materialized Decision
qualified Dependency when relation history/addressability matters
```

Canonical rule:

```text
stable reference/history
!= native referent identity
```

### 25.3 MaterialStateRef

`MaterialStateRef` remains the distinct address of the materially relevant state/version of a target.

```text
NativeRef / ScopedRecordRef
!= MaterialStateRef
```

Exact construction remains Slice D.

### 25.4 ExternalRef remains separate

Provider/source addressability remains an external identity space.

```text
ExternalRef != NativeRef
ExternalRef != ScopedRecordRef
ExternalRef != MaterialStateRef
```

### 25.5 Reference Contract now constrains address variant too

A Reference Contract must preserve, where relevant:

```text
semantic role/family
eligible ReferenceAddress variants
eligible target owner/family
scope/context
cardinality/directionality
unresolved-target behavior
material-state/facet binding
history/materiality
Visibility/Authority implications
specialist boundary
```

A resolvable global address is not automatically semantically valid for a slot.

### 25.6 Reconsidered technology/mechanism alternatives

The A+B checkpoint reopened the reference architecture decision rather than treating Slice A as privileged because it had already passed.

Reconsidered:

```text
owner-specific references only
global Node/Entity registry/interface
one undifferentiated TypedRef(kind,id)
discriminated ReferenceAddress family + Reference Contract
```

Verdict:

```text
ReferenceAddress family + Reference Contract
RETAIN + HARDEN
```

Owner-specific references remain a strong physical implementation ingredient. A narrow technical registry may remain physically valid. A global semantic Node/Entity root remains rejected.

### 25.7 External calibration

Transferable evidence used in the reconsideration:

- FHIR typed/limited References show common reference machinery can retain target-type constraints;
- FHIR version-specific Provenance targets reinforce target versus target-state distinction;
- Kubernetes ObjectReference separates kind/UID from resourceVersion and can bind to a field path;
- Kubernetes UID remains distinct from resourceVersion;
- PostgreSQL inheritance still does not make PK/unique/FK constraints span children, so a universal parent-table hierarchy is not a free integrity solution;
- Relay/GraphQL global Node is useful for API refetching but is a negative ontology benchmark for LifeOS because it deliberately defines a universal globally identified object interface.

LifeOS copies none of those ontologies. It adopts only the structural lesson that addressability, type eligibility and addressed state can remain explicit and separable.

### 25.8 Regression impact

```text
IMPACT
R3 WHOLE-LOGICAL
```

All later slices must treat `ReferenceAddress` as representation-only vocabulary and must not collapse its variants into a universal semantic object identity.
