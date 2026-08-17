# Pre-Physical Repository & Architecture Coherence

- Status: **FINAL CLOSURE CANDIDATE — Phase 12 activation pending final remote gate QA**
- Branch: `chore/pre-physical-coherence`
- Original workstream base: `main @ 148a4cb5d5741b4a5b9667cf8d30231ebc0545f0`
- Started: 2026-08-17
- Production backend code: **NOT STARTED**
- Physical Model: **NOT STARTED / NOT AUTHORIZED**
- Core Domain Model / Domain Atlas: **CLOSED / unchanged**
- Logical Model: **CLOSED / unchanged**
- Main integration: **NOT AUTHORIZED YET**

## Purpose

Bridge the closed Domain + Logical Models and any later separately authorized Physical Model by making repository/current architecture truth coherent, establishing pre-Physical technical requirements and benchmark inputs, hardening repository integration safety and proving clean-room recoverability from repository truth.

A genuine semantic contradiction requires a separate explicit Domain/Logical reopen. Cleanup, Physical design or implementation convenience must never silently alter closed semantics.

## Current accepted stage

```text
PRODUCT / NORTH STAR
CURRENT

DOMAIN MODEL / DOMAIN ATLAS
CLOSED
Whole-Domain PASS WITH HARDENING / POST-WRITE QA PASS

LOGICAL MODEL
CLOSED
Whole-Logical PASS WITH HARDENING / REMOTE QA PASS
WD-03 PASS
WD-05 PASS
WL-H01..WL-H12 active

PRE-PHYSICAL COHERENCE
FINAL CLOSURE CANDIDATE
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
Phase 12 closure record written / activation pending final exact remote gate QA

AFTER PHASE 12 ACTIVATION
independent total repository audit REQUIRED before definitive whole-workstream closure

MAIN INTEGRATION
NOT AUTHORIZED

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND FOUNDATION / PRODUCTION IMPLEMENTATION
NOT STARTED / DEFERRED
```

## Mandatory bootstrap

Before any further work:

1. read root `README.md`;
2. read `docs/README.md`;
3. read `docs/PROJECT-STATUS.md`;
4. read `docs/development/agent-operating-manual.md`;
5. read `docs/development/operating-rules.md`;
6. read `docs/development/documentation-and-handoff.md`;
7. read `docs/development/branching-and-environments.md`;
8. read `docs/development/repository-engineering-safety.md`;
9. read this complete handoff;
10. read `docs/architecture/README.md` and linked current architecture sources;
11. read `docs/architecture/pre-physical-architecture-baseline.md`;
12. read `docs/architecture/pre-physical-clean-room-qa.md`;
13. read all Phase 5 requirement packages;
14. read Phase 6 AI/context/runtime + Integration Hub contracts;
15. read Phase 7 durable-execution benchmark;
16. read Phase 8 governed-operation/effect contract;
17. read Phase 9 search/observability/calendar/solver contract;
18. read all three Phase 10 Physical benchmark-method documents;
19. read complete cumulative/split Domain/Logical authority where material;
20. read relevant ADR/evidence/methodology;
21. verify current branch/ref and relation to `main` before any write;
22. issue a fresh exact PRE-SCOPE/write gate for any new write scope.

## Domain / Logical closure discoverability

Do not stop at an early cumulative payload carrying truthful historical state.

Domain closure authority includes:

- `docs/domain/README.md` — entry payload;
- `docs/domain/README-part-20.md` — final corrected closure/status continuation;
- `docs/domain/checkpoints/whole-domain-final-regression-v0-validation-part-7.md` — final closure evidence;
- `docs/domain/language-map.md` + `docs/domain/language-map-part-22.md` — language authority/final disposition.

Logical closure authority includes:

- `docs/logical-model/whole-logical-model-v1.md` — canonical content payload;
- complete `docs/logical-model/decision-and-assumption-register-v1*` logical chain;
- `docs/logical-model/checkpoints/whole-logical-v1-remote-qa.md` — separate closure activation.

```text
DOMAIN REOPEN REQUIRED 0
LOGICAL REOPEN REQUIRED 0
```

## Documentation lifecycle rule

```text
CURRENT SPECIFICATION
= current truth only

ADR
= rationale + explicit status/supersession/qualification

HISTORICAL / VALIDATION EVIDENCE
= truthful chronology

GIT / PR HISTORY
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

### Size/tool-limit split rule — mandatory

```text
ONE COMPLETE LOGICAL PAYLOAD
→ LOSSLESS PHYSICAL PARTITION
→ ONE COMPLETE LOGICAL PAYLOAD
```

A size/tool-limit split is **not** summarization, condensation, omission, paraphrase-as-compression or hidden semantic cleanup. If content itself changes, that is a separate content/current-truth operation. Chronological/evidence continuation may append genuine later evidence and is distinct from a transport split.

## Non-negotiable downstream hardenings

Later architecture/Physical/runtime/backend work must preserve all `WL-H01..WL-H12`, including:

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

Current high-risk non-collapse rules include:

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

Backend Foundation remains deferred/non-executable.

### Phase 4 — Current Pre-Physical Architecture Baseline

```text
PRE-SCOPE
46b963394e29179fadf20cb3b11c35dbf3b6edc2

CONTENT HEAD
d67cd83f462611b2cc6d341937432e705f7a8682

RESULT
QA PASS
```

The old accidental `__no-op__` ref is absent.

### Phase 5 — requirements constraining Physical

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

FINAL PHASE-6 HEAD
2cf77ea7e3d548147bbe2b0d87304b4d5393ff5f

RESULT
QA PASS
```

Context categories:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

Integration Hub preserves five modes. No AI provider/model, agent framework, generic AI-memory truth store, MCP/A2A implementation, workflow engine or provider adapter was selected.

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
DB + worker/outbox style = valid baseline class

DEDICATED DURABLE EXECUTION
Restate   preferred structural-fit candidate — NOT selected
Temporal  strongest mandatory challenger — NOT selected
DBOS      conditional PostgreSQL-dependent challenger — NOT selected
```

### Phase 10 — Physical benchmark method

```text
PRE-SCOPE
01df10a4267880a213ede8582b0193ff616f9a70

CONTENT HEAD
057df9bdc19d89ea74fcee0e5d999ebc34cf93dc

PROPAGATION HEAD
0a9d80fa9d2ecaf373f0d5ad22b7953b73412a8c

FINAL VERIFIED PHASE-10 HEAD
7a87cba891c24e58e4448faf20c9feb30c1559bf

RESULT
QA PASS
```

Phase 10 defines **how** the later Physical benchmark must run, not which technology wins.

```text
PRIMARY
PostgreSQL hybrid — preferred mandatory baseline, NOT selected
TypeDB            — mandatory challenger, NOT selected

SECONDARY GRAPH
no-specialized-store baseline vs Neo4j

SEARCH / VECTOR
structured + lexical/full-text baseline vs bounded pgvector
```

Hard correctness gates precede scoring; synthetic tiers are not forecasts; exact version/edition/deployment evidence is required; `PREFERRED != SELECTED`.

### Phase 11 — repository engineering safety

```text
PRE-SCOPE
7a87cba891c24e58e4448faf20c9feb30c1559bf

STEP-A CONTENT / POLICY HEAD
62d9118def30c8545b9db2de49d654b4b74e55ab

CLOSURE PROPAGATION HEAD
c1ea90f417d3b680b1815c46b2b05b85295afb7c

FINAL VERIFIED PHASE-11 HEAD
d7fe582872be97ddb9c7a4e322918fccbb3e26e0

RESULT
QA PASS
```

Phase 11 final physical result:

```text
ahead_by      13
behind_by      0
unique_paths  12
added          2
modified      10
deleted        0
unexpected     0
```

Effective GitHub state verified:

```text
lifeos-main-safety active
main protected
PR required
deletion blocked
force-push / non-fast-forward blocked
review-thread resolution required
required approvals 0
required checks 0 while no real stable contexts exist
auto-delete merged branches enabled
confirmed accidental refs absent
```

Dependabot/secret/code-scanning endpoints remain connector-unverifiable because of integration permissions; no independent API PASS was fabricated.

## Phase 12 — clean-room repository / architecture QA

Approved Phase 12 gate:

```text
PRE-SCOPE
d7fe582872be97ddb9c7a4e322918fccbb3e26e0

CREATE
1

docs/architecture/pre-physical-clean-room-qa.md

UPDATE
10

CONTRIBUTING.md
README.md
docs/README.md
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/architecture/README.md
docs/architecture/pre-physical-architecture-baseline.md
docs/architecture/system-overview.md
docs/workstreams/backend-foundation.md
docs/workstreams/pre-physical-coherence.md

DELETE
0

UNIQUE PATHS
11
```

### Initial read-only clean-room verdict

```text
PASS WITH BOUNDED REPAIR

DOMAIN REOPEN REQUIRED                 0
LOGICAL REOPEN REQUIRED                0
NEW DOMAIN OWNER REQUIRED              0
SEMANTIC CONTRADICTION                 0
ARCHITECTURAL CONTRADICTION            0
PHYSICAL MODEL STARTED                 0
BACKEND STARTED                        0
BOUNDED CURRENT-TRUTH REPAIRS          5
```

Repairs discovered:

1. architecture navigation had not consumed Phase 11 and did not make cumulative Domain closure sufficiently discoverable;
2. Pre-Physical baseline still treated Phase 11 as open/next;
3. system overview stopped at Phase 10;
4. Backend handoff still said GitHub settings verification pending;
5. `CONTRIBUTING.md` retained an obsolete instruction that could imply Domain work inside Backend Foundation.

No Domain/Logical semantic payload was changed.

### Phase 12 repair HEAD

```text
4d4c5eaccd97096e55a0736b18ef836e6c9fa673
```

Repair compare from PRE-SCOPE:

```text
ahead_by       5
behind_by      0
total_commits  5
added          0
modified       5
deleted        0
unexpected     0
```

### Post-repair clean-room rerun

```text
Domain closure discoverable               PASS
Logical closure discoverable              PASS
Phase 11 consumed by current architecture PASS
Backend still NOT STARTED                 PASS
Physical still NOT STARTED                PASS
PREFERRED != SELECTED                     PASS
current-vs-history distinction             PASS
ruleset still active                      PASS
remaining Phase-12 repair blocker         0
```

### Phase 12 closure evidence

Created:

```text
docs/architecture/pre-physical-clean-room-qa.md
```

Evidence commit:

```text
ab945295fe4e84d2ec86a75f577a19cff1fae320
```

The evidence record is conditionally activating and is not self-validating.

### Phase 12 propagation point before final save-game

```text
PROPAGATION HEAD
73be96456b3f30cb9d13d41f55324a2f85daa774

compare PRE-SCOPE -> PROPAGATION HEAD
status          ahead
ahead_by        10
behind_by       0
total_commits   10
unique_paths    10
added            1
modified         9
deleted          0
unexpected       0
```

At that point the **only approved path not yet written was this save-game**.

## Phase 12 activation contract

After this save-game write, do **no further content write** before QA.

Phase 12 becomes operative as:

```text
PHASE 12
QA PASS / CLOSED
```

only if final remote QA proves:

```text
branch         chore/pre-physical-coherence
base           d7fe582872be97ddb9c7a4e322918fccbb3e26e0
unique_paths   11
added           1
modified       10
deleted         0
unexpected      0
behind_by       0
main           148a4cb5d5741b4a5b9667cf8d30231ebc0545f0 unchanged
critical Phase-12/current closure payloads remotely readable
```

If any condition fails, do not call Phase 12 closed.

## Boundary after successful Phase 12 activation

Current explicit user instruction changes the previous immediate-merge plan.

Successful Phase 12 means:

```text
PHASE 12
QA PASS / CLOSED

DOMAIN
UNCHANGED / CLOSED

LOGICAL
UNCHANGED / CLOSED

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND
NOT STARTED / DEFERRED
```

But the **whole Pre-Physical workstream remains a final-closure candidate**, not definitively closed yet:

```text
PRE-PHYSICAL COHERENCE
FINAL CLOSURE CANDIDATE
NOT YET DEFINITIVELY CLOSED
```

The next exact activity is:

```text
INDEPENDENT TOTAL REPOSITORY AUDIT
READ-ONLY FIRST
```

That audit must inspect the complete relevant repository/workstream for mistakes, contradictions, stale current instructions, knowledge loss, erroneous supersession/current-vs-history classification, unintended scope changes, false PASS/CLOSED claims, branch/PR/ruleset inconsistencies and any implicit Physical/backend start.

Only after that total audit passes may the user separately authorize definitive Pre-Physical closure.

## Explicitly out of scope until that audit/authorization

```text
PR / merge of chore/pre-physical-coherence into main
main writes
Physical Model start
PostgreSQL / TypeDB / Neo4j selection
Physical schema / benchmark implementation
SQL / TypeQL / Cypher implementation
Backend Foundation branch/code
concrete API routes / DTOs
Auth implementation
Restate / Temporal / DBOS adoption
queue/outbox implementation
provider adapters
AI provider/model/agent framework
MCP/A2A adoption
dedicated search/vector deployment
observability vendor
solver implementation
Domain / Logical semantic changes
```

## Next safe action

Immediately after this save-game write:

1. re-fetch branch HEAD;
2. compare Phase-12 PRE-SCOPE to final HEAD;
3. verify exact 11-path physical delta;
4. re-fetch `main` and prove unchanged;
5. read back `docs/architecture/pre-physical-clean-room-qa.md` and current status/navigation markers;
6. if and only if all activation conditions pass, report **Phase 12 QA PASS / CLOSED**;
7. do **not** merge or definitively close the whole Pre-Physical workstream;
8. next begin the separately requested independent total repository audit read-only.
