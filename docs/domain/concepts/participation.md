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

Attendance may be full, partial, absent where established, unknown, or represented through one or multiple actual participation intervals where justified.

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

Likewise, visibility of Person + Event must not imply visibility of their Participation relation, response, attendance interval, reason for decline, or private note.

Canonical rule:

> **Endpoint visibility does not imply Participation-relation visibility, and Participation does not manufacture Authority.**

Authority v0 and Visibility v0 close these boundaries independently. Participation may be a basis considered by policy, but it creates neither governance power nor automatic disclosure.

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

# 16. Actual Participation evidence and epistemic integrity

Provider attendance telemetry can be strong evidence without becoming unquestioned canonical human Participation.

Possible problems include stale connection, shared device/account, provider identity mismatch, imported duplication, corrected timestamps, and participant dispute.

Therefore:

```text
provider attendance record
+
Provenance
+
applicable Evidence/reconciliation policy
↓
may establish or support Actual Participation
```

not:

```text
provider telemetry = canonical Participation universally
```

Canonical rule:

> **No attendance evidence != proved absence, and provider attendance evidence does not bypass Provenance/Authority/reconciliation semantics.**

---

# 17. Epistemic distinctions

Participation v0 requires these differences to remain representable:

```text
not invited != invited + no response
no response != declined
accepted != actually participated
declined != proved absent
no attendance evidence != proved absent
partial participation != full participation
removed from expected participants != historically never invited
unknown Actual Participation != established non-participation
```

These distinctions may be hidden in simple UI but must not be destroyed by the domain.

---

# 18. Partial and interval participation

Actual Participation may cover only part of a shared occurrence.

```text
Event
10:00–12:00

Luca
participated 10:35–11:10
```

Some systems may provide multiple intervals. LifeOS must not create multiple Person identities or multiple Events merely because participation is discontinuous.

The exact interval/segment persistence is deferred.

---

# 19. Recurrence and occurrence-specific Participation

A response to a recurring series and a response to one occurrence need not be identical.

```text
weekly meeting series
Anna generally expected

occurrence 17
Anna declines only this one
```

Participation v0 requires occurrence-specific state to remain representable without rewriting series-level expectation.

Exact series inheritance/override persistence remains Recurrence/logical-model work.

---

# 20. Large participant sets and incomplete provider representations

External systems may omit, truncate or partially propagate participant data at scale.

> **Absence from an incomplete provider payload does not establish non-participation or non-invitation.**

Provider completeness is Provenance/integration evidence, not Participation truth.

LifeOS should avoid materializing unnecessary full social/member graphs merely because a large Event exists.

---

# 21. Multi-actor implications

Participation must support:

- non-LifeOS Persons;
- one shared Event/Actual with actor-scoped Participation;
- different responses from different people;
- invitation without response;
- response changed over time;
- accepted but absent;
- declined but later present;
- uninvited actual participant;
- partial participation;
- response submitted on behalf of another Person;
- selective visibility of participant relation/state;
- historical attribution after Account changes;
- conflicting provider/user assertions;
- participation without Responsibility;
- Responsibility without actual participation.

No per-actor duplicate Event is required for genuinely shared reality.

---

# 22. AI boundary

AI may suggest likely participants, summarize response state, propose invitations, identify likely attendance mismatches, reconcile provider attendance candidates, or derive safe aggregate participation projections where authorized.

AI must not silently:

- establish Participation from social inference;
- turn an invitation into acceptance;
- turn acceptance into Actual participation;
- turn no telemetry into absence;
- reveal private participation/reasons merely because endpoints are visible;
- impersonate the participant when submitting a response;
- rewrite earlier response history from later attendance.

Canonical rule:

> **AI may propose or interpret Participation; inference capability does not establish actor intent, Actual participation, Authority, or disclosure permission.**

Visibility v0 strengthens this: authorized processing of private participation context does not permit disclosure of that context unless the recipient/output has its own valid Visibility basis.

---

# 23. Simple UI versus kernel semantics

Low-consequence Event UI may remain simple:

```text
Going
Maybe
Can't go
```

and later:

```text
Attended
Didn't attend
```

Power-user/specialist views may expose invited by, response history/time, required/optional role, actual interval(s), on-behalf-of response, provider/source, reconciliation/conflict, and selective visibility.

The semantic distinction must not force enterprise wording into casual personal use.

---

# 24. External benchmark synthesis

External systems are benchmark evidence only.

Useful recurring patterns include iCalendar separating attendee identity/participation status/role/RSVP/delegation; calendar APIs separating organizer from attendee response; meeting platforms maintaining attendance telemetry separately; specialist systems separating planned participation from actual encounter participation; and large-scale calendars exposing incomplete propagation.

LifeOS adapts the recurring separation of **expected participation, response, and actual involvement** without importing provider-specific enums or treating provider attendance as unquestioned truth.

---

# 25. Adversarial reductio summary

```text
REMOVE Participation                         FAIL
Participant = Person subtype/entity          FAIL
Participation = attendee list                FAIL
Participation = response                     FAIL
Participation = Actual                       FAIL
Participation = Session                      FAIL
Participation = performer                    FAIL
Participation = Responsibility               FAIL
Participation = Resource                     FAIL
universal membership/member relation         FAIL
specific Participation relation family       PASS WITH HARDENING
```

---

# 26. Core invariants

1. **Participation is a contextual specific semantic relation family, not a native entity/root.**
2. **Participant is a contextual role over native identity, not a Person subtype/root.**
3. **Participation may represent expected/intended involvement and Actual involvement as distinct facets.**
4. **Intended/response Participation != Actual Participation.**
5. **Invitation is a participation proposal/request, not Actual participation or Acceptance.**
6. **Participation response != Actual participation.**
7. **Accepted != attended.**
8. **Declined != proven absence.**
9. **No response != declined.**
10. **No attendance evidence != proved absence.**
11. **Event identity != participant set/state.**
12. **Participation != Session.**
13. **Shared Event Actual != identical actor-specific Participation.**
14. **Participation != performer.**
15. **Participation != Responsibility.**
16. **Participation != Resource.**
17. **Participation != organizer/requester.**
18. **Participation != Authority or Visibility.**
19. **Response Actor/Principal may differ from participant identity.**
20. **Provider attendance telemetry does not automatically establish canonical human Participation.**
21. **Partial/multi-interval actual involvement must not create duplicate Event/Person identity.**
22. **Later Actual participation does not rewrite earlier response history.**
23. **Series-level participation does not erase occurrence-specific exceptions.**
24. **Specific actor roles take precedence over generic Participation when the narrower role is the real semantic question.**
25. **AI inference does not establish Participation, response, Actual attendance, Authority or disclosure permission.**
26. **No universal Participant/Participation root/table/member graph is pre-approved.**
27. **Participation grants neither Visibility nor Authority to re-disclose by itself.**

---

# 27. Relationship v0 compatibility

```text
simple expected involvement
→ direct specific participation relation may suffice

material response/history/role/privacy semantics
→ specific qualified Participation context may be justified

Actual involvement
→ independently representable Participation facet/context

universal Relationship wrapper
→ still unnecessary
```

The logical model may later choose one aggregate/record containing intended and Actual facets when it preserves their independent semantics. Participation v0 does not require two tables or two entity identities.

---

# 28. Persistence/API implications — deliberately not physical design

Future logical modeling must support, where justified:

- native participant reference;
- expected/intended participation separate from Actual participation;
- invitation/proposal source;
- actor-scoped response and response history;
- actual participation state and optional interval(s);
- occurrence-specific overrides for recurrence;
- response Actor/Account/Principal separate from participant;
- Provenance/provider mapping and reconciliation;
- explicit unknown versus established non-participation;
- selective visibility;
- direct simple versus richer qualified representation.

Do not infer universal participants/participations roots, one status enum, Invitation entity, Attendance entity, one Session per attendee, participant=Account/User, provider attendee/resource ontology, response=Actual attendance, telemetry=canonical truth, or universal membership graph.

---

# 29. Adjacent Dependency Sweep

## RESOLVED NOW

- Participation ↔ Event: Event identity independent from participant set/response/Actual involvement.
- Participation ↔ Person/Actor/Account: contextual role; Account not required; response Actor/Principal may differ.
- Participation ↔ Session: attendance/Actual involvement does not require Session.
- Participation ↔ Actual: shared Event Actual distinct from actor-scoped Actual Participation.
- Participation ↔ Invitation: participation proposal/request semantics, no universal primitive.
- Participation ↔ response: response/intention distinct from Actual participation.
- Participation ↔ Attendance: Event-facing Actual Participation semantics, no universal primitive.
- Participation ↔ Performer: narrower execution role != generic involvement.
- Participation ↔ Responsibility: involvement != accountability.
- Participation ↔ Resource: eligibility/allocation != involvement.
- Participation ↔ organizer/requester: organizing/requesting != involvement.
- Participation ↔ Authority: governance separately owned.
- Participation ↔ Visibility: exposure separately owned.

## SAFE DEFERRED

### Acceptance / Acknowledgement

**Owner:** Relationships / Reasoning — collaboration-state review.  
**Why safe:** Participation response is bounded without equating it with generic Acceptance/Acknowledgement across domains.  
**Reopening trigger:** invitation/response cannot compose with future common-ground model without changing Participation meaning.  
**Tests to rerun:** CORE-02, CORE-04, MA-05, MA-11, XCON-04, XCON-05.

### Participant role taxonomy

**Owner:** product/specialist relationship review.  
**Why safe:** specific roles may coexist without one universal enum.  
**Reopening trigger:** ordinary cross-domain workflows require stable shared role ontology changing Participation boundaries.  
**Tests to rerun:** CORE-03, CORE-04, CORE-12, XCON-04, XCON-06.

### Group / collective invitation or participation

**Owner:** collective/group actor review.  
**Why safe:** current native-referent semantics do not require inventing Team identity.  
**Reopening trigger:** common workflows require one collective Participation identity not decomposable into referents.  
**Tests to rerun:** CORE-04, CORE-06, MA-01, MA-03, XCON-01, XCON-04.

### Delegation / on-behalf-of

**Owner:** Principal/Authority/delegation review.  
**Why safe:** participant identity and response Actor already separated.  
**Reopening trigger:** response Provenance/agency cannot be represented without changing Participation.  
**Tests to rerun:** MA-01, MA-06, MA-10, MA-13, MA-17, XCON-02.

### Recurring-series Participation

**Owner:** Recurrence + logical model.  
**Why safe:** series baseline and occurrence override semantics preserved conceptually.  
**Reopening trigger:** occurrence-specific Participation cannot override series expectations without identity/history loss.  
**Tests to rerun:** CORE-02, XCON-03, XCON-04, CL-02, CL-06.

### Provider attendance reconciliation / evidence threshold

**Owner:** Provenance/Authority/Decision + Integration logical model.  
**Why safe:** telemetry explicitly Evidence, not automatic canonical Participation.  
**Reopening trigger:** provider facts cannot establish/correct Actual Participation without altering Participation semantics.  
**Tests to rerun:** CORE-09, MA-10, MA-12, XCON-03, XCON-05.

### Retention / deletion

**Owner:** privacy/retention review.  
**Why safe:** Participation Visibility and history already separable.  
**Reopening trigger:** deletion/revocation requires per-user duplicate reality or destructive history rewrite.  
**Tests to rerun:** MA-07, MA-08, MA-11, XCON-05.

### Exact qualified Participation identity / persistence

**Owner:** logical data model.  
**Why safe:** semantic facets fixed without pre-approving table/entity identity.  
**Reopening trigger:** persistence cannot preserve response/Actual/history/interval semantics under direct/qualified modeling.  
**Tests to rerun:** CORE-06, CORE-10, CORE-13, XCON-01, XCON-04.

```text
REOPEN                         0
unclassified material items    0
```

---

# 30. Rejected alternatives

Rejected:

- universal Participant entity/root;
- universal Participation/member/social-graph root;
- one Event `participants` list as complete Participation truth;
- Participation = response;
- response = Actual attendance;
- accepted = attended;
- declined = proved absent;
- no response = declined;
- no telemetry = proved absence;
- Participation = Session/Event Actual/performer/Responsibility/Resource;
- organizer = participant;
- resource attendee/provider vocabulary as ontology;
- provider telemetry as universally authoritative truth;
- retroactive response rewrite from attendance;
- Invitation as standalone universal primitive;
- Attendance as standalone universal primitive.

---

# 31. Deliberately deferred questions

- generic Acceptance/Acknowledgement relationship to Participation response;
- on-behalf-of/delegated response semantics;
- participant role taxonomy;
- collective/group participation;
- recurring-series participation inheritance/override;
- exact evidence/Authority threshold for established Actual Participation;
- retention/deletion/privacy lifecycle;
- exact qualified Participation identity/cardinality/persistence;
- specialist interaction/encounter extensions;
- final API/SQL representation.

Authority and Visibility are no longer deferred at the semantic-boundary level; detailed policy/enforcement/persistence remains separately owned.

---

# 32. Reopening triggers

Reopen Participation v0 if later evidence shows that:

1. intended/response and Actual involvement cannot remain distinct without a materially different model;
2. generic Acceptance/Acknowledgement semantics require response to move outside Participation entirely;
3. Authority/Visibility cannot remain external to Participation;
4. collective/group participation requires native identity semantics changing the relation family;
5. Event/Session/Actual integration cannot preserve actor-scoped intervals without duplication;
6. provider reconciliation consistently requires a different truth model;
7. logical persistence cannot represent simple/direct and rich/qualified cases without contradiction.

Until stronger evidence appears, Participation remains the current accepted **specific semantic relation family** for intended and Actual involvement, with their histories kept distinct.

---

# 2026-08-12 — Acknowledgement / generic Acceptance closure amendment

Acknowledgement v0 resolves the common-ground dependency that Participation v0 intentionally left open.

```text
Acknowledgement
= explicit actor-scoped taking-notice of a specific target/material version/change/request

Acknowledgement != Participation response
```

Therefore the response sequence can be represented without collapsing states:

```text
Invitation
!= delivered/read
!= Acknowledgement
!= Participation response
!= Actual Participation
```

`accepted` inside Participation remains **Participation-response semantics**. The later common-ground review tested generic cross-domain `Acceptance` and rejected it as a standalone kernel primitive.

Examples:

```text
acknowledge changed Event time
+
decline Participation
```

and:

```text
accepted Participation
→ later no-show
```

remain independently truthful.

The historical `Acceptance / Acknowledgement` SAFE DEFERRED item is now downstream-closed as:

```text
Participation ↔ Acknowledgement     RESOLVED
Participation ↔ generic Acceptance  RESOLVED — universal primitive rejected
```

Agreement/Consent, detailed delegation/on-behalf-of, Decision/effective change, collective semantics, provider reconciliation and persistence remain separately owned dependencies. No Participation reopening is required.

---

# 2026-08-13 — Representation / on-behalf-of downstream closure

Representation v0 closes Participation's explicit response-Actor / participant / Principal / on-behalf-of semantic boundary without changing Participation itself.

Canonical separation:

```text
participant/native referent
= whose involvement/response is at stake

response Actor
= who actually submitted/changed the Participation response

Representation / on-behalf-of
= response Actor acted for a distinct represented participant/party in that bounded action/context

Principal
= technical security identity used for the request
```

Therefore:

```text
participant != response Actor by default
response Actor != Principal
Representation != Participation
Representation != Participation response
```

A represented response may have effect for the participant under applicable Authority/policy, but LifeOS does not rewrite the actual response Actor as if the participant personally performed the action.

The former `Delegation / on-behalf-of` SAFE DEFERRED item is **RESOLVED at the semantic relation boundary**. Exact Principal/AuthN/AuthZ mechanics, legal/specialist representative validity, collective representation, provider evidence thresholds and physical persistence remain independently SAFE DEFERRED.

AI/service submission follows the same rule: the AI/service remains the actual Actor where material and cannot manufacture a human response merely by prediction or technical access.

No Participation hardening failed. **Participation remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `representation.md`;
- `../checkpoints/representation-delegation-principal-v0-validation.md`.
