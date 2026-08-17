<!-- LIFEOS-CANONICAL-SPLIT document="participation.md" part="2" total="3" -->
> **Canonical document split — Part 2 of 3.** Parts 1–3 together form one authoritative document; this is a physical split only, not a summary/reference hierarchy. The payload preserves the full pre-compaction baseline first and later downstream amendments in sequence; later explicit amendments override stale status/deferral wording without deleting the earlier rationale. Navigation: [Part 1](participation.md) · **Part 2** · [Part 3](participation-part-3.md)

<!-- LIFEOS-CANONICAL-PAYLOAD -->
# 16. Actual Participation evidence and epistemic integrity

Provider attendance telemetry can be strong evidence without becoming unquestioned canonical human Participation.

Example:

```text
provider record
Anna joined 10:00–11:00
```

Possible problems include:

- stale connection;
- shared device/account;
- provider identity mismatch;
- imported duplication;
- corrected timestamps;
- participant dispute.

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
not invited
!= invited + no response

no response
!= declined

accepted
!= actually participated

declined
!= proved absent

no attendance evidence
!= proved absent

partial participation
!= full participation

removed from expected participants
!= historically never invited

unknown Actual Participation
!= established non-participation
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

Some systems may provide multiple intervals:

```text
10:00–10:20
10:40–11:30
```

LifeOS must not create multiple Person identities or multiple Events merely because participation is discontinuous.

The exact interval/segment persistence is deferred.

---

# 19. Recurrence and occurrence-specific Participation

A response to a recurring series and a response to one occurrence need not be identical.

Example:

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

Therefore:

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

AI may:

- suggest likely participants;
- summarize response state;
- propose invitations;
- identify likely attendance mismatches;
- reconcile provider attendance candidates;
- derive safe aggregate participation projections where authorized.

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

Power-user/specialist views may expose:

- invited by;
- response history/time;
- required/optional role;
- actual interval(s);
- on-behalf-of response;
- provider/source;
- reconciliation/conflict;
- selective visibility.

The semantic distinction must not force enterprise wording into casual personal use.

---

# 24. External benchmark synthesis

External systems are benchmark evidence only.

Useful recurring patterns include:

- iCalendar separating attendee identity, participation status, role, RSVP and delegation/sent-by semantics;
- calendar APIs separating organizer from attendee response state;
- meeting platforms maintaining attendance telemetry separately from invitation response;
- healthcare/specialist systems separating planned appointment participation from actual encounter participation/periods;
- large-scale calendar systems exposing incomplete/limited attendee propagation under some conditions.

LifeOS adapts the recurring separation of **expected participation, response, and actual involvement** without importing provider-specific enums or treating provider attendance as unquestioned truth.

---

# 25. Adversarial reductio summary

## REMOVE Participation semantics

Actor-scoped expected/actual involvement collapses into Event fields, Session, performer or generic membership.

**Result:** FAIL.

## Participant = Person subtype/entity

Contextual involvement becomes native identity.

**Result:** FAIL.

## Participation = Event attendee list

Invitation, response, historical state and actual involvement collapse.

**Result:** FAIL.

## Participation = response

Accepted/declined cannot represent Actual attendance.

**Result:** FAIL.

## Participation = Actual

Shared Event realization and actor-scoped involvement collapse.

**Result:** FAIL.

## Participation = Session

Attendance creates redundant execution episodes and breaks Event semantics.

**Result:** FAIL.

## Participation = Performer

Non-performing attendees/listeners/audience cases fail.

**Result:** FAIL.

## Participation = Responsibility

Involvement becomes accountability.

**Result:** FAIL.

## Participation = Resource

Bookability/eligibility becomes involvement.

**Result:** FAIL.

## Universal membership/member relation

Long-lived membership/social-graph semantics are wrongly conflated with bounded participation.

**Result:** FAIL.

## Specific Participation relation family

Preserves intended/response and Actual facets without duplicate identity.

**Result:** PASS WITH HARDENING.

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

Participation is the second major stress of the accepted Relationship modeling discipline.

Current result:

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

The logical model may later choose one aggregate/record that contains both intended and Actual facets when it preserves their independent semantics. Participation v0 does **not** require two tables or two entity identities.

Qualified structure still does not automatically imply independent entity identity.

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

Do not infer from Participation v0 that LifeOS requires:

- universal `participants` table/root;
- universal `participations` entity/table;
- one `participant_status` enum;
- Invitation entity;
- Attendance entity;
- one Session per attendee;
- participant = Account/User;
- provider attendee/resource vocabulary as LifeOS ontology;
- response = Actual attendance;
- telemetry = canonical truth;
- universal membership/social graph.

---

# 29. Adjacent Dependency Sweep

## RESOLVED NOW

### Participation ↔ Event

**Resolution:** Event identity is independent from participant set, response and Actual participation.

### Participation ↔ Person / Actor / Account

**Resolution:** Participant is contextual involvement over native identity; Account is not required; response Actor/Principal may differ.

### Participation ↔ Session

**Resolution:** attendance/Actual involvement does not require a Session; Session remains performed-execution episode semantics.

### Participation ↔ Actual

**Resolution:** shared Event Actual is distinct from actor-scoped Actual Participation.

### Participation ↔ Invitation

**Resolution:** Invitation is participation proposal/request semantics, not standalone universal primitive.

### Participation ↔ response

**Resolution:** response/intention is distinct from Actual participation.

### Participation ↔ Attendance

**Resolution:** Attendance is Event-facing Actual Participation language/semantics, not standalone universal primitive.

### Participation ↔ Performer

**Resolution:** performed execution is a narrower Actor role and not generic Participation.

### Participation ↔ Responsibility

**Resolution:** involvement != accountability.

### Participation ↔ Resource

**Resolution:** eligibility/allocation != involvement.

### Participation ↔ organizer/requester

**Resolution:** organizing/requesting does not establish Participation.

### Participation ↔ Authority

**Resolution:** Authority v0 defines governance separately; Participation creates no canonical-change power.

### Participation ↔ Visibility

**Resolution:** Visibility v0 defines information exposure separately; endpoints may be visible while Participation/response/attendance remains hidden.

## SAFE DEFERRED

### Acceptance / Acknowledgement

**Owner:** Relationships / Reasoning — collaboration-state review.  
**Why safe:** Participation response is bounded without equating it with generic Acceptance/Acknowledgement across other domains.  
**Reopening trigger:** invitation/response cannot compose with a future common-ground model without changing Participation meaning.  
**Tests to rerun:** CORE-02, CORE-04, MA-05, MA-11, XCON-04, XCON-05.

### Participant role taxonomy

**Owner:** product/specialist relationship review.  
**Why safe:** specific roles may coexist without one universal enum.  
**Reopening trigger:** ordinary cross-domain workflows require a stable shared role ontology that changes Participation boundaries.  
**Tests to rerun:** CORE-03, CORE-04, CORE-12, XCON-04, XCON-06.

### Group / collective invitation or participation

**Owner:** collective/group actor review.  
**Why safe:** current Person/native-referent semantics do not require inventing Team identity.  
**Reopening trigger:** common workflows require one collective Participation identity not decomposable into referents.  
**Tests to rerun:** CORE-04, CORE-06, MA-01, MA-03, XCON-01, XCON-04.

### Delegation / on-behalf-of

**Owner:** Principal/Authority/delegation review.  
**Why safe:** participant identity and response Actor are already separated.  
**Reopening trigger:** response provenance/agency cannot be represented without changing Participation itself.  
**Tests to rerun:** MA-01, MA-06, MA-10, MA-13, MA-17, XCON-02.

### Recurring-series Participation

**Owner:** Recurrence + logical model.  
**Why safe:** series baseline and occurrence override semantics are preserved conceptually.  
**Reopening trigger:** occurrence-specific participation cannot override series expectations without identity/history loss.  
**Tests to rerun:** CORE-02, XCON-03, XCON-04, CL-02, CL-06.

### Provider attendance reconciliation / evidence threshold

**Owner:** Provenance/Authority/Decision + Integration logical model.  
**Why safe:** telemetry is explicitly evidence, not automatic canonical Participation.  
**Reopening trigger:** provider facts cannot establish/correct Actual Participation without altering Participation semantics.  
**Tests to rerun:** CORE-09, MA-10, MA-12, XCON-03, XCON-05.

### Retention / deletion

**Owner:** privacy/retention review.  
**Why safe:** Participation visibility and history are already separable.  
**Reopening trigger:** deletion/revocation requirements require per-user duplicate reality or destructive history rewriting.  
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
- Participation = Session;
- Participation = Event Actual;
- Participation = performer;
- Participation = Responsibility;
- Participation = Resource;
- organizer = participant;
- resource attendee/provider vocabulary as ontology;
- provider attendance telemetry as universally authoritative truth;
- retroactive rewrite of response from later attendance;
- Invitation as standalone universal primitive;
- Attendance as standalone universal primitive.

---

