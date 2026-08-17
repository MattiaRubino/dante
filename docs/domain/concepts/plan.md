# Plan v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-10  
**Meaning of accepted:** best current decision; reopenable with better evidence  
**Workstream:** Core Domain Model v0

## Canonical definition

> **A Plan is a persistent, revisable structure that represents how LifeOS intends to coordinate work, behaviors, milestones, rules, or other execution elements in pursuit of a purpose. A Plan describes how something is intended to be pursued or organized; it is not the desired outcome itself, a single executable action, or the actual history of what happened.**

A Plan can support one or more Goals, but it may also exist without an explicit Goal when the user simply wants to organize a bounded body of execution.

Examples:

- preparation plan for an exam;
- language-learning plan;
- training plan;
- plan to rebuild a website;
- moving-house plan;
- travel preparation plan;
- release plan for an album;
- rehabilitation plan;
- structured plan for a temporary high-workload period.

## Why this concept exists

The previous LifeOS vocabulary treated `Program` and `Project` as separate canonical concepts. After the Goal review, that separation is no longer assumed to be fundamental.

Many real-world structures commonly called projects or programs share a large common execution model:

- phases;
- work items;
- milestones;
- dependencies;
- repeated sessions;
- routines;
- constraints;
- scheduling policies;
- review points;
- adaptation rules;
- resources or requirements.

The differences between a project-like structure and a program-like structure may be meaningful to presentation and specialized behavior, but those differences do not yet prove that the kernel needs two independent aggregate roots.

`Plan` is therefore introduced as the smallest currently justified execution-strategy primitive. `Project` and `Program` remain candidates for later specialization or domain views if further review demonstrates materially distinct identity, lifecycle, or invariants.

## Core semantic separation

Conceptually:

```text
Goal      -> what is wanted
Plan      -> how it is intended to be pursued or organized
Activity  -> what concrete action is intended
Schedule  -> when concrete execution is planned
Actual    -> what actually happened
Evidence  -> what supports evaluation
```

A Plan does not replace the Goal, Activity, Routine, Schedule, or Actual models.

## Plan versus Goal

A Goal defines a desired result, condition, change, or behavioral pattern.

A Plan defines an intended execution strategy or organizational structure.

Example:

```text
Goal
Reach spoken English B2

Plan A
Intensive six-month language plan
```

If the strategy changes substantially, the Goal may remain stable while the Plan is replaced.

Therefore:

> **Plan != Goal.**

## Plan versus Activity

An Activity is an executable unit of intended work or action.

A Plan can coordinate Activities, but is not itself equivalent to one Activity.

Example:

```text
Plan
Rebuild personal website

Activities
- define requirements
- design homepage
- migrate portfolio
- test responsive behavior
- deploy
```

Therefore:

> **Plan != Activity.**

## Plan versus Schedule

A Plan may have an effective period, target window, phase dates, deadlines, or scheduling policies.

That temporal information does not mean the Plan itself directly occupies operational calendar time.

Example:

```text
Plan
Exam preparation
Effective window: 1 September -> 15 November

Scheduled execution
12 September 18:00-20:00 — Study chapter 3
14 September 19:00-20:00 — Exercises
16 September 10:00-12:00 — Mock exam
```

Therefore:

> **Plan horizon != schedule occupancy.**

## Plan versus Routine

A Routine is a reusable rule or pattern for recurring behavior.

A Plan may contain, reference, generate, or coordinate one or more Routines, but it is not necessarily repetitive.

Example:

```text
Plan
Half-marathon preparation

Routines
- easy run
- long run
- strength session
```

A Routine may also exist without any Plan.

Therefore:

> **Plan != Routine.**

## Plan may exist without an explicit Goal

A Plan is not required to reference a Goal.

This avoids creating artificial duplicate Goal objects when the user simply wants to organize execution.

Example:

```text
User intent
"Organize my move."

Plan
Move to new house
```

LifeOS should not be forced to create a redundant Goal such as `Complete the move` unless the user or product semantics actually benefit from tracking that result as a persistent Goal.

If a Goal is useful, the relationship can be explicit:

```text
Goal
Move into the new house by 1 October

supported by

Plan
Moving-house plan
```

Therefore the conceptual relationship is many-to-many:

```text
Plan -> 0..N Goals
Goal -> 0..N Plans
```

The exact persistence representation of this relationship is deferred to the relationship-model review.

## A Plan has independent identity

A Plan has persistent identity separate from the Goal or purpose it supports.

Example:

```text
Goal
Reach spoken English B2

Plan A
Six-month intensive course
```

After two months, the user decides that the approach is unsuitable.

```text
Plan A
closed/replaced

Plan B
Immersion + tutor + speaking practice
```

The Goal remains the same because the desired result did not change. The execution strategy did.

This history is meaningful to future analytics, adaptation, and AI reasoning.

## Revision versus replacement

Not every operational change creates a new Plan.

Examples that normally should not imply replacement by themselves:

- moving one session;
- changing one occurrence;
- correcting a typo;
- adjusting a minor scheduling preference;
- changing one optional task.

Examples that may justify a new Plan or a linked replacement:

- abandoning one execution strategy for a materially different one;
- replacing the structure, progression logic, or governing rules;
- switching to a different program methodology;
- closing a failed or unsuitable plan and starting a new approach.

The precise boundary between versioning an existing Plan and creating a replacement Plan remains deferred to the history/versioning review.

## Structural capabilities

The future Plan model must be able to coordinate some or all of the following where applicable:

- phases;
- activities or work items;
- milestones;
- dependencies;
- constraints;
- routines;
- recurring or generated execution patterns;
- progression rules;
- review points;
- scheduling policies;
- fallback or adaptation rules;
- resources;
- requirements;
- optional outputs/deliverables;
- source/provenance information.

These are capabilities that a Plan may use, not mandatory fields every Plan must contain.

## Avoiding an untyped mega-object

Introducing `Plan` does not mean collapsing all execution semantics into one generic JSON object.

The intended direction is:

- one stable Plan identity and core lifecycle;
- explicit typed components where behavior differs materially;
- reviewed extensions where specialized planning needs recur;
- no arbitrary `plan_type + metadata JSON` architecture that pushes all invariants into application code or AI interpretation.

The exact entity/value-object boundaries of phases, milestones, dependencies, progression rules, and other components will be reviewed separately.

## Project revalidation

The current conclusion is:

> **`Project` is not yet justified as an independent Domain Kernel primitive.**

Typical project characteristics such as finite scope, deliverables, milestones, tasks, dependencies, and deadlines can currently be represented as characteristics of a Plan.

Example:

```text
Goal
Rebuild the personal website by 30 September

Plan
Website rebuild plan
```

A second mandatory aggregate named `Project: Website rebuild` would currently duplicate identity without proven domain value.

This does not remove the word `Project` from the product. It may remain useful as:

- a user-facing label;
- a specialized Plan profile;
- a view optimized for finite deliverable-oriented work;
- a later specialization if distinct invariants are demonstrated.

## Program revalidation

`Program` has a stronger case for specialization because program-like execution commonly includes:

- phases;
- repeated sessions;
- progression logic;
- cycles;
- generation rules;
- adaptation policies;
- assessment points.

However, those capabilities can currently be modeled as structured Plan components.

Therefore:

> **`Program` is not yet accepted as a separate kernel primitive.**

A future review must determine whether program-like structures require identity, lifecycle, or invariants that cannot remain cleanly inside the Plan model.

Until that review is complete, `Program` should be treated as a semantic/product specialization candidate rather than an assumed aggregate root.

## Project-like, program-like, and hybrid Plans

A Plan may be predominantly deliverable-oriented, progression-oriented, or hybrid.

Examples:

```text
Project-like Plan
Website rebuild
- finite deliverables
- dependencies
- deadline
- milestones
```

```text
Program-like Plan
Language learning
- phases
- repeated sessions
- progression
- assessments
- adaptation
```

```text
Hybrid Plan
Exam preparation
- finite exam date
- study deliverables
- recurring sessions
- progression
- mock assessments
```

The existence of common hybrids is one of the reasons not to force a premature `PROJECT | PROGRAM` kernel enum.

## Temporal semantics

A Plan may contain temporal concepts including:

- effective/start date;
- expected end date;
- target window;
- phase boundaries;
- internal deadlines;
- milestone dates;
- review cadence;
- scheduling rules.

These describe the Plan's intended operating horizon and rules.

Concrete occupation of the user's time is represented by schedulable execution objects rather than by the Plan itself.

## Relationship to Goals

A Plan can:

- support no explicit Goal;
- support one Goal;
- support multiple Goals.

A Goal can likewise be supported by:

- no Plan;
- one Plan;
- multiple concurrent or sequential Plans.

This prevents forced one-parent hierarchies and supports real cases such as one health plan contributing simultaneously to fitness, weight, and race-performance Goals.

## Lifecycle direction

Plan v0 does not yet fix a complete lifecycle enum.

The model must eventually support at least the semantics required for:

- draft/incomplete planning;
- future-approved planning;
- active execution;
- pause/suspension;
- closure/completion;
- early termination;
- replacement;
- continuation;
- archive as visibility separate from execution outcome.

The existing Goal/Program lifecycle documentation remains input, but the final lifecycle must be revalidated against the new Plan abstraction rather than copied directly.

## User control and AI boundary

AI may propose or help revise a Plan, including:

- phases;
- activities;
- milestones;
- scheduling policies;
- alternative strategies;
- adaptation rules;
- replacements or continuations.

AI proposals do not directly rewrite canonical plan structure or past execution history.

Material plan changes must pass domain validation and LifeOS user-control rules. Past Actual history is not rewritten merely because the future Plan changes.

## Current invariants

1. `Plan != Goal`.
2. `Plan != Activity`.
3. `Plan != Schedule`.
4. `Plan != Routine`.
5. A Plan has persistent identity independent of the Goal or purpose it supports.
6. A Plan may exist without an explicit Goal.
7. A Plan may support multiple Goals.
8. A Goal may be supported by multiple Plans.
9. A Plan may have a temporal horizon without directly occupying calendar time.
10. A Plan may coordinate phases, activities, milestones, dependencies, routines, constraints, rules, and resources without requiring every capability.
11. Ordinary operational changes do not automatically create a replacement Plan.
12. Materially different execution strategies may be represented as linked replacement Plans.
13. `Project` is not currently accepted as a separate kernel primitive.
14. `Program` is not currently accepted as a separate kernel primitive.
15. Project-like and program-like semantics may be represented through typed Plan capabilities and product-level specializations.
16. The kernel must not collapse Plan into an arbitrary metadata/JSON container.
17. Plan changes do not silently rewrite past Actual history.
18. AI proposals do not bypass Plan invariants or user-control rules.

## Stress-test coverage

The Plan abstraction currently fits representative LifeOS scenarios without requiring distinct Project and Program aggregate roots:

| Scenario | Plan interpretation |
|---|---|
| English B2 | progression-oriented Plan with repeated sessions and assessments |
| Exam preparation | hybrid Plan with deadline, milestones, study work, recurrence, and mocks |
| Website rebuild | deliverable-oriented Plan with work items, dependencies, and deadline |
| Album release | hybrid Plan with deliverables, production stages, reviews, and release milestones |
| Half-marathon | progression-oriented Plan with cycles, routines, recovery, and race milestone |
| Rehabilitation | progression/adaptation Plan with sessions, constraints, and review points |
| Moving house | finite Plan with tasks, appointments, checklists, assets, and deadlines |
| Trip preparation | finite Plan with bookings, documents, reminders, and dependencies |
| Temporary intense-work period | time-bounded Plan with temporary policies and review points |
| Plan without Goal | organizational Plan whose purpose is sufficient without creating a redundant Goal |
| One Plan supporting several Goals | shared execution strategy linked to multiple desired outcomes |
| One Goal with replacement strategies | multiple sequential Plans preserving the same Goal identity |

No reviewed scenario currently requires `Project` or `Program` to be independent primitives.

## Alternatives considered

### Keep Goal, Project, and Program as separate mandatory primitives

Not preferred because boundaries become ambiguous in hybrid cases such as exam preparation, rehabilitation, album production, or structured creative work. It also encourages duplicate identities such as `Goal: rebuild website` plus `Project: rebuild website` without proven value.

### Treat every Plan type as a separate domain entity

Not preferred because it creates topic-specific or workflow-specific models and scales poorly across LifeOS domains.

### One generic Plan with arbitrary metadata

Not preferred because it destroys enforceable invariants and moves too much semantics into untyped application logic.

### Plan as a child that must belong to exactly one Goal

Not preferred because many real planning structures are useful without an explicit Goal, and one Plan may support multiple Goals.

## Deliberately deferred questions

Plan v0 does not yet decide:

- final lifecycle state machine;
- exact version-versus-replacement boundary;
- physical persistence model;
- API representation;
- entity/value-object boundaries for phases, milestones, dependencies, progression rules, and scheduling policies;
- whether `Program` eventually deserves a formal specialization;
- whether `Project` remains only a product label/view or eventually gains distinct domain behavior;
- exact relationship representation between Plan and Goal;
- exact ownership/workspace rules;
- how imported external plans map into Plan versions and source/provenance;
- how reusable Templates differ from live Plans.

## Decision note

Plan v0 is the current baseline for the active Domain Model workstream.

It intentionally replaces the earlier assumption that `Program` and `Project` must each be independent canonical primitives. That older vocabulary remains preserved as historical/product-definition input until the surrounding concepts have been revalidated and the new model is ready to propagate across the repository.