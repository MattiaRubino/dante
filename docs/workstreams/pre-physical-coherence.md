# Pre-Physical Repository & Architecture Coherence

- Status: **IN PROGRESS — Phase 2 content written; final remote path + knowledge-coverage QA pending**
- Branch: `chore/pre-physical-coherence`
- Original workstream base: `main @ 148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`
- Phase 2 PRE-SCOPE: `d9610a7da4fe8fc759e9809843d989f1befcda5c`
- Started: 2026-08-17
- Production backend code: **NOT STARTED**
- Physical Model: **NOT STARTED / NOT AUTHORIZED**
- Core Domain Model / Domain Atlas: **CLOSED / unchanged**
- Logical Model: **CLOSED / unchanged**

## Purpose

This workstream bridges the closed Domain + Logical Models and any later Physical Model authorization.

It exists to make repository/current architecture truth coherent, define pre-Physical technical requirements and benchmark inputs, and close with a clean-room QA before any Physical Model begins.

A genuine material semantic contradiction triggers a separate explicit Domain/Logical reopen. Documentation cleanup must not silently alter closed semantics.

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
Phase 2 CONTENT WRITTEN / FINAL QA PENDING

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND PRODUCTION IMPLEMENTATION
NOT STARTED
```

## Mandatory bootstrap

Before later work:

1. read root `README.md`;
2. read `docs/README.md`;
3. read `docs/PROJECT-STATUS.md`;
4. read `docs/development/agent-operating-manual.md`;
5. read `docs/development/operating-rules.md`;
6. read `docs/development/documentation-and-handoff.md`;
7. read `docs/development/branching-and-environments.md`;
8. read this complete handoff;
9. read `docs/architecture/README.md` and linked current model/architecture sources;
10. read relevant ADR/evidence/methodology;
11. verify current branch/ref and relation to `main`;
12. before writes, issue a new exact PRE-SCOPE/write gate unless an approved gate is still in flight.

## Documentation lifecycle rule

Current specifications contain **current truth only**; they are not chronological design logs.

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

Before replacing/deleting stale current docs:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```

The objective is clean current documentation **without losing useful knowledge**.

## Current architecture navigation

Current sources:

- `docs/architecture/README.md`;
- `docs/architecture/system-overview.md`;
- `docs/architecture/technical-decisions.md`;
- accepted Domain Atlas;
- closed Whole Logical Model;
- current ADR statuses;
- this workstream for open pre-Physical obligations.

Historical `docs/architecture/domain-model-logical-readiness*` files remain transition/validation evidence and are not current architecture specifications.

## Non-negotiable Whole-Logical hardenings

Later architecture/Physical/runtime work must preserve:

- `WL-H01` — Agreement terms bind justified material owner/state;
- `WL-H02` — governed operation/effect contract;
- `WL-H03` — bounded projection/disclosure surface;
- `WL-H04` — absence/unknown is not universally false;
- `WL-H05` — expected-state semantics for consequential writes;
- `WL-H06` — idempotency is not semantic identity;
- `WL-H07` — truthful atomic/staged multi-owner consistency;
- `WL-H08` — canonical state != provider sync state;
- `WL-H09` — consequential derived-state use requires freshness/material basis;
- `WL-H10` — retention/redaction/tombstone integrity and non-reused identity;
- `WL-H11` — reconstructible consequential AuthZ provenance;
- `WL-H12` — selective disclosure includes non-interference/inference leakage.

## Semantic non-reopen boundary

Do not create universal Domain owners merely because a product/runtime term is useful.

Unless separately revalidated, terms such as Memory, Agent, Automation, Job, Workflow, Notification, Reminder, Priority, Preference, Context, Task, Workspace, Risk, Focus Time, Out of Office and Working Location remain product/runtime/composition/profile/projection/policy concepts rather than new universal Domain roots.

## Phase 0 — freeze/current-state inventory — PASS

Verified the integrated main baseline, Domain/Logical closure, Physical/backend non-started state and stale global/architecture sequencing before writes.

A broader clean-room repository-wide audit remains part of Phase 12 closure.

## Phase 1 — global current-truth entry-point alignment — QA PASS

Original Phase 0+1 PRE-SCOPE:

`148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`

Phase 0+1 final branch HEAD:

`d9610a7da4fe8fc759e9809843d989f1befcda5c`

Physical path classification:

```text
added      1
modified   7
deleted    0
unexpected 0
```

The native GitHub compare endpoint was unavailable; fallback remote QA used verified refs, a bounded linear commit chain, per-commit changed-path evidence and remote payload readback. `main` remained unchanged.

## Phase 2 — architecture supersession/current-truth cleanup — CONTENT WRITTEN / QA PENDING

### Approved Phase 2 gate

```text
BRANCH
chore/pre-physical-coherence

PRE-SCOPE
d9610a7da4fe8fc759e9809843d989f1befcda5c

CREATE
docs/architecture/README.md

UPDATE
README.md
docs/README.md
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/pre-physical-coherence.md
docs/development/agent-operating-manual.md
docs/development/operating-rules.md
docs/development/documentation-and-handoff.md
docs/architecture/system-overview.md
docs/architecture/technical-decisions.md
docs/decisions/ADR-002-backend.md
docs/decisions/ADR-003-primary-database.md
docs/decisions/ADR-005-ai-gateway.md
docs/decisions/ADR-006-hybrid-personal-data-model.md
docs/decisions/ADR-007-domain-model-informed-persistence-boundaries.md

DELETE
docs/architecture/personal-data-ai-integration.md
```

### Phase 2 current results

- current architecture navigation is explicit;
- current system overview no longer selects Physical persistence prematurely;
- current technical decisions distinguish decided direction from benchmark/open choices;
- PostgreSQL is a preferred Physical baseline, not final selection;
- TypeDB remains mandatory challenger;
- generic EAV/generic-edge/universal meta-model remains rejected;
- ADR-002 is qualified at ORM/migration boundary;
- ADR-003 is superseded as final database selection but keeps useful PostgreSQL rationale;
- ADR-005 remains accepted with Logical/governed-effect qualification;
- ADR-006 is superseded as canonical generic hybrid semantic architecture;
- ADR-007 remains accepted as semantic guardrail but is qualified for Physical posture;
- documentation governance now requires current-truth-only specifications + knowledge coverage before replace/delete;
- root README ADR-007 path is corrected to the actual file;
- historical Domain→Logical readiness chain remains evidence, not current architecture.

### Knowledge coverage for retiring `personal-data-ai-integration.md`

Meaningful content was classified as follows:

```text
AI/external source != canonical truth
→ current system overview + ADR-005 + Logical hardenings

provider provenance / deduplication / reconciliation
→ current system overview + technical decisions + later integration requirements

Context Builder / minimal relevant context
→ ADR-005 + current technical decisions + later Phase 6

deterministic vs AI responsibility
→ current system overview + technical decisions

planned/current/actual/derived/raw distinctions
→ Domain/Logical current semantics + technical decisions

file/object storage abstraction
→ ADR-004 + current system overview/technical decisions

history/version/correction/reconciliation
→ Domain/Logical + WL-H hardenings

specialist extension boundary
→ Domain/Logical specialist boundary + current technical direction

universal grammar / generic Entity-Relation ontology
→ SUPERSEDED / REJECTED

entity_relations-style canonical semantic layer
→ SUPERSEDED / REJECTED

generic relation/property AI fallback
→ SUPERSEDED / REJECTED

generic-model-first semantic rule
→ SUPERSEDED / REJECTED

old kernel owner list using Program/Project/Skill/Register/etc.
→ SUPERSEDED by Domain Atlas

PostgreSQL final selection
→ SUPERSEDED by Physical benchmark posture

measured-workload-only infrastructure rule
→ REPLACED by demonstrated-benefit rule

open Physical/runtime requirements
→ retained in this roadmap/workstream for later explicit phases
```

Required final coverage verdict after remote deletion/readback:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```

### Phase 2 final QA requirements

Before Phase 2 can be called PASS:

```text
expected physical paths == actual physical paths
CREATE 1
UPDATE 15
DELETE 1
unexpected 0
main unchanged
remote payload readback current docs PASS
retired file absent on branch
knowledge coverage PASS
historical readiness evidence unchanged
Domain reopen 0
Logical reopen 0
```

## Phase 3 — Backend Foundation handoff cleanup — NEXT ONLY AFTER PHASE 2 QA PASS

Candidate target under a separate exact write gate:

`docs/workstreams/backend-foundation.md`

Backend Foundation must eventually consume:

```text
CLOSED Domain Atlas
+
CLOSED Logical Model
+
future accepted Physical Model
+
current architecture/runtime/security/integration contracts
```

The stale handoff must not instruct contributors to create Domain Model v0 inside backend bootstrap or execute pre-Domain persistence assumptions.

## Phase 4 — current Pre-Physical Architecture Baseline

Create one current bridge source stating decided/open/prohibited architecture, `WL-H01..WL-H12`, runtime-vs-Domain boundaries and future benchmark obligations.

## Phase 5 — requirements that can constrain Physical design

Define requirements, not implementation, for:

1. AuthN/AuthZ;
2. security/privacy/retention/recovery;
3. transaction/consistency/outbox/side effects;
4. non-functional/multi-device/recovery envelope.

AuthN/AuthZ minimum boundary:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
```

## Phase 6 — AI/context/runtime/integration boundaries

Keep distinct:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate/unresolved state
transient LLM working context
```

Runtime Agent/Workflow/Automation/Notification concepts do not become Domain owners automatically.

Integration modes:

1. canonical import;
2. synchronized/mirrored provider state;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

Protocols such as MCP/A2A/future equivalents are adapters, not ontology.

## Phase 7 — durable workflow / async benchmark

Compare at least:

- PostgreSQL + worker + transactional outbox;
- Temporal;
- Restate;
- DBOS.

No winner is preselected.

## Phase 8 — governed API/command/effect contract

Define consequential-operation contract before concrete routes.

```text
HTTP route / UI button / AuthZ action string
!= canonical Governed Operation
```

## Phase 9 — search/observability/calendar/solver pressure

Define requirements/benchmark pressure without premature infrastructure selection.

## Phase 10 — Physical benchmark specification/register

Current posture:

```text
PostgreSQL hybrid — preferred baseline, not selected
TypeDB — mandatory challenger
Neo4j/property graph — secondary/read-projection candidate
event/document mechanisms — bounded candidates
pgvector — bounded semantic-retrieval candidate
generic EAV/generic edge/universal meta-model — hard reject
```

Use destructive LifeOS scenarios: consequential concurrency, multi-owner mutation, selective disclosure, provider divergence, redaction/history, DST recurrence, stale derived state, AuthZ provenance, search inference leakage, AI proposal→approval→effect, revoked governance during execution, crash/restart, restore and schema evolution.

## Phase 11 — repository engineering safety

Establish appropriate main protection/ruleset/CI/required checks before production backend implementation.

## Phase 12 — clean-room QA and closure

A new agent without chat context must reconstruct current truth, closed Domain/Logical, current architecture, downstream requirements/candidates and what remains unauthorized.

Target:

```text
REPOSITORY / ARCHITECTURE COHERENCE PASS
DOMAIN UNCHANGED / CLOSED
LOGICAL UNCHANGED / CLOSED
PHYSICAL READY FOR SEPARATE AUTHORIZATION / NOT STARTED
```

## Specialized infrastructure rule

Specialized infrastructure requires demonstrated benefit. Evidence may come from measured workload **or** a sufficiently strong structural improvement in correctness, durability, security, evolvability, operational reliability or migration-risk reduction.

## Explicitly out of scope until separately gated

- Domain semantic changes;
- Logical semantic changes;
- Physical Model;
- SQL/schema/indexes/migrations;
- concrete API/backend implementation;
- concrete Auth provider/runtime selection;
- provider adapters;
- frontend/prototype changes inside this workstream;
- historical branch cleanup/deletion;
- direct modification of `main`.

## Current exact continuation

Complete Phase 2 remote physical-path + knowledge-coverage QA.

Only if that passes:

```text
PHASE 2
QA PASS

NEXT
PHASE 3 — READ-ONLY BACKEND FOUNDATION HANDOFF AUDIT
THEN A SEPARATE EXACT WRITE GATE
```

Do not begin Phase 3 writes from this gate.

## Tool incident record relevant to current continuation

- Before Phase 2 real writes, three malformed/no-op test operations were rejected (`409` bad blob SHA; `404` nonexistent path/branch). They did not move the branch or change content.
- Two same-SHA `update_ref` calls left the branch at the identical PRE-SCOPE and created no content commit.
- One initial ADR-007 update returned upstream `502`; remote readback proved the old blob remained unchanged, so the write was retried once and succeeded.

Only remote repository state counts as completion.
