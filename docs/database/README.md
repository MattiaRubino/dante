# DANTE Database System of Record

- **Status:** CURRENT / CP6 BASELINE CLOSED IN `main` / M3 ACCESS-AUTH DB EVOLUTION CLOSED + PROVEN ON BRANCH
- **Scope:** DANTE PostgreSQL architecture, Dictionary, mappings, migrations, human current reference, direct proof and documentation consistency
- **PostgreSQL:** 18.6
- **Current branch Alembic head:** `20260827_10`
- **Protected-main CP6 baseline head:** `20260826_08`
- **Current Access/Auth DB reference:** `access-auth.md`
- **Current workstream:** `../workstreams/access-auth.md`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Architecture decision:** `../decisions/ADR-010-postgresql-persistence-constitution.md`
- **Final CP6 acceptance:** `../development/backend-cp6-05-whole-database-qa.md`

## 1. Purpose

This directory is the durable entry point for understanding the DANTE database itself.

A developer must be able to answer:

```text
what database objects exist?
why does each object exist?
what does every persisted field mean?
how are objects related?
what integrity does PostgreSQL enforce?
what is canonical vs provider/derived/technical state?
what migration created or changed an object?
what SQLAlchemy mapping represents it?
what tests prove it?
what remains intentionally unmaterialized and why?
```

This documentation does not replace Domain, Logical, Physical or the PostgreSQL Persistence Constitution. It is the **current operational/structural database reference produced from them**.

---

## 2. Protected-main baseline and current branch

Protected-main CP6 baseline:

```text
PostgreSQL          18.6
Alembic             20260826_08
tables              68
views                5
routines             14
triggers             75
physical indexes     95
foreign keys         68
CHECK constraints    120
standalone entries   87
```

Current `feature/access-auth` materialization after closed M3:

```text
PostgreSQL          18.6
Alembic             20260827_10
tables              72
views                5
routines             15
triggers             75
physical indexes     104
foreign keys         71
CHECK constraints    137
standalone entries   92
```

M3 forward evolution:

```text
20260827_09
→ account
→ email_identity
→ password_credential
→ auth_session

20260827_10
→ dante.acquire_account_security_lock(uuid)
```

These branch-local objects remain unmerged until the user explicitly gates integration to protected `main`.

---

## 3. Current authority model

```text
closed Domain / Logical / Physical
→ semantic and architectural source

Persistence Constitution + ADR-010
→ reusable PostgreSQL doctrine

Alembic
→ schema evolution authority

SQLAlchemy mappings
→ application representation

real PostgreSQL introspection
→ observed materialization

Database Architecture & Reference
→ human current database meaning

Database Dictionary
→ structured current object metadata

generated reference / diagrams
→ derived structural views

direct tests
→ executable proof
```

A mismatch is a defect. Do not choose whichever representation is convenient.

Permanent consistency invariant:

```text
Database current reference
≈ Database Dictionary
≈ SQLAlchemy mappings
≈ Alembic head
≈ real PostgreSQL
≈ direct tests
```

Historical acceptance such as CP6 remains exact to its historical revision; current references must still evolve when a later accepted product migration changes current truth.

---

## 4. Current directory roles

```text
docs/database/
├── README.md                         # this authority/lifecycle entry point
├── access-auth.md                    # current Access/Auth DB module
├── dante-postgresql-database.md      # whole-DB current/evolving reference, part 1
├── dante-postgresql-database-part-2.md
├── ...
├── dante-postgresql-database-part-19.md
├── dictionary/
│   ├── README.md
│   ├── scope.json
│   ├── schema/
│   ├── tables/
│   ├── views/
│   └── routines/
├── generated/
├── diagrams/
└── evolution/
```

The multi-part whole-DB blueprint originated during CP6 but is a **current/evolving reference**, not frozen history. Historical CP6 rationale may remain where useful; current status/inventory/open-item statements must be reconciled when their trigger fires.

Subject modules such as `access-auth.md` are detailed parts of the same System of Record, not detached amendment diaries.

---

## 5. Dictionary contract

Every materialized DANTE table/view/routine has structured current metadata. Table-owned FK/CHECK/index/trigger data remains under the owning object where the Dictionary schema defines it.

The Dictionary records, where applicable:

```text
identity / object type / purpose
semantic role and source
introducing migration + stage
SQLAlchemy mapping
columns/types/nullability/defaults
PK/FK/UQ/CHECK relationships
indexes + reason
history/current-state semantics
lifecycle
runtime privilege posture
proof/test traceability
```

Post-CP6 entries identify their actual introducing stage rather than pretending to belong to CP6.

`dictionary/scope.json` deliberately separates:

```text
expected_baseline
→ immutable CP6 closure benchmark

current_materialization
→ current evolving branch inventory
```

---

## 6. Same-change database rule

A structural DB change is incomplete unless the same reviewed slice updates all affected current representations:

```text
semantic/security contract
→ Alembic forward migration
→ SQLAlchemy mapping/metadata
→ mapping registry when applicable
→ Database Dictionary
→ whole-DB current reference
→ subject DB reference when applicable
→ direct tests
→ real PostgreSQL proof
→ workstream/status docs when milestone state changes
```

The same change must audit prior current-reference claims such as:

```text
DEFERRED
OPEN
TBD
NOT MATERIALIZED
```

when the new capability satisfies their trigger.

A resolved item becomes either:

```text
RESOLVED / MATERIALIZED
or
RESOLVED WITHOUT MATERIALIZATION
```

Historical rationale may remain, but current reference text must not pretend the item is still open.

---

## 7. DANTE-specific non-collapse rules

Database documentation and implementation must keep these boundaries explicit:

```text
technical address anchor != semantic Entity/Thing
technical material-state control != universal Fact/Version owner
NativeRef != ScopedRecordRef != MaterialStateRef != ExternalRef
current accepted state != newest inserted row
material history != universal event sourcing
provider state != canonical DANTE state
derived/search state != canonical DANTE truth
Person != Account != Principal != Actor
AuthSession != DANTE Session
Authority != AuthZ decision
absence/unknown != explicit negative
idempotency != semantic identity
```

Do not introduce generic relational escape hatches to avoid closing actual semantics.

---

## 8. Security/role baseline

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
```

CP6 proves the baseline role topology and runtime posture.

M3 adds exact Auth ACLs plus one narrow runtime function:

```text
dante.acquire_account_security_lock(uuid)
SECURITY DEFINER
owner dante_owner
exact trusted search_path
PUBLIC EXECUTE denied
dante_migrator EXECUTE denied
dante_runtime EXECUTE granted
runtime Account UPDATE denied
runtime direct Account FOR UPDATE denied
```

Do not widen Account UPDATE merely to obtain a row lock.

---

## 9. M3 database proof

Direct real PostgreSQL evidence:

```text
Alembic head                                         20260827_10
current topology                                     72 tables / 5 views / 15 routines
Dictionary standalone entries                       92
real PostgreSQL marked suite                        83 / 83 PASS
real Auth signin/session integration                4 / 4 PASS
migration round-trip / Alembic drift                PASS
CP6 historical catalog regression                   PASS
Dictionary ≈ SQLAlchemy ≈ Alembic ≈ live PG        PASS
exact Auth ACL                                      PASS
Account security-definer lock                       PASS
runtime direct Account FOR UPDATE denied            PASS
transaction-scoped competing-lock proof             PASS
runtime recovery / transaction suites               PASS
```

The real browser harness then proved this DB-backed Auth path through production Web/FastAPI:

```text
7 scenarios × Chromium / Firefox / WebKit
21 / 21 PASS
```

Database-sensitive browser cases include real session creation/logout, independent sessions, server-side revoke, server-side expiry and actual temporary PostgreSQL outage.

M3 database status:

```text
MATERIALIZED + CURRENT + DIRECTLY PROVEN + M3 CLOSED
```

---

## 10. Current Access/Auth DB routing

Detailed Auth persistence meaning is in `access-auth.md`.

Current topology:

```text
Account
├── EmailIdentity
├── 0..1 PasswordCredential
└── 0..N AuthSession

security capability
└── acquire_account_security_lock(uuid)
```

Current intentionally absent later-slice structures:

```text
ExternalIdentity
PasskeyCredential
verification/recovery proof persistence
provider transaction state
MFA/TOTP/recovery-code persistence
Principal table
```

M4/M5 may materialize only the minimal structures justified by their accepted contracts.

---

## 11. Former deferrals reconciled by M3

```text
DB-U09 Account persistence
→ CP6: correctly deferred
→ M3: RESOLVED / MATERIALIZED

DB-U10 Principal/security persistence
→ CP6: correctly deferred
→ M2/M3: RESOLVED WITHOUT PERSISTENCE
→ runtime Principal only
```

Do not collapse Account into Person or Principal merely because the persistence now exists.

---

## 12. Automated QA obligations

Current/future DB QA must detect:

```text
undocumented real object
stale Dictionary object
column/type/nullability/default drift
PK/FK/UQ/CHECK/index drift
trigger/routine/view drift
SQLAlchemy-vs-Alembic drift
migration head mismatch
owner/ACL drift
stale current-reference deferral after trigger satisfaction
```

Generated artifacts may cover structural facts; semantic meaning/rationale remains human-reviewed.

---

## 13. M4 forward rule

M3 database work is closed. M4 must not start from “what tables do auth systems usually have?”.

Correct sequence:

```text
close exact signup/verification/recovery/reset/reauth semantics
→ identify persistence pressure
→ design single-use/replay/race constraints
→ forward migration
→ mapping + Dictionary + references
→ real PostgreSQL proof
→ API/client/Web proof
```

No speculative generic token table, no parallel Account root and no broad privilege expansion.

---

## 14. Navigation

```text
docs/database/README.md
→ authority/lifecycle/current inventory

docs/database/dante-postgresql-database.md + parts 2–19
→ whole-DB current/evolving human reference

docs/database/access-auth.md
→ current detailed Auth persistence

docs/database/dictionary/
→ machine current reference

docs/development/backend-cp6-05-whole-database-qa.md
→ historical CP6 acceptance evidence
```
