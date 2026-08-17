# System Overview

- Status: **Current architecture overview**
- Last updated: 2026-08-17

## Stage boundary

This document describes the current logical/system architecture without selecting the future Physical Model.

```text
Core Domain Model / Domain Atlas
CLOSED

Logical Model
CLOSED

Pre-Physical Repository & Architecture Coherence
IN PROGRESS
Phase 5 requirements accepted
Phase 6 AI/context/runtime/integration boundaries established on active branch

Physical Model
NOT STARTED / NOT AUTHORIZED

Backend production implementation
NOT STARTED
```

Domain semantics are defined by the accepted Domain Atlas. Logical representation and downstream hardenings are defined by the closed Logical Model. This overview must not introduce a universal semantic Entity/Relationship root, a generic canonical property model, or a concrete persistence design by convenience.

## Logical architecture

```text
Web client (Next.js) -----------------------\
                                             \
Mobile client (Expo / React Native) ----------> Versioned LifeOS backend boundary
                                                  |-- authentication context / AuthZ enforcement
                                                  |-- governed domain operations and validation
                                                  |-- scheduling / planning / reasoning services
                                                  |-- provenance / history / reconciliation services
                                                  |-- projection / disclosure services
                                                  |-- Integration Hub / provider adapters
                                                  |-- AI Gateway + Context Builder
                                                  |-- provider-neutral tool/action interfaces
                                                  |-- observability / operational runtime boundaries
                                                            |
                                                            v
                                                Physical persistence/runtime
                                                TO BE SELECTED / BENCHMARKED
                                                            |
                                                StorageProvider / object storage
```

External providers, assistants, caches, indexes, projections and device-local stores are not alternate canonical LifeOS truth merely because they contain data.

## Client responsibilities

Clients are responsible for presentation, navigation, local interaction state, secure session handling, platform-specific capabilities and collection of user intent/confirmation where required.

A later multi-device/offline contract may authorize bounded local caches, queues or synchronization behavior. This document does not preselect those semantics beyond the Phase 5 requirement envelope.

Clients do not hold primary persistence credentials and do not own critical authorization or canonical domain invariants.

## Backend responsibilities

The backend boundary is responsible for enforcing accepted Domain/Logical semantics through technical services, including:

- validation of semantic target and operation intent;
- authorization enforcement without collapsing Principal, Actor, Authority, Consent or Visibility into one concept;
- expected-state/conflict handling for consequential writes where required;
- provenance, history, correction and reconciliation behavior;
- truthful multi-owner consistency or explicit staged/partial outcomes;
- provider-state versus canonical-state separation;
- selective projection/disclosure enforcement;
- scheduling/reasoning/replanning services;
- deterministic calculations and constraint handling where appropriate;
- AI context construction, proposal/effect validation and provider routing;
- integration/provider orchestration;
- technical observability and operational controls.

Concrete API routes, DTOs, transaction mechanics, AuthZ engine, workflow engine and persistence structures remain later stage decisions.

## Canonical-state responsibility

LifeOS owns canonical state and its material history. Physical representation remains open until the separately authorized Physical Model benchmark/design stage.

Any future persistence must preserve the closed Logical Model, including:

- owner-specific identity and lifecycle boundaries;
- discriminated references rather than a universal semantic root;
- planned/current/actual/observed/derived distinctions;
- specific relationship/governance semantics;
- provider identity/state as external representation rather than automatic canonical identity/truth;
- material history, correction, reconciliation and retention/tombstone integrity;
- bounded flexible/provider metadata without generic semantic fallback;
- unresolved/candidate interpretation where meaning is not yet established.

Current Physical benchmark posture:

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
REJECTED FOR CANONICAL KERNEL
```

## Integration responsibility

External applications and services are isolated behind provider/capability boundaries. Provider-specific payloads do not define LifeOS ontology.

The current Integration Hub contract preserves five distinct modes:

1. canonical import;
2. synchronized/mirrored provider state;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

Each flow must identify the applicable mode or bounded composition rather than treating all integrations as equivalent.

External identifiers, revisions and source data retain enough provenance for reconciliation and remain distinguishable from canonical LifeOS identity/state. `ExternalRef != NativeRef`; provider revision/token != `MaterialStateRef` by identity.

Canonical import requires explicit validation/mapping/acceptance. Sync/mirror preserves canonical and provider apply states separately. Live reads retain source/freshness/unknown state. Retrieval/index state remains derived and deletion-aware. Action/tool integration preserves governance, idempotency, ambiguous-outcome and reconciliation truth.

Provider callbacks/webhooks/polling are adapter mechanisms; duplicate/out-of-order delivery does not create latest-arrival canonical truth.

See [`integration-hub-boundaries.md`](integration-hub-boundaries.md).

## AI responsibility

AI access remains behind a replaceable/provider-neutral gateway and bounded Context Builder.

AI may interpret ambiguous input, help reason across domains, generate proposals and support explanation. It does not become canonical truth by producing output and does not bypass domain validation, governance, expected-state checks or confirmation/autonomy policy.

The runtime keeps distinct:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate / unresolved state
transient LLM working context
```

The Context Builder is purpose-, disclosure-, provenance- and freshness-aware. It does not default to unrestricted database or complete-history exposure.

LifeOS does not maintain a generic second source of truth called `AI memory`: durable AI-relevant information must be classified into an accepted canonical/history/candidate/derived/source/provider representation.

AI output is classified according to task: answer/explanation, candidate/unresolved interpretation, structured extraction, Proposal/proposal-like candidate, scenario/recommendation or governed-effect request. Model output is not an accepted effect merely because it is structured.

Runtime Agent, service Principal, Tool, Workflow or Automation state remains technical/product/runtime state unless a separate accepted semantic role applies. `Principal != Actor`; tool/protocol action strings != canonical governed operation.

MCP/A2A/future tool/agent protocols are adapters, not ontology or LifeOS governance.

See [`ai-context-runtime-boundaries.md`](ai-context-runtime-boundaries.md).

Deterministic calculations, constraints, authorization decisions and straightforward state transitions should remain deterministic services where appropriate.

## Storage responsibility

Large object/file bytes remain behind a provider abstraction rather than normal domain rows. Domain semantics refer to accepted Content Artifact identity/meaning; blob path, URL, provider object or storage identifier is representation/integration state, not automatically domain identity.

The current storage abstraction direction remains compatible with local development and future S3-compatible/cloud object storage.

## Scalability and specialized infrastructure

The current backend architecture direction is a modular monolith.

Specialized infrastructure is introduced only when it demonstrates material benefit. Evidence may come from measured workload **or** a sufficiently strong structural improvement in correctness, durability, security, evolvability, operational reliability or migration-risk reduction.

Search/vector stores, caches, graph stores, analytics/time-series systems, workflow engines, policy engines, event infrastructure and similar systems are therefore evaluated as bounded mechanisms rather than assumed defaults.

## Non-negotiable Logical hardenings

Any later Physical/API/runtime architecture must preserve `WL-H01..WL-H12`, including:

- justified material Agreement terms;
- governed operation/effect semantics;
- bounded projection/disclosure surfaces;
- absence/unknown not collapsing to false;
- expected-state consequential writes;
- idempotency distinct from identity;
- truthful multi-owner consistency;
- canonical/provider-state separation;
- derived-state freshness/material basis;
- retention/redaction/tombstone integrity;
- reconstructible consequential AuthZ provenance;
- non-interference/inference-leakage protection.

Phase 5 requirement packages and the Phase 6 AI/context/runtime + Integration Hub contracts are mandatory downstream constraints.

See [`../logical-model/decision-and-assumption-register-v1-part-9.md`](../logical-model/decision-and-assumption-register-v1-part-9.md).

## Current navigation

For architecture navigation and the distinction between current specifications and historical transition evidence, read [`README.md`](README.md).