# Pre-Physical Repository & Architecture Coherence

- Status: **IN PROGRESS — Phase 11 QA PASS; Phase 12 clean-room coherence QA next**
- Branch: `chore/pre-physical-coherence`
- Original workstream base: `main @ 148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`
- Started: 2026-08-17
- Production backend code: **NOT STARTED**
- Physical Model: **NOT STARTED / NOT AUTHORIZED**
- Core Domain Model / Domain Atlas: **CLOSED / unchanged**
- Logical Model: **CLOSED / unchanged**

## Purpose

Bridge the closed Domain + Logical Models and any later separately authorized Physical Model.

This workstream makes repository/current architecture truth coherent, establishes pre-Physical technical requirements and benchmark inputs, hardens repository integration safety, and closes only after a clean-room Phase 12 QA.

A genuine material semantic contradiction triggers a separate explicit Domain/Logical reopen. Cleanup or implementation convenience must not silently alter closed semantics.

## Current accepted stage

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL / DOMAIN ATLAS
CLOSED

LOGICAL MODEL
CLOSED
Whole-Logical PASS WITH HARDENING / REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active

PRE-PHYSICAL COHERENCE
ACTIVE
Phase 0 PASS
Phase 1 QA PASS
Phase 2 QA PASS
Phase 3 QA PASS
Phase 4 QA PASS
Phase 5 QA PASS
Phase 6 QA PASS
Phase 7 QA PASS WITH CONDITIONAL RANKING
Phase 8 QA PASS
Phase 9 QA PASS
Phase 10 QA PASS
Phase 11 QA PASS

NEXT
Phase 12 — CLEAN-ROOM REPOSITORY / ARCHITECTURE COHERENCE QA
READ-ONLY FIRST

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND FOUNDATION / PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED
```

## Mandatory bootstrap

Before Phase 12 or later work:

1. read root `README.md`;
2. read `docs/README.md`;
3. read `docs/PROJECT-STATUS.md`;
4. read `docs/development/agent-operating-manual.md`;
5. read `docs/development/operating-rules.md`;
6. read `docs/development/documentation-and-handoff.md`;
7. read `docs/development/branching-and-environments.md`;
8. read `docs/development/repository-engineering-safety.md`;
9. read this complete handoff;
10. read `docs/architecture/README.md` and all linked current architecture sources;
11. read `docs/architecture/pre-physical-architecture-baseline.md`;
12. read `docs/architecture/requirements/README.md` + all four Phase 5 packages;
13. read Phase 6 AI/context/runtime + Integration Hub contracts;
14. read Phase 7 durable-execution benchmark;
15. read Phase 8 governed-operation/effect contract;
16. read Phase 9 search/observability/calendar/solver contract;
17. read all three Phase 10 Physical benchmark-method documents;
18. read complete canonical split/continuation chains where a logical document is physically split;
19. read relevant ADR/evidence/methodology;
20. verify current branch/ref and relation to `main`;
21. before any write phase, issue a fresh exact PRE-SCOPE/write gate.

## Documentation lifecycle rule

```text
CURRENT SPECIFICATION
= current truth only

ADR
= rationale + explicit status/supersession

HISTORICAL / VALIDATION EVIDENCE
= truthful chronology

GIT
= recoverable history
```

Before replacing/deleting stale current documentation:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```

Phase 11 closure propagation cleaned repeated historical narrative from current entry-point/status documents. Knowledge coverage passed because current technical requirements remain in their canonical architecture/development sources, exact continuation state remains in this handoff, and historical prose/changes remain recoverable in Git.

### Size/tool-limit split rule — mandatory

A physical split does not create separate logical authority.

```text
ONE COMPLETE LOGICAL PAYLOAD
→ LOSSLESS PHYSICAL PARTITION
→ ONE COMPLETE LOGICAL PAYLOAD
```

A size/tool-limit split is **not** summarization, condensation, omission, paraphrase-as-compression or hidden semantic cleanup.

If content itself needs revision, that is a separate content/current-truth operation. Chronological/evidence continuation is distinct and may append genuine later evidence after the previous payload.

## Current architecture navigation

Current sources include:

- `docs/architecture/pre-physical-architecture-baseline.md`;
- `docs/architecture/requirements/README.md` + all four Phase 5 packages;
- `docs/architecture/ai-context-runtime-boundaries.md`;
- `docs/architecture/integration-hub-boundaries.md`;
- `docs/architecture/durable-execution-benchmark.md`;
- `docs/architecture/governed-operation-effect-contract.md`;
- `docs/architecture/search-observability-calendar-solver-boundaries.md`;
- `docs/architecture/physical-benchmark-specification.md`;
- `docs/architecture/physical-benchmark-scenario-corpus.md`;
- `docs/architecture/physical-benchmark-register.md`;
- `docs/architecture/README.md`;
- `docs/architecture/system-overview.md`;
- `docs/architecture/technical-decisions.md`;
- `docs/development/repository-engineering-safety.md`;
- accepted complete Domain Atlas + Language Map logical documents;
- closed Whole Logical Model + complete decision/assumption-register logical document + remote closure evidence;
- current ADR statuses;
- this handoff for still-open Pre-Physical obligations.

Historical `docs/architecture/domain-model-logical-readiness*` files remain transition/validation evidence, not current architecture specifications.

## Non-negotiable downstream hardenings

Later architecture/Physical/runtime work must preserve `WL-H01..WL-H12`, including:

- justified material Agreement terms;
- governed operation/effect semantics;
- bounded projection/disclosure surfaces;
- absence/unknown not collapsing to false;
- expected-state consequential writes;
- idempotency distinct from semantic identity;
- truthful atomic/staged multi-owner consistency;
- canonical state != provider sync state;
- consequential derived-state freshness/material basis;
- retention/redaction/tombstone integrity and non-reused identity;
- reconstructible consequential AuthZ provenance;
- selective disclosure including non-interference/inference leakage.

Phase 5 requirements, Phase 6 boundary contracts, Phase 7–9 architecture contracts, the Phase 10 benchmark method and Phase 11 repository safety add current downstream constraints without replacing those hardenings.

## Semantic non-reopen boundary

Do not create universal Domain owners because a product/runtime term is useful.

Unless separately revalidated, terms such as Memory, Agent, Automation, Job, Workflow, Notification, Reminder, Priority, Preference, Context, Task, Workspace, Risk, Focus Time, Out of Office and Working Location remain product/runtime/composition/profile/projection/policy concepts rather than new universal Domain roots.

Current high-risk invariants include:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
provider state != canonical LifeOS state
derived projection != canonical truth
AI / solver inference != accepted canonical effect
runtime workflow completion != Actual automatically
technical cancellation != Domain cancellation automatically
search miss != canonical nonexistence
telemetry != Domain Provenance / audit automatically
preferred / registered benchmark candidate != selected technology
```

## Phase ledger — exact continuation evidence

### Phase 0–1

```text
BASE / PRE-SCOPE
148a4cb5d5741b4a5b9667cf8d30231ebc0545f0

FINAL HEAD
d9610a7da4fe8fc759e9809843d989f1befcda5c

RESULT
QA PASS
```

### Phase 2 — architecture supersession/current-truth cleanup

```text
PRE-SCOPE
d9610a7da4fe8fc759e9809843d989f1befcda5c

CONTENT HEAD
dfc1f4e124f362d342c336485e166c8ac57afba4

RESULT
QA PASS
```

Knowledge coverage for retired `docs/architecture/personal-data-ai-integration.md`:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```

### Phase 3 — Backend Foundation handoff cleanup

```text
PRE-SCOPE
d2f190de06bf0e4e1e491c0c2dc601eb48668da9

CONTENT HEAD
50731dbee3d2cc661972700ef0bce521b67098c6

RESULT
QA PASS
```

Backend Foundation remains current but deferred/non-executable.

### Phase 4 — Current Pre-Physical Architecture Baseline

```text
PRE-SCOPE
46b963394e29179fadf20cb3b11c35dbf3b6edc2

CONTENT HEAD
d67cd83f462611b2cc6d341937432e705f7a8682

RESULT
QA PASS
```

```text
DECIDED CURRENT DIRECTION != IMPLEMENTATION AUTHORIZATION
PREFERRED BENCHMARK BASELINE != TECHNOLOGY SELECTION
```

The old accidental `__no-op__` ref created during this period is now absent and is no longer a repository-hygiene residual.

### Phase 5 — requirements that can constrain Physical

```text
PRE-SCOPE
e26f95af6d46292bf0f42aa43fa67b1f9f4fc05f

CONTENT HEAD
c29cfe4bde47d5df4f46507a5f1717acd1903112

PROPAGATION HEAD BEFORE HANDOFF
26882e376f1a6ad826d5aabfb4364f2a2ba30dd5

RESULT
QA PASS
```

Owners: AuthN/AuthZ; Security/Privacy/Retention/Security-aware Recovery; Consistency/Side Effects; Non-functional/Multi-device/Operational Recovery.

No arbitrary RPO/RTO/SLA/latency/scale/offline targets or implementation mechanisms were selected.

### Phase 6 — AI/context/runtime/integration boundaries

```text
PRE-SCOPE
40728080ae7a69703d40d14dd256a556516ccc58

CONTENT HEAD
67d6a0d63ecaf39379912606dcf5113550718594

PROPAGATION HEAD BEFORE HANDOFF
5f9c2285f0de4a0f7c497ad36c12fae9b7548f1f

RESULT
QA PASS
```

Current context categories:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

Integration Hub preserves five modes: canonical import, sync/mirror, live federated read, retrieval/index projection and action/tool integration.

No AI provider/model, agent framework, memory store, MCP/A2A implementation, workflow engine or provider adapter was selected.

### Coordinated Phase 7–9 tranche

```text
PRE-SCOPE
2cf77ea7e3d548147bbe2b0d87304b4d5393ff5f

PHASE 7 CHECKPOINT
022131c2568c0375e74563e46a22c9347b277fc5
PASS WITH CONDITIONAL RANKING

PHASE 8 CHECKPOINT
1d92f9e77ecc808095086fc5497eaac88e2039fa
PASS

PHASE 9 CHECKPOINT
95df2a17b1187a590b5cba646ba0e107c038e5d3
PASS

CONTENT HEAD
4cbf50ec23ede3b02a49c75bc52fa57c3b192a6d

PROPAGATION HEAD BEFORE HANDOFF
d930ef5818df566a3bf9c5b2b36e9ba38e4e7b8a

RESULT
QA PASS
```

Current durable-execution posture:

```text
BOUNDED ASYNC
DB + worker/outbox style = valid baseline mechanism class

DEDICATED DURABLE EXECUTION
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional PostgreSQL-dependent challenger — NOT selected
```

Phase 8 keeps governed operation/effect meaning independent of HTTP/UI/tool/AuthZ/workflow implementation. Phase 9 keeps search/vector/telemetry/calendar/solver state from becoming canonical truth by convenience.

### Phase 10 — Physical benchmark specification/register

```text
PRE-SCOPE
01df10a4267880a213ede8582b0193ff616f9a70

CONTENT HEAD
057df9bdc19d89ea74fcee0e5d999ebc34cf93dc

PROPAGATION HEAD BEFORE HANDOFF
0a9d80fa9d2ecaf373f0d5ad22b7953b73412a8c

FINAL VERIFIED PHASE-10 HEAD
7a87cba891c24e58e4448faf20c9feb30c1559bf

RESULT
QA PASS
```

Phase 10 defines **how** the later Physical benchmark must run, not which technology wins.

Current role posture:

```text
PRIMARY
PostgreSQL hybrid — preferred mandatory baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH
no-specialized-store baseline vs Neo4j

SEARCH / VECTOR
structured + lexical/full-text baseline vs bounded pgvector

EVENT / DOCUMENT
bounded native mechanisms first; specialized products only on demonstrated gap/benefit
```

Hard correctness gates precede weighted scoring; LOW/BASE/HIGH are synthetic qualification envelopes, not forecasts; `PREFERRED != SELECTED`.

### Phase 11 — repository engineering safety — QA PASS

Approved Phase 11 gate:

```text
PRE-SCOPE
7a87cba891c24e58e4448faf20c9feb30c1559bf

CREATE
docs/development/repository-engineering-safety.md
docs/development/github-main-ruleset.json

UPDATE
.github/pull_request_template.md
docs/development/branching-and-environments.md
docs/development/operating-rules.md
docs/development/agent-operating-manual.md
docs/workstreams/backend-foundation.md
README.md
docs/README.md
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/pre-physical-coherence.md

DELETE
none
```

Step-A content/policy HEAD before GitHub settings application:

`62d9118def30c8545b9db2de49d654b4b74e55ab`

Step-A remote QA:

```text
ahead_by       7
behind_by      0
total_commits  7
added           2
modified        5
deleted         0
unexpected      0
```

GitHub-side verification after admin application:

```text
ruleset lifeos-main-safety present                 PASS
ruleset enforcement active                        PASS
ruleset target ~DEFAULT_BRANCH                    PASS
ruleset bypass none                               PASS
main deletion blocked                             PASS
main force-push/non-fast-forward blocked          PASS
pull request required                             PASS
required approvals = 0                            PASS
review-thread resolution required                 PASS
allowed merge method = merge                      PASS
required status checks = 0                        PASS / expected today
GitHub Actions workflows = 0                      PASS / observed baseline
auto-delete merged head branches = true           PASS
__do_not_create__                                 404 / PASS
__noop_should_fail__                              404 / PASS
__tmp_should_not_create__                         404 / PASS
main SHA unchanged                                PASS
```

Dependabot/secret/code-scanning API endpoints remain `403 Resource not accessible by integration`. The repository owner applied the requested security settings; the connector limitation is recorded explicitly and not misreported as independent API evidence.

Closure propagation HEAD before this handoff marker:

`c1ea90f417d3b680b1815c46b2b05b85295afb7c`

Remote compare at propagation point from Phase 11 PRE-SCOPE:

```text
ahead_by       12
behind_by      0
total_commits  12
unique_paths   11
added           2
modified        9
deleted         0
unexpected      0
```

At that point the only approved physical path not yet included was this save-game itself.

Phase 11 introduced no fake CI workflow/check, no Domain/Logical change, no Physical schema/benchmark execution and no backend implementation.

## Current repository engineering safety

Current policy source:

`docs/development/repository-engineering-safety.md`

Canonical ruleset source:

`docs/development/github-main-ruleset.json`

Current main protection:

```text
lifeos-main-safety
active
~DEFAULT_BRANCH
no bypass
main deletion blocked
force-push/non-fast-forward blocked
pull request required
required approvals = 0 while owner-driven
review-thread resolution required
merge commits only
required status checks = 0 until real stable checks exist
auto-delete merged head branches enabled
```

Future implementation must create real tests/lint/types/security/Physical checks first, prove stable unique check contexts, then separately promote material checks into the main ruleset.

## Phase 12 — exact next task

Phase 12 is **read-only first**. No Phase 12 write gate exists yet.

It is a clean-room final coherence audit. The reviewing agent should behave as if it does not have conversation history and must reconstruct current truth only from the repository.

At minimum verify:

1. root/doc/status/roadmap/workstream navigation agrees;
2. current vs ADR vs historical/evidence authority is unambiguous;
3. all complete canonical split chains needed for conclusions are read;
4. Product/North Star remains current;
5. Domain Atlas remains closed and internally reachable from navigation;
6. Logical Model remains closed and `WL-H01..WL-H12` are consistently propagated;
7. Phase 5 requirements are complete/current and their open parameters remain explicit;
8. Phase 6 AI/context/runtime/integration boundaries remain coherent;
9. Phase 7 durable-execution candidate posture remains candidate-only;
10. Phase 8 governed-operation/effect contract remains transport/runtime neutral;
11. Phase 9 search/observability/calendar/solver pressure remains bounded and non-canonical where required;
12. Phase 10 benchmark method is complete, executable in principle and still distinct from technology selection;
13. Phase 11 repository safety is applied and current;
14. Backend Foundation remains deferred/non-executable;
15. Physical Model remains not started/not authorized;
16. no stale current source contradicts the accepted current state;
17. no unresolved repository anomaly materially blocks closure;
18. a new agent can identify the exact next safe action without chat memory.

Phase 12 target:

```text
REPOSITORY / ARCHITECTURE COHERENCE PASS
DOMAIN UNCHANGED / CLOSED
LOGICAL UNCHANGED / CLOSED
PHYSICAL MODEL READY FOR SEPARATE AUTHORIZATION / NOT STARTED
```

Only after Phase 12 closure may the user separately decide whether to authorize a Physical Model workstream.

## Specialized infrastructure rule

Specialized infrastructure requires demonstrated benefit from measured workload **or** sufficiently strong structural improvement in correctness, durability, security, evolvability, operational reliability or migration-risk reduction.

Current application:

- dedicated durable execution is structurally justified for material long-running operation classes, but no engine is selected;
- dedicated search/vector infrastructure is not justified by default;
- OR-Tools CP-SAT is a preferred specialized solver benchmark candidate, not an implementation selection;
- Neo4j must beat a no-specialized-store graph/traversal baseline on net benefit before adoption;
- specialized event/document products need a concrete gap/benefit admission trigger.

## Explicitly out of scope until separately gated

- Domain semantic changes;
- Logical semantic changes;
- Domain/Logical split rewriting;
- Physical Model or concrete schema;
- SQL/TypeQL/Cypher schema/query implementation;
- tables/keys/indexes/constraints/migrations;
- Physical benchmark execution/harness;
- concrete API/backend implementation;
- concrete Auth provider/runtime selection;
- Restate/Temporal/DBOS adoption;
- bounded worker/outbox implementation;
- AI provider/model/agent implementation;
- MCP/A2A adoption/implementation;
- provider adapters;
- dedicated search/vector deployment;
- observability vendor deployment;
- calendar provider implementation;
- solver implementation;
- frontend/prototype changes inside this workstream;
- direct modification of `main`.

## Exact continuation

```text
PHASE 7
QA PASS WITH CONDITIONAL RANKING

PHASE 8
QA PASS

PHASE 9
QA PASS

COORDINATED PHASE 7–9 TRANCHE
QA PASS

PHASE 10
QA PASS

PHASE 11
QA PASS

NEXT
PHASE 12 — CLEAN-ROOM REPOSITORY / ARCHITECTURE COHERENCE QA
READ-ONLY FIRST

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND FOUNDATION
NOT STARTED / DEFERRED

NO PHASE 12 WRITES YET
```
