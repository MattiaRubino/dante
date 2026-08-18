# Consistency / Side-Effect Requirements

- Status: **CURRENT — Phase 5 accepted requirement package**
- Stage: Pre-Physical Repository & Architecture Coherence
- Physical/runtime mechanism selection: **DEFERRED**

## Purpose

Define the consistency, concurrency, idempotency, provider/external-effect and reconciliation requirements that later Physical/runtime/API/backend work must satisfy.

This package defines semantics and acceptance pressure. It does not select transaction isolation, optimistic-lock tokens, outbox/inbox design, queue, workflow engine, event bus, saga framework, CRDT/OT strategy or database technology.

## Accepted upstream boundary

The CLOSED Logical Model already requires:

```text
WL-H05 expected-state semantics for consequential writes
WL-H06 idempotency != semantic identity
WL-H07 truthful atomic/staged multi-owner consistency
WL-H08 canonical state != provider sync state
WL-H09 consequential derived-state use requires freshness/material basis
```

The Domain/Logical model also rejects universal last-write-wins, provider-wins, user-wins, recency-wins and AI-confidence-wins as canonical reconciliation policy.

Conflict detection and conflict resolution remain distinct. Unresolved conflict is valid reality.

## Normative requirements

### CONS-01 — Consequential writes use expected-state semantics

A consequential mutation MUST carry, derive or otherwise enforce an expected materially relevant state/precondition when stale execution could materially corrupt meaning.

The accepted mechanism MUST prevent a stale operation from silently applying as though it were based on the current material state.

### CONS-02 — Technical concurrency token is not MaterialStateRef

ETag, MVCC version, database row version, provider revision, timestamp, content hash or equivalent technical token MAY support concurrency control but MUST NOT be treated as semantically identical to `MaterialStateRef`.

Where both semantic and technical state matter, the design MUST preserve both questions.

### CONS-03 — Idempotency controls repeated effect, not identity

Retry/replay handling MAY use idempotency semantics so one intended operation does not produce duplicate effect.

An idempotency key MUST NOT become native Domain identity, Goal/Request/Decision identity or a universal command identifier by implication.

### CONS-04 — Conflicting idempotency reuse rejects

Reusing an idempotency key/correlation binding for a materially different operation MUST conflict/reject rather than silently returning or applying the first operation's result as though the requests were equivalent.

Key lifetime/scope remains implementation-deferred but MUST be sufficient for the accepted retry/failure contract.

### CONS-05 — No silent material last-write-wins

Arrival order, write timestamp, latest provider revision or newest local write MUST NOT automatically resolve materially consequential conflict.

A low-consequence technical overwrite policy MAY exist only where the owning semantics explicitly prove the changes are non-material for that purpose.

### CONS-06 — Conflict detection != conflict resolution

The system MUST be able to represent:

```text
conflict known
resolution unresolved
```

without manufacturing a winner.

Resolution requires an applicable bounded basis such as semantic equivalence, accepted source-of-record policy, Authority, Decision, Evidence, user/specialist action or another accepted deterministic rule.

### CONS-07 — Multi-owner atomicity follows semantic invariants

Where one governed operation changes multiple semantic owners/facets and accepted invariants require all-or-nothing success, later Physical/runtime design MUST provide an atomic consistency boundary adequate to that invariant.

The implementation MUST NOT split an invariant solely because a storage mapping makes atomicity inconvenient.

### CONS-08 — Distributed/provider non-atomicity is represented truthfully

When external/provider/distributed effects cannot share an atomic boundary with canonical state, the system MUST expose the actual state truthfully, such as:

```text
pending
staged
partially applied
external acknowledgement pending
failed after canonical commit
external success / canonical reconciliation pending
compensation pending
unresolved
```

Exact status vocabulary remains operation-specific; one universal status enum is not required.

Hidden partial success represented as complete success is forbidden.

### CONS-09 — Canonical effect state is separate from provider apply/sync state

Provider acknowledgement, revision, delivery, apply result or synchronization status MUST NOT automatically determine canonical LifeOS truth.

Canonical state and provider/external state MUST remain independently addressable enough for reconciliation and diagnosis.

### CONS-10 — Retry after ambiguous technical failure must not duplicate consequence

For operations where the caller cannot know whether a prior attempt took effect, the runtime MUST have an accepted strategy to determine/reconcile prior effect before creating another materially identical consequence.

This applies both to canonical writes and external/provider side effects according to their consequence class.

### CONS-11 — External irreversible/partial effects require explicit reconciliation or compensation semantics

If an external effect succeeds and a later local step fails, or vice versa, the system MUST NOT claim a rollback that did not happen.

The design MUST expose and resolve/compensate/reconcile the actual partial state according to the governed operation's contract.

Compensation is not assumed to be a literal inverse; some effects may require manual resolution or may be irreversible.

### CONS-12 — Consequential derived-state inputs require freshness/material basis

When a canonical effect depends on LR-08 derived/effective state such as Effective Availability, Capacity, Authority, Visibility, candidate set or another projection, the effect MUST revalidate or bind to an accepted material derivation basis/snapshot before consequence where staleness could matter.

A cache hit MUST NOT become semantic proof of freshness.

### CONS-13 — Delayed execution validates both target and governance applicability

A delayed/queued consequential effect MUST evaluate the applicability of:

- the target material state/precondition; and
- the applicable governance/authorization basis;

at the appropriate execution boundary.

A previously valid operation MUST NOT execute after a material target/governance change merely because it remained in a queue.

### CONS-14 — Effect history is reconstructible where consequence warrants

For consequential effects, the system MUST retain/reconstruct enough bounded correlation/provenance to determine as applicable:

```text
what operation/effect was intended
who/what initiated it
which target/material basis applied
which governance basis applied
which idempotency/correlation context applied
what canonical effect occurred
what external/provider effect was attempted
what external acknowledgement/result occurred
what conflict/partial/reconciliation state followed
```

This does not require universal event sourcing.

### CONS-15 — Concurrent device/provider/actor divergence remains representable

If two materially divergent states arise from a common base, both MUST be preservable long enough to apply the accepted reconciliation policy.

The system MUST NOT discard one branch solely because it arrived later/earlier.

### CONS-16 — Merge is semantic/facet-aware, not generic payload merge

Independent non-conflicting changes MAY be combined only where the owning semantics prove the facets can coexist safely.

A generic JSON/object merge algorithm MUST NOT decide Domain materiality, Authority or truth by itself.

### CONS-17 — Publication/notification side effects respect commit truth

If later runtime publishes events/messages/notifications/provider actions derived from canonical changes, the design MUST prevent publishing a durable success claim for a canonical transaction that did not commit.

Likewise, successful canonical commit with pending publication MUST remain recoverable/retriable without duplicating materially identical publication effect.

This requirement creates outbox/publication pressure but does not preselect a transactional-outbox implementation.

### CONS-18 — Consumer/replay processing preserves idempotent effect semantics

If later architecture uses queues, streams, workflows or provider callbacks with at-least-once delivery/replay possibility, consumers MUST tolerate duplicate delivery without duplicating the governed consequence.

Transport message identity MUST remain distinct from semantic owner identity.

### CONS-19 — Reconciliation history preserves prior assertions/results where material

A later resolution/correction MUST NOT rewrite prior competing assertions, provider states or decisions as though they never existed where retention policy permits reconstruction.

Current accepted result remains owned by the affected semantic owner, not by a universal reconciliation object.

### CONS-20 — Absence and timeout are not automatically negative semantic results

Missing acknowledgement, timeout, unavailable provider or absent response MUST NOT automatically become semantic `false`, `declined`, `cancelled`, `not performed` or `not authorized` unless the owning operation/policy explicitly defines that consequence.

Unknown/pending/unresolved outcomes remain representable.

## Open parameters / decisions

The following must be explicitly resolved before dependent implementation/benchmark acceptance:

```text
CONS-OPEN-01 operation classes requiring strict atomic multi-owner commit
CONS-OPEN-02 operation classes allowed explicit staged/partial state
CONS-OPEN-03 idempotency scope/lifetime by operation class
CONS-OPEN-04 retry/backoff/dead-letter policy classes
CONS-OPEN-05 external-effect acknowledgement semantics by integration mode
CONS-OPEN-06 compensation/manual-reconciliation requirements by effect class
CONS-OPEN-07 conflict escalation/user-review thresholds
CONS-OPEN-08 allowable low-consequence auto-merge/equivalence rules
CONS-OPEN-09 publication durability requirements by message/event class
CONS-OPEN-10 duplicate/replay windows that benchmark candidates must survive
```

## Deferred mechanisms — not selected by Phase 5

No choice is made here among:

```text
transaction isolation level
row/advisory/application locking
ETag/version token format
transactional outbox
inbox/dedup store
queue/event bus/stream product
workflow engine
saga framework
CRDT / OT
retry library
idempotency database/schema
provider sync engine
change-data-capture/event-log strategy
universal event sourcing
```

A later mechanism is acceptable only if it satisfies the accepted semantics above.

## Downstream acceptance / benchmark pressure

Physical/runtime candidates MUST be tested against destructive cases including:

1. two concurrent consequential writes from the same material base;
2. materially different reuse of one idempotency key;
3. multi-owner invariant requiring all-or-nothing state;
4. canonical commit succeeds but external provider action fails;
5. provider action succeeds but canonical follow-up fails;
6. timeout where external outcome is initially unknown;
7. duplicate/replayed message or callback;
8. stale LR-08 availability/authority input used for a consequence;
9. delayed operation after Authority/Consent/target state changes;
10. offline/device/provider divergence requiring unresolved reconciliation;
11. restore/restart between commit and publication/side effect;
12. schema/runtime upgrade while pending effects/reconciliation remain in flight.

## Traceability

Primary downstream Logical pressure:

```text
WL-H04 absence/unknown != false
WL-H05 expected-state semantics
WL-H06 idempotency != identity
WL-H07 truthful atomic/staged consistency
WL-H08 canonical != provider state
WL-H09 derived-state freshness/material basis
WL-H11 AuthZ/effect provenance where applicable
```

This package does not authorize SQL/schema/API/backend/runtime implementation.
