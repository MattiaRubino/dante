# Logical Model Workstream

**Status:** Stage 0 + Stage 0H remote QA PASS — Slice A activation conditional on remote QA  
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

The active validation standard is:

```text
LM-WF-01..19
LM-01..23
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

### WD-05 — persistence/API pressure

Current Domain verdict:

```text
PASS WITH HARDENING
```

Slice A proves identity/reference logical feasibility against realistic persistence/API pressure while deliberately retaining more than one physical implementation option. Full WD-05 discharge remains integrated Whole-Logical work.

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

The mandatory workflow is `LM-WF-01..19`.

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
WRITE COMPLETE
ACTIVATION CONDITIONAL ON REMOTE QA

SLICE B
Intention / Execution
NOT STARTED BY SLICE-A WRITE

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

Canonical Slice-A files after successful activation:

```text
docs/logical-model/slices/identity-reference-v1.md
docs/logical-model/checkpoints/identity-reference-v1-validation.md
docs/logical-model/benchmarks/identity-reference-v1.md
docs/logical-model/traceability-and-regression-ledger-v1.md
docs/logical-model/decision-and-assumption-register-v1.md
docs/logical-model/test-corpus-v1.md
docs/logical-model/representation-framework-v1.md
docs/workstreams/logical-model.md
```

### Candidate comparison

```text
Universal semantic Entity/Object root
REJECTED LOGICALLY

Owner/role-specific reference families only
VIABLE STRONG ALTERNATIVE
not selected as logical baseline; retained as physical ingredient/retest comparator

Mandatory global identity registry as logical root
REJECTED AS LOGICAL REQUIREMENT
technical anchor/registry remains possible physically

Layered Typed Identity & Reference Model
SELECTED — PASS WITH HARDENING
activation conditional on remote QA
```

### Broad external benchmark

Slice A deliberately researched large systems and unrelated domains, using current official/primary documentation, including:

```text
OpenID Connect
SCIM
Auth0
Sign in with Apple
Microsoft Entra
Microsoft Graph / Outlook
FHIR
Salesforce
Shopify
Asana
Atlassian ARI
AWS ARN
OCI OCID
Kubernetes
Git
GitHub GraphQL
Google People
Wikidata
Home Assistant
Twilio
PostgreSQL
```

The adopted LifeOS model is a synthesis of transferable structural lessons, not a vendor schema copy.

Benchmark evidence is canonical in:

```text
docs/logical-model/benchmarks/identity-reference-v1.md
```

### Traceability / regression state

```text
TA-01..TA-17
Slice-A trace entries

INV-041..INV-060
Slice-A invariant additions

TC-M01..TC-M12
new permanent Slice-A regression scenarios

REGRESSION IMPACT
R3 WHOLE-LOGICAL

DOMAIN REOPEN REQUIRED
0
```

### Physical decisions deliberately deferred

```text
technical anchor/registry vs owner-specific FK vs typed composite vs hybrid
native key technology/data type
indexing/partitioning
ORM mapping
API/public identity-handle format
runtime authorization enforcement
```

PostgreSQL inheritance/global-parent-table behavior is not assumed to solve heterogeneous referential integrity.

---

## Slice-A approved write gate

```text
BRANCH
feature/logical-model

PRE-SCOPE
0076b02715acf418cd9ef2840ed719b4201c8730

CREATE
3

UPDATE
5

DELETE
0
```

CREATE:

```text
docs/logical-model/slices/identity-reference-v1.md
docs/logical-model/checkpoints/identity-reference-v1-validation.md
docs/logical-model/benchmarks/identity-reference-v1.md
```

UPDATE:

```text
docs/logical-model/traceability-and-regression-ledger-v1.md
docs/logical-model/decision-and-assumption-register-v1.md
docs/logical-model/test-corpus-v1.md
docs/logical-model/representation-framework-v1.md
docs/workstreams/logical-model.md
```

Explicitly out of scope:

```text
Domain Model changes
SQL / physical tables
UUID/key choice
registry/FK implementation
migrations
API/backend
AuthN/AuthZ runtime
frontend
main
Slice B
```

---

## Slice-A remote activation condition

No status-only write is required if all conditions below are satisfied:

```text
1 PRE-SCOPE immediately before first write was exactly
  0076b02715acf418cd9ef2840ed719b4201c8730

2 compare from PRE-SCOPE contains exactly 8 approved paths

3 added = 3
4 modified = 5
5 deleted = 0
6 unexpected = 0
7 all 8 current payloads are fetched/read remotely
8 main remains 068da4cc66620b3f3811051170e4913097091a04
```

When satisfied, effective state becomes:

```text
SLICE A — IDENTITY / REFERENCE
PASS WITH HARDENING
REMOTE QA PASS
ACTIVE

DOMAIN REOPEN REQUIRED 0
LOGICAL STRUCTURAL BLOCKER 0

NEXT
SLICE B — INTENTION / EXECUTION
READ-ONLY ONLY AFTER DISTINCT CONTINUATION AUTHORIZATION
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
