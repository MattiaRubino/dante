# Pre-Vertical Dogfood and Personas

- **Status:** CURRENT / PRE-VERTICAL FOUNDATION / PV-02 CLOSED / PASS
- **Scope:** persistent LOCAL/DEV dogfood plus deterministic product-independent personas
- **Closure record:** `../workstreams/pre-vertical-foundation-closure-2026-09-06.md`

## Purpose

The pre-vertical foundation needs data that survives ordinary application restarts so DANTE can be exercised repeatedly before the first product vertical exists. This is deliberately different from the PostgreSQL pytest harness, whose databases are disposable by design.

The boundary is:

```text
persistent LOCAL/DEV dogfood
!= disposable PostgreSQL acceptance data
!= production/UAT data
!= product vertical fixtures
```

Dogfood and personas consume the existing Access/Auth and authenticated DANTE-context contracts. They do not create a second auth model or a product-domain fixture framework.

## Persistent dogfood account

The dogfood bootstrap creates or verifies one password-authenticated Account in the ordinary persistent LOCAL/DEV `dante` database.

It reuses:

- `dante.auth.email.normalize_email` for canonical email identity;
- `dante.auth.passwords.PasswordKdf` for the exact Argon2id + pepper credential policy;
- canonical `account`, `email_identity` and `password_credential` persistence;
- `dante.ensure_account_application_context(...)` through the normal `dante_runtime` role for Account → self Person initialization.

The bootstrap is an administrative LOCAL/DEV seed path, not a product signup endpoint. It intentionally does not create a signup challenge or send verification email. The resulting EmailIdentity is marked verified because the operator is explicitly provisioning synthetic development state.

### Idempotence and conflict behavior

Canonical email identity is the dogfood lookup key.

On rerun:

```text
same email + same password + compatible active Account
→ return existing Account
→ return existing self Person/context
→ no credential rewrite

same email + different password
→ FAIL
→ no password reset

same email + disabled/unverified/non-password incompatible state
→ FAIL
→ no silent repair/reconciliation
```

A concurrent product/signup creation that wins the unique email race is re-read and must satisfy the same compatibility checks before the seed is accepted.

## Secret handling

The tooling never embeds or logs passwords, database credentials or pepper values.

Normal runtime database/password-pepper configuration is loaded from the same environment used by the backend, normally through the ignored `apps/backend/.env.local` file:

```bash
uv run --env-file .env.local ...
```

The dogfood/persona password and the `dante_migrator` password are supplied through separate `*.local` files. The repository ignores `infra/compose/secrets/*.local` and `.env.*` except `.env.example`.

Recommended LOCAL files:

```text
infra/compose/secrets/pre_vertical_dogfood_password.local
infra/compose/secrets/pre_vertical_persona_password.local
infra/compose/secrets/dante_migrator_password.local
```

These names are conventions only; the tooling accepts any existing single-line `*.local` file passed explicitly by the operator.

## Dogfood command

From `apps/backend`, with the normal persistent PostgreSQL database already provisioned and migrated to the current candidate/protected-main head:

```bash
uv run --env-file .env.local \
  python -m tooling.pre_vertical_foundation.dogfood \
  --email dante.dogfood@example.com \
  --password-file ../../infra/compose/secrets/pre_vertical_dogfood_password.local \
  --migrator-password-file ../../infra/compose/secrets/dante_migrator_password.local
```

The command prints only non-secret identity/result information: email, Account ref, self Person ref, whether the Account was newly created or already verified, and timezone mode.

The command refuses to run unless `DANTE_ENV` is exactly `local` or `dev`, and the configured runtime database identity must be exactly `dante_runtime`.

## Deterministic personas

The foundation defines exactly three initial product-independent personas:

| Persona | Purpose | Timezone policy | Device context | Temporal anchors |
|---|---|---|---|---|
| `normal` | ordinary current-use context | `follow_device` | `Europe/Rome` | ordinary Rome summer local time |
| `temporal_edge` | DST/named-zone edge semantics | fixed `America/New_York` | `Europe/Rome` | 2026 spring gap + fall overlap |
| `historical` | explicit long-history anchors | fixed `Europe/Rome` | `America/Los_Angeles` | 2016 history start + 2026 as-of instant |

The device zones intentionally differ from fixed policies for the edge/historical personas so tests can prove that device movement does not rewrite a fixed persisted preference.

### Deterministic UUIDv7

Persona `account_ref` and self Person refs are stable synthetically generated UUIDv7 values. Their UUIDv7 timestamp field is only deterministic fixture-construction data.

It is explicitly forbidden to derive semantic chronology or currentness from persona UUID ordering. Historical chronology is represented by the persona's explicit temporal anchors.

## Persona materialization

All personas can be materialized into the ordinary LOCAL/DEV database with one shared synthetic password secret:

```bash
uv run --env-file .env.local \
  python -m tooling.pre_vertical_foundation.seed_personas \
  --password-file ../../infra/compose/secrets/pre_vertical_persona_password.local \
  --migrator-password-file ../../infra/compose/secrets/dante_migrator_password.local
```

A subset can be selected by repeating `--persona`:

```bash
... --persona normal --persona temporal_edge
```

Materialization:

1. creates/verifies the deterministic Account using canonical Auth normalization/KDF;
2. initializes the deterministic self Person through the bounded runtime capability;
3. specializes the pristine `follow_device` context to a persona's fixed timezone policy when required;
4. refuses to overwrite an incompatible existing deterministic Account, self Person or timezone policy.

No Timeline, Activity, Event, Routine, Occurrence, Session, Actual, Outcome, Observation or other vertical-specific records are created.

## Relationship to Scale Harness

`../development/pre-vertical-scale-harness.md` reuses these three personas to build deterministic product-independent scale plans. The persistent dogfood database remains distinct from the disposable PostgreSQL acceptance harness.

The scale harness and whole-branch local QA are closed. This tooling remains useful after merge as LOCAL/DEV operator/test support; it is not an active workstream roadmap.

## Acceptance evidence

PV-02 bounded tests and operational smoke have established:

```text
LOCAL/DEV-only environment guard                        PASS
canonical dante_runtime identity requirement             PASS
canonical Base64URL pepper configuration parsing         PASS
*.local secret-file discipline                           PASS
deterministic unique UUIDv7 persona refs                 PASS
Rome/New York ordinary/gap/overlap classification        PASS
fixed timezone independence from device zone             PASS
real PostgreSQL account/context first materialization    PASS
rerun returns same Account and self Person               PASS
wrong password fails without credential rewrite          PASS
persona timezone persistence                             PASS
persistent dogfood seed/rerun                            PASS
real browser email/password login                        PASS
```

The real PostgreSQL tests use the existing disposable PostgreSQL 18.6 acceptance harness; this tooling does not introduce a second database-test framework.

## Permanent boundary

Dogfood/personas are development support. They must never be widened into a generic user/profile model, production data bootstrap, fake product history model or justification for product-domain rows that do not yet have a real owning vertical.
