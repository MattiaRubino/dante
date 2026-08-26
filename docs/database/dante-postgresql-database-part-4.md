# DANTE PostgreSQL Database — Architecture, Reference & Whole-Database Blueprint — Part 4

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
- **Part 3:** `dante-postgresql-database-part-3.md` — section 32
- **Continuation numbering:** section 33 onward
- **Continuation anchor:** `8a3f0e4c978139cfcd20e589114c570cf502383f`
- **Implementation status:** business schema / business SQLAlchemy mappings / product vertical **NOT YET MATERIALIZED**

---

## Canonical continuity contract

This file is the canonical continuation of Parts 1, 2 and 3. It does not replace, summarize or supersede any prior part as a whole.

```text
dante-postgresql-database.md
PART 1 / sections 1–30
+

dante-postgresql-database-part-2.md
PART 2 / section 31
+

dante-postgresql-database-part-3.md
PART 3 / section 32
+

dante-postgresql-database-part-4.md
PART 4 / section 33 onward
=

ONE CANONICAL HUMAN-READABLE
DANTE DATABASE ARCHITECTURE & REFERENCE
```

Readers, reviewers, migrations, implementation work, Database Dictionary reconciliation and whole-database audits MUST consume every active part. Part 4 exists only to keep writes bounded and safe; it introduces no independent semantic authority.

The preservation, explicit-supersession and whole-database cumulative-audit rules established in Parts 2 and 3 remain fully applicable.

---

## 33. Consolidation checkpoint F — Temporal Constraint baseline disposition

### 33.1 Scope and authority

This checkpoint closes the remaining exact local blocker concerned with PostgreSQL materialization of Temporal Constraint:

```text
TC-U01
```

The decision is derived from the complete accumulated authority, including:

```text
Temporal Constraint Domain v0
Temporal Constraint Domain continuation / Dependency boundary
Scheduling Flexibility product contract
Logical Slice C — Time / Reality
Whole-Logical 57/57 model
CP6-01 persistence coverage Parts 1–2
accepted PostgreSQL Physical mapping
CP6-02 Persistence Constitution / ADR-010
Part 1 sections 1–30, especially sections 21, 27, 28, 29 and 30
Part 2 section 31 Outcome / Milestone closure
Part 3 section 32 Criterion / Evaluation closure
real CP3 PostgreSQL/Alembic/SQLAlchemy foundation
```

This is a physical closure only. It does not redefine Temporal Constraint semantics. The accepted Domain remains authoritative:

```text
Temporal Constraint
= rule restricting or preferring temporal placement,
  duration or temporal relationship

Temporal Constraint
!= accepted Schedule
!= Actual reality
```

The decisive persistence facts are:

```text
Temporal Constraint
→ LR-05 typed rule/specification
→ structured representation required when a concrete family is materialized
→ owner/consumer-bound by default
→ independent ScopedRecordRef only when independent addressability/history/reuse is real

CP6-01 remaining physical stage
→ planning/scheduling vertical
```

The Domain deliberately leaves the exact entity/value-object split, SQL structures, constraint-type vocabulary, inheritance/scoping resolution, soft-weight model, override/Authority semantics, effective dating, provenance and relative-constraint interactions to downstream design.

No accepted repository authority currently supplies one first concrete Temporal Constraint profile whose complete SQL contract is deterministic across scope, constrained temporal feature, geometry, frame, inheritance and override semantics.

Therefore the maximum non-speculative CP6 baseline result is:

```text
Temporal Constraint
→ semantic capability retained
→ NO generic CP6 baseline business DDL
```

This is a final baseline disposition, not an invitation to hide unresolved semantics in generic columns or JSON.

### 33.2 Canonical semantic boundary retained

Temporal Constraint remains the planning-rule layer describing where or how temporal placement/execution is permitted, required, bounded or preferred.

Canonical non-collapse remains:

```text
Temporal Constraint != Schedule
Temporal Constraint != Session
Temporal Constraint != Actual
Temporal Constraint != Recurrence
Temporal Constraint != Availability
Temporal Constraint != Capacity
Temporal Constraint != Movement Policy
Temporal Constraint != Goal/Milestone target by default
Temporal Constraint != Review Date
Temporal Constraint != Dependency
Temporal Constraint != Criterion
Temporal Constraint != Outcome
Temporal Constraint != Authority
```

Identical temporal geometry does not imply identical semantic meaning.

For example:

```text
17:00–21:00
```

may represent:

```text
hard validity window
soft preferred window
Availability window
accepted Schedule placement
target window
```

Those meanings cannot be inferred from two timestamps alone.

### 33.3 TC-U01 — CLOSED with NO CP6 baseline Temporal Constraint DDL

Part 1 section 27.4 correctly identified Temporal Constraint as LR-05 and explored a possible scoped/material representation. It left the exact feature/window/anchor/inheritance shape open under `TC-U01`.

The cumulative audit now closes that blocker by explicit non-materialization because the proposed generic identity/strength shell does not contain enough semantics to represent an actual constraint safely.

CP6-04 MUST NOT create generic objects equivalent to:

```text
dante.temporal_constraint
dante.temporal_constraint_definition_state
dante.temporal_constraint_current_definition
dante.temporal_constraint_current_history

temporal_constraint scoped_address family
temporal_constraint.definition MaterialState facet

temporal_feature_code
constraint_kind
relationship_code
window_type
boundary_type
duration_scope
inheritance_mode
override_mode
priority_weight
rule_expression
constraint_payload jsonb
rule_payload jsonb
```

Closed baseline disposition:

```text
TC-U01
CLOSED

CP6-04 BASELINE TEMPORAL CONSTRAINT BUSINESS OBJECTS
0
```

This does not remove Temporal Constraint from Domain/Logical authority. It prevents a semantically incomplete generic rule shell from becoming canonical persistence before a concrete scheduling/planning profile exists.

### 33.4 Narrow supersession of Part 1 section 27.4 / 27.5

This checkpoint does not edit or delete Part 1. It narrowly supersedes only the earlier CP6-04 materialization candidate that would have created a generic Temporal Constraint scoped identity and definition state before the first concrete profile was closed.

The following Part-1 ideas remain valid future constraints:

```text
owner/consumer-bound by default
independent scoped identity only when independently meaningful
material history when consequential
exact subject/reference eligibility
hard/soft distinction
exact typed temporal value semantics
no JSON semantic escape hatch
```

The following Part-1 baseline authorization is withdrawn:

```text
generic dante.temporal_constraint owner
+
generic definition MaterialState containing only broad strength/identity shell
```

Reason:

```text
identity + subject + hard/soft
```

does not establish:

```text
what temporal feature is constrained
what semantic relation must hold
what scope the rule governs
what temporal frame applies
what inclusivity semantics apply
what relative anchor is valid
how inherited/exception rules compose
```

A shell that cannot answer those questions is not the “maximum non-speculative” baseline; it is premature abstraction.

### 33.5 Milestone scoped-subject candidate is no longer baseline-valid

Part 1 explored a scoped Temporal Constraint target that could include a material Milestone reference.

Checkpoint D subsequently closed:

```text
Milestone CP6 baseline DDL                  0
Milestone scoped_address family            0
Milestone material checkpoint definition   future trigger only
```

Therefore CP6-04 cannot authorize a Temporal Constraint baseline Reference Contract that points to a baseline Milestone scoped family that does not exist.

This does not prohibit a future concrete Milestone family from participating in a future Temporal Constraint profile after both sides are materially defined.

The correction is structural:

```text
no current Milestone persistence
→ no current Temporal Constraint FK/reference slot to Milestone
```

not semantic:

```text
Milestone can never have temporal constraints
```

The latter is false and is not asserted.

### 33.6 Why a generic subject + strength row is insufficient

Consider:

```text
Activity A
Temporal Constraint C
strength = hard
```

That record cannot determine whether the rule means:

```text
start no earlier than 07:00
completion no later than Friday 17:00
whole execution contained in 07:00–09:00
execution may overlap 17:00–21:00
Session duration between 45 and 90 minutes
at least 48 elapsed hours after qualifying prior workout
follow-up within 7 days after qualifying visit
exclude lunchtime
```

Nor can it determine whether the rule applies to:

```text
the Activity as a whole
each execution Session
one generated Occurrence
all future Occurrences under a Routine
a Plan-level governed child set
```

A generic identity row would therefore force later meaning into free text, magic enums, JSON or application-only conventions. CP6 explicitly rejects that outcome.

### 33.7 Deadline semantic family retained without generic Deadline object

Deadline remains accepted product/domain vocabulary:

```text
Deadline
= specialized latest-bound Temporal Constraint
```

The database must preserve what temporal condition is constrained when the distinction matters.

Examples:

```text
begin treatment no later than Monday
→ constrains start

submit report by Friday
→ constrains completion/delivery

arrive by 08:30
→ constrains arrival
```

Therefore no baseline shortcut is authorized:

```text
dante.deadline
due_at
subject.end_at as universal deadline truth
```

A future concrete latest-bound profile must close the constrained feature explicitly.

### 33.8 Deadline passage does not establish Outcome

The passage of a latest boundary establishes at most a temporal condition such as:

```text
current clock > deadline boundary
```

It does not establish:

```text
not completed
missed
failed
cancelled
late completion
```

because actual reality may be unknown or may have occurred before/after the boundary.

Therefore CP6 MUST NOT create a generic automatic effect equivalent to:

```text
ON deadline passage
SET outcome = 'missed'
```

Checkpoint D Outcome boundaries remain authoritative.

### 33.9 Hard versus soft semantics retained

At semantic level:

```text
hard
→ defines planner admissibility under current accepted rules

soft
→ influences optimization/ranking but may be violated according to policy
```

This distinction remains mandatory for future concrete profiles.

However CP6 creates no standalone global SQL enum/domain merely because `hard` and `soft` are accepted words. There is no baseline Temporal Constraint object to consume such a type.

Future concrete families may use a bounded shared type only if reuse across actual materialized objects is demonstrated and the value semantics are identical.

### 33.10 Strength is not Authority, mutability or override permission

The following are separate axes:

```text
constraint strength
hard / soft

constraint Authority / provenance
who or what establishes the rule

mutability
whether the current rule can be revised

override permission
who/what may accept a placement that violates the current rule
```

Examples:

```text
self-imposed Friday deadline
→ hard for automatic planning
→ user may revise it to Monday

external application deadline
→ hard for planning
→ scheduler must not rewrite it merely because planning is difficult
```

Therefore no generic inference is permitted:

```text
hard = immutable
hard = externally authoritative
hard = no override
soft = freely editable
```

Authority and governed effect semantics remain separate.

### 33.11 Boundary-family requirements retained

Future Temporal Constraint materialization must support lower and upper bounds where concrete verticals require them.

Representative semantics include:

```text
earliest start / not-before
latest start
latest completion
earliest completion
```

A boundary profile must define:

```text
constrained feature
comparison direction
inclusive/exclusive semantics
temporal value form
scope
strength
```

A plain column named `min_at` or `max_at` is not sufficient without the rule relationship that gives it meaning.

### 33.12 Window-family requirements retained

A future window constraint must preserve the relationship between the constrained execution feature and the window.

Possible materially different relationships include:

```text
start inside range
completion inside range
entire execution contained in range
any overlap with range
must not overlap range
must occur entirely outside range
```

The database must not assume that every window means full containment or that every pair of boundaries is an interchangeable range.

The profile must also close boundary inclusivity/exclusivity explicitly rather than inheriting an accidental PostgreSQL range default.

### 33.13 Exclusion-family requirements retained

Temporal exclusions such as:

```text
do not schedule meetings during lunch
```

are not represented by inventing negative Schedule rows or by treating Availability absence as the same fact.

A future exclusion profile must establish:

```text
subject/scope
excluded temporal feature/relationship
exact interval/frame semantics
hard/soft strength
recurring applicability where relevant
```

No generic exclusion table is introduced in CP6 baseline.

### 33.14 Duration-family requirements retained

Temporal Constraint may govern duration independently from placement.

Example:

```text
focus Session
minimum 45 minutes
maximum 90 minutes
```

A future concrete duration profile must define at least:

```text
which duration is constrained
elapsed / active / another accepted duration measure
minimum/maximum relation
inclusive/exclusive semantics
scope (whole subject vs each execution slice)
strength
```

It must not silently reuse Schedule interval length or Session elapsed time unless the profile explicitly defines those semantics.

Checkpoint B Session timing remains separate canonical actual chronology.

### 33.15 Spacing / recovery-family requirements retained

Spacing and recovery rules constrain relationships between distinct relevant executions/facts.

Examples:

```text
at least 48 elapsed hours between hard workouts
no earlier than 12 hours after prior dose
```

A future profile must close:

```text
which prior facts qualify as anchors
which feature of the anchor is used
which feature of the constrained subject is compared
elapsed vs calendar offset semantics
minimum / maximum relation
same-source vs cross-source eligibility
scope/inheritance
```

The database must not infer “previous row by timestamp” as the semantic anchor unless the profile proves that ordering/eligibility contract.

### 33.16 Relative Temporal Constraint requirements retained

Relative temporal rules may reference another Event, Activity, Occurrence, Session, Observation, Milestone or other reviewed fact when a concrete Reference Contract permits it.

Examples:

```text
follow-up within 7 days after medical visit
start no earlier than 24h after qualifying approval
```

A future profile must define:

```text
relative target Reference Contract
exact target state/facet where state matters
anchor feature
constrained feature
offset kind
frame/zone semantics where calendar-relative
lower/upper relationship
missing-anchor behavior
```

No generic:

```text
anchor_kind text
anchor_id uuid
offset_value jsonb
```

is authorized.

### 33.17 Temporal Constraint != Dependency

The accepted downstream amendment establishes:

```text
Temporal Constraint
= temporal geometry/rule

Dependency
= material contingency on prerequisite state/result/condition
```

Thus:

```text
B.start >= A.end + 24h
```

may be purely temporal,

while:

```text
B may proceed only if A.state = approved
```

is Dependency semantics even without a time offset.

They may compose:

```text
Dependency:
B requires A.approved

Temporal Constraint:
B.start >= A.approved_at + 24h
```

but CP6 does not collapse them into a universal edge with `relation_type + lag`.

### 33.18 Temporal Constraint != Recurrence

A temporal rule may recur in applicability without itself generating expected Occurrence identity.

Canonical separation:

```text
Recurrence
→ structured repeated/generative rule

Temporal Constraint
→ admissibility/preference rule
```

Example:

```text
study only weekdays 17:00–21:00
```

may require both recurring applicability and temporal-window semantics.

Checkpoint C remains authoritative:

```text
Recurrence state
!= Temporal Constraint state
```

No RRULE, provider recurrence string or generic policy expression is adopted as Temporal Constraint canonical truth.

### 33.19 Completion-relative Recurrence boundary remains explicit

The Domain intentionally leaves borderline cases between completion-relative Recurrence and relative Temporal Constraint to a concrete downstream contract.

Difference pressure:

```text
"create the next expected instance 30 days after qualifying completion"
→ generative / Recurrence pressure

"this already-existing action may not occur until 30 days after qualifying completion"
→ Temporal Constraint pressure
```

CP6 does not encode this distinction through one generic `relative_rule_type` field.

The first relevant vertical must identify whether the rule generates identity, restricts an existing subject, or does both through two distinct accepted records.

### 33.20 Temporal Constraint != Availability / Capacity

Availability/Capacity describes whether resources/capability are available or consumable.

Temporal Constraint describes whether a subject is allowed/required/preferred at a time.

Example:

```text
Availability:
user free 18:00–20:00

Temporal Constraint:
workout must finish by 20:00
```

Even identical ranges do not make them the same semantic record.

No Temporal Constraint row is inferred from Availability and no Availability record is fabricated from a Constraint.

### 33.21 Temporal Constraint != movement/replanning policy

A constraint defines temporal validity/preference. Movement policy defines whether/how an accepted Schedule can be changed.

Two subjects may share the same deadline while one is:

```text
freely replannable inside valid range
```

and another is:

```text
locked unless explicit approval
```

Therefore a future Temporal Constraint schema must not absorb:

```text
locked
movable
confirmation-required
AI-replannable
```

unless a concrete composite product object deliberately owns both dimensions and keeps them distinguishable.

### 33.22 Goal/Milestone target and review-date boundaries retained

A desired target horizon is not automatically a planning-validity rule.

```text
Goal target 31 December
```

may mean desired achievement horizon while the Goal remains meaningful afterwards.

A review date means “reassess then,” not “must be achieved by then.”

Therefore CP6 MUST NOT automatically convert:

```text
Goal.target
Milestone.target
review_at
```

into hard Temporal Constraint rows.

Any future promotion from target to planning constraint must be an explicit product/domain operation with a concrete profile and provenance.

### 33.23 Temporal value semantics remain typed and non-lossy

Future concrete Temporal Constraint families must reuse accepted temporal value semantics and preserve where applicable:

```text
civil date/date-only
floating local wall-clock
named-zone wall-clock + IANA zone
absolute instant
bounded/open interval/range
duration / elapsed amount
precision/granularity
period frame
```

Forbidden simplification:

```text
all temporal values → timestamptz
```

when that would destroy accepted civil/local meaning.

Likewise, date-only does not imply a midnight-to-midnight Capacity block.

### 33.24 Named-zone and DST behavior cannot be hidden

A future named-zone constraint can encounter:

```text
nonexistent local time (DST gap)
ambiguous repeated local time (DST overlap)
```

No PostgreSQL/library conversion default becomes canonical semantics merely because it returns a timestamp.

Where resolution affects consequence, the concrete profile must define or retain the accepted resolution basis.

Checkpoint C's no-hidden-DST-policy discipline applies analogously: unresolved temporal semantics are not repaired by choosing an implementation default silently.

### 33.25 Precision must not be invented

The database must preserve the distinction among accepted meanings such as:

```text
Tuesday
Tuesday afternoon
Tuesday 18:00
Tuesday 18:00–20:00
approximately 18:00
start known / end unknown
```

A coarse value may not be materialized as an exact clock interval unless the corresponding bounded vocabulary/range semantics have been accepted.

The earlier Schedule SCH-U01 negative disposition remains an important precedent:

```text
qualitative day-part with no accepted canonical boundary vocabulary
→ no invented 12:00–18:00 interval
```

Temporal Constraint must follow the same rule.

### 33.26 Broader-scope application and inheritance

Accepted Domain pressure includes rules defined at broader scope, for example Plan or Routine, that govern children without physically duplicating the same constraint onto every child.

Canonical rule:

```text
DO NOT duplicate identical governing constraints onto every child
merely to simplify querying
```

A future vertical must close:

```text
which owner families may govern descendants
which relation establishes scope membership
when a rule becomes applicable
how multiple inherited rules compose
which rule is overridden vs supplemented
how history is reconstructed after hierarchy/relation changes
```

CP6 baseline introduces no generic inheritance graph or precedence number because those semantics are not closed.

### 33.27 Occurrence-specific exceptions

A generated Occurrence may require a narrower one-off temporal rule without rewriting the source Routine/Event recurrence or governing rule set.

Future materialization must distinguish:

```text
source rule revision
!= one-Occurrence exception
!= this-and-future recurrence revision
```

The exact exception record may be owner-bound or independently scoped depending on the concrete scheduling contract.

No generic:

```text
exception_scope = 'this' / 'future'
```

is introduced before the operation/effective-state semantics are defined.

### 33.28 Constraint revision != Schedule revision

A material constraint revision changes the governing rule.

A Schedule revision changes accepted placement.

Conceptually:

```text
constraint C1
→ constraint C2

may cause

Schedule S1
→ Schedule S2
```

but the two histories remain distinct.

A future material Temporal Constraint family must preserve exact rule-state history where later decisions depend on the earlier rule, while Schedule keeps its own accepted-placement history under Checkpoint B.

The database must be able eventually to explain:

```text
why a placement moved
which rule state governed the prior decision
whether the rule itself changed or the scheduler simply replanned
```

### 33.29 Rule revision != hard-rule override

Two distinct operations remain:

```text
RULE REVISION
Friday deadline → Monday deadline

RULE OVERRIDE / EXCEPTION
Friday deadline remains authoritative
but an exceptional placement/result is accepted under sufficient Authority
```

A future concrete profile must not rewrite rule history merely to record an exceptional placement.

The exact Authority/Consent/governed-effect basis is vertical-specific and remains outside this baseline disposition.

### 33.30 Truthful Actual is never rejected merely by planning violation

This is a hard whole-model invariant.

Example:

```text
Temporal Constraint
workout must finish <= 20:00

actual Session
18:45–20:15
```

The Session/Actual must remain recordable as truthful reality.

Therefore CP6-04 MUST NOT add DB enforcement equivalent to:

```text
CHECK Actual satisfies current Temporal Constraint
```

or trigger logic that refuses Session/Actual insertion because a planning rule is violated.

Planning admissibility constrains automated planning; it does not rewrite reality.

### 33.31 Constraint violation/compliance is Evaluation semantics by default

After Checkpoint E:

```text
constraint compliance / violation assessment
→ derived Evaluation by default
```

Potential derived results may include profile-specific facts such as:

```text
inside admissible window
15 minutes beyond latest completion
minimum spacing violated
```

but CP6 baseline authorizes no generic canonical objects equivalent to:

```text
temporal_constraint_violation
violation_status
is_violated
violation_minutes
```

A future consequential compliance snapshot may be materialized only through an accepted concrete Evaluation profile with exact Constraint and Evidence/Actual basis.

### 33.32 Absence and infeasibility boundaries

No Schedule does not mean a Temporal Constraint failed.

An infeasible set of hard constraints means the current planner problem has no admissible solution under those rules; it does not authorize silently weakening a hard externally authoritative rule.

The system may derive/report:

```text
infeasible under current accepted constraints
```

and propose rule revision, scope reduction or another governed action.

It must not manufacture a “valid” Schedule by silently violating hard constraints.

Likewise:

```text
constraint exists + no Actual
```

does not establish miss/failure/non-realization.

### 33.33 Owner-bound representation remains the default future shape

When a concrete Temporal Constraint exists only as part of one owner/context's rule state and has no independent addressability, the future physical default is owner-bound:

```text
<owner>.<temporal-constraint facet/profile>
→ complete MaterialStateRef when material history is required
→ typed child rows for the concrete constraint components
```

No independent constraint identity is introduced merely because SQL rows are easier to manipulate that way.

A materially changed complete rule set creates a new owner/facet MaterialStateRef when historical consequence requires it.

### 33.34 Independently scoped Temporal Constraint threshold

A future Temporal Constraint may become an independently scoped contextual record only when a concrete contract proves real independent semantics such as:

```text
independent revision lifecycle
reuse across bounded subjects
independent cross-reference
independent reconciliation/provider mapping
independent override/exception history
independent governance/Visibility
stable addressability required by another accepted record
```

Only then may a concrete profile introduce:

```text
ScopedRecordRef(<temporal-constraint profile>)
scoped_address registration
own MaterialState definition/currentness
owner-specific current-history where justified
```

Temporal Constraint never becomes a new LR-01 NativeRef owner. Native-owner count remains exactly 15.

### 33.35 Future concrete Temporal Constraint profile trigger

The first scheduling/planning vertical that requires canonical Temporal Constraint persistence MUST close a complete typed contract before schema evolution is authorized.

Minimum trigger information:

```text
exact owning subject family / consumer
exact subject Reference Contract
exact constraint scope
  whole owner
  each execution slice
  one Occurrence
  governed child set
  other bounded accepted scope

exact constrained temporal feature
  start
  completion
  delivery
  arrival
  whole execution
  Session duration
  other bounded accepted feature

exact semantic form
  lower bound
  upper bound
  bounded window
  exclusion
  duration
  spacing/recovery
  relative temporal relationship
  other explicitly accepted form

exact strength semantics
  hard / soft

exact temporal value form
  date-only
  floating local
  named-zone local
  absolute instant
  range
  duration

exact inclusivity/exclusivity
exact range/window relationship
exact relative-anchor Reference Contract
exact anchor MaterialState requirement where state matters
exact elapsed-vs-calendar offset semantics
exact recurrence/applicability interaction
exact inheritance/scoping resolution
exact Occurrence-exception precedence
exact rule revision/currentness/history semantics
exact world/effective chronology where relevant
exact recorded/accepted chronology where relevant
exact Authority/override boundary
exact Provenance/source requirements
exact planner feasibility semantics
exact violation Evaluation semantics
exact query/index contract
exact runtime write surface
exact ACL/role requirements
exact direct PostgreSQL proof obligations
```

A future vertical may materialize one small concrete profile without solving every possible Temporal Constraint family globally.

### 33.36 No generic universal Temporal Constraint DSL

The breadth of Temporal Constraint semantics does not justify a universal DSL/AST/expression root in CP6 baseline.

Forbidden baseline patterns include:

```text
rule_type + json_payload
expression_text
left_operand / operator / right_operand generic AST
predicate JSON
from_ref / relation_type / to_ref / lag
provider RRULE as canonical rule
```

Reusable technical parsing/evaluation machinery may later exist behind concrete semantic families, but canonical persistence must remain typed and inspectable.

### 33.37 No generic JSON semantic escape hatch

The Domain allows controlled JSONB only for extension metadata where accepted LR-10 flexibility exists.

Required Temporal Constraint semantics MUST NOT disappear into:

```text
constraint_payload jsonb
metadata jsonb containing required boundary/window semantics
provider_payload as canonical rule truth
```

A future family may retain provider/raw extension metadata separately, but the canonical rule needed for planner integrity must be formally represented.

### 33.38 Current-state/history topology is not pre-created

Because CP6 baseline contains no material Temporal Constraint business family, CP6 also creates no generic:

```text
temporal_constraint_current_definition view
temporal_constraint_current_history table
current MaterialState binding facet registration
constraint replacement trigger
```

When a concrete future profile becomes material, it must explicitly select whether it uses:

```text
owner-bound native/scoped current binding
owner-specific current-history episodes
append-retained material definition states
```

according to the already-accepted MaterialState/currentness doctrine.

The common pattern is available; unused infrastructure is not pre-instantiated.

### 33.39 Lifecycle and deletion

DB-U14 remains authoritative:

```text
foreign-key lifecycle default            ON DELETE NO ACTION
ordinary runtime semantic DELETE         NOT AUTHORIZED
NativeRef reuse                           FORBIDDEN
universal soft-delete columns             FORBIDDEN
universal tombstone semantic root         FORBIDDEN
```

Since no Temporal Constraint baseline rows exist, CP6 adds no constraint-specific delete/retire columns.

A future concrete rule family must preserve historical rule-state basis when later Schedule/Evaluation/Decision history depends on it and must not erase consequential rule history through ordinary mutable-row overwrite.

### 33.40 Provider/integration boundary

An external calendar/task/provider may expose constructs labeled:

```text
deadline
due date
working hours
constraint
availability
recurrence exception
```

Provider vocabulary does not automatically define canonical DANTE Temporal Constraint semantics.

A future integration must map provider state into a concrete accepted DANTE profile or retain it as provider/external state until reconciliation/acceptance occurs.

No provider identifier, RRULE, due timestamp or flag becomes canonical simply because it exists upstream.

DB-U17 remains the final provider/integration baseline disposition and is not closed by this checkpoint.

### 33.41 Derived planner feasibility and DB-U20 boundary

Planner feasibility, ranking and compliance projections are LR-08 derived state by default.

Examples:

```text
candidate placement satisfies all hard rules
placement violates one soft preference
current rule set is infeasible
ranking score under current preferences
```

CP6 creates no generic persisted feasibility/cache/search structures solely because such derivations will exist.

If a future consumer needs a materialized/cache projection for performance, DB-U20/future evolution rules require exact source MaterialState basis, freshness and rebuildability boundaries.

### 33.42 PostgreSQL type disposition

This checkpoint authorizes no new PostgreSQL enum/domain/composite solely for future Temporal Constraint use.

Specifically absent from CP6 baseline inventory:

```text
constraint_strength
constraint_kind
temporal_feature
window_relation
boundary_relation
inheritance_mode
exception_scope
```

A future type may be introduced only when at least one real materialized object consumes a closed bounded vocabulary and shared reuse improves integrity rather than freezing speculative semantics.

### 33.43 Index disposition

Because no Temporal Constraint business objects are materialized, this checkpoint adds zero structural/query indexes to DB-U15 inventory.

No speculative indexes such as:

```text
(subject_ref, strength)
(boundary_at)
(range)
(anchor_ref)
```

are created without an actual query contract.

Future concrete profiles must justify indexes by:

```text
FK/uniqueness structural need
current-state lookup
planner range query
relative-anchor lookup
history lookup
other measured/known query contract
```

DB-U15 remains open for final inventory review.

### 33.44 ACL / privilege disposition

Because no Temporal Constraint business objects are materialized, this checkpoint adds zero tables/views/functions/types requiring a new DB-U21 business ACL row.

Future concrete profiles remain subject to the accepted direction:

```text
provisioning owns roles/schema technical baseline
Alembic migration owns exact ACL for created/changed business objects
runtime receives only required object privileges
no blanket future-table CRUD/default privilege broadening
```

DB-U21 remains open for the final object-specific matrix.

### 33.45 SQLAlchemy mapping disposition

CP6-04 creates no generic ORM objects equivalent to:

```text
TemporalConstraint
TemporalConstraintDefinition
TemporalConstraintWindow
TemporalConstraintBoundary
TemporalConstraintViolation
```

There is no table contract to map.

Future scheduling/planning verticals must map their concrete typed profile directly and must not introduce a generic base-class hierarchy that re-creates the rejected universal rule ontology in Python.

### 33.46 Alembic migration disposition

CP6-04 baseline migrations contain no Temporal Constraint business DDL.

This means:

```text
CREATE TABLE temporal_constraint            NO
CREATE TYPE constraint_strength             NO
CREATE VIEW current_temporal_constraint     NO
CREATE TRIGGER temporal_constraint_*        NO
```

A future vertical introduces its own additive reviewed migration once the first concrete profile contract is complete.

Historical Domain/Logical support is preserved through documentation authority; absence of baseline DDL is intentional, not an implementation omission.

### 33.47 Database Dictionary disposition

The machine-readable Database Dictionary describes **real materialized database objects**, not abstract Domain capabilities.

Therefore CP6 baseline dictionary object catalogs contain no fake entries for:

```text
temporal_constraint
deadline
temporal_constraint_violation
```

The human-readable architecture records this explicit non-materialization and future trigger.

When a future concrete profile creates real objects, the same schema change must add corresponding dictionary entries, migrations, mappings and direct tests.

### 33.48 Direct PostgreSQL proof obligations for future profile

No Temporal Constraint business schema exists yet, so no direct CP6-05 test may falsely claim that its specific invariants passed.

The first materialized profile must add direct PostgreSQL proofs appropriate to its contract, including as applicable:

```text
eligible subject/reference enforcement
exact owner/facet MaterialState totality
invalid temporal-form combinations rejected
range/boundary inclusivity preserved
named-zone/DST resolution basis enforced where material
relative-anchor eligibility enforced
history/current-binding invariants
scope/inheritance resolution integrity
Occurrence-specific exception isolation
concurrent rule revision expected-state conflict
hard-rule planner validation without blocking truthful Actual
ACL least privilege
migration upgrade/downgrade/evolution behavior
```

This checkpoint records design obligations only; it does not manufacture execution evidence.

### 33.49 Regression against Schedule / Actual / Session

Checkpoint B remains intact:

```text
Schedule
→ current accepted placement

Session
→ actual execution episode

Actual
→ contextual realization
```

Temporal Constraint non-materialization does not move its semantics into any of those objects.

Forbidden regressions:

```text
Activity/Event/Schedule gains generic deadline/window fields
Session gains planning-validity fields
Actual gains constraint-compliance status
Schedule doubles as constraint state
```

The future vertical must add a concrete rule family rather than contaminating existing owners with generic temporal-rule columns.

### 33.50 Regression against Recurrence / Occurrence

Checkpoint C remains intact:

```text
Recurrence state generates/structures repeated expectation
Occurrence preserves one expected-instance identity when differentiated
```

Temporal Constraint future rules may apply to Recurrence sources or individual Occurrences, but must not alter generation identity implicitly.

An Occurrence-specific constraint exception does not by itself mean:

```text
new Recurrence rule
new Occurrence identity
source recurrence revision
```

unless a concrete governed operation establishes that effect explicitly.

### 33.51 Regression against Criterion / Evaluation

Checkpoint E remains intact:

```text
Criterion
→ evaluative specification

Evaluation
→ derived assessment by default

Temporal Constraint
→ planning temporal rule
```

A rule such as:

```text
must finish by 20:00
```

is Temporal Constraint.

An assessment such as:

```text
Session ended at 20:15, therefore violated the applicable latest-completion rule by 15 minutes
```

is Evaluation semantics.

No generic Temporal Constraint table is justified merely to make generic Evaluation possible; both remain future typed profiles until a concrete vertical requires them.

### 33.52 Regression against Outcome / Milestone

Checkpoint D remains intact:

```text
deadline passed
!= Outcome missed

target date passed
!= Milestone unattained as a canonical automatic fact
```

Temporal rules can become Evidence/input for future evaluation/outcome decisions, but they do not manufacture those semantic records automatically.

### 33.53 Whole accumulated database A/B/C audit — method

The checkpoint was replayed against the complete accumulated Database Architecture & Reference rather than only section 27.

Classification retained:

```text
A
correct / compatible; retain

B
incomplete, ambiguous or not yet implementation-safe;
harden before PASS

C
contradictory, semantically lossy, generic-fallback,
or implementation-unsafe;
repair/reject before PASS
```

No B/C finding is left hidden as a “later implementation detail” if CP6-04 would otherwise need to invent the decision.

### 33.54 Audit findings and repairs

| Finding | Class | Repair / final disposition |
|---|---|---|
| generic `temporal_constraint` shell with identity + strength only | C | NO baseline DDL |
| generic definition MaterialState without exact typed rule payload | C | NO baseline facet/state |
| generic scoped Temporal Constraint address before independent addressability is proven | C | future concrete threshold only |
| Part-1 scoped Milestone target after Checkpoint-D Milestone non-materialization | C | baseline candidate superseded |
| universal deadline field / `subject.end_at` equivalence | C | constrained temporal feature must be explicit |
| generic `start/end` window | C | exact window relationship + scope required |
| implicit range inclusivity | C | concrete profile must define inclusivity |
| generic duration scope | C | exact duration measure/scope required |
| generic relative anchor `kind + uuid` | C | bounded Reference Contract required |
| “previous row by timestamp” as spacing anchor | C | qualifying-anchor semantics required |
| hard = immutable/externally authoritative/no override | C | strength remains separate from governance |
| hard planning violation rejects Session/Actual | C | truthful Actual remains recordable |
| deadline passage creates missed Outcome | C | time passage != reality/result |
| constraint violation generic canonical row | C | derived Evaluation by default |
| target date automatically becomes hard Temporal Constraint | C | explicit promotion only |
| review date automatically becomes Temporal Constraint | C | rejected |
| Temporal Constraint = Recurrence | C | non-collapse retained |
| Temporal Constraint = Dependency/lag edge | C | non-collapse retained |
| Temporal Constraint = Availability/Capacity | C | non-collapse retained |
| movement policy stored inside constraint strength | C | separate policy/governance axis |
| broader-scope rule duplicated onto every child | C | inheritance/effective scope derived/typed future contract |
| universal inheritance/precedence table before accepted semantics | B/C | future scheduling vertical |
| one-off Occurrence exception rewrites source rule automatically | C | separate future exception contract |
| generic RRULE/provider rule as canonical Temporal Constraint | C | rejected |
| generic Temporal Constraint JSON/DSL/AST | C | rejected |
| speculative indexes for non-existent family | B/C | zero baseline index inventory |
| speculative ACL/mappings for non-existent family | B/C | zero baseline inventory |
| fake CP6 direct test PASS without schema | C | future proof obligations only |

All C findings were repaired by the final disposition and future-trigger contract.

### 33.55 Whole-model non-collapse regression

Post-repair regression result:

```text
57 / 57 Domain concepts                           PASS
15 / 15 LR-01 native owners                       PASS
new LR-01 owner                                   0
new generic Rule root                             0
new semantic JSON fallback                        0
new unclassified item                             0

Temporal Constraint != Schedule                   PASS
Temporal Constraint != Session                    PASS
Temporal Constraint != Actual                     PASS
Temporal Constraint != Recurrence                 PASS
Temporal Constraint != Availability               PASS
Temporal Constraint != Capacity                   PASS
Temporal Constraint != Movement Policy            PASS
Temporal Constraint != Goal/Milestone target      PASS
Temporal Constraint != Review Date                PASS
Temporal Constraint != Dependency                 PASS
Temporal Constraint != Criterion                  PASS
Temporal Constraint != Outcome                    PASS
Temporal Constraint != Authority                  PASS

hard != immutable                                 PASS
hard != Authority                                 PASS
hard violation != invalid Actual                  PASS
deadline passage != missed Outcome                PASS
geometry != semantic meaning                      PASS
scope != duplicated child rows                    PASS
constraint revision != Schedule revision          PASS
rule revision != override                         PASS

C DEFECTS AFTER REPAIR                            0
UNCLASSIFIED NEW ITEMS                            0
```

### 33.56 CP6-04 baseline inventory consequence

After this checkpoint, the approved CP6-04 baseline contains:

```text
TEMPORAL CONSTRAINT BUSINESS TABLES              0
TEMPORAL CONSTRAINT VIEWS                        0
TEMPORAL CONSTRAINT MATERIAL FACETS              0
TEMPORAL CONSTRAINT SCOPED FAMILIES              0
TEMPORAL CONSTRAINT CURRENT-HISTORY TABLES       0
TEMPORAL CONSTRAINT TYPES/ENUMS/DOMAINS          0
TEMPORAL CONSTRAINT INDEXES                      0
TEMPORAL CONSTRAINT TRIGGERS/FUNCTIONS           0
TEMPORAL CONSTRAINT SQLALCHEMY MAPPINGS          0
TEMPORAL CONSTRAINT RUNTIME ACL OBJECTS          0
```

This zero-object inventory is intentional and normative for CP6-04.

The first product/scheduling vertical remains free to add a concrete typed family through normal additive schema evolution without reopening the Domain concept.

### 33.57 TC-U01 final closure

Final exact disposition:

```text
TC-U01
CLOSED

TEMPORAL CONSTRAINT
SEMANTIC CAPABILITY RETAINED

CP6 BASELINE GENERIC TEMPORAL CONSTRAINT DDL
NO

FIRST CONCRETE MATERIALIZATION
TRIGGER-BOUND TO A PLANNING/SCHEDULING VERTICAL
WITH COMPLETE TYPED PROFILE CONTRACT
```

There is no residual “choose table shape during CP6-04” decision.

CP6-04 implementers are explicitly forbidden from inventing generic Temporal Constraint storage merely because the semantic concept exists.

### 33.58 Checkpoint F closure register

```text
CONSOLIDATION CHECKPOINT F
TEMPORAL CONSTRAINT BASELINE DISPOSITION

PASS AFTER HARDENING

TC-U01
CLOSED

TEMPORAL CONSTRAINT CP6 BASELINE DDL
NONE

WHOLE ACCUMULATED DATABASE AUDIT
PASS AFTER REPAIR

GLOBAL UNRESOLVED DB-U ITEMS
9

LOCAL EXACT UNRESOLVED ITEMS
1

LOCAL EXACT OPEN
AGR-U01

UNCLASSIFIED NEW ITEMS
0

CP6 BUSINESS DDL AUTHORIZED
NO

GATE 03
NOT YET EARNED
```

### 33.59 Next exact work block

After this checkpoint the only exact local CP6-03 blocker is:

```text
AGR-U01
Agreement
```

The next block must audit Agreement/Consent common-terms semantics, exact terms-bearing MaterialState eligibility, represented-party versus actual Actor, assent basis/history and whether the existing Part-1 Agreement candidate is sufficiently concrete for baseline DDL.

That block must remain separate from the nine global DB-U closures unless a direct dependency requires otherwise.

After `AGR-U01` closes:

```text
LOCAL EXACT OPEN
0
```

and CP6-03 can move to global final consolidation:

```text
DB-U08 naming
DB-U09 Account
DB-U10 Principal/security
DB-U15 final indexes
DB-U17 provider/integration
DB-U18 idempotency
DB-U19 outbox
DB-U20 derived/search/vector
DB-U21 exact ACL matrix

→ final object inventory
→ migration DAG
→ SQLAlchemy mapping plan
→ Database Dictionary
→ direct PostgreSQL test plan
→ whole-database final audit
→ Gate 03
```

No part of this checkpoint authorizes CP6-04 business DDL before those final closures are complete.
