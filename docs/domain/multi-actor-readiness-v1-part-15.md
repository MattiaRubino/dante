<!-- LIFEOS-CANONICAL-CONTINUATION document="multi-actor-readiness-v1.md" follows="multi-actor-readiness-v1-part-14.md" -->
> **Canonical continuation of the single logical Multi-Actor Readiness v1 document.** Earlier readiness conclusions remain preserved; this continuation records MonetaryAmount integration only.

# 2026-08-16 — MonetaryAmount integration

MonetaryAmount v0 passes Multi-Actor readiness with hardening.

Canonical boundaries:

```text
MonetaryAmount value
!= Actor identity
!= payer / payee role
!= Ownership
!= Responsibility
!= Authority
!= Agreement / Consent / Confirmation
!= Visibility
```

## Shared planning without private-source disclosure

A shared context may expose a bounded monetary value:

```text
family trip budget = 1,000 EUR
shared estimated hotel cost = 300 USD
```

without automatically exposing:

```text
private FinancialAccount
private balance Observation
private transaction history
private Evidence/source document
```

Visibility of the shared amount, conversion basis and underlying source records remains independently governed.

## Actor-specific display currency

Different Actors may use different presentation currencies:

```text
source quote = 300 USD
Actor A view ≈ 276 EUR
Actor B view = 300 USD
```

without creating competing canonical source amounts.

```text
display-currency preference != source mutation
```

Where a displayed conversion materially influences a shared Decision, the applicable conversion basis must remain attributable/reconstructible to the required consequence level.

## Actor roles remain separate

The following may all differ:

```text
source Actor
recorder
payer
beneficiary
budget owner/steward
Authority holder
Decision maker
viewer
represented party
```

Entering, viewing or converting an amount does not infer payment responsibility, spending Authority or ownership of the underlying funds.

Representation/on-behalf-of semantics remain separate. An assistant entering a cost for another Person does not become payer or owner and does not fabricate that Person's agreement.

## Collective boundary

Several Actors sharing or contributing monetary values do not automatically form a Collective. A true Collective may have a shared budget context, but Collective semantics remain independently established.

## Conflicts and source precedence

Different Actors/providers may report different prices, charges or FX rates. Existing Reconciliation/Source Precedence semantics handle bounded conflict; MonetaryAmount introduces no universal newest/provider/highest-confidence winner.

## AI boundary

AI may propose or calculate bounded monetary comparisons under attributable inputs and conversion basis. AI access/confidence does not create financial Authority, consent to spend, payment truth, source precedence or permission to disclose private financial context.

```text
MA-01..20
PASS / PASS WITH HARDENING

MULTI-ACTOR READINESS
PASS WITH HARDENING
REOPEN 0
UNCLASSIFIED 0
UNRESOLVED 0
```

No new Principal/Auth implementation, ACL schema, account-sharing model, transaction model or FX-provider implementation is accepted here.

Normative reference: `checkpoints/monetary-amount-v0-validation.md`.