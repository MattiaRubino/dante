# DANTE Roadmap

- **Status:** CURRENT REPOSITORY ROADMAP + AI INTEGRATION CANDIDATE
- **Last reconciled:** 2026-09-05
- **Current macro state:** **ACCESS/AUTH M1–M5 + SHARED EMAIL + RECOVERY + PLATFORM OBSERVABILITY CLOSED / INTEGRATED; AI DETERMINISTIC FOUNDATION CLOSED / MAIN-RECONCILED CANDIDATE**
- **AI main-reconciliation merge:** `4a0a69d9f331a65dcf4f72f53f33f06babddca46`
- **Protected-main Observability merge:** `b74a806deed68b2729dd04678c0a5674cd572e8a` via PR `#58`
- **Alembic head:** `20260904_17`

## 1. Current sequence

```text
Product / Domain / Logical / Physical
        CLOSED / CURRENT
              ↓
Engineering + Frontend + Backend CP1–CP6
        CLOSED / ACCEPTED
              ↓
Access M1–M5 + Shared Email Platform
        CLOSED / INTEGRATED
              ↓
Recovery + Access/Auth + Email convergence
        20260904_17 / ACCEPTED
              ↓
CP07 database-local recovery
        PASS FOR EXECUTED SCOPE
              ↓
CP08 Email/application reopen
        PASS
              ↓
Platform Observability
        CLOSED / PROTECTED-MAIN INTEGRATED
              ↓
AI low-level deterministic foundation
        CLOSED / BRANCH-LOCAL PASS
              ↓
main -> feature/ai-implementation reconciliation
        4a0a69d9 / TRUE TWO-PARENT MERGE COMPLETE
              ↓
AI integration PR required gates
        PENDING
              ↓
protected-main AI integration
        NOT YET CLAIMED
```

Platform Observability is protected-main truth through PR `#58`. The AI foundation is a main-reconciled integration candidate and remains unmerged truth until its pull request passes the required repository gates and is merged.

## 2. Access/Auth + Email + Recovery

M1–M5 remain closed and integrated for their accepted scope. Password/session, signup/recovery/reset/reauth, Google, passkeys/Windows Hello, authenticator lifecycle, generated client, Web security surface and the shared durable Email Platform remain accepted at their documented evidence levels.

Apple real registered-domain UAT remains **BOUNDED DEFERRED / NON-BLOCKING**. It is not a real-provider PASS and must be reopened before future Apple production enablement.

The historical CP07 run proves the LOCAL PostgreSQL/database-local and MaterialState scope it actually executed. CP08 separately proves the forward Email/application reopen sequence after PITR. Neither proof is widened into production/cloud recovery.

## 3. Platform Observability integration

The source workstream is closed and frozen at `828cfd231debb1326933052fefd74e81c653a6c3`. The real integration branch was created from protected-main baseline `318ae452556e8bada3aaeee09688a89acc548a32`, carries the true two-parent merge `14faecfb11bded15aa929b0eaac91427031072ed`, and was integrated into protected `main` via PR `#58` at merge commit `b74a806deed68b2729dd04678c0a5674cd572e8a`.

Accepted integrated gates:

```text
observability source verification           13/13 PASS
PostgreSQL 18.6 / ACL acceptance             155/155 PASS
observer least-privilege posture             PASS
backend observability-enabled bootstrap       PASS
backend readiness                             HTTP 200
Alloy readiness                               PASS
Web/Faro LOCAL production-build smoke         PASS
Grafana Cloud metrics/logs/traces/Faro path   PASS
Tempo privacy boundary                        PASS
collector-outage isolation                    PASS
Grafana acceptance service-account cleanup    PASS
PR #58 Backend CI Gate                        PASS
PR #58 Frontend CI Gate                       PASS
PR #58 Dependency Review                      PASS
```

## 4. AI low-level foundation

The deterministic AI foundation is closed for its bounded development scope. Current authority is:

- `architecture/dante-ai-implementation-baseline-final.md`
- `architecture/dante-ai-search-intelligence-boundary-amendment-2026-09.md`
- `workstreams/ai-implementation.md`
- `workstreams/ai-foundation-closure-2026-09-05.md`
- `workstreams/ai-runtime-model-target-closure-acceptance-2026-09-05.md`

Current disposition:

```text
I0 architecture/application ownership boundaries         CLOSED / PASS
I1 deterministic Search foundation                       CLOSED / PASS
I2 Intelligence request-local contracts/fakes            CLOSED / PASS
I3 first real Search/structured owner family              DEFERRED / REAL OWNER-SEAM GATE
I4 provider/binding foundation                            CLOSED FOR DEVELOPMENT FOUNDATION
I5 native provider conformance + bounded evidence         CLOSED / PASS FOR DEVELOPMENT FOUNDATION
I6 first real read-only Ask DANTE integration             DEFERRED / PRODUCT-READINESS GATE
I7 full production hardening                              FUTURE BEYOND LOW-LEVEL FOUNDATION
I8 scenario/planning vertical                             FUTURE
I9 consequential Effect vertical                          FUTURE
I10 proactive/background/external-agent work              FUTURE / TRIGGER-GATED
```

Development binding remains application-owned and provider-hidden:

```text
STRUCTURED_INTERPRETATION -> Gemini 3.8 Flash
GENERAL_REASONING         -> Gemini 3.8 Flash
DEEP_REASONING            -> dormant / no binding
protocol                  -> native Gemini Interactions API v1beta
route revision            -> gemini-flash-dev-v2
production                -> off
private-data eligibility  -> no
```

Search remains independent from Intelligence. The backend Search materialized by this foundation is deterministic contracts/application/ports; real owner/data persistence or product routing is not fabricated merely to close the foundation.

The main reconciliation is complete through merge `4a0a69d9f331a65dcf4f72f53f33f06babddca46`, whose parents are the prior AI feature head and current `main@9dae13163549ca6d342978876be9582d7ec08610`. Current-main Auth/Access/Home/Timeline/Observability truth is retained.

## 5. Current bounded gate

The foundation implementation gate itself is closed. The remaining gate is **repository integration**, not more AI feature expansion:

```text
AI deterministic foundation closure         CLOSED / PASS
current-main reconciliation                  CLOSED / PASS
current-truth documentation reconciliation  IN PROGRESS / FEATURE
required PR Backend CI Gate                  PENDING
required PR Dependency Review                PENDING
required PR Frontend CI Gate                 PENDING
protected-main merge                         PENDING
post-merge acceptance                        AFTER MERGE
```

Do not reopen I3/I6 or manufacture a product vertical merely to make this PR larger. Do not activate production/private-data use as part of integration.

## 6. Database contract

Current application database contract remains:

```text
PostgreSQL          18.6
Alembic             20260904_17
88 tables / 5 views / 16 routines
76 triggers / 172 indexes / 89 FKs / 270 CHECKs
```

The AI integration candidate adds **no database/Alembic change**. Platform Observability likewise adds no business DDL. `dante_observer` remains a provisioning-owned operational role with `pg_read_all_stats` membership only and no DANTE/public business-object access.

## 7. Later work

Future bounded workstreams may include:

```text
AI real Search owner/data adapters          REAL-SEAM TRIGGERED
AI real Ask DANTE product integration       PRODUCT-READINESS TRIGGERED
AI memory integration                       FUTURE
AI solver integration                       FUTURE
FTS / pg_trgm / embeddings / pgvector       NEED-DRIVEN
voice / realtime                            FUTURE
browser / computer / code execution         FUTURE / SEPARATE SECURITY GATE
second provider / failover / local model    EVIDENCE-TRIGGERED
deep-reasoning physical binding             EVIDENCE-TRIGGERED
AI production/private-data qualification    SEPARATE ACCEPTANCE
M6 Native Mobile                            OPTIONAL / RE-GATE
session/device inventory                    FUTURE
per-session revoke / revoke all others      FUTURE
security-event history                      FUTURE
new-login/security notifications            FUTURE
Security UI refinement                      FUTURE
vertical observability metrics              FUTURE / NEED-DRIVEN
production observability tuning             FUTURE / MEASURED-EVIDENCE ONLY
production/cloud recovery                   FUTURE / SEPARATE ACCEPTANCE
```

Start each future scope from then-current protected `main`; do not continue from an obsolete pre-integration AI branch snapshot.

## 8. Permanent rules

```text
protected main is integration authority
UNMERGED CANDIDATE TRUTH != PROTECTED-MAIN TRUTH
applied Alembic revisions are immutable
Dictionary ≈ SQLAlchemy ≈ Alembic ≈ PostgreSQL ≈ current DB reference
Search != Intelligence and must remain independently usable
provider output != canonical DANTE truth
no blind retry after ambiguous external effects
restored external-effect work != permission to replay
telemetry != canonical DANTE state
telemetry failure must not alter product behavior
no fake PASS
LOCAL recovery PASS != production/cloud recovery PASS
CURRENT SPECIFICATION != APPEND-ONLY DIARY
TEMPORARY HANDOFF != DURABLE DOCUMENTATION
```
