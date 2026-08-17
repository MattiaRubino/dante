<!-- LIFEOS-CANONICAL-CONTINUATION document="representation-framework-v1.md" follows="representation-framework-v1-part-4.md" -->
> **Canonical continuation of `representation-framework-v1.md`.** This Part 5 records Integrated A+B+C+D hardening.

# 2026-08-17 — Integrated A+B+C+D representation hardening

## 41. `current` is axis-qualified

Logical representations MUST NOT use one unqualified semantic `current` flag for both:

```text
knowledge-current / accepted-current
world-current / applicable-now
```

A current knowledge state may describe a historically ended condition.

## 42. Unknown applicability

Applicability must be able to remain unresolved/unknown when the owner/source cannot establish current validity.

```text
unknown != active
unknown != inactive
unknown != permanent
```

Physical projections may use tri-state/multi-state representations, but exact vocabulary remains owner/profile-specific.

## 43. Applicability is not MaterialStateRef identity

```text
MaterialStateRef
= address of material state

applicability
= semantic facet/state interpreted under owner/time context
```

A MaterialStateRef does not imply truth, currentness, applicability or Visibility.

## 44. Historical relevance

Knowledge/retrieval projections may retain/index information that is no longer currently applicable.

```text
not applicable now
!= not retrievable
!= irrelevant to every query
```

Retrieval ranking/purpose must not change canonical applicability.

## 45. Continuing-state establishment

Point Observation or AI inference cannot silently manufacture a continuing condition/state.

A continuing state must be owned by an applicable typed owner/profile and preserve the actual establishment/reconciliation/source path.

## 46. Projection axis contract

Where material, LR-08 knowledge/retrieval projections may carry derived fields for:

```text
semantic owner/reference
MaterialStateRef
world/effective applicability
knowledge/acceptance currentness
epistemic/source nature
query relevance/ranking
Visibility eligibility
```

These may be denormalized for speed but remain projections.

## 47. Bitemporal physical mapping

A later Physical Model may map selected owner histories to valid-time/transaction-time structures.

That mapping must not infer:

```text
transaction-current = canonical current interpretation universally
valid-now = query relevance universally
row history = material semantic history automatically
```

## 48. Simple-case contract

For a simple current personal fact/state, UI/runtime may expose only the natural result. The additional axes may remain implicit/derived when unambiguous.

Precision is required in the logical model; bureaucracy is not required in ordinary product interaction.