# DANTE Documentation Index

- **Status:** CURRENT NAVIGATION / AUTHORITY INDEX
- **Last reconciled:** 2026-09-03
- **Active branch-local workstream:** `feature/access-auth`

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

Protected `main` remains integrated authority for closed shared foundations. `feature/access-auth` contains newer branch-local truth for Access/Auth and the shared Email Platform until explicit integration.

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

EMAIL PLATFORM ARCHITECTURE          ACCEPTED / SHARED SUBSYSTEM
EMAIL PLATFORM IMPLEMENTATION        ACCEPTED
EMAIL PLATFORM AUTOMATED ACCEPTANCE  PASS
PRIMARY EMAIL PROVIDER ADAPTER       AMAZON SES API V2
REAL DANTE → SES SIGNUP UAT           PASS
REAL DANTE → SES RECOVERY UAT         PASS
REAL RESET-NOTIFICATION UAT          PASS
EMAIL PLATFORM ENGINEERING WORK      CLOSED

REAL APPLE UAT                       DEFERRED / OPEN
WHOLE M5                             ACTIVE / FINAL CLOSURE RECONCILIATION

ACCESS/AUTH ALEMBIC                  20260903_15
ACCESS/AUTH TOPOLOGY                 87/5/15/75/170/88/267
```

Email Platform closure is an engineering/UAT closure. Production sender-domain/DNS/reputation and cloud-event deployment remain separate operational gates.

## 3. Mandatory continuation entry points

Read in this order:

1. `../README.md`
2. `PROJECT-STATUS.md`
3. `ROADMAP.md`
4. `development/agent-operating-manual.md`
5. `workstreams/access-auth.md`
6. subject authority relevant to the task
7. current Git branch/ref and its relation to protected `main`

For the standalone Email Platform:

- `architecture/email-platform.md`
- `development/email-platform-local-uat.md` — reproducible AWS CLI / SES local UAT runbook
- `development/email-platform-acceptance-2026-09-03.md` — observed real-provider acceptance evidence
- `decisions/ADR-012-email-delivery-platform.md`
- `database/dictionary/tables/email_delivery_intent.json`
- `database/dictionary/tables/email_delivery_attempt.json`
- `database/dictionary/tables/email_provider_event.json`
- `database/dictionary/tables/email_recipient_suppression.json`

For Access/Auth architecture/security/API/testing:

- `architecture/access-auth-architecture.md`
- `architecture/access-auth-security-contract.md`
- `architecture/access-auth-api-contract.md`
- `architecture/access-auth-testing-contract.md`
- `architecture/access-auth-m4-contract.md`
- `architecture/access-auth-m5-contract.md`
- `architecture/access-auth-m5-persistence-api-contract.md`
- `architecture/access-auth-email-delivery.md` — Access/Auth integration with the shared Email Platform only
- `decisions/ADR-011-access-auth-architecture.md`

For current product/reference state:

- `frontend/access.md`
- `database/README.md`
- `database/access-auth.md`
- `../apps/backend/README.md`

## 4. Progress-metadata reconciliation

Some large durable M5 contracts contain milestone-time sections such as `M5-F NEXT` or `public routes later`. Those statements are preserved as historical reconciliation of the slice in which they were written. They are **not current progress authority** when they conflict with `PROJECT-STATUS.md`, `ROADMAP.md` or the active workstream.

The old dated file `workstreams/access-auth-m5-live-handoff-2026-08-29.md` is superseded/historical.

While `feature/access-auth` remains active, `workstreams/access-auth-m5-live-handoff-2026-09-02.md` is a temporary branch-operational continuation aid. It must be consolidated/removed before protected-main integration under `development/documentation-lifecycle-policy.md`.

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

Important subsystem documents:

- `architecture/email-platform.md` — reusable outbound Email Platform
- `architecture/access-auth-architecture.md` — Account/authenticator/session architecture
- `architecture/access-auth-email-delivery.md` — Access/Auth consumer integration with Email Platform

Important ADRs:

- `decisions/ADR-007-domain-model-informed-persistence-boundaries.md`
- `decisions/ADR-008-frontend-engineering-stack.md`
- `decisions/ADR-009-frontend-architecture-boundaries.md`
- `decisions/ADR-010-postgresql-persistence-constitution.md`
- `decisions/ADR-011-access-auth-architecture.md`
- `decisions/ADR-012-email-delivery-platform.md`

The Email Platform is a materialized shared subsystem built around PostgreSQL transactional intent, provider-neutral delivery orchestration, Amazon SES API v2, feedback/suppression and privacy-minimized observability.

Access/Auth is its first consumer, not its architectural owner.

## 7. Database

Start at:

- `database/README.md`
- `database/access-auth.md`
- `database/dictionary/README.md`

Current branch DB:

```text
PostgreSQL          18.6
Alembic             20260903_15
87 tables
5 views
15 routines
75 triggers
170 physical indexes
88 foreign keys
267 CHECK constraints
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

The Email Platform persistence is included in the current catalog through:

```text
dante.email_delivery_intent
dante.email_delivery_attempt
dante.email_provider_event
dante.email_recipient_suppression
```

## 8. Frontend

Start at:

- `frontend/README.md`
- `frontend/access.md`
- `frontend/home/current-checkpoint.md`
- `frontend/home/contract.md`

Access is now a real full-stack Auth surface on `feature/access-auth`; old pre-backend statements are historical baseline context, not current runtime truth.

## 9. Testing / proof

Access/Auth and Email Platform proof deliberately separate:

```text
unit/application
PostgreSQL
HTTP/OpenAPI/generated client
browser full-stack
real provider/authenticator UAT
real external-delivery UAT
```

Current observed evidence includes:

```text
local password/passkey UAT PASS
real Windows Hello passkey UAT PASS
real Google UAT PASS
Email Platform unit tests PASS
Email Platform PostgreSQL acceptance PASS
Auth mutation + EmailIntent atomicity PASS
Email observability PostgreSQL acceptance PASS
backend non-PostgreSQL regression PASS
real SES signup/recovery/reset-notification UAT PASS
direct UAT DB provider-correlation + secret-wipe PASS
```

The exact accepted live evidence is `development/email-platform-acceptance-2026-09-03.md`.

One explicit non-claim is preserved there: the exact same consumed recovery URL was not manually reopened a second time in the final live run.

## 10. Email Platform closure and production boundary

Email Platform engineering is closed:

```text
architecture                    ACCEPTED
persistence                     ACCEPTED
SES API v2 adapter              ACCEPTED
SMTP compatibility adapter      ACCEPTED
automated/PostgreSQL proof      PASS
real signup SES UAT             PASS
real recovery SES UAT           PASS
real reset-notification UAT     PASS
reproducible AWS local UAT      MATERIALIZED
```

Production deployment remains separately gated on:

```text
controlled DANTE sender/domain
DKIM
SPF
DMARC
production IAM/workload identity
SES production account/quota/reputation posture
live cloud feedback/event routing
operational alerting and traffic/reputation segmentation
Apple relay sender-domain compatibility where applicable
```

These are deployment/operations tasks. They do not mean the shared Email Platform must be redesigned.

## 11. Documentation lifecycle

Current docs are not an append-only diary. Historical evidence remains recoverable in Git; current subject/index documents should not carry stale `NEXT/TBD/NOT IMPLEMENTED` claims after their trigger is satisfied.

Repository truth beats conversation memory.
