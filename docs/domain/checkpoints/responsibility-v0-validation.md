# Responsibility v0 — Validation Checkpoint

**Status:** PASS WITH HARDENING  
**Validated:** 2026-08-12  
**Validation standard:** [Domain Validation Methodology v3](../validation-methodology-v3.md)  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## 1. Scope

- **Primary candidate:** Responsibility
- **Family reviewed together:** Responsibility / Assignment / Claim / Hand-off / Stewardship / expected performer / actual performer
- **Why reviewed as one family:** these terms overlap strongly in product/task language. Reviewing them separately first would risk manufacturing five primitives from vocabulary before proving distinct identity/lifecycle semantics.
- **Inherited pressure:** Activity identity independence; Actor specific-role precedence; Resource eligibility separation; Relationship v0 direct-vs-qualified discipline; multi-actor open/claim/transfer/actual-performer scenarios.

This checkpoint validates Responsibility as a **specific semantic relation family**. It does not select final SQL/API/cardinality, create a universal Responsibility root, accept Assignment/Claim/Hand-off as standalone primitives, or accept Stewardship as a standalone primitive.

---

# 2. Candidate conclusion

> **Responsibility is the contextual semantic relation through which an eligible Actor bears the obligation/accountability to ensure that a bounded commitment is appropriately handled within a defined scope and context. Responsibility is independent of who requested the commitment, who is expected to perform it, who actually performs it, who coordinates it, who has Authority over it, and who may view it.**

Current classification:

```text
RESPONSIBILITY
CANONICAL SPECIFIC SEMANTIC RELATION FAMILY
may be direct or specifically qualified depending on consequence
NOT universal entity/root

ASSIGNMENT
role-specific establishment/change operation
NOT standalone universal primitive

CLAIM
self-initiated role-acquisition operation
NOT standalone universal primitive

HAND-OFF
role-specific transfer workflow/pattern
NOT standalone universal primitive

COORDINATION STEWARDSHIP
semantically distinct from Responsibility
standalone primitive SAFE DEFERRED

EXPECTED PERFORMER
specific planned Actor role
NOT Responsibility

ACTUAL PERFORMER
specific actual Actor role
NOT Responsibility
```

---

# 3. Evidence reviewed

## Internal

- Activity v0, especially identity independent of requester/responsible actor/performer;
- Actor v0 and specific-role precedence;
- Resource v0 and Requirement/candidate/Allocation/Reservation/Actual-use separation;
- Multi-Actor Readiness v1 and evidence synthesis;
- Deferred Dependency Closure — Clusters 1–4;
- Cross-Cluster Validation v4;
- Relationship v0 validation;
- personal, household, care, work, maintenance, scheduling, shared-resource and external-participant scenarios.

## External benchmark patterns

External systems were used as evidence, not schemas to copy. Recurring useful patterns included:

- specialist workflow systems separating requester, owner/responsible party, requested performer and actual performer;
- task/work systems distinguishing candidates from assignee and preserving assignment history;
- systems distinguishing claim from assignment as operations/events;
- products allowing unassigned work and/or multiple assignees without defining a universal accountability ontology;
- cognitive-labor research separating anticipation/monitoring/coordination burden from physical execution.

External vocabulary/status taxonomies were not adopted as LifeOS invariants.

---

# 4. Core Semantic Validation Gate

| Test ID | Result | Finding |
|---|---|---|
| CORE-01 Workflow inversion | PASS | Real workflows repeatedly need accountability distinct from requester, expected performer and actual performer. |
| CORE-02 Deep chronology | PASS WITH HARDENING | Open/claimable work, pending transfer, refusal, substitution and later history require current/history semantics that must not overwrite Activity identity. |
| CORE-03 Reductio | PASS | Removing Responsibility collapses accountability into assignee/performer; merging with Resource/Authority/Stewardship fails; five standalone family primitives are unnecessary. |
| CORE-04 Redundancy / merge-split | PASS WITH HARDENING | Responsibility survives; Assignment/Claim/Hand-off reduce to role-specific operations/workflows; Stewardship remains distinct but not yet standalone. |
| CORE-05 Traceability | PASS | requester → Responsibility → expected performer → Actual performer remains reconstructable without duplicate Activity. |
| CORE-06 Orphan / independence | PASS | Responsibility is contextual relation semantics, not native identity; richer qualified form may have persistent record semantics without universal entity identity. |
| CORE-07 External benchmark | PASS | Mature systems repeatedly separate these roles/operations, but no universal provider schema dominates. |
| CORE-08 Anti-pattern | PASS | universal `assigned_to`, Responsibility=root, Resource=responsible, handoff=request-immediate-transfer all rejected. |
| CORE-09 Correction / epistemic integrity | PASS WITH HARDENING | `unknown holder != explicitly open/unassigned`; conflict/correction cannot silently rewrite historical responsibility. |
| CORE-10 Scale/history | PASS | No universal responsibility-event graph required; material history can be retained selectively. |
| CORE-11 Simple vs power user | PASS | casual UI may show `Assigned to Anna`; richer distinctions stay progressive. |
| CORE-12 Product value/complexity | PASS | semantics add value in transfer/shared/high-consequence cases without forcing enterprise workflow into personal use. |
| CORE-13 Implementation pressure | PASS WITH HARDENING | direct simple vs specific qualified Responsibility is allowed; exact identity/table/state representation remains logical-model work. |

**Core Gate:** PASS WITH HARDENING.

---

# 5. Deep chronology stress

Representative chronology:

```text
T0  work explicitly open / claimable
T1  Anna assigns Responsibility to Luca
T2  Luca has not accepted under a policy that requires acceptance
T3  Luca accepts; Responsibility effective
T4  Luca requests hand-off to Maria
T5  Maria has not responded; Luca remains current holder
T6  Maria declines
T7  authorized coordinator reassigns to Marco
T8  Marco becomes responsible
T9  Luca actually performs as substitute
T10 later historical query
```

Required truths:

- T0 explicit openness is not unknown data;
- assignment does not universally equal acceptance/effectiveness;
- hand-off request does not universally transfer the role;
- current Responsibility and actual performer may differ;
- Activity identity survives ordinary transfer/reassignment;
- history is not rewritten to make the eventual performer look responsible all along.

A lower-consequence policy may collapse some of these moments; the kernel semantics must not force that collapse globally.

---

# 6. Reductio / candidate elimination

## Responsibility = assignee / expected performer

Fails delegated accountability and manager/worker cases.

**Result:** REJECTED.

## Responsibility = actual performer

Fails substitution and historical accountability.

**Result:** REJECTED.

## Responsibility = Resource

Eligibility/capability becomes obligation.

**Result:** REJECTED.

## Responsibility = Authority

Accountability becomes permission/governance.

**Result:** REJECTED.

## Responsibility = Stewardship

Execution accountability collapses into coordination/mental-load burden.

**Result:** REJECTED.

## Assignment / Claim / Hand-off as three standing universal entities

Each is incomplete unless it identifies the semantic role being established/acquired/transferred.

**Result:** REJECTED as universal primitives.

## Responsibility as specific relation family

Simple relationship may remain direct; material open/transfer/history semantics may justify a specific qualified Responsibility context.

**Result:** PASS WITH HARDENING.

---

# 7. Key hardenings

## 7.1 Unknown != explicitly open/unassigned

```text
unknown responsibility holder
!=
intentionally no current holder / claimable
```

A future physical model must not let one ambiguous null value erase this difference.

## 7.2 Assignment must name the role

```text
assign Responsibility
assign expected performer
assign reviewer
```

`Assignment` without role semantics is insufficient.

## 7.3 Claim must name the role

Claim means self-initiated acquisition attempt/action for a specific role. Whether it becomes effective immediately is policy-dependent.

## 7.4 Hand-off must name the role

Transfer may concern Responsibility, expected performance, Stewardship, Authority or another role. Moving one must not silently move all.

## 7.5 Assignment/Claim/Hand-off effect is policy/Authority/Acceptance dependent

Neither of these is universal:

```text
assignment always requires acceptance
assignment always changes responsibility immediately
```

## 7.6 Qualified relation != entity automatically

Rich Responsibility may need state/effective interval/history while still not proving a universal independent Responsibility identity/root.

---

# 8. Multi-Actor Compatibility Gate

| Test ID | Result | Finding |
|---|---|---|
| MA-01 Identity/account independence | PASS | Accountless Person can bear Responsibility; Account revocation does not erase historical attribution. |
| MA-02 Shared fact / actor overlay | PASS | One Activity remains shared while Responsibility and private overlays vary. |
| MA-03 Responsibility/assignment/claim | PASS WITH HARDENING | Open, assignment, claim and transfer semantics remain separable. |
| MA-04 Stewardship/mental load | PASS WITH HARDENING | Responsibility != coordination Stewardship; standalone primitive remains deferred. |
| MA-05 Common-ground states | PASS WITH HARDENING | assignment/proposal/receipt/acceptance/effective role change cannot be one universal state. |
| MA-06 Authority/canonical change | PASS WITH HARDENING | Responsibility does not grant Authority; effective changes need policy/authority basis where consequence requires it. |
| MA-07 Selective disclosure | PASS | Responsibility does not imply visibility of all related facts/reasons. |
| MA-08 Inference privacy | PASS | AI/private inference does not establish or disclose Responsibility automatically. |
| MA-09 Partial adoption | PASS | non-LifeOS Person can be requester/responsible/performer. |
| MA-10 Assisted participation/provenance | PASS | recorder/requester/responsible/performer can differ truthfully. |
| MA-11 Lifecycle/revocation | PASS WITH HARDENING | current role changes do not erase historical attribution. |
| MA-12 Conflict/adversarial | PASS WITH HARDENING | conflicting claims about responsibility may remain unresolved pending Authority/Decision. |
| MA-13 Unequal power | PASS WITH HARDENING | acceptance cannot be universal because authority may be asymmetric, but asymmetry is contextual. |
| MA-14 Multi-resource/capacity | PASS | Resource candidate/availability remains independent of Responsibility. |
| MA-15 Coordination burden | PASS WITH HARDENING | assignment/responsibility transfer does not prove mental-load transfer. |
| MA-16 Formality/progressive disclosure | PASS | simple UI can collapse roles only under explicit low-consequence product policy. |
| MA-17 AI authority | PASS WITH HARDENING | AI may propose but does not gain assignment/transfer Authority. |
| MA-18 Specialist boundary | PASS | regulated accountability may remain externally authoritative without becoming LifeOS universal workflow. |
| MA-19 Primitive redundancy | PASS | Assignment/Claim/Hand-off do not survive as universal independent primitives. |
| MA-20 Actor-scoped reality attribution | PASS | responsible / planned performer / actual performer remain separately attributable. |

**Multi-Actor Gate:** PASS WITH HARDENING.

---

# 9. Cross-Concept Consistency Gate

```text
XCON-01 Identity                         PASS
XCON-02 Ownership / Authority            PASS WITH HARDENING
XCON-03 Planned / current / actual/history PASS
XCON-04 Relationships                    PASS WITH HARDENING
XCON-05 Multi-actor                      PASS WITH HARDENING
XCON-06 Language                         PASS
```

No accepted Cluster 1–4 concept requires structural reopening.

Activity is strengthened: ordinary Responsibility changes preserve Activity identity.

Actor is strengthened: Responsibility is a specific role/relation, not Actor itself.

Resource is strengthened: eligibility/capability does not imply accountability.

Relationship v0 is confirmed: simple direct Responsibility and richer specific qualified Responsibility can coexist without a universal Relationship root.

---

# 10. Adjacent Dependency Sweep

## RESOLVED

| Boundary | Resolution |
|---|---|
| Responsibility ↔ Activity | ordinary responsibility change preserves Activity identity |
| Responsibility ↔ Actor/Person/Account | responsibility holder is a role-bearing native Actor/referent; identity/access remain separate |
| Responsibility ↔ expected performer | accountability != planned execution |
| Responsibility ↔ actual performer | accountability != actual execution |
| Responsibility ↔ Resource | eligibility/capability != obligation |
| Responsibility ↔ Assignment | Assignment = role-specific establishment/change operation |
| Responsibility ↔ Claim | Claim = self-initiated role-acquisition operation |
| Responsibility ↔ Hand-off | Hand-off = role-specific transfer workflow; request != effective transfer by default |
| Responsibility ↔ Stewardship boundary | coordination burden is semantically distinct; primitive status deferred |

## SAFE DEFERRED

### Authority / delegation

**Owner:** Authority/Principal/delegation review.  
**Safe because:** Responsibility explicitly grants no Authority.  
**Reopening trigger:** responsibility cannot be established/transferred without embedding Authority into Responsibility.  
**Rerun:** CORE-04, MA-06, MA-13, MA-17, XCON-02, XCON-05.

### Acceptance / Acknowledgement

**Owner:** collaboration-state review.  
**Safe because:** Assignment/Claim/Hand-off effect remains policy-dependent and Confirmation remains distinct.  
**Reopening trigger:** ordinary transfer cannot distinguish proposal/receipt/willingness/effectiveness under current semantics.  
**Rerun:** CORE-02, CORE-04, MA-03, MA-05, MA-11, XCON-04.

### Visibility

**Owner:** Visibility/Authority review.  
**Safe because:** Responsibility grants no disclosure semantics.  
**Reopening trigger:** necessary role access cannot remain separate from Responsibility.  
**Rerun:** MA-07, MA-08, MA-13, MA-17, XCON-02, XCON-05.

### Version / Provenance / Decision / reconciliation

**Owner:** Relationships / Reasoning + logical model.  
**Safe because:** material history requirement is fixed without choosing version mechanics.  
**Reopening trigger:** current/effective responsibility cannot be reconstructed after correction/conflict.  
**Rerun:** CORE-02, CORE-05, CORE-09, MA-12, XCON-03, XCON-04.

### Coordination Stewardship primitive

**Owner:** Relationships / Reasoning / product workflow validation.  
**Safe because:** distinct semantics are protected; no standalone persistent primitive is yet required.  
**Reopening trigger:** LifeOS must independently assign/transfer/query/measure coordination burden and cannot reconstruct it otherwise.  
**Rerun:** CORE-03, CORE-04, CORE-12, MA-04, MA-15, XCON-04.

### Collective/joint Responsibility

**Owner:** collective/group/cardinality review.  
**Safe because:** multiple holders are allowed without assuming joint vs individual accountability.  
**Reopening trigger:** ordinary workflows require a collective responsibility identity/group actor.  
**Rerun:** CORE-03, CORE-04, MA-03, MA-13, XCON-01, XCON-04.

### Fallback/conditional Responsibility

**Owner:** Trigger/policy review.  
**Safe because:** fallback is not current Responsibility.  
**Reopening trigger:** common fallback/rotation cannot be represented without generic condition logic embedded in Responsibility.  
**Rerun:** CORE-02, CORE-04, XCON-03, XCON-04.

### Qualified Responsibility identity/persistence

**Owner:** logical data model.  
**Safe because:** semantic richness is accepted without prematurely claiming universal identity.  
**Reopening trigger:** persistence cannot preserve open/current/history semantics under the direct/qualified model.  
**Rerun:** CORE-06, CORE-10, CORE-13, XCON-01, XCON-04.

```text
REOPEN                         0
unclassified material items    0
```

---

# 11. Relationship v0 regression

The first major relation-family stress does **not** reopen Relationship v0.

```text
simple case
Activity --responsible_for--> Actor

rich case
Activity
  ↕
specific qualified Responsibility context
  ↕
Actor
```

The richer form may preserve open state, effective interval, transfer/history or other material relation semantics when required.

No universal `Relationship` wrapper or universal `responsibilities` root is justified.

---

# 12. Final verdict

```text
RESPONSIBILITY FAMILY
PASS WITH HARDENING

Responsibility
✅ canonical specific semantic relation family
✅ direct/simple or specifically qualified/rich form
❌ not universal entity/root
❌ not assignee
❌ not expected performer
❌ not actual performer
❌ not Resource
❌ not Authority
❌ not Stewardship

Assignment
❌ standalone universal primitive
✅ role-specific change/establishment operation

Claim
❌ standalone universal primitive
✅ self-initiated role-acquisition operation

Hand-off
❌ standalone universal primitive
✅ role-specific transfer workflow/pattern

Stewardship
✅ distinct semantic dimension
⏳ standalone primitive SAFE DEFERRED
```

**Structural reopenings:** 0.  
**Unclassified material dependencies:** 0.

---

# 13. Documentation propagation

Required current propagation:

- [x] `concepts/responsibility.md`
- [x] this checkpoint
- [ ] `concepts/activity.md`
- [ ] `concepts/actor.md`
- [ ] `concepts/resource.md`
- [ ] `language-map.md`
- [ ] `README.md`
- [ ] `workstreams/domain-model.md`

No `assignment.md`, `claim.md`, `handoff.md`, or `stewardship.md` is justified by this review.

---

# 14. Next-stage implication

Do not select the next candidate merely from roadmap order.

After documentation propagation, re-check dependency leverage across the remaining Relationships / Reasoning space. `Participation` is a strong likely next candidate because it pressures Event/Session/Actual, actor-scoped state, invitation/acceptance and historical participation, but it is not pre-selected by this checkpoint.