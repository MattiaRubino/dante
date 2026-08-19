# Environments and Promotion v0

- Status: **CLOSED / ACCEPTED**
- Scope: LOCAL / DEV / UAT / PROD lifecycle, isolation and promotion
- Cloud/compute provider: **DEFERRED**

## 1. Environment vocabulary

DANTE uses exactly these promotion/lifecycle contexts:

```text
LOCAL
individual developer execution context
not a remote deployment stage

DEV
shared remote integration environment

UAT
production-like release-candidate/acceptance environment

PROD
real released environment and real user data
```

Automated tests may use a `TEST` execution context, but TEST is not a fifth promotion environment.

Optional ephemeral preview environments may be added when useful. Preview is not part of the durable DEV→UAT→PROD chain.

## 2. Environment != Git branch

Protected `main` is the integrated source truth.

No permanent `develop`, `staging` or `production` Git branch is introduced.

Normal source flow:

```text
bounded feature/fix/chore branch
        ↓ PR + validation
protected main
```

Deployment state is represented by exact source/build/artifact/environment identity, not parallel source histories.

## 3. Activation sequence

The architecture defines all environments now but materializes them progressively.

```text
LOCAL
active from first production implementation

DEV
remote activation only when shared/remote integration is useful

UAT
activation when real release candidates need acceptance/rehearsal

PROD
activation at production-readiness / real-user boundary
```

This preserves enterprise-grade separation without paying/operating unused remote environments prematurely.

## 4. LOCAL

LOCAL optimizes developer feedback while preserving server/database semantics that matter.

Baseline:

- Windows 11 host is supported;
- canonical backend execution semantics are Linux through WSL2 on Windows;
- backend repository/worktree used by server tooling is kept in WSL filesystem;
- Python backend runs directly in WSL/Linux for normal reload/debug;
- Docker Compose runs stateful selected dependencies;
- PostgreSQL is real PostgreSQL 18.4, not SQLite substitution;
- full selected PostgreSQL extension envelope is installed/enabled from the first LOCAL DB;
- data/credentials are synthetic/non-production;
- local state is disposable/rebuildable from migrations/fixtures where applicable;
- ignored `.env.local` may provide LOCAL convenience only.

LOCAL does not need to run every future specialist service before its implementation exists.

## 5. DEV

DEV is the first shared remote integration environment once activated.

Purpose:

- run accepted-main backend artifacts remotely;
- validate remote networking/config/provider integration;
- provide stable non-production endpoints to real clients/integration tests;
- expose failures that LOCAL cannot reproduce truthfully.

Rules:

- deploy accepted `main` artifact, not arbitrary workstation code;
- DEV state/credentials are DEV-only;
- synthetic/shared test data by default;
- no raw production database copy for convenience;
- reset/destructive procedures remain controlled and traceable;
- DEV does not possess PROD credentials.

Auto-deploy from accepted `main` is a target only after real deployment automation proves stable. Before that, any manual deployment remains traceable to exact commit/artifact identity.

## 6. UAT

UAT is a release-candidate environment, not a second development sandbox.

Purpose:

- end-to-end acceptance;
- migration rehearsal;
- deployment/release rehearsal;
- provider integration verification;
- supported-client compatibility verification;
- applicable security/performance/recovery/PSV checks;
- final release evidence before PROD.

UAT resembles PROD topology/configuration behavior as far as practical without using PROD credentials or ad-hoc raw PROD data.

A UAT PASS belongs to an exact candidate and evidence basis.

## 7. PROD

PROD contains real released service state and real user data.

Rules:

- deploy only an accepted exact release candidate;
- use PROD-only identities/secrets/resources;
- do not share state with DEV/UAT;
- serialize release/migration operations where concurrent mutation is unsafe;
- activate recovery/observability/security controls required by the production boundary;
- reconcile emergency manual infrastructure repair back to versioned desired state;
- direct console changes do not create a second infrastructure authority.

## 8. Environment isolation

Each remote environment is independently addressed, credentialed and stateful.

Target minimum:

```text
DEV DB != UAT DB != PROD DB
DEV object namespace/resource != UAT != PROD
DEV credentials != UAT != PROD
DEV secrets != UAT != PROD
DEV deployment identity != UAT != PROD
DEV telemetry environment != UAT != PROD
```

Using multiple schemas inside one production database is not the default substitute for environment isolation.

## 9. Provider-native security boundary

The exact provider is not selected yet.

When chosen, DANTE prefers the provider's strong administrative/security isolation primitive where operationally reasonable, e.g. conceptually:

```text
AWS    separate accounts
Azure  separate subscriptions/resource security boundaries
GCP    separate projects
other  equivalent provider-native isolation unit
```

The principle is provider-neutral: limit blast radius and prevent lower environments from possessing production privilege.

A weaker shared boundary requires an explicit reason and compensating controls; it is not the default merely because the team is small.

## 10. GitHub Environments

When remote deployment workflows exist, GitHub Environments are used for:

```text
dev
uat
prod
```

They control deployment workflow identity/variables/secrets/protection/history as supported.

GitHub Environment is a deployment-control boundary; it is **not** the cloud runtime itself. Cloud/provider resources remain separate execution/data boundaries.

Human approval requirements reflect real independent reviewer capacity. DANTE does not create a fake multi-reviewer ceremony while there is one active developer.

## 11. Artifact identity

Future backend/server artifacts are immutable.

Required identity includes, as available:

```text
Git source SHA
build ID
OCI/artifact digest
release/version
migration revision/head
configuration/environment identity
```

Mutable tags such as `latest` are navigation aids only, never sufficient release evidence.

## 12. Build once, promote exact artifact

Server default:

```text
accepted source
→ build once
→ validate immutable artifact
→ deploy exact artifact to DEV
→ select exact candidate
→ promote exact candidate to UAT
→ promote exact candidate to PROD
```

Environment-specific runtime configuration is supplied externally.

A platform that fundamentally requires environment-specific build output is an explicit exception and must preserve source/toolchain/config traceability.

Frontend/mobile artifact semantics are deferred to the frontend workstream.

## 13. Release-candidate identity

A release candidate is not “whatever main is now”.

Record at least:

```text
source commit
build ID
artifact digest
migration head
configuration/environment identity
```

A later commit on `main` does not mutate an in-flight candidate. A fix creates a new commit/artifact and re-enters validation.

## 14. Database migration promotion

When migrations exist:

```text
CI validates migration graph / empty→head / drift / risk
        ↓
DEV controlled migration + deploy + smoke
        ↓
UAT migration rehearsal + deploy + E2E
        ↓
PROD preflight
        ↓
one serialized migration/release operation
        ↓
compatible application rollout
        ↓
post-deploy validation
```

Application replicas do not independently race Alembic at startup.

Expand/migrate/contract changes may span multiple releases.

## 15. Rollback / forward-repair

`alembic downgrade` is not a universal production rollback strategy.

Possible recovery actions include:

- redeploy previous compatible application artifact;
- approved feature/operational control where one exists;
- forward repair migration;
- data repair/reconciliation job;
- accepted restore/PITR path for destructive data failure.

Risky release evidence states what path actually exists.

## 16. Deployment concurrency

- superseded non-deployment PR CI may be cancelled where safe;
- deployment per environment is serialized where migrations/resource mutation make concurrency unsafe;
- in-progress critical production mutation is not blindly cancelled because a newer commit arrived.

## 17. Data policy by environment

```text
LOCAL
synthetic/developer-owned non-sensitive data

DEV
synthetic/shared test/demo data

UAT
representative synthetic or explicitly sanitized/minimized acceptance data

PROD
real data under production privacy/security controls
```

Production-derived data in lower environments requires a deliberate sanitization/minimization/authorization process. Raw ad-hoc dumps are forbidden by default.

## 18. Infrastructure-as-code

Once durable remote infrastructure exists:

- intended state is version controlled/reviewable;
- secrets remain external;
- drift is detected/reconciled where chosen tooling supports reliable mechanisms;
- emergency manual changes are documented and reconciled;
- provider and IaC engine are selected/pinned through the first remote-infrastructure scope.

## 19. Specialist service activation

Environment design does not force every selected Physical component to exist everywhere on day one.

Key fixed posture:

- PostgreSQL: active with first backend persistence;
- selected PostgreSQL extension envelope: enabled from first LOCAL DB and reproduced in later DB environments as persistence deploys;
- PowerSync: activates with real mobile/offline implementation;
- R2: activates with real ContentArtifact byte handling;
- OR-Tools: activates with solver-backed capability;
- Restate: dormant until first real Class-B durable workflow;
- pgBackRest + AWS S3: dormant until recovery/production boundary or real rehearsal.

Activation never cancels applicable PSV obligations.

## 20. Promotion evidence rule

Every PASS claim is scoped to what actually ran.

```text
PR PASS != UAT PASS
migration rehearsal PASS != recovery PASS
UAT E2E PASS != complete PSV PASS
selected target != deployed component
```
