<!-- LIFEOS-CANONICAL-CONTINUATION document="deferred-dependency-closure-clusters-1-4-v0.md" follows="deferred-dependency-closure-clusters-1-4-v0-part-13.md" -->
> **Canonical continuation of the single logical Clusters 1–4 deferred dependency closure register.** Earlier classifications remain preserved; this continuation records the final Money / MonetaryAmount resolution produced by the Whole-Domain repair.

# 2026-08-16 — Money / MonetaryAmount final resolution

The historical Quantity and Observation boundaries correctly refused to collapse Money into ordinary scalar-unit semantics, but retained Money / MonetaryAmount as a transition-stage dependency question.

The Whole-Domain audit promoted that dependency to **REQUIRED NOW** because current LifeOS V1 needs truthful budget, cost, price, affordability and multi-currency planning/evaluation semantics.

V3 result:

```text
MonetaryAmount
REUSABLE CURRENCY-AMOUNT VALUE SEMANTICS
PASS WITH HARDENING

amount + unambiguous currency
NO independent native identity/root

FX conversion
contextual derived operation under applicable basis
NOT ordinary Quantity unit conversion
```

Historical deferred resolution:

```text
Quantity ↔ Money / MonetaryAmount
HISTORICAL SAFE-DEFER CANDIDATE
→ FINAL RESOLUTION: REQUIRED BY CURRENT LIFEOS CORE
→ MonetaryAmount accepted
→ Quantity boundary preserved
→ CLOSED

Observation ↔ Money / MonetaryAmount
HISTORICAL SEPARATE DEPENDENCY QUESTION
→ FINAL RESOLUTION: ALREADY COMPOSABLE AFTER MonetaryAmount ACCEPTANCE
→ Observation may use MonetaryAmount as value semantics
→ CLOSED
```

Resolved dependencies:

```text
MonetaryAmount ↔ Quantity                RESOLVED
MonetaryAmount ↔ Resource                RESOLVED
MonetaryAmount ↔ Observation             RESOLVED
MonetaryAmount ↔ Actual                  RESOLVED
MonetaryAmount ↔ Evidence/Provenance     RESOLVED
MonetaryAmount ↔ Criterion/Evaluation    RESOLVED
MonetaryAmount ↔ Decision/history        RESOLVED WITH HARDENING
MonetaryAmount ↔ Visibility/Multi-Actor  RESOLVED WITH HARDENING
MonetaryAmount ↔ FX                      RESOLVED WITH HARDENING
```

Definitive specialist/kernel boundary:

```text
FinancialAccount / ledger / transaction lifecycle
accounting classification
settlement / tax / securities / trading / portfolio semantics
generalized crypto/token/points instruments

→ SPECIALIST / OUTSIDE CURRENT GENERAL KERNEL
→ NOT SEMANTIC DEFERRED
```

Engineering-stage concerns:

```text
decimal precision/scale
minor-unit storage
rounding algorithms
FX provider/API/caching
persistence/query/API shape

→ LATER ENGINEERING OWNERSHIP
→ NOT SEMANTIC DEBT
```

No semantic deferred item is created by this repair.

```text
MONETARY AMOUNT
SEMANTIC SAFE DEFERRED 0
SEMANTIC UNCLASSIFIED  0
SEMANTIC UNRESOLVED     0
STRUCTURAL REOPEN       0
```

Whole-Domain REQUIRED NOW semantic repair inventory is now exhausted:

```text
Place             RESOLVED
Content Artifact  RESOLVED
MonetaryAmount    RESOLVED

REQUIRED NOW unresolved 0
```

The Whole-Domain audit itself remains open until post-write QA and the full WD-01..07 rerun pass.

Normative reference: `monetary-amount-v0-validation.md`.