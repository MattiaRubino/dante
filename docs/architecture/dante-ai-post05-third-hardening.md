# DANTE AI — Post-AI-05 Third Hardening

- **Status:** FRESH V2 MEGA RETEST FAIL BOUNDED / POST05-H19..H25 REQUIRED
- **Branch:** `feature/ai-architecture`
- **Established:** 2026-09-02
- **PRE-SCOPE:** `e48a92d1fd253b50af56a1f6bb4c48b6bb7731bd`
- **Input baseline:** `docs/architecture/dante-ai-implementation-baseline-v2.md`
- **Implementation:** NONE
- **Provider/model/SDK:** OPEN
- **Database/Alembic change:** NONE
- **Domain/Logical/Physical/PostgreSQL reopen:** NONE

The fresh MKT pass against baseline v2 found another bounded implementation-boundary cluster. None of the findings requires a new semantic owner or database shape. They close responsibilities already present in AI-02/03/04/PRE-AI05 but still not concrete enough in the implementation baseline.

Result:

```text
MKT-001..MKT-090 FRESH PASS
→ FAIL BOUNDED DURING ADVERSARIAL EXECUTION
→ POST05-H19..H25
```

---

# POST05-H19 — Search publication/currentness, cursor and navigation are not authorization

## Failure

Pure deterministic Search had correct query-time eligibility but could still be implemented as:

```text
query with eligible universe
→ build safe SearchResult
→ permissions/source state changes
→ return old SearchResult anyway
```

This weakens the accepted rule:

```text
RUN/REQUEST-START AUTHORIZATION != PERPETUAL AUTHORIZATION
```

The same issue exists for pagination cursors and navigation references.

A cursor or `SearchTargetRef` can preserve position/address semantics but cannot preserve authorization.

## Binding hardening

Search has an explicit response/publication boundary.

Before emitting material private Search data, revalidate current eligibility/currentness where the family/consequence profile requires it.

```text
SEARCH QUERY ELIGIBLE AT T1
!= AUTOMATICALLY PUBLISHABLE AT T2
```

A page cursor:

```text
!= AuthZ token
!= frozen permission snapshot
!= permission to reveal rows that became ineligible
```

Every paged request constructs a fresh current `SearchEligibilityEnvelope`. Cursor semantics are bound to family/query/sort/version enough to avoid corruption, but current access is independently re-evaluated.

If permission/source/currentness changes invalidate a cursor's safe semantics, DANTE may restart/rebase/fail the page safely rather than manufacture continuity.

A `SearchTargetRef` is an address/navigation hint only. Opening the canonical object performs current owning-capability authorization/visibility checks again.

```text
SEARCH RESULT ONCE VISIBLE
!= PERPETUAL NAVIGATION AUTHORITY
```

Source retirement/deletion between query and response is handled by the applicable currentness/revalidation contract; a stale result is not published as current.

---

# POST05-H20 — concrete ExecutionStatus and ResultMaturity vocabulary

## Failure

Baseline v2 referenced `ResultMaturity` and request execution state but did not freeze the already-accepted first-vertical vocabulary strongly enough.

An implementation could otherwise collapse provider completion, verification and publication into one boolean/status.

## Binding hardening

Request-local `ExecutionStatus` includes at least:

```text
ACCEPTED
RUNNING
COMPLETED
FAILED
CANCELLATION_REQUESTED
CANCELLED
SUPERSEDED
```

These are runtime execution states, not Domain Actual/Outcome.

First-vertical `ResultMaturity` includes at least:

```text
PROVISIONAL
VERIFIED
PUBLISHABLE
REJECTED
```

`PUBLISHABLE` requires the applicable verification/currentness/disclosure/publication checks; provider `completed` does not imply it.

```text
PROVIDER COMPLETED
!= VERIFIED
!= PUBLISHABLE
```

No first-vertical response is labelled stronger than its evidence.

---

# POST05-H21 — SemanticQueryGateway cannot become Intelligence-owned cross-capability SQL

## Failure

V2 correctly restored `SemanticQueryGateway`, but the phrase “bounded approved typed query handler” could be implemented as an Intelligence-private SQL adapter reading arbitrary business tables.

That would recreate the ownership bypass AI-05A explicitly rejected.

## Binding hardening

`SemanticQueryGateway` is orchestration, not persistence ownership.

Allowed implementations consume:

```text
owning capability public typed query contract
or
an explicitly accepted capability-owned read projection
```

Search's special cross-capability read projection remains Search/discovery-specific and is **not** a generic semantic analytics backdoor.

```text
INTELLIGENCE SEMANTIC QUERY
→ Search only when the InformationNeed is genuinely Search/discovery
→ owning capability query seam for canonical structured meaning
```

If no owning/public typed query seam exists yet:

```text
SemanticQueryOutcome = UNSUPPORTED / NOT_INTEGRATION_READY
```

not:

```text
Intelligence opens AsyncSession and queries tables itself
Search adapter is abused for arbitrary analytics
model writes SQL
```

This may delay a deterministic Ask family; it does not justify a parallel owner.

---

# POST05-H22 — every auxiliary model inference is first-class governed inference

## Failure

V2 allowed bounded model assistance for natural-language interpretation/reference resolution and mentioned possible future model verification, but did not explicitly force every such auxiliary inference through the same production model-access/governance path.

A hidden helper call could bypass provider/data/resource/eval/evidence controls.

## Binding hardening

Every model inference is a real governed inference/data recipient, including:

```text
NL intent interpreter
reference resolver helper
query rewrite/decomposition model
router model
reranker model
summarizer
verifier/judge
advisor/sub-inference
```

If activated, each call uses:

```text
WorkContract / bounded derived work meaning
Context/ConsumerContext appropriate to that exact consumer
current provider/data eligibility
ModelAccessPort / ModelAccessRuntime
RouteConfigIdentity
resource admission
EgressAttempt / exposure accounting
provider attempt evidence
applicable verification/eval qualification
```

No helper imports or calls a provider SDK directly.

```text
"ONLY A ROUTER / VERIFIER / REWRITE MODEL"
!= FREE PROVIDER CALL
```

The first implementation may keep these helper-model features OFF and use deterministic/application logic instead.

---

# POST05-H23 — evidence delivery failure and evidence minimization semantics

## Failure

V2 separated telemetry from audit but did not freeze the behavior when the operational evidence exporter fails, and did not explicitly prevent hidden-result/internal counts from entering ordinary telemetry.

## Binding hardening

Operational telemetry/export failure:

```text
!= canonical transaction failure automatically
!= permission to weaken safety/privacy
!= permission to expose raw context for debugging
```

For ordinary non-mandatory operational telemetry, exporter/backpressure failure is handled as an operational degradation/incident signal and must not silently mutate canonical truth or invent success/failure semantics.

Where a security/audit/effect evidence write is a mandatory precondition, that is a different evidence plane and may fail closed according to its owning contract.

Runtime telemetry remains minimized. Search evidence uses disclosed/eligible aggregate metadata only; it does not export hidden pre-filter candidate counts or protected row content.

Default telemetry excludes raw:

```text
private user request body
ConsumerContext
hidden Search candidates
model response
source content
credentials/secrets
```

A debug mode cannot silently override this production privacy boundary.

---

# POST05-H24 — retry budget controls SDK/gateway/application layering

## Failure

V2 owned application retry/fallback but did not explicitly constrain provider-SDK automatic retry behavior.

Without this rule:

```text
DANTE retry 2x
× SDK retry 3x
× gateway retry 2x
= hidden attempt multiplication
```

This breaks resource, disclosure, provider-attempt and ambiguous-outcome semantics.

## Binding hardening

DANTE owns the effective retry budget.

Provider adapter integration must either:

```text
disable SDK/gateway automatic retries
```

or

```text
make every material wire/provider attempt visible/accounted under DANTE attempt/evidence/resource/disclosure semantics
```

No hidden retry may cause uncounted provider data egress.

Every resource-consuming new attempt requires current admission according to WP-07.

Every data-egress new attempt creates/evaluates a corresponding egress exposure event.

A provider SDK retry after an indeterminate acceptance state is forbidden unless exact safe retry/idempotency semantics are proven.

---

# POST05-H25 — operational non-interference across routing, errors, latency and fallback

## Failure

Search non-interference was concrete, but AI-04 `WP-18` also requires operational behavior not to become a hidden-information oracle.

Example:

```text
hidden sensitive context exists
→ route becomes provider-ineligible
→ API returns a uniquely different error/latency pattern
→ caller infers hidden context existence
```

## Binding hardening

Where protected/withheld information influences internal route/policy decisions, externally observable behavior is reviewed for non-interference across:

```text
error class/message
fallback behavior
provider choice exposure
latency/timing class where material
counts/limits
resource behavior
retry behavior
```

Raw provider/security/policy errors do not flow directly to recipients when they reveal protected context/internal policy detail.

Safe external errors/limitations describe what the caller is allowed to know, not every internal reason.

The architecture does not claim perfect timing-channel elimination. It requires bounded threat-model-aware non-interference tests where the hidden state could create a practical oracle.

---

# Required fresh test extensions

Add:

```text
MKT-091 Search permission revoked after query before response
MKT-092 pagination cursor reused after AuthZ/source change
MKT-093 SearchTargetRef navigation after permission revocation
MKT-094 provider completed but VerificationResult rejected
MKT-095 SemanticQueryGateway has no owner seam and must return unsupported
MKT-096 Intelligence attempts direct SQL semantic query -> architecture failure
MKT-097 auxiliary NL interpreter/provider helper bypass attempt
MKT-098 telemetry exporter failure does not become canonical/safety bypass
MKT-099 SDK hidden retry multiplication / ambiguous acceptance
MKT-100 hidden sensitive state changes route/error and must not create practical oracle
```

Fresh acceptance becomes:

```text
MKT-001..MKT-100
+ compound collision suite
+ reverse authority pass
+ representative simulation replay
```

---

# Verdict

```text
POST-AI05 THIRD HARDENING
→ FAIL BOUNDED
→ POST05-H19..H25 REQUIRED

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
materialize baseline v3
→ rerun MKT-001..MKT-100 from zero
→ compound collision suite
→ reverse authority pass
→ simulation replay
→ only after clean PASS repair current routing and release I0 HOLD
```
