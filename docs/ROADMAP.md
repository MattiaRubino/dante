# DANTE Roadmap

- **Status:** CURRENT FOR `feature/access-auth`
- **Last reconciled:** 2026-09-03
- **Current macro state:** **M5 CLOSED / PRE-INTEGRATION AUDIT ACTIVE**
- **Feature branch Alembic head:** `20260903_15`
- **Protected-main Alembic head:** `20260830_09`

## 1. Current sequence

```text
Product / North Star
        CURRENT
          ↓
Domain / Logical / Physical
        CLOSED
          ↓
Engineering + Frontend + Backend CP1–CP6
        CLOSED / ACCEPTED
          ↓
Access M1–M4
        CLOSED / ACCEPTED
          ↓
Access M5 Multi-authenticator Account Layer
        CLOSED / ACCEPTED
          ↓
Shared Email Platform
        CLOSED / REAL SES UAT PASS
          ↓
PRE-INTEGRATION AUDIT
        CURRENT
          ↓
MERGE protected main → feature/access-auth
        Recovery + Access/Auth + Email convergence
          ↓
ALEMBIC FORWARD MERGE + FULL INTEGRATION QA
          ↓
PR feature/access-auth → protected main
          ↓
MERGE enriched main → feature/platform-observability
          ↓
OBSERVABILITY INTEGRATION RECHECK
          ↓
PR platform-observability → protected main
          ↓
SHARED FOUNDATION UNBLOCKED ON MAIN
          ↓
new bounded feature branches
```

This order is intentional. Do not start additional Access/M7/Mobile feature scope while core shared foundations are still trapped on long-lived branches.

## 2. M5 closure

M5 is closed for its accepted engineering scope.

Proved:

```text
password + opaque PostgreSQL-backed AuthSession
signup / verification / recovery / reset / reauth
Google backend + real provider UAT
Apple backend/grant/notification lifecycle
passkeys / WebAuthn + real Windows Hello UAT
passwordless Accounts
explicit provider linking/unlinking
anti-lockout authenticator lifecycle
FastAPI/OpenAPI/generated client
/security Web management surface
shared durable Email Platform
real SES signup/recovery/reset-notification UAT
post-reset no-auto-login + prior-session revocation
```

### Apple disposition

Real Apple registered-domain UAT is **BOUNDED DEFERRED / NON-BLOCKING** because the required real Apple account + registered HTTPS domain are unavailable.

This means:

```text
Apple implementation             IMPLEMENTED / ENGINEERING PROVED
real Apple external UAT           NOT EXECUTED
M5 blocked by unavailable Apple   NO
future Apple enablement           MUST run real external acceptance first
```

Never rewrite this as a fake real-UAT PASS.

## 3. Email Platform

The shared Email Platform is closed as engineering infrastructure and is not an Access/Auth-owned mailer.

Current accepted path:

```text
DANTE feature mutation
+ durable EmailIntent
→ PostgreSQL COMMIT
→ claim / lease / bounded worker
→ protected versioned payload/template
→ provider-neutral adapter
→ SES API v2 / SMTP local-CI compatibility
→ provider evidence / suppression
```

Exact real-provider evidence: `development/email-platform-acceptance-2026-09-03.md`.

Production sender domain, SPF/DKIM/DMARC, production IAM/workload identity, SES production posture, live cloud feedback routing and reputation operations remain deployment work.

## 4. Immediate gate — pre-integration audit

Before merging main into this feature branch, verify and repair:

```text
documentation lifecycle
CURRENT vs historical classification
stale DEFERRED / OPEN / NEXT claims
protected-main vs branch-local status
Database System of Record
Database Dictionary + scope/schema
SQLAlchemy mappings
Alembic DAG/head
runtime ACL
frozen CP6 proof
Access/Auth + Email direct tests
OpenAPI/generated client
Web/backend regressions
```

No applied migration is rewritten to make the graphs look simpler.

## 5. Access/Auth ↔ protected-main convergence

Protected main currently owns Recovery on a different Alembic child of `20260826_08`:

```text
main
20260826_08
└── 20260830_09 recovery_material_state_retirement
```

Feature Access/Auth owns:

```text
20260826_08
└── 20260827_09
    └── 20260827_10
        └── 20260829_11
            └── 20260830_12
                └── 20260831_13
                    └── 20260903_14
                        └── 20260903_15
```

Integration policy:

```text
merge main into feature/access-auth
DO NOT rebase
DO NOT rewrite applied migrations
preserve both heads
add one normal forward Alembic merge revision
prove fresh DB + upgrade path + catalog parity
prove Recovery + Auth + Email behavior together
then PR to protected main
```

The combined topology is not pre-declared. Exact counts are accepted only after the merged branch is migrated and introspected against real PostgreSQL.

## 6. Platform observability integration after Access

`feature/platform-observability` is already source-closed and operationally accepted, but not integrated.

After Access/Auth lands on main:

```text
new protected main
→ merge into feature/platform-observability
→ resolve only real integration deltas
→ re-run release identity / redaction / correlation / CI checks
→ PR platform-observability → main
```

Do not recreate OTel/Alloy/Grafana/Faro/observer/dashboard/alert work that the observability branch has already proved.

## 7. Foundation state after both integrations

Target protected-main common base:

```text
Product / Domain / Logical / Physical
Engineering + Frontend foundations
PostgreSQL CP1–CP6
Recovery
Access/Auth
Email Platform
Platform Observability
```

At that point other product workstreams can branch from main without depending on Access/Auth or Observability feature branches.

## 8. Later Access maturity / M7

Later Access/security maturity remains future work, not a prerequisite for the current integration:

```text
session/device inventory
per-session revoke
revoke all others / logout everywhere
security-event history
new-login/security notifications
"this wasn't me" response
Security UI refinement/componentization
final authenticated Home handoff
release/accessibility/security polish
```

When this work starts, it should start from the enriched protected main on a new bounded branch.

## 9. M6 Native Mobile

Native Mobile remains **FUTURE / OPTIONAL / RE-GATE**.

Do not build mobile merely to advance a roadmap number. When the product priority is explicit, create a fresh branch from the then-current protected main and reuse the same backend Account/AuthSession/Email/Observability foundations.

## 10. Permanent integration rules

```text
protected main is the integration authority
feature branch truth must be clearly scoped until merged
applied Alembic revisions are immutable
Dictionary ≈ SQLAlchemy ≈ Alembic ≈ PostgreSQL ≈ current DB reference
no blind retry after ambiguous external effects
no network I/O in authoritative DB transactions
no generic Entity/EAV/JSONB semantic escape hatch
no fake PASS
```

## 11. Current authorities

```text
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/access-auth.md
docs/database/README.md
docs/database/access-auth.md
docs/database/dictionary/
docs/architecture/access-auth-*.md
docs/architecture/email-platform.md
docs/development/email-platform-acceptance-2026-09-03.md
docs/development/documentation-lifecycle-policy.md
```

Historical handoffs/reviews are evidence only and never override these current sources.