# DANTE

DANTE is a personal operating system designed to help people understand, organize and improve real life by turning intentions, needs and possibilities into outcomes they can realistically pursue.

**Compass:** *Understand life. Shape what comes next.*

## Current repository state

Protected `main` remains the integrated source authority. `feature/access-auth` currently contains newer accepted Access/Auth + shared Email Platform work and is in **pre-integration audit**.

```text
PRODUCT / NORTH STAR                    CURRENT
DOMAIN / LOGICAL / PHYSICAL             CLOSED
ENGINEERING / FRONTEND FOUNDATION       CLOSED / ACCEPTED
BACKEND CP1–CP6                         CLOSED / ACCEPTED
POSTGRESQL                              18.6

PROTECTED MAIN
  Recovery                              CLOSED / INTEGRATED
  Alembic head                          20260830_09

FEATURE/ACCESS-AUTH
  Access M1–M5                          CLOSED / ACCEPTED
  local password/passkey UAT            PASS
  real Windows Hello UAT                PASS
  real Google UAT                       PASS
  real Apple registered-domain UAT      BOUNDED DEFERRED / NON-BLOCKING
  shared Email Platform                 CLOSED / ACCEPTED
  real SES signup/recovery/notification PASS
  Alembic head                          20260903_15
  DB topology                           87 tables / 5 views / 15 routines /
                                        75 triggers / 170 indexes / 88 FKs /
                                        267 CHECKs
  current work                          PRE-INTEGRATION AUDIT

M6 Native Mobile                        FUTURE / OPTIONAL
later Access/M7 maturity                FUTURE
```

The feature branch and protected main currently have divergent Alembic children of `20260826_08`. They are not yet one database history. Integration will preserve both histories and use a normal forward Alembic merge revision.

For exact status use:

- `docs/PROJECT-STATUS.md`
- `docs/ROADMAP.md`
- `docs/workstreams/access-auth.md`
- `docs/database/README.md`

## Repository

Production development uses the single monorepo:

```text
MattiaRubino/dante
```

Ownership boundaries:

```text
apps/
├── backend/      Python/FastAPI product backend
├── web/          React Web application
└── mobile/       React Native/Expo boundary
packages/         genuine shared packages only
infra/            infrastructure definitions
tooling/          repository/runtime/QA tooling
tests/system/     system-level proof
docs/             durable project authority
prototypes/       non-production design/reference evidence
.github/          CI/repository automation
```

Production applications do not import prototype implementation. A new feature does not justify a new repository or generic abstraction layer by default.

## Technical baseline

Backend:

```text
Python                   3.14.x
package manager          uv
server                    FastAPI
ORM/SQL                   SQLAlchemy 2.x
PostgreSQL driver         psycopg 3
migrations                Alembic
format/lint               Ruff
typecheck                 mypy strict
testing                   pytest / Hypothesis where meaningful
```

Frontend:

```text
Node                      24 LTS
TypeScript                6 strict
pnpm                      11
Turborepo                 2
React                     19.2
Vite                      8
TanStack Router / Query
Expo / React Native       mobile boundary
Zod / Orval               governed API contract
```

Database roles:

```text
dante_owner      NOLOGIN ownership identity
dante_migrator   LOGIN migration identity
dante_runtime    LOGIN application runtime identity
```

Canonical persistence is PostgreSQL. The outer application-operation boundary owns commit/rollback; persistence adapters may flush but never commit implicitly.

## Access/Auth architecture

Permanent rules:

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal runtime-derived
provider identity = issuer + subject
provider email != Account/link authority
provider token/assertion != DANTE AuthSession
passwordless Account valid
PasskeyCredential != Account
WebAuthn user_handle = opaque Account binding
reauthentication != signin
frontend/provider/browser completion != backend-authoritative success
```

Web sessions are opaque, server-authoritative and cookie-backed. Browser Auth state is not localStorage/sessionStorage JWT authority. Unsafe authenticated mutations use session-bound CSRF plus exact same-origin protections.

Google, Apple, password and passkeys are authentication methods for the same Account and converge on the same AuthSession model.

## Shared Email Platform

Email is reusable DANTE infrastructure, separate from Access/Auth ownership.

```text
feature/application mutation
+ durable EmailIntent
→ PostgreSQL COMMIT
→ claim / lease / worker
→ protected payload + versioned template
→ provider-neutral adapter
→ Amazon SES API v2 / SMTP local-CI compatibility
→ provider evidence / suppression
```

Current Email persistence:

```text
dante.email_delivery_intent
dante.email_delivery_attempt
dante.email_provider_event
dante.email_recipient_suppression
```

Permanent delivery rules:

```text
DANTE owns lifecycle/state
provider owns last-mile transport
provider accepted != delivered
no provider I/O in caller DB transaction
no blind retry after ambiguous send
operation-scoped idempotency + immutable fingerprint
short-lived AEAD-protected sensitive payload
terminal/unsafe-state secret wipe
future consumers reuse the shared platform
```

Final real SES UAT on 2026-09-03 proved signup verification, password recovery, reset notification, no auto-login and prior-session revocation. Direct PostgreSQL inspection showed provider MessageId and sensitive-payload wipe for all three accepted intents.

Exact evidence: `docs/development/email-platform-acceptance-2026-09-03.md`.

## Production email boundary

The Email Platform is closed as engineering infrastructure. Production sender deployment remains separately gated on, as applicable:

```text
DANTE-controlled sender domain/subdomain
SPF / DKIM / DMARC
production workload identity
SES production account/quota/reputation posture
live cloud provider-feedback routing
production alerting/SLOs
traffic/reputation segmentation
Apple Private Email Relay compatibility when enabled
```

## Current integration order

```text
feature/access-auth pre-integration audit
→ merge protected main into feature/access-auth
→ forward Alembic merge revision + combined QA
→ PR Access/Auth + Email Platform to protected main
→ merge enriched main into feature/platform-observability
→ observability integration/release rechecks
→ PR observability to protected main
→ open future bounded product branches from enriched main
```

No rebase/history rewrite/force push/direct protected-main write.

## Documentation entry points

Start at:

- `docs/README.md`
- `docs/PROJECT-STATUS.md`
- `docs/ROADMAP.md`
- `docs/database/README.md`
- `docs/architecture/README.md`
- `docs/frontend/README.md`
- `apps/backend/README.md`

Repository executable truth and accepted current documentation beat conversation memory and historical handoffs.