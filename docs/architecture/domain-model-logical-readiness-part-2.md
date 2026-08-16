<!-- LIFEOS-CANONICAL-CONTINUATION document="domain-model-logical-readiness.md" follows="domain-model-logical-readiness.md" -->
> **Canonical continuation of the Domain Model → Logical Model Readiness Contract.** The original contract remains historically valid for the semantic baseline it assessed. This continuation records the later second-V3 safety finding and temporarily suspends the readiness verdict until the corrected semantic kernel is revalidated.

# 2026-08-16 — Logical readiness HOLD after targeted semantic reopen

## Trigger

A later safety rerun, performed after synchronization of the accepted LifeOS North Star, demonstrated one bounded semantic gap that had not been part of the earlier readiness baseline:

```text
Living Referent
= native identity for individually tracked non-human living organisms/specimens
```

This is a semantic-model change, not merely a persistence concern. Therefore logical mapping must not start from the previous `READY` verdict as if the semantic owner set were unchanged.

## Current authority order

The existing authority rule remains unchanged:

```text
accepted current Domain Atlas / current validation checkpoints
        >
this readiness contract and its continuations
        >
legacy architecture examples
        >
provider/storage convenience
```

The new Living Referent concept and its validation are now part of the semantic owner set once repository closure QA succeeds.

## Required additional identity distinction

Any future logical model must preserve at least:

```text
Person != Living Referent != Asset
Living Referent != Subject
Living Referent != Resource

name/species/breed/cultivar != Living Referent identity
provider/tag/microchip ID != canonical Living Referent identity
owner/caregiver/location != Living Referent identity
```

A shared technical registry/discriminator/reference mechanism may still be used, but must not manufacture a universal semantic `Thing`, `Entity`, `LivingThing` or `ManagedObject` superclass.

## Required history/reconciliation pressure

Logical design must be able to represent without semantic loss:

```text
rename with identity continuity
classification correction with identity continuity
owner/caregiver/location change with identity continuity
death with historical continuity
replacement organism != prior organism
propagated specimen becoming independently tracked
provider identity reconciliation without silent merge
material correction without silent history rewrite
```

Bulk populations must not force one native identity record per organism where individual identity does not materially matter.

## Multi-actor/privacy pressure

The existing bounded-projection rule extends naturally:

```text
Visibility(Living Referent)
!= Visibility(all care/health/location/ownership/history facets)

Ownership
!= Responsibility
!= Authority
!= Visibility
```

External/accountless Persons may relate to a Living Referent without Account identity becoming domain identity.

## Current readiness verdict

The previous readiness verdict is superseded for current execution until the new owner set is fully revalidated.

```text
SEMANTIC MODEL
TARGETED REPAIR IN PROGRESS

LIVING REFERENT LOCAL V3
PASS WITH HARDENING

LIVING REFERENT REPOSITORY CLOSURE QA
PENDING

FRESH WHOLE-DOMAIN WD-01..10
REQUIRED

LOGICAL MODEL / PERSISTENCE MAPPING
HOLD

SQL / MIGRATIONS / API IMPLEMENTATION
NOT AUTHORIZED
```

Readiness may be restored only after the complete corrected semantic kernel passes the requested final V3/WD safety rerun and the Whole-Domain closure is recorded with remote evidence.

This continuation changes no PostgreSQL/hybrid-storage/provider-adapter direction by itself. It only prevents logical/physical design from beginning against a semantically stale owner set.
