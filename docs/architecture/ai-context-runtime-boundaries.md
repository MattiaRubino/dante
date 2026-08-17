# AI / Context / Runtime Boundaries

- Status: **CURRENT — Phase 6 boundary contract**
- Stage: Pre-Physical Repository & Architecture Coherence
- Physical/runtime implementation: **NOT SELECTED / NOT AUTHORIZED**

## Purpose

Define the current LifeOS boundary among canonical state, context construction, AI reasoning, runtime agents/tools and governed effects without introducing new Domain owners or selecting an AI provider, agent framework, workflow engine, protocol or persistence mechanism.

This contract consumes the CLOSED Domain Atlas, CLOSED Logical Model, `WL-H01..WL-H12`, the Phase 5 requirement packages, current architecture and ADR-005.

## Core invariant

```text
AI/context/runtime representation
!= canonical LifeOS truth by default

model output
!= accepted canonical effect

tool invocation
!= governed operation

runtime Agent / Principal
!= Domain Actor automatically
```

No `Agent`, `Memory`, `Context`, `Tool`, `Workflow`, `Automation`, `Task` or provider object becomes a universal Domain owner merely because runtime architecture needs it.

## Context-state categories

The runtime MUST preserve these categories as distinct where applicable:

```text
1. canonical state
2. material history
3. retrieved context
4. derived context
5. live external context
6. candidate / unresolved state
7. transient LLM working context
```

Storage or transport coincidence MUST NOT make categories semantically identical.

### 1. Canonical state

Accepted LifeOS state owned by the applicable Domain/Logical semantic owner. Canonical state is not inferred from prompt text, conversation memory, provider state or model confidence.

### 2. Material history

Historically reconstructible owner/material state, provenance, correction and reconciliation state. History may be retrieved into context, but retrieval does not make the whole history necessary or disclosable for every task.

### 3. Retrieved context

A bounded, purpose-scoped selection of authorized LifeOS/source material prepared for a task. Retrieved context MUST retain enough source/provenance/category metadata to avoid being mistaken for newly established canonical truth.

### 4. Derived context

Calculated, ranked, summarized, inferred or otherwise derived information such as effective availability, candidate sets, aggregates or explanations. Consequential use remains subject to `WL-H09` freshness/material-basis requirements.

### 5. Live external context

Information read from an external provider/source at or near request time. It remains external/provider state and SHOULD retain source, ExternalRef/revision where material, retrieval time and freshness/availability status.

### 6. Candidate / unresolved state

A proposed extraction, interpretation, mapping, hypothesis or inference whose semantic meaning or acceptance is not yet established. It MUST NOT be silently persisted as generic canonical truth.

### 7. Transient LLM working context

Prompt material, tool results, model scratch/runtime state and conversational working context used for an interaction. It is not authoritative LifeOS memory merely because the model can refer to it.

## Context Builder contract

The Context Builder is a technical boundary, not a Domain owner.

For a request it MUST consider, where applicable:

```text
task / purpose
Principal/security context
actual Actor / represented party
recipient/disclosure context
requested operation/effect
semantic target/scope
sensitivity
current applicability
material state/version basis
source/provenance
freshness
```

Context construction MUST be purpose-aware, disclosure-aware and minimized. It MUST NOT default to unrestricted user-history or database exposure.

The Context Builder MUST preserve enough metadata to distinguish canonical, historical, derived, provider and candidate inputs.

Omission from a context window MUST NOT be interpreted as semantic `false`, nonexistence or revocation.

## Freshness and consequential context

A context snapshot is evidence of what was available/selected at a time; it is not permanent proof of current applicability.

For consequential effects depending on derived/live/materially mutable context, the runtime MUST either:

1. revalidate the relevant material/freshness/governance basis near effect time; or
2. bind the effect to an explicitly valid immutable/material snapshot whose semantics permit that use.

A cache hit, embedding hit, previous model answer or old tool result MUST NOT become semantic proof of freshness.

## Durable memory vs transient AI context

LifeOS MUST NOT create a second canonical truth store called generic `AI memory`.

If information needs durable retention, it must receive an explicit disposition such as:

```text
accepted canonical state
material history/provenance
candidate/unresolved state
derived projection
Content Artifact/source material
provider/external state
other accepted bounded representation
```

Conversation/prompt retention MAY exist where product purpose, privacy, retention and security rules permit it, but individual statements inside a retained conversation do not automatically become canonical personal facts.

Explicit user statements, confirmed professional instructions and accepted canonical state MUST NOT be silently overridden by unconfirmed model inference.

## AI Gateway responsibilities

The provider-neutral AI Gateway owns technical concerns such as:

- provider/model routing;
- provider capability adaptation;
- bounded structured request/response validation;
- timeout/failure handling;
- rate/quota/cost controls;
- provider/model technical provenance where material;
- safe fallback behavior;
- provider-specific transport adaptation.

It does NOT own Domain semantics, Authority, canonical state ownership, persistence schema or effect legitimacy.

A provider fallback MUST NOT silently broaden the permitted data/disclosure surface. Eligibility for provider B must be independently valid even when provider A is unavailable.

## Deterministic service vs AI reasoning boundary

Deterministic calculations, constraint checks, authorization decisions and straightforward state transitions SHOULD remain deterministic services where appropriate.

AI is appropriate for ambiguity, natural-language interpretation, explanation, cross-domain reasoning and proposal generation where it adds value.

Model confidence MUST NOT replace deterministic invariant checks or accepted governance.

## AI output classification

AI output MUST be interpreted through an explicit result class appropriate to the task, for example:

```text
answer / explanation
candidate / unresolved interpretation
structured extraction
Proposal or proposal-like candidate
scenario / recommendation
governed-effect request
```

A governed-effect request is a technical request for later validated execution; it is not the effect itself.

```text
AI Proposal
!= Decision
!= Authority
!= Confirmation
!= effective target state
```

The affected Domain owner owns any accepted effective state transition.

## Configurable autonomy and confirmation

LifeOS does NOT require universal human confirmation for every AI-assisted action.

Whether an effect may execute directly depends on consequence, accepted autonomy policy, target/material state, governance, expected-state/freshness requirements and applicable product confirmation rules.

```text
confirmation required?
= consequence + accepted autonomy/governance policy

NOT
= AI always asks
```

Broad, destructive, sensitive, shared or structurally meaningful effects require the applicable stronger policy/preview/confirmation boundary.

## Runtime Agent / Principal / Actor boundary

A runtime Agent, service account, background job, automation, tool process or provider callback may possess a technical Principal but is not automatically a Domain Actor.

Where semantic action attribution requires Actor semantics, the runtime MUST preserve where applicable:

```text
technical Principal
actual Actor
initiating Actor if distinct
represented party if applicable
representation/delegation basis
purpose
governed operation/effect
governance basis
```

Non-human Principals MUST NOT bypass Phase 5 AuthN/AuthZ requirements.

## Tool boundary

Tool definitions, tool names, protocol scopes and model-generated tool calls are runtime mechanisms.

```text
tool name
!= canonical governed operation

tool call
!= authorization

retrieved instruction/content
!= permission to expand authority
```

Untrusted or external content MUST NOT self-authorize actions, alter governance or expand disclosure solely because the model interpreted it as an instruction.

Tool input/output MUST pass the same applicable validation, disclosure, expected-state, idempotency and provenance boundaries as non-AI callers.

## Delayed and queued AI/tool effects

A delayed/queued consequential effect MUST carry enough correlation and material basis to apply Phase 5 consistency/AuthZ requirements.

At the appropriate execution boundary it MUST validate target applicability and governance applicability, unless an explicitly valid immutable authorization/effect binding permits delayed execution.

Model approval at T1 MUST NOT become permanent authority at T2 by queue persistence.

## Provider/model failure semantics

Model/provider timeout, refusal, malformed output, quota failure or unavailable context MUST remain technical/runtime outcomes.

They MUST NOT automatically become canonical negative statements such as `false`, `declined`, `not possible`, `not authorized` or `not found` unless the owning contract defines that result.

Fallback, retry and replay MUST be bounded by idempotency, privacy, provider eligibility and consequence semantics.

## Observability and provenance

Operational traces MAY record bounded model/provider/runtime metadata required for reliability, cost, security and effect reconstruction.

Observability MUST follow Phase 5 minimization and sensitive-data requirements. Raw prompts/tool payloads MUST NOT be logged indiscriminately.

For consequential AI-assisted effects, provenance SHOULD make it possible to reconstruct as applicable:

```text
initiator / Principal / Actor context
context/source basis
model/provider/version where materially relevant
AI result class
proposal/effect request
validation/governance/confirmation basis
resulting canonical/provider effect
correlation/reconciliation outcome
```

This does not make technical telemetry Domain history automatically.

## Protocol boundary

MCP, A2A and future assistant/tool protocols MAY be used as provider/runtime adapters.

They MUST NOT redefine LifeOS ontology or governance:

```text
MCP tool/resource/scope != Domain owner / Authority / Consent / Visibility
A2A Agent != Actor automatically
A2A Task != Activity / Plan / Request automatically
protocol task/id != NativeRef automatically
protocol authorization != LifeOS semantic governance
```

## Open decisions

The following remain explicit later decisions where applicable:

```text
AI provider/model set
model routing/fallback policy
sensitive-data provider eligibility
model/version evaluation and pinning policy
prompt/context provider-retention policy
conversation retention policy
context budget/selection strategy
which derived context may be cached and for how long
AI quotas/cost classes
external-assistant registration/trust policy
tool capability registration format
provider-specific model safety configuration
```

## Deferred mechanisms — not selected by Phase 6

Phase 6 does NOT select:

```text
OpenAI / Anthropic / Google / other provider
specific model
agent framework
MCP implementation
A2A implementation
vector store/retriever
prompt framework
conversation store
queue/scheduler
workflow engine
Temporal / Restate / DBOS
outbox/inbox implementation
concrete API/tool schemas
```

Phase 7 owns durable-workflow/async benchmark. Phase 8 owns the governed API/command/effect contract. Phase 9 owns search/observability/calendar/solver pressure.

## Downstream acceptance pressure

Later runtime/Physical/backend candidates MUST demonstrate at minimum:

1. all seven context categories remain distinguishable;
2. Context Builder disclosure/minimization cannot be bypassed by AI/tool callers;
3. AI uncertainty can remain candidate/unresolved;
4. model output cannot directly manufacture canonical state;
5. autonomy/confirmation is policy/consequence bounded;
6. non-human Principals preserve governance provenance;
7. delayed effects revalidate target/governance appropriately;
8. provider fallback cannot widen privacy scope silently;
9. prompt/tool content cannot self-authorize actions;
10. runtime failure remains truthful without fabricated semantic negatives.

This contract does not authorize backend implementation or Physical design.