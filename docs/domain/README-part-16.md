<!-- LIFEOS-CANONICAL-CONTINUATION document="README.md" follows="README-part-15.md" -->
> **Canonical continuation of the single logical Domain Atlas README.** Earlier index/status entries remain preserved; this continuation records MonetaryAmount v0 only.

# 2026-08-16 — MonetaryAmount v0

Whole-Domain repair status:

```text
MonetaryAmount
PASS WITH HARDENING
semantic propagation written/in progress
repository closure pending remote QA
```

Accepted domain result:

```text
MonetaryAmount
= REUSABLE CURRENCY-AMOUNT VALUE SEMANTICS
= numerical amount + unambiguous currency semantics

NEW NATIVE REFERENT
NO

NEW VALUE SEMANTICS
YES
```

Key boundaries:

```text
MonetaryAmount != Quantity
MonetaryAmount != Subject
MonetaryAmount != Resource
MonetaryAmount != Budget / Price / Cost / Estimate / Balance
MonetaryAmount != Transaction / FinancialAccount
MonetaryAmount != Observation / Actual / Evidence / Provenance
FX rate != MonetaryAmount
```

Cross-currency derivation requires an applicable conversion basis and does not mutate source amount. Current FX does not rewrite historical FX basis; reference estimate does not automatically equal executed charge.

Canonical concept:
- `concepts/monetary-amount.md`

Canonical validation:
- `checkpoints/monetary-amount-v0-validation.md`

Propagated owners:
- Quantity
- Observation
- Data / Subjects
- Deferred Dependency Closure
- Cross-Cluster Validation
- Multi-Actor Readiness
- Language Map
- Whole-Domain Audit

Whole-Domain REQUIRED NOW repair queue after successful MonetaryAmount propagation QA:

```text
Place             RESOLVED
Content Artifact  RESOLVED
MonetaryAmount    RESOLVED

REQUIRED NOW unresolved 0
```

This does **not** yet close the Whole-Domain audit. The next mandatory semantic action after durable MonetaryAmount closure is the full `WD-01..07` Whole-Domain rerun.

The repair does not introduce a universal FinancialAccount, Transaction, ledger, settlement, accounting, tax, trading or portfolio ontology. Decimal storage, rounding, FX providers and SQL/API/persistence remain later engineering concerns.