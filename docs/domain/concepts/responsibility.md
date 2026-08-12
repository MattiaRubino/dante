# Responsibility v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-12  
**Meaning of accepted:** best current decision; reopenable with stronger evidence  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Relationships / Reasoning

## Canonical definition

> **Responsibility is the contextual semantic relation family through which an eligible native referent is accountable for ensuring that a bounded commitment is appropriately handled. Responsibility does not create referent identity and does not by itself imply requester status, expected or actual performance, Participation, Resource eligibility, Authority, Visibility, Acknowledgement, ownership, custody, or coordination Stewardship.**

Responsibility answers:

> **Who is accountable for ensuring this bounded commitment is appropriately handled?**

Responsibility is a **specific semantic relation family**, not a native entity/root and not a universal assignment/workflow object.

---

# 1. Why Responsibility exists

LifeOS must preserve accountability independently from request, expected execution and Actual execution.

Representative case:

```text
Activity
Repair laptop

requester = Mattia
responsible Actor = IT team / Anna
expected performer = technician
actual performer = Luca
```

Those roles may coincide in a simple personal case, but coincidence is not ontology.

Without Responsibility semantics the model tends to overload `assigned_to`, confuse accountability with performance, or rewrite Activity identity when responsibility changes.

---

# 2. Responsibility is contextual role/relation semantics

A Person/Actor does not become a separate native `Responsible` entity.

```text
Person Anna
   ↓ Responsibility role
Activity / commitment C17
```

A non-LifeOS Person may bear Responsibility where real-world semantics require it.

Exact eligible non-human/collective referents remain separately reviewable.

---

# 3. Responsibility versus requester

```text
requester != responsible Actor
```

The person who asks for work may not be accountable for ensuring it is handled.

Likewise the responsible actor may not have originated the commitment.

---

# 4. Responsibility versus expected and actual performer

```text
Responsibility != expected performer
Responsibility != actual performer
```

A responsible actor may ensure work is handled by someone else.

A performer may execute work without inheriting broader accountability.

Responsibility changes therefore do not automatically change Activity identity.

---

# 5. Responsibility versus Participation and Resource

```text
Responsibility != Participation
Responsibility != Resource
```

Involvement is not accountability. Eligibility/capability/bookability is not accountability.

A Person can be Resource-eligible and not responsible; a responsible actor may never participate in the eventual execution episode.

---

# 6. Responsibility versus Authority

Responsibility grants no automatic governance power.

```text
responsible Actor
!= Authority holder
```

An Authority holder may reassign Responsibility without becoming responsible for execution.

Authority v0 owns governance/effect semantics.

---

# 7. Responsibility versus Visibility

Responsibility does not grant access to every related private fact, source, participant, Observation, Provenance record, or reason for unavailability.

```text
Responsibility != Visibility
```

A product/policy may expose the bounded information needed to act, but accountability and exposure remain independent.

---

# 8. Responsibility versus ownership / possession / custody

```text
owner != responsible Actor
holder != responsible Actor
custodian != responsible Actor
```

Example:

```text
Asset laptop
owner = Company
holder = Mattia
maintenance Responsibility = IT
repair coordinator = Anna
actual repair performer = Technician
```

No relation is inferred automatically from another.

---

# 9. Responsibility versus coordination Stewardship

Coordination Stewardship covers anticipating, remembering, monitoring, reminding, coordinating and repairing the process around a commitment.

```text
Responsibility != coordination Stewardship
Assignment != Stewardship transfer
```

The semantic distinction is accepted. Standalone Stewardship primitive status remains SAFE DEFERRED until concrete workflows prove independent persistent identity/state/query value.

---

# 10. Explicitly open/unassigned versus unknown

```text
UNKNOWN
!=
EXPLICITLY OPEN / UNASSIGNED
```

An intentionally claimable responsibility is not the same as missing information.

A future physical model must not use one ambiguous null to erase that difference.

---

# 11. Assignment

`Assignment` is a role-specific establishment/change operation, not a standalone universal primitive.

Examples:

```text
assign Responsibility to Anna
assign expected performer to Luca
assign reviewer to Marco
```

> **Every material assignment must name the semantic role being assigned.**

Whether the operation becomes effective immediately depends on the applicable role semantics, policy, Authority and any required response/common-ground conditions.

---

# 12. Claim

`Claim` is a self-initiated role-acquisition operation, not a standalone universal primitive.

```text
open Responsibility
→ Anna claims Responsibility
```

Claim must name the role. Whether the claim becomes effective immediately is context/policy/Authority dependent.

---

# 13. Hand-off

`Hand-off` is a role-specific transfer workflow, not a standalone universal primitive.

A transfer may concern Responsibility, expected performance, Stewardship, Authority or another role; transferring one must not silently transfer the others.

Current common-ground decomposition after Acknowledgement v0:

```text
hand-off requested
!= delivered/read
!= Acknowledgement
!= role-specific accepted response
!= authoritative/effective transfer
!= Actual performer later
```

Canonical rules:

- hand-off request != effective transfer;
- Acknowledgement != acceptance of Responsibility;
- role-specific acceptance != effective transfer automatically;
- generic cross-domain Acceptance is not a kernel primitive;
- effect remains governed by applicable Authority/policy/decision semantics.

---

# 14. Acknowledgement boundary

Acknowledgement records explicit taking-notice of a specific hand-off/request/change.

Responsibility records accountability.

```text
Acknowledgement != Responsibility
```

Example:

```text
Anna: "I got the hand-off request."
```

may coexist with:

```text
Anna has not accepted the role
Responsibility still belongs to Luca
```

Acknowledgement is now a canonical neighboring concept; the earlier generic common-ground dependency is closed at the semantic-boundary level.

---

# 15. History and effective Responsibility

Responsibility may change over time without rewriting the commitment.

```text
T0 Luca responsible
T1 transfer requested to Anna
T2 Anna acknowledges
T3 Anna gives role-specific positive response
T4 applicable Authority/policy makes transfer effective
T5 Anna responsible
T6 actual performer later = Marco
```

Required historical queries include:

- who was responsible then?;
- what transfer/request/response occurred?;
- when did current Responsibility become effective?;
- who actually performed?;
- what was corrected later?

Current state must not erase material historical attribution.

---

# 16. Multi-actor and unequal-power semantics

Responsibility must support:

- non-LifeOS Persons;
- open/claimable responsibility;
- reassignment and temporary substitution;
- hand-off with explicit common-ground states where consequence warrants;
- asymmetric Authority;
- Responsibility without Participation and vice versa;
- historical attribution after Account/access changes;
- conflict/dispute about who is responsible;
- care/guardian/manager contexts without assuming every assignment is voluntary.

Acceptance cannot be universal because some responsibility changes are voluntary, some authoritative, some policy-derived, and some require multiple stages.

---

# 17. AI boundary

AI may propose assignment, reassignment, claim candidates or hand-off actions.

AI must not silently:

- establish Responsibility from inference alone;
- turn Acknowledgement into acceptance;
- turn a role-specific response into effective transfer without applicable Authority/policy;
- gain assignment/transfer Authority merely because it can act;
- treat actual performance as proof of historical Responsibility;
- disclose private context merely because Responsibility exists.

> **AI proposal/ability does not manufacture Responsibility, Acknowledgement, Authority, or effective transfer.**

---

# 18. Product / UI language

Typical UI may use:

```text
Responsible
Assigned to
Who's handling this?
I'll take it
Claim
Hand off
Transfer
```

A low-consequence personal flow may collapse operation details. High-consequence workflows may expose request, Acknowledgement, role-specific response, approval/effect and history through progressive disclosure.

UI `Accept` or `I'll take it` does not create a generic Acceptance domain object.

---

# 19. Relationship-modeling implication

Responsibility follows Relationship v0 discipline.

```text
simple complete accountability relation
→ direct specific relation may suffice

material open/transfer/history/time/privacy/Authority semantics
→ specific qualified Responsibility context may be justified
```

Qualified relation != independent native entity automatically.

---

# 20. Core invariants

1. **Responsibility is contextual accountability relation semantics, not native identity/root.**
2. **Responsibility != requester.**
3. **Responsibility != expected performer.**
4. **Responsibility != actual performer.**
5. **Responsibility != Participation.**
6. **Responsibility != Resource.**
7. **Responsibility != Authority.**
8. **Responsibility != Visibility.**
9. **Responsibility != Acknowledgement.**
10. **Responsibility != ownership/custody/coordination Stewardship.**
11. **Unknown holder != explicitly open/unassigned.**
12. **Assignment/Claim/Hand-off must name the role.**
13. **Assignment/Claim/Hand-off are operations/workflows, not universal primitives.**
14. **Hand-off request != Acknowledgement != role-specific acceptance != effective transfer.**
15. **Generic cross-domain Acceptance is rejected; positive response remains role/workflow-specific.**
16. **Responsibility change does not change Activity identity by default.**
17. **Current Responsibility does not rewrite historical Responsibility.**
18. **Actual performer does not retroactively define Responsibility.**
19. **AI inference/proposal does not establish Responsibility or Authority.**
20. **Simple UI may hide structure without collapsing kernel distinctions.**

---

# 21. Adjacent Dependency Sweep

## RESOLVED

- Responsibility ↔ Activity: ordinary role change preserves Activity identity.
- Responsibility ↔ Actor/Person/Account: accountability role over native referent; Account not required.
- Responsibility ↔ expected performer: accountability != planned execution.
- Responsibility ↔ actual performer: accountability != Actual execution.
- Responsibility ↔ Resource: eligibility/capability != obligation.
- Responsibility ↔ Participation: involvement != accountability.
- Responsibility ↔ Authority: accountability != governance.
- Responsibility ↔ Visibility: accountability != exposure.
- Responsibility ↔ Assignment/Claim/Hand-off: role-specific operation/workflow semantics, not universal primitives.
- Responsibility ↔ Acknowledgement: taking notice != accountability.
- hand-off acceptance ↔ generic Acceptance: universal primitive rejected; positive response stays role-specific.
- Responsibility ↔ Stewardship semantic boundary: distinct; primitive status deferred.

## SAFE DEFERRED

### Decision / Approval / effective transfer mechanics

**Owner:** Decision/Reasoning review.  
**Why safe:** role response and Authority/effect are already separate from Responsibility identity.  
**Reopening trigger:** current/effective Responsibility cannot be reconstructed without making Responsibility itself a Decision record.  
**Tests to rerun:** CORE-02, CORE-04, CORE-09, MA-06, MA-12, XCON-03, XCON-04.

### Delegation / on-behalf-of

**Owner:** Principal/Authority/delegation review.  
**Why safe:** actor, represented party and Authority remain separate.  
**Reopening trigger:** delegated assignment/acceptance cannot preserve agency/Authority chain.  
**Tests to rerun:** MA-01, MA-06, MA-10, MA-13, MA-17, XCON-02.

### Version / Provenance / reconciliation

**Owner:** Version/Decision/logical model.  
**Why safe:** material history is required without choosing mechanics.  
**Reopening trigger:** responsibility history/correction cannot be reconstructed after conflict/change.  
**Tests to rerun:** CORE-02, CORE-05, CORE-09, MA-12, XCON-03, XCON-04.

### Coordination Stewardship primitive

**Owner:** Relationships / Reasoning + product workflow validation.  
**Why safe:** distinct semantics are protected without standalone identity.  
**Reopening trigger:** LifeOS must independently assign/transfer/query/measure coordination burden and cannot reconstruct it otherwise.  
**Tests to rerun:** CORE-03, CORE-04, CORE-12, MA-04, MA-15, XCON-04.

### Collective/joint Responsibility

**Owner:** collective/group/cardinality review.  
**Why safe:** multiple holders do not require a Group/root yet.  
**Reopening trigger:** ordinary workflows require a persistent collective responsibility identity with distinct lifecycle.  
**Tests to rerun:** CORE-04, CORE-06, MA-03, MA-19, XCON-01, XCON-04.

```text
REOPEN                         0
unclassified material items    0
```

---

# 22. Rejected alternatives

Rejected:

- universal Responsibility entity/root;
- responsibility = assignee/performer/requester;
- responsibility = participation/resource/authority/visibility/acknowledgement;
- universal Assignment primitive;
- universal Claim primitive;
- universal Hand-off primitive;
- generic Acceptance root controlling every assignment/transfer;
- ambiguous null meaning both unknown and intentionally open;
- assignment automatically effective in every context;
- assignment automatically voluntary in every context;
- actual performer retroactively defining accountability;
- task assignment automatically transferring coordination Stewardship.

---

# 23. Reopening triggers

Reopen Responsibility v0 if later evidence shows that:

1. accountability cannot remain distinct from expected/actual execution;
2. common-ground/Decision semantics require Responsibility itself to absorb Acknowledgement/response/effect;
3. Authority/Visibility cannot remain independent;
4. collective/joint Responsibility requires materially different native identity semantics;
5. Stewardship consistently requires integration into Responsibility rather than a separate relation/dimension;
6. logical persistence cannot preserve open/unknown/history/transfer semantics without contradiction.

Until then, Responsibility remains the current accepted **specific accountability relation family**.
