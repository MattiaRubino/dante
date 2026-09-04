# DANTE AI Eval Lab

Status: **evaluation tooling / non-production**

This directory is DANTE's isolated direct-evaluation laboratory. It exists to compare
model/provider candidates against DANTE workloads without coupling benchmark code to
the production Intelligence runtime.

## Authority and non-claims

The semantic authority remains the accepted DANTE direct-evaluation architecture
(`DANTE-E01..DANTE-E14`). This tooling is only an executable runner/fixture surface.

This directory does **not**:

- select a production provider;
- make Azure, OpenAI, GPT-4.1, or any other model canonical;
- activate a DANTE `ProviderBinding`;
- authorize private/production data egress;
- prove production qualification;
- alter PostgreSQL/Alembic;
- replace DANTE runtime, Auth/AuthZ, verification, publication, effects, or audit.

`MODEL TARGET != PROVIDER != MODEL != DEPLOYMENT` remains binding.

## Current first candidate

The first laboratory candidate is Azure OpenAI Responses using an existing deployment.
It is deliberately candidate-specific only at the adapter boundary.

Supported environment variables:

```text
DANTE_EVAL_AZURE_ENDPOINT
DANTE_EVAL_AZURE_API_KEY
DANTE_EVAL_AZURE_DEPLOYMENT
```

For convenience, the adapter also accepts the existing local names when the DANTE
names are not present:

```text
DOC_CLASS_AZURE_ENDPOINT
DOC_CLASS_API_KEY
DOC_CLASS_DEPLOYMENT
```

Secrets are never printed and must never be committed.

The Azure resource root is normalized to:

```text
https://<resource>.openai.azure.com/openai/v1/
```

The deployment name is sent as the Responses API `model` value.

## Cost / blast-radius guardrails

Paid execution is fail-closed by default:

- command default is **dry-run**;
- `--execute` is required for any provider call;
- default suite requires 13 model calls;
- hard global cap is 30 calls;
- per-call output hard cap is 512 tokens;
- per-fixture input + instructions hard cap is 16,000 characters;
- provider SDK automatic retries are disabled (`max_retries=0`);
- calls are sequential;
- `store=false`;
- streaming, background mode, and tools are disabled;
- only synthetic/public fixture data is allowed.

For priced execution, provide both token prices and optionally a maximum euro budget.
The budget guard uses a conservative pre-dispatch input estimate and actual provider
usage after each call. It is a safety guardrail, **not** a cloud billing authority.

Execution without prices is blocked unless `--allow-unpriced` is explicitly supplied.

## Suite design

`fixtures/mini-baseline-v1.json` is the first cheap baseline. It is not full DANTE
qualification.

It currently samples:

```text
E01 model avoidance                 no provider call; runtime proof remains separate
E02 intent/reference                2 cases
E03 structured extraction           1 case
E05 context/privacy                 1 case
E06 planning/replanning             2 cases
E07 document grounding              1 case
E09 consequential boundary          1 case
E10 multi-actor disclosure          1 case
E11 adaptive memory/learning        1 case
E12 currentness/supersession        1 case
E13 open-world abstention            1 case
E14 proactivity/duplicate attention 1 case
```

That is **14 fixtures / 13 paid model calls maximum** for the complete mini suite.

E04 and E08 are intentionally not faked into this first model-only baseline:
native query/history and real capability/tool use need their relevant DANTE/application
surfaces rather than pretending that a prompt alone proves them.

The same principle applies to future multimodal, voice/realtime, browser/computer use,
code execution, durable background work, and embedding/vector suites: they are added
when their actual trigger/capability surface exists.

## Dry-run first

From the repository root:

```bash
uv run --project apps/backend \
  python tooling/ai-evals/run_dante_eval.py
```

This performs no paid call. It validates the suite and prints the execution plan.

## One-call smoke test

After configuring the Azure variables:

```bash
uv run --project apps/backend \
  python tooling/ai-evals/run_dante_eval.py \
  --only e02-resolved-reference \
  --max-calls 1 \
  --allow-unpriced \
  --execute
```

This is intentionally the only documented unpriced path: one bounded call.

## Priced mini-baseline

After obtaining the exact price for the serving SKU/region/deployment, use:

```bash
uv run --project apps/backend \
  python tooling/ai-evals/run_dante_eval.py \
  --execute \
  --max-calls 13 \
  --input-eur-per-million <INPUT_PRICE> \
  --output-eur-per-million <OUTPUT_PRICE> \
  --max-cost-eur <MAX_BUDGET> \
  --report tooling/ai-evals/reports/azure-gpt41-mini-v1.json
```

`reports/` is ignored by Git. Model output is excluded from reports by default.
Add `--include-output` only when inspecting synthetic failures locally.

## Deterministic tooling tests

```bash
uv run --project apps/backend \
  python -m unittest discover -s tooling/ai-evals/tests -p "test_*.py"
```

These tests make no provider calls.

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

A hard semantic/privacy/safety failure outranks softer quality. Cost, latency, and
nice prose never average away a hard failure.

E01 is not falsely marked PASS in a model-candidate run. It is recorded as
`SKIPPED_MODEL_AVOIDANCE` because proving that DANTE correctly avoids the model belongs
to runtime-routing evaluation, not to a provider invocation.

## Adding another candidate

Do not clone the suite around a provider.

Add a candidate adapter implementing the same minimal laboratory contract:

```text
EvalFixture
    ↓
candidate.invoke(...)
    ↓
CandidateResult
    ↓
provider-neutral grader/report
```

Provider-specific endpoint/authentication/protocol behavior remains in the candidate
adapter. Fixtures, assertions, workload identities, budget policy, verdicts, and
reports remain provider-neutral.

A candidate performing well here is only **model-candidate evidence**. Production
qualification still requires the applicable DANTE binding, security/privacy,
capacity, reliability, integration, and direct-proof gates.
