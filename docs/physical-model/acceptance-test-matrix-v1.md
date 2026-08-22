# Physical Model Acceptance Test Matrix v1

- Status: **CURRENT PHYSICAL ACCEPTANCE LEDGER — PM-14 TARGET CLOSURE COMPLETE / INTEGRATED INTO MAIN VIA PR #15**
- Physical business-semantic HG/direct benchmark corpus: **NOT EXECUTED / DIRECT HG PASS 0**
- Current technical PostgreSQL substrate after Physical closure: **CP2/CP3 DIRECT QA PASS**
- Former workstream branch: `feature/physical-model` — **MERGED / AUTO-DELETED**
- Main integration: `e6f191bad947388a44defe2c15f4939345084f58`
- Primary finalists: PostgreSQL 18.4, TypeDB CE 3.12.3
- PM-10 preferred primary: **PostgreSQL 18.4 / PASS-CONDITIONAL**
- PM-11 selected primary: **PostgreSQL 18.4**
- PM-12 accepted Physical Model: **ESTABLISHED**
- PM-13 architecture/documentation QA: **PASS**
- PM-14 branch closure: **COMPLETE**
- Post-closure traceability maintenance: **2026-08-22 — SC-017/SC-018 labels reconciled to the canonical scenario corpus; no architecture, selection, qualification or execution result changed.**

## Result-layer rule

```text
PM-03 STATIC PREFLIGHT
!=
PM-04A EVIDENCE SUFFICIENCY
!=
PM-05 SCENARIO QUALIFICATION
!=
PM-06/07 FINALIST QUALIFICATION
!=
PM-08 SPECIALIST QUALIFICATION
!=
PM-09 EVIDENCE-WEIGHTED DECISION SCORE
!=
PM-10 PREFERRED RECOMMENDATION
!=
PM-11 TARGET SELECTION
!=
PM-12 ACCEPTED PHYSICAL MODEL
!=
PM-13 ARCHITECTURE/DOCUMENTATION QA
!=
VERIFIED-RUN BENCHMARK SCORE
!=
DIRECT BUSINESS-SEMANTIC HG EXECUTION
```

`EVIDENCE-QUALIFIED != DIRECT PASS`, `PREFERRED != SELECTED`, `SELECTED != DEPLOYED`, `NOT RUN != PASS`, and `CP3 TECHNICAL QA != BUSINESS-SEMANTIC HG PASS`.

## Primary disposition

| Candidate | PM-09 score | PM-10 | PM-11 | PM-12 |
|---|---:|---|---|---|
| PostgreSQL 18.4 | **89.25** | PREFERRED / PASS-CONDITIONAL | **SELECTED CANONICAL PRIMARY** | **ACCEPTED PRIMARY** |
| TypeDB CE 3.12.3 | 80.00 | RUNNER-UP | NOT SELECTED | historical semantic challenger |
| XTDB 2.1.0 | — | excluded from recommended primary | NOT SELECTED | historical evidence |
| SurrealDB 3.2.3 | — | excluded from recommended primary | NOT SELECTED | historical evidence |

## Direct hard-gate status

No direct DANTE **business-semantic HG/destructive scenario** run has occurred merely by virtue of Physical selection or CP3 technical foundation work.

| Gate | PostgreSQL | TypeDB | XTDB | SurrealDB |
|---|---|---|---|---|
| HG-01 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-02 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-03 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-04 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-05 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-06 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-07 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-08 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-09 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-10 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-11 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| HG-12 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

Direct business-semantic HG PASS count: `0`.

CP2/CP3 later directly proved the technical PostgreSQL container, selected extension envelope, Alembic technical baseline, role/privilege model and transaction/test harness. Those proofs are real and current, but do not satisfy the business-semantic HG rows above.

## Direct benchmark tiers

| Tier | PostgreSQL | TypeDB |
|---|---|---|
| LOW | NOT RUN | NOT RUN |
| BASE | NOT RUN | NOT RUN |
| HIGH | NOT RUN | NOT RUN |

Verified-run weighted score: `NOT AVAILABLE`.

## Inherited scenario qualification

### Primary semantic set

```text
SC-001 SC-002 SC-003 SC-009 SC-010 SC-012
SC-014 SC-015 SC-016 SC-022 SC-023 SC-024
```

Classification remains `PRIMARY-EVIDENCE-SUFFICIENT` for the selected architecture.

### System/runtime/provider set

```text
SC-004 SC-005 SC-006 SC-007 SC-008
SC-025 SC-026 SC-027 SC-028 SC-029 SC-033 SC-034
```

Classification remains `SYSTEM-BOUNDARY`.

### Selected-stack direct validation

| Scenario | Status | Treatment |
|---|---|---|
| SC-011 old-backup anti-resurrection | NOT RUN | mandatory implementation validation |
| SC-013 deep-history scale | NOT RUN | reopen NO under PM-09/10 ranking |
| SC-030 V1→V2 evolution | NOT RUN | mandatory implementation validation |
| SC-031 destructive restore + semantic verification | NOT RUN | mandatory implementation validation |
| SC-032 capacity/backpressure | NOT RUN | mandatory implementation validation |

None is declared PASS.

## Accepted companion matrix

| Capability / component | PM-11/12 status | Direct validation | Authority rule |
|---|---|---|---|
| PostgreSQL 18.4 | SELECTED / ACCEPTED | technical substrate later CP2/CP3 PASS; semantic corpus NOT RUN | sole canonical persistence |
| PostGIS 3.6.4 | SELECTED | local extension envelope CP2 PASS; accepted geo corpus NOT RUN | technical geo capability only |
| PostgreSQL FTS + pg_trgm + unaccent | SELECTED | pg_trgm/unaccent envelope CP2 PASS; search corpus NOT RUN | derived/query capability |
| pgvector 0.8.6 | SELECTED | local extension envelope CP2 PASS; vector corpus NOT RUN | derived vector index only |
| pg_stat_statements | SELECTED | CP2 local preload/query PASS | operational telemetry only |
| PgBouncer 1.25.2 | SELECTED | NOT RUN | connection layer only |
| encrypted SQLite | SELECTED bounded local/offline | NOT RUN | never canonical |
| PowerSync 1.25.0 Open Edition | SELECTED / HARDENING REQUIRED | NOT RUN | sync/projection only |
| PostgreSQL outbox + bounded worker | SELECTED | NOT MATERIALIZED | bounded async runtime |
| Restate runtime | SELECTED / HARDENING REQUIRED | NOT RUN | durable runtime only |
| Restate self-hosted | ALLOWED / FIRST-CLASS | NOT RUN | deployment option |
| Restate Cloud EU | ALLOWED MANAGED OPTION | NOT RUN | deployment option; not mandatory |
| Restate Python SDK 1.0.3 | SELECTED SDK SUBJECT | NOT RUN | runtime client |
| Restate Server 1.7.2 | SELECTED self-hosted/reproducible subject | NOT RUN | runtime only |
| Cloudflare R2 Standard EU | SELECTED | NOT RUN | raw bytes only |
| pgBackRest 2.59.0 | SELECTED | NOT RUN | backup/recovery mechanism |
| AWS S3 eu-south-1 backup repos | SELECTED production target | NOT RUN | recovery copies only |
| OR-Tools 9.15 CP-SAT | SELECTED | NOT RUN | candidate/derived solver output |
| OpenTelemetry + Alloy 1.18.0 + Grafana Cloud EU | SELECTED | NOT RUN | operational telemetry only |

## Offline acceptance rule

```text
LOCAL SQLITE
!= CANONICAL

POWERSYNC DELIVERY ORDER
!= CONFLICT RESOLUTION

OFFLINE MUTATION
must re-enter DANTE backend
and revalidate expected state + governance + AuthZ
before canonical PostgreSQL commit
```

Universal consequential last-write-wins is rejected.

## PowerSync mandatory hardening tests

```text
replication/checkpoint lag monitoring
stalled replication detection
half-open source connection scenario
controlled restart/reconnect
client reconciliation after recovery
Visibility/Consent/redaction invalidation
approved sync_projection-only publication
encrypted local storage
```

## Durable-execution mandatory tests

```text
crash/replay without duplicate consequence
human/external wait with governance change
ambiguous provider effect
cancellation/timeout truthfulness
in-flight workflow version evolution
runtime journal privacy minimization
self-hosted vs Cloud EU deployment-mode review
Python path must not assume TypeScript-only journal encryption
```

## Object/recovery mandatory tests

```text
ContentArtifact metadata/object partial failure
R2 deletion/redaction propagation
R2 -> S3 object recovery
PostgreSQL pgBackRest restore/PITR
DB + object semantic reconciliation
old-backup anti-resurrection
```

## Search/vector/projection mandatory tests

```text
SC-017 search hidden-result non-interference
SC-018 FTS mixed filter/query correctness under applicable Visibility/user/scope filtering
SC-019 filtered vector recall/relevance
SC-020 projection freshness/material basis
SC-021 deletion propagation
```

`SC-017` and `SC-018` are separate canonical scenarios and MUST NOT be merged under one label.

## Solver mandatory tests

```text
deterministic corpus
UNKNOWN != INFEASIBLE
candidate output cannot bypass Decision/governance
timeout/degraded behavior
```

## PM-09 scoring retained

| Dimension | Weight | PostgreSQL | TypeDB |
|---|---:|---:|---:|
| Semantic mapping simplicity / evolvability | 20 | 8.5 | **9.5** |
| Transaction / concurrency ergonomics | 15 | **9.5** | 7.0 |
| Query / reporting / traversal | 15 | **9.0** | 8.5 |
| History + current-state efficiency | 10 | 8.5 | 8.5 |
| Operations / backup / restore / HA | 15 | **9.5** | 6.5 |
| Schema evolution / migration | 10 | **9.0** | 8.0 |
| Performance / resource efficiency | 10 | 8.0 | 8.0 |
| Python / tooling / cost / exit risk | 5 | **9.5** | 7.0 |
| **Evidence-weighted score** | **100** | **89.25** | **80.00** |

Sensitivity remains `ROBUST / NOT SENSITIVITY-DEPENDENT / NOT PERFORMANCE-DEPENDENT`.

## Execution admission result

```text
ranking-critical execution gaps          0
PM-04B reopened                          NO
benchmark host                           HOLD / DORMANT
verified-run score                       NOT AVAILABLE
```

## PM-13 clean-room result

```text
ARCHITECTURE / DOCUMENTATION COHERENCE
QA PASS

BLOCKING ARCHITECTURE DEFECTS
0

FALSE DIRECT PASS CLAIMS
0

LOST PSV OBLIGATIONS
0
```

This does not discharge direct implementation tests.

## Current project boundary

```text
PHYSICAL TARGET
CLOSED / SELECTED / ACCEPTED

BACKEND FOUNDATION CP1–CP5
CLOSED / INTEGRATED / DIRECT QA PASS

CP6 CONCRETE PERSISTENCE READINESS
ACTIVE / DESIGN-FIRST

BUSINESS PERSISTENCE SCHEMA
NOT IMPLEMENTED

BUSINESS-SEMANTIC HG / PSV DIRECT PROOF
ONLY WHEN THE EXACT REAL SUBJECT EXISTS AND IS EXECUTED
```
