# Documentation Index

This directory is the durable project memory for LifeOS. It is designed so a new human/AI contributor can resume from the repository without reconstructing decisions from chat history.

## Start here

Read in this order:

1. [`../README.md`](../README.md)
2. [`PROJECT-STATUS.md`](PROJECT-STATUS.md)
3. [`development/agent-operating-manual.md`](development/agent-operating-manual.md)
4. [`development/operating-rules.md`](development/operating-rules.md)
5. [`development/documentation-and-handoff.md`](development/documentation-and-handoff.md)
6. [`development/branching-and-environments.md`](development/branching-and-environments.md)
7. the active [`workstreams/`](workstreams/) handoff
8. current model/architecture index and linked current sources
9. relevant ADRs/evidence/methodologies
10. relevant implementation/tests

## Current backend/architecture stage

```text
PRODUCT / NORTH STAR
CURRENT

CORE DOMAIN MODEL / DOMAIN ATLAS
CLOSED — PR #10

LOGICAL MODEL
CLOSED — PR #11
Whole-Logical PASS WITH HARDENING / REMOTE QA PASS
WD-03 PASS
WD-05 PASS

PRE-PHYSICAL REPOSITORY & ARCHITECTURE COHERENCE
IN PROGRESS

PHYSICAL MODEL
NOT STARTED / NOT AUTHORIZED

BACKEND PRODUCTION IMPLEMENTATION
NOT STARTED
```

Active handoff: [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md).

## Current semantic/model sources

- [`product/product-identity-and-north-star.md`](product/product-identity-and-north-star.md) — current product identity/North Star.
- [`domain/README.md`](domain/README.md) — Domain Atlas entry point.
- [`domain/language-map.md`](domain/language-map.md) — current Domain language map.
- [`logical-model/whole-logical-model-v1.md`](logical-model/whole-logical-model-v1.md) — closed Whole Logical Model.
- [`logical-model/decision-and-assumption-register-v1-part-9.md`](logical-model/decision-and-assumption-register-v1-part-9.md) — final Whole-Logical decisions/hardenings/deferrals.
- [`logical-model/checkpoints/whole-logical-v1-remote-qa.md`](logical-model/checkpoints/whole-logical-v1-remote-qa.md) — canonical Logical closure evidence.

Product/UI terminology does not override accepted Domain/Logical semantics.

## Current architecture sources

Start with [`architecture/README.md`](architecture/README.md). It explicitly separates current architecture from historical transition evidence.

Current specifications:

- [`architecture/system-overview.md`](architecture/system-overview.md)
- [`architecture/technical-decisions.md`](architecture/technical-decisions.md)

The old mixed `personal-data-ai-integration.md` current specification has been retired after knowledge coverage; its useful current content is carried by the current architecture/ADR/Logical sources, and its old payload remains recoverable in Git history.

Historical `domain-model-logical-readiness*` files remain truthful transition/validation evidence and are **not** current architecture specifications.

## ADR status

ADRs preserve rationale and explicit current status:

- ADR-001 — accepted client platforms;
- ADR-002 — accepted backend platform direction, qualified at ORM/migration boundary;
- ADR-003 — superseded as final database selection; retained PostgreSQL rationale;
- ADR-004 — accepted storage abstraction;
- ADR-005 — accepted replaceable AI gateway, Logical-qualified;
- ADR-006 — superseded as canonical generic hybrid semantic model;
- ADR-007 — accepted semantic persistence guardrail, qualified for Physical posture.

An older `Accepted` label is not timeless authority; use the current status inside the ADR and current model/architecture sources.

## Current Physical benchmark posture

```text
PostgreSQL hybrid
CURRENT PREFERRED BASELINE — not final selection

TypeDB
MANDATORY CHALLENGER

Neo4j / property graph
SERIOUS SECONDARY / READ-PROJECTION CANDIDATE

event/document mechanisms
BOUNDED CANDIDATES

generic EAV / generic edge / universal meta-model
HARD REJECT FOR CANONICAL KERNEL
```

## Workstreams

- [`workstreams/pre-physical-coherence.md`](workstreams/pre-physical-coherence.md) — active backend/architecture preparation workstream.
- [`workstreams/today-home.md`](workstreams/today-home.md) — active separate Phase 4 UX/product-structure workstream.
- [`workstreams/backend-foundation.md`](workstreams/backend-foundation.md) — deferred/stale handoff; do not execute until its later bounded cleanup and prerequisites.
- Domain/Logical workstream documents are closed-stage evidence; `main` is authoritative for integrated state.

## Documentation lifecycle rule

```text
CURRENT SPECIFICATION
= current truth only

ADR
= rationale + explicit current status/supersession

HISTORICAL / VALIDATION EVIDENCE
= truthful chronology

GIT
= recoverable history
```

Before a stale current document is replaced/deleted:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```

Do not accumulate obsolete design history inside current specifications. Do not delete useful knowledge before coverage proves it safe.

## Development process

- [`development/agent-operating-manual.md`](development/agent-operating-manual.md) — exact write gates, remote QA, documentation lifecycle, split/tool-failure rules.
- [`development/operating-rules.md`](development/operating-rules.md) — authority, branches/path ownership, coherence gates.
- [`development/documentation-and-handoff.md`](development/documentation-and-handoff.md) — current-truth/evidence separation and handoff protocol.
- [`development/branching-and-environments.md`](development/branching-and-environments.md) — Git/environment policy.

## Source-of-truth rule

For integrated state, current `main` wins over conversation memory and historical branches/files. For an active unmerged workstream, its bounded handoff/current files may contain newer work only inside that scope.
