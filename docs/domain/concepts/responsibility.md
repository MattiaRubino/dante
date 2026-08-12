# Responsibility v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-12  
**Meaning of accepted:** best current decision; reopenable with stronger evidence  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Relationships / Reasoning

## Canonical definition

> **Responsibility is the contextual semantic relation through which an eligible Actor bears the obligation/accountability to ensure that a bounded commitment is appropriately handled within a defined scope and context. Responsibility is independent of who requested the commitment, who is expected to perform it, who actually performs it, who coordinates it, who has Authority over it, and who may view it.**

Responsibility answers the bounded question:

> **Who is accountable for ensuring this commitment is appropriately handled in this context?**

It does not answer, by itself:

- who requested the commitment;
- who is operationally eligible to perform it;
- who is expected/planned to perform it;
- who actually performed it;
- who coordinates/reminds/monitors it;
- who may assign or transfer it;
- who has canonical-change Authority;
- who may view the commitment or relationship;
- whether a proposed transfer has been accepted;
- whether the underlying Activity/Event/commitment actually occurred.

Responsibility is therefore a **specific semantic relation family**, not a universal entity/root and not a synonym for `assignee`.

---

# 1. Why Responsibility exists

LifeOS already needs to preserve the identity of a commitment while the people around it change.

Representative case:

```text
Activity
Pick up prescription

requested_by
Maria

responsible
Anna

expected_performer
Luca

actual_performer
Marco
```

All of these may be true simultaneously.

Without distinct Responsibility semantics, the model tends toward weak alternatives:

1. one `assigned_to` field that mixes accountability and expected execution;
2. current Account/User implicitly treated as responsible;
3. actual performer overwriting planned/responsible actor;
4. transfer request treated as immediate transfer;
5. Resource eligibility treated as obligation;
6. ownership or Authority treated as automatic responsibility;
7. assignment treated as proof that coordination burden transferred;
8. `NULL assignee` used ambiguously for both unknown and intentionally open work.

The semantic need is real even though a universal Responsibility entity is not required for every simple case.

---

# 2. Responsibility is contextual, not native identity

Responsibility does not create a second identity for the responsible Actor or target.

```text
Person Anna
        ↓ responsible-for
Activity A17
```

Anna retains Person identity and Actor semantics.

The Activity retains Activity identity.

Ordinary reassignment or transfer changes the relationship, not the underlying Activity or Person identity.

Canonical rule:

> **Responsibility attaches accountability to an existing bounded commitment/context; it does not define the identity of the target or the holder.**

A simple case may be expressible as a direct specific relation. A richer case may require a qualified Responsibility context when the relationship itself has material state/history/scope.

---

# 3. Responsibility versus requester

Requester answers approximately:

> Who asked for this commitment/action?

Responsibility answers:

> Who must ensure it is appropriately handled?

These may coincide but are not equivalent.

```text
Manager requests report
Analyst responsible
```

```text
Parent requests pickup
Sibling responsible
```

Therefore:

```text
requester != responsible Actor
```

Requesting work does not automatically establish Responsibility unless the governing product/policy semantics explicitly do so.

---

# 4. Responsibility versus expected performer

Expected performer answers:

> Who is intended/planned to execute the work?

Responsibility answers:

> Who must ensure the commitment is appropriately handled?

Example:

```text
Manager responsible
Analyst expected performer
```

The responsible Actor may delegate execution while retaining accountability.

Therefore:

```text
Responsibility != expected performer
```

A simple personal task may collapse these roles in UI, but the kernel must not equate them universally.

---

# 5. Responsibility versus actual performer

Actual performer answers:

> Who actually executed the work?

Responsibility answers:

> Who bore accountability for ensuring it was handled?

Example:

```text
Responsible
Anna

Expected performer
Luca

Actual performer
Marco
```

Possible because Luca was unavailable and Marco substituted.

Therefore:

```text
Responsibility != actual performer
expected performer != actual performer
```

Actual execution must not rewrite historical Responsibility to make the eventual performer appear responsible all along.

---

# 6. Responsibility versus Actor

Actor is the contextual agency category/capability of the referent/system.

Responsibility is one specific semantic relationship that an eligible Actor may bear.

```text
Actor != Responsibility
```

The specific-role precedence rule remains:

```text
responsible_for
performed_by
recorded_by
confirmed_by
requested_by
```

are stronger than a generic `actor` edge when those meanings are known.

Responsibility does not turn Actor into an entity/root.

---

# 7. Responsibility versus Resource

Resource answers:

> What could satisfy this execution need?

Responsibility answers:

> Who is accountable for ensuring the commitment is handled?

A Person may be Resource-eligible without being responsible.

A responsible Actor may be unavailable or lack the capability to perform the work personally.

Therefore:

```text
Resource eligibility != obligation/accountability
Responsibility != Resource
```

This boundary prevents candidate selection and responsibility assignment from collapsing into one planner field.

---

# 8. Responsibility versus Authority

Responsibility does not grant the right to assign, override, disclose, approve, delete, or establish canonical state.

```text
responsible Actor
!= Authority holder
```

Likewise, an Authority holder may reassign a commitment without becoming responsible for it.

Example:

```text
Manager
has Authority to reassign

Employee
currently responsible
```

Exact Authority scope, delegation and policy semantics remain a separate Relationships / Reasoning review.

Canonical rule:

> **Responsibility never manufactures Authority by itself.**

---

# 9. Responsibility versus Visibility

Being responsible does not automatically grant access to every related private fact, source, participant, Observation, Provenance record, or reason for unavailability.

Likewise, being able to view a commitment does not establish Responsibility.

```text
Responsibility != Visibility
```

Future policy may grant minimum access needed to perform a role, but that is an Authority/Visibility rule, not intrinsic Responsibility semantics.

---

# 10. Responsibility versus ownership / possession / custody

Ownership, possession, custody and responsibility answer different questions.

Example:

```text
Asset laptop
owner = Company
holder = Mattia
maintenance responsibility = IT
repair coordinator = Anna
actual repair performer = Technician
```

No relation is inferred automatically from another.

Therefore:

```text
owner != responsible Actor
holder != responsible Actor
custodian != responsible Actor
```

---

# 11. Responsibility versus coordination Stewardship

Coordination Stewardship covers the distinct burden of anticipating, remembering, monitoring, reminding, coordinating, and repairing the process around a commitment.

Example:

```text
Child
responsible for taking recycling out

Parent
remembers deadline
monitors completion
reminds child
repairs failure
```

The parent may carry coordination burden without being the current Responsibility holder for execution.

Therefore:

```text
Responsibility != coordination Stewardship
Assignment != Stewardship transfer
```

The semantic distinction is accepted. A standalone Stewardship primitive is **not** accepted yet.

Stewardship remains SAFE DEFERRED until concrete LifeOS workflows prove that it must be explicitly assigned/transferred/queried as independent domain state rather than represented through actions, provenance, product state or another smaller model.

---

# 12. Explicitly open / unassigned versus unknown

This is a canonical epistemic distinction.

```text
UNKNOWN
!=
EXPLICITLY OPEN / UNASSIGNED
```

Examples:

```text
Activity
Take recycling out

responsibility intentionally open
someone eligible may claim
```

is not equivalent to:

```text
Activity imported from external system
responsible Actor unknown
```

Therefore a future logical representation must not use one ambiguous `NULL responsible_id` to mean both conditions without another semantic discriminator.

Canonical rule:

> **Absence of a known current holder is not evidence that the commitment is intentionally open, and intentional openness is not missing information.**

---

# 13. Assignment

`Assignment` is not accepted as a standalone universal kernel primitive.

Assignment is an operation/process through which an Actor is nominated or established for a **specific named role**.

Examples:

```text
assign Responsibility to Anna
```

```text
assign expected performer to Luca
```

```text
assign reviewer to Marco
```

The noun `Assignment` alone is semantically incomplete because it does not identify which role is being changed.

Canonical rule:

> **Every material assignment must identify the semantic role being assigned.**

Whether assignment immediately makes the role effective depends on the governing Authority, policy and acceptance semantics.

Therefore neither rule is universal:

```text
Assignment always requires Acceptance
```

nor:

```text
Assignment always makes Responsibility effective immediately
```

---

# 14. Claim

`Claim` is not accepted as a standalone universal kernel primitive.

A Claim is a self-initiated attempt/action by an Actor to acquire a specific role.

Example:

```text
open household chore
Luca: "I'll take it"
```

In a low-consequence household policy, Claim may also constitute acceptance and immediately establish Responsibility.

In a formal workflow, Claim may only nominate the Actor pending approval/acceptance.

Canonical rule:

> **Claim expresses self-initiated role acquisition intent/action; whether it establishes the role is policy-dependent.**

`Claim` must therefore name the role being claimed rather than becoming a generic relationship object.

---

# 15. Hand-off

`Hand-off` is not accepted as a standalone universal kernel primitive.

Hand-off is a transfer workflow/pattern around a **specific semantic role**.

Representative chronology:

```text
T0
Luca responsible

T1
Luca requests transfer to Anna

T2
Anna has not responded

T3
Anna accepts / valid Authority establishes transfer

T4
Luca responsibility ends
Anna responsibility begins
```

At T2:

```text
Anna is not automatically responsible
Luca is not automatically no longer responsible
```

Canonical rule:

> **Hand-off request != effective role transfer unless the applicable policy/Authority/acceptance basis makes it effective.**

A different context may allow an authoritative coordinator to make the transfer effective immediately. Therefore LifeOS must preserve the distinction without imposing one universal state machine.

Hand-off must identify what is transferred:

```text
Responsibility
expected performer role
Stewardship
Authority
another specific role
```

Never infer a transfer of all roles/rights merely because one role moved.

---

# 16. Responsibility chronology and historical integrity

Material changes must remain reconstructable where the workflow requires history.

Example:

```text
T0 Anna responsible
T1 transfer requested to Luca
T2 Luca declines
T3 Anna remains responsible
T4 Marco assigned by authorized manager
T5 Marco responsible
T6 Luca actually performs as substitute
```

The current state must not erase:

- previous Responsibility holders;
- rejected/pending transfer where material;
- the policy/Authority basis for effective change where material;
- the difference between current responsibility and actual performance.

Exact Version/Decision/Provenance mechanics remain deferred, but Responsibility semantics must not permit silent history rewriting.

---

# 17. Multiple / joint responsibility

More than one Actor may be associated with responsibility semantics in some workflows.

However:

```text
A responsible
+
B responsible
```

may mean either:

```text
A and B each independently accountable
```

or:

```text
A+B jointly/collectively accountable as one responsibility context
```

These meanings are not automatically equivalent.

Exact collective/joint cardinality and possible Group/collective-Actor semantics remain SAFE DEFERRED.

Do not invent a universal Team entity solely to resolve this case.

---

# 18. Fallback / conditional responsibility

A fallback Actor is not the current Responsibility holder merely because they may become responsible later.

```text
Luca current responsible
Anna fallback if Luca unavailable
```

Therefore:

```text
fallback responsibility != current responsibility
```

Conditional/fallback activation belongs to future Trigger/policy semantics when concrete workflows require it.

---

# 19. Personal-first defaults

A personal task such as:

```text
Buy milk
```

must not force users to see or configure Responsibility machinery.

A product may apply a simple default policy in a personal context, for example treating the creator/current person as responsible when that policy is semantically appropriate.

But the kernel must not encode:

```text
responsible = current_account.person
```

as universal truth.

A default must remain policy/product behavior rather than identity coincidence.

---

# 20. Multi-actor implications

Responsibility must support:

- a Person with no LifeOS Account being responsible;
- current Account deletion/revocation without erasing historical Responsibility attribution;
- separate requester/responsible/expected performer/actual performer;
- open/claimable work;
- pending/refused transfer;
- temporary substitution;
- asymmetric authority contexts;
- conflicting assertions about who was responsible;
- actor-specific visibility without per-actor copies of the underlying commitment.

A shared Activity remains one Activity while Responsibility changes.

Conflicting assertions may remain unresolved until a future Authority/Decision/reconciliation policy establishes the current interpretation.

---

# 21. AI boundary

AI may:

- suggest a responsible Actor;
- identify open work;
- propose reassignment;
- suggest fallback/substitution;
- detect mismatches between Responsibility and Resource availability;
- summarize Responsibility history where authorized.

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

---

# 22. Simple UI versus kernel semantics

Ordinary UI can remain simple:

```text
Assigned to Anna
```

when product policy makes the meaning unambiguous.

Advanced/high-consequence workflows may expose:

- Responsible;
- Requested by;
- Expected performer;
- Open / available to claim;
- Transfer pending;
- Transfer history;
- Actual performer;
- coordination details;
- authority/acceptance basis.

The internal distinction must not force enterprise workflow language into casual personal use.

---

# 23. External benchmark synthesis

External systems are benchmark evidence only.

Useful recurring patterns include:

- specialist workflow systems distinguishing requester, owner/responsible party, requested performer and actual performer;
- task/work systems distinguishing candidates from assignee;
- some systems preserving claim/assignment as separate operations/events;
- issue/task products supporting unassigned work and assignment history;
- products allowing several assignees without thereby defining one universal accountability model.

LifeOS keeps the stronger semantic distinctions while avoiding provider-specific state machines or a universal `assignee` field.

---

# 24. Adversarial reductio summary

## REMOVE Responsibility semantics

Accountability collapses into assignee/performer/requester fields and transfer/open work cannot be represented truthfully.

**Result:** FAIL.

## Responsibility = expected performer

Delegated execution and manager/accountability cases fail.

**Result:** FAIL.

## Responsibility = actual performer

Substitution and historical accountability fail.

**Result:** FAIL.

## Responsibility = Resource

Eligibility/capability becomes obligation.

**Result:** FAIL.

## Responsibility = Authority

Accountability becomes permission/governance.

**Result:** FAIL.

## Responsibility = Stewardship

Execution accountability and coordination/mental-load burden collapse.

**Result:** FAIL.

## Universal Assignment / Claim / Hand-off entities

The operations lack meaning without the specific role they act upon and create redundant generic workflow objects.

**Result:** FAIL.

## Responsibility as specific relation family

Simple cases stay direct; rich/open/transfer/history cases may use a specific qualified Responsibility context.

**Result:** PASS WITH HARDENING.

---

# 25. Core invariants

1. **Responsibility is a contextual semantic relation family, not a native entity/root.**
2. **Responsibility answers who is accountable for ensuring a bounded commitment is appropriately handled.**
3. **Responsibility != requester.**
4. **Responsibility != expected performer.**
5. **Responsibility != actual performer.**
6. **Responsibility != Resource eligibility.**
7. **Responsibility != Actor identity/category.**
8. **Responsibility != Authority.**
9. **Responsibility != Visibility.**
10. **Responsibility != ownership/possession/custody.**
11. **Responsibility != coordination Stewardship.**
12. **Unknown holder != explicitly open/unassigned.**
13. **Assignment is a role-specific establishment/change operation, not a universal primitive.**
14. **Claim is a self-initiated role-acquisition operation whose effect is policy-dependent.**
15. **Hand-off is a role-specific transfer workflow; request != effective transfer by default.**
16. **Every Assignment/Claim/Hand-off must identify the semantic role being changed.**
17. **Assignment does not universally require Acceptance and does not universally establish Responsibility immediately.**
18. **Current Responsibility must not be inferred from eventual Actual performer.**
19. **Responsibility transfer does not change underlying Activity identity.**
20. **Account creation/deletion does not define or erase native Responsibility attribution.**
21. **AI proposals do not establish Responsibility or transfer Authority.**
22. **Simple UI may collapse roles only when product policy makes the meaning unambiguous.**
23. **Qualified Responsibility structure does not automatically imply independent entity identity.**
24. **No universal `responsibility_id`/`assigned_to`/Relationship wrapper is pre-approved.**

---

# 26. Relationship v0 compatibility

Responsibility is the first major stress test of the accepted Relationship modeling discipline.

Result:

```text
simple Responsibility semantics
→ direct specific relation may suffice

materially rich/open/transfer/history semantics
→ specific qualified Responsibility relation/context may be justified

universal Relationship wrapper
→ still unnecessary
```

Responsibility therefore **confirms rather than reopens** Relationship v0 at the current baseline.

No universal Responsibility table/entity is implied by this semantic result.

---

# 27. Persistence/API implications — deliberately not physical design

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

Do not infer from Responsibility v0 that LifeOS requires:

- one universal `responsibilities` table;
- one universal `assigned_to` field;
- Assignment entity;
- Claim entity;
- HandOff entity;
- Stewardship entity;
- one universal Responsibility status enum;
- Acceptance for every assignment;
- automatic Responsibility from Resource selection;
- automatic Responsibility from actual performer;
- automatic Authority/Visibility from Responsibility.

---

# 28. Adjacent Dependency Sweep

## RESOLVED NOW

### Responsibility ↔ Activity

**Resolution:** Activity identity is independent of Responsibility holder. Ordinary assignment/transfer preserves one Activity identity.

### Responsibility ↔ Actor / Person / Account

**Resolution:** an eligible Actor/native referent bears Responsibility; Actor/Person/Account identity remains separate. No Account is required.

### Responsibility ↔ expected performer

**Resolution:** planned execution role is distinct from accountability.

### Responsibility ↔ actual performer

**Resolution:** actual execution attribution is distinct from current/historical accountability.

### Responsibility ↔ Resource

**Resolution:** operational eligibility/capability does not create obligation/accountability.

### Responsibility ↔ Assignment

**Resolution:** Assignment is a role-specific establishment/change operation, not a standalone universal primitive.

### Responsibility ↔ Claim

**Resolution:** Claim is a self-initiated role-acquisition operation with policy-dependent effect, not a standalone universal primitive.

### Responsibility ↔ Hand-off

**Resolution:** Hand-off is a role-specific transfer workflow/pattern; transfer request is not universally effective transfer.

### Responsibility ↔ Stewardship boundary

**Resolution:** coordination Stewardship is semantically distinct from Responsibility; standalone primitive status remains SAFE DEFERRED.

## SAFE DEFERRED

### Authority / delegation

**Owner:** Relationships / Reasoning — Authority/Principal/delegation review.  
**Why safe:** Responsibility explicitly creates no Authority and can exist under several authority policies.  
**Reopening trigger:** no authority model can establish/change Responsibility without embedding Authority into Responsibility itself.  
**Tests to rerun:** CORE-04, MA-06, MA-13, MA-17, XCON-02, XCON-05.

### Acceptance / Acknowledgement

**Owner:** Relationships / Reasoning — collaboration-state review.  
**Why safe:** assignment/claim/hand-off effects are explicitly policy-dependent and do not equate with Confirmation.  
**Reopening trigger:** ordinary responsibility transfer cannot distinguish proposal, receipt, willingness and effective change without altering Responsibility semantics.  
**Tests to rerun:** CORE-02, CORE-04, MA-03, MA-05, MA-11, XCON-04.

### Visibility

**Owner:** Relationships / Reasoning — Visibility/Authority review.  
**Why safe:** Responsibility grants no disclosure semantics by itself.  
**Reopening trigger:** minimum role access cannot be represented without making Visibility intrinsic to Responsibility.  
**Tests to rerun:** MA-07, MA-08, MA-13, MA-17, XCON-02, XCON-05.

### Provenance / Version / Decision / reconciliation

**Owner:** Relationships / Reasoning + logical model.  
**Why safe:** Responsibility requires reconstructable material history but does not pre-decide versioning/decision mechanics.  
**Reopening trigger:** effective/current responsibility cannot be reconstructed after corrections/conflict without changing the relation semantics.  
**Tests to rerun:** CORE-02, CORE-05, CORE-09, MA-12, XCON-03, XCON-04.

### Coordination Stewardship primitive

**Owner:** Relationships / Reasoning / product workflow validation.  
**Why safe:** the distinction from Responsibility is fixed, but no current workflow requires standalone persistent Stewardship identity/state.  
**Reopening trigger:** LifeOS must explicitly assign, transfer, query or measure coordination burden independently and cannot reconstruct it from actions/provenance/product state.  
**Tests to rerun:** CORE-03, CORE-04, CORE-12, MA-04, MA-15, XCON-04.

### Collective / joint Responsibility

**Owner:** Relationships / Reasoning + future collective/group/cardinality review.  
**Why safe:** current semantics allow multiple holders without assuming whether accountability is joint or individual.  
**Reopening trigger:** ordinary workflows require one collective responsibility identity or group actor that cannot be represented by specific holder relations.  
**Tests to rerun:** CORE-03, CORE-04, MA-03, MA-13, XCON-01, XCON-04.

### Fallback / conditional Responsibility

**Owner:** Trigger/policy review.  
**Why safe:** fallback is explicitly not current Responsibility; activation semantics remain outside the current relation.  
**Reopening trigger:** common fallback/rotation workflows cannot activate responsibility without embedding generic condition logic into Responsibility.  
**Tests to rerun:** CORE-02, CORE-04, XCON-03, XCON-04.

### Qualified Responsibility identity / physical representation

**Owner:** logical data model.  
**Why safe:** current semantics decide when richer structure may be needed without claiming universal independent identity.  
**Reopening trigger:** persistence cannot preserve open/current/history/query semantics without a materially different domain model.  
**Tests to rerun:** CORE-06, CORE-10, CORE-13, XCON-01, XCON-04.

```text
REOPEN                         0
unclassified material items    0
```

No current dependency blocks the accepted Responsibility baseline.

---

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

- Authority/Principal/delegation and who may establish/transfer Responsibility;
- Acceptance/Acknowledgement and exact proposal-response semantics;
- Visibility/access policy around responsibility context;
- collective/group/joint accountability semantics;
- fallback/conditional/rotation policy;
- standalone coordination Stewardship primitive status;
- exact Version/Decision/Provenance representation of changes;
- exact qualified Responsibility identity/cardinality/persistence;
- specialist regulated-accountability extensions;
- final API/SQL shape.

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

Both Responsibility and Participation continue to expose the same unresolved adjacent governance/common-ground questions — Authority, Visibility, Acceptance/Acknowledgement, delegation and reconciliation — but neither absorbs them.

See:

- `concepts/participation.md`;
- `checkpoints/participation-v0-validation.md`.
