# Pre-Physical Repository & Architecture Coherence

- Status: **IN PROGRESS — Phase 0 + Phase 1 QA PASS; Phase 2 read-only next**
- Branch: `chore/pre-physical-coherence`
- Base / original Phase 0+1 PRE-SCOPE: `main @ 148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`
- Started: 2026-08-17
- Phase 0+1 content HEAD before this closure marker: `b8b568f4542b40e730ab529d04377ab4bb67cbc9`
- Production backend code: **NOT STARTED**
- Physical Model: **NOT STARTED / NOT AUTHORIZED**
- Core Domain Model / Domain Atlas: **CLOSED / unchanged**
- Logical Model: **CLOSED / unchanged**

## Purpose

This workstream is the deliberate bridge between the closed Domain + Logical Models and any later Physical Model authorization.

It exists to make the repository reconstructible and internally coherent before persistence/runtime design begins, reconcile older architecture material with the closed semantic model, identify downstream technical requirements that can materially constrain a future Physical Model, and define technology benchmarks without prematurely implementing or selecting them.

This workstream does **not** reopen Domain or Logical semantics by default. If a material semantic contradiction is discovered, stop, record the finding, and open a separate explicit reopen scope rather than silently changing accepted model truth.

## Current accepted baseline

```text
PRODUCT / NORTH STAR
CURRENT

CORE DOMAIN MODEL / DOMAIN ATLAS
CLOSED — integrated into main via PR #10

LOGICAL MODEL
CLOSED — integrated into main via PR #11
Whole-Logical: PASS WITH HARDENING / REMOTE QA PASS
WD-03: PASS
WD-05: PASS
WL-H01..WL-H12: active downstream hardenings

PRE-PHYSICAL COHERENCE
ACTIVE on this branch
PHASE 0 + PHASE 1: QA PASS
PHASE 2: READ-ONLY INVENTORY NEXT

PHYSICAL MODEL
NOT STARTED / requires separate future authorization

BACKEND PRODUCTION IMPLEMENTATION
NOT STARTED
```

`main` remains the single integrated source of accepted project truth. This branch is authoritative only for this bounded, unmerged Pre-Physical Coherence workstream.

## Mandatory operating rules

Before any later write in this workstream:

1. read `README.md`, `docs/README.md` and `docs/PROJECT-STATUS.md`;
2. read `docs/development/agent-operating-manual.md`;
3. read `docs/development/operating-rules.md`;
4. read `docs/development/documentation-and-handoff.md`;
5. read `docs/development/branching-and-environments.md`;
6. read this complete handoff;
7. verify the branch ref and compare/reconstruct its relation to current `main`;
8. perform the next phase read-only analysis before proposing writes where the roadmap requires it;
9. present an exact Git write gate with branch, PRE-SCOPE, CREATE/UPDATE/DELETE, purpose and explicit out-of-scope;
10. re-fetch the branch HEAD before the first approved write;
11. after writes, run remote path/delta/readback QA before claiming PASS/CLOSED.

Historical checkpoints and canonical continuation chains are evidence. Do not rewrite them merely to make history look current.

## Two independent review inputs

The workstream was formed after two independent pre-Physical backend/architecture reviews were compared on 2026-08-17.

They converged on the following major conclusions:

- no demonstrated new universal Domain primitive requires reopening the Domain Atlas;
- the closed Logical Model remains the strongest current backend semantic foundation;
- the largest immediate risk is stale or ambiguously superseded repository documentation above/around the Logical Model;
- PostgreSQL remains the current preferred Physical baseline but is not yet a final Physical selection;
- TypeDB remains a mandatory Physical benchmark challenger;
- generic EAV / generic edge / universal meta-model approaches remain rejected for the canonical kernel;
- modular-monolith, Python, FastAPI/Pydantic and provider-neutral boundaries remain sensible current directions without authorizing implementation;
- AuthN/AuthZ, security/privacy, consistency/side-effects, durable workflow/async behavior, AI context/runtime boundaries, integrations, search, observability and non-functional requirements need explicit downstream contracts before or around the Physical stage;
- durable workflow technology deserves an explicit benchmark rather than assuming a lightweight worker or adopting Temporal automatically;
- repository current truth must be repaired before Physical Model work starts.

## Semantic non-reopen result

Do **not** introduce a new universal Domain owner merely because a term is useful at product/runtime level. Current examples that remain compositions, profiles, projections, policies or technical/runtime concepts unless future evidence proves otherwise include:

- Memory;
- Agent;
- Automation;
- Job;
- Workflow;
- Notification;
- Reminder;
- Priority;
- Preference;
- Context;
- Task;
- Workspace;
- Risk;
- Focus Time;
- Out of Office;
- Working Location.

Product/UI terminology may remain useful without becoming a new kernel owner.

## Downstream logical hardenings that must survive

Any later architecture/Physical/runtime work must preserve:

- `WL-H01` — Agreement terms bind to justified material state;
- `WL-H02` — Governed Operation / Effect Contract;
- `WL-H03` — Projection / Disclosure Surface Contract;
- `WL-H04` — absence/unknown is not automatically false or a negative state;
- `WL-H05` — expected-state / optimistic-concurrency semantics for consequential writes;
- `WL-H06` — idempotency is effect/retry control, not semantic identity;
- `WL-H07` — truthful multi-owner atomicity or explicit staged/partial reconciliation;
- `WL-H08` — canonical LifeOS state remains distinct from provider sync state;
- `WL-H09` — consequential use of derived state requires freshness/material-basis semantics;
- `WL-H10` — retention/redaction/tombstone handling must not falsify history or reuse identity;
- `WL-H11` — consequential AuthZ decisions require reconstructible provenance;
- `WL-H12` — selective disclosure includes non-interference and inference-leakage pressure.

## Unified work program

The work is intentionally separated into **cleanup**, **architecture requirements**, **technology benchmark preparation**, and only later a separately authorized **Physical Model**.

### Phase 0 — Freeze and current-state inventory — PASS

Completed for the mandatory bootstrap/current-state surface used to open this workstream:

- verified `main @ 148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`;
- confirmed Domain/Logical closure and Physical/backend non-started state;
- inventoried mandatory bootstrap/global documents;
- identified stale Domain/Backend sequencing and pre-Logical technology wording;
- did not alter Domain or Logical semantic documents.

A broader clean-room/repository-wide inventory remains part of final Phase 12 closure rather than being falsely claimed complete here.

### Phase 1 — Global current-truth documentation alignment — QA PASS

Approved/final physical path set:

```text
CREATE
docs/workstreams/pre-physical-coherence.md

UPDATE
README.md
docs/README.md
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/README.md
docs/development/operating-rules.md
docs/development/branching-and-environments.md

DELETE
none
```

Resulting current truth across the mandatory entry path:

```text
Domain CLOSED
Logical CLOSED
Pre-Physical Coherence ACTIVE
Physical NOT STARTED
Backend NOT STARTED
repository PUBLIC
main remains canonical
```

The old operational instruction that Domain Model v0 should start in parallel with or inside Backend Foundation has been removed/qualified from the mandatory bootstrap path. Backend Foundation is now explicitly deferred pending this workstream and later accepted prerequisites.

#### Phase 0+1 remote QA evidence

The normal GitHub compare endpoint for `base=148a4cb5...` vs `head=chore/pre-physical-coherence` returned `404`; this failure was **not** counted as PASS.

Fallback remote QA used repository evidence instead:

- branch creation was verified from the exact approved PRE-SCOPE;
- GitHub commit-list readback showed a linear chain from `148a4cb5...` through the eight Phase-1 content commits to `b8b568f...`;
- each content commit was fetched individually and changed exactly one approved physical path;
- first content commit added `docs/workstreams/pre-physical-coherence.md`;
- seven subsequent content commits modified the seven approved existing files;
- no delete commit or unapproved path was observed;
- `main` remained exactly `148a4cb5d5741b4a5b9667cf8d30231ebc0545f0` after the writes;
- branch ref after the eight content writes was `b8b568f4542b40e730ab529d04377ab4bb67cbc9`;
- remote payload readback confirmed README, PROJECT-STATUS, ROADMAP and this handoff expose the aligned state and future sequence.

Scope result before this same-path closure update:

```text
added      1
modified   7
deleted    0
unexpected 0
content commits ahead of PRE-SCOPE 8
```

This closure update changes only the already-approved newly created handoff path and does not alter the final physical-path classification above. Its resulting commit/HEAD must be verified after write before relying on this closure record.

### Phase 2 — Architecture supersession cleanup — NEXT, READ-ONLY FIRST

Before any Phase-2 write, perform a fresh read-only inventory of at least:

- `docs/architecture/personal-data-ai-integration.md`;
- `docs/architecture/technical-decisions.md`;
- `docs/architecture/system-overview.md`;
- relevant architecture/index material;
- ADR-003, ADR-005, ADR-006, ADR-007 and any later relevant ADR/current Logical decisions.

Classify findings as:

```text
CURRENT / KEEP
QUALIFY
PARTIALLY SUPERSEDED
SUPERSEDED
HISTORICAL / KEEP
DECISION REQUIRED
NO ISSUE
```

Only then propose the exact Phase-2 write gate.

Phase-2 goals:

- preserve historical reasoning;
- make later Domain/Logical authority explicit;
- prevent `entity_relations`, generic Relation/property fallback or generic-first wording from being interpreted as current canonical ontology;
- distinguish technical shared registries/edges from semantic owners/relations;
- explicitly mark older accepted architecture as partially superseded/qualified where appropriate;
- do not rewrite historical checkpoints retroactively.

### Phase 3 — Backend Foundation handoff cleanup

Candidate target under a separate exact write gate: `docs/workstreams/backend-foundation.md`.

Backend Foundation must eventually consume:

```text
CLOSED Domain Atlas
+
CLOSED Logical Model
+
future accepted Physical Model
+
current architecture/runtime contracts
```

It must no longer instruct contributors to create Domain Model v0 as part of backend bootstrap or use pre-Domain persistence assumptions as current truth.

### Phase 4 — Current Pre-Physical Architecture Baseline

Create one current bridge source stating:

- what is already decided;
- what is semantically prohibited;
- what remains open;
- which `WL-H01..WL-H12` constraints are mandatory downstream;
- what belongs to runtime/backend rather than Domain;
- which older architecture documents are partially superseded;
- what must be benchmarked during Physical design.

### Phase 5 — Requirements that can materially constrain a Physical Model

Define requirements, not implementations, for:

1. **AuthN/AuthZ contract** — `Person != Account != Principal != Actor`; represented party, service/external-agent identity, session/device context; Authority/Consent/Visibility remain Domain truth; policy/version and AuthZ provenance requirements.
2. **Security/privacy technical baseline** — data classification, sensitive handling, encryption/key/secret boundaries, isolation, retention/redaction/deletion propagation, audit/log minimization, backup/recovery implications, AI/provider minimization.
3. **Transaction/consistency/side-effect contract** — expected state, transaction boundaries, idempotency, outbox/publication pressure, external acknowledgement, partial state, reconciliation/compensation, derived-state freshness.
4. **Non-functional/recovery envelope** — scale/concurrency assumptions, latency classes where material, long-term history, multi-device conflict assumptions, online/offline posture, RPO/RTO/restore expectations.

### Phase 6 — AI, runtime and integration boundaries

Preserve explicit technical separation among:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate/unresolved state
transient LLM working context
```

Define runtime families without promoting them to Domain owners:

- agent/workflow execution;
- automation definition vs automation execution;
- reminder/product behavior vs notification delivery;
- provider/agent capability contracts;
- integration modes:
  1. canonical import;
  2. synced/mirrored provider state;
  3. live federated read;
  4. retrieval/index projection;
  5. action/tool integration.

Internal governed LifeOS contracts remain protocol-neutral; MCP, A2A or future protocols may be adapters rather than LifeOS ontology.

### Phase 7 — Durable workflow / async benchmark

Benchmark on LifeOS scenarios rather than technology fashion:

- PostgreSQL + worker + transactional outbox;
- Temporal;
- Restate;
- DBOS.

Pressure cases include provider sync/retry, human approval, long-running AI work, reconciliation, cancellation/timeouts, partial external effects and crash recovery.

No durable-workflow product is selected by this roadmap.

### Phase 8 — Governed API / command contract

Before concrete routes, define the general consequential-write contract around:

- principal/actor;
- semantic target;
- operation family/effect;
- expected state;
- inputs and purpose/context;
- authorization basis;
- idempotency/correlation;
- confirmation where required;
- result/provenance/conflict semantics.

Invariant:

```text
HTTP route / UI button / AuthZ action string
!= canonical Governed Operation
```

### Phase 9 — Search, observability, calendar and solver pressure

Define requirements and benchmark inputs, not premature infrastructure:

- search/retrieval projection separate from canonical truth;
- PostgreSQL structured/full-text baseline and pgvector as bounded semantic-retrieval candidate;
- dedicated search/vector infrastructure only on demonstrated benefit;
- OpenTelemetry-first or equivalent standard instrumentation direction with privacy-minimized AI telemetry;
- iCalendar, JSCalendar, Google Calendar and Microsoft Graph semantics as interoperability pressure tests, not ontology;
- deterministic solvers/services for deterministic constraints, calculations, authorization and state transitions;
- AI for ambiguity, interpretation, explanation and cross-domain reasoning where useful;
- planner outputs support truthful feasible/infeasible/uncertain/at-risk/conflicting/partially-feasible results with explanations.

### Phase 10 — Physical benchmark specification/register

Current posture entering the future benchmark:

```text
PostgreSQL hybrid
CURRENT PREFERRED BASELINE — not final selection

TypeDB
MANDATORY CHALLENGER

Neo4j / property graph
SERIOUS SECONDARY / read-projection challenger

event store
BOUNDED history/integration mechanism, not primary ontology

document store
BOUNDED provider/specialist/flexible use, not canonical kernel

generic EAV / generic edge / universal meta-model
HARD REJECT for canonical kernel

pgvector
BOUNDED semantic-retrieval candidate
```

Benchmark destructive LifeOS scenarios including concurrent consequential edits, multi-owner changes, selective disclosure, provider divergence, redaction/history reconstruction, recurrence across DST, stale availability, AuthZ provenance, search inference leakage, AI proposal→approval→effect, revoked consent during execution, long-running crash/restart, restore and schema evolution over historical state.

### Phase 11 — Repository engineering safety alignment

Before production backend implementation, establish appropriate repository safety such as:

- main branch/ruleset protection;
- no unauthorized direct/force pushes;
- CI skeleton;
- required checks when concrete checks exist.

Concrete Python/toolchain bootstrap choices belong to backend bootstrap unless they materially affect architecture.

### Phase 12 — Full clean-room coherence QA and closure

A new human/AI agent with no chat context must be able to reconstruct from Git:

```text
what LifeOS is
→ what is current/canonical
→ Domain CLOSED
→ Logical CLOSED
→ what historical architecture was superseded/qualified
→ what requirements constrain downstream design
→ what technology candidates must compete
→ what remains unauthorized
```

Target closure:

```text
REPOSITORY / ARCHITECTURE COHERENCE
PASS

DOMAIN MODEL
UNCHANGED / CLOSED

LOGICAL MODEL
UNCHANGED / CLOSED

PHYSICAL MODEL
READY FOR SEPARATE AUTHORIZATION
NOT STARTED
```

Only after this closure may the user separately authorize a Physical Model workstream.

## Specialized-infrastructure decision rule

Do not use the overly narrow rule "specialized infrastructure only after measured production need" as an absolute gate.

Current evaluation principle:

> Specialized infrastructure requires demonstrated benefit. Evidence may come from measured workload **or** a sufficiently strong structural improvement in correctness, durability, security, evolvability, operational reliability, or cost/risk of later migration.

This avoids both premature complexity and waiting until a preventable architectural problem becomes expensive.

## Explicit out of scope until separately gated

- new Domain primitives or silent Domain semantic changes;
- silent Logical Model semantic changes;
- Physical Model implementation;
- SQL, schema, indexes, migrations;
- concrete API endpoints;
- production FastAPI/backend implementation;
- concrete Auth provider integration;
- provider adapters;
- frontend/prototype changes inside this backend/coherence workstream;
- historical branch deletion/cleanup;
- direct modification of `main`.

Specific architecture/Auth/AI/runtime/integration documents are only writable when their phase receives an exact approved gate.

## Exact continuation point

**Phase 0 + Phase 1 are closed at the content/path level and have remote fallback QA PASS.**

Next action after verifying this closure commit:

```text
PHASE 2
READ-ONLY ARCHITECTURE SUPERSESSION INVENTORY

NO WRITES YET
```

A new chat should begin by reading this file, verifying the current branch HEAD and current `main`, then reading the Phase-2 candidate architecture/ADR sources listed above. It should not ask the user to reconstruct the two earlier reviews from conversation history.

## Tool incident record

During branch setup, the first GitHub branch-creation attempt returned upstream `502`. A direct ref read immediately afterward returned `404`, proving that attempt had not created the branch. After re-verifying that `main` still matched the approved PRE-SCOPE, a single retry created `chore/pre-physical-coherence` successfully from the exact approved SHA.

The normal compare endpoint later returned `404`. This was treated as a connector/API limitation, not a successful compare. Phase-0/1 QA therefore used commit-chain, per-commit changed-file, ref and payload-readback evidence instead.

No `main` write occurred.