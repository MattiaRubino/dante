# MonetaryAmount

**Status:** Current accepted semantic candidate — V3 PASS WITH HARDENING, propagation in progress  
**Validated:** 2026-08-16  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 / Whole-Domain repair  
**Branch:** `feature/domain-model`

## Canonical definition

> **MonetaryAmount is reusable scalar value semantics representing an amount of monetary currency through a numerical amount plus unambiguous currency semantics, without independent identity or lifecycle. Cross-currency derivation requires an explicit applicable conversion basis and does not mutate the source amount.**

Canonical shape:

```text
numerical amount
+ unambiguous currency semantics
→ MonetaryAmount
```

Classification:

```text
MonetaryAmount
REUSABLE CURRENCY-AMOUNT VALUE SEMANTICS

✅ amount + currency
✅ reusable across budget, price, cost, estimate, observation and criterion contexts
✅ may participate in derived cross-currency comparisons when an applicable basis exists

❌ native entity/root
❌ independent lifecycle
❌ Quantity
❌ Currency entity
❌ Resource
❌ Budget
❌ Price
❌ Cost
❌ Estimate
❌ Balance
❌ Transaction
❌ FinancialAccount
❌ Observation / Actual / Evidence / Provenance
❌ FX rate
```

---

## 1. Why MonetaryAmount exists

LifeOS needs monetary values in ordinary planning and reasoning: budgets, estimated costs, prices, actual charges, affordability constraints and goal criteria. A naked number is not enough because `100` does not identify whether the amount is EUR, USD, JPY or another currency.

Money also cannot be collapsed into ordinary `Quantity` unit semantics. Stable physical conversions such as `1 kg = 1000 g` differ structurally from cross-currency conversion, whose result depends on time, source, rate basis and sometimes transaction context.

Canonical rule:

> **MonetaryAmount is distinct reusable value semantics because currency identity is intrinsic to the amount while cross-currency equivalence is contextual and time-dependent.**

---

## 2. Amount and currency are inseparable semantic components

A MonetaryAmount must carry both:

```text
amount
currency
```

Examples:

```text
1000 EUR
300 USD
25000 JPY
```

The currency must be unambiguous. A display symbol alone is not universally sufficient because symbols can be shared or ambiguous across currencies.

ISO 4217-compatible codes are appropriate vocabulary where applicable, but an external standard remains vocabulary/evidence rather than ontology authority.

`Currency` is not accepted here as a native LifeOS entity/root.

---

## 3. MonetaryAmount is not Quantity

`Quantity` owns ordinary scalar measurement semantics where applicable unit conversion can establish stable equivalence.

`MonetaryAmount` owns currency-bearing scalar value semantics.

```text
1 kg → 1000 g
```

can be treated as stable unit conversion.

```text
100 EUR → USD
```

cannot be resolved without an applicable conversion basis.

Therefore:

```text
MonetaryAmount != Quantity
Currency != ordinary Quantity Unit semantics
```

A future physical implementation may reuse scalar infrastructure, but storage reuse must not erase this semantic distinction.

---

## 4. Context owns monetary meaning

The same MonetaryAmount value can be used under different contextual meanings:

```text
1000 EUR
```

may be:

- a trip budget;
- a quoted price;
- a planned cost;
- an estimated cost;
- an actual charge;
- an observed account balance;
- a criterion threshold.

Those meanings belong to the surrounding concept or relation.

Therefore:

```text
MonetaryAmount != Budget
MonetaryAmount != Price
MonetaryAmount != Cost
MonetaryAmount != Estimate
MonetaryAmount != Balance
```

No separate monetary value type is created merely because the contextual use differs.

---

## 5. FX is separate contextual derivation

Cross-currency conversion is not intrinsic state of MonetaryAmount.

Conceptually:

```text
source MonetaryAmount
+ target currency
+ applicable conversion basis
  - rate
  - source
  - effective time/window
  - purpose/context where material
→ derived MonetaryAmount
```

Canonical invariants:

```text
converted amount != mutation of source amount
current FX != historical FX
reference rate != executed transaction rate automatically
no FX basis != zero
no FX basis != established equivalence
```

Where a conversion materially influences a Decision, Evaluation, Plan or historical outcome, the applicable conversion basis must be attributable or reconstructible to the level required by consequence.

---

## 6. Historical truth

A source fact remains a source fact even when later displayed or evaluated in another currency.

Example:

```text
T0 hotel quote = 300 USD
T1 LifeOS estimate = 276 EUR using rate R1
T2 user approves Plan using that estimate
T3 FX changes
T4 actual card charge = 281.40 EUR
```

All of these may remain simultaneously truthful:

- original quote: `300 USD`;
- historical estimate: `276 EUR` under R1;
- later current estimate under another rate;
- actual charge: `281.40 EUR`.

Canonical rule:

> **A later FX rate, converted display value or actual charge does not silently rewrite the original MonetaryAmount or a materially consequential historical conversion basis.**

Correction remains correction, not silent overwrite.

---

## 7. Comparison and aggregation

Two MonetaryAmounts in the same currency may be numerically comparable where the owning context makes comparison meaningful.

Same currency alone does not authorize every aggregation.

```text
100 EUR salary
+ 100 EUR liability
```

must not be combined merely because both use EUR.

Cross-currency comparison additionally requires an applicable conversion basis.

The kernel therefore does not assume a universal sum, net, sign convention or accounting treatment.

---

## 8. Sign and accounting semantics

Positive/negative sign does not universally mean:

```text
income / expense
debit / credit
asset / liability
cash in / cash out
```

Those meanings belong to specialist or contextual financial semantics.

`Transaction`, `FinancialAccount`, ledger, tax, fee decomposition, settlement, accounting classification and portfolio/trading semantics are not introduced by MonetaryAmount v0.

---

## 9. Multi-actor and visibility

A shared context can expose a MonetaryAmount without exposing every underlying financial source.

Example:

```text
shared trip budget = 1,000 EUR
```

may be visible to participants while:

```text
private bank account
private balance
private transaction history
```

remain governed independently by Visibility.

Different Actors may prefer different display currencies. Display conversion is a view/projection concern and does not mutate the canonical source amount.

---

## 10. AI boundary

AI may:

- identify candidate monetary amounts from user or source material;
- propose budget/cost comparisons;
- calculate a conversion under an explicit rate/basis;
- explain a comparison within allowed Visibility;
- flag missing or stale FX basis.

AI must not:

- invent a currency when source meaning is ambiguous;
- convert without an attributable/applicable basis when consequence matters;
- replace a historical rate with the current rate silently;
- treat a reference conversion as an executed charge;
- infer a private account or transaction from a shared amount;
- fabricate Authority, Evidence or financial truth from confidence.

---

## 11. Product simplicity

Most users should see natural monetary language:

```text
Budget €1,000
Estimated €820
Spent €610
```

or:

```text
Hotel $300
≈ €276 at planning rate
Actual card charge €281.40
```

The UI does not need to expose `MonetaryAmount`, FX provenance or conversion material-state details unless consequence or user intent requires it.

---

## 12. Specialist boundary

The current general LifeOS kernel does not require a universal ontology for:

- accounts;
- transactions;
- ledgers;
- settlement;
- accounting entries;
- tax;
- securities;
- trading;
- portfolio positions;
- generalized crypto/token/points instruments.

Such capabilities may be owned by specialist modules/adapters if future product scope requires them.

This is a definitive kernel boundary, not unresolved semantic debt.

---

## 13. Implementation boundary

MonetaryAmount v0 does not approve:

- SQL types or tables;
- decimal precision/scale;
- minor-unit storage strategy;
- rounding algorithms;
- FX provider contracts;
- caching;
- API payload shapes;
- persistence/materialization strategy.

Those are later engineering decisions constrained by these semantics.

---

## 14. Core invariants

1. MonetaryAmount is reusable value semantics, not a native entity/root.
2. A number alone is not a MonetaryAmount.
3. MonetaryAmount requires numerical amount plus unambiguous currency semantics.
4. MonetaryAmount is not Quantity.
5. Currency is not ordinary Quantity Unit semantics.
6. Currency vocabulary does not imply a native Currency entity.
7. MonetaryAmount is not Resource.
8. MonetaryAmount is not Budget, Price, Cost, Estimate, Balance, Transaction or FinancialAccount.
9. MonetaryAmount is not Observation, Actual, Evidence or Provenance.
10. Equal monetary values do not create shared entity identity.
11. FX rate is not intrinsic state of MonetaryAmount.
12. Cross-currency conversion requires an applicable basis.
13. Converted value is derived and does not mutate the source amount.
14. Current FX is not historical FX.
15. Reference rate is not an executed transaction rate automatically.
16. Consequential historical conversion basis must remain attributable/reconstructible where required.
17. Missing FX does not establish zero or equivalence.
18. Same currency does not authorize every aggregation.
19. Sign does not universally encode accounting meaning.
20. Display-currency preference does not mutate source truth.
21. Shared amount visibility does not imply private financial-source visibility.
22. Specialist finance semantics remain outside the general kernel unless separately justified.
23. No SQL/API/persistence shape is accepted here.

## Normative validation

See `../checkpoints/monetary-amount-v0-validation.md`.