# Post-Selection Validation Register v1

- Status: **PM-10 MANDATORY CARRY-FORWARD / DIRECTLY UNEXECUTED**
- Purpose: define the validation obligations that remain after recommendation and must not be mistaken for already executed PASS results.

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
PSV-06  SC-017 selective disclosure/search non-interference
PSV-07  SC-018 hidden-result leakage surfaces
PSV-08  SC-019 vector recall/relevance after real Visibility/user/scope filtering
PSV-09  SC-020 projection freshness/material-basis behavior
PSV-10  SC-021 deletion/redaction propagation
```

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
```

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
PM-10 RECOMMENDATION
may remain PASS-CONDITIONAL

PM-12/PM-13/implementation acceptance
must preserve this register and discharge applicable items at the correct stage
```

If an obligation cannot be satisfied with the recommended stack, stop and reopen the relevant Physical decision rather than weakening Domain/Logical semantics.
