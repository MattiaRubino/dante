# Workstream Addendum — Multi-Actor Readiness

**Status:** ACTIVE CROSS-CUTTING BASELINE  
**Established:** 2026-08-11  
**Active branch:** `feature/domain-model`  
**Parent workstream:** `domain-model.md`

## Why this addendum exists

The Domain Model workstream remains personal-first in product scope, but future LifeOS versions are expected to support collaboration and multi-actor scenarios ranging from casual shared plans to professional and specialist workflows.

The project must therefore avoid building the current domain kernel around structural assumptions that every object belongs to, is performed by, concerns, and is visible to one registered user.

This addendum records the current operational consequence:

> **From this point forward, multi-actor readiness is a mandatory domain-model validation dimension.**

This does not mean implementing the full collaboration feature set now.

---

## Required reading for multi-actor-sensitive work

1. [`../domain/multi-actor-readiness-v0.md`](../domain/multi-actor-readiness-v0.md)
2. [`../domain/checkpoints/multi-actor-readiness-v0.md`](../domain/checkpoints/multi-actor-readiness-v0.md)
3. [`../domain/validation-methodology-v2.md`](../domain/validation-methodology-v2.md)
4. [`../domain/validation-methodology-v2-multi-actor-addendum.md`](../domain/validation-methodology-v2-multi-actor-addendum.md)
5. [`../domain/checkpoints/intention-execution-v0.md`](../domain/checkpoints/intention-execution-v0.md)
6. [`../domain/checkpoints/time-v0.md`](../domain/checkpoints/time-v0.md)
7. [`../domain/checkpoints/cross-cluster-validation-v2.md`](../domain/checkpoints/cross-cluster-validation-v2.md)

---

## Current cluster state

```text
Intention & Execution v0
PASS — validated current baseline
PASS — multi-actor readiness checkpoint

Time v0
PASS — validated current baseline
PASS — multi-actor readiness checkpoint
```

No structural reopening was required.

No new mandatory primitive was introduced.

The baseline was hardened through cross-cutting invariants rather than by prematurely designing Actor/Team/Organization/ACL tables.

---

## Current hardening summary

```text
Goal identity       != owner/governor/stakeholder/subject
Plan identity       != coordinator/contributor/responsible actor
Activity identity   != requester/assignee/performer
Event identity      != organizer/participant/participant response
Routine identity    != performer
Milestone identity  != stakeholder/governor
Occurrence identity != assigned actor
Schedule identity   != participant acceptance/capacity owner
Session identity    != performer count
Constraint identity != authority actor
Recurrence identity != assignment rotation
Capacity identity   != one mandatory user
```

Additional baseline rules:

- shared canonical object + actor-scoped state is preferred over per-user semantic duplication;
- Account/Principal is not assumed to be Actor/Person identity;
- non-LifeOS actors must remain representable;
- private source facts may produce authorized derived projections without source disclosure;
- authority, visibility, participation, ownership, responsibility, and provenance remain distinct dimensions;
- AI cannot gain authority beyond the actor/principal and approved policy under which it acts.

---

## How to work from now on

Every new concept review must retain all existing Validation Methodology v2 tests and additionally perform the Multi-Actor / Collaboration Compatibility Test.

At minimum ask:

```text
Can this exist for one or many actors?
Does actor reassignment alter identity?
Can owner differ from participant?
Can performer differ from subject?
Can shared state coexist with actor-private state?
Can non-LifeOS actors participate?
Whose capacity is affected?
Who has authority to change what?
Can private facts support safe shared reasoning?
```

Do not introduce collaboration-specific primitives merely to pass the test. Introduce them only if distinct identity, lifecycle, invariants, authority, or query behavior is demonstrated.

---

## Relationship to upcoming clusters

Multi-actor readiness is expected to materially influence later reviews of:

```text
Actual
Outcome
Observation
Evidence
Provenance

Subject
Person / Actor
Resource
Asset

Relationship
Responsibility / Assignment
Authority
Visibility
Decision
Version
AI Proposal
```

The exact cluster membership and naming remain open.

The first two clusters must not be re-opened merely because those later models become more explicit unless a genuine contradiction is discovered.

---

## Full Collaboration Discovery Simulation — pending

A broader dedicated collaboration/multi-user simulation is intentionally pending.

Expected scenario families include:

- friends / outings / shared travel;
- household and shared resources;
- work meetings and assignments;
- team Goals and Plans;
- shift work and swaps;
- caregiving;
- specialist professional relationships;
- medical/clinical multi-role operations;
- organizational workflows;
- external/non-LifeOS actors and providers;
- privacy, disagreement, concurrent changes, authority, and visibility.

When that simulation is available, it becomes new validation evidence and must be used to stress the entire Domain Atlas.

It may confirm, harden, or reopen current decisions.

---

## Current next step

Do **not** automatically start the Observed Reality & Evidence cluster merely because this addendum is complete.

The immediate conversation/workstream state remains:

```text
first two clusters validated
multi-actor readiness baseline established
full collaboration simulation pending
user-led brainstorming/questions/additional tests may continue
next domain cluster not yet selected
```

This preserves the previously agreed sequencing rule.
