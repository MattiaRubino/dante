# DANTE System Overview

- **Status:** CURRENT ARCHITECTURE / IMPLEMENTATION-BOUNDARY OVERVIEW
- **Last reconciled:** 2026-09-03
- **PostgreSQL:** 18.6
- **Protected-main Alembic:** `20260830_09` / Recovery
- **Feature/access-auth Alembic:** `20260903_15` / Access/Auth + Email Platform
- **Current branch work:** PRE-INTEGRATION AUDIT

## 1. Product and authority

DANTE is a personal operating system whose canonical truth represents real life over time while preserving authority, provenance, uncertainty and distinctions between intention, execution and outcome.

North Star execution loop:

```text
Understand
→ Discover
→ Orchestrate
→ Decide
→ Plan & Coordinate
→ Act
→ Observe
→ Learn & Adapt
```

Permanent semantic constraints include:

```text
reality != plan
inference != fact
Effort != Execution != Outcome != Goal progress
unknown != false
Person != Account != Principal != Actor
provider state != canonical DANTE state
derived projection != canonical truth
MaterialStateRef != ETag/MVCC/provider revision
idempotency != semantic identity
AI/solver output != accepted canonical effect
client local state != canonical accepted effect
```

Implementation consumes Product/Domain/Logical/Physical authority. Framework/storage convenience does not redefine accepted semantics.

## 2. Repository topology

```text
DANTE monorepo
├── apps/backend
├── apps/web
├── apps/mobile
├── packages
├── infra
├── tooling
├── tests/system
├── docs
├── prototypes
└── .github
```

Backend posture is a capability-first modular monolith with explicit application transaction ownership and provider/ORM/HTTP details outside semantic authority.

## 3. Foundation state

```text
Engineering Foundation                  CLOSED / ACCEPTED
Frontend Foundation                     CLOSED / ACCEPTED
Backend CP1–CP6                         CLOSED / ACCEPTED
PostgreSQL 18.6                         CURRENT
schema dante                            CURRENT
owner/migrator/runtime privilege split  CURRENT
real PostgreSQL acceptance testing      CURRENT
```

Historical PostgreSQL 18.4 CP2/CP3 runs remain historical exact evidence; current repository patch is 18.6.

## 4. Canonical persistence

```text
PostgreSQL 18 major family
SOLE CANONICAL PERSISTENCE / MATERIAL-HISTORY AUTHORITY
```

Current `feature/access-auth` catalog before main convergence:

```text
Alembic             20260903_15
87 tables
5 views
15 routines
75 triggers
170 physical indexes
88 foreign keys
267 CHECK constraints
```

Protected main independently contains Recovery at `20260830_09` and is not yet combined with this branch.

The accepted relational thesis remains:

```text
owner-specific canonical families
+ owner-specific material-state/history families
+ specific typed relation families
+ bounded technical address/control structures where required
+ separate provider / derived / runtime concerns
```

Rejected globally:

```text
universal Entity / Thing
universal Relationship / generic edge
canonical EAV/property bag
universal event ontology
universal Fact/Version semantic root
JSONB required-semantic escape hatch
```

## 5. Reference / material-state architecture

Reference families remain distinct:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

Provider revisions, MVCC tokens, timestamps and ETags do not become MaterialStateRef.

Shared Email Platform persistence is technical delivery-control state and is **not MaterialState**.

## 6. CP6 and Recovery

CP6 is closed. Later database work evolves the schema through forward Alembic revisions under ADR-010; applied CP6 history is never rewritten.

Protected main additionally owns the closed Recovery material-state retirement evolution at `20260830_09`.

This feature branch does not claim Recovery as materialized until protected main is merged into it and combined PostgreSQL proof passes.

## 7. Access/Auth architecture

Access/Auth is a real full-stack capability.

```text
Account
├── EmailIdentity 1..N
├── PasswordCredential 0..1
├── AuthSession 0..N
├── ExternalIdentity 0..N
└── WebAuthnAccount 0..1 → PasskeyCredential 0..N
```

Permanent rules:

```text
Person != Account
EmailIdentity != Account
PasswordCredential optional
passwordless Account valid
provider identity = issuer + subject
provider email != linking authority
provider token/assertion != DANTE AuthSession
opaque server-authoritative AuthSession
recent-auth required for sensitive mutation
passkeys use WebAuthn/FIDO2
```

M1–M5 engineering is closed/accepted. Real Windows Hello and Google UAT passed. Real Apple registered-domain UAT is bounded-deferred until external prerequisites exist and is not reported as PASS.

## 8. Shared Email Platform

The Email Platform is shared DANTE infrastructure. Access/Auth is its first consumer.

```text
feature/application transaction
        │
        ├── canonical mutation
        └── durable EmailIntent
                 ▼
          PostgreSQL COMMIT
                 ▼
         claim / lease / worker
                 ▼
         protected payload + template
                 ▼
        provider-neutral adapter
          ├── SES API v2
          └── SMTP local/CI
                 ▼
          provider evidence
                 ▼
       suppression / operations state
```

Current persistence:

```text
dante.email_delivery_intent
dante.email_delivery_attempt
dante.email_provider_event
dante.email_recipient_suppression
```

Permanent rules:

```text
DANTE owns lifecycle/state
provider owns last-mile transport
provider accepted != delivered
provider I/O after caller COMMIT
no blind retry after ambiguous send
operation-scoped idempotency + fingerprint
short-lived AES-GCM protected sensitive payload
terminal/unsafe-state wipe
Auth/security tracking/link rewriting OFF
```

Final real SES UAT proved signup verification, password recovery, reset notification, no auto-login and revocation of the previous AuthSession. Direct PostgreSQL inspection proved provider MessageId + sensitive-payload wipe for the three accepted intents.

## 9. Client data authority

```text
canonical accepted state/effect   backend + PostgreSQL
synced local projection           PowerSync/SQLite noncanonical
offline pending mutation          local staging only
remote request state              TanStack Query + typed API
form/component transient state    frontend only
```

Provider/browser ceremony completion is evidence only; backend response is the authoritative Auth result.

## 10. Integration state

The project currently has two accepted but uncombined database lines after `20260826_08`:

```text
protected main → 20260830_09 Recovery
Access branch  → 20260903_15 Access/Auth + Email
```

Correct convergence:

```text
pre-integration audit
→ merge main into feature/access-auth
→ preserve both Alembic histories
→ add forward Alembic merge revision
→ reconcile Dictionary/reference/mappings
→ real combined PostgreSQL + backend + Web proof
→ PR to protected main
```

After Access/Auth + Email land, the enriched main is merged into the already-closed `feature/platform-observability` branch for its integration/release rechecks, then Observability returns to main.

## 11. Future work boundary

Do not expand this feature branch with later maturity work before integration.

Future fresh branches may own:

```text
M6 Native Mobile when re-gated
session/device management
remote session revoke
security event center / "this wasn't me"
future Access UX/polish
authenticated Home handoff
other product verticals
```

Those branches should start from the enriched protected main containing common Auth/Email/Observability foundations.

## 12. Current authority

Use:

```text
../PROJECT-STATUS.md
../ROADMAP.md
../workstreams/access-auth.md
../database/README.md
../database/access-auth.md
../database/dictionary/
access-auth-*.md
email-platform.md
../development/documentation-lifecycle-policy.md
```

Historical phase banners and handoffs are evidence only.