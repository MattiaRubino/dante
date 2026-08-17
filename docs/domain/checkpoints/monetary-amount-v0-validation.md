# MonetaryAmount v0 Validation

**Status:** PASS WITH HARDENING — semantic propagation in progress  
**Validated:** 2026-08-16  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 / Whole-Domain repair  
**Branch:** `feature/domain-model`

## Verdict

```text
MONETARY AMOUNT v0

PASS WITH HARDENING

CORE  PASS WITH HARDENING
MA    PASS WITH HARDENING
XCON  PASS WITH HARDENING
ADS   COMPLETE

NEW NATIVE REFERENT
NO

NEW VALUE SEMANTICS
YES — MonetaryAmount

SEMANTIC SAFE DEFERRED  0
SEMANTIC UNCLASSIFIED   0
SEMANTIC UNRESOLVED     0
STRUCTURAL REOPEN       0
```

Durable repository `CLOSED` remains conditional on exact propagation write + remote QA. This checkpoint records the semantic decision, not post-write closure.

---

# 1. Candidate formation

## 1.1 Trigger

The Whole-Domain audit identified `MonetaryAmount` as the final REQUIRED NOW repair after Place and Content Artifact / Document.

The trigger is legitimate because ordinary LifeOS product requirements already include:

- budget and affordability constraints;
- prices and expected costs in planning;
- planned versus actual cost comparison;
- monetary Goal/Evaluation thresholds;
- multi-currency travel and external-provider contexts.

The accepted Quantity baseline had intentionally kept Money outside ordinary Quantity unit semantics because currency conversion is not a stable measurement-unit equivalence.

## 1.2 Candidate family

Candidate family tested:

```text
MonetaryAmount
Currency
Money
Budget
Price
Cost
Estimate
Balance
Transaction
FinancialAccount
FX rate / conversion
```

The review tested whether any of these require native kernel identity or whether a smaller value semantic owner is sufficient.

---

# 2. Candidate reductio

```text
H0 Currency as ordinary Quantity Unit
REJECTED
Reason: cross-currency equivalence is contextual/time/source dependent.

H1 MonetaryAmount as reusable value semantics
ACCEPTED WITH HARDENING
Reason: ordinary LifeOS workflows need amount + unambiguous currency without independent identity/lifecycle.

H2 MonetaryAmount as native entity/root
REJECTED
Reason: value equality and reuse do not imply independent identity.

H3 Currency as native entity/root
REJECTED FOR CURRENT KERNEL
Reason: bounded currency vocabulary is sufficient for current product scope.

H4 Budget as native kernel primitive
REJECTED
Reason: budget is contextual planning/constraint semantics using MonetaryAmount plus scope/time/policy/evaluation semantics where applicable.

H5 Universal Money / Transaction / FinancialAccount root
REJECTED AS OVERMODELING
Reason: current LifeOS core does not require general ledger/account/transaction lifecycle.

H6 FX rate embedded as intrinsic MonetaryAmount state
REJECTED
Reason: rate is contextual derivation basis, not part of source amount identity/value semantics.
```

Surviving classification:

> **MonetaryAmount is reusable scalar value semantics representing an amount of monetary currency through a numerical amount plus unambiguous currency semantics, without independent identity or lifecycle. Cross-currency derivation requires an explicit applicable conversion basis and does not mutate the source amount.**

---

# 3. CORE-01..13

## CORE-01 — Identity necessity

**PASS.** Independent native identity is not required. Two occurrences of `100 EUR` need not be the same object/referent; semantic use belongs to context.

## CORE-02 — Boundary precision

**PASS WITH HARDENING.** Explicitly separate:

```text
MonetaryAmount != Quantity
MonetaryAmount != Resource
MonetaryAmount != Budget/Price/Cost/Estimate/Balance
MonetaryAmount != Transaction/FinancialAccount
MonetaryAmount != Observation/Actual/Evidence/Provenance
MonetaryAmount != FX rate
```

## CORE-03 — Required information preservation

**PASS.** `amount + currency` preserves the minimum information required for truthful monetary interpretation.

A naked numeric scalar fails this test because it cannot distinguish `100 EUR` from `100 USD`.

## CORE-04 — False-collapse resistance

**PASS WITH HARDENING.** Currency must not be modeled as ordinary Quantity unit conversion. Budget/cost/price meaning must not be collapsed into the MonetaryAmount value itself.

## CORE-05 — Lifecycle

**PASS.** MonetaryAmount has no independent lifecycle. Material lifecycle belongs to the surrounding owner such as Plan, Observation, Actual, Quote/Artifact, Criterion or specialist finance object.

## CORE-06 — Current versus historical state

**PASS WITH HARDENING.** Source amount, historical conversion estimate, current conversion projection and actual settled/charged amount may coexist.

```text
current FX != historical FX
converted amount != source mutation
actual charge != prior estimate
```

## CORE-07 — Correction

**PASS.** Correction of an amount or its source record must preserve applicable history according to the owning concept. A later rate or later charge does not silently rewrite earlier source/conversion facts.

## CORE-08 — Conflict

**PASS.** Conflicting monetary assertions may coexist under Observation/Evidence/Reconciliation. MonetaryAmount itself does not choose a winner.

## CORE-09 — Unknown / missing state

**PASS.** Missing currency is not safely inventable. Missing FX basis does not mean zero, equality or established cross-currency equivalence.

## CORE-10 — Derived state

**PASS WITH HARDENING.** Converted MonetaryAmounts are derived under a bounded conversion basis. Derived presentation must not replace the source amount.

## CORE-11 — Authority / common-ground boundary

**PASS.** A MonetaryAmount carries no Authority, Agreement, Confirmation or Consent. An amount may be proposed, observed, agreed, decided or charged in surrounding semantics.

## CORE-12 — AI boundary

**PASS WITH HARDENING.** AI may extract/propose/convert where basis is explicit; it may not fabricate currency, historical rate, transaction truth or Authority.

## CORE-13 — Product simplicity

**PASS.** UI can remain natural (`Budget €1,000`) while advanced provenance/FX basis appears only when useful or consequential.

CORE verdict:

```text
PASS WITH HARDENING
```

---

# 4. MA-01..20

## MA-01 — Multiple Actors

**PASS.** MonetaryAmount is actor-neutral value semantics. Actor attribution belongs to surrounding records.

## MA-02 — External/non-account Persons

**PASS.** An external Person may quote, pay, receive, observe or propose an amount without LifeOS Account identity.

## MA-03 — Collective context

**PASS.** A Collective may have a shared budget/cost context without MonetaryAmount becoming collective identity.

## MA-04 — Multiple holders/owners

**PASS.** Equal/shared amounts do not infer Ownership, Membership or Collective status.

## MA-05 — Shared context, private source

**PASS WITH HARDENING.** Shared budget visibility does not imply visibility of private bank account, balance or transaction evidence.

## MA-06 — Actor-specific display preference

**PASS WITH HARDENING.** Different Actors may view derived values in different currencies without mutating canonical source monetary truth.

## MA-07 — Proposal versus effective value

**PASS.** Proposed cost/budget/price remains Proposal/context until owning semantics establish effect; MonetaryAmount itself does not establish acceptance.

## MA-08 — Responsibility

**PASS.** MonetaryAmount does not imply who is responsible to pay/manage/approve.

## MA-09 — Authority

**PASS.** Amount knowledge does not imply spending or approval Authority.

## MA-10 — Visibility

**PASS.** Amount, conversion basis and underlying financial source may have distinct Visibility.

## MA-11 — Representation

**PASS.** An Actor may enter or approve an amount on behalf of another under Representation semantics without becoming that party.

## MA-12 — Agreement / Consent

**PASS.** Same observed/shared amount does not imply agreement to spend/pay or consent to disclosure.

## MA-13 — Confirmation

**PASS.** Confirmation of an amount is separate attestation, not intrinsic state of MonetaryAmount.

## MA-14 — Decision

**PASS WITH HARDENING.** If a Decision materially depends on an FX-derived amount, the consequential basis should remain attributable/reconstructible.

## MA-15 — Reconciliation

**PASS.** Competing amount/rate/source assertions can be reconciled externally; MonetaryAmount does not impose source precedence.

## MA-16 — Unequal power / specialist actors

**PASS.** Bank, merchant, tax authority, employer or provider source-of-record status remains bounded to the relevant facet.

## MA-17 — AI delegation

**PASS WITH HARDENING.** AI acting as assistant may calculate/propose but cannot create financial Authority or execute semantic settlement by inference.

## MA-18 — No automatic group inference

**PASS.** Several Actors associated with an amount do not automatically form a Collective.

## MA-19 — No automatic disclosure

**PASS.** Shared planning need does not authorize disclosure of private financial Evidence.

## MA-20 — Actor-scoped history

**PASS.** Actor-specific display projections/history can coexist with source truth without multiplying MonetaryAmount identity.

MA verdict:

```text
PASS WITH HARDENING
```

---

# 5. Cross-concept validation (XCON)

## XCON-01 — Quantity

```text
MonetaryAmount != Quantity
```

Physical/unit-equivalence machinery cannot silently define FX conversion.

**PASS WITH HARDENING.** Quantity requires a continuation closing the historical Money dependency.

## XCON-02 — Resource

```text
Money != Resource
Budget != Resource
```

A MonetaryAmount can quantify a budget/cost constraint but is not itself a Resource referent/capability.

**PASS.** Existing Resource boundaries are sufficient.

## XCON-03 — Criterion / Evaluation

A Criterion may use MonetaryAmount thresholds and Evaluation may produce projections such as `€5,000 / €20,000` without MonetaryAmount becoming Criterion identity.

**PASS.** Existing Criterion/Evaluation semantics are sufficient.

## XCON-04 — Observation

An Observation may assert a monetary state (`observed balance = 1,200 EUR`, `observed price = 300 USD`). The Observation owns assertion context/source/time; MonetaryAmount owns only amount+currency value semantics.

**PASS WITH HARDENING.** Observation requires a continuation closing its historical Money dependency.

## XCON-05 — Actual

An actual charge/payment occurrence may carry MonetaryAmount, but:

```text
MonetaryAmount != Actual
```

**PASS.** No Actual change required.

## XCON-06 — Evidence / Provenance

FX rate source, quote artifact, bank statement or provider assertion may become Evidence/Provenance. MonetaryAmount itself does not establish evidentiary weight or lineage.

**PASS.** Existing Evidence/Provenance boundaries are sufficient.

## XCON-07 — Decision

A Decision may rely on monetary comparisons. Historical material FX basis must remain reconstructible when it materially affected the decision.

**PASS WITH HARDENING.** No Decision primitive change required.

## XCON-08 — Version / Reconciliation

Changed FX projection does not necessarily create a new version of the source amount. Material owner state/history and competing source assertions remain governed by Version/Reconciliation.

**PASS.**

## XCON-09 — Content Artifact

A receipt, quote, invoice-like document or screenshot may contain monetary values. Artifact identity is independent from extracted MonetaryAmount.

**PASS.**

## XCON-10 — Place / travel

Travel plans may combine prices in multiple currencies; Place semantics remain unaffected. FX is contextual derivation.

**PASS.**

XCON verdict:

```text
PASS WITH HARDENING
```

---

# 6. Adversarial / regression scenarios (ADS)

## ADS-01 — Ambiguous symbol

Input: `$100` without sufficient context.

Expected:

```text
currency UNKNOWN/AMBIGUOUS
NOT silently USD
```

**PASS.**

## ADS-02 — Stable-unit false analogy

Input: `100 EUR`, request convert to USD without rate/source/time.

Expected: no canonical equivalence inferred.

**PASS.**

## ADS-03 — Historical planning rate

Trip quote `300 USD`; LifeOS estimates `276 EUR` under R1; later FX changes.

Expected: source quote preserved; historical decision basis can remain R1; current projection may differ.

**PASS.**

## ADS-04 — Actual charge differs

Historical estimate `276 EUR`; card charge later `281.40 EUR`.

Expected: both remain truthful; actual charge does not rewrite estimate.

**PASS.**

## ADS-05 — Reference versus transaction rate

Reference FX produces `276 EUR`; provider settlement produces `281.40 EUR`.

Expected:

```text
reference estimate != executed charge
```

**PASS WITH HARDENING.**

## ADS-06 — Missing FX

Two prices: `100 EUR`, `100 USD`; no applicable conversion basis.

Expected: no universal cheaper/equal conclusion.

**PASS.**

## ADS-07 — Same currency invalid aggregation

`100 EUR salary` and `100 EUR liability`.

Expected: same currency alone does not authorize sum/net semantics.

**PASS.**

## ADS-08 — Sign misuse

`-50 EUR` appears in provider data.

Expected: sign does not universally mean expense/debit without source/domain meaning.

**PASS.**

## ADS-09 — Shared budget privacy

Family trip budget visible to all; payer bank balance private.

Expected: shared MonetaryAmount does not expose private source/account data.

**PASS.**

## ADS-10 — Actor display currency

Actor A views EUR; Actor B views USD.

Expected: projections differ; source amount remains unchanged.

**PASS.**

## ADS-11 — AI extraction

OCR reads receipt `€87.20`.

Expected: extracted MonetaryAmount may be proposed/observed with provenance; AI extraction is not automatically Actual/payment truth.

**PASS.**

## ADS-12 — AI invented currency

Text says `cost 100` with no currency.

Expected: AI must not silently invent EUR from user locale.

**PASS WITH HARDENING.**

## ADS-13 — Equal values, distinct contexts

Two unrelated costs are both `50 EUR`.

Expected: value equality does not merge contextual records.

**PASS.**

## ADS-14 — Budget overmodeling

Trip has `Budget 1,000 EUR` and weekly envelope `250 EUR`.

Expected: budget meaning belongs to contextual scope/time/criteria; no universal Budget entity required by MonetaryAmount.

**PASS.**

## ADS-15 — Specialist finance pressure

Connected bank exposes accounts, transactions, settlement states and fees.

Expected: adapter/specialist model may preserve those semantics; general MonetaryAmount does not become universal ledger/account ontology.

**PASS.**

ADS verdict:

```text
COMPLETE
```

---

# 7. Accepted hardenings MON-01..38

```text
MON-01  MonetaryAmount is reusable value semantics, not entity/root.
MON-02  Number alone != MonetaryAmount.
MON-03  MonetaryAmount = numerical amount + unambiguous currency semantics.
MON-04  MonetaryAmount != Quantity.
MON-05  Currency != ordinary Quantity Unit semantics.
MON-06  Currency vocabulary != native Currency entity.
MON-07  External currency standards are vocabulary/evidence, not ontology authority.
MON-08  Currency symbol alone is not universally sufficient identity.
MON-09  MonetaryAmount != Budget.
MON-10  MonetaryAmount != Price/Cost/Estimate/Balance/Transaction/FinancialAccount.
MON-11  MonetaryAmount != Resource.
MON-12  MonetaryAmount != Observation/Actual/Evidence/Provenance.
MON-13  Equal monetary values do not create shared entity identity.
MON-14  FX rate is not intrinsic state of MonetaryAmount.
MON-15  Cross-currency conversion requires applicable conversion basis.
MON-16  Converted value is derived, not source mutation.
MON-17  Consequential FX basis preserves rate/source/time/purpose where material.
MON-18  current FX != historical FX.
MON-19  reference rate != transaction/settlement rate automatically.
MON-20  No universal latest/provider/reference-rate winner.
MON-21  Consequential historical conversion basis must remain reconstructible.
MON-22  Missing FX != zero/equivalence.
MON-23  Cross-currency comparison requires an applicable basis.
MON-24  Same currency does not authorize every aggregation.
MON-25  Sign does not universally mean income/expense/debit/credit.
MON-26  Precision/rounding must not be fabricated.
MON-27  Source amount != converted/display presentation.
MON-28  Actor display-currency preference != source mutation.
MON-29  Shared amount visibility != private financial-source visibility.
MON-30  AI conversion/proposal requires attributable basis where consequence matters.
MON-31  Budget is contextual semantics over MonetaryAmount, not root.
MON-32  Price/Cost are contextual meanings around MonetaryAmount.
MON-33  Tax/fee/accounting decomposition is separate.
MON-34  Ledger/Transaction/FinancialAccount ontology is not accepted here.
MON-35  Trading/advice/portfolio semantics are outside current general kernel.
MON-36  Crypto/points/generalized value-instrument ontology is not accepted without separate product need.
MON-37  Decimal storage/minor-unit/rounding/FX-provider algorithms are later-stage concerns.
MON-38  No SQL/API/persistence shape is accepted.
```

---

# 8. Dependency classification

```text
REQUIRED NOW
- MonetaryAmount value semantics                 RESOLVED
- Quantity boundary propagation                  REQUIRED PROPAGATION
- Observation boundary propagation               REQUIRED PROPAGATION
- Whole-Domain repair integration                REQUIRED PROPAGATION

ALREADY COVERED / COMPOSED
- Resource boundary                              existing semantics
- Criterion/Evaluation usage                     existing semantics
- Actual/Evidence/Provenance ownership            existing semantics
- Decision/Reconciliation/Version boundaries      existing semantics
- Visibility / Multi-Actor privacy                existing semantics

SPECIALIST / OUTSIDE GENERAL KERNEL
- FinancialAccount / ledger / transaction lifecycle
- accounting classification
- settlement/tax/securities/trading/portfolio semantics
- generalized crypto/token/points instruments

ENGINEERING STAGE — NOT SEMANTIC DEBT
- decimal precision/scale
- minor-unit storage
- rounding implementation
- FX provider/API/caching
- persistence/query/API shape
```

Final semantic debt for this candidate:

```text
SEMANTIC SAFE DEFERRED  0
SEMANTIC UNCLASSIFIED   0
SEMANTIC UNRESOLVED     0
STRUCTURAL REOPEN       0
```

---

# 9. Propagation target

Required canonical propagation:

1. add `concepts/monetary-amount.md`;
2. append Quantity boundary/old dependency resolution;
3. append Observation monetary-value boundary/old dependency resolution;
4. propagate through Data/Subjects, deferred register, Cross-Cluster, Multi-Actor, Language Map, Domain README, workstream and Whole-Domain audit;
5. perform remote compare/fetch/read QA;
6. only then append `monetary-amount-v0-validation-part-2.md` with POST-WRITE QA PASS / CLOSED.

No SQL/API/logical-persistence work is authorized by this validation.
