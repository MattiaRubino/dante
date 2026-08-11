# Multi-Actor Readiness Checkpoint v0

**Status:** PASS WITH CROSS-CUTTING HARDENING  
**Validated:** 2026-08-11  
**Branch:** `feature/domain-model`  
**Scope:** Intention & Execution v0 + Time v0

## Purpose

This checkpoint verifies whether the first two validated LifeOS Domain Atlas clusters can support future multi-user and multi-actor collaboration without structural redesign.

The checkpoint is deliberately narrower than a full collaboration design.

It asks:

> **Do the existing concepts remain semantically correct when one real-world object may involve several actors, several resources, actor-specific state, private facts, different authorities, and actors who do not have LifeOS accounts?**

The answer is currently **yes**, with explicit hardening recorded in `../multi-actor-readiness-v0.md`.

---

## Scope reviewed

### Intention & Execution

- Goal v0
- Plan v0
- Activity v0
- Event v0
- Routine v0
- Milestone v0

### Time

- Occurrence v0
- Schedule v0
- Session v0
- Temporal Constraint v0
- Recurrence v0
- Availability & Capacity v0

No SQL, API, permissions, organization, membership, or messaging model was fixed by this checkpoint.

---

## Validation questions

Each concept was tested against:

1. Can identity survive a change of responsible/participating actor?
2. Can ownership differ from participation?
3. Can subject/beneficiary differ from performer?
4. Can several actors participate in one shared object without semantic duplication?
5. Can actor-specific state coexist with shared canonical state?
6. Can one actor decline/modify personal state without changing the shared object for everyone?
7. Can a non-LifeOS person still be represented as involved?
8. Can Schedule remain shared while capacity impact differs by actor/resource?
9. Can private source facts produce safe shared derived projections?
10. Can authority differ among participants?
11. Can AI operate without gaining authority beyond the actor/policy it represents?
12. Does multi-actor support require a new primitive in the first two clusters?

---

## Scenario matrix

| Scenario | Result | Key finding |
|---|---|---|
| Dinner with friends | PASS | one Event + actor-scoped participation; no per-user Event copies required |
| Work meeting | PASS | Schedule can be shared while participant responses differ |
| Household recurring chore | PASS | one Routine/Recurrence; responsibility may rotate per Occurrence |
| Shared trip Goal/Plan | PASS WITH HARDENING | Goal/Plan identity must not imply one mandatory owner |
| Activity reassignment | PASS WITH HARDENING | Activity identity survives assignee change |
| Shift swap | PASS | Event/Occurrence may stay fixed while participation/assignment changes |
| Caregiver + assisted person | PASS WITH DEFERRED SUBJECT MODEL | owner, subject, performer can differ |
| Medical appointment | PASS | Event subject/participant/availability can remain distinct |
| Collaborative physical task | PASS WITH SESSION HARDENING | one Session may represent one joint execution episode with actor-specific participation |
| Surgical team + room/equipment | PASS | Event + Activity + Constraint + multi-resource Capacity remain composable |
| Private appointment used for free/busy | PASS WITH PRIVACY REQUIREMENT | derived unavailability need not disclose private source |
| External/non-LifeOS participant | PASS WITH FUTURE ACTOR MODEL | domain involvement must not depend on Account identity |

---

# Concept results

## Goal v0 — PASS WITH HARDENING

Current semantics remain valid, but personal-first wording must not imply one mandatory user-owner.

Required interpretation:

```text
Goal identity
!= owner/governor
!= stakeholder
!= subject
!= contributor
```

A Goal may later be personal, shared, team-oriented, caregiving-oriented, or organizational without becoming a different Goal primitive.

No new shared-goal primitive is justified yet.

---

## Plan v0 — PASS WITH HARDENING

Plan already has independent identity from Goal and coordinated work.

Multi-actor hardening:

```text
Plan identity
!= coordinator
!= contributor
!= responsible actor
```

A Plan may later coordinate work across several actors and resources.

No TeamPlan/SharedPlan primitive is justified.

---

## Activity v0 — PASS WITH MATERIAL HARDENING

Activity remains the intended actionable work.

The earlier personal wording `the user intends to perform` is too narrow as a universal invariant.

Required interpretation:

```text
Activity
= actionable intended work

Actor relationships
= requester / assignee / responsibility / performer / subject as applicable
```

Assignment changes must not automatically change Activity identity.

No separate AssignmentActivity primitive is justified.

---

## Event v0 — PASS / ALREADY STRONG

Event already separates occurrence-centred identity from participation, response, attendance, Schedule, and Actual.

Multi-actor hardening mainly makes existing implications explicit:

```text
Event identity
!= organizer
!= participant
!= participant response
!= actual attendance
```

A shared Event normally remains one Event even when participants hold different actor-scoped states.

---

## Routine v0 — PASS WITH MATERIAL HARDENING

Routine remains recurring behavior/execution policy.

Required rule:

```text
Routine identity != performer
```

A household/team Routine may produce Occurrences assigned to different actors over time without duplicating the Routine.

Responsibility rotation is not Recurrence semantics by default.

---

## Milestone v0 — PASS

Milestone is contextual checkpoint semantics and does not intrinsically depend on one actor.

Hardening:

```text
Milestone identity != stakeholder/governor
```

No structural change is required.

---

## Occurrence v0 — PASS WITH HARDENING

Occurrence already has stable identity independent from current Schedule and Actual.

Extend the identity rule:

```text
Occurrence identity != assigned actor
```

A one-off reassignment does not create a new Occurrence.

---

## Schedule v0 — PASS WITH IMPORTANT AUTHORITY CLARIFICATION

Schedule remains accepted temporal assignment.

Multi-actor clarification:

> **Accepted Schedule means canonical temporal assignment under the governing authority/context of the scheduled subject. It does not mean that every participant accepted participation.**

Therefore:

```text
Schedule acceptance != participant response
Schedule identity   != capacity owner
```

---

## Session v0 — PASS WITH MATERIAL HARDENING

Session remains one logically continuous actual execution episode.

Multi-actor test exposed a distinction that must be preserved later:

```text
one collaborative execution episode
may involve several performers
```

while actor-specific participation intervals/effort may differ.

Current rule:

> **Session identity is determined by logical execution continuity, not performer count and not merely timestamp overlap.**

The exact group-Session versus actor-participation persistence model is deferred to Actual/Relationship work.

No new Session primitive is justified now.

---

## Temporal Constraint v0 — PASS WITH SCOPE/AUTHORITY HARDENING

Temporal Constraint already distinguishes rule strength from authority/mutability.

Multi-actor requirement:

- the governed subject/scope must remain explicit;
- authority to revise/override may differ by actor;
- one actor's personal constraint is not automatically a shared constraint on all actors.

No redesign required.

---

## Recurrence v0 — PASS

Recurrence remains repeating/generative pattern semantics.

Important negative rule:

> **Actor assignment rotation must not be absorbed into Recurrence merely because it repeats.**

A future rotation/assignment policy may reference recurrence or cycles while preserving distinct responsibility semantics.

---

## Availability & Capacity v0 — PASS / ALREADY STRONG

This concept family is already resource-oriented rather than intrinsically user-oriented.

A shared Schedule may create independent claims against:

- several people;
- rooms;
- vehicles;
- devices;
- equipment;
- other schedulable resources.

Participant response and capacity effect remain separate.

Privacy requirement added:

> **An authorized free/busy or capacity projection must not require revealing the private source fact that produced it.**

---

# Cross-cutting invariants accepted by this checkpoint

1. Domain object identity is not account identity.
2. Domain object identity is not automatically ownership.
3. Ownership/stewardship is not participation.
4. Participation is not responsibility.
5. Responsibility/assignment is not actual performance.
6. Performer is not necessarily subject/beneficiary.
7. Visibility is not authority.
8. Provenance/source is not ownership.
9. A non-LifeOS actor may participate in domain reality.
10. Shared canonical state may coexist with actor-scoped state.
11. Actor-scoped state may be private even when the shared object is visible.
12. Assignment changes do not automatically replace Goal/Plan/Activity/Routine/Occurrence/Event identity.
13. Participant response does not change shared Event Schedule automatically.
14. One shared Schedule may generate multiple actor/resource Capacity claims.
15. Session identity does not require exactly one performer.
16. Private facts may generate authorized derived projections without source disclosure.
17. Authority to modify a shared object is explicit future semantics and is not inferred from mere participation.
18. AI authority is bounded by the actor/principal and approved policy under which it acts.
19. Collaboration support must not require duplicating one shared real-world object for every user.
20. Personal-first UX must not become a single-user kernel invariant.

---

# Reductio checks

## Make `user_id` the universal owner/participant/performer

**FAIL.**

Breaks caregiving, shared Goals, team work, external participants, reassignment, shift swaps, and non-LifeOS people.

## Duplicate shared objects per user

**FAIL.**

Creates synchronization ambiguity, competing Schedule truth, duplicate Event lifecycle, and expensive reconciliation.

## Make participant response part of Event/Schedule state

**FAIL.**

One participant declining would incorrectly mutate shared Event semantics.

## Make assignment part of Activity identity

**FAIL.**

Reassignment would destroy work continuity/history.

## Make every collaborative execution one Session per actor

**FAIL AS UNIVERSAL RULE.**

Some execution is genuinely one shared episode; actor-specific participation should be representable without forcing semantic duplication.

## Make every collaborative execution one Session only

**FAIL AS UNIVERSAL RULE.**

Independent simultaneous execution attempts may need separate Session identities.

Therefore Session cardinality must follow logical execution continuity rather than actor count.

---

# Remaining dependencies

The checkpoint intentionally defers the following to later work:

- Actor / Person / Account / Principal;
- Subject and beneficiary semantics;
- Organization / Team / Household / Workspace;
- semantic Relationship model;
- Assignment / Responsibility / Role;
- Authority / permissions / visibility;
- Actual and actor-specific execution attribution;
- Provenance and correction authority;
- Version/conflict/concurrency semantics;
- invitation and collaboration lifecycle;
- external identity/federation;
- messaging/comments/notifications;
- exact persistence/API model.

The full Collaboration Discovery Simulation is still required and may reopen these decisions.

---

# Decision

```text
Intention & Execution v0
PASS
+ multi-actor hardening applied as cross-cutting guardrail

Time v0
PASS
+ multi-actor hardening applied as cross-cutting guardrail

Structural redesign required now
NO

New mandatory primitive required now
NO
```

The first two clusters remain validated current baselines.

All subsequent Domain Atlas work must apply the Multi-Actor Compatibility Test defined by the validation-methodology addendum and the guardrails in `../multi-actor-readiness-v0.md`.
