# DANTE

DANTE is a personal operating system designed to help people understand, organize and improve real life by turning intentions, needs and possibilities into outcomes they can realistically pursue.

**Compass:** *Understand life. Shape what comes next.*

## Current repository state

The integrated foundation on protected `main` remains closed. The active branch-local product vertical is Access/Auth on `feature/access-auth`.

```text
PRODUCT / NORTH STAR                    CURRENT
DOMAIN / LOGICAL / PHYSICAL             CLOSED
ENGINEERING / FRONTEND FOUNDATION       CLOSED / ACCEPTED
BACKEND CP1–CP6                         CLOSED / ACCEPTED
POSTGRESQL                              18.6
PROTECTED-MAIN CP6 ALEMBIC              20260826_08

ACCESS/AUTH M1–M4                       CLOSED / ACCEPTED
M5.1 / M5.2 / M5-A–D                    COMPLETE
M5 GROUPS 1–3                           COMPLETE / ENGINEERING PASS
M5 GROUP 4 WEB ENGINEERING              AUTOMATED QA PASS
LOCAL PASSWORD/PASSKEY UAT              PASS
REAL GOOGLE UAT                         PASS
REAL INTERNET EMAIL DELIVERY            OPEN / RESEARCH + UAT REQUIRED
REAL APPLE REGISTERED-DOMAIN UAT        DEFERRED / OPEN
WHOLE ACCESS/AUTH M5                     ACTIVE / NOT FORMALLY CLOSED

ACCESS/AUTH BRANCH POSTGRESQL            18.6
ACCESS/AUTH ALEMBIC HEAD                 20260831_13
ACCESS/AUTH DB TOPOLOGY                  83 tables / 5 views / 15 routines /
                                         75 triggers / 156 indexes / 85 FKs /
                                         233 CHECKs
```

For exact branch truth use:

- `docs/PROJECT-STATUS.md`
- `docs/ROADMAP.md`
- `docs/workstreams/access-auth.md`
- `docs/workstreams/access-auth-m5-review-2026-09-02.md`

Do not reconstruct current state from old handoffs or phase-time progress labels.

## Repository

Production development continues in the single monorepo:

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

Production applications do not import prototype implementation. A new feature does not justify a new repository or a generic abstraction layer by default.

## Current technical baseline

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

Current Access/Auth preserves:

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal runtime-derived
provider identity = issuer + subject
provider email != Account/link authority
provider auth != provider-data authorization
provider token/assertion != DANTE AuthSession
passwordless Account valid
PasskeyCredential != Account
WebAuthn user_handle = opaque Account binding
reauthentication != signin
frontend/provider/browser completion != backend-authoritative success
```

Web sessions are opaque, server-authoritative and cookie-backed. Browser Auth state is not stored as JWT/localStorage authority. Unsafe authenticated mutations are protected by session-bound CSRF plus origin/fetch-metadata policy.

Google, Apple, password and passkeys are authentication methods for the same DANTE Account; they do not create parallel Account/session systems.

## Access/Auth proof state

The reviewed product checkpoint `ab2716...` passed:

```text
Prettier / TypeScript / ESLint / architecture     PASS
Web unit/component                               68 / 68 PASS
Auth Playwright HTTPS                            60 / 60 PASS
Chromium / Firefox / WebKit                      PASS through canonical suite
```

Manual UAT then proved real Windows Hello passkeys, passwordless signin, recent-auth/session rotation, authenticator lifecycle/anti-lockout and direct PostgreSQL coherence.

Real Google UAT proved official Google Identity Services → real ID token → DANTE backend verification → direct mailbox proof where Google was not authoritative → passwordless Account + ExternalIdentity + canonical AuthSession. Details are in `docs/workstreams/access-auth-m5-review-2026-09-02.md`.

## Current open boundary — email delivery

No production email provider has been selected.

The next gate must research the architecture before choosing a vendor:

```text
DANTE-owned email intent/security state
vs external delivery responsibility
SMTP vs provider HTTP API
SPF/DKIM/DMARC
bounce/complaint/suppression handling
ambiguous delivery outcome and retry semantics
observability/privacy/secrets
Apple Private Email Relay requirements
self-hosted SMTP operational/deliverability cost
provider portability
```

The opt-in real-SMTP local-UAT capability at `9c0587...` is only a test transport path; deterministic automated tests continue to use loopback SMTP capture.

## Documentation entry points

Start at:

- `docs/README.md`
- `docs/PROJECT-STATUS.md`
- `docs/ROADMAP.md`
- `docs/architecture/README.md`
- `docs/database/README.md`
- `docs/frontend/README.md`
- `apps/backend/README.md`

Repository executable truth and accepted current documentation beat conversation memory.