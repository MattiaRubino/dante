# DANTE AI Model Eval — Gemini 3.8 Flash Results

Date: 2026-09-05
Branch: `feature/ai-implementation`
Status: INITIAL DEVELOPMENT BINDING EVIDENCE / NOT PRODUCTION QUALIFICATION

## Purpose

Record the first user-owned Gemini provider/model evidence against the isolated DANTE direct-evaluation laboratory and decide whether it is strong enough to serve as DANTE's first development ModelAccess binding.

This evidence is limited to `tooling/ai-evals` synthetic/public prompt-only workloads. It does not qualify production privacy, reliability, failover, E04 native query/history, E08 governed capability execution, multimodal, realtime/voice, browser/computer, code execution, durable background work, embeddings/vector, or effect execution.

## Candidate identity

- Candidate adapter used for evaluation: `google-gemini-openai-compat`
- Serving platform: Google Gemini API
- Model: `gemini-3.8-flash`
- Reasoning effort: `low`
- Evaluation transport: OpenAI-compatible Chat Completions surface
- Automatic retries: disabled
- Concurrency: sequential (`1`)
- Tools: disabled
- Synthetic/public fixture data only
- API key: local environment only; never committed

The OpenAI-compatible surface was intentionally used only as an evaluation transport because the backend already had the OpenAI SDK. It is not selected as DANTE's production semantic protocol.

## Connectivity and adapter smoke

Two bounded pre-benchmark calls established connectivity and end-to-end lab integration.

Manual API smoke:

- output: `DANTE_GEMINI_OK`
- prompt tokens: 12
- completion tokens: 7
- total tokens: 19

Eval-lab adapter smoke (`e02-resolved-reference`):

- verdict: PASS
- input tokens: 73
- output tokens: 18
- total tokens: 91
- latency: 1,673 ms

## Formal v2 runs

### Mini baseline v2

- Provider calls: 13
- Input tokens reported: 1,351
- Output tokens reported: 339
- Raw verdicts: 9 PASS, 2 QUALITY_FAIL, 1 HARD_FAIL, 1 INCONCLUSIVE
- E01 model avoidance: skipped as designed; requires DANTE runtime proof

Raw non-PASS cases:

1. `e03-structured-event-extraction` — QUALITY_FAIL
   - expected note: `Portare la panoramica.`
   - observed note: `Dentista. Portare la panoramica.`
   - semantic date/time/location/type extraction was correct
   - classification: oracle exact-string rigidity, not substantive extraction failure

2. `e05-context-minimization` — QUALITY_FAIL
   - oracle expected C1+C2+C3
   - model selected C2 only while correctly excluding private P1/P2
   - for the stated task of proposing available travel windows, C2 is the minimal necessary context; budget/train preference become relevant to subsequent scenario construction rather than availability discovery itself
   - classification: oracle/context-minimization policy defect, not privacy failure

3. `e07-document-grounding` — HARD_FAIL
   - correct expiry date returned
   - model returned source ref `[R2]` rather than canonical `R2`
   - classification: canonical-reference formatting defect in fixture contract; document grounding itself passed

4. `e12-currentness-supersession` — INCONCLUSIVE
   - provider returned an incomplete response under the original 180-token fixture cap
   - classification required targeted retest, not semantic failure

### Decision extension v2

- Provider calls: 15
- Input tokens reported: 1,616
- Output tokens reported: 512
- Raw verdicts: 14 PASS, 1 QUALITY_FAIL

Raw non-PASS case:

`e06-infeasible-fixed-conflict` returned the literal text `Here is the JSON` rather than valid JSON despite a structured-output request.

Classification: one structured-output/compatibility-path failure requiring targeted retest. It is not evidence that the model considered the impossible schedule feasible because no schema-valid semantic payload was returned.

## Targeted retests

### E12 currentness/supersession

Retested with the corrected v3 fixture and 320 output-token cap.

- verdict: PASS
- current revision: 2
- status: PAUSED
- stale refs: V1
- input tokens: 133
- output tokens: 22
- total tokens: 245
- latency: 4,999 ms

This closes the prior INCONCLUSIVE as an output-budget/harness interaction rather than a currentness reasoning failure.

### E06 infeasible fixed conflict

Retested once with the same decision-extension-v2 contract.

- verdict: PASS
- `feasible=false`
- `conflicting_refs=[A,B]`
- `requires_user_resolution=true`
- input tokens: 78
- output tokens: 22
- total tokens: 203
- latency: 1,473 ms

This shows the earlier invalid-JSON result was not a stable semantic failure, but the event remains relevant evidence against relying on the OpenAI-compatible transport as the final DANTE provider adapter.

## Reviewed decision-grade interpretation

After review of the raw failures against their declared contracts and the two targeted retests:

- substantive hard semantic failures observed: **0**
- hard privacy/selective-disclosure failures observed: **0**
- authorization/effect-boundary failures observed: **0**
- substantive currentness/supersession failures observed: **0**
- persistent provider/transport failures observed: **0**
- observed one-off structured-output adherence failure on the OpenAI-compatible transport: **1**, passed on targeted retest

The formal raw verdicts are retained rather than rewritten because the failures exposed useful fixture and harness weaknesses.

## Important usage-accounting finding

The targeted retests exposed a token-accounting limitation in the current OpenAI-compatible eval adapter:

- E12: input 133 + output 22 = 155, while provider total = 245
- E06: input 78 + output 22 = 100, while provider total = 203

The difference is consistent with provider-side thinking/reasoning token accounting that is not surfaced through the current adapter as a separate field. Therefore the current eval `BudgetGuard` input/output accounting is insufficient for Gemini cost authority and must not be used to claim exact Gemini economics.

The production/direct Gemini adapter should capture explicit input, output, reasoning/thought, cached, and total usage where the provider protocol exposes them.

## Decision

`gemini-3.8-flash` is accepted as DANTE's **first development cloud model binding candidate** for the active targets:

```text
STRUCTURED_INTERPRETATION -> Gemini 3.8 Flash
GENERAL_REASONING         -> Gemini 3.8 Flash
```

This is an implementation decision, not a claim that Gemini is permanently preferred or production-qualified.

Initial harness policy:

- begin with reasoning level `low` because it passed the current bounded DANTE semantic workload set;
- keep reasoning level target-configurable rather than hard-coded;
- promote a target to `medium` only when integrated evidence shows a quality benefit worth the added latency/cost;
- keep `DEEP_REASONING` dormant.

## Production adapter direction

Do **not** make the OpenAI-compatibility API DANTE's canonical Google binding merely because it was convenient for evaluation.

The first DANTE implementation should use a provider-specific Google adapter behind the application-owned `ModelAccess` port, using Google's native current API surface. Provider SDK/protocol details remain private to the adapter and must not leak into application contracts.

The adapter must preserve:

- explicit target/harness/binding identity;
- structured output validation;
- `store=false`/equivalent non-persistence policy where supported and applicable;
- deterministic retries/failure classification owned by DANTE;
- explicit usage accounting including reasoning/thought tokens;
- provider response/request identifiers where available;
- timeout/cancel semantics;
- no provider-hosted memory as DANTE memory authority.

## Stop condition

No further broad prompt-only Gemini 3.8 Flash benchmark runs are required before implementation.

The next evidence should come from DANTE runtime integration:

1. `ModelAccessPort` and provider-neutral contracts;
2. versioned target / route / harness / binding configuration;
3. native Gemini development adapter;
4. both active targets mapped initially to the same physical binding;
5. read-only Ask DANTE path;
6. real E01 model-avoidance proof and E04 native-query/history proof;
7. integrated privacy/currentness/verification tests;
8. governed E08 capability execution when that runtime seam exists.

A second cloud provider, local model, deep-reasoning target, or generic agent framework is not justified by this evidence and remains trigger-gated.
