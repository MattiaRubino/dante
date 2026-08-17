<!-- LIFEOS-CANONICAL-CONTINUATION document="time-v0.md" follows="time-v0-part-3.md" -->
> **Canonical continuation of the logical Time v0 checkpoint.** `time-v0.md` + `time-v0-part-2.md` + `time-v0-part-3.md` + this part remain one logical document. This continuation records only the downstream Dependency v0 closure.

# 2026-08-15 — Dependency v0 downstream closure

**Time verdict:** unchanged — PASS  
**REOPEN:** 0

Dependency v0 confirms that Time owns temporal geometry while Dependency owns prerequisite contingency.

Canonical separation:

```text
Dependency
= dependent state/transition is materially contingent on prerequisite state/result

Temporal Constraint
= allowed/required/preferred temporal relationship

Schedule
= current accepted temporal assignment

Actual
= what actually happened
```

Time-cluster consequences:

- `after`, `before`, lead, lag and spacing do not establish Dependency by themselves;
- a true Dependency may coexist with a Temporal Constraint that expresses its temporal consequences;
- satisfying Dependency does not create Schedule or Actual;
- an unsatisfied Dependency does not erase a previously accepted Schedule;
- a Schedule that conflicts with current Dependency state can remain historically true while becoming infeasible/inconsistent for planning;
- actual execution that violates Dependency remains recordable Actual;
- no `FS/SS/FF/SF`-style provider enum is adopted as kernel ontology;
- no universal `blocked` time state is introduced;
- no Time concept becomes a workflow node or graph edge merely because planning uses dependencies.

Example:

```text
Dependency
B.release depends on A.approved

Temporal Constraint
B.start >= A.approved_at + 24h

Schedule
B planned for Thursday 10:00

Actual
B occurred Wednesday 18:00
```

All four layers can coexist and remain independently reconstructible. LifeOS may derive violations or infeasibility but must not rewrite one layer into another.

Normative downstream references:

- `../concepts/dependency.md`;
- `../concepts/temporal-constraint-part-2.md`;
- `../concepts/schedule-part-3.md`;
- `dependency-v0-validation.md`.

The original **Time v0 verdict remains PASS**.