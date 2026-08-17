# Resource Requirement / Allocation v0 Validation — Methodology v3

**Status:** PASS WITH HARDENING — accepted semantic verdict; propagation write in progress  
**Validated:** 2026-08-15  
**Concept / family:** Resource Requirement / Resource Allocation v0 + schedulable Capacity Claim integration  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Validation standard:** `../validation-methodology-v3.md`  
**Branch:** `feature/domain-model`  
**Approved pre-scope:** `c6c324ff5a5806f9c99c793d7db587f9ce0e4822`

---

# 0. Candidate formation and accepted minimum

The candidate was selected only after Proposal / Request v0 was fully closed and the remaining Relationships / Reasoning candidate space was freshly reconsidered. The review did not inherit the older ranking as roadmap authority.

The initial label `Resource Requirement / Allocation / Reservation` was deliberately reduced by validation.

The smallest surviving semantic decomposition is:

```text
Resource Requirement
= what a bounded planning/execution context needs

Candidate Set
= contextual/derived eligibility projection

Resource Allocation
= which provider/supply/capacity source is currently designated in the plan

Capacity Reservation / Claim
= existing Time / Availability & Capacity semantics for schedulable capacity actually held/protected

Actual Resource Use / Consumption
= realized reality/execution/inventory fact; not Allocation
```

Critical correction:

> **No new universal `Reservation` primitive is accepted.**

The existing schedulable Capacity Reservation / Claim semantics apply to rooms, people/time, equipment availability and other schedulable capacity. Inventory holds, stock reservation, warehouse commitment and consumable reservation remain owned by future inventory/supply semantics.

---

# 1. Accepted definitions

## Resource Requirement

> **Resource Requirement is the contextual semantic specification of what a bounded planning or execution context needs from Resource-capable providers, capacity, services, pools or supply without identifying the provider merely by expressing the need.**

Potential components include capability, qualification, compatibility, Quantity, location, temporal/capacity need, supply characteristics and other bounded eligibility requirements.

```text
Resource Requirement != Request
Resource Requirement != Resource
Resource Requirement != Criterion
Resource Requirement != Quantity
Resource Requirement != Temporal Constraint
Resource Requirement != Allocation
```

Criterion, Quantity, Temporal Constraint and Availability/Capacity may contribute without being absorbed.

A Requirement may be explicit or implicit/reconstructible depending consequence. No standalone persisted Requirement object is mandatory in simple flows.

## Resource Allocation

> **Resource Allocation is the contextual planned designation or selection of one or more eligible providers, supplies or capacity sources intended to satisfy a bounded Resource Requirement.**

```text
Allocation != Candidate
Allocation != Capacity Reservation / Claim
Allocation != Responsibility
Allocation != Participation
Allocation != Agreement / Consent
Allocation != Authority
Allocation != Decision
Allocation != Schedule
Allocation != Actual use
```

Decision may select an Allocation; Proposal may propose it; Request may ask for it; Authority/policy may govern its effect. None is the Allocation itself.

---

# 2. Core Semantic Validation Gate

| Test | Result | Key finding / hardening |
|---|---|---|
| CORE-01 Workflow inversion | PASS WITH HARDENING | real workflows require need/provider/selection/held-capacity/actual separation without forcing every step to materialize |
| CORE-02 Deep chronology | PASS WITH HARDENING | candidate changes, material Requirement change, reallocation, failed claims, substitution, correction and withdrawal preserve distinct histories |
| CORE-03 Adversarial reductio | PASS | removing Requirement or Allocation semantics fails; universal roots/merges fail; contextual pair survives |
| CORE-04 Redundancy | PASS WITH HARDENING | Requirement/Allocation remain distinct from Request, Resource, Criterion, Capacity Claim, Responsibility, Participation, Actual and governance families |
| CORE-05 Traceability | PASS WITH HARDENING | planned designation can be reconstructed against materially relevant need and later actual use without fabricating intent |
| CORE-06 Orphan / independence | PASS WITH HARDENING | Requirement may exist without candidate/allocation; Allocation may exist without claim; Actual use may exist without prior Allocation |
| CORE-07 External benchmark | PASS WITH HARDENING | external systems support phase separation/late binding but do not dictate LifeOS ontology |
| CORE-08 Anti-pattern review | PASS | universal Requirement/Allocation/Booking/Assignment/Reservation roots and state-machine defaults rejected |
| CORE-09 Correction / reconciliation | PASS WITH HARDENING | wrong/stale Allocation/provider claims preserve history and use Reconciliation rather than silent overwrite |
| CORE-10 Scale / performance / history | PASS WITH HARDENING | Candidate Set remains derived; no eager candidate expansion or per-unit identity requirement |
| CORE-11 Simple vs power user | PASS | simple UI may collapse operational steps without collapsing semantics |
| CORE-12 Product value / complexity | PASS WITH HARDENING | richer materialization is consequence-sensitive rather than mandatory bureaucracy |
| CORE-13 Implementation pressure | PASS WITH HARDENING | queryability/history required where consequential; no SQL/API/cardinality chosen |

```text
CORE GATE
PASS WITH HARDENING
```

---

# 3. Deep chronological simulation

Representative chronology:

```text
T0 Requirement exists
   Allocation = none
   Capacity Claim = none
   Actual use = none
```

Valid.

```text
T1 candidate set changes because new information arrives
```

Result:

```text
candidate-set revision != Requirement revision
```

```text
T2 Allocation A1 selects provider A17
```

This means only that the current plan designates A17 to satisfy the Requirement. It does not prove reservation, actual use, responsibility or perpetual availability.

```text
T3 schedulable Capacity Claim C1 holds A17 17:00–20:00
```

Requirement, Allocation and Claim remain linked but distinct. Cancelling C1 does not automatically erase A1.

```text
T4 Requirement changes materially
```

Prior Allocation does not silently carry forward. It remains bound to the materially relevant prior Requirement state where consequence requires it.

```text
T5 later reallocation selects A18
```

Historical `R1 → A17` and later `R2-state → A18` remain reconstructible.

```text
T6 reservation/Capacity Claim attempt fails
```

Failure does not make the prior Allocation false.

```text
T7 actual provider differs from planned provider
```

A later formal reallocation may exist, or Actual use may simply show the substitute. LifeOS must not invent retroactive Allocation merely because the actual provider is known.

```text
T8 allocated quantity = 500 ml
   actual consumed = 430 ml
```

Both remain independently reconstructible.

```text
T9 earlier recorded Allocation is later proven wrong
```

Preserve prior assertion, corrected current understanding and material Provenance/Reconciliation basis.

```text
T10 Requirement withdrawn
```

Future applicability changes; historical Allocation/Claim/Actual history is not erased.

```text
T11 Allocation removed while external provider claim remains active
```

Temporary inconsistency is valid reality and may require Reconciliation/corrective action.

```text
T12 historical query
```

Where material, LifeOS can distinguish what was required, candidates known, Allocation, capacity held, changes, actual use and later correction. Candidate computations need not universally be persisted.

CORE-02 result: **PASS WITH HARDENING; REOPEN 0.**

---

# 4. Adversarial reductio

```text
REMOVE Resource Requirement semantics
→ FAIL

Requirement = Request
→ FAIL

Requirement = Resource
→ FAIL

Requirement = Criterion
→ FAIL

universal Requirement root
→ FAIL

REMOVE Resource Allocation semantics
→ FAIL

Allocation = Resource
→ FAIL

Allocation = Reservation / Capacity Claim
→ FAIL

Allocation = Responsibility
→ FAIL

Allocation = Actual
→ FAIL

Candidate Set as required primitive
→ FAIL

Requirement + Allocation contextual semantics
→ SURVIVES
```

The possible sequence:

```text
Requirement → Candidate → Allocation → Capacity Claim → Actual
```

is not mandatory. Valid alternatives include Requirement→Actual, Requirement→Allocation, pool Capacity Claim before concrete Allocation, and simple flows where Requirement remains implicit/reconstructible.

No universal workflow/state machine is accepted.

---

# 5. Multi-Actor Compatibility Gate

| Test | Result |
|---|---|
| MA-01 Identity/account independence | PASS |
| MA-02 Shared fact / actor overlay | PASS WITH HARDENING |
| MA-03 Responsibility/assignment | PASS WITH HARDENING |
| MA-04 Stewardship | PASS |
| MA-05 Common ground | PASS WITH HARDENING |
| MA-06 Authority/current effect | PASS WITH HARDENING |
| MA-07 Selective disclosure | PASS WITH HARDENING |
| MA-08 Inference privacy | PASS WITH HARDENING |
| MA-09 Partial adoption | PASS |
| MA-10 Assisted/on-behalf-of | PASS WITH HARDENING |
| MA-11 Revocation/lifecycle | PASS WITH HARDENING |
| MA-12 Conflict | PASS WITH HARDENING |
| MA-13 Unequal power | PASS WITH HARDENING |
| MA-14 Multi-resource/capacity | PASS WITH HARDENING |
| MA-15 Coordination burden | PASS |
| MA-16 Progressive disclosure | PASS WITH HARDENING |
| MA-17 AI authority | PASS WITH HARDENING |
| MA-18 Specialist-system boundary | PASS |
| MA-19 Primitive redundancy | PASS |
| MA-20 Actor-scoped reality | PASS WITH HARDENING |

```text
MULTI-ACTOR GATE
PASS WITH HARDENING
```

Critical Person-as-Resource rule:

```text
Requirement: qualified interpreter
Allocation: Anna
```

never implies:

```text
Anna agreed
Anna consented
Anna participates
Anna is responsible
Anna acknowledged it
Anna is actual performer
```

Allocation result visibility may also remain separate from private matching/eligibility basis.

---

# 6. AI boundary

AI may discover candidates, evaluate compatibility, rank candidates, propose an Allocation and perform a bounded Allocation under explicit applicable Authority/policy.

It may not collapse:

```text
AI ranking != Allocation
AI proposal != effective Allocation
AI optimization != Authority
AI access to private eligibility data != disclosure permission
```

Actual AI/system attribution and material policy/Authority basis remain truthful where consequential.

---

# 7. Cross-Concept Consistency Gate

| Test | Result | Finding |
|---|---|---|
| XCON-01 Identity | PASS WITH HARDENING | Requirement/Allocation do not manufacture provider identity or universal relation identity |
| XCON-02 Authority | PASS WITH HARDENING | allocation choice/effect requires separate Authority/policy where governed |
| XCON-03 planned/current/Actual/history | PASS WITH HARDENING | planned designation, held capacity and Actual use stay independently reconstructible |
| XCON-04 Relationship | PASS | specific contextual semantics; no generic Relationship root |
| XCON-05 Multi-Actor | PASS WITH HARDENING | shared facts and actor-scoped privacy/common-ground states remain distinct |
| XCON-06 Language Map | PASS WITH UPDATE REQUIRED | Requirement/Allocation promoted from deferred to canonical semantics |

```text
XCON GATE
PASS WITH HARDENING
```

---

# 8. External benchmark classification

External systems were used only as evidence.

- Kubernetes: separation of requested resources, feasible candidates, scoring/selection/binding and actual usage is **ADAPT** evidence for phase separation; Kubernetes ontology is not imported.
- HL7 FHIR Appointment: requested participant type/role can exist before a concrete actor is known, supporting late binding; specialist healthcare semantics are not imported.
- Google Calendar resource booking: room/equipment booking and resource-calendar acceptance provide **ADAPT WITH CAUTION** evidence; provider `resource attendee` vocabulary does not define LifeOS Participation or universal Reservation semantics.

Canonical direction remains:

```text
LifeOS semantics
→ internal model
→ provider/standard adapters
```

---

# 9. Adjacent Dependency Sweep

## RESOLVED

```text
Requirement ↔ Resource
Requirement ↔ Request
Requirement ↔ Criterion
Requirement ↔ Quantity
Requirement ↔ Temporal Constraint / Availability
Requirement ↔ Candidate Set

Allocation ↔ Requirement
Allocation ↔ Resource
Allocation ↔ Candidate Set
Allocation ↔ schedulable Capacity Reservation / Claim
Allocation ↔ Schedule
Allocation ↔ Responsibility
Allocation ↔ Participation
Allocation ↔ Authority
Allocation ↔ Decision
Allocation ↔ Proposal / Request
Allocation ↔ Actual use
Allocation ↔ Version
Allocation ↔ Provenance / Reconciliation
Allocation ↔ Visibility
Allocation ↔ Representation
```

Reconciliation remains separate. Competing Allocation assertions/provider states may remain unresolved or be reconciled under a bounded basis. No last-write-wins/provider-wins rule is accepted.

## SAFE DEFERRED

| Dependency | Owner | Reopening trigger |
|---|---|---|
| Requirement composition `all/any/alternatives` | planning/logical model | ordinary multi-requirement flows cannot express alternatives/cumulative satisfaction |
| candidate matching/ranking expression | planning + Criterion/Evaluation | eligibility cannot be computed without changing Requirement semantics |
| pool / late-binding mechanics | logical Resource model | pool allocation requires independent semantics not representable by current model |
| non-temporal stock/inventory reservation | inventory/supply | consumable holds cannot compose without universalizing Capacity Claim |
| actual inventory consumption/movement | inventory + Actual | real consumption history cannot be reconstructed |
| Place/Service/Skill native semantics | future respective reviews | repeated workflows require stronger native concepts |
| exact Allocation lifecycle/cardinality | logical model | simple/direct + rich/history cases cannot coexist coherently |
| automatic fallback/reallocation | Trigger/policy | Allocation must embed conditional automation to work |
| collective/group allocation | collective/group review | ordinary workflows require collective Actor/quorum semantics |
| specialist booking/source-of-record behavior | integrations/specialist adapters | external authoritative state cannot reconcile safely |
| retention/audit | privacy/retention | required history conflicts with minimization/deletion |
| SQL/API representation | logical/physical/API stage | implementation pressure exposes semantic contradiction |

Relevant reopening retests are CORE-02/03/04/09/10/13, MA-02/06/07/12/14/17/18/20 and XCON-01/02/03/04/05 according to dependency.

```text
REOPEN       0
UNCLASSIFIED 0
```

---

# 10. Mandatory hardenings

```text
RRA-01 Requirement may exist without candidate or Allocation.
RRA-02 Requirement need not be materialized as a standalone object in low-consequence/simple cases.
RRA-03 Candidate Set is contextual/derived by default.
RRA-04 Candidate-set change != Requirement revision automatically.
RRA-05 Requirement material change does not automatically carry prior Allocation forward.
RRA-06 Allocation != Reservation / Capacity Claim.
RRA-07 Allocation != Actual use.
RRA-08 Allocation may exist without Reservation.
RRA-09 Actual use may exist without prior Allocation.
RRA-10 schedulable Capacity Claim may exist before concrete Allocation in legitimate late-binding/pool cases.
RRA-11 non-temporal inventory reservation is NOT automatically Capacity Reservation / Claim.
RRA-12 allocation/reallocation must preserve material history.
RRA-13 failed/cancelled reservation does not erase prior Allocation.
RRA-14 correcting Allocation preserves Provenance/history where material.
RRA-15 Allocation may temporarily conflict with external/provider claims; use Reconciliation, not silent overwrite.
RRA-16 allocating a Person does not create Responsibility, Participation, Agreement or Consent.
RRA-17 Allocation requires applicable Authority/policy for shared canonical effect where governance requires it.
RRA-18 Proposal/Request for Allocation != effective Allocation.
RRA-19 AI recommendation/proposal != effective Allocation.
RRA-20 private eligibility/ranking basis may remain hidden while exposing an authorized bounded result.
RRA-21 Resource/provider identity is never manufactured by Requirement or Allocation.
RRA-22 no universal Requirement root, Allocation root, ResourcePlan, Booking or ResourceAssignment mega-object.
RRA-23 no mandatory Requirement→Candidate→Allocation→Reservation→Actual workflow/state machine.
RRA-24 persistence/materialization is consequence-sensitive.
```

All hardenings were rechecked against the applicable gates. None requires REOPEN.

---

# 11. Adversarial / regression corpus

Validated scenarios include:

- no candidate exists yet;
- candidate disappears;
- Requirement changes materially;
- two actors choose different providers;
- Allocation has no reservation;
- reservation/Capacity Claim fails;
- pool capacity held before member selection;
- Person allocated without Consent;
- Actual provider differs from planned;
- Actual use happens spontaneously;
- partial consumable use;
- external provider still holds stale reservation;
- private qualification drives matching;
- AI chooses under insufficient Authority;
- provider says A / user says B;
- old Allocation corrected months later.

No scenario requires a new universal primitive.

---

# 12. Final semantic verdict

```text
RESOURCE REQUIREMENT / ALLOCATION v0
+ SCHEDULABLE CAPACITY CLAIM INTEGRATION

PASS WITH HARDENING

Resource Requirement
✅ canonical contextual semantic family/capability
✅ explicit or implicit/reconstructible depending consequence
✅ material-state-aware where required
❌ universal Requirement root/entity/table

Resource Allocation
✅ canonical contextual planned selection/designation relation/state
✅ history/version-aware where required
✅ simple direct or richer qualified representation allowed
❌ universal Allocation root/entity/workflow

Candidate Set
✅ contextual/derived projection
❌ universal primitive/entity

Capacity Reservation / Claim
✅ existing accepted schedulable-capacity semantics
❌ universal Reservation concept for every Resource domain

Actual resource use
✅ owned by execution/reality/inventory semantics
❌ Allocation

Universal ResourcePlan / Booking / ResourceAssignment mega-root
❌ REJECTED

REOPEN       0
UNCLASSIFIED 0
```

The accepted semantic verdict does not authorize SQL, API, backend implementation, Trigger/policy, inventory/supply reservation, Group/quorum or logical/physical design.

Post-write propagation QA must prove exact approved path scope and preservation before this checkpoint can be marked CLOSED.