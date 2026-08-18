# Final Stack Simulation v1

- Status: **PM-10 SUPPORTING RECORD — COMPLETE**
- Purpose: replay representative LifeOS product simulations against the recommended physical stack and check for capability gaps or semantic violations.

## Scenario A — field technician offline with photos/location

```text
device offline
-> encrypted SQLite contains approved local projection
-> user records bounded offline mutation + photo metadata
-> raw photo held/uploaded under object workflow
-> reconnect
-> PowerSync upload path reaches LifeOS backend
-> expected/material basis + AuthZ/governance revalidated
-> PostgreSQL canonical commit if valid
-> R2 object state coordinated with ContentArtifact metadata
-> PostGIS supports location/proximity queries
```

Failure rule: offline arrival order never establishes canonical truth.

## Scenario B — two-device divergent edit

Device A and B start from the same material state. A commits online; B edits offline and reconnects later.

```text
B expected basis != current canonical basis
-> conflict/reconciliation state
-> no universal last-write-wins
```

Both branches remain representable where material until accepted resolution.

## Scenario C — semantic search over private data

```text
query
-> lexical FTS and/or pgvector
-> user/purpose/Visibility filtering
-> ranked bounded result
-> source/material basis retained where consequential
```

Hidden candidates must not leak through counts, ranks, timing surfaces or snippets beyond accepted non-interference policy.

## Scenario D — delete/redact private ContentArtifact

```text
PostgreSQL authoritative delete/redaction state
-> search/vector invalidation
-> PowerSync client projection invalidation/reset as required
-> device-local purge/reconciliation
-> R2 object deletion/retention action
-> backup anti-resurrection ledger/policy preserved
```

A UI hide is not sufficient.

## Scenario E — long-running provider action with human approval

```text
canonical Request/operation state in PostgreSQL
-> Restate durable process
-> human wait / callback
-> target + governance revalidation before consequence
-> provider attempt/result stored separately from canonical truth
-> ambiguous timeout remains unknown/pending/reconciliation as applicable
```

Restate journal state does not become Domain Decision/Confirmation/Actual automatically.

## Scenario F — short publication/index refresh

```text
canonical commit
+ transactional outbox row in same PostgreSQL transaction
-> bounded worker
-> publish/refresh
-> idempotent consumer/update
```

No dedicated message broker is required for this class.

## Scenario G — travel/offline documents/timezone

PostgreSQL retains semantic timezone/effective-time state and ContentArtifact metadata; R2 stores raw document bytes; encrypted SQLite exposes only approved local copies; PowerSync manages synchronization without becoming canonical authority.

## Scenario H — geographic reminder

PostGIS supports server-side place/radius logic. Device OS geofencing may support local trigger delivery, but a device trigger is not automatically a canonical consequential effect. Governed actions re-enter backend validation.

## Scenario I — planning/capacity optimization

```text
PostgreSQL material inputs
-> OR-Tools CP-SAT
-> OPTIMAL / FEASIBLE / INFEASIBLE / UNKNOWN technical result
-> candidate explanation/proposal
-> applicable user/governance acceptance
-> canonical effect only after acceptance
```

`UNKNOWN != INFEASIBLE`.

## Scenario J — destructive restore

```text
restore PostgreSQL from pgBackRest/S3
-> apply current deletion/redaction/anti-resurrection controls
-> semantic verification
-> reconcile R2/object backup state
-> purge/rebuild nonauthoritative PowerSync/search/vector state as required
-> invalidate stale clients
-> resume traffic only after checks
```

## Scenario K — capacity/backpressure

Connection saturation, worker backlog, PowerSync lag, Restate retry pressure, object-copy failures and solver time limits remain observable. The product must expose pending/degraded/failed state truthfully rather than claiming canonical completion.

## Simulation verdict

```text
REPRESENTATIVE MATERIAL SCENARIOS COVERED     PASS-CONDITIONAL
NEW DATABASE ENGINE REQUIRED                 NO
NEW MESSAGE BROKER REQUIRED                  NO
NEW SEARCH SERVER REQUIRED                   NO
NEW GRAPH SERVER REQUIRED                    NO
SECOND CANONICAL AUTHORITY                   NO

POST-SELECTION DIRECT VALIDATION
STILL REQUIRED WHERE REGISTERED
```
