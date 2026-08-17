<!-- LIFEOS-CANONICAL-CONTINUATION document="logical-model.md" follows="logical-model-part-4.md" -->
> **Canonical continuation of `docs/workstreams/logical-model.md`.** This Part 5 records the Integrated A+B+C+D checkpoint.

# Logical Model Workstream — Part 5

**Date:** 2026-08-17  
**Branch:** `feature/logical-model`

## Entry state

```text
Slice A ACTIVE
Slice B ACTIVE
Slice C ACTIVE
Slice D ACTIVE
Slice-D closure HEAD 54d7b2c8c280e78f1fdb4bd07549d602be284ca3
```

Slice E remains blocked pending Integrated A+B+C+D closure.

## Integrated findings

```text
ABCD-H01 knowledge-current != world-current/applicable-now
ABCD-H02 unknown applicability must remain representable
ABCD-H03 not currently applicable != irrelevant forever
ABCD-H04 point Observation / AI inference cannot silently become continuing canonical state
```

## Architecture result

```text
Layered Typed model
RETAIN + HARDEN

ReferenceAddress
RETAIN + HARDEN

MaterialStateRef
RETAIN + HARDEN

Universal bitemporal Fact root
REJECTED
```

Bitemporal/event/snapshot/owner-history techniques remain Physical Model candidates.

## New regression range

```text
INV-179..190
TC-S01..S12
MUT-ABCD01..12
CF-ABCD01..08
```

## WD-03

```text
A+B+C+D SCOPE
PASS WITH HARDENING

FINAL WHOLE-LOGICAL DISCHARGE
DEFERRED UNTIL E/F + FINAL REGRESSION
```

## Proposed integrated write scope

```text
CREATE 8
UPDATE 0
DELETE 0
```

Paths:

```text
docs/logical-model/checkpoints/integrated-a-b-c-d-v1-validation.md
docs/logical-model/slices/evidence-knowledge-history-v1-part-2.md
docs/logical-model/benchmarks/integrated-a-b-c-d-v1.md
docs/logical-model/representation-framework-v1-part-5.md
docs/logical-model/test-corpus-v1-part-5.md
docs/logical-model/traceability-and-regression-ledger-v1-part-5.md
docs/logical-model/decision-and-assumption-register-v1-part-5.md
docs/workstreams/logical-model-part-5.md
```

Out of scope:

```text
Slice E design
Domain changes
SQL/migrations
API/backend
main
physical history technology selection
```

## Next step

After exact remote compare/readback and closure of Integrated A+B+C+D:

```text
Slice E — Resources / Values / Capacity
may begin read-only
```

Do not begin Slice E before the integrated closure.