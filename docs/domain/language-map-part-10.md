<!-- LIFEOS-CANONICAL-CONTINUATION document="language-map.md" follows="language-map-part-9.md" -->
> **Canonical continuation of the single logical LifeOS Domain Language Map.** Earlier terminology remains preserved; this physical continuation records Verification v0 vocabulary only.

# 2026-08-16 — Verification terminology

## Canonical term — Verification

> **Verification is bounded purpose-specific Criterion / Evaluation semantics used to assess whether a target, claim, state or result sufficiently satisfies applicable requirements using relevant Evidence for a defined purpose/context.**

Use when the semantic question is:

> **Does the applicable Criterion/Evidence basis sufficiently support this assessment for this purpose?**

## Canonical vocabulary

```text
Criterion
what/how is evaluated

Evidence
information materially relevant to the evaluation

Evaluation
application of applicable Criterion to relevant Evidence/context

Verification
bounded purpose/profile of Evaluation

Verifier
contextual Actor role in that verification-purpose evaluation

verified-for-purpose
contextual assessment/projection, not universal truth
```

## Canonical separations

```text
Verification != Criterion
Verification != Evidence
Verification != Confirmation
Verification != Acknowledgement
Verification != comprehension
Verification != Provenance
Verification != Decision / Approval
Verification != Authority
Verification != Actual / Outcome
Verification != Reconciliation
Verification != Conditional Policy
```

## Preferred wording

Prefer:

```text
verification-purpose Evaluation
Verification assessment
verified for this purpose/context
insufficient Evidence
indeterminate assessment
verifier Actor
```

Avoid kernel claims such as:

```text
universally verified
verified = true everywhere
VerificationResult root
Validation root
Verifier entity
```

unless explicitly referring to a specialist/external system vocabulary rather than LifeOS kernel semantics.

## Confirmation boundary

```text
Verification
= evidence/criteria-based assessment purpose

Confirmation
= contextual attestation by a confirmer
```

Neither manufactures the other.

## Acknowledgement / comprehension boundary

```text
Acknowledgement = took notice
Verification      = evaluated against requirements/evidence
comprehension     = understood; separately reviewable
```

`Verification != comprehension` is canonical. Comprehension/check-understanding remains SAFE DEFERRED.

## Truth / Authority guardrails

```text
verified-for-purpose != universal truth
Verification != Authority
Verifier role != Authority
Verification assessment != effective target state automatically
```

## Missing/conflicting data guardrails

```text
no Evidence != failed Verification
insufficient Evidence may remain unknown/indeterminate
conflicting assessments may coexist
```

No universal newest/provider/user/manager/AI/highest-confidence winner is accepted.

## Rejected current kernel roots

```text
Verification
VerificationResult
Validation
Verifier
verified boolean/status
```

The rejection is about independent universal roots/state. `Verification` remains canonical vocabulary/profile over Criterion / Evaluation semantics.

Normative references:

- `concepts/verification.md`;
- `checkpoints/verification-v0-validation.md`.
