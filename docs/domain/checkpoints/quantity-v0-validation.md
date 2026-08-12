# Quantity v0 — Validation Checkpoint

**Status:** PASS WITH HARDENING — accepted current baseline  
**Validated:** 2026-08-12  
**Validation standard:** Domain Validation Methodology v3  
**Cluster:** Data / Subjects  
**Branch:** `feature/domain-model`

## 1. Scope

- Concept: Quantity
- Candidate version: v0
- Adjacent concepts: Observation, Register, GoalCriterion, Temporal Constraint, Capacity, Asset, Resource, Money/MonetaryAmount, Rating/Scale, Ratio/Percentage, Duration, Range
- Why this review exists: LifeOS needs reusable scalar amount semantics across multiple domains without duplicating measurement/unit behavior or turning every numeric value into an entity.

---

# 2. Evidence reviewed

## Internal

Reviewed accepted/current LifeOS material covering:

- Observation v0 and its explicit `Quantity != Observation` boundary;
- Goal criteria and evidence expectations;
- Temporal Constraint and Capacity semantics;
- Time-cluster distinctions between elapsed duration and calendar-relative semantics;
- Provenance source-representation/correction requirements;
- Multi-Actor Readiness v1;
- feature-discovery scenarios involving body weight, distance, stock, pages, repetitions, consumption, inventory, scores, finance and custom practical units.

## External benchmark evidence

| Source/pattern | Finding | Classification |
|---|---|---|
| UCUM | Computable unit semantics and dimensional compatibility are useful, but unit semantics do not replace domain-property meaning | ADAPT |
| HL7 FHIR Quantity | Reusable measured-amount datatype is a useful value-semantics pattern rather than an independent business entity | ADAPT |
| HL7 FHIR Range | Interval can be composed from Quantity endpoints instead of bloating Quantity | ADAPT |
| HL7 FHIR Money | Currency amount can justify semantics distinct from ordinary physical-unit conversion | ANTI-PATTERN against collapsing Money into basic Quantity |

External models are benchmark evidence only and do not define the LifeOS kernel.

---

# 3. Candidate definition

> **A Quantity is reusable scalar value semantics representing an amount through a numerical magnitude together with unit semantics sufficient to interpret that amount. A Quantity has no independent subject, property, time, identity, provenance, intention, observation history, or evaluative meaning. Comparison, conversion, and arithmetic are valid only where the unit/scale semantics and the surrounding quantity-kind context make those operations semantically valid.**

## Domain question answered

> What amount is represented, and under which unit semantics can that amount be interpreted?

## Identity

No independent domain identity. Quantity is value semantics used by containing records/rules.

## Independent/contextual existence

Quantity can be used in Observation, criteria, constraints, capacity, specifications and other structures without being an entity or historical assertion itself.

## Nearest boundaries

```text
Quantity != Observation
Quantity != Register / RegisterEntry
number != Quantity by default
property / quantity kind != unit
compatible unit != semantic equivalence by itself
same unit != universal aggregation permission
Quantity != Range / comparator / criterion
```

---

# 4. Core Semantic Validation Gate

| Test ID | Applicable? | Evidence/scenario | Result | Finding / hardening / deferral |
|---|---|---|---|---|
| CORE-01 Workflow inversion | Yes | weight, distance, pages, repetitions, inventory, temperature, capacity | PASS | Reusable amount semantics reduce duplicated unit logic without adding user workflow |
| CORE-02 Deep chronology | Yes | imported 5.00 km normalized to 5000 m; later display conversion | PASS WITH HARDENING | source representation/history must not be rewritten by normalization/display |
| CORE-03 Reductio | Yes | remove/merge/entity/universal-number alternatives | PASS | bounded value semantics survive; alternatives lose reuse or create fake identity |
| CORE-04 Redundancy | Yes | Quantity vs Observation/Register/criterion/range | PASS | distinct domain questions and lifecycle/identity behavior |
| CORE-05 Traceability | Yes | same Observation quantity later used for Goal evaluation | PASS | value reuse does not fabricate intent or duplicate source record |
| CORE-06 Orphan/independence | Yes | threshold/specification quantity without Observation | PASS | Quantity legitimately exists as embedded value semantics outside historical observations |
| CORE-07 External benchmark | Yes | UCUM/FHIR Quantity/Range/Money | PASS WITH HARDENING | adapt unit/value separation; reject healthcare-specific resource shapes |
| CORE-08 Anti-pattern review | Yes | generic numeric wrapper, unit text blobs, quantity entity | PASS | all rejected explicitly |
| CORE-09 Correction/reconciliation/epistemic integrity | Yes | source 5.00 km, normalized 5000 m, user/display unit change | PASS WITH HARDENING | containing Provenance owns source/correction history; Quantity itself does not |
| CORE-10 Scale/performance/history | Yes | ten-year registers/high-frequency imports | PASS | independent Quantity rows are explicitly rejected |
| CORE-11 Simple vs power user | Yes | simple display vs normalized/converted advanced use | PASS | unit internals can stay hidden while power users retain precision/source detail |
| CORE-12 Product value/complexity cost | Yes | ordinary weight/distance entry | PASS | concept is mostly implementation/domain semantics and need not surface as UI noun |
| CORE-13 Implementation pressure | Yes | decimal precision, unit codes, embedded values | PASS WITH HARDENING | semantic precision required; final SQL/Python representation deferred |

## Core-gate hardenings incorporated

1. Quantity is value semantics, not entity.
2. Numeric representation alone does not make a Quantity.
3. Property/quantity-kind meaning remains outside the unit token.
4. Unit/dimensional compatibility alone does not establish semantic interchangeability.
5. Same/compatible unit does not authorize every aggregation/arithmetic operation.
6. Normalization/display conversion does not rewrite source representation/history.
7. Money and calendar-relative time are not silently absorbed into ordinary Quantity semantics.
8. Range/comparator/criterion semantics remain outside basic Quantity.

Core Gate verdict: **PASS WITH HARDENING**, with all required hardenings incorporated in `concepts/quantity.md`.

---

# 5. Multi-Actor Compatibility Gate

| Test ID | Applicable? | Evidence/scenario | Result | Finding / hardening / deferral |
|---|---|---|---|---|
| MA-01 Identity/account independence | Yes | same quantity displayed to several actors | PASS | no Quantity identity tied to account/actor |
| MA-02 Shared fact/actor overlay | Yes | 66.4 kg vs 146.4 lb display | PASS | display preference is actor-scoped presentation, not duplicate fact |
| MA-03 Responsibility/assignment/claim | No | Quantity has no execution responsibility lifecycle | N/A | belongs to containing domain object |
| MA-04 Stewardship/mental load | No | basic scalar value semantics | N/A | no coordination workflow introduced |
| MA-05 Common ground/state separation | Limited | shared value with different display units | PASS | presentation does not create separate shared truth |
| MA-06 Authority/canonical change | Yes | actor edits containing Observation/criterion | PASS | authority belongs to container/context, not Quantity object |
| MA-07 Selective disclosure | Yes | private weight fact converted for display | PASS | conversion capability does not grant visibility to containing fact |
| MA-08 Inference privacy | Yes | AI converts private value | PASS | numeric transformation cannot leak private source/context |
| MA-09 Partial adoption/external participant | Yes | external provider sends unit-coded value | PASS | provider/account identity not required for Quantity semantics |
| MA-10 Assisted participation/provenance | Limited | caregiver records another person's amount | PASS | subject/recorder/provenance belong to Observation/container |
| MA-11 Relationship lifecycle/revocation | No | no independent Quantity access lifecycle | N/A | follows containing record/policy |
| MA-12 Conflict/adversarial relationship | Limited | two actors report different values | PASS | disagreement creates separate assertions/Observations, not competing Quantity identity |
| MA-13 Unequal power | Limited | caregiver/clinician context | PASS | authority does not attach to unit/magnitude alone |
| MA-14 Multi-resource/capacity | Yes | resource capacity expressed through amount | PASS | Quantity can be reused without becoming Resource/Capacity itself |
| MA-15 Coordination-burden distribution | No | no new coordination step | N/A | value semantics hidden in normal UX |
| MA-16 Formality/progressive disclosure | Yes | simple unit display vs source/precision details | PASS | progressive disclosure works |
| MA-17 AI authority/multi-party context | Yes | automatic unit conversion | PASS | AI may convert validated equivalents but not invent custom rules/semantic equivalence |
| MA-18 Specialist-system boundary | Yes | health/finance/scientific measurements | PASS | LifeOS reuses value semantics without replacing specialist unit/finance systems |
| MA-19 Multi-actor primitive redundancy | Yes | per-user Quantity objects | PASS | explicitly rejected |
| MA-20 Actor-scoped reality attribution | Limited | shared Observation, actor display preferences | PASS | actor-specific presentation remains separate from reality attribution |

Multi-Actor Gate verdict: **PASS**.

---

# 6. Cross-Concept Consistency Gate

| Test ID | Applicable? | Result | Notes |
|---|---|---|---|
| XCON-01 Identity compatibility | Yes | PASS | Quantity claims no independent identity and therefore does not collide with Observation/Register/Asset |
| XCON-02 Ownership/authority compatibility | Yes | PASS | authority/ownership stay with containing context |
| XCON-03 Planned/current/actual/history compatibility | Yes | PASS | Quantity is reusable value semantics and does not own temporal/historical state |
| XCON-04 Relationship compatibility | Yes | PASS | no hidden hierarchy or universal Quantity entity introduced |
| XCON-05 Multi-actor readiness compatibility | Yes | PASS | shared value + actor-specific display preference remains compatible |
| XCON-06 Language-map compatibility | Yes | PASS WITH HARDENING | promote Quantity from DEFERRED to CANONICAL VALUE SEMANTICS |

Cross-Concept Gate verdict: **PASS** after terminology propagation.

---

# 7. Adjacent Dependency Sweep — transition handling

Data / Subjects is the transition cluster for the new dependency-closure discipline. Dependencies are recorded now and receive final `RESOLVED / SAFE DEFERRED / REOPEN` classification during the post-Cluster-4 closure unless resolved earlier by a Cluster 4 concept.

| Dependency / boundary | Why it matters | Current closure candidate | Owner / future concept or stage | Exact reopening trigger | Tests to rerun |
|---|---|---|---|---|---|
| Quantity ↔ Register aggregation | determines what same-kind values may be summed/averaged/last/trended | RESOLVE DURING CLUSTER 4 | Register | Register candidate requires aggregation semantics that contradict Quantity invariants | CORE-04, CORE-13, XCON-03 |
| Quantity ↔ Money/MonetaryAmount | FX conversion is contextual/time/source-dependent | SAFE DEFERRED candidate | post-Cluster-4 closure / finance value review if needed | finance workflows require currency identity/conversion semantics in core | CORE-03, CORE-07, CORE-13 |
| Quantity ↔ Rating/Scale | ordinal/interval scales are not generic amounts | SAFE DEFERRED candidate | Register/Observation review | rating series cannot be represented without broadening basic Quantity | CORE-04, CORE-08 |
| Quantity ↔ Ratio/Percentage/Count | dimensionless does not imply identical arithmetic semantics | SAFE DEFERRED candidate | Register + GoalCriterion review | core evaluation/aggregation requires a common scalar abstraction incompatible with Quantity v0 | CORE-04, CORE-13 |
| Quantity ↔ custom UnitDefinition | custom conversions may need identity/version/context | SAFE DEFERRED candidate | post-Cluster-4 closure/logical model | shared/versioned custom conversions require lifecycle/authority | CORE-02, CORE-06, MA-06 |
| Quantity ↔ elapsed Duration/calendar time | Time cluster preserves elapsed/calendar distinction | SAFE DEFERRED candidate | dependency closure against Time | Duration requirements contradict basic magnitude/unit semantics | CORE-04, XCON-03 |
| Quantity ↔ Range/Threshold/comparator | scalar amount must remain separate from interval/rule semantics | SAFE DEFERRED candidate | GoalCriterion/Temporal Constraint | ranges/comparators require identity/lifecycle beyond composed values | CORE-03, CORE-04 |
| Quantity ↔ final decimal/unit persistence | precision/conversion implementation pressure | SAFE DEFERRED candidate | logical/physical model | no implementation can preserve semantic precision/source behavior without changing concept | CORE-10, CORE-13 |

No current dependency is a structural blocker to accepting bounded Quantity value semantics.

---

# 8. Adversarial scenario log

| Scenario | What was stressed | Result | Model change required? |
|---|---|---|---|
| Same 66.4 kg used in Observation and Goal criterion | independent history/identity | PASS | no; value semantics reuse |
| 66.4 kg shown as 146.4 lb to another actor | shared reality vs display | PASS | actor presentation separated |
| Garmin sends 5.00 km, LifeOS normalizes 5000 m | source/history integrity | PASS WITH HARDENING | preserve source representation through Provenance |
| 20 °C and 25 °C in a Register | same-unit aggregation | PASS WITH HARDENING | aggregation not owned by Quantity |
| 60% and 70% | dimensionless arithmetic | PASS | percentage semantics not silently generalized |
| 1 scoop = 30 g for product X | custom conversion | PASS WITH DEFERRAL | conversion definition contextual; no universal custom unit rule |
| 100 EUR converted to USD | currency boundary | PASS WITH DEFERRAL | Money not collapsed into ordinary Quantity |
| 1 calendar month vs 30 days | temporal boundary | PASS | accepted Time semantics preserved |
| 120/80 mmHg | composite numeric structure | PASS | do not force into one Quantity |
| priority=2 / version=4 | numeric universality reductio | PASS | number != Quantity |

---

# 9. Reopening / dependency register

Material dependencies are listed in section 7. None currently forces `REOPEN`.

Important reopening triggers:

- Register requires semantics that make Quantity own series/aggregation policy;
- Money/rating/time semantics prove the current definition is over-broad rather than adjacent;
- custom units require independent lifecycle/authority inside basic Quantity;
- implementation cannot preserve precision/source representation without semantic change.

---

# 10. Concept verdict

**PASS WITH HARDENING — accepted current baseline.**

## Rationale

Quantity is necessary as reusable value semantics and remains sharply distinct from Observation, Register, criteria, ranges and historical/domain identity. All identified hardenings can be expressed as bounded invariants without adding a new entity or changing previous clusters.

## Hardenings incorporated before acceptance

- value semantics, not entity;
- number != Quantity;
- property/kind != unit;
- dimension/unit compatibility != semantic equivalence;
- same unit != universal aggregation permission;
- source normalization/display != historical source rewrite;
- custom label != conversion rule;
- Money/calendar-time/Range semantics not absorbed prematurely;
- no final SQL/API shape pre-approved.

## Dependency-sweep summary

- RESOLVED now: Quantity vs Observation; Quantity identity; source/display separation; basic Range/comparator non-collapse.
- Must resolve during Cluster 4: Quantity vs Register aggregation boundary.
- SAFE-DEFER candidates pending formal closure: Money, ratings/scales, ratio/percentage/count, custom UnitDefinition, elapsed Duration boundary, some Range/Threshold details, final persistence.
- REOPEN: 0.

## Mandatory future re-tests

1. Register v0.
2. Data / Subjects cluster integration + multi-actor stress.
3. Deferred Dependency Closure across clusters 1–4.
4. Cross-Cluster Validation v4.
5. GoalCriterion/Relationship review for thresholds/ratios/evaluation.
6. Persistence/API pressure for decimal/unit representation.

---

# 11. Regression corpus additions

Promote the following scenarios:

1. shared measurement displayed in different actor units without data duplication;
2. provider source unit normalized without rewriting source history;
3. same-unit values whose aggregation is semantically invalid;
4. custom unit whose conversion exists only in product/context;
5. calendar-relative time mistaken for elapsed-unit Quantity;
6. currency mistaken for stable physical-unit conversion.

---

# 12. Documentation propagation

Quantity acceptance requires:

- `concepts/quantity.md`;
- this checkpoint;
- promotion in `language-map.md`;
- Domain README update;
- workstream handoff update;
- explicit dependency closure obligations retained for the post-Cluster-4 transition gate.

No change to Observation is required because its accepted boundary already states `Observation != Quantity` and describes Quantity as reusable value/unit semantics.