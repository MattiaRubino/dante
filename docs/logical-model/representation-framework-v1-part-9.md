<!-- LIFEOS-CANONICAL-CONTINUATION document="representation-framework-v1.md" follows="representation-framework-v1-part-8.md" -->
> **Canonical continuation of the single Logical Representation Framework v1 document.** Earlier representation roles and Slice A–F contracts remain authoritative. This continuation records Whole-Logical A+B+C+D+E+F integration hardening only.

# Whole-Logical representation hardening

## WL-RF-01 — Agreement terms are MaterialState-owned, not a generic reference family

Material Agreement terms must bind to a `MaterialStateRef` of an explicitly justified semantic owner/facet.

Possible owners include:

```text
Proposal material state
Content Artifact material state
Agreement-owned LR-02 terms state
another explicitly justified owner/facet
```

Forbidden:

```text
TermsRef universal address family
Terms root introduced only for storage convenience
ownerless terms_id
```

The exact terms owner must be recoverable through the Reference Contract.

## WL-RF-02 — Governed Operation / Effect Contract

Whole integration adds a logical contract for consequential governed effects.

Where applicable it preserves:

```text
operation family
target semantic owner/facet
target MaterialStateRef or equivalent material basis
effect semantics
input/context
purpose
preconditions
Authority / Consent / Visibility / Representation requirements
expected-state semantics
idempotency semantics
```

This is representation vocabulary, not a new Domain `Operation`, `Command` or `Action` root.

```text
HTTP route
AuthZ action string
UI command name
!= canonical governed effect
```

## WL-RF-03 — Projection / Disclosure Surface Contract

A derived/recipient-visible surface may be governed without introducing persistent Projection identity.

Where material, the contract preserves:

```text
source owner / bounded source set
projection/facet kind
derivation/profile
material source/version basis
purpose/context
permitted exposure
source-disclosure boundary
recipient/governance context
```

Therefore:

```text
projection is governable
!= ProjectionRef required
```

Visibility of a safe projection does not imply Visibility of its source.

## WL-RF-04 — Absence/negative-state contract

No universal representation convention may translate absence into false.

```text
missing representation
!= false
!= no
!= inactive
!= declined
!= cancelled
!= non-realization
```

Owner-specific negative semantics may be explicit. Otherwise unknown/unresolved remains representable.

This rule applies across relational joins, API fields, projections and derived states.

## WL-RF-05 — Expected-state contract

Consequential mutation over mutable material state must support an expected-state precondition when stale write would be materially unsafe.

Logical form:

```text
mutation
+ expected MaterialStateRef / semantically equivalent expected-state condition
-> apply only if still applicable
```

Mismatch becomes conflict/re-read/reconcile/retry/user resolution as appropriate.

Transport/storage representations may include:

```text
ETag
row revision
MVCC token
provider revision
```

but:

```text
concurrency token != MaterialStateRef by semantic identity
```

## WL-RF-06 — Idempotency contract

The representation framework permits bounded operation/transport idempotency without promoting retry identity into Domain identity.

```text
same idempotency key
+ materially equivalent operation
-> may reuse prior effect/result

same key
+ materially different operation
-> conflict/reject
```

Forbidden:

```text
IdempotencyKey = NativeRef
IdempotencyKey = Goal/Request/Decision identity
IdempotencyKey -> universal Command root
```

## WL-RF-07 — Multi-owner consistency contract

Where one consequential operation spans multiple owners/relations:

```text
if invariants require all-or-nothing
-> physical atomic consistency boundary required
```

Where provider/distributed boundaries prevent global atomicity:

```text
explicit staged state
+ partial result
+ reconciliation / compensation
```

A hidden partial effect may never be represented as complete canonical success.

No Domain `Transaction` root is introduced.

## WL-RF-08 — Canonical / provider-sync separation

Slice A/D LR-09 separation is promoted to a Whole invariant.

```text
canonical LifeOS state
!= provider representation
!= provider revision
!= sync/apply status
!= reconciliation status
```

Example:

```text
LifeOS Schedule 16:00
provider still 15:00
sync failed
reconciliation required
```

is valid and must remain representable without silently rewriting canonical state.

## WL-RF-09 — LR-08 freshness / consequential use

LR-08 remains derived/effective state. Materialization or caching does not promote it to canonical truth.

For consequential use, one of the following must hold as appropriate:

```text
revalidate underlying material basis
OR
bind to exact historical Evaluation/input state
OR
persist a bounded consequential snapshot
```

Current examples include:

```text
Candidate Set
Effective Availability
Free Capacity
current knowledge
Effective Authority
Effective Visibility
recipient-specific projection
```

```text
stale LR-08 cache -> canonical effect
FORBIDDEN
```

## WL-RF-10 — Retention / redaction / tombstone integrity

History representation must distinguish where policy permits:

```text
never existed
historically existed but payload later redacted/unavailable
```

A minimal tombstone/reference continuity may be used physically later, but it may retain only what applicable policy permits.

Permanent identity rule:

```text
deleted/retired NativeRef
NEVER reused for another referent
```

Redaction does not itself imply historical nonexistence.

## WL-RF-11 — Consequential AuthZ provenance

Security-runtime representation remains separate from Domain governance while being linkable for consequential audit/history.

Where required, preserve/reconstruct:

```text
actual Actor
represented party
Principal/session/security context
Authority basis
Consent / Visibility basis
MaterialStateRefs
technical policy/model version
allow/deny decision
effect produced
```

Canonical non-equivalences:

```text
ALLOW != Authority
DENY != established absence of Authority
Principal != Actor
AuthZ log != Domain history automatically
```

OpenFGA/Cedar/OPA/capability/custom engines remain replaceable Physical/runtime candidates.

## WL-RF-12 — Non-interference / inference-leakage contract

Selective disclosure is evaluated across the full observable recipient surface.

Potential leakage channels include:

```text
object existence
relationship existence/kind
counts
ranking
candidate membership
free/busy detail
errors
explanations
aggregations
derived scores
timing-sensitive behavior
```

A permitted coarse projection may use a private source without disclosing or making inferable more source information than the applicable disclosure contract allows.

```text
Visibility(projection)
!= Visibility(source)
```

## Whole representation owner coverage

The complete Domain census has been replayed against LR-01..LR-13 and accepted role/reference contracts.

```text
DOMAIN CONCEPTS              57
CLASSIFIED                   57
UNCLASSIFIED                  0
NEW REPRESENTATION ROOT       0
```

Native identity set remains:

```text
Person
Living Referent
Asset
Place
Content Artifact
Collective
Possibility
Goal
Plan
Activity
Event
Routine
Occurrence
Session
Observation
```

`Actor`, `Subject`, `Resource`, Agreement terms and derived projections do not gain wrapper/native identity merely for technical convenience.

## Whole ReferenceAddress verdict

```text
ReferenceAddress                   RETAIN
NativeRef                          RETAIN
ScopedRecordRef                    RETAIN
MaterialStateRef                   RETAIN + WHOLE CONSEQUENCE USE
ExternalRef                        RETAIN
Reference Contract                 RETAIN + OWNER/RELATION/EFFECT PROFILE

LR-01                              RETAIN
LR-02                              RETAIN
LR-03                              RETAIN + SPECIFIC SEMANTIC OWNER RULE
LR-04                              RETAIN
LR-05                              RETAIN
LR-06                              RETAIN
LR-07                              RETAIN
LR-08                              RETAIN + FRESHNESS CONTRACT
LR-09                              RETAIN + SYNC-SEPARATION CONTRACT
LR-10                              RETAIN BOUNDED
LR-11                              RETAIN
LR-12                              RETAIN
LR-13                              RETAIN
```

Rejected:

```text
universal Entity / Thing
universal Relationship / Edge
universal Rule
universal Fact / Assertion
universal WorkItem
universal Version root
universal RelationRef
universal TermsRef
universal ProjectionRef
universal Command/Operation root
universal Permission root
```

## Reverse-mapping requirement

For every Whole representation, an independent reader must still recover:

```text
specific Domain owner/family
identity class
semantic role/facet
material state/history
source/provider relation
actor/governance context
derived/canonical classification
specialist boundary
```

Result after WL-RF-01..12:

```text
57 / 57 OWNER REVERSE MAPPING
PASS

GENERIC FALLBACK DEPENDENCY
0
```

## Physical freedom retained

This continuation does not choose:

```text
table layout
key/UUID strategy
indexes
constraints
history table/event design
PostgreSQL schema
TypeDB schema
Neo4j schema
transaction boundary implementation
ETag/API precondition format
idempotency storage
provider outbox/inbox
RLS/application-policy split
AuthZ engine
API routes/DTOs
```

Physical Model must prove that whichever mechanisms are chosen preserve this framework.

## Closure boundary

This representation hardening is part of the nine-file Whole content package. It becomes final Logical Model closure evidence only after exact remote QA and the separately gated `checkpoints/whole-logical-v1-remote-qa.md` record.

Until then:

```text
LOGICAL MODEL NOT YET CLOSED
WD-03 CLEARANCE READY
WD-05 CLEARANCE READY
PHYSICAL MODEL NOT YET AUTHORIZED
```
