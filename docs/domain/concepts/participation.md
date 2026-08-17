<!-- LIFEOS-CANONICAL-SPLIT document="participation.md" part="1" total="3" -->
> **Canonical document split — Part 1 of 3.** Parts 1–3 together form one authoritative document; this is a physical split only, not a summary/reference hierarchy. The payload preserves the full pre-compaction baseline first and later downstream amendments in sequence; later explicit amendments override stale status/deferral wording without deleting the earlier rationale. Navigation: **Part 1** · [Part 2](participation-part-2.md) · [Part 3](participation-part-3.md)

<!-- LIFEOS-CANONICAL-PAYLOAD -->
# Participation v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-12  
**Meaning of accepted:** best current decision; reopenable with stronger evidence  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Relationships / Reasoning

## Canonical definition

> **Participation is the contextual semantic relation family through which a native referent is represented as expected or intended to be involved, or as actually involved, in a bounded shared occurrence or interaction context. Intended/response participation and Actual participation are distinct semantic facets and may differ in state, time, role, provenance, authority and visibility. Participation does not create referent identity and does not by itself imply Responsibility, performance, organization, Authority, Visibility, Resource allocation, or Account identity.**

Participation answers bounded questions such as:

> **Who is expected/intended to be involved here?**

and, separately:

> **Who actually participated, and in what way/interval, where that matters?**

Participation is a **specific semantic relation family**, not a native entity/root and not a universal membership/social-graph primitive.

---

# 1. Why Participation exists

LifeOS already distinguishes one shared Event/Activity/Actual from actor-scoped state.

Representative chronology:

```text
Event
Dinner

Anna
invited
→ accepted
→ actually attended

Luca
invited
→ declined
→ did not attend

Marco
not invited
→ actually attended
```

All three histories are valid.

Without explicit Participation semantics, LifeOS is pushed toward weak alternatives:

1. one `participants` list that cannot distinguish invitation, response and reality;
2. one attendee `status` that overwrites earlier intention when reality differs;
3. one Session per attendee merely to record attendance;
4. actual participant inferred from invitation/acceptance;
5. decline inferred as proof of absence;
6. Resource booking confused with participation;
7. organizer/requester/responsible actor confused with participant;
8. provider attendance telemetry treated as unquestioned canonical human reality.

The actor-scoped semantic need is real; a universal Participant identity is not.

---

# 2. Participant is a contextual role, not identity

A Person does not become a second domain object merely by being involved in an Event.

```text
Person Anna
        ↓ Participation role
Event E17
```

Rejected shape:

```text
Participant P99
    ↓ wraps
Person Anna
```

Canonical rule:

> **Participation references the native referent whose involvement is at stake; it does not manufacture a Participant identity.**

A Person with no LifeOS Account may participate ordinarily.

The exact future eligible non-human referents, collective actors and typed-reference mechanism remain deferred.

---

# 3. Participation versus Event identity

Event identity is independent from participant relations and states.

```text
Event
Project meeting
```

may retain one identity while:

```text
Anna accepts
Luca declines
Marco joins unexpectedly
Sara is removed from expected participants
```

Therefore:

```text
Event identity != participant set
Event identity != participant response
Event identity != actual attendance
```

Adding/removing/changing ordinary participant state does not automatically create a new Event.

---

# 4. Intended/expected participation versus Actual participation

This is the core Participation invariant.

```text
planned / expected / response participation
!=
Actual participation
```

Example:

```text
T0 Anna invited
T1 Anna accepts
T2 Event occurs
T3 Anna does not attend
```

The correct history is not:

```text
accepted rewritten to declined
```

Instead:

```text
historical response = accepted
Actual participation = none / established absence if evidence supports it
```

Likewise:

```text
declined
→ later attends anyway
```

and:

```text
never invited
→ later participates
```

are valid.

Canonical rule:

> **Later Actual participation must not rewrite earlier invitation/response history, and earlier invitation/response must not establish Actual participation.**

---

# 5. Invitation

`Invitation` is not accepted as a standalone universal kernel primitive.

Invitation is a participation-related proposal/request that a referent become an expected/intended participant in a bounded context.

Conceptually:

```text
Event
        ↓ invitation/proposal
Person Anna
```

Invitation does not by itself establish:

```text
Anna intends to participate
Anna accepted
Anna will attend
Anna actually attended
```

Canonical rule:

> **Invitation != intended acceptance != Actual participation.**

A future product may persist invitation workflow state where consequence requires it, but no universal Invitation root/table/state machine is pre-approved.

---

# 6. Participation response

A Participation response captures actor-scoped response/intention toward expected participation.

Possible contextual states may include, depending on domain/product:

```text
needs action
tentative
accepted
declined
conditional
waitlisted
```

No universal enum is accepted here.

Response answers something like:

> **What is the participant's current expressed stance toward expected participation?**

It does not answer:

> **Did they actually participate?**

Therefore:

```text
accepted != attended
accepted != Actual participation

declined != proven absence
no response != declined
```

Response history may be material and must not be silently overwritten when changed.

---

# 7. Attendance

`Attendance` is accepted as Event-facing product/domain language for Actual Participation semantics, not as a standalone universal kernel primitive.

Example:

```text
Event
Workshop
10:00–12:00

Anna
Actual Participation
10:00–12:00

Luca
Actual Participation
10:35–11:10
```

Attendance may be:

- full;
- partial;
- absent where established;
- unknown;
- represented through one or multiple actual participation intervals where justified.

But the domain must not impose one universal attendance enum across every participation context.

Canonical rule:

> **Attendance is an Event-oriented expression of Actual Participation; it is not the same semantic as invitation response.**

---

# 8. Actual Participation versus Session

Session represents a bounded episode of performed behavior/execution.

Actual Participation represents actor-scoped involvement in a shared occurrence/interaction.

An ordinary Event does not require one Session per attendee.

Rejected default shape:

```text
Event meeting

Anna attendance → Session Anna
Luca attendance → Session Luca
Marco attendance → Session Marco
```

Correct conceptual separation:

```text
Event
   ↓
Actual Event realization
   ├── Anna Actual Participation
   ├── Luca Actual Participation
   └── Marco Actual Participation
```

A Session may still exist when a distinct performed/execution episode is semantically real.

Therefore:

```text
Participation != Session
Event attendance != Session by default
```

---

# 9. Participation versus Actual

Actual represents how a shared/intended expectation resolved overall.

Participation represents actor-scoped involvement facets.

Example:

```text
Event Actual
meeting occurred 10:08–11:23

Anna Actual Participation
10:08–11:23

Luca Actual Participation
10:08–10:45

Sara Actual Participation
established absent
```

Therefore:

> **Shared Actual != identical actor-specific Participation.**

Actual Participation may contribute to/reconcile the broader Actual without becoming the same record or meaning.

---

# 10. Participation versus performer

`performed_by` answers who executed work/behavior.

Participation answers who was involved in a shared occurrence/interaction.

Examples:

```text
concert audience member
= participant
!= performer
```

```text
meeting listener
= participant
!= performer by default
```

```text
Activity execution
Anna performed the work
```

Where performance is the real semantic question, `performed_by` is stronger than generic Participation.

Canonical rule:

> **Use the most specific truthful actor role; Participation must not replace performer/recorder/confirmer/responsible/etc. when that specific role is what matters.**

---

# 11. Participation versus Responsibility

Involvement and accountability are independent.

```text
Person Anna
participates in meeting
```

does not imply:

```text
Anna responsible for meeting outcome
```

Likewise:

```text
Manager responsible for event logistics
```

does not prove actual participation.

Therefore:

```text
Participation != Responsibility
Participant != responsible Actor
```

Responsibility transfer does not automatically alter Participation, and Participation does not grant responsibility.

---

# 12. Participation versus Resource

A Resource can be required/booked without participating.

Example:

```text
Conference Room 3
Resource for meeting
```

The room is not automatically a Participant merely because a calendar provider represents it as a resource attendee.

Likewise a Person can be Resource-eligible for an activity without being a participant in a specific Event.

Therefore:

```text
Participation != Resource
Resource allocation != Participation
```

Specialist domains may later justify non-human participation semantics, but provider vocabulary does not decide LifeOS ontology.

---

# 13. Participation versus organizer/requester

Organizing or requesting an occurrence does not automatically imply participation.

```text
organizer != participant
requester != participant
```

A Person may organize an Event and not attend it.

A Person may participate without organizing/requesting anything.

Do not derive Participation from organizer/creator fields.

---

# 14. Participation versus Authority and Visibility

Participation grants neither canonical-change Authority nor universal information exposure.

```text
Participant
!= Authority holder
!= viewer of every related fact
```

Likewise, visibility of:

```text
Person
+
Event
```

must not imply visibility of:

```text
their participation
response
attendance interval
reason for decline
private note
```

Canonical rule:

> **Endpoint visibility does not imply Participation-relation visibility, and Participation does not manufacture Authority.**

Authority v0 and Visibility v0 now close these boundaries independently. Participation may be a basis considered by policy, but it creates neither governance power nor automatic disclosure.

---

# 15. Response actor versus participant identity

The Person whose participation is at stake may differ from the Actor/Principal submitting a response.

Examples:

```text
assistant responds on behalf of manager
parent responds for child where authorized
caregiver responds for cared-for Person
service imports external response
```

Therefore conceptually distinguish:

```text
participant/native referent
response Actor
Account/Principal used
on-behalf-of/delegation basis
```

Participation v0 does not solve delegation; it preserves the boundary.

---

