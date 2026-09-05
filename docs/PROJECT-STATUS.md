# DANTE — Project Status

- **Status:** CURRENT PROTECTED-MAIN TRUTH + AI INTEGRATION CANDIDATE
- **Last reconciled:** 2026-09-05
- **AI main-reconciliation merge:** `4a0a69d9f331a65dcf4f72f53f33f06babddca46`
- **AI merge parents:** `feature/ai-implementation@68f38e153ab97df2bd2a86a84d31f62b3bdd0bf4` + `main@9dae13163549ca6d342978876be9582d7ec08610`
- **Protected-main Observability merge:** `b74a806deed68b2729dd04678c0a5674cd572e8a` via PR `#58`
- **Platform Observability source closure:** `828cfd231debb1326933052fefd74e81c653a6c3`
- **Platform Observability integration merge:** `14faecfb11bded15aa929b0eaac91427031072ed`
- **Current Alembic head:** `20260904_17`

The AI status below is branch-local integration-candidate truth. It does **not** become protected-main truth until the pull request is accepted by the required repository gates and merged.

## 1. Current state

```text
Product / North Star                       CURRENT
Domain / Logical / Physical                CLOSED
Engineering + Frontend + Backend CP1–CP6  CLOSED / ACCEPTED
PostgreSQL                                 18.6

Access M1–M5                               CLOSED / INTEGRATED
Shared Email Platform                      CLOSED / INTEGRATED / OWNERSHIP VERIFIED
PostgreSQL Recovery                        CLOSED / INTEGRATED
local password/passkey UAT                 PASS
real Windows Hello UAT                     PASS
real Google UAT                            PASS
real Apple registered-domain UAT           BOUNDED DEFERRED / NON-BLOCKING

Alembic                                    20260904_17
database topology                          88/5/16/76/172/89/270
database-local CP07                        PASS
application / Email reopen CP08            PASS

Platform Observability source workstream   CLOSED / OPERATIONAL ACCEPTANCE PASS
Platform Observability protected main      CLOSED / INTEGRATED VIA PR #58
observability source verification          13/13 PASS
PostgreSQL/ACL integration acceptance      155/155 PASS
backend readiness + Alloy                  PASS
Web/Faro integrated LOCAL production-build smoke PASS
Grafana Cloud metrics/logs/traces/Faro path PASS
Tempo route-attribute privacy boundary     PASS
collector-outage failure isolation         PASS
Grafana acceptance service-account cleanup PASS

AI deterministic low-level foundation      CLOSED / PASS / BRANCH-LOCAL
AI main reconciliation                     TRUE TWO-PARENT MERGE COMPLETE
AI protected-main integration              PR / REQUIRED GATES PENDING
AI production/private-data qualification   NOT CLAIMED
AI real product/owner-seam integrations     DEFERRED / TRIGGER-GATED

M6 Native Mobile                           FUTURE / OPTIONAL
later Access/M7 maturity                   FUTURE
```

Platform Observability is protected-main truth. PR `#58` merged `integration/platform-observability-v2` into `main` with merge commit `b74a806deed68b2729dd04678c0a5674cd572e8a`; its parents are the prior protected-main head `318ae452556e8bada3aaeee09688a89acc548a32` and accepted integration head `33228f576bfc2cdd479ea4f527164c7ba9dd8a2d`.

The AI candidate has now incorporated current `main` through the real two-parent merge `4a0a69d9f331a65dcf4f72f53f33f06babddca46`. Current-main Auth/Access/Home/Timeline/Observability and database truth are retained; AI is an additive capability foundation over that baseline.

Apple is not reported as PASS. Real Apple external acceptance remains a future enablement prerequisite when its external account/domain prerequisites exist.

Remote backup-provider activation and production/cloud recovery remain **NOT CLAIMED**.

## 2. Current database truth

```text
PostgreSQL          18.6
Alembic             20260904_17
tables              88
views                5
routines             16
triggers             76
physical indexes     172
foreign keys         89
CHECK constraints    270
```

The current cross-representation database contract remains aligned across the Dictionary, SQLAlchemy mappings, Alembic and real PostgreSQL. Platform Observability and the AI integration candidate add no DANTE business DDL, Alembic revision or SQLAlchemy business mapping.

Its PostgreSQL operational reader is the provisioning-owned `dante_observer` role: `LOGIN NOINHERIT`, with `pg_read_all_stats` membership using `INHERIT TRUE / SET FALSE / ADMIN FALSE`, no DANTE/public business-object access, no database `CREATE`/`TEMP`, and `search_path=pg_catalog`. The exact contract remains in `database/dante-postgresql-database-part-12.md` and the live provisioning/acceptance tests.

## 3. Accepted foundation evidence

Access/Auth + Email + Recovery remain closed at their accepted evidence levels. The historical CP07 database-local proof and the later CP08 application/Email reopen proof remain distinct; CP07 is not widened retroactively. Their durable evidence remains in `workstreams/access-auth-integration-acceptance-2026-09-04.md`, `archive/branches/2026-09-feature-access-auth.md` and the Recovery operator references.

Platform Observability acceptance includes:

```text
true Git three-way integration merge             PASS
frozen source history retained                   PASS
observability source verification                13/13 PASS
Web tests                                        23 files / 101 tests PASS
backend non-PostgreSQL regression                286/286 PASS
strict mypy                                      148 source files / zero issues
backend package build                            PASS
PostgreSQL 18.6 marked acceptance                155/155 PASS
observer role / membership / ACL proof           PASS
backend bootstrap with observability enabled     PASS
backend /health/ready                            HTTP 200
Alloy readiness                                  PASS
Web/Faro LOCAL production-build smoke surface    PASS
Grafana Cloud metrics/logs/traces/Faro path      PASS
Tempo route-attribute privacy boundary           PASS
collector-outage failure isolation               PASS
Grafana acceptance service account remote delete PASS
PR #58 Backend CI Gate                           PASS
PR #58 Frontend CI Gate                          PASS
PR #58 Dependency Review                         PASS
protected-main merge reachability                PASS
```

The source workstream had already proved the real Grafana Cloud path for metrics, logs, traces, PostgreSQL statistics, black-box readiness and Web Faro/Web Vitals, plus dashboard/alert materialization and collector-outage failure isolation. That evidence is retained rather than rerun merely for repetition.

Dedicated Google/Apple, passkey, Auth-lifecycle and Email-to-central-OTel domain metrics are future observability enhancements. They are not blockers for the accepted platform foundation because global HTTP, database, Web, Auth signin/KDF/dependency and collector telemetry already cover the integration boundary without changing product semantics.

## 4. AI branch-local foundation and integration candidate

Durable AI closure authority is `workstreams/ai-foundation-closure-2026-09-05.md`; implementation scope and deferred stages remain in `workstreams/ai-implementation.md` and the final AI architecture baseline.

Current branch-local truth:

```text
deterministic low-level AI foundation            CLOSED / PASS
ModelAccess/provider boundary                     MATERIALIZED
Gemini 3.8 Flash development binding             ACCEPTED FOR DEVELOPMENT FOUNDATION
Global Search deterministic backend foundation   CLOSED / INDEPENDENT FROM INTELLIGENCE
write / consequential semantics                   NON-PRODUCTION / NO UNBOUNDED EFFECT ACTIVATION
production qualification                         NOT CLAIMED
private-data eligibility                         NO
real Search owner/data seam                       DEFERRED
real Ask DANTE product integration                DEFERRED
main -> feature reconciliation                    PASS / TRUE TWO-PARENT MERGE
protected-main PR gates                           PENDING
```

The reconciled dependency graph preserves current-main runtime dependencies and adds the OpenAI SDK only for its bounded private outbound adapter. The lock was regenerated/validated against the reconciled graph before the merge candidate was built. Search remains a first-class deterministic capability boundary and has no dependency on Intelligence/model/provider runtime.

The main-reconciled candidate was structurally compared back to current `main`: the delta is additive AI/Search foundation, AI tests/tooling/docs, `openai` dependency/lock materialization, the bounded transport/dependency architecture tests, and the AI deterministic CI gate. Current-main application, Auth, Email, Recovery, Home/Timeline and Observability changes are not replaced by stale feature versions.

## 5. Integration state

Platform Observability integration is complete.

```text
source closure                              PASS
true integration merge                      PASS
integrated source verification              PASS
PostgreSQL/ACL acceptance                    PASS
runtime/Grafana Cloud smoke                  PASS
collector-outage isolation                   PASS
documentation lifecycle reconciliation      PASS
PR #58 required CI                           PASS
protected-main merge                         PASS
```

AI integration is deliberately reported separately:

```text
foundation closure                           PASS / BRANCH-LOCAL
main reconciliation                          PASS / 4a0a69d9
current-truth documentation reconciliation   IN PROGRESS ON FEATURE
required PR CI                               PENDING
protected-main merge                         NOT YET CLAIMED
post-merge main acceptance                   NOT YET APPLICABLE
```

Do not reopen accepted OTel/Alloy/Grafana/Faro/PostgreSQL-observer implementation merely to repeat evidence. Future Observability work is a new bounded scope from current protected `main`.

## 6. Documentation lifecycle state

Platform Observability has no active workstream authority file. Current truth is routed through:

- `architecture/observability-runtime-contract.md`
- `development/observability-runbook.md`
- `../infra/observability/README.md`
- `database/dante-postgresql-database-part-12.md` for the observer-role contract
- executable code, tests and source-controlled Grafana/Alloy assets

AI currently retains an active integration-candidate workstream authority at `workstreams/ai-implementation.md` plus dated closure/evaluation evidence. Those files remain branch-local until protected-main integration.

One consolidated historical Observability record is retained at `archive/branches/2026-09-feature-platform-observability.md`. It is **NON-AUTHORITATIVE / HISTORICAL / EVIDENCE ONLY**.

Temporary live/session/resume handoffs are absent. Historical source-workstream chronology that is not current authority remains recoverable from the consolidated branch record and Git/PR history.

## 7. Permanent safety rules

```text
protected main is integration authority
unmerged candidate truth != protected-main truth
no rebase/history rewrite of accepted work
no force push for normal integration
applied migrations are immutable
no schema claim without Dictionary/mapping/migration/PG/test parity
no PASS without executed evidence
AI/model output != canonical DANTE truth
Search must remain usable independently from Intelligence
telemetry != canonical DANTE state
telemetry failure != permission to alter product truth
LOCAL recovery PASS != production/cloud recovery PASS
```

## 8. Authority order

1. executable code / migrations / tests / real PostgreSQL
2. Product / Domain / Logical / Physical / constitutions / ADRs
3. current subsystem references
4. this status + roadmap
5. durable evidence / Git chronology
6. conversation memory
