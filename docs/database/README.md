# DANTE Database System of Record

- **Status:** CURRENT / CP6 BASELINE CLOSED IN `main` / M3–M4 DB CLOSED / M5-A DB MATERIALIZED + REAL POSTGRESQL PROVEN
- **Scope:** DANTE PostgreSQL architecture, Dictionary, mappings, migrations, human current reference, direct proof and documentation consistency
- **PostgreSQL:** 18.6
- **Current accepted branch Alembic head:** `20260830_12`
- **Accepted M5-A implementation checkpoint:** `7e40e02d301b0812b3f55e0d9d4ce6439e420b2a`
- **Accepted M4 baseline head:** `20260829_11`
- **Accepted M3 head:** `20260827_10`
- **Protected-main CP6 baseline head:** `20260826_08`
- **Current Access/Auth DB reference:** `access-auth.md`
- **Current live handoff:** `../workstreams/access-auth-m5-live-handoff-2026-08-29.md`
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

Current-reference documentation evolves with branch truth. Historical CP6/M3/M4 evidence remains historical and is never rewritten to impersonate later state.

---

## 2. Accepted baseline progression

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

Accepted M4 Access/Auth baseline:

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

Accepted current M5-A branch truth:

```text
PostgreSQL          18.6
Alembic             20260830_12
tables              83
views                5
routines             15
triggers             75
physical indexes     156
foreign keys         85
CHECK constraints    233
standalone entries   103
```

The M5-A counts are **observed PostgreSQL truth**, reconciled against the Dictionary, SQLAlchemy and Alembic. They are no longer source-only targets.

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

## 4. Access/Auth evolution

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

M4 materialized and proved:

```text
20260829_11
→ password_signup_challenge
→ password_recovery_challenge
→ exact EmailIdentity↔Account composite recovery binding
→ narrow runtime ACL delta for verified account establishment
→ narrow AuthSession reauth update capability
```

M5-A materialized and proved:

```text
20260830_12
→ EmailIdentity recovery-restriction state
→ external_identity
→ external_auth_transaction
→ external_link_challenge
→ external_signup_challenge
→ account_profile_bootstrap
→ apple_auth_grant
→ webauthn_account
→ passkey_credential
→ webauthn_challenge
→ exact Apple/WebAuthn composite bindings
→ least-privilege runtime ACL
```

No generic token/proof god-table was introduced.

Detailed semantics:

```text
docs/database/access-auth.md
```

---

## 5. M5-A physical hardening accepted during implementation

The physical implementation preserved the M5.2 semantic contract while strengthening database-enforced exact ownership/lifecycle invariants:

```text
ExternalIdentity
→ composite UQ(external_identity_ref, issuer, subject)
→ exact target for Apple grant binding

AppleAuthGrant
→ exact ExternalIdentity issuer+subject binding
→ pending unbound lifecycle retained for abandoned-flow revocation

ExternalLinkChallenge / ExternalSignupChallenge
→ exact Apple grant issuer+subject binding

AuthSession
→ composite UQ(auth_session_ref, account_ref)

WebAuthnAccount
→ composite UQ(account_ref, user_handle)

WebAuthnChallenge
→ exact Account+AuthSession ownership
→ exact Account+userHandle ownership

PasskeyCredential
→ account_ref references WebAuthnAccount ownership
→ explicit cose_algorithm
→ logical active/revoked lifecycle
→ lifetime credential_id uniqueness retained
→ backup_state=true requires backup_eligible=true

cleanup
→ account_profile_bootstrap(expires_at)
→ apple_auth_grant(pending_expires_at)

EmailIdentity ACL
→ INSERT remains column-scoped and now includes the two new nullable recovery columns
→ UPDATE remains limited to recovery_restriction_code / recovery_restriction_observed_at
```

PostgreSQL identifier-limit shortening accepted consistently:

```text
fk_external_link_challenge_apple_grant
fk_external_signup_challenge_apple_grant
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

## 7. Dictionary contract

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

M3/M4 objects keep their original introducing stage even when later stages legitimately evolve current ACL/constraints.

---

## 8. Security / role posture

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
```

Permanent security capability:

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

Access/Auth runtime grants remain least privilege and column-bounded where broad table write authority is not required.

M5-A explicitly preserves:

```text
no runtime DELETE of durable ExternalIdentity
no runtime DELETE of durable PasskeyCredential
no broad EmailIdentity INSERT/UPDATE
no runtime network/provider authority encoded into PostgreSQL grants
```

---

## 9. Accepted M5-A database proof

```text
uv lock                                      PASS
Ruff format / lint                           PASS
mypy strict                                  PASS
backend fast                                 87 / 87 PASS
real PostgreSQL 18.6                         95 / 95 PASS
M5 persistence tests                          8 / 8 PASS
migration previous-head → head                PASS
fresh DB → head                               PASS
migration head/base/head                      PASS
single Alembic head                           PASS
Alembic autogenerate drift                    PASS
CP6 historical regressions                    PASS
M3/M4 Auth DB regressions                     PASS
Dictionary ≈ SQLAlchemy ≈ Alembic ≈ PG       PASS
exact Auth runtime ACL                        PASS
negative constraint cases                     PASS
backend build                                 PASS
```

M5-A database status:

```text
MATERIALIZED + REAL POSTGRESQL PROVEN + COMPLETE
```

This persistence proof does not claim later Google/Apple/WebAuthn runtime, public API, generated-client or browser/provider acceptance.

---

## 10. DANTE-specific non-collapse rules

```text
technical address anchor != semantic Entity/Thing
current accepted state != newest inserted row
provider state != canonical DANTE state
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != ExternalIdentity
provider email != provider identity key
provider authentication != provider-data integration authorization
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

M5-A has materialized the accepted multi-authenticator persistence foundation.

Next runtime/infrastructure work is bounded by M5-B and later M5 slices.

Still deferred unless separately authorized:

```text
TOTP / generic MFA / recovery-code persistence
Principal table
Account ↔ Person convenience relation
provider-data integration grants for Gmail/Calendar/iCloud
whole-vertical security-event/observability persistence owned by M7
```

Correct forward sequence remains:

```text
exact semantic/security contract
→ minimal migration/runtime delta
→ mapping/Dictionary where structural
→ human current reference
→ direct proof at the truthful boundary
```

---

## 13. Navigation

```text
docs/database/access-auth.md
→ current detailed Access/Auth persistence

docs/workstreams/access-auth-m5-live-handoff-2026-08-29.md
→ current M5 continuation/evidence state

docs/database/dictionary/
→ structured machine current reference

docs/database/dante-postgresql-database.md + parts
→ whole-DB current/evolving human reference
```
