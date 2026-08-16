<!-- LIFEOS-CANONICAL-CONTINUATION document="quantity-v0-validation.md" follows="quantity-v0-validation.md" -->
> **Canonical continuation of the single logical Quantity v0 validation checkpoint.** Earlier validation evidence and transition-stage dependency wording remain preserved; this continuation records the post-MonetaryAmount regression and final dependency resolution.

# 2026-08-16 — MonetaryAmount boundary propagation

## Dependency result

The historical Quantity ↔ Money / MonetaryAmount dependency has now received its final semantic resolution:

```text
REQUIRED BY CURRENT LIFEOS CORE
→ V3 COMPLETE
→ MonetaryAmount accepted as distinct reusable value semantics
→ NOT a Quantity subtype/root
→ dependency CLOSED
```

## Regression

Stable measurement-unit conversion remains valid where compatible unit and quantity-kind semantics establish equivalence:

```text
1 kg
↔ 1000 g
```

Currency conversion remains structurally different:

```text
100 EUR
→ USD
```

cannot be interpreted as stable ordinary unit conversion. It requires an applicable FX conversion basis and produces a derived MonetaryAmount without mutating the source value.

Expected invariants:

```text
MonetaryAmount != Quantity
Currency != ordinary Quantity Unit semantics
current FX != historical FX
converted amount != source mutation
reference rate != transaction rate automatically
```

All pass.

## Existing Quantity invariants

No accepted Quantity invariant is weakened:

- Quantity remains reusable scalar measurement value semantics;
- Quantity has no independent entity identity/lifecycle;
- contextual property meaning remains outside the unit token;
- unit compatibility alone does not establish full domain-semantic equivalence;
- same/compatible units do not authorize universal aggregation;
- source representation and display/normalized representation remain distinguishable;
- no standalone SQL/API/persistence shape is implied.

## Verdict impact

```text
QUANTITY v0
PASS WITH HARDENING — ACCEPTED BASELINE PRESERVED

MONEY / MONETARY AMOUNT DEPENDENCY
FINAL RESOLUTION COMPLETE

STRUCTURAL REOPEN       0
SEMANTIC UNCLASSIFIED   0
SEMANTIC UNRESOLVED     0
```

The old transition-stage `SAFE-DEFER candidate` wording remains historical evidence only and is superseded for current interpretation by this final resolution.

Normative MonetaryAmount validation: `monetary-amount-v0-validation.md`.