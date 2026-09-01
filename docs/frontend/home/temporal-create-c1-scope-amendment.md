# DANTE — Temporal Create C1 Scope Amendment

**Status:** ACTIVE AUTHORITY — USER-MANDATED SCOPE EXPANSION
**Date:** 2026-09-01
**Owner workstream:** `feature/home-timeline`
**Integration target:** `feature/home-react`
**Supersedes where conflicting:** `temporal-create-q0-contract.md`, `temporal-create-q0-approval.md`, and the C1 section of `temporal-frontend-roadmap.md`
**Scope stop:** maximum useful pre-backend Create system; no real API, PostgreSQL persistence, provider synchronization, authoritative solver runtime, AI runtime, voice runtime, or server-side ACL/auth implementation

## 1. Why this amendment exists

The original Q0/C1 contract intentionally bounded the first Create vertical to a compact Activity/Event grammar and deferred recurrence, flexible scheduling and several richer authoring concerns to later temporal phases.

After implementation of that compact scope, the user explicitly clarified that the `+` workstream must not stop at a basic Quick Add. The target is the **complete DANTE Create system to the maximum useful frontend/application depth before backend integration**.

Therefore the earlier bounded C1 scope is no longer sufficient as the implementation stop line.

This amendment does not discard Q0. It preserves Q0's semantic, architecture, accessibility, performance, draft, validation, command, reconciliation and backend-boundary rules while expanding what Create must author before it can be considered complete.

## 2. Permanent semantic invariants retained

The expanded Create system must continue to preserve:

```text
Activity != Event
identity != placement
Schedule != Occurrence != Session != Actual
planned != actual
all-day != midnight hack
floating local != zoned != absolute
unscheduled != invalid
proposal != accepted effect
calendar/context != sharing/ACL
manual input != AI interpretation
frontend projection id != canonical backend identity
```

No richer UI may collapse these distinctions for convenience.

## 3. Product topology — three progressive surfaces, one capability

Create is one application capability with progressive presentation depth:

```text
ENTRY
  │
  ├── Timeline/header +
  ├── contextual Timeline position/range
  ├── future global Create
  ├── future keyboard command
  ├── future deterministic/NL interpretation
  ├── future voice
  └── future governed AI
          │
          ▼
      CREATE DRAFT
          │
          ├── QUICK CREATE
          │     fast title/type/time/context path
          │
          ├── EXPANDED CREATE
          │     richer scheduling/organization fields
          │
          └── FULL CREATE EDITOR
                deep entity-specific authoring surface
          │
          ▼
    validation / candidate preview
          │
          ▼
      user commit
          │
          ▼
       F0/application command boundary
          │
          ▼
 local deterministic adapter now
 authoritative adapter later
```

Quick, Expanded and Full Create are not three independent implementations. They must share the same draft/application model and command path.

## 4. Quick Create — retained role

Quick Create remains intentionally fast and calm. It may expose only the most common fields:

- title;
- Activity/Event;
- primary temporal placement;
- context/calendar/life area;
- one clear expansion path;
- one truthful commit action.

The existing compact composer is therefore a valid **entry surface**, not the complete Create product.

## 5. Expanded / Full Activity authoring

When semantically applicable and supported by current DANTE contracts, Activity creation must be able to progressively author:

### Identity and organization

- title;
- context/calendar/life area;
- notes;
- tags/labels where a real owning model exists;
- links/handoffs to Project, Goal, Routine, Program or World where those concepts already exist as authoritative references;
- template reference when the template vertical/contract exists.

Create must not implement independent CRUD for external verticals. A missing Project/Goal/Routine editor is a handoff dependency, not permission to duplicate that vertical inside Timeline.

### Scheduling intent

Create must be able to represent, without collapsing semantics:

- fixed placement;
- all-day/date span where meaningful;
- unscheduled/open Activity;
- bounded scheduling window;
- deadline-constrained Activity;
- preferred window;
- earliest start;
- explicit deadline/due boundary;
- timezone/floating-local intent as applicable.

These authoring semantics may exist before an authoritative solver exists. In that case Create stores/validates the structured intent and shows truthful local behavior; it does not fake an optimized schedule.

### Duration and execution structure

As applicable:

- expected duration/effort;
- minimum session duration;
- splittable vs indivisible;
- maximum/target session count only where product semantics justify it;
- preparation/recovery/spacing constraints when already authoritative.

These fields describe planning intent. They do not fabricate Session or Actual records.

### Replanning / movement policy

As applicable:

- locked/fixed;
- movable;
- movable inside an accepted window;
- confirmation-required;
- freely replannable where authoritative policy permits.

Create authors the policy/intent. C5/C7 still own richer Timeline-wide replanning interaction and any future solver behavior.

### Priority / planning pressure

Where supported by Product semantics:

- priority/importance;
- deadline pressure;
- preferred timing;
- other solver-relevant constraints already present in authoritative models.

Do not invent a competitor-style priority system if DANTE has a different canonical concept.

### Recurrence

Create must provide an architecture and UI path for recurrence authoring where the created source legitimately owns recurrence.

The UI must preserve the distinction between:

```text
recurrence source
!= generated occurrence
```

Changing a recurrence source later remains a deeper C5/Detail responsibility. Create only establishes the initial recurrence specification and provenance-safe reference.

### Reminder / confirmation policy

Where already supported by DANTE contracts, Create may author reminder/confirmation policy. It must not fake notification delivery before the notification/backend vertical exists.

## 6. Expanded / Full Event authoring

Event creation has its own grammar and must not inherit Activity-only semantics blindly.

Progressively supported Event fields may include:

- title;
- start/end;
- duration;
- all-day/date span;
- floating/zoned time semantics;
- timezone;
- context/calendar;
- location;
- notes;
- recurrence/source semantics;
- availability/busy semantics where supported;
- visibility where supported independently from ACL;
- reminder policy;
- participant/resource/conferencing **integration seams**.

Participants, rooms/resources, external calendar invitations and conferencing links must remain truthful unavailable/integration states until their owning backend/provider capability exists. No fake invitation or meeting-link success is allowed.

## 7. Other DANTE object types

The Timeline `+` is not required to become a universal CRUD factory.

The Create system must nevertheless have a scalable handoff path such as `Altro tipo…` / global Create registry for types owned elsewhere, for example:

- Goal;
- Project;
- Program;
- Routine;
- Reminder where it becomes an independent type;
- Template;
- Asset;
- other future registry-backed entity types.

Handoff must preserve the user's draft/context where feasible and must not force every type into Activity/Event semantics.

## 8. UI / interaction quality target

The expanded scope must not become a giant administrative form.

Required interaction direction:

- title remains dominant;
- frequent properties are lightweight/editable;
- deeper properties are grouped by semantic responsibility;
- Activity and Event can expose different sections;
- Quick Create remains fast even after Full Create exists;
- Full Create may use a side sheet or dedicated editor surface instead of stretching one popup indefinitely;
- contextual Timeline creation pre-fills temporal context;
- candidate preview remains distinct from accepted state;
- keyboard, focus, touch, mobile and reduced-motion behavior remain first-class;
- no raw translation keys or debug-like status rows may leak into production UI;
- visual density must remain comparable to mature large applications rather than a settings form.

## 9. Application architecture expansion

The existing F0 foundation remains valid but may be extended only where the richer Create system demonstrates a concrete need.

Likely additions must remain application-level and backend-agnostic, such as:

- richer Create draft schema;
- scheduling-constraint value objects;
- recurrence specification;
- reminder/confirmation intent;
- external-reference/handoff contracts;
- capability-specific validation;
- candidate preview model;
- operation result/reconciliation handling.

Do not mirror DB rows or invent REST DTOs.

## 10. Relationship with C5 and C7

This amendment expands **creation-time authoring**, not every later temporal runtime responsibility.

C1 now owns:

- authoring the initial structured scheduling/recurrence/replanning intent;
- validating it;
- previewing it;
- applying it through the local application boundary;
- preserving it for future adapter swap.

C5 still owns:

- broader recurrence management;
- occurrence/source scope editing;
- scheduling-flexibility interaction across existing items;
- deeper constraint editing after creation.

C7 still owns:

- conflict/replanning experience;
- candidate plan comparison;
- affected-item consequences;
- accept/modify/reject of solver/replan proposals;
- future authoritative solver integration seam.

This prevents Create from becoming the entire temporal product while still making it complete as an authoring system.

## 11. Backend stop line

The frontend Create system is complete pre-backend when its UI/application semantics no longer need structural redesign merely to connect a server.

The later backend vertical owns:

- API transport;
- canonical server identities;
- auth/ACL enforcement;
- PostgreSQL transactions/persistence;
- durable idempotency;
- provider/calendar synchronization;
- multi-device reconciliation;
- notification delivery;
- external invitation/conferencing execution;
- authoritative solver runtime.

Connecting those must replace/extend adapters and integration ports rather than force a Create UI/application rewrite.

## 12. Acceptance / closure rule

C1 is **not closed** because Quick Create works or because CI is green.

C1 closes only when:

1. Quick Create is genuinely fast and polished;
2. Expanded Create covers the meaningful pre-backend Activity/Event authoring grammar;
3. Full Create/handoff exists for depth that should not live in the compact popup;
4. all currently authoritative scheduling forms needed at creation can be represented without semantic collapse;
5. recurrence and policy authoring seams are complete where applicable;
6. external/backend-only capabilities are truthful seams, never fake success;
7. draft/validation/preview/commit/recovery/Undo paths are coherent;
8. responsive, accessibility, keyboard, focus, i18n and performance gates pass;
9. automated CI is green on one final commit;
10. the user manually reviews the **complete Create system** and explicitly accepts it.

Until then, C1 remains OPEN / ACTIVE.
