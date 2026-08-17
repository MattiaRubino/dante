# Non-Functional / Multi-Device / Operational-Recovery Requirements

- Status: **CURRENT — Phase 5 accepted requirement package**
- Stage: Pre-Physical Repository & Architecture Coherence
- Numeric targets / mechanisms: **OPEN / DEFERRED WHERE MARKED**

## Purpose

Define the non-functional, multi-device, offline/degraded-mode, resilience and operational-recovery requirements that later Physical/runtime designs must satisfy without inventing unsupported numeric targets.

This package intentionally separates required capability/classes from values that are not yet responsibly known. `OPEN` means a later gate must set the value before candidate scoring or implementation where the value materially affects design.

## Accepted upstream boundary

LifeOS already requires:

- web + mobile clients behind governed backend contracts;
- no direct client ownership of canonical persistence;
- provider/cache/index/device-local state remains distinct from canonical LifeOS state;
- concurrent/divergent material states can exist;
- no universal last-write-wins policy;
- historical/current/derived/provider/candidate states remain distinguishable;
- current-state queries must not require lifetime history replay by default;
- offline capability is not globally pre-authorized and must be explicitly bounded.

## Normative requirements

### NFR-01 — Multiple clients/devices cannot silently overwrite consequential state

Concurrent use from web/mobile/multiple devices MUST NOT create silent materially consequential overwrite solely because one write arrived last.

Expected-state/conflict semantics from `consistency-side-effects.md` apply equally to multi-device writes.

### NFR-02 — Divergent material states remain detectable/recoverable

When materially divergent states arise from a common base, the architecture MUST preserve enough information to detect and reconcile the divergence according to accepted semantic policy.

One branch MUST NOT disappear merely because another device/provider synchronized later.

### NFR-03 — Offline behavior is operation-specific, not globally assumed

For every operation intentionally made offline-capable, later design MUST explicitly define:

- what data may be read locally;
- freshness/expiry semantics;
- what may be mutated locally;
- what may be queued for later effect;
- which operations are forbidden offline;
- required expected/material base state;
- governance/authentication revalidation at synchronization/effect time;
- conflict/reconciliation behavior;
- local sensitive-data protection and deletion behavior;
- user-visible pending/degraded semantics.

Offline support MUST NOT be inferred automatically from the existence of a mobile client.

### NFR-04 — Consistency and availability expectations are operation/consequence specific

LifeOS MUST NOT be modeled with one universal `strong consistency` or `eventual consistency` label.

Later architecture MUST classify operation/read families according to the consequences of stale/partial data and define the appropriate consistency/availability expectation per class.

### NFR-05 — Provider outage/degraded mode remains truthful

When an external provider is unavailable, stale or rate-limited, LifeOS MUST distinguish as applicable:

```text
canonical known state
last known provider state
cached projection
provider unavailable/unknown
pending synchronization
unresolved divergence
```

A cached/provider value MUST NOT silently masquerade as freshly current canonical truth.

### NFR-06 — Current-state access must scale independently of lifetime replay

Normal current-state/product queries MUST NOT require replaying the entire historical lifetime of an owner merely to reconstruct common current views.

Later Physical design MUST support bounded current/effective access while retaining the required history/provenance/reconstruction semantics.

This does not mandate snapshot tables, event sourcing or another specific technique.

### NFR-07 — RPO must be explicitly defined before dependent Physical scoring

Recovery Point Objective MUST be classified/set for data/effect classes before a candidate is accepted where data-loss tolerance materially affects technology or topology.

No numeric RPO is selected by Phase 5.

### NFR-08 — RTO / restore objective must be explicitly defined

Recovery Time Objective / restore-service expectation MUST be classified/set for critical service/data classes before Physical/runtime acceptance where downtime tolerance affects design.

No numeric RTO is selected by Phase 5.

### NFR-09 — Restore procedures must be testable and verified

Accepted backup/restore mechanisms MUST support repeatable restore testing that proves the restored system is semantically usable, not merely that backup bytes exist.

Validation MUST include integrity of required references/history/governance and interaction with later deletion/redaction state.

### NFR-10 — Latency/availability classes must exist before final Physical scoring

The project MUST define material user-operation/read classes and their latency/availability targets before final Physical benchmark scoring where performance could change candidate ranking.

Phase 5 does not invent p95/p99/SLA values.

### NFR-11 — Scale/concurrency/data-growth assumptions are explicit benchmark inputs

Before Physical candidate acceptance, benchmark assumptions MUST state realistic ranges or scenarios for at least:

- active users/accounts relevant to the selected release target;
- concurrent sessions/devices;
- canonical owners/relations/material history growth;
- write/read concurrency;
- provider/integration traffic;
- file/object growth where relevant;
- derived/index/search growth where relevant.

Unknown values MUST be modeled as explicit scenarios/sensitivity ranges rather than hidden assumptions.

### NFR-12 — Schema/data evolution preserves semantic history and reference integrity

Future Physical migrations/evolution MUST preserve accepted identity/reference/material-history/provenance/governance/tombstone semantics.

An upgrade MUST NOT silently remap historical meaning, reuse native identity, drop materially required state bindings or turn unavailable/redacted history into `never existed`.

### NFR-13 — Temporal behavior preserves timezone/DST/effective-time semantics

Scheduling/time-related implementation MUST preserve accepted Domain/Logical distinctions across timezone, offset, daylight-saving transitions, effective chronology and historical interpretation.

Technical normalization MUST NOT erase the semantic timezone/local-time information required to reconstruct what was planned/understood/applied.

### NFR-14 — Operational observability must not become privacy leakage

Metrics, traces, health signals and diagnostics MUST be sufficient to detect failures, latency, queue/backlog/reconciliation pressure and restore issues while respecting the minimization/disclosure constraints in `security-privacy-retention-recovery.md`.

A need for observability MUST NOT justify broad sensitive payload logging.

### NFR-15 — Client/runtime version compatibility must preserve newer constraints

Older clients, stale local schemas or delayed queued operations MUST NOT bypass newer mandatory governance, expected-state, privacy or effect constraints.

Later API/runtime versioning must have an accepted compatibility/rejection/upgrade policy for consequential behavior.

### NFR-16 — Degraded mode cannot manufacture successful canonical state

If persistence, provider, policy, queue/workflow or other required infrastructure is unavailable, the product/runtime MUST represent failure/pending/degraded/unknown state truthfully.

Availability pressure MUST NOT be satisfied by claiming a canonical effect occurred when the required durable effect did not occur.

### NFR-17 — Recovery preserves pending/partial-effect truth

After restart/restore/failover, pending, staged, partially externally applied or reconciliation-required operations MUST remain recoverable enough to avoid duplicate or falsely completed effects.

This requirement cross-links `consistency-side-effects.md` and does not choose a workflow/outbox mechanism.

### NFR-18 — Capacity failure has explicit safe behavior

Resource exhaustion, provider quota/rate limits, storage pressure, worker backlog and similar operational limits MUST have defined safe/degraded behavior for consequential paths.

The system MUST prefer explicit backpressure/failure/pending state over silent data loss or uncontrolled duplicate effects.

### NFR-19 — Availability does not override governance/freshness

A cached or locally available answer MUST NOT be served/applied merely to preserve availability if the applicable operation requires stronger current governance, expected-state or freshness guarantees.

The later design MUST state which stale/read-only experiences are safe and which operations must fail/require connectivity/revalidation.

### NFR-20 — Recovery testing includes realistic destructive scenarios

Later architecture MUST validate recovery across at least:

- process/service crash;
- persistence unavailability;
- provider outage;
- restart between canonical commit and side effect/publication;
- restore from backup;
- restore after later deletion/redaction;
- queued operation after governance/target change;
- device divergence after extended offline period;
- schema/runtime upgrade with pending work.

## Operational recovery vs security/privacy recovery

This document owns operational targets/behavior:

```text
RPO
RTO
service restoration
degraded mode
availability/resilience
capacity/backpressure
restore verification
multi-device/offline recovery
```

`security-privacy-retention-recovery.md` owns backup-data protection, restore authorization/audit, deletion/redaction correctness and prevention of unauthorized data resurrection.

## Open parameters / decisions

The following are mandatory later decisions, not Phase 5 guesses:

```text
NFR-OPEN-01 RPO target/classes
NFR-OPEN-02 RTO target/classes
NFR-OPEN-03 availability/SLO classes
NFR-OPEN-04 p50/p95/p99 or other latency targets by material operation class
NFR-OPEN-05 expected active-account/user scale scenarios
NFR-OPEN-06 expected concurrent session/device scale
NFR-OPEN-07 write/read concurrency scenarios
NFR-OPEN-08 historical data growth horizon/scenarios
NFR-OPEN-09 provider/integration traffic/quota scenarios
NFR-OPEN-10 maximum intentionally supported offline duration by operation class
NFR-OPEN-11 local cache retention/size constraints
NFR-OPEN-12 supported client-version compatibility window
NFR-OPEN-13 backup frequency/restore-validation cadence in operational terms
NFR-OPEN-14 capacity/backpressure thresholds and user-visible degradation classes
```

Where exact product forecasts are unavailable, Phase 10 MUST benchmark explicit low/base/high scenarios and sensitivity rather than inventing one precise forecast.

## Deferred mechanisms — not selected by Phase 5

No mechanism is selected here for:

```text
single-region / multi-region topology
replication mechanism
failover technology
backup provider/product
read replica strategy
cache product
local mobile database
sync engine
CRDT / OT
queue/workflow engine
load balancer/orchestrator
Kubernetes
specific observability stack
specific autoscaling strategy
specific database partition/sharding design
```

Specialized infrastructure still requires demonstrated measured or structural benefit.

## Downstream benchmark pressure

Later candidates MUST be compared under at least these scenarios:

1. concurrent edits from web + mobile against the same material base;
2. mobile device offline while provider/another actor changes the same target;
3. stale free/busy/availability projection during a consequential decision;
4. provider outage while canonical state remains usable;
5. long history with efficient current-state query;
6. DST/timezone recurrence and historical reconstruction;
7. service crash between canonical commit and external/publication effect;
8. backup restore after later deletion/redaction;
9. client version lag across a governance/effect-contract change;
10. high backlog/quota/rate-limit pressure without duplicate/lost consequence.

## Traceability

Primary downstream pressure:

```text
WL-H05 expected-state consequential writes
WL-H07 truthful multi-owner consistency
WL-H08 canonical/provider-state separation
WL-H09 derived-state freshness
WL-H10 retention/tombstone integrity during restore/evolution
WL-H11 provenance where recovery/effect requires it
WL-H12 non-interference through degraded/cached surfaces
```

This package does not authorize infrastructure, Physical persistence or backend implementation.
