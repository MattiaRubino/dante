# Logical Model Workstream

**Status:** Stage 0 + Stage 0H + Slice A + Slice B active; integrated A+B hardening written — activation conditional on current remote QA; Slice C HOLD  
**Started:** 2026-08-17  
**Branch:** `feature/logical-model`  
**Base main:** `068da4cc66620b3f3811051170e4913097091a04`

## Purpose

Translate the closed LifeOS Core Domain Model / Domain Atlas into a validated logical representation that is implementable, queryable, historical, multi-actor safe, provider-aware and evolvable without silently changing accepted semantic meaning.

This workstream is **not** SQL/physical schema/API/backend implementation.

---

## Canonical authority

Read in this order for semantic/logical decisions:

1. accepted Domain Atlas and current Whole-Domain closure chain;
2. accepted Product Identity / North Star;
3. `docs/decisions/ADR-007-domain-model-informed-persistence-boundaries.md`;
4. `docs/architecture/domain-model-logical-readiness.md` plus current continuation chain;
5. `docs/logical-model/validation-methodology-v1.md`;
6. `docs/logical-model/traceability-and-regression-ledger-v1.md`;
7. `docs/logical-model/decision-and-assumption-register-v1.md`;
8. accepted slice decisions and cumulative integrated checkpoints created by this workstream;
9. current external evidence under `docs/logical-model/external-benchmark-policy-v1.md`.

Provider schemas, legacy architecture examples and implementation convenience remain subordinate evidence.

---

## Starting repository state

```text
main
068da4cc66620b3f3811051170e4913097091a04

domain integration PR
#10 merged

feature/logical-model
created directly from main
068da4cc66620b3f3811051170e4913097091a04
```

No Domain Model content was rewritten during branch creation.

Canonical split Domain files remain physically split and logically unified according to the documentation/handoff protocol.

---

## Stage-0 foundation — completed QA

Initial foundation scope:

```text
5 CREATE
0 UPDATE
0 DELETE
```

Paths:

```text
docs/logical-model/validation-methodology-v1.md
docs/logical-model/test-corpus-v1.md
docs/logical-model/external-benchmark-policy-v1.md
docs/logical-model/representation-framework-v1.md
docs/workstreams/logical-model.md
```

Verified remote result:

```text
Stage-0 HEAD
3dc8fdb869e445b84255fb881c0e11da76cf2a43

ahead_by       5
behind_by      0
added          5
modified       0
deleted        0
unexpected     0

remote payload read
5 / 5

main
068da4cc66620b3f3811051170e4913097091a04
UNCHANGED
```

Therefore:

```text
LOGICAL MODEL STAGE 0
REMOTE QA PASS
```

---

## Stage-0H methodology hardening — completed QA

Approved PRE-SCOPE:

```text
3dc8fdb869e445b84255fb881c0e11da76cf2a43
```

Approved physical scope:

```text
2 CREATE
4 UPDATE
0 DELETE
```

Created:

```text
docs/logical-model/traceability-and-regression-ledger-v1.md
docs/logical-model/decision-and-assumption-register-v1.md
```

Updated:

```text
docs/logical-model/validation-methodology-v1.md
docs/logical-model/test-corpus-v1.md
docs/logical-model/representation-framework-v1.md
docs/workstreams/logical-model.md
```

Verified Stage-0H result:

```text
HEAD
0076b02715acf418cd9ef2840ed719b4201c8730

from PRE-SCOPE
commits         6
added           2
modified        4
deleted         0
unexpected      0
remote readback 6 / 6
main unchanged
```

Therefore:

```text
LOGICAL MODEL STAGE 0H
HARDENED FOUNDATION
REMOTE QA PASS
ACTIVE
```

The active validation standard is now:

```text
LM-WF-01..21
LM-01..25 where applicable
+
traceability matrix
cumulative invariant ledger
mutation/destructive testing
counterfactual testing
cross-slice regression
rejected-alternative register
assumption/freshness register
simple-case / worst-case pairing
Product Reality pressure
cumulative integrated checkpoint after every slice
mechanism/technology reconsideration when triggered
final clean-room reconstruction
```

---

## Foundational operating rules

1. **Domain Atlas is authoritative.** Logical discomfort or implementation convenience is not Domain-reopen evidence.
2. **Falsification before acceptance.** Every material logical candidate is attacked before optimization.
3. **Multiple plausible alternatives.** Strong alternatives are compared rather than constructing straw men.
4. **Mandatory traceability.** Every material owner/invariant traces to representation, query/operation, tests and verdict.
5. **Cumulative invariant ledger.** Later slices cannot silently weaken earlier accepted invariants.
6. **Mutation/destructive testing.** Remove, merge, genericize, overwrite or provider-identify structures to prove necessity.
7. **Counterfactual testing.** Near-identical cases with different accepted meaning must remain distinguishable.
8. **Retroactive/cross-slice regression.** Later shared-mechanism changes replay earlier affected tests.
9. **Rejected alternatives remain documented.** Do not rediscover failed architecture without new evidence.
10. **Assumptions are explicit and freshness-scoped.** No final PASS depends materially on stale or unproven assumptions.
11. **Fresh external research.** Search direct, adjacent, specialist, infrastructure and structurally useful unrelated systems.
12. **External evidence is not ontology authority.** LifeOS may fuse useful mechanisms but must not copy vendor taxonomy by popularity.
13. **Negative benchmarks are mandatory.** Learn from architectural reversals/failure patterns as well as successful patterns.
14. **Simple and worst cases both matter.** Avoid both toy architecture and needless universal complexity.
15. **Product Reality cases are tests, not commands.** Separate Domain coverage, logical requirement, capability gap and specialist boundary.
16. **No semantic-free escape hatch.** Required meaning cannot disappear into generic relations/properties/JSON.
17. **Clean-room closure.** Final meaning must be reconstructible from repository documentation without chat/designer memory.
18. **Remote Git truth.** No checkpoint is active/closed until exact remote compare + payload readback succeed.
19. **Cumulative integration is mandatory.** A local slice PASS never authorizes the next slice until Stage 0 + all accepted slices are tested together and any hardening is QA-closed.
20. **Architecture has no incumbency privilege.** When new integrated evidence changes material trade-offs, the selected representation mechanism must compete again against strong rejected and newly plausible alternatives.

---

## Stage-bound obligations inherited from Domain closure

### WD-03 — historical reconstruction

Current Domain verdict:

```text
PASS WITH HARDENING
```

Logical stage target:

> demonstrate material historical reconstruction against the integrated logical representation.

Slice A proves identity/reconciliation chronology but does not fully discharge WD-03; exact Version/Provenance history remains primarily Slice D + final regression.

Slice B adds explicit material-version/governed-by/approval-applicability requirements but likewise does not fully discharge WD-03.

Integrated A+B additionally requires stable distinction among semantic-record address and material-state address, plus auditability even when a standalone Request/Decision is intentionally omitted.

### WD-05 — persistence/API pressure

Current Domain verdict:

```text
PASS WITH HARDENING
```

Slice A proves identity/reference logical feasibility against realistic persistence/API pressure while deliberately retaining more than one physical implementation option.

Slice B proves intention/execution feasibility without requiring universal WorkItem/status/workflow storage and preserves several physical implementation options.

Integrated A+B reopens the representation-mechanism choice and retains/hardens it as a discriminated ReferenceAddress family rather than assuming the earlier NativeRef-only surface was enough.

Full WD-05 discharge remains integrated Whole-Logical work.

Neither target authorizes physical implementation.

---

## Logical gate framework

Current hardened methodology defines:

```text
LM-01 Semantic owner coverage
LM-02 Identity/reference preservation
LM-03 Lifecycle/state separation
LM-04 Historical reconstruction / WD-03
LM-05 Relation/governance specificity
LM-06 Multi-actor/selective visibility
LM-07 Provenance/reconciliation
LM-08 Simple-case compactness
LM-09 Specialist boundary
LM-10 No semantic-free fallback
LM-11 Reverse mapping
LM-12 High-value query feasibility
LM-13 Evolution/obsolescence resilience
LM-14 Scale/concurrency plausibility
LM-15 External benchmark/anti-pattern mining
LM-16 Persistence/API pressure / WD-05
LM-17 Traceability completeness
LM-18 Mutation / inverse-necessity survival
LM-19 Counterfactual distinguishability
LM-20 Decision / assumption integrity
LM-21 Cross-slice regression integrity
LM-22 Product Reality coherence
LM-23 Clean-room reconstructibility
LM-24 Cumulative Integrated Coherence
LM-25 Mechanism / Technology Reconsideration Integrity
```

The mandatory workflow is `LM-WF-01..21` with LM-WF-21 triggered when material trade-offs change.

---

## Permanent between-slice gate

After every slice:

```text
Slice N read-only design/falsification
-> bounded write gate
-> Slice N exact remote QA
-> CUMULATIVE INTEGRATED CHECKPOINT
   Stage 0 + Stage 0H + Slice A ... Slice N
-> if findings: classify + bounded hardening write
-> if mechanism trade-offs changed: LM-WF-21 TECHNOLOGY/MECHANISM RECONSIDERATION
-> exact remote QA
-> rerun cumulative checkpoint
-> only then Slice N+1 may start
```

Technology/mechanism reconsideration must include:

```text
current selected mechanism
strongest previously rejected-but-not-logically-impossible alternative(s)
new plausible mechanisms
fresh current structural/negative external evidence where material
```

Allowed verdicts:

```text
RETAIN
HARDEN
REPLACE
BLOCKED
```

At Logical Model stage `technology` means representation/architecture mechanism. The later Physical Model must repeat the same discipline for concrete database/API/runtime technologies.

---

## Logical roadmap

```text
STAGE 0
foundation / methodology / corpus / benchmark policy
REMOTE QA PASS

STAGE 0H
methodology hardening / ledgers / regression discipline
REMOTE QA PASS / ACTIVE

SLICE A
Identity / Reference
PASS WITH HARDENING
REMOTE QA PASS / ACTIVE

SLICE B
Intention / Execution
PASS WITH HARDENING
REMOTE QA PASS / ACTIVE

INTEGRATED CHECKPOINT A+B
READ-ONLY REVIEW COMPLETE
6 cross-slice hardenings classified
technology/mechanism reconsideration COMPLETE
WRITE COMPLETE
ACTIVATION CONDITIONAL ON CURRENT REMOTE QA

SLICE C
Time / Reality
HOLD — NOT STARTED

SLICE D
Evidence / Knowledge / History

SLICE E
Resources / Values / Capacity

SLICE F
Relationships / Multi-Actor / Governance

FINAL
Whole-Logical integrated regression
clean-room reconstruction
WD-03 discharge
WD-05 discharge
Logical closure
```

Slice grouping is operational only and does not create new semantic clusters.

---

## Slice A — Identity / Reference

### Read-only work completed

Required phases were completed before canonical write:

```text
A0 canonical reconstruction                         DONE
A1 identity/reference requirement + query corpus    DONE
A2 multiple candidate reference architectures       DONE
A3 native identity pressure                         DONE
A4 Actor/Subject/Resource role-reference pressure   DONE
A5 provider identity + reconciliation               DONE
A6 merge/split/correction/history                   DONE
A7 multi-actor/privacy                              DONE
A8 scale/evolution/external benchmark               DONE
A9 mutation/counterfactual/cross-slice regression   DONE
A10 reverse mapping + LM gate review                DONE
```

The assistant stopped before write, presented the complete result/candidate comparison to the user, and received explicit approval before the write gate was executed.

### Selected logical model

```text
Layered Typed Identity & Reference Model
```

Canonical separation:

```text
NATIVE IDENTITY
!= NativeRef / technical addressability
!= Reference Contract semantic meaning
!= ExternalRef / provider identity
!= Account / Principal identity
!= identity Reconciliation state
!= Version / material-state reference
!= disclosure/public correlation handle
```

Primary contract:

```text
native Domain owner identity
        ↓
logical NativeRef addressability
        ↓
slot/relation-specific Reference Contract

ExternalRef / Account / Principal
remain separate scoped identity spaces

Reconciliation/history
links identities without destructive semantic collapse
```

Critical hardenings:

```text
NativeRef != Entity / Thing
owner/type deterministically recoverable
native key opaque and non-reused
Reference Contract owns semantic target eligibility
polymorphic technical ref != any-object semantic relation
Actor / Subject / Resource do not create wrapper identity
not every valid role target requires native identity
ExternalRef != NativeRef
unresolved mapping is valid
identity merge/link is explicit, history-preserving and correctable
current identity resolution != historically always known
NativeRef != Version
internal native identity != universal public/API handle
referenceability != Visibility != Authority
shared native identity != per-actor duplicate canonical identity
physical representation remains open
```

Canonical Slice-A files:

```text
docs/logical-model/slices/identity-reference-v1.md
docs/logical-model/checkpoints/identity-reference-v1-validation.md
docs/logical-model/benchmarks/identity-reference-v1.md
```

Trace/register/framework/corpus/workstream integrate the same accepted contract.

### Slice-A effective state

The approved Slice-A scope passed exact remote QA before Slice-B work began.

```text
SLICE A — IDENTITY / REFERENCE
PASS WITH HARDENING
REMOTE QA PASS
ACTIVE

HEAD AFTER SLICE-A CHECKPOINT
30190d2f54d8e7a3bf079f1ae1d9dc910da2d392

DOMAIN REOPEN REQUIRED 0
```

---

## Slice B — Intention / Execution

### Read-only design/falsification completed

```text
B0  canonical reconstruction                         DONE
B1  requirements + high-value query corpus           DONE
B2  multiple candidate architectures                 DONE
B3  owner/identity/material-state pressure            DONE
B4  lifecycle + version/replacement pressure          DONE
B5  Proposal / Request / Decision pressure            DONE
B6  Dependency / Milestone / Routine pressure         DONE
B7  Product Reality + multi-actor pressure            DONE
B8  scale / evolution / broad external benchmark      DONE
B9  mutation / counterfactual / Slice-A regression    DONE
B10 reverse mapping + LM gate review                  DONE
```

### Selected candidate

```text
Layered Typed Intention & Execution Model
```

Core separation:

```text
semantic owner
!= material state/version
!= typed link / semantic act
!= occurrence/schedule/execution
!= Actual
!= Outcome
!= derived operational status
```

Primary dispositions after integrated hardening:

```text
retained canonical Possibility -> LR-01
Goal         -> LR-01
Plan         -> LR-01
canonical persisted Activity -> LR-01
canonical persisted Event    -> LR-01
Routine      -> LR-01
Milestone    -> normally LR-02
Proposal     -> LR-02 conditionally materialized
Request      -> LR-02 conditionally materialized
Decision     -> LR-02 conditionally materialized
Dependency   -> LR-03
```

Transient suggestions/import candidates remain pre-canonical until applicable semantics establish an owner.

Critical hardenings:

```text
no universal WorkItem/Intent/WorkflowNode root
no universal canonical lifecycle/status enum
Possibility maturation creates/links Goal; no historical retyping
Goal pursuit != evaluation/outcome
Plan revision != Plan replacement automatically
material replacement preserves predecessor history
owner identity != material state/version
Proposal/Request/Decision use selective materialization
Decision != effect
material target change may stale prior approval/Decision applicability
previously authorized policy effect != mandatory fresh Decision
explicit instruction may establish requester intent but never manufactures Authority/Consent
Dependency != hierarchy/order/DAG
Dependency endpoints bind relevant facet/state/result/transition where material
blocked/satisfied normally derived
Milestone date passage != attainment
Routine != Recurrence != Occurrence != Actual
execution may require governing material Plan/Routine/Policy state
AI candidate/proposal != user adoption/Decision
selective materialization != selective auditability
Possibility->Goal and Plan replacement use typed lineage
```

Canonical Slice-B files:

```text
docs/logical-model/slices/intention-execution-v1.md
docs/logical-model/checkpoints/intention-execution-v1-validation.md
docs/logical-model/benchmarks/intention-execution-v1.md
```

### Slice-B remote QA state

The approved Slice-B write gate already passed exact remote QA before this cumulative checkpoint began.

```text
SLICE B — INTENTION / EXECUTION
PASS WITH HARDENING
REMOTE QA PASS
ACTIVE

HEAD AFTER SLICE-B CHECKPOINT
5d7b3d35b529a80808c719c390bdf6df6e20a6b0

DOMAIN REOPEN REQUIRED 0
LOGICAL STRUCTURAL BLOCKER 0
```

---

## Integrated A+B checkpoint

### Why it ran

The user explicitly required that after each accepted logical slice the project review **everything completed so far together**, rather than moving immediately to the next slice.

Read-only cumulative review covered:

```text
Stage 0 + Stage 0H
Slice A
Slice B
cumulative invariants/tests
Product Reality
clean-room reconstruction
provider/history/privacy/scale pressure
```

### Findings

```text
AB-H01 canonical Activity/Event identity wording too permissive
AB-H02 persistent non-native semantic records lacked an explicit address-space category
AB-H03 Request/intention wording incorrectly risked manufacturing Authority
AB-H04 Dependency endpoint required material facet/state binding
AB-H05 selective materialization risked being misread as selective auditability
AB-H06 Possibility->Goal and Plan-replacement links required typed lineage classification
```

These findings did **not** demonstrate a Domain gap or failure of the Layered Typed architecture.

```text
DOMAIN REOPEN REQUIRED       0
NEW DOMAIN OWNER REQUIRED    0
STRUCTURAL REDESIGN          0
CROSS-SLICE HARDENINGS       6
```

### Hardened shared reference mechanism

Selected integrated representation:

```text
ReferenceAddress
=
  NativeRef
  OR ScopedRecordRef
  OR MaterialStateRef
  OR ExternalRef

+
Reference Contract
```

Meanings:

```text
NativeRef
independently justified native Domain identity

ScopedRecordRef
stable address for a materialized dependent/contextual semantic record
without native-referent promotion

MaterialStateRef
materially relevant target state/version
exact mechanism Slice D

ExternalRef
provider/source-scoped external identity
```

Non-collapse:

```text
ReferenceAddress != Entity / Thing / Object root
NativeRef != ScopedRecordRef != MaterialStateRef != ExternalRef
resolvable != semantically eligible
```

The Reference Contract owns target/address-variant eligibility and contextual semantic meaning.

### Technology/mechanism reconsideration

The addressability gap changed the representation constraints, so the newly formalized LM-WF-21 was applied immediately.

Reconsidered:

```text
TECH-AB-A owner-specific references only
TECH-AB-B global Node/Entity registry/interface
TECH-AB-C one undifferentiated TypedRef(kind,id)
TECH-AB-D discriminated ReferenceAddress family + Reference Contract
```

Current verdict:

```text
TECH-AB-D
SELECTED

MECHANISM / TECHNOLOGY
RETAIN + HARDEN
```

Owner-specific references remain a strong physical ingredient. A technical registry remains possible physically. A global semantic Node/Entity root and an undifferentiated address space remain rejected.

Current primary/official structural evidence includes FHIR typed/limited references and version-specific target pressure, Kubernetes object/UID/resourceVersion/fieldPath separation, PostgreSQL inheritance constraint limitations, and Relay GraphQL Node as a useful global-address but negative ontology benchmark.

External evidence is mechanism evidence, not LifeOS ontology authority.

### Permanent regression additions

```text
INV-085..INV-100
integrated invariants

TC-O01..TC-O10
integrated permanent scenarios

MUT-AB01..MUT-AB10
10 / 10 PASS

INTEGRATED COUNTERFACTUALS
9 / 9 PASS
```

Canonical checkpoint:

```text
docs/logical-model/checkpoints/integrated-a-b-v1-validation.md
```

---

## Integrated A+B approved write gate

```text
BRANCH
feature/logical-model

PRE-SCOPE
5d7b3d35b529a80808c719c390bdf6df6e20a6b0

CREATE
1

UPDATE
8

DELETE
0
```

CREATE:

```text
docs/logical-model/checkpoints/integrated-a-b-v1-validation.md
```

UPDATE:

```text
docs/logical-model/validation-methodology-v1.md
docs/logical-model/representation-framework-v1.md
docs/logical-model/slices/identity-reference-v1.md
docs/logical-model/slices/intention-execution-v1.md
docs/logical-model/traceability-and-regression-ledger-v1.md
docs/logical-model/decision-and-assumption-register-v1.md
docs/logical-model/test-corpus-v1.md
docs/workstreams/logical-model.md
```

Explicitly out of scope:

```text
Domain Model changes
Slice C design/write
SQL / physical tables
UUID/key choice
migrations
API/backend
AuthN/AuthZ runtime
frontend
main
exact MaterialStateRef persistence
exact Dependency expression language
```

---

## Integrated A+B remote activation condition

The checkpoint becomes active only if remote QA confirms:

```text
1 PRE-SCOPE immediately before first write was exactly
  5d7b3d35b529a80808c719c390bdf6df6e20a6b0

2 compare from PRE-SCOPE contains exactly 9 approved paths
3 added = 1
4 modified = 8
5 deleted = 0
6 unexpected = 0
7 all 9 final payloads fetched/read remotely
8 branch behind_by = 0 from PRE-SCOPE
9 main remains 068da4cc66620b3f3811051170e4913097091a04
```

When satisfied:

```text
INTEGRATED A+B
PASS WITH HARDENING
REMOTE QA PASS
ACTIVE

LM-24
PASS WITH HARDENING / CLOSED FOR A+B

LM-25
PASS — RETAIN + HARDEN

DOMAIN REOPEN REQUIRED 0
LOGICAL STRUCTURAL BLOCKER 0

SLICE C
READY FOR DISTINCT READ-ONLY START
NOT STARTED AUTOMATICALLY
```

---

## Current out-of-scope boundary

Until Logical Model closure, do **not** start:

```text
SQL DDL
migrations
ORM entities as canonical design
API resource implementation
backend services
AuthN/AuthZ runtime implementation
physical indexing/partitioning decisions
frontend/prototype changes
```

Physical feasibility may be researched/tested conceptually when needed, but no physical representation becomes authoritative before the logical gate passes.
