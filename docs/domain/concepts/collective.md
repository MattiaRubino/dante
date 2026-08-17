# Collective v0

**Status:** Current accepted baseline — propagation pending final QA  
**Accepted:** 2026-08-16  
**Meaning of accepted:** best current semantic decision; reopenable with stronger evidence  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Relationships / Reasoning

## Canonical definition

> **A Collective is a scoped persistent native referent representing a materially meaningful plurality as one domain referent where that plurality has identity, state, history or agency that cannot be truthfully reduced to the current set of individual members.**

Collective answers:

> **Is this plurality itself the thing whose identity/state/history/agency matters, rather than merely a convenient set of separate referents?**

```text
materially meaningful plurality
          ↓
      Collective
          ↓
scoped native referent identity
```

Collective is a **scoped native referent concept**. It is not a universal Group/Organization superclass and does not manufacture a collective whenever several referents appear together.

## Identity boundary

```text
Collective identity
!= exact current member set
```

Ordinary membership change does not automatically create a new Collective.

```text
member joins/leaves
→ Membership state changes
→ Collective may remain the same referent
```

Conversely, a material split, merger, replacement or purpose/identity change may require a different Collective identity where treating continuity as unchanged would be false.

No universal continuity rule is accepted. Context, identity invariants and material history govern the decision.

## Set / cohort / query boundary

```text
Collective
!= arbitrary set
!= saved query
!= cohort
!= audience
!= attendee list
!= recipient list
!= candidate set
!= current eligible set
```

A query such as `all overdue tasks owned by household members` does not create a Collective. A temporary set of people in a meeting does not automatically create one either.

## Membership boundary

Membership is the specific contextual relation connecting an eligible native referent to a Collective.

```text
native referent
   ↓ Membership
Collective
```

Therefore:

```text
Collective != Membership
member != Collective
member set != Collective identity
```

Membership history may change while Collective identity remains stable.

## Actor boundary

A Collective may play Actor role when agency is truthfully attributable to the Collective under applicable governance/context.

```text
Collective
→ may play Actor role
```

But:

```text
Collective != Actor
member action != Collective action automatically
one member speaks != Collective decided automatically
```

Collective agency must not be inferred merely from membership or activity.

## Subject boundary

A Collective may be the Subject of a descriptive record where the record is genuinely about the Collective.

```text
Collective as Subject
!= every member individually has the asserted state
```

Several individual Subjects likewise do not automatically create one Collective Subject.

## Participation / Responsibility / Stewardship

Collective may participate, bear Responsibility or bear Coordination Stewardship where the respective semantics truthfully apply.

These are independent contextual relations/roles:

```text
Collective identity
!= Participation
!= Responsibility
!= Coordination Stewardship
```

Several participants/responsible actors/stewards do not automatically constitute a Collective.

## Agreement / Decision / Consent

A Collective may be a party to Agreement or may be the referent whose bounded collective Decision is established where governance semantics support that result.

However:

```text
Agreement party set != Collective identity
member assent != Collective assent automatically
member stance != Collective Decision automatically
Collective Decision != unanimous personal Agreement
```

Consent remains actor-scoped bounded permission semantics and is not inherited automatically from Collective membership or governance.

## Authority / Visibility

```text
Collective != Authority
Collective != Visibility
Membership != Authority
Membership != Visibility
```

Collective membership does not grant universal governance capability or disclosure rights. Collective-level Authority or Visibility must come from their owning semantics.

## Quorum boundary

Quorum is not part of Collective identity.

```text
Quorum
= bounded eligibility/threshold evaluation vocabulary
  under applicable governance/policy
```

Changing current Membership may change the eligible set used by a quorum evaluation without rewriting the Collective's identity.

## Chronology

Representative chronology:

```text
T0 Collective C exists
T1 Anna Membership active
T2 Luca Membership active
T3 Sara joins
T4 Criterion requires >= 2 of 3 eligible responses
T5 Anna + Luca respond
T6 Evaluation says threshold satisfied
T7 applicable governance establishes Collective Decision D1
T8 Sara leaves
T9 C remains same Collective where identity invariants remain satisfied
T10 later material split creates C2/C3 if continuity as C would be false
```

Required preservation:

- Membership changes do not silently rewrite historical eligible sets;
- prior quorum evaluations remain bound to the material eligible/policy state used;
- Collective Decision history does not become each member's personal stance;
- split/merge/replacement does not silently inherit every prior relation/state;
- historical attribution remains reconstructible where consequence requires.

## Epistemic integrity

```text
unknown membership
!= non-member

unknown Collective identity continuity
!= same Collective automatically

majority behavior
!= Collective Decision automatically
```

Conflicts may remain unresolved. No universal newest/provider/manager/creator/majority/AI-confidence winner is accepted.

## Product simplicity

Ordinary UX may use familiar labels such as household, team, family, committee, group or community where context warrants. Those product/domain labels do not each create separate kernel primitives.

The kernel distinction appears only when the plurality itself has materially useful identity/state/history/agency.

## Rejected abstractions

```text
universal Group root
universal Organization root
universal Party root
universal Team root
universal Household root
universal Family root
universal Committee root
universal Community root
member wrapper entity solely for FK convenience
saved query/cohort = Collective
attendee set = Collective
security/ACL group = Collective by default
current member set = Collective identity
```

## Accepted hardenings — COL-01..16

```text
COL-01  Collective is a scoped native referent for a materially meaningful plurality.
COL-02  Collective is not a universal Group/Organization superclass.
COL-03  Collective identity != exact current member set.
COL-04  ordinary join/leave does not automatically create a new Collective.
COL-05  material split/merge/replacement may require identity change.
COL-06  no universal continuity rule is accepted.
COL-07  arbitrary sets/queries/cohorts do not create Collective identity.
COL-08  Collective may play Actor role but Collective != Actor.
COL-09  member action does not automatically establish Collective action.
COL-10  Collective may play Subject role but collective assertion != every member assertion.
COL-11  Participation/Responsibility/Stewardship do not manufacture Collective identity.
COL-12  Agreement party set does not manufacture Collective identity.
COL-13  Membership grants neither Authority nor Visibility.
COL-14  Collective Decision does not rewrite individual member stance.
COL-15  Quorum evaluation is not part of Collective identity.
COL-16  consequential Collective identity/history must remain reconstructible where required.
```

## SAFE DEFERRED

Separately owned:

- organization/legal-entity semantics;
- household/family/couple/team/community specialist semantics if independent identity/lifecycle later proves necessary;
- collective/joint Responsibility among several distinct Actors versus Responsibility borne by one true Collective;
- collective/joint Coordination Stewardship among several distinct Actors;
- voting/ballot/proxy/delegated-vote specialist semantics;
- exact continuity mechanics for split/merge/replacement;
- security/ACL group mapping;
- persistence/API/indexing/runtime implementation.

## Current verdict

```text
COLLECTIVE v0

PASS WITH HARDENING

Collective
✅ scoped native referent
✅ independent identity where plurality itself materially matters
✅ may play Actor / Subject and other contextual roles
❌ universal Group / Organization root
❌ exact current-member-set identity
❌ arbitrary set/query/cohort

REOPEN       0
UNCLASSIFIED 0
```

Repository closure remains conditional on approved propagation and remote post-write QA.
