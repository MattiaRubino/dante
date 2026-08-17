# Multi-Actor Readiness v0

**Status:** Current cross-cutting domain guardrail  
**Established:** 2026-08-11  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

LifeOS is personal-first in product experience, but its domain kernel must not assume that every meaningful object belongs to, concerns, is performed by, is governed by, or is visible to exactly one registered user.

This document establishes the minimum multi-actor semantics that all current and future Domain Atlas concepts must preserve before the full Collaboration Discovery Simulation is complete.

It is intentionally **not** a complete collaboration, permissions, organization, or messaging design.

The objective is narrower and foundational:

> **Avoid structural single-user assumptions now so future collaboration can be introduced without rewriting the domain kernel.**

The product may remain single-user-first in V1. The domain model must remain multi-actor-ready.

---

## 1. Governing principle

The domain must not collapse these dimensions into one `user_id` concept:

```text
identity
ownership / stewardship
participation
responsibility
assignment
performer
subject / beneficiary
authority
visibility
provenance
account / authentication principal
```

These dimensions may coincide in simple personal cases, but they are semantically independent.

Canonical guardrail:

> **Domain object identity must not be defined by the identity of one user merely because the initial product experience is personal-first.**

A future physical schema may temporarily optimize the personal-first case, but no persistence shortcut may redefine this semantic rule.

---

## 2. Shared canonical state and actor-scoped state

When several actors refer to the same real-world object, LifeOS should normally preserve one canonical object rather than create one semantic duplicate per actor.

Example:

```text
Event
Dinner Saturday 21:00
```

Shared state may include:

```text
identity
current accepted Schedule
place
shared description
shared lifecycle/disposition
```

Actor-scoped state may include:

```text
participation response
role
responsibility
personal reminder
personal note
personal capacity effect
private constraints
visibility choices
```

Preferred direction:

```text
Shared domain object
        │
        ├── shared canonical state
        ├── Actor A relation/state
        ├── Actor B relation/state
        └── Actor C relation/state
```

Avoid by default:

```text
Actor A copy of Event
Actor B copy of Event
Actor C copy of Event
```

unless the records genuinely represent different intentions, legal records, provider records, or independently governed objects.

---

## 3. Account is not actor identity

A person or other relevant actor may participate in LifeOS domain reality without owning a LifeOS account.

Examples:

- a friend invited to dinner;
- a colleague in a meeting;
- a patient represented in caregiving or medical context;
- an external contractor;
- a teacher, doctor, mechanic, lawyer, technician, or client;
- a household member who has not joined LifeOS.

Therefore:

> **Actor / Person identity must be representable independently from LifeOS Account / Principal identity.**

The exact future boundaries among `Actor`, `Person`, `Principal`, `Account`, `Organization`, `Team`, and external identities are deliberately deferred to Subject/Relationship/Authority work.

This document fixes only the non-collapse rule.

---

## 4. Ownership is not participation

Creating, owning, stewarding, governing, participating in, or being affected by a domain object are different relations.

Example:

```text
Event
Team meeting

Organizer
Team Lead

Required participants
A, B

Optional participant
C
```

The Event identity does not belong separately to A, B, or C.

Likewise one participant declining the Event does not delete or alter the shared Event for everyone else.

Canonical guardrail:

> **Ownership/stewardship, participation, response state, attendance, and object identity remain separable.**

---

## 5. Responsibility is not Activity identity

An Activity represents intended actionable work. The identity of that work must survive ordinary assignment changes.

Example:

```text
Activity
Prepare presentation

requested by
Manager

responsible
Luca

performed by
Luca + Sara

created/imported by
Mattia / external system
```

Changing responsibility from Luca to Sara does not automatically create a new Activity.

Canonical guardrails:

> **Activity identity != assignee.**

> **Activity identity != requester.**

> **Activity identity != eventual performer.**

The precise relationship vocabulary and authority rules are deferred.

---

## 6. Goal and Plan governance

A Goal or Plan may be personal, shared, team-oriented, organizational, caregiving-oriented, or otherwise governed by more than one actor/context.

Examples:

```text
Personal Goal
Reach spoken English B2
```

```text
Shared Goal
Organize a trip to Japan
```

```text
Team Goal
Release product
```

The desired condition remains Goal semantics regardless of governance cardinality.

A participant or contributor does not automatically become a Goal owner/governor.

Canonical guardrails:

> **Goal identity != one mandatory personal owner.**

> **Goal ownership/governance != Goal subject != contributor/stakeholder relations.**

Likewise:

> **Plan identity != coordinator != contributor != responsible actor.**

Exact shared-governance, approval, workspace, and permissions models remain deferred.

---

## 7. Routine, Recurrence, and Occurrence assignments

A recurring policy may remain one Routine even when responsibility rotates across expected instances.

Example:

```text
Routine
Take trash out every Thursday

Occurrence 1 -> Mattia
Occurrence 2 -> Luca
Occurrence 3 -> Sara
```

LifeOS should not require three duplicate Routines merely because the performer changes.

Canonical guardrails:

> **Routine identity != performer.**

> **Occurrence identity != assigned actor.**

> **Recurrence describes repetition/generation, not responsibility rotation by default.**

A responsibility/rotation policy may later use Recurrence or other rule machinery where semantically appropriate, but Recurrence itself must not become a generic assignment engine.

---

## 8. Schedule acceptance is not participant acceptance

A shared Event may have one current canonical Schedule while individual participants have different responses.

Example:

```text
Event
Meeting

Schedule
15:00-16:00

Mattia
accepted

Luca
declined

Sara
tentative
```

Canonical rule:

> **The accepted Schedule is the currently canonical temporal assignment according to the governing authority/context of the schedulable subject. It does not mean that every participant has accepted participation.**

Participant response, participation intention, and actual attendance remain actor-scoped semantics.

Schedule authority and participant authority are related but not identical concerns.

---

## 9. Session and collaborative execution

A Session represents one logically continuous episode of actual execution.

The number of performers must not define Session identity.

Example:

```text
Activity
Move sofa upstairs

Session
17:00-17:30

performers
Mattia
Luca
```

This can be one collaborative execution episode.

However actor-specific participation may differ:

```text
Session envelope
17:00-17:30

Mattia actual participation
17:00-17:30

Luca actual participation
17:05-17:25
```

LifeOS must not infer that every performer participated for the entire Session envelope.

Conversely, two actors may perform independent execution attempts against the same Activity at the same time; in that case separate Sessions may be more correct.

Current semantic rule:

> **Session identity is governed by logical execution continuity, not by actor count and not merely by timestamp overlap.**

The exact future shape of actor-specific participation, collaborative execution, Session-to-Actual aggregation, and performance attribution is deferred to Actual/Relationship work.

---

## 10. Event participation and shift-swap semantics

A change in actor participation must not automatically be represented as a temporal change to the Event.

Example:

```text
Shift A
Monday 08:00-16:00
assigned Mattia

Shift B
Tuesday 08:00-16:00
assigned Luca
```

After a swap:

```text
Shift A -> Luca
Shift B -> Mattia
```

If LifeOS is representing institutional shift occurrences, neither Event needs to move. Participation/assignment changed.

This reinforces:

> **Event identity != participant.**

> **Event Schedule != actor assignment.**

Product-specific views may still present a personal schedule derived from the actor's current participation.

---

## 11. Availability and Capacity are actor/resource scoped

Availability and Capacity already operate on a schedulable resource rather than only on a user.

Multi-actor scheduling must preserve separate capacity claims for each relevant resource.

Example:

```text
Meeting
15:00-16:00

claims
Mattia primary attention
Luca primary attention
Meeting Room 3
```

One shared Schedule may therefore produce several resource-specific capacity claims.

A participant declining may remove or avoid that actor's claim without deleting the shared Event or Schedule.

Canonical guardrail:

> **Schedule identity != capacity owner.**

> **A shared scheduled subject may affect several resources independently.**

---

## 12. Privacy and safe derived projections

Multi-actor scheduling must not require disclosure of private source facts.

Example:

```text
Sara private Event
Medical appointment 18:00-20:00
```

Another actor asking for a common free time may be authorized to learn only:

```text
Sara unavailable 18:00-20:00
```

not:

```text
Sara has a medical appointment
```

Canonical rule:

> **A private fact may produce an authorized derived projection without making the private source fact visible.**

This applies beyond calendars to preferences, health, finance, location, notes, AI inference, and other sensitive data.

The exact visibility/access-control model is deferred, but the domain must not make source disclosure a prerequisite for useful derived reasoning.

---

## 13. Authority and disagreement

Different actors may have different authority over the same shared object.

Examples:

- an Event organizer may change Schedule while participants only respond;
- a team member may edit an assigned Activity but not a Team Goal;
- a surgeon, nurse, patient, and hospital administrator have different operational authority;
- a shared household Plan may permit broader editing than a medical record.

Canonical guardrail:

> **Authority is not inferred merely from participation, ownership label, or visibility.**

The future authority model must support disagreement and concurrent change without silently overwriting one actor's state.

The physical solution may involve versioning, optimistic concurrency, proposals, approvals, conflict states, or another reviewed mechanism.

---

## 14. AI acts with bounded authority

AI must not gain authority merely because it can see or reason about shared data.

Canonical rule:

> **AI effective authority must never exceed the authority of the actor/principal and policy under which it is acting.**

Examples:

- an AI acting for one participant cannot reschedule an externally governed Event unless that participant has sufficient authority;
- an AI may propose a new common time without silently applying it;
- an AI may use private availability to determine feasibility without disclosing the private cause;
- an AI may surface conflicts while preserving each actor's visibility boundary.

---

## 15. Multi-resource / specialist stress case

The model must remain coherent at scales beyond casual social planning.

Representative case:

```text
Event
Surgical operation

Subject
Patient

Actors
Lead surgeon
Assistant surgeon
Anaesthetist
Nurses
Patient

Resources
Operating room
Equipment

Activities
Pre-op preparation
Anaesthesia preparation
Procedure work
Post-op work

Constraints
patient preparation
staff availability
room availability
equipment availability
clinical timing rules

Schedule
accepted operation placement
```

The current Domain Atlas decomposition can represent this without making Event, Activity, Schedule, Capacity, or Temporal Constraint synonymous.

This is a stress-test example, not a claim that LifeOS V1 should replace specialist clinical software.

Specialist systems may remain authoritative integrations while LifeOS uses permitted context and projections.

---

## 16. Current baseline interpretation for the first two clusters

The accepted Intention & Execution and Time concepts remain valid under this hardening.

Single-user wording such as `the user` in an earlier concept document must be interpreted as the personal-first case, **not** as a new invariant that the concept may involve only one actor.

The following cross-cutting hardenings apply immediately:

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

These guardrails refine the current baselines without introducing a new universal Actor primitive yet.

---

## 17. Deliberately deferred

This readiness contract does **not** yet decide:

- final Actor/Person/Account/Principal model;
- organizations, teams, households, groups, workspaces, or membership;
- ownership cardinalities;
- shared Goal/Plan governance lifecycle;
- assignment and responsibility ontology;
- participant roles and role inheritance;
- ACL/RBAC/ABAC or other access-control model;
- per-field or per-relation visibility;
- invitation lifecycle;
- collaboration messaging/chat;
- comments, mentions, reactions, or notification delivery;
- approval workflows;
- collaborative editing conflict resolution;
- actor-specific Actual/Outcome attribution schema;
- group Session persistence;
- legal/clinical authority semantics;
- external federation;
- exact SQL/API implementation.

These decisions require the future Subject/Relationship/Authority work and the dedicated Collaboration Discovery Simulation.

---

## 18. Reopening rule

The future Collaboration Discovery Simulation may reopen any current hardening if stronger real-world evidence shows that the model is insufficient.

The current status is therefore:

```text
Personal-first product
Multi-actor-ready domain kernel
Full collaboration model pending
```

This is the minimum structural baseline that all subsequent domain work must respect.
