# Architecture Documentation

- Status: **Current navigation**
- Last updated: 2026-08-17

## Purpose

This directory separates **current architectural truth** from historical transition/validation evidence.

Current specifications must describe the architecture as it is understood now. They are not chronological logs. When a current specification changes, obsolete prose is replaced after a knowledge-coverage check; useful rationale/history remains recoverable through Git, ADRs, checkpoints, or explicitly historical evidence.

## Current architecture sources

Read these for the current architecture state:

1. [`system-overview.md`](system-overview.md) — current logical/system boundary overview;
2. [`technical-decisions.md`](technical-decisions.md) — current decided technical directions and explicitly open benchmark choices;
3. [`../domain/README.md`](../domain/README.md) and [`../domain/language-map.md`](../domain/language-map.md) — accepted Domain Atlas semantics;
4. [`../logical-model/whole-logical-model-v1.md`](../logical-model/whole-logical-model-v1.md) — accepted Logical Model;
5. [`../logical-model/decision-and-assumption-register-v1-part-9.md`](../logical-model/decision-and-assumption-register-v1-part-9.md) — current downstream hardenings, assumptions, rejected alternatives and Physical/runtime deferrals;
6. [`../logical-model/checkpoints/whole-logical-v1-remote-qa.md`](../logical-model/checkpoints/whole-logical-v1-remote-qa.md) — Logical Model closure evidence;
7. [`../workstreams/pre-physical-coherence.md`](../workstreams/pre-physical-coherence.md) — active Pre-Physical architecture/repository workstream.

## Current stage boundary

```text
Domain Model
CLOSED

Logical Model
CLOSED

Pre-Physical Repository & Architecture Coherence
IN PROGRESS

Physical Model
NOT STARTED / NOT AUTHORIZED

Backend production implementation
NOT STARTED
```

The current persistence posture is a benchmark posture, not a final Physical selection:

- PostgreSQL hybrid — current preferred baseline;
- TypeDB — mandatory challenger;
- Neo4j/property graph — serious secondary/read-projection candidate;
- event/document mechanisms — bounded candidates;
- generic EAV/generic-edge/universal meta-model — rejected for the canonical kernel.

## Historical transition / validation evidence

The following canonical chain records the truthful Domain → Logical readiness transition. It is **evidence**, not a current architecture specification:

- [`domain-model-logical-readiness.md`](domain-model-logical-readiness.md)
- [`domain-model-logical-readiness-part-2.md`](domain-model-logical-readiness-part-2.md)
- [`domain-model-logical-readiness-part-3.md`](domain-model-logical-readiness-part-3.md)
- [`domain-model-logical-readiness-part-4.md`](domain-model-logical-readiness-part-4.md)
- [`domain-model-logical-readiness-part-5.md`](domain-model-logical-readiness-part-5.md)

Those files intentionally retain READY/HOLD/reopen/restoration/clearance chronology. Do not rewrite them to look current.

## ADR handling

ADRs preserve decision rationale and explicit supersession state. An older ADR may remain useful historical evidence while no longer being current execution authority.

Current architecture specifications should not repeat obsolete ADR prose merely to preserve history. They should state the current result and link to the relevant ADR only where rationale is useful.

## Documentation rule

```text
CURRENT SPECIFICATION
= current truth only

HISTORICAL / VALIDATION EVIDENCE
= truthful chronology preserved

ADR
= decision rationale + explicit supersession/qualification

GIT
= complete recoverable file history
```

Before replacing or deleting a stale current document, classify every meaningful statement and prove:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```
