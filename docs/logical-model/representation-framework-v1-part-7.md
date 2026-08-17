<!-- LIFEOS-CANONICAL-CONTINUATION document="representation-framework-v1.md" follows="representation-framework-v1-part-6.md" -->
> **Canonical continuation of the single Logical Representation Framework v1 document.** Earlier representation roles remain authoritative. This continuation records Integrated A+B+C+D+E hardening only.

# Integrated A+B+C+D+E representation hardening

## R-H01 — Role-target addressability remains broader than NativeRef

A Reference Contract may allow a target represented by:

```text
NativeRef
OR
ScopedRecordRef / bounded dependent record
OR
value/supply/pool/service/specialist representation
```

where the semantic owner justifies that target family.

Canonical rule:

```text
referenceable in a contextual role
!= independent native identity
```

`Resource` is the main current pressure case, but the rule applies generally to contextual-role targets.

No `ResourceRef`, `SubjectRef` or `ActorRef` wrapper identity is introduced merely for uniformity.

## R-H02 — Material input binding for consequential derived/effective records

When a consequential record/result depends materially on mutable source state, the representation must support binding to or reconstructing the applicable material source state.

Current examples:

```text
Evaluation
-> Criterion MaterialStateRef
-> Evidence/source material states

Resource Allocation
-> Resource Requirement MaterialStateRef where material

Capacity Claim
-> Schedule/temporal-footprint MaterialStateRef or claim-owned historical footprint

solver/AI accepted result
-> materially relevant Requirement/constraint/Availability/Capacity/policy/model basis
```

This does not create one universal `InputSnapshot` semantic root.

Possible physical implementations remain open:

```text
owner-specific version FK
material-state anchor
immutable revision reference
bounded snapshot
bitemporal reconstruction
hybrid
```

## R-H03 — Derived projection history is consequence-sensitive

`LR-08` remains derived by default.

Examples:

```text
Candidate Set
Effective Availability
Effective Free Capacity
Goal Progress
current knowledge/read models
```

Canonical rule:

```text
current LR-08 recomputation
!= historical LR-08 result automatically
```

If a historical derived result becomes materially consequential, preserve either:

```text
sufficient historical inputs + computation semantics to reconstruct it
OR
bounded materialized historical result/snapshot
```

according to consequence.

Do not make every projection canonical merely to obtain auditability.

## R-H04 — LR-05 is a representation role, not a semantic superclass

`LR-05 Rule / policy / specification` may support multiple semantic owners:

```text
Criterion
Resource Requirement
Temporal Constraint
Availability rule
Conditional Policy
other reviewed bounded specifications
```

Shared infrastructure may include:

```text
predicate/expression representation
comparison operators
composition helpers
unit-aware conditions
versioning primitives
validation/evaluation engine components
```

but the containing semantic owner remains explicit.

Forbidden logical shape:

```text
Rule
  id
  type
  payload

where Rule itself becomes the universal canonical owner
```

Canonical rule:

```text
same LR role
!= same semantic identity/lifecycle/governance
```

## R-H05 — `Actual` remains expectation-reconciliation only

The Representation Framework must not use `Actual` as the generic representation role for everything that happened.

```text
Actual
-> realization of a prior intended/expected subject
```

Spontaneous reality may instead be represented through the appropriate owner:

```text
Session
Observation
Transaction
Inventory Movement
specialist record
```

A Resource Allocation/usage comparison may reference an Actual only where an expectation is actually being reconciled.

## R-H06 — Implicit specification materialization threshold

An LR-05 specification may remain embedded/implicit in simple cases when:

```text
no independent lifecycle
no material version history
no consequential reference
no governance/reconciliation requirement
```

It must become materially reconstructible once a later consequential record/result depends on its specific state.

This is a general framework rule, not Resource Requirement-only.

Conceptual escalation:

```text
implicit / embedded LR-05
        ↓ consequence threshold
LR-02 dependent semantic record
+ ScopedRecordRef / MaterialStateRef as required
```

The escalation mechanism remains owner-specific.

## R-H07 — Temporal basis of a consequential relation must not float with current state

A qualified relation may point at a current owner while its historical meaning depends on the owner's state at the time.

Example:

```text
Capacity Claim
-> Schedule S
```

If Schedule S moves later, historical claim meaning must remain tied to the applicable Schedule material state or to its own temporal footprint.

General rule:

```text
reference to continuing owner identity
!= automatic reference to owner's current material state
```

Use `MaterialStateRef` or another typed historical binding when the state matters.

## R-H08 — Computation engine metadata is not domain identity

Solver/model/rule-engine details may need to be retained for reproducibility, but they remain computation metadata/provenance unless an independently justified domain owner exists.

Potential material computation metadata:

```text
engine family/version
model/configuration version
objective/ranking version
input snapshot/reference set
random seed where material
provider/model identifier
reason/rationale summary
```

Canonical rule:

```text
computation metadata
!= NativeRef owner
!= Decision
!= Authority
!= canonical Allocation
```

## R-H09 — Feasibility-state vocabulary is typed, not one generic boolean

Representation must preserve, where material:

```text
eligible
candidate
available
feasible
capacity-sufficient
allocated
claimed
realized-use
```

A projection may expose a simplified status for product/API convenience, but the semantic basis must remain recoverable.

## Integrated representation verdict

```text
ReferenceAddress                 RETAIN
MaterialStateRef                 RETAIN + EXTEND USAGE
LR-05 owner-specific specs       RETAIN + HARDEN
LR-08 derived projections        RETAIN + HARDEN HISTORY RULE
LR-03 qualified relations        RETAIN
LR-02 material dependent records RETAIN
LR-13 specialist boundaries      RETAIN

universal Entity root            REJECT
universal Resource root          REJECT
universal Rule root              REJECT
universal Claim root             REJECT
universal Fact/State root        REJECT
solver-first canonical model     REJECT
```

No new universal representation role or ReferenceAddress family is introduced by the cumulative checkpoint.