# Possession v0

Status: **PASS WITH HARDENING**

Possession is a **specific contextual relation family** describing actual holding or physical possession/control of a bounded physical referent by an eligible possessor within an applicable context.

```text
eligible possessor
→ Possession
→ bounded physical referent
```

The core question is:

> **Who actually holds or possesses this physical referent in the relevant context?**

`Possessor` / `Holder` are contextual roles, not native entity/root identities.

## Canonical boundaries

```text
Possession != Ownership
Possession != Custody
Possession != Location
Possession != Resource role
Possession != Resource Allocation
Possession != Actual use
Possession != Responsibility
Possession != Coordination Stewardship
Possession != Authority
Possession != Visibility
```

## Actuality and physicality

Possession is about actual holding/physical control, not merely intention, entitlement, planning or assignment.

```text
planned holder != Possessor
allocated Resource != Possessor automatically
owner != Possessor automatically
scheduled use != Possession
```

A possession assertion may be derived from reliable evidence, but it remains a claim about actual holding rather than a planning state.

## Location boundary

Knowing where an Asset is does not necessarily establish who possesses it.

```text
Asset located at Place P
!= Actor X possesses Asset
```

Likewise an Actor may possess a mobile Asset while its exact current location is unknown.

## Resource / Allocation / use boundary

```text
Resource eligibility != Possession
Resource Allocation != Possession
Actual use != Possession universally
```

An Asset can be allocated to Anna while still physically held by Luca. Anna may use an Asset without exclusive possession, and a possessor may hold an Asset without actively using it.

## Ownership boundary

Ownership and Possession can diverge truthfully.

Examples:

```text
owner lends camera to Luca
→ owner may remain owner
→ Luca may become possessor

camera returned
→ possession changes
→ ownership need not change
```

No ownership transfer is inferred from possession duration or physical control alone.

## Custody boundary

Custody is a bounded profile built around entrusted/safeguarding holding semantics where additional responsibility/governance basis matters.

Possession alone does not establish Custody.

```text
Possession
+ applicable safeguarding / return Responsibility
+ applicable Authority / Agreement / policy basis where relevant
→ possible Custody profile
```

Custody therefore does not become a third universal primitive/root in v0.

## Current, historical and conflicting possession

Possession may change frequently and may require historical reconstruction where consequential.

```text
current possessor != historical possessor
correction != silent overwrite
no current evidence != established non-possession
```

Conflicting possession assertions may coexist until reconciled. No universal newest/provider/owner/highest-confidence winner is accepted.

## Multi-Actor boundary

Possession need not be exclusive by ontology. Joint/shared physical possession may be represented where truthful, but v0 does not create universal exclusivity, percentage or joint-control mechanics.

Several possessors do not create a Collective automatically.

## Non-goals

Possession v0 does **not** establish:

- jurisdiction-specific legal possession;
- tenancy, bailment or rental law;
- chain-of-custody forensic procedure;
- inventory movement engine;
- location tracking model;
- exclusive-control assumptions;
- universal `Holder` / `Possessor` entity/root;
- SQL/API/persistence shape.

These require explicit LifeOS need and their owning review.

## Canonical result

```text
POSSESSION v0
SPECIFIC CONTEXTUAL RELATION FAMILY
PASS WITH HARDENING

Possessor / Holder
CONTEXTUAL ROLE
NOT NATIVE ENTITY / ROOT
```

Normative validation: `../checkpoints/ownership-possession-custody-v0-validation.md`.
