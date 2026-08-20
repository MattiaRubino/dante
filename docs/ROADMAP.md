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
        PASSO 1 PASS
        PASSO 2 PASS
        PASSO 3 FINAL REVIEW PASS
        DESIGN / ARCHITECTURE CLOSED / ACCEPTED
        INTEGRATED VIA PR #22
```

Architecture closure remains distinct from implementation/direct validation.

## Immediate next sequence

### 1. Frontend production materialization

Frontend Foundation is integrated on `main` via PR #22. Open a fresh exact scope to create only real artifacts required for the accepted baseline:

```text
root JS workspace manifests/config
apps/web
apps/mobile
only real shared packages
architecture lint/boundary/cycle enforcement
selected test scaffolds that can actually run
```

Materialization progressively validates Node/pnpm/Turbo, Vite, Expo/RN, package exports/boundaries/cycles, generated tokens, Orval when real OpenAPI exists, TanStack Form, PowerSync/OP-SQLite/SQLCipher, WSL↔Android tooling, runtime config and Cloudflare/EAS/Sentry only at applicable activation boundaries.

No dormant specialist receives placeholder infrastructure.

### 2. Backend production scaffold — separate workstream

Backend scaffold remains **NOT STARTED** and independent from Frontend Foundation closure/integration.

When separately authorized, materialize only real backend scaffold required by the closed Engineering Foundation under accepted `infra/` ownership.

### 3. Concrete Logical → PostgreSQL implementation

After backend scaffold QA, consume closed Logical contracts, review mappings, implement migrations, test against real PostgreSQL and build capability vertical slices.

### 4. Product vertical slices

Production product surfaces begin only after relevant frontend/backend foundations and contracts exist.

Prototype UX remains evidence/oracle; production implementation follows accepted feature/data/UI boundaries.

### 5. Capability-triggered Physical implementation

Activate specialist components only at real requirements. Applicable validation obligations travel with activation.

### 6. Remote DEV

Activate shared remote integration only when LOCAL implementation benefits. Backend hosting/compute and IaC remain deliberate decisions at that boundary.

### 7. UAT

Activate for real release candidates and applicable release/provider/performance/security/recovery rehearsal.

### 8. PROD

Activate at production readiness with isolated production resources/identity/secrets and exact accepted artifacts.

## Persistent rules

```text
SELECTED ARCHITECTURE != IMPLEMENTED COMPONENT
DOCUMENTATION PASS != DIRECT IMPLEMENTATION PASS
CLIENT LOCAL STATE != CANONICAL EFFECT AUTHORITY
ENVIRONMENT != GIT BRANCH
```

Continue from durable closure/handoff sources rather than redesigning closed decisions from chat memory.
