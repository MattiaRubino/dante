# Membership v0

**Status:** Current accepted baseline — propagation pending final QA  
**Accepted:** 2026-08-16  
**Meaning of accepted:** best current semantic decision; reopenable with stronger evidence  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Relationships / Reasoning

## Canonical definition

> **Membership is the specific contextual relation through which an eligible native referent belongs to a Collective within a defined scope and material state, independently from Participation, Responsibility, Coordination Stewardship, Authority, Visibility, Agreement, Consent, Account/security membership and actual activity.**

Membership answers:

> **Does this native referent currently or historically belong to this Collective in the relevant scope?**

```text
native referent
     ↓
 Membership
     ↓
 Collective
```

Membership is a **specific contextual relation family/capability**, not a native entity/root and not a generic `related_to` edge.

## Identity boundary

Membership does not create a new wrapper identity for the member.

```text
Person P
Membership → Collective C
```

P remains Person P.

```text
Member
= contextual role inside Membership semantics
!= native entity/root
```

Likewise the Collective retains its own native referent identity.

## Material state and chronology

Membership may carry materially meaningful state/history where consequence requires it, such as bounded scope, start/end, current/historical status, source/provenance, applicable governance or qualified role/facet.

```text
T0 Collective C exists
T1 Anna joins C
T2 Anna is active member
T3 Anna leaves
T4 historical query
```

Required truth:

```text
current non-membership
!= never was a member
```

A correction does not silently erase prior recorded state. A material Collective identity change does not automatically carry Membership forward unless continuity is established truthfully.

## Participation boundary

```text
Membership
= belongs to Collective

Participation
= intended/response/Actual involvement in a bounded shared occurrence/interaction
```

Therefore:

```text
Membership != Participation
member != participant automatically
participant != member automatically
attendance != Membership
```

## Responsibility / Stewardship / performer

```text
Membership != Responsibility
Membership != Coordination Stewardship
Membership != expected performer
Membership != Actual performer
```

A member may hold none, some or all of those separate relations/roles.

## Authority / Visibility

```text
Membership != Authority
Membership != Visibility
```

Being a member does not automatically grant governance power or access to every Collective-related fact. Any such consequences belong to Authority/Visibility/policy semantics.

## Agreement / Consent / Decision

```text
Membership != Agreement
Membership != Consent
Membership != Decision
```

Joining a Collective does not automatically mean assent to every future term, permission for every use, or acceptance of every future collective decision.

Likewise a member's personal Agreement/Consent/Decision does not automatically become Collective-level state.

## Account / security-group boundary

```text
Membership != Account membership
Membership != ACL/security-group membership
Membership != technical role assignment
```

External security/provider representations may map to LifeOS Membership where semantics are genuinely equivalent, but provider schema/cardinality is never ontology authority.

## Subject / Actor composition

A member referent may independently play Subject or Actor roles.

```text
Membership
!= Actor
!= Subject
```

A Collective may itself play Actor or Subject role. Member and Collective roles remain independently attributable.

## Quorum / eligibility

Membership may contribute Evidence/source state for determining an eligible set, but:

```text
current Membership set
!= quorum result
!= eligible set universally
```

Eligibility may depend on additional bounded Criterion/policy/Authority semantics.

Membership changes after a consequential quorum/Decision do not rewrite the material eligible set historically used.

## Direct versus qualified relation

Use direct specific Membership semantics where the relation is semantically complete and no material independent relation state is needed.

Use a qualified Membership relation where scope, lifecycle, role/facet, governance, history, provenance or visibility materially matters.

```text
row ID / FK / M:N
!= independent domain identity
```

## Epistemic integrity

```text
unknown Membership
!= explicit non-membership

invited
!= member

observed activity
!= member automatically

technical account access
!= member automatically
```

No universal source priority, newest-write rule or AI-confidence winner is accepted.

## Accepted hardenings — COL-17..26

```text
COL-17  Membership is a specific contextual relation family, not native entity/root.
COL-18  Member is a contextual role, not wrapper identity.
COL-19  Membership does not replace native member or Collective identity.
COL-20  Membership != Participation / Responsibility / Stewardship / performer.
COL-21  Membership != Authority / Visibility.
COL-22  Membership != Agreement / Consent / Decision.
COL-23  Membership != Account/security-group membership by default.
COL-24  consequential Membership history must remain reconstructible where required.
COL-25  current member set is not universal quorum eligibility.
COL-26  M:N/cardinality/row identity does not manufacture a new primitive.
```

## SAFE DEFERRED

- stable membership-role/facet taxonomy;
- invitation/application/admission specialist flows where not reducible to Proposal/Request/Decision/Agreement;
- proxy/delegated membership rights;
- organization/legal membership constraints;
- automatic external-directory/security-group mapping;
- exact persistence/cardinality/indexing/API representation.

## Current verdict

```text
MEMBERSHIP v0

PASS WITH HARDENING

Membership
✅ specific contextual relation family/capability
✅ history-sensitive where material
✅ native referents retain their identity
❌ native entity/root
❌ generic Relationship wrapper
❌ Participation / Authority / Visibility / Agreement

Member
✅ contextual role
❌ native entity/root

REOPEN       0
UNCLASSIFIED 0
```

Repository closure remains conditional on approved propagation and remote post-write QA.
