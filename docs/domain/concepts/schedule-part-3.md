<!-- LIFEOS-CANONICAL-CONTINUATION document="schedule.md" follows="schedule-part-2.md" -->
> **Canonical continuation of `schedule.md`.** `schedule.md` + `schedule-part-2.md` + this part remain one logical Schedule document. This continuation records only the downstream Dependency v0 amendment.

# 2026-08-15 — Dependency v0 downstream amendment

Dependency v0 does not alter Schedule identity. It closes the planning boundary between prerequisite contingency and accepted temporal placement.

Canonical separation:

```text
Dependency
= what prerequisite state/result a dependent state/transition is contingent on

Schedule
= when a schedulable subject is currently accepted/intended to occur
```

Consequences:

- a Dependency can exist while the dependent target has no Schedule;
- a Dependency can be satisfied while the dependent target remains unscheduled;
- satisfying a Dependency does not create or accept a Schedule;
- an unsatisfied Dependency does not silently delete an existing Schedule;
- if a newly established/corrected Dependency conflicts with a current Schedule, LifeOS may diagnose/replan/reconcile, but preserves the Schedule assertion/history until legitimately changed;
- dependency violation in Actual does not cause Schedule to be rewritten to match reality;
- moving a Schedule earlier/later does not by itself create/change a Dependency;
- `after prerequisite` used as a temporal placement rule remains Temporal Constraint semantics unless true state contingency also exists;
- lead/lag/spacing remain Time semantics, not Schedule-owned Dependency metadata;
- no universal `blocked` Schedule state is introduced.

Example:

```text
Dependency
Publish release depends on master.approved

Schedule
Publish release: 20 August 09:00

Current master state
approval pending
```

This can be an inconsistent or infeasible plan state. The model must preserve all three facts rather than silently deleting the Schedule or inventing approval.

Likewise:

```text
master.approved = true
```

makes the Dependency satisfied but does not imply:

```text
Publish release now
```

That would require Schedule and/or Trigger/Conditional Policy semantics.

Normative downstream references:

- `dependency.md`;
- `temporal-constraint-part-2.md`;
- `../checkpoints/dependency-v0-validation.md`.

Schedule remains a **Current accepted baseline**; no Schedule identity or history invariant is reopened.