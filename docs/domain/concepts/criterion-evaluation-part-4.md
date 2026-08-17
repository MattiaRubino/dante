<!-- LIFEOS-CANONICAL-CONTINUATION document="criterion-evaluation.md" follows="criterion-evaluation-part-3.md" -->
> **Canonical continuation of the single logical Criterion / Evaluation document.** Earlier semantics remain preserved; this physical continuation records Quorum integration only.

# 2026-08-16 — Quorum integration

Collective / Membership / Quorum v0 resolves quorum threshold semantics without introducing a new primitive or evaluation engine.

Canonical decomposition:

```text
eligible set
+
applicable threshold Criterion
+
relevant Evidence / response state
↓
Evaluation
↓
quorum assessment for bounded purpose/context
```

Therefore:

```text
Quorum
= canonical bounded governance/evaluation vocabulary/profile
  over eligibility + Criterion/Evaluation

Quorum primitive/root
= REJECTED
```

Example:

```text
Eligible set: Anna, Luca, Sara
Criterion: >= 2 eligible affirmative responses
Evidence/state: Anna yes, Luca yes, Sara unknown
Evaluation: threshold satisfied
Quorum assessment: satisfied for this bounded process
```

This assessment does not itself establish:

```text
Decision
Agreement
Consent
Authority
universal truth
```

The applicable governance/policy semantics own what, if anything, follows from the assessment.

## Eligibility is contextual

Current Membership may be one source for deriving eligibility, but:

```text
Membership set != eligible set universally
```

Eligibility may depend on bounded role/facet, suspension, scope, Authority, policy or other applicable Criterion semantics.

## Missing / unknown

Existing epistemic rules remain authoritative:

```text
unknown eligibility != ineligible
no response != negative response
insufficient Evidence != failed Criterion automatically
```

An evaluation may remain unknown/indeterminate.

## Material-state history

Consequential quorum assessment must bind to the material state actually used:

```text
eligible set S1
Criterion C1
policy/governance P1
Evidence E1
→ Evaluation Q1
```

Later changes do not silently rewrite or carry forward Q1:

```text
Membership/eligibility S1 → S2
Criterion C1 → C2
policy P1 → P2
Evidence corrected
```

Current assessment may change while historical Q1 remains reconstructible where required.

## Result

```text
Criterion / Evaluation v0
PASS WITH HARDENING
REOPEN       0
UNCLASSIFIED 0

Quorum semantic pressure
RESOLVED WITHOUT NEW PRIMITIVE
```

Voting/ballot/proxy mechanics remain separately SAFE DEFERRED.

Normative downstream references:

- `collective.md`;
- `membership.md`;
- `../checkpoints/collective-membership-quorum-v0-validation.md`.
