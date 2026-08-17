<!-- LIFEOS-CANONICAL-CONTINUATION document="observation-v0-validation.md" follows="observation-v0-validation.md" -->
> **Canonical continuation of the single logical Observation v0 validation checkpoint.** Earlier validation evidence remains preserved; this continuation records MonetaryAmount integration and closes the historical Money dependency without reopening Observed Reality.

# 2026-08-16 — MonetaryAmount propagation regression

## Dependency result

```text
Observation ↔ Money / MonetaryAmount
HISTORICAL SEPARATE DEPENDENCY QUESTION
→ MonetaryAmount V3 COMPLETE
→ Observation can use MonetaryAmount as value semantics
→ no new Observation subtype/root
→ dependency CLOSED
```

## Boundary regression

```text
Observation
owns assertion / Subject / property-state / effective context / identity

MonetaryAmount
owns amount + unambiguous currency value semantics

Observation != MonetaryAmount
```

No accepted Observation boundary is weakened:

```text
Observation != Actual
Observation != Outcome
Observation != Evidence
Observation != Provenance
Observation != universal transaction/fact table
```

## Adversarial tests

### MON-OBS-01 — Receipt extraction

OCR extracts `€87.20` from a receipt Content Artifact.

Expected:

```text
Content Artifact / extraction Provenance
→ candidate or imported Observation/value where workflow supports it

€87.20 extraction
!= automatic proof of payment Actual/Transaction
```

**PASS.**

### MON-OBS-02 — Balance observation

Provider reports `1,200 EUR` account balance at T1.

Expected: Observation may preserve `1,200 EUR` with Subject/context/time/source; this does not create universal FinancialAccount/ledger semantics in the kernel.

**PASS.**

### MON-OBS-03 — Quote

Provider quote says `300 USD`.

Expected: source Observation preserves `300 USD`; a later EUR conversion does not rewrite it.

**PASS.**

### MON-OBS-04 — Conflicting sources

Receipt reports `281.40 EUR`; bank provider reports `282.10 EUR`.

Expected: distinct assertions may coexist; Reconciliation/Evidence handles bounded conflict, not MonetaryAmount itself.

**PASS.**

### MON-OBS-05 — Missing currency

Imported text says `cost = 100`.

Expected: no silent EUR assignment from locale/context guess alone.

**PASS WITH HARDENING.**

### MON-OBS-06 — Historical FX

Quote `300 USD` is converted to `276 EUR` for a material planning Decision under rate R1; later FX changes.

Expected: source quote remains `300 USD`; consequential historical conversion basis remains attributable/reconstructible where required.

**PASS WITH HARDENING.**

### MON-OBS-07 — Shared context / private source

Private balance Observation contributes to an affordability Evaluation for a shared trip.

Expected: bounded result may be shared without automatic disclosure of the private Observation/source.

**PASS.**

## Verdict impact

```text
OBSERVATION v0
ACCEPTED BASELINE PRESERVED
PASS WITH HARDENING

MONETARY AMOUNT INTEGRATION
PASS WITH HARDENING

STRUCTURAL REOPEN       0
SEMANTIC UNCLASSIFIED   0
SEMANTIC UNRESOLVED     0
```

The historical statement that Money / MonetaryAmount remained a separate dependency question is retained as chronology and is superseded for current interpretation by this final resolution.

Normative MonetaryAmount validation: `monetary-amount-v0-validation.md`.