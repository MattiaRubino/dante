# DANTE Access/Auth Database Reference

- **Status:** CURRENT / BRANCH-LOCAL / M3 CLOSED / DATABASE SPINE MATERIALIZED + PROVEN
- **Branch:** `feature/access-auth`
- **Current Alembic head on this branch:** `20260827_10`
- **Protected-main CP6 baseline:** `20260826_08`
- **Whole-DB current reference:** `dante-postgresql-database.md` + continuations
- **Database system-of-record authority:** `README.md`
- **Architecture authority:** `../architecture/access-auth-architecture.md`
- **Security authority:** `../architecture/access-auth-security-contract.md`
- **Persistence doctrine:** `../development/backend-cp6-02-postgresql-persistence-constitution.md`
- **Current workstream:** `../workstreams/access-auth.md`

## 1. Purpose

This document is the detailed current Access/Auth module of the DANTE Database System of Record. It does not replace the whole-DB reference. The whole-DB reference owns global topology and current whole-database reconciliation; this file owns the detailed meaning of Access/Auth persistence introduced by M3 and the bounded account-security lock capability used by the production signin/session spine.

Authority relationship:

```text
docs/database/README.md
→ Database System of Record / lifecycle

whole-DB current/evolving reference
→ global topology and current inventory

this file
→ Access/Auth object semantics and DB proof

Dictionary + SQLAlchemy + Alembic + real PostgreSQL + tests
→ machine/executable/observed representations
```

Historical CP6 deferrals remain valid history, but they are no longer current unresolved truth:

```text
DB-U09 Account persistence
→ RESOLVED / MATERIALIZED

DB-U10 Principal/security persistence
→ RESOLVED WITHOUT PERSISTENCE
```

`Person != Account != Principal != Actor` and `AuthSession != dante.session` remain mandatory.

---

## 2. Current M3 topology

```text
Account
├── EmailIdentity
├── 0..1 PasswordCredential
└── 0..N AuthSession

bounded DB capability
└── acquire_account_security_lock(uuid)
```

Current branch inventory:

```text
PostgreSQL          18.6
Alembic             20260827_10
72 tables
5 views
15 routines
75 triggers
104 physical indexes
71 foreign keys
137 CHECK constraints
92 standalone Dictionary entries
```

Not materialized by M3:

```text
ExternalIdentity
PasskeyCredential
verification/recovery proof persistence
provider state
TOTP / MFA / recovery codes
Principal table
Account ↔ Person convenience relation
```

Those are not omissions in M3. They belong to later gated slices if their semantics require persistence.

---

## 3. `dante.account`

Role: durable Access/security lifecycle root.

Columns:

```text
account_ref   uuid        PK, UUIDv7
status_code   text        active | disabled
created_at    timestamptz finite
disabled_at   timestamptz nullable
```

Integrity:

```text
active   → disabled_at IS NULL
disabled → disabled_at finite and >= created_at
```

The table intentionally contains no email, password verifier, provider identifier, Person/profile payload, device identity or global role.

Current runtime ACL:

```text
SELECT  yes
INSERT  no
UPDATE  no
DELETE  no
```

The runtime cannot acquire the required security row lock through direct `SELECT ... FOR UPDATE`, because PostgreSQL requires corresponding UPDATE privilege. M3 deliberately keeps Account UPDATE denied and exposes only the narrow database-owned `dante.acquire_account_security_lock(uuid)` function for transaction-scoped account-security serialization.

Later Account creation/disable/change operations must receive their own narrow reviewed capabilities; do not widen Account UPDATE merely for convenience.

---

## 4. `dante.email_identity`

Role: canonical DANTE email identity representation for an Account.

Columns:

```text
email_identity_ref uuid        PK, UUIDv7
account_ref        uuid        FK → account
address            text        normalized delivery/display form
comparison_key     text        UNIQUE canonical lookup key
created_at         timestamptz finite
verified_at        timestamptz nullable, finite and >= created_at
```

Application normalization/comparison:

```text
local comparison  NFC + Unicode casefold
domain comparison UTS #46 / IDNA canonical ASCII lowercase
```

`address` and `comparison_key` are deliberately separate. PostgreSQL remains the final concurrency arbiter through `uq_email_identity_comparison_key`.

Explicit index:

```text
ix_email_identity_account_ref(account_ref)
```

Current runtime ACL is SELECT only. M4 signup/verification/email-lifecycle work must add mutation capability only through its exact accepted contract.

---

## 5. `dante.password_credential`

Role: optional current password credential for an Account.

Columns:

```text
password_credential_ref uuid        PK, UUIDv7
account_ref             uuid        FK → account, UNIQUE
verifier                text        Argon2id encoded verifier
pepper_key_id           text        non-secret external pepper-key identifier
created_at              timestamptz finite
updated_at              timestamptz finite and >= created_at
```

`UNIQUE(account_ref)` enforces `Account → 0..1 current PasswordCredential`.

The verifier shape check is database defense; exact security parameters remain application policy:

```text
Argon2id v19
memory 64 MiB
time cost 3
parallelism 4
separate HMAC-SHA256 pepper
```

Never persisted:

```text
raw password
normalized password bytes
pepper secret
HIBP protocol material
```

Current runtime ACL:

```text
SELECT                                      yes
UPDATE verifier, pepper_key_id, updated_at  yes
INSERT                                      no
DELETE                                      no
```

The narrow UPDATE exists only for authenticated verifier upgrade/rehash after authoritative stale-credential revalidation. Runtime cannot change Account binding or credential identity.

---

## 6. `dante.auth_session`

Role: one independent server-authoritative authentication session for one Account.

Columns:

```text
auth_session_ref       uuid        PK, UUIDv7; non-secret correlation identity
account_ref            uuid        FK → account
secret_verifier        bytea       UNIQUE, exactly 32 bytes
created_at             timestamptz
authenticated_at       timestamptz
recent_auth_at         timestamptz
last_user_activity_at  timestamptz
expires_at             timestamptz
revoked_at             timestamptz nullable
revocation_reason_code text        nullable
```

`secret_verifier` stores SHA-256 of the CSPRNG session secret. The raw bearer secret is never stored in PostgreSQL and is emitted to the browser only after durable commit or safe ambiguous-outcome reconciliation.

Current usability is derived:

```text
not revoked
AND overall expiry not reached
AND inactivity expiry not reached
AND owning Account is active
```

No mutable `EXPIRED` flag is persisted.

Indexes:

```text
uq_auth_session_secret_verifier(secret_verifier)
ix_auth_session_account_ref(account_ref)
```

Current runtime ACL:

```text
SELECT                                                   yes
INSERT                                                   yes
UPDATE last_user_activity_at, revoked_at,
       revocation_reason_code                            yes
UPDATE secret/account/session identity or auth timestamps no
DELETE                                                   no
```

Current logout is terminal revocation, not physical deletion.

---

## 7. Foreign-key/deletion posture

M3 adds exactly three Auth foreign keys:

```text
email_identity.account_ref       → account.account_ref
password_credential.account_ref  → account.account_ref
auth_session.account_ref         → account.account_ref
```

All use `NO ACTION` update/delete behavior. Security identity/session state is not cascade-deleted implicitly.

No current runtime DELETE exists on the Auth tables.

---

## 8. Account security lock

Migration `20260827_10_m3_auth_security_lock.py` introduces:

```text
dante.acquire_account_security_lock(uuid)
SECURITY DEFINER
owner dante_owner
trusted exact search_path
VOLATILE
PARALLEL UNSAFE
not leakproof
```

Privilege posture:

```text
PUBLIC EXECUTE           no
dante_migrator EXECUTE   no
dante_runtime EXECUTE    yes
Account UPDATE runtime   no
direct FOR UPDATE runtime no
```

The function takes the canonical Account row lock inside the caller's existing transaction and returns no authority beyond the lock operation.

Real two-connection proof verifies:

```text
runtime direct FOR UPDATE          denied / 42501
security function acquires lock    yes
competing NOWAIT lock              blocked / 55P03
rollback releases lock             yes
```

Do not replace this with advisory Account locks or broad Account UPDATE grants.

---

## 9. Signin transaction relationship

M3 signin intentionally keeps expensive work outside the authoritative mutation transaction:

```text
read EmailIdentity / Account / PasswordCredential snapshot
→ Argon2 + HIBP outside DB transaction
→ BEGIN
→ acquire_account_security_lock(account_ref)
→ re-read Account + current credential
→ prove authenticated evidence is still current
→ optional narrow verifier rehash
→ insert AuthSession
→ COMMIT
→ reconcile ambiguous outcome if necessary
→ only then issue raw session secret
```

Rules:

```text
READ COMMITTED default
Account row = serialization point for account-wide security mutation
no hidden commit
no blind ambiguous-commit retry
no network/human wait inside DB transaction
two valid concurrent signins may create two independent sessions
```

Normal session admission is a read path and does not lock Account merely to authenticate a request.

---

## 10. Migration / mapping / Dictionary traceability

Migrations:

```text
20260827_09_m3_auth_signin_spine.py
→ account / email_identity / password_credential / auth_session

20260827_10_m3_auth_security_lock.py
→ acquire_account_security_lock(uuid)
```

SQLAlchemy:

```text
dante.platform.database.mappings.auth
├── AccountRow
├── EmailIdentityRow
├── PasswordCredentialRow
└── AuthSessionRow
```

Dictionary:

```text
dictionary/tables/account.json
dictionary/tables/email_identity.json
dictionary/tables/password_credential.json
dictionary/tables/auth_session.json
dictionary/routines/acquire_account_security_lock.json
```

The post-CP6 Dictionary schema supports truthful later `introducing_stage`/`runtime_acl_stage` values instead of pretending later product objects belonged to CP6.

---

## 11. Protected-main baseline vs current branch

```text
                         CP6 baseline   M3 branch current
tables                   68             72
views                     5              5
routines                  14             15
standalone entries        87             92
triggers                  75             75
physical indexes          95             104
foreign keys              68             71
CHECK constraints         120            137
Alembic                   20260826_08    20260827_10
```

`dictionary/scope.json` keeps CP6 `expected_baseline` separate from current materialization. Later product evolution must not rewrite historical CP6 acceptance counts.

---

## 12. Former whole-DB deferrals

```text
DB-U09 — Account persistence
CP6:
→ correctly DEFERRED while Access/Auth semantics were open.

Current:
→ RESOLVED / MATERIALIZED.
→ account + email_identity + password_credential + auth_session.

DB-U10 — Principal/security persistence
CP6:
→ correctly DEFERRED.

Current:
→ RESOLVED WITHOUT PERSISTENCE.
→ Principal is runtime-derived from Account + AuthSession + request/security context.
```

These resolutions preserve `Person != Account != Principal != Actor` and do not retroactively invalidate CP6.

---

## 13. Direct proof

Real PostgreSQL execution completed for the M3 backend/database spine:

```text
real PostgreSQL marked suite                                         83 / 83 PASS
real signin/session API integration                                   4 / 4 PASS
CP6 historical regression                                             PASS
current catalog / Auth ACL / Account security lock                    PASS
migration fresh-head / round-trip / Alembic drift                     PASS
privilege / runtime / transaction suites                              PASS
Dictionary ≈ SQLAlchemy ≈ Alembic ≈ live PostgreSQL                   PASS
```

The cross-stack browser harness later proved the same canonical database behavior through the real production Web/FastAPI path:

```text
Chromium / Firefox / WebKit
7 scenarios each
21 / 21 PASS
```

Database-sensitive browser cases include:

```text
real AuthSession creation/bootstrap/logout
independent sessions
server-side AuthSession revoke
server-side AuthSession expiry
disposable PostgreSQL actually stopped → service-unavailable/no fake auth → restart
real process signin rate limiter → 429/no fake auth
```

The E2E fault-control utility is test support only and does not add public test endpoints to FastAPI.

---

## 14. M3 closure boundary

Database verdict for M3:

```text
M3 Auth persistence              MATERIALIZED
current Alembic head             20260827_10
representation parity            PASS
runtime ACL                      PASS
security lock                    PASS
real PostgreSQL proof            PASS
full-stack DB-backed proof       PASS
M3 database work                 CLOSED
```

M3 closure does **not** authorize speculative later Auth persistence.

M4 may introduce verification/recovery/account-establishment structures only after the exact proof lifecycle and mutation contract are closed. M5 may introduce ExternalIdentity/PasskeyCredential only when provider/passkey semantics enter implementation. MFA persistence remains deferred.

Permanent rule:

```text
later Auth need
→ exact semantic/security contract
→ minimal forward migration
→ mapping
→ Dictionary
→ whole-DB current reference
→ this subject reference
→ direct real PostgreSQL proof
```
