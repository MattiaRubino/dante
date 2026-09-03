# DANTE Backend

- **Status:** CURRENT BACKEND ENTRY POINT
- **Last reconciled:** 2026-09-03 for `feature/access-auth`
- **Backend root:** `apps/backend`
- **Current Access/Auth Alembic head:** `20260903_15`
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
20260903_14  durable shared Email Platform persistence
20260903_15  exact Email Platform runtime ACL hardening
```

Applied migration history is immutable; corrections use new forward revisions.

## 5. Current Access/Auth backend

The branch contains the M3–M5 backend/public API needed by the current Web workstream, including:

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

Exact wire authority remains FastAPI declarations, deterministic OpenAPI snapshot, generated client and Access/Auth API contracts.

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

This third-party-mailbox branch passed real Google UAT.

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

## 9. Shared Email Platform

Email delivery is no longer owned by a process-memory SMTP dispatcher.

Current architecture:

```text
feature/Auth transaction
+
durable EmailIntent
→ PostgreSQL commit
→ durable claim/lease worker
→ protected payload + versioned template
→ provider-neutral adapter
→ Amazon SES API v2 or SMTP local/CI compatibility
```

Current platform persistence:

```text
dante.email_delivery_intent
dante.email_delivery_attempt
dante.email_provider_event
dante.email_recipient_suppression
```

Permanent rules:

```text
provider I/O outside caller DB transaction
provider accepted != delivered
no blind retry after ambiguous send outcome
stable DANTE intent before external send
short-lived dedicated AES-GCM protected payload
terminal/unsafe-state payload wipe
provider SDK types do not cross into Auth/application contracts
```

Amazon SES API v2 is the accepted primary external adapter. The SES client is created from a region-bound boto3 Session so temporary `aws login` credential refresh also receives the configured region.

SMTP remains a last-mile compatibility adapter behind the same durable worker; it is not a second queue or canonical lifecycle.

Architecture/evidence:

- `../../docs/architecture/email-platform.md`
- `../../docs/architecture/access-auth-email-delivery.md`
- `../../docs/development/email-platform-local-uat.md`
- `../../docs/development/email-platform-acceptance-2026-09-03.md`

## 10. Real Email UAT posture

Repository-owned local real-provider tooling supports:

```text
AWS CLI user-local bootstrap
named dante-uat profile
non-root SES preflight
least-privilege IAM policy template
SES eu-west-3 UAT
fresh disposable PostgreSQL 18.6
fresh signup/recovery flow
```

Backend UAT dependencies include Botocore AWS CRT support through the lockfile. Do not repair browser-login support with ad-hoc `pip install` state.

The final real UAT directly proved signup verification, password recovery, reset notification, no auto-login after reset, prior-session revocation and direct PostgreSQL provider-correlation/secret-wipe state.

Production sender-domain/DKIM/SPF/DMARC, workload identity and live cloud feedback ingress remain separate deployment gates.

## 11. Run locally

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

For real Email UAT, follow the dedicated runbook instead of composing ad-hoc environment variables from old shell history.

## 12. Quality commands

From `apps/backend`:

```bash
uv run --locked ruff format --check .
uv run --locked ruff check .
uv run --locked mypy src
uv run --locked pytest -m "not postgres"
uv run --locked pytest -m postgres
uv build
```

PostgreSQL-marked tests use the disposable canonical PostgreSQL 18.6 image. Automated acceptance must not mutate the ordinary persistent LOCAL DANTE database.

## 13. API generation

FastAPI/Pydantic declarations feed the deterministic OpenAPI 3.1 snapshot and governed Orval/Zod client. Live `/openapi.json` is not the CI generation authority.

Normal environment posture:

```text
LOCAL / DEV / UAT   docs/openapi enabled as configured for engineering
PROD                interactive docs/openapi disabled unless explicitly governed
```

## 14. Current proof pointers

Current authorities/evidence:

- `../../docs/PROJECT-STATUS.md`
- `../../docs/workstreams/access-auth.md`
- `../../docs/database/access-auth.md`
- `../../docs/architecture/email-platform.md`
- `../../docs/development/email-platform-acceptance-2026-09-03.md`

Historical CP5/CP6/M3/M4 acceptance details remain available in dedicated development/database docs and Git history.
