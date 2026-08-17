# Ownership v0

Status: **PASS WITH HARDENING**

Ownership is a **specific contextual relation family** describing that an eligible owner bears the ownership relation to a bounded owned referent within an applicable context. Ownership is not an Asset identity, Actor identity, Authority grant, Visibility grant, Responsibility state, Possession state or Custody state.

```text
eligible owner
→ Ownership
→ bounded owned referent
```

The core question is:

> **Who is contextually established as owner of this referent under the applicable ownership basis?**

`Owner` is a contextual role established by Ownership. It is not a native entity/root.

## Canonical boundaries

```text
Ownership != Asset identity
Ownership != Possession
Ownership != Custody
Ownership != Responsibility
Ownership != Coordination Stewardship
Ownership != Authority
Ownership != Visibility
Ownership != Membership
Ownership != Contribution
Ownership != Allocation
Ownership != Actual use
```

The same Actor may coincide across several of these relations, but coincidence does not collapse their semantics.

## Identity continuity

Ownership is external to the owned referent's native identity.

```text
new owner != new Asset
ownership transfer != Asset replacement
ownership correction != Asset correction automatically
```

A materially continuous Asset may survive sale, gift, transfer or correction of ownership attribution without becoming a new Asset.

## Establishment and transfer

Ownership may be established, changed, transferred, disputed or corrected through an applicable domain-specific basis. v0 deliberately does not impose one universal legal or transactional establishment workflow.

Therefore:

```text
Proposal != Ownership
Request != Ownership
Agreement != Ownership automatically
Decision != Ownership automatically
payment != Ownership automatically
handover != Ownership automatically
Possession change != Ownership change automatically
```

These facts may be Evidence or components of a specialist process, but none universally manufactures Ownership.

## Current, historical and conflicting claims

Ownership is consequence-sensitive where ownership history matters.

```text
current ownership != historical ownership
correction != silent overwrite
material change != automatic carry-forward
```

Conflicting ownership assertions may coexist pending applicable reconciliation. No universal newest-source, creator, provider, manager, possessor or highest-confidence winner is accepted.

Unknown ownership is not negative ownership truth.

## Multi-owner and Collective boundary

Several owners may coexist where the applicable semantics truthfully support co-ownership.

```text
multiple owners != Collective automatically
Membership != Ownership
```

A true Collective may itself bear Ownership when the Collective referent is genuinely the owner. That does not imply every member personally owns the referent, and member ownership does not automatically create Collective Ownership.

Exact legal capacity, ownership shares and jurisdiction-specific co-ownership mechanics remain specialist/deferred semantics.

## Authority and Visibility

Ownership does not itself define all governance powers or disclosure permissions.

```text
Owner != all-powerful Authority
Owner != universal Visibility entitlement
```

Where ownership legitimately contributes to an Authority or Visibility decision, that effect remains owned by the applicable Authority/Visibility/policy semantics rather than by Ownership alone.

## Resource and Allocation boundary

An owned Asset may play Resource role, but:

```text
Ownership != Resource role
Ownership != Resource Allocation
Ownership != Actual use
```

A non-owner may be allocated or use an Asset; an owner may never be allocated or use it in a given context.

## Possession boundary

Ownership and Possession may coincide, but neither implies the other universally.

```text
owner may not possess
possessor may not own
ownership transfer may occur without immediate possession change
possession change may occur without ownership transfer
```

## Custody boundary

Custody is not an Ownership subtype. Custody expresses a bounded entrusted/safeguarding holding profile built from possession/holding plus applicable responsibility and governance basis where relevant.

```text
Custodian != Owner automatically
Owner != Custodian automatically
```

## Non-goals

Ownership v0 does **not** establish:

- legal title or jurisdiction-specific property law;
- deeds, registries or conveyancing workflows;
- beneficial ownership;
- liens, usufruct, encumbrances or security interests;
- intellectual-property ownership;
- financial/accounting ownership;
- co-ownership percentages/shares;
- universal `Owner` entity/root;
- SQL/API/persistence shape.

These require explicit product need and their owning specialist review.

## Canonical result

```text
OWNERSHIP v0
SPECIFIC CONTEXTUAL RELATION FAMILY
PASS WITH HARDENING

Owner
CONTEXTUAL ROLE
NOT NATIVE ENTITY / ROOT
```

Normative validation: `../checkpoints/ownership-possession-custody-v0-validation.md`.
