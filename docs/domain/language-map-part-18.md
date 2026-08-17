<!-- LIFEOS-CANONICAL-CONTINUATION document="language-map.md" follows="language-map-part-17.md" -->
> **Canonical continuation of the single logical Domain Language Map.** Earlier language mappings remain preserved; this continuation records MonetaryAmount terminology only.

# 2026-08-16 — MonetaryAmount language

Canonical domain term:

```text
MonetaryAmount
```

Meaning:

> reusable currency-amount value semantics consisting of a numerical amount plus unambiguous currency semantics, without independent native identity/lifecycle.

Preferred natural product vocabulary may include, where truthful:

```text
budget
price
cost
estimate
actual charge
balance
```

These words describe surrounding contextual meaning; they are not synonyms for MonetaryAmount and do not imply separate universal kernel roots.

Canonical distinctions:

```text
MonetaryAmount != Quantity
Currency != ordinary Quantity Unit semantics
MonetaryAmount != Resource
MonetaryAmount != Budget
MonetaryAmount != Price
MonetaryAmount != Cost
MonetaryAmount != Estimate
MonetaryAmount != Balance
MonetaryAmount != Transaction
MonetaryAmount != FinancialAccount
MonetaryAmount != Observation / Actual / Evidence / Provenance
FX rate != MonetaryAmount
```

Use an unambiguous currency identifier/code where source semantics support it. Do not rely on a symbol alone where the symbol is ambiguous.

For cross-currency reasoning, use language that preserves derivation and basis:

```text
source amount
converted amount
planning estimate
reference rate
conversion basis
actual charge
```

Do not call a current conversion the historical source amount, and do not call a reference-rate estimate an executed charge.

Examples:

```text
Hotel quote: 300 USD
Planning estimate: ≈ 276 EUR using the applicable planning-rate basis
Actual card charge: 281.40 EUR
```

Prefer `MonetaryAmount` over generic `Money` in canonical semantic documentation when referring to the reusable amount+currency value abstraction. `Money` may remain ordinary product/domain language where no ambiguity results.

`FinancialAccount`, `Transaction`, ledger, settlement, accounting, tax, trading and portfolio language belongs to specialist semantics unless a separate accepted review establishes otherwise.

Do not use `currency` as though it were an ordinary Quantity unit solely to reuse physical-unit conversion machinery.

Normative reference: `checkpoints/monetary-amount-v0-validation.md`.