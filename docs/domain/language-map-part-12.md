<!-- LIFEOS-CANONICAL-CONTINUATION document="language-map.md" follows="language-map-part-11.md" -->
> **Canonical continuation of the single logical Domain Language Map.** Earlier terminology remains preserved; this physical continuation records Collective / Membership / Quorum v0 vocabulary only.

# 2026-08-16 — Collective / Membership / Quorum vocabulary

## Canonical terms

### Collective

> A scoped persistent native referent for a materially meaningful plurality whose identity/state/history/agency cannot be truthfully reduced to the exact current member set.

Use `Collective` in domain reasoning when the plurality itself is the referent.

Do not silently substitute:

```text
Group
Organization
Team
Household
Family
Committee
Community
Party
```

as universal kernel synonyms. These may be contextual/product/specialist labels.

### Membership

> The specific contextual relation through which an eligible native referent belongs to a Collective within a defined scope/material state.

`Member` = contextual role inside Membership semantics, not native entity/root.

Do not use Membership to mean:

```text
Participation
Responsibility
Coordination Stewardship
Authority
Visibility
Agreement
Consent
Account membership
ACL/security-group assignment
```

### Quorum

> Bounded governance/evaluation vocabulary for whether materially applicable eligibility and threshold conditions are sufficiently satisfied for a particular collective process/context.

Canonical semantic owner:

```text
eligibility
+
Criterion / Evaluation
+
applicable governance/policy
```

Do not model `Quorum` as a universal primitive/root.

## Required distinctions

```text
Collective != current member set
Collective != arbitrary set/query/cohort
Collective != Actor
Collective != Subject

Membership != Participation
Membership != Authority / Visibility
Membership != Agreement / Consent

quorum satisfied != Decision
quorum satisfied != Agreement
quorum satisfied != Consent
quorum satisfied != Authority
quorum satisfied != unanimous assent
```

## Allowed UX language

Simple interfaces may use familiar nouns such as:

```text
household
family
team
committee
group
community
```

when the product context is clear. UX wording must not create additional kernel primitives or alter Collective identity semantics.

## Deferred language

The following remain non-canonical kernel primitives pending separate review:

```text
Organization / Legal Entity
Vote
Ballot
Proxy Vote
Joint Responsibility
Joint Stewardship
Membership Role taxonomy
```

Normative reference: `checkpoints/collective-membership-quorum-v0-validation.md`.
