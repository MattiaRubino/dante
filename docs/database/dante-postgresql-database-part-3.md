# DANTE PostgreSQL Database — Architecture, Reference & Whole-Database Blueprint — Part 3

- **Status:** CP6-03 ACTIVE / CANONICAL CONTINUATION / GATE 03 NOT YET EARNED
- **Created:** 2026-08-23
- **Product:** DANTE
- **Database:** PostgreSQL 18 major family
- **Current repository patch:** PostgreSQL 18.6
- **Schema:** `dante`
- **Workstream:** `../workstreams/logical-postgresql.md`
- **Database documentation authority:** `README.md`
- **Part 1:** `dante-postgresql-database.md` — sections 1–30
- **Part 2:** `dante-postgresql-database-part-2.md` — section 31
- **Continuation numbering:** section 32 onward
- **Continuation anchor:** `6a8605130bc9ec46c3751f03296b3bc34c484131`
- **Implementation status:** business schema / business SQLAlchemy mappings / product vertical **NOT YET MATERIALIZED**

---

## Canonical continuity contract

This file is the canonical continuation of Parts 1 and 2. It does not replace, summarize or supersede either prior part as a whole.

```text
dante-postgresql-database.md
PART 1 / sections 1–30
+

dante-postgresql-database-part-2.md
PART 2 / section 31
+

dante-postgresql-database-part-3.md
PART 3 / section 32 onward
=

ONE CANONICAL HUMAN-READABLE
DANTE DATABASE ARCHITECTURE & REFERENCE
```

Readers, reviewers, migrations, implementation work, Database Dictionary reconciliation and whole-database audits MUST consume all active parts. Part 3 exists only to keep writes bounded and safe; it introduces no independent semantic authority.

The write-preservation, explicit-supersession and whole-database cumulative-audit rules established in Part 2 remain fully applicable.

---

## 32. Consolidation checkpoint E — Criterion / Evaluation baseline disposition

### 32.1 Scope and authority

This checkpoint closes the two remaining exact local blockers concerned with evaluative specification and evaluative process/result persistence:

```text
CRT-U01
EVL-U01
```

The decision is derived from the complete accumulated authority, including:

```text
Criterion / Evaluation Domain v0
Criterion / Evaluation v0 Validation — Methodology v3
Logical Slice B — Intention / Execution
Logical Slice C — Time / Reality
Logical Slice D — Evidence / Knowledge / History
Whole-Logical 57/57 model
CP6-01 persistence coverage
accepted PostgreSQL Physical mapping
CP6-02 Persistence Constitution / ADR-010
Part 1 sections 1–30, especially section 27
Part 2 section 31 Outcome / Milestone closure
real CP3 PostgreSQL/Alembic/SQLAlchemy foundation
```

This is a physical closure only. It does not redefine Criterion or Evaluation semantics and it does not infer a universal rules language from the examples in the Domain.

The decisive authority facts are:

```text
Criterion
→ contextual LR-05 evaluative specification / capability
→ may require material state when historical consequence exists
→ is not a universal native root

Evaluation
→ LR-08 derived contextual reasoning/process-result by default
→ may become LR-02 material snapshot only when consequence/reproducibility/history requires it
→ need not be persisted for ordinary transient evaluation
```

The Domain and validation material deliberately leave exact physical representation, comparator/range/threshold structures, composite-expression representation, materialized Evaluation snapshots, API/SQL cardinality, indexing and caching to downstream physical design. No accepted repository authority provides a first concrete profile whose complete SQL contract is already deterministic.

Therefore the maximum non-speculative CP6 baseline result is:

```text
Criterion
→ semantic capability retained
→ no baseline Criterion business DDL

Evaluation
→ derived capability retained
→ no baseline canonical Evaluation business DDL
```

These are final baseline dispositions, not placeholders waiting for arbitrary generic columns.

### 32.2 Criterion semantic boundary retained

Criterion remains the contextual evaluative specification that defines how a bounded target is assessed for a defined purpose/context.

Canonical non-collapse remains:

```text
Criterion != Goal
Criterion != Milestone
Criterion != Evidence
Criterion != Evaluation
Criterion != Temporal Constraint
Criterion != Trigger / Conditional Policy
Criterion != Decision
Criterion != Authority
```

A Criterion may describe semantics such as:

```text
boolean condition
threshold at/above or at/below a typed value
target value
acceptable range
accumulation
frequency within a period
duration within a period
Milestone/checkpoint attainment
trend/directional change
external result
manual/qualitative assessment
composite criteria
```

but this list establishes required semantic expressiveness only. It is not authorization for one PostgreSQL enum, one `kind` column, one AST, one DSL or one generic table family.

### 32.3 CRT-U01 — CLOSED with NO CP6 baseline Criterion DDL

Part 1 section 27.1 correctly closed Criterion ownership/materialization discipline while keeping the first concrete typed payload/profile open.

The cumulative audit now closes that remaining blocker by explicit non-materialization because no accepted first profile supplies all required physical semantics.

CP6-04 MUST NOT create generic objects equivalent to:

```text
dante.criterion
dante.goal_criterion
criterion_kind
criterion_type
operator_code
comparison_code
value_text
value_numeric + unit without a concrete value contract
criterion_expression text
criterion_ast
criterion_payload jsonb
rule_payload jsonb
universal criterion enum
universal criterion component table
```

Closed baseline disposition:

```text
CRT-U01
CLOSED

CP6-04 BASELINE CRITERION BUSINESS OBJECTS
0
```

This does not remove Criterion from Domain/Logical authority. It prevents a generic placeholder representation from becoming accidental canonical semantics.

### 32.4 Why accepted examples do not authorize a first SQL profile

Representative examples such as:

```text
>= 3 qualifying training Sessions per week
recognized B2 assessment result
balance >= EUR 20,000
weight in accepted range for a sustained period
Milestone attained
manual qualitative assessment
```

demonstrate that Criterion semantics are required, but they do not jointly close one physical structure.

Each example leaves profile-specific questions such as:

```text
which target family/state is evaluated?
what typed value semantics apply?
which comparator semantics are valid?
what unit/currency/range normalization is authoritative?
what temporal frame/window applies?
which source records/states count as eligible Evidence?
what does missing Evidence mean under this profile?
how are conflicting sources treated?
what composition operator applies when several components exist?
which result semantics are produced?
when does a rule change become materially new/current?
```

DANTE MUST NOT hide those unanswered questions inside `operator_code`, expression text or JSON.

### 32.5 Future owner-bound Criterion materialization contract retained

The ownership rule from Part 1 section 27.1 remains authoritative for future concrete profiles:

```text
OWNER / CONSUMER-BOUND CRITERION
→ typed material state/children owned by the concrete target/policy context
→ no independent Criterion identity merely for storage uniformity
```

A concrete owner-bound profile may eventually take a shape conceptually like:

```text
<owner>.<criterion-facet>
→ one complete MaterialStateRef
→ exact typed component rows belonging to that state
```

but only the concrete profile may define its table/column names and payloads.

The baseline does not pre-register a generic `criterion.definition` MaterialState facet because no generic Criterion owner exists.

### 32.6 Multi-Criterion set semantics retained

The already-closed current-binding topology permits one current MaterialStateRef per owner/facet:

```text
PRIMARY KEY(owner_ref, facet_code)
```

Therefore, when one owner/context semantically supports multiple simultaneously applicable Criterion components, the future physical rule remains:

```text
one complete current Criterion-set state
→ one MaterialStateRef for the owner/facet
→ N exact typed criterion components inside that state
```

and not:

```text
N unrelated current MaterialStateRefs competing under the same owner/facet
```

A materially changed set produces a new complete MaterialStateRef where historical consequence requires it.

DANTE does not introduce a generic `criterion_id` merely to bypass the current-binding model. Component identity is added only when a particular Criterion genuinely has independent identity/lifecycle/reference semantics.

### 32.7 Independently scoped Criterion threshold retained

A future Criterion becomes an independently scoped contextual record only when a concrete contract proves independent semantic pressure such as:

```text
independent addressability
reuse by multiple bounded consumers
cross-record reference
independent reconciliation
independent lifecycle/history
independent governance/visibility
```

Only at that threshold may a concrete profile introduce:

```text
ScopedRecordRef(Criterion-profile)
+ scoped_address registration
+ owner-specific MaterialState definition/currentness
```

Criterion does not become LR-01 NativeRef. The accepted native-owner count remains exactly 15.

### 32.8 Future concrete Criterion profile trigger

The first future material Criterion family must close a complete typed contract before schema evolution is authorized.

Minimum required trigger information:

```text
exact owning consumer/context
exact target Reference Contract
exact target-state eligibility where target MaterialState matters
exact typed rule/value structure
exact comparator/range/threshold semantics where applicable
exact unit/currency/value normalization where applicable
exact temporal window/period frame where applicable
exact Evidence eligibility
exact source completeness / missing-data semantics
exact conflict/reconciliation interaction
exact component cardinality
exact multi-component composition rule
exact result/assessment profile expected downstream
exact materiality/history/currentness contract
exact governance/Visibility requirements where material
```

A future schema review may close one small profile without solving every possible Criterion family globally. Additive specialist evolution is preferred to premature universalization.

### 32.9 Typed value and comparison boundary

Criterion comparison semantics must reuse or extend accepted typed value semantics rather than treating SQL scalar type as complete semantic meaning.

Examples:

```text
5 km
EUR 20,000
B2 level
3 qualifying Sessions
70–80 kg
```

are not interchangeable merely because some may use `numeric` or text in PostgreSQL.

A future criterion profile must make exact distinctions among applicable:

```text
magnitude/value
unit or currency
normalization/conversion basis
comparison direction
inclusive/exclusive bound semantics
range geometry
ordered versus categorical value domain
source measurement precision where relevant
```

No global `value_numeric`, `unit_code`, `operator_code` schema is introduced by this checkpoint.

### 32.10 Criterion temporal-window boundary

An evaluation window/period inside Criterion semantics does not become Schedule or Temporal Constraint.

Canonical distinction:

```text
Criterion: >= 3 qualifying Sessions per calendar week
Temporal Constraint: do not schedule training after 21:00
Schedule: accepted placement Tuesday 18:00
```

A future criterion profile that depends on a period must close the applicable frame explicitly, for example calendar week under a named/owner-bound frame, rolling duration or another accepted profile-specific window.

The database must not silently inherit device locale, current timezone, ISO-week assumptions or a library default unless that behavior is the accepted semantic contract.

### 32.11 Evidence eligibility and completeness are profile-owned

Criterion may define what Evidence is relevant and what absence means, but no universal completeness policy is accepted.

Mandatory epistemic separation remains:

```text
no Evidence
!= Evidence against
!= Criterion not satisfied
!= non-occurrence
```

A future profile may assign negative meaning to absence only when it explicitly owns a justified completeness/negative-observation contract, for example a bounded authoritative source-of-record interval.

Therefore there is no baseline column such as:

```text
missing_means_failure boolean
source_is_complete boolean
```

on a universal Criterion table.

### 32.12 Criterion composition remains contextual

A target may require several Criteria or several typed components, but DANTE assumes no universal composition operator.

Not globally accepted:

```text
all components AND
any component OR
weighted average
arithmetic mean
lowest score wins
highest score wins
boolean expression text
```

Concrete profiles may define:

```text
all mandatory components satisfied
one of several alternatives
mandatory + optional components
threshold + sustained duration
ordered specialist adjudication
manual qualitative composition
other bounded typed rule
```

Composition must be represented by the concrete family that owns its semantics. CP6 does not introduce a generic expression engine merely to make all future evaluation possible in one schema.

### 32.13 Criterion material-state/history boundary

When a future Criterion profile has material historical consequence:

```text
Criterion definition at T1 = C1
later accepted definition at T2 = C2
```

historical Evaluation E1 remains bound to C1 where that state mattered.

Forbidden:

```text
Evaluation E1 stores only owner_ref
→ later reads current Criterion C2
→ historical meaning silently changes
```

A future consequential profile therefore uses exact MaterialStateRef or another equally reconstructible exact typed rule-state anchor accepted by that profile.

Criterion material-state identity is semantic state identity, not:

```text
updated_at
row revision
provider revision
content hash
MVCC xmin
```

### 32.14 Evaluation semantic boundary retained

Evaluation remains contextual application of the materially applicable Criterion semantics to relevant Evidence under the applicable target/time/context/governance basis.

Canonical non-collapse remains:

```text
Evaluation != Criterion
Evaluation != Evidence
Evaluation != Actual
Evaluation != Outcome
Evaluation != Milestone
Evaluation != Decision
Evaluation != Reconciliation
Evaluation != Authority
Evaluation != Confirmation
Evaluation != target current/effective state
```

Evaluation can be deterministic, manual, specialist-assisted, policy-governed or partially derived according to the concrete context. Those possibilities do not imply one universal evaluation workflow.

### 32.15 Derived-by-default Evaluation remains canonical

Ordinary reproducible/transient Evaluation is not canonical persistence merely because the product displays it.

Examples:

```text
2 of 3 qualifying Sessions this week
current balance / target balance
current B2 evidence summary
current trend calculation
```

may be evaluated on demand from canonical typed sources when this remains correct and performant.

The baseline rule is:

```text
ordinary Evaluation
→ LR-08 derived/process-result
→ no canonical row required
```

A screen refresh, planner pass, query execution or periodic recomputation does not mint an Evaluation identity automatically.

### 32.16 EVL-U01 — CLOSED with NO CP6 baseline Evaluation DDL

Part 1 section 27.2 correctly defined the material-snapshot threshold but left the first consequential profile open.

No accepted repository authority currently closes a first profile with exact target, Criterion, Evidence, result, chronology and material identity/currentness semantics.

Therefore CP6-04 MUST NOT create generic objects equivalent to:

```text
dante.evaluation
evaluation_status
evaluation_result_code
evaluation_score
evaluation_confidence
evaluation_payload jsonb
evaluation_context jsonb
generic evaluation workflow/state machine
generic evaluation current table/view
```

Closed baseline disposition:

```text
EVL-U01
CLOSED

CP6-04 BASELINE CANONICAL EVALUATION BUSINESS OBJECTS
0
```

This preserves Evaluation semantics while preventing a generic assessment row from becoming an accidental universal truth store.

### 32.17 Consequential material Evaluation trigger

A future Evaluation snapshot becomes canonical persistence only when consequence/reproducibility/history requires retaining the exact assessment and its basis.

A concrete material profile must establish at minimum:

```text
exact evaluation owner/context
exact target Reference Contract
exact target MaterialStateRef requirement where target state matters
exact Criterion MaterialStateRef / reconstructible typed rule state
exact Evidence/source basis
exact Evidence completeness rules
exact evaluation window/period/context
exact assessment/result semantics
exact unknown/indeterminate semantics
exact evaluator/Actor attribution where material
exact represented party where material
exact Authority/policy/specialist basis where material
exact world/effective chronology where relevant
exact recorded/accepted chronology where relevant
exact correction/reevaluation/reconciliation behavior
exact material identity/currentness requirement, if any
```

Only after those facts are accepted may Alembic/SQLAlchemy materialize that concrete profile.

### 32.18 Exact target-state basis

A material historical Evaluation must not silently follow current target state where target material state affected the assessment.

Example:

```text
Goal/target state G3
+ Criterion state C1
+ Evidence S1/S2
→ Evaluation E1
```

Later target correction/revision to G4 does not change what E1 evaluated.

A concrete profile therefore binds `target MaterialStateRef` when the material target state is part of the evaluative claim. If stable identity alone is sufficient, that narrower profile may use identity only; the profile must decide explicitly.

### 32.19 Exact Criterion-state basis

A consequential Evaluation under Criterion state C1 remains under C1 after C2 becomes current.

```text
E1 → exact C1 basis
current Criterion later = C2
E1 remains historically C1-based
new/current reevaluation may produce E2 under C2
```

Criterion revision does not retroactively rewrite historical evaluation rules.

### 32.20 Exact Evidence/source basis

Where source state matters, a consequential Evaluation snapshot must bind the exact source MaterialStateRef actually used.

Forbidden:

```text
Evaluation stores source identity only
→ later source correction changes historical evaluation input silently
```

When source material-state distinction is not part of the claim, a narrower reference may be sufficient. The concrete profile owns that decision.

### 32.21 Evaluation window and chronology

Evaluation chronology may involve distinct questions:

```text
what world/effective interval is evaluated?
when was the assessment calculated/recorded?
when did it become accepted/current for a bounded context?
when was it later corrected/reconsidered?
```

No universal four-timestamp Evaluation table is introduced. A future profile stores only the chronology its semantics require. Database insertion time is never a substitute for evaluation-window meaning.

### 32.22 Assessment/result semantics are profile-specific

Potential semantics such as:

```text
satisfied
not satisfied
partial
unknown
indeterminate
insufficient Evidence
specialist/manual result
```

are not a universal PostgreSQL enum.

Therefore CP6 does not create generic `assessment_code`, score or confidence fields.

### 32.23 Missing and conflicting Evidence remain epistemically honest

The database/model retains:

```text
missing Evidence
!= negative Evidence
!= failed Evaluation

conflicting Evidence
!= automatic forced result
```

If a concrete profile cannot justify resolution, Evaluation may remain unknown/indeterminate/unresolved. Source recency, frequency or AI confidence does not become global Source Precedence.

### 32.24 Evaluation does not own target effect

A material Evaluation result does not make a target current/effective merely because a row exists.

```text
Evaluation says satisfied
!= automatic Goal/Milestone/target mutation
```

The owning concept plus applicable Decision, Authority or authorized policy owns consequential effect.

### 32.25 No generic Evaluation current binding

The baseline creates no universal concept of `current Evaluation` because possible meanings differ:

```text
latest calculation
latest recorded snapshot
currently applicable accepted assessment
projection over current Evidence
latest specialist adjudication
```

A future concrete profile may define explicit currentness only if semantically required; it may never infer current from `created_at`, UUID order or latest row.

### 32.26 Correction and reevaluation semantics

Historical correction and reevaluation remain distinct.

```text
E1 under C1 + S1/S2
later S2 corrected
→ E1 basis remains reconstructible
→ E2 may be produced where reevaluation is required
```

A direct correction of E1 itself follows profile-specific MaterialState/Reconciliation semantics. No generic `superseded_by_evaluation_id` or universal lifecycle enum is introduced.

### 32.27 Evaluator / represented party / Authority boundary

Potential roles remain distinct:

```text
target subject
Evidence source actor
recorder
evaluator
represented party
Authority holder
viewer
beneficiary
```

Future concrete profiles use the existing Actor/Representation/Authority contracts. Evaluator does not automatically equal subject or Authority holder; AI evaluator does not automatically become authoritative human assessment.

### 32.28 Shared result versus private Evidence

A shareable Evaluation result may be supported by Evidence not visible to every viewer of that result.

```text
private Evidence
→ authorized Evaluation
→ bounded shareable result
```

must not imply Evidence disclosure. Criterion/result/Evidence Visibility remain independently governed where applicable.

### 32.29 Evidence remains contextual use, not a universal root

Because no concrete material Evaluation profile exists in the baseline, this checkpoint authorizes no generic Evidence-use table merely to prepare for future evaluation.

CP6-04 MUST NOT create generic:

```text
dante.evidence
evidence_source
evidence_target
evidence_strength
confidence
support_code
universal evidence graph
```

Evidence semantics remain authoritative and materialize only in consumer/profile-specific relations when a real consequential use requires them.

### 32.30 Future material Evidence-use association pattern

A concrete material profile may use profile-specific FK-backed associations. For heterogeneous sets, the already-closed DB-U22 pattern remains applicable:

```text
<profile>_evidence_native
<profile>_evidence_scoped
<profile>_evidence_material_state
```

only for admitted address spaces/families. Each row owns real FK and eligibility constraints; no generic `kind + uuid` fallback exists.

### 32.31 Evidence payload and certainty boundary

Evidence use does not duplicate source payload by default.

Forbidden universal pattern:

```text
evidence_data jsonb
source_snapshot jsonb copied by convenience
confidence numeric
strength numeric
weight numeric
```

A concrete specialist profile may define bounded weight/quality semantics if genuinely required. Source truth, Evidence relevance and assessment result remain separate.

### 32.32 Goal Progress remains derived

Goal Progress remains LR-08/evaluation projection rather than universal canonical state.

Useful product forms may include:

```text
EUR 5,000 / EUR 20,000
2 of 3 qualifying Sessions
within range for 5 of 6 months
B1 attained / B2 not established
on trajectory / off trajectory / unknown
```

but CP6-04 does not create `progress_percentage`, generic Goal score/status or `dante.goal_progress` merely because these views are useful.

### 32.33 Milestone and Outcome integration after Checkpoint D

Checkpoint D remains intact:

```text
Outcome → NO baseline DDL
Milestone → NO baseline DDL
```

Criterion/Evaluation closure does not silently rematerialize either concept. Future typed Outcome may become Evidence for future Evaluation. Future concrete Milestone attainment may be evaluation-backed. Those future contracts trigger schema evolution only when their exact profiles exist.

### 32.34 Temporal Constraint remains separate and open

`TC-U01` remains an exact local blocker.

Criterion does not solve Temporal Constraint by providing a generic predicate language.

```text
Criterion → how a target is evaluated
Temporal Constraint → where/when placement, duration or temporal relation is constrained/preferred
```

Temporal Constraint may later participate in compliance/violation Evaluation without collapsing into Criterion.

### 32.35 Agreement remains separate and open

`AGR-U01` remains open.

```text
Evaluation result
!= Agreement
!= assent
!= Consent
!= Acknowledgement
```

Criterion/Evaluation does not become a generic Agreement-terms representation.

### 32.36 CP6 baseline object-inventory consequences

Exact baseline result:

```text
CRITERION
canonical business tables             0
generic scoped-address families       0
generic MaterialState facets          0
generic current-binding views         0
indexes                               0
business triggers                     0
SQLAlchemy mappings                   0
runtime ACL objects                   0

EVALUATION
canonical business tables             0
generic scoped-address families       0
generic MaterialState facets          0
generic current-binding views         0
indexes                               0
business triggers                     0
SQLAlchemy mappings                   0
runtime ACL objects                   0

GENERIC EVIDENCE-USE INFRASTRUCTURE
canonical business tables             0
indexes                               0
SQLAlchemy mappings                   0
runtime ACL objects                   0
```

This zero-object result must be preserved when final inventory, DB-U15 and DB-U21 are frozen.

### 32.37 Database Dictionary consequences

The Database Dictionary table/view catalogs describe real PostgreSQL objects only. They MUST NOT advertise generic `criterion`, `goal_criterion`, `evaluation` or `evidence` tables that do not exist.

A separate non-materialized-capability/decision register may later cite `CRT-U01`/`EVL-U01` if useful, without contaminating SQL object catalogs.

### 32.38 Alembic migration consequences

CP6-04 baseline migrations MUST NOT create generic Criterion/Evaluation/Evidence objects, types, current views, scoped-address families, MaterialState facets, indexes, triggers or grants.

A future concrete profile is introduced by a reviewed additive migration. No historical backfill may fabricate prior Criterion/Evaluation/Evidence rows unless a deterministic auditable backfill contract is separately accepted.

### 32.39 SQLAlchemy mapping consequences

CP6-04 MUST NOT introduce generic mapped semantic roots such as:

```text
Criterion
GoalCriterion
CriterionComponent
Evaluation
EvaluationResult
Evidence
```

solely to mirror Domain names.

Reusable typed Python helpers are allowed when they encode real concrete values, but helper reuse does not create semantic inheritance or generic table identity.

### 32.40 Runtime/API boundary

Runtime must not hide missing canonical schema in:

```text
Goal.metadata["criterion"]
Goal.metadata["progress"]
generic semantic JSON
free-text expression fields
generic status/result fields
provider payload promoted to canonical Criterion/Evaluation
```

A vertical requiring durable concrete Criterion or consequential Evaluation performs schema evolution first. Transient deterministic Evaluation may remain application/query logic over canonical sources when persistence threshold is not crossed.

### 32.41 DB-U21 privilege consequences

No baseline Criterion/Evaluation/Evidence business objects exist, so final ACL inventory contains no imagined entries for them.

The accepted direction remains migration-owned least privilege. Future immutable material snapshots receive only exact DML required by their operation contract; ordinary UPDATE/DELETE remain denied absent specific lifecycle semantics.

### 32.42 DB-U14 lifecycle consequences

No generic Criterion/Evaluation lifecycle enum or soft-delete columns are introduced.

Future material states remain under:

```text
ON DELETE NO ACTION by default
no ordinary destructive history rewrite
no universal deleted_at/is_deleted
MaterialStateRef non-retargeting
redaction/tombstone only under concrete policy
```

Criterion becoming non-current is not historical deletion. Reevaluation superseding an assessment is not erasure of the prior material snapshot.

### 32.43 DB-U15 index consequences

No generic Criterion/Evaluation/Evidence indexes are added. The final DB-U15 matrix evaluates only actual frozen structures and actual query/integrity pressure. Future profile indexes require an explicit PK/UNIQUE/FK/query reason.

### 32.44 DB-U20 projection/search consequences

Derived Evaluation and Goal Progress do not automatically justify persisted projections, materialized views, search tables or vector embeddings.

```text
cheap/reconstructible result → derive
proven expensive consumer/freshness need → DB-U20-reviewed projection/cache
```

Any future persisted projection remains rebuildable and traceable to canonical source/material basis.

### 32.45 Direct CP6-04/05 absence-proof obligations

Final schema/mapping QA must prove at least:

```text
no dante.criterion table                                  PASS
no dante.goal_criterion table                             PASS
no generic Criterion enum/type                            PASS
no generic operator/expression/JSON fallback              PASS
no generic Criterion scoped_address family                PASS
no generic Criterion MaterialState facet                  PASS

no dante.evaluation table                                 PASS
no generic evaluation status/result/score/confidence      PASS
no generic Evaluation current binding/view                PASS
no universal evaluation workflow                          PASS

no dante.evidence generic table                           PASS
no universal evidence-strength/confidence scalar          PASS
no generic source kind+uuid Evidence relation             PASS

no universal Goal progress persistence                    PASS
no generic Criterion/Evaluation SQLAlchemy roots          PASS
no generic Criterion/Evaluation/Evidence ACL entries      PASS
Database Dictionary advertises no non-existent objects    PASS
```

These are implementation obligations, not tests claimed executed by this documentation checkpoint.

### 32.46 Future concrete Criterion proof obligations

The first concrete Criterion family must prove its exact target, typed rule/value semantics, component totality, window/frame, Evidence completeness, history and rejection behavior.

At minimum:

```text
valid target/reference accepted                           PASS
wrong target family/state                                 REJECT
valid typed payload                                       PASS
invalid comparator/value/unit/range                       REJECT
complete component set                                    PASS
invalid/incomplete set                                    REJECT
profile window/frame enforced                             PASS
missing Evidence follows profile semantics                PASS
Criterion revision preserves exact historical state       PASS
no generic JSON/expression escape                         PASS
```

### 32.47 Future material Evaluation proof obligations

A future consequential profile must prove exact target, Criterion and Evidence basis, profile result semantics and history stability:

```text
valid exact target basis                                  PASS
wrong target state/family                                 REJECT
valid Criterion-state basis                               PASS
wrong Criterion state/family                              REJECT
valid Evidence basis                                      PASS
wrong/dangling Evidence state                             REJECT
unknown/indeterminate preserved                           PASS
later Criterion revision does not mutate historical E1    PASS
later source correction does not mutate historical E1     PASS
reevaluation may create E2 without erasing E1             PASS
Evaluation existence alone does not mutate target         PASS
private Evidence not exposed by result persistence        PASS
```

If a concrete profile has currentness, it must be explicit and never inferred from storage chronology.

### 32.48 Whole-database A/B/C cumulative audit — findings

The complete accumulated database was replayed after closing CRT-U01 and EVL-U01.

| Finding | Class | Repair / final disposition |
|---|---|---|
| universal Criterion root | C | rejected; CRT-U01 closed NO baseline DDL |
| universal GoalCriterion root | C | rejected |
| generic operator/value model | C | rejected; concrete typed profile required |
| generic Criterion JSON/AST/DSL | C | rejected |
| competing current MaterialStates per criterion component | B/C | retain one complete Criterion-set state per owner/facet |
| generic Criterion identity inflation | C | rejected |
| examples treated as complete SQL vocabulary | B/C | rejected |
| universal Evaluation root | C | rejected; EVL-U01 closed NO baseline DDL |
| durable Evaluation per query/tick | C | rejected; derived by default |
| universal assessment/status enum | C | rejected |
| universal score/confidence | C | rejected |
| missing Evidence = failure | C | rejected |
| conflict forced to one result | C | rejected |
| recency/frequency/AI confidence = precedence | C | rejected |
| historical Evaluation follows current target | C | exact target state required when material |
| historical Evaluation follows current Criterion | C | exact Criterion state required |
| historical Evaluation follows corrected Evidence | C | exact source state required |
| Evaluation row mutates Goal/Milestone | C | rejected |
| current Evaluation inferred from latest row | C | rejected |
| generic Evidence graph | C | rejected |
| Evidence payload copied generically | C | rejected |
| universal Goal progress percentage/score | C | rejected |
| projection created without DB-U20 consumer | B/C | rejected |
| speculative mappings/ACL/indexes for zero objects | B/C | explicit zero inventory |

No finding requires reopening Domain, Whole-Logical, Physical, CP6-01 or CP6-02.

### 32.49 Whole-database A/B/C cumulative audit — retained invariants

```text
57 / 57 Domain concepts                                PASS
15 / 15 LR-01 native owners                            PASS
NativeRef != ScopedRecordRef                           PASS
ScopedRecordRef != MaterialStateRef                    PASS
MaterialState existence != current                      PASS
current binding never inferred from timestamp/UUID     PASS
DB-U14 non-destructive lifecycle                        PASS
DB-U12 recurrence / Occurrence closure                  PASS
Schedule / Session / Actual separation                  PASS
Outcome / Milestone Checkpoint-D dispositions           PASS

Criterion != Goal                                       PASS
Criterion != Milestone                                  PASS
Criterion != Evidence                                   PASS
Criterion != Evaluation                                 PASS
Criterion != Temporal Constraint                        PASS
Criterion != Trigger                                    PASS
Evaluation != Evidence                                  PASS
Evaluation != Actual                                    PASS
Evaluation != Outcome                                   PASS
Evaluation != Milestone                                 PASS
Evaluation != Decision                                  PASS
Evaluation != Reconciliation                            PASS
Evaluation != Authority                                 PASS
Evaluation != Confirmation                              PASS
Evaluation != effective target state                    PASS
no Evidence != Evidence against                         PASS
missing Evidence != failure                             PASS
conflicting Evidence may remain unresolved              PASS
historical target/rule/source basis                      PASS
Goal Progress remains derived                            PASS

universal Entity/Thing root                              0
universal Relationship/edge root                         0
universal Criterion root                                 0
generic Criterion DSL/JSON                               0
universal Evaluation root                                0
universal Evidence root                                  0
universal Goal progress                                  0
semantic JSON fallback                                   0
new LR-01 owner                                          0
new unclassified item                                    0
C defects after repair                                   0
```

### 32.50 Exact unresolved-register transition

Before this checkpoint:

```text
AGR-U01
CRT-U01
EVL-U01
TC-U01
COUNT = 4
```

Closed now:

```text
CRT-U01
EVL-U01
```

Remaining exact local set:

```text
AGR-U01
TC-U01
COUNT = 2
```

Global unresolved DB-U set remains:

```text
DB-U08
DB-U09
DB-U10
DB-U15
DB-U17
DB-U18
DB-U19
DB-U20
DB-U21
COUNT = 9
```

No new local/global unresolved identifier is introduced.

### 32.51 Checkpoint-E closure register

```text
CONSOLIDATION CHECKPOINT E
CRITERION / EVALUATION BASELINE DISPOSITION
PASS AFTER HARDENING

CRT-U01
CLOSED
FINAL CP6 BASELINE DISPOSITION: NO GENERIC CRITERION DDL

EVL-U01
CLOSED
FINAL CP6 BASELINE DISPOSITION: NO GENERIC EVALUATION DDL

GENERIC EVIDENCE-USE BUSINESS INFRASTRUCTURE
NOT MATERIALIZED IN CP6 BASELINE
FUTURE CONCRETE PROFILE-SPECIFIC ASSOCIATIONS ONLY

GOAL PROGRESS
DERIVED
NO UNIVERSAL BASELINE PERSISTED OBJECT

GLOBAL UNRESOLVED DB-U ITEMS
9

LOCAL EXACT UNRESOLVED ITEMS
2

LOCAL EXACT OPEN
AGR-U01
TC-U01

UNCLASSIFIED NEW ITEMS
0

CP6 BUSINESS DDL AUTHORIZED
NO

GATE 03
NOT YET EARNED
```

This closes the current block. The next substantive block must begin from this exact saved boundary, preserve the complete multi-part database audit, and must not recreate generic Criterion/Evaluation/Evidence infrastructure while closing Temporal Constraint or Agreement.