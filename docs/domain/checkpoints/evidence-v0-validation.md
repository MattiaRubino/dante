# Evidence v0 Validation — Methodology v3

**Status:** PASS WITH HARDENING — accepted current baseline  
**Date:** 2026-08-11  
**Concept:** Evidence v0  
**Workstream:** Core Domain Model v0 — Observed Reality & Evidence  
**Methodology:** `../validation-methodology-v3.md`

---

# 1. Scope

This checkpoint validates whether LifeOS requires distinct Evidence semantics and whether that concept remains bounded when separated from source facts, Observation, Actual, Outcome, Confirmation, Provenance, GoalCriterion, Milestone, and future Decision/Relationship semantics.

Primary risks:

- treating every fact as Evidence by default;
- copying source data into every evaluation context;
- interpreting Evidence as universal proof;
- equating absence of data with negative Evidence;
- collapsing Evidence with Provenance/Confirmation;
- introducing one universal confidence score;
- materializing an unbounded Evidence graph in persistence;
- leaking private source information through shared evaluations or AI explanations.

Candidate under test:

> Evidence is a contextual evaluative role/relationship played by information when it materially bears on a specific evaluation target.

---

# 2. Evidence basis

## EV-01 — Existing LifeOS evidence

Reviewed:

- Goal v0 evidence/progress requirements;
- Milestone v0 attainment/evidence distinction;
- Actual v0;
- Outcome v0;
- Observation v0;
- Confirmation v0;
- feature-discovery simulations;
- multi-actor discovery/research;
- Validation Methodology v3.

Result: **PASS**.

The existing model repeatedly requires information to be reused as progress/evaluation input without rewriting source identity or historical intent.

## EV-02 — Real-world workflow evidence

Representative workflows:

1. weight measurements used for maintenance-goal evaluation;
2. workout Actuals used for weekly frequency criteria;
3. exam score + result used for Goal/Milestone evaluation;
4. design-review result used for approval checkpoint;
5. conflicting sensor/provider records used in reconciliation;
6. private facts used to derive a shareable scheduling consequence;
7. historical information becoming relevant to a later-created Goal.

Result: **PASS**.

## EV-03 — Targeted external benchmark

Reviewed mature patterns from:

- W3C PROV — provenance remains distinct from information use/evaluation;
- W3C Verifiable Credentials — claims/credentials may carry contextual evidence without evidence becoming the claim or issuer/subject identity;
- HL7 FHIR R5 Evidence — specialist evidence representation demonstrates contextual variables/statistics/certainty while being too research-specific for direct LifeOS adoption.

Classification:

| Pattern | Result |
|---|---|
| source information remains distinct | BORROW |
| contextual evidence use | ADAPT |
| provenance != evidence | BORROW |
| certainty depends on evidence context | ADAPT |
| specialist research Evidence resource | NOT APPLICABLE as kernel model |
| one universal evidence score | ANTI-PATTERN |

Result: **PASS WITH HARDENING**.

## EV-04 — Candidate minimality

Tested stronger alternatives:

- no Evidence concept;
- Evidence == Observation;
- Evidence == Provenance;
- Evidence == Confirmation;
- Evidence == GoalCriterion;
- generic persisted Evidence entity for every relationship.

The minimal surviving model is semantic role/relation plus deferred persistence strategy.

Result: **PASS**.

---

# 3. Core Semantic Validation Gate

## CORE-01 — Real-World Workflow Inversion

Without LifeOS, people commonly:

- collect facts in trackers/apps/files;
- later decide which facts matter to a question;
- interpret contradictory sources;
- reuse the same information in multiple assessments;
- distinguish source reliability from relevance;
- make decisions while some evidence is missing.

LifeOS improves this by preserving source identity while making evaluative relevance explicit/reconstructible.

Failure avoided: requiring users to duplicate facts into each Goal/assessment.

Result: **PASS**.

## CORE-02 — Deep Chronological Simulation

Chronology tested:

```text
T1 Observation captured independently
T2 new Goal/criterion created
T3 old Observation becomes relevant Evidence
T4 contradictory provider record arrives
T5 source Observation corrected
T6 evaluation recomputed
T7 criterion changes
T8 historical query asks what evidence supported the old conclusion
```

Required distinctions survive:

- source creation time != Evidence-relevance discovery time;
- source correction != silent historical evaluation rewrite;
- new Evidence can change current evaluation without pretending it existed earlier;
- past evaluation can retain its then-applicable Evidence/rule basis where consequential.

Result: **PASS WITH HARDENING**.

Hardening: future evaluation/version model must preserve or reconstruct material historical Evidence basis.

## CORE-03 — Adversarial Reductio

### REMOVE

Without Evidence, LifeOS cannot distinguish information existence from evaluative relevance without embedding source semantics inside every evaluator.

Result: **FAIL alternative**.

### MERGE with Observation

Fails because one Observation can be Evidence for A, Evidence against B, and irrelevant to C.

Result: **FAIL alternative**.

### MERGE with Confirmation

Fails because Confirmation does not define evaluative target/relevance.

Result: **FAIL alternative**.

### MERGE with Outcome/Actual

Fails because Actual/Outcome can later become Evidence without losing realization/result meaning.

Result: **FAIL alternative**.

### MERGE with Provenance

Fails because source history can remain stable while evaluative relevance changes.

Result: **FAIL alternative**.

### MAKE UNIVERSAL PROOF OBJECT

Fails because Evidence may contradict/qualify and may be weak/context-limited.

Result: **FAIL alternative**.

### MAKE UNIVERSAL PERSISTED EDGE

Fails scale/product simplicity: deterministic Evidence uses may be derived, while only consequential evaluations need materialized history.

Result: **FAIL alternative**.

Candidate relation/use model survives.

Result: **PASS**.

## CORE-04 — Semantic Redundancy / Merge-Split Pair Test

| Pair | Classification | Reason |
|---|---|---|
| Evidence / Observation | DISTINCT | fact assertion vs evaluative use |
| Evidence / Actual | DISTINCT | realization vs evaluative use |
| Evidence / Outcome | DISTINCT | result vs evaluative use |
| Evidence / Confirmation | DISTINCT | attestation vs relevance/use |
| Evidence / Provenance | DISTINCT | origin/derivation vs relevance/use |
| Evidence / GoalCriterion | DISTINCT | evaluation rule/question vs input |
| Evidence / Milestone | DISTINCT | checkpoint vs information used to establish it |
| Evidence / typed Relationship | DEFERRED | Evidence may later be implemented as typed relation semantics |

Result: **PASS WITH DEFERRED DEPENDENCY**.

## CORE-05 — Multidirectional Traceability

Downward:

```text
Goal -> Criterion -> Evidence selection -> evaluation
```

Upward:

```text
Observation/Actual/import
-> later-discovered Evidence relevance
-> Goal/review
```

without fabricated historical intent.

Lateral:

```text
one source record
-> several independent evaluations
```

without duplication.

Result: **PASS**.

## CORE-06 — Orphan / Independence

- Observation without Evidence: YES.
- Actual without Evidence: YES.
- Outcome without Evidence: YES.
- Evidence without an evaluative target/context: NO meaningful Evidence semantics; it remains merely source information.
- Evaluation target without Evidence: YES; may be unevaluated/unknown or manually assessed depending semantics.

Evidence therefore has **contextual relational identity**, not independent universal fact identity.

Result: **PASS**.

## CORE-07 — External Cross-Domain Benchmark

External systems support separation of:

- source/claim;
- provenance;
- evidence/supporting information;
- certainty/interpretation.

LifeOS adopts the separation but rejects specialist research schemas as universal kernel design.

Result: **PASS**.

## CORE-08 — External Anti-Pattern Review

Rejected:

- universal generic fact/evidence object;
- arbitrary JSON evidence payloads as core semantics;
- source duplication;
- evidence=true as truth;
- absence=negative by default;
- provider IDs as Evidence identity;
- one universal confidence score;
- forced manual Evidence management in simple UI.

Result: **PASS**.

## CORE-09 — Correction / Reconciliation / Epistemic Integrity

Tested:

- source record corrected after evaluation;
- user correction outranks import for current view without deleting import history;
- two providers disagree;
- Confirmation added later;
- missing evidence remains missing;
- retrospective relevance does not create retrospective intention;
- current evaluation differs from historical evaluation.

Result: **PASS WITH HARDENING**.

Hardening: evaluation history must preserve/reconstruct material source versions and applicable rules.

## CORE-10 — Scale / Performance / History Stress

Stress:

- ten years of observations;
- many rolling Goal windows;
- high-frequency sources;
- one source used by many evaluations;
- repeated recalculation;
- multiple providers/corrections.

No semantic requirement forces eager persisted Evidence edge per use.

Result: **PASS WITH HARDENING**.

Hardening: future persistence must support explicit, derived, and materialized Evidence strategies without changing semantics.

## CORE-11 — Simple User / Power User

Simple UI:

- progress/reason shown automatically;
- no manual evidence graph;
- source details optional.

Power-user/high consequence:

- inspect source records;
- inspect contradictions;
- inspect Confirmation/Provenance;
- inspect historical evaluation basis.

Result: **PASS**.

## CORE-12 — Product Value / Complexity Cost

Benefit:

- explainable progress/evaluation;
- reuse of existing data;
- no duplication;
- contradiction visibility;
- better AI reasoning traceability.

Cost remains low if Evidence is mostly hidden/derived.

Result: **PASS**.

## CORE-13 — Implementation Pressure Without Premature Schema

High-value queries remain expressible conceptually:

- why is this criterion satisfied?;
- which records contradicted this conclusion?;
- which source versions were used?;
- what changed since last evaluation?;
- what Evidence can this actor see?;
- which Goals use this source record?;
- which conclusion depended on corrected data?

No final table/API design is required yet.

Result: **PASS**.

---

# 4. Dedicated Multi-Actor Compatibility Gate

## MA-01 — Identity / Account Independence

Evidence source/evaluator/subject need not be LifeOS accounts.

Result: **PASS**.

## MA-02 — Shared Canonical Fact / Actor-Scoped Overlay

One shared evaluation may reference actor-private source information without copying the source into shared state.

Result: **PASS WITH HARDENING**.

## MA-03 — Responsibility / Assignment / Claim / Substitution

Usually N/A to Evidence identity. Where execution/hand-off Actuals are Evidence, their responsibility semantics remain on source records/relationships.

Result: **N/A — justified**.

## MA-04 — Coordination Stewardship / Mental Load

Evidence requirements can create manual review burden. High-value automated selection should reduce, not shift, monitoring work.

Result: **PASS WITH PRODUCT HARDENING**.

## MA-05 — Common Ground / State Separation

Acknowledgement/acceptance/Confirmation may themselves be source information relevant to an evaluation, but are not Evidence automatically.

Result: **PASS**.

## MA-06 — Authority / Canonical Change

Evidence source/evaluator does not gain authority merely by supplying information.

Result: **PASS WITH HARDENING**.

## MA-07 — Selective Disclosure

Private Evidence may produce shareable derived consequence without raw Evidence disclosure.

Result: **PASS WITH HARDENING**.

## MA-08 — Inference Privacy

AI explanations/rankings/tool arguments must not leak hidden Evidence.

Result: **PASS WITH HARDENING**.

## MA-09 — Partial Adoption / External Participant

External provider/person records can be Evidence without LifeOS account.

Result: **PASS**.

## MA-10 — Assisted Participation / Assertion Provenance

Subject/source/recorder/evaluator remain distinct; assisted entry does not become subject assertion.

Result: **PASS**.

## MA-11 — Relationship Lifecycle / Revocation

Future access revocation can remove visibility/use while historical evaluation attribution may remain where retention policy permits.

Result: **PASS WITH DEFERRED DEPENDENCY**.

## MA-12 — Conflict / Adversarial Relationship

Conflicting Evidence remains representable; system does not force consensus or overwrite.

Result: **PASS**.

## MA-13 — Unequal Power / Guardian / Caregiver

Evidence supplied by guardian/caregiver/manager does not automatically become universal authority or expand visibility.

Result: **PASS WITH HARDENING**.

## MA-14 — Multi-Resource / Capacity

Evidence may inform resource/capacity evaluations without changing resource identity.

Result: **PASS**.

## MA-15 — Coordination-Burden Distribution

Do not require every participant to maintain evidence state for organizer convenience.

Result: **PASS WITH PRODUCT HARDENING**.

## MA-16 — Formality / Progressive Disclosure

Low consequence: hidden/automatic Evidence selection.

High consequence: inspect basis, source, contradictions, Confirmation/authority where necessary.

Result: **PASS**.

## MA-17 — AI Authority / Multi-Party Context

AI may discover/propose Evidence but cannot turn access into authority or disclosure permission.

Result: **PASS WITH HARDENING**.

## MA-18 — Concurrent Change / Provenance

Source correction and evaluation update must preserve relevant historical basis.

Result: **PASS WITH DEFERRED DEPENDENCY**.

## MA-19 — Privacy-Preserving Derived Projection

Share conclusion/consequence where authorized without exposing private Evidence.

Result: **PASS**.

## MA-20 — Actor-Scoped Reality Attribution

Evidence source actor, subject, confirmer, evaluator and authority actor may differ.

Result: **PASS**.

---

# 5. Cross-Concept Consistency Gate

## XCON-01 — Actual / Evidence

Actual remains realization truth; Evidence may use Actual in evaluation.

**PASS**.

## XCON-02 — Outcome / Evidence

Outcome remains result/disposition; Evidence may use Outcome in later evaluation.

**PASS**.

## XCON-03 — Observation / Evidence

Observation remains descriptive record; Evidence is contextual evaluative use.

**PASS**.

## XCON-04 — Confirmation / Evidence

Confirmation remains attestation; Evidence relevance is independent.

**PASS**.

## XCON-05 — Provenance / Evidence

Boundary survives conceptually; mandatory re-test during Provenance review.

**PASS WITH DEFERRED DEPENDENCY**.

## XCON-06 — GoalCriterion / Evidence

Criterion defines evaluation; Evidence supplies information.

**PASS**.

## XCON-07 — Milestone / Evidence

Milestone is checkpoint; Evidence may establish/contest attainment.

**PASS**.

## XCON-08 — Relationship / Evidence

Evidence may ultimately be represented through typed relationship semantics. This is a persistence/domain-shape question, not semantic redundancy.

**DEFERRED DEPENDENCY**.

---

# 6. Hardening register

| ID | Finding | Severity | Required treatment |
|---|---|---|---|
| E-H01 | Evidence is contextual use, not intrinsic data type | HARDENING | canonical invariant |
| E-H02 | no Evidence != Evidence against | HARDENING | canonical invariant |
| E-H03 | no LifeOS record != non-occurrence | HARDENING | completeness rule required before absence gains meaning |
| E-H04 | source record must not be duplicated | HARDENING | logical/persistence re-test |
| E-H05 | support/contradict/qualify must be representable | HARDENING | relationship/evaluation re-test |
| E-H06 | universal evidence score rejected | HARDENING | specialist/local certainty only |
| E-H07 | later relevance must not rewrite source intent/history | HARDENING | chronology invariant |
| E-H08 | private Evidence use != disclosure permission | HARDENING | Authority/Visibility/AI re-test |
| E-H09 | conflicting Evidence must coexist | HARDENING | Provenance/Decision re-test |
| E-H10 | no mandatory persisted edge per evaluative use | HARDENING | persistence pressure re-test |
| E-H11 | historical evaluation basis must be reproducible where material | DEFERRED DEPENDENCY | Version/Decision/persistence |
| E-H12 | Evidence may map to typed Relationship later | DEFERRED DEPENDENCY | Relationships cluster |

---

# 7. Regression corpus additions

1. historical Observation later becomes relevant to new Goal;
2. same Observation supports one Criterion and contradicts another;
3. missing Session must not prove missed workout;
4. authoritative-but-unconfirmed import used under policy;
5. conflicting watch/phone sensor records;
6. private Evidence produces shareable derived availability;
7. corrected source after previous evaluation;
8. one source used by several Goals/reviews;
9. external non-LifeOS actor supplies source information;
10. AI finds candidate Evidence but lacks authority to expose/use it universally.

---

# 8. Concept verdict

**PASS WITH HARDENING**

Evidence survives removal, merge, universalization, chronology, correction, privacy, multi-actor, conflict, AI, scale, and product-complexity tests when defined as a **canonical contextual evaluative role/relationship**.

No structural reopening of Actual, Outcome, Observation, Confirmation, Time, or Intention/Execution is required.

Evidence is **not** pre-approved as an aggregate root, physical entity/table, generic graph edge, or universal confidence model.

Mandatory future re-tests:

- Evidence vs Provenance;
- Evidence vs GoalCriterion final model;
- Evidence vs typed Relationship semantics;
- Evidence vs Decision/Version;
- Authority/Visibility and private Evidence;
- cluster integration + multi-actor stress;
- whole-domain regression;
- logical/persistence/API pressure.

---

# 9. Documentation propagation

Acceptance requires:

- `concepts/evidence.md`;
- this checkpoint;
- Language Map promotion;
- Domain Atlas README update;
- workstream handoff update;
- Provenance left as the final individual concept before cluster integration.

---

# 10. Downstream closure — Decision v0 (2026-08-13)

Decision v0 closes the semantic `Evidence vs Decision` boundary while preserving the original Evidence validation.

Canonical separation:

```text
Evidence
= contextual evaluative relevance/use of information

Decision
= bounded contextual resolution to a result
```

Evidence may support, contradict, qualify or otherwise inform a Decision. It does not become the resolution merely because a decision-maker relied on it, and conflicting Evidence need not be collapsed before a Decision can record a bounded resolution.

```text
Evidence != Decision
Evidence exists != target decided
Decision result != supporting Evidence
```

A visible Decision result does not make all supporting Evidence visible. Authority to decide also does not arise from supplying Evidence.

Decision v0 deliberately leaves GoalCriterion/evaluation semantics independent: deterministic evaluation may derive a current result without an explicit Decision, and a material Decision may incorporate judgment/policy without becoming a universal criterion engine.

Downstream classification:

```text
Evidence ↔ Decision  RESOLVED
```

Still deferred:

- GoalCriterion/evaluation model;
- evaluation snapshots/versioning;
- Evidence weighting/admissibility;
- typed Relationship representation;
- detailed reconciliation/source-precedence policy;
- privacy/retention;
- logical/physical Evidence materialization.

No Evidence hardening failed; **Evidence remains PASS WITH HARDENING, REOPEN = 0**.

Normative downstream references:

- `../concepts/decision.md`;
- `decision-v0-validation.md`.

---

# 11. Downstream closure — Version / material-equivalence v0 (2026-08-13)

Version v0 resolves the historical `evaluation snapshots/versioning` dependency without changing the original Evidence validation result.

A consequential historical evaluation must be able to bind, directly or reconstructibly, to:

```text
material source state(s)
material evaluation-target state
material rule/policy state
evaluation time/context
```

Later material correction of source, target or rule does not silently rewrite the earlier Evidence basis or conclusion. Non-material equivalence may preserve applicability only for the purpose/facet that remained unchanged.

Version is not admissibility, relevance, certainty, truth, weighting or Authority. It identifies the material state being reasoned over; evaluation/policy semantics still determine what that state means for the question.

Derived Evidence may rely on a reconstructible source-set/rule state instead of forcing one persisted edge per query. Provider versions, hashes, ETags and storage revisions may support concurrency/lineage but do not establish semantic materiality by themselves. Historical reconstruction does not mandate indefinite retention of all sensitive payloads.

Downstream classification:

```text
Evidence ↔ Version/evaluation history   RESOLVED
Version ↔ Evidence meaning/weight       RESOLVED — not owner
```

GoalCriterion/evaluation, weighting/admissibility, detailed reconciliation, privacy/retention and physical materialization remain independently owned.

No original Evidence hardening failed. **Evidence remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `../concepts/version.md`;
- `version-material-equivalence-v0-validation.md`.

---

# 12. Downstream closure — Reconciliation / Source Precedence v0 (2026-08-13)

Reconciliation v0 resolves the checkpoint's detailed conflict/source-precedence dependency without changing the original Evidence validation result.

Canonical separation:

```text
Evidence
= contextual evaluative input/relevance

Reconciliation
= contextual process/capability handling materially competing states/assertions under an applicable bounded basis
```

Conflicting Evidence remains Evidence; reconciliation does not erase it or convert it into one universal score. Evidence can support, contradict or qualify while Version/Provenance/Confirmation/Authority and applicable policy provide additional context. No evidence score, source recency, provider identity or AI confidence becomes universal precedence.

Reconciliation may leave conflict unresolved, apply bounded specialist/source-of-record policy, culminate in Decision or deterministically resolve under already-authorized policy. Evidence itself does not select the winner or establish objective truth.

A reconciled result may be visible while underlying contradictory/private Evidence remains hidden. Historical Evidence uses and source material states remain reconstructible where consequential; later resolution does not rewrite what was considered earlier.

Downstream classification:

```text
Evidence ↔ detailed Reconciliation   RESOLVED
Evidence ↔ Source Precedence         RESOLVED — bounded policy only
Evidence ↔ winner/truth              RESOLVED — not owner
```

GoalCriterion/evaluation, weighting/admissibility, specialist policy, retention and physical representation remain independently owned.

No original Evidence hardening failed. **Evidence remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `../concepts/reconciliation.md`;
- `reconciliation-source-precedence-v0-validation.md`.

---

# 13. Downstream closure — Criterion / Evaluation v0 (2026-08-15)

Criterion / Evaluation v0 closes the checkpoint's remaining GoalCriterion/evaluation semantic dependency while preserving the original Evidence verdict.

Canonical separation is now explicit:

```text
Criterion
= contextual evaluative specification/capability

Evidence
= contextual information bearing on the evaluation

Evaluation
= contextual application of applicable Criterion state to relevant Evidence
  under material target/rule/context/time
```

Regression results:

- Evidence remains distinct from Criterion and Evaluation;
- missing Evidence does not imply failed Criterion;
- unknown/insufficient Evidence remains a valid Evaluation outcome/state;
- conflicting Evidence does not permit an invented average, score or winner;
- a consequential historical Evaluation remains reconstructible against material target, Criterion and Evidence/source state;
- later source correction or Criterion revision may cause re-evaluation without rewriting the earlier basis;
- private Evidence may support an authorized shareable bounded result without raw-source disclosure;
- AI may discover candidate Evidence or calculate under an authorized Criterion but cannot fabricate Evidence, Authority, Criterion adoption or certainty.

Downstream classification:

```text
Evidence ↔ Criterion             RESOLVED — distinct
Evidence ↔ Evaluation            RESOLVED — input/use, not identity
GoalCriterion final semantics    RESOLVED — Goal-scoped Criterion
Evaluation history basis         RESOLVED — Version/material-state binding where consequential
```

Weighting/admissibility policy, specialist evidence models, retention/materialization and physical/API representation remain separate downstream concerns.

No original Evidence hardening failed. **Evidence remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `../concepts/criterion-evaluation.md`;
- `criterion-evaluation-v0-validation.md`.