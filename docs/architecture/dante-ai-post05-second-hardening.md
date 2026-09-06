# DANTE AI — Post-AI-05 Second Hardening

- **Status:** FRESH BASELINE RETEST FAIL BOUNDED / POST05-H14..H18 REQUIRED
- **Branch:** `feature/ai-architecture`
- **Established:** 2026-09-02
- **PRE-SCOPE:** `02c32d7d69fc20fc589888bde1be920981326650`
- **Input baseline:** `docs/architecture/dante-ai-implementation-baseline.md`
- **Upstream:** AI-05 CLOSED / POST05-H01..H13 discovered
- **Implementation:** NONE
- **Provider/model/SDK selection:** OPEN
- **Database change:** NONE
- **Alembic change:** NONE
- **Domain/Logical/Physical/PostgreSQL reopen:** NONE

This document preserves the second independent attack on the first consolidated post-AI05 implementation baseline.

The baseline was deliberately treated as if authored by an independent team. The review did not infer correctness from the fact that the baseline had just been materialized.

Result:

```text
FRESH BASELINE RETEST
→ FAIL BOUNDED
→ POST05-H14..H18
```

The failures are implementation-contract/privacy/traceability hardenings. They do not require a new Domain owner, Logical root, Physical target, PostgreSQL table/index, Alembic migration, provider choice or framework.

---

# 1. POST05-H14 — reference-resolution non-interference

## Failure

The first consolidated baseline correctly restored `Reference / Target Resolution`, but did not state strongly enough that reference resolution itself is an observable disclosure surface.

Example:

```text
query: "show commitments with Marco"

eligible visible candidates:
Marco A

hidden/ineligible candidate:
Marco B
```

Unsafe resolver:

```text
query all candidates
→ discovers Marco A + hidden Marco B
→ returns AMBIGUOUS
```

The caller learns that another matching referent exists even though that referent is not eligible for disclosure.

Therefore:

```text
REFERENCE RESOLUTION
IS SUBJECT TO THE SAME ELIGIBLE-UNIVERSE / NON-INTERFERENCE RULE
AS SEARCH / PROJECTION.
```

## Binding hardening

A `ReferenceResolutionRequest` carries the current purpose/security/eligibility ceiling.

Candidate generation/resolution must operate over the eligible candidate universe before any externally observable:

```text
RESOLVED
AMBIGUOUS
NOT_FOUND
candidate count
candidate labels
clarification options
confidence/ranking clue
```

An ineligible candidate must not create externally visible ambiguity.

Where a hidden existence denial itself would leak information, the resolver returns the safe result appropriate to the eligible universe.

```text
AMBIGUOUS IN ALL DATA
!= AMBIGUOUS IN ELIGIBLE DATA.
```

Direct proof coverage for hidden-result non-interference applies to material reference-resolution families as well as Search/result families.

---

# 2. POST05-H15 — qualification traffic is real disclosure

## Failure

The first baseline separated:

```text
candidate admission
adapter conformance
live compatibility
direct DANTE eval
production qualification
```

but did not make the privacy consequence of live qualification traffic explicit enough.

A provider candidate that is not yet production-qualified is still an external data recipient if real payload crosses its boundary.

```text
"ONLY AN EVAL"
!= FREE DATA DISCLOSURE.
```

A provider route may be technically callable before DANTE has established that the candidate is eligible to receive private/sensitive DANTE data.

## Binding hardening

Before provider/data eligibility is established, qualification work uses:

```text
synthetic fixtures
public/non-sensitive fixtures
purpose-built minimized test payloads
provider-owned sample data
```

rather than production/private user context.

Live compatibility is split conceptually:

```text
PROTOCOL / FEATURE COMPATIBILITY
→ synthetic/minimized payload sufficient where possible

PRIVATE-DATA ELIGIBILITY PROOF
→ requires the applicable legal/security/privacy/processor/data-flow gate
```

Direct DANTE eval may use representative private-like synthetic fixtures before real-data eligibility. It does not need real production personal data to establish model quality or semantic behavior.

If a qualification case truly requires real sensitive/private data, that disclosure must already have an explicit legitimate purpose, data-recipient eligibility, applicable consent/legal basis and audit/evidence posture.

Shadow/canary traffic remains real disclosure and receives the same treatment.

---

# 3. POST05-H16 — lossless carry-forward of concrete runtime contracts

## Failure

The first consolidated baseline preserved the main semantic architecture but did not yet carry forward every implementation-grade contract previously frozen in AI-05B.

Missing or insufficiently explicit items included:

```text
provider/application error taxonomy
first HTTP outcome mapping posture
method-level Policy consumer seam
method-level Resource control seam
provider conformance fixture minimums
route/config artifact minimum schema
qualification artifact minimum schema
lifecycle semantics for original first-vertical objects
framework/dependency lock
```

A baseline cannot claim to remove patch algebra while forcing an implementer to return to the AI-05B candidate for these details.

## Binding hardening

The accepted implementation baseline must be lossless for still-valid build substance.

At minimum it carries forward:

### Application error taxonomy

```text
InvalidRequestError
StaleBasisError
PreconditionFailedError
CapabilityUnavailableError
PolicyDeniedError
ProviderTransientError
ProviderPermanentError
IndeterminateExternalOutcomeError
IsolationExecutionFailureError
CancellationError
DeadlineExceededError
```

### Provider adapter error taxonomy

```text
ProviderTransientError
ProviderPermanentError
ProviderRateLimitedError
ProviderTimeoutError
ProviderInvalidResponseError
ProviderDisconnectedError
IndeterminateExternalOutcomeError
CancellationError
DeadlineExceededError
```

### Policy consumer methods

```text
authorize_context_exposure(...)
authorize_model_egress(...)
authorize_effect(...)
authorize_publication(...)
```

### Resource consumer methods

```text
estimate(...)
admit(...)
settle(...)
```

### First HTTP mapping posture

```text
invalid request                 -> 400/422
stale basis / precondition      -> 409 when disclose-safe
policy denied                   -> 403 only when disclose-safe
capability unavailable          -> 503
provider transient/rate-limit   -> 503 or bounded mapped service error
provider permanent/bad gateway  -> 502
indeterminate external outcome  -> 502/503 without unsafe duplicate replay
deadline                        -> 504
```

Hidden existence remains filtered/empty where an error itself would disclose protected state.

### Dependency lock

Provider SDK imports remain confined to the admitted private binding adapter. No LangChain/LangGraph-style semantic ownership, generic provider gateway, vector/search database, model-to-SQL framework, generic Repository/UoW or MCP framework is introduced without an independent trigger.

---

# 4. POST05-H17 — attempted egress/exposure accounting survives provider failure

## Failure

The first baseline correctly said that `ContextManifest` records established exposure, but could still be implemented as if exposure exists only when the provider returns a successful/completed result.

That is false.

Example:

```text
DANTE sends ConsumerContext to provider
network/provider accepts bytes
response times out
```

DANTE may not know whether the provider completed inference, but it does know that the data egress boundary may have been crossed.

```text
PROVIDER ATTEMPT FAILED
!= DISCLOSURE DID NOT HAPPEN.
```

## Binding hardening

The request-local runtime keeps explicit egress/exposure state separate from provider completion state.

Conceptually:

```text
EgressAttempt
- recipient/provider binding
- purpose
- ConsumerContext projection identity
- disclosure/security basis
- dispatch state
- bytes/request handed to transport or equivalent send-boundary evidence
- acceptance certainty where knowable
- outcome state
```

`ContextManifest`/exposure evidence records actual or conservatively possible provider exposure at the material send boundary according to the adapter/protocol evidence available.

Provider completion/refusal/error remains separate.

A timeout after material send can therefore result in:

```text
provider outcome = UNKNOWN / FAILED
exposure occurrence = ESTABLISHED or POSSIBLE according to evidence
```

This runtime state is request-local in the first vertical. It does not create cross-Run durable prior-disclosure storage by itself.

---

# 5. POST05-H18 — retry/failover/hedging are cumulative-disclosure events

## Failure

Provider fallback had current eligibility/resource qualification, but the first baseline did not explicitly require cumulative-disclosure evaluation across multiple provider attempts inside the same Work.

Example:

```text
provider A receives minimized private context
A times out after possible acceptance
runtime falls back to provider B
B receives the same or expanded context
```

Even if A and B are individually eligible recipients, the combined disclosure may be broader than the policy intended.

```text
SAFE DISCLOSURE TO A
+
SAFE DISCLOSURE TO B
!= AUTOMATICALLY SAFE COMBINED DISCLOSURE.
```

## Binding hardening

Before every material provider retry/failover/new attempt, DANTE re-evaluates:

```text
current provider/data eligibility
current Work/purpose/currentness
current ConsumerContext needed by the alternate route
request-local prior egress/exposure occurrences
cumulative disclosure to known recipients/sinks
resource admission
retry/fallback qualification
```

A fallback with a different capability/context envelope rebuilds/minimizes ConsumerContext rather than blindly replaying the previous provider request.

Server-side fallback/hedging that can disclose data to multiple providers is OFF by default for the first route.

```text
MULTI-PROVIDER HEDGING
!= LATENCY-ONLY OPTIMIZATION.
```

It requires explicit qualification of privacy/security/cost/operational semantics before activation.

Provider refusal cannot trigger refusal-shopping.

A possibly accepted/processed attempt cannot be blindly replayed merely because a fallback provider exists.

---

# 6. Required fresh retest additions

The next full mega battery adds dedicated cases for:

```text
MKT-081 hidden same-name referent must not create observable ambiguity
MKT-082 resolver candidate labels/counts cannot leak ineligible referents
MKT-083 live provider compatibility before private-data eligibility uses synthetic/minimized fixture
MKT-084 shadow/canary evaluation is treated as real disclosure
MKT-085 provider timeout after send records exposure independently from completion
MKT-086 fallback after possible exposure reevaluates cumulative disclosure
MKT-087 alternate provider smaller/different context rebuilds ConsumerContext
MKT-088 multi-provider hedging remains disabled without explicit qualification
MKT-089 consolidated baseline includes application/provider error taxonomy
MKT-090 consolidated baseline includes concrete Policy/Resource/config/qualification/lifecycle/dependency contracts
```

The fresh pass must therefore execute:

```text
MKT-001..MKT-090
+ compound collision suite
+ reverse authority pass
+ representative product/simulation replay
```

No previous PASS label substitutes for this new run.

---

# 7. Verdict

```text
POST-AI05 SECOND HARDENING
→ FAIL BOUNDED
→ POST05-H14..H18 REQUIRED

Domain reopen       NO
Logical reopen      NO
Physical reopen     NO
PostgreSQL change   NO
Alembic change      NO
provider selected   NO
implementation      NO
```

Next:

```text
materialize consolidated baseline v2
→ rerun MKT-001..MKT-090 from zero
→ compounds
→ reverse authority pass
→ simulation replay
→ only then consider routing/implementation-entry closure
```
