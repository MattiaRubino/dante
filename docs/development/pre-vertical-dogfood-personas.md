# Pre-Vertical Dogfood and Personas

- **Status:** CURRENT / BRANCH-LOCAL PV-02
- **Branch:** `feature/pre-vertical-foundation`
- **Scope:** persistent LOCAL/DEV dogfood plus deterministic product-independent personas

## Purpose

PV-02 needs data that survives ordinary application restarts so DANTE can be exercised repeatedly before the first product vertical exists. This is deliberately different from the existing PostgreSQL pytest harness, whose databases are disposable by design.

The boundary is:

```text
persistent LOCAL/DEV dogfood
!= disposable PostgreSQL acceptance data
!= production/UAT data
!= product vertical fixtures
```

No new database schema is introduced. Dogfood and personas consume the existing Access/Auth and authenticated DANTE-context contracts.

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

Normal runtime database/password-pepper configuration is loaded from the same environment used by the backend, normally by launching through the ignored `apps/backend/.env.local` file:

```bash
uv run --env-file .env.local ...
```

The dogfood/persona password and the `dante_migrator` password are supplied through separate `*.local` files. The repository already ignores `infra/compose/secrets/*.local` and `.env.*` except `.env.example`.

Recommended LOCAL files:

```text
infra/compose/secrets/pre_vertical_dogfood_password.local
infra/compose/secrets/pre_vertical_persona_password.local
infra/compose/secrets/postgres_migrator_password.local
```

These names are conventions only; the tooling accepts any existing single-line `*.local` file.

## Dogfood command

From `apps/backend`, with the normal persistent PostgreSQL database already provisioned and migrated to the branch head:

```bash
uv run --env-file .env.local \
  python -m tooling.pre_vertical_foundation.dogfood \
  --email dante.dogfood@example.com \
  --password-file ../../infra/compose/secrets/pre_vertical_dogfood_password.local \
  --migrator-password-file ../../infra/compose/secrets/postgres_migrator_password.local
```

The command prints only non-secret identity/result information: email, Account ref, self Person ref, whether the Account was newly created or already verified, and timezone mode.

The command refuses to run unless `DANTE_ENV` is exactly `local` or `dev`, and the configured runtime database identity must be exactly `dante_runtime`.

## Deterministic personas

PV-02 defines exactly three initial foundation personas:

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
  --migrator-password-file ../../infra/compose/secrets/postgres_migrator_password.local
```

A subset can be selected by repeating `--persona`:

```bash
... --persona normal --persona temporal_edge
```

Materialization:

1. creates/verifies the deterministic Account using canonical Auth normalization/KDF;
2. initializes the deterministic self Person through the PV-02 runtime capability;
3. specializes the pristine `follow_device` context to a persona's fixed timezone policy when required;
4. refuses to overwrite an incompatible existing deterministic Account, self Person or timezone policy.

No Timeline, Activity, Event, Routine, Session, Actual or other vertical-specific records are created.

## Relationship to PV-03

PV-03 consumes these persona definitions and the existing disposable PostgreSQL 18.6 acceptance harness to build deterministic scale profiles and whole-branch acceptance.

PV-03 must not replace the persistent dogfood database with the disposable pytest database, and it must not turn these three personas into a generic product data model.

## Proof obligations

PV-02 dogfood/persona implementation is accepted when bounded tests prove:

- LOCAL/DEV-only environment guard;
- canonical runtime identity requirement;
- canonical Base64URL pepper configuration parsing;
- `*.local` secret-file discipline;
- deterministic unique UUIDv7 persona refs;
- real Rome/New York local-time classification for ordinary/gap/overlap anchors;
- fixed timezone independence from current device zone;
- real PostgreSQL account/context first-run materialization;
- rerun returns the same Account and self Person;
- wrong password fails without credential rewrite;
- persona timezone persistence matches the deterministic specification.
