# DANTE AI Eval Lab

Status: **evaluation tooling / non-production**

This directory is DANTE's isolated direct-evaluation laboratory. It exists to compare model/provider candidates against DANTE workloads and to exercise production-shaped ModelAccess paths without making benchmark code a product/runtime authority.

## Authority and non-claims

The semantic authority remains the accepted DANTE direct-evaluation architecture (`DANTE-E01..DANTE-E14`). This tooling is only an executable runner/fixture surface.

This directory does **not**:

- select or promote a production provider;
- make Google, Gemini, Azure, OpenAI, GPT-4.1, or any other model timeless/canonical;
- authorize private/production data egress;
- prove production qualification;
- alter PostgreSQL/Alembic;
- replace DANTE runtime, Auth/AuthZ, verification, publication, effects, or audit.

`MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT` remains binding.

## Current development candidate

The current development champion evidence path is:

```text
Google Gemini Developer API
native Interactions API v1beta
gemini-3.8-flash
reasoning = low
route = gemini-flash-dev-v2
binding = google-gemini-interactions-flash-v2
harness = gemini-flash-low-v1
```

The production-shaped eval candidate is:

```text
google-gemini-native-modelaccess
```

Unlike the historical compatibility candidate, it executes through the actual DANTE development composition:

```text
EvalFixture
  -> ModelInvocationRequest
  -> ModelAccessRuntime
  -> immutable route config
  -> native Gemini Interactions adapter/HTTP transport
  -> DANTE normalization + structured-output validation
  -> CandidateResult
```

Accepted local secret names:

```text
DANTE_GEMINI_API_KEY
DANTE_EVAL_GEMINI_API_KEY
```

Secrets are never printed and must never be committed.

The historical candidates remain available for comparison/evidence preservation:

```text
azure-openai-responses
google-gemini-openai-compat
```

The OpenAI-compatible Gemini adapter is evaluation-only and is not the default production-shaped binding.

## Cost / blast-radius guardrails

Paid execution is fail-closed by default:

- command default is **dry-run**;
- `--execute` is required for any provider call;
- hard global cap is 30 calls;
- per-call output hard cap is 512 tokens in direct-eval fixtures;
- per-fixture input + instructions hard cap is 16,000 characters;
- provider SDK/runtime automatic retries are disabled for qualification;
- calls are sequential;
- `store=false`;
- streaming, background mode, continuation, and provider-native tools are disabled;
- only synthetic/public fixture data is allowed.

For priced execution, provide both token prices and optionally a maximum euro budget. The budget guard uses a conservative pre-dispatch input estimate and actual provider usage after each call. It is a safety guardrail, **not** a cloud billing authority.

Execution without prices is blocked unless `--allow-unpriced` is explicitly supplied.

## Current suite lineage

Fixture history is versioned rather than overwritten.

Mini qualification lineage:

```text
mini-baseline-v1 / v2          historical baselines
mini-baseline-v3               corrected semantic fixture set
mini-baseline-v4               native headroom/oracle delta
mini-baseline-v5               bounded E11 headroom delta
```

The final native development qualification reuses unchanged PASS evidence across the versioned deltas and reaches:

```text
13 / 13 model fixtures semantic PASS
E01 model avoidance = intentionally no provider call
```

Decision qualification lineage:

```text
decision-extension-v1 / v2     historical/corrected decision set
decision-extension-v3          native headroom delta for 8 incomplete cases
decision-extension-v4          corrected E10 delegation oracle
```

Final native development qualification:

```text
15 / 15 model fixtures semantic PASS
```

The durable result checkpoint is:

```text
docs/workstreams/ai-model-eval-gemini-native-modelaccess-results-2026-09-05.md
```

E04 and real E08 are intentionally not faked into model-only suites: native owner history/absence and real capability/tool use require their relevant DANTE/application surfaces.

The same principle applies to multimodal, voice/realtime, browser/computer use, code execution, durable background work, and embedding/vector suites: add them only when the real trigger/capability surface exists.

## Dry-run first

From the repository root, a current native dry-run example is:

```bash
uv run --locked --project apps/backend \
  python tooling/ai-evals/run_dante_eval.py \
  --candidate google-gemini-native-modelaccess \
  --suite tooling/ai-evals/fixtures/decision-extension-v4.json \
  --only e10-delegation-scope \
  --max-calls 1
```

This performs **zero provider calls** and prints the bounded execution plan.

## Paid execution

Paid execution must always be explicit. Example syntax:

```bash
uv run --locked --project apps/backend \
  python tooling/ai-evals/run_dante_eval.py \
  --candidate google-gemini-native-modelaccess \
  --suite tooling/ai-evals/fixtures/<suite>.json \
  --execute \
  --max-calls <BOUND> \
  --allow-unpriced \
  --report tooling/ai-evals/reports/<local-report>.json
```

Use `--allow-unpriced` only when the call/output hard caps are sufficient and an exact EUR price is intentionally not being claimed. Otherwise configure explicit prices and `--max-cost-eur`.

`reports/` is ignored by Git. Model output is excluded from reports by default. Add `--include-output` only when inspecting synthetic failures locally.

Do **not** repeat successful qualification calls merely to prove branch closure. The closure gate is deterministic and zero-provider-call by design.

## Native runtime smoke

The standalone guarded smoke is:

```bash
uv run --locked --project apps/backend \
  python tooling/ai-evals/run_gemini_native_runtime_smoke.py
```

Default is dry-run/zero provider calls. `--execute` performs a real synthetic native call and should only be used when a new compatibility question actually needs live evidence.

## Deterministic tooling tests

```bash
uv run --locked --project apps/backend pytest tooling/ai-evals/tests
```

Ruff checks use the backend configuration:

```bash
uv run --locked --project apps/backend ruff format --check \
  --config apps/backend/pyproject.toml tooling/ai-evals

uv run --locked --project apps/backend ruff check \
  --config apps/backend/pyproject.toml tooling/ai-evals
```

These commands make no provider calls and are part of backend CI.

## Foundation closure gate

The branch-level deterministic gate is:

```bash
bash tooling/ai-evals/run_ai_foundation_closure_gate.sh
```

Optionally include canonical PostgreSQL acceptance:

```bash
bash tooling/ai-evals/run_ai_foundation_closure_gate.sh --with-postgres
```

The gate checks the existing lock; it does **not** regenerate it and performs **zero provider calls**.

## Verdict policy

The runner uses the DANTE direct-eval taxonomy where applicable:

```text
PASS
HARD_FAIL
QUALITY_FAIL
INVALID_FIXTURE
INVALID_GRADER
INVALID_HARNESS
PROVIDER_INFRA_FAILURE
INCONCLUSIVE
```

A hard semantic/privacy/safety failure outranks softer quality. Cost, latency, and prose never average away a hard failure.

Provider `incomplete` is preserved as incomplete/inconclusive evidence rather than being reclassified as an infrastructure failure merely because a partial structured JSON fragment cannot be parsed.

E01 is not falsely marked PASS in a model-candidate run. It is recorded as `SKIPPED_MODEL_AVOIDANCE` because proving that DANTE correctly avoids the model belongs to runtime-routing evaluation, not to a provider invocation.

## Adding another candidate

Do not clone the suite around a provider.

Add a candidate adapter implementing the same minimal laboratory contract:

```text
EvalFixture
    -> candidate.invoke(...)
    -> CandidateResult
    -> provider-neutral grader/report
```

Provider-specific endpoint/authentication/protocol behavior remains in the candidate adapter. Fixtures, assertions, workload identities, budget policy, verdicts, and reports remain provider-neutral.

A candidate performing well here is only **model/runtime-candidate evidence**. Production qualification still requires the applicable DANTE binding, security/privacy, capacity, reliability, integration, and direct-proof gates.
