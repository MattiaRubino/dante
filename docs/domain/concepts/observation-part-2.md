<!-- LIFEOS-CANONICAL-CONTINUATION document="observation.md" follows="observation.md" -->
> **Canonical continuation of the single logical Observation document.** Earlier Observation v0 rationale and boundaries remain preserved; this continuation records the final Money / MonetaryAmount dependency resolution and its integration with observed reality.

# 2026-08-16 — MonetaryAmount value integration

The historical Observation boundary listed Money / MonetaryAmount as a separate dependency question rather than silently absorbing currency values into Quantity. MonetaryAmount v0 now resolves that question.

Final classification:

```text
HISTORICAL OBSERVATION ↔ MONEY / MONETARY AMOUNT DEPENDENCY
→ FINAL RESOLUTION: ALREADY COMPOSABLE AFTER MonetaryAmount ACCEPTANCE
→ Observation may use MonetaryAmount as observed/asserted value semantics
→ Observation identity/boundaries unchanged
→ SEMANTIC DEBT CLOSED
```

## Canonical composition

```text
Observation
- Subject / property-state context
- effective time/context
- assertion/observation identity
- applicable source/Provenance
- value: MonetaryAmount where truthful
```

Example:

```text
Observation O1
property: quoted room price
subject/context: hotel stay option
value: 300 USD
observed/effective time: T1
source: provider quote
```

or:

```text
Observation O2
property: account balance
subject/context: bounded financial source
value: 1,200 EUR
observed/effective time: T2
source: connected provider
```

The value semantics and the observational assertion remain separate:

```text
MonetaryAmount != Observation
```

MonetaryAmount owns only amount + unambiguous currency semantics. Observation owns what was measured/reported/asserted, about what, under which effective context/time and observational identity.

## Observed money does not create transaction truth

An observed monetary value must not be promoted automatically into richer finance semantics.

```text
observed balance
!= FinancialAccount identity

observed price
!= Transaction

receipt-extracted amount
!= actual payment automatically

provider-reported charge
!= universally settled/authorized transaction state
```

If a future specialist financial module owns transaction/account/settlement lifecycle, Observation may describe or ingest bounded facts without replacing that richer native model.

## FX and historical assertion integrity

Observation may preserve a source amount and separately preserve a derived monetary observation/projection where the owning workflow justifies it.

```text
source quote observation
300 USD

planning conversion
276 EUR under FX basis R1
```

The later conversion must not silently rewrite the source observation.

```text
source MonetaryAmount != derived FX amount
current FX != historical FX
reference estimate != actual charge
```

Where a conversion itself is an explicitly derived Observation, its derivation/source basis belongs to Provenance and material historical context where consequence requires it.

## Conflicting monetary observations

Distinct sources may produce different monetary assertions:

```text
provider A quote = 300 USD
provider B quote = 285 USD
```

or:

```text
merchant receipt = 281.40 EUR
bank posting = 282.10 EUR
```

Observation preserves the assertions; Reconciliation/Evidence/Source Precedence may later determine how a bounded decision/evaluation treats them. MonetaryAmount does not select a winner.

## Missing or ambiguous currency

```text
"cost = 100"
```

without sufficient currency context is not silently normalized into `100 EUR`, even if the user locale is Italy.

AI/import pipelines may retain an unresolved/candidate interpretation according to the owning ingestion semantics; they must not fabricate currency certainty.

## Multi-actor and privacy

A monetary Observation can participate in shared planning without disclosing every private financial source.

```text
private balance Observation
→ authorized bounded affordability Evaluation/result
→ shared planning context
```

is compatible with:

```text
private financial Observation
!= automatically visible to every shared-context participant
```

Visibility remains independently governed.

## No Observation reopen

MonetaryAmount integration does not broaden Observation into a universal finance fact table.

```text
OBSERVATION v0
STRUCTURAL REOPEN 0

MONEY / MONETARY AMOUNT DEPENDENCY
RESOLVED
```

The base document's earlier statement that Money / MonetaryAmount remained a separate dependency question is historical chronology. This continuation provides the current final resolution.

Normative MonetaryAmount reference: `../checkpoints/monetary-amount-v0-validation.md`.