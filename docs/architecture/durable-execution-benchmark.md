# Durable Execution / Async Benchmark

- Status: **CURRENT — Phase 7 benchmark contract**
- Stage: Pre-Physical Repository & Architecture Coherence
- Runtime implementation: **NOT SELECTED / NOT AUTHORIZED**
- Physical Model: **NOT STARTED / NOT AUTHORIZED**

## Purpose

Define the current LifeOS durable-execution posture and benchmark the minimum required candidate set without turning workflow/runtime machinery into Domain ontology or selecting implementation prematurely.

This benchmark consumes the CLOSED Domain Atlas, CLOSED Logical Model, `WL-H01..WL-H12`, all Phase 5 requirement packages, the Phase 6 AI/context/runtime contract and the Phase 6 Integration Hub contract.

It answers two separate questions:

```text
1. WHEN does LifeOS need dedicated durable orchestration?
2. WHICH current candidate best fits that dedicated boundary?
```

It does not answer which runtime is implemented now. No backend implementation is authorized by this document.

## Core boundary

```text
runtime Workflow / Job / Queue / Timer
!= Domain owner automatically

durable workflow completion
!= Domain Actual / Outcome / Confirmation automatically

runtime cancellation
!= Domain cancellation automatically

transport delivery
!= canonical effect

provider acknowledgement
!= canonical effect completeness automatically
```

The affected Domain owner remains responsible for the resulting semantic state. Runtime state exists to execute/recover technical work, not to become a universal business ontology.

## Why one async mechanism for everything is rejected

LifeOS has at least two materially different async classes.

### Class A — bounded asynchronous work

Representative work:

- publish a committed notification/message;
- refresh a search/index projection;
- run a bounded document transformation;
- perform a short provider retry/poll;
- propagate deletion/redaction to a bounded downstream projection;
- execute a short background calculation;
- retry a bounded idempotent publication.

These operations may justify a database-backed worker/outbox style mechanism without introducing a dedicated workflow platform.

### Class B — material durable process

Representative work:

- wait for human approval/review/confirmation;
- wait hours/days for provider callback or asynchronous external completion;
- perform multi-step provider synchronization with partial/ambiguous external effects;
- coordinate reconciliation/compensation after divergence;
- resume after process/node/redeployment failure;
- enforce cancellation/timeout/deadline behavior across multiple durable steps;
- execute delayed governed effects requiring target/governance revalidation;
- coordinate long-running AI/tool execution with external events or human oversight;
- preserve pending/partial-effect truth across crash/restart and runtime upgrades.

For these cases, the project recognizes structural benefit from a dedicated durable-execution mechanism rather than rebuilding every primitive ad hoc.

Canonical Phase 7 rule:

```text
bounded background work
MAY use a simple DB/worker/outbox mechanism

material long-running/recoverable coordination
SHOULD benchmark/use dedicated durable execution
when the accepted operation class requires it
```

This is not a rule that every asynchronous function becomes a workflow.

## Mandatory semantic/runtime requirements

Any candidate used for material durable execution MUST preserve the following.

### DEX-01 — Replay/recovery cannot duplicate governed consequence

Recovery/replay MUST NOT duplicate canonical or external effects. Runtime replay identity remains distinct from semantic identity and must respect Phase 5 idempotency requirements.

### DEX-02 — External reality is not exactly-once by runtime fiat

No runtime may be treated as proof of exactly-once external reality.

```text
workflow step recorded
!= provider effect known

request timed out
!= provider effect failed
```

External side effects remain subject to provider idempotency, reconciliation and unknown-outcome handling.

### DEX-03 — Delayed execution revalidates target/governance

A durable execution surviving beyond the original request boundary MUST revalidate materially mutable target and governance state where required, unless an explicitly valid immutable binding permits delayed execution.

### DEX-04 — Human wait is durable but does not fabricate semantics

Waiting for a human response may be runtime-durable, but:

```text
external signal received
!= Confirmation automatically
!= Decision automatically
!= Agreement / Consent automatically
```

The signal must still be translated through the owning semantic contract.

### DEX-05 — Runtime cancellation is separate from semantic effect

Cancelling/terminating a workflow or job stops/changes runtime execution according to its technical contract. It MUST NOT silently fabricate cancellation of Event, Activity, Request, Proposal, Schedule or another Domain state.

### DEX-06 — Partial state remains explicit

Crash, provider failure, cancellation or compensation MUST preserve truthful pending/partial/reconciliation state instead of collapsing the process to one generic `failed/success` bit.

### DEX-07 — Execution state is observable/recoverable

For material workflows, operators and application logic MUST be able to determine enough bounded runtime state to diagnose and safely continue/cancel/reconcile work after failures.

### DEX-08 — Runtime version evolution cannot replay obsolete semantics silently

A deployment/runtime upgrade MUST have an accepted strategy for in-flight durable executions. Older work MUST NOT continue under materially incompatible governance/effect semantics without explicit compatibility/version handling.

### DEX-09 — Runtime identity is technical

Workflow ID, execution ID, run ID, queue item ID, task token, callback token and similar runtime references MUST NOT become NativeRef/MaterialStateRef/ExternalRef by identity.

### DEX-10 — Runtime infrastructure remains replaceable at the semantic boundary

The governed operation/effect contract and Domain/Logical state MUST remain intelligible without the chosen workflow engine's internal ontology.

## Candidate evaluation criteria

Candidates are compared against LifeOS-specific pressure, not feature-count marketing.

Priority criteria:

1. durable crash/restart recovery;
2. long waits and timers;
3. external events / human-in-the-loop;
4. retry/idempotency/external-effect ergonomics;
5. cancellation/timeout handling;
6. versioning / in-flight deployment evolution;
7. Python ecosystem fit;
8. operational/deployment complexity;
9. self-host/managed optionality;
10. observability and debugging;
11. decoupling from canonical Physical persistence;
12. local-development practicality;
13. ability to coexist with bounded DB/worker jobs rather than forcing one universal runtime.

## Candidate A — PostgreSQL + worker + transactional outbox style

### Strengths

- lowest conceptual/infrastructure expansion if PostgreSQL is already present;
- transactional publication/outbox can align committed canonical state with pending publication;
- queue-like worker claiming can be implemented with row locking such as `FOR UPDATE ... SKIP LOCKED` where appropriate;
- simple current-state inspection using ordinary database tooling;
- good fit for bounded jobs, publication, reindexing and short retry loops;
- no separate workflow platform required.

### Limitations

The application owns most higher-level durable semantics, including as applicable:

- durable timers/sleeps;
- external callback wait/correlation;
- human approval waits;
- workflow progression/state machine discipline;
- cancellation semantics;
- retry classification/backoff/dead-letter behavior;
- step replay protection;
- multi-step recovery;
- versioning of in-flight workflows;
- compensation/reconciliation coordination;
- operational UI/inspection beyond custom tooling.

PostgreSQL `SKIP LOCKED` is useful for queue-like consumers but intentionally provides an inconsistent view and is not a general-purpose consistency model. `LISTEN/NOTIFY` is useful simple IPC/signaling; structured durable state still belongs in tables and the application must handle listener/recovery behavior.

### Verdict

```text
POSTGRESQL + WORKER / OUTBOX
RETAIN

ROLE
BOUNDED ASYNC BASELINE

GENERAL LONG-RUNNING DURABLE ORCHESTRATOR
NOT PREFERRED
```

Do not reject this baseline merely because dedicated workflow technology exists. Do not promote it to universal durable orchestration merely because a database can store state.

## Candidate B — Restate

### Structural fit

Current Restate documentation provides:

- durable execution with replay/recovery of completed steps;
- durable timers/sleeps;
- durable external-event patterns;
- Awakeables for externally completed work;
- Durable Promises for workflow signaling;
- human-in-the-loop / webhook / asynchronous external-process patterns;
- Python SDK/runtime support;
- service/workflow state and reliable communication primitives;
- local single-server development path with later clustered/managed options.

These primitives map directly to LifeOS pressure around delayed provider effects, approval/review waits, external callbacks, AI/tool oversight and crash-resumable coordination.

### Strengths

- strong external-event/human-wait ergonomics;
- durable timers and stateful coordination are native rather than rebuilt application-by-application;
- Python support aligns with current backend direction;
- runtime can be introduced specifically at the durable boundary rather than becoming canonical persistence;
- suitable for service/agent/workflow patterns without requiring LifeOS Domain concepts to inherit a workflow ontology;
- current deployment model allows relatively lightweight local adoption compared with operating a larger workflow platform from day one.

### Risks / questions to benchmark later

- production HA/stateful operational model must be evaluated against actual deployment targets;
- retry behavior must be bounded explicitly for non-idempotent/ambiguous external effects;
- in-flight version/deployment rules must be tested against LifeOS governed-effect evolution;
- operational maturity/skills/ecosystem fit must be validated before production selection;
- exact retention/history behavior of workflow runtime state must not replace LifeOS material history/provenance.

### Verdict

```text
RESTATE
PREFERRED DEDICATED DURABLE-EXECUTION CANDIDATE

NOT SELECTED
NOT AUTHORIZED TO IMPLEMENT
```

The preference is structural-fit evidence, not an implementation decision.

## Candidate C — Temporal

### Structural fit

Current Temporal documentation emphasizes durable/crash-resumable Workflow Execution across failures and very long durations. Temporal provides Python support, durable timers/signals and asynchronous Activity completion patterns for externally completed work.

### Strengths

- strongest established durable-workflow platform in this candidate set;
- explicit long-running workflow model;
- strong crash/outage resume guarantees at workflow level;
- mature signal/external-event and asynchronous activity patterns;
- strong operational/debugging model and managed/self-hosted paths;
- Python SDK available;
- substantial ecosystem/history for durable business processes.

### Costs / risks

- larger platform/model commitment than bounded worker approaches;
- deterministic workflow/replay/versioning rules require deliberate engineering discipline;
- a dedicated Temporal service becomes significant runtime infrastructure;
- application team must prevent Temporal workflow state from becoming a replacement LifeOS ontology/history model;
- operational/platform overhead must be justified against actual LifeOS deployment scale and team capacity.

### Verdict

```text
TEMPORAL
STRONGEST / MANDATORY DEDICATED CHALLENGER

NOT SELECTED
```

Any later decision favoring Restate MUST continue to compare against Temporal on destructive LifeOS scenarios rather than eliminating Temporal by preference alone.

## Candidate D — DBOS

### Structural fit

Current DBOS documentation provides Python durable workflows, queues and workflow recovery by checkpointing execution state in PostgreSQL. DBOS therefore aligns closely with the current Python direction and can collapse part of the workflow-system footprint into PostgreSQL-backed runtime state.

### Strengths

- Python-first usable path;
- straightforward durable workflow/step programming model;
- durable queues and restart recovery;
- operational simplicity can be attractive when PostgreSQL is already accepted infrastructure;
- workflow metadata remains queryable in a relational system;
- useful fit for AI/unreliable API orchestration patterns.

### Costs / risks

- DBOS requires PostgreSQL for its system database, making candidate adoption dependent on PostgreSQL infrastructure even though LifeOS Physical persistence is not yet selected;
- choosing DBOS before the Physical stage would create an unjustified PostgreSQL coupling;
- distributed/HA operational requirements and managed/self-hosted boundaries require later validation;
- workflow/runtime tables remain technical runtime state and cannot become canonical semantic storage by convenience.

### Verdict

```text
DBOS
CONDITIONAL CHALLENGER

STRONGER IF POSTGRESQL SURVIVES PHYSICAL SELECTION
WEAKER AS A PRE-PHYSICAL COMMITMENT

NOT SELECTED
```

## Comparative result

Current Phase 7 ranking:

```text
BOUNDED ASYNC
1. PostgreSQL + worker/outbox style — baseline mechanism class

DEDICATED DURABLE EXECUTION
1. Restate   — preferred structural-fit candidate
2. Temporal  — strongest mandatory challenger
3. DBOS      — conditional PostgreSQL-dependent challenger
```

This is intentionally not one global ranking because the bounded-job problem and material durable-process problem are not identical.

## Why dedicated durable execution is structurally justified

The specialized-infrastructure rule permits adoption when measured workload OR sufficiently strong structural correctness/durability/reliability benefit exists.

LifeOS already has structural scenarios where dedicated durable execution materially reduces risk:

- a governed effect waits for approval while Authority/Consent/target state can change;
- provider request may have taken effect even when response is lost;
- process crashes between canonical commit and external side effect;
- reconciliation spans callbacks and manual resolution;
- queued action survives deployment/runtime restart;
- external callback arrives after a long wait;
- user cancels a pending technical process without necessarily cancelling the Domain target;
- retry/replay must preserve effect idempotency and provenance;
- AI/tool execution waits for human oversight or external completion.

Therefore the project does not require production traffic measurements before recognizing that a dedicated durable mechanism may be justified for those classes.

## External-effect boundary — no exactly-once fantasy

Every candidate must preserve:

```text
runtime durable execution
!= globally atomic external effect
```

A provider may apply an action while the response is lost. A workflow system can remember what it attempted and resume safely, but it cannot retroactively create a distributed transaction with an arbitrary external service.

Therefore Phase 5/6 requirements remain mandatory:

- bounded idempotency;
- provider-side idempotency keys where supported;
- effect inquiry/read-back where supported;
- explicit unknown outcome;
- reconciliation/compensation/manual resolution where necessary.

## Operation-class routing rule

A later implementation SHOULD classify background work before assigning runtime infrastructure.

### Bounded worker candidate

Prefer the simplest accepted bounded mechanism where the operation:

- is short-lived;
- has no durable human/external wait;
- can be retried safely under bounded idempotency;
- has simple failure/recovery state;
- does not require multi-step long-lived cancellation/compensation;
- can be reconstructed cheaply from canonical/outbox state.

### Dedicated durable candidate

Escalate to dedicated durable execution where one or more materially applies:

- long wait or timer is part of correctness;
- human approval/review is part of progression;
- asynchronous provider callback determines later progression;
- multiple steps cross failure domains;
- ambiguous external effects must be tracked across time;
- cancellation/timeout/deadline is materially stateful;
- crash/restart must resume from prior durable progression;
- in-flight workflow version must remain compatible across deployments;
- compensation/reconciliation spans multiple durable steps;
- debugging/recovery from partial execution otherwise requires substantial custom state-machine infrastructure.

This routing rule itself is current architecture guidance. Exact operation classes remain Phase 8/implementation-specific.

## Phase 8 handoff

The governed operation/effect contract MUST remain independent of the runtime selected here.

It may classify execution needs conceptually, for example:

```text
immediate
bounded asynchronous
durable long-running
```

but MUST NOT encode `TemporalWorkflow`, `RestateWorkflow`, `DBOSWorkflow` or database queue rows as semantic operation identity.

## Phase 10 benchmark carry-forward

If Phase 10/Physical choices materially alter runtime economics or coupling, Phase 7 ranking must be pressure-tested again.

Especially:

- PostgreSQL selected vs not selected;
- single-node/managed vs HA deployment expectations;
- actual RPO/RTO/SLO classes;
- provider/integration load;
- long-running workflow volume;
- operational team capacity.

The benchmark does not need to be repeated from zero unless those inputs materially change the conclusion.

## Evidence basis checked for this benchmark

Current primary technical evidence reviewed on 2026-08-17 includes:

- PostgreSQL current documentation for queue-like `SKIP LOCKED`, transactions and `LISTEN/NOTIFY` behavior;
- Restate current documentation for durable execution, Python external events, Awakeables/Durable Promises and timers;
- Temporal current documentation for durable Workflow Execution, Python SDK and asynchronous Activity completion;
- DBOS current documentation for Python durable workflows/queues and PostgreSQL-backed system state.

External product documentation is benchmark evidence, not LifeOS semantic authority.

## Phase 7 verdict

```text
PHASE 7 — DURABLE WORKFLOW / ASYNC BENCHMARK
PASS WITH CONDITIONAL RANKING

DOMAIN REOPEN REQUIRED          0
LOGICAL REOPEN REQUIRED         0
NEW DOMAIN OWNER REQUIRED       0
WORKFLOW ENGINE SELECTED        0
BACKEND IMPLEMENTATION STARTED  0

BOUNDED ASYNC BASELINE
PostgreSQL + worker/outbox style

DEDICATED PREFERRED CANDIDATE
Restate

MANDATORY STRONG CHALLENGER
Temporal

CONDITIONAL CHALLENGER
DBOS
```

This verdict authorizes Phase 8 contract work only. It does not authorize durable-runtime implementation.