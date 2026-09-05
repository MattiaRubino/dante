# DANTE AI-05A — Whole-System Build Boundary Candidate

- **Status:** CANDIDATE / FIRST DESTRUCTIVE PASS FAIL BOUNDED / FRESH RETEST REQUIRED
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-05 — Whole-System Acceptance + Implementation Blueprint
- **Sub-phase:** AI-05A — Whole-System Build Boundary / Ownership Map
- **Established:** 2026-09-02
- **Upstream:** AI-02.1 / AI-03 / AI-04 / PRE-AI05 CLOSED / STRUCTURALLY ACCEPTED
- **Current core eval:** DANTE-E01..DANTE-E14
- **Implementation:** NONE
- **Provider/model/SDK selection:** OPEN
- **Database change:** NONE
- **First destructive pass:** FAIL BOUNDED / BD-31..BD-40 ADDED

AI-05A translates the accepted architecture into repository-real ownership and build boundaries. It is deliberately not production code and does not treat architecture nouns as automatic modules, services or tables.

The first destructive `T01..T26` pass found five coupled implementation-boundary gaps: Search was too easily absorbed into Intelligence, cross-capability read projection ownership was underspecified, resource admission/settlement had no explicit consuming seam, static control configuration could be misread as environment-variable behavior policy, and the first-vertical zero-persistence claim lacked a sufficiently explicit activation envelope. `BD-31..BD-40` harden those joins. No PASS is claimed until a fresh full retest runs from zero.

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

GLOBAL SEARCH / DISCOVERY SEMANTICS
→ separate shared read/search capability ownership

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
NO requirement to materialize all future product capability modules before first useful search/read slice
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
ModelTarget / deterministic-vs-model route request
qualified route composition consumption
model-assisted capability invocation orchestration
verification
result maturity
safe publication coordination
Attention/proactivity orchestration when activated
```

It does **not** own canonical business objects already owned by DANTE capabilities and, after the first destructive pass, it explicitly does **not** own the product's deterministic Global Search capability.

```text
INTELLIGENCE MODULE
!= canonical calendar/goals/people/health/work owner
!= Global Search canonical/read-projection owner
!= SQLAlchemy model owner for the whole product
!= authorization authority
!= provider gateway product
!= conversation database
```

`modules/intelligence` is therefore an orchestration/application boundary around replaceable intelligence, not the place where every cross-cutting DANTE feature is collected.

---

# 5. Separate shared Search capability

The accepted Product/Search contract is broader than chat or assistant behavior. Search must remain useful for structured filtering, lexical/current/history discovery, canonical navigation and deterministic results when no model is available.

AI-05A therefore separates:

```text
modules/search
!=
modules/intelligence
```

Candidate Search responsibility:

```text
permission/disclosure-aware discovery
structured filtering
keyword/lexical search when activated
current vs historical qualification
absence/search-miss semantics
safe snippets/facets/counts/ranking
canonical/source navigation references
source/material-basis/currentness metadata
```

Search does **not** own the searched canonical semantics and does not perform arbitrary mutations.

```text
SEARCH RESULT / RANK / INDEX
!= CANONICAL TRUTH
!= DOMAIN OWNER
!= AUTHORITY
```

The first vertical can therefore compose:

```text
native Search request
→ modules/search
→ deterministic result

Ask DANTE question
→ modules/intelligence
→ modules/search public query surface + other bounded sources
→ optional governed model route
→ verified/safe answer
```

This preserves Global Search as a shared product capability rather than a hidden implementation detail of the assistant.

---

# 6. Search cross-capability read projection

The current repository has a canonical PostgreSQL database but has not yet materialized all future `modules/<capability>` application owners. AI-05A must not create the impossible prerequisite that every future capability module be implemented before Global Search can read anything.

A Search capability may therefore own a **read-only cross-capability projection/query adapter** whose purpose is explicitly search/discovery.

Candidate path:

```text
modules/search/application
        ↓ search-owned read/query port
modules/search/adapters/outbound/persistence
        ↓ reviewed SQLAlchemy Core / explicit SQL where clearest
canonical PostgreSQL
```

Binding limits:

```text
SEARCH CROSS-CAPABILITY READ PROJECTION
!= CANONICAL BUSINESS OWNER
!= GENERIC Repository[T]
!= UNIVERSAL Entity API
!= RAW MODEL SQL TOOL
!= MUTATION BYPASS
```

The adapter may read the exact canonical/material-history tables required by an accepted searchable family, but it must encode the Search contracts for:

```text
permission / disclosure eligibility
hidden-result non-interference
current vs historical semantics
search miss != canonical nonexistence
source/reference/material-basis traceability
safe snippet/facet/count/ranking behavior
```

As real capability modules/public read interfaces emerge, Search may consume them where that better preserves ownership or reuse. That evolution must not change Search result semantics or grant the model direct persistence access.

Consequential commands initiated from a search result always leave Search and enter the owning application use case/effect governance boundary.

---

# 7. Candidate Intelligence internal shape

The implementation should create folders only when real code needs them. A plausible first Intelligence materialization is:

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
│   ├── search_access.py       # narrow consumer seam to Search/public query capability
│   ├── capability_access.py
│   ├── policy.py
│   ├── resource_control.py    # conceptual admission/settlement seam; exact API deferred
│   └── telemetry.py           # only if a real seam is useful
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

Exact filenames/classes are AI-05B work. The ownership and dependency direction are the AI-05A concern.

---

# 8. Kernel posture

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

# 9. Provider boundary

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

# 10. Provider test levels

Application/runtime tests and provider qualification are different evidence planes.

```text
DANTE APPLICATION TEST FAKE
!= PROVIDER ADAPTER CONFORMANCE TEST
!= LIVE PROVIDER SMOKE/COMPATIBILITY PROOF
!= DANTE DIRECT MODEL/ROUTE EVAL
!= PRODUCTION CAPACITY QUALIFICATION
```

Initial pure application tests may use a deterministic fake implementing the DANTE-owned `ModelAccessPort`.

After a concrete provider is selected, the adapter additionally requires protocol/SDK-specific contract tests that exercise material request, structured-output, stream, tool-call, cancellation, usage and error/acceptance-uncertainty translation behavior. These may use controlled fake HTTP/provider fixtures where appropriate.

Decision-critical provider/model quality is still earned through DANTE direct evals. Production route activation still requires the AI-04 qualification/capacity gates. A fake port implementation can never prove provider semantics by itself.

---

# 11. Route composition / behavior-bearing control configuration

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

AI-05A candidate implementation posture remains:

```text
STATIC / VERSIONED / TYPED FIRST
DYNAMIC CONTROL-PLANE STORAGE ONLY WHEN OPERATIONAL NEED PROVES IT
```

But the first destructive pass hardens what “static” means.

Behavior-bearing definitions such as:

```text
ModelTarget definitions
HarnessProfile definitions
ProviderBinding compatibility metadata
route-policy rules
feature/capability profiles
qualification references
control-profile references
```

must live in a versioned, reviewable, typed artifact/configuration source with identifiable immutable revision semantics.

```text
BEHAVIOR-BEARING ROUTE / HARNESS / POLICY CONFIG
!= SCATTERED ENVIRONMENT VARIABLES
```

Deployment environment may supply only appropriate deployment/runtime concerns such as:

```text
active approved revision/selector where applicable
endpoint/deployment locator
region
secret/credential reference
operational feature/kill selector where approved
resource/environment-specific limits
```

It must not silently become a second unreviewed business/intelligence policy language.

Before one logical ModelInvocation starts, DANTE resolves a coherent approved configuration snapshot. That snapshot remains identifiable for evidence/reproducibility through the invocation.

```text
COHERENT INVOCATION CONFIG SNAPSHOT
!= PERPETUAL AUTHORIZATION
!= IMMUNITY FROM CURRENT EMERGENCY DENY
```

The exact active-pointer, rollout, canary and emergency-disable mechanism remains implementation work. A production route may not activate until the selected mechanism satisfies AI-04C lifecycle/rollout/emergency-control requirements. If static/release configuration cannot satisfy the required production control, that deficiency itself triggers a bounded dynamic control mechanism before production activation.

```text
CONTROL PLANE RESPONSIBILITY
!= CONTROL PLANE DATABASE REQUIRED ON DAY ONE
```

---

# 12. Resource admission / usage settlement boundary

AI-04 requires route-specific resource admission and eventual usage settlement, but the Intelligence module must not become the owner of commercial subscription or shared usage ledgers.

Binding ownership:

```text
INTELLIGENCE
→ requests estimate / admission / reservation / settlement

RESOURCE / COMMERCIAL AUTHORITY
→ owns applicable durable shared budget/quota/metering truth

PROVIDER ADAPTER
→ reports provider usage/evidence
→ does NOT decide commercial entitlement
```

Conceptually:

```text
eligible candidate route
→ route-specific resource estimate
→ Resource Admission boundary
→ bounded reservation where required
→ provider/tool execution
→ actual usage evidence
→ Usage Settlement boundary
```

Exact port names and the future commercial/resource owner are not selected here.

```text
ENTITLEMENT INPUT
!= INTELLIGENCE OWNS SUBSCRIPTION
COMMERCIAL QUOTA
!= PROVIDER QUOTA
!= PLATFORM CAPACITY
```

A first technical slice may run without production commercial metering if commercial packaging is not yet activated. Once a shared/monthly/commercial quota is enforced across requests, the necessary durable accounting must be owned and tested by its proper commercial/resource boundary, not hidden in model routing or provider adapter state.

---

# 13. Platform ownership

Use `platform/` only for shared technical mechanics that remain meaningful outside one capability module.

Candidate AI-related platform additions only when implementation requires them:

```text
platform/config/intelligence.py
→ deployment-only typed configuration / secret references / approved config selector

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

The intelligence/search modules consume platform mechanics; platform does not become the owner of DANTE intelligence/product/search semantics.

---

# 14. Bootstrap ownership

`bootstrap/` owns concrete composition and lifecycle resources.

When the first AI vertical is implemented, bootstrap may need a real `wiring.py` or equivalent composition boundary to construct:

```text
Search application/public surface
Intelligence application service/facade
provider adapter(s)
qualified registry/config snapshot source
capability/public-query adapters
policy/security adapters
resource-control adapter
telemetry adapter
```

FastAPI route registration remains inbound composition, not application orchestration.

```text
BOOTSTRAP WIRES
BOOTSTRAP DOES NOT BECOME THE AI SERVICE LAYER
```

---

# 15. Capability / semantic-query integration

The model/intelligence runtime may not bypass capability/search ownership by reading arbitrary business tables directly.

Preferred dependencies are:

```text
Intelligence application
→ modules/search public query surface
→ permission-safe search projection

and, for non-search capability needs:

Intelligence application
→ narrow owning capability public query/command interface
→ owning capability application semantics
```

The dedicated Search read projection in section 6 is an explicit cross-cutting read capability, not an exception allowing arbitrary Intelligence-table access.

A generic Semantic Query / Projection Gateway remains an orchestration responsibility, but its concrete implementation composes real Search/capability query contracts instead of becoming a universal Entity API.

```text
SEMANTIC QUERY GATEWAY
!= RAW SQL TOOL FOR MODEL
!= UNIVERSAL CRUD API
```

If a required mutation capability/public command contract does not exist at implementation time, AI code must not compensate by reaching into private persistence. It is implemented at the owning application boundary.

---

# 16. Capability Runtime

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

For the first read-only Search/Ask vertical, consequential mutation capabilities are not exposed.

---

# 17. Auth / Actor boundary

AI-05A consumes the already accepted distinction:

```text
Person != Account != Principal != Actor
```

The intelligence/search application receives a resolved current security/agency context through an application/security boundary. It does not infer:

```text
actor_id = account_id
```

and does not own identity-provider/session validation.

Consequential work must carry current Actor/represented-party/purpose/governance meaning into `WorkContract` and later revalidation boundaries.

Exact Auth implementation remains outside this branch scope; the dependency contract is binding.

---

# 18. Runtime-only vs persistence classification

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
| Search result/projection | recomputable / request-scoped initially | Search capability; canonical source remains elsewhere |
| Search FTS/vector/index state | NOT ACTIVATED by AI-05A | trigger-gated derived retrieval |
| `ModelTarget` / `HarnessProfile` / `ProviderBinding` | versioned config | immutable typed registry/config first |
| coherent invocation config identity | request/invocation evidence | runtime snapshot/reference; persistence only if consequence/evidence requires |
| provider attempt / token usage | operational evidence | telemetry/eval, not canonical Domain |
| direct eval fixtures/results | durable engineering evidence | `tooling/ai-evals` / CI artifact / accepted docs summary |
| commercial entitlement | external input | commercial/product owner, not intelligence ownership |
| shared/commercial quota accounting | durable only when activated | proper resource/commercial authority, not Intelligence |
| Attention aggregate state | no persistence until proactive need proves it | trigger-gated |
| prior-disclosure accounting | minimum technical state only if threat model requires | trigger-gated security persistence |
| embeddings/indexes | no materialization until retrieval consumer proves need | trigger-gated derived state |
| durable Class-B Run state | no activation until qualifying workflow | Restate target when triggered |
| object bytes | no AI-specific activation | R2 only for real ContentArtifact flow |

This table is a build candidate, not a persistence migration authorization.

---

# 19. First vertical candidate

AI-05A recommends the first AI implementation vertical be a composition of two separately useful product capabilities:

```text
GLOBAL SEARCH
DETERMINISTIC / READ-ONLY / CANONICAL NAVIGATION

+

ASK DANTE
READ-ONLY MODEL-ASSISTED ANSWER WHEN NEEDED
+ SOURCE / PROVENANCE / CURRENTNESS
+ NO CONSEQUENTIAL MUTATION
```

Why this is the strongest first slice:

1. Global Search is already an accepted V1 product capability independent of chat;
2. deterministic Search exercises real DANTE-native discovery and remains useful without a model;
3. Ask DANTE exercises `WorkContract`, target/reference resolution, Context, Basis, routing, model access, verifier, Result Maturity and Safe Publication;
4. both paths preserve current/history/absence semantics and source/provenance disclosure;
5. the composition avoids making first provider integration depend on consequential effect/approval/reconciliation complexity;
6. it can start without generic conversation persistence, embeddings, Restate, R2, MCP/A2A or an Execution Environment;
7. it gives DANTE-E01/E02/E04/E05/E07/E12/E13 meaningful real coverage early;
8. model/provider outage does not take deterministic Search down with it.

---

# 20. First-vertical activation envelope

The zero-new-AI-table and inline-runtime posture applies only to an explicit first activation envelope.

Initial candidate:

```text
surface          private authenticated in-app
recipient        current resolved user/Actor context only
interaction      single-turn request/response semantics
reasoning        deterministic OR bounded model-assisted
durability       inline / request-owned
effect           read-only
topology         single or bounded sequential
latency          interactive
isolation        normal / no Execution Environment
external effects NONE
background work  NONE
durable resume   NONE
shared/lock/voice/external-recipient surfaces  OUT OF INITIAL ENVELOPE
```

A first transport may stream an inline response, but transport streaming does not by itself create durable Run/InteractionSession persistence or reconnect/resume semantics.

```text
INLINE STREAM
!= DURABLE RUN REGISTRY REQUIRED
```

If a product requirement later demands detached execution, reconnect/resume, cross-process cancellation, background waits or crash-safe continuation, the corresponding durability trigger is evaluated explicitly.

Single-turn initial UX does not prohibit later conversation continuity. It simply means:

```text
CHAT-LIKE UI
!= GENERIC CONVERSATION DATABASE REQUIRED ON DAY ONE
```

---

# 21. Cumulative disclosure / persistence activation gate

The private in-app/read-only label does not magically make cumulative disclosure safe.

The first activation envelope must therefore restrict source/sensitivity/policy cases to those for which current per-request publication policy can safely decide without durable cross-Run prior-exposure accounting.

```text
FIRST VERTICAL ZERO-ACCOUNTING ELIGIBLE CASE
→ current policy proves no H19 durable prior-exposure state is required

CASE REQUIRES CROSS-RUN / RELATED-SINK DISCLOSURE ACCOUNTING
→ not eligible for zero-persistence envelope
→ activate minimum justified H19 technical state first
   OR narrow/defer/deny the unsupported case safely
```

Similarly, if a specific read-only query requires durable audit/security evidence, that evidence requirement is implemented under its own evidence owner before the case becomes production-eligible.

```text
ZERO NEW AI TABLES
!= ZERO DURABLE TECHNICAL STATE FOREVER
```

The claim is only that the initial bounded read-only envelope does not itself justify generic AI persistence.

---

# 22. First vertical query behavior

Initial supported behavior candidate:

```text
structured/keyword/native query
→ modules/search deterministic result where sufficient

natural-language question requiring interpretation/synthesis
→ modules/intelligence governed route
→ permission-aware Search/public query dependencies
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
no semantic/vector retrieval unless exact/structured/lexical baseline proves insufficient
no external web research unless explicitly activated as a later slice
no shared/lock-screen/voice/external-recipient publication
```

A UI may navigate directly to canonical objects from Search/Ask results.

---

# 23. Why planning is second, not first

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

AI-03C remains binding:

```text
Scenario Workspace = runtime / NO-STORE by default
accepted saved scenario → promote to proper Possibility / Proposal / Plan / other accepted owner
```

Only after that should a bounded mutation vertical activate full Effect Runtime, effect idempotency, approval/revalidation and reconciliation end to end.

---

# 24. Proactivity is later activation

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

# 25. Eval implementation boundary

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

Qualification promotion must leave a durable engineering evidence reference identifying the material candidate configuration and result. The initial artifact home may be repository/CI evidence rather than a runtime database.

---

# 26. Testing placement candidate

```text
apps/backend/tests/unit/
→ pure WorkContract/context/routing/policy/resource/verification behavior

apps/backend/tests/integration/
→ Search read-projection behavior against real PostgreSQL where applicable
→ module wiring
→ provider adapter protocol contract with controlled provider fixtures after selection

apps/backend/tests/
→ process/bootstrap/config contracts where appropriate

tooling/ai-evals/
→ DANTE-E01..E14 direct/stochastic candidate qualification

tests/system/
→ true Web/backend/streaming/end-to-end black-box cases only once real cross-app surface exists
```

Architecture tests must prevent Domain/application code from depending directly on provider SDKs, prevent Intelligence from importing Search/private persistence adapters, prevent model code from seeing raw sessions/SQLAlchemy objects, and preserve the public-module dependency rules.

---

# 27. Dependency posture

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

# 28. Streaming / transport posture

AI-05A does not yet select SSE vs WebSocket/realtime transport.

The architecture already requires:

```text
RAW PROVIDER EVENT
!= DANTE RUNTIME EVENT
!= RECIPIENT PUBLICATION EVENT
```

AI-05B must choose the simplest transport that satisfies the first real vertical.

For the initial activation envelope, a transport may be ordinary non-streaming HTTP or an inline server stream. Voice/realtime needs must not force a bidirectional transport or durable session registry into the ordinary Search/Ask path prematurely.

---

# 29. Implementation sequence candidate

The first destructive pass changes the initial sequence by making Search an independent prerequisite/capability rather than burying it inside Intelligence.

```text
I0  repository/application ownership skeleton
    create only the Search + Intelligence boundaries required by first slice

I1  Search application/read-projection contract
    permission/disclosure/current/history/source semantics
    deterministic structured/keyword baseline

I2  pure Intelligence contracts + fake ModelAccess
    WorkContract / Context / routing / verification / publication
    consume Search through public/query seam

I3  deterministic Global Search vertical
    private in-app / read-only / canonical navigation
    no provider dependency

I4  provider-neutral ModelAccessPort + one concrete adapter
    only after provider choice becomes decision-critical

I5  provider adapter conformance + direct DANTE eval tooling / qualification
    applicable E01..E14 subset + hard gates

I6  read-only Ask DANTE vertical
    model-assisted query/synthesis + provenance/currentness

I7  production hardening of Search/Ask
    observability / privacy / resource control / retries / fallback / load / cost / release gates

I8  planning/scenario proposal vertical

I9  first bounded consequential effect vertical

I10 proactivity/background/durable/external-agent capabilities
    only as their triggers become real
```

The exact split may change after destructive acceptance; dependency direction may not.

---

# 30. Direct-proof activation map candidate

Examples:

```text
provider/model selection
→ direct DANTE eval required

production provider route
→ binding/security/data/economics/capacity qualification

Search hidden-result behavior
→ applicable SC-017 / PSV-06 direct proof before production scope relying on it

FTS/pg_trgm retrieval activation
→ actual lexical-search need + applicable SC/PSV direct proof

pgvector / ANN
→ exact/structured/lexical baseline insufficient + recall/permission/freshness evidence

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
→ operational change frequency/rollout need that static versioned config cannot safely satisfy

commercial/shared usage ledger
→ real cross-request quota/metering/billing requirement
```

---

# 31. AI-05A candidate invariants BD-01..BD-40

Original candidate invariants remain, with first-pass hardening appended.

```text
BD-01  REPOSITORY-REAL OWNERSHIP PRECEDES FOLDER CREATION.
BD-02  RESPONSIBILITY BOUNDARY != MODULE != SERVICE != TABLE.
BD-03  DANTE INTELLIGENCE APPLICATION SEMANTICS BELONG IN A CAPABILITY/APPLICATION BOUNDARY, NOT GENERIC PLATFORM INFRASTRUCTURE.
BD-04  `modules/intelligence` IS A CANDIDATE ORCHESTRATION OWNER, NOT A NEW CANONICAL DOMAIN ROOT.
BD-05  PROVIDER SDK OBJECTS STAY BEHIND OUTBOUND ADAPTERS.
BD-06  PROVIDER ADAPTER != PROVIDER-NEUTRAL DANTE SEMANTICS.
BD-07  NO PROVIDER GATEWAY IS REQUIRED BEFORE MEASURED VALUE EXISTS.
BD-08  AI-SPECIFIC CONTRACTS DO NOT ENTER `kernel/` WITHOUT PROVEN STABLE CROSS-CAPABILITY VALUE.
BD-09  INTELLIGENCE MAY NOT BYPASS CAPABILITY/SEARCH OWNERSHIP THROUGH RAW BUSINESS-TABLE ACCESS.
BD-10  SEMANTIC QUERY/PROJECTION != UNIVERSAL ENTITY/CRUD/SQL TOOL.
BD-11  CAPABILITY REQUEST != PROVIDER TOOL CALL.
BD-12  BOOTSTRAP WIRES; IT DOES NOT OWN AI ORCHESTRATION.
BD-13  PLATFORM OWNS SHARED TECHNICAL MECHANICS ONLY, NOT INTELLIGENCE BUSINESS/WORK/SEARCH SEMANTICS.
BD-14  STATIC VERSIONED TYPED CONTROL CONFIG IS THE V1 DEFAULT UNTIL DYNAMIC CONTROL-PLANE NEED IS PROVEN.
BD-15  CONTROL-PLANE RESPONSIBILITY != CONTROL-PLANE DATABASE REQUIRED.
BD-16  DEFAULT NONCANONICAL AI PERSISTENCE REMAINS NO.
BD-17  FIRST BOUNDED READ-ONLY VERTICAL SHOULD REQUIRE ZERO NEW GENERIC AI TABLES UNLESS A CONCRETE EVIDENCE/SURVIVAL REQUIREMENT PROVES OTHERWISE.
BD-18  EVAL TOOLING IS OUTSIDE THE ORDINARY PRODUCTION REQUEST PATH.
BD-19  DIRECT PAID/STOCHASTIC PROVIDER EVAL != ORDINARY BACKEND CI.
BD-20  FIRST PROVIDER INTEGRATION MUST PRESERVE A REAL NO-MODEL/DETERMINISTIC PATH.
BD-21  FIRST VERTICAL SHOULD MAXIMIZE ARCHITECTURE COVERAGE WHILE MINIMIZING IRREVERSIBLE EFFECT RISK.
BD-22  GLOBAL SEARCH + ASK DANTE READ-ONLY/PROVENANCE IS THE CURRENT FIRST-VERTICAL COMPOSITION CANDIDATE.
BD-23  PLANNING/SCENARIO PROPOSAL PRECEDES GENERAL AUTONOMOUS MUTATION.
BD-24  PROACTIVITY/DURABILITY/EXTERNAL-AGENT/ISOLATION TECHNOLOGIES ACTIVATE ONLY ON THEIR ACCEPTED TRIGGERS.
BD-25  COMMERCIAL ENTITLEMENT IS AN INPUT TO INTELLIGENCE, NOT SUBSCRIPTION OWNERSHIP BY THE INTELLIGENCE MODULE.
BD-26  CONVERSATION HISTORY DOES NOT GET A GENERIC PERSISTENCE MODEL UNTIL PRODUCT SEMANTICS REQUIRE IT.
BD-27  AUTHENTICATED ACCOUNT/PRINCIPAL ID IS NOT SILENTLY REUSED AS ACTOR/REPRESENTED-PARTY IDENTITY.
BD-28  RESULT PROVENANCE/CURRENTNESS IS PART OF THE FIRST VERTICAL CONTRACT, NOT OPTIONAL UI DECORATION.
BD-29  A FRAMEWORK MAY HELP EXECUTE DANTE CONTRACTS; IT MAY NOT DEFINE OR REPLACE THEM.
BD-30  AI-05 IMPLEMENTATION BLUEPRINT MUST REMAIN BUILDABLE WITH ONE PRIMARY PROVIDER AND WITH LATER PROVIDER REPLACEMENT.

BD-31  GLOBAL SEARCH / DISCOVERY != INTELLIGENCE ORCHESTRATION; SEARCH REMAINS A SEPARATELY USEFUL SHARED PRODUCT CAPABILITY.
BD-32  SEARCH MAY OWN A BOUNDED CROSS-CAPABILITY READ PROJECTION, BUT SEARCH DOES NOT OWN THE SEARCHED CANONICAL SEMANTICS OR MUTATIONS.
BD-33  DETERMINISTIC SEARCH MUST REMAIN OPERABLE WITHOUT INITIALIZING OR DEPENDING ON MODEL/PROVIDER ROUTES.
BD-34  RESOURCE ADMISSION / RESERVATION / SETTLEMENT IS AN EXPLICIT CONSUMED BOUNDARY; INTELLIGENCE DOES NOT OWN COMMERCIAL/SHARED USAGE LEDGER TRUTH.
BD-35  BEHAVIOR-BEARING ROUTE/HARNESS/POLICY CONFIG != SCATTERED ENVIRONMENT VARIABLES.
BD-36  STATIC-FIRST CONTROL CONFIG STILL REQUIRES IMMUTABLE REVISION IDENTITY, APPROVED ACTIVE SELECTION, COHERENT INVOCATION SNAPSHOT AND CURRENT EMERGENCY-DENY SEMANTICS BEFORE PRODUCTION ACTIVATION.
BD-37  FIRST-VERTICAL ZERO-PERSISTENCE CLAIM APPLIES ONLY TO AN EXPLICIT INLINE / SINGLE-TURN / PRIVATE-IN-APP / READ-ONLY ACTIVATION ENVELOPE.
BD-38  A CASE REQUIRING H19 CROSS-WORK DISCLOSURE ACCOUNTING, DURABLE AUDIT, RESUME/BACKGROUND OR OTHER SURVIVAL STATE IS NOT ELIGIBLE FOR THE ZERO-PERSISTENCE ENVELOPE UNTIL THAT MINIMUM STATE IS IMPLEMENTED.
BD-39  APPLICATION FAKE MODEL != PROVIDER ADAPTER CONFORMANCE != DIRECT DANTE MODEL/ROUTE EVAL != PRODUCTION CAPACITY QUALIFICATION.
BD-40  CHAT-LIKE PRESENTATION OR INLINE STREAMING != GENERIC CONVERSATION/INTERACTION/RUN PERSISTENCE REQUIRED.
```

---

# 32. Destructive acceptance questions T01..T26

The fresh retest restarts from zero. The same tests remain binding so hardening cannot hide a prior failure by changing the exam.

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
T10 Do provenance/currentness/eval/audit requirements force a receipt store?
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

Fresh PASS requires no unexplained ownership gap, no hidden mutation/data bypass, no fake zero-persistence claim, no provider lock-in and no architecture noun materialized solely because it exists.

---

# 33. First-pass verdict matrix

The first destructive pass is retained rather than rewritten as an earlier success.

```text
T01 FAIL BOUNDED → BD-31 / Search separated from Intelligence
T02 PASS CANDIDATE → platform/kernel boundaries remain bounded
T03 FAIL BOUNDED → BD-32 / explicit Search cross-capability read projection
T04 FAIL BOUNDED → BD-31..33 / deterministic Search independent of model runtime
T05 PASS CANDIDATE
T06 FAIL BOUNDED → BD-35..36 / config source + snapshot/lifecycle hardening
T07 PASS CANDIDATE
T08 FAIL BOUNDED / UNDER-SPECIFIED → BD-39 / fake vs adapter conformance vs live proof
T09 PASS ONLY INSIDE BOUNDED ENVELOPE → BD-37..38
T10 PASS ONLY INSIDE BOUNDED ENVELOPE → durable evidence still trigger-gated
T11 PASS ONLY FOR INLINE NON-RESUMABLE SLICE → BD-37 / BD-40
T12 PASS ONLY FOR SINGLE-TURN INITIAL UX → BD-40
T13 FAIL BOUNDED → BD-34 / explicit resource admission-settlement boundary
T14 FAIL BOUNDED → BD-37..38 / H19 requirement gates expansion
T15 PASS ONLY WITH EXPLICIT SURFACE/SENSITIVITY ENVELOPE → BD-37..38
T16 PASS CANDIDATE → Search/current/history/absence remain application semantics
T17 FAIL BOUNDED UNDER ORIGINAL OWNERSHIP → BD-31..33 restores deterministic availability
T18 PASS CANDIDATE → Scenario runtime/no-store default preserved
T19 PASS CANDIDATE
T20 PASS CANDIDATE after BD-39 test separation
T21 PASS CANDIDATE
T22 PASS CANDIDATE
T23 PASS CANDIDATE / exact qualification artifact schema deferred AI-05B
T24 PASS CANDIDATE
T25 PASS CANDIDATE / executable import enforcement remains implementation work
T26 PASS CANDIDATE
```

Because any bounded FAIL prevents closure, AI-05A remains candidate pending a fresh full retest.

---

# 34. Current non-claims

```text
AI-05 ACTIVE                              YES
AI-05A CANDIDATE MATERIALIZED             YES
FIRST T01..T26 DESTRUCTIVE PASS            FAIL BOUNDED
BD-31..BD-40 HARDENING                     MATERIALIZED
FRESH RETEST AFTER HARDENING               NOT YET EXECUTED
AI-05A PASS/CLOSED                         NO
modules/search IMPLEMENTED                 NO
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
commercial/resource ledger implemented     NO
FTS/vector/pgvector activated              NO
Restate/R2/MCP/A2A activated               NO
Execution Environment selected             NO
commercial pricing/billing implemented     NO
```

---

# 35. Next exact action

```text
READ BACK HARDENED AI-05A
→ restart T01..T26 from zero
→ run compound collisions:
   Search + Intelligence + provider outage
   Search hidden-result + Ask synthesis
   static config rollout + invocation snapshot + emergency deny
   quota admission + provider retry/failover + settlement
   inline stream + disconnect + no durable Run
   cumulative disclosure + zero-persistence activation envelope
→ reverse-check against AI-04/PRE-AI05/AI-03/AI-02
→ harden only newly demonstrated gaps
```

Only after a clean fresh retest may AI-05A close and AI-05B freeze concrete ports/classes/config artifacts/API/streaming/persistence/proof sequence.