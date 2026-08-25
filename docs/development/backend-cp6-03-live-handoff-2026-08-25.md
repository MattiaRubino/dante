# CP6-03 CURRENT LIVE HANDOFF — 2026-08-25

**Status:** CURRENT / TEMPORARY / CROSS-CHAT CONTINUITY / NON-NORMATIVE  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/logical-postgresql`  
**Authoritative snapshot HEAD before this handoff write:** `7c465d5f69d2e4d4e11b712e05276cb7f37650dd`  
**Protected `main` observed at handoff preparation:** `87fe668c2ade78b17e0326d635e4d7a67920ae8a`  
**Branch relation observed:** diverged / feature ahead 146 / behind 6 / merge base `f1aacb0724088e0b4b086008a5219c2fba5ce0cf`  
**Main realignment:** intentionally deferred; DO NOT merge/rebase/reconcile `main` during the current CP6-03 security/final-audit sequence unless separately gated.  
**Current phase:** CP6-03 — Whole DANTE Database Blueprint / final security + audit closure  
**CP6-04 real database materialization:** NOT STARTED / NOT AUTHORIZED  
**Gate 03:** NOT YET EARNED

---

## 0. Why this file exists

This is the current cross-chat resume artifact for the CP6 PostgreSQL workstream. It is deliberately detailed so a fresh ChatGPT conversation can resume without asking the user to restate decisions, without reconstructing the database from conversation memory, and without silently dropping the repository-engineering discipline used so far.

This file is **not** a new architecture authority. Repository canonical sources listed below remain authoritative. If this handoff conflicts with those sources, the canonical source wins. Later canonical Database Reference parts supersede earlier provisional statements only where they explicitly say so.

The older file:

```text
docs/development/backend-cp6-03-live-handoff.md
```

is retained as historical continuity/evidence. This dated handoff is the **current resume document** for the next chat. Read this file first; consult the older LIVE file when detailed historical chronology is useful.

---

# 1. Mandatory first actions for the next chat

A fresh conversation MUST NOT immediately write Part 18 or claim Gate 03.

It must execute this bootstrap in order:

```text
1. verify live HEAD of feature/logical-postgresql;
2. compare it to the snapshot/known current state recorded here;
3. if HEAD moved, inspect every intervening commit before trusting this handoff;
4. verify protected main relation but DO NOT integrate main unless separately authorized;
5. read docs/database/README.md;
6. read this handoff fully;
7. consume ALL active Database Architecture & Reference Parts 1–17 together;
8. read CP6 workstream + CP6-02 Constitution + CP6-01 coverage closure;
9. inspect current backend/provisioning/migration/test code for every security/implementation claim;
10. independently verify the proposed DB-U26 security hardening before writing it;
11. show/use an exact bounded write gate;
12. immediately before first write re-check HEAD == approved PRE-SCOPE;
13. after writes perform remote readback + PRE-SCOPE→HEAD exact compare;
14. only after DB-U26 repair is clean rerun the final independent tombstone/security replay over Parts 1–18;
15. only a clean replay may earn Gate 03;
16. STOP at Gate 03; CP6-04 requires a separate explicit user authorization.
```

Never ask the user to repeat known project state when the repository can answer it.

---

# 2. Repository/authority hierarchy

Use repository truth over conversation memory.

For this workstream consume authority in this order:

```text
1. protected repository truth / real code / migrations / tests where implementation state matters;
2. closed Domain model;
3. closed Whole Logical model;
4. accepted PostgreSQL Physical model;
5. CP6-01 concrete persistence coverage + closure;
6. CP6-02 PostgreSQL Persistence Constitution + closure / ADR-010;
7. complete CP6-03 Database Architecture & Reference Parts 1–17 consumed together;
8. docs/database/dictionary readiness contract;
9. current CP6 workstream routing/resume documents;
10. this handoff for operational continuity only;
11. historical chat memory only as secondary context.
```

Do not use one late Database Reference part as a standalone summary. Parts 1–17 are one accumulated authority with narrow explicit supersessions.

---

# 3. Mandatory documents to study before material work

## 3.1 Repository operating/safety layer

Read or re-check at minimum:

```text
README.md
docs/README.md
docs/PROJECT-STATUS.md
docs/ROADMAP.md

docs/development/agent-operating-manual.md
docs/development/operating-rules.md
docs/development/documentation-and-handoff.md
docs/development/branching-and-environments.md
docs/development/repository-engineering-safety.md
```

The current branch may intentionally differ from protected main. Do not treat divergence as permission to merge.

## 3.2 CP6 routing/current workstream

```text
docs/workstreams/logical-postgresql.md
docs/development/backend-cp6-03-live-handoff.md
docs/development/backend-cp6-03-live-handoff-2026-08-25.md  ← THIS FILE
```

## 3.3 CP6-01

```text
docs/development/backend-cp6-01-concrete-persistence-coverage.md
docs/development/backend-cp6-01-concrete-persistence-coverage-part-2.md
docs/development/backend-cp6-01-concrete-persistence-coverage-closure.md
```

Gate 01 is CLOSED/PASS. The Part-2 non-57/cross-cutting ledger remains mandatory input: Account, Principal/security context, reference controls, current state, idempotency pressure, provider/derived boundaries, tombstone/anti-resurrection, outbox triggers, specialist activation pressure, etc. Do not audit only the 57 Domain concepts.

## 3.4 CP6-02

```text
docs/development/backend-cp6-02-postgresql-persistence-constitution.md
docs/development/backend-cp6-02-postgresql-persistence-constitution-closure.md
docs/decisions/ADR-010-postgresql-persistence-constitution.md
```

Gate 02 is CLOSED/PASS. The Constitution is the reusable PostgreSQL doctrine for TECH/ID/REF/MAT/HIST/TIM/MISS/LIFE/TYP/REL/CON/IDX/TX/IDEM/PROV/CAP/MIG/SEC/QA.

## 3.5 PostgreSQL Physical model

At minimum:

```text
docs/physical-model/README.md
docs/physical-model/pm-02-primary-mapping-overview-v1.md
docs/physical-model/mappings/postgresql-18.4-v1.md
docs/physical-model/pm-03-semantic-hard-gate-preflight-v1.md
docs/physical-model/pm-11-explicit-selection-v1.md
docs/physical-model/pm-12-accepted-physical-model-v1.md
docs/physical-model/pm-13-clean-room-qa-v1.md
docs/physical-model/recommendation/post-selection-validation-register-v1.md
```

Historical Physical phase-time patch evidence is PostgreSQL 18.4. Current technical local/foundation patch used later is PostgreSQL 18.6. Do not rewrite old evidence as if it had run on 18.6.

## 3.6 Database Architecture & Reference — ALL active parts

```text
docs/database/dante-postgresql-database.md             Part 1
docs/database/dante-postgresql-database-part-2.md      Part 2
docs/database/dante-postgresql-database-part-3.md      Part 3
docs/database/dante-postgresql-database-part-4.md      Part 4
docs/database/dante-postgresql-database-part-5.md      Part 5
docs/database/dante-postgresql-database-part-6.md      Part 6
docs/database/dante-postgresql-database-part-7.md      Part 7
docs/database/dante-postgresql-database-part-8.md      Part 8
docs/database/dante-postgresql-database-part-9.md      Part 9
docs/database/dante-postgresql-database-part-10.md     Part 10
docs/database/dante-postgresql-database-part-11.md     Part 11
docs/database/dante-postgresql-database-part-12.md     Part 12
docs/database/dante-postgresql-database-part-13.md     Part 13
docs/database/dante-postgresql-database-part-14.md     Part 14
docs/database/dante-postgresql-database-part-15.md     Part 15
docs/database/dante-postgresql-database-part-16.md     Part 16
docs/database/dante-postgresql-database-part-17.md     Part 17
```

Do not modify Parts 1–17 merely to make them prettier. Narrow correction/continuation belongs in a later Part unless a separately gated repair explicitly authorizes otherwise.

## 3.7 Database Dictionary foundation

```text
docs/database/dictionary/README.md
docs/database/dictionary/scope.json
docs/database/dictionary/schema/object-v1.schema.json
docs/database/dictionary/schema/scope-v1.schema.json
```

Dictionary status is readiness/hardened only. Object-specific entries do not exist yet because CP6-04 has not materialized the corresponding PostgreSQL objects.

## 3.8 Current real backend/foundation code that must be inspected when relevant

At minimum:

```text
apps/backend/src/dante/platform/database/metadata.py
apps/backend/src/dante/platform/database/provisioning.py
apps/backend/src/dante/platform/database/runtime.py
apps/backend/src/dante/config/settings.py
apps/backend/migrations/env.py
apps/backend/migrations/versions/20260820_01_cp3_persistence_baseline.py
apps/backend/tests/integration/database/conftest.py
apps/backend/tests/integration/database/test_migrations.py
apps/backend/tests/integration/database/test_privileges.py
apps/backend/tests/integration/database/test_runtime.py
apps/backend/tests/integration/database/test_transactions.py
apps/backend/pyproject.toml
.github/workflows/backend-ci.yml
```

Important current truth: CP3 business migration is still business-empty; there is no hidden business ORM schema. `provisioning.py` still contains the broad CP3 grant posture that future P0 must harden before M1.

---

# 4. Methodology / quality bar — mandatory

The user expects the database to be engineered like a serious large product, not a demo.

For every coherent block use this process:

```text
A. derive from complete repository authority;
B. audit cumulatively against Domain + Logical + Physical + CP6 + real code;
C. classify findings:
   A = sound/retain
   B = real hardening/repair needed before write/materialization
   C = structural/semantic contradiction that may require upstream reopen;
D. repair every B/C before calling the block closed;
E. never convert importance into a generic table by reflex;
F. never omit determinable structure by calling it vertical-specific;
G. never invent fields/state/vocabulary to fill uncertainty;
H. freeze exact implementation contract before CP6-04;
I. use PostgreSQL declarative constraints before triggers;
J. use triggers only for real cross-row/cross-table/commit-time invariants;
K. every trigger lookup must be bounded/index-backed;
L. no speculative indexes;
M. no broad runtime grants by habit;
N. no SQL/query behavior that depends on insertion order, UUID order or implicit latest;
O. history/current/correction must remain truthful;
P. provider/AI/solver state never silently becomes canonical;
Q. proof evidence is PASS only when actually executed; staged evidence stays staged;
R. after write: remote readback + exact diff + unexpected=0 + truthful CI status.
```

Documentation is implementation in CP6-03: if the design leaves a decision for Alembic to invent, CP6-03 is incomplete.

---

# 5. Exact Git write discipline

Every repository mutation requires a stated gate:

```text
BRANCH
feature/logical-postgresql

PRE-SCOPE
<exact current HEAD>

CREATE
<exact paths>

UPDATE
<exact paths>

DELETE
<exact paths>

PURPOSE
<bounded purpose>

EXPLICITLY OUT OF SCOPE
<bounded exclusions>
```

Immediately before first mutation:

```text
compare approved PRE-SCOPE → feature/logical-postgresql
must be IDENTICAL
```

If HEAD moved, STOP and re-gate.

After writes:

```text
remote readback
PRE-SCOPE → HEAD compare
exact unique paths
added/modified/deleted counts
unexpected paths = 0
historical approved content preserved unless explicit gate allowed edits
feature relation to protected main
actual CI/status evidence only
```

Never say CI PASS on docs-only commits when no run/status exists.

---

# 6. CP6 phase roadmap

The current simplified lifecycle is:

```text
CP6-01  Concrete Persistence Coverage
✅ CLOSED / Gate 01 PASS

CP6-02  PostgreSQL Persistence Constitution
✅ CLOSED / Gate 02 PASS

CP6-03  WHOLE DANTE DATABASE BLUEPRINT
ACTIVE / near closure

  ✅ 57/57 final materialization disposition / DB-U23
  ✅ Final Actual PostgreSQL Object Inventory
  ✅ DB-U08 Final PostgreSQL Naming
  ✅ DB-U15 Final Index Matrix
  ✅ DB-U21 Exact ACL Matrix
  ✅ Migration / Materialization DAG
  ✅ SQLAlchemy Mapping Plan
  ✅ Database Dictionary Readiness
  ✅ DB-U24 Implementation Determinism Hardening
  ✅ Direct PostgreSQL Proof/Test Plan
  ✅ DB-U25 Second Tombstone Repair / Part 17
  ✅ post-Part17 semantic/database tombstone replay currently clean
  ▶ DB-U26 DATABASE SECURITY EXECUTION HARDENING — NEXT / PROPOSED
  ⏳ final independent Parts 1–18 tombstone + security replay
  ⏳ Gate 03 closure

CP6-04  WHOLE DATABASE MATERIALIZATION
NOT STARTED / NOT AUTHORIZED

CP6-05  WHOLE DATABASE DIRECT QA + CP6 CLOSURE
NOT STARTED

POST-CP6
FIRST PRODUCT VERTICAL
NOT STARTED
```

Critical boundary: when Gate 03 is earned, STOP. Do not create business migrations/tables/mappings until a separate user-approved CP6-04 materialization gate.

---

# 7. Closed semantic baseline

## 7.1 Whole Domain/Logical census

Exactly 57 Domain concepts are classified. Whole Logical is closed. No unclassified Domain concept remains.

Exactly 15 LR-01 native identity owners:

```text
Person
Living Referent
Asset
Place
Content Artifact
Collective
Possibility
Goal
Plan
Activity
Event
Routine
Occurrence
Session
Observation
```

Actor / Subject / Resource are roles/capabilities, not native roots.

Reference families remain distinct:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

## 7.2 Hard non-collapse invariants

Preserve at minimum:

```text
Person != Account != Principal != Actor
Person != Living Referent != Asset
Subject != Resource != native identity
Possibility != Goal != Proposal != Decision != Plan != Activity
Routine != Recurrence != Occurrence
Occurrence != Schedule != Session != Actual
Actual != Observation != Outcome
Outcome != Milestone
Evidence != Provenance
Version != Reconciliation
Authority != Visibility
Agreement != Consent
Ownership != Possession
Schedule != Capacity Claim != Resource Allocation != Actual use
provider state != canonical DANTE state
derived projection != canonical truth
current != historical
correction != overwrite
AI/solver inference != accepted canonical effect
```

Rejected globally:

```text
universal Entity / Thing
universal Relationship / edge
canonical EAV/property bag
universal event ontology
generic semantic Fact/Version root
required-semantics JSONB escape hatch
PostgreSQL inheritance as ontology
generic kind+uuid reference without DB integrity
```

---

# 8. Final 57-concept materialization disposition

Checkpoint J / DB-U23 is CLOSED.

Final classes:

```text
A — BASELINE PHYSICAL OBJECT(S)                       17
B — REPRESENTED THROUGH EXISTING STRUCTURE             2
C — NO INDEPENDENT ROOT / VALUE / ROLE                 7
D — FINAL NO BASELINE DDL + FUTURE TRIGGER            31
--------------------------------------------------------
TOTAL                                                   57
```

Baseline-physical concepts:

```text
Activity
Actual
Asset
Collective
Content Artifact
Event
Goal
Living Referent
Observation
Occurrence
Person
Place
Plan
Possibility
Routine
Schedule
Session
```

Existing-structure representation:

```text
Recurrence
Version
```

No independent root/value/role:

```text
Actor
Capacity
Monetary Amount
Quantity
Resource
Subject
Verification
```

All other 31 concepts are final no-baseline-DDL with explicit future capability/profile triggers. Do not reintroduce generic Agreement/Milestone/TemporalConstraint/Criterion/Evaluation/Outcome/etc. objects from older provisional sections.

Schema object existence does not authorize semantic creation. Observation identity shell remains baseline but semantic Observation creation waits for the first concrete typed assertion profile.

---

# 9. Final surviving object model before materialization

## 9.1 DANTE-owned baseline

```text
68 tables
5 current-facet views
14 integrity routines
75 trigger attachments
95 physical indexes
68 foreign keys
120 CHECK constraints
```

No change to these counts is currently expected from DB-U26 security hardening.

No baseline DANTE-owned:

```text
custom ENUMs/domains
application sequences
materialized views
RLS policies
partitioned business tables
generic recurrence root
generic provider/idempotency/outbox/search/vector table
```

Technical foundation is separate:

```text
schema dante
dante.alembic_version
dante_owner
dante_migrator
dante_runtime
```

Extension-owned objects are separate and not DANTE Dictionary entries:

```text
postgis
vector
pg_trgm
unaccent
pg_stat_statements
```

## 9.2 Scoped families

Exactly:

```text
schedule
actual
```

## 9.3 MaterialState facets

Exactly:

```text
schedule.placement
actual.realization
session.timing
routine.recurrence
event.recurrence
```

No historical provisional facet may reappear merely because an earlier Part mentioned it.

---

# 10. Table allocation summary

The 68-table baseline is frozen as:

```text
15 native owner identity shells
 5 shared address/current/material control tables
 2 scoped semantic owner tables: schedule / actual
 6 Schedule placement companion/history tables
 4 Actual realization companion/history tables in addition to actual owner
 5 Session timing/history companion tables
26 Routine/Event Recurrence tables
 5 Occurrence-generation tables
-----------------------------------
68 total
```

Read Part 9/17 for exact names and full table-by-table structure. Do not reconstruct the schema from this summary alone.

---

# 11. Naming / indexes / ACL / integrity — frozen

## DB-U08 — CLOSED

Professional PostgreSQL naming is frozen:

```text
ASCII lowercase lower_snake_case
unquoted
semantic
<= 63 bytes
```

CP3 convention retained:

```text
pk_<table>
fk_<table>_<columns>_<target>
uq_<table>_<columns>
ix_<table>_<columns>
ck_<table>_<semantic_rule>
```

Explicit `ux_`, `trg_`, `ctrg_` conventions were added where required. Overlength FK names use registered semantic aliases; no silent PostgreSQL truncation dependency.

## DB-U15 — CLOSED

```text
95 DANTE physical indexes
= 68 PK-backed
+ 2 UNIQUE-backed
+ 25 explicit indexes
```

All 68 FKs were reviewed; no index-every-FK shortcut. No speculative GiST/GIN/BRIN/trigram/vector/INCLUDE index.

## DB-U21 — CLOSED, then Part 17 narrowly hardens history INSERT

Runtime baseline:

```text
SELECT          68/68 tables
INSERT          bounded; shell/create barriers respected
TABLE UPDATE    0 blanket
COLUMN UPDATE   five history current_until_at columns only
BASE DELETE     0
TRUNCATE        0
REFERENCES      0
TRIGGER         0
MAINTAIN        0
GRANT OPTION    0
```

Five current views are the bounded current-binding capability surface. Base current-control tables are not direct runtime DML surfaces.

Part 17 narrows the five current-history INSERT surfaces so runtime can insert only owner/state/current_from columns; `current_until_at` must be born NULL and can only move once NULL→timestamp through the already-bounded column UPDATE.

## Integrity layer

```text
14 bounded integrity routine roles
75 trigger attachments
18 immediate
57 deferred constraint triggers
120 named CHECK constraints
68 FKs
```

Part 16 freezes physical function/trigger properties and error contract. Part 17 repairs exact recurrence/generation/history semantics without changing object counts.

---

# 12. Migration/materialization DAG — FROZEN

P0 plus one linear seven-node Alembic chain:

```text
CP3 baseline
↓
P0 provisioning/security hardening prerequisite — non-Alembic
↓
M1 cp6_native_identity_address
↓
M2 cp6_scoped_material_control
↓
M3 cp6_schedule_actual_session
↓
M4 cp6_recurrence
↓
M5 cp6_core_integrity_current_views
↓
M6 cp6_occurrence_generation
↓
M7 cp6_runtime_acl_activation
```

One Alembic DAG/head only.

Allocation reconciles to:

```text
68 tables
95 indexes
14 routines
75 triggers
5 views
```

Runtime business DML is deliberately activated only at M7, after integrity surfaces are present.

P0 must be fail-closed before M1 so CP3 blanket default privileges cannot leak onto new business objects. Part 16 freezes the M1 preflight requirement.

---

# 13. SQLAlchemy Mapping Plan — FROZEN

Target mapping topology:

```text
dante/platform/database/
  metadata.py
  references.py
  locking.py
  mappings/
    identity.py       15 Row mappings
    addressing.py      5
    schedule.py        7
    actual.py          5
    session.py         5
    recurrence.py     26
    occurrence.py      5
    views.py            Core-only view handles
```

Exactly 68 table mappings, conventionally `...Row` to avoid pretending persistence rows are Domain entities.

Baseline:

```text
ORM relationship()  0
ORM cascade         0
delete-orphan       0
implicit lazy graph 0
```

The five current views are SQLAlchemy Core handles in separate view metadata, not fake ORM entities.

`NativeRef`, `ScopedRecordRef`, `MaterialStateRef` remain distinct typed Python references over PostgreSQL UUID.

UUIDv7 stable IDs are emitted explicitly at application boundary; PostgreSQL root checks enforce version 7 at the true identity emission roots.

Functions/triggers/views remain migration-owned DDL, not ORM-event replicas.

Advisory lock scheme is frozen in Part 14/17; no lock table or fake mutable owner column is introduced.

---

# 14. Database Dictionary — READY / HARDENED

Format:

```text
JSON
JSON Schema Draft 2020-12
schema version 1
```

Target standalone entries after materialization:

```text
68 table entries
5 view entries
14 routine entries
= 87 standalone entries
```

Triggers/indexes/constraints are embedded in owning table entries rather than exploding into hundreds of micro-files.

Validation is intentionally two-level:

```text
JSON Schema structural validation
+
DANTE semantic/cross-file validator
```

Semantic validator must check uniqueness/cross-references/count reconciliation and PostgreSQL/SQLAlchemy/Alembic drift. Object-specific entries remain absent until the same CP6-04 change creates the real object.

---

# 15. Direct PostgreSQL Proof/Test Plan — FROZEN

Part 16 defines DBP-01..DBP-20. CP6-05 must extend the existing real PostgreSQL suite, not create a parallel fake framework.

Required proof dimensions include:

```text
exact PostgreSQL/extension environment
P0 provisioning hardening / legacy CP3 upgrade path
single linear Alembic DAG
fresh→head
CP3→CP6 head
truthful empty-DB downgrade roundtrip where applicable
M1..M7 stage topology
68/5/14/75/95 inventory reconciliation
68 FK / 120 CHECK structural reconciliation
95/95 index properties
SQLAlchemy↔PostgreSQL drift
Dictionary↔PostgreSQL↔SQLAlchemy↔Alembic drift
ACL tests as actual roles
Native/Scoped/Material address integrity
current/history semantics
deferred-trigger SET CONSTRAINTS proof
Schedule positive/negative matrix
Actual missingness/negative matrix
Session timing/pause matrix
Routine/Event recurrence × four physical families
Occurrence generation matrix
current-view DML/capability proof
real multi-connection concurrency/advisory-lock proof
historical reconstruction
truthful staged evidence
```

Do not assert planner-specific `EXPLAIN MUST choose index` behavior on an empty synthetic DB.

---

# 16. Part 17 / DB-U25 — repair status

Part 17 is CLOSED and repository QA for its repair is clean.

Verified repair delta:

```text
PRE-SCOPE
f2bdab00faee84c3be6e951b848417fae9330446

FINAL REPAIR HEAD
7c465d5f69d2e4d4e11b712e05276cb7f37650dd

unique paths
4

CREATE
docs/database/dante-postgresql-database-part-17.md

UPDATE
docs/database/README.md
docs/workstreams/logical-postgresql.md
docs/development/backend-cp6-03-live-handoff.md

unexpected paths
0

deletions
0

Parts 1–16 changed
0
```

Five real B findings repaired:

```text
TOMB-B01
Recurrence selector / phase / range determinism

TOMB-B02
non-quota generated-coordinate duplicate prevention

TOMB-B03
five NULL-unsafe CHECK expressions

TOMB-B04
materialized Occurrence exact membership in governing Recurrence

TOMB-B05
one-way current-history lifecycle + column-scoped INSERT
```

No Domain, Logical or Physical reopen was required. No new semantic root, table, view, routine, trigger or index was introduced.

---

# 17. Post-Part17 tombstone replay status

A deep post-repair replay has been performed over Domain → Logical → Physical → CP6 → Parts 1–17.

Current result before the extra security lane:

```text
missing Domain concept                 0
unclassified concept                  0
Domain reopen                         0
Logical reopen                        0
Physical reopen                       0
new semantic root                     0
generic Entity/Relationship/EAV       0
dangling scoped family                0
dangling MaterialState facet          0
hidden business schema                0
object inventory drift                0

68 tables                             RECONCILED
5 views                               RECONCILED
14 routines                           RECONCILED
75 triggers                           RECONCILED
95 indexes                            RECONCILED
68 FKs                                RECONCILED
120 CHECKs                            RECONCILED

DB-U25 findings                       5/5 REPAIRED
```

Do **not** yet call this final Gate-03 PASS because the user explicitly requested an additional security review before closure. That security review identified one sensible final pre-Gate03 hardening umbrella: DB-U26.

---

# 18. DB-U26 — DATABASE SECURITY EXECUTION HARDENING — NEXT

## Status

```text
DB-U26
PROPOSED / OPEN

Database semantic redesign required
NO

Expected new database objects
0

Expected table/index/trigger/routine count changes
0
```

This is a PostgreSQL execution/security hardening layer, not a new Domain concept.

The new chat must **independently verify this candidate against current code + PostgreSQL security authority before freezing Part 18**.

## 18.1 SQL injection / query-construction doctrine

Freeze a strict baseline such as:

```text
business/user values
→ ALWAYS bind parameters

SQLAlchemy
→ Core/ORM expressions
→ or text() + named bind parameters

psycopg
→ execute(statement, params)

SQL identifiers
→ never arbitrary caller/user strings
→ static identifiers or bounded allow-list
→ psycopg.sql.Identifier / SQLAlchemy schema objects when dynamic identifier construction is genuinely required

f-string / %-format / string concatenation containing untrusted/business values
→ FORBIDDEN

caller-provided arbitrary SQL fragments
→ FORBIDDEN
```

For the 14 integrity functions:

```text
baseline dynamic EXECUTE = 0
known DANTE relations → static schema-qualified SQL
generic table/function names supplied as trigger/runtime arguments → FORBIDDEN
```

The DB schema is known in advance; there is no reason to create a generic dynamic SQL integrity engine.

## 18.2 Search-path / object-hijacking defense

Already-closed direction should be preserved and tested:

```text
runtime CREATE in dante        DENIED
runtime CREATE in public       DENIED
runtime CREATE TEMP TABLE      DENIED
runtime SET ROLE dante_owner   DENIED
runtime SET ROLE dante_migrator DENIED
runtime direct EXECUTE on integrity routines DENIED
PUBLIC EXECUTE on integrity routines          DENIED
```

Integrity routines already freeze bounded `search_path = pg_catalog, dante` / schema qualification posture. Verify the exact implementation contract and test it.

Do not allow a writable untrusted schema in an execution path where function/operator masking could redirect SQL resolution.

## 18.3 Credential/password handling hardening

Current CP3 provisioning builds safe SQL identifiers, but password handling should be independently inspected.

Candidate hardening from the security review:

```text
avoid password-bearing SQL statements where supported
use psycopg/libpq password-change capability rather than composing ALTER ROLE ... PASSWORD with a secret literal
password_encryption = scram-sha-256
MD5 password storage = forbidden
no password/DSN secret leakage to logs/errors
hide_parameters / redaction preserved
```

Before freezing this, the next chat must verify the exact psycopg 3 / libpq API available in the pinned stack and the exact PostgreSQL 18 semantics. Do not copy API names from conversation memory without verification.

## 18.4 Runtime/migrator/admin role pinning

Architecture says:

```text
application runtime DB role = dante_runtime
migration DB role           = dante_migrator
owner role                  = dante_owner / NOLOGIN
admin/bootstrap credential  = provisioning-only
```

Candidate security contract:

```text
runtime process MUST fail closed if configured with postgres/dante_owner/dante_migrator instead of dante_runtime
migration process MUST fail closed unless using dante_migrator as the login role before bounded SET ROLE
owner/admin credentials MUST NOT become normal application settings/runtime identity
```

Verify how settings/CLI/bootstrap currently separate these credentials before writing the final rule.

## 18.5 Logging / error / secret exposure

Audit/freeze:

```text
DB URLs/passwords never logged in clear
SQL parameter values not dumped in production exception logging merely for diagnostics
trigger DETAIL fields remain bounded and non-secret
no secret in migration messages
no secret in CI artifact/log output
no password in committed repo/config
```

Do not over-redact structural SQLSTATE/constraint/table diagnostics needed for operations.

## 18.6 Migration/privilege escalation negative proof

Add exact proof obligations to CP6-05:

```text
runtime cannot CREATE/ALTER/DROP schema objects
runtime cannot SET ROLE owner/migrator
runtime cannot grant itself privileges
runtime cannot execute integrity routines directly
PUBLIC cannot execute them
runtime cannot write base current-control tables directly
runtime cannot bypass view facet restrictions
runtime cannot use temp/public object hijacking path
migrator SET ROLE is bounded and required for migration ownership
P0/provisioning rerun cannot broaden M7 ACLs
```

## 18.7 SQL injection negative proof

Tests should prove safe construction boundaries instead of attempting an unrealistic global “SQL injection test”. At minimum:

```text
malicious string values remain data under bound parameters
quotes/semicolon/comment tokens cannot alter statement shape
arbitrary identifier/query fragment APIs do not exist at business boundary
bounded dynamic identifier path rejects non-allow-listed identifiers
PL/pgSQL integrity functions contain no dynamic EXECUTE baseline
```

Static/lint/code-review enforcement may complement runtime tests. Do not pretend one payload proves all injection classes.

## 18.8 Security scope separation

DATABASE SECURITY — CP6-03/04/05 relevant now:

```text
SQL query construction
injection resistance
DB roles/ACL
search_path
function/trigger execution
password/SCRAM handling
secret/log leakage
migration privilege escalation
real PostgreSQL negative proof
```

DEPLOYMENT SECURITY — staged before real production deployment, not invented here:

```text
TLS / verify-full or platform equivalent
CA/certificate strategy
private network/firewall/VPC exposure
managed PostgreSQL controls
secret manager + rotation
backup encryption / restore access control
PgBouncer production auth/TLS if activated
host hardening/patching
```

APPLICATION/API SECURITY — belongs to the first real vertical/application layers:

```text
AuthN
AuthZ
IDOR/BOLA
mass assignment
rate limiting
CSRF
CORS
SSRF
XSS
file upload validation
session/token/JWT security
selective disclosure and indirect-surface non-interference
```

Do not create API-security schema now just to check a box.

---

# 19. Proposed next write gate — Part 18

The user has already expressed the desire to close the database-security hardening before Gate 03, but the next chat must still verify live HEAD and candidate details before writing.

If repository state remains unchanged except for this handoff file, derive a fresh exact PRE-SCOPE from live branch.

Expected conceptual gate shape:

```text
BRANCH
feature/logical-postgresql

PRE-SCOPE
<EXACT LIVE HEAD AFTER THIS HANDOFF WRITE>

CREATE
docs/database/dante-postgresql-database-part-18.md

UPDATE
docs/database/README.md
docs/workstreams/logical-postgresql.md
docs/development/backend-cp6-03-live-handoff-2026-08-25.md
(optional old LIVE pointer only if explicitly justified and lossless)

DELETE
0

PURPOSE
Close DB-U26 — Database Security Execution Hardening.
Freeze injection-safe query-construction rules, bounded identifier policy,
no dynamic PL/pgSQL SQL baseline, search-path/object-hijack defense,
role identity fail-closed, credential/SCRAM/logging hardening,
and exact DB security proof obligations/staged deployment+API security boundaries.

EXPLICITLY OUT OF SCOPE
new tables/views/indexes/triggers/routines
Domain/Logical/Physical reopen
business Alembic migrations
SQLAlchemy business mappings
real GRANT/REVOKE/DDL execution
production network/TLS architecture finalization
application/API AuthN/AuthZ implementation
main realignment
CP6-04
```

Do not mark DB-U26 CLOSED until Part 18 is derived, audited, written, remotely read back and its diff is clean.

---

# 20. Final audit sequence after Part 18

After DB-U26 is clean, perform **one final independent replay over Parts 1–18**. It must not inherit PASS from earlier audits.

Replay at minimum:

```text
Domain 57/57
15 native owners
Whole Logical + WL-H01..WL-H12
accepted Physical PostgreSQL mapping
CP6-01 57 + non-57/cross-cutting coverage
CP6-02 full Constitution
Parts 1–18 complete supersession chain
final 68-table inventory
scoped families
MaterialState facets
PK/FK/UQ/CHECK manifest
95 indexes
14 routines
75 trigger attachments
5 views
current/history/lifecycle
Recurrence phase/range/selector semantics
Occurrence-generation membership/duplicate behavior
ACLs/history column grants
P0/M1/M7 security posture
SQLAlchemy mapping plan
advisory locks/concurrency
Dictionary schema/readiness
DBP-01..20 + DB-U26 security proof additions
real backend/provisioning/migration/test drift
security: injection construction, role escalation, search_path/object hijack, secrets
all tombstone/no-DDL supersessions
all staged evidence honesty
```

Final target:

```text
missing concept                      0
unclassified concept/family          0
unresolved DB-U                      0
Domain/Logical/Physical reopen        0
new accidental semantic root          0
generic semantic fallback             0
dangling scoped family                0
dangling MaterialState facet          0
contradictory supersession            0
missing structural constraint         0
missing lifecycle/history rule        0
missing ACL/security decision         0
missing index justification           0
SQL injection construction gap        0
privilege-escalation gap              0
search-path/object-hijack gap         0
credential/log secret-handling gap    0
backend/docs drift                    0
speculative schema                    0
```

If any real B/C appears, repair it and rerun the affected audit; do not grant Gate 03 by exhaustion.

---

# 21. Gate 03 closure behavior

Only after the Parts 1–18 final replay is clean may CP6-03 be marked:

```text
CP6-03
CLOSED / GATE 03 PASS
```

At that point explicitly tell the user:

```text
CP6-03 is complete.
The DANTE PostgreSQL database blueprint is closed.
The next action enters CP6-04 and starts REAL database materialization.
No business database object has been created yet.
A separate explicit CP6-04 materialization gate is required.
```

Do **not** silently continue into migrations.

A small durable Gate03 closure checkpoint/record may be appropriate after the final replay, using its own exact write gate.

---

# 22. CP6-04 preview — DO NOT EXECUTE YET

Once separately authorized, CP6-04 is where the project finally creates the real database:

```text
P0 provisioning/security hardening
Alembic M1..M7 business revisions
68 business/control tables
5 current views
95 indexes
120 CHECK constraints
68 FKs
14 integrity routines
75 triggers
exact DB-U21/Part17 ACLs
68 SQLAlchemy Row mappings
5 Core view handles
Database Dictionary object entries
```

Then CP6-05 runs the full real PostgreSQL QA/proof corpus.

No product application vertical belongs inside CP6-04/05 beyond database-level materialization/proof.

---

# 23. Security review context already established

The review leading to DB-U26 did **not** identify an already-exploitable business SQL injection in current code; there are no business query paths yet.

Positive current observations that should be reverified rather than blindly trusted:

```text
runtime foundation SQL is mostly static/controlled
PostgreSQL parameter hiding/logging posture exists
provisioning uses identifier-safe construction for dynamic role/schema identifiers
Ruff security S rules are enabled
CI actions are SHA-pinned / persist-credentials disabled / permissions bounded
Dependency Review / Dependabot exist
```

Security hardening is being added now to ensure future CP6-04/business code cannot weaken those boundaries.

Do not confuse “no business injection surface exists yet” with “security work is done”.

---

# 24. Technical baseline to preserve

Current intended stack at this phase:

```text
PostgreSQL 18 canonical family
current local/foundation patch 18.6
Python 3.14.x line
SQLAlchemy 2.0.x stable line
Alembic 1.x current pinned line
psycopg 3.x
PostGIS 3.6.4
pgvector 0.8.6
```

Do not upgrade to beta/pre-release technology merely for novelty. Verify actual pinned versions from `pyproject.toml`/lockfile when exact version matters.

Runtime session doctrine inherited from CP3/CP6-02:

```text
one AsyncEngine per process
one async_sessionmaker per process
one AsyncSession per application operation
autobegin=False
autoflush=True
expire_on_commit=False
outer operation owns commit/rollback
adapter may flush, never commit
READ COMMITTED default
stronger serialization only for proven invariants
no generic Repository/UoW/BaseService abstraction
```

---

# 25. Current main-divergence rule

At handoff preparation the feature branch is intentionally diverged from protected main.

Do not perform an opportunistic merge/rebase during DB-U26/audit work.

Before final integration:

```text
1. fetch current protected main;
2. review every main-only commit since merge base;
3. prove whether DB/backend/database authority changed;
4. derive an exact main-reconciliation gate;
5. use a genuine merge commit / protected workflow as required;
6. preserve CP6 canonical truth when reconciling shared status/routing docs;
7. verify behind_by=0 afterward.
```

The user explicitly wants main reconciliation later, not now.

---

# 26. What the next chat must NOT do

```text
DO NOT create business tables yet.
DO NOT create Alembic M1..M7 yet.
DO NOT implement SQLAlchemy business mappings yet.
DO NOT execute GRANT/REVOKE business ACLs yet.
DO NOT claim Gate 03 from the pre-security audit.
DO NOT merge main because it is behind/ahead.
DO NOT replace old canonical Parts with summaries.
DO NOT reopen Domain/Logical/Physical without concrete contradiction.
DO NOT add generic Account/Principal/Permission/Relationship/Entity tables.
DO NOT add RLS simply because security is being reviewed.
DO NOT add TLS/API/Auth schema merely to complete a security checklist.
DO NOT invent production deployment architecture without deployment context.
DO NOT claim CI PASS unless an actual qualifying run/status exists for the current HEAD.
```

---

# 27. Immediate resume checklist for the new chat

The fastest safe resume is:

```text
A. verify feature HEAD and read this entire handoff;
B. read docs/database/README.md and Part 17;
C. read Part 12 (ACL), Part 13 (DAG), Part 14 (mapping), Part 16 (implementation/proof hardening);
D. read CP6-02 SEC/TX/MIG/QA rules;
E. inspect current settings/runtime/provisioning/migration/test code;
F. verify proposed DB-U26 points against actual pinned psycopg/PostgreSQL behavior;
G. run a focused read-only security audit for additional PostgreSQL execution gaps;
H. if clean, state exact Part-18 write gate with live PRE-SCOPE;
I. freeze DB-U26 without changing database object counts;
J. remote-readback/diff QA;
K. rerun full Parts 1–18 tombstone + security audit from zero;
L. if zero blockers, derive/record Gate 03 closure;
M. STOP and ask/require separate explicit authorization before CP6-04.
```

---

# 28. User quality expectation

The user explicitly wants:

```text
professional / high-level / large-company standard
no yes-man acceptance
maximum non-speculative completeness
strong PostgreSQL integrity
serious naming/ACL/security discipline
thorough audits before materialization
clear documentation so another AI/engineer can resume
```

If the next chat finds a real defect, surface it and repair it. Do not force a clean verdict merely because CP6-03 has taken a long time.

Conversely, do not keep CP6-03 open by inventing endless theoretical future requirements. Security/deployment/application concerns that have no current database implementation subject must be explicitly staged to the correct future phase.

---

# 29. Current one-line resume

```text
DANTE CP6-03 is semantically/database-design clean through repaired Part 17 at HEAD 7c465d5f..., but Gate 03 is intentionally held for one final database-execution security hardening (candidate DB-U26 / Part 18), followed by a fresh independent Parts 1–18 tombstone+security replay. No real business PostgreSQL schema has been materialized yet.
```
