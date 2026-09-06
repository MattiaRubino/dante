# Search / Observability / Calendar / Solver Boundaries

- Status: **CURRENT CONTRACT / HISTORICAL PHASE-9 SELECTION SNAPSHOT — consumed by the closed Physical Model**
- Stage: Pre-Physical Repository & Architecture Coherence / Phase-9 pressure input
- Phase-9 selection state recorded below: **specialized infrastructure not selected at that phase**
- Current Physical resolution: **PostgreSQL FTS + pgvector, OpenTelemetry + Grafana Alloy/Grafana Cloud EU target, OR-Tools 9.15 CP-SAT selected where applicable by PM-11/12**
- Observability implementation: **MATERIALIZED ON `feature/platform-observability`; final remote/stack proof pending**

> **Current-truth qualification:** the semantic pressure/boundary rules in this document remain current. Statements below such as `NOT SELECTED`, `NO VENDOR SELECTED`, `PREFERRED ... CANDIDATE` or `PHYSICAL MODEL SELECTED 0` are the truthful state **at Phase 9** and do not override later PM-11/12 selected truth.
>
> **Naming continuity:** `DANTE` is the current product/app name. `LifeOS` references retained below reflect the previous working/project name for the same product lineage and are preserved as historical evidence.

## Purpose

Define the Pre-Physical pressure and durable architecture boundary for:

- search / retrieval / indexing;
- observability / technical diagnostics;
- calendar interoperability;
- deterministic constraint solving / planning.

This contract consumes the CLOSED Domain Atlas, CLOSED Logical Model, `WL-H01..WL-H12`, all Phase 5 requirements, Phase 6 AI/integration boundaries, the Phase 7 durable-execution benchmark and the Phase 8 Governed Operation / Effect Contract.

At Phase 9 this document did not select a dedicated search cluster, vector database, observability vendor, calendar provider SDK, solver service topology or Physical persistence design. PM-11/12 later resolved the applicable target mechanisms without changing the boundary rules here.

## Current Physical resolution of Phase-9 selectable mechanisms

```text
SEARCH / LEXICAL
PostgreSQL native FTS + pg_trgm + unaccent — SELECTED

SEMANTIC / VECTOR
pgvector 0.8.6 — SELECTED / DERIVED RETRIEVAL

DEDICATED SEARCH / VECTOR SERVER
NONE IN ACCEPTED TARGET

OBSERVABILITY TARGET
OpenTelemetry + Grafana Alloy 1.19.2 + Grafana Cloud Free EU — SELECTED / MATERIALIZED TARGET

CALENDAR
standards/providers remain adapter pressure; no provider ontology adopted

SOLVER
OR-Tools 9.15 CP-SAT — SELECTED

DIRECT IMPLEMENTATION VALIDATION
APPLICATION/STATIC PROOF IN PROGRESS; ALLOY/POSTGRES/TARGET-STACK GATES REMAIN
```

# Cross-cutting invariant

```text
search/index projection
!= canonical truth

telemetry
!= Domain history / Provenance / security audit automatically

calendar/provider schema
!= LifeOS ontology

solver result
!= accepted canonical effect
```

Any action initiated from search, calendar integration, telemetry tooling or solver output still crosses the Phase 8 governed-operation boundary.

# Part I — Search / retrieval / indexing

## Search role

LifeOS search is a permission-/disclosure-aware discovery and retrieval capability over authorized canonical, historical, derived and explicitly connected-source material.

Search does not own the searched semantics. It returns bounded references/projections to sources that remain owned elsewhere.

Current product pressure includes:

- exact/structured filtering;
- keyword/full-text discovery;
- historical search;
- cross-domain search;
- connected-source discovery;
- semantic similarity where useful;
- natural-language question support;
- navigation from a result to the canonical/source object;
- action requests from search results through the governed-operation contract.

## SEARCH-01 — Structured filtering is a first-class baseline

Search MUST preserve deterministic filtering by accepted dimensions where available, including as applicable:

```text
time range
owner/type/facet
Person/participant
calendar/product profile
source/provider
status/lifecycle
sensitivity/disclosure scope
current vs historical
canonical vs provider vs derived/candidate category
```

Flexible search MUST NOT require every query to become semantic/vector search.

## SEARCH-02 — Full-text/keyword capability is baseline pressure

A later design SHOULD support practical lexical search and relevance ranking before specialized search infrastructure is adopted merely by fashion.

If PostgreSQL survives the Physical benchmark, its native text-search capabilities (`tsvector`, `tsquery`, phrase/query parsing, ranking and GIN/GiST indexing) form a strong baseline candidate.

This was conditional on PostgreSQL selection at Phase 9; PM-11/12 later selected PostgreSQL and the native lexical baseline.

## SEARCH-03 — Search ranking is derived state

```text
rank / relevance score
!= canonical priority
!= truth
!= Authority
!= semantic importance universally
```

Ranking may combine lexical match, recency, context, source quality, semantic similarity and other bounded signals, but the ranking function remains LR-08/technical projection logic.

When ranking affects consequential behavior, its material basis/freshness must be available under `WL-H09`.

## SEARCH-04 — Search miss != nonexistence

A missing result may reflect:

- authorization/disclosure filtering;
- index lag;
- lexical mismatch;
- approximate-retrieval recall;
- source/provider outage;
- query scope;
- redaction/deletion;
- stale projection;
- actual absence.

Therefore:

```text
not returned by search
!= canonical nonexistence
```

## SEARCH-05 — Disclosure applies before/through ranking

Search MUST preserve `WL-H03` and `WL-H12` across every observable surface, including:

- result inclusion/exclusion;
- result count;
- facets/aggregations;
- snippets/highlights;
- ranking/order;
- autocomplete/suggestions;
- semantic-neighbor candidates;
- explanation/reason text;
- source/provenance hints;
- timing/error differences.

A search index MUST NOT become a bypass around Visibility/Authority/Consent or reveal hidden relationship/source information through indirect signals.

## SEARCH-06 — Result references trace back to source/material basis

A result/projection SHOULD retain enough bounded source/reference/version/provenance metadata to open or revalidate the underlying material item where applicable.

The search document/index row/embedding ID does not become the Domain identity.

## Search/vector posture

Phase-9 posture:

```text
structured filters + lexical/full-text search
BASELINE

semantic/vector retrieval
BOUNDED CAPABILITY CANDIDATE

pgvector
BOUNDED CANDIDATE IF POSTGRESQL SURVIVES PHYSICAL SELECTION

dedicated search/vector service
NOT JUSTIFIED BY DEFAULT
```

Current PM-11/12 resolution selects PostgreSQL lexical search and pgvector while keeping a dedicated search/vector service out of the accepted target.

### pgvector-specific pressure

Current pgvector documentation distinguishes:

```text
exact nearest-neighbor search
vs
approximate HNSW / IVFFlat search
```

Approximate indexes trade recall for speed. Filtering may occur after an ANN scan, so authorization/scope filtering can materially affect result count/recall/performance. Shared approximate indexes across tenants/scopes can also create recall/performance coupling.

Therefore a later vector benchmark MUST test:

- exact vs approximate recall;
- filtering under authorization/sensitivity constraints;
- result-count stability;
- tenant/user/scope isolation strategies;
- delete/redaction propagation;
- index staleness;
- ranking reproducibility where consequence matters;
- performance against exact lexical/structured baseline.

### Vector non-collapse

```text
embedding similarity
!= semantic truth

nearest neighbor
!= Evidence automatically

semantic retrieval result
!= canonical relationship

model/vector confidence
!= Authority / Decision / Confirmation
```

Vector output may feed candidate/retrieved context, not bypass canonical interpretation.

## Search index lifecycle

Index/projection state is downstream technical state.

Later design MUST define:

```text
source/material version basis
index update trigger/cadence
staleness semantics
delete/redaction propagation
rebuild/reindex behavior
index recovery after restore
provider/source availability behavior
```

A rebuilt index may be disposable/reconstructable; canonical history must not depend exclusively on retaining index internals.

# Part II — Observability / technical diagnostics

## Observability role

Observability exists to diagnose and operate the technical system. It does not replace canonical/domain history, governance provenance or dedicated security/audit requirements.

Phase-9 direction:

```text
OpenTelemetry-first or equivalent standards-based instrumentation
```

OpenTelemetry semantic conventions are useful for consistent technical naming/correlation across traces, metrics, logs, profiles and resources. They remain telemetry conventions rather than LifeOS ontology.

## OBS-01 — Technical correlation identities remain distinct

```text
trace_id
span_id
request_id
workflow/execution id
idempotency key
correlation id
NativeRef
MaterialStateRef
ExternalRef
```

are not semantically interchangeable.

A trace may correlate with a governed operation while remaining technical observability state.

## OBS-02 — Telemetry is not the sole audit/provenance store

Telemetry may be sampled, expired, filtered, unavailable or vendor-transformed.

Information required by `WL-H11`, Phase 5 security requirements or the Phase 8 execution/effect contract MUST NOT exist only because a telemetry backend happened to receive it.

```text
telemetry event
!= Domain Provenance automatically
!= material history automatically
!= security audit record automatically
```

## OBS-03 — Privacy minimization applies to observability

The system MUST NOT solve diagnostics by indiscriminately logging:

- prompts;
- tool payloads;
- health/sensitive personal data;
- raw provider content;
- credentials/tokens;
- private notes;
- hidden relationship/governance detail.

Operational identifiers/attributes must be bounded to diagnostic purpose and retention.

High-cardinality identifiers must also be treated deliberately to avoid cost/performance/pathological telemetry behavior.

## OBS-04 — Required pressure signals

Later runtime/Physical design SHOULD make the following observable without requiring sensitive payload logging:

- request/operation latency/error classes;
- expected-state conflicts;
- authorization-denial categories at safe aggregation level;
- worker/durable-execution backlog;
- retry rates;
- long durable waits;
- provider/API latency/failure/rate-limit state;
- unknown external outcomes;
- provider sync lag/divergence;
- reconciliation/compensation backlog;
- outbox/publication lag where applicable;
- search/index lag/rebuild pressure;
- deletion/redaction propagation lag;
- solver runtime/status classes;
- restore/recovery verification failures;
- capacity/backpressure/resource exhaustion.

Exact metrics/SLOs remain tied to Phase 5 open NFR parameters.

## OBS-05 — Result/error telemetry preserves semantic distinction

Technical dashboards MUST NOT merge materially different cases merely for simple counting where doing so hides correctness risk.

Examples:

```text
provider failure known
!= provider outcome unknown

canonical conflict
!= validation failure

security safe-deny
!= canonical absence of Authority

solver UNKNOWN
!= INFEASIBLE

search index miss
!= canonical not found
```

Aggregation may group them at higher levels only if the underlying distinction remains recoverable where operationally necessary.

## Observability vendor posture

At Phase 9, no vendor was selected. PM-11/12 later selected the target
`OpenTelemetry + Grafana Alloy + Grafana Cloud EU`. The current bounded
materialization uses Alloy 1.19.2 pinned by image digest and Grafana Cloud Free
EU; exact runtime, privacy, failure and budget behavior is owned by
`observability-runtime-contract.md`.

Specialized observability infrastructure remains bounded by operational requirements rather than assumed as semantic authority.

# Part III — Calendar interoperability pressure

## Calendar boundary

LifeOS owns its accepted Domain/Logical time/scheduling semantics.

External calendar standards/providers are interoperability pressure and adapter contracts, not ontology authority.

```text
iCalendar VEVENT
!= LifeOS Event by identity

provider event id
!= NativeRef

RRULE text
!= required Physical representation of LifeOS Recurrence

provider sync token / ETag
!= MaterialStateRef
```

## CAL-01 — Recurrence must preserve source/series/occurrence distinctions

Interoperability pressure includes recurrence sets generated from a source/series rule plus inclusions/exclusions/overrides.

LifeOS must preserve its own accepted distinctions among:

```text
Routine / Recurrence
Occurrence
Schedule
Session
Actual
```

A provider recurrence instance may map to an Occurrence/Schedule representation according to the bounded adapter contract, but provider recurrence identity must not redefine the Domain model.

## CAL-02 — Instance exception/override semantics are first-class pressure

RFC 5545 recurrence semantics include the recurrence set and `RECURRENCE-ID`-style instance addressing. JSCalendar includes recurrence rules and per-instance recurrence overrides.

LifeOS must pressure-test at least:

- one occurrence changed;
- one occurrence cancelled/excluded;
- additional occurrence;
- selected/future occurrences changed;
- source recurrence later revised;
- provider exception arrives out of order;
- historical instance reconstructed after source-rule change.

The exact mapping depends on provider/standard semantics and must retain provenance.

## CAL-03 — Timezone/floating/local-time semantics must survive

Calendar adapters MUST preserve enough information for accepted timezone/DST/effective-time semantics.

Pressure includes:

```text
UTC instant
zoned local time
floating local time
all-day date semantics
DST gap
DST fold/ambiguity
timezone rule change
historical timezone interpretation
```

Technical UTC normalization MUST NOT erase the original semantic local/zoned meaning required for future recurrence or historical reconstruction.

JSCalendar explicitly distinguishes a timezone identifier from `null` floating time. iCalendar carries timezone and recurrence semantics through its own representation. These are adapter evidence, not a mandate to copy either schema internally.

## CAL-04 — All-day/date semantics are not ordinary timed instants

Provider/standard all-day events may use date-only boundaries. LifeOS adapters MUST avoid fabricating timezone-shifted timed events merely to fit one storage representation.

## CAL-05 — Provider sync tokens are adapter state

Google Calendar incremental synchronization is a representative pressure case:

- an initial/full synchronization can yield a sync token;
- incremental requests use that token;
- deleted entries participate in synchronization;
- tokens can become invalid and require a new full synchronization.

Therefore:

```text
sync token invalidated
!= LifeOS canonical state invalidated

full provider resync
!= delete/recreate canonical LifeOS truth blindly
```

Provider re-baselining must reconcile provider state/mappings without pretending canonical history never existed.

## CAL-06 — Provider deletion/cancellation semantics require mapping

Provider `deleted`, `cancelled`, missing, tombstoned or inaccessible states may have provider-specific meaning.

They MUST NOT be mapped blindly to LifeOS Event/Activity/Schedule cancellation or nonexistence without the bounded integration policy.

## CAL-07 — Free/busy is a disclosure projection

Free/busy/availability responses are bounded derived/disclosure surfaces.

A recipient may legitimately learn:

```text
unavailable 18:00–20:00
```

without learning the hidden source reason/event.

Search/calendar/provider integration must preserve `WL-H03`/`WL-H12` and must not leak private source detail through busy labels, counts, conflicts or explanations.

## CAL-08 — Calendar action uses governed operation contract

An adapter action such as create/update/delete/move at a provider MUST flow through Phase 8.

```text
LifeOS governed effect
→ adapter/provider request
→ provider acknowledgement/result
→ canonical/provider reconciliation as applicable
```

Provider API method names do not become canonical operation semantics.

## Calendar technology posture

Current architecture does not require native internal iCalendar or JSCalendar persistence.

Current posture:

```text
iCalendar / JSCalendar
INTEROPERABILITY / TEST CORPUS / ADAPTER PRESSURE

Google/Microsoft/other provider calendar APIs
PROVIDER-SPECIFIC ADAPTER PRESSURE

LifeOS Domain + Logical model
SEMANTIC AUTHORITY
```

Compatibility should be pursued where it improves interoperability without weakening LifeOS semantics.

# Part IV — Deterministic solver / planner boundary

## Solver role

LifeOS needs deterministic planning/constraint evaluation for scheduling and replanning problems where explicit constraints/objectives can be represented.

AI remains useful for:

- interpreting ambiguous natural-language constraints;
- explaining solutions/trade-offs;
- generating candidate policies/objectives for review;
- cross-domain reasoning where deterministic modeling is incomplete.

AI should not replace a deterministic solver for constraints the system can represent explicitly.

## SOLVER-01 — Hard constraints are not silently relaxed

Hard constraints MUST remain explicit and MUST NOT be weakened merely to produce a visually pleasing/feasible plan.

If the model is infeasible, LifeOS may:

- report the conflict;
- explain a minimal/meaningful subset where possible;
- propose which constraint could be changed;
- widen replanning scope;
- ask the user/authorized actor for a Decision/change.

It must not silently violate the constraint.

## SOLVER-02 — Soft preferences/objectives remain distinguishable

Preferences, priorities and optimization weights are not hard truth.

The solver model MUST distinguish as applicable:

```text
hard constraint
soft preference
objective/weight
penalty
candidate decision variable
```

A weight is technical/model input and does not become a universal Domain priority owner.

## SOLVER-03 — Solver status semantics remain truthful

Current OR-Tools CP-SAT provides materially useful result distinctions:

```text
OPTIMAL
FEASIBLE
INFEASIBLE
MODEL_INVALID
UNKNOWN
```

LifeOS MUST preserve equivalent distinctions where applicable rather than collapsing them to success/failure.

In particular:

```text
UNKNOWN
!= INFEASIBLE
```

A time/memory/custom limit may produce no proof of infeasibility.

## SOLVER-04 — Solver result is candidate/projection, not effect

```text
solver solution
!= accepted Schedule automatically
!= Decision automatically
!= Authority
```

Conceptual flow:

```text
material input snapshot
+ constraints/objective
→ solver
→ candidate/scenario
→ explanation/preview as applicable
→ Governed Operation Request
→ accepted canonical effect if authorized
```

Direct solver writes to canonical scheduling state are rejected as general architecture.

## SOLVER-05 — Material input basis is reconstructible where consequence matters

For consequential planner output, preserve enough basis to reconstruct as applicable:

- target scope;
- material state/version snapshot;
- availability/capacity/dependency basis;
- hard constraints;
- soft preferences;
- objective/weights;
- solver/model version;
- time limit/search configuration where it affects result status;
- candidate result/status.

This supports explanation, stale-result rejection and repeatability without making every solver trace canonical history.

## SOLVER-06 — Replanning starts with smallest viable scope

Current product behavior remains:

```text
choose the smallest scope that can produce a valid useful result
→ expand only when needed
```

Pressure scopes may include:

- selected item;
- surrounding dependencies/blocks;
- day;
- week;
- remaining date range;
- remaining Plan/Routine/program profile.

A solver should not rearrange the whole user's life merely because a larger search space exists.

## SOLVER-07 — Existing accepted state is not disposable input

Fixed commitments, Authority/Consent/Visibility boundaries, material decisions, professional restrictions, hard temporal constraints and accepted external/provider commitments MUST be represented according to their actual semantics.

A solver objective MUST NOT override them simply because another solution scores better.

## SOLVER-08 — Uncertain inputs remain uncertain

Candidate/unresolved information, stale provider availability or incomplete data must not be silently hardened into deterministic truth.

The system may solve under explicit assumptions/scenarios but must preserve the assumption boundary.

## Solver technology posture

Phase-9 posture:

```text
simple deterministic rules / heuristics
BASELINE

OR-Tools CP-SAT
PREFERRED SPECIALIZED SOLVER BENCHMARK CANDIDATE

AI
INTERPRETATION / AMBIGUITY / EXPLANATION / REASONING
NOT DETERMINISTIC CONSTRAINT AUTHORITY
```

PM-11/12 later selected OR-Tools 9.15 CP-SAT; its output remains candidate/derived state until governed acceptance.

### Why CP-SAT is a strong candidate

Current OR-Tools documentation supports integer constraint programming with result states that distinguish feasible/optimal/infeasible/unknown outcomes and is widely applicable to scheduling/assignment-style problems.

Structural benefits for LifeOS include:

- hard/soft constraint modeling;
- interval/scheduling primitives in the OR-Tools ecosystem;
- deterministic service boundary independent from LLM output;
- ability to time-bound search and preserve `UNKNOWN` rather than fabricate infeasibility;
- Python support consistent with backend direction.

### Limits / later benchmark questions

- integer-only CP-SAT modeling may require bounded conversion of some continuous concepts;
- objective design can embed product assumptions and therefore requires explicit governance/validation;
- model size/performance must be benchmarked on realistic LifeOS schedules;
- incremental/repeated replanning latency must be tested;
- explanation of infeasibility/trade-offs may require additional model instrumentation;
- solver use does not remove the need for Domain/Logical materiality and Phase 8 effect validation.

No solver implementation was performed by Phase 9. Direct selected-stack solver validation remains `NOT RUN` until separately executed.

# Cross-pressure tests

Phase 9 establishes the following destructive/cross-boundary tests for later Physical/runtime implementation.

## Search + governance

1. hidden object must not appear through result count/ranking/autocomplete;
2. visible endpoint pair must not expose hidden relationship;
3. index lag after Visibility revocation must not leak data;
4. deletion/redaction must propagate to lexical/vector projection or expose pending state safely;
5. ANN filtering must not silently return unauthorized candidates.

## Search + action

6. user finds an item and requests a change; the search result reference must resolve/revalidate through Phase 8 expected-state/governance rather than acting on stale index payload;
7. AI-generated search answer must distinguish canonical records, provider/live data and inference.

## Observability + privacy

8. trace/debug data cannot contain broad sensitive payload by default;
9. sampled/missing telemetry cannot destroy the ability to reconstruct a consequential effect where required;
10. unknown provider outcome remains diagnosable separately from known failure.

## Calendar + recurrence

11. recurrence crosses DST gap/fold;
12. one occurrence override followed by source recurrence change;
13. provider sync token invalidation/full resync without canonical-history destruction;
14. provider event deleted while LifeOS canonical item has independent accepted state;
15. free/busy projection exposes availability without private reason.

## Solver + effect

16. stale availability/constraint snapshot used after target state changed;
17. solver reports `UNKNOWN` under time limit and must not be presented as infeasible;
18. hard constraint conflicts and no valid solution exists;
19. feasible solution exists but violates a later governance/consent change before execution;
20. solver candidate accepted only through Phase 8 governed effect;
21. broad replan is rejected when a smaller scope satisfies constraints.

## Combined durable execution

22. long-running replan/provider action waits for human confirmation and Authority changes during wait;
23. provider applies calendar change but response is lost; retry must not duplicate effect;
24. crash occurs after canonical commit but before provider/index publication;
25. pending delete/redaction propagation survives restart without exposing forbidden content.

# Specialized-infrastructure rule applied

Phase-9 result:

```text
DEDICATED SEARCH CLUSTER
NOT JUSTIFIED YET

DEDICATED VECTOR DATABASE
NOT JUSTIFIED YET

PGVECTOR
BOUNDED CANDIDATE IF POSTGRESQL SELECTED

OPENTELEMETRY-FIRST / EQUIVALENT
PHASE-9 OBSERVABILITY DIRECTION
NO VENDOR SELECTED AT PHASE 9

CALENDAR STANDARD/PROVIDER SDK
ADAPTER CONCERN
NO ONTOLOGY AUTHORITY

OR-TOOLS CP-SAT
PREFERRED SPECIALIZED SOLVER BENCHMARK CANDIDATE
NOT IMPLEMENTED AT PHASE 9
```

Later PM-11/12 resolution selected pgvector, OpenTelemetry + Grafana Alloy/Grafana Cloud EU target and OR-Tools 9.15 CP-SAT while keeping dedicated search/vector servers out of the accepted target.

Specialized infrastructure may become justified by measured load or structural correctness/reliability/evolvability benefit. Phase 10 already supplies explicit synthetic LOW/BASE/HIGH qualification envelopes and sensitivity rules; later direct selected-stack validation executes applicable scenarios rather than inventing new scale claims here.

# Open decisions / parameters from Phase 9

Phase 9 deliberately left the following open. Some technology-level choices were later resolved by PM-11/12, while configuration/deployment details remain for Development Profile/implementation:

```text
search indexing topology
search document projection shape
lexical ranking formula
semantic embedding model/provider
vector dimensions/distance metric
exact vs approximate vector query classes
HNSW / IVFFlat parameterization
dedicated search/vector adoption threshold
index refresh/consistency SLOs
OpenTelemetry SDK/Collector deployment shape
telemetry backend/vendor
trace/log/metric retention
sampling strategy
high-cardinality policy
calendar provider SDK choices
provider-specific recurrence mapping
provider sync polling/webhook strategy
CalDAV adoption if any
solver model decomposition
solver objective weights
solver time limits by operation class
solver service deployment topology
```

Current target selection does not imply every configuration parameter above is fixed.

# Physical benchmark-method integration already established

The current Phase 10 Physical benchmark specification/register/corpus already consume this document together with Phases 5–8.

The Phase 10 method carries forward candidate pressure around:

- lexical/structured search baseline;
- optional vector projection and ANN filtering/recall;
- long history with current-state/search access;
- privacy-safe observability;
- provider/calendar recurrence and sync state;
- solver input/result materiality;
- durable execution ranking from Phase 7;
- governed-effect contract from Phase 8;
- Phase 5 open scale/latency/availability/RPO/RTO scenarios.

No Physical database/search/runtime selection was made **by this Phase-9 document or by the Phase-10 method itself**; PM-11/12 later made the explicit target selection.

# Evidence basis checked for this contract

Primary technical evidence reviewed for this contract includes:

- PostgreSQL documentation for full-text search types, query parsing and relevance ranking;
- pgvector project documentation for exact vs approximate HNSW/IVFFlat search, filtering and recall behavior;
- OpenTelemetry semantic-conventions documentation;
- RFC 5545 iCalendar recurrence/timezone semantics;
- RFC 8984 JSCalendar recurrence overrides and timezone/floating-time semantics;
- Google Calendar incremental-sync documentation including sync-token invalidation/full-resync behavior;
- Google OR-Tools CP-SAT documentation and status semantics.

External standards/products are pressure evidence and adapter inputs, not LifeOS semantic authority.

# Phase 9 verdict

```text
PHASE 9 — SEARCH / OBSERVABILITY / CALENDAR / SOLVER PRESSURE
PASS

DOMAIN REOPEN REQUIRED             0
LOGICAL REOPEN REQUIRED            0
NEW DOMAIN OWNER REQUIRED          0
DEDICATED SEARCH ENGINE SELECTED   0   # at Phase 9
VECTOR DATABASE SELECTED           0   # at Phase 9
OBSERVABILITY VENDOR SELECTED      0   # at Phase 9
CALENDAR PROVIDER MODEL ADOPTED    0
SOLVER IMPLEMENTED                 0   # at Phase 9
PHYSICAL MODEL SELECTED            0   # at Phase 9
BACKEND IMPLEMENTATION STARTED     0

SEARCH BASELINE
structured + lexical/full-text

VECTOR
bounded candidate only

OBSERVABILITY
OpenTelemetry-first / equivalent

CALENDAR
standards/providers = interoperability pressure

SOLVER
OR-Tools CP-SAT = preferred specialized benchmark candidate
```

This verdict remains current downstream architecture pressure. It records **Phase-9 state**, not current PM-11/12 selection. Current target selection is PostgreSQL lexical search + pgvector, OpenTelemetry + Grafana Alloy/Grafana Cloud EU target and OR-Tools 9.15 CP-SAT; direct implementation validation remains not started.
