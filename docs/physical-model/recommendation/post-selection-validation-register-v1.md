# Post-Selection Validation Register v1

- Status: **PM-11 SELECTED-STACK CARRY-FORWARD / DIRECTLY UNEXECUTED**
- Purpose: define the validation obligations that remain after target-stack selection and must not be mistaken for already executed PASS results.
- Post-closure traceability maintenance: **2026-08-22 — SC-017/SC-018 labels reconciled to the canonical Physical Benchmark Scenario Corpus; no architecture, selection or validation obligation changed.**

Scenario identifiers and canonical scenario names in this register MUST follow `docs/architecture/physical-benchmark-scenario-corpus.md`. This register may assign selected-stack validation obligations to those scenarios, but MUST NOT rename or reinterpret a canonical `SC-*` identifier.

## Primary correctness/recovery

```text
PSV-01  SC-011 old-backup anti-resurrection
PSV-02  SC-030 actual LifeOS V1 -> V2 mapping/schema evolution
PSV-03  SC-031 destructive restore + semantic verification
PSV-04  SC-032 capacity/backpressure truthful degradation
PSV-05  WL-H12 system-level non-interference
```

## Search / vector / projection

```text
PSV-06  SC-017 search hidden-result non-interference
PSV-07  SC-018 FTS mixed filter/query correctness under applicable Visibility/user/scope filtering
PSV-08  SC-019 vector recall/relevance after real Visibility/user/scope filtering
PSV-09  SC-020 projection freshness/material-basis behavior
PSV-10  SC-021 deletion/redaction propagation
```

`SC-017` is the canonical hidden-result non-interference scenario and already covers observable leakage surfaces such as result contents, counts, ranking, error behavior and timing classes. `SC-018` is the canonical FTS mixed filter/query scenario. These obligations are distinct and MUST NOT be collapsed or relabeled.

## Offline / PowerSync

```text
PSV-11  two-device divergence from common material base
PSV-12  offline mutation after remote canonical change
PSV-13  Authority/Consent/Visibility change while client offline
PSV-14  local encrypted-database validation and key-storage posture
PSV-15  device deletion/redaction purge/invalidation
PSV-16  PowerSync source half-open/stalled replication scenario
PSV-17  independent replication/checkpoint-lag monitoring
PSV-18  controlled restart/reconnect + client reconciliation
PSV-19  broad publication regression: only approved sync projections replicated
PSV-20  consequential LWW rejection
```

## Durable execution / Restate

```text
PSV-21  crash between canonical commit and external side effect
PSV-22  provider applied effect but response lost/ambiguous
PSV-23  human wait followed by target/governance change
PSV-24  duplicate/replay idempotency
PSV-25  cancellation/timeout truthfulness
PSV-26  in-flight workflow version/deployment evolution
PSV-27  runtime-journal privacy minimization
PSV-28  recovery/reconciliation after runtime outage
PSV-28A deployment-mode review: self-hosted vs Cloud EU privacy/operability/cost posture
PSV-28B Python path must not assume TypeScript-only client-side journal encryption
```

Restate technology is selected, but deployment is conditional. A deployment profile may choose self-hosted or Cloud EU without reopening the technology selection only if the selected mode satisfies the applicable privacy, durability, availability and recovery obligations above.

## Object storage / backup

```text
PSV-29  ContentArtifact metadata commit vs object upload partial failure
PSV-30  R2 deletion/redaction propagation
PSV-31  R2 primary object loss -> S3 object restore
PSV-32  DB restore + object backup reconciliation
PSV-33  no unauthorized public/private-cache exposure
PSV-34  backup access/audit and finite retention controls
```

## PostgreSQL / extensions / pooling

```text
PSV-35  PostgreSQL selected mapping end-to-end smoke corpus
PSV-36  PostGIS query/index correctness for accepted geo cases
PSV-37  pgvector model/source/freshness provenance
PSV-38  PgBouncer pool-mode compatibility by connection class
PSV-39  PowerSync logical replication bypasses incompatible transaction pooling
PSV-40  pgBackRest archive/restore/PITR rehearsal
```

## Solver

```text
PSV-41  deterministic OR-Tools corpus
PSV-42  UNKNOWN != INFEASIBLE behavior
PSV-43  candidate result cannot bypass Decision/governance
PSV-44  timeout/capacity degradation
```

## Observability/privacy

```text
PSV-45  no sensitive payload logging by default
PSV-46  required backlog/lag/failure signals observable
PSV-47  telemetry outage does not mutate semantic truth
```

## Gate rule

No entry above is a PASS until a direct selected-stack artifact exists.

```text
PM-11 TARGET SELECTION
may be COMPLETE

PM-12 ACCEPTED PHYSICAL MODEL
may preserve implementation-validation obligations

PM-13 CLEAN-ROOM QA
may verify architecture/documentation coherence
but MUST NOT relabel unexecuted PSV entries as PASS

implementation/release acceptance
must discharge applicable direct obligations at the correct stage
```

If an obligation cannot be satisfied with the selected stack, stop and reopen the relevant Physical decision rather than weakening Domain/Logical semantics.
