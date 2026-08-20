# DANTE Roadmap

- Status: **CURRENT**

## Completed architecture/design sequence

```text
Product / North Star
        CURRENT
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
Engineering Foundation v0
        CLOSED / ACCEPTED
          ↓
Frontend Engineering Foundation
        PASSO 1 DESIGN COMPLETE
        PASSO 2 DESIGN COMPLETE
        PASSO 3 CLEAN REVIEW IN PROGRESS
```

Engineering Foundation replaced the previously considered standalone Development Profile phase. Runtime/infrastructure activation occurs at the implementation boundary that actually needs it.

## Immediate next sequence

### 1. Frontend Foundation Passo 3

Perform one clean whole-foundation review across:

```text
Passo-1 technology selections
+
Passo-2 architecture/ownership boundaries
+
closed Product/Domain/Logical/Physical/Engineering constraints
```

If blocking design/documentation defects are zero:

```text
record Frontend Foundation design/architecture closure
→ prepare protected-main integration
```

Do not require a pre-closure mega PSV. Direct implementation validation is carried into materialization.

### 2. Protected-main integration

Frontend Foundation remains branch-local until reviewed integration.

PR/merge follows normal repository safety:

- exact changed paths;
- branch relation to main;
- real checks if applicable;
- expected-head merge protection;
- post-merge readback;
- branch lifecycle verification.

No PR or merge is implied without explicit authorization.

### 3. Frontend production materialization

Only after Foundation integration, open a new exact scope to create real artifacts required for the selected/accepted baseline:

```text
root JS workspace manifests/config
apps/web
apps/mobile
only real shared packages
architecture lint/boundary enforcement
selected test scaffolds that can really run
```

Materialization progressively validates Node/pnpm/Turbo, Vite, Expo/RN, package exports/boundaries, generated tokens, Orval when real OpenAPI exists, TanStack Form, PowerSync/OP-SQLite/SQLCipher, WSL↔Android tooling, Web runtime config, Cloudflare/EAS/Sentry only at their activation boundaries.

Do not create placeholder packages/directories for dormant specialists.

### 4. Backend production scaffold — separate workstream

Backend scaffold remains **NOT STARTED** and independent from Frontend Foundation closure.

When authorized, create only real backend scaffold required by the already-closed Engineering Foundation:

- `apps/backend`;
- Python/uv/tooling;
- typed config;
- SQLAlchemy/psycopg/Alembic;
- LOCAL Compose/PostgreSQL under accepted `infra/` ownership;
- real PostgreSQL test/migration harness;
- only CI checks that can actually execute.

### 5. Concrete Logical → PostgreSQL implementation

After backend scaffold QA, consume closed Logical owner/ref/invariant contracts, review concrete mapping, implement migrations, test against real PostgreSQL and build persistence/application vertical slices.

Do not mechanically translate 57 Logical owners into 57 services/modules/tables.

### 6. Product vertical slices

Production product surfaces begin only after the relevant frontend/backend foundations and contracts exist.

Prototype UX is evidence/oracle; production implementation is deliberate and follows accepted feature/data/UI boundaries.

### 7. Capability-triggered Physical implementation

Activate selected specialist components only at real requirements:

```text
PowerSync + encrypted SQLite
→ mobile/local-offline capability and later Web only if explicitly activated

R2
→ ContentArtifact byte flow

OR-Tools
→ solver-backed capability

Restate
→ first Class-B durable workflow

pgBackRest + AWS S3
→ recovery/production boundary or real rehearsal
```

Applicable validation obligations travel with activation.

### 8. Remote DEV

Activate shared remote integration only when LOCAL implementation benefits from it. Select backend hosting/compute and IaC deliberately at that boundary; use isolated state/identity/secrets and immutable artifact deployment.

### 9. UAT

Activate for real release candidates and applicable migration/release/E2E/provider/performance/security/recovery rehearsal.

### 10. PROD

Activate at production readiness with isolated production resources/identity/secrets, accepted recovery/observability/security posture and exact candidate artifacts.

## Persistent rules

```text
SELECTED ARCHITECTURE != IMPLEMENTED COMPONENT
DOCUMENTATION PASS != DIRECT IMPLEMENTATION PASS
CLIENT LOCAL STATE != CANONICAL EFFECT AUTHORITY
ENVIRONMENT != GIT BRANCH
```

Continue from durable workstream handoffs rather than redesigning closed decisions from chat memory.
