# DANTE Database System of Record

- **Status:** CURRENT / CP6 BASELINE CLOSED IN `main` / M3 DB CLOSED + PROVEN / M4 DB SOURCE CANDIDATE ACTIVE
- **Scope:** DANTE PostgreSQL architecture, Dictionary, mappings, migrations, human current reference, direct proof and documentation consistency
- **PostgreSQL:** 18.6
- **Current branch Alembic head in source:** `20260829_11`
- **Accepted M3 head:** `20260827_10`
- **Protected-main CP6 baseline head:** `20260826_08`
- **Current Access/Auth DB reference:** `access-auth.md`
- **Current live handoff:** `../workstreams/access-auth-m4-live-handoff-2026-08-29.md`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Architecture decision:** `../decisions/ADR-010-postgresql-persistence-constitution.md`

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

Current-reference documentation evolves with branch truth. Historical CP6/M3 evidence remains historical and is never rewritten to impersonate later state.

---

## 2. Protected-main baseline / accepted M3 / current M4 source target

Protected-main CP6 baseline:

```text
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

Accepted M3 Access/Auth baseline:

```text
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

Current M4 branch source/catalog target:

```text
Alembic             20260829_11
tables              74
views                5
routines             15
triggers             75
physical indexes     113
foreign keys         72
CHECK constraints    149
standalone entries   94
```

Evidence rule:

```text
source/Dictionary/migration target
!= accepted observed PostgreSQL PASS
```

The M4 counts above become accepted observed truth only after the canonical real PostgreSQL/current-catalog run passes.

---

## 3. Current authority model

```text
closed Domain / Logical / Physical
→ semantic and architectural source

Persistence Constitution + ADR-010
→ PostgreSQL doctrine

Alembic
→ schema evolution authority

SQLAlchemy mappings
→ application representation

Database Dictionary
→ structured current object metadata

human current DB references
→ current semantic/operational meaning

real PostgreSQL introspection + direct tests
→ observed executable proof
```

A mismatch is a defect.

Permanent invariant:

```text
Database current reference
≈ Database Dictionary
≈ SQLAlchemy mappings
≈ Alembic head
≈ real PostgreSQL
≈ direct tests
```

---

## 4. Current Access/Auth evolution

M3 materialized and proved:

```text
20260827_09
→ account
→ email_identity
→ password_credential
→ auth_session

20260827_10
→ dante.acquire_account_security_lock(uuid)
```

M4 current source evolution:

```text
20260829_11
→ password_signup_challenge
→ password_recovery_challenge
→ exact EmailIdentity↔Account composite recovery binding
→ narrow runtime ACL delta for verified account establishment
→ narrow AuthSession reauth update capability
```

M4 does not add a generic token/proof god-table.

Detailed semantics:

```text
docs/database/access-auth.md
```

---

## 5. Same-change database rule

A structural DB change is incomplete unless the same reviewed slice updates all affected current representations:

```text
semantic/security contract
→ Alembic forward migration
→ SQLAlchemy mapping/metadata
→ mapping registry when applicable
→ Database Dictionary
→ whole-DB current reference
→ subject DB reference
→ direct tests
→ real PostgreSQL proof
→ workstream/status docs when milestone state changes
```

Historical migrations are immutable evidence.

The same change must audit stale current claims such as:

```text
DEFERRED
OPEN
TBD
NOT MATERIALIZED
```

when their trigger is satisfied.

---

## 6. Dictionary contract

Every materialized DANTE table/view/routine has structured current metadata.

The Dictionary records, where applicable:

```text
object identity / type / purpose
semantic role/source
introducing migration + stage
current runtime ACL stage
SQLAlchemy mapping
columns/types/nullability/defaults
PK/FK/UQ/CHECK
indexes + reason
lifecycle/current-state semantics
security/ownership
proof/test traceability
```

`dictionary/scope.json` separates immutable historical baselines from current materialization.

M3 objects keep their original introducing stage even when M4 legitimately evolves their current ACL stage.

---

## 7. Security / role posture

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
```

M3 security capability remains:

```text
dante.acquire_account_security_lock(uuid)
SECURITY DEFINER
owner dante_owner
trusted exact search_path
PUBLIC EXECUTE denied
dante_migrator EXECUTE denied
dante_runtime EXECUTE granted
broad Account UPDATE denied
runtime direct Account FOR UPDATE denied
```

M4 adds only narrow reviewed privileges required by its exact contract:

```text
column-bounded Account INSERT
column-bounded EmailIdentity INSERT
column-bounded PasswordCredential INSERT
narrow AuthSession secret/recent-auth/expiry UPDATE
purpose-specific challenge-table operational ACL
```

Do not widen Account/Auth tables for convenience.

---

## 8. M3 accepted database proof

```text
Alembic head                                         20260827_10
real PostgreSQL marked suite                        83 / 83 PASS
real Auth signin/session integration                4 / 4 PASS
migration round-trip / Alembic drift                PASS
CP6 historical catalog regression                   PASS
Dictionary ≈ SQLAlchemy ≈ Alembic ≈ live PG        PASS
exact Auth ACL                                      PASS
Account security-definer lock                       PASS
runtime direct Account FOR UPDATE denied            PASS
browser full-stack DB-backed proof                  21 / 21 PASS
```

M3 database status remains:

```text
MATERIALIZED + PROVEN + CLOSED
```

---

## 9. M4 current database evidence state

M4 test code now exists for:

```text
current catalog / ACL
signup pre-verification non-materialization
verified Account establishment
existing-email collision non-overwrite
recovery supersession
single-use reset
all-session revocation
replacement password validity
same-session reauth
exact bearer rotation
stale bearer rejection
```

At this live checkpoint:

```text
M4 schema/mappings/Dictionary       MATERIALIZED IN SOURCE
M4 real PostgreSQL acceptance       PENDING CANONICAL EXECUTION
M4 browser DB-backed acceptance     PENDING
M4 DB closure                        NOT CLOSED
```

`TEST CODE EXISTS != TEST EXECUTION PASS`.

---

## 10. DANTE-specific non-collapse rules

```text
technical address anchor != semantic Entity/Thing
current accepted state != newest inserted row
provider state != canonical DANTE state
Person != Account != Principal != Actor
AuthSession != DANTE Session
Authority != AuthZ decision
absence/unknown != explicit negative
idempotency != semantic identity
```

Do not introduce generic relational escape hatches to avoid closing actual semantics.

---

## 11. Current directory roles

```text
docs/database/
├── README.md
├── access-auth.md
├── dante-postgresql-database.md + continuations
├── dictionary/
├── generated/
├── diagrams/
└── evolution/
```

Subject modules such as `access-auth.md` are parts of the same System of Record, not detached amendment diaries.

---

## 12. Forward Auth persistence boundary

M4 may materialize only its accepted signup/recovery lifecycle objects.

Still deferred to later explicit contracts:

```text
ExternalIdentity
PasskeyCredential
provider transaction/challenge state
TOTP/MFA/recovery-code persistence
Principal table
Account ↔ Person convenience relation
```

Correct future sequence:

```text
exact semantic/security contract
→ minimal migration
→ mapping
→ Dictionary
→ human current reference
→ direct real PostgreSQL proof
```

No speculative generic token table and no parallel Account/security root.

---

## 13. Navigation

```text
docs/database/access-auth.md
→ current detailed Access/Auth persistence

docs/workstreams/access-auth-m4-live-handoff-2026-08-29.md
→ current M4 continuation/evidence state

docs/database/dictionary/
→ structured machine current reference

docs/database/dante-postgresql-database.md + parts
→ whole-DB current/evolving human reference
```
