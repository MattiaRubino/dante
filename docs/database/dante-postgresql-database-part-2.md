# DANTE PostgreSQL Database — Architecture, Reference & Whole-Database Blueprint — Part 2

- **Status:** CP6-03 ACTIVE / CANONICAL CONTINUATION / GATE 03 NOT YET EARNED
- **Created:** 2026-08-23
- **Product:** DANTE
- **Database:** PostgreSQL 18 major family
- **Current repository patch:** PostgreSQL 18.6
- **Schema:** `dante`
- **Workstream:** `../workstreams/logical-postgresql.md`
- **Database documentation authority:** `README.md`
- **Part 1:** `dante-postgresql-database.md`
- **Continuation numbering:** future substantive sections begin at section 31
- **Structural split anchor:** `efb80da23db60b82f641b6e9329500af00cbbf46`
- **Implementation status:** business schema / business SQLAlchemy mappings / product vertical **NOT YET MATERIALIZED**

---

## Canonical continuity contract

This file is the canonical continuation of `dante-postgresql-database.md`. It does not replace, summarize or supersede Part 1 as a whole.

The human-readable DANTE Database Architecture & Reference is one logical authority physically split across active parts:

```text
dante-postgresql-database.md
PART 1
sections 1–30
+

dante-postgresql-database-part-2.md
PART 2
section 31 onward
=

ONE CANONICAL HUMAN-READABLE
DANTE DATABASE ARCHITECTURE & REFERENCE
```

A reader, reviewer, implementation task, migration plan, Database Dictionary reconciliation or whole-database audit MUST consume all active parts. The latest part alone is never the whole database reference.

The split exists solely to keep future Git writes bounded, reviewable and safe as the database reference grows. It does not change database meaning, authority ordering, Gate-03 requirements or any previously accepted physical decision.

Part 1 remains authoritative and intact for every decision recorded in sections 1–30 unless a later numbered section in an active continuation explicitly identifies a narrower earlier statement that it supersedes after the required cumulative audit.

---

## Authority and derivation contract

The derivation chain remains exactly:

```text
closed Domain
→ closed Whole-Logical model
→ CP6-01 persistence coverage / pressure
→ accepted PostgreSQL Physical mapping
→ CP6-02 PostgreSQL Persistence Constitution / ADR-010
→ concrete CP6-03 PostgreSQL blueprint
→ CP6-04 Alembic + SQLAlchemy + real PostgreSQL materialization
→ CP6-05 direct PostgreSQL / consistency proof
```

This continuation does not gain authority to redefine upstream semantics merely because it is later in file order.

For every later database fact:

```text
semantic meaning
→ must remain traceable to upstream authority

physical PostgreSQL decision
→ must preserve that meaning

fact not determinable from accepted authority
→ explicit classified non-materialization / future trigger
→ never an invented placeholder
```

The existing non-collapse and anti-shortcut rules remain in force across every part, including the rejection of universal Entity/Thing, universal Relationship/edge, canonical EAV/property bags, universal Fact/Version payload roots, universal Rule(type,payload), generic semantic JSON fallbacks and application-only heterogeneous `kind + uuid` references without database integrity.

---

## Explicit supersession rule

Later numbered sections may supersede an earlier provisional or candidate statement only when all of the following are true:

```text
1. the later section names the affected earlier area explicitly;
2. the replacement is derived from the accepted authority chain;
3. the complete accumulated database is regressed after the change;
4. every B/C finding is repaired before PASS;
5. no unrelated earlier decision is silently reinterpreted;
6. the write is bounded by an approved Git scope and remotely QA'd.
```

Therefore:

```text
later file position
!= blanket higher semantic authority

new checkpoint
!= permission to rewrite unrelated accepted history

physical convenience
!= authority to change Domain/Logical meaning
```

Where no explicit later supersession exists, the applicable Part-1 contract remains fully in force.

---

## Write-preservation rule

The multi-part layout exists to preserve detail, not to reduce it.

Future database-reference writes MUST NOT simplify Git operations by deleting, condensing or replacing accepted detailed content with summaries.

Forbidden write behavior:

```text
replace detailed approved sections with a shorter recap
remove negative dispositions because a later section mentions the result
collapse table/constraint/test detail into prose for file-size reasons
rewrite historical PASS/audit evidence as if it had always existed
move content between parts without a dedicated structural gate
silently renumber previously approved sections
truncate an earlier part while creating a continuation
use a "latest state" summary as a substitute for the canonical prior derivation
```

Required behavior:

```text
new independently audited block
→ detailed numbered section in the active continuation
→ explicit relationship to earlier provisional statements where necessary
→ exact Git delta QA
→ earlier canonical content retained
```

If another physical split becomes necessary for write safety or maintainability, a later `part-3` may be introduced through a dedicated structural gate using the same no-loss rules. The existence of multiple parts never changes the requirement to consume them together.

Any future re-fusion into one physical file is itself a dedicated structural documentation migration and requires full content-equivalence QA. Re-fusion must concatenate/reorganize without semantic loss; it must never replace the parts with a summary.

---

## Cumulative whole-database audit rule

Splitting the reference does not split the database audit.

Every future substantive block beginning with section 31 MUST be evaluated against the complete accumulated authority:

```text
all active Database Architecture & Reference parts
+
closed Domain
+
closed Logical
+
accepted Physical PostgreSQL mapping
+
CP6-01
+
CP6-02 Constitution / ADR
+
real backend/PostgreSQL foundation where relevant
```

The required block loop remains:

```text
derive one concrete block
→ classify candidate only
→ audit the ENTIRE accumulated database
→ A = sound / retained
→ B = underspecified / closed too early / hardening needed
→ C = contradiction / defect / missing contract
→ repair every B/C
→ repeat whole-database audit
→ PASS only when C defects = 0 and no unclassified item remains
→ exact bounded Git write gate
→ write
→ remote readback + exact PRE-SCOPE→HEAD QA
→ only then open the next block
```

A block-local PASS without accumulated regression is insufficient for CP6-03.

---

## Part 1 continuity anchor

This structural split begins immediately after the final saved state of Part 1.

```text
PART 1 FILE
docs/database/dante-postgresql-database.md

PART 1 FINAL NUMBERED SECTION
30. Consolidation checkpoint C — Recurrence / Occurrence-generation physical closure

PART 1 REPOSITORY HEAD AT SPLIT
efb80da23db60b82f641b6e9329500af00cbbf46

DB-U12
CLOSED

WHOLE ACCUMULATED DATABASE AUDIT
PASS AFTER REPAIR

GLOBAL UNRESOLVED DB-U ITEMS
9

LOCAL EXACT UNRESOLVED ITEMS
6

UNCLASSIFIED NEW ITEMS
0

CP6 BUSINESS DDL AUTHORIZED
NO

GATE 03
NOT YET EARNED
```

The globally unresolved set at this continuity anchor is exactly:

```text
DB-U08  final PostgreSQL object naming
DB-U09  Account persistence disposition
DB-U10  Principal/security persistence disposition
DB-U15  final structural/query index matrix
DB-U17  provider/integration object shapes
DB-U18  idempotency persistence timing
DB-U19  transactional outbox timing
DB-U20  derived/search/vector persisted structures
DB-U21  exact object-by-object runtime privilege matrix

COUNT = 9
```

The exact local unresolved set is exactly:

```text
OUT-U01
MIL-U01
AGR-U01
CRT-U01
EVL-U01
TC-U01

COUNT = 6
```

These identifiers retain the exact meanings established in Part 1. This structural file creation does not close, reopen or reinterpret any of them.

---

## Section numbering and continuation discipline

Part 1 owns numbered sections:

```text
1 through 30
```

Part 2 reserves future substantive numbering beginning at:

```text
31
```

This structural preamble is intentionally unnumbered so that the first future semantic/technical checkpoint can begin cleanly at section 31.

Numbering across active parts is one continuous logical sequence. A future Part 3, if justified, continues from the next unused number rather than resetting numbering.

---

## Structural split scope — no semantic database change

This file creation is documentation structure only.

It introduces no new:

```text
Domain concept
Logical representation
native owner
ScopedRecordRef owner
MaterialState facet
PostgreSQL table/view/type/domain/routine/index
column
constraint
Reference Contract
lifecycle rule
ACL
migration
SQLAlchemy mapping
test result
provider/search/security object
```

It also does not authorize CP6 business DDL or earn Gate 03.

The next substantive database block must start at section 31 and must begin from the exact accumulated state above rather than reconstructing or abbreviating Part 1.

---

## 31. Consolidation checkpoint D — Outcome / Milestone baseline disposition

### 31.1 Scope and authority

This checkpoint closes the two remaining Pass-II local items concerned with result/disposition and contextual checkpoint persistence:

```text
OUT-U01
MIL-U01
```

The closure is derived from the complete accumulated authority, not from table-count minimization:

```text
Outcome Domain v0
Milestone Domain v0
Criterion / Evaluation Domain v0
Logical Slice B — Intention / Execution
Logical Slice C — Time / Reality
Logical Slice D — Evidence / Knowledge / History
CP6-01 persistence coverage
accepted PostgreSQL Physical mapping
CP6-02 Persistence Constitution / ADR-010
Part 1 sections 1–30
Part 2 continuity contract
```

This checkpoint does not weaken either Domain concept. It decides only what the **maximum non-speculative CP6 baseline database** may materialize now.

Canonical result:

```text
Outcome
→ authoritative semantic capability retained
→ no universal CP6 baseline persistence object

Milestone
→ authoritative contextual checkpoint capability retained
→ no CP6 baseline persistence object until a concrete checkpoint-definition profile exists
```

The negative baseline dispositions are final physical decisions for CP6, not temporary placeholders. A later product vertical may add concrete typed structures through normal schema evolution when the exact semantics become real.

### 31.2 Outcome semantic boundary retained

Outcome remains:

```text
contextual result / disposition
of a specific Actual realization
in a bounded context where the result itself has semantic value
```

The following boundaries remain mandatory:

```text
Outcome != Actual
Outcome != Session
Outcome != Observation
Outcome != produced artifact/output
Outcome != Milestone
Outcome != Evidence
Outcome != Confirmation
Outcome != Provenance
Outcome != generic lifecycle/operational state
Outcome != actor-specific Participation/Contribution by default
```

Outcome is optional. The existence of an Actual does not require an Outcome row, value or placeholder.

Canonical epistemic rule:

```text
no Outcome
!= negative Outcome
!= failed Outcome
!= skipped Outcome
!= unconfirmed Outcome
```

Unknown/unconfirmed knowledge remains epistemic/Confirmation/Provenance territory. A negative result exists only when a concrete result family establishes that negative meaning.

### 31.3 OUT-U01 — CLOSED with NO CP6 baseline Outcome DDL

The Domain intentionally rejects one universal Outcome vocabulary. Accepted examples such as:

```text
passed
failed
partial
changes requested
decision deferred
approved
rejected
skipped
resolved
```

are contextual semantic examples, not one global PostgreSQL enum.

Therefore CP6-04 MUST NOT create any generic object equivalent to:

```text
dante.outcome
outcome_status
result_code text
result_kind text
result_value text
result_payload jsonb
outcome_type + payload
universal passed/failed/completed/skipped enum
```

No universal Outcome semantic root is authorized merely because the Physical Model recognizes Outcome as LR-06/LR-02 when materially persistent.

The closed baseline disposition is:

```text
OUT-U01
CLOSED

CP6-04 BASELINE OUTCOME OBJECTS
0
```

This is stronger than leaving OUT-U01 unresolved: it explicitly forbids placeholder result persistence until a concrete typed result family exists.

### 31.4 Future concrete Outcome materialization trigger

A future schema evolution may introduce a concrete Outcome family only when an accepted bounded result context supplies all semantics required to make the relation deterministic.

The minimum trigger contract is:

```text
exact result-bearing owner/context
exact applicability
exact typed result vocabulary or structure
exact cardinality against Actual
exact unknown/negative distinctions
exact correction/history semantics
exact source/Evidence/Provenance obligations
exact shared-versus-actor-specific result semantics
exact current/material-state requirements
```

Examples of future bounded families may eventually include an exam-result family, review-disposition family or another concrete product result model, but no such example authorizes a schema until its own authority is accepted.

No future implementation may satisfy this trigger by introducing a generic JSON result blob or free-text result discriminator.

### 31.5 Future material Outcome identity and addressability

When a future concrete result becomes persistent, addressability remains consequence-driven.

Two shapes remain possible depending on the real family:

```text
owner-bound typed result state
```

or, only when independent result lifecycle/reference/history justifies it:

```text
addressable LR-02 contextual Outcome record
+ ScopedRecordRef
+ MaterialStateRef where material consequence requires history
```

The existence of the Domain concept Outcome does not itself force independent ScopedRecordRef identity.

No Outcome NativeRef is introduced. The accepted 15 LR-01 native-owner set remains unchanged.

### 31.6 Exact Actual-state basis for consequential Outcome history

A future consequential historical Outcome must not float to whatever Actual state is current when the Outcome is later queried.

Required semantic basis:

```text
Outcome material state O1
→ Actual contextual identity A
→ exact actual.realization MaterialStateRef AR3
```

If Actual is later corrected:

```text
AR3
→ corrected/reconciled to AR4
```

historical Outcome O1 remains based on AR3 unless a new Outcome state/reconciliation explicitly changes that result basis.

Forbidden:

```text
Outcome row stores only actual_ref
and historical meaning silently follows current Actual state
```

This applies the already-closed MaterialState rule:

```text
source identity
!= source material state used by a consequential historical assertion/evaluation/result
```

### 31.7 Outcome correction, provenance and reconciliation boundary

A material Outcome correction may create another material Outcome state when the concrete future family requires retained history.

The database must preserve enough basis to distinguish:

```text
previous result assertion
new/corrected result assertion
source/provenance of each material assertion
applicable authority/confirmation/reconciliation where consequential
```

Outcome itself does not decide source precedence and does not become Reconciliation.

Provider or AI result assertions remain source/candidate information until the applicable acceptance/reconciliation contract establishes a canonical material Outcome.

### 31.8 Shared Outcome versus actor-specific reality

A shared Actual may have one shared/common result while individual actor facts differ.

Example semantic shape:

```text
shared Event Actual
→ shared Outcome: decision postponed

Actor A
→ follow-up assigned

Actor B
→ no action

Actor C
→ absent
```

Therefore future Outcome persistence MUST NOT duplicate a shared result once per Actor merely because Participation or Contribution is actor-scoped.

Likewise, one actor/provider assertion about a result does not automatically become canonical for every context. Source, Authority, Confirmation, Provenance, Visibility and Reconciliation remain separate.

### 31.9 Outcome as later Evidence

An accepted Outcome may be used as Evidence by another evaluation without becoming Evidence intrinsically.

Conceptual path:

```text
Outcome material state
→ typed Evidence use
→ Criterion / Evaluation context
```

Evidence use must bind the exact consequential source state where required.

No duplicate Outcome payload is copied into a generic Evidence store.

### 31.10 Part-1 Milestone candidate — precise supersession

Part 1 section 25.4 closed a candidate physical shape consisting of:

```text
dante.milestone

facet milestone.context

dante.milestone_context_state
dante.milestone_context_goal
dante.milestone_context_plan
```

That section correctly derived several **future contextual invariants**:

```text
Milestone is LR-02 / contextual rather than LR-01 native
Milestone normally matters within at least one Goal and/or Plan
Milestone may matter to multiple Goals and/or Plans
no rigid Goal → Plan → Milestone tree
Goal/Plan context may itself be materially version-sensitive
```

Those semantic/contextual conclusions remain valid.

However, the cumulative audit exposed one C-level physical defect in treating that context-only structure as sufficient CP6-04 baseline materialization:

```text
Milestone identity
+
Goal/Plan context
```

answers:

```text
where this checkpoint matters
```

but does not answer:

```text
what checkpoint has been defined
```

A persistent contextual UUID whose only material content is Goal/Plan context would therefore be a semantically incomplete LR-02 shell.

Section 31 explicitly supersedes **only** the Part-1 conclusion that the context-only Milestone family is implementation-authorized in the CP6 baseline.

It does not delete, rewrite or silently invalidate Part 1. The earlier derivation remains canonical historical reasoning and its valid future invariants are retained above.

### 31.11 Milestone requires a real checkpoint-definition profile

The Domain definition requires Milestone to represent a meaningful checkpoint such as a state, achievement, decision, delivery or transition that has become significant within a broader Goal/Plan path.

Therefore a material Milestone requires more than:

```text
milestone_ref
Goal references
Plan references
```

A future material family must contain or bind an exact **checkpoint-definition profile** that determines what it means for that Milestone to be the checkpoint it claims to be.

The definition may eventually be expressed by a typed state, accepted Criterion profile, external/specialist checkpoint contract or another owner-specific structure, depending on the real product requirement.

CP6 does not invent that profile now.

Forbidden placeholders include:

```text
checkpoint_type text with no closed vocabulary
criterion_json jsonb
rule_json jsonb
milestone_payload jsonb
generic label/name treated as executable checkpoint meaning
generic expression DSL introduced only to make the table non-empty
```

A human-readable label may later exist as presentation/content, but label text alone cannot supply the missing persistence semantics.

### 31.12 MIL-U01 — CLOSED with NO CP6 baseline Milestone DDL

Because no concrete checkpoint-definition profile is implementation-deterministic today, CP6 closes Milestone by **non-materialization**, not by leaving an empty envelope waiting for later fields.

The CP6-04 baseline MUST NOT create:

```text
dante.milestone
dante.milestone_context_state
dante.milestone_context_goal
dante.milestone_context_plan
milestone ScopedRecordRef registration
milestone scoped_address row/family
milestone.context MaterialState payload/current binding
milestone current-state view
milestone target state
milestone attainment state
milestone reached/status column
milestone indexes/triggers/ACLs
```

Closed disposition:

```text
MIL-U01
CLOSED

CP6-04 BASELINE MILESTONE OBJECTS
0
```

This does not remove Milestone from the Domain or Logical Model. It states that the current accepted semantics are insufficient to instantiate a truthful baseline SQL owner without inventing the defining checkpoint contract.

### 31.13 Future Milestone materialization trigger

The first future material Milestone family must establish at minimum:

```text
stable dependent/scoped Milestone identity where material addressability/history is needed
+
exact checkpoint-definition profile
+
non-empty contextual relevance to at least one Goal and/or Plan
```

The future design must then determine from the concrete family:

```text
exact current/material-state facets
exact context cardinalities
exact target representation if any
exact attainment/evaluation relationship
exact replacement/waiver/cancellation lifecycle if applicable
exact Evidence/Provenance requirements
exact query/index/ACL needs
```

No generic Milestone table is pre-authorized to receive arbitrary future checkpoint types.

### 31.14 Future Goal/Plan context invariants retained

When a concrete Milestone family is eventually materialized, the following Part-1 contextual invariants remain active unless a later accepted authority explicitly supersedes them:

```text
Milestone is dependent/contextual
Milestone is not a new LR-01 native owner
at least one Goal and/or Plan context must exist
one Milestone may matter to multiple Goals
one Milestone may matter to multiple Plans
one Goal/Plan may reference multiple Milestones
no rigid universal parent tree
```

If context changes materially while checkpoint identity remains coherent, the applicable future Milestone context state may require MaterialState history rather than mutable sparse foreign keys.

The exact concrete tables are intentionally not frozen before the checkpoint-definition family exists.

### 31.15 Definition, target expectation and attainment remain separate

A future Milestone implementation must preserve three distinct semantic dimensions:

```text
checkpoint definition
!= target expectation
!= actual/evaluated attainment
```

Example:

```text
Milestone
Beta release checkpoint

Target expectation
1 October
→ later revised to 15 October

Attainment
release becomes live on 18 October
```

Ordinary target movement does not automatically change Milestone identity.

Passing the target does not automatically establish:

```text
reached
failed
missed
cancelled
completed
```

Those conclusions require their own accepted semantics.

### 31.16 Future Milestone target semantics

If a future concrete Milestone carries a target expectation, the target uses the already accepted typed temporal representation appropriate to the real target semantics.

Potential exact forms may include:

```text
date-only target
floating-local target
named-zone-local target
absolute instant target
bounded target window
```

but only the forms required by the concrete family are materialized.

A Milestone target is not automatically:

```text
Schedule
Deadline / Temporal Constraint
capacity reservation
execution Session
Actual achievement time
```

Schedule placement and hard/soft Temporal Constraint remain separate concepts even when their geometry resembles a target date/window.

### 31.17 Milestone attainment cannot become an autonomous truth source

The Domain and Criterion/Evaluation authority require Milestone attainment to remain evaluation/evidence-backed checkpoint state.

Forbidden baseline/future shortcut:

```text
milestone.reached boolean
milestone.status = 'reached'
milestone.completed_at
```

when such a field becomes an independent canonical truth disconnected from its basis.

A future consequential attainment record/state must bind or reconstruct, as applicable:

```text
exact Milestone/checkpoint-definition MaterialStateRef
exact Criterion MaterialStateRef or equivalent exact typed rule state
exact Evidence/source material basis actually used
Evaluation context/result
relevant world/effective time
accepted/current chronology where material
Provenance/Authority/Confirmation basis where applicable
```

The exact schema belongs to the concrete future Criterion/Evaluation/Milestone family and is not invented by CP6 merely to provide a reached flag.

### 31.18 Outcome may support Milestone attainment without collapsing into it

Canonical composition remains:

```text
Actual
→ Outcome
→ typed Evidence use
→ Evaluation
→ Milestone attainment
```

when that chain is semantically justified.

But the following are forbidden:

```text
Outcome row copied into Milestone truth
Outcome presence automatically marks Milestone reached
Outcome = Milestone
```

A Milestone may also be reached from other valid evidence sources, including Observation, imported/external state, Decision, explicit authorized declaration or composite evidence.

### 31.19 No automatic Milestone manufacture

The database/runtime must not automatically create or attain a Milestone merely because another record exists or changed.

Forbidden universal implications:

```text
Activity completed
→ create/reach Milestone

Event occurred
→ create/reach Milestone

Outcome exists
→ create/reach Milestone

Goal reaches arbitrary mathematical percentage
→ create Milestone

current date passes target date
→ reach/fail Milestone
```

A Milestone is intentional/significant contextual structure, not a mechanical duplicate of every execution result or metric threshold.

### 31.20 Milestone identity, revision and replacement boundary

Ordinary changes such as:

```text
target-date revision
supporting-Evidence update
label/presentation correction
additional Goal/Plan context
readiness/progress recalculation
```

need not create a new Milestone identity when checkpoint meaning remains coherent.

A material change from one checkpoint meaning to another may require replacement/new contextual identity rather than a new version of the same Milestone.

Example pressure:

```text
"B1 reached"
→ redefined as
"C1 reached"
```

must not be preserved as one identity merely because an implementation wants to update a definition column.

The future concrete checkpoint-definition profile must therefore participate in identity/replacement review.

### 31.21 CP6 object-inventory consequences

This checkpoint removes speculative objects from the CP6-04 baseline object inventory.

Exact result:

```text
OUTCOME BASELINE
canonical tables                 0
scoped-address families          0
material-state facets            0
current-binding views            0
indexes                           0
business triggers                0
SQLAlchemy business mappings      0
runtime business ACL objects      0

MILESTONE BASELINE
canonical tables                 0
scoped-address families          0
material-state facets            0
current-binding views            0
indexes                           0
business triggers                0
SQLAlchemy business mappings      0
runtime business ACL objects      0
```

No sequence is required because DANTE native/scoped/material identifiers are UUID-based where they exist, and these families do not exist in the CP6 baseline anyway.

DB-U15 and DB-U21 therefore must not include imagined Outcome/Milestone objects when the final index/privilege matrices are frozen.

### 31.22 Database Dictionary consequences

The final CP6 Database Dictionary describes **real baseline database objects only**.

Therefore the machine-readable dictionary MUST NOT fabricate table entries for:

```text
Outcome
Milestone
```

as though they were materialized.

The human-readable blueprint remains the authority explaining their explicit non-materialization and future trigger contract.

If the dictionary supports a separate non-object/deferred register later, such a register may reference these dispositions without pretending they are SQL objects. That representation must not pollute the table/view catalogs.

### 31.23 Alembic migration consequences

CP6-04 migrations MUST NOT create Outcome or Milestone business DDL.

Specifically, the migration DAG has no baseline migration operations for:

```text
CREATE TABLE outcome
CREATE TABLE milestone
CREATE TABLE milestone_context_*
ADD scoped_address family milestone
ADD material facet milestone.*
CREATE outcome/milestone current views
CREATE outcome/milestone indexes/triggers
GRANT outcome/milestone runtime privileges
```

A future concrete family is introduced by an ordinary reviewed additive migration after its semantic trigger is accepted.

Such a future migration must preserve compatibility with historical data without retroactively inventing Outcome/Milestone records for prior Actual/Goal/Plan rows unless an explicit backfill rule is semantically justified and auditable.

### 31.24 SQLAlchemy mapping consequences

CP6-04 MUST NOT introduce generic mapped classes such as:

```text
Outcome
OutcomeState
Milestone
MilestoneContextState
```

solely to mirror Domain concept names.

No abstract/general result mapping or generic checkpoint mapping substitutes for the missing concrete schema.

Future mappings must correspond one-to-one with the accepted concrete PostgreSQL objects and retain the normal DANTE rule:

```text
ORM convenience
!= semantic authority
```

### 31.25 Runtime/API consequences

This checkpoint does not prohibit product-level Outcome or Milestone language in future APIs/UI. It prohibits pretending the current baseline has canonical generic persistence for those concepts.

Until a concrete family is introduced, runtime code must not persist them through:

```text
JSON blob columns on unrelated owners
generic metadata/property bags
universal semantic relation tables
free-text status fields
provider payload promoted to canonical result/checkpoint truth
```

A future vertical that needs a concrete Outcome/Milestone must perform schema evolution first rather than hiding the new semantics in application-only structures.

### 31.26 Privilege / DB-U21 consequences

Because no Outcome/Milestone baseline objects exist:

```text
runtime privileges for those objects
= none
```

This does not change the already accepted DB-U21 direction:

```text
provisioning
→ roles/database/schema foundation only

object migration
→ grants exact business/control privileges required by that object
```

Future Outcome/Milestone objects, if introduced, must receive explicit least-privilege ACL design in the same migration/review that introduces them.

### 31.27 Lifecycle / DB-U14 consequences

No universal Outcome/Milestone lifecycle columns are introduced.

The existing baseline remains:

```text
no universal deleted_at
no universal is_deleted
no generic tombstone/status
ON DELETE NO ACTION by default
non-destructive historical continuity where material
```

Future concrete families must define their own exact replacement/redaction/retention behavior where real policy requires it.

The negative baseline disposition means there is no hidden lifecycle contract to maintain for non-existent Outcome/Milestone tables.

### 31.28 Index / DB-U15 consequences

No Outcome/Milestone index is added speculatively.

The final DB-U15 matrix must therefore evaluate only the actual frozen object/query inventory.

Future concrete result/checkpoint families must justify each index from real integrity/query pressure, following the existing rule:

```text
PK/UNIQUE/FK-supporting/query index
→ exact reason recorded

"might be useful"
→ insufficient
```

### 31.29 Direct PostgreSQL proof obligations for this disposition

Because the baseline decision is non-materialization, CP6-04/05 proof is primarily **absence and boundary proof**, not CRUD proof.

The final schema QA must prove at least:

```text
no dante.outcome table                                  PASS
no generic Outcome enum/type                            PASS
no universal result_code/result_payload fallback        PASS
no generic Outcome SQLAlchemy mapping                   PASS

no dante.milestone table                                PASS
no milestone_context_* baseline tables                  PASS
no milestone scoped_address family registration         PASS
no milestone.* baseline MaterialState facet             PASS
no reached/status/completed_at Milestone truth shortcut PASS

no unexpected Outcome/Milestone migration operations    PASS
no Outcome/Milestone runtime ACL entries                PASS
Database Dictionary advertises no non-existent object   PASS
```

These checks belong to final CP6-04/05 schema/dictionary/mapping reconciliation. They are obligations, not tests claimed as already executed by this documentation checkpoint.

### 31.30 Future evolution proof obligations

When a concrete Outcome or Milestone family is eventually introduced, the implementing change must add its own direct proof matrix.

At minimum, a future Outcome family must prove:

```text
exact typed result vocabulary/structure enforced
invalid result shape rejected
absence remains distinct from negative result
exact Actual realization state basis retained where consequential
historical correction does not rewrite earlier source basis
shared result is not duplicated merely by actor-specific participation
```

A future Milestone family must prove:

```text
checkpoint definition is non-empty and typed
context includes at least one eligible Goal/Plan as required
no rigid hierarchy is accidentally imposed
checkpoint definition / target / attainment remain separate
target passage alone does not establish attainment
attainment retains exact evaluation/evidence basis where material
checkpoint replacement does not rewrite prior identity/history
```

### 31.31 Whole-database A/B/C cumulative audit — findings

The complete accumulated database was replayed after the candidate dispositions.

Findings and repairs for this block:

| Finding | Class | Repair / final disposition |
|---|---|---|
| universal Outcome enum/table | C | forbidden; OUT-U01 closed NO baseline DDL |
| generic Outcome `result_code` / JSON payload | C | forbidden |
| Outcome mandatory for every Actual | C | forbidden; Outcome remains optional |
| missing Outcome interpreted as negative | C | forbidden |
| consequential Outcome follows current Actual after correction | B/C | future material Outcome binds exact Actual realization MaterialStateRef |
| shared Outcome duplicated per Actor/Contribution | C | forbidden; actor-scoped facts stay separate |
| provider/AI assertion treated as canonical Outcome | C | source/confirmation/reconciliation remains separate |
| Part-1 Milestone context-only envelope treated as implementation-complete | C | §25.4 materialization conclusion narrowly superseded |
| Milestone UUID + Goal/Plan context without checkpoint definition | C | no CP6 baseline Milestone DDL |
| generic Milestone checkpoint type/JSON used to fill missing semantics | C | forbidden |
| `reached` boolean/status as autonomous canonical truth | C | forbidden |
| Milestone target collapsed into Schedule/Deadline | C | forbidden |
| Activity/Event/Outcome automatically reaches Milestone | C | forbidden |
| target-date passage automatically reaches/fails Milestone | C | forbidden |
| stored universal Milestone progress percentage | C | forbidden |
| future attainment floats to current Criterion/Evidence states | B/C | exact material evaluation/source basis required where consequential |
| Milestone promoted to LR-01 native owner | C | forbidden; future materialization remains dependent/scoped |
| speculative baseline Outcome/Milestone indexes/ACLs/mappings | B/C | object inventory count explicitly zero |

No repair requires reopening Domain, Logical, Physical or CP6-02 authority.

### 31.32 Whole-database A/B/C cumulative audit — retained invariants

Post-repair regression retains the previously closed database boundaries:

```text
57 / 57 Domain concepts                              PASS
15 / 15 LR-01 native owners                          PASS

NativeRef != ScopedRecordRef                         PASS
ScopedRecordRef != MaterialStateRef                   PASS
MaterialState existence != current                    PASS
current binding never inferred from timestamp/UUID   PASS
DB-U14 non-destructive lifecycle                      PASS
DB-U12 recurrence/Occurrence closure                  PASS
Schedule / Session / Actual separation                PASS
Actual unknown != known non-realization               PASS

Outcome != Actual                                     PASS
Outcome != Session                                    PASS
Outcome != Observation                                PASS
Outcome != Milestone                                  PASS
Outcome != Evidence                                   PASS
Outcome != lifecycle state                            PASS

Milestone != Goal                                     PASS
Milestone != Criterion                                PASS
Milestone != Activity/Event                           PASS
Milestone != Outcome                                  PASS
Milestone != Deadline                                 PASS
checkpoint definition != target != attainment         PASS
attainment != duplicated underlying reality           PASS

universal Entity/Thing root                           0
universal Relationship/edge root                      0
universal Outcome root                                0
context-only Milestone shell                          0
generic result enum                                   0
generic milestone rule payload                        0
semantic JSON fallback                                0
new LR-01 owner                                       0
unclassified new item                                 0
C defects after repair                                0
```

### 31.33 Checkpoint-D closure register

Final checkpoint status:

```text
CONSOLIDATION CHECKPOINT D
OUTCOME / MILESTONE BASELINE DISPOSITION
PASS AFTER HARDENING

OUT-U01
CLOSED
FINAL CP6 BASELINE DISPOSITION: NO OUTCOME DDL

MIL-U01
CLOSED
FINAL CP6 BASELINE DISPOSITION: NO MILESTONE DDL

PART 1 SECTION 25.4
RETAINED AS HISTORICAL DERIVATION
NARROWLY SUPERSEDED ONLY FOR CP6-04
MILESTONE CONTEXT-ONLY MATERIALIZATION AUTHORIZATION

GLOBAL UNRESOLVED DB-U ITEMS
9

LOCAL EXACT UNRESOLVED ITEMS
4

LOCAL EXACT OPEN
AGR-U01
CRT-U01
EVL-U01
TC-U01

UNCLASSIFIED NEW ITEMS
0

CP6 BUSINESS DDL AUTHORIZED
NO

GATE 03
NOT YET EARNED
```

This closes the current block. The next substantive block must begin from this exact saved boundary and must not silently rematerialize generic Outcome or Milestone structures while closing Agreement, Criterion, Evaluation or Temporal Constraint.