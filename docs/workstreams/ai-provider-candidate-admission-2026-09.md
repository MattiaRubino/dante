# DANTE AI — Provider Candidate Admission — 2026-09

- **Status:** CURRENT C8 / P1 ADMISSION DECISION
- **Branch:** `feature/ai-implementation`
- **Decision date:** 2026-09-03
- **Architecture authority:** `../architecture/dante-ai-implementation-baseline-final.md`
- **Implementation workstream:** `ai-implementation.md`
- **Database/Alembic change:** NONE
- **SDK/adapter implementation:** NONE
- **Production qualification:** NOT CLAIMED
- **Production activation:** NONE

This record closes the first provider discovery/admission checkpoint for DANTE Intelligence. It admits one concrete provider/model/API composition **for qualification work only**. It does not make that composition production-eligible, private-data-eligible, entitled, rollout-active or preferred forever.

```text
CANDIDATE ADMISSION != PRODUCTION QUALIFICATION
QUALIFIED != ELIGIBLE != AVAILABLE != ENTITLED != ROLLOUT-ACTIVE
```

Provider/protocol facts are time-sensitive. The sources below were rechecked on 2026-09-03 immediately before this decision. Any material provider/model/API change re-enters the applicable admission/qualification gates.

---

## 1. First-vertical requirement

The accepted first DANTE technical vertical remains:

```text
private authenticated in-app
single-turn
inline/request-owned
READ_ONLY
non-streaming public Ask
no durable Run
no background resume
no consequential mutation
```

The first model-assisted path needs a provider composition that can be isolated behind DANTE-owned application contracts and can later prove, at minimum:

```text
text input/output
structured output when required
provider-neutral error/outcome normalization
usage evidence
bounded timeout/cancellation/retry semantics
no hidden SDK retry authority
request-local data handling compatible with DANTE policy
conformance/live-compatibility testability
direct DANTE eval feasibility
capacity/reliability/security/privacy/economics evidence path
```

Built-in provider tools, provider memory, provider-managed conversation state, background execution, web/file search, MCP, code execution, computer use and consequential tools are **not required** by this admission.

---

## 2. P0 shortlist

Current shortlist reviewed:

```text
A. OpenAI native API / Responses API / GPT-5.6 Terra
B. Anthropic native Claude API / Messages API / Claude Sonnet 5
C. Google Cloud Vertex AI / Gemini 3.8 Flash
```

The shortlist is deliberately narrow. No benchmark leaderboard or vendor marketing claim is sufficient for admission or qualification.

---

## 3. Evidence matrix

### A. OpenAI native Responses API / GPT-5.6 Terra

Observed current facts:

```text
model id                 gpt-5.6-terra
context                  1,050,000 tokens
max output               128,000 tokens
standard token price     $2 / MTok input; $12 / MTok output
function calling         supported
structured outputs       supported
Responses API            supported
response statuses        completed / failed / in_progress /
                         cancelled / queued / incomplete
response usage           explicit token-usage object
response cancellation    explicit cancel endpoint exists
business/API training    OFF by default unless customer opts in
ZDR                       available to eligible API organizations
SDK retries              2 automatic retries by default;
                         configurable to max_retries=0
```

DANTE implications:

```text
+ narrow non-streaming first vertical fits the Responses surface
+ structured-output and usage evidence are directly representable
+ provider response status/cancel semantics are explicit enough for
  a private adapter conformance suite
+ SDK automatic retry can be disabled so DANTE owns retry budget
+ ZDR path exists for later private/sensitive-data eligibility

- data-residency/model-snapshot applicability must be rechecked for
  the exact qualified GPT-5.6 Terra composition before private-data
  promotion; generic platform availability is not sufficient proof
- provider model identity remains material qualification evidence;
  alias/version drift cannot inherit old qualification automatically
- built-in tools/background/provider conversation state remain OFF
  unless separately admitted and qualified
```

### B. Anthropic native Claude API / Claude Sonnet 5

Observed current facts:

```text
model id                 claude-sonnet-5
context                  1,000,000 tokens
max output               128,000 tokens
standard token price     $2 / MTok input; $10 / MTok output
structured output        supported through current output-config path
Messages/tool surface    mature and feature-rich
ZDR                       supported for approved organizations
standard API retention   inputs/outputs deleted within 30 days,
                         subject to documented exceptions
SDK retries              transient failures retried twice by default;
                         configurable/disableable
error taxonomy           explicit 4xx/5xx/timeout/overload classes
refusal                   may be HTTP 200 with stop_reason=refusal
Priority Tier            not newly purchasable for Sonnet 5;
                         guaranteed capacity requires sales path
first-party storage      documented as US storage by default
```

DANTE implications:

```text
+ strong technical fit; structured output, usage and error evidence
  are sufficient to justify retention on the challenger list
+ ZDR exists for organizations with approved agreements
+ SDK retry authority can be disabled

- first-party storage/residency posture is less direct for an EU-bound
  deployment than Vertex regional processing; a cloud-hosted Claude
  binding would be a materially different ProviderBinding and must be
  admitted/qualified separately
- refusal-as-HTTP-200 must be normalized as refusal, never completion
- no reason to introduce a second adapter before the first qualification
  loop produces evidence that it is needed
```

### C. Google Cloud Vertex AI / Gemini 3.8 Flash

Observed current facts:

```text
model id                 gemini-3.8-flash
launch stage             GA
release date             2026-09-02
context                  1,048,576 tokens
max output               65,536 tokens
structured output        supported
function calling         supported
regions                  global + us/eu multi-region
security controls        data residency / CMEK / VPC-SC / AXT
usage metadata           explicit
API cancellation/error   canonical Google error model includes 499
                         CANCELLED and 504 DEADLINE_EXCEEDED
ZDR                       achievable subject to documented controls;
                         abuse-monitoring exception may be required
in-memory cache          isolated project-level cache with 24h TTL
                         documented by Vertex ZDR guidance
intro token price        $0.75 / $3.75 per MTok through 2026-12-31
standard from 2027       $1.50 / $7.50 per MTok global
```

DANTE implications:

```text
+ strongest currently documented regional-control posture of the
  shortlist and materially lower list price
+ explicit usage/finish/error semantics are suitable for normalization

- model became GA one day before this decision; operational maturity and
  workload quality have not yet been directly demonstrated by DANTE
- max output is lower than the two other shortlisted models, although
  still far above the first vertical's expected requirement
- Vertex ZDR requires configuration discipline; certain grounding and
  session features introduce retention and therefore remain OFF
- adding a second cloud/provider operational surface before first
  qualification would increase scope without current product evidence
```

---

## 4. P1 decision

```text
PROVIDER CANDIDATE
OpenAI native API

API SURFACE
Responses API

MODEL CANDIDATE
gpt-5.6-terra

ADMISSION STATUS
ADMITTED FOR QUALIFICATION ONLY

PRODUCTION QUALIFICATION
NO

PRIVATE/SENSITIVE DATA ELIGIBILITY
NO

PRODUCTION PROMOTION
NO
```

Reason for selecting this **first qualification candidate**:

1. It satisfies the minimum first-vertical capability envelope without requiring provider-managed tools, memory, search, background work or consequential execution.
2. Responses exposes explicit response lifecycle states, usage and cancellation surfaces that can be normalized behind DANTE's own contracts.
3. Structured outputs and function calling exist, while DANTE can keep all non-required feature modes disabled.
4. The official Python SDK's automatic retry behavior can be disabled with `max_retries=0`, preserving DANTE ownership of ProviderAttempt identity, retry budget, resource admission and egress evidence.
5. A ZDR path exists for later eligible API organizations, while live compatibility before private-data eligibility can use synthetic/public/minimized fixtures as already required by the architecture.
6. GPT-5.6 Terra's current $2/$12 price and 1.05M/128k envelope are sufficient to enter qualification without pre-judging final quality/economics.
7. Selecting exactly one candidate keeps C9 bounded. Claude Sonnet 5 and Gemini 3.8 Flash remain credible challengers if direct DANTE evaluation, privacy/residency requirements, capacity, cost or reliability evidence later justifies another admission.

This decision is **not** a claim that GPT-5.6 Terra is globally superior to Sonnet 5 or Gemini 3.8 Flash. DANTE quality ranking is intentionally deferred to production-owned direct evaluation.

---

## 5. Mandatory C9 qualification-candidate profile

The first private adapter candidate must start inactive and with the narrowest feature composition:

```text
provider                  OpenAI native API
API                       Responses API
model                     gpt-5.6-terra
public streaming          OFF
background mode           OFF
provider conversation     OFF
previous_response_id      OFF
provider built-in tools   OFF
web search                OFF
file search               OFF
code interpreter          OFF
shell / computer use      OFF
MCP / external tools      OFF
provider memory           OFF
store                     false
SDK automatic retries     OFF / max_retries=0
DANTE retries             only after classified safe pre-acceptance failure
live-compatibility data   synthetic/public/minimized until private-data gates pass
production activation     OFF
```

Structured output may be exercised only as a qualification feature of the direct model-access boundary. It does not authorize model-generated SQL, canonical mutation or Effect authority.

---

## 6. C9 hard gates

C9 may materialize the admitted **inactive** binding/adapter and conformance/live-compatibility evidence only if it preserves:

```text
DANTE allocates ProviderAttemptId before dispatch
SDK retries disabled or every real attempt becomes DANTE-visible
request timeout != proof request was not accepted
possible accepted/processed + lost response -> indeterminate outcome
no blind replay after ambiguous acceptance
refusal != infrastructure failure
usage known != estimated != unknown
provider error != recipient-safe error automatically
ProviderAdapter != routing authority
ProviderAdapter != Auth/AuthZ/Policy authority
ProviderAdapter != Effect authority
provider IDs != DANTE semantic/idempotency identity
```

The adapter must not import database mappings or inbound HTTP schemas and no provider SDK type may escape into application/public contracts.

---

## 7. Private-data and promotion blockers

Candidate admission alone does not permit real private/sensitive DANTE content.

Before such eligibility/promotion, the exact material composition must prove as applicable:

```text
current processor/DPA/subprocessor posture
current retention/ZDR eligibility and actual account configuration
current regional processing/data-residency support for the exact model/API
security/privacy review and data-class eligibility
provider conformance
live compatibility
production-owned direct DANTE eval
capacity/reliability evidence
cost/usage evidence
route-config revision + exact content digest
adapter/SDK identity and retry configuration
applicable SC/PSV register
```

Missing evidence is not `N/A`.

---

## 8. Non-admitted challengers

```text
Claude Sonnet 5
STATUS: RETAINED SHORTLIST CHALLENGER / NOT ADMITTED IN THIS C8

Gemini 3.8 Flash on Vertex AI
STATUS: RETAINED SHORTLIST CHALLENGER / NOT ADMITTED IN THIS C8
```

They may enter a later candidate-admission checkpoint if DANTE direct evidence or deployment constraints justify the added adapter/provider surface. No old C8 evidence automatically qualifies a future binding.

---

## 9. Current public evidence snapshot

Reviewed 2026-09-03. URLs are evidence references, not DANTE runtime dependencies.

### OpenAI

- `https://developers.openai.com/api/docs/models/gpt-5.6-terra`
- `https://developers.openai.com/api/docs/models`
- `https://developers.openai.com/api/reference/cli/resources/responses/methods/create`
- `https://developers.openai.com/api/reference/cli/resources/beta/subresources/responses`
- `https://github.com/openai/openai-python/blob/main/README.md`
- `https://openai.com/index/offering-zero-data-retention-for-frontier-models/`
- `https://openai.com/business-data/`
- `https://platform.openai.com/docs/models/default-usage-policies-by-endpoint`

### Anthropic

- `https://platform.claude.com/docs/en/models/sonnet-5/whats-new-sonnet-5`
- `https://platform.claude.com/docs/en/api/errors`
- `https://platform.claude.com/docs/en/about-claude/pricing`
- `https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data`
- `https://privacy.claude.com/en/articles/8956058-i-have-a-zero-data-retention-agreement-with-anthropic-what-products-does-it-apply-to`
- `https://privacy.claude.com/en/articles/7996890-where-are-your-servers-located-do-you-host-your-models-on-eu-servers`

### Google Cloud / Vertex AI

- `https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-flash`
- `https://docs.cloud.google.com/vertex-ai/generative-ai/docs/vertex-ai-zero-data-retention`
- `https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/api-errors`
- `https://cloud.google.com/vertex-ai/generative-ai/docs/reference/rest/v1/GenerateContentResponse`
- `https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing`

---

## 10. Verdict

```text
P0 SHORTLIST REVIEW                         COMPLETE
P1 CANDIDATE ADMISSION                      COMPLETE
FIRST ADMITTED PROVIDER                     OpenAI native API
FIRST ADMITTED API                          Responses API
FIRST ADMITTED MODEL CANDIDATE              gpt-5.6-terra
PROVIDER SDK INSTALLED                      NO
PRIVATE ADAPTER MATERIALIZED                NO
LIVE PROVIDER CALL EXECUTED                 NO
DIRECT DANTE EVAL                           NO
PRODUCTION QUALIFICATION                    NO
PRIVATE-DATA ELIGIBILITY                    NO
PRODUCTION PROMOTION                        NO
DATABASE/ALEMBIC CHANGE                     NO
```

Next implementation checkpoint:

```text
C9
→ admitted inactive provider adapter/binding
→ conformance
→ live compatibility on synthetic/public/minimized data
```
