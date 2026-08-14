<!-- LIFEOS-CANONICAL-SPLIT document="responsibility.md" part="3" total="3" -->
> **Canonical document split — Part 3 of 3.** Parts 1–3 together form one authoritative document; this is a physical split only, not a summary/reference hierarchy. The payload preserves the full pre-compaction baseline first and later downstream amendments in sequence; later explicit amendments override stale status/deferral wording without deleting the earlier rationale. Navigation: [Part 1](responsibility.md) · [Part 2](responsibility-part-2.md) · **Part 3**

<!-- LIFEOS-CANONICAL-PAYLOAD -->
# 29. Rejected alternatives

Rejected:

- universal Responsibility entity/root;
- `assigned_to` as universal Responsibility truth;
- Responsibility = requester;
- Responsibility = expected performer;
- Responsibility = actual performer;
- Responsibility = Resource;
- Responsibility = Authority;
- Responsibility = Visibility;
- Responsibility = ownership/custody;
- Responsibility = coordination Stewardship;
- Assignment as standalone universal primitive;
- Claim as standalone universal primitive;
- Hand-off as standalone universal primitive;
- `NULL` as sufficient universal representation of both unknown and intentionally open/unassigned;
- hand-off request = effective transfer by default;
- assignment = Acceptance by default;
- Resource selection = Responsibility;
- actual performance = historical Responsibility;
- AI recommendation = effective Responsibility change.

---

# 30. Deliberately deferred questions

- Acceptance/Acknowledgement and exact proposal-response semantics;
- collective/group/joint accountability semantics;
- fallback/conditional/rotation policy;
- standalone coordination Stewardship primitive status;
- exact Version/Decision/Provenance representation of changes;
- exact qualified Responsibility identity/cardinality/persistence;
- specialist regulated-accountability extensions;
- final API/SQL shape.

Authority and Visibility are no longer deferred at the semantic-boundary level; their exact enforcement/persistence still belongs to later logical/security design.

---

# 31. Reopening triggers

Reopen Responsibility v0 if later evidence shows that:

1. accountability cannot remain distinct from expected/actual performer in ordinary workflows;
2. Authority/Acceptance modeling requires a materially different Responsibility definition;
3. open/unassigned and unknown cannot be represented without another stronger concept;
4. collective/joint accountability requires a common entity that changes Responsibility identity semantics;
5. coordination Stewardship consistently behaves as part of Responsibility rather than an independent semantic dimension;
6. logical persistence cannot support direct/simple and qualified/rich cases without contradictory behavior;
7. specialist-system requirements reveal that the current `ensure this is appropriately handled` boundary is too broad or too weak.

Until stronger evidence appears, Responsibility remains the current accepted **specific semantic relation family** with simple direct and richer qualified forms allowed according to consequence.

---

# 2026-08-12 — Participation v0 closure amendment

Participation v0 closes the Responsibility ↔ Participation boundary without changing Responsibility semantics.

Canonical distinction:

```text
Responsibility
= accountability to ensure a bounded commitment is appropriately handled

Participation
= expected/intended or Actual involvement in a bounded shared occurrence/interaction
```

Therefore:

```text
Responsibility != Participation
responsible Actor != Participant by default
Participation != expected performer
Participation != actual performer
```

A responsible Actor may not participate in the Event/interaction. A Participant may bear no Responsibility for the outcome. Actual attendance/involvement must not be used to rewrite historical Responsibility, and Responsibility must not be used to infer actual attendance.

Assignment/Claim/Hand-off remain role-specific: assigning Responsibility does not silently establish Participation, and changing Participation does not transfer Responsibility.

Both Responsibility and Participation continue to expose the same unresolved adjacent common-ground questions — Acceptance/Acknowledgement, delegation/on-behalf-of and reconciliation — but neither absorbs them.

See:

- `concepts/participation.md`;
- `checkpoints/participation-v0-validation.md`;
- `concepts/authority.md`;
- `concepts/visibility.md`.

---

# 2026-08-13/14 — Downstream current-state consolidation amendment

This amendment is part of the same canonical document. It preserves downstream current-state sections without deleting the full pre-compaction baseline above. A current section is retained in full whenever it contains material text not already present verbatim in the baseline, so heading/list/example context is preserved. Where a later status, closure, or repository-state statement conflicts with an earlier one, the later amendment is authoritative; earlier rationale, examples, rejected alternatives, tests, and boundary detail remain preserved unless explicitly superseded.

## 21. AI boundary
AI may suggest a responsible Actor, identify open work, propose reassignment, suggest fallback/substitution, detect mismatches between Responsibility and Resource availability, or summarize Responsibility history where authorized.

AI must not silently:

- establish Responsibility merely from inference;
- convert candidate eligibility into obligation;
- treat its own proposal as Acceptance;
- transfer Responsibility without required Authority/policy;
- infer Authority or Visibility from Responsibility;
- rewrite history to match actual performer;
- disclose private reasons used in a recommendation.

Canonical rule:

> **AI may propose Responsibility changes; proposal capability does not grant assignment/transfer Authority.**

Visibility v0 further hardens this: AI may use an authorized private basis to propose a change without being permitted to disclose that basis.

---


## 22. Simple UI versus kernel semantics
Ordinary UI can remain simple:

```text
Assigned to Anna
```

when product policy makes the meaning unambiguous.

Advanced/high-consequence workflows may expose Responsible, Requested by, Expected performer, Open/claimable, Transfer pending/history, Actual performer, coordination details, and Authority/acceptance basis.

The internal distinction must not force enterprise workflow language into casual personal use.

---


## 23. External benchmark synthesis
External systems are benchmark evidence only.

Useful recurring patterns include specialist systems distinguishing requester, owner/responsible party, requested performer and actual performer; task/work systems distinguishing candidates from assignee; claim/assignment as separate operations/events; unassigned work/history; and multiple assignees without proving one universal accountability model.

LifeOS keeps the stronger semantic distinctions while avoiding provider-specific state machines or a universal `assignee` field.

---


## 24. Adversarial reductio summary
```text
REMOVE Responsibility                         FAIL
Responsibility = expected performer           FAIL
Responsibility = actual performer             FAIL
Responsibility = Resource                     FAIL
Responsibility = Authority                    FAIL
Responsibility = Stewardship                  FAIL
Universal Assignment / Claim / Hand-off       FAIL
Responsibility as specific relation family    PASS WITH HARDENING
```

---


## 26. Relationship v0 compatibility
```text
simple Responsibility semantics
→ direct specific relation may suffice

materially rich/open/transfer/history semantics
→ specific qualified Responsibility relation/context may be justified

universal Relationship wrapper
→ still unnecessary
```

Responsibility confirms rather than reopens Relationship v0. No universal Responsibility table/entity is implied.

---


## 27. Persistence/API implications — deliberately not physical design
Future logical modeling must support, where justified:

- specific Responsibility holder reference to an eligible Actor/native identity;
- explicitly open/unassigned state distinct from unknown;
- expected performer separately from Responsibility;
- actual performer separately from planned/current Responsibility;
- role-specific assignment/claim/hand-off operations;
- material current/effective interval and history when consequence requires it;
- transfer proposal/acceptance/Authority basis where required;
- external/non-account Persons;
- selective visibility;
- conflicting assertions/reconciliation;
- optional direct simple representation versus richer qualified Responsibility context.

Do not infer one universal responsibilities table, assigned_to field, Assignment/Claim/HandOff/Stewardship entity, status enum, Acceptance for every assignment, Resource selection=Responsibility, actual performer=Responsibility, or automatic Authority/Visibility.

---


## 28. Adjacent Dependency Sweep
### RESOLVED NOW
- Responsibility ↔ Activity: ordinary role changes preserve Activity identity.
- Responsibility ↔ Actor/Person/Account: role over native referent; Account not required.
- Responsibility ↔ expected performer: accountability != planned execution.
- Responsibility ↔ actual performer: accountability != Actual execution.
- Responsibility ↔ Resource: eligibility/capability != obligation.
- Responsibility ↔ Assignment: role-specific establishment/change operation.
- Responsibility ↔ Claim: role-specific self-acquisition operation.
- Responsibility ↔ Hand-off: role-specific transfer workflow; request != effective transfer.
- Responsibility ↔ Stewardship boundary: distinct; primitive status deferred.
- Responsibility ↔ Authority: governance/effect power separately owned.
- Responsibility ↔ Visibility: exposure separately owned.

### SAFE DEFERRED
#### Acceptance / Acknowledgement
**Owner:** Relationships / Reasoning — collaboration-state review.  
**Why safe:** assignment/claim/hand-off effects are policy-dependent and not Confirmation.  
**Reopening trigger:** ordinary transfer cannot distinguish proposal/receipt/willingness/effective change without altering Responsibility.  
**Tests to rerun:** CORE-02, CORE-04, MA-03, MA-05, MA-11, XCON-04.

#### Provenance / Version / Decision / reconciliation
**Owner:** Relationships / Reasoning + logical model.  
**Why safe:** reconstructable history required without pre-deciding mechanics.  
**Reopening trigger:** effective/current Responsibility cannot be reconstructed after correction/conflict.  
**Tests to rerun:** CORE-02, CORE-05, CORE-09, MA-12, XCON-03, XCON-04.

#### Coordination Stewardship primitive
**Owner:** Relationships / Reasoning / product workflow validation.  
**Why safe:** distinction fixed, no current standalone identity/state requirement.  
**Reopening trigger:** LifeOS must explicitly assign/transfer/query/measure coordination burden independently.  
**Tests to rerun:** CORE-03, CORE-04, CORE-12, MA-04, MA-15, XCON-04.

#### Collective / joint Responsibility
**Owner:** collective/group/cardinality review.  
**Why safe:** multiple holders allowed without assuming joint/individual semantics.  
**Reopening trigger:** ordinary workflows require one collective Responsibility identity or group Actor.  
**Tests to rerun:** CORE-03, CORE-04, MA-03, MA-13, XCON-01, XCON-04.

#### Fallback / conditional Responsibility
**Owner:** Trigger/policy review.  
**Why safe:** fallback explicitly not current Responsibility.  
**Reopening trigger:** common fallback/rotation workflows require generic condition logic inside Responsibility.  
**Tests to rerun:** CORE-02, CORE-04, XCON-03, XCON-04.

#### Qualified Responsibility identity / physical representation
**Owner:** logical data model.  
**Why safe:** richer structure may be needed without universal independent identity.  
**Reopening trigger:** persistence cannot preserve open/current/history/query semantics.  
**Tests to rerun:** CORE-06, CORE-10, CORE-13, XCON-01, XCON-04.

```text
REOPEN                         0
unclassified material items    0
```

---


## 29. Rejected alternatives
Rejected:

- universal Responsibility entity/root;
- `assigned_to` as universal Responsibility truth;
- Responsibility = requester/expected performer/actual performer/Resource/Authority/Visibility/ownership/custody/Stewardship;
- Assignment/Claim/Hand-off as standalone universal primitives;
- one null meaning both unknown and intentionally open;
- hand-off request = effective transfer;
- assignment = Acceptance by default;
- Resource selection = Responsibility;
- actual performance = historical Responsibility;
- AI recommendation = effective Responsibility change.

---


## 30. Deliberately deferred questions
- Acceptance/Acknowledgement and exact proposal-response semantics;
- collective/group/joint accountability;
- fallback/conditional/rotation policy;
- standalone Stewardship primitive status;
- exact Version/Decision/Provenance representation;
- exact qualified Responsibility identity/cardinality/persistence;
- specialist regulated-accountability extensions;
- final API/SQL shape.

Authority and Visibility are no longer deferred at the semantic-boundary level; exact enforcement/persistence remains later logical/security design.

---


## 31. Reopening triggers
Reopen Responsibility v0 if later evidence shows that:

1. accountability cannot remain distinct from expected/actual performer;
2. Authority/Acceptance modeling requires a materially different Responsibility definition;
3. open/unassigned and unknown require a stronger concept;
4. collective/joint accountability changes Responsibility identity semantics;
5. Stewardship consistently behaves as part of Responsibility rather than independent dimension;
6. logical persistence cannot support direct/simple and qualified/rich cases;
7. specialist-system requirements show the current boundary too broad or weak.

Until stronger evidence appears, Responsibility remains the current accepted **specific semantic relation family** with simple direct and richer qualified forms allowed according to consequence.

---


## 2026-08-12 — Participation v0 closure amendment
Participation v0 closes the Responsibility ↔ Participation boundary without changing Responsibility semantics.

```text
Responsibility
= accountability to ensure a bounded commitment is appropriately handled

Participation
= expected/intended or Actual involvement in a bounded shared occurrence/interaction
```

Therefore:

```text
Responsibility != Participation
responsible Actor != Participant by default
Participation != expected performer
Participation != actual performer
```

A responsible Actor may not participate. A Participant may bear no Responsibility. Actual attendance must not rewrite historical Responsibility, and Responsibility must not infer attendance.

Assignment/Claim/Hand-off remain role-specific: assigning Responsibility does not silently establish Participation, and changing Participation does not transfer Responsibility.

Both concepts continue to expose common-ground/delegation/reconciliation dependencies without absorbing them.

---


## 2026-08-12 — Acknowledgement / generic Acceptance closure amendment
Acknowledgement v0 closes the common-ground dependency that Responsibility v0 intentionally left open.

Current transfer decomposition:

```text
hand-off requested
!= delivered/read/displayed
!= Acknowledgement
!= role-specific positive/accepted response
!= authoritative/effective Responsibility transfer
!= Actual performer later
```

Acknowledgement therefore records explicit taking-notice of the specific hand-off/request/change, not accountability and not willingness to take the role.

```text
Acknowledgement != Responsibility
Acknowledgement != role-specific acceptance
```

The joint common-ground review also rejected generic cross-domain `Acceptance` as a standalone kernel primitive. `Accept` / `I'll take it` in a Responsibility hand-off remains **Responsibility-specific response/operation semantics**. Whether the transfer becomes effective still depends on the applicable Authority/policy/Decision semantics.

The historical `Acceptance / Acknowledgement` SAFE DEFERRED item is now downstream-closed as:

```text
Responsibility ↔ Acknowledgement     RESOLVED
Responsibility ↔ generic Acceptance  RESOLVED — universal primitive rejected
```

Decision/Approval/effective-transfer mechanics, Principal/delegation/on-behalf-of, Version/Provenance/reconciliation, Stewardship, collective Responsibility and physical persistence remain separately owned dependencies. No Responsibility reopening is required.

---


## 2026-08-13 — Decision / Approval / effective-transfer closure amendment
Decision v0 closes the semantic Decision/effective-transfer portion of Responsibility's `Provenance / Version / Decision / reconciliation` deferral without changing Responsibility semantics.

Current transfer decomposition:

```text
hand-off requested
!= delivered/read/displayed
!= Acknowledgement
!= Responsibility-specific positive/accepted response
!= Approval / Decision where required
!= effective Responsibility transfer
!= later Actual performer
```

Canonical separation:

```text
Decision
= bounded resolution of the transfer/role-change question

Approval
= scoped Decision/review result whose significance depends on applicable Authority/policy

Responsibility
= current accountability relation state
```

Decision/Approval do not create Authority or Responsibility merely by existing. A Decision may reject a transfer and leave current Responsibility unchanged. Conversely, an already-authorized bounded policy may make a transfer effective without fabricating a new human Decision.

The affected Responsibility semantics own the effective transfer/current holder. No universal `EffectiveChange` object is introduced.

Downstream closure:

```text
Responsibility ↔ Decision                    RESOLVED
Responsibility ↔ Approval                    RESOLVED
Responsibility ↔ effective transfer          RESOLVED
Responsibility ↔ Reconciliation boundary     RESOLVED semantically
```

Version/Provenance mechanics, detailed reconciliation policy, Principal/delegation/on-behalf-of, Coordination Stewardship, collective/joint Responsibility, Trigger/fallback policy and physical persistence remain independently deferred.

**Responsibility v0 verdict is unchanged. REOPEN = 0.**

---


## 2026-08-13 — Version / Material-State downstream closure
Version / Material-State v0 resolves the state/version portion of Responsibility's historical `Provenance / Version / Decision / reconciliation` dependency without changing Responsibility semantics.

A role-specific request/response/Decision remains bound to the materially relevant Responsibility/hand-off state it actually concerned:

```text
hand-off request H1
scope: Responsibility for bounded commitment C
Anna accepts H1

later request H2 materially expands scope/duties
→ Anna's H1 response remains historical
→ H1 response does not silently accept H2
```

Likewise a current Responsibility holder state may change over time while prior holders, requests, responses and effective intervals remain reconstructible. The underlying Activity/commitment identity need not change merely because Responsibility state changes.

Materiality is role/scope specific. Technical row/provider/ETag/hash revisions do not decide whether a prior hand-off response or Approval still applies; same commitment identity does not guarantee carry-forward after material role/scope change.

Canonical separation:

```text
Version != Responsibility
Version != Assignment / Claim / Hand-off
Version != Decision / Authority / reconciliation
Version != Provenance
material-equivalent state != role acceptance by itself
```

Version identifies/reconstructs the state to which response/Decision applied; Responsibility still owns the current accountability relation; Provenance explains lineage; Decision/Authority/reconciliation govern applicable resolution/effect.

Remaining SAFE DEFERRED Responsibility dependencies include detailed source-precedence/reconciliation policy, Principal/delegation/on-behalf-of, Coordination Stewardship, collective/joint Responsibility, Trigger/fallback/rotation policy, qualified persistence/API and specialist accountability extensions.

AI may detect that a proposed hand-off/assignment has become stale after a material scope change but must not infer renewed human acceptance or silently transfer Responsibility.

No Responsibility hardening failed. **Responsibility remains PASS WITH HARDENING, REOPEN = 0**.

Normative downstream references:

- `version.md`;
- `../checkpoints/version-material-equivalence-v0-validation.md`.

