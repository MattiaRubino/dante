# Schedule v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-11  
**Meaning of accepted:** best current decision; reopenable with stronger evidence  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Time cluster

## Canonical definition

> **Schedule is the temporal arrangement or placement of something that is intended, expected, committed, authorized, reserved, or otherwise planned to occur in time. Schedule represents planned temporal state, not realized temporal truth.**

Schedule answers:

> **When is this currently planned/accepted/expected to occur?**

It does not answer:

- whether the thing happened;
- when it actually happened;
- whether the plan succeeded;
- whether the plan was confirmed;
- who approved it;
- which proposal/request led to the current placement;
- which actor is responsible;
- which resource is available;
- whether a recurring policy generated it;
- whether it remains possible under current Capacity.

---

# 1. Schedule is planned temporal state

A Schedule is not merely a timestamp.

It is contextual temporal state attached to some target such as:

- Activity;
- Event;
- Milestone;
- Routine/Occurrence;
- Reservation/allocation candidate;
- deadline/checkpoint;
- another bounded temporal target.

A Schedule may include one or more of:

- planned start;
- planned end;
- duration expectation;
- all-day/day-level placement;
- time zone / local-time context;
- accepted temporal placement;
- recurrence-derived occurrence placement;
- material history where consequence requires it.

The exact physical shape remains deferred.

---

# 2. Schedule versus Actual

Canonical separation:

```text
Schedule
= planned/accepted temporal state

Actual
= realized temporal state
```

Example:

```text
Schedule
18:00–19:00

Actual
18:12–19:04
```

Both may be true simultaneously.

Therefore:

```text
Schedule != Actual
```

Actual execution must never overwrite Schedule history merely to make the final record look clean.

---

# 3. Proposal/request versus current Schedule

A proposed or requested time is not automatically the current accepted Schedule.

```text
proposal
Tuesday 19:00

current Schedule
Monday 18:00
```

Both may coexist.

Likewise:

```text
request to move to 20:00
!= Schedule 20:00
```

Canonical rule:

> **A proposed/requested temporal placement becomes current Schedule only through the applicable domain effect/governance process; proposal/request identity and Schedule state remain separate.**

---

# 4. Schedule versus Decision / Authority

Schedule owns the resulting temporal state.

Decision may record that a bounded question was resolved.

Authority determines who/what may legitimately make the governed effect effective.

Therefore:

```text
Schedule != Decision
Schedule != Authority
```

An approved/resolved proposal may lead to a Schedule change without becoming the Schedule object itself.

An already-authorized bounded policy may change Schedule without fabricating a new human Decision.

---

# 5. Schedule history

Where consequence warrants it, LifeOS must preserve materially relevant Schedule history.

Example:

```text
S1  Monday 18:00
S2  Tuesday 19:00
S3  Tuesday 20:00
Actual 20:18
```

Required distinctions:

```text
current Schedule
!= previous Schedule
!= proposal/request history
!= Decision history
!= Actual
```

Version/Material-State v0 provides the cross-cutting material-state discipline used by Schedule and consumers of Schedule state.

---

# 6. Material Schedule change

Not every edit is equally material.

Example:

```text
label typo corrected
```

may not matter to a prior Acknowledgement of the time.

But:

```text
15:00 -> 23:00
```

is materially relevant to many participation/availability/acknowledgement contexts.

Materiality is consumer/purpose-specific where needed.

Canonical rule:

> **A materially changed temporal placement does not silently inherit prior Acknowledgement, Participation response, Decision/Approval or other state whose meaning depended on the prior placement.**

---

# 7. Schedule versus Recurrence / Routine

A recurring policy is not the same as the Schedule of a specific occurrence.

```text
Routine / Recurrence policy
Mon/Wed/Fri 18:00

Occurrence O1 Schedule
Monday 18:00
```

Changing a future recurrence policy does not rewrite earlier occurrence Schedule history.

A one-off occurrence override does not necessarily change the recurrence policy.

Therefore:

```text
Schedule != Recurrence
Schedule != Routine
```

---

# 8. Schedule versus Temporal Constraint

A Schedule says when something is currently planned.

A Temporal Constraint says when it may/must/preferably occur.

Example:

```text
Constraint
not after 21:00

Schedule
20:00
```

Therefore:

```text
Schedule != Temporal Constraint
```

A Schedule can violate a constraint in error or under override while both states remain representable.

---

# 9. Schedule versus Capacity / Resource

Schedule does not prove feasibility.

```text
scheduled at 18:00
!= Resource available at 18:00
!= Capacity exists at 18:00
```

Likewise Resource allocation/reservation may constrain or establish feasibility but does not automatically become Schedule semantics.

---

# 10. Schedule versus Participation

An Event may have one shared Schedule and multiple actor-scoped Participation states.

```text
Event Schedule
18:00

Anna going
Luca declined
Marco no response
```

Changing the Schedule may affect those responses, but it does not collapse them.

```text
Schedule != Participation response
```

---

# 11. Schedule versus Acknowledgement

Acknowledgement records explicit taking-notice of a material target/change.

```text
Schedule changed to 19:00
Luca acknowledged that change
```

The Ack does not become the Schedule and the Schedule does not prove Ack.

```text
Schedule != Acknowledgement
```

---

# 12. Schedule versus Agreement / Consent

Parties may agree on a time before Schedule becomes effective under applicable governance.

Agreement does not automatically own current Schedule.

Consent to one bounded use/action does not create a Schedule.

```text
Schedule != Agreement
Schedule != Consent
```

---

# 13. Actor / requester / organizer

The following may differ:

```text
requester
proposer
organizer
Authority holder
Schedule editor
responsible Actor
participant
actual performer
```

Creation/editing/requesting does not automatically establish Authority or Responsibility.

Representation/on-behalf-of must preserve actual Actor and represented party where material.

---

# 14. AI boundary

AI may:

- propose candidate times;
- identify conflicts;
- summarize Schedule changes;
- request review/confirmation;
- apply an already-authorized bounded scheduling policy where permitted.

AI must not:

- treat a proposal as current Schedule;
- treat a Request as effective temporal state;
- fabricate participant acceptance/acknowledgement;
- exceed Authority;
- silently apply a stale-base proposal after material Schedule change;
- hide conflicting resource/capacity constraints;
- rewrite Schedule history to match Actual.

Canonical rule:

> **AI scheduling proposals remain proposals until the applicable domain effect legitimately changes Schedule.**

---

# 15. Simple UI versus kernel semantics

Ordinary UI can say:

```text
Tomorrow at 18:00
Move to 19:00?
Changed from 18:00 to 19:00
```

without exposing Proposal, Request, Decision, Authority or Version ontology language.

Kernel semantics must nevertheless preserve the distinction where consequence requires it.

---

# 16. Core invariants

1. Schedule is planned/accepted temporal state, not Actual.
2. Proposed/requested time != current Schedule.
3. Schedule owns current temporal placement, not Decision/Authority.
4. Material Schedule history remains reconstructible where consequential.
5. Material change does not silently inherit prior Ack/response/Decision state.
6. Schedule != Recurrence/Routine.
7. Schedule != Temporal Constraint.
8. Schedule != Resource/Capacity truth.
9. Schedule != Participation response.
10. Schedule != Acknowledgement.
11. Schedule != Agreement/Consent.
12. requester/proposer/organizer/editor != Authority holder by default.
13. Actual does not overwrite Schedule history.
14. AI proposal/request != Schedule.
15. Exact persistence and effective dating remain downstream design.

---

# 17. Rejected alternatives

Rejected:

- Schedule = timestamp field;
- Schedule = Actual;
- proposed/requested time = current Schedule;
- Schedule = Decision;
- Schedule = Authority;
- Schedule = Recurrence;
- Schedule = Constraint;
- Schedule = Reservation/Capacity;
- Schedule = Participation response;
- Schedule = Agreement;
- latest write always wins;
- Actual overwrites planned history;
- AI proposal as effective Schedule.

---

# 18. Adjacent Dependency Sweep

## RESOLVED

- Schedule ↔ Actual: planned != realized.
- Schedule ↔ Version/material state: materially relevant history/state binding uses Version discipline.
- Schedule ↔ Decision/Authority: resolution/governance separate; Schedule owns resulting temporal state.
- Schedule ↔ Acknowledgement: current placement != taking-notice.
- Schedule ↔ Participation: shared temporal state != actor-scoped response/involvement.
- Schedule ↔ Recurrence/Routine: policy != occurrence placement.
- Schedule ↔ Temporal Constraint: current plan != allowable/preferred bounds.
- Schedule ↔ Agreement/Consent: mutual assent/permission != current temporal placement.
- Schedule ↔ Representation: acting for another != temporal state.

## SAFE DEFERRED

### Proposal / request reusable identity

**Owner:** Proposal/Request review.  
**Why safe:** proposal/current/effect separation already canonical.  
**Reopening trigger:** cross-family temporal proposals/requests cannot be targeted/versioned/responded to without duplicating identities.  
**Tests:** CORE-02/03/04/06/13, MA-05/06/17, XCON-03/04.

### Resource Requirement / Allocation / Reservation

**Owner:** resource-allocation review.  
**Why safe:** Schedule does not claim feasibility or reservation ownership.  
**Reopening trigger:** common scheduling cannot represent booked/held/allocated capacity without Schedule absorbing resource state.  
**Tests:** CORE-03/04/10/13, MA-14/15, XCON-04.

### Trigger / conditional policy

**Owner:** Trigger/automation review.  
**Why safe:** Schedule may be changed by authorized policy without embedding generic condition logic.  
**Reopening trigger:** ordinary temporal automation requires Schedule itself to own trigger identity/effect semantics.  
**Tests:** CORE-03/04/13, MA-06/17, XCON-02/04.

### Exact effective dating / persistence

**Owner:** Time + logical model.  
**Why safe:** current/history/effect-time distinctions are canonical.  
**Reopening trigger:** implementation cannot reconstruct which Schedule state was applicable at T without stronger shared structure.  
**Tests:** CORE-02/09/10/13, XCON-03.

```text
REOPEN                         0
unclassified material items    0
```

---

# 19. Reopening triggers

Reopen Schedule v0 if later evidence shows that:

1. planned/current temporal state cannot remain separate from Proposal/Decision semantics;
2. Resource allocation/reservation is structurally inseparable from Schedule;
3. exact effective dating requires a materially different temporal state model;
4. Recurrence/Occurrence cannot preserve historical schedule policy without redefining Schedule;
5. product workflows require a universal booking/workflow state machine rather than bounded Schedule semantics.

Until then Schedule remains the current planned temporal-state concept.

---

# 20. Downstream closure — Proposal / Request v0 (2026-08-15)

Proposal / Request v0 resolves Schedule's historical `Proposal / request reusable identity` SAFE DEFERRED dependency without changing Schedule semantics.

Canonical chain:

```text
Proposal of temporal placement
or Request to change Schedule
!= delivery / Acknowledgement
!= Participation/family-specific response
!= Agreement / Decision / Approval
!= Authority
!= current/effective Schedule
!= later Actual
```

A Schedule Proposal identifies a materially specific candidate temporal state. A Request asks an Actor/system to review/change/respond to a bounded temporal question. Neither becomes current Schedule simply by existing.

A materially different counter-Proposal — for example 20:00 instead of 19:00 — is a distinct Proposal and does not silently inherit prior response/Acknowledgement/Decision. Version/material-state semantics preserve which candidate the actors actually considered.

Withdrawal/expiry of a Proposal/Request affects future applicability of that semantic act; it does not automatically revert a Schedule change that already became effective through applicable Decision/Authority/policy.

AI-generated candidate times remain AI Proposals and cannot be laundered into human intention or accepted Schedule merely because they are operationally convenient.

Downstream classification:

```text
Schedule ↔ Proposal / Request       RESOLVED
Proposal / Request = Schedule       REJECTED
Request to reschedule = effect      REJECTED
```

Resource Requirement/Allocation/Reservation, Trigger/conditional policy and exact effective dating/persistence remain independently SAFE DEFERRED.

No Schedule hardening failed. **Schedule remains current accepted baseline, REOPEN = 0.**

Normative downstream references:

- `proposal.md`;
- `request.md`;
- `../checkpoints/proposal-request-v0-validation.md`.
