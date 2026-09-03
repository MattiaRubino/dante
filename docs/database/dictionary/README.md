# DANTE Database Dictionary

- **Status:** CURRENT / MATERIALIZED / PRE-INTEGRATION
- **Schema version:** 1
- **Serialization:** JSON
- **Structural dialect:** JSON Schema Draft 2020-12
- **PostgreSQL:** 18.6
- **Feature/access-auth Alembic head:** `20260903_15`
- **Frozen CP6 head:** `20260826_08`

## 1. Purpose

This directory is the machine-readable companion to the current DANTE Database System of Record.

It does not replace Domain, Logical, Physical, the PostgreSQL Persistence Constitution, Alembic, SQLAlchemy or real PostgreSQL introspection. It provides one structured current object contract that all of those representations must reconcile against.

```text
Current DB Reference
≈ Database Dictionary
≈ SQLAlchemy MetaData / mappings
≈ Alembic
≈ real PostgreSQL
≈ direct tests
```

A mismatch is a defect.

## 2. Current Access-branch inventory

```text
dictionary/
├── README.md
├── scope.json
├── schema/
│   ├── object-v1.schema.json
│   └── scope-v1.schema.json
├── tables/       87
├── views/         5
└── routines/     15
```

Standalone total:

```text
87 tables
5 views
15 routines
----------
107 standalone entries
```

Embedded/current topology:

```text
75 trigger attachments
170 physical indexes
88 foreign keys
267 CHECK constraints
```

These values are branch-local through Alembic `20260903_15`. They do not include protected-main Recovery until the branches are deliberately integrated.

## 3. Frozen CP6 baseline vs current materialization

`scope.json` intentionally separates the historical CP6 closure benchmark from the evolving current inventory.

Frozen `expected_baseline` at `20260826_08`:

```text
68 tables / 5 views / 14 routines / 87 standalone entries
75 triggers / 95 physical indexes / 68 FKs / 120 CHECKs
```

Current branch `current_materialization`:

```text
87 tables / 5 views / 15 routines / 107 standalone entries
75 triggers / 170 physical indexes / 88 FKs / 267 CHECKs
```

The two sets must not be forced equal merely because later product work added real objects.

### `completed_stages`

This field records the **frozen CP6 materialization sequence only**:

```text
CP6-M01
CP6-M02
CP6-M03
CP6-M04
CP6-M05
CP6-M06
CP6-M07
```

Post-CP6 provenance is not appended to that list. It belongs on each object entry through:

```text
implementation.introducing_stage
implementation.alembic_revision
implementation.runtime_acl_stage
```

This distinction keeps `scope.json` valid against `scope-v1.schema.json` while allowing current inventory counts to evolve.

## 4. Post-CP6 Access/Auth evolution

M3:

```text
20260827_09
account
email_identity
password_credential
auth_session

20260827_10
acquire_account_security_lock(uuid)
```

M4:

```text
20260829_11
password_signup_challenge
password_recovery_challenge
```

M5 multi-authenticator persistence:

```text
20260830_12
external_identity
external_auth_transaction
apple_auth_grant
external_link_challenge
external_signup_challenge
account_profile_bootstrap
webauthn_account
passkey_credential
webauthn_challenge

20260831_13
authenticator-lifecycle ACL only
```

Shared Email Platform:

```text
20260903_14
email_delivery_intent
email_delivery_attempt
email_provider_event
email_recipient_suppression

20260903_15
exact Email Platform lifecycle UPDATE ACL hardening
```

## 5. Shared Email Platform classification

The four Email Platform objects are bounded shared technical infrastructure. Access/Auth is the first current consumer, but it is not the platform owner.

Dictionary semantics must therefore preserve:

```text
technical persistence role
no Domain owner invented
not MaterialState
shared Email Platform architecture/ADR as authority
Access/Auth may remain a current logical/consumer traceability source
```

The platform must not become a generic event bus, generic outbox semantic root or JSON/EAV escape hatch.

## 6. Object entry contract

Every standalone entry contains:

```text
object
purpose
classification
semantic_traceability
implementation
structure
state_history
lifecycle
security
proof
```

Object types remain exactly:

```text
table
view
routine
```

Strict `additionalProperties: false` schema shapes prevent accidental metadata conventions from becoming silent contract.

Object key/filename contract:

```text
table:dante.<name>    → tables/<name>.json
view:dante.<name>     → views/<name>.json
routine:dante.<name>  → routines/<name>.json
```

## 7. Embedded objects

Table entries own their embedded:

```text
primary key
foreign keys
unique constraints
CHECK constraints
physical indexes
trigger attachments
```

Standalone routines remain separate because signature/security/search-path/ACL are independently governed PostgreSQL facts.

## 8. Structural vs semantic metadata

Mechanically reconcilable facts include:

```text
object name/type
columns/types/nullability/defaults
PK/FK/UQ/CK
indexes + validity/readiness/liveness
trigger properties
view definitions/properties
routine signature/security/volatility/search_path
relation persistence/RLS/partitioning/replica identity
owner + ACL
Alembic revision
SQLAlchemy mapping
current inventory counts
```

Human-authored reviewed facts include:

```text
why an object exists
what fields/references mean
canonicality/technical role
state/history semantics
lifecycle/redaction meaning
index/constraint rationale
semantic traceability
proof rationale
```

Generated structural tooling must never overwrite semantic meaning automatically.

## 9. Security metadata

Expected grants are represented explicitly as:

```text
grantee
privilege
columns
grant_option
```

Column-scoped INSERT/UPDATE authority must not be widened into generic CRUD merely for convenience.

Examples:

```text
Account/security mutation  → bounded exact capabilities
ExternalIdentity/passkeys  → logical revoke where required
Email intents/attempts      → only reviewed lifecycle columns mutable
provider events             → insert-only evidence for runtime
```

## 10. Validation contract

Two levels are required.

### Level 1 — structural schema consistency

`scope.json` and object entries must obey their declared schema contracts. In particular, a value cannot be added to `completed_stages` unless the scope schema admits it and the field's lifecycle meaning actually requires it.

### Level 2 — DANTE semantic/cross-representation consistency

At minimum:

```text
unique exact object keys
filename/name agreement
all referenced columns exist
all FK targets resolve
trigger routine references resolve
object type ↔ SQLAlchemy mode
current scope counts ↔ entry tree
Dictionary ↔ SQLAlchemy ↔ Alembic ↔ PostgreSQL
owner/ACL parity
routine search_path/security parity
extension-owned objects excluded correctly
```

`apps/backend/tests/integration/database/test_current_catalog.py` provides the live PostgreSQL cross-representation gate for current branch materialization. Historical CP6 tests independently migrate/prove the frozen CP6 baseline rather than mutating that evidence to match later stages.

## 11. Same-change rule

A real database structural change is incomplete unless its reviewed change updates affected:

```text
Dictionary entry/schema/scope where needed
SQLAlchemy mapping
Alembic forward revision
current human DB reference
direct tests
real PostgreSQL proof
```

No real object → no ceremonial Dictionary entry.

Real current DANTE object → matching Dictionary entry required.

## 12. Protected-main Recovery divergence

Protected main currently owns Recovery at `20260830_09` and has independently evolved its Dictionary scope/schema to represent that integrated history.

Do **not** copy main's Recovery scope values into this branch before main is merged. Until then, this branch must remain internally truthful to its own materialized object set.

During integration:

```text
merge main into feature/access-auth
→ reconcile the two Dictionary evolutions deliberately
→ preserve both semantic histories
→ update scope/schema for the combined current inventory
→ add forward Alembic merge revision
→ prove combined real PostgreSQL parity
```

The combined counts are accepted only from the merged live catalog.

## 13. Current proof status

Access/Auth branch PostgreSQL acceptance already proves the current object sets, mapping parity, owners, Alembic single head and exact runtime ACL. Email-specific PostgreSQL acceptance proves durable intent/attempt lifecycle, idempotency, claim/lease, ambiguity, secret wipe, feedback/suppression and least privilege.

Real SES UAT additionally observed three accepted intents with provider MessageId and wiped sensitive payload.

Current truth:

- `../README.md` — Database System of Record
- `../access-auth.md` — Access/Auth/Email branch DB reference
- `../../architecture/email-platform.md` — shared Email Platform architecture
- `../../development/email-platform-acceptance-2026-09-03.md` — live Email evidence
- `../../development/backend-cp6-05-whole-database-qa.md` — retained frozen CP6 QA evidence
