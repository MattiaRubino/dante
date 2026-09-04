# DANTE Intelligence — Runtime / Model-Target Closure Proposal

- **Date:** 2026-09-04
- **Branch:** `feature/ai-implementation`
- **Status:** MATERIALIZED DECISION CANDIDATE / DOES NOT OVERRIDE ACCEPTED ARCHITECTURE UNTIL ACCEPTED
- **Scope:** close the concrete runtime/model-selection gap intentionally left open by AI-04 and the implementation baseline, using the completed DANTE simulation corpus, accepted architecture and first direct GPT-4.1 baseline evidence.
- **Database/Alembic change:** NONE
- **Production provider activation:** NONE

## 1. Why this document exists

The accepted architecture already solved the hard semantic/runtime problem. It intentionally left concrete production choices open, including:

- exact `ModelTarget` vocabulary;
- concrete primary/fallback provider(s);
- concrete model snapshots/defaults;
- provider SDKs/adapters;
- actual direct provider evidence;
- AI gateway product;
- production route activation.

The first direct DANTE baseline is now available. Across the two formal suites, the Azure GPT-4.1 deployment completed 28 provider calls using 5,240 total tokens. Raw verdicts were 25 PASS, 2 QUALITY_FAIL and 1 HARD_FAIL; review classified all three non-PASS results as oracle/normalization/canonical-format defects rather than substantive semantic/privacy/effect failures. No provider/transport failure occurred. The smoke call adds one additional real API call but is not counted as a separate benchmark fixture.

The supported inference is narrow but important: bounded structured DANTE workloads do not currently justify a mandatory frontier/premium model. A replaceable logical target architecture should therefore start with the smallest number of active target classes and allow one physical model to satisfy multiple logical targets when evidence permits.

## 2. Decisions proposed

### D1 — Keep three peer reasoning paths

The accepted peer paths remain:

```text
DETERMINISTIC COMPUTE
SOLVER
MODEL ACCESS
```

`NO_MODEL` is a first-class production route, not a degraded fallback.

### D2 — Exactly two active generative ModelTargets initially

Proposed active target vocabulary:

```text
STRUCTURED_INTERPRETATION
GENERAL_REASONING
```

Proposed dormant target:

```text
DEEP_REASONING
```

`DEEP_REASONING` has no production binding by default and is activated only if integrated DANTE evidence shows that `GENERAL_REASONING` cannot meet a required quality/reliability floor economically.

#### `STRUCTURED_INTERPRETATION`

Purpose:

- bounded natural-language interpretation;
- intent classification;
- reference/target candidate discrimination;
- structured extraction;
- normalization;
- bounded rewrite/summarization where semantics are externally verifiable;
- candidate production for later deterministic/application validation.

Required posture:

- low latency;
- deterministic/inspectable schema contract;
- structured outputs when supported;
- minimal context;
- no authority/effect ownership;
- cheap enough for high-frequency use;
- may be skipped entirely when deterministic parsing/query logic suffices.

Primary eval families: E02, E03, bounded portions of E05/E11/E12.

#### `GENERAL_REASONING`

Purpose:

- grounded Ask-DANTE synthesis;
- explanation and decision support;
- scenario comparison;
- multi-constraint planning support around the deterministic solver;
- conflict/uncertainty reasoning;
- longer document reasoning after deterministic extraction/OCR as applicable;
- open-world synthesis after governed acquisition;
- multi-step capability planning where the Capability Runtime remains execution authority.

Required posture:

- high semantic reliability;
- grounding discipline;
- long-context support where useful, without treating context capacity as correctness;
- structured output/tool-call support where the workload needs it;
- current provider/data/feature eligibility;
- no canonical truth/effect/publication ownership.

Primary eval families: E05, E06, E07, E09-E14 and integrated E08 where applicable.

#### Why not more active targets now

The simulation corpus justifies many capability dimensions, but it does not justify one model target per capability. Vision, OCR, audio, embeddings, web acquisition, browser/computer use and code execution have materially different security/data/runtime properties and are better represented as capability requirements or specialist capability adapters. They can constrain route eligibility without multiplying logical reasoning targets.

### D3 — One physical model may back both active targets

Logical target separation does not imply multiple paid models.

Valid configuration:

```text
STRUCTURED_INTERPRETATION -> Binding A
GENERAL_REASONING         -> Binding A
```

If later evidence supports a cheaper fast model:

```text
STRUCTURED_INTERPRETATION -> Binding B
GENERAL_REASONING         -> Binding A
```

This allows DANTE to begin operationally simple and split only when economics/latency evidence proves value.

### D4 — Routing remains deterministic and content-minimizing

No router LLM is selected.

Routing consumes only the minimum necessary route metadata, including:

- target;
- required capabilities;
- quality floor;
- context/latency class;
- consequence class;
- provider/data/feature eligibility;
- region/residency requirements;
- entitlement/resource budget;
- binding health/capacity;
- rollout/canary state;
- measured cost policy.

Full private task content is not disclosed to an auxiliary model merely to choose a model.

### D5 — Champion/challenger is configuration, not application code

Every target resolves through a versioned route revision.

Conceptual configuration:

```text
RouteRevision
  target
  champion_binding
  qualified_challenger_bindings[]
  fallback_bindings[]
  harness_revision
  qualification_evidence
  eligibility/profile refs
  rollout state
  effective-from
```

Application/domain code never names OpenAI, Anthropic, Google, Mistral, Azure, Bedrock or Vertex.

Promotion path:

```text
candidate admission
-> exact candidate identity
-> direct DANTE capability eval
-> integrated DANTE eval where required
-> binding/privacy/feature qualification
-> repeated reliability
-> latency + effective cost/task
-> bounded canary
-> champion promotion
```

Rollback is a route-revision change, not an application rewrite.

Shadow/dual-send is not the default because it is real disclosure and duplicate provider exposure. Prefer synthetic/offline replay and bounded canary traffic.

### D6 — Exact model/binding identity is pinned

Production qualification records at least:

```text
vendor
serving platform
protocol family
endpoint/deployment
region/data-zone
model ID
snapshot/version
reasoning/thinking settings
HarnessProfile revision
feature mode
structured-output/tool settings
retention/ZDR posture
capability projection
service tier
retry/fallback policy
```

Moving `latest` aliases are not sufficient production qualification identity unless the provider cannot offer pinning and DANTE explicitly accepts/requalifies that risk.

### D7 — Failover is qualified route recomposition

No blind replay of a serialized provider request.

Fallback requires:

- independent qualification for the current target;
- current data/provider/feature eligibility;
- a compatible current HarnessProfile;
- rebuilt/minimized ConsumerContext where required;
- current resource admission;
- no safety-arbitrage after provider refusal.

Cross-provider continuation rebuilds DANTE context; provider conversation state never becomes DANTE memory.

## 3. Service inventory

### Required for first usable Intelligence vertical

#### A. DANTE Model Access Runtime

Application-owned provider-neutral port/runtime. Required now.

Provider SDKs/HTTP clients exist only in private outbound ProviderAdapters.

#### B. Deterministic route + Semantic Query Gateway

Required now.

DANTE-native current/history/absence questions, calculations, verification and source truth should avoid model calls where accepted application query seams can answer them.

#### C. Constraint solver

Required as a peer path for scheduling/packing/feasibility work.

Recommended first implementation candidate: **OR-Tools CP-SAT** behind a DANTE-owned solver port. It is a local library, not an external AI service. Model reasoning may formulate/explain candidate constraints; solver output remains deterministic evidence where applicable.

#### D. Internal Search

Required as a separate product/application capability, not as Ask-DANTE's mandatory backend.

Initial implementation should use the already-owned PostgreSQL stack for structured/lexical discovery (`PostgreSQL`, `pg_trgm`, normal indexes/search projections). No external search SaaS or vector database is required for first activation.

`pgvector` is already available and remains dormant/derived until semantic retrieval evidence justifies embeddings.

#### E. Eval/regression tooling

Required now.

`tooling/ai-evals` remains the provider-neutral engineering qualification boundary. It must grow from prompt-only fixtures into integrated E01/E04/E08 proof as the real application seams materialize.

No external eval SaaS is required to own DANTE semantics.

### Trigger-gated specialist services

#### Embeddings / reranking

Activate only when semantic retrieval is product-required and E04/embedding-vector direct proof shows measurable gain over PostgreSQL lexical/typed retrieval.

Embeddings are derived search artifacts, never truth or memory.

No Pinecone/Qdrant/external vector database is currently justified because PostgreSQL + pgvector already exists.

#### OCR / document parsing

Use deterministic PDF/text extraction first. Activate OCR only for scanned/image documents or layouts that require it.

OCR/document service remains a specialist capability and does not define the general reasoning provider.

#### Speech-to-text / text-to-speech / realtime voice

Progressive product capability; separate service/binding qualification. Not required to close the current Ask-DANTE vertical.

#### External web/research acquisition

Separate governed capability. A provider-native web-search tool may be one binding, but Global Search remains DANTE-internal discovery and must not be conflated with external open-world research.

#### Browser/computer/code execution

Dormant until product scope activates it. Must go through Capability Runtime plus Execution Environment Broker/isolation. Provider-hosted execution is not automatically sufficient DANTE isolation.

#### Durable orchestration

Keep accepted decision:

```text
Class A -> PostgreSQL transactional outbox + bounded worker
Class B -> Restate selected but dormant until a real qualifying workflow exists
```

Do not introduce Temporal/Celery/agent workflow infrastructure merely for AI convenience.

## 4. Explicitly not selected

The following are not required as core architecture choices now:

- LangChain/LangGraph as application architecture;
- a generic autonomous-agent framework;
- a separate AI microservice;
- a routing LLM;
- Pinecone/Qdrant/vector SaaS;
- OpenRouter/LiteLLM as DANTE's semantic abstraction;
- provider conversation/thread state as memory;
- provider-hosted fallback as DANTE routing authority;
- a local frontier GPU fleet;
- a premium/deep model by default;
- a second production provider before reliability/privacy economics justify it.

A gateway such as LiteLLM/OpenRouter could later be evaluated as a *serving/transport binding* for experimentation, but it must not replace DANTE's ModelAccess/ProviderBinding semantics or become a lowest-common-denominator authority.

## 5. Current model/provider evidence and qualification shortlist

### Existing baseline

Azure-hosted GPT-4.1 is the only model with direct DANTE evidence today.

It is **baseline evidence**, not a selected production provider/model.

The result supports using one ordinary non-frontier-quality general model as the initial performance floor for bounded prompt-only DANTE semantics.

### Candidate classes worth qualifying next

The objective is not to test every current flagship. Test candidates that answer a distinct architectural/economic question.

#### Question A — how cheap can `STRUCTURED_INTERPRETATION` become without regression?

Useful candidates include:

- **GPT-4.1 Mini** — older/stable non-reasoning control; inexpensive and snapshot-pinnable;
- **GPT-5.6 Luna** — very low current OpenAI price with reasoning levels and broad tool/structured-output support;
- **Mistral Small 4** — low-cost independent/EU-oriented challenger.

Do not test all merely because they exist. Select at least one old/stable control and one materially cheaper/newer alternative if API access is practical.

#### Question B — can one economical model also satisfy `GENERAL_REASONING`?

High-information challengers:

- **Gemini 3.8 Flash** — GA, 1M context, tunable thinking, broad multimodal/tool surface and low current price; its introductory 2026 price must not be treated as permanent economics;
- **Claude Sonnet 5** — strong independent-provider general reasoning/document/tool challenger with 1M context;
- **Mistral Large 3 / Medium 3.5** — value/EU track when regional/privacy economics materially matter;
- **GPT-5.6 Terra** — useful only if an OpenAI-family comparison becomes decision-critical; not automatically required just because it is newer than the measured GPT-4.1 baseline.

No frontier/premium model is mandatory at this stage.

### `DEEP_REASONING`

No candidate should be purchased/qualified for this target until a concrete integrated DANTE workload fails or is materially uneconomic on the general target.

If that trigger occurs, then frontier candidates are evaluated against the specific failing workload rather than by public leaderboard rank.

## 6. Provider/privacy binding posture

Provider selection is made at **binding** granularity, not vendor-name granularity.

Examples of materially different bindings include:

```text
same model + Azure Global
same model + Azure EU DataZone
same model + Azure regional
same model + OpenAI Europe project/ZDR eligibility
Claude direct API
Claude through an EU cloud serving platform
Gemini Developer API
Gemini through Vertex regional controls
Mistral global endpoint
Mistral EU regional endpoint
```

The binding eligibility record must capture actual processing/storage/retention/feature behavior. A provider/model can be eligible for one DANTE data/work class and ineligible for another.

Privacy, Authority, disclosure and currentness are hard gates and cannot be traded for lower price or benchmark quality.

## 7. Regression and replacement contract

DANTE is deliberately designed so that today's champion can be replaced rapidly without semantic migration.

A material model/Harness/binding change requires risk-proportionate requalification.

Minimum comparison record:

```text
hard failures
quality failures
pass@1 / repeated reliability
input/output/reasoning usage
TTFT where observable
end-to-end task latency
provider infra failures
feature/tool reliability
region/privacy eligibility
effective cost per successful DANTE task
```

Promotion requires no applicable hard semantic/privacy/safety failure.

Public benchmark wins cannot override a DANTE hard failure.

If a new candidate does not materially improve cost, latency, reliability, capability or operational/privacy posture, the current champion remains in place even if the candidate is newer.

## 8. Implementation consequence

The next code vertical should not be another architecture mega-round. It should materialize the already-accepted seams in this order:

1. provider-neutral `ModelAccessPort` + invocation/result contracts;
2. versioned target/route/Harness/ProviderBinding configuration skeleton;
3. one development ProviderAdapter/binding;
4. `STRUCTURED_INTERPRETATION` and `GENERAL_REASONING` logical targets, initially allowed to map to the same binding;
5. read-only Ask-DANTE execution path;
6. deterministic E01 + native semantic-query E04 proof;
7. integrated context/privacy/currentness/verification proof;
8. E08 capability/tool proof only when a real governed capability seam exists;
9. integrated regression suite and exact route evidence;
10. only then production binding qualification/activation.

No database/Alembic change is implied by this closure.

## 9. Acceptance criteria for this proposal

Accept if it is agreed that:

1. the semantic/runtime architecture remains unchanged;
2. only two generative targets are initially active;
3. premium/deep reasoning is dormant and evidence-triggered;
4. capability specialists remain orthogonal to general model targets;
5. routing is deterministic and versioned;
6. champion/challenger promotion is eval-driven and rollbackable;
7. one physical model may back multiple logical targets;
8. provider/model/version/region/feature/retention are binding-level qualification dimensions;
9. no generic agent/gateway/vector/service platform is required merely to start Intelligence;
10. the next work is implementation + integrated proof, not another broad architecture simulation round.
