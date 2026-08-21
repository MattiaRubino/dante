# DANTE Roadmap

- Status: **CURRENT**

## Completed architecture / design sequence

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

## Active implementation workstreams

### Frontend production materialization — ACTIVE

Branch:

`feature/frontend-materialization`

The closed Frontend Foundation is being materialized under its own bounded workstream. Direct frontend PASS is earned only by the real carried validations; active branch status is not evidence by itself.

Frontend and backend may progress in parallel through separate worktrees. Shared repository/global documentation must be reconciled semantically when either workstream integrates.

### Backend production scaffold — ACTIVE

Branch:

`feature/backend-scaffold`

Current checkpoint truth:

```text
CP1 Python/process/config
CLOSED / DIRECT QA PASS

CP2 reproducible LOCAL PostgreSQL
CLOSED / DIRECT QA PASS

CP3 persistence/migrations/privileges/real PostgreSQL
CLOSED / DIRECT QA PASS

CP4 quality / CI enforcement
DESIGN CLOSED
M1 CLOSED
M2 MATERIALIZED / REMOTE READBACK PASS
M3 DIRECT LOCAL QA PASS
M4 CURRENT MAIN RECONCILED
POST-MERGE REGRESSION QA NEXT
REMOTE PR CALIBRATION NOT RUN

CP5 full scaffold QA / closure
NOT STARTED
```

CP4 materialized:

```text
Backend CI
├── Backend Quality
├── Backend PostgreSQL
└── Backend CI Gate

Dependency Review
└── separate repository-wide workflow

Dependabot
├── uv
└── GitHub Actions
```

Required status checks remain **0** until real remote calibration proves stable emitted contexts and failure semantics.

## Immediate backend sequence

### 1. CP4 post-main reconciliation regression

Run on the reconciled branch:

- exact locked uv bootstrap;
- Ruff format/lint;
- mypy strict;
- non-PostgreSQL tests;
- backend build;
- canonical `dante-postgres-local:18.4` rebuild;
- PostgreSQL-marked acceptance.

Do not infer PASS from the pre-merge M3 run.

### 2. CP4 real PR green calibration

After regression PASS, open the real PR to current protected `main` and observe:

```text
Backend Quality
Backend PostgreSQL
Backend CI Gate
Dependency Review
```

Record exact emitted contexts/source and real logs.

### 3. CP4 deliberate red

Under a separately bounded calibration change, prove:

- mandatory upstream failure makes `Backend CI Gate` fail;
- Dependency Review detects the intended dependency-policy violation;
- a real `uv.lock` dependency delta is visible/evaluated before Dependency Review can be promoted.

### 4. CP4 recovery green

Restore the branch without weakening policy and prove all intended checks green again.

### 5. Required-check / repository settings decision

Only after green → red → recovery green:

- consider stable required contexts;
- bind expected GitHub Actions source where supported;
- consider repository full-SHA enforcement where supported;
- reread effective rules/protection after any mutation.

No required check is configured merely because YAML exists.

### 6. CP4 closure

Record `CLOSED / DIRECT QA PASS` only when the CP4 acceptance matrix is truthfully satisfied or an item is explicitly deferred as unsupported/out of boundary.

### 7. CP5 scaffold QA / closure

Perform the final integrated scaffold acceptance/handoff.

### 8. Concrete Logical → PostgreSQL implementation

Only after scaffold closure:

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

## Product vertical slices

Production product surfaces begin only after the relevant frontend/backend foundations, scaffolds and contracts exist. Prototype UX remains evidence/oracle; production implementation follows accepted feature/data/UI boundaries.

## Capability-triggered Physical implementation

Activate specialist components only at real requirements. Applicable validation obligations travel with activation:

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

## Remote environments

```text
LOCAL
→ current implementation boundary

DEV
→ activate when shared remote integration provides real value

UAT
→ activate for real release candidates

PROD
→ activate only at production readiness
```

Backend hosting/compute, IaC and remote sizing remain deliberate decisions at the first real remote-infrastructure boundary.

## Persistent rules

```text
SELECTED ARCHITECTURE != IMPLEMENTED COMPONENT
DOCUMENTATION PASS != DIRECT IMPLEMENTATION PASS
CLIENT LOCAL STATE != CANONICAL EFFECT AUTHORITY
ENVIRONMENT != GIT BRANCH
WORKFLOW EXISTS != REQUIRED CHECK PROVEN
```

Continue from durable contracts/handoffs rather than redesigning closed decisions from conversation memory.