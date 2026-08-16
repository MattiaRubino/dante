<!-- LIFEOS-CANONICAL-CONTINUATION document="data-subjects-v0.md" follows="data-subjects-v0-part-6.md" -->
> **Canonical continuation of the single logical Data / Subjects v0 checkpoint.** Earlier Cluster-4 validation, Place repair and Content Artifact repair remain preserved; this continuation records MonetaryAmount integration only.

# 2026-08-16 — MonetaryAmount bounded completion

The Whole-Domain product-coverage audit required currency-bearing scalar value semantics for current LifeOS planning, affordability, budget/cost and evaluation workflows.

Accepted completion:

```text
MonetaryAmount
= REUSABLE CURRENCY-AMOUNT VALUE SEMANTICS
= numerical amount + unambiguous currency semantics

NEW NATIVE REFERENT
NO
```

Canonical boundaries:

```text
MonetaryAmount != Quantity
MonetaryAmount != Subject
MonetaryAmount != Resource
MonetaryAmount != Budget / Price / Cost / Estimate / Balance
MonetaryAmount != Transaction / FinancialAccount
MonetaryAmount != Observation / Actual / Evidence / Provenance
FX rate != MonetaryAmount
```

MonetaryAmount itself has no independent Subject or lifecycle. The surrounding Observation, Plan, Criterion, Decision, source record or specialist object owns aboutness, identity, time/history, Provenance, Authority and Visibility.

A Subject-bearing record may use MonetaryAmount without turning the value into a Subject:

```text
Observation
subject: bounded referent/context
property: price/balance/cost state
value: 300 USD
```

Multi-actor sharing of a monetary value does not imply disclosure of private account/balance/transaction sources. Actor-specific display-currency projection does not mutate source truth.

This is a bounded Data / Subjects hardening. Person, Actor, Account, Asset, Subject, Resource, Quantity, Place and Content Artifact semantics remain accepted; Quantity's historical Money boundary is now finally resolved rather than deferred.

```text
DATA / SUBJECTS v0
MonetaryAmount gap RESOLVED
accepted prior identities preserved
REOPEN 0
UNCLASSIFIED 0
UNRESOLVED 0
```

Whole-Domain REQUIRED NOW semantic repair queue after this integration:

```text
Place             RESOLVED
Content Artifact  RESOLVED
MonetaryAmount    RESOLVED

REQUIRED NOW unresolved 0
```

This does not close the Whole-Domain audit; WD-01..07 must be rerun after durable propagation QA.

Normative reference: `monetary-amount-v0-validation.md`.