<!-- LIFEOS-CANONICAL-SPLIT document="responsibility.md" part="2" total="3" -->
> **Canonical document split — Part 2 of 3.** Parts 1–3 together form one authoritative document; this is a physical split only, not a summary/reference hierarchy. The payload preserves the full pre-compaction baseline first and later downstream amendments in sequence; later explicit amendments override stale status/deferral wording without deleting the earlier rationale. Navigation: [Part 1](responsibility.md) · **Part 2** · [Part 3](responsibility-part-3.md)

<!-- LIFEOS-CANONICAL-PAYLOAD -->
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

Visibility v0 further hardens this: AI may use an authorized private basis to propose a change without being permitted to disclose that basis.

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
25. **Responsibility grants neither Visibility nor re-disclosure Authority by itself.**

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

### Responsibility ↔ Authority

**Resolution:** Authority v0 establishes governance/effect power independently; Responsibility creates no Authority. Effective assignment/transfer uses applicable Authority/policy without changing Responsibility semantics.

### Responsibility ↔ Visibility

**Resolution:** Visibility v0 establishes bounded information exposure independently; Responsibility creates no automatic visibility or re-disclosure right.

## SAFE DEFERRED

### Acceptance / Acknowledgement

**Owner:** Relationships / Reasoning — collaboration-state review.  
**Why safe:** assignment/claim/hand-off effects are explicitly policy-dependent and do not equate with Confirmation.  
**Reopening trigger:** ordinary responsibility transfer cannot distinguish proposal, receipt, willingness and effective change without altering Responsibility semantics.  
**Tests to rerun:** CORE-02, CORE-04, MA-03, MA-05, MA-11, XCON-04.

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

