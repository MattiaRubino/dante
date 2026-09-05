# DANTE AI Model Eval — Azure GPT-4.1 Baseline Results

Date: 2026-09-04
Branch: `feature/ai-implementation`
Status: RECORDED BASELINE / NOT A PRODUCTION PROVIDER QUALIFICATION

## Purpose

Record the first real provider-backed DANTE model-quality baseline before broader provider/model screening.

This evidence is intentionally limited to the isolated `tooling/ai-evals` laboratory. It does **not** select Azure, OpenAI, GPT-4.1, or any other provider/model for production. It does **not** close C10 or replace the existing binding runtime/provider qualification process.

No private or production DANTE data was used. Fixtures were synthetic/minimized.

## Candidate identity available to the lab

- Candidate adapter: `azure-openai-responses`
- Azure resource endpoint: existing company-managed Azure OpenAI resource supplied locally
- Deployment name: `gpt-4.1-4`
- Model class: GPT-4.1-class Azure deployment
- API credentials: local environment only; never committed
- Retry policy: automatic retries disabled
- Concurrency: sequential (`1`)
- Tools: disabled
- Streaming/background: disabled
- Provider response storage request: disabled by the lab adapter

The exact Azure commercial SKU, model snapshot/version, and billing price were not available because the company Azure resource is access-restricted. Therefore no price-normalized conclusion is recorded here.

## Run 0 — connectivity smoke

Fixture: `e02-resolved-reference`

- Calls: 1
- Verdict: PASS
- Input tokens: 141
- Output tokens: 18
- Total tokens: 159
- Latency: 2,139 ms

This run established that the endpoint, deployment, Responses API path, structured output path, and deterministic grader could execute end-to-end.

## Run 1 — mini baseline

Suite: `dante-mini-baseline-v1`

- Selected fixtures: 14
- Provider calls: 13
- Model-avoidance fixtures: 1 (no provider call)
- Input tokens: 2,047
- Output tokens: 271
- Total tokens: 2,318
- Raw verdict counts: 11 PASS, 2 QUALITY_FAIL
- Provider/infra failures: 0
- Raw suite overall: FAIL because any quality failure makes the runner summary non-pass

### Run 1 mismatches

#### E11 — `e11-declared-vs-observed`

Hard invariant passed:

- `update_memory = false`

Quality expectation mismatch:

- expected `action = ask_confirmation`
- observed `action = keep_declared`

Interpretation: this is not evidence of a semantic or safety failure. Keeping the explicit declared preference unchanged is compatible with the fixture's hard rule that a short observed series must not permanently overwrite declared memory. The fixture/oracle is too prescriptive if it treats asking for confirmation as the only acceptable next action.

Classification for decision use: **oracle/quality-policy ambiguity; not a hard model failure**.

#### E12 — `e12-currentness-supersession`

Hard invariants passed:

- `current_revision = 2`
- `status = PAUSED`

Quality expectation mismatch:

- expected stale reference `V1`
- observed stale reference `V1 revision=1`

Interpretation: currentness and supersession reasoning were correct. The mismatch is canonical-reference formatting, not selection of the wrong revision.

Classification for decision use: **canonical-format quality mismatch; currentness reasoning passed**.

## Run 2 — decision extension

Suite: `dante-decision-extension-v1`

- Selected fixtures: 15
- Provider calls: 15
- Input tokens: 2,572
- Output tokens: 350
- Total tokens: 2,922
- Raw verdict counts: 14 PASS, 1 HARD_FAIL
- Provider/infra failures: 0
- Raw suite overall: FAIL because of the single hard assertion mismatch

The run covered harder cases across typed reference resolution, uncertainty-preserving extraction, provenance conflicts, selective disclosure, capacity/deadline planning, infeasible schedules, replanning without rewriting history, scenario trade-offs, document grounding, authorization-vs-execution truth, delegation scope, learning/memory conflict, currentness, conflicting equal-authority evidence, and material proactive changes.

### Run 2 mismatch

#### E07 — `e07-invoice-document-grounding`

The model selected the correct final approved invoice data and correct calendar date, but emitted the date in the source-document format:

- expected `due_date = 2026-09-18`
- observed `due_date = 18/09/2026`

The fixture schema declared `due_date` only as a generic string and did not require ISO-8601 formatting. Therefore the grader's hard equality expectation is stricter than the declared response contract.

Classification for decision use: **fixture/normalization defect; document grounding itself passed**.

The local raw report was written to:

`tooling/ai-evals/reports/gpt41-decision-v1.json`

The reports directory is intentionally gitignored, so this checkpoint document is the durable repository record.

## Aggregate evidence

### Formal benchmark runs only (Run 1 + Run 2)

- Provider calls: 28
- Input tokens: 4,619
- Output tokens: 621
- Total tokens: 5,240
- Raw verdicts: 25 PASS, 2 QUALITY_FAIL, 1 HARD_FAIL
- Provider/infra failures: 0

### Actual API traffic in this evaluation session including Run 0 smoke

- Provider calls: 29
- Input tokens: 4,760
- Output tokens: 639
- Total tokens: 5,399

This distinction is deliberate: the smoke call is real API usage but is not counted as a separate benchmark fixture in the two formal suite summaries.

## Decision interpretation

After reviewing the three raw mismatches against their declared fixture contracts:

- substantive hard semantic failures observed: **0**
- hard privacy/selective-disclosure failures observed: **0**
- hard authorization/effect-boundary failures observed: **0**
- substantive currentness/supersession failures observed: **0**
- provider/transport failures observed: **0**

The three non-PASS raw verdicts are retained above rather than rewritten away. They matter because they exposed weaknesses in the evaluation oracle/normalization rules.

The supported conclusion is therefore narrow:

> This GPT-4.1 Azure deployment is a strong initial baseline for the bounded, structured, prompt-only DANTE workloads exercised here.

Unsupported conclusions include:

- GPT-4.1 is DANTE's final or preferred production model.
- Azure is DANTE's final or preferred production provider.
- The candidate is qualified for all DANTE workloads.
- Tool use, native DANTE query/history semantics, multimodal, realtime/voice, browser/computer, code execution, durable background work, embeddings/vector, long-horizon agent behavior, or integrated runtime effects have been qualified.
- Cost economics have been established.

## Stop condition for this candidate

No additional prompt-only Azure GPT-4.1 calls are required for the initial model-selection stage.

Further calls against the same isolated harness would mostly add repetition, while important remaining evidence requires different surfaces:

- E04 native query/history/absence semantics requires real DANTE application/query seams.
- E08 capability/tool use requires actual governed capability/tool execution and outcome evidence.
- Multimodal, voice/realtime, browser/computer, code execution, durable background work, embeddings/vector, and other trigger-gated capabilities require their own applicable harnesses.
- Reliability/failover/provider qualification belongs to the binding/runtime qualification path rather than this prompt-only model-quality probe.

Accordingly, the next step is **market/provider/model screening using this GPT-4.1 result as the baseline**, followed by testing only a small number of materially different challengers. Do not spend additional calls on this company-managed Azure deployment merely to increase sample count.
