<!-- LIFEOS-CANONICAL-SPLIT document="participation.md" part="3" total="3" -->
> **Canonical document split — Part 3 of 3.** Parts 1–3 together form one authoritative document; this is a physical split only, not a summary/reference hierarchy. The payload preserves the full pre-compaction baseline first and later downstream amendments in sequence; later explicit amendments override stale status/deferral wording without deleting the earlier rationale. Navigation: [Part 1](participation.md) · [Part 2](participation-part-2.md) · **Part 3**

<!-- LIFEOS-CANONICAL-PAYLOAD -->
# 31. Deliberately deferred questions

- generic Acceptance/Acknowledgement relationship to participation response;
- on-behalf-of/delegated response semantics;
- participant role taxonomy;
- collective/group participation;
- recurring-series participation inheritance/override;
- exact evidence/authority threshold for established Actual Participation;
- retention/deletion/privacy lifecycle;
- exact qualified Participation identity/cardinality/persistence;
- specialist interaction/encounter extensions;
- final API/SQL representation.

Authority and Visibility are no longer deferred at the semantic-boundary level; their detailed policy/enforcement/persistence remains separately owned.

---

# 32. Reopening triggers

Reopen Participation v0 if later evidence shows that:

1. intended/response and Actual involvement cannot remain distinct without a materially different model;
2. generic Acceptance/Acknowledgement semantics require response to move outside Participation entirely;
3. Authority/Visibility cannot remain external to Participation;
4. collective/group participation requires native identity semantics that change the relation family;
5. Event/Session/Actual integration cannot preserve actor-scoped intervals without duplication;
6. provider reconciliation consistently requires a different truth model;
7. logical persistence cannot represent simple/direct and rich/qualified cases without contradiction.

Until stronger evidence appears, Participation remains the current accepted **specific semantic relation family** for intended and actual involvement, with their histories kept distinct.

---

# 2026-08-13/14 — Downstream current-state consolidation amendment

This amendment is part of the same canonical document. It preserves downstream current-state sections without deleting the full pre-compaction baseline above. A current section is retained in full whenever it contains material text not already present verbatim in the baseline, so heading/list/example context is preserved. Where a later status, closure, or repository-state statement conflicts with an earlier one, the later amendment is authoritative; earlier rationale, examples, rejected alternatives, tests, and boundary detail remain preserved unless explicitly superseded.

## 7. Attendance
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


## 14. Participation versus Authority and Visibility
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


## 16. Actual Participation evidence and epistemic integrity
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


## 17. Epistemic distinctions
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


## 18. Partial and interval participation
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


## 22. AI boundary
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


## 23. Simple UI versus kernel semantics
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


## 24. External benchmark synthesis
External systems are benchmark evidence only.

Useful recurring patterns include iCalendar separating attendee identity/participation status/role/RSVP/delegation; calendar APIs separating organizer from attendee response; meeting platforms maintaining attendance telemetry separately; specialist systems separating planned participation from actual encounter participation; and large-scale calendars exposing incomplete propagation.

LifeOS adapts the recurring separation of **expected participation, response, and actual involvement** without importing provider-specific enums or treating provider attendance as unquestioned truth.

---


## 25. Adversarial reductio summary
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


## 27. Relationship v0 compatibility
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


## 28. Persistence/API implications — deliberately not physical design
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


## 29. Adjacent Dependency Sweep
### RESOLVED NOW
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

### SAFE DEFERRED
#### Acceptance / Acknowledgement
**Owner:** Relationships / Reasoning — collaboration-state review.  
**Why safe:** Participation response is bounded without equating it with generic Acceptance/Acknowledgement across domains.  
**Reopening trigger:** invitation/response cannot compose with future common-ground model without changing Participation meaning.  
**Tests to rerun:** CORE-02, CORE-04, MA-05, MA-11, XCON-04, XCON-05.

#### Participant role taxonomy
**Owner:** product/specialist relationship review.  
**Why safe:** specific roles may coexist without one universal enum.  
**Reopening trigger:** ordinary cross-domain workflows require stable shared role ontology changing Participation boundaries.  
**Tests to rerun:** CORE-03, CORE-04, CORE-12, XCON-04, XCON-06.

#### Group / collective invitation or participation
**Owner:** collective/group actor review.  
**Why safe:** current native-referent semantics do not require inventing Team identity.  
**Reopening trigger:** common workflows require one collective Participation identity not decomposable into referents.  
**Tests to rerun:** CORE-04, CORE-06, MA-01, MA-03, XCON-01, XCON-04.

#### Delegation / on-behalf-of
**Owner:** Principal/Authority/delegation review.  
**Why safe:** participant identity and response Actor already separated.  
**Reopening trigger:** response Provenance/agency cannot be represented without changing Participation.  
**Tests to rerun:** MA-01, MA-06, MA-10, MA-13, MA-17, XCON-02.

#### Recurring-series Participation
**Owner:** Recurrence + logical model.  
**Why safe:** series baseline and occurrence override semantics preserved conceptually.  
**Reopening trigger:** occurrence-specific Participation cannot override series expectations without identity/history loss.  
**Tests to rerun:** CORE-02, XCON-03, XCON-04, CL-02, CL-06.

#### Provider attendance reconciliation / evidence threshold
**Owner:** Provenance/Authority/Decision + Integration logical model.  
**Why safe:** telemetry explicitly Evidence, not automatic canonical Participation.  
**Reopening trigger:** provider facts cannot establish/correct Actual Participation without altering Participation semantics.  
**Tests to rerun:** CORE-09, MA-10, MA-12, XCON-03, XCON-05.

#### Retention / deletion
**Owner:** privacy/retention review.  
**Why safe:** Participation Visibility and history already separable.  
**Reopening trigger:** deletion/revocation requires per-user duplicate reality or destructive history rewrite.  
**Tests to rerun:** MA-07, MA-08, MA-11, XCON-05.

#### Exact qualified Participation identity / persistence
**Owner:** logical data model.  
**Why safe:** semantic facets fixed without pre-approving table/entity identity.  
**Reopening trigger:** persistence cannot preserve response/Actual/history/interval semantics under direct/qualified modeling.  
**Tests to rerun:** CORE-06, CORE-10, CORE-13, XCON-01, XCON-04.

```text
REOPEN                         0
unclassified material items    0
```

---


## 30. Rejected alternatives
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


## 31. Deliberately deferred questions
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


## 32. Reopening triggers
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


## 2026-08-12 — Acknowledgement / generic Acceptance closure amendment
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


## 2026-08-13 — Representation / on-behalf-of downstream closure
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

---


## 2026-08-13 — Version / Material-State downstream closure
Version / Material-State v0 resolves Participation's material response-state dependency without turning `accepted` into a generic Acceptance concept.

A Participation response remains bound to the materially relevant invitation / occurrence / shared-event state it actually concerned:

```text
Participation response R1 = accepted for Event state S1
Event materially changes to S2
→ R1 remains historical response to S1
→ R1 does not silently become response to S2
```

Whether a later state is materially equivalent for Participation is owned by Participation/product policy. For example, a harmless title correction may leave the response applicable, while a material time/location/role change may require renewed stance. Technical row/provider/ETag/hash changes do not decide this by themselves.

Series/occurrence scope is also preserved:

```text
series response != one occurrence response
occurrence state change != automatic series policy rewrite
```

Canonical separation:

```text
Version != Participation
Version != Participation response
material equivalence != willingness/intention
same Event identity != automatic response carry-forward
```

Remaining SAFE DEFERRED Participation dependencies include participant role taxonomy, collective/group participation, exact recurring-series inheritance/override persistence, provider attendance evidence threshold/reconciliation, retention/deletion, exact qualified persistence and specialist extensions.

AI may detect that a response is stale after a material change but must not infer renewed human acceptance/decline.

No Participation hardening failed. **Participation remains PASS WITH HARDENING, REOPEN = 0**.

Normative downstream references:

- `version.md`;
- `../checkpoints/version-material-equivalence-v0-validation.md`.

---

# 2026-08-15 — Proposal / Request downstream closure amendment

Proposal / Request v0 makes explicit the invitation/proposal boundary already anticipated by Participation without changing Participation semantics.

Canonical decomposition:

```text
Participation invitation / request
!= delivery / view
!= Acknowledgement
!= Participation response
!= Agreement / Consent / Decision
!= Actual Participation
```

An invitation is a Request and/or Proposal applied to Participation context depending on whether it asks the recipient to act/respond, proposes a candidate participation state/terms, or both. This does **not** create a universal Invitation entity or a generic Acceptance state.

A response such as `going`, `maybe`, or `declined` remains Participation-specific response semantics. Silence remains neither acceptance nor rejection. A material change to event time/location/role may require a new Proposal or Request and does not silently inherit the previous response.

Where an Actor responds on behalf of another participant, Representation preserves the actual response Actor and represented party. Account membership is not required.

Downstream classification:

```text
Participation ↔ Proposal / Request      RESOLVED
Invitation universal primitive          REJECTED
generic Acceptance / Response root      REJECTED
Proposal / Request = Participation      REJECTED
Proposal / Request = Actual attendance  REJECTED
```

Collective/group participation, role taxonomy, recurring-series inheritance, provider evidence threshold, retention and physical representation remain separately owned dependencies.

No Participation hardening failed. **Participation remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `proposal.md`;
- `request.md`;
- `../checkpoints/proposal-request-v0-validation.md`.
