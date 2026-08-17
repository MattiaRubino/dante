# Logical Model Workstream

**Status:** Stage 0 foundation — remote QA pending  
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
6. accepted slice decisions created by this workstream;
7. current external evidence under `docs/logical-model/external-benchmark-policy-v1.md`.

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

## Stage-0 foundation scope

Approved initial foundation write scope:

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

Stage 0 intentionally contains no concrete owner mapping and no table/schema design.

---

## Foundational operating rules

### 1. Domain Atlas is authoritative

Logical discomfort is not semantic evidence by itself.

A Domain reopen requires the strict evidence bar in `validation-methodology-v1.md`.

### 2. Falsification before acceptance

Every material logical candidate is attacked before optimization.

### 3. Multiple candidate representations

Where materially different options exist, compare at least two before acceptance.

### 4. Retroactive regression

Every later slice reruns earlier scenarios it can affect.

A locally correct slice may still fail integrated regression.

### 5. Fresh external research

Benchmark direct, adjacent, specialist and infrastructure systems relevant to the problem.

Search beyond superficially similar LifeOS apps when another domain has solved the same structural problem better.

### 6. External evidence is not authority

Borrow mechanisms/invariants where useful; do not copy ontology/schema by popularity.

### 7. Negative benchmarks are mandatory

Record external behaviors LifeOS must explicitly reject, not only patterns to adopt.

### 8. Simple cases stay simple

Internal semantic precision must not force unnecessary standalone records/UI complexity for trivial cases.

### 9. No semantic-free escape hatch

Required meaning cannot be hidden in generic relations/properties/JSON because classification is inconvenient.

### 10. Remote Git truth

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

Current methodology defines:

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
```

Verdicts and reopen rules are normative in `docs/logical-model/validation-methodology-v1.md`.

---

## Initial slice roadmap

```text
STAGE 0
foundation / methodology / corpus / benchmark policy

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
WD-03 discharge
WD-05 discharge
Logical closure
```

Slice grouping is operational only and does not create new semantic clusters.

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

## Exact next step after Stage-0 remote QA

Begin **Slice A — Identity / Reference** in read-only analysis first.

Required first pass:

1. reconstruct current canonical semantics for Person, Actor/Account boundary, Living Referent, Asset, Place, Content Artifact, Collective identity pressure, Subject/Resource roles and provider identity mapping;
2. define high-value identity/reference queries;
3. research current direct/adjacent/specialist/infrastructure identity patterns;
4. propose multiple logical reference/identity candidates;
5. falsify candidates using test corpus;
6. run reverse mapping;
7. present result before Git write.

Do not start Slice B automatically after Slice A closure without a distinct gate.

---

## Stage-0 acceptance condition

Stage 0 becomes the active Logical Model baseline only after:

```text
feature/logical-model starts from main 068da4cc...
exactly 5 approved CREATE paths exist
0 UPDATE
0 DELETE
0 unexpected paths
remote compare is clean
all 5 payloads are remotely fetched/read
main remains unchanged
```

Until then:

```text
LOGICAL MODEL STAGE 0
REMOTE QA PENDING
```
