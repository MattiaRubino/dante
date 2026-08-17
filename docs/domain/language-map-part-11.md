<!-- LIFEOS-CANONICAL-CONTINUATION document="language-map.md" follows="language-map-part-10.md" -->
> **Canonical continuation of the single logical LifeOS Domain Language Map.** Earlier terminology remains preserved; this physical continuation records Coordination Stewardship v0 vocabulary only.

# 2026-08-16 — Coordination Stewardship terminology

## Canonical term — Coordination Stewardship

> **Coordination Stewardship is the bounded contextual relation describing which Actor carries the ongoing burden of keeping a coordination context attended over time — noticing, remembering, monitoring, prompting, synchronizing, escalating or repairing where applicable.**

Use when the real semantic question is:

> **Who is expected to keep track of this coordination context and make sure follow-up or exception handling does not silently fall through the cracks?**

## Canonical vocabulary

```text
Coordination Stewardship
specific contextual relation family/capability

Steward
contextual Actor role in that relation

coordination action
an actual reminder / escalation / repair / monitoring action
not Stewardship state by itself
```

## Canonical separations

```text
Coordination Stewardship != Responsibility
Coordination Stewardship != Participation
Coordination Stewardship != expected performer
Coordination Stewardship != Actual performer
Coordination Stewardship != Authority
Coordination Stewardship != Visibility
Coordination Stewardship != Conditional Policy
Coordination Stewardship != Proposal / Request / Decision
Coordination Stewardship != Acknowledgement / Agreement / Consent
Coordination Stewardship != ownership / possession / custody
Coordination Stewardship != actual coordination action
Coordination Stewardship != Contribution
```

## Preferred wording

Prefer:

```text
carries Coordination Stewardship
Steward for this coordination context
coordination burden
Stewardship transfer
bounded coordination scope
```

Avoid kernel claims such as:

```text
Coordinator entity
Manager entity
Steward entity
owner = coordinator
responsible = coordinator
latest reminder sender = Steward
```

unless referring to specialist/product vocabulary rather than LifeOS kernel semantics.

## Responsibility boundary

```text
Responsibility
who is accountable for ensuring the bounded commitment is handled

Coordination Stewardship
who carries ongoing burden of keeping the coordination attended
```

Assignment/transfer of one does not silently transfer the other.

## Automation boundary

```text
Conditional Policy / automation
what response is initiated when qualifying conditions hold

Coordination Stewardship
who carries ongoing coordination burden
```

Automation may assist a Steward without becoming Stewardship automatically.

## Identity guardrail

`Steward` is a contextual Actor role, not a Person subtype, Account, Principal or universal native identity.

## Rejected current kernel roots/defaults

```text
Steward
Coordinator
Manager
generic Stewardship root
universal mental-load / fairness score
```

The rejection concerns universal independent roots/defaults. `Coordination Stewardship` remains accepted as a specific contextual relation family/capability.

Normative references:

- `concepts/coordination-stewardship.md`;
- `checkpoints/coordination-stewardship-v0-validation.md`.
