<!-- LIFEOS-CANONICAL-CONTINUATION document="quantity.md" follows="quantity.md" -->
> **Canonical continuation of the single logical Quantity document.** Earlier Quantity v0 rationale, invariants and transition-stage dependency wording remain preserved; this continuation records the final MonetaryAmount boundary resolution produced by the Whole-Domain repair.

# 2026-08-16 — Money / MonetaryAmount dependency resolution

The historical Quantity v0 boundary deliberately did not collapse currency-bearing values into ordinary Quantity semantics. That dependency is now fully resolved.

Final classification:

```text
HISTORICAL MONEY / MONETARY AMOUNT DEPENDENCY
→ FINAL RESOLUTION: REQUIRED BY CURRENT LIFEOS CORE
→ VALIDATED AS MonetaryAmount reusable value semantics
→ NOT a Quantity subtype/root
→ SEMANTIC DEBT CLOSED
```

Canonical boundary:

```text
Quantity
= reusable scalar measurement value semantics
  where magnitude + applicable unit semantics support truthful interpretation

MonetaryAmount
= reusable currency-amount value semantics
  where numerical amount + unambiguous currency semantics are intrinsic

MonetaryAmount != Quantity
Currency != ordinary Quantity Unit semantics
```

The distinction is structural rather than representational convenience.

```text
1 kg → 1000 g
```

may express stable unit equivalence under compatible quantity-kind context.

By contrast:

```text
100 EUR → USD
```

requires an applicable conversion basis such as rate, source and effective time/context. A later FX rate may differ without changing the original `100 EUR` source value.

Therefore:

> **Quantity conversion semantics must not be reused as though currency conversion were stable physical-unit equivalence. Cross-currency derivation belongs to MonetaryAmount plus an explicit applicable conversion basis.**

## Shared implementation does not erase semantic distinction

A later logical/physical model may reuse scalar/decimal infrastructure across Quantity and MonetaryAmount. Such implementation reuse does not make the two concepts semantically interchangeable and does not authorize one universal `number + unit` wrapper.

```text
shared scalar machinery MAY exist
semantic collapse MUST NOT
```

## Historical and display integrity

The existing Quantity rules remain unchanged:

```text
source representation != normalized/display representation
actor display preference != canonical/source mutation
precision/rounding must not be fabricated
```

MonetaryAmount adds an analogous but separately owned rule:

```text
source monetary amount != derived FX display/estimate
current FX != historical FX
```

## No Quantity reopen

The MonetaryAmount V3 review does not invalidate Quantity v0. It confirms the correctness of the original anti-collapse boundary.

```text
QUANTITY v0
STRUCTURAL REOPEN 0

MONEY / MONETARY AMOUNT DEPENDENCY
RESOLVED
```

Remaining historical dependency wording in the base Quantity document is preserved as chronology. For current interpretation, this continuation is authoritative for the Money / MonetaryAmount boundary.

Normative MonetaryAmount reference: `../checkpoints/monetary-amount-v0-validation.md`.