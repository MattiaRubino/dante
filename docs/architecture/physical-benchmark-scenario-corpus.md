# Physical Benchmark Scenario Corpus

- Status: **CURRENT CORPUS / HISTORICAL PHASE-TIME EXECUTION STATUS — Phase 10 QA PASS / consumed by the closed Physical Model**
- Stage: Physical Model benchmark corpus authority
- Phase-time Physical state recorded at corpus handoff: **AUTHORIZED / IN PROGRESS — PM-00 BOOTSTRAP**
- Current Physical truth: **CLOSED / SELECTED / ACCEPTED / integrated via PR #15**
- Direct benchmark execution: **NOT RUN / direct HG PASS 0**
- Business forecast: **NOT ASSERTED BY THIS DOCUMENT**

> **Current-truth qualification:** the fixture families, scenarios, synthetic tiers, assertions and sensitivity inputs below remain the current reusable corpus. Statements describing PM-00, the active Physical branch or future benchmark execution are truthful **phase-time handoff state** and do not override PM-11/12/13/14 closure. Later selection did not retroactively execute this corpus.
>
> **Naming continuity:** `DANTE` is the current product/app name. `LifeOS` references retained in this corpus reflect the previous working/project name for the same product lineage and are preserved in the benchmark/evidence vocabulary.

## Purpose

Define the common LifeOS fixture families, destructive scenarios, synthetic qualification tiers and sensitivity inputs for candidate-specific idiomatic mappings and later selected-stack validation.

This corpus is designed to test correctness first and performance second.

```text
SYNTHETIC BENCHMARK TIER
!= BUSINESS / SALES FORECAST
```

The numeric tiers below exist to make benchmark runs reproducible before accepted product-scale evidence exists. They may be replaced or supplemented by later accepted evidence without weakening semantic assertions.

## Authority

This corpus consumes:

- the CLOSED Domain Atlas and Logical Model;
- `WL-H01..WL-H12`;
- all Phase 5 requirements;
- Phase 6 AI/context/runtime and Integration Hub boundaries;
- Phase 7 durable-execution pressure;
- Phase 8 Governed Operation / Effect Contract;
- Phase 9 search/observability/calendar/solver pressure;
- `physical-benchmark-specification.md`.

The corpus does not create new Domain owners, product requirements or Physical decisions.

# Corpus families

## C0 — Semantic correctness corpus

Purpose: prove that the candidate mapping can represent the accepted semantic model before performance numbers count.

Minimum contents:

- all 57 Domain concepts represented through applicable Logical families;
- all 15 native identity-bearing owners;
- contextual Actor / Subject / Resource use without native-identity collapse;
- representative LR-01..LR-13 records/projections/policies/history;
- NativeRef / ScopedRecordRef / MaterialStateRef / ExternalRef examples;
- representative typed binary and n-ary relation families;
- Authority / Consent / Visibility / Representation examples;
- Agreement terms with justified material binding;
- Proposal / Decision / Confirmation / effective-state separation;
- Version / Reconciliation / Provenance examples;
- canonical / provider / derived / candidate state separation.

Mandatory correctness assertion:

```text
no fixture requires universal Entity/Thing/EAV/generic-edge ontology
```

## C1 — Deep personal history corpus

Purpose: pressure material history, provenance and current-state efficiency for long-lived LifeOS use.

Fixture pattern:

- one or a few long-lived personal contexts;
- repeated changes across plans, activities, schedules, actuals, observations and relationships;
- corrections that supersede but do not falsify prior states;
- authority/visibility/consent changes over time;
- provider revisions and reconciliation state;
- derived projections rebuilt from changing material bases;
- tombstone/redaction events;
- historical references spanning schema/mapping evolution.

Benchmark must measure both:

```text
current-state access
AND
historical reconstruction
```

Current reads must not require lifetime replay by default.

## C2 — Population / concurrency corpus

Purpose: measure independent-account scale plus collisions on materially shared targets.

Contains:

- many independent personal accounts/owners;
- web + mobile concurrent clients;
- intentionally contended owners/material states;
- low-contention background reads/writes;
- provider callback traffic;
- history and projection growth during active writes.

The corpus includes expected-state races rather than only embarrassingly parallel CRUD.

## C3 — Governance / disclosure corpus

Purpose: test semantic governance and `WL-H12` non-interference.

Includes:

- same canonical source visible differently to different recipients;
- Visibility constraints on owner, relation and derived surfaces;
- Authority effective/expired/revoked states;
- Consent effective/withdrawn states;
- Representation with actual Actor distinct from represented party;
- hidden relation existence;
- hidden candidate membership;
- free/busy disclosure without source exposure;
- counts/rankings whose raw values could leak hidden records;
- error and not-found behaviors with hidden targets;
- search/index projection with access changes after indexing.

## C4 — Integration / provider corpus

Purpose: pressure `ExternalRef`, canonical/provider separation and reconciliation.

Includes:

- provider objects scoped by provider + account/tenant/integration context;
- same opaque provider ID in different scopes;
- provider revision separate from `MaterialStateRef`;
- canonical import with candidate mapping;
- accepted mapping followed by provider change;
- bidirectional sync divergence;
- provider callback duplicates/reordering;
- provider timeout with unknown external outcome;
- provider resync/full-rebaseline state;
- deletion/redaction propagation to applicable provider/projected copies.

## C5 — Temporal / calendar corpus

Purpose: pressure temporal fidelity independently of a specific calendar provider schema.

Includes:

- timezone-aware timed events;
- all-day events;
- local/floating-time style cases where applicable;
- recurrence series;
- individual occurrence override;
- exclusion/cancellation of one occurrence;
- future recurrence changes;
- DST spring-forward gap;
- DST fall-back fold/ambiguous local time;
- timezone definition/update pressure;
- historical reconstruction of what was scheduled under then-applicable rules;
- provider recurrence/sync identifiers mapped as external state rather than native identity.

## C6 — Search / retrieval corpus

Purpose: compare structured/lexical search baseline and bounded semantic retrieval.

Includes:

- exact/structured filters;
- lexical/full-text relevance queries;
- mixed filter + text search;
- semantically similar but lexically different content;
- near-duplicate content;
- adversarially irrelevant high-similarity content;
- access/Visibility filters;
- tenant/scope filters;
- deleted/redacted content;
- stale index entries;
- updated source content requiring reindex;
- long-tail candidate sets where ANN recall can degrade after filtering.

Required metrics include correctness/recall **after** applicable security/scope filtering.

## C7 — Recovery / evolution corpus

Purpose: prove recovery and evolution without false history.

Includes:

- backup at state B0;
- later canonical writes B1;
- later deletion/redaction D1;
- restore from B0 followed by required reconciliation of D1;
- pending provider effect at crash time;
- partial multi-owner operation;
- in-flight durable operation across runtime/schema version change;
- schema/mapping evolution from V1 to V2;
- historical references created under V1 and queried after V2;
- native identity non-reuse after deletion/redaction;
- derived/index rebuild after restore.

# Synthetic qualification tiers

The initial tiers are benchmark envelopes only.

They are intentionally spaced widely to expose scale-sensitivity.

## Tier LOW

```text
active accounts                         100
concurrent clients                       10
current canonical/relation records   ~200k
material history/provenance records    ~2M
searchable chunks                    ~100k
provider/integration objects          ~100k
```

Use cases:

- local/small-service operability;
- correctness and low-load latency;
- minimal infrastructure overhead;
- developer/recovery ergonomics.

## Tier BASE

```text
active accounts                       5,000
concurrent clients                      250
current canonical/relation records    ~10M
material history/provenance records  ~100M
searchable chunks                      ~5M
provider/integration objects           ~5M
```

Use cases:

- realistic qualification pressure without claiming a forecast;
- mixed current/history/search/provider load;
- sustained concurrency and background projection work.

## Tier HIGH

```text
active accounts                      50,000
concurrent clients                    2,000
current canonical/relation records   ~100M
material history/provenance records    ~1B
searchable chunks                     ~50M
provider/integration objects          ~50M
```

Use cases:

- expose scaling cliffs;
- evaluate whether ranking changes materially at a larger envelope;
- pressure storage/index/history growth and concurrency.

## Tier interpretation rule

A candidate is not required to hit an arbitrary business SLA defined nowhere in the repository.

The run records comparative behavior and any evident failure/saturation points.

If later accepted product evidence says only LOW or beyond HIGH matters, Phase 10 methodology remains valid; the Physical benchmark reruns/reweights the relevant evidence rather than rewriting semantic hard gates.

# Load profiles

Each applicable tier should execute at least these profiles.

## LP-01 — Read-heavy current state

```text
85% current/effective reads
10% low-consequence writes
5% consequential writes/background reconciliation
```

Purpose: product Home/Today/current-state style access with background mutation.

## LP-02 — Mixed interactive

```text
60% reads
25% writes
15% consequential/conflict/provider work
```

Purpose: active planning/editing plus provider and history pressure.

## LP-03 — Write/conflict burst

```text
40% reads
40% writes
20% intentionally contended consequential writes
```

Purpose: expected-state, locking/conflict and multi-device pressure.

## LP-04 — History/reporting

```text
historical reconstruction
cross-owner reporting
provenance lineage
current-vs-past comparisons
```

Run concurrently with a bounded interactive workload to expose interference.

## LP-05 — Projection/search churn

```text
canonical writes
index/projection updates
search traffic
deletions/redactions
access/Visibility changes
```

Purpose: measure lag, stale-result behavior and downstream propagation.

# Core scenario register

Each scenario has a common semantic assertion. Candidate-specific implementation may differ.

## SC-001 — Same-base consequential race

Setup:

- material state `S1`;
- two clients both read `S1`;
- client A requests consequential effect EA;
- client B requests materially conflicting EB.

Assertions:

- one write does not silently erase the other by arrival order;
- expected-state conflict is detectable;
- resulting material lineage is truthful;
- retry cannot turn conflict into duplicate effect.

Primary hard gates: HG-04, HG-06.

## SC-002 — Idempotency-key conflicting reuse

Setup:

- execute operation O1 with idempotency key K;
- retry exact equivalent O1/K;
- attempt materially different O2/K.

Assertions:

- equivalent retry does not duplicate intended consequence;
- materially different reuse conflicts/rejects;
- K never becomes Domain identity.

## SC-003 — Atomic multi-owner mutation

Setup:

A consequential operation requires coordinated material changes to more than one canonical owner/facet where the accepted invariant is all-or-nothing.

Assertions:

- no hidden partial canonical success if atomicity is required;
- rollback/failure preserves prior truthful state;
- provenance identifies attempted operation.

Primary hard gate: HG-05.

## SC-004 — Distributed/provider partial outcome

Setup:

- canonical step succeeds;
- provider side effect fails or remains unknown.

Assertions:

- canonical success and provider result remain separate axes;
- system exposes pending/partial/reconciliation state;
- no fictional rollback.

## SC-005 — Provider effect may have occurred before timeout

Setup:

- external request sent;
- response lost/timeout;
- provider effect status initially unknown.

Assertions:

- timeout != external failure;
- blind retry is not assumed safe;
- inquiry/idempotency/reconciliation path is representable.

## SC-006 — Duplicate/out-of-order callback

Assertions:

- replay does not duplicate canonical consequence;
- arrival order does not establish canonical truth by itself;
- stale/provider revisions remain explicit.

## SC-007 — Revoked governance during delayed execution

Setup:

- effect accepted/queued at T1;
- Authority/Consent/Visibility or represented-party basis changes before T2.

Assertions:

- applicable governance is revalidated or a valid immutable binding is proven;
- queued technical deliverability is not permanent authority.

## SC-008 — Stale LR-08 consequential basis

Setup:

- Effective Availability/Authority/Visibility/Candidate Set derived at S1;
- material sources change to S2;
- effect attempts to rely on old projection.

Assertions:

- stale projection does not silently authorize consequence;
- revalidation or bound material basis is enforced.

## SC-009 — Web/mobile offline divergence

Setup:

- device A goes offline from base S1;
- device B/provider changes same target to S2;
- device A later submits S1-derived mutation.

Assertions:

- no universal last-write-wins;
- divergence remains detectable/reconcilable;
- local cache availability does not override freshness/governance.

## SC-010 — Correction without false rewrite

Setup:

- historical state H1 later proven materially incorrect/incomplete;
- correction H2 recorded.

Assertions:

- H1 remains reconstructible as prior recorded state where policy permits;
- H2 does not pretend it was always known;
- current/effective query returns correct corrected view.

## SC-011 — Redaction then restore older backup

Setup:

- backup B0 contains sensitive payload X;
- later accepted deletion/redaction D1 removes/restricts X;
- system restores B0.

Assertions:

- restore does not silently resurrect X into permitted current visibility/state;
- D1 remains enforceable/reconcilable;
- minimum permitted tombstone/reference continuity remains truthful;
- NativeRef not reused.

Primary hard gates: HG-09, HG-12.

## SC-012 — Native identity non-reuse

After deletion/redaction of referent R/NativeRef N, create unrelated referent R2.

Assertion: N is never reassigned to R2.

## SC-013 — Deep-history current-state query

Run common current/effective queries against C1 at LOW/BASE/HIGH history depth.

Assertions:

- no lifetime replay required by default;
- current result matches full-history truth oracle;
- performance degradation is recorded.

## SC-014 — Historical reconstruction

Query owner/relation/governance state as-of selected material points and reconstruct provenance/correction path.

Assertion: result matches deterministic corpus oracle.

## SC-015 — Typed n-ary relation fidelity

Construct representative relation with multiple typed roles, governance/material context and lifecycle.

Assertions:

- role identity/cardinality preserved;
- no generic-edge semantic loss;
- update/query/history remains intelligible.

Primary hard gate: HG-03.

## SC-016 — Selective disclosure without source leakage

A permitted derived result depends on private source material.

Assertions:

- permitted result may be exposed when policy allows;
- private source need not be exposed;
- hidden source existence/count is not leaked beyond accepted surface.

## SC-017 — Search hidden-result non-interference

Setup includes visible and hidden matching records.

Measure:

- result contents;
- counts;
- ranking;
- error behavior;
- timing classes where material.

Assertion: hidden records do not become inferable beyond accepted disclosure contract.

## SC-018 — FTS mixed filter/query

Run structured + lexical queries across owner type, time, visibility and textual relevance.

Compare correctness, ranking and performance.

## SC-019 — Vector recall after security/scope filter

Run exact-reference oracle plus vector top-k under tenant/Visibility/category filters.

Record:

```text
unfiltered recall@k
filtered recall@k
precision@k
latency
candidate count before/after filters
```

Assertion: ANN quality is judged after the real filter boundary.

## SC-020 — Search/index stale source

Canonical/source material changes while projection update is delayed.

Assertions:

- stale result remains identifiable/controlled where material;
- consequential use cannot treat stale hit as current truth;
- repair/rebuild path exists.

## SC-021 — Search/index deletion propagation

Delete/redact source then exercise search/vector/graph projection before, during and after propagation.

Assertions:

- pending propagation is observable;
- post-propagation hidden/deleted payload does not remain queryable contrary to policy.

## SC-022 — Recurrence across DST spring gap

Fixture contains recurrence whose local time intersects a DST-forward transition.

Assertions:

- accepted recurrence semantics are preserved;
- historical/local timezone meaning remains reconstructible;
- provider adapter representation does not redefine canonical semantics.

## SC-023 — Recurrence across DST fall fold

Same as SC-022 for ambiguous repeated local time.

## SC-024 — Individual recurrence override

Modify one occurrence while preserving series identity and other occurrences.

Assertions:

- occurrence/series distinction preserved;
- provider recurrence ID is not automatically LifeOS NativeRef;
- history reconstructs override.

## SC-025 — Provider calendar sync-token invalidation/rebaseline

Simulate provider requiring full resynchronization after token invalidation.

Assertions:

- provider rebaseline does not erase canonical history/state;
- duplicates/mappings reconciled;
- sync token is not `MaterialStateRef`.

## SC-026 — Solver candidate from stale snapshot

Generate solver candidate from material snapshot S1; mutate relevant constraints/state to S2 before application.

Assertions:

- solver result remains candidate/proposal;
- stale candidate cannot directly write canonical state;
- governed effect revalidates applicable basis.

## SC-027 — Solver UNKNOWN vs INFEASIBLE

Exercise solver/model time limit/uncertain result and a proven infeasible case.

Assertion: result categories remain distinct and neither becomes canonical truth automatically.

## SC-028 — Crash between canonical commit and external publication/effect

Inject process failure at the boundary.

Assertions:

- recovery can determine pending/attempted state;
- no duplicate canonical effect;
- external publication/effect is resumed/reconciled safely.

## SC-029 — Durable in-flight execution across version change

A long-running governed operation begins under runtime/effect contract V1 and survives deployment V2.

Assertions:

- compatibility/version policy prevents silent reinterpretation;
- target/governance/material checks remain valid;
- technical workflow identity does not replace semantic operation identity.

## SC-030 — Schema/mapping evolution with historical references

Migrate candidate mapping V1 -> V2 with:

- live current state;
- long history;
- external refs;
- tombstones;
- governed-effect provenance;
- pending reconciliation state.

Assertions:

- all required references/meaning survive;
- no NativeRef reuse/remap;
- history queries remain semantically equivalent.

Primary hard gate: HG-11.

## SC-031 — Backup/restore operational verification

For exact version/edition/deployment:

- create backup/snapshot/export as applicable;
- destroy or isolate active state;
- restore;
- run semantic verification suite.

Assertions:

- restored bytes are not enough; canonical current/history/reference/governance assertions must pass;
- documented RPO/RTO observations are recorded, not inferred.

## SC-032 — Capacity/backpressure failure

Pressure storage, connection/worker/query capacity or provider quota until degraded behavior appears.

Assertions:

- no silent data loss;
- consequential work becomes rejected/pending/backpressured truthfully;
- no uncontrolled duplicates.

## SC-033 — Older client/effect contract version

Submit a consequential request encoded under an older contract after a newer mandatory governance/expected-state rule exists.

Assertions:

- request is upgraded/rejected/handled according to explicit compatibility policy;
- older client cannot bypass newer safety constraint.

## SC-034 — Provider/derived/search state unavailable

Remove provider/index/projection while canonical data remains available.

Assertions:

- canonical known state remains separate from unavailable external/derived state;
- absence/timeout does not become false/nonexistence;
- operation classes requiring freshness fail/degrade safely.

## SC-035 — Graph projection divergence/rebuild

For Lane G:

- build graph projection;
- apply canonical relation/history/access changes;
- interrupt projection update;
- query both G0 and G1;
- rebuild/reconcile G1.

Assertions:

- G1 never becomes alternate canonical truth;
- stale/divergent state is diagnosable;
- rebuild reproduces canonical projection assertions.

# Qualification measurements

For each applicable scenario/tier capture at least:

```text
semantic assertion PASS/FAIL
operation latency distribution
throughput where meaningful
conflict/retry count
CPU
RAM
storage/disk growth
index/projection size
write amplification where measurable
recovery time observation
recovery point/data loss observation
manual intervention required
query/plan/profile evidence where available
```

No single metric is sufficient across all scenarios.

# Sensitivity bands

The benchmark SHALL explicitly record sensitivity rather than invent one permanent target.

## SB-RPO

Test/record candidate capability under progressively stricter data-loss tolerance assumptions relevant to the selected deployment mode.

The benchmark must distinguish:

```text
capability demonstrated
vs
business RPO accepted
```

Phase 10 defines no business RPO.

## SB-RTO

Record restore/recovery behavior and topology requirements under progressively stricter recovery expectations.

A candidate requiring a higher edition/cluster/topology to satisfy a band is `PASS-CONDITIONAL` for that band.

## SB-LATENCY

Record p50/p95/p99 where supported for material interactive operation classes and query families.

Do not fabricate a pass threshold until accepted product targets exist; use comparative/saturation evidence and later accepted thresholds.

## SB-HISTORY

Run shallow, medium and deep history multipliers independent of current-record count to reveal systems whose current-state access degrades with lifetime history.

## SB-CONCURRENCY

Vary both independent concurrency and hot-target contention. High throughput on independent owners does not substitute for correct expected-state conflict handling.

## SB-HA

Where an HA topology is material to operational scoring, pin exact edition/version/topology and execute failover/recovery evidence rather than assigning points from a generic product claim.

# Deterministic fixture generation

The Physical benchmark harness SHOULD use a deterministic seeded generator.

Generator inputs SHOULD include:

```text
seed
tier
history multiplier
relationship-density profile
governance-density profile
provider-integration profile
search/vector corpus profile
calendar/timezone profile
content-size profile
```

The generator must produce a manifest with counts/hashes sufficient to confirm that candidates received semantically equivalent corpora.

# Oracle strategy

Correctness scenarios require an implementation-independent expected-result oracle derived from accepted semantics and fixture construction.

The oracle may be generated by deterministic fixture rules/test assertions; it MUST NOT be the result returned by one candidate and then treated as truth for the others.

Examples:

- expected current material state after a known event sequence;
- expected conflict for stale `MaterialStateRef` basis;
- expected recipient-visible result set;
- expected recurrence instances around DST fixture;
- expected historical lineage;
- expected provider mapping/reconciliation state;
- exact brute-force vector neighbor set for recall comparison where feasible.

# Candidate run matrix

## Primary lane P0/P1

Mandatory:

- C0 semantic correctness;
- C1 deep history;
- C2 population/concurrency;
- C3 governance/disclosure;
- C4 integration/provider representation;
- C5 temporal/calendar representation;
- C7 recovery/evolution;
- primary-relevant C6 structured/search pressure;
- SC-001..SC-016 as applicable;
- SC-022..SC-034 as applicable;
- LOW / BASE / HIGH tiers;
- sensitivity bands affecting primary ranking.

## Graph lane G0/G1

Mandatory:

- graph-relevant C0 relation corpus;
- C3 governance/disclosure;
- graph/traversal subset of C1/C2;
- SC-015;
- SC-016/017 where projections expose results;
- SC-021 deletion/access propagation;
- SC-030 mapping evolution where projection schema changes;
- SC-035 projection divergence/rebuild;
- LOW / BASE / HIGH graph-density variants where meaningful.

## Search lane S0/S1

Mandatory:

- C6;
- SC-017..SC-021;
- deletion/access propagation;
- exact-reference recall oracle;
- LOW / BASE / HIGH searchable-chunk tiers;
- filtered ANN sensitivity if S1 uses ANN.

# Stop conditions

A run may stop early for a candidate/role when:

- a non-compensable hard gate is conclusively failed;
- the candidate cannot represent the common corpus without prohibited semantic collapse;
- required product/version/edition capability cannot be verified and the result becomes `HOLD`;
- the benchmark setup is no longer semantically equivalent to the other candidates.

Record the stop reason and evidence. Do not continue only to generate flattering performance numbers after correctness failure.

# Phase 10 boundary — current corpus, historical execution state

This corpus defines the benchmark inputs consumed by the completed Physical Model and retained for later selected-stack validation where applicable.

It does not:

- predict DANTE user count;
- set final RPO/RTO/SLA/latency requirements;
- create Physical schemas by itself;
- run the benchmark by itself;
- select PostgreSQL, TypeDB, Neo4j, pgvector or another product by itself;
- authorize production backend implementation.

The later Physical workstream selected and accepted PostgreSQL 18.4 plus the bounded companion target through PM-11/12 and integrated through PR #15. Direct execution of this corpus remains `NOT RUN` where recorded; LOW/BASE/HIGH remain unexecuted and `DIRECT HG PASS = 0`. Development Profile v0 is the next separate operational scope.
