# Criterion / Evaluation v0 Validation — Methodology v3

**Status:** PASS WITH HARDENING — hardenings incorporated; post-write propagation QA PASS  
**Validated:** 2026-08-15  
**Concept / family:** Criterion / Evaluation v0  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Validation standard:** `../validation-methodology-v3.md`  
**Branch:** `feature/domain-model`  
**Approved pre-scope:** `1cf754e32286814d6ac873bf78bcb1c4c876416d`

---

# 0. Fresh candidate re-score

This review began only after Reconciliation / Source Precedence v0 completed branch-level post-write QA. No next candidate was inherited automatically from the previous ranking.

The remaining Relationships / Reasoning candidate space was freshly re-scored against:

1. current accepted Domain Atlas dependencies;
2. historical SAFE DEFERRED owners/triggers;
3. risk of losing identity/history/Authority/privacy if deferred;
4. cross-cluster leverage;
5. the current Product North Star evidence;
6. whether the issue is truly semantic now or can remain logical/specialist work;
7. product-complexity cost.

The current strongest pressure became Criterion / Evaluation because the accepted model already needs a semantic owner for the relationship among Goal/Milestone, Evidence, materially applicable rule state, historical evaluation, conflict and derived Goal Progress.

The Product North Star added explicit pressure:

```text
Effort != Execution != Outcome != Goal Progress
```

The candidate was therefore selected from current evidence, not because an earlier checkpoint ranked `GoalCriterion / evaluation` highly.

---

# 1. Scope

- **Candidate:** Criterion / Evaluation v0.
- **Goal-scoped name:** GoalCriterion = Criterion used to evaluate a Goal.
- **Date:** 2026-08-15.
- **Primary adjacent concepts:** Goal, Milestone, Evidence, Actual, Outcome, Observation, Version, Reconciliation, Decision, Authority, Visibility.
- **Secondary adjacent areas:** Trigger/conditional policy, Verification/comprehension, Proposal/Request identity, specialist evaluation, retention/materialization, logical/physical/API representation.

## Why this review exists

Existing accepted concepts already state that:

- Goal criteria are separate from Goal identity;
- Milestone != GoalCriterion;
- Milestone attainment is Evidence/evaluation-backed;
- Criterion != Evidence;
- missing Evidence is not automatically negative Evidence;
- historical Evaluation must preserve source/rule material state where consequential;
- Reconciliation can preserve conflicting Evidence without last-write-wins;
- Goal Progress must not be manufactured as a universal percentage.

The unresolved question is no longer whether evaluation semantics exist. It is whether LifeOS requires an explicit bounded Criterion/Evaluation semantic family, and whether that can remain smaller than a universal rule engine/entity/workflow.

Primary risks:

- Goal becoming `target_value + progress_percentage`;
- Criterion collapsing into Evidence or Milestone;
- Evaluation becoming current Goal truth;
- missing data becoming failure;
- conflict being flattened by source recency/count;
- new rules rewriting historical evaluation;
- multiple criteria silently assuming one composition operator;
- shared evaluations leaking private Evidence;
- AI assessments becoming human intention or Authority;
- high-frequency evaluation forcing unbounded persistence.

---

# 2. Evidence reviewed

## EV-01 — Existing LifeOS evidence

Reviewed current accepted semantics and checkpoints, especially:

- `../concepts/goal.md`;
- `../concepts/milestone.md`;
- `../concepts/evidence.md`;
- `evidence-v0-validation.md`;
- `../concepts/version.md`;
- `version-material-equivalence-v0-validation.md`;
- `../concepts/reconciliation.md`;
- `reconciliation-source-precedence-v0-validation.md`;
- `intention-execution-v0.md`;
- `observed-reality-evidence-v0.md`;
- `deferred-dependency-closure-clusters-1-4-v0.md`;
- `cross-cluster-validation-v4.md`;
- current Multi-Actor Readiness, Language Map, README and workstream;
- current Product Identity / North Star on `main` as read-only product evidence.

Material inherited requirements include:

```text
Goal != Criterion
Milestone != GoalCriterion
Criterion != Evidence
missing Evidence != negative Evidence by default
historical evaluation basis must be reconstructible where consequential
current rule/source state != historical rule/source state
conflicting Evidence may remain unresolved
Goal Progress != universal stored percentage
```

**EV-01 result: PASS.**

## EV-02 — Real-world workflow inversion

Representative workflows without LifeOS were reconstructed before mapping:

1. spoken-English B2 Goal evaluated by formal/qualitative assessment rather than hours alone;
2. savings Goal evaluated by accumulated balance;
3. weight-maintenance Goal evaluated over a range and sustained period;
4. training-frequency Goal evaluated over a weekly window;
5. monthly publishing Goal evaluated from external release Outcomes;
6. qualitative social/wellbeing Goal with manual assessment;
7. Milestone attainment supported by external approval/result;
8. incomplete device/import coverage where missing records cannot prove failure;
9. conflicting specialist/self/provider evidence;
10. Criterion change after historical evaluations;
11. shared Goal where supporting Evidence is actor-private;
12. AI-proposed Criterion based on observed patterns.

The recurring real-world structure is:

```text
desired/checkpoint/question
!= evaluation rule
!= source information
!= assessment result
```

**EV-02 result: PASS.**

## EV-03 — Targeted external benchmark

External systems are evidence only; they do not dictate LifeOS ontology.

| Source / pattern | Finding | Classification | LifeOS disposition |
|---|---|---|---|
| HL7 FHIR R5 Goal | Goal separated from target/measure/detail/due/outcome | ADAPT | supports target/evaluation separation |
| HL7 FHIR R5 Goal | multiple targets are expressible | ADAPT | LifeOS must support multiple criteria |
| FHIR clinical lifecycle/status taxonomy | domain-specific status model | NOT APPLICABLE | do not copy as universal Goal/Evaluation status |
| FHIR all-targets-required fulfillment behavior | one composition rule for its resource | ANTI-PATTERN if universalized | LifeOS criteria composition must remain contextual |
| OpenSLO | indicator + target/threshold + time window | ADAPT | supports explicit evaluative window/input/target distinction |
| OpenSLO service reliability objective ontology | metrics/SLO-specific domain | NOT APPLICABLE as kernel ontology | useful benchmark only |
| W3C SHACL | constraints/shapes separated from data graph | ADAPT | Criterion != Evidence/source data |
| W3C SHACL | validation result/report separated from rules/data | ADAPT | Evaluation result can remain distinct |
| W3C SHACL | validation does not mutate input data/shapes | BORROW / ADAPT | Evaluation must not rewrite Evidence/source truth |
| generic RDF validation engine | universal technical validation model | NOT APPLICABLE | do not import as LifeOS rule engine |

External convergence:

```text
criterion / rule
!= evaluated data / Evidence
!= evaluation result
```

**EV-03 result: PASS WITH HARDENING.**

## EV-04 — Candidate minimality

Destructive candidate comparison:

```text
A. Goal + Evidence only, no Criterion owner
FAIL — evaluation rule/history/composition leaks into Goal/Evidence

B. universal target_value/progress fields on Goal
FAIL — cannot represent sustained, qualitative, external, composite or unknown semantics honestly

C. universal GoalCriterion entity/root
FAIL — Goal-scoped naming does not justify universal independent identity/root

D. universal Evaluation entity/workflow
FAIL — most low-consequence evaluations may be transient/derived; one lifecycle/state machine is artificial

E. contextual Criterion capability
+ contextual Evaluation process/result semantics
+ GoalCriterion as Goal-scoped use
+ Goal Progress as derived projection
SURVIVES
```

**EV-04 result: PASS.**

---

# 3. Candidate definition

> **Criterion is the contextual evaluative specification through which LifeOS defines what condition, rule, threshold, pattern, checkpoint, assessment or combination is relevant when evaluating a bounded target for a defined purpose and context. Evaluation is the contextual application of the materially applicable Criterion state to relevant Evidence under the applicable target, time/window, Authority/policy and material-state context, producing an assessment without rewriting the underlying Evidence, Actual, Outcome, Milestone or target identity.**

## Domain question answered

> **Under which applicable rule should this bounded target be evaluated, using which relevant Evidence and material states, and what assessment follows for this evaluation context?**

## Identity

- Criterion has contextual evaluative semantics and may require materially distinguishable state/history where consequence requires it.
- Criterion is not a universal native identity/root.
- GoalCriterion is Goal-scoped Criterion semantics, not a second primitive.
- Evaluation is contextual process/result semantics; durable identity is consequence-sensitive rather than universal.

## Independent/contextual existence

- Goal without explicit Criterion: valid; may be unevaluated, qualitative or not yet operationalized.
- Criterion without Evidence at a given time: valid; Evaluation may remain unknown/insufficient.
- Evidence without Criterion/evaluation: valid source information, but not Evidence for that target/context.
- Evaluation without relevant Criterion semantics: invalid as a Criterion-based assessment; a human Decision/judgment may still exist separately.
- Evaluation without persisted record: valid for transient/derived low-consequence cases.

## Nearest boundaries

```text
Goal != Criterion
Milestone != Criterion
Criterion != Evidence
Evaluation != Evidence
Evaluation != Actual / Outcome
Criterion != Temporal Constraint
Criterion != Trigger
Evaluation != Decision
Evaluation != Reconciliation
Evaluation != Authority
Evaluation != Confirmation
Evaluation result != effective target state automatically
```

## Deliberate deferrals

- final logical/physical Criterion representation;
- comparator/range/threshold reusable value structures;
- composite Criterion AST/expression/DSL representation;
- Trigger/conditional policy/action semantics;
- Verification/comprehension;
- Proposal/Request identity for proposed Criterion changes;
- specialist scoring/adjudication models;
- retention/materialized Evaluation snapshots;
- API/SQL/cardinality/indexing/caching.

---

# 4. Core Semantic Validation Gate

| Test ID | Applicable? | Evidence / scenario | Result | Finding / hardening / deferral |
|---|---:|---|---|---|
| CORE-01 Workflow inversion | yes | B2, savings, maintenance, weekly frequency, qualitative Goals | PASS | rule/input/result separation improves reality representation |
| CORE-02 Deep chronology | yes | C1 -> later Evidence -> C2 effective later -> historical query | PASS WITH HARDENING | preserve applicable Criterion/source/target states and evaluation window/time |
| CORE-03 Reductio | yes | remove/merge/universalize Criterion/Evaluation/progress | PASS WITH HARDENING | universal target/progress/evaluation object fails |
| CORE-04 Redundancy | yes | Goal, Milestone, Evidence, Trigger, Decision, Reconciliation, Version | PASS WITH HARDENING | boundaries distinct; GoalCriterion is scoped use, not new root |
| CORE-05 Traceability | yes | Goal -> Criterion -> Evidence; imported reality -> later relevance; one source -> several Goals | PASS | no source duplication or fabricated historical intent |
| CORE-06 Orphan/independence | yes | Goal with zero criteria; criterion with no Evidence; transient evaluation | PASS WITH HARDENING | contextual capability, consequence-sensitive persistence |
| CORE-07 External benchmark | yes | FHIR/OpenSLO/SHACL | PASS | adopt separation, not external schemas |
| CORE-08 Anti-pattern review | yes | universal score/status/target/progress/DSL/latest-wins | PASS | all rejected as universal defaults |
| CORE-09 Correction/reconciliation/epistemic integrity | yes | missing data, source correction, conflicting providers, rule change | PASS WITH HARDENING | unknown remains unknown; conflict may remain indeterminate; history not rewritten |
| CORE-10 Scale/performance/history | yes | rolling windows, 10-year history, sensor data, many Goals | PASS WITH HARDENING | no one persisted evaluation/edge per query/tick |
| CORE-11 Simple vs power user | yes | natural UI vs explainable source/rule/history | PASS | ontology may remain hidden |
| CORE-12 Product value/complexity cost | yes | reduce false progress without rule bureaucracy | PASS WITH HARDENING | progressive disclosure; defaults must remain simple |
| CORE-13 Implementation pressure | yes | query historical basis/current result/private Evidence/conflict | PASS WITH HARDENING | queryability required; no final SQL/API/DSL chosen |

## Core-gate chronology

```text
T0 Goal = train regularly
T1 Criterion C1 = >= 3 qualifying Sessions/week
T2 W1 has two known qualifying Sessions
T3 third workout occurs outside LifeOS but is not imported
T4 end-of-week Evaluation E1 = unknown/insufficient under non-complete source policy
T5 external provider imports third qualifying Actual
T6 W1 can be reevaluated using later Evidence; E1 remains historically explainable if material
T7 user changes Criterion to C2 = >= 4/week, effective next week
T8 W1 remains evaluated under C1, not retroactively C2
T9 provider conflicts with user about one workout
T10 Reconciliation may resolve or preserve conflict unresolved; Evaluation must not invent certainty
```

## Core hardenings incorporated

```text
CRIT-H01 Goal != Criterion
CRIT-H02 Milestone != Criterion
CRIT-H03 GoalCriterion = Goal-scoped Criterion semantics, not separate universal primitive
CRIT-H04 Criterion != Evidence
CRIT-H05 Evaluation != Evidence / Actual / Outcome / Confirmation
CRIT-H06 Criterion != Temporal Constraint / Trigger
CRIT-H07 Evaluation != Decision / Reconciliation / Authority
CRIT-H08 missing Evidence != failure by default
CRIT-H09 unknown/insufficient Evidence may remain unknown/indeterminate
CRIT-H10 absence becomes negative only under explicit justified completeness/negative-observation semantics
CRIT-H11 conflicting Evidence may remain unresolved/indeterminate
CRIT-H12 no universal newest/most-frequent/highest-confidence winner
CRIT-H13 historical Evaluation preserves/reconstructs materially applicable target/Criterion/Evidence states
CRIT-H14 later Criterion change does not rewrite earlier rule applicability
CRIT-H15 current reevaluation may differ without erasing prior material Evaluation
CRIT-H16 multiple criteria do not imply universal AND/OR/weighted-average rule
CRIT-H17 Goal Progress is derived/evaluation projection
CRIT-H18 no universal progress percentage/score/confidence/status
CRIT-H19 Evaluation result does not own effective/current target state
CRIT-H20 persistence/materialization is consequence-sensitive
```

```text
CORE GATE
PASS WITH HARDENING
```

All mandatory hardenings were incorporated into `../concepts/criterion-evaluation.md` before acceptance.

---

# 5. Multi-Actor Compatibility Gate

| Test ID | Applicable? | Evidence / scenario | Result | Finding / hardening / deferral |
|---|---:|---|---|---|
| MA-01 Identity/account independence | yes | external subject/source/evaluator without Account | PASS | Criterion/Evidence roles do not depend on `user_id` |
| MA-02 Shared fact/actor overlay | yes | shared Goal with actor-private Evidence | PASS WITH HARDENING | shared result != shared source visibility |
| MA-03 Responsibility/assignment/claim | yes | evaluator/recorder/responsible actor can differ | PASS | evaluation does not absorb Responsibility |
| MA-04 Stewardship/mental load | yes | manual review of missing/conflicting Evidence | PASS WITH PRODUCT HARDENING | automate where safe; do not shift monitoring burden silently |
| MA-05 Common ground/state separation | yes | canonical Criterion vs individual Ack/Agreement/Consent | PASS | criterion application does not fabricate actor assent |
| MA-06 Authority/canonical change | yes | who may set/change shared Criterion vs who evaluates | PASS WITH HARDENING | evaluator/source/creator != Authority automatically |
| MA-07 Selective disclosure | yes | private health/finance Evidence -> bounded shared result | PASS WITH HARDENING | result visibility independent from Evidence visibility |
| MA-08 Inference privacy | yes | AI explanation/ranking from private Evidence | PASS WITH HARDENING | explanation/tool arguments cannot leak hidden basis |
| MA-09 Partial adoption/external participant | yes | external provider/person supplies Evidence | PASS | no synthetic Account needed |
| MA-10 Assisted participation/provenance | yes | caregiver/helper records/evaluates for another | PASS WITH HARDENING | actual Actor, subject, represented party and basis remain distinct |
| MA-11 Relationship lifecycle/revocation | yes | access/Authority revoked after historical evaluation | PASS WITH HARDENING | future capability changes; historical attribution remains where policy permits |
| MA-12 Conflict/adversarial relationship | yes | actors disagree on criterion/admissibility/evidence | PASS WITH HARDENING | disagreement not flattened into one truth |
| MA-13 Unequal power | yes | manager/clinician/guardian criterion context | PASS WITH HARDENING | bounded Authority does not expand all visibility/autonomy |
| MA-14 Multi-resource/capacity | limited | resource/capacity facts used as Evidence | PASS | Evaluation does not absorb allocation/capacity identity |
| MA-15 Coordination-burden distribution | yes | who sets rule, supplies data, reviews exceptions | PASS WITH PRODUCT HARDENING | benefit/burden must be distributed consciously |
| MA-16 Formality/progressive disclosure | yes | casual Goal vs regulated/specialist assessment | PASS | same kernel can remain simple or auditable |
| MA-17 AI authority/multi-party context | yes | AI proposes/executes Evaluation | PASS WITH HARDENING | AI authority <= principal/context/policy; no human-state fabrication |
| MA-18 Specialist-system boundary | yes | exam/clinical/workforce source of record | PASS | bounded specialist authority, no universal precedence/imported ontology |
| MA-19 Multi-actor primitive redundancy | yes | shared Evaluation/GoalCriterion entities | PASS | no SharedCriterion/SharedEvaluation primitive required |
| MA-20 Actor-scoped reality attribution | yes | shared target with actor-specific Evidence/consequences | PASS WITH HARDENING | shared Actual/Outcome does not imply identical actor evaluation |

## Multi-actor hardenings incorporated

1. criterion-setting Authority is separate from evaluator/source/subject/creator;
2. shared Goal does not imply shared Evidence visibility;
3. group membership/Participation does not imply Agreement to a Criterion;
4. actor-private Evidence may support a bounded shared result without source disclosure;
5. assisted/represented evaluation preserves actual Actor and represented party;
6. revocation changes future access/Authority without rewriting legitimate historical evaluation attribution;
7. specialist authority/source-of-record remains target/facet/context bounded;
8. AI may calculate/propose but cannot fabricate human intention, Agreement, Consent, Acknowledgement or Authority;
9. conflicting actor positions may remain unresolved;
10. product formality and coordination burden remain consequence-sensitive.

```text
MULTI-ACTOR GATE
PASS WITH HARDENING
```

---

# 6. Cross-Concept Consistency Gate

| Test ID | Applicable? | Result | Notes |
|---|---:|---|---|
| XCON-01 Identity compatibility | yes | PASS | Criterion/Evaluation does not claim Goal/Milestone/Evidence/Decision identity |
| XCON-02 Ownership/Authority compatibility | yes | PASS WITH HARDENING | evaluation does not establish Authority/current state merely by producing a result |
| XCON-03 Planned/current/Actual/history compatibility | yes | PASS WITH HARDENING | desired rule, source reality, evaluation then/current reevaluation remain separable |
| XCON-04 Relationship compatibility | yes | PASS | no universal hierarchy/root or source duplication required |
| XCON-05 Multi-actor readiness compatibility | yes | PASS WITH HARDENING | shared target + actor-private Evidence/common-ground separation survives |
| XCON-06 Language-map compatibility | yes | PASS WITH UPDATE REQUIRED | Criterion/Evaluation promoted; Goal Progress remains derived; old generic deferral must be downstream-closed |

```text
XCON GATE
PASS WITH HARDENING
```

No accepted concept requires structural reopening.

---

# 7. Adjacent Dependency Sweep

Every material adjacent question is classified below. No `TBD` or unnamed future owner remains.

| Dependency / boundary | Why it matters | Closure class | Current resolution / why safe to defer | Owner / future stage | Exact reopening trigger | Tests to rerun |
|---|---|---|---|---|---|---|
| Goal ↔ Criterion | desired meaning vs evaluative rule | RESOLVED | separate identities/semantics; Criterion change may preserve Goal if desired meaning survives | Goal / whole-domain regression | Criterion edits repeatedly hide desired-state replacement | CORE-03/04/06/09, XCON-01/03 |
| Milestone ↔ Criterion | checkpoint vs rule | RESOLVED | Criterion may reference/evaluate Milestone; attainment remains evaluation-backed | Milestone | attainment cannot be represented without duplicate reality | CORE-04/05/09, XCON-03/04 |
| Evidence ↔ Criterion | input vs rule | RESOLVED | explicit non-collapse | Evidence | Evidence requires rule ownership/source duplication | CORE-03/04/05/09, XCON-04 |
| Evidence ↔ Evaluation | source use vs assessment | RESOLVED | Evaluation consumes Evidence without rewriting it | Evidence/Version | historical basis cannot remain attributable | CORE-02/09/10/13 |
| Actual/Outcome ↔ Evaluation | reality/result vs assessment | RESOLVED | source reality may influence many evaluations | reality cluster | current assessment must overwrite source truth | CORE-04/05/09, XCON-03 |
| Decision ↔ Evaluation | explicit resolution vs calculated/judged assessment | RESOLVED | deterministic evaluation need not fabricate Decision | Decision | every material evaluation requires independent resolution identity | CORE-03/04, MA-06, XCON-02 |
| Reconciliation ↔ Evaluation | conflict handling vs assessment | RESOLVED | unresolved conflict may yield indeterminate Evaluation; reconciliation remains separate | Reconciliation | evaluation cannot handle conflicting Evidence without owning conflict process | CORE-09, MA-12, XCON-03/04 |
| Authority ↔ Evaluation | who may effect/change vs what assessment says | RESOLVED | Evaluation does not grant governance power/current-state ownership | Authority/security | evaluation output must itself establish Authority | CORE-04, MA-06/13/17, XCON-02 |
| Version ↔ Criterion state | historical rule applicability | RESOLVED | material rule/source/target state binding follows Version discipline | Version/logical | evaluation history cannot be reconstructed without new universal version root | CORE-02/09/13, XCON-03 |
| Visibility ↔ Evaluation/Evidence | shared result vs private basis | RESOLVED | independently governed | Visibility/privacy | result cannot be shared without leaking source | MA-07/08/13/17, XCON-05 |
| Goal Progress ↔ Evaluation | projection vs canonical state | RESOLVED | Progress derived from applicable Goal evaluation semantics | Goal/product | progress requires universal persisted percentage to remain coherent | CORE-03/10/12/13 |
| Trigger / conditional policy | evaluation result may cause action | SAFE DEFERRED | Evaluation can exist without deciding downstream effect | Trigger/automation review | Criterion must embed firing/action semantics to represent ordinary automation | CORE-03/04/13, MA-06/17, XCON-02/04 |
| comparator/range/threshold reusable representation | common numeric/value forms | SAFE DEFERRED | semantic forms known; no universal value hierarchy needed yet | Quantity/value + logical model | common criteria cannot be represented/queryable without stronger shared value semantics | CORE-04/10/13, XCON-01/04 |
| composite Criterion representation | AND/OR/alternatives/weighted/temporal composition | SAFE DEFERRED | composition must be explicit/contextual; universal operator not assumed | evaluation logical model | common composite cases require changing Criterion identity/boundary | CORE-03/10/13, MA-16/18, XCON-04 |
| Verification / comprehension | checking validity/process vs evaluation | SAFE DEFERRED | semantically separable now | Verification/Evidence review | specialist verification cannot remain separate from Evaluation/Evidence | CORE-03/04/09, MA-18, XCON-04 |
| specialist evaluation/adjudication | formal domain scoring/certification | SAFE DEFERRED | adapters/extensions can own bounded domain rules | specialist domain/extensions | several specialist domains require one stronger common lifecycle/identity | CORE-07/13, MA-13/18, XCON-02/05 |
| retention / materialized Evaluation snapshots | history vs privacy/volume | SAFE DEFERRED | transient/derived vs consequential snapshot distinction is sufficient semantically | privacy/retention + logical model | required history cannot coexist with minimization/recomputation strategy | CORE-02/09/10/13, MA-07/11, XCON-03 |
| Proposal/Request identity for Criterion changes | proposed rule != effective rule | SAFE DEFERRED | Criterion can distinguish proposal from effective state using existing governance semantics without universal Proposal root now | Proposal/Request review | cross-family proposed Criterion changes cannot be targeted/reviewed/versioned precisely | CORE-04/09/13, MA-05/06/17, XCON-02/04 |
| physical/logical/API representation | queryability/cardinality/materialization | SAFE DEFERRED | semantics fixed without table/API commitment | logical/physical model | no representation preserves identity/history/privacy/performance invariants | CORE-10/13, XCON-01/03/05 |

```text
REOPEN                         0
unclassified material items    0
```

---

# 8. Adversarial scenario log

| Scenario | What was stressed | Result | Model change required? |
|---|---|---|---|
| 10 hours English study but no proficiency assessment | Effort vs Goal Progress | PASS | Criterion prevents effort=progress collapse |
| one in-range weight reading vs six-month maintenance | sustained semantics | PASS WITH HARDENING | evaluation period/coverage required |
| device offline, only two workouts visible | missing Evidence | PASS WITH HARDENING | unknown/insufficient rather than automatic failure |
| third workout imported later | reevaluation/history | PASS | current reevaluation may change while prior basis remains historical |
| criterion changes 3/week -> 4/week | rule Version/effective applicability | PASS WITH HARDENING | prior periods stay under old rule |
| official exam and self-assessment conflict | conflicting Evidence | PASS WITH HARDENING | may reconcile or remain indeterminate |
| one shared Goal with private health Evidence | selective disclosure | PASS WITH HARDENING | result/basis Visibility separated |
| three criteria, one unknown | composition/unknown | PASS WITH HARDENING | no invented average/pass; composition contextual |
| AI proposes Criterion after seeing data | historical intention | PASS WITH HARDENING | proposal does not become retroactive human Goal meaning |
| specialist source authoritative for one facet only | source-of-record scope | PASS | bounded specialist authority, no global rank |
| helper records/evaluates for another Person | representation/provenance | PASS WITH HARDENING | actual Actor/subject/represented party remain distinct |
| high-frequency rolling evaluation | scale/materialization | PASS WITH HARDENING | no universal persisted Evaluation per tick |

---

# 9. Reopening / dependency register

| Finding | Severity | Closure class | Current treatment | Owner / future stage | Reopening trigger |
|---|---|---|---|---|---|
| Goal identity vs Criterion state | STRUCTURAL | RESOLVED | explicit separation + identity guard | Goal/whole-domain | Criterion edits hide desired-state replacement |
| missing Evidence semantics | STRUCTURAL | RESOLVED | unknown/insufficient allowed; completeness rule required for negative meaning | Criterion/Evidence | product cannot distinguish unknown from failed |
| conflicting Evidence | HARDENING | RESOLVED | indeterminate + Reconciliation boundary | Reconciliation | Evaluation must become conflict owner |
| historical rule applicability | STRUCTURAL | RESOLVED | Version binds material Criterion/source/target states | Version/logical | past evaluation cannot be explained |
| multiple-criteria composition | DEFERRED DEPENDENCY | SAFE DEFERRED | composition explicit/contextual, representation open | logical evaluation model | real cases require Criterion redesign |
| Trigger/action after evaluation | DEFERRED DEPENDENCY | SAFE DEFERRED | downstream effect separate | Trigger/automation | Criterion must own action firing |
| Verification/comprehension | DEFERRED DEPENDENCY | SAFE DEFERRED | checking process remains distinct | Verification | specialist use proves inseparable |
| specialist scoring/adjudication | DEFERRED DEPENDENCY | SAFE DEFERRED | bounded adapters/extensions | specialist domains | common stronger lifecycle becomes unavoidable |
| materialized snapshots/retention | DEFERRED DEPENDENCY | SAFE DEFERRED | consequence-sensitive persistence | privacy/logical | history/minimization cannot coexist |
| proposed Criterion changes | DEFERRED DEPENDENCY | SAFE DEFERRED | proposal/effective state distinction can remain contextual | Proposal/Request | cross-family reusable identity becomes necessary |
| AI authority | HARDENING | RESOLVED | proposal/calculation != intention/Authority/common ground | AI/application | AI action cannot remain bounded without stronger semantics |
| universal progress/score | STRUCTURAL | RESOLVED | derived contextual projection only | product/logical | user value requires universal score without semantic distortion |

```text
REOPEN 0
```

---

# 10. Concept verdict

- [ ] PASS
- [x] PASS WITH HARDENING
- [ ] REOPEN
- [ ] DEFERRED DEPENDENCY

## Rationale

Criterion / Evaluation survives removal, merge, universalization, chronology, correction, conflict, multi-actor, privacy, AI, specialist, scale and product-complexity pressure.

The accepted model is intentionally smaller than a universal rule engine:

```text
Criterion
= contextual evaluative specification/capability

GoalCriterion
= Goal-scoped Criterion semantics

Evaluation
= contextual application/process-result semantics

Goal Progress
= derived projection
```

No universal Criterion root/table, Evaluation entity/workflow, progress percentage, score, confidence model or composition operator is accepted.

## Hardenings incorporated before acceptance

All CRIT-H01..20 core hardenings plus the multi-actor hardenings above are incorporated into `../concepts/criterion-evaluation.md` and re-tested through CORE/MA/XCON.

## Dependency-sweep summary

```text
REOPEN                         0
unclassified material items    0
```

Every material remaining question is explicitly SAFE DEFERRED with owner, trigger and tests.

## Mandatory future re-tests

- Criterion composition / logical representation;
- Trigger/conditional policy;
- Verification/comprehension;
- Proposal/Request identity;
- specialist evaluation boundaries;
- retention/materialized snapshots;
- logical/physical/API pressure;
- Cluster-5 integration and multi-actor stress;
- whole-domain semantic/multi-actor regression.

---

# 11. Cluster-only integration section

**N/A — justified.**

Relationships / Reasoning candidate space remains open. Criterion / Evaluation v0 does not authorize a cluster verdict or preselect the next candidate.

After clean post-write QA:

```text
fresh remaining-candidate re-score
→ select one family only
→ full Methodology v3
```

---

# 12. Regression corpus additions

| ID | Scenario | New boundary covered | Reuse trigger |
|---|---|---|---|
| R-CRIT-01 | 10h study but no B2 evidence | Effort != Goal Progress | Goal analytics/evaluation |
| R-CRIT-02 | one in-range reading vs six-month maintenance | sustained evaluation/window | maintenance goals |
| R-CRIT-03 | device offline with missing workout | absence != failure | incomplete provider data |
| R-CRIT-04 | late import changes current weekly evaluation | reevaluation vs historical basis | delayed sync/import |
| R-CRIT-05 | criterion changes 3/week -> 4/week | rule material state/effective applicability | Goal edits/versioning |
| R-CRIT-06 | official exam vs self-assessment conflict | conflict/indeterminate | specialist + personal evidence |
| R-CRIT-07 | shared Goal + private Evidence | selective disclosure | collaboration/privacy |
| R-CRIT-08 | one unknown among multiple criteria | composition + unknown | aggregate Goal progress |
| R-CRIT-09 | AI proposes criterion after seeing data | no retroactive intention | adaptive AI |
| R-CRIT-10 | specialist source authoritative for one facet | bounded source-of-record | specialist integrations |
| R-CRIT-11 | helper evaluates for represented Person | Actor/subject/representation | caregiving/assisted use |
| R-CRIT-12 | rolling high-frequency evaluation | persistence scale | sensors/continuous analytics |

---

# 13. Documentation propagation

Approved pre-scope:

```text
1cf754e32286814d6ac873bf78bcb1c4c876416d
```

Approved exact scope:

## CREATE — 2

1. `docs/domain/concepts/criterion-evaluation.md`
2. `docs/domain/checkpoints/criterion-evaluation-v0-validation.md`

## UPDATE — 16

3. `docs/domain/concepts/goal.md`
4. `docs/domain/concepts/milestone.md`
5. `docs/domain/concepts/evidence.md`
6. `docs/domain/concepts/version.md`
7. `docs/domain/concepts/reconciliation.md`
8. `docs/domain/checkpoints/evidence-v0-validation.md`
9. `docs/domain/checkpoints/version-material-equivalence-v0-validation.md`
10. `docs/domain/checkpoints/reconciliation-source-precedence-v0-validation.md`
11. `docs/domain/checkpoints/intention-execution-v0.md`
12. `docs/domain/checkpoints/observed-reality-evidence-v0.md`
13. `docs/domain/checkpoints/deferred-dependency-closure-clusters-1-4-v0.md`
14. `docs/domain/checkpoints/cross-cluster-validation-v4.md`
15. `docs/domain/multi-actor-readiness-v1-part-3.md`
16. `docs/domain/language-map-part-5.md`
17. `docs/domain/README-part-3.md`
18. `docs/workstreams/domain-model-part-2.md`

## DELETE — 0

Propagation discipline:

> Historical checkpoints are append-only evidence. Existing reasoning, rejected alternatives, scenarios, old SAFE DEFERRED state and earlier QA records are preserved; later downstream closure amendments state the current resolution without pretending the dependency was already closed during the earlier review.

Current split documents preserve their canonical split structure; only their current downstream state is amended.

Explicitly out of scope:

```text
main
main synchronization
backend
SQL / migrations
API
auth / Principal implementation
prototype / frontend
logical / physical model
Trigger
Proposal / Request
Verification
Resource Requirement / Allocation
collective / group semantics
next candidate selection
historical-record deletion/rewrite
docs/domain/concepts/relationship.md
```

---

# 14. Post-write QA requirements

This checkpoint is semantically accepted but branch propagation is not QA-closed until the approved commit is written and verified against the exact pre-scope.

Required post-write checks:

```text
branch = feature/domain-model
pre-scope = 1cf754e32286814d6ac873bf78bcb1c4c876416d
exact changed paths = 18 / 18
CREATE = 2 / 2
UPDATE = 16 / 16
DELETE = 0
out-of-scope paths = 0
```

Semantic/document checks:

- concept file complete;
- EV-01..04 present;
- CORE-01..13 complete;
- MA-01..20 complete;
- XCON-01..06 complete;
- Adjacent Dependency Sweep complete;
- every material deferral has owner + exact trigger + tests;
- adversarial/reopening/regression sections complete;
- `PASS WITH HARDENING` hardenings incorporated;
- `REOPEN = 0`;
- unclassified material dependencies = 0;
- Goal/Milestone/Evidence/Version/Reconciliation boundaries preserved;
- historical checkpoint text preserved with downstream append-only closure;
- Language Map/README/Multi-Actor/workstream current-state coherent;
- Goal Progress remains derived;
- no universal GoalCriterion/Evaluation root/table/workflow/score/progress default introduced;
- no `docs/domain/concepts/relationship.md` created;
- no next candidate preselected;
- `main`, prototype, SQL/API/backend/auth untouched.

Only after those checks pass may this checkpoint be marked `post-write QA PASS` and the approval considered consumed.

---

# 15. Final post-write QA closure — 2026-08-15

Criterion / Evaluation v0 is QA-closed on `feature/domain-model`.

The original approved semantic scope began at:

```text
1cf754e32286814d6ac873bf78bcb1c4c876416d
```

The two new canonical files were created first, leaving the branch at:

```text
bf5c9bd497af699f61ac6c80177117b6a6bbf175
```

The approved 16-path propagation was then completed and remotely verified at:

```text
47fce09ee7bc546485c1c91b13ee52aea629fade
```

Final semantic-scope QA:

```text
approved unique paths          18 / 18
CREATE                           2 / 2
UPDATE                          16 / 16
DELETE                           0
out-of-scope paths               0
historical preservation          PASS
REOPEN                           0
unclassified material items      0
```

The apparent single-line deletions reported by Git on ten append-only files were verified as EOF newline normalization: the former final content line was reinserted unchanged before the downstream amendment. No historical reasoning, verdict, scenario, hardening, SAFE DEFERRED item or QA evidence was removed.

Repository guards were also verified:

```text
main = 2739e96955974d1273e704905ace03f9ac478e05
main changed by this scope = no
docs/domain/concepts/relationship.md = absent by design
backend / SQL / API / auth / prototype = untouched
next candidate = not preselected
```

The status marker in this checkpoint is therefore promoted from `pending post-write propagation QA` to `post-write propagation QA PASS` without changing the accepted Criterion / Evaluation semantics.

This marker-closure write is separately scoped from propagation itself:

```text
marker-closure pre-scope = 47fce09ee7bc546485c1c91b13ee52aea629fade
marker-closure paths     = 1 UPDATE
marker-closure path      = docs/domain/checkpoints/criterion-evaluation-v0-validation.md
```

No next Relationships / Reasoning candidate is selected here. The next semantic action is a fresh re-score of the remaining candidate space under Methodology v3.