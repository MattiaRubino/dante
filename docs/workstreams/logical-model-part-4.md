<!-- LIFEOS-CANONICAL-CONTINUATION document="logical-model.md" follows="logical-model-part-3.md" -->
> **Canonical continuation of `docs/workstreams/logical-model.md`.** This is Part 4 of the same logical handoff and records Slice-D Evidence / Knowledge / History progress.

# Logical Model Workstream — Part 4

**Date:** 2026-08-17  
**Branch:** `feature/logical-model`

## Entry state

```text
Stage 0 / 0H ACTIVE
Slice A ACTIVE
Slice B ACTIVE
Integrated A+B ACTIVE
Slice C ACTIVE
Integrated A+B+C ACTIVE
Entry HEAD 8fd619b5c2d7f8d51a12a8aa7ba378e81ac7d568
```

Slice D was permitted to begin read-only only after Integrated A+B+C remote closure.

---

## Slice D objective

Establish a logical representation for evidence, knowledge and history that supports durable cross-domain personal context, correction, lineage, evaluation and historical reconstruction without creating a universal Fact/Claim/Version/Event root or pre-selecting one physical history technology.

Scope owners/pressures:

```text
Observation
Actual / Outcome history
Version / Material-State
Provenance
Evidence
Confirmation
Acknowledgement
Criterion / Evaluation / Verification
Reconciliation / Source Precedence
current/historical knowledge projection
world/effective vs knowledge chronology
applicability of ongoing/temporary/resolved/intermittent state
provider/AI/import lineage
privacy/retention
```

---

## Selected Slice-D candidate

```text
Layered Typed Epistemic & History Model
LOCAL PASS WITH HARDENING
```

Key dispositions:

```text
Observation -> LR-01 + NativeRef
Actual -> LR-02 + LR-06
MaterialStateRef -> precise target-state contract
Provenance -> LR-07 + typed lineage
Evidence -> LR-03 evaluative-use relation
Confirmation -> LR-03 target-state attestation
Acknowledgement -> LR-03 target-state common-ground attestation
Criterion -> LR-05
Evaluation -> LR-08; consequential snapshot may be LR-02
Verification -> Evaluation purpose/profile
qualified Reconciliation -> LR-02/LR-07 only where materially recorded
knowledge/retrieval memory -> LR-08
```

No `FactRef`, `AssertionRef`, universal `Version`, `Attestation`, `Knowledge` or event root is added.

---

## Applicability hardening added before write

Product pressure:

```text
celiac / durable condition context
broken leg / temporary injury episode
fever / point observation or bounded temporary episode
```

Result:

```text
historical record exists != currently applicable
ongoing != bounded episode
resolved != deleted
unknown end != permanent
intermittent/recurrent != continuously active
point Observation != continuing condition automatically
```

The shared kernel contract preserves effective applicability/history; owner/specialist semantics own the actual lifecycle/status vocabulary.

This hardening is part of Slice D, not deferred to a future patch.

---

## Mechanism reconsideration

LM-WF-21 reopened:

```text
Universal Fact / Claim graph
Universal event-sourced/bitemporal ledger
Fully owner-specific history
Global PROV-like lineage graph
Layered Typed Epistemic & History
```

Current result:

```text
Layered Typed Epistemic & History SELECTED
ReferenceAddress RETAIN + HARDEN
MaterialStateRef HARDENED
```

Alternative technologies remain eligible as bounded Physical Model ingredients. They receive no incumbency or exclusion solely from this Logical verdict.

---

## External benchmark families checked

Fresh official/primary evidence was used from:

```text
W3C PROV
W3C Verifiable Credentials 2.0
HL7 FHIR R5 Provenance / Condition / Observation
Wikidata statement/reference/rank model
SQL Server system-versioned temporal tables
Datomic history/as-of
Apache Iceberg snapshots/branches/tags
OpenLineage
```

External systems remain mechanism/anti-pattern evidence rather than LifeOS ontology authority.

---

## Validation state before remote write

```text
D0 canonical reconstruction                    DONE
D1 query/requirement corpus                    DONE
D2 candidate architectures                     DONE
D3 identity / MaterialStateRef pressure         DONE
D4 Observation/source/assertion pressure        DONE
D5 Provenance/Confirmation/Acknowledgement      DONE
D6 Evidence/Criterion/Evaluation/Verification   DONE
D7 Reconciliation/current-knowledge pressure    DONE
D8 scale/evolution/external benchmark           DONE
D9 mutation/counterfactual/A+B+C regression     DONE
D10 reverse mapping / local review              DONE

MUTATION FAIL                                  0
COUNTERFACTUAL FAIL                            0
HISTORICAL REPLAY FAIL                         0
A+B+C REGRESSION FAIL                          0
DOMAIN REOPEN REQUIRED                         0
NEW DOMAIN OWNER REQUIRED                      0
LOGICAL STRUCTURAL BLOCKER                     0
```

---

## WD-03 position

```text
WD-03 historical reconstructibility
LOGICAL MECHANISM SUBSTANTIVELY ESTABLISHED BY SLICE D
FINAL DISCHARGE NOT YET AUTHORIZED
```

Required before final PASS:

```text
Integrated A+B+C+D checkpoint
Slice E/F regressions
Whole-Logical final regression
```

---

## Remote activation gate

Slice D becomes ACTIVE only after exact remote QA proves the approved file set and reads back every payload.

Approved write scope from entry HEAD:

```text
CREATE 8
UPDATE 0
DELETE 0
```

Expected paths:

```text
docs/logical-model/slices/evidence-knowledge-history-v1.md
docs/logical-model/checkpoints/evidence-knowledge-history-v1-validation.md
docs/logical-model/benchmarks/evidence-knowledge-history-v1.md
docs/logical-model/representation-framework-v1-part-4.md
docs/logical-model/test-corpus-v1-part-4.md
docs/logical-model/traceability-and-regression-ledger-v1-part-4.md
docs/logical-model/decision-and-assumption-register-v1-part-4.md
docs/workstreams/logical-model-part-4.md
```

Out of scope:

```text
Domain changes
Slice E
SQL/migrations
API/backend
AuthN/AuthZ enforcement
frontend
main
physical history technology selection
retention implementation
specialist clinical schema
```

---

## Next mandatory step after Slice-D remote activation

Do **not** start Slice E immediately.

Run:

```text
INTEGRATED A+B+C+D
Stage 0 + Stage 0H + A + B + C + D

replay INV-001..178
cross-slice regression
Product Reality memory/applicability
historical reconstruction
MaterialStateRef pressure
mechanism/technology reconsideration if triggered
hardening if required
exact remote QA
```

Only after Integrated A+B+C+D remote closure may Slice E — Resources / Values / Capacity begin read-only.