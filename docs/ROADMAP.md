# DANTE Roadmap

- Last updated: 2026-08-18
- Purpose: current delivery/architecture-stage sequence, not a calendar commitment

## Completed foundations

### Product / North Star

Accepted current DANTE identity/North Star and supporting product studies are integrated.

Naming continuity:

```text
CURRENT PRODUCT / APP NAME
DANTE

PREVIOUS WORKING / PROJECT NAME
LifeOS

LEGACY REFERENCES
Historical evidence, Git history and existing technical/repository identifiers
may still use LifeOS for the same product lineage.

RENAME IMPACT
Naming only — no Product North Star, Domain, Logical or Physical semantic change.
```

### Core Domain Model / Domain Atlas

**CLOSED — integrated into `main` via PR #10.**

```text
Whole-Domain PASS WITH HARDENING
POST-WRITE QA PASS
```

### Logical Model

**CLOSED — integrated into `main` via PR #11.**

```text
Whole-Logical PASS WITH HARDENING
REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active downstream
```

### Pre-Physical Repository & Architecture Coherence

**DEFINITIVE CLOSED / FINAL QA PASS / integrated / post-merge verified.**

```text
Phase 0–11         QA PASS
Phase 12           QA PASS / CLOSED
Independent audit  PASS
PR #13             Pre-Physical integration
PR #14             post-merge current-truth alignment
Physical base main 3de84bb49f9cef30e88e9bde4961ed84335daa79
```

### Physical Model target architecture

**CLOSED / SELECTED / ACCEPTED / INTEGRATED INTO `main` VIA PR #15.**

```text
PM-00  QA PASS
PM-01  PASS-CONDITIONAL
PM-02  COMPLETE
PM-03  STATIC COMPLETE / 0 REJECTS
PM-04A COMPLETE / 0 EXECUTION-WORTHY GAPS
PM-04B NOT ADMITTED
PM-05  COMPLETE
PM-06  EVIDENCE QUALIFICATION COMPLETE
PM-07  EVIDENCE QUALIFICATION COMPLETE
PM-08  SECONDARY/SPECIALIST QUALIFICATION COMPLETE
PM-09  EVIDENCE-WEIGHTED SCORING + SENSITIVITY COMPLETE
PM-10  FINAL STACK RECOMMENDATION COMPLETE
PM-11  EXPLICIT USER-APPROVED SELECTION COMPLETE
PM-12  ACCEPTED PHYSICAL MODEL COMPLETE
PM-13  CLEAN-ROOM ARCHITECTURE/DOCUMENTATION QA PASS
PM-14  BRANCH CLOSURE COMPLETE
PR #15  PROTECTED-MAIN INTEGRATION COMPLETE
PHYSICAL INTEGRATION COMMIT e6f191bad947388a44defe2c15f4939345084f58
FORMER  feature/physical-model MERGED / AUTO-DELETED
```

Selected canonical primary:

```text
PostgreSQL 18.4
```

Selected target companion architecture:

```text
PostGIS 3.6.4
pgvector 0.8.6
PostgreSQL native FTS / pg_trgm / unaccent
pg_stat_statements
PgBouncer 1.25.2
PowerSync 1.25.0 Open Edition
encrypted SQLite
PostgreSQL transactional outbox + bounded worker
Restate runtime
Cloudflare R2 Standard EU/private
pgBackRest 2.59.0
AWS S3 Standard eu-south-1 recovery target
OR-Tools 9.15 CP-SAT
OpenTelemetry + Grafana Alloy 1.18.0 + Grafana Cloud EU
```

Restate deployment is intentionally profile-dependent when Restate is activated:

```text
SELF-HOSTED
FIRST-CLASS

CLOUD EU
ALLOWED MANAGED OPTION

GLOBAL DEFAULT
NONE
```

Initial DEV activation is already fixed for two selected target components:

```text
RESTATE
DORMANT / NOT ACTIVE
ACTIVATE ON FIRST REAL CLASS-B DURABLE-WORKFLOW NEED
DEPLOYMENT MODE DECIDED ONLY AT ACTIVATION

pgBackRest + AWS S3 eu-south-1
DORMANT / NOT ACTIVE
ACTIVATE AT RECOVERY/PRODUCTION BOUNDARY
OR WHEN A REAL RECOVERY-REHEARSAL REQUIREMENT EXISTS
```

## Physical evidence truth retained

Target closure/integration does not mean direct implementation execution occurred.

```text
DATABASE DEPLOYMENT      NOT STARTED
FIXTURE/HARNESS           NOT STARTED
DIRECT HG PASS            0
LOW/BASE/HIGH            NOT RUN
RESTORE/MIGRATION         NOT RUN
FAILURE INJECTION         NOT RUN
POWERSYNC                 NOT RUN
RESTATE                   NOT RUN
OBJECT RECOVERY           NOT RUN
SOLVER                    NOT RUN
VERIFIED-RUN SCORE        NOT AVAILABLE
```

The mandatory direct selected-stack validation register remains active for implementation/release.

## Current next architecture/engineering track — Development Profile v0

The next separate operational-design scope decides **only how the already-selected Physical target is used where current activation posture has not already been fixed**.

Expected questions include:

```text
which still-unresolved selected components are active immediately
which other components remain dormant until their first real capability need
self-hosted vs managed only where an active component requires the choice now
accounts/credentials/environment setup
initial observability activation
upgrade/production triggers
```

This profile must not silently change the accepted Physical target.

Two day-1 questions are already closed and must not be reopened:

```text
Restate active now?                 NO — DORMANT UNTIL REAL CLASS-B NEED
Restate self-hosted vs Cloud EU?    NOT YET — DECIDE ONLY AT ACTIVATION
pgBackRest/AWS S3 active now?       NO — DORMANT UNTIL RECOVERY/PRODUCTION BOUNDARY
```

## Backend Foundation — later explicit authorization

Backend Foundation remains:

```text
NOT STARTED / DEFERRED
```

Physical closure/integration removes the persistence-selection blocker, but backend production implementation still requires its own explicit authorization/gate. Development Profile v0 may be established first so the actual initial infrastructure/deployment posture is deliberate rather than improvised.

## Active parallel product/design track

### Phase 4 — UX prototype/product-structure validation

Separate workstream on `prototype/phase-4-today-home`.

It may continue independently but does not redefine accepted Domain/Logical/Physical authority.

## Upstream constraints that remain active

Later engineering must preserve:

- CLOSED Domain Atlas and final closure/language authority;
- CLOSED Whole Logical Model + complete decision register + `WL-H01..WL-H12`;
- accepted Physical Model ownership/topology boundaries;
- Phase 5 AuthN/AuthZ, security/privacy/retention/recovery, consistency/side-effects and NFR/multi-device/recovery requirements;
- Phase 6 AI/context/runtime and Integration Hub boundaries;
- consequential AI behavior-change evaluation requirement;
- Phase 7 durable-execution contract as physically resolved by PM-11/12;
- Phase 8 governed operation/effect contract;
- Phase 9 search/observability/calendar/solver contract as physically resolved where selected;
- calendar/provider adapter separation;
- selected-stack direct validation obligations;
- repository engineering safety.

```text
SEMANTIC OWNER != IMPLEMENTATION MECHANISM
DOMAIN TERM != ENGINE
ADDRESSABILITY != DOMAIN IDENTITY
STORAGE COINCIDENCE != SEMANTIC EQUIVALENCE
SELECTED != DIRECT PASS
SELECTED != DEPLOYED
```

## Current accepted runtime/search/solver posture

```text
DURABLE EXECUTION
bounded async → PostgreSQL outbox + bounded worker
material durable Class-B → Restate runtime
initial DEV Restate → DORMANT until first real Class-B need
Restate deployment → self-hosted or Cloud EU, decided only when activated

RECOVERY
pgBackRest + AWS S3 eu-south-1 → selected production/off-site target
initial DEV → DORMANT until recovery/production boundary or real rehearsal need

SEARCH
PostgreSQL native FTS + pg_trgm + unaccent
semantic/vector retrieval → pgvector
no dedicated search/vector service in accepted target

OBSERVABILITY
OpenTelemetry + Grafana Alloy + Grafana Cloud EU target

CALENDAR
iCalendar / JSCalendar / providers = adapter pressure, not ontology

SOLVER
OR-Tools 9.15 CP-SAT selected
UNKNOWN != INFEASIBLE
solver output != accepted canonical effect
```

## AI evaluation posture

Material consequential changes to model/version/provider, prompt/instruction layer, Context Builder policy, tool/action schema, tool-selection policy or fallback/routing policy require versioned/reproducible evaluation before promotion.

```text
eval result != canonical DANTE truth
eval PASS != Authority / governed-effect authorization
```

## Repository engineering safety

`main` remains protected by `lifeos-main-safety`. Physical integration used the normal protected PR path through PR #15. No direct-main bypass, no invented required checks and no production secrets/personal data in test/evidence artifacts.

## Immediate sequence

```text
1. Development Profile v0 — separate bounded operational-design scope
2. identify only genuinely unresolved initial activation/deployment/configuration choices
3. preserve Restate and pgBackRest/AWS S3 as initial-DEV dormant until their fixed triggers
4. later Backend Foundation authorization when explicitly approved
5. discharge applicable direct selected-stack validation obligations at their proper implementation/release gates
```