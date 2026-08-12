# Participation v0 — Validation Checkpoint

**Status:** PASS WITH HARDENING  
**Validated:** 2026-08-12  
**Validation standard:** [Domain Validation Methodology v3](../validation-methodology-v3.md)  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## 1. Scope

- **Primary candidate:** Participation
- **Family reviewed together:** Participation / Participant / Invitation / Participation Response / Attendance / planned-intended participation / Actual participation
- **Why reviewed as one family:** calendar/product language often collapses invitation, attendee response, presence and membership into one `participant`/`status` shape. Reviewing the nouns separately first would risk manufacturing several primitives before proving their semantic independence.
- **Inherited pressure:** Event state vs participant response vs attendance; Session != Event attendance; shared Actual != actor-specific participation; Actor specific-role precedence; Responsibility/Resource separation; Relationship v0 direct-vs-qualified discipline.

This checkpoint validates Participation as a **specific semantic relation family**. It does not select final SQL/API/cardinality, create a universal Participant/Participation root, accept Invitation or Attendance as standalone universal primitives, or establish a universal participation-status enum.

---

# 2. Candidate conclusion

> **Participation is the contextual semantic relation family through which a native referent is represented as expected or intended to be involved, or as actually involved, in a bounded shared occurrence or interaction context. Intended/response participation and Actual participation are distinct semantic facets and may differ in state, time, role, provenance, authority and visibility. Participation does not create referent identity and does not by itself imply Responsibility, performance, organization, Authority, Visibility, Resource allocation, or Account identity.**

Current classification:

```text
PARTICIPATION
CANONICAL SPECIFIC SEMANTIC RELATION FAMILY
may be direct or specifically qualified depending on consequence
NOT native entity/root

PARTICIPANT
contextual role over native identity
NOT entity/root

INVITATION
participation proposal/request semantics
NOT standalone universal primitive

PARTICIPATION RESPONSE
actor-scoped intended/response state
NOT Actual participation

ATTENDANCE
Event-facing Actual Participation semantics
NOT standalone universal primitive

PLANNED / INTENDED PARTICIPATION
!=
ACTUAL PARTICIPATION
```

---

# 3. Evidence reviewed

## Internal

- Event v0, especially `Event state != participant response != actual attendance`;
- Session v0, especially Event attendance not requiring Session;
- Actual v0, especially shared Actual != actor-specific participation;
- Actor v0 and specific-role precedence;
- Responsibility v0;
- Resource v0;
- Multi-Actor Readiness v1 and evidence synthesis;
- Relationship v0 validation;
- personal, household, social, work, care, meeting, shift, webinar and recurring-event scenarios.

## External benchmark patterns

External systems were used as evidence, not schemas to copy. Recurring useful patterns included:

- iCalendar separating attendee identity, participation status, role, RSVP and delegation/sent-by semantics;
- calendar APIs separating organizer from attendee response state;
- meeting systems maintaining actual attendance intervals separately from invitation response;
- specialist interaction systems distinguishing planned appointment participation from actual encounter participation;
- large-calendar provider behavior showing attendee representations may be incomplete or selectively propagated at scale.

Provider enums/terminology are not LifeOS invariants.

---

# 4. Core Semantic Validation Gate

| Test ID | Result | Finding |
|---|---|---|
| CORE-01 Workflow inversion | PASS | Real workflows need actor-scoped expected and actual involvement distinct from Event identity. |
| CORE-02 Deep chronology | PASS WITH HARDENING | invitation → response → changed response → actual presence/absence/partial presence must remain historically separable. |
| CORE-03 Reductio | PASS | attendee list, response, Session, Actual, performer, Responsibility and Resource each fail as Participation replacement. |
| CORE-04 Redundancy / merge-split | PASS WITH HARDENING | Participation survives; Participant is role; Invitation/Attendance do not justify universal standalone primitives. |
| CORE-05 Traceability | PASS | invitation/response/intended/Actual involvement remains reconstructable without duplicate Event/Person. |
| CORE-06 Orphan / independence | PASS | Participation is contextual relation semantics, not native identity; rich qualified form does not automatically imply entity identity. |
| CORE-07 External benchmark | PASS | Mature systems repeatedly distinguish planned response from actual attendance/involvement. |
| CORE-08 Anti-pattern | PASS | universal member/attendee/status/social graph and one-Session-per-attendee are rejected. |
| CORE-09 Correction / epistemic integrity | PASS WITH HARDENING | no response != declined; no telemetry != absence; later attendance does not rewrite earlier response. |
| CORE-10 Scale/history | PASS WITH HARDENING | incomplete provider participant payloads must not become negative facts; no full social graph required. |
| CORE-11 Simple vs power user | PASS | casual UI may remain Going/Maybe/Can't go and Attended/Didn't attend. |
| CORE-12 Product value/complexity | PASS | richer states remain progressive and consequence-driven. |
| CORE-13 Implementation pressure | PASS WITH HARDENING | direct simple vs specific qualified Participation allowed; exact physical representation deferred. |

**Core Gate:** PASS WITH HARDENING.

---

# 5. Deep chronology stress

Representative chronology:

```text
T0  Anna invited
T1  Anna has not responded
T2  Anna accepts
T3  Anna later changes response to tentative
T4  Event occurs
T5  Anna participates only 10:30–11:15
T6  provider reports 10:25–11:20
T7  Anna corrects/disputes provider timing
T8  later historical query
```

Required truths:

- invitation does not establish acceptance;
- no response does not establish decline;
- response history remains historical intent/stance;
- actual participation is distinct from response;
- partial actual participation is valid;
- provider telemetry is evidence/provenance, not unquestioned canonical truth;
- Event identity survives all ordinary participant changes.

Counter-chronologies also remain valid:

```text
declined → later attends
never invited → later participates
accepted → later absent
```

No retroactive fabricated invitation/response is created from later reality.

---

# 6. Reductio / candidate elimination

## Participant = Person subtype/entity

Contextual involvement becomes native identity.

**Result:** REJECTED.

## Participation = Event attendee list

Invitation/response/history/Actual involvement collapse.

**Result:** REJECTED.

## Participation = response

Accepted/declined cannot represent Actual involvement.

**Result:** REJECTED.

## Participation = Event Actual

Shared occurrence reality and actor-scoped involvement collapse.

**Result:** REJECTED.

## Participation = Session

Attendance creates redundant execution episodes and breaks Session semantics.

**Result:** REJECTED.

## Participation = performer

Non-performing attendees/listeners/audience cases fail.

**Result:** REJECTED.

## Participation = Responsibility

Involvement becomes accountability.

**Result:** REJECTED.

## Participation = Resource

Eligibility/bookability becomes involvement.

**Result:** REJECTED.

## Universal member/membership/social graph

Bounded participation is confused with long-lived membership/social relationship.

**Result:** REJECTED.

## Participation as specific relation family

Expected/intended/response and Actual facets remain distinct around one shared context.

**Result:** PASS WITH HARDENING.

---

# 7. Key hardenings

## 7.1 Response/intention != Actual participation

```text
accepted != attended
declined != proved absent
no response != declined
```

Later actual reality does not rewrite earlier response history.

## 7.2 No evidence != established absence

```text
no attendance telemetry
!=
proved non-participation
```

Evidence completeness/authority matters.

## 7.3 Invitation does not create Participation truth

Invitation is a proposal/request for intended involvement; it does not establish response or Actual participation.

## 7.4 Participant is a role, not an identity

No `Participant` wrapper/root is justified. Native referent identity remains authoritative.

## 7.5 Attendance is Event-facing Actual Participation

Attendance is not a universal separate primitive and does not require Session by default.

## 7.6 Specific-role precedence survives

Where the real semantic question is performer, recorder, confirmer, responsible actor, organizer, etc., use that specific role rather than generic Participation.

## 7.7 Qualified relation != entity automatically

Rich Participation may need response history, role, interval, provenance and privacy without proving a universal independent Participation identity/root.

---

# 8. Multi-Actor Compatibility Gate

| Test ID | Result | Finding |
|---|---|---|
| MA-01 Identity/account independence | PASS | Accountless Person can participate; Account lifecycle does not erase historical Participation. |
| MA-02 Shared fact / actor overlay | PASS | one shared Event/Actual supports separate actor-scoped Participation. |
| MA-03 Responsibility/assignment/claim | PASS | involvement remains distinct from accountability/role assignment. |
| MA-04 Stewardship/mental load | PASS | participation does not imply coordination burden. |
| MA-05 Common-ground states | PASS WITH HARDENING | invitation/delivery/response/acceptance/Actual involvement cannot be one universal state. |
| MA-06 Authority/canonical change | PASS WITH HARDENING | Participation grants no Authority; delegated response remains contextual. |
| MA-07 Selective disclosure | PASS WITH HARDENING | endpoint visibility != participation/response/attendance visibility. |
| MA-08 Inference privacy | PASS WITH HARDENING | AI/social inference does not establish/disclose Participation. |
| MA-09 Partial adoption | PASS | non-LifeOS Persons are ordinary participants. |
| MA-10 Assisted participation/provenance | PASS WITH HARDENING | participant may differ from response Actor/Account/Principal. |
| MA-11 Lifecycle/revocation | PASS WITH HARDENING | response/participation changes preserve material history. |
| MA-12 Conflict/adversarial | PASS WITH HARDENING | provider/user participation assertions may remain unresolved pending reconciliation. |
| MA-13 Unequal power | PASS WITH HARDENING | on-behalf-of/guardian/manager response requires contextual Authority, not universal assumptions. |
| MA-14 Multi-resource/capacity | PASS | resource booking/capacity remains separate from participation. |
| MA-15 Coordination burden | PASS | attendance/involvement does not establish stewardship. |
| MA-16 Formality/progressive disclosure | PASS | simple participation UI remains possible. |
| MA-17 AI authority | PASS WITH HARDENING | AI may propose/infer but does not establish response/attendance/Authority. |
| MA-18 Specialist boundary | PASS | specialist encounter/attendance models remain adapters/extensions. |
| MA-19 Primitive redundancy | PASS | Invitation/Attendance/Participant roots do not survive. |
| MA-20 Actor-scoped reality attribution | PASS | shared Actual and actor-specific Actual Participation remain distinct. |

**Multi-Actor Gate:** PASS WITH HARDENING.

---

# 9. Cross-Concept Consistency Gate

```text
XCON-01 Identity                           PASS
XCON-02 Ownership / Authority              PASS WITH HARDENING
XCON-03 Planned / current / actual/history PASS
XCON-04 Relationships                      PASS WITH HARDENING
XCON-05 Multi-actor                        PASS WITH HARDENING
XCON-06 Language                           PASS
```

No accepted Cluster 1–4 concept requires structural reopening.

Event is strengthened: participant state remains independent from Event identity/state.

Session is strengthened: attendance does not require Session by default.

Actual is strengthened: shared Actual remains distinct from actor-scoped Actual Participation.

Actor is strengthened: Participant is another specific contextual role, not Actor identity.

Responsibility is strengthened: involvement != accountability.

Resource is strengthened: eligibility/allocation != participation.

Relationship v0 is confirmed again: direct/simple and richer qualified Participation can coexist without a universal Relationship root.

---

# 10. Adjacent Dependency Sweep

## RESOLVED

| Boundary | Resolution |
|---|---|
| Participation ↔ Event | Event identity independent from participant set/response/Actual involvement |
| Participation ↔ Person/Actor/Account | Participant is contextual role over native identity; Account not required |
| Participation ↔ Session | attendance/Actual involvement does not require Session |
| Participation ↔ Actual | shared Actual != actor-scoped Actual Participation |
| Participation ↔ Invitation | participation proposal/request; no universal standalone primitive |
| Participation ↔ response | response/intention != Actual participation |
| Participation ↔ Attendance | Event-facing Actual Participation; no universal standalone primitive |
| Participation ↔ performer | narrower execution role != generic involvement |
| Participation ↔ Responsibility | involvement != accountability |
| Participation ↔ Resource | eligibility/allocation != involvement |
| Participation ↔ organizer/requester | organizing/requesting != participation |

## SAFE DEFERRED

### Acceptance / Acknowledgement

**Owner:** collaboration-state review.  
**Safe because:** Participation response is bounded without claiming a universal Acceptance/Acknowledgement model.  
**Reopening trigger:** invitation/response cannot compose with common-ground semantics without changing Participation meaning.  
**Rerun:** CORE-02, CORE-04, MA-05, MA-11, XCON-04, XCON-05.

### Authority / Visibility

**Owner:** Authority/Visibility review.  
**Safe because:** Participation explicitly grants neither.  
**Reopening trigger:** participation state/access cannot be governed without making permission intrinsic to Participation.  
**Rerun:** MA-06, MA-07, MA-08, MA-13, MA-17, XCON-02, XCON-05.

### Participant role taxonomy

**Owner:** product/specialist relationship review.  
**Safe because:** specific roles can remain contextual without one universal enum.  
**Reopening trigger:** ordinary cross-domain workflows require a stable shared role ontology that changes Participation boundaries.  
**Rerun:** CORE-03, CORE-04, CORE-12, XCON-04, XCON-06.

### Group / collective Participation

**Owner:** collective/group actor review.  
**Safe because:** no Team/group native identity is required by current cases.  
**Reopening trigger:** common workflows require one collective Participation identity not decomposable into native referents.  
**Rerun:** CORE-04, CORE-06, MA-01, MA-03, XCON-01, XCON-04.

### Delegation / on-behalf-of response

**Owner:** Principal/Authority/delegation review.  
**Safe because:** participant identity and response Actor are already separated.  
**Reopening trigger:** response agency/provenance cannot be represented without changing Participation.  
**Rerun:** MA-01, MA-06, MA-10, MA-13, MA-17, XCON-02.

### Recurring-series Participation

**Owner:** Recurrence + logical model.  
**Safe because:** series expectation and occurrence override are conceptually separable now.  
**Reopening trigger:** occurrence-specific participation cannot override series baseline without history/identity loss.  
**Rerun:** CORE-02, XCON-03, XCON-04, CL-02, CL-06.

### Provider attendance reconciliation / evidence threshold

**Owner:** Provenance/Authority/Decision + Integration logical model.  
**Safe because:** telemetry is explicitly evidence rather than automatic canonical truth.  
**Reopening trigger:** provider facts cannot establish/correct Actual Participation without changing Participation semantics.  
**Rerun:** CORE-09, MA-10, MA-12, XCON-03, XCON-05.

### Retention / deletion

**Owner:** privacy/retention review.  
**Safe because:** relation visibility/history are already separable from endpoints.  
**Reopening trigger:** deletion/revocation requires per-user duplicate Event reality or destructive history rewriting.  
**Rerun:** MA-07, MA-08, MA-11, XCON-05.

### Qualified Participation identity / persistence

**Owner:** logical data model.  
**Safe because:** semantic facets are fixed without claiming universal independent entity identity.  
**Reopening trigger:** persistence cannot preserve response/Actual/history/interval semantics under direct/qualified modeling.  
**Rerun:** CORE-06, CORE-10, CORE-13, XCON-01, XCON-04.

```text
REOPEN                         0
unclassified material items    0
```

---

# 11. Relationship v0 regression

The second major relation-family stress does **not** reopen Relationship v0.

```text
simple case
Event --expected_participant--> Person

rich planned/response case
Event
  ↕
specific qualified Participation context
  ↕
Person

actual case
Event Actual
  ↕
actor-scoped Actual Participation
  ↕
Person
```

A future logical model may group planned/response and Actual facets into one aggregate/record only if it preserves their independent semantics and history.

No universal Relationship/Participant/Participation root is justified.

---

# 12. Final verdict

```text
PARTICIPATION FAMILY
PASS WITH HARDENING

Participation
✅ canonical specific semantic relation family
✅ intended/response and Actual facets remain distinct
✅ direct/simple or specifically qualified/rich form
❌ not native entity/root
❌ not universal membership/social graph

Participant
✅ contextual role
❌ entity/root

Invitation
✅ participation proposal/request semantics
❌ standalone universal primitive

Participation Response
✅ actor-scoped intended/response state
❌ Actual participation

Attendance
✅ Event-facing Actual Participation semantics
❌ standalone universal primitive
```

**Structural reopenings:** 0.  
**Unclassified material dependencies:** 0.

---

# 13. Documentation propagation

Required current propagation:

- [x] `concepts/participation.md`
- [x] this checkpoint
- [ ] `concepts/event.md`
- [ ] `concepts/session.md`
- [ ] `concepts/actual.md`
- [ ] `concepts/actor.md`
- [ ] `concepts/responsibility.md`
- [ ] `concepts/resource.md`
- [ ] `language-map.md`
- [ ] `README.md`
- [ ] `workstreams/domain-model.md`

No `participant.md`, `invitation.md`, or `attendance.md` is justified by this review.

---

# 14. Next-stage implication

After propagation, re-score remaining Relationships / Reasoning dependencies rather than following roadmap order.

Responsibility and Participation now both expose unresolved common-ground and governance boundaries. Authority / Visibility / Acceptance-Acknowledgement therefore gain leverage, but none is pre-selected by this checkpoint.