# LifeOS Logical Model — Integrated A+B Validation v1

**Date:** 2026-08-17  
**Scope:** Stage 0 + Stage 0H + Slice A Identity/Reference + Slice B Intention/Execution  
**Pre-scope:** `5d7b3d35b529a80808c719c390bdf6df6e20a6b0`  
**Status:** PASS WITH HARDENING — activation conditional on exact remote QA

---

## 1. Purpose

This checkpoint validates the Logical Model accumulated so far as one system before Slice C begins.

It is deliberately not a repetition of the local Slice-A and Slice-B validations. It asks whether individually accepted representations remain coherent after composition and whether newly exposed pressure changes which representation mechanism is actually preferable.

The checkpoint therefore includes two distinct controls:

```text
CUMULATIVE INTEGRATION
Do all accepted slices still fit together without contradiction, omission or semantic leakage?

MECHANISM / TECHNOLOGY RECONSIDERATION
Given the new integrated evidence, is the previously selected representation mechanism still the best current option compared with strong rejected alternatives and newly plausible mechanisms?
```

No physical technology is selected by this checkpoint. At the Logical Model stage, `technology` means representation mechanism / architecture pattern. Concrete PostgreSQL/API/runtime technology remains stage-deferred.

---

## 2. Inputs replayed

Canonical inputs:

```text
accepted Domain Atlas / Whole-Domain closure
Product Identity / North Star
ADR-007
Domain -> Logical readiness contract
Logical Validation Methodology v1 + Stage-0H
Slice A accepted contract/checkpoint/benchmark
Slice B accepted contract/checkpoint/benchmark
traceability ledger
decision/assumption register
test corpus
current external primary-source evidence
```

Repository integrity before the checkpoint:

```text
feature/logical-model
HEAD 5d7b3d35b529a80808c719c390bdf6df6e20a6b0

main
068da4cc66620b3f3811051170e4913097091a04

branch relative to main
27 commits ahead
0 behind

Logical Model paths only
13

Domain / SQL / backend / frontend modifications
0
```

---

## 3. Integrated result

The fundamental architecture holds.

```text
DOMAIN REOPEN REQUIRED       0
NEW DOMAIN OWNER REQUIRED    0
UNIVERSAL ROOT REQUIRED      0
GENERIC FALLBACK REQUIRED    0
SLICE-A DESIGN FAILURE       0
SLICE-B DESIGN FAILURE       0
CROSS-SLICE HARDENINGS       6
STRUCTURAL REPLACEMENT       0
```

The correct verdict is not `PASS` without qualification because the composition exposed representation gaps that were not visible enough in the isolated slice checkpoints.

```text
INTEGRATED A+B
PASS WITH HARDENING
```

---

## 4. Finding AB-H01 — canonical Activity/Event identity was stated too conditionally

Slice B originally described:

```text
Activity -> LR-01 when persistent independent identity is required
Event    -> LR-01 when persistent independent event identity is required
```

The Domain definitions already classify canonical Activity and Event as persistent representations with continuity rules.

Therefore the storage/logical layer cannot make canonical identity optional after the semantic object already exists.

Correct integrated rule:

```text
canonical persisted Possibility -> LR-01
canonical Goal                  -> LR-01
canonical Plan                  -> LR-01
canonical Activity              -> LR-01
canonical Event                 -> LR-01
canonical Routine               -> LR-01
```

This does **not** force every transient suggestion/input/search result into one of these owners.

```text
transient candidate
!= canonical Possibility / Activity / Event automatically
```

`LR-01` remains a logical identity requirement, not a one-table-per-owner SQL decision.

---

## 5. Finding AB-H02 — addressability must cover persistent non-native semantic records

Slice A correctly established:

```text
NativeRef
= address of independently justified native identity
```

Slice B then introduced/used semantic records that may require stable addressability/history without becoming native referent identities, including:

```text
Milestone
Proposal when materially persisted
Request when materially persisted
Decision when materially persisted
qualified Dependency when relation history/addressability matters
```

Promoting these to NativeRef merely for referencing would violate Slice A.
Leaving them only as vague `persistently addressable` records would leave reverse mapping and later reference contracts underspecified.

### Accepted hardening — discriminated Reference Address family

LifeOS adopts a **Reference Address family** as a representation mechanism:

```text
ReferenceAddress
=
  NativeRef
  OR ScopedRecordRef
  OR MaterialStateRef
  OR ExternalRef
  OR another later explicitly accepted bounded address variant
```

This is a discriminated union/family of logical addresses, not a Domain superclass.

```text
ReferenceAddress != Entity / Thing / Object
ReferenceAddress != Relationship
ReferenceAddress != common lifecycle
```

Variants preserve distinct address spaces:

```text
NativeRef
addresses independently justified native Domain identity

ScopedRecordRef
addresses a materialized semantic record whose identity/history is scoped/dependent rather than native-referent identity

MaterialStateRef
addresses a materially relevant state/version of a target; exact mechanism remains Slice D

ExternalRef
addresses provider/source identity under its provider-specific scope
```

Canonical non-collapse:

```text
NativeRef != ScopedRecordRef
NativeRef != MaterialStateRef
NativeRef != ExternalRef
ScopedRecordRef != MaterialStateRef
ExternalRef != canonical identity
```

### Reference Contract remains authoritative

A `ReferenceAddress` is not semantically valid merely because it resolves.

The containing Reference Contract must constrain:

```text
semantic role/family
allowed address variants
eligible target owner/family
scope/context
cardinality/directionality
material-state binding where required
history/visibility/authority implications
specialist boundary
```

A globally resolvable address therefore does not become an `any object` relation.

---

## 6. Finding AB-H03 — explicit Request must not manufacture Authority

Slice B originally used wording equivalent to:

```text
explicit user request may itself authorize the bounded requested action
```

That wording is too broad against accepted Request/Authority semantics.

Correct rule:

```text
an explicit user instruction/request
may be sufficient evidence of that Actor's bounded intent/instruction
and may eliminate a redundant confirmation step
```

but:

```text
Request != Authority
Request != Consent
Request != governance power
requester != Authority holder automatically
```

Effective mutation of shared/governed state still requires the independently applicable Authority/Consent/policy basis.

Examples:

```text
personal Activity
"move it to 16:00"
-> direct instruction may be enough; no pointless second confirmation

shared company Event
"move it to 16:00"
-> instruction/request exists
-> Authority must still be independently established
```

The product may remain friction-light without corrupting governance semantics.

---

## 7. Finding AB-H04 — Dependency endpoints need facet/state binding

A Dependency is not semantically complete as only:

```text
from target -> to target
```

where the contingency concerns a specific state/result/transition/facet.

Integrated logical requirement:

```text
DependencyEndpoint
=
  target ReferenceAddress
  + materially relevant facet/state/result/transition/condition
```

Example:

```text
prerequisite
ScopedRecordRef(Milestone M1)
facet = attainment
condition = attained

Dependent
NativeRef(Activity A1)
facet = execution admissibility
```

This preserves:

```text
M1 exists
!= M1 attained
```

No universal expression language is introduced now. `all/any/quorum/alternative` composition and predicate technology remain deferred until concrete evidence justifies the minimum mechanism.

---

## 8. Finding AB-H05 — selective materialization must not become selective auditability

The accepted rule remains:

```text
not every Proposal / Request / Decision needs a standalone persisted semantic record
```

But:

```text
no standalone semantic-act record
!= no lineage/provenance/history for a consequential target change
```

Where a direct instruction produces a materially consequential target change, later history must still be able to explain the applicable actor/source/basis according to Slice-D/F semantics even if no standalone Request/Decision record was justified.

Example:

```text
user says "move my Activity to 16:00"
```

may avoid a standalone Request + Decision pair, while the material Schedule/target change may still preserve:

```text
previous state
new state
actor/source
direct-instruction basis
applicable time/history
```

Selective materialization is an anti-overmodeling rule, not permission to erase consequence lineage.

---

## 9. Finding AB-H06 — maturation/replacement links are typed lineage, not generic relation

Two critical cross-owner identity transitions require explicit typed lineage semantics:

```text
Possibility P1
-- adoption/origin lineage -->
Goal G1
```

and:

```text
Plan PL2
-- replacement/continuation lineage -->
Plan PL1
```

These links must not become generic `related_to` edges.

They also must not collapse into Version:

```text
Goal G1 != Possibility P1 v2
Plan PL2 != Plan PL1 v2 automatically
```

Version/material-state may operate inside one continuing owner identity; typed lineage preserves truthful succession/origin where identity changes or a distinct owner is established.

---

## 10. Mechanism / technology reconsideration — triggered

Because AB-H02 changed the required addressability surface, the newly established `LM-WF-21` reconsideration gate was applied immediately rather than defending the original Slice-A mechanism by inertia.

Candidates reopened/reconsidered:

### TECH-AB-A — owner-specific reference families only

Examples:

```text
PersonRef
GoalRef
MilestoneRef
DecisionRef
...
```

**Strength:** strongest local type/FK specificity.

**Weakness under A+B:** repeated addressability, history and cross-owner contract machinery grows across slices; heterogeneous slots need expanding unions repeatedly.

**Verdict:** `RETAIN AS STRONG PHYSICAL INGREDIENT / NOT SELECTED LOGICAL BASELINE`.

### TECH-AB-B — global Node/Entity registry/interface

One common globally addressable object root.

**Strength:** simple universal refetch/addressing.

**Current external evidence:** Relay/GraphQL Global Object Identification intentionally defines a universal `Node` interface with globally unique IDs for refetching.

**Failure for LifeOS:** exactly the abstraction pressure LifeOS must not treat as semantic ontology; it also encourages native, scoped-record, state and provider identity spaces to converge accidentally.

**Verdict:** `REJECTED AS LOGICAL BASELINE`.

A later technical registry remains physically possible if it does not redefine semantics.

### TECH-AB-C — one undifferentiated TypedRef(kind,id)

**Strength:** compact common mechanism.

**Failure pressure:** insufficiently protects:

```text
native identity
scoped semantic record
material target state
provider identity
```

from being treated as one address/identity class by callers. The model can theoretically add more discriminators, at which point it converges toward TECH-AB-D.

**Verdict:** `REJECTED AS UNDERSPECIFIED`.

### TECH-AB-D — discriminated Reference Address family + Reference Contract

```text
ReferenceAddress
  NativeRef
  ScopedRecordRef
  MaterialStateRef
  ExternalRef

+
Reference Contract
```

**Strengths:** common addressability without common ontology; explicit address spaces; target eligibility remains contextual; future variants can be added without changing existing identity meaning; compatible with owner-specific physical constraints.

**External evidence:**

- FHIR `Reference` preserves typed/limited target reference semantics and can identify target type while reference constraints restrict legitimate targets;
- FHIR Provenance commonly points to version-specific targets, reinforcing target identity versus addressed state/version;
- Kubernetes `ObjectReference` separates kind/name/namespace/UID from optional `resourceVersion` and can address a specific field path;
- Kubernetes keeps object UID distinct from `resourceVersion`;
- PostgreSQL current documentation continues to warn that inheritance does not extend unique/PK/FK constraints through child tables, so a universal parent-table hierarchy is not a free referential-integrity solution.

**Anti-copy:** FHIR and Kubernetes have their own universal resource/object models. LifeOS adopts only the transferable address/type/state separation, not their ontology.

**Verdict:** `SELECTED — RETAIN + HARDEN`.

---

## 11. Why the selected mechanism remains the best current fit

The integrated evidence changes the shape but not the architectural family.

```text
ORIGINAL
NativeRef + Reference Contract + separate ExternalRef/Version pressure

HARDENED
ReferenceAddress discriminated family
  NativeRef
  ScopedRecordRef
  MaterialStateRef
  ExternalRef
+
Reference Contract
```

This preserves all Slice-A invariants while closing the Slice-B addressability gap.

It also leaves physical freedom:

```text
owner-specific foreign keys
technical address registry/anchor
composite typed keys
union/envelope at API/read-model layer
hybrid strategies
```

No exact table/UUID/API representation is selected.

---

## 12. New integrated invariants

```text
INV-085 canonical persisted Activity has stable LR-01 identity; persistence choice cannot demote an accepted Activity to identity-less state
INV-086 canonical persisted Event has stable LR-01 identity; persistence choice cannot demote an accepted Event to identity-less state
INV-087 transient candidate/input != canonical owner solely because it resembles Activity/Event/Possibility content
INV-088 ReferenceAddress is a representation family, not a semantic Entity/Thing/Object root
INV-089 NativeRef != ScopedRecordRef != MaterialStateRef != ExternalRef
INV-090 stable addressability of an LR-02/LR-03 record != promotion to native referent identity
INV-091 Reference Contract constrains eligible address variant + target semantics; resolvable != semantically eligible
INV-092 Request/instruction may establish requester intent without establishing Authority/Consent/governance power
INV-093 redundant confirmation may be omitted only where applicable governance already permits the bounded effect
INV-094 Dependency endpoint target identity != required prerequisite/dependent facet/state/result/transition
INV-095 Dependency facet/state binding != universal predicate/expression language
INV-096 selective semantic-act materialization != selective auditability of consequential change
INV-097 Possibility->Goal maturation link is typed origin/adoption lineage, not retyping or generic relation
INV-098 Plan replacement/continuation link is typed lineage and does not imply Version identity continuity automatically
INV-099 mechanism hardening must trigger candidate/technology reconsideration before advancing to the next slice when material trade-offs changed
INV-100 technology/mechanism reconsideration may retain, harden, replace or block the previous choice; prior acceptance carries no privileged status
```

---

## 13. Integrated mutation tests

```text
MUT-AB01 promote every addressable LR-02 record to NativeRef
-> FAIL: native referent identity inflation

MUT-AB02 use one untyped global ref for Native/Record/State/External
-> FAIL: address-space collapse / ambiguous reverse mapping

MUT-AB03 allow ReferenceAddress without Reference Contract eligibility
-> FAIL: any-object semantic relation

MUT-AB04 keep Activity/Event LR-01 optional after canonical persistence
-> FAIL: Domain persistence/continuity contradiction

MUT-AB05 direct user Request creates Authority
-> FAIL: governance semantic collapse

MUT-AB06 Dependency references only whole endpoints
-> FAIL when only one material facet/state is contingent

MUT-AB07 omit standalone Request/Decision and omit all consequential change lineage
-> FAIL: selective materialization becomes history loss

MUT-AB08 Possibility->Goal represented as same row kind/status mutation
-> FAIL: pre-adoption history rewrite

MUT-AB09 Plan replacement represented only as same Plan version
-> FAIL where execution-strategy identity genuinely changed

MUT-AB10 skip mechanism reconsideration after integrated hardening changes constraints
-> FAIL: architecture becomes path-dependent and rejected alternatives are never legitimately retested
```

```text
INTEGRATED MUTATION PASS 10 / 10
```

---

## 14. Counterfactuals

```text
canonical Activity
vs transient suggested action                           PASS

Native Goal address
vs scoped Milestone address                            PASS

Decision record identity
vs Decision material-state reference                   PASS

provider ExternalRef
vs native target                                       PASS

user instructs personal change
vs user requests change they lack Authority to impose PASS

Dependency on target existence
vs Dependency on target attained state                 PASS

no standalone Request object
vs no audit/lineage at all                             PASS

Possibility matured to Goal
vs same Possibility retyped Goal                       PASS

Plan revised in place
vs distinct replacement Plan                          PASS
```

---

## 15. New workflow rule — cumulative checkpoint

After every accepted slice:

```text
slice N local validation
-> exact remote QA
-> cumulative integrated checkpoint over Stage 0 + all accepted slices through N
-> repair any integrated hardening
-> mechanism/technology reconsideration when triggered
-> exact remote QA
-> rerun cumulative checkpoint
-> only then authorize/read-start slice N+1
```

This prevents local slice PASS from hiding integration defects until the end.

---

## 16. New workflow rule — mechanism / technology reconsideration

Trigger when any of these materially changes the candidate trade-off:

```text
cumulative checkpoint finds a new gap/hardening
new external primary evidence challenges a mechanism
later slice requires a capability the selected mechanism handled poorly
physical feasibility evidence invalidates an assumed option
scale/privacy/history/concurrency pressure changes materially
```

Required candidate set:

```text
current selected mechanism
strongest previously rejected-but-not-logically-impossible alternative(s)
new plausible mechanism(s)
relevant current external structural patterns / negative benchmarks
```

Required assessment:

```text
semantic preservation
reverse mapping
history/correction
privacy/governance
queryability
simple-case ceremony
worst-case complexity
scale/concurrency plausibility
evolution/migration risk
physical implementation freedom
external evidence freshness
```

Allowed verdicts:

```text
RETAIN
HARDEN
REPLACE
BLOCKED
```

If `REPLACE`, classify impact and rerun every affected cumulative regression before proceeding.

---

## 17. Gate results

```text
LM-01..LM-23 prior applicable gates      PASS / PASS WITH existing hardenings
LM-24 Cumulative Integrated Coherence    PASS WITH HARDENING
LM-25 Mechanism/Technology Reconsideration PASS — RETAIN + HARDEN

DOMAIN REOPEN REQUIRED                   0
LOGICAL STRUCTURAL BLOCKER               0
CROSS-SLICE HARDENING UNCLASSIFIED       0
MECHANISM ALTERNATIVE UNREVIEWED         0
```

---

## 18. Final integrated verdict

```text
STAGE 0 / 0H
PASS

SLICE A
PASS WITH HARDENING
ACTIVE

SLICE B
PASS WITH HARDENING
ACTIVE

INTEGRATED A+B
PASS WITH HARDENING

SELECTED REFERENCE MECHANISM
DISCRIMINATED REFERENCE ADDRESS FAMILY + REFERENCE CONTRACT
RETAIN + HARDEN

DOMAIN REOPEN REQUIRED       0
NEW DOMAIN OWNER REQUIRED    0
STRUCTURAL REDESIGN          0

SLICE C
HOLD UNTIL THIS CHECKPOINT + ALL 8 PROPAGATION UPDATES PASS REMOTE QA
```

No SQL, migrations, API, backend, AuthN/AuthZ runtime, frontend or Domain Model change is authorized by this checkpoint.
