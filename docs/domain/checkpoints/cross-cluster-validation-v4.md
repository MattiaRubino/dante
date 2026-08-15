# Cross-Cluster Validation v4 — Clusters 1–4

**Status:** PASS WITH HARDENING — current integrated baseline  
**Validated:** 2026-08-12  
**Validation standard:** Domain Validation Methodology v3  
**Scope:** Intention & Execution + Time + Observed Reality & Evidence + Data / Subjects  
**Branch:** `feature/domain-model`

## 1. Purpose

Cross-Cluster Validation v4 verifies that the first four Domain Atlas clusters remain coherent after Data / Subjects introduced native identity, value semantics, contextual roles, longitudinal-query rejection, and the Person / Actor / Account / Asset / Resource boundaries.

It runs only after:

1. Data / Subjects Cluster Integration;
2. Data / Subjects Multi-Actor Stress;
3. terminology-neutral Asset re-review;
4. Deferred Dependency Closure — Clusters 1–4.

This checkpoint supersedes v3 as the current cross-cluster integration baseline while preserving v3 as historical evidence.

---

## 2. Cluster status entering v4

```text
Intention & Execution v0        PASS
Time v0                         PASS
Observed Reality & Evidence v0  PASS
Data / Subjects v0              PASS WITH HARDENING
Deferred Dependency Closure     PASS
```

No cluster enters v4 with a structural `REOPEN` dependency.

---

# 3. Integrated semantic topology

```text
INTENTION / STRATEGY
Goal
Plan
Activity / Event / Routine / Milestone

TEMPORAL EXPECTATION / PLACEMENT
Recurrence
Occurrence
Temporal Constraint
Availability / Capacity
Schedule

EXECUTION / REALITY
Session
Actual
Outcome
Observation

EPISTEMIC / EVALUATION
Confirmation
Evidence
Provenance

VALUE SEMANTICS
Quantity

NATIVE IDENTITY
Person
Asset — current scoped physical-object baseline

CONTEXTUAL ROLES
Subject  — aboutness
Actor    — agency category, expressed through specific roles
Resource — execution/planning eligibility/capability

ACCESS / SECURITY BOUNDARY
Account — platform/access identity
Principal — deferred

LONGITUDINAL PRODUCT PROJECTION
native records
→ query/filter/group
→ valid aggregate/trend/comparison
→ History / Tracker / Progress / Register UI
```

This topology is not a mandatory chain, parent tree, SQL schema, or object inheritance graph.

---

# 4. Top-down reconstruction

Representative workflow:

```text
Goal
Improve fitness
        ↓ optional
Plan
        ↓
Routine
        ↓
Recurrence
        ↓
Occurrence
        ↓
Activity / execution intention
        ↓
Resource Requirement (future typed semantics)
        ↓
Person / Asset / other provider playing Resource role
        ↓
Availability / Capacity
        ↓
Schedule
        ↓
Session
        ↓
Actual
        ├─ Outcome
        └─ Observation(s)
             └─ Quantity values where appropriate
        ↓ optional evaluative use
Evidence
        ↓
Goal / Milestone evaluation
```

Result: **PASS**.

No intermediate object is mandatory merely because it exists in the model. Each layer appears only when it adds real semantic value.

---

# 5. Bottom-up reconstruction

Representative spontaneous measurement:

```text
Observation
body weight = Quantity(66.4 kg)
        ↓
Subject role → Person P17
        ↓
Provenance
        ↓ optional
Confirmation / Evidence use
        ↓ optional
Goal / Milestone evaluation
        ↓ optional
longitudinal query / trend projection
```

Result: **PASS**.

No fake Activity, Actual, Plan, Register, RegisterEntry or Resource is required to explain the record.

---

# 6. Lateral propagation tests

## Account access ends

```text
Account disabled/deleted
```

must not silently cause:

```text
Person deleted
historical Actor attribution erased
Subject identity rewritten
```

**PASS**.

## Asset sold / transferred

```text
Asset A17 ownership/use changes
```

must not silently cause:

```text
Asset history replaced
Subject observations deleted
Resource role history rewritten
```

**PASS**.

## Resource substitution

```text
planned camera A17
actual camera A18
```

must preserve:

- Activity identity where intended work is unchanged;
- original allocation/reservation history;
- actual-use difference.

**PASS WITH HARDENING**.

## Subject correction

Correcting a descriptive record from Person/Asset A to B must not silently rewrite Actor, Account, Resource, or earlier attribution history.

**PASS WITH HARDENING**.

## Quantity display conversion

```text
66.4 kg → 146.4 lb display
```

must not duplicate Observation truth or silently change source representation.

**PASS**.

## Delete tracker/view

Native records remain.

**PASS**.

---

# 7. Deep chronology regression

## Person / Account chronology

```text
Person exists
→ later Account created
→ provider/login changes
→ Account disabled
→ Person/history remain where policy permits
```

**PASS**.

## Asset chronology

```text
acquired
→ observed
→ repaired
→ used as Resource
→ lent
→ sold
→ historical record retained
```

**PASS**.

## Resource chronology

```text
Requirement
→ candidates
→ allocation A
→ reservation A
→ substitution B
→ Actual use B
```

**PASS WITH HARDENING** — stages remain distinguishable.

## Observation correction chronology

```text
Observation attributed to Subject A
→ later corrected to B
```

Provenance/history must preserve the earlier attribution when material.

**PASS**.

---

# 8. Redundancy / destructive regression

| Destructive proposal | Result | Reason |
|---|---|---|
| merge Person + Account | FAIL | non-account humans and access lifecycle |
| merge Person + Actor | FAIL | passive humans + non-human/software agency |
| merge Person + Subject | FAIL | identity vs contextual aboutness |
| merge Person + Resource | FAIL | human identity vs planning role |
| merge Asset + Subject | FAIL | physical identity vs aboutness |
| merge Asset + Resource | FAIL | physical identity vs operational eligibility |
| universal Subject entity/root | FAIL | duplicate native identity |
| universal Actor entity/root | FAIL | duplicate native/system identity |
| universal Resource entity/root | FAIL | operational abstraction becomes identity hierarchy |
| universal User root | FAIL | product/access vocabulary absorbs domain identity |
| universal ManagedObject root | FAIL | unrelated lifecycle/identity semantics collapse |
| universal Register + RegisterEntry | FAIL | duplicates native records and history |
| Quantity as entity / universal number | FAIL | contextual meaning and value semantics collapse |

No mandatory merge or new primitive emerges from v4.

---

# 9. Multi-Actor regression

The integrated model must preserve:

```text
shared canonical fact / native identity
+
actor-scoped state / preference / participation / visibility
```

without creating per-user duplicate reality.

Representative stress results:

- caregiver measurement — PASS;
- external participant without Account — PASS;
- shared Asset with different owners/holders/stewards/viewers — PASS WITH HARDENING;
- one Resource with private unavailability reason but shareable free/busy projection — PASS WITH HARDENING;
- different actor Confirmations — PASS;
- conflicting actor Observations/assertions — PASS;
- AI/service Actor under separate Account/Principal/Authority context — PASS WITH HARDENING;
- access revocation without historical attribution deletion — PASS WITH HARDENING.

No multi-actor scenario requires a universal Team/User/Actor/Subject/Resource root.

---

# 10. Privacy / authority regression

Cross-cluster v4 confirms:

```text
visibility != authority
subject != owner/viewer
actor != authority
resource eligibility != allocation authority
asset ownership != universal visibility
account authentication != semantic actor
provenance visibility != upstream payload visibility
aggregate visibility != source-record visibility
AI context access != disclosure permission
```

Exact Authority/Visibility/Principal/consent/delegation mechanics remain SAFE DEFERRED to Relationships / Reasoning and security modeling.

Result: **PASS WITH HARDENING**.

---

# 11. AI regression

AI may propose, infer, rank, transform, summarize, or automate within authorized policy, but v4 preserves these boundaries:

```text
AI inference != established Actual
AI inference != Person/Asset/Subject identity establishment by default
AI proposal != Confirmation / Acceptance
AI agency != human authorship
AI action != Authority
AI knowledge != disclosure permission
AI Resource ranking != allocation Authority
```

Result: **PASS**.

---

# 12. Scale / implementation-pressure regression

The current model avoids several known scaling traps:

- no row-per-sensor-sample requirement from Observation semantics;
- no one-Asset-per-consumable-unit requirement;
- no universal RegisterEntry copy layer;
- no universal Actor/Subject/Resource wrapper rows;
- no eager concrete Resource assignment for abstract Requirements;
- no requirement to materialize every derived longitudinal aggregate;
- no requirement to use provider identifiers as native domain primary identity;
- no one giant arbitrary JSON object for all life data.

Remaining logical/physical pressures are explicitly SAFE DEFERRED and do not change current semantic verdicts.

Result: **PASS WITH HARDENING**.

---

# 13. Simple-user regression

Kernel distinctions do not require ontology-heavy UX.

Examples:

```text
Weight 66.4 kg
```

can imply established `me` context without exposing `Subject`.

```text
Done by Anna
```

uses a specific action role rather than displaying `Actor`.

```text
Need a camera
```

can expose requirement/candidate flow without calling the camera a `Resource` object.

```text
Sony A7 IV
```

can present an Asset-backed profile without exposing the term `Asset`.

Result: **PASS**.

---

# 14. Specialist-system boundary regression

Specialist adapters may map:

- external users/contacts/accounts to Person/Account evidence;
- devices/equipment to Asset-like native referents where compatible;
- booking resources to Resource-role semantics;
- health measurements to Observation + Quantity + Subject;
- provider free/busy to Availability/Capacity evidence/projection;
- longitudinal reports to query projections.

External schemas remain adapters/evidence rather than internal design authority.

Result: **PASS**.

---

# 15. Hardening incorporated by v4

1. **Actor specific-role precedence** — Actor is a useful agency category but does not replace `recorded_by`, `performed_by`, `confirmed_by`, `proposed_by`, etc.
2. **Resource identity hardening** — Resource preserves whatever native identity/value/pool/supply/service semantics independently exist; it never manufactures identity.
3. **Resource stage separation** — Requirement, candidate, allocation, reservation/claim, actual use/consumption remain distinguishable.
4. **Asset terminology-neutral result** — universal ManagedObject root rejected; current individually tracked physical-object identity survives; exact noun remains non-semantic/reopenable.
5. **Longitudinal source-truth rule** — query/tracker/product presentation remains above native records and does not recreate RegisterEntry.

---

# 16. Deferred-dependency linkage

Normative transition checkpoint:

- `deferred-dependency-closure-clusters-1-4-v0.md` — **PASS**.

All material remaining boundaries are either RESOLVED or SAFE DEFERRED with owner/reopening trigger/tests.

```text
REOPEN = 0
unclassified material dependencies = 0
```

---

# 17. Final v4 verdict

- [ ] PASS
- [x] PASS WITH HARDENING
- [ ] REOPEN
- [ ] DEFERRED DEPENDENCY

```text
CROSS-CLUSTER VALIDATION v4
PASS WITH HARDENING

Clusters covered: 4
Structural reopenings: 0
Mandatory concept removals from current accepted baseline: 0
Mandatory new primitives: 0
Unclassified material dependencies: 0
```

The first four clusters are now coherent enough to proceed to Relationships / Reasoning under Methodology v3.

This is not permission to jump directly to SQL/API implementation. Relationships / Reasoning and final whole-domain gates remain mandatory.

---

# 18. Next stage

```text
Relationships / Reasoning
→ Adjacent Dependency Sweep mandatory before every concept verdict
→ whole-domain semantic regression
→ whole-domain multi-actor regression
→ persistence/API pressure
→ logical model
→ physical PostgreSQL model
→ APIs / backend packages / implementation
```

Likely Cluster-5 review space remains candidate space rather than a checklist: Relationship, Dependency, Responsibility/Assignment/Hand-off, Contribution, Participation, Authority/Visibility, Decision, Version, AI Proposal, Goal/Evidence/Criterion relationships, Principal/delegation and any other concept that concrete scenarios prove necessary.

---

# 19. Downstream integration amendment — Criterion / Evaluation v0 (2026-08-15)

Cross-Cluster Validation v4 remains a historical Clusters 1–4 integration checkpoint. Criterion / Evaluation v0 adds a downstream semantic closure that extends — but does not retroactively rewrite — the integrated topology above.

Current downstream topology now includes:

```text
EVALUATIVE SPECIFICATION
Criterion
  └─ GoalCriterion = Goal-scoped Criterion semantics, not a separate universal root

EVALUATION
applicable material target state
+ applicable Criterion state
+ relevant Evidence/source basis
+ evaluation context / time
→ contextual Evaluation
→ optional derived Goal Progress / assessment projection
```

This downstream addition preserves the v4 separations:

```text
Goal / Milestone != Criterion
Criterion != Evidence
Evaluation != Evidence
Evaluation != Actual / Outcome
Evaluation != Decision
Evaluation != Confirmation
Evaluation != Reconciliation
Goal Progress != universal stored percentage/status
```

Cross-cluster regressions remain coherent under the accepted Criterion / Evaluation hardenings:

- no Evidence does not automatically mean failure or non-occurrence;
- unknown/insufficient Evidence is a valid evaluation condition;
- multiple Criteria do not imply a universal AND/average/score;
- frequency/duration/range/threshold/maintenance semantics use the applicable Criterion and time window rather than one universal Goal field;
- materially consequential historical Evaluation remains reconstructible against the target, Criterion and Evidence/source states that actually applied;
- later Criterion change, source correction or Reconciliation may produce a later Evaluation without rewriting historical intention, Evidence basis or prior result;
- shared Goal does not imply same Evidence visibility, same personal assessment or automatic Agreement on the Criterion;
- private Evidence may yield an authorized bounded shareable result without raw-source disclosure;
- AI may propose Criteria or calculate under authorized semantics but cannot fabricate Evidence, Criterion adoption, Authority or certainty;
- no universal Evaluation root/workflow, target-value field, progress percentage, source rank or evaluation DSL is introduced.

Downstream status:

```text
Cross-Cluster v4 historical verdict        PASS WITH HARDENING — unchanged
Criterion / Evaluation semantic closure    INTEGRATED downstream
structural reopenings                      0
unclassified material dependencies         0
```

This amendment does not close Relationships / Reasoning as a cluster and does not preselect the next Cluster-5 candidate. The remaining candidate space must still be freshly re-scored under Methodology v3 before the next individual review.

Normative downstream references:

- `../concepts/criterion-evaluation.md`;
- `criterion-evaluation-v0-validation.md`;
- `deferred-dependency-closure-clusters-1-4-v0.md`.