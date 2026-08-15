# Criterion / Evaluation v0

**Status:** Current accepted baseline — PASS WITH HARDENING  
**Validated:** 2026-08-15  
**Validation standard:** Domain Validation Methodology v3  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Canonical definition

> **Criterion is the contextual evaluative specification through which LifeOS defines what condition, rule, threshold, pattern, checkpoint, assessment or combination is relevant when evaluating a bounded target for a defined purpose and context. Evaluation is the contextual application of the materially applicable Criterion state to relevant Evidence under the applicable target, time/window, Authority/policy and material-state context, producing an assessment without rewriting the underlying Evidence, Actual, Outcome, Milestone or target identity.**

Canonical question:

> **Under which applicable rule should this bounded target be evaluated, using which relevant Evidence and material states, and what assessment follows for this evaluation context?**

Classification:

```text
CRITERION
CANONICAL CONTEXTUAL EVALUATIVE SPECIFICATION / CAPABILITY

✅ defines how a bounded target is assessed
✅ may express threshold/range/frequency/duration/accumulation/trend/checkpoint/external/qualitative/composite semantics
✅ may define applicable period/window and Evidence eligibility/completeness rules
✅ may have materially relevant state where historical applicability matters

GOALCRITERION
✅ Goal-scoped use of Criterion semantics
❌ separate universal primitive/root

EVALUATION
CANONICAL CONTEXTUAL REASONING / PROCESS-RESULT SEMANTICS

✅ applies materially applicable Criterion state to relevant Evidence
✅ may be deterministic, manual, specialist-assisted or policy-governed
✅ may be transient/derived or materially recorded where consequence requires
✅ may result in satisfied / not-satisfied / partial / unknown / indeterminate / other criterion-specific assessment semantics where justified

EVALUATION
❌ universal native entity/root
❌ universal workflow/state machine
❌ Evidence
❌ Actual / Outcome
❌ Decision
❌ Reconciliation
❌ Authority
❌ Confirmation
❌ automatic effective target state

GOAL PROGRESS
✅ DERIVED / EVALUATION PROJECTION
❌ universal stored percentage/status
```

---

# 1. Why Criterion / Evaluation exists

The accepted model already distinguishes desired state, execution, observed reality and evidence, but it still needs a semantic owner for the question:

> **How do we determine whether this desired condition/checkpoint/question is satisfied, progressing, sustained, uncertain or not established?**

Without Criterion/Evaluation semantics, implementations are pushed toward weak shortcuts:

- `target_value` on every Goal;
- `progress_percentage` on every Goal;
- every Milestone as a duplicate boolean truth source;
- Evidence treated as proof merely because it exists;
- missing data treated as failure;
- latest Evidence or newest provider silently winning;
- one global score/confidence model;
- current rules silently rewriting historical evaluations;
- AI-generated assessments treated as user intention or canonical truth.

The current Product North Star further requires the distinction:

```text
Effort != Execution != Outcome != Goal Progress
```

Two hours of study can establish Effort and Session execution without establishing progress toward B2 proficiency. Conversely, a certification result may materially advance a Goal without being reducible to time spent.

Criterion/Evaluation provides the missing evaluation semantics while keeping source reality, governance and current-state ownership separate.

---

# 2. Criterion is not Goal identity

A Goal expresses what is intentionally desired. A Criterion expresses how a bounded target is evaluated.

```text
Goal
Reach spoken English B2

Criterion
recognized B2 assessment result
```

or:

```text
Goal
Train regularly

Criterion
>= 3 qualifying training Sessions / week
```

Changing a Criterion can preserve Goal identity when the desired state remains materially the same.

However, Criterion cannot be used to hide a genuine change in desired meaning. If the desired state itself changes materially, Goal identity/version/replacement rules still apply.

Canonical rule:

> **Goal identity and Criterion state are separate. Criterion revision does not automatically replace the Goal, and Goal identity cannot be preserved through a Criterion edit when the desired meaning itself was replaced.**

---

# 3. GoalCriterion is a scoped use, not another primitive

`GoalCriterion` is useful language for a Criterion attached to or governing evaluation of a Goal.

It does not require a separate universal ontology root from Criterion.

```text
Criterion
= reusable semantic family/capability

GoalCriterion
= Criterion used in Goal evaluation
```

A future logical model may use different physical structures for different criterion families. The semantic classification does not pre-approve one universal `goal_criteria` table or DSL.

---

# 4. Criterion versus Milestone

A Milestone is a meaningful contextual checkpoint that can be attained. A Criterion defines how a target is evaluated and may reference a Milestone.

```text
Goal
Publish album

Criterion
Release-live Milestone attained

Milestone
Release live on distribution platforms
```

Therefore:

```text
Criterion != Milestone
```

A Milestone may also have attainment evaluation semantics without becoming a Goal or Criterion. Its attainment remains evaluation-backed checkpoint state rather than a duplicate source of Actual/Outcome/Observation truth.

---

# 5. Criterion versus Evidence

Criterion defines the evaluative rule/question. Evidence provides information used in that evaluation.

```text
Criterion
>= 3 qualifying workouts/week

Evidence
Actual A
Actual B
Actual C
```

Therefore:

```text
Criterion != Evidence
Evaluation != Evidence
```

Criterion may specify what Evidence is eligible, which window applies, what completeness assumption is justified, or how conflicting inputs are interpreted. It does not own or duplicate source records.

---

# 6. Criterion versus Temporal Constraint

A Temporal Constraint governs where/when scheduling or temporal placement is allowed, required, bounded or preferred.

A Criterion may use a time window or period as part of evaluation without becoming a scheduling constraint.

```text
Criterion
>= 3 Sessions per calendar week

Temporal Constraint
Do not schedule training after 21:00
```

Therefore:

```text
Criterion != Temporal Constraint
```

Evaluation period/window semantics do not make the Criterion a Schedule or Capacity claim.

---

# 7. Criterion versus Trigger / conditional policy

A Criterion answers how something is assessed.

A Trigger/conditional policy answers whether a condition should cause some later action/effect.

```text
Criterion result
Goal is off trajectory

Trigger/policy
if off trajectory for 2 periods -> propose plan review
```

The evaluation result may become input to automation, but:

```text
Criterion != Trigger
Evaluation != Trigger
```

Trigger/automation remains separately reviewable.

---

# 8. Evaluation semantics

Evaluation applies an applicable Criterion state to relevant Evidence in a bounded context.

Conceptually:

```text
bounded target/material state
+ applicable Criterion/material state
+ relevant Evidence/material source states
+ evaluation time/window/context
+ applicable policy/Authority where needed
→ Evaluation
→ contextual assessment/result
```

This is semantic composition, not a mandatory persistence pipeline.

An Evaluation can be:

- transient and recalculated;
- derived from deterministic data;
- based on an authorized declaration;
- manual/qualitative;
- specialist-provided or specialist-backed;
- materialized as a historical snapshot where consequence/reproducibility requires it.

The concept does not require every evaluation tick to become a durable entity.

---

# 9. Supported criterion forms

The semantic family must remain capable of expressing, where useful:

- boolean/binary condition;
- threshold at or above a value;
- threshold at or below a value;
- target value;
- acceptable range;
- accumulation;
- frequency within a period;
- duration within a period;
- milestone/checkpoint attainment;
- trend/directional change;
- external result;
- manual/qualitative assessment;
- composite criteria.

These are requirements of expressiveness, not an accepted universal enum, AST, expression language or one-table-per-form design.

---

# 10. Missing Evidence and epistemic integrity

A critical invariant remains:

```text
no Evidence
!= Evidence against
!= Criterion failed
```

and:

```text
no LifeOS record
!= non-occurrence
```

Example:

```text
Criterion
>= 3 qualifying workouts/week

LifeOS currently sees only 2
```

If the source boundary is incomplete, the honest Evaluation may be:

```text
unknown / insufficient Evidence
```

rather than `failed`.

Absence gains negative meaning only where an applicable rule establishes a justified completeness assumption, negative-observation semantics or authoritative source boundary.

---

# 11. Conflicting Evidence and Reconciliation

Criterion/Evaluation does not erase conflict.

```text
watch distance = 5.1 km
phone distance = 4.7 km
Criterion threshold = 5.0 km
```

If no sufficient bounded resolution basis exists, the Evaluation may remain indeterminate or unresolved.

Reconciliation may be invoked where materially competing states/assertions must be handled.

```text
Evaluation != Reconciliation
```

Reconciliation may preserve conflict, apply bounded Source Precedence, combine compatible inputs, escalate, defer or resolve under applicable policy/Authority. Criterion does not create a universal source ranking.

---

# 12. Historical evaluation and Version

Evaluation history becomes false if current Criterion/source state is treated as though it always existed.

Representative chronology:

```text
T0 Goal: train regularly
T1 Criterion C1: >= 3 qualifying Sessions/week
T2 week W1 has two known qualifying Sessions
T3 third workout occurs externally but is not yet imported
T4 end-of-week Evaluation E1 = unknown/insufficient under non-complete source policy
T5 provider imports the third qualifying Actual
T6 W1 may be re-evaluated/corrected using later Evidence
T7 Criterion changes to C2: >= 4/week effective next week
T8 W1 remains historically evaluated under C1, not retroactively C2
T9 provider conflict about one workout may remain unresolved or be reconciled under applicable basis
```

Canonical rule:

> **Where consequence requires historical reproducibility, Evaluation must bind to or reconstruct the material target, Criterion and Evidence/source states actually applicable at evaluation time.**

Current reevaluation may differ from historical evaluation without pretending the earlier evaluation never existed.

---

# 13. Multiple criteria and composition

A Goal or other target may have multiple criteria.

The kernel must not assume a universal composition rule such as:

```text
all criteria AND
any criterion OR
weighted average
simple arithmetic mean
lowest score wins
```

Different targets may require:

- all mandatory criteria satisfied;
- one of several alternatives;
- required + optional criteria;
- qualitative judgment;
- threshold plus sustained duration;
- specialist policy;
- another bounded composition rule.

Criterion-composition representation remains deferred to logical/evaluation modeling. The semantic requirement is that composition be explicit/contextual rather than silently universal.

---

# 14. Goal Progress is derived

Goal Progress is not universal canonical stored state.

Useful projections may include:

```text
€5,000 / €20,000
2 of 3 qualifying Sessions this week
within target range for 5 of 6 months
B1 attained / B2 not yet established
on trajectory / off trajectory / unknown
```

A percentage may be meaningful in some contexts and false precision in others.

Therefore:

> **Goal Progress is a derived/evaluation projection whose representation depends on the Goal's applicable Criterion semantics; no universal `progress_percentage` is accepted.**

---

# 15. Decision, Authority and effective target state

Evaluation answers an assessment question under a Criterion. Decision records a bounded resolution when the resolution itself matters. Authority determines legitimate bounded governance/effect power.

```text
Evaluation != Decision
Evaluation != Authority
```

A deterministic already-authorized rule may produce an Evaluation without fabricating a human Decision.

Conversely, a human Decision may consider Evidence and judgment without being reducible to a Criterion calculation.

An Evaluation result also does not automatically make the affected target's state effective/current. The owning domain concept plus applicable Authority/Decision/policy owns that effect.

---

# 16. Confirmation and Agreement / Consent

Evaluation does not manufacture common ground.

```text
Evaluation result
!= Confirmation
!= Acknowledgement
!= Agreement
!= Consent
```

A shared Goal can have a canonical Criterion under applicable governance while different actors retain different Acknowledgement, Agreement, Consent, private Evidence and personal perspectives.

Group membership or participation does not imply assent to a Criterion.

---

# 17. Shared targets and private Evidence

A shared target does not imply shared visibility of all supporting Evidence.

Valid shape:

```text
private actor/source Evidence
→ authorized Evaluation
→ bounded shareable result
```

without:

```text
private Evidence
→ automatic disclosure to every participant
```

Examples include health, availability, finance, HR, caregiving or specialist facts that legitimately influence a shared result but must remain private.

Evaluation-result Visibility, Criterion Visibility and Evidence/source Visibility remain independently governed.

---

# 18. Actor attribution and assisted evaluation

The following roles may differ:

```text
subject
source actor
recorder
Evidence selector
evaluator
Authority holder
represented party
viewer
beneficiary
```

A helper/caregiver/assistant/manager entering data or running an evaluation does not become the subject and does not fabricate the subject's personal declaration.

Represented/on-behalf-of evaluation preserves actual Actor and represented party where material. Representation does not itself create Authority or Evidence validity.

---

# 19. Unequal power and specialist systems

A manager, clinician, teacher, regulator, institution or specialist system may have context-bounded authority or source-of-record status for one facet.

That does not grant universal authority over every Criterion, Evidence source, target or visibility boundary.

LifeOS may coordinate around specialist evaluation without rebuilding the specialist administrative system.

Specialist scoring, legal validity, clinical interpretation, educational certification and other domain-specific evaluation semantics may remain in adapters/extensions where appropriate.

---

# 20. AI boundary

AI may:

- propose a Criterion;
- translate a user Goal into candidate evaluative forms;
- discover candidate Evidence;
- calculate an Evaluation under an authorized deterministic rule;
- identify missing/conflicting Evidence;
- explain an Evaluation within the viewer's Visibility;
- recommend reevaluation or review.

AI must not:

- infer that a proposed Criterion was historically the user's intention;
- fabricate Evidence/source facts;
- convert confidence into Authority or Source Precedence;
- hide contradictory Evidence to create a neat result;
- infer human Agreement/Consent/Acknowledgement from evaluation behavior;
- expose private Evidence through explanations/tool arguments;
- treat an Evaluation as effective target state without applicable policy/Authority.

Canonical rule:

> **AI may reason within Criterion/Evaluation semantics, but AI confidence and access do not create human intention, Evidence, Authority, common ground or disclosure permission.**

---

# 21. Scale and materialization

Criterion/Evaluation can be high-volume:

- rolling weekly evaluations;
- years of measurements;
- high-frequency sensor sources;
- many Goals reusing the same Evidence;
- continuous trend computation;
- repeated recalculation after correction/import.

Semantic correctness must not require one durable Evaluation record for every query/tick.

Valid future strategies include:

- derive Evaluation on demand;
- cache/materialize a projection;
- persist consequential snapshots;
- retain reconstructible source/rule basis;
- delegate detailed specialist state to an authoritative external system.

Physical optimization may denormalize but cannot redefine semantic truth/history.

---

# 22. Product simplicity

Most users should not have to manage `Criterion`, `Evaluation`, Evidence graphs or rule versions explicitly.

Natural UI may show:

```text
Goal
Train 3 times this week

2 / 3 completed
Based on 2 verified Sessions
```

or:

```text
B2 progress
Not enough evidence yet
Next assessment: September
```

Power/high-consequence surfaces may expose:

- Criterion details;
- evaluation window;
- source/Evidence basis;
- contradictions;
- material rule version;
- specialist source;
- historical evaluations;
- Authority/Decision basis.

Kernel precision must remain compatible with progressive disclosure.

---

# 23. Core invariants

1. Criterion is contextual evaluative specification/capability, not universal native identity/root.
2. GoalCriterion is Goal-scoped Criterion semantics, not a separate universal primitive.
3. Evaluation is contextual reasoning/process-result semantics, not a universal entity/root/workflow.
4. Goal != Criterion.
5. Milestone != Criterion.
6. Criterion != Evidence.
7. Evaluation != Evidence.
8. Evaluation != Actual.
9. Evaluation != Outcome.
10. Evaluation != Decision.
11. Evaluation != Reconciliation.
12. Evaluation != Authority.
13. Evaluation != Confirmation.
14. Criterion != Temporal Constraint.
15. Criterion != Trigger.
16. No Evidence != Evidence against.
17. Missing Evidence != Criterion failure by default.
18. Unknown/insufficient Evidence may remain unknown/indeterminate.
19. Absence becomes negative only under a justified completeness/negative-observation rule.
20. Conflicting Evidence may remain unresolved and need not yield a forced result.
21. Source identity/recency/frequency/AI confidence does not create universal precedence.
22. Criterion material state may matter historically.
23. Historical Evaluation must preserve/reconstruct materially applicable Criterion/source/target states where consequential.
24. Later Criterion change does not retroactively rewrite earlier Evaluation rules.
25. Later Evidence/correction may change current evaluation without rewriting earlier basis.
26. Multiple criteria do not imply one universal composition operator.
27. Goal Progress is derived/evaluation projection, not universal stored percentage/status.
28. Evaluation result does not automatically make target state current/effective.
29. Criterion/Evaluation does not create Authority, Agreement, Consent or human common ground.
30. Shared Evaluation result does not imply shared Visibility of all Evidence.
31. AI may propose/calculate but cannot fabricate intention, Evidence, Authority or disclosure permission.
32. A transient Evaluation need not be persisted.
33. Materialized evaluation history is consequence-sensitive.
34. Specialist evaluation authority remains bounded to the specialist context/facet.
35. Exact persistence, expression language and physical cardinalities remain downstream decisions.

---

# 24. Rejected alternatives

Rejected as universal LifeOS kernel defaults:

```text
Goal = target_value field
GoalCriterion as separate universal root
Criterion = Evidence
Criterion = Milestone
Criterion = Temporal Constraint
Criterion = Trigger
Evaluation = current Goal state
Evaluation = Decision
Evaluation = Reconciliation
Evaluation entity/root for every assessment
universal evaluation workflow/state machine
missing Evidence = failure
latest Evidence wins
most frequent source wins
all criteria always AND
all criteria averaged
universal progress percentage
universal Goal score
universal confidence score
one global criterion DSL pre-approved now
one persisted evaluation row per rolling query/tick
AI evaluation = truth
```

---

# 25. Adjacent Dependency Sweep summary

Resolved now:

```text
Goal ↔ Criterion
Milestone ↔ Criterion
Evidence ↔ Criterion / Evaluation
Actual / Outcome ↔ Evaluation
Decision ↔ Evaluation
Reconciliation ↔ Evaluation
Authority ↔ Evaluation
Version ↔ Criterion material state / historical Evaluation
Visibility ↔ private Evidence / shared result
Goal Progress ↔ Evaluation
```

SAFE DEFERRED with executable owners/triggers:

- Trigger / conditional policy;
- comparator/range/threshold logical value representation;
- composite Criterion / expression representation;
- Verification / comprehension;
- specialist evaluation/adjudication structures;
- retention/materialized Evaluation snapshots;
- Proposal/Request identity for proposed Criterion changes;
- logical/physical/API representation.

```text
REOPEN                         0
unclassified material items    0
```

Normative details are recorded in `../checkpoints/criterion-evaluation-v0-validation.md`.

---

# 26. Persistence/API implications without physical commitment

A future logical model must be able, where material, to represent or reconstruct:

- bounded evaluation target;
- Criterion identity/state or equivalent reconstructible rule reference where consequence requires;
- evaluation purpose/context;
- applicable time/window/period;
- eligible Evidence/source set or reconstructible selection basis;
- material source/target/rule states;
- support/contradiction/qualification where necessary;
- unresolved/indeterminate evaluation;
- evaluator/Actor/represented party where material;
- applicable Authority/policy/specialist basis;
- historical result/basis where consequence requires;
- independent Visibility of Criterion/result/Evidence/history.

This does **not** pre-approve:

```text
criteria table
goal_criteria table
evaluations table
progress_percentage column
one status enum
universal expression AST/DSL
universal polymorphic target FK
one row per rolling evaluation
one confidence field
one weighting algorithm
trigger/actions embedded in Criterion
```

---

# 27. Reopening triggers

Reopen Criterion / Evaluation v0 if later evidence shows that:

1. Criterion can be fully absorbed into Goal/Milestone/Decision/Trigger without semantic loss;
2. Goal-scoped Criterion requires materially different identity/lifecycle from the broader Criterion family;
3. Evaluation requires a universal persistent lifecycle/identity rather than consequence-sensitive process/result semantics;
4. multiple-criterion composition cannot be represented without changing the accepted Criterion boundary;
5. specialist evaluation requires a stronger common abstraction across domains;
6. historical reproducibility cannot be preserved with Version/Evidence without universal snapshots;
7. missing/conflicting Evidence semantics cannot preserve unknown/indeterminate states;
8. shared/private evaluation cannot preserve Visibility and Authority boundaries;
9. logical/persistence pressure demonstrates a structural contradiction rather than an implementation preference;
10. whole-domain regression shows Criterion/Evaluation adds more complexity than it removes.

Vocabulary or database convenience alone is not sufficient reason to reopen.

---

# 28. Current validation position

Normative validation checkpoint:

- `../checkpoints/criterion-evaluation-v0-validation.md`

Current V3 result:

```text
CRITERION / EVALUATION v0
PASS WITH HARDENING

CORE gate                       PASS WITH HARDENING
Multi-Actor gate                PASS WITH HARDENING
Cross-Concept gate              PASS WITH HARDENING
REOPEN                          0
unclassified material items     0
```

No next Relationships / Reasoning candidate is selected by this document. After post-write QA, candidate selection must return to a fresh re-score of the remaining candidate space.
