# DANTE Documentation Index

- **Status:** CURRENT NAVIGATION / AUTHORITY INDEX
- **Last reconciled:** 2026-09-03
- **Active branch:** `feature/access-auth`
- **Current work:** PRE-INTEGRATION AUDIT

This directory is the durable documentation surface for DANTE. Current specifications describe present truth directly; historical checkpoints never silently override current operational documents.

## 1. Authority order

When sources conflict, use the narrowest accepted current authority:

```text
1. executable/materialized repository truth
   code / migrations / tests / governed generated artifacts / real schema evidence

2. accepted semantic + architectural authority
   Product / Domain / Logical / Physical / constitutions / ADRs / durable contracts

3. current subsystem reference
   database / frontend / backend / security / API contracts

4. current operational routing
   PROJECT-STATUS / ROADMAP / active workstream

5. evidence / historical checkpoints / Git chronology

6. conversation memory
```

Protected `main` owns integrated shared truth. `feature/access-auth` currently owns newer branch-local Access/Auth + Email Platform truth until the integration gate completes.

## 2. Current lifecycle

```text
PRODUCT / NORTH STAR                    CURRENT
DOMAIN / LOGICAL / PHYSICAL             CLOSED
ENGINEERING / FRONTEND FOUNDATION       CLOSED / ACCEPTED
BACKEND CP1–CP6                         CLOSED / ACCEPTED
POSTGRESQL                              18.6

PROTECTED MAIN
  Recovery                              CLOSED / INTEGRATED
  Alembic                               20260830_09

FEATURE/ACCESS-AUTH
  M1–M5                                 CLOSED / ACCEPTED
  local password/passkey UAT            PASS
  real Windows Hello UAT                PASS
  real Google UAT                       PASS
  real Apple external UAT               BOUNDED DEFERRED / NON-BLOCKING
  shared Email Platform                 CLOSED / ACCEPTED
  real SES signup/recovery/notification PASS
  Alembic                               20260903_15
  DB topology                           87/5/15/75/170/88/267
  work                                  PRE-INTEGRATION AUDIT

M6 Native Mobile                        FUTURE / OPTIONAL
later Access/M7 maturity                FUTURE
```

## 3. Mandatory continuation entry points

Read in this order:

1. `../README.md`
2. `PROJECT-STATUS.md`
3. `ROADMAP.md`
4. `development/agent-operating-manual.md`
5. `development/documentation-lifecycle-policy.md`
6. `workstreams/access-auth.md` while this branch remains active
7. subsystem authority relevant to the task
8. exact current Git branch/ref and its relation to protected main

## 4. Access/Auth authorities

Architecture/security/API/testing:

- `architecture/access-auth-architecture.md`
- `architecture/access-auth-security-contract.md`
- `architecture/access-auth-api-contract.md`
- `architecture/access-auth-testing-contract.md`
- `architecture/access-auth-m4-contract.md`
- `architecture/access-auth-m5-contract.md`
- `architecture/access-auth-m5-persistence-api-contract.md`
- `decisions/ADR-011-access-auth-architecture.md`

Current implementation/reference:

- `workstreams/access-auth.md`
- `frontend/access.md`
- `database/access-auth.md`
- `../apps/backend/README.md`

Evidence:

- `workstreams/access-auth-m5-review-2026-09-02.md`

Large M5 contracts contain milestone-time phrases such as `M5-F NEXT` or `public routes later`. Those sections preserve the implementation decomposition at that checkpoint; they do **not** override current status documents now that M5 is closed.

## 5. Shared Email Platform authorities

- `architecture/email-platform.md` — platform architecture
- `architecture/access-auth-email-delivery.md` — Access/Auth consumer integration only
- `decisions/ADR-012-email-delivery-platform.md`
- `development/email-platform-local-uat.md`
- `development/email-platform-acceptance-2026-09-03.md`
- `database/dictionary/tables/email_delivery_intent.json`
- `database/dictionary/tables/email_delivery_attempt.json`
- `database/dictionary/tables/email_provider_event.json`
- `database/dictionary/tables/email_recipient_suppression.json`

Email Platform is shared DANTE technical infrastructure. Access/Auth is its first consumer, not its architectural owner.

Engineering + real-provider UAT is closed. Production sender-domain/DNS/reputation/workload-identity/cloud-event deployment remains a separate operations gate.

## 6. Database authorities

Start at:

- `database/README.md` — current Database System of Record
- `database/access-auth.md` — current branch Auth/Email database reference
- `database/dictionary/README.md` — machine-readable contract
- `development/backend-cp6-02-postgresql-persistence-constitution.md`
- `decisions/ADR-010-postgresql-persistence-constitution.md`

Permanent invariant:

```text
current human DB reference
≈ Database Dictionary
≈ SQLAlchemy mappings
≈ Alembic
≈ real PostgreSQL
≈ direct tests
```

### Whole-database Blueprint corpus

`database/dante-postgresql-database.md` and its continuation parts contain deep CP6 derivation/design/closure rationale. They remain valuable reference history, but old phase banners and historical `OPEN/NEXT/NOT MATERIALIZED` statements inside that corpus are not current operational routing when later accepted work has satisfied their trigger.

For present materialized truth, use `database/README.md`, current subsystem DB references, Dictionary, migrations/mappings and direct PostgreSQL proof.

## 7. Product / Domain / Logical / Physical

Product:

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

## 8. Frontend

Start at:

- `frontend/README.md`
- `frontend/access.md`
- `frontend/home/current-checkpoint.md`
- `frontend/home/contract.md`

Access is a real full-stack Auth surface on the branch; old statements that it is still pre-backend are historical context only.

## 9. Current integration sequence

```text
pre-integration audit on feature/access-auth
→ merge protected main into feature/access-auth
→ reconcile divergent Alembic histories with forward merge revision
→ combined Recovery + Access/Auth + Email QA
→ PR Access/Auth + Email Platform to protected main
→ merge enriched main into feature/platform-observability
→ observability integration/release rechecks
→ PR observability to protected main
→ future bounded product branches from enriched main
```

No M6/M7 feature expansion belongs on the Access branch before this sequence is complete.

## 10. Documentation lifecycle

Temporary live/session handoffs are branch-operational artifacts and must not reach protected main. Before removal they pass the knowledge-coverage gate in `development/documentation-lifecycle-policy.md`.

At most one branch closure/history record should remain if it has continuing value beyond normal Git/PR history. Pure duplicates should leave the working tree; Git already preserves their exact content.

Current specs must not become append-only diaries. Repository truth beats conversation memory.