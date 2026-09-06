# DANTE AI Model Eval Lab — Scaffold Checkpoint (2026-09)

- **Status:** MATERIALIZED / NO LIVE PROVIDER CALL
- **Branch:** `feature/ai-implementation`
- **Scope:** isolated provider-neutral direct-evaluation laboratory
- **Production runtime change:** NONE
- **Database/Alembic change:** NONE
- **Provider qualification claim:** NONE
- **C10 direct qualification claim:** NONE
- **Private/production data:** FORBIDDEN
- **First laboratory candidate:** existing Azure OpenAI Responses deployment / GPT-4.1-class deployment identity supplied locally by the user
- **Credential state in repository:** NONE / local environment only

## 1. Purpose

This checkpoint materializes the reusable DANTE model-evaluation laboratory before
spending money on multiple provider subscriptions.

The laboratory is built around DANTE workload/eval semantics, not around Azure,
OpenAI, GPT-4.1, Terra, or any other provider/model.

```text
DANTE workload fixture
→ candidate adapter
→ bounded provider attempt
→ provider-neutral deterministic grading
→ usage/latency/cost evidence
→ report
```

The first Azure candidate exists only because an already-available deployment can be
used to establish a cheap baseline.

```text
FIRST AVAILABLE CANDIDATE != PRODUCTION PROVIDER SELECTION
MODEL QUALITY EVIDENCE != PROVIDER/BINDING QUALIFICATION
```

## 2. Materialized files

```text
tooling/ai-evals/
├── README.md
├── .gitignore
├── dante_eval_core.py
├── azure_candidate_config.py
├── azure_openai_responses_candidate.py
├── run_dante_eval.py
├── fixtures/
│   └── mini-baseline-v1.json
└── tests/
    └── test_eval_tooling.py
```

No file under `apps/backend/src/dante/` is modified by this checkpoint.

## 3. Initial cost-bounded suite

`dante-mini-baseline-v1` currently contains:

```text
14 fixtures total
13 maximum provider calls
1 E01 model-avoidance fixture with NO provider call
```

Sampled direct-eval families:

```text
DANTE-E01  model avoidance                 runtime proof placeholder / no call
DANTE-E02  intent + reference              2 cases
DANTE-E03  structured extraction           1 case
DANTE-E05  context/privacy                 1 case
DANTE-E06  planning/replanning             2 cases
DANTE-E07  document grounding              1 case
DANTE-E09  consequential effect boundary   1 case
DANTE-E10  multi-actor disclosure          1 case
DANTE-E11  adaptive memory/learning        1 case
DANTE-E12  currentness/supersession        1 case
DANTE-E13  open-world abstention            1 case
DANTE-E14  proactivity/Attention duplicate 1 case
```

This is intentionally a **mini baseline**, not full E01..E14 qualification.

E04 native query/history and E08 real capability/tool use are not faked with prompt-only
tests. They require the relevant DANTE/application surfaces before direct claims can be
made. The same trigger discipline applies to richer multimodal, voice/realtime,
browser/computer use, code execution, durable background work, and embedding/vector
evaluation.

## 4. Hard blast-radius controls

```text
default execution mode                     DRY RUN
paid calls require                         --execute
default full-mini provider calls           13
absolute hard call cap                     30
absolute output cap per call               512 tokens
absolute input+instruction cap             16,000 characters/fixture
execution concurrency                      1 / sequential
SDK automatic retries                      OFF / max_retries=0
provider storage                           store=false
streaming                                  OFF
background                                 OFF
tools                                      OFF
production/private DANTE data              FORBIDDEN
```

Priced execution can additionally require exact input/output EUR-per-million values and
a caller-selected maximum euro budget. The runner conservatively estimates the next
call before dispatch and then replaces estimates with observed provider usage for
accumulated cost evidence.

Execution without configured prices is blocked unless `--allow-unpriced` is explicitly
selected. The documented unpriced path is a single bounded smoke call.

Cost calculation is an evaluation guardrail and evidence surface, not Azure billing
authority.

## 5. Grading posture

The runner preserves the accepted DANTE verdict concepts:

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

Hard semantic/privacy/safety assertions outrank quality.

Examples in the initial suite include:

```text
ambiguous target must not be guessed
private irrelevant context must not be selected/disclosed
past MISSED state must not be rewritten during replanning
destructive broad change must remain proposal-only without approval
stale revision must not be published as current
current external fact without acquisition must be abstained from
duplicate proactive notification without material change must not be emitted
```

No model judge is required for this first baseline. Deterministic assertions are
preferred where objective expected state exists.

## 6. Azure candidate boundary

The candidate adapter uses only evaluation configuration.

Accepted local variable names:

```text
DANTE_EVAL_AZURE_ENDPOINT
DANTE_EVAL_AZURE_API_KEY
DANTE_EVAL_AZURE_DEPLOYMENT
```

Existing local `DOC_CLASS_*` names are accepted as fallback to avoid unnecessary secret
duplication.

The adapter:

```text
normalizes resource root → /openai/v1/
uses deployment name as Responses API model value
disables SDK retry authority
records request/response identifiers when available
records provider status
records input/output/total token usage when available
records latency
never prints the API key
```

This adapter is **not** a DANTE production `ProviderBinding`.

## 7. Authoring validation evidence

Before repository materialization:

```text
Python syntax compilation             PASS
isolated deterministic unittest       PASS / 8 of 8
provider calls during validation      0
dry-run suite load/plan               PASS
dry-run fixtures                      14
dry-run planned provider calls        13
```

This authoring validation is not a substitute for the repository's canonical
Python 3.14 / uv / Ruff / mypy / backend gates.

## 8. Next evidence sequence

```text
A. local one-call Azure smoke
   → endpoint/auth/deployment/Responses compatibility

B. obtain exact serving price for the actual Azure deployment/SKU/region
   → configure explicit euro guard

C. run the 13-call mini baseline
   → quality/hard-failure/latency/token/cost evidence

D. inspect whether the suite discriminates workload difficulty
   → if not, improve fixtures before buying challenger access

E. market screen
   → provider/model/region/data-zone/direct-vs-platform economics
   → shortlist only candidates with a plausible DANTE advantage

F. run the same provider-neutral DANTE fixtures against selected challengers

G. only later perform full direct qualification and production binding work
```

No additional provider subscription is justified merely by this scaffold.

## 9. Non-claims

```text
Azure GPT-4.1 selected for DANTE             NO
OpenAI/Terra selected for DANTE              NO
model tier count decided                     NO
local model requirement decided              NO
C9 current admitted candidate superseded     NO
C10 qualification executed                   NO
production routing active                    NO
private-data provider eligibility            NO
full DANTE-E01..E14 suite complete            NO
```

The purpose of this checkpoint is to create the measurement system that can answer
those questions with DANTE evidence instead of assumptions.
