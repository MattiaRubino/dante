# Logical Model Workstream

**Status:** Stage 0 remote QA PASS — Stage 0H hardening activation conditional on remote QA  
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
8. accepted slice decisions created by this workstream;
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

## Stage-0 foundation scope and completed QA

Initial foundation write scope:

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

Verified remote result from base main:

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

Stage 0 intentionally contains no concrete owner mapping and no table/schema design.

---

## Stage-0H methodology hardening scope

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

CREATE:

```text
docs/logical-model/traceability-and-regression-ledger-v1.md
docs/logical-model/decision-and-assumption-register-v1.md
```

UPDATE:

```text
docs/logical-model/validation-methodology-v1.md
docs/logical-model/test-corpus-v1.md
docs/logical-model/representation-framework-v1.md
docs/workstreams/logical-model.md
```

Purpose:

```text
elevate Logical Model validation beyond Domain V3 baseline
mandatory traceability matrix + invariant ledger
mutation/destructive testing
counterfactual testing
cross-slice regression
rejected-alternative register
assumption/freshness register
simple-case vs worst-case pairing
Product Reality / cross-domain retrieval pressure
final clean-room reconstruction
record Stage-0 remote QA PASS
```

Explicitly out of scope:

```text
Domain Atlas changes/reopen
Slice A mapping decisions
SQL / schema / migrations
API / backend / AuthN/AuthZ
frontend
main
```

---

## Foundational operating rules

### 1. Domain Atlas is authoritative
Logical discomfort is not semantic evidence by itself. A Domain reopen requires the strict evidence bar in `validation-methodology-v1.md`.

### 2. Falsification before acceptance
Every material logical candidate is attacked before optimization.

### 3. Multiple candidate representations
Where materially different options exist, compare at least two before acceptance.

### 4. Mandatory traceability
Every material Domain owner/invariant must trace to logical representation, query/operation, tests and verdict.

### 5. Cumulative invariant ledger
A passed invariant remains part of later regression pressure; later slices cannot silently weaken it.

### 6. Mutation / destructive testing
Remove, merge, genericize, overwrite or provider-identify structures to prove why distinctions matter.

### 7. Counterfactual testing
Near-identical cases with different accepted meaning must remain logically distinguishable.

### 8. Retroactive / cross-slice regression
Every later slice reruns earlier scenarios/invariants it can affect. A locally correct slice may still fail integrated regression.

### 9. Rejected alternatives are preserved
A selected candidate must be compared with plausible alternatives and failed alternatives remain documented with rationale.

### 10. Assumptions are explicit
Material decisions cannot depend on hidden, stale or unproven assumptions.

### 11. Fresh external research
Benchmark direct, adjacent, specialist and infrastructure systems relevant to the problem, including structurally useful systems outside the obvious product category.

### 12. External evidence is not authority
Borrow mechanisms/invariants where useful; do not copy ontology/schema by popularity.

### 13. Negative benchmarks are mandatory
Record external behaviors LifeOS must explicitly reject, not only patterns to adopt.

### 14. Simple and worst cases both matter
Internal precision must not make trivial use pathological, while simple-case elegance must not fail under long history/scale/multi-actor/provider conflict.

### 15. Product Reality cases are tests, not commands
Concrete desired behaviors are classified into Domain coverage, Logical requirement, capability/algorithm gap, specialist boundary or true semantic contradiction.

### 16. No semantic-free escape hatch
Required meaning cannot be hidden in generic relations/properties/JSON because classification is inconvenient.

### 17. Clean-room closure
Final Logical Model meaning must be reconstructible from canonical documentation without designer memory/chat context.

### 18. Remote Git truth
No logical checkpoint is CLOSED/PASS until remote compare and actual payload readback succeed.

---

## Stage-bound obligations inherited from Domain closure

### WD-03 — historical reconstruction

Current Domain verdict:

```text
PASS WITH HARDENING
```

Logical stage obligation:

> demonstrate material historical reconstruction against the actual integrated logical representation.

Target:

```text
WD-03 PASS
```

### WD-05 — persistence/API pressure

Current Domain verdict:

```text
PASS WITH HARDENING
```

Logical stage obligation:

> pressure-test the actual integrated logical representation against identity, history, semantic boundaries, multi-actor state, provider mapping and high-value operations.

Target:

```text
WD-05 PASS
```

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
```

The mandatory workflow is LM-WF-01..19.

Verdicts and reopen rules are normative in `docs/logical-model/validation-methodology-v1.md`.

---

## Logical roadmap

```text
STAGE 0
foundation / methodology / corpus / benchmark policy
REMOTE QA PASS

STAGE 0H
methodology hardening / ledgers / regression discipline
activation conditional on remote QA

SLICE A
Identity / Reference

SLICE B
Intention / Execution

SLICE C
Time / Reality

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

## Slice A — exact read-only start

Slice A may begin read-only once Stage 0 is active. No Slice A decision is created by Stage 0H hardening.

Pressure owners/families:

```text
Person
Living Referent
Asset
Place
Content Artifact
Collective
Actor role
Subject role
Resource role
Account / Principal boundary
provider identity mapping
```

Primary question:

> How can LifeOS share technical identity/reference infrastructure across independently meaningful native referents and contextual roles without creating a universal semantic Entity/Thing root or parallel role-wrapper identities?

Required phases:

```text
A0 canonical reconstruction
A1 identity/reference query + requirement corpus
A2 multiple candidate reference architectures
A3 native identity pressure
A4 Actor/Subject/Resource role-reference pressure
A5 provider identity + reconciliation
A6 merge/split/correction/history
A7 multi-actor/privacy
A8 scale + external benchmark
A9 mutation/counterfactual/cross-slice regression
A10 reverse mapping + LM gate verdict
```

No Slice A write occurs until the read-only evidence/candidates are presented under a separate explicit gate.

---

## Stage-0 external calibration already performed

Current official documentation was checked to seed the benchmark policy with positive and negative patterns including:

```text
Google Calendar
recurring master / instance / originalStartTime separation

Todoist
work date != fixed deadline
floating time != fixed timezone-aware time

Motion
adaptive schedule derived from constraints/availability

Reclaim
recurring default != adaptive conflict policy != scheduled instance
negative case: elapsed scheduled task event may be assumed done

Notion
flexible property/relation/rollup mechanisms
without making them LifeOS semantic authority

Plaid
pending/posting specialist linkage pressure

Odoo Inventory
physical count != inventory movement/adjustment lifecycle

FHIR Provenance
version-specific lineage/history pressure
```

These are calibration evidence only; every slice must refresh the external set relevant to its own decisions.

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

---

## Stage-0H activation condition

No additional write is required to activate Stage 0H if the following remote conditions are all satisfied:

```text
1 branch PRE-SCOPE was exactly 3dc8fdb869e445b84255fb881c0e11da76cf2a43 before first write
2 compare from PRE-SCOPE shows exactly 6 approved physical paths
3 added = 2
4 modified = 4
5 deleted = 0
6 unexpected = 0
7 all 6 current payloads are fetched/read remotely
8 main remains 068da4cc66620b3f3811051170e4913097091a04
```

When satisfied, this document's effective current state is:

```text
LOGICAL MODEL STAGE 0
REMOTE QA PASS

LOGICAL MODEL STAGE 0H
HARDENED FOUNDATION
REMOTE QA PASS
ACTIVE

NEXT
SLICE A — IDENTITY / REFERENCE
READ-ONLY ANALYSIS
```
