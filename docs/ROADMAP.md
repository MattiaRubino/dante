# DANTE Roadmap

- Status: **CURRENT**

## Completed architecture/design sequence

```text
Product / North Star
        CLOSED/CURRENT
          ↓
Domain Model
        CLOSED
          ↓
Logical Model
        CLOSED
          ↓
Pre-Physical Repository & Architecture Coherence
        CLOSED
          ↓
Physical Model / Target Selection
        CLOSED / ACCEPTED
          ↓
Current-truth dormant-component alignment
        COMPLETE
          ↓
Engineering Foundation v0
        CLOSED / ACCEPTED
```

Engineering Foundation replaces the previously considered standalone Development Profile phase. Tool/runtime/infrastructure activation now happens under the closed Foundation contract and the implementation boundary that actually needs the capability.

## Immediate next sequence

### 0. Repository identity governance

Keep the current repository; **do not create a new repository** for implementation.

Recommended small next operation:

```text
rename GitHub repository
lifeos → dante
```

The rename must be an explicit governance write. If intentionally deferred, document that defer and continue on the same repository.

### 1. Production repository/backend scaffold

Open a fresh bounded branch/write gate and create only real scaffold required for:

```text
apps/backend
Python 3.14.x / initial 3.14.7
uv + pyproject.toml + uv.lock + .python-version
src/dante
Ruff
mypy strict
pytest + Hypothesis baseline
architecture-test skeleton where an enforceable package graph exists
pydantic-settings bootstrap
SQLAlchemy + psycopg + Alembic bootstrap
LOCAL Docker Compose
DANTE-owned PostgreSQL 18.4 image/config
full selected PostgreSQL extension envelope enabled
initial migration harness
initial real PostgreSQL integration harness
initial GitHub Actions checks only where they can really execute
```

Do not create frontend implementation or unused remote-cloud scaffolding in this scope.

### 2. Scaffold QA

Before concrete schema work prove:

- exact changed paths;
- clean locked dependency bootstrap;
- backend can start in WSL/Linux;
- PyCharm WSL interpreter workflow remains straightforward;
- DANTE PostgreSQL image builds/starts;
- selected extensions are installed/enabled and versions inspectable;
- basic database connection works through selected driver/toolkit;
- migration harness can create/upgrade an empty DB baseline;
- initial unit/integration/architecture checks actually run;
- real emitted CI contexts are observed before any required-check activation.

No direct Physical HG/PSV PASS may be claimed unless the specific required scenario/artifact is actually executed.

### 3. Concrete Logical → PostgreSQL implementation

After scaffold PASS:

```text
consume closed Logical owner/ref/invariant contracts
        ↓
propose concrete physical mapping
        ↓
review schema/constraints/indexes/history semantics
        ↓
Alembic migration(s)
        ↓
real PostgreSQL tests
        ↓
persistence/application vertical slice
```

Do not mechanically translate 57 Logical owners into 57 tables/modules/services.

### 4. Backend vertical slices

Build capability-by-capability:

- explicit application use cases;
- expected-state/idempotency/governance semantics;
- transaction boundaries;
- persistence adapters;
- material history/provenance;
- HTTP adapter only after semantic/application boundary is sound;
- outbox/async effects when real Class-A use cases appear.

### 5. Frontend production engineering

Frontend internal engineering remains on its own workstream/branch after the current frontend design/prototype work is ready.

That scope will decide, against current evidence:

- production web/mobile internal structure;
- Node/package-manager/workspace/task tooling;
- detailed web/mobile testing;
- generated API-client consumption;
- mobile build/release/EAS posture;
- shared frontend package boundaries.

It consumes backend contracts; it does not reopen backend Foundation by default.

### 6. Capability-triggered Physical implementation

Activate selected components when their real feature boundary arrives:

```text
PowerSync + encrypted SQLite
→ real offline/multi-device implementation

R2
→ real ContentArtifact byte flow

OR-Tools
→ solver-backed planning capability

Restate
→ first real Class-B durable workflow

pgBackRest + AWS S3
→ recovery/production boundary or real recovery rehearsal
```

Applicable PSV obligations travel with activation.

### 7. Remote DEV

When LOCAL implementation has enough value to require real remote integration:

- compare current hosting/compute options;
- select provider and IaC engine deliberately;
- create isolated DEV only;
- use workload identity/secret manager/OIDC;
- deploy exact immutable artifact;
- validate remote config/network/provider wiring.

Do not materialize UAT/PROD merely to have empty enterprise-looking environments.

### 8. UAT

Activate when a real release candidate exists.

Use for:

- migration rehearsal;
- release deployment rehearsal;
- E2E/provider compatibility;
- performance/failure/security/recovery checks as applicable;
- release acceptance.

### 9. PROD

Activate at production readiness with:

- isolated production resources/identity/secrets;
- accepted recovery posture;
- observability/security release gates;
- exact candidate artifact/digest;
- controlled migration/release procedure;
- post-deploy verification.

## Persistent rule

```text
SELECTED ARCHITECTURE
!= IMPLEMENTED COMPONENT

DOCUMENTATION PASS
!= DIRECT IMPLEMENTATION PASS
```

The next conversation should start from the Engineering Foundation closure handoff rather than redesigning the same decisions.
