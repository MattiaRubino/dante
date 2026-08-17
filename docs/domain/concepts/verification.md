# Verification v0

**Status:** Current accepted semantic baseline — resolved without new primitive  
**Accepted:** 2026-08-16  
**Validation standard:** Domain Validation Methodology v3  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0

## Canonical definition

> **Verification is a bounded evaluative purpose in which materially applicable Criteria are applied to relevant Evidence to assess whether a specific target, claim, state or result sufficiently satisfies defined requirements for a particular purpose and context. Verification uses Criterion / Evaluation semantics; it does not establish universal truth, create Authority, or replace the target, Evidence, Provenance or Confirmation.**

Verification answers:

> **For this target, purpose and context, do the applicable Criteria and relevant Evidence sufficiently support the required assessment?**

Canonical shape:

```text
target / claim / state
        +
applicable Criterion
        +
relevant Evidence
        ↓
     Evaluation
        ↓
verification-purpose assessment
```

This is not a new universal pipeline, entity or persistence schema.

## Classification

```text
Verification
✅ canonical purpose-specific vocabulary/profile
✅ Criterion / Evaluation semantics
✅ may be historically material where consequence requires
❌ independent universal primitive/root
❌ universal truth mechanism
❌ universal workflow/state machine

Verifier
✅ contextual Actor role
❌ universal entity/root

verified
✅ contextual assessment/projection where meaningful
❌ universal stored boolean/status
❌ proof of universal truth

VerificationResult universal primitive
❌ rejected

Generic Verification / Validation root
❌ rejected
```

## Verification versus Criterion / Evaluation

Criterion specifies what is checked. Evidence provides materially relevant information. Evaluation applies the applicable Criterion to relevant Evidence/context and yields an assessment. Verification names a bounded purpose/profile of that Evaluation.

```text
Criterion
= what/how to check

Evidence
= relevant information

Evaluation
= application + assessment

Verification
= evaluation purpose/profile
```

Therefore Verification does not duplicate Criterion identity, Evidence identity or Evaluation process/result semantics.

## Verification versus Confirmation

Confirmation is a contextual attestation by a confirmer toward a specific target/material version/purpose. Verification is an evidence/criteria-based assessment purpose.

```text
Verification != Confirmation
```

Valid combinations include:

```text
Verification = PASS
Confirmation = absent
```

and:

```text
Verification = FAIL / INDETERMINATE
Confirmation = "I confirm this is what I observed"
```

Neither state manufactures the other.

## Verification versus Acknowledgement and comprehension

```text
Acknowledgement
= explicit taking-notice

Verification
= bounded evidence/criteria-based assessment

comprehension
= stronger understanding semantics, separately reviewable
```

Therefore:

```text
Verification != Acknowledgement
Verification != comprehension
Acknowledgement != comprehension
```

Verification v0 does not absorb or resolve whether LifeOS needs an independently meaningful comprehension/check-understanding capability.

## Verification versus Evidence

Evidence is contextual evaluative use of information. Verification consumes relevant Evidence through Criterion/Evaluation semantics.

```text
Evidence exists
!= verification succeeded
```

No Evidence is not automatically failure. Missing or insufficient Evidence may yield unknown/indeterminate assessment unless a justified completeness rule gives absence negative meaning.

## Verification versus truth, Actual and Outcome

```text
verified-for-purpose != universal truth
Verification != Actual
Verification != Outcome
```

Verification assesses a target; it does not rewrite the target or establish that real-world realization/result occurred merely because a check passed.

Cryptographic/authenticity verification may establish a bounded property of an artifact or credential while leaving embedded claims independently contestable.

## Verification versus Provenance

Provenance explains origin, attribution and material evolution. Verification evaluates under applicable Criteria/Evidence.

```text
Verification != Provenance
```

A provenance fact may influence admissibility or interpretation without becoming Verification itself.

## Verification versus Decision / Approval / Authority

```text
Verification != Decision
Verification != Approval
Verification != Authority
```

A Verification assessment may become input to a Decision or policy, but it does not choose a governed result or grant governance/effect power. A verifier does not gain Authority merely by performing a verification-purpose Evaluation.

## Verification versus Conditional Policy

A Verification assessment may be used as activation basis by an applicable Conditional Policy.

```text
Verification assessment
→ may be policy input

Verification
!= Conditional Policy
!= downstream response
```

The assessment itself does not initiate action without separately applicable policy/operation semantics.

## Target and material-state binding

Where consequence requires reconstruction, Verification must remain bound to the materially relevant target state, Criterion state and Evidence/source basis that actually applied.

```text
S1 verified under C1/E1
later target materially changes to S2
→ S1 assessment remains history
→ S2 is not silently verified
```

Likewise a materially changed Criterion/procedure does not silently carry prior Verification forward.

Technical storage/provider revision alone is not necessarily semantic material change.

## Correction and conflict

Later source correction may change current evaluation without erasing consequential historical assessment basis.

Competing Verification assessments may coexist:

```text
Verifier A → supported
Verifier B → indeterminate
```

No universal rule is accepted such as:

```text
latest wins
provider wins
user wins
manager wins
highest-confidence wins
AI wins
```

Reconciliation/Decision/Authority remain separately owned where a bounded current interpretation is needed.

## Multi-Actor semantics

The following may differ:

```text
subject
source Actor
recorder
Evidence selector
evaluator / verifier
Authority holder
represented party
viewer
beneficiary
```

A verifier may be external/accountless. Verifier identity does not require Account identity.

Private Evidence may support a bounded authorized Verification result without forcing disclosure of the private basis:

```text
private Evidence
→ authorized verification-purpose Evaluation
→ shareable bounded result
```

Result Visibility and Evidence/source Visibility remain independently governed.

## AI boundary

AI may propose Criteria, identify candidate Evidence, perform an authorized deterministic Evaluation, surface contradictions, or propose a Verification assessment.

AI does not thereby create:

```text
human Confirmation
human comprehension
Authority
universal truth
Source Precedence
permission to disclose private Evidence
```

## Specialist boundary

Identity verification, digital signatures, clinical verification, certification, testing/calibration and regulated assurance may require specialist rules, statuses and lifecycle. Those systems are evidence for adapters/extensions and bounded domain semantics; they do not justify a universal LifeOS `VerificationResult` root.

## Canonical hardenings — VER-01..26

```text
VER-01  Verification is canonical purpose vocabulary over Criterion/Evaluation, not a new primitive.
VER-02  Materially relevant target/state must be identifiable where consequential.
VER-03  Verification uses applicable Criterion semantics.
VER-04  Evidence retains independent source/use semantics.
VER-05  Verification != Evidence.
VER-06  Verification != Confirmation.
VER-07  Verification != Acknowledgement.
VER-08  Verification != comprehension.
VER-09  Verification != Decision / Approval.
VER-10  Verification does not create Authority.
VER-11  Verifier is contextual Actor role, not entity/root.
VER-12  Verifier role does not grant Authority.
VER-13  Verification != Actual / Outcome.
VER-14  Verification != Provenance.
VER-15  Assessment does not automatically make target state effective/current.
VER-16  verified-for-purpose != universal truth.
VER-17  authenticity verification does not prove every embedded claim true.
VER-18  no Evidence != failed Verification by default.
VER-19  insufficient Evidence may remain indeterminate.
VER-20  material target change does not silently inherit prior Verification.
VER-21  material Criterion/procedure change does not silently carry forward prior Verification.
VER-22  source correction may alter current assessment without erasing consequential history.
VER-23  conflicting Verification assessments may coexist.
VER-24  no universal LWW/newest/provider/highest-confidence winner.
VER-25  AI evaluation does not fabricate Confirmation, Authority or universal truth.
VER-26  no universal VerificationResult/Validation root/table/API is accepted here.
```

## SAFE DEFERRED

### Comprehension / check-understanding
Owner: future common-ground / cognitive-state review.  
Reopen when consequential ordinary LifeOS coordination must preserve `understood` independently from Acknowledgement, Confirmation and Evaluation.  
Re-test: CORE-03/04/12, MA-05/13/15/17, XCON-04/05.

### Specialist verification / certification
Owner: specialist integration/domain review.  
Reopen when a specialist workflow requires common kernel semantics that cannot remain in adapter/domain-specific structures.  
Re-test identity, lifecycle, Authority, Evidence, Version and specialist-system boundaries.

### Assurance / confidence scales
No universal confidence/assurance level is accepted. Reopen only when a cross-domain stable semantic need is evidenced.

### Procedure / checklist structure
Owner: Plan/Activity + Criterion/Evaluation review. Reopen if a reusable verification procedure cannot be expressed without new semantic identity.

### Persistence / retention / API
Historical material Verification may require durable Evaluation snapshots, but exact logical/physical/API representation remains downstream.

## Final semantic position

```text
VERIFICATION v0

RESOLVED WITHOUT NEW PRIMITIVE

Verification
= canonical purpose-specific Criterion / Evaluation semantics

CORE  PASS WITH HARDENING
MA    PASS WITH HARDENING
XCON  PASS WITH HARDENING
ADS   COMPLETE

NEW KERNEL PRIMITIVE  NO
REOPEN                0
UNCLASSIFIED          0
```

Normative validation: `../checkpoints/verification-v0-validation.md`.
