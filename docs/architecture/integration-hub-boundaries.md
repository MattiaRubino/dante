# Integration Hub Boundaries

- Status: **CURRENT — Phase 6 boundary contract**
- Stage: Pre-Physical Repository & Architecture Coherence
- Provider/runtime implementation: **NOT SELECTED / NOT AUTHORIZED**

## Purpose

Define the current LifeOS integration boundary across imports, synchronization, live reads, retrieval/index projections and external actions without turning provider concepts, identifiers or protocols into canonical LifeOS ontology.

This contract consumes the CLOSED Domain Atlas, CLOSED Logical Model, `WL-H01..WL-H12`, Phase 5 requirements, current architecture and the AI/context/runtime boundary contract.

## Core invariant

```text
provider/source identity != LifeOS native identity
provider/source state != canonical LifeOS state
provider revision != MaterialStateRef by identity
protocol surface != LifeOS ontology
provider success != canonical effect completeness automatically
```

The Integration Hub is a technical/runtime boundary, not a Domain owner.

## Five integration modes

Every material integration flow MUST identify which mode or bounded composition of modes it uses:

1. canonical import;
2. synchronized/mirrored provider state;
3. live federated read;
4. retrieval/index projection;
5. action/tool integration.

Calling all five simply `integration` is insufficient where behavior, truth ownership, retention, freshness or side effects differ.

## Mode 1 — Canonical import

Canonical import brings external/source information into LifeOS for possible accepted canonical ownership.

The flow MUST preserve, where material:

```text
source/provider
ExternalRef/source identity
source revision/time
raw/source evidence or traceable source basis
candidate mapping/interpretation
validation/reconciliation
acceptance/governance basis
resulting LifeOS owner/material state
provenance
```

Import MUST NOT assume provider data is canonical merely because it is structurally valid.

Ambiguous mapping MAY remain candidate/unresolved. The runtime MUST NOT manufacture a default owner or generic Entity target solely to make import succeed.

A changed provider record does not automatically overwrite an accepted LifeOS state unless the bounded import/reconciliation policy explicitly permits that effect.

## Mode 2 — Synchronized / mirrored provider state

Synchronization maintains both LifeOS state and provider-side representation/apply state.

The following MUST remain distinguishable:

```text
canonical LifeOS target state
provider representation state
last known provider revision
sync/apply request state
provider acknowledgement/result
conflict/divergence state
reconciliation/compensation state
```

```text
canonical LifeOS state != provider sync state
```

Provider failure does not automatically roll canonical state back. Provider current value does not automatically win against LifeOS canonical state.

Directionality MUST be explicit by integration/facet where relevant:

```text
LifeOS -> provider
provider -> LifeOS
bidirectional
read-only mirror
write-through projection
other bounded mode
```

Bidirectional synchronization MUST define conflict/reconciliation semantics rather than relying on generic last-write-wins.

## Mode 3 — Live federated read

A live federated read obtains provider/source information on demand without automatically creating canonical LifeOS state.

The runtime SHOULD preserve where material:

```text
provider/source
ExternalRef or bounded source locator
retrieval/request time
provider revision/version where available
freshness/expiry semantics
availability/error/unknown state
recipient/disclosure context
```

A provider timeout or unavailable result MUST NOT automatically mean the requested fact is false or nonexistent.

Live data MAY inform a consequential decision only when freshness/material-basis requirements are satisfied.

Persisting a federated read result for cache/retrieval purposes does not silently convert it into canonical import.

## Mode 4 — Retrieval / index projection

Search indexes, vector indexes, embeddings, summaries, caches and retrieval projections are downstream representations.

They MUST retain enough source/reference/version/provenance information to trace results back to the applicable source/material basis.

```text
retrieval/index result
!= canonical state

embedding similarity
!= semantic truth

indexed existence
!= disclosure permission
```

Deletion, correction, redaction and access changes MUST have an explicit propagation/invalidation/reconciliation path under Phase 5 requirements.

If propagation is pending or impossible, the system MUST not falsely claim that all downstream copies are current/deleted.

A deliberately shareable derived result does not automatically declassify its hidden source.

## Mode 5 — Action / tool integration

Action/tool integration causes or requests an external side effect.

The runtime MUST distinguish, where material:

```text
LifeOS governed operation/effect request
canonical target/material basis
Principal / Actor / represented party / governance basis
idempotency/correlation context
adapter/provider request
provider acknowledgement
known / unknown external outcome
provider revision/result
canonical follow-up effect
partial/pending/failure state
reconciliation/compensation
```

A tool call or provider API operation string is not the canonical governed operation.

External effects MUST satisfy applicable expected-state, AuthZ, privacy, idempotency and consequence requirements.

## Mode composition

One integration may use multiple modes, but transitions MUST be explicit.

Example:

```text
live provider read
-> candidate interpretation
-> user/authorized acceptance
-> canonical import
```

is not the same as:

```text
live provider read
-> automatic canonical write
```

Likewise, an indexed provider result may support discovery while a later action/tool call uses a separately governed side-effect path.

## ExternalRef contract

Provider/source identities use the Logical `ExternalRef` boundary.

Conceptually, uniqueness may depend on:

```text
provider/source system
realm / tenant / account / integration instance
provider object/resource type
opaque external identifier
provider revision/version where material
```

The exact physical fields remain provider-specific.

```text
ExternalRef != NativeRef
ExternalRef != Account/Principal identity automatically
ExternalRef != MaterialStateRef
```

LifeOS MUST NOT assume `provider + id` is globally sufficient when tenant/account/source scope is material.

## Provider mapping and reconciliation

Mappings between external and LifeOS references are explicit logical/integration state.

A mapping MAY be:

```text
candidate
proposed
accepted
rejected
superseded
unresolved
```

and may retain confidence/evidence/provenance, actor/authority attribution and correction/revocation history where material.

Forbidden implicit reconciliation shortcuts include:

```text
same email -> same Person
current user -> default Person
provider object -> NativeRef
latest provider revision -> canonical winner
highest model confidence -> canonical mapping
```

A wrong mapping/merge MUST remain correctable without pretending the final resolution was always known.

## Provider revision vs material state

Provider revision, ETag, sequence number, change token or timestamp MAY support synchronization/concurrency but is not semantically identical to LifeOS `MaterialStateRef`.

Where consequential logic depends on both, the runtime MUST preserve both questions:

```text
which provider representation/revision?
which LifeOS material state/basis?
```

## Provider callbacks / webhooks / polling

Callback, webhook, polling and push transports are adapter mechanisms.

Incoming callbacks MUST be authenticated/validated according to provider/runtime policy and treated as external technical events/data, not direct canonical truth.

Duplicate/replayed callbacks MUST be safe under Phase 5 idempotency/replay requirements.

Out-of-order callbacks or missing revisions MUST remain representable as stale/unknown/conflicting provider state rather than forcing latest-arrival truth.

The choice among webhook/polling/push is provider/runtime-specific and deferred.

## Ambiguous external outcomes

A timeout/network failure may leave the external outcome unknown.

```text
timeout
!= external effect failed

provider 2xx
!= canonical LifeOS operation fully complete automatically
```

Before retrying a consequential external action, the runtime MUST use an accepted strategy to determine/reconcile whether the prior effect occurred when duplicate consequence is possible.

If provider and canonical effects diverge, the system MUST expose actual pending/partial/reconciliation truth rather than claiming rollback/success that did not happen.

## Delayed / queued external actions

Delayed/queued integration effects MUST revalidate target material state and applicable governance at the appropriate execution boundary unless an accepted immutable binding explicitly permits delayed execution.

A queued request surviving longer than Authority/Consent/target applicability MUST NOT execute merely because it remains technically deliverable.

Phase 7 owns durable workflow/async mechanism benchmarking; this contract only defines required behavior.

## Security, privacy, retention and deletion

Provider/integration exposure is subject to Phase 5 purpose, minimization, sensitivity and disclosure requirements.

For every material integration, later design MUST define as applicable:

```text
what data leaves LifeOS
purpose
provider/processor eligibility
retention/deletion capability
training/secondary-use restrictions where relevant
source/provenance retained locally
how access/revocation affects future calls
how deletion/correction propagates
what limitations remain outside LifeOS control
```

External copies MUST NOT become uncontrolled shadow truth.

When deletion/correction cannot be propagated immediately, the unresolved propagation state MUST be represented truthfully.

Restore/recovery MUST not silently recreate an integration/export copy whose current policy requires deletion/restriction.

## Provider outages and degraded mode

Provider outage, rate limit, quota exhaustion or stale source state MUST have truthful degraded behavior.

Cached/live/provider data MUST NOT masquerade as fresh canonical state merely to preserve availability.

Where a safe stale read is permitted, the staleness/source status SHOULD be explicit enough for the consuming contract.

Consequential actions that require current provider/governance/material state MUST fail/pause/revalidate rather than using unsafe stale data.

## AI + Integration interaction

AI may consume provider/live/retrieval context only through the applicable Context Builder/disclosure boundary.

AI-generated mappings/actions remain candidate/proposal/effect requests until accepted through LifeOS governance.

External content, provider metadata or retrieved instructions MUST NOT self-authorize a tool action or widen permissions.

Provider/tool output SHOULD retain enough provenance for later explanation/reconciliation where it influences a material decision/effect.

## Protocol adapter boundary

MCP, A2A and future tool/agent protocols are adapters.

They do NOT define LifeOS semantics:

```text
MCP resource/tool/scope != Domain owner / governed effect / Authority
A2A Agent != Actor automatically
A2A Task != Activity / Plan / Request automatically
protocol task/resource ID != NativeRef automatically
protocol authorization != semantic Authority/Consent/Visibility
```

Provider/protocol task state may be LR-09/runtime state and MUST not silently replace the applicable LifeOS owner/effect state.

## Open decisions

The following remain explicit later decisions by integration/provider where applicable:

```text
provider set and prioritization
source-of-record direction per provider/facet
provider-specific object mapping rules
sync direction and conflict policy per bounded integration
polling vs webhook vs push
provider revision/change-token strategy
provider retention/deletion limitations
provider quota/rate-limit classes
external assistant registration/trust policy
protocol adoption (MCP/A2A/future)
provider-specific retry/acknowledgement semantics
```

## Deferred mechanisms — not selected by Phase 6

Phase 6 does NOT select:

```text
Google/Microsoft/etc adapter implementation
provider SDK
sync engine
queue/event bus
workflow engine
transactional outbox/inbox
CDC mechanism
webhook framework
polling scheduler
MCP server/client implementation
A2A implementation
search/vector store
provider-specific storage schema
```

## Downstream acceptance pressure

Later runtime/Physical/backend candidates MUST demonstrate at minimum:

1. all five integration modes remain distinguishable;
2. ExternalRef cannot silently become NativeRef;
3. provider revisions cannot replace LifeOS material state semantics;
4. sync conflict does not rely on universal last-write-wins;
5. federated read unavailability remains unknown/degraded rather than false;
6. retrieval/index state remains derived and deletion-aware;
7. action/tool effects preserve idempotency, governance and partial-state truth;
8. duplicate/out-of-order callbacks remain safe;
9. delayed actions revalidate target/governance appropriately;
10. deletion/privacy limitations of external copies remain explicit;
11. provider outage cannot manufacture canonical success;
12. protocol adoption cannot redefine Domain/Logical semantics.

This contract does not authorize provider adapters, backend implementation or Physical design.