# DANTE Intelligence — Model Target / Binding Closure Acceptance

Date: 2026-09-05  
Branch: `feature/ai-implementation`  
Status: **ACCEPTED / MATERIALIZED FOR DEVELOPMENT FOUNDATION**  
Production qualification: **NOT CLAIMED**  
Database/Alembic change: **NONE**

## Authority

This checkpoint accepts the decision set materialized in
`docs/workstreams/ai-runtime-model-target-closure-proposal-2026-09.md` after the direct Azure
GPT-4.1 baseline, Gemini 3.8 Flash challenger evaluation, oracle corrections and targeted
retests recorded in the workstream.

The proposal remains the detailed rationale/history. This acceptance record supersedes only its
`MATERIALIZED DECISION CANDIDATE` status; it does not rewrite the historical chronology.

## Accepted logical reasoning surface

DANTE keeps three peer reasoning paths:

```text
DETERMINISTIC COMPUTE
SOLVER
MODEL ACCESS
```

A Run may contain zero model invocations.

The initially active logical model targets are exactly:

```text
STRUCTURED_INTERPRETATION
GENERAL_REASONING
```

`DEEP_REASONING` exists as a dormant logical target with no binding. It is activated only from
integrated DANTE evidence, not because a premium model exists.

## Accepted development binding

The first development route is:

```text
STRUCTURED_INTERPRETATION -> Gemini 3.8 Flash
GENERAL_REASONING         -> Gemini 3.8 Flash
DEEP_REASONING            -> dormant
```

This is a development implementation decision, not permanent provider preference and not
production/private-data qualification.

The accepted Google binding uses the native Gemini Interactions API behind DANTE's
application-owned ModelAccess boundary. The OpenAI-compatible Gemini surface remains evaluation
history only and is not the canonical Google runtime protocol.

Initial harness policy:

```text
thinking/reasoning level = low
streaming                = off
background               = off
provider continuation    = off
provider-native tools    = off
provider storage         = off / store=false
fallback                 = off
DANTE retry              = off for foundation activation
```

The binding remains ineligible for private DANTE data until a separate privacy/security and
production binding qualification is complete.

## Binding decisions retained

The following are accepted without reopening:

- application/domain code never names a provider or provider SDK;
- `ModelTarget != ProviderBinding != model != deployment`;
- routing is deterministic, inspectable and content-minimizing;
- champion/challenger/fallback are route configuration, not application branches;
- one physical model may back multiple logical targets;
- fallback is independently qualified route recomposition, never blind provider-request replay;
- provider state/threads are never DANTE memory authority;
- provider output is never canonical truth or automatically publishable;
- reasoning/thought, cached, tool-use and total usage remain distinct evidence when exposed;
- provider IDs are attempt-level evidence, not DANTE semantic/idempotency identity;
- no second provider, local model, router LLM, agent framework or deep model is activated without a
  concrete trigger.

## Current implementation closure boundary

The foundation is considered materialized when the backend can execute:

```text
ModelInvocationRequest
  -> ModelAccessPort
  -> exact RouteConfig revision
  -> target route
  -> HarnessProfile
  -> ProviderBinding
  -> native ProviderAdapter
  -> normalized ProviderAttempt
  -> provider-independent structured-output validation
  -> normalized usage/error/result
  -> minimized runtime evidence
```

without the caller knowing that the development champion is Google.

The foundation does **not** require Ask DANTE, Timeline integration, product context assembly,
memory, native E04 query seams, capability/effect execution or any artificial vertical created only
to demonstrate an AI call.

## Stop / reopen rules

After deterministic regression and one synthetic native Gemini runtime smoke pass, broad prompt-only
model evaluation stops again.

Reopen model/provider selection only when there is evidence of a material need in quality,
reliability, latency, privacy/region posture, capability or effective cost per successful DANTE task.
