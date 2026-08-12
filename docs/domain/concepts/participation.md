# Participation v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-12  
**Meaning of accepted:** best current decision; reopenable with stronger evidence  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Relationships / Reasoning

## Canonical definition

> **Participation is the contextual semantic relation family through which a native referent is represented as expected or intended to be involved, or as actually involved, in a bounded shared occurrence or interaction context. Intended/response participation and Actual participation are distinct semantic facets and may differ in state, time, role, provenance, authority and visibility. Participation does not create referent identity and does not by itself imply Responsibility, performance, organization, Authority, Visibility, Resource allocation, Acknowledgement, or Account identity.**

Participation answers bounded questions such as:

> **Who is expected/intended to be involved here?**

and, separately:

> **Who actually participated, and in what way/interval, where that matters?**

Participation is a **specific semantic relation family**, not a native entity/root and not a universal membership/social-graph primitive.

---

# 1. Why Participation exists

LifeOS already distinguishes one shared Event/Activity/Actual from actor-scoped state.

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

Without explicit Participation semantics, LifeOS is pushed toward weak alternatives such as one participant list/status, one Session per attendee, invitation/acceptance treated as Actual, decline treated as proved absence, Resource booking confused with involvement, or provider attendance telemetry treated as unquestioned human truth.

The actor-scoped semantic need is real; a universal Participant identity is not.

---

# 2. Participant is a contextual role, not identity

A Person does not become a second native domain object merely by being involved.

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

Eligible non-human referents, collective actors and exact typed-reference mechanics remain deferred.

---

# 3. Event identity is independent from Participation

```text
Event identity != participant set
Event identity != participant response
Event identity != actual attendance
```

Adding/removing/changing ordinary participant state does not automatically create a new Event.

Organizer/requester identity also does not establish Participation.

---

# 4. Intended/response Participation versus Actual Participation

This is the core invariant:

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

Correct history:

```text
historical response = accepted
Actual participation = none / established absence only if evidence supports it
```

Likewise:

```text
declined → later attends
never invited → later participates
```

are valid.

> **Later Actual participation must not rewrite earlier invitation/response history, and earlier invitation/response must not establish Actual participation.**

---

# 5. Invitation

`Invitation` is participation-related proposal/request semantics, not a standalone universal primitive.

Invitation does not establish:

```text
intended acceptance
Acknowledgement
Actual participation
```

A product may persist invitation workflow state where consequence requires it, but no universal Invitation root/table/state machine is pre-approved.

---

# 6. Participation response and the Acceptance boundary

A Participation response captures actor-scoped stance/intention toward expected participation.

Contextual states may include, depending on product/domain:

```text
needs action
tentative
accepted
declined
conditional
waitlisted
```

No universal enum is accepted.

Response answers:

> **What is the participant's current expressed stance toward expected participation?**

It does not answer whether the actor actually participated.

```text
accepted != attended
accepted != Actual participation
declined != proved absence
no response != declined
```

The later Acknowledgement v0 review tested generic cross-domain `Acceptance` and rejected it as a standalone kernel primitive.

Canonical current rule:

> **`accepted` inside Participation is Participation-response semantics; it is not an instance of a universal Acceptance root.**

Response history may be material and must not be silently overwritten.

---

# 7. Participation versus Acknowledgement

Acknowledgement records explicit taking-notice of a specific target/version/change/request.

Participation response records willingness/intention toward involvement.

```text
acknowledged changed Event time
!= accepted Participation
```

An actor may truthfully:

```text
acknowledge the new time
+
decline Participation
```

Therefore:

```text
Invitation != Acknowledgement
Acknowledgement != Participation response
```

Acknowledgement is now a canonical neighboring concept; it is no longer an unresolved generic common-ground dependency for Participation.

---

# 8. Attendance / Actual Participation

`Attendance` is Event-facing product/domain language for Actual Participation, not a standalone universal primitive.

Actual participation may be full, partial, multi-interval, established absent, or unknown where the domain/evidence supports those distinctions.

```text
Event 10:00–12:00
Anna Actual Participation 10:00–12:00
Luca Actual Participation 10:35–11:10
```

Attendance is not the same semantic as invitation response.

---

# 9. Participation versus Session and shared Actual

Session is bounded performed/execution episode semantics.

Participation is involvement in a shared occurrence/interaction.

```text
Participation != Session
Event attendance != Session by default
```

Likewise:

```text
shared Event Actual
!= identical actor-specific Actual Participation
```

A shared Event may occur once while actors have different participation intervals or established/unknown attendance states.

---

# 10. Participation versus performer

`performed_by` answers who executed work/behavior. Participation answers who was involved.

```text
concert audience member = participant != performer
meeting listener = participant != performer by default
```

> **Use the most specific truthful actor role; Participation must not replace performer/recorder/confirmer/acknowledger/responsible/etc. when that narrower role is what matters.**

---

# 11. Participation versus Responsibility

```text
Participation != Responsibility
Participant != responsible Actor
```

Involvement does not establish accountability, and accountability does not prove actual participation.

Responsibility changes may occur without changing Event/Activity identity or Participation.

---

# 12. Participation versus Resource

```text
Participation != Resource
Resource allocation != Participation
```

A room/equipment provider can be a Resource without being a participant merely because a calendar provider represents it as a resource attendee.

Provider vocabulary does not decide LifeOS ontology.

---

# 13. Participation versus Authority and Visibility

Participation grants neither governance nor universal exposure.

```text
Participation != Authority
Participation != Visibility
```

Visibility of Person + Event does not imply visibility of their Participation relation, response, attendance interval, decline reason, or private note.

Authority v0 and Visibility v0 own those independent questions.

---

# 14. Response actor versus participant identity

The native referent whose participation is at stake may differ from the Actor/Principal submitting a response.

Examples:

```text
assistant responds on behalf of manager
parent responds for child where authorized
caregiver responds for cared-for Person
service imports external response
```

Conceptually distinguish:

```text
participant/native referent
response Actor
Account/Principal used
on-behalf-of/delegation basis
```

Participation does not solve delegation; it preserves the boundary.

---

# 15. Actual Participation evidence and epistemic integrity

Provider attendance telemetry can be Evidence/Provenance without becoming unquestioned canonical Participation.

Possible failure modes include stale connection, shared device/account, identity mismatch, duplicates, corrected timestamps and participant dispute.

```text
provider attendance assertion
+
Provenance
+
applicable Evidence/reconciliation/Authority policy
↓
may establish/support current Actual Participation
```

Canonical rules:

```text
no attendance evidence != proved absence
provider telemetry != canonical human Participation universally
```

---

# 16. Epistemic distinctions

Participation must preserve:

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

Simple UI may hide these distinctions; the domain must not destroy them.

---

# 17. Recurrence / occurrence-specific Participation

Series-level participation expectation does not erase occurrence-specific response/state.

```text
weekly meeting series
Anna generally expected

occurrence 17
Anna declines only this one
```

Exact series inheritance/override persistence remains Recurrence/logical-model work.

---

# 18. Large participant sets and provider incompleteness

External systems may omit/truncate/partially propagate participant data.

> **Absence from an incomplete provider payload does not establish non-participation or non-invitation.**

Provider completeness is integration/Provenance evidence, not Participation truth.

Avoid materializing a universal social/member graph merely because a large Event exists.

---

# 19. Multi-actor implications

Participation supports, conceptually:

- non-LifeOS Persons;
- one shared object with actor-scoped Participation;
- different actor responses;
- invitation without response;
- response changed over time;
- accepted but absent;
- declined but later present;
- uninvited actual participant;
- partial/multi-interval participation;
- on-behalf-of response with truthful attribution;
- selective Visibility;
- historical attribution after Account/access changes;
- conflicting provider/user assertions;
- Participation without Responsibility and vice versa.

No per-actor duplicate Event is required for genuinely shared reality.

---

# 20. AI boundary

AI may suggest likely participants, summarize response state, propose invitations, surface likely mismatches, reconcile evidence candidates, or derive safe aggregates where authorized.

AI must not silently:

- establish Participation from social inference;
- turn Invitation into response;
- turn `accepted` response into Actual participation;
- turn no telemetry into absence;
- reveal private participation/reasons merely because endpoints are visible;
- impersonate the participant when responding;
- fabricate Acknowledgement from telemetry;
- rewrite response history from later attendance.

> **AI may propose or interpret Participation; inference capability does not establish actor intent, Acknowledgement, Actual participation, Authority, or disclosure permission.**

---

# 21. Product / UI language

Low-consequence UI may remain:

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

Power-user/specialist views may expose response history, role, Actual interval(s), on-behalf-of attribution, provider/source, reconciliation/conflict and selective Visibility.

The UI word `Accept` maps here to Participation response only when participation is the real domain question.

---

# 22. External benchmark synthesis

External products/standards remain evidence, not design authority.

Recurring useful patterns include separation of attendee identity, participation status, organizer, RSVP/delegation semantics, planned participation and attendance telemetry.

LifeOS retains the stronger internal boundary:

```text
expected participation
!= response
!= Acknowledgement
!= Actual involvement
```

without importing provider-specific enums as kernel truth.

---

# 23. Core invariants

1. **Participation is a contextual specific relation family, not native entity/root.**
2. **Participant is contextual role over native identity.**
3. **Expected/intended/response and Actual Participation are distinct facets.**
4. **Invitation is proposal/request semantics, not standalone universal primitive.**
5. **Invitation != Acknowledgement != Participation response != Actual Participation.**
6. **`accepted` is Participation-response semantics, not a universal Acceptance primitive.**
7. **Accepted != attended.**
8. **Declined != proved absence.**
9. **No response != declined.**
10. **No attendance evidence != proved absence.**
11. **Event identity != participant set/state.**
12. **Participation != Session/shared Actual/performer/Responsibility/Resource/organizer/requester.**
13. **Participation != Authority/Visibility.**
14. **Response Actor/Principal may differ from participant identity.**
15. **Provider telemetry does not automatically establish canonical Participation.**
16. **Partial/multi-interval involvement must not duplicate Event/Person identity.**
17. **Later Actual participation does not rewrite earlier response history.**
18. **Series-level participation does not erase occurrence-specific exceptions.**
19. **Specific actor roles take precedence where semantically narrower.**
20. **AI inference does not establish response, Acknowledgement, Actual attendance, Authority or disclosure permission.**
21. **No universal Participant/Participation/member/social-graph root is pre-approved.**

---

# 24. Relationship v0 compatibility

```text
simple expected involvement
→ direct specific Participation relation may suffice

material response/history/role/privacy semantics
→ specific qualified Participation context may be justified

Actual involvement
→ independently representable Participation facet/context

universal Relationship wrapper
→ unnecessary
```

Qualified structure does not automatically imply independent native entity identity.

---

# 25. Persistence/API implications — not physical design

Future logical modeling must support equivalent semantics where justified for:

- native participant reference;
- expected/intended state separate from Actual participation;
- invitation/proposal source;
- actor-scoped response/history;
- Actual state/interval(s);
- occurrence-specific overrides;
- response Actor/Account/Principal separate from participant;
- Provenance/provider reconciliation;
- explicit unknown versus established non-participation;
- selective Visibility;
- Acknowledgement separation;
- direct simple versus richer qualified representation.

Do not infer a universal participants/participations table, one status enum, Invitation entity, Attendance entity, one Session per attendee, participant=User/Account, or provider attendee vocabulary as ontology.

---

# 26. Adjacent Dependency Sweep

## RESOLVED

- Participation ↔ Event: Event identity independent from participant set/response/Actual involvement.
- Participation ↔ Person/Actor/Account: contextual role; Account not required; response Actor may differ.
- Participation ↔ Session: attendance does not require Session.
- Participation ↔ Actual: shared Actual != actor-scoped Actual Participation.
- Participation ↔ Invitation: proposal/request semantics; no universal primitive.
- Participation ↔ response: response/intention != Actual involvement.
- Participation ↔ Attendance: Event-facing Actual Participation; no universal primitive.
- Participation ↔ performer: narrower execution role != generic involvement.
- Participation ↔ Responsibility: involvement != accountability.
- Participation ↔ Resource: eligibility/allocation != involvement.
- Participation ↔ organizer/requester: organizing/requesting != participation.
- Participation ↔ Authority: involvement creates no governance power.
- Participation ↔ Visibility: involvement creates no universal exposure.
- Participation ↔ Acknowledgement: explicit taking-notice != participation response.
- Participation ↔ generic Acceptance: universal primitive rejected; `accepted` remains Participation response.

## SAFE DEFERRED

### Participant role taxonomy

**Owner:** product/specialist relationship review.  
**Why safe:** specific roles can coexist without one universal enum.  
**Reopening trigger:** ordinary cross-domain workflows require stable shared role ontology changing Participation boundaries.  
**Tests to rerun:** CORE-03, CORE-04, CORE-12, XCON-04, XCON-06.

### Group / collective participation

**Owner:** collective/group review.  
**Why safe:** current native-referent semantics do not require inventing Group identity.  
**Reopening trigger:** ordinary workflows require one collective Participation identity not decomposable into referents.  
**Tests to rerun:** CORE-04, CORE-06, MA-01, MA-03, XCON-01, XCON-04.

### Delegation / on-behalf-of

**Owner:** Principal/Authority/delegation review.  
**Why safe:** participant identity and response Actor are already distinct.  
**Reopening trigger:** response provenance/agency cannot be represented without changing Participation.  
**Tests to rerun:** MA-01, MA-06, MA-10, MA-13, MA-17, XCON-02.

### Recurring-series Participation

**Owner:** Recurrence + logical model.  
**Why safe:** series baseline and occurrence overrides remain separable.  
**Reopening trigger:** occurrence-specific participation cannot override series expectation without identity/history loss.  
**Tests to rerun:** CORE-02, XCON-03, XCON-04, CL-02, CL-06.

### Provider attendance reconciliation

**Owner:** Provenance/Authority/Decision + Integration logical model.  
**Why safe:** telemetry is Evidence/Provenance, not automatic truth.  
**Reopening trigger:** provider facts cannot establish/correct Actual Participation without altering Participation semantics.  
**Tests to rerun:** CORE-09, MA-10, MA-12, XCON-03, XCON-05.

### Retention / deletion

**Owner:** privacy/retention review.  
**Why safe:** Participation Visibility and history are separable.  
**Reopening trigger:** deletion/revocation requires per-user duplicate truth or destructive history rewrite.  
**Tests to rerun:** MA-07, MA-08, MA-11, XCON-05.

### Exact qualified Participation identity / persistence

**Owner:** logical data model.  
**Why safe:** semantic facets are fixed without pre-approving table/entity identity.  
**Reopening trigger:** persistence cannot preserve response/Actual/history/interval semantics under direct/qualified modeling.  
**Tests to rerun:** CORE-06, CORE-10, CORE-13, XCON-01, XCON-04.

```text
REOPEN                         0
unclassified material items    0
```

---

# 27. Rejected alternatives

Rejected:

- universal Participant entity/root;
- universal Participation/member/social-graph root;
- one Event `participants` list as complete truth;
- Participation = response;
- response = Actual attendance;
- accepted = attended;
- generic Acceptance root above Participation response;
- declined = proved absent;
- no response = declined;
- no telemetry = proved absence;
- Participation = Session/Event Actual/performer/Responsibility/Resource;
- organizer = participant;
- provider attendee/resource vocabulary as ontology;
- provider telemetry as universally authoritative truth;
- retroactive response rewrite from attendance;
- Invitation universal primitive;
- Attendance universal primitive.

---

# 28. Reopening triggers

Reopen Participation v0 if later evidence shows that:

1. intended/response and Actual involvement cannot remain distinct without a materially different model;
2. a stronger future common-ground model makes Participation response redundant or misplaced;
3. Authority/Visibility/Acknowledgement cannot remain external to Participation;
4. collective/group participation changes the relation-family identity;
5. Event/Session/Actual integration cannot preserve actor-scoped intervals without duplication;
6. provider reconciliation consistently requires a different truth model;
7. logical persistence cannot represent simple/direct and rich/qualified cases without contradiction.

Until stronger evidence appears, Participation remains the current accepted **specific semantic relation family** for intended and Actual involvement, with their histories kept distinct.
