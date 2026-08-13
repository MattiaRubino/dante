# LifeOS — Product Identity and North Star

**Status:** Proposed canonical product definition — pending final review/acceptance  
**Date:** 2026-08-13  
**Scope:** durable product identity, mission, capability boundaries and product-level guardrails

## 0. Purpose and authority

This document defines what LifeOS is, what problem it exists to solve, which capabilities belong to its product identity, how those capabilities relate to external/specialist systems, and what LifeOS must not become.

It is intentionally product-level. It does **not** define physical schemas, APIs, final frontend navigation/layout, provider selection, pricing, security enforcement mechanics or specialist-domain implementations.

Terminology rule:

- current accepted Domain Atlas definitions govern kernel/domain semantics;
- this document governs product identity and product-level intent once accepted;
- older accepted product documents remain authoritative for detailed behaviour where not superseded;
- examples here are stress cases, not automatic V1 implementation commitments.

---

# 1. Canonical definition

> **LifeOS is a personal operating system designed to help people turn intentions, needs and possibilities into outcomes they can realistically pursue. It maintains a structured, updateable representation of the user's situation, history, resources, constraints, commitments and relevant context; connects the different parts of life; identifies relevant opportunities and problems; helps compare alternatives; orchestrates competing demands and capacity; builds and coordinates realistic paths; helps execute them; observes what actually happens; and adapts what comes next. LifeOS does not seek to maximize productivity or take control away from the person. Its purpose is to reduce the distance between what a person wants or needs to do and what they can realistically make happen, while preserving clarity, history, privacy and user authority.**

Internal product compass:

> **Understand life. Shape what comes next.**

This short form is not approved public marketing copy.

---

# 2. Product mission

Real life is not naturally divided into calendar, tasks, goals, notes, work, health, finance, hobbies and relationships. Those are software boundaries.

A person may simultaneously have obligations, aspirations, work, projects, routines, people to coordinate with, things to maintain, learning goals, creative work, travel, finances, temporary disruptions and many unfinished ideas — all competing for limited time, attention, capacity, money and resources.

A calendar primarily answers **when**.  
A task manager primarily answers **what to do**.  
A goal tracker primarily answers **what outcome is desired**.  
A database primarily answers **what has been recorded**.

LifeOS must help with the **system formed by all of them together**.

> **Mission: help the user understand, coordinate and progressively shape their real life as one interconnected system rather than as isolated calendars, lists, goals and applications.**

---

# 3. The task is not the fundamental unit

LifeOS must not force every meaningful thing to become a task, event or calendar block.

Persistent real-world things may matter even when nothing is scheduled today: a person, vehicle, home, field, document, trip, song, course, project, goal, program, equipment, plant, animal, idea, constraint, measurement, external plan or historical body of activity.

> **Time is a first-class dimension of LifeOS, but the calendar is not the ontological center of the product.**

A simple appointment must remain simple and independent. Conversely, a persistent thing may exist meaningfully without current calendar placement.

---

# 4. The LifeOS North Star Loop

```text
UNDERSTAND
    ↓
DISCOVER
    ↓
ORCHESTRATE
    ↓
DECIDE
    ↓
PLAN & COORDINATE
    ↓
ACT
    ↓
OBSERVE
    ↓
LEARN
    ↓
ADAPT
    ↺
```

Not every interaction traverses every stage.

> **LifeOS must be simple when the problem is simple and become more structured only when consequence, uncertainty or coordination justifies it.**

## UNDERSTAND

Maintain enough structured context to reason about the current situation: commitments, goals, plans, routines, availability, capacity, constraints, resources, relevant preferences, external instructions, previous decisions, actual history, outcomes, temporary conditions, people and provenance.

Understanding does not mean unrestricted collection. Use the minimum relevant context for the current purpose.

## DISCOVER

**Newly elevated product capability.** LifeOS may eventually surface relevant opportunities or emerging problems not already represented as tasks.

Examples: realistic options for going out tonight; an upcoming astronomical event relevant to photography; an opportunity related to a followed interest; an old aspiration that has become feasible; a maintenance/supply/trajectory problem before failure.

Discovery must not become an engagement, advertising or unsolicited-notification feed.

```text
opportunity != mandatory action
suggestion != Decision
interest inference != permanent preference
```

## ORCHESTRATE

**Newly elevated explicit capability.** LifeOS must reason about the whole set rather than optimizing each goal or area independently.

Orchestration may identify competing demands, dependencies and useful synergies; protect hard constraints; move flexible work; sequence, reduce, postpone or pause work; broaden replanning when local movement fails; and explain when everything simply cannot fit.

> **LifeOS does not promise to make everything fit. A correct answer may be to do less, change scope, change timing or choose between outcomes.**

Its objective is coherence and attainability of the user's chosen direction, not maximum activity volume.

## DECIDE

Help compare alternatives using expected benefit, cost, time, capacity impact, dependencies, affected goals, constraints, uncertainty, assumptions and risk.

LifeOS may recommend; recommendation and Decision remain separate.

```text
proposal != Decision
Decision != effective change
Decision != Actual outcome
```

## PLAN & COORDINATE

Turn vague intent into executable structure progressively:

```text
aspiration / need / possibility
→ clarified outcome
→ feasibility / scenarios
→ chosen direction
→ plan/program where useful
→ milestones / requirements / dependencies
→ activities / sessions / events
→ scheduling / coordination
→ execution
```

A meeting, for example, is not only a calendar block: it may require participant coordination, preparation, the meeting itself, decisions and follow-up.

## ACT

Where safe, authorized and supported, help make the chosen thing happen: create/update LifeOS state, schedule/replan, create reminders, coordinate meetings, start sessions, import material, prepare connected actions, request review/confirmation and coordinate follow-up.

> **Capability to propose does not imply Authority to act. Authority in one scope does not imply Authority in another.**

## OBSERVE

Preserve what actually happened rather than inferring it from the clock.

Planned schedule, actual execution/participation, observed quantities, completion/disposition, outcome, confirmation, evidence, provenance and uncertainty are not one universal status.

> **The passage of time does not prove completion, and current state must not silently rewrite material history.**

## LEARN & ADAPT

Use structured history to improve future estimates, plans and questions without fabricating truth.

```text
observed pattern != declared preference
correlation != causal truth
AI inference != confirmed fact
new current state != rewritten history
```

Learning may produce an insight, question, proposed preference, changed estimate or replan. Weak evidence may correctly produce no change.

---

# 5. From "someday" to something realistically pursuable

LifeOS should accept intentions before the user knows how to express them as goals, milestones or projects.

Examples:

- `I want to learn English.`
- `I would like to publish an album.`
- `I want to improve this field's yield.`
- `I want to change career.`
- `I would like a richer social life.`

LifeOS can help clarify desired outcome, importance, feasibility, current resources, missing requirements, capacity, alternative routes, constraints and a useful first action.

> **LifeOS does not promise to make dreams come true. It aims to reduce the distance between vague intention and concrete, realistically pursuable action within the user's actual constraints and capabilities.**

Ideas and aspirations do not need to become active Goals immediately.

---

# 6. Effort, execution, outcome and progress are different

Credible progress tracking requires:

```text
effort / input
!= execution state
!= outcome
!= Goal progress
```

`Studied English for 2 hours` may prove effort and execution but does not automatically prove progress toward `spoken English B2`.

If the Goal is `100 hours of practice`, hours are directly part of the target. If the Goal is competency, hours are only one contributor/evidence source.

Progress may therefore depend on appropriate combinations of user declaration, quantity, milestones, assessments, actual activity, outcomes, external results or domain-specific evaluation.

> **Never manufacture reassuring percentage progress merely because activity occurred.**

---

# 7. Import and external programs are first-class inputs

LifeOS should be able to use plans and structured information created elsewhere without pretending to be their author or specialist authority.

Examples include a study course, exercise material, professional diet, rehabilitation program, work-shift sheet, travel itinerary, maintenance schedule, production plan, checklist or document containing instructions/deadlines.

LifeOS may:

1. preserve the original source;
2. extract proposed structure;
3. let the user confirm/correct interpretation;
4. create or link justified LifeOS plans, activities, sessions, schedules, materials or constraints;
5. distribute executable elements in time;
6. preserve external instruction versus LifeOS suggestion;
7. track execution/outcomes without claiming the original author approved later changes.

> **LifeOS may transform external information into structured operational context while preserving source, authorship and semantic boundaries.**

---

# 8. Specialist capability and AI boundary

LifeOS does not need to contain every specialist skill required by the user's life.

It can organize an English-learning path without being the language teacher; organize a professional diet without being the dietitian; schedule rehabilitation without being the physiotherapist; organize agricultural work without becoming a complete agronomy ERP; coordinate financial or legal obligations without becoming an adviser or law firm.

> **LifeOS orchestrates specialist capability; it does not need to own all specialist capability.**

Specialist execution may come from a professional, dedicated application, external service, external AI, connected provider or a future native LifeOS capability when scope, economics, quality and safety justify it.

LifeOS may use AI heavily, but:

> **LifeOS is not an AI chatbot.**

Durable value resides in structured context, history, constraints, relationships, state, decisions, actions and integrations that survive provider/model changes.

The initial product may use external/manual AI workflows where advanced native AI is not yet economically or operationally justified.

Example:

```text
LifeOS stores:
Goal + Program + materials + schedule + history

external AI performs:
tutoring / specialist interaction

LifeOS may receive:
session evidence + completed material + provider assessment
```

A provider assessment remains attributable evidence; it does not silently become confirmed objective truth.

> **Native AI depth is a product/economic decision, not a requirement of LifeOS identity.**

---

# 9. LifeOS as an orchestration layer across tools

LifeOS may coexist with calendars, learning platforms, fitness apps, document systems, professional software and AI providers.

Its value can be knowing why the user uses them, which goal/plan/context they serve, when they are needed, what relevant result came back and how that affects the rest of life.

> **Prefer coherent orchestration and reusable context over rebuilding every specialist product category.**

This does not require integration with every platform or standard.

---

# 10. Personal-first, not personal-only

LifeOS starts from the individual's own operating system, but real life already involves other people — including people without LifeOS accounts.

Future scenarios may include meetings, families, caregivers, small groups, work teams, shifts, responsibility/assignment flows, shared resources and external participants.

The domain direction preserves independent Person/Actor/Participation/Responsibility/Authority/Visibility/Representation semantics rather than collapsing them into one `user/member/owner` model.

> **Future LifeOS should coordinate shared reality among independent personal systems rather than merge everyone's personal LifeOS into one shared account/workspace by default.**

Collaboration must not become bureaucracy, surveillance or compulsory platform adoption.

---

# 11. LifeOS can manage systems and things, not only tasks

The same grammar should work when the managed reality centers on a persistent referent.

### Agriculture

```text
field
→ history / observations / quantities
→ resources / constraints
→ desired yield
→ alternatives
→ plan
→ scheduled work
→ actual inputs / observations
→ harvest outcome
→ comparison / adaptation
```

### Vehicle

```text
vehicle
→ mileage / fuel / documents / maintenance / costs
→ time- or usage-based triggers
→ upcoming needs
→ activities / decisions
```

### Creative work

```text
song/work
→ idea / versions / materials / production stages
→ sessions
→ milestones / release process
→ external metrics / outcomes
```

> **A persistent real-world referent must not be forced to become a calendar item merely because work around it occurs in time.**

---

# 12. Productivity is not the objective function

A valid recommendation may be:

- do less;
- pause a plan;
- protect recovery/free time;
- postpone an idea;
- reduce a target;
- choose between competing goals;
- gather more information before acting;
- stop pursuing something that no longer provides enough value.

> **LifeOS serves the user's chosen direction and sustainable reality, not an abstract productivity score.**

No universal Life Score, punitive streak model or moralized optimization target is part of product identity.

---

# 13. Capability classification

Every major future capability should be classified before becoming core product work.

## CORE IDENTITY

Capabilities without which the product stops being recognizably LifeOS:

- structured personal context/history;
- cross-domain connection of intentions, commitments and reality;
- whole-life orchestration under real constraints/capacity;
- planning and adaptation;
- planned-versus-actual integrity;
- user-controlled decisions/autonomy;
- explainability/provenance where material;
- progressive complexity;
- integration of outside reality without losing source/context.

## NATIVE CAPABILITY

Broadly reusable capabilities LifeOS can reasonably provide directly, subject to release slicing: capture/inbox, Today/time planning, goals/plans/programs/routines, review/decision surfaces, observations/quantities/history, search/commands, scheduling/replanning, basic import/export and cross-domain context/progress views.

## CONNECTED CAPABILITY

Specialist execution that may remain external while LifeOS coordinates it: advanced tutoring, professional diet design, specialist medical/rehabilitation work, advanced financial/legal analysis, booking/provider operations, specialist agricultural/industrial systems and high-cost advanced AI.

## DOMAIN EXTENSION

A specialized experience that reuses the kernel without redefining LifeOS: learning, wellness/training, travel, photography, creative work, agriculture, finance organization, vehicle/home management and similar domains.

## OUT OF BOUNDS

Capabilities that distort product identity, create unjustified safety/complexity risk, or duplicate specialist systems without a strong LifeOS orchestration reason.

---

# 14. What LifeOS is NOT

LifeOS is not primarily:

- an advanced calendar;
- a universal task manager;
- a goal percentage tracker;
- a habit/streak product;
- a Notion-like database workspace;
- a chatbot with calendar access;
- a personal analytics dashboard or universal Life Score;
- a system for filling every available minute;
- an autonomous manager that controls the person;
- a general social/engagement/advertising feed;
- an employee/family surveillance platform;
- a universal ERP/CRM/project-management replacement;
- a doctor, therapist, dietitian, physiotherapist, lawyer, financial adviser or teacher;
- a universal specialist application for every life domain;
- a system that collects information merely because it can;
- a system that treats AI inference as confirmed truth;
- a system that silently rewrites history;
- a system that turns every idea into an active Goal/task;
- a system that exposes domain-model complexity in routine UI merely because the kernel can represent it.

LifeOS may contain capabilities found in some of these products, but those capabilities do not define its identity.

---

# 15. Non-negotiable product principles

**User authority.** The user controls material decisions and automation according to scope.  
**Historical integrity.** Material past state is not silently rewritten.  
**Reality over appearance.** Scheduled placement, elapsed time or AI confidence do not fabricate completion/progress/truth.  
**Sustainable capacity.** Free clock time is not realistic capacity.  
**Progressive disclosure.** Kernel precision must not force enterprise ceremony into simple personal use.  
**Explainability proportional to consequence.** Material recommendations/changes expose enough reason, assumptions and impact.  
**Privacy and purpose limitation.** Use minimum relevant context; private causes are not automatically disclosable.  
**Source preservation.** External/professional/AI material remains attributable.  
**Specialist humility.** Coordinate domains LifeOS does not professionally own.  
**Reversibility where practical.** Material automation/replanning supports preview, confirmation and/or undo according to risk/settings.  
**No imposed life ideology.** LifeOS does not define one universal balance, productivity level or good life.

---

# 16. Product qualification test

Before introducing a major feature, surface or module, ask:

1. What real-life problem is reduced?
2. Which part of the North Star Loop does it serve?
3. Does it connect to the user's broader reality or create another isolated app inside LifeOS?
4. Is it core, native, connected, a domain extension or out of bounds?
5. Does LifeOS need to perform the specialist work itself or only coordinate it?
6. Can a smaller reusable capability achieve the same value?
7. Does it preserve plan vs action vs Actual vs progress?
8. Does it respect total capacity and competing commitments?
9. Can a simple user ignore the extra complexity?
10. Does it preserve user authority, privacy, history and source?
11. Can LifeOS explain a material proposal/action?
12. Would the capability still make sense if Calendar were not the primary UI?
13. Would it still make sense if the current AI provider disappeared?
14. Are we building LifeOS, or recreating a specialist product category without a strong orchestration reason?

A major feature that repeatedly fails these questions should be redesigned, connected externally, deferred or rejected.

---

# 17. Consequences for future UX architecture

This document does not choose final navigation or layout, but establishes these guardrails:

1. **Calendar/Today are essential temporal/operational projections, not the whole product architecture.**
2. Persistent things/structures need inspection independent of calendar placement.
3. Home should represent operational life state rather than merely a decorated calendar dashboard.
4. Review/attention/decision needs are cross-cutting; timeline cards should not permanently expose every kernel state.
5. The product must support unresolved ideas/possibilities without forcing Goal/task/schedule creation.
6. Progress UI must distinguish activity volume from outcome progress.
7. External programs/tools must preserve visible source/authorship where material.
8. Complex semantics should be projected through simple context-sensitive UX.
9. Future multi-actor UX coordinates shared reality without becoming an enterprise workspace by default.
10. AI is a cross-product capability, not the sole navigation architecture.

These constraints are inputs to the upcoming structural frontend rebaseline, not a final frontend proposal.

---

# 18. Relationship to existing documentation

This document synthesizes the durable direction already present across the product vision, Phase 3 review, V1 Today/calendar/scheduling/goal/program/context/history/AI/work documents, functional discovery simulation, multi-actor discovery/readiness, and current Domain Atlas boundaries.

It makes the following product-level ideas more explicit than earlier documents:

- whole-life **Orchestration** as a first-class capability;
- controlled **Opportunity Discovery** as a future capability;
- LifeOS as an orchestration layer for external specialist tools/AI;
- the explicit North Star Loop;
- capability classification (`CORE / NATIVE / CONNECTED / DOMAIN EXTENSION / OUT OF BOUNDS`);
- the rule that Calendar is a projection, not the product architecture.

These additions remain **Proposed** until final acceptance.

Before changing this document to **Accepted**, confirm that it captures LifeOS without reducing it to Calendar/Goals/AI; does not promise universal expertise; preserves specialist/AI boundaries; keeps orchestration non-paternalistic; keeps Opportunity Discovery controlled; remains compatible with personal-first/multi-actor direction; does not contradict the current Domain Atlas; and does not prematurely fix final UX or implementation.
