# DANTE AI-05B — Fresh Retest Failure + Second Bounded Hardening

- **Status:** FRESH RETEST FAIL BOUNDED / AI05B-H08..H12 MATERIALIZED / FULL RETEST REQUIRED
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-05 — Whole-System Acceptance + Implementation Blueprint
- **Sub-phase:** AI-05B — Concrete Implementation Blueprint
- **Established:** 2026-09-02
- **Initial candidate:** `docs/architecture/dante-ai-05b-concrete-implementation-blueprint.md`
- **First hardening:** `docs/architecture/dante-ai-05b-first-destructive-hardening.md`
- **Fresh-retest PRE-SCOPE:** `b5df0aeb0aa305041118b37c76299e932fd49e21`
- **Result:** FAIL BOUNDED
- **Architecture reopen:** NONE
- **Database/Alembic change:** NONE
- **Provider/model/SDK selection:** NONE
- **Runtime implementation:** NONE

This document preserves failures found by a fresh review of the original candidate plus `AI05B-H01..H07`. It does not rewrite earlier FAIL evidence into PASS.

The second review attacks contract ownership and trust boundaries that remained implementable in more than one materially different — and potentially unsafe — way.

---

# 1. Fresh-retest failure set

```text
AI05B-H08  Intelligence must consume the single Search-owned public contract;
           no shadow SearchAccessPort owned by Intelligence.

AI05B-H09  ProviderAdapter requires a concrete private protocol and
           conformance surface distinct from ModelAccessPort.

AI05B-H10  READ_ONLY / NO_EFFECT must be enforced by an actual Effect boundary,
           not inferred from control-flow convention.

AI05B-H11  operational evidence needs a typed RuntimeEvidencePort contract;
           no scattered logger/telemetry semantics.

AI05B-H12  untrusted HTTP DTOs must not carry authority-bearing fields;
           server-owned trusted application context is built after authentication.
```

No new persistence or infrastructure is required.

---

# 2. Updated destructive cases

The fresh pass changes these dispositions:

```text
B05-02  Search/Intelligence public/private dependency direction
→ FAIL BOUNDED / H08

B05-18  provider SDK confinement
→ PASS boundary, but provider adapter build contract incomplete

B05-20  first vertical explicit NO_EFFECT
→ FAIL BOUNDED / H10

B05-26  telemetry/evidence N/A vs missing
→ PASS semantics, but port/DTO ownership incomplete / H11

B05-30  architecture imports
→ PASS only after H08 removes the duplicate Search consumer contract
```

New cases:

```text
B05-40 one Search public semantic contract only
→ FAIL BOUNDED / H08

B05-41 ModelAccessPort != ProviderAdapter and adapter protocol is executable
→ FAIL BOUNDED / H09

B05-42 model/provider output cannot bypass explicit read-only Effect boundary
→ FAIL BOUNDED / H10

B05-43 runtime evidence cannot devolve into untyped logging/full-content export
→ FAIL BOUNDED / H11

B05-44 client-controlled HTTP body cannot forge principal/purpose/policy/route/provider/effect authority
→ FAIL BOUNDED / H12
```

Reverse acceptance remains HOLD until the entire battery is rerun with both hardening layers.

---

# 3. AI05B-H08 — single Search-owned public contract

## 3.1 Failure

AI-05A explicitly binds:

```text
Ask DANTE
→ modules/intelligence
→ modules/search PUBLIC QUERY SURFACE
```

The initial target skeleton also proposed:

```text
modules/intelligence/ports/search_access.py
```

If that file defines an Intelligence-owned duplicate of Search semantics, two contracts can drift:

```text
Search public meaning A
!=
Intelligence shadow Search meaning B
```

That violates the ownership boundary even if both happen to look identical initially.

## 3.2 Hardening

The stable Search request/result/guarantee/family contracts are owned once by:

```text
modules/search/public.py
modules/search/contracts.py
```

Intelligence imports only those public Search contracts/protocols.

Correct dependency:

```text
modules/intelligence/application/retrieval.py
        ↓
modules/search/public.py
```

Remove from the target skeleton:

```text
modules/intelligence/ports/search_access.py
```

unless a future adapter has a materially different responsibility that does **not** duplicate Search semantics and is explicitly justified.

For testing, Intelligence uses a fake implementation of the **Search-owned public protocol**, not a second Intelligence-owned protocol.

Binding:

```text
TESTABILITY DOES NOT JUSTIFY DUPLICATING CONTRACT OWNERSHIP.
```

Search remains independently usable without Intelligence.

---

# 4. AI05B-H09 — concrete ProviderAdapter protocol

## 4.1 Failure

`ModelAccessPort` is the application-owned seam used by Intelligence. It is not the provider adapter itself.

The initial candidate specified provider fixture cases but did not freeze the private adapter protocol precisely enough to prevent routing/policy/provider semantics from leaking into an SDK adapter.

## 4.2 Ownership split

```text
Intelligence application
        ↓
ModelAccessPort                 DANTE application contract
        ↓
ModelAccessRuntime              route/attempt supervision
        ↓
ProviderAdapter                 private provider protocol contract
        ↓
provider SDK / HTTP protocol
```

Binding:

```text
MODEL ACCESS PORT != PROVIDER ADAPTER
PROVIDER ADAPTER != ROUTING POLICY
PROVIDER ADAPTER != EGRESS AUTHORITY
PROVIDER ADAPTER != EFFECT AUTHORITY
```

## 4.3 ProviderAttemptRequest

Before adapter dispatch the ModelAccessRuntime has already resolved the eligible concrete binding and allocated the DANTE technical attempt identity.

Minimum private request semantics:

```text
ProviderAttemptRequest
    attempt_id: ProviderAttemptId
    provider_binding_id
    concrete model/deployment locator owned by selected binding
    feature_mode
    normalized provider-neutral input projection
    structured-output projection when requested
    capability/tool transport projection when requested
    deadline
    request-local cancellation signal/handle
    exact route/config material identity
    harness/profile identity
```

First vertical:

```text
capability/tool projection = EMPTY
provider background mode   = OFF
stored/continuation mode    = OFF unless separately qualified
```

The adapter does not receive raw `AsyncSession`, canonical DB mutation authority or unfiltered application context.

## 4.4 ProviderAdapter methods

Concrete private protocol:

```text
ProviderAdapter.invoke(
    ProviderAttemptRequest
) -> ProviderAttemptResult

ProviderAdapter.stream(
    ProviderAttemptRequest
) -> AsyncIterator[ProviderRuntimeEvent]
```

Cancellation is observed through the request-owned cancellation mechanism; the adapter maps a cancellation request to provider-specific mechanics where supported.

If a selected provider protocol requires an explicit active-call handle, that handle remains private adapter/runtime state and never becomes an application contract.

## 4.5 ProviderAttemptResult

Minimum normalized result semantics:

```text
attempt_id
provider outcome class
normalized finalized output when available
provider correlation IDs as evidence only
finish/stop/refusal class
acceptance-known / acceptance-unknown evidence
cancellation requested/confirmed/quiesced evidence where available
usage evidence + evidence quality
provider capability/feature usage evidence
started_at / completed_at / latency evidence
classified provider error when unsuccessful
```

Provider-specific raw payloads are not promoted into ordinary DANTE application contracts.

## 4.6 ProviderRuntimeEvent

Streaming normalization may represent typed event families such as:

```text
attempt_started
output_delta
structured_output_final
usage_update
refusal
attempt_completed
attempt_failed
cancellation_observed
```

Raw provider event IDs may be carried as evidence/correlation only.

```text
RAW PROVIDER EVENT != PROVIDER RUNTIME EVENT != PUBLICATION EVENT
```

## 4.7 Conformance contract

Every selected adapter implementation must pass the same provider-adapter conformance suite for the feature modes it claims to support.

Mandatory controlled cases:

```text
normal finalized response
rate limit
pre-acceptance connection failure
timeout before acceptance known
timeout after acceptance possible / ambiguous submit
invalid structured response
stream disconnect
request cancellation before dispatch
request cancellation in flight
cancellation requested but completion races/arrives
usage present
usage absent
unsupported requested feature
provider refusal
```

The suite proves normalization behavior, not model quality.

Distinct evidence remains:

```text
adapter conformance
!= live compatibility smoke
!= DANTE direct eval
!= capacity qualification
```

---

# 5. AI05B-H10 — explicit read-only Effect boundary

## 5.1 Failure

The initial candidate correctly said:

```text
ConsequenceProfile = READ_ONLY
EffectDisposition = NO_EFFECT
```

but an implementation could satisfy that text by simply never calling an Effect component, leaving model/tool/application code free to accidentally dispatch a mutation elsewhere.

The first vertical must prove the **boundary**, not only the intended behavior.

## 5.2 Hardening

Materialize an application-owned Effect consumer contract:

```text
EffectBoundary.finalize(
    WorkContract,
    proposed_effects,
    current_policy_basis
) -> EffectOutcome
```

First-vertical invariant:

```text
WorkContract.ConsequenceProfile == READ_ONLY
AND proposed_effects is empty
→ EffectOutcome.NO_EFFECT
```

If any effect/capability mutation intent reaches the boundary under the first-vertical envelope:

```text
→ REJECT
→ no mutation adapter invoked
→ no canonical transaction opened for mutation
→ safe internal evidence emitted
```

The first vertical therefore has an **explicit no-op outcome through the Effect boundary**, not an absent boundary.

## 5.3 Future consequence path

Later consequential work may extend the same responsibility with:

```text
validated EffectIntent
→ target/current-state resolution
→ policy/approval
→ owning application use case
→ outer transaction
→ persistence adapters may flush, not independently commit
→ EffectOutcome
→ reconciliation when external outcome is uncertain
```

Provider/model code never gains direct canonical mutation authority.

---

# 6. AI05B-H11 — typed RuntimeEvidencePort

## 6.1 Failure

The candidate listed a future `telemetry.py` port and strong evidence fields but did not define an ownership contract. That leaves a possible implementation where every module logs arbitrary dictionaries or raw prompts independently.

## 6.2 Hardening

Rename the application concept to emphasize evidence rather than a vendor telemetry API:

```text
RuntimeEvidencePort
```

Candidate path:

```text
modules/intelligence/ports/runtime_evidence.py
```

The port accepts a closed/typed union of DANTE runtime evidence events for the currently implemented vertical.

Conceptual operation:

```text
RuntimeEvidencePort.emit(RuntimeEvidenceEvent) -> None
```

The concrete observability adapter may later map these typed events to the project observability stack.

## 6.3 Event families

At minimum first-vertical typed event families cover:

```text
WorkLifecycleEvidence
SearchEvidence
ContextReadinessEvidence
BasisRevalidationEvidence
PolicyBoundaryEvidence
RouteDecisionEvidence
ResourceEvidence
ProviderAttemptEvidence
VerificationEvidence
EffectBoundaryEvidence
PublicationEvidence
```

Common safe envelope:

```text
event type/schema version
observed_at
work_id / run-local correlation where present
release/build identity
RouteConfigIdentity where applicable
stage/outcome classification
```

Event-specific types add only fields required by their evidence contract.

## 6.4 Content minimization

Default typed evidence must not contain:

```text
raw user question when not required
raw Search result body/snippet content
raw ConsumerContext
raw prompt
raw model response
secrets
provider credentials
hidden-result counts before eligibility filtering
```

When qualification/debug evidence needs protected content, that is an explicit separate evidence mode with purpose, access and retention — not a hidden field in ordinary telemetry.

## 6.5 Failure semantics

For the first read-only vertical, ordinary operational telemetry delivery is not canonical application success authority.

```text
telemetry exporter unavailable
!= automatically fabricate success evidence
!= automatically widen safety
```

Required qualification runs must prove the evidence needed for qualification was actually collected. A missing required evidence event makes the qualification artifact incomplete.

Future consequential audit evidence remains a distinct stronger plane and may have fail-closed obligations not owned by this operational port.

---

# 7. AI05B-H12 — untrusted HTTP DTO vs trusted application context

## 7.1 Failure

The candidate listed fields such as purpose, resolved access context and route/config semantics in internal request contracts but did not explicitly prevent those fields from entering through the public HTTP body.

Unsafe shape:

```text
client JSON
{
  "query": "...",
  "principal": "someone-else",
  "purpose": "admin",
  "provider": "...",
  "consequence_profile": "..."
}
```

A strict Pydantic model is not an authorization system.

## 7.2 Trust split

Freeze three separate layers:

```text
UNTRUSTED HTTP INPUT DTO
        ↓ authentication + route-owned purpose/surface resolution
TRUSTED RequestContext / SearchEligibilityEnvelope / WorkContract
        ↓
INTERNAL APPLICATION REQUEST
```

The client never directly supplies server-authoritative security/routing/effect fields.

## 7.3 Search HTTP DTO

Candidate untrusted shape:

```text
SearchHttpRequest
    query
    optional user-facing filters
    optional requested Search family/type hints
    current/history intent when product allows
    pagination/cursor request
```

Explicitly absent from client body:

```text
principal
represented party authority
SearchEligibilityEnvelope
Authority/AuthZ basis
purpose escalation
recipient/surface authority
raw table/model name
SQL/ORM expression
provider/model/route
Effect authorization
```

Server constructs:

```text
SearchExecutionRequest
    user query/filter projection
    trusted SearchEligibilityEnvelope
    route-owned purpose/surface
    bounded page/guarantee contract
```

Requested family/filter hints are intersected with the eligibility envelope and active family registry; they never widen either.

## 7.4 Ask HTTP DTO

Candidate untrusted shape:

```text
AskHttpRequest
    question
    optional user-facing scope/filter hints
```

Explicitly absent from client authority:

```text
ModelTarget
ProviderBinding
provider/model name
HarnessProfile
RouteConfigIdentity override
principal/Authority/AuthZ basis
ConsumerContext
PolicyDecision
ConsequenceProfile upgrade
Effect authorization
resource/commercial entitlement
```

Server constructs the trusted `WorkContract`, policy context, ContextPlan and route inputs.

## 7.5 Responses

Public response DTOs remain recipient-safe projections.

`SearchHttpResponse` may expose:

```text
safe hits
safe facets/counts only after eligibility-safe computation
pagination
result guarantee/limitations where product-safe
```

`AskHttpResponse` may expose:

```text
work correlation safe for client
verified/publishable answer
safe sources/provenance
safe currentness/limitation information
model-assisted boolean where desired by product contract
```

Never expose merely because internally available:

```text
raw prompt/context
hidden Search universe information
policy internals
provider secret/config
provider raw IDs unless product needs them
internal cost/budget details
private telemetry
```

## 7.6 Validation layer rule

Pydantic boundary validation establishes structure only.

```text
VALID JSON / VALID PYDANTIC
!= AUTHORIZED REQUEST
!= ELIGIBLE SEARCH
!= ROUTABLE MODEL CALL
!= AUTHORIZED EFFECT
```

---

# 8. Corrected target skeleton deltas

Apply these deltas when reading the original candidate:

```text
REMOVE
apps/backend/src/dante/modules/intelligence/ports/search_access.py

RENAME / MATERIALIZE
apps/backend/src/dante/modules/intelligence/ports/telemetry.py
→ apps/backend/src/dante/modules/intelligence/ports/runtime_evidence.py

KEEP
apps/backend/src/dante/modules/search/public.py
→ sole owner of Search public application/query contract

KEEP
apps/backend/src/dante/modules/intelligence/ports/model_access.py
→ application ModelAccessPort only

ADD CONTRACT DETAIL
apps/backend/src/dante/modules/intelligence/contracts/provider.py
→ ProviderAttemptId / ProviderAttemptRequest / ProviderAttemptResult / ProviderRuntimeEvent

KEEP PRIVATE PROVIDER IMPLEMENTATION
apps/backend/src/dante/modules/intelligence/adapters/outbound/models/<provider>.py
→ implements private ProviderAdapter protocol after selection gate

KEEP / STRENGTHEN
apps/backend/src/dante/modules/intelligence/ports/effect.py
→ explicit EffectBoundary including first-vertical NO_EFFECT enforcement
```

No actual file is created by AI-05B documentation work.

---

# 9. Updated architecture-test obligations

Implementation architecture tests must additionally prove:

```text
Intelligence imports Search only through modules.search public/contracts surface
no Intelligence-owned duplicate Search DTO/protocol
Search does not import Intelligence
provider SDK import exists only inside selected private provider adapter package
ProviderAdapter cannot import HTTP inbound schemas
ProviderAdapter cannot import database runtime/mappings
HTTP DTO modules cannot construct/accept caller-supplied Authority/AuthZ/RouteConfig/ProviderBinding authority fields
production application does not emit arbitrary untyped dicts through RuntimeEvidencePort
read-only Ask cannot reach mutation adapter without failing EffectBoundary
```

---

# 10. Updated full retest battery

The next pass is not a targeted H08..H12 retest. It must restart from zero against:

```text
original AI-05B candidate
+ AI05B-H01..H07
+ AI05B-H08..H12
+ current branch truth
```

Required cases now:

```text
B05-01..B05-44
+ all prior compound collision cases
+ new compounds:

client family hint + hidden family + count/facet computation
client attempts provider override + route config rollout
client disconnect + provider cancellation race + unknown usage
provider SDK adapter conformance + direct eval same-composition proof
model emits command-like output + READ_ONLY EffectBoundary
telemetry exporter outage + required qualification evidence
```

Then:

```text
reverse AI-05B
→ AI-05A
→ AI-04
→ PRE-AI05
→ AI-03
→ AI-02
→ Product Global Search/North Star constraints where touched
```

Only a clean fresh pass may create AI-05B acceptance/closure authority.

---

# 11. Explicit non-claims

```text
first candidate                              MATERIALIZED
first destructive pass                       FAIL BOUNDED
AI05B-H01..H07                               MATERIALIZED
fresh retest after first hardening            FAIL BOUNDED
AI05B-H08..H12                               MATERIALIZED
full fresh retest after H08..H12              NOT YET RUN
AI-05B accepted                               NO
whole AI-05 closed                            NO
implementation                               NONE
provider/model/SDK                            OPEN
new database/Alembic                          NONE
```

---

# 12. Exact next action

```text
fresh B05-01..B05-44 from zero
→ compounds from zero
→ reverse consistency
→ if PASS, materialize AI-05B acceptance authority
→ if FAIL, preserve failure and harden only the demonstrated gap
```
