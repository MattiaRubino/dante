# DANTE Backend

- **Status:** CURRENT BACKEND ENTRY POINT
- **Last reconciled:** 2026-09-02 for `feature/access-auth`
- **Backend root:** `apps/backend`
- **Current Access/Auth Alembic head:** `20260831_13`
- **PostgreSQL:** 18.6

This README describes current backend engineering/runtime boundaries. Historical CP/M3 acceptance details remain recoverable in Git and dedicated documentation rather than being duplicated as current state here.

## 1. Baseline

```text
Python                   3.14.x
package manager          uv
application              FastAPI
ORM/SQL toolkit          SQLAlchemy 2.x
driver                    psycopg 3
migrations                Alembic
format/lint               Ruff
typecheck                 mypy strict
testing                   pytest / Hypothesis where meaningful
runtime semantics         Linux / WSL2 local workflow
canonical persistence     PostgreSQL 18.6
```

Source root:

```text
apps/backend/src/dante
```

## 2. Architecture

Backend remains a capability-first modular monolith. Do not introduce generic `Repository[T]`, generic Unit of Work, BaseService or service-locator layers merely for uniformity.

The outer application-operation boundary owns commit/rollback. Persistence adapters may flush but do not commit implicitly.

```text
HTTP/FastAPI
→ capability API/application boundary
→ persistence/provider/security adapters
→ PostgreSQL / bounded external dependencies
```

## 3. Database roles

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
```

Migrations use the dedicated migrator identity and explicit owner role. Normal application startup never runs migrations.

## 4. Alembic progression

```text
20260820_01  technical baseline
20260825_*   CP6 materialization
20260826_08  protected-main CP6 final hardening
20260827_09  Account / EmailIdentity / PasswordCredential / AuthSession
20260827_10  bounded Account security-lock capability
20260829_11  signup/recovery lifecycle challenges + ACL
20260830_12  M5 provider/Apple/WebAuthn/passkey persistence
20260831_13  bounded authenticator-lifecycle runtime ACL
```

Applied migration history is immutable; corrections use new forward revisions.

## 5. Current Access/Auth backend

The branch now contains the complete M3–M5 backend/public API needed by the current Web vertical, including:

```text
email/password signin/session/logout
signup/OTP/recovery/reset/reauth
methods inventory
password establish/remove
Google sign-in/link/reauth
Apple begin/callback/grant/notification lifecycle
provider enrollment/link confirmation/unlink
passkey registration/authentication/reauthentication/update/remove
canonical AuthSession creation/rotation/revocation
anti-lockout
```

Do not treat this list as a manually maintained wire contract. Exact paths, models, operation IDs and machine problems are owned by the FastAPI declarations, deterministic OpenAPI snapshot, generated client and Access/Auth API contracts.

## 6. Auth security model

```text
Account != EmailIdentity != credential
PasswordCredential optional
provider identity = issuer + subject
provider token != DANTE AuthSession
passkey != Account
Principal runtime-derived
opaque high-entropy AuthSession secret
stored session verifier only
same-origin Web cookie authority
session-bound CSRF
recent-auth for sensitive operations
```

Password work uses NFC + HMAC pepper boundary + Argon2id. HIBP screening is bounded according to the accepted lifecycle policy.

Provider/JWK/network work and browser WebAuthn ceremony wait are kept outside authoritative DB write transactions.

## 7. Google

Current backend verifies real Google ID tokens through trusted JWK material and validates allowed algorithm, issuer, audience/authorized party where applicable, expiry/timing, nonce and subject.

Federated identity is `issuer + sub`, never email.

Mailbox classification:

```text
Gmail                         provider-authoritative
verified Workspace + hd       provider-authoritative
third-party Google mailbox    requires additional DANTE mailbox proof where current control matters
```

This exact third-party-mailbox branch passed real Google UAT on 2026-09-02.

## 8. WebAuthn

Backend uses `python-fido2` for RP/ceremony verification.

Policy:

```text
discoverable credential required
user verification required
attestation none
exact configured RP ID/origin
short single-use challenge
multiple passkeys
```

DANTE persists credential public key/material only; no biometric template/PIN/private key.

## 9. Email delivery

The application owns bounded email intents/commands and uses `SmtpEmailDispatcher` as the current delivery adapter. Automated acceptance uses a deterministic loopback SMTP capture.

Production/external delivery architecture is **not yet selected**. Do not infer that SMTP or any specific provider is the permanent production choice merely because the current adapter and UAT tooling can speak SMTP.

The next architecture gate must evaluate SMTP vs provider HTTP APIs, provider neutrality, deliverability/DNS, bounce/complaint/suppression, retry ambiguity, observability/privacy and Apple relay requirements.

## 10. Run locally

After PostgreSQL roles/schema and local configuration are prepared:

```bash
uv run --env-file .env.local \
  uvicorn dante.bootstrap.app:create_app \
  --factory \
  --reload
```

Technical probes:

```text
GET /health/live
GET /health/ready
```

Health endpoints deliberately expose no credentials/DSN/SQL details and are not product API authority.

## 11. Quality commands

From `apps/backend`:

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest -m "not postgres"
uv run pytest -m postgres
uv run pytest
uv build
```

PostgreSQL-marked tests use the disposable canonical PostgreSQL 18.6 image. If needed from repository root:

```bash
docker compose -f infra/compose/local.yaml build postgres
```

Automated acceptance must not mutate the ordinary persistent LOCAL DANTE database.

## 12. API generation

FastAPI/Pydantic declarations feed the deterministic OpenAPI 3.1 snapshot and governed Orval/Zod client. Live `/openapi.json` is not the CI generation authority.

Normal environment posture:

```text
LOCAL / DEV / UAT   docs/openapi enabled as configured for engineering
PROD                interactive docs/openapi disabled unless explicitly governed
```

## 13. Current proof pointer

Current product-code Web gate and manual UAT are recorded in:

- `../../docs/workstreams/access-auth-m5-review-2026-09-02.md`
- `../../docs/PROJECT-STATUS.md`
- `../../docs/database/access-auth.md`

Historical CP5/CP6/M3/M4 acceptance details remain available in dedicated development/database docs and Git history.