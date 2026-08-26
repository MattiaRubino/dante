# DANTE Logical Model

**Status:** CURRENT / AUTHORITATIVE ENTRY POINT  
**Logical Model verdict:** CLOSED / REMOTE QA PASS  
**Closure date:** 2026-08-17  
**Domain carry-forward:** WD-03 PASS; WD-05 PASS; no Domain reopen required

## 1. Current truth

The integrated Logical Model is closed.

Canonical closure evidence:

- [`checkpoints/whole-logical-v1-remote-qa.md`](checkpoints/whole-logical-v1-remote-qa.md)

Activated result:

```text
WHOLE-LOGICAL A+B+C+D+E+F
CORE ARCHITECTURE HOLDS
PASS WITH HARDENING
REMOTE QA PASS
ACTIVE

OWNER CENSUS                      57 / 57
WHOLE HARDENINGS                       12
FRESH WHOLE MUTATIONS            40 / 40 REJECTED
FRESH WHOLE COUNTERFACTUALS      26 / 26 DISTINGUISHED
DOMAIN OWNER GAP                       0
DOMAIN REOPEN REQUIRED                 0
NEW DOMAIN OWNER REQUIRED              0
UNIVERSAL ROOT REQUIRED                0
CROSS-SLICE REGRESSION FAILURE         0
STRUCTURAL REDESIGN                    0

WD-03 PASS
WD-05 PASS

LOGICAL MODEL
CLOSED
```

The Domain Model remains closed for the accepted kernel.

## 2. Authority and reading order

For the current Logical Model, read in this order:

1. this README for current status and navigation;
2. [`whole-logical-model-v1.md`](whole-logical-model-v1.md) for the integrated 57-owner representation contract and WL-H01..WL-H12;
3. [`checkpoints/whole-logical-v1-validation.md`](checkpoints/whole-logical-v1-validation.md) for Whole validation evidence;
4. [`checkpoints/whole-logical-v1-remote-qa.md`](checkpoints/whole-logical-v1-remote-qa.md) for closure activation and final status;
5. [`benchmarks/whole-logical-v1.md`](benchmarks/whole-logical-v1.md) and other benchmark/checkpoint records for supporting evidence;
6. accepted Domain specifications remain the semantic authority above logical representation.

Important lifecycle rule:

> `whole-logical-model-v1.md` was written before its separately gated remote-QA closure, so its original status banner records the pre-activation state. The later remote-QA closure is the authoritative activation evidence. The technical payload of the Whole file remains canonical.

Do not interpret `PENDING REMOTE QA`, `CLEARANCE READY` or `NOT YET CLOSED` inside pre-closure content as the current repository state after the closure record activated successfully.

## 3. Core current representation contract

The integrated model classifies all accepted Domain concepts through bounded logical roles rather than universal semantic superclasses.

```text
LR-01 Native identity-bearing record
LR-02 Dependent/material contextual record
LR-03 Specific typed association/relation
LR-04 Value semantics
LR-05 Rule/policy/specification
LR-06 Realization/result semantics
LR-07 Version/correction/lineage/history
LR-08 Derived/effective projection/read model
LR-09 Provider/external state and mapping
LR-10 Flexible low-consequence descriptive metadata
LR-11 Unresolved/candidate interpretation
LR-12 Product/organizational profile
LR-13 Specialist extension record
```

The accepted native LR-01 owner set is:

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

`Actor`, `Subject` and `Resource` remain contextual roles/capabilities, not wrapper identities.

## 4. Whole hardenings retained downstream

WL-H01..WL-H12 remain active logical contracts:

```text
WL-H01 Agreement terms material owner/state
WL-H02 Governed Operation / Effect Contract
WL-H03 Projection / Disclosure Surface Contract
WL-H04 absence != false
WL-H05 expected-state / optimistic concurrency
WL-H06 idempotency != identity
WL-H07 multi-owner atomicity / explicit staged reconciliation
WL-H08 canonical state != provider sync state
WL-H09 LR-08 freshness / consequential revalidation
WL-H10 retention / redaction / tombstone integrity
WL-H11 consequential AuthZ provenance
WL-H12 non-interference / inference leakage
```

Later physical/database/backend implementation must preserve these contracts. Shared technical structures do not create generic Domain semantics.

## 5. Split-document classification

The Logical Model contains several chronological continuation families produced during staged validation, including the decision/assumption register and representation/test/traceability ledgers through `part-9`.

Current rule:

- the final Whole model + Whole validation + remote-QA closure establish the integrated current result;
- continuation families remain **REFERENCE / EVIDENCE** according to their content and are not independent project-status authorities;
- a higher `part-N` number does not automatically outrank a later consolidated closure document;
- compaction/removal is allowed only after lossless knowledge coverage is proven for that complete logical family.

In particular, do not delete the `decision-and-assumption-register-v1-part-*`, representation, test-corpus or traceability parts merely because the Whole closure exists: they contain rationale, test cases and decision evidence that may not be duplicated verbatim by the Whole summary.

## 6. Transition boundary

Logical closure does not retroactively make every physical choice part of the Logical Model.

The Whole closure handed forward a preferred benchmark posture:

```text
PostgreSQL hybrid
current preferred physical baseline

TypeDB
mandatory physical-model benchmark challenger

Neo4j / event / document mechanisms
bounded or secondary candidates where justified

Generic EAV / generic edge / meta-model
hard reject
```

Concrete physical/database decisions belong to their later accepted Physical Model, ADR and backend/database contracts.

## 7. Reopening rule

Reopen the Logical Model only if later accepted requirements or implementation evidence expose an actual contradiction with the 57-owner mapping, WL-H01..WL-H12, material history reconstruction, specific relation semantics, multi-actor disclosure, provider separation or another accepted invariant.

Implementation convenience, ORM/table shape or provider schemas are not sufficient reasons to redefine logical/domain truth silently.
