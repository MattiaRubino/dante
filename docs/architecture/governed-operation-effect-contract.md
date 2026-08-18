# Governed Operation / Effect Contract

- Status: **CURRENT — Phase 8 contract**
- Stage: Pre-Physical Repository & Architecture Coherence
- Concrete API/routes/DTOs: **NOT DEFINED / NOT AUTHORIZED**
- Durable runtime implementation: **NOT SELECTED / NOT AUTHORIZED**
- Physical Model: **NOT STARTED / NOT AUTHORIZED**

## Purpose

Define the LifeOS technical/application contract for consequential operations before concrete HTTP routes, DTOs, tool schemas or workflow-engine bindings are designed.

This contract consumes:

- the CLOSED Domain Atlas;
- the CLOSED Logical Model and `WL-H01..WL-H12`;
- all Phase 5 requirement packages;
- Phase 6 AI/context/runtime and Integration Hub boundaries;
- Phase 7 durable-execution benchmark and its engine-neutral routing boundary.

The contract translates caller intent into governed consequence without creating a new universal Domain `Command`, `Operation`, `Action`, `Effect`, `Task` or `Workflow` owner.

## Core invariant

```text
HTTP route
!= UI button
!= tool name
!= AuthZ action string
!= runtime workflow step
!= canonical governed operation/effect meaning
```

Likewise:

```text
request accepted
!= effect completed

workflow completed
!= Domain Actual / Outcome automatically

provider acknowledgement
!= canonical effect completeness automatically

technical cancellation
!= Domain cancellation automatically
```

The affected Domain owner owns the effective semantic state transition. This contract carries the technical/application information needed to validate, govern, execute and explain that transition.

## Contract layers

A consequential interaction SHOULD remain decomposable into these layers:

```text
caller intent / request
        ↓
operation interpretation / target resolution
        ↓
Governed Operation Request
        ↓
material/freshness preconditions
        ↓
governance + disclosure + autonomy/confirmation
        ↓
accepted execution plan/class
        ↓
canonical and/or external effect attempts
        ↓
result axes + provenance + reconciliation state
```

Not every low-consequence operation requires every field to be materialized durably. Materiality is consequence-specific.

## Governing vocabulary

The following vocabulary is technical/logical application vocabulary. It does not create new Domain owners.

### Governed Operation Request

A structured request for a bounded effect under explicit target, context, purpose, state and governance assumptions.

### Effect semantics

The semantic change/result requested against the applicable owner/facet, expressed in a way that can be mapped back to accepted Domain/Logical meaning.

### Execution receipt / result

The technical record/result needed to determine what was accepted, attempted, committed, externally applied, rejected, conflicted, left pending or reconciled.

These constructs MAY be persistent where consequence/audit/recovery requires. Persistence does not make them Domain roots.

## Required contract fields by materiality

Where applicable, a Governed Operation Request MUST carry or be able to reconstruct the following.

### GOP-01 — Contract/version identity

The technical contract version/profile used to interpret the request MUST be identifiable where compatibility matters.

```text
contract version
!= Domain Version automatically
```

It exists to prevent old clients/queued work from silently executing under incompatible newer semantics.

### GOP-02 — Semantic target

The request MUST resolve to a bounded semantic target/facet according to the accepted reference/owner model.

Possible addressability may use:

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef where the operation is explicitly external/provider-scoped
other later accepted bounded reference variants
```

The contract MUST NOT fall back to a universal generic Entity/Thing target merely for API convenience.

### GOP-03 — Operation/effect family

The requested effect MUST be stated at semantic/application level strongly enough to distinguish materially different consequences.

Examples of effect meaning may include:

- revise a Schedule state;
- cancel a bounded planned expectation through the owning semantics;
- establish a Confirmation toward a specific target/material state;
- create/revise a Proposal;
- expose a bounded disclosure projection;
- create a Resource Allocation under the applicable contract;
- request provider-side creation/update through an Integration Hub action mode.

The effect vocabulary may be implemented as typed application contracts later; no universal Domain operation table is mandated.

### GOP-04 — Input / candidate state

The intended new values/candidate/parameters MUST remain distinct from the current target state and from derived/provider data used to calculate them.

```text
requested candidate
!= accepted target state
```

### GOP-05 — Purpose/context

Purpose and contextual scope MUST be explicit enough to apply relevant Authority, Consent, Visibility, privacy/minimization and specialist rules.

### GOP-06 — Material target state / expected state

Where stale execution could materially corrupt meaning, the operation MUST bind to an expected material state or semantically equivalent precondition under `WL-H05`.

```text
ETag / MVCC token / provider revision
MAY implement a check
BUT
!= MaterialStateRef by identity
```

Mismatch MUST produce conflict/re-read/reconcile/retry/user-resolution behavior rather than silent overwrite.

### GOP-07 — Derived/live input basis and freshness

Where the effect depends on LR-08 or live external state, the request/execution path MUST retain enough basis to revalidate or bind the consequential decision under `WL-H09`.

Examples:

```text
Effective Availability basis
candidate set basis
capacity snapshot
provider free/busy revision/time
Effective Authority/Visibility basis
solver input snapshot
```

A cache/index/embedding/tool result is not proof of current applicability.

### GOP-08 — Principal / Actor / represented party

Where applicable the contract MUST distinguish:

```text
technical Principal/security context
actual Actor
represented party
initiating Actor if distinct
```

```text
Principal != Actor
actual Actor != represented party automatically
```

Runtime Agent/service/job identity does not manufacture Domain Actor attribution.

### GOP-09 — Governance basis

Where consequence requires it, the operation MUST evaluate/reconstruct applicable governance such as:

- Authority;
- Consent;
- Visibility/disclosure boundary;
- Agreement/material terms basis;
- Representation/delegation basis;
- accepted policy/criterion/model version;
- purpose/context restrictions.

Technical `ALLOW` remains a technical result, not Domain Authority/Consent/Visibility by identity.

### GOP-10 — Autonomy / preview / confirmation requirement

The contract MUST determine whether the operation may execute directly, requires preview/confirmation, requires specialist/other-party action, or is not permitted.

This decision is consequence/governance/policy based.

```text
AI caller
!= always require confirmation

AI caller
!= permission to bypass confirmation
```

If a user/actor confirms a materially specific candidate, later material change to the candidate or relevant target state MUST NOT silently inherit that confirmation unless an accepted equivalence/policy rule permits it.

### GOP-11 — Idempotency semantics

Where duplicate request/effect is possible, the contract MUST define bounded idempotency semantics.

```text
same idempotency key + materially equivalent operation
→ replay/return prior result may be valid

same key + materially different operation
→ conflict/reject
```

Idempotency key is not semantic owner identity.

### GOP-12 — Correlation / causation

Where consequence/recovery/audit requires, the operation MUST preserve enough correlation to link:

```text
caller request
prior Proposal/Decision/Request where applicable
canonical mutation attempt
runtime execution
provider action
callback/acknowledgement
reconciliation/compensation
```

Correlation IDs remain technical references; they do not replace Provenance or native identity.

### GOP-13 — Execution class

The contract MAY classify required execution behavior independently from the implementation engine.

Current conceptual classes:

```text
IMMEDIATE
- completes within the bounded request/application transaction path

BOUNDED ASYNCHRONOUS
- durable enough for bounded background execution/retry/publication
- no material long-lived human/external wait required

DURABLE LONG-RUNNING
- material timers/waits/callbacks/human approval/recovery/reconciliation
```

Phase 7 guidance:

- bounded async may use DB/worker/outbox style infrastructure;
- dedicated durable execution is justified for material long-running classes;
- Restate is preferred dedicated candidate, Temporal the mandatory strongest challenger, and DBOS a conditional challenger whose PostgreSQL coupling depends on deployment topology;
- none is selected/implemented by this contract.

The execution class MUST NOT contain engine-specific semantic identity such as `TemporalWorkflow` or `RestateWorkflow` as the canonical operation meaning.

### GOP-14 — Deadline / expiry / delayed applicability

Where applicable, the request MUST define deadline/expiry/delay semantics distinct from runtime retry timing.

A queued operation surviving past its semantic validity MUST NOT execute merely because a worker/runtime can still run it.

### GOP-15 — Technical cancellation policy

The contract MUST distinguish:

```text
cancel technical execution
pause technical execution
stop future retries
request semantic reversal/cancellation
```

These are not equivalent.

Cancelling a workflow/job MUST NOT automatically change the Domain target unless an explicit governed effect performs the corresponding semantic transition.

## Result model — reject one universal success/status field

A single `success=true/false` or one universal operation status is insufficient for consequential LifeOS operations.

The result MAY need several independent axes.

### Axis A — request/admission result

Examples:

```text
accepted for evaluation/execution
rejected malformed/unsupported
rejected governance
confirmation required
conflict before execution
expired/stale before execution
```

### Axis B — canonical effect result

Examples:

```text
not attempted
committed/applied
no canonical mutation required
conflicted
failed before commit
partially established across owners
reconciliation required
```

Exact vocabulary remains operation-family specific.

### Axis C — external/provider effect result

Examples:

```text
not applicable
not attempted
pending
acknowledged
applied known
failed known
outcome unknown
partially applied
reconciliation/compensation required
```

### Axis D — runtime execution result

Examples:

```text
not scheduled
running/waiting
completed technically
cancelled technically
timed out technically
retrying
terminal runtime failure
```

Runtime result does not replace canonical/provider result.

### Axis E — user/domain response/result where semantically applicable

Examples may involve separate Domain families such as:

```text
Acknowledgement
Confirmation
Decision
Agreement
Consent
Participation response
Actual / Outcome
```

The technical result MUST NOT synthesize these merely from runtime completion.

## Representative non-collapse cases

### Request accepted but effect not complete

```text
request accepted
canonical state committed
provider application pending
```

Valid state. Do not report universal completion.

### Provider success but local follow-up uncertain

```text
provider effect succeeded
canonical follow-up failed/crashed
→ reconciliation required
```

Do not pretend the provider action rolled back.

### Timeout with unknown provider outcome

```text
external request timed out
→ outcome unknown
```

Do not map automatically to `failed` and retry destructively.

### Runtime completion without Domain realization

A workflow can complete because it delivered a request or finished monitoring. That does not establish that the user performed an Activity, attended an Event or achieved an Outcome.

### Technical cancellation without Domain cancellation

Stopping a queued provider sync may leave canonical state unchanged and provider state pending/divergent. Cancelling the runtime does not erase the original intention/history.

## Confirmation/material-version binding

Confirmation semantics remain Domain-owned.

Where a confirmation/preview is required for a proposed material effect:

```text
confirmation target
= materially specific candidate/effect + relevant target state/purpose/context
```

If the candidate or materially relevant target basis changes:

```text
prior confirmation
!= automatically applicable
```

unless an accepted policy defines the change as materially equivalent for that confirmation purpose.

This prevents stale preview acceptance from becoming blanket authority for a later different operation.

## Proposal / Decision / Request boundary

The contract MUST preserve actual semantic families where present.

```text
Proposal
= candidate put forward

Request
= directed ask

Decision
= bounded resolution

Governed Operation Request
= technical/application request to validate/execute a bounded effect
```

They may correlate but are not interchangeable.

A natural-language command may create a Proposal, a Request, a Decision input or a direct low-risk governed operation depending on actual semantics and autonomy/governance policy.

## AI/tool caller boundary

AI, MCP/A2A/future agent protocols and provider tools use the same governed operation boundary as UI/API callers.

```text
model output
!= operation authorization

tool call
!= accepted effect

protocol scope
!= Authority / Consent / Visibility
```

External/retrieved text MUST NOT expand Authority or bypass validation merely because it contains imperative instructions.

The AI Gateway/Context Builder may assemble a governed-effect request, but the deterministic application/effect boundary owns validation and execution eligibility.

Material AI/model/provider/prompt/tool changes that can affect consequential behavior are additionally subject to the current Phase 6 versioned/reproducible AI evaluation requirement before promotion.

## External/provider action boundary

For Integration Hub mode 5, the governed operation MUST remain distinguishable from provider-specific adapter requests.

Conceptual flow:

```text
Governed Operation Request
→ validated canonical/governance basis
→ adapter request
→ provider acknowledgement/result
→ canonical follow-up / reconciliation as applicable
```

Provider API operation names and request schemas remain adapter concerns.

## Multi-owner effect boundary

One governed operation may affect several semantic owners/facets.

If accepted invariants require all-or-nothing behavior, the future Physical/runtime implementation MUST supply the appropriate atomic boundary.

If global atomicity is impossible because external/distributed systems are involved:

```text
explicit staged/partial state
+ truthful provider/canonical result axes
+ reconciliation / compensation
```

No generic `Transaction` Domain root is introduced.

## Disclosure / non-interference result surface

Operation results, errors and previews are recipient-visible surfaces and therefore subject to `WL-H03`/`WL-H12`.

The implementation MUST prevent unauthorized inference through:

- target existence/nonexistence;
- different error codes/messages;
- counts/affected-item numbers;
- preview details;
- candidate alternatives;
- reason/explanation text;
- timing differences;
- provider/source details;
- hidden relationship/governance information.

A safe denial/error may intentionally reveal less than the internal diagnostic state.

## Error taxonomy principles

Technical errors must not be silently translated into false Domain semantics.

Examples:

```text
provider unavailable
!= requested fact false

AuthZ context unavailable
!= semantic proof of no Authority

solver timeout
!= infeasible

search index miss
!= canonical nonexistence

workflow timeout
!= Domain cancellation
```

The public/client error taxonomy is a later API design detail, but these distinctions are mandatory.

## Execution provenance / audit boundary

Where consequence requires, LifeOS MUST retain/reconstruct enough bounded evidence to answer as applicable:

```text
what was requested
which contract version interpreted it
who/what initiated it
which actual Actor / represented party applied
which target/material basis applied
which governance basis applied
which confirmation/autonomy rule applied
which idempotency/correlation context applied
which execution class/runtime handled it
what canonical effect occurred
what provider effect was attempted/resulted
what partial/conflict/reconciliation state remained
```

This execution/effect record does not require universal event sourcing and does not replace Domain Provenance by identity.

## Client/API evolution requirements

Concrete API design later MUST preserve:

- versioned compatibility for consequential semantics;
- explicit rejection/upgrade behavior for stale clients where newer governance/effect constraints cannot be safely honored;
- operation contracts stable enough that client/UI labels do not become ontology;
- separation between transport resource shape and semantic target/effect meaning;
- response/result semantics sufficient to represent partial/unknown/conflict state without lying.

## Open decisions / parameters

Phase 8 deliberately does NOT select:

```text
API style: REST / RPC / GraphQL / mixed
route layout
DTO serialization format
OpenAPI operation names
command bus library
effect dispatcher implementation
concrete operation registry representation
idempotency key header/body convention
correlation header convention
public error code vocabulary
confirmation UI/API choreography
execution-handle serialization
webhook/callback endpoint shape
AuthZ technical action vocabulary
runtime engine binding
```

These may be chosen only after preserving this contract.

Still-required operation-specific decisions include:

```text
which operation classes require expected-state binding
which require confirmation/preview
which may execute under reusable autonomy policy
which require atomic multi-owner commit
which may use staged/partial behavior
which require durable long-running execution
which permit cancellation and what cancellation means
which external actions support safe provider idempotency/inquiry
which result/provenance fields require durable retention
```

These are not universal defaults.

## Rejected shortcuts

Rejected as general LifeOS architecture:

```text
one universal Command Domain entity
one universal Operation Domain entity
one generic target_id without bounded semantic owner/facet
one success boolean
one universal workflow status replacing Domain state
route name = Authority action = semantic operation
provider 2xx = canonical completion
workflow completed = Actual
workflow cancelled = Domain cancellation
AI tool call = authorization
confirmation=true with no material target binding
retry any timeout blindly
latest result wins
```

## Downstream compatibility already established

The current Phase 9 search/observability/calendar/solver contract consumes this boundary. In particular:

- search result/action surfaces must not bypass governed operations;
- telemetry correlation must not become operation identity or Provenance by identity;
- calendar provider actions map through semantic target/effect + provider result axes;
- solver output remains candidate/proposal input until a governed operation establishes accepted state;
- `WL-H12` applies to search ranking/results/errors/previews/explanations.

Phase 10's benchmark method also carries the consequential consistency, recovery and state-separation pressure established here into later Physical evaluation.

## Phase 8 verdict

```text
PHASE 8 — GOVERNED API / COMMAND / EFFECT CONTRACT
PASS

DOMAIN REOPEN REQUIRED          0
LOGICAL REOPEN REQUIRED         0
NEW DOMAIN OWNER REQUIRED       0
CONCRETE API SELECTED           0
ROUTES/DTOs STABILIZED          0
COMMAND/EFFECT LIBRARY SELECTED 0
RUNTIME ENGINE SELECTED         0
BACKEND IMPLEMENTATION STARTED  0
```

This contract remains current downstream authority. It does not authorize concrete API/backend implementation.