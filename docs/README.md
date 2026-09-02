# DANTE Documentation Index

- **Status:** CURRENT NAVIGATION / AUTHORITY INDEX
- **Last reconciled:** 2026-09-02
- **Active branch-local vertical:** `feature/access-auth`

This directory is the durable documentation surface for DANTE. Current specifications describe present truth directly; historical handoffs and phase-time evidence do not silently override current operational documents.

## 1. Authority order

When sources conflict, prefer the narrowest accepted current authority for the subject:

```text
1. executable repository truth
   code / migrations / tests / governed generated artifacts

2. accepted semantic + architectural authority
   Product / Domain / Logical / Physical / ADRs / durable contracts

3. current subsystem reference
   database / frontend / backend / security / API contracts

4. current operational status
   PROJECT-STATUS / ROADMAP / active workstream / current review

5. historical handoffs / milestone reconciliation / Git chronology

6. conversation memory
```

Protected `main` remains integrated authority for closed shared foundations. `feature/access-auth` contains newer branch-local truth for the bounded Access/Auth vertical until explicit integration.

## 2. Current lifecycle

```text
PRODUCT / NORTH STAR                 CURRENT
DOMAIN MODEL                         CLOSED
LOGICAL MODEL                        CLOSED / 57 OF 57
PHYSICAL TARGET                      CLOSED / ACCEPTED
ENGINEERING FOUNDATION               CLOSED / ACCEPTED
FRONTEND FOUNDATION                  CLOSED / ACCEPTED
BACKEND CP1–CP6                      CLOSED / ACCEPTED
POSTGRESQL                           18.6

ACCESS/AUTH M1–M4                    CLOSED / ACCEPTED
M5.1 / M5.2 / M5-A–D                 COMPLETE
M5 GROUPS 1–3                        COMPLETE / ENGINEERING PASS
M5 GROUP 4 ENGINEERING               AUTOMATED QA PASS
LOCAL PASSWORD/PASSKEY UAT           PASS
REAL GOOGLE UAT                      PASS
REAL INTERNET EMAIL DELIVERY         OPEN
REAL APPLE UAT                       DEFERRED / OPEN
WHOLE M5                             ACTIVE / NOT FORMALLY CLOSED

ACCESS/AUTH ALEMBIC                  20260831_13
ACCESS/AUTH TOPOLOGY                 83/5/15/75/156/85/233
```

## 3. Mandatory continuation entry points

Read in this order:

1. `../README.md`
2. `PROJECT-STATUS.md`
3. `ROADMAP.md`
4. `development/agent-operating-manual.md`
5. `workstreams/access-auth.md`
6. `workstreams/access-auth-m5-review-2026-09-02.md`
7. subject authority relevant to the task
8. current Git branch/ref and its relation to protected `main`

For Access/Auth architecture/security/API/testing:

- `architecture/access-auth-architecture.md`
- `architecture/access-auth-security-contract.md`
- `architecture/access-auth-api-contract.md`
- `architecture/access-auth-testing-contract.md`
- `architecture/access-auth-m4-contract.md`
- `architecture/access-auth-m5-contract.md`
- `architecture/access-auth-m5-persistence-api-contract.md`
- `decisions/ADR-011-access-auth-architecture.md`

For current product/reference state:

- `frontend/access.md`
- `database/README.md`
- `database/access-auth.md`
- `../apps/backend/README.md`

## 4. Progress-metadata reconciliation

Some large durable M5 contracts contain milestone-time sections such as `M5-F NEXT` or `public routes later`. Those statements are preserved as historical reconciliation of the slice in which they were written. They are **not current progress authority** when they conflict with `PROJECT-STATUS.md`, `ROADMAP.md`, the active workstream or the 2026-09-02 review.

This distinction avoids destroying valuable design rationale merely to update chronology.

The old dated file `workstreams/access-auth-m5-live-handoff-2026-08-29.md` is explicitly superseded/historical.

## 5. Product / Domain / Logical / Physical

Product entry point:

- `product/README.md`
- `product/product-identity-and-north-star.md`

Domain:

- `domain/README.md`

Logical:

- `logical-model/README.md`
- `logical-model/whole-logical-model-v1.md`

Physical:

- `physical-model/README.md`

Permanent cross-model invariants remain binding unless deliberately superseded through an accepted architecture gate.

## 6. Architecture

Start at `architecture/README.md`.

Important ADRs:

- `decisions/ADR-007-domain-model-informed-persistence-boundaries.md`
- `decisions/ADR-008-frontend-engineering-stack.md`
- `decisions/ADR-009-frontend-architecture-boundaries.md`
- `decisions/ADR-010-postgresql-persistence-constitution.md`
- `decisions/ADR-011-access-auth-architecture.md`

## 7. Database

Start at:

- `database/README.md`
- `database/access-auth.md`
- `database/dictionary/README.md`

Current Access/Auth branch DB:

```text
PostgreSQL          18.6
Alembic             20260831_13
83 tables
5 views
15 routines
75 triggers
156 physical indexes
85 foreign keys
233 CHECK constraints
103 standalone Dictionary entries
```

Permanent rule:

```text
human DB reference
≈ Dictionary
≈ SQLAlchemy
≈ Alembic
≈ real PostgreSQL
≈ direct tests
```

## 8. Frontend

Start at:

- `frontend/README.md`
- `frontend/access.md`
- `frontend/home/current-checkpoint.md`
- `frontend/home/contract.md`

Access is now a real full-stack Auth surface on `feature/access-auth`; old pre-backend statements are historical baseline context, not current runtime truth.

## 9. Testing / proof

Access/Auth proof deliberately separates:

```text
unit/application
PostgreSQL
HTTP/OpenAPI/generated client
browser full-stack
real provider/authenticator UAT
```

The 2026-09-02 review records 68/68 Web unit/component tests, 60/60 Auth browser tests, real Windows Hello passkey UAT and real Google UAT.

## 10. Current open research

The next architecture research is outbound transactional/security email. No vendor is selected yet. The research must cover provider-vs-internal responsibility, deliverability/DNS, feedback loops, retry ambiguity, observability, privacy and Apple relay requirements before implementation/provider choice.

## 11. Documentation lifecycle

Current docs are not an append-only diary. Historical evidence remains recoverable in Git; current subject/index documents should not carry stale `NEXT/TBD/NOT IMPLEMENTED` claims after their trigger is satisfied.

Repository truth beats conversation memory.