# Evidence v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-11  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Observed Reality & Evidence cluster

## Canonical definition

> **Evidence is the contextual evaluative role played by information when that information is used to support, contradict, qualify, or otherwise materially inform the evaluation of a specific claim, criterion, checkpoint, decision, or other evaluative target. Evidence represents the relationship between source information and an evaluation context; it does not duplicate the source information, establish truth by itself, or imply that the information was originally created for that evaluation.**

Evidence answers:

> **What information materially bears on this evaluation, in what direction and context, and on what basis is it being used?**

Evidence is therefore primarily semantic relationship/use, not a universal fact record.

Conceptually:

```text
source information
Observation / Actual / Outcome / Confirmation /
Milestone / external record / derived result / specialist fact
                    │
                    ↓
              Evidence role
                    │
                    ↓
             evaluation target
claim / criterion / checkpoint / decision / assessment
```

The source information preserves its own identity and history. Becoming Evidence for one evaluation does not mutate that source into a new domain object or rewrite why it originally existed.

---

# 1. Why Evidence exists

LifeOS needs to distinguish between information that exists and information that is relevant to a particular evaluation.

Without Evidence semantics the model tends toward one of several weak alternatives:

1. every Observation is treated as evidence for every related Goal;
2. source records are copied into Goal/Milestone/progress structures;
3. criteria embed provider-specific facts directly;
4. confirmation is mistaken for proof;
5. provenance/source reputation is mistaken for evaluative relevance;
6. absence of data is interpreted as negative evidence;
7. one global `confidence` score attempts to summarize context-dependent relevance and quality;
8. later-discovered relevance silently rewrites historical intent.

Evidence gives LifeOS a bounded way to express that existing information matters **for this evaluation** without creating a second copy of the information.

---

# 2. Evidence is contextual role, not intrinsic data type

The same source record may be evidence in one context, contradictory evidence in another, and irrelevant in a third.

Example:

```text
Observation
body weight = 66.4 kg
```

For:

```text
Criterion A
65 kg <= weight <= 67 kg
```

the Observation may support satisfaction.

For:

```text
Criterion B
weight >= 70 kg
```

the same Observation may contradict satisfaction.

For:

```text
Criterion C
publish website
```

it is irrelevant.

Therefore:

> **Information is not Evidence merely because it exists. Evidentiary meaning arises from its relationship to a specific evaluation context.**

---

# 3. Evidence does not duplicate source information

Evidence must preserve source identity rather than creating copied `evidence data`.

Preferred semantic shape:

```text
Observation O-17
weight = 66.4 kg
        │
        ├── Evidence use -> Criterion A
        └── Evidence use -> Review B
```

not:

```text
Observation O-17
weight = 66.4 kg

Evidence copy 1
weight = 66.4 kg

Evidence copy 2
weight = 66.4 kg
```

The exact persistence implementation is deferred. A future logical model may represent some Evidence relations explicitly, derive others from rules/queries, and materialize historical evaluation snapshots where reconstruction requires it.

Canonical rule:

> **Evidence semantics do not imply one persisted Evidence entity/row/edge for every source-target use.**

---

# 4. Evidence versus Observation

Observation describes a measured, perceived, reported, or derived property/state/assertion about a subject.

Evidence describes how information bears on an evaluation.

```text
Observation
exam score = 78/100

Criterion
score >= 60/100

Evidence use
Observation supports Criterion
```

The Observation can exist without the Criterion or Evidence use.

The same Observation can later become relevant to a new evaluation without changing its historical identity or original purpose.

Therefore:

> **Evidence != Observation.**

---

# 5. Evidence versus Actual

Actual represents how a specific intention/expectation was realized.

An Actual may become Evidence for a criterion or later assessment.

```text
Actual
workout occurred

Criterion
>= 3 qualifying workouts/week

Evidence use
Actual contributes to weekly evaluation
```

The Actual remains realization truth. Evidence is its evaluative use.

> **Evidence != Actual.**

---

# 6. Evidence versus Outcome

Outcome represents the result/disposition of a realization.

An Outcome may serve as Evidence for another evaluative target.

```text
Outcome
exam passed

Milestone
B1 certification checkpoint reached

Evidence use
Outcome supports Milestone attainment
```

The Outcome does not become Evidence intrinsically or lose its own lifecycle/history.

> **Evidence != Outcome.**

---

# 7. Evidence versus Confirmation

Confirmation records a contextual attestation by a confirmer toward a specific target/version.

Evidence records evaluative relevance/use.

```text
Observation
weight = 66.4 kg

Confirmation
user affirms Observation v1

Evidence use
Observation, with its confirmation/provenance context,
used to evaluate Criterion C
```

Confirmation may strengthen, qualify, or otherwise affect evaluation policy, but it does not define what the information is evidence for.

A source may be usable Evidence without personal Confirmation where the relevant policy permits it.

> **Evidence != Confirmation.**

---

# 8. Evidence versus Provenance

Provenance explains how information came to exist, changed, was derived, imported, recorded, or attributed.

Evidence explains how information is used in an evaluation.

```text
Observation
weight = 66.4 kg

Provenance
imported from provider/device X

Evidence relation
Observation used for maintenance Criterion Y
```

The same provenance can remain unchanged while evidentiary relevance changes across evaluation contexts.

Source/provenance can influence evidence quality, admissibility, or interpretation without becoming Evidence itself.

> **Evidence != Provenance.**

---

# 9. Evidence versus GoalCriterion

A Criterion defines what/how something is evaluated.

Evidence supplies information bearing on that evaluation.

```text
Criterion
>= 3 workouts/week

Evidence
qualifying Actual A
qualifying Actual B
qualifying Actual C
```

Therefore:

> **Criterion != Evidence.**

A criterion may define eligibility/admissibility rules for Evidence without owning or duplicating the source records.

---

# 10. Evidence versus Milestone

A Milestone represents a meaningful contextual checkpoint that may become attained.

Evidence may establish or contest whether the checkpoint has been reached.

```text
Milestone
Design approved

Possible Evidence
- review Outcome = approved
- signed specialist record
- authorized Confirmation
```

The Milestone is the checkpoint. Evidence is the information used to evaluate its attainment.

> **Evidence != Milestone.**

---

# 11. Direction is not universally positive

Evidence must not mean only `proof for`.

Information may:

- support;
- contradict;
- qualify;
- limit applicability;
- make an evaluation uncertain;
- supply a required input without itself determining the result.

Example:

```text
Claim
run distance >= 5 km

Evidence A
watch = 5.1 km

Evidence B
phone GPS = 4.7 km
```

Both records remain legitimate Evidence inputs. LifeOS must not manufacture a canonical average merely to remove contradiction.

Exact evaluation/weighting rules belong to the relevant criterion, decision, specialist policy, authority context, or later reasoning model.

---

# 12. Evidence does not establish truth by existence

Canonical rule:

> **The existence of Evidence does not by itself establish the truth, satisfaction, attainment, or authority of the evaluated target.**

A verifier/evaluator may need to consider:

- relevance;
- source/provenance;
- recency/effective period;
- coverage/completeness;
- Confirmation;
- authority;
- contradictions;
- specialist rules;
- applicable policy;
- privacy/visibility constraints.

LifeOS must therefore avoid:

```text
evidence exists
=> target true
```

unless an explicit evaluation rule makes that inference valid.

---

# 13. Absence is not automatically negative Evidence

This is a critical invariant.

```text
no supporting Evidence
!= Evidence against
```

and:

```text
no LifeOS record
!= event did not happen
```

Example:

```text
No Session recorded for Tuesday workout
```

usually means only that LifeOS has no qualifying Session record. The workout might have happened outside LifeOS.

Absence may become meaningful Evidence only where the evaluation context has a justified completeness assumption, explicit negative-observation semantics, authoritative source boundary, or another valid rule.

Therefore:

> **Missing information must remain missing unless a justified evaluation rule gives absence evidentiary meaning.**

---

# 14. Retrospective and later-discovered relevance

Evidence relevance may be discovered after the source information was created.

Example:

```text
January
Observation O-1 recorded independently

March
Goal/criterion introduced
LifeOS identifies O-1 as relevant historical Evidence
```

The relationship discovered in March does not imply the January Observation was created for the Goal.

Canonical rule:

> **Later evidentiary relevance must not fabricate earlier intention, ownership, contribution, or causal purpose.**

This preserves upward reconstruction without rewriting history.

---

# 15. Evidence can be reused laterally

One source fact may bear on several evaluations without duplication.

```text
Observation
active minutes = 180
        │
        ├── Evidence -> weekly activity Criterion
        ├── Evidence -> wellbeing Review
        └── Evidence -> training-load assessment
```

Each Evidence use can differ in:

- direction;
- admissibility;
- temporal window;
- weight/importance;
- visibility;
- evaluator;
- applicable policy.

The source identity stays singular.

---

# 16. Evidence strength / confidence is contextual

LifeOS must not assume one universal scalar `evidence_strength` or `confidence` property.

The same source can be strong for one question and weak for another.

Example:

```text
heart-rate sensor data
```

may be useful evidence for exercise intensity while being weak evidence for overall wellbeing.

Strength/certainty may depend on:

- evaluation target;
- source/provenance;
- measurement method;
- Confirmation;
- authority;
- coverage;
- consistency with other Evidence;
- specialist rules;
- time/context;
- uncertainty model.

Specialist domains may define formal confidence/certainty models. The LifeOS kernel does not impose one universal scoring system.

---

# 17. Derived information as Evidence

A derived Observation/result/aggregate may be used as Evidence when traceability is sufficient.

Example:

```text
source Observations
weekly distances
        ↓
derived weekly total
        ↓
Evidence for weekly distance Criterion
```

Do not require every query aggregate to be persisted merely because it is temporarily used as Evidence.

Where historical reproducibility matters, the future evaluation/version model may need to preserve:

- the evaluation rule/version;
- source set or reconstructible selection basis;
- material derived result;
- decision/evaluation time;
- provenance.

Exact materialization rules are deferred.

---

# 18. Multi-actor semantics

Evidence is evaluation-context scoped, not actor-owner scoped.

The following may differ:

```text
source subject
source observer/recorder
source provider/device
Evidence selector
Evaluator
Confirmer
Authority actor
Viewer
Beneficiary
```

A source actor being a LifeOS user does not make their information authoritative by default.

Conflicting actors/providers may supply competing Evidence that remains representable until evaluation/reconciliation rules decide how to interpret it.

---

# 19. Shared evaluations and actor-scoped Evidence

A shared Goal/Milestone/decision does not imply every supporting fact is shared.

LifeOS may need:

```text
private source information
        ↓
authorized evaluation / derived consequence
        ↓
shareable result
```

without disclosing the source Evidence.

Example:

```text
private health context
        ↓
Evidence used in scheduling feasibility
        ↓
shared projection: unavailable 14:00–16:00
```

Canonical rule:

> **Using private information as Evidence does not create permission to disclose the Evidence or its private reason.**

---

# 20. Evidence under disagreement and unequal authority

Different actors may reasonably disagree on:

- whether information is admissible Evidence;
- how much weight it should receive;
- which source is authoritative;
- whether a criterion has been satisfied.

LifeOS must not silently flatten disagreement into one `evidence=true` flag.

In high-consequence contexts, specialist systems/institutions may remain authoritative even when LifeOS stores other observations or confirmations.

Authority belongs to future relationship/governance semantics and specialist policy, not to Evidence identity itself.

---

# 21. AI semantics

AI may:

- discover candidate Evidence;
- explain possible relevance;
- identify contradictions;
- propose an evaluation;
- select information according to an authorized rule;
- generate a derived assessment where permitted.

AI must not:

- convert candidate information into authoritative Evidence by confidence alone;
- fabricate source facts;
- hide contradictory Evidence to make a conclusion cleaner;
- infer authority from access;
- reveal private Evidence in explanations/tool calls to unauthorized actors.

Canonical rule:

> **AI discovery of Evidence is not authority, Confirmation, or disclosure permission.**

---

# 22. Lifecycle and history

Evidence relevance may change because:

- a criterion/evaluation changes;
- a source record is corrected/superseded;
- provenance is updated;
- Confirmation is added/retracted;
- an authority rule changes;
- new contradictory information appears;
- a later evaluation uses a different time window.

Historical reconstruction must distinguish:

```text
source fact/version then
Evidence considered then
evaluation rule then
conclusion then
later corrections/relevance changes
```

Do not rewrite past evaluations solely because the current source/evaluation rule changed.

Exact evaluation snapshots/versioning are deferred to later reasoning/persistence work.

---

# 23. Scale and persistence implications

Evidence semantics can become extremely high-cardinality if physically materialized naïvely.

Examples:

- years of weight observations reused by multiple Goal windows;
- high-frequency activity data used by several reports;
- one external record relevant to multiple criteria;
- rolling evaluations recomputed daily.

The logical/physical model must therefore permit several implementation strategies while preserving semantics:

- explicit persisted Evidence relation where identity/history matters;
- rule/query-derived applicability where deterministic and reconstructible;
- materialized evaluation snapshot when historical reproducibility requires it;
- specialist reference where the authoritative system retains detail.

Do not commit yet to:

- universal `evidence` table;
- universal polymorphic target FK;
- one row per query use;
- one global evidence score;
- copying source payloads into evaluation records.

---

# 24. Product / UI implications

Evidence is usually hidden or advanced domain language.

Simple UI may show:

- Why is this progressing?;
- Based on 3 workouts;
- Evidence / supporting data;
- Conflicting data;
- Source details;
- Why did LifeOS conclude this?;
- Review supporting information.

A simple user should not need to manually manage an Evidence graph for ordinary Goals.

Higher-consequence/power-user surfaces may expose:

- source records;
- support/contradiction;
- confirmation/provenance;
- evaluation rule;
- unresolved conflict;
- authority basis;
- historical evaluation snapshot.

---

# 25. External benchmark interpretation

External standards support useful boundaries but do not dictate LifeOS architecture.

- W3C PROV distinguishes provenance relationships around entities, activities, and agents; this reinforces that origin/derivation is a different problem from evaluative use.
- W3C Verifiable Credentials supports evidence associated with claims/credentials while keeping issuer, subject, status, and other credential semantics distinct; it is evidence that supporting material can remain contextual rather than becoming the claim itself.
- HL7 FHIR R5 `Evidence` is a specialist research representation including variables, statistics, and certainty. It confirms the importance of context/certainty, but its research-specific resource model is deliberately **not** adopted as the LifeOS kernel model.

Classification:

```text
contextual Evidence relation/use        ADAPT
source information remains distinct     BORROW
Provenance != Evidence                  BORROW
specialist universal evidence resource  NOT APPLICABLE to LifeOS kernel
one evidence score for all domains      ANTI-PATTERN
```

---

# 26. Invariants

1. Evidence is contextual evaluative role/use, not intrinsic source-data type.
2. Source information retains its own identity when used as Evidence.
3. Evidence does not duplicate source payload by default.
4. Evidence does not establish truth merely by existing.
5. Evidence may support, contradict, qualify, or otherwise materially inform an evaluation.
6. Evidence != Observation.
7. Evidence != Actual.
8. Evidence != Outcome.
9. Evidence != Confirmation.
10. Evidence != Provenance.
11. Evidence != GoalCriterion.
12. Evidence != Milestone.
13. No Evidence != Evidence against.
14. No LifeOS record != proof of non-occurrence unless justified by an explicit completeness/evaluation rule.
15. Later-discovered Evidence relevance does not rewrite historical intention/source purpose.
16. One source may serve several evaluations without duplication.
17. Evidentiary strength/certainty is context-dependent; no universal scalar is required.
18. Conflicting Evidence must be representable.
19. Source/subject/observer/recorder/evaluator/confirmer/authority/viewer may differ.
20. Shared evaluation does not imply shared visibility of all Evidence.
21. Private Evidence may support an authorized derived result without source disclosure.
22. AI access/discovery does not create authority or disclosure permission.
23. Evidence semantics do not imply one physical row/entity for every evaluative use.
24. Historical evaluation must remain reconstructible where consequential.

---

# 27. Rejected alternatives

Rejected:

- Evidence as synonym for Observation;
- Evidence as synonym for source/provenance;
- Evidence as synonym for Confirmation;
- Evidence as synonym for Outcome;
- Evidence as intrinsic property of a record;
- Evidence as only positive proof;
- Evidence existence implies target truth;
- absence of records as universal negative Evidence;
- universal evidence-confidence score;
- duplication of source records into each Goal/Milestone/evaluation;
- pre-approving one generic `Evidence` aggregate/table for all uses.

---

# 28. Deliberately deferred questions

- exact evaluation/evaluand model;
- GoalCriterion final representation;
- explicit versus derived Evidence relation persistence;
- support/contradict/qualify vocabulary and whether it belongs to Relationship semantics;
- weighting/certainty models;
- authority/admissibility rules;
- evaluation snapshots/versioning;
- evidence retention under privacy/deletion constraints;
- specialist legal/medical/research evidence requirements;
- materialization/cache strategy;
- generic target-reference mechanics;
- AI-generated derived assessments;
- exact Evidence-to-Decision semantics.

---

# 29. Persistence/API implications without physical commitment

The future logical model must be capable of representing or reconstructing, where needed:

- source information identity/version;
- evaluative target/context;
- direction/relevance semantics where material;
- applicable time/window;
- evaluation rule/version;
- provenance/confirmation/authority context without collapsing them;
- conflicting Evidence;
- historical evaluation snapshot or reconstruction basis;
- privacy/visibility boundary;
- derived/materialized Evidence usage distinction.

This does **not** yet imply a universal Evidence entity/table or polymorphic relationship implementation.

---

# 30. Reopening triggers

Reopen Evidence v0 if later Provenance, GoalCriterion, Relationship, Decision, Authority, or persistence work demonstrates that:

- Evidence is fully reducible to a stronger typed-Relationship/evaluation model without losing the canonical semantics;
- evidence identity/lifecycle is materially richer than the role model assumed here;
- specialist requirements require a universal stronger abstraction;
- the proposed contextual relation cannot preserve evaluation history efficiently/correctly;
- evidence/privacy/retention requirements expose a structural contradiction.

Absent such evidence, Evidence remains the current accepted semantic baseline as a **canonical evaluative role/relationship**, with physical representation intentionally deferred.

---

# 2026-08-13 — Decision closure amendment

Decision v0 closes the exact `Evidence-to-Decision` semantic boundary without turning Evidence into a decision engine.

Canonical separation:

```text
Evidence
= information bearing on an evaluation/question in context

Decision
= bounded contextual resolution of a question to a specific result
```

Therefore:

```text
Evidence != Decision
Evidence existence != Decision result
conflicting Evidence != automatically reconciled Decision
```

A Decision may use supporting, contradicting or qualifying Evidence while preserving those source records and their evaluative roles. The same Evidence can support several different Decisions/evaluations without duplication.

A Decision result may be visible while supporting Evidence remains private. Conversely, an Actor allowed to inspect Evidence does not automatically have Authority to decide the target question.

Decision does not replace GoalCriterion/evaluation semantics: deterministic evaluation may derive a result without an explicit material Decision, while a material Decision may consider Evidence without being reducible to a criterion calculation.

Downstream closure:

```text
Evidence ↔ Decision  RESOLVED
```

GoalCriterion/evaluation, evaluation snapshot/versioning, weighting/admissibility, detailed reconciliation policy, privacy/retention and physical Evidence representation remain independently deferred.

**Evidence v0 verdict is unchanged. REOPEN = 0.**

---

# 2026-08-13 — Version / material-equivalence downstream closure amendment

Version v0 resolves Evidence's former `evaluation snapshot / versioning` semantic dependency without turning Evidence into a universal persisted graph.

Canonical binding when consequential:

```text
source material state(s)
+ evaluation target material state
+ evaluation rule/policy material state
+ evaluation time/context
→ historical Evidence use / conclusion
```

Therefore a historical evaluation remains about the exact source/target/rule states it actually used. If an Observation, Outcome, criterion or rule later changes materially, the earlier Evidence relationship/evaluation is not silently rewritten and does not automatically apply to the new state.

Version does not decide whether information is admissible, relevant, strong, true or authoritative. Those remain evaluation/policy/Authority questions. Version only makes the material state being evaluated referenceable and reconstructible where consequence requires it.

Materiality is purpose-specific: an irrelevant metadata change need not invalidate an Evidence use, while a change to the value, target meaning, applicable window or evaluation rule that the conclusion depends on generally does. Hash/ETag/storage-version equality is insufficient to decide this universally.

Derived Evidence may bind to a reconstructible source-set/rule state rather than force persistence of every query edge. Non-linear source history and later corrections are valid; historical reproducibility does not require retaining every sensitive payload indefinitely.

The historical evaluation-version dependency is now downstream-closed at the semantic boundary. GoalCriterion/evaluation semantics, weighting/admissibility, detailed reconciliation, privacy/retention and physical Evidence persistence remain independently owned.

No Evidence hardening failed. **Evidence remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `version.md`;
- `../checkpoints/version-material-equivalence-v0-validation.md`.