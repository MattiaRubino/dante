# DANTE AI Model Eval — Decision Run (2026-09)

- **Status:** READY / LIVE RUN NOT YET EXECUTED
- **Branch:** `feature/ai-implementation`
- **Purpose:** obtain one decision-grade baseline from the already-available Azure OpenAI GPT-4.1 deployment before spending money on challenger providers/models
- **Production runtime change:** NONE
- **Database/Alembic change:** NONE
- **Private/production data:** FORBIDDEN
- **Provider qualification claim:** NONE

## 1. Evidence already obtained

The initial `dante-mini-baseline-v1` run executed 13 provider calls and produced:

```text
provider calls                 13
input tokens                 2047
output tokens                 271
PASS                           11
QUALITY_FAIL                    2
HARD_FAIL                       0
provider/infra failures         0
```

The two quality mismatches were not hard semantic/privacy/safety failures:

- E11 preserved the declared preference and correctly refused automatic memory replacement, but selected `keep_declared` rather than the fixture's preferred `ask_confirmation`;
- E12 selected the correct current revision/status but returned a non-canonical textual stale reference label.

Those observations are treated as benchmark-design evidence, not as proof that the model is production-qualified.

## 2. Final bounded decision extension

The next and intended final baseline run uses:

```text
tooling/ai-evals/fixtures/decision-extension-v1.json
```

It contains exactly **15 provider calls**. It does not repeat the easy baseline wholesale; it adds harder, more discriminating cases for:

```text
DANTE-E02  typed reference resolution
DANTE-E03  uncertainty-preserving extraction
DANTE-E05  provenance/currentness conflict + selective disclosure
DANTE-E06  constrained planning, infeasibility, replanning, scenario trade-off
DANTE-E07  document grounding with superseded/distractor material
DANTE-E09  authorization != execution truth
DANTE-E10  delegation scope
DANTE-E11  declared preference != observed behavior truth laundering
DANTE-E12  authoritative current state != stale derived cache
DANTE-E13  conflicting equally authoritative evidence / abstention
DANTE-E14  material proactive change
```

E04 native query/history and E08 real capability/tool execution remain trigger/integration dependent and are not faked with prompt-only tests.

## 3. Spend/blast-radius posture

The decision extension is intentionally small:

```text
provider calls                 15
execution concurrency           1
SDK automatic retries           0
largest fixture input+instruction < 1,000 chars
maximum output cap/call       220 tokens
sum of fixture output caps   2,680 tokens
production/private data         0
```

The runner's existing absolute hard call cap remains 30. `store=false`, tools/background/streaming are disabled by the Azure candidate adapter.

This is not a throughput, soak, or million-token benchmark.

## 4. Decision rule after this run

After this extension, the first Azure GPT-4.1 baseline will consist of **28 total real calls** across the initial and decision suites.

The evidence is interpreted in this order:

1. hard semantic/privacy/safety failures;
2. provider/infra failures;
3. quality failures and whether the oracle itself is sound;
4. latency and token usage;
5. workload families where the model is clearly sufficient, borderline, or insufficient.

The run is intended to answer the next architecture/business question, not to prove a provider winner:

```text
Is GPT-4.1-class capability already sufficient for most DANTE model-required work?
Where is it overkill?
Where is it insufficient?
Which workload families justify a cheaper/smaller challenger?
Which, if any, justify a stronger challenger?
```

Only after those answers are available should DANTE perform market screening across current providers/models, regions/data zones, privacy/residency posture, latency and effective cost per successful DANTE task.

## 5. Stop rule

After the 15-call decision extension:

- do **not** keep iterating the same baseline casually;
- allow at most one small targeted rerun only when a result is ambiguous because of fixture/grader semantics or a transient provider failure;
- otherwise stop Azure baseline testing and move to provider/model/region market analysis and a minimal challenger shortlist.

No additional subscription is justified before that analysis.
