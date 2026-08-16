<!-- LIFEOS-CANONICAL-CONTINUATION document="domain-model.md" follows="domain-model-part-16.md" -->
> **Canonical continuation of the single logical Domain Model workstream handoff.** Earlier workstream history remains preserved; this continuation records MonetaryAmount repair propagation and the next mandatory Whole-Domain action.

# 2026-08-16 — MonetaryAmount repair

Pre-scope baseline:

```text
feature/domain-model
b7781fff333e94e9b284d8731ce5b1ce63d93d54
```

Whole-Domain repair under execution:

```text
MonetaryAmount
REQUIRED NOW
```

V3 semantic result:

```text
MonetaryAmount
REUSABLE CURRENCY-AMOUNT VALUE SEMANTICS

amount + unambiguous currency semantics
NO native entity/root

MonetaryAmount != Quantity
Currency != ordinary Quantity Unit semantics
FX conversion = contextual derived operation under applicable basis

Budget / Price / Cost / Estimate
contextual meanings, not separate universal roots

FinancialAccount / Transaction / ledger / settlement / accounting / trading
specialist / outside current general kernel

VERDICT
PASS WITH HARDENING

SEMANTIC SAFE DEFERRED 0
SEMANTIC UNCLASSIFIED  0
SEMANTIC UNRESOLVED     0
STRUCTURAL REOPEN       0
```

Key historical integrity rules:

```text
source MonetaryAmount != derived FX projection
current FX != historical FX
reference rate != transaction rate automatically
historical decision basis must remain reconstructible where material
correction != silent overwrite
```

Key Multi-Actor rules:

```text
shared budget/cost != private FinancialAccount disclosure
actor display currency != source mutation
amount knowledge != payment/spending Authority
shared value != Agreement / Consent / Responsibility
```

Operational propagation scope is CREATE-only and preserves existing canonical payloads through continuation files. No SQL/API/Auth/frontend/prototype/persistence implementation is in scope.

## Mandatory next action after MonetaryAmount remote QA closure

Once `monetary-amount-v0-validation-part-2.md` records POST-WRITE QA PASS / CLOSED, the original Whole-Domain REQUIRED NOW repair queue will be exhausted:

```text
Place             RESOLVED
Content Artifact  RESOLVED
MonetaryAmount    RESOLVED

REQUIRED NOW unresolved 0
```

Do **not** interpret that as automatic Whole-Domain closure.

The next mandatory action is:

```text
FULL WHOLE-DOMAIN RERUN

WD-01 Semantic regression
WD-02 Redundancy
WD-03 Historical reconstruction
WD-04 Multi-Actor regression
WD-05 Persistence/API pressure
WD-06 Simple-user regression
WD-07 Specialist-boundary regression
```

Only that rerun may determine whether the whole-domain baseline is ready to close and whether logical/persistence/API work can begin.

Do not automatically select another semantic candidate before the Whole-Domain rerun. Do not start SQL/API/logical persistence merely because the three known repairs are integrated.

Do not skip remote compare + fetch/read QA. Do not mark MonetaryAmount `CLOSED` until the conditional closure continuation is written after successful QA.

Normative validation: `../domain/checkpoints/monetary-amount-v0-validation.md`.