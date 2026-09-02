# DANTE AI-05A — Whole-System Build Boundary Candidate

- **Status:** CANDIDATE / DESTRUCTIVE ACCEPTANCE NOT YET EXECUTED
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-05 — Whole-System Acceptance + Implementation Blueprint
- **Sub-phase:** AI-05A — Whole-System Build Boundary / Ownership Map
- **Established:** 2026-09-02
- **Upstream:** AI-02.1 / AI-03 / AI-04 / PRE-AI05 CLOSED / STRUCTURALLY ACCEPTED
- **Current core eval:** DANTE-E01..DANTE-E14
- **Implementation:** NONE
- **Provider/model/SDK selection:** OPEN
- **Database change:** NONE

AI-05A translates the accepted architecture into repository-real ownership and build boundaries. It is deliberately not production code and does not treat architecture nouns as automatic modules, services or tables.

---

# 1. Objective

AI-05 answers a different question from AI-02..04:

```text
AI-02..04
WHAT MUST BE TRUE

AI-05
HOW DOES THAT BECOME A BUILDABLE DANTE SYSTEM
WITHOUT WEAKENING THE ACCEPTED CONTRACTS?
```

AI-05A is the first step: decide where responsibilities belong and which things should **not** be materialized yet.

Primary acceptance question:

```text
Can the accepted DANTE intelligence architecture be implemented
inside the existing capability-first modular monolith
with bounded ports/adapters, minimal persistence and no provider lock-in,
without inventing parallel Domain/application authority?
```

---

# 2. Observed repository truth

Current branch-local backend source is intentionally foundation-heavy:

```text
apps/backend/src/dante/
├── __init__.py
├── bootstrap/
│   ├── __init__.py
│   ├── app.py
│   └── lifespan.py
└── platform/
    ├── config/
    ├── database/
    └── recovery/
```

Current materialized facts:

```text
bootstrap exists
platform/config exists
platform/database exists
platform/recovery exists
kernel does NOT yet exist
modules does NOT yet exist
provider/AI SDK dependency does NOT exist
tooling/ai-evals does NOT exist
production AI runtime does NOT exist
```

This matters. AI-05 must not draw a directory tree and then claim that the tree already exists.

The accepted application target remains:

```text
bootstrap = composition/lifecycle/inbound process host
kernel    = only proven small stable cross-capability primitives
platform  = bounded shared technical infrastructure
modules   = capability/application behavior and owned adapters
```

---

# 3. Build-boundary thesis

The strongest initial implementation posture is:

```text
DANTE INTELLIGENCE APPLICATION SEMANTICS
→ capability module ownership

CONCRETE PROVIDER SDK / PROTOCOL
→ outbound adapter

CONFIG / DB / OBSERVABILITY / SECURITY MECHANICS
→ bounded platform infrastructure where genuinely shared

WIRING / LIFECYCLE
→ bootstrap

DIRECT EVAL TOOLING
→ tooling, outside ordinary production runtime
```

Binding anti-patterns:

```text
NO giant platform/ai package owning product semantics
NO provider SDK in Domain/application meaning
NO one microservice per AI responsibility box
NO one Python module per WorkContract/ContextPlan/Run/etc.
NO generic shared/common/utils AI dumping ground
NO raw SQL/SQLAlchemy access from model reasoning
NO agent framework as semantic owner
NO gateway as mandatory architecture just because multiple providers exist
```

---

# 4. Candidate application owner — `modules/intelligence`

AI-05A proposes one initial capability module for DANTE-owned intelligence orchestration:

```text
apps/backend/src/dante/modules/intelligence/
```

This is a **candidate implementation boundary**, not a new Domain owner and not a claim that the folder exists today.

Its responsibility is the DANTE intelligence application contract:

```text
Work intake / WorkContract execution semantics
Run-local orchestration
Context planning / readiness orchestration
ModelTarget / deterministic route request
qualified route composition consumption
capability invocation orchestration
verification
result maturity
safe publication coordination
Attention/proactivity orchestration when activated
```

It does **not** own canonical business objects already owned by DANTE capabilities.

```text
INTELLIGENCE MODULE
!= canonical calendar/goals/people/health/work owner
!= SQLAlchemy model owner for the whole product
!= authorization authority
!= provider gateway product
!= conversation database
```

---

# 5. Candidate internal shape

The implementation should create folders only when real code needs them. A plausible first materialization is:

```text
modules/intelligence/
├── application/
│   ├── work/
│   ├── context/
│   ├── routing/
│   ├── capabilities/
│   ├── verification/
│   └── publication/
├── ports/
│   ├── model_access.py
│   ├── capability_access.py
│   ├── policy.py
│   └── telemetry.py          # only if a real seam is useful
├── adapters/
│   ├── inbound/http/
│   └── outbound/models/
└── public.py
```

Possible later folders are trigger-based:

```text
attention/       only when proactive/notification work is implemented
durability/      only when detached/Class-B work is implemented
execution/       only when browser/computer/code isolation is implemented
```

A `domain/` folder is **not automatically required** for the intelligence module. AI-02/03/04 runtime contracts are not permission to manufacture a second canonical Domain model.

---

# 6. Kernel posture

AI-05A does **not** place AI-specific contracts in `kernel/` by default.

```text
kernel small
kernel low-change
kernel proven cross-capability
```

`WorkContract`, `ContextPlan`, `ProviderBinding`, `HarnessProfile`, `Run`, `ContextManifest` and similar AI/runtime nouns remain inside the owning intelligence/application/control boundary unless later non-AI reuse proves a genuinely stable kernel primitive.

```text
USED IN MANY AI FILES
!= KERNEL PRIMITIVE
```

Existing accepted cross-capability reference semantics such as `NativeRef` / `MaterialStateRef` may eventually have small shared implementation value, but AI-05A does not force that extraction before real consumers exist.

---

# 7. Provider boundary

Concrete provider SDKs remain outbound adapters behind a DANTE-owned port.

Candidate shape:

```text
modules/intelligence/ports/model_access.py
        ↑
modules/intelligence/adapters/outbound/models/<provider>.py
        ↑
provider SDK / HTTP protocol
```

The port represents DANTE needs, not a lowest-common-denominator `generate(prompt)->str` abstraction.

It may eventually cover required DANTE semantics such as:

```text
invoke
stream
structured output
provider tool-call translation
cancellation
usage
provider-attempt identity
classified errors / acceptance uncertainty
feature capability description
```

Exact method/class names are AI-05B implementation work.

```text
PROVIDER SDK
!= APPLICATION CONTRACT
```

No LiteLLM/Portkey/provider gateway is required initially. A gateway becomes eligible only if measured multi-provider operational value exceeds the extra control/data-path complexity.

---

# 8. Route composition / control configuration

Accepted route semantics remain:

```text
WorkContract + current consequence/eligibility
→ ModelTarget / deterministic need
→ eligible qualified route compositions
→ Routing Policy
→ compatible HarnessProfile + ProviderBinding + feature/control composition
→ route-specific admission
→ current egress authorization
→ provider adapter
```

AI-05A candidate implementation posture:

```text
STATIC / VERSIONED / TYPED FIRST
DYNAMIC CONTROL PLANE ONLY WHEN OPERATIONAL NEED PROVES IT
```

Initial registries may be immutable process configuration/versioned package data for:

```text
ModelTarget definitions
HarnessProfile definitions
ProviderBinding definitions
route-policy rules
feature/capability profiles
qualification references
```

Secrets, endpoint credentials and deployment-only values remain in the existing typed config/secret boundary, not in Domain data or committed registry payloads.

A future mutable admin/control plane may replace the static source without changing the semantic contracts.

```text
CONTROL PLANE RESPONSIBILITY
!= CONTROL PLANE DATABASE REQUIRED ON DAY ONE
```

---

# 9. Platform ownership

Use `platform/` only for shared technical mechanics that remain meaningful outside one capability module.

Candidate AI-related platform additions only when implementation requires them:

```text
platform/config/intelligence.py
→ deployment-only typed configuration / secret references

platform/observability/
→ shared telemetry implementation once that platform boundary is materialized

platform/security/
→ shared security/runtime identity mechanics when materialized
```

Do not create:

```text
platform/ai/domain
platform/ai/business_rules
platform/ai/conversation_truth
platform/ai/all_tools
```

The intelligence module consumes platform mechanics; platform does not become the owner of DANTE intelligence/product semantics.

---

# 10. Bootstrap ownership

`bootstrap/` owns concrete composition and lifecycle resources.

When the first AI vertical is implemented, bootstrap may need a real `wiring.py` or equivalent composition boundary to construct:

```text
intelligence application service/facade
provider adapter(s)
qualified registry/config snapshot
capability/public-query adapters
policy/security adapters
telemetry adapter
```

FastAPI route registration remains inbound composition, not application orchestration.

```text
BOOTSTRAP WIRES
BOOTSTRAP DOES NOT BECOME THE AI SERVICE LAYER
```

---

# 11. Capability / semantic-query integration

The intelligence module may not bypass capability ownership by reading arbitrary business tables directly.

Preferred dependency:

```text
Intelligence application
→ narrow capability/public query or command interface
→ owning capability application semantics
→ persistence adapter / PostgreSQL
```

For Global Search/Ask DANTE this means the implementation depends on permission-aware application/search projections rather than `model -> SQL`.

A generic Semantic Query / Projection Gateway is an orchestration responsibility, but its concrete implementation should compose real use-case-shaped public query contracts instead of becoming a universal Entity API.

```text
SEMANTIC QUERY GATEWAY
!= RAW SQL TOOL FOR MODEL
!= UNIVERSAL CRUD API
```

If a required capability module/public query contract does not yet exist at implementation time, AI code must not compensate by reaching into its private tables. The dependency is recorded and implemented at the owning application boundary.

---

# 12. Capability Runtime

A model/provider tool request becomes a DANTE capability request only after DANTE translation and validation.

Candidate path:

```text
provider/model tool request
→ provider adapter normalization
→ typed DANTE CapabilityRequest
→ capability registry / lookup
→ schema + semantic validation
→ current policy / Authority / AuthZ / Consent / Visibility
→ target resolution + expected-state checks where applicable
→ owning application/public capability
→ receipt
→ verifier / reconciliation
```

Capability definitions should expose only bounded application operations. SQLAlchemy models, raw sessions, secret-bearing clients and arbitrary Python callables are not capability contracts.

---

# 13. Auth / Actor boundary

AI-05A consumes the already accepted distinction:

```text
Person != Account != Principal != Actor
```

The intelligence application receives a resolved current security/agency context through an application/security boundary. It does not infer:

```text
actor_id = account_id
```

and does not own identity-provider/session validation.

Consequential work must carry current Actor/represented-party/purpose/governance meaning into `WorkContract` and later revalidation boundaries.

Exact Auth implementation remains outside this branch scope; the dependency contract is binding.

---

# 14. Runtime-only vs persistence classification

Default posture remains AI-03C:

```text
DEFAULT NONCANONICAL PERSISTENCE = NO
ARCHITECTURE CONTRACT != PERSISTENCE OWNER
```

Initial classification candidate:

| Contract / state | Default survival | Initial owner / mechanism |
|---|---|---|
| `WorkContract` | request/run-local | intelligence application |
| `Run` inline state | request/run-local | process task/runtime |
| `InteractionSession` AI continuation | no generic server persistence by default | product/interaction requirement if later justified |
| `ContextPlan` / `InformationNeed` | ephemeral | intelligence application |
| `ContextFragment` / `ContextReadiness` | ephemeral | intelligence application |
| `ConsumerContext` | ephemeral | intelligence application/provider boundary |
| `ContextManifest` | ephemeral by default; evidence-gated | runtime/evidence only if required |
| `BasisManifest` | ephemeral by default; evidence-gated | runtime/evidence only if required |
| `ModelTarget` / `HarnessProfile` / `ProviderBinding` | versioned config | static typed registry first |
| provider attempt / token usage | operational evidence | telemetry/eval, not canonical Domain |
| direct eval fixtures/results | durable engineering evidence | `tooling/ai-evals` / CI artifact / accepted docs summary |
| commercial entitlement | external input | commercial/product owner, not intelligence ownership |
| Attention aggregate state | no persistence until proactive need proves it | trigger-gated |
| prior-disclosure accounting | minimum technical state only if threat model requires | trigger-gated security persistence |
| embeddings/indexes | no materialization until retrieval consumer proves need | trigger-gated derived state |
| durable Class-B Run state | no activation until qualifying workflow | Restate target when triggered |
| object bytes | no AI-specific activation | R2 only for real ContentArtifact flow |

This table is a build candidate, not a persistence migration authorization.

---

# 15. First vertical candidate

AI-05A recommends the first AI implementation vertical be:

```text
GLOBAL SEARCH / ASK DANTE
READ-ONLY ANSWER
+ CANONICAL NAVIGATION
+ SOURCE / PROVENANCE DISCLOSURE
+ NO CONSEQUENTIAL MUTATION
```

Why this is the strongest first slice:

1. it is already an accepted V1 product capability;
2. it exercises real DANTE-native semantic query rather than a demo chatbot;
3. it exercises `WorkContract`, target/reference resolution, Context, Basis, routing, model access, verifier, Result Maturity and Safe Publication;
4. it can prove deterministic/no-model fast paths alongside model-assisted paths;
5. it supports current/history/absence semantics and source/provenance display;
6. it avoids making the first provider integration depend on consequential effect/approval/reconciliation complexity;
7. it can start without conversation persistence, embeddings, Restate, R2, MCP/A2A or an Execution Environment;
8. it gives DANTE-E01/E02/E04/E05/E07/E12/E13 meaningful real coverage early.

The first slice should remain useful when the model is unavailable for deterministic supported queries.

---

# 16. First vertical boundaries

Initial supported behavior candidate:

```text
structured/keyword/native query
→ deterministic result where sufficient

natural-language question requiring interpretation/synthesis
→ governed intelligence route
→ permission-aware capability/public queries
→ bounded Context
→ answer with source/provenance/currentness semantics
```

Initial non-goals:

```text
no automatic mutation
no autonomous scheduling
no background agent
no persistent generic conversation history
no provider-native memory as continuity authority
no semantic/vector retrieval unless exact/structured baseline proves insufficient
no external web research unless explicitly activated as a later slice
```

A UI may still navigate to canonical objects from results.

---

# 17. Why planning is second, not first

Next candidate vertical after read-only Search/Ask DANTE:

```text
PLANNING / REPLANNING / SCENARIO PROPOSAL
NO AUTOMATIC EFFECT
```

This adds:

```text
Scenario Workspace
capacity/constraint reasoning
solver where justified
ChangeSet proposal
preview
approval binding
```

without yet requiring automatic consequential dispatch.

Only after that should a bounded mutation vertical activate full Effect Runtime, effect idempotency, approval/revalidation and reconciliation end to end.

---

# 18. Proactivity is later activation

Proactive watches/Attention are accepted architecture but should not be the first AI integration slice.

They require additional evidence around:

```text
trigger authenticity/currentness
material-delta detection
AttentionBudget
causal-loop/oscillation control
notification transport truth
cross-Run lifecycle
possibly durable technical state
```

`DANTE-E14` must be executable before proactive production activation.

---

# 19. Eval implementation boundary

AI-04A eval semantics do not belong inside the production request path.

Candidate repository boundary:

```text
tooling/ai-evals/
├── fixtures/
├── graders/
├── candidates/
├── runners/
└── results/ or CI-artifact references
```

Exact structure is AI-05B/tooling implementation work. The important rule is:

```text
DANTE EVAL SEMANTICS
!= PRODUCTION RUNTIME SEMANTICS
!= THIRD-PARTY EVAL RUNNER SEMANTICS
```

Direct paid/stochastic provider evals stay out of ordinary backend unit/integration CI by default.

Backend tests still own deterministic runtime/adapter contracts with fakes/stubs.

---

# 20. Testing placement candidate

```text
apps/backend/tests/unit/
→ pure WorkContract/context/routing/policy/verification behavior

apps/backend/tests/integration/
→ module wiring, provider adapter contract with fake/local transport,
   real PostgreSQL through owning capability boundaries when applicable

apps/backend/tests/
→ process/bootstrap/config contracts where appropriate

tooling/ai-evals/
→ DANTE-E01..E14 direct/stochastic candidate qualification

tests/system/
→ true Web/backend/streaming/end-to-end black-box cases only once real cross-app surface exists
```

Architecture tests must prevent Domain/application code from depending directly on provider SDKs and prevent intelligence code from importing private persistence adapters of other capability modules.

---

# 21. Dependency posture

Current backend dependencies contain no AI/provider SDK. AI-05A treats that as correct until a provider is selected.

Do not add:

```text
OpenAI SDK
Anthropic SDK
Google SDK
LangChain/LangGraph
agent gateway
AI eval SaaS SDK
```

merely to scaffold abstractions.

A selected provider adapter adds only the dependencies required by that adapter. Provider/runtime helper frameworks remain replaceable implementation aids and may not own DANTE semantics.

---

# 22. Streaming / transport posture

AI-05A does not yet select SSE vs WebSocket/realtime transport.

The architecture already requires:

```text
RAW PROVIDER EVENT
!= DANTE RUNTIME EVENT
!= RECIPIENT PUBLICATION EVENT
```

AI-05B must choose the simplest transport that satisfies the first real vertical. Voice/realtime needs must not force a bidirectional transport into an ordinary text/search path prematurely.

---

# 23. Implementation sequence candidate

```text
I0  repository/application ownership skeleton
    only folders/contracts required by first vertical

I1  pure intelligence contracts + fake model/capability adapters
    WorkContract / Context / routing / verification / publication

I2  first permission-aware capability/public-query dependencies
    deterministic Global Search path

I3  provider-neutral ModelAccessPort + one concrete adapter
    only after provider choice becomes decision-critical

I4  direct DANTE provider eval tooling / qualification
    E01..E14 applicable subset + hard gates

I5  read-only Ask DANTE vertical
    model-assisted query/synthesis + provenance/currentness

I6  production-hardening of the first vertical
    observability / privacy / retries / fallback / load / cost / release gates

I7  planning/scenario proposal vertical

I8  first bounded consequential effect vertical

I9  proactivity/background/durable/external-agent capabilities
    only as their triggers become real
```

The exact split may change after destructive acceptance; dependency direction may not.

---

# 24. Direct-proof activation map candidate

Examples:

```text
provider/model selection
→ direct DANTE eval required

production provider route
→ binding/security/data/economics/capacity qualification

FTS/pg_trgm/vector retrieval activation
→ actual retrieval need + SC/PSV direct proof

pgvector / ANN
→ exact baseline insufficient + recall/permission/freshness evidence

Restate
→ first real Class-B durable workflow

R2
→ real ContentArtifact byte flow

MCP
→ real external capability client/server integration

A2A
→ real independent external-agent collaboration

Execution Environment
→ generated/untrusted/browser/computer/code workload threat-model trigger

prior-disclosure persistence
→ material cross-work disclosure threat requiring bounded accounting

dynamic control-plane database/admin UI
→ operational change frequency/rollout need that static versioned config cannot satisfy
```

---

# 25. AI-05A candidate invariants

```text
BD-01  REPOSITORY-REAL OWNERSHIP PRECEDES FOLDER CREATION.
BD-02  RESPONSIBILITY BOUNDARY != MODULE != SERVICE != TABLE.
BD-03  DANTE INTELLIGENCE APPLICATION SEMANTICS BELONG IN A CAPABILITY/APPLICATION BOUNDARY, NOT GENERIC PLATFORM INFRASTRUCTURE.
BD-04  `modules/intelligence` IS A CANDIDATE ORCHESTRATION OWNER, NOT A NEW CANONICAL DOMAIN ROOT.
BD-05  PROVIDER SDK OBJECTS STAY BEHIND OUTBOUND ADAPTERS.
BD-06  PROVIDER ADAPTER != PROVIDER-NEUTRAL DANTE SEMANTICS.
BD-07  NO PROVIDER GATEWAY IS REQUIRED BEFORE MEASURED VALUE EXISTS.
BD-08  AI-SPECIFIC CONTRACTS DO NOT ENTER `kernel/` WITHOUT PROVEN STABLE CROSS-CAPABILITY VALUE.
BD-09  INTELLIGENCE MAY NOT BYPASS CAPABILITY OWNERSHIP THROUGH RAW BUSINESS-TABLE ACCESS.
BD-10  SEMANTIC QUERY/PROJECTION != UNIVERSAL ENTITY/CRUD/SQL TOOL.
BD-11  CAPABILITY REQUEST != PROVIDER TOOL CALL.
BD-12  BOOTSTRAP WIRES; IT DOES NOT OWN AI ORCHESTRATION.
BD-13  PLATFORM OWNS SHARED TECHNICAL MECHANICS ONLY, NOT INTELLIGENCE BUSINESS/WORK SEMANTICS.
BD-14  STATIC VERSIONED TYPED CONTROL CONFIG IS THE V1 DEFAULT UNTIL DYNAMIC CONTROL-PLANE NEED IS PROVEN.
BD-15  CONTROL-PLANE RESPONSIBILITY != CONTROL-PLANE DATABASE REQUIRED.
BD-16  DEFAULT NONCANONICAL AI PERSISTENCE REMAINS NO.
BD-17  FIRST READ-ONLY VERTICAL SHOULD REQUIRE ZERO NEW AI TABLES UNLESS A CONCRETE EVIDENCE OBLIGATION PROVES OTHERWISE.
BD-18  EVAL TOOLING IS OUTSIDE THE ORDINARY PRODUCTION REQUEST PATH.
BD-19  DIRECT PAID/STOCHASTIC PROVIDER EVAL != ORDINARY BACKEND CI.
BD-20  FIRST PROVIDER INTEGRATION MUST PRESERVE A REAL NO-MODEL/DETERMINISTIC PATH.
BD-21  FIRST VERTICAL SHOULD MAXIMIZE ARCHITECTURE COVERAGE WHILE MINIMIZING IRREVERSIBLE EFFECT RISK.
BD-22  GLOBAL SEARCH / ASK DANTE READ-ONLY + PROVENANCE IS THE CURRENT FIRST-VERTICAL CANDIDATE.
BD-23  PLANNING/SCENARIO PROPOSAL PRECEDES GENERAL AUTONOMOUS MUTATION.
BD-24  PROACTIVITY/DURABILITY/EXTERNAL-AGENT/ISOLATION TECHNOLOGIES ACTIVATE ONLY ON THEIR ACCEPTED TRIGGERS.
BD-25  COMMERCIAL ENTITLEMENT IS AN INPUT TO INTELLIGENCE, NOT SUBSCRIPTION OWNERSHIP BY THE INTELLIGENCE MODULE.
BD-26  CONVERSATION HISTORY DOES NOT GET A GENERIC PERSISTENCE MODEL UNTIL PRODUCT SEMANTICS REQUIRE IT.
BD-27  AUTHENTICATED ACCOUNT/PRINCIPAL ID IS NOT SILENTLY REUSED AS ACTOR/REPRESENTED-PARTY IDENTITY.
BD-28  RESULT PROVENANCE/CURRENTNESS IS PART OF THE FIRST VERTICAL CONTRACT, NOT OPTIONAL UI DECORATION.
BD-29  A FRAMEWORK MAY HELP EXECUTE DANTE CONTRACTS; IT MAY NOT DEFINE OR REPLACE THEM.
BD-30  AI-05 IMPLEMENTATION BLUEPRINT MUST REMAIN BUILDABLE WITH ONE PRIMARY PROVIDER AND WITH LATER PROVIDER REPLACEMENT.
```

---

# 26. Destructive acceptance questions

AI-05A is **not closed** until at least the following are attacked:

```text
T01 Can `modules/intelligence` become an accidental god-module?
T02 Does any accepted responsibility actually belong to platform/kernel instead?
T03 Does first vertical secretly require business-table access because capability APIs are absent?
T04 Can deterministic search work without initializing model/runtime complexity?
T05 Can provider replacement happen without rewriting application behavior?
T06 Does HarnessProfile/ProviderBinding static config become hidden environment-variable business logic?
T07 Can one-provider V1 remain simple without designing fake multi-provider runtime machinery?
T08 Does fake/no provider testing preserve realistic adapter semantics?
T09 Does read-only Ask DANTE really need zero new persistence?
T10 Do provenance/currentness/eval/audit requirements force a justified receipt store?
T11 Does cancellation/streaming force a Run registry or durable state earlier than expected?
T12 Does conversation UX force InteractionSession persistence earlier than expected?
T13 Can user/commercial quotas be consumed without the intelligence module owning subscription truth?
T14 Can cumulative disclosure be safe in the first private read-only surface without H19 durable accounting?
T15 Can first vertical exclude sensitive/shared surfaces honestly rather than pretending full coverage?
T16 Do target-resolution/history/absence semantics remain application-owned through the query boundary?
T17 Can first vertical operate safely during provider outage using deterministic routes?
T18 Does planning second require Scenario persistence, or can it remain bounded runtime state?
T19 Does a future consequential effect reuse owning application use cases rather than duplicate mutation logic?
T20 Can provider SDK/framework updates be isolated to adapters/harnesses and requalification?
T21 Can eval fixtures/graders remain reproducible without becoming runtime persistence?
T22 Can observability remain useful without exporting full prompts/context?
T23 Does direct provider qualification have a clear artifact home and promotion gate?
T24 Does the proposed sequence accidentally block future voice/MCP/A2A/background work?
T25 Can the architecture enforce import/dependency rules automatically once code exists?
T26 Is any new AI table/service/package being proposed merely because a noun exists?
```

Any real failure reopens only the smallest affected build boundary.

---

# 27. Current non-claims

```text
AI-05 ACTIVE                              YES
AI-05A CANDIDATE MATERIALIZED             YES
AI-05A DESTRUCTIVE ACCEPTANCE              NOT YET EXECUTED
AI-05A PASS/CLOSED                         NO
modules/intelligence IMPLEMENTED           NO
kernel CREATED                             NO
AI provider/model/SDK selected             NO
direct provider eval executed              NO
API/stream transport selected              NO
AI backend/frontend implemented            NO
new PostgreSQL/Alembic change              NO
new AI table/index                         NO
conversation persistence selected          NO
control-plane persistence selected         NO
FTS/vector/pgvector activated              NO
Restate/R2/MCP/A2A activated               NO
Execution Environment selected             NO
commercial pricing/billing implemented     NO
```

---

# 28. Next exact action

```text
READ BACK AI-05A CANDIDATE
→ run destructive buildability/minimality tests T01..T26
→ compare against accepted AI-02/03/04/PRE-AI05 in both directions
→ harden only demonstrated gaps
→ then decide whether AI-05A can close
```

Only after AI-05A acceptance should AI-05B freeze concrete ports/classes/config artifacts/API/streaming/persistence/proof sequence.