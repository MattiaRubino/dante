# DANTE AI-02.1 — Intelligence Reengineering & Simulation Pressure-Test

- **Status:** ACTIVE / BRANCH-LOCAL ARCHITECTURE CHECKPOINT / NOT CLOSED
- **Workstream:** `feature/ai-architecture`
- **Established:** 2026-09-01
- **Phase:** AI-02.1
- **Scope:** pressure-test and reengineer the DANTE Intelligence Architecture against actual product obligations before AI-03
- **Implementation:** NOT STARTED by this document
- **Provider/model/SDK selection:** OPEN
- **Database evolution:** NONE AUTHORIZED BY THIS DOCUMENT
- **AI-03:** BLOCKED until AI-02.1 completes its remaining adversarial acceptance work

---

## 1. Purpose

AI-02.1 exists to answer a narrower and harder question than the previous AI research work:

> **Does the proposed DANTE Intelligence Architecture actually survive what DANTE must do in real life, under the already accepted Product, Domain, Logical, Physical and PostgreSQL contracts?**

This phase does not start from a preferred model, agent framework, provider, vector database or chat UI. It starts from product obligations and tries to break the architecture.

The method is deliberately adversarial:

```text
Product / North Star
+ single-user and cross-domain simulations
+ multi-actor simulations
+ accepted Domain semantics
+ Whole Logical Model / WL-H01..WL-H12
+ Physical / PostgreSQL authority
+ AI-00 semantic baseline
+ production AI / agent engineering research
        ↓
representative DANTE workloads
        ↓
end-to-end architecture pressure-test
        ↓
PASS / GAP / CONTRADICTION / OVER-ABSTRACTION
        ↓
smallest justified reengineering change
        ↓
repeat
```

This document records the current **v0.2 checkpoint after the first serious simulation pass**. It is not the final AI-02.1 closure record.

---

## 2. Authority and interpretation discipline

This document does not create a new Domain ontology and does not supersede closed Product/Domain/Logical/Physical/database authority.

Precedence remains:

```text
protected-main executable truth
→ accepted Product / Domain / Logical / Physical / ADR authority
→ current Database System of Record and engineering contracts
→ AI-00 semantic/architectural baseline
→ this AI-02.1 branch-local reengineering checkpoint
→ external research / simulation evidence
→ conversation memory
```

If a responsibility introduced here can be expressed using an existing accepted semantic family, the existing family remains the semantic owner.

Terms such as:

```text
Interaction Session
Semantic Query Gateway
Scenario Workspace
ChangeSet
Effect Graph
Attention Engine
Disclosure Projection
VerificationReceipt
HarnessProfile
```

are **architecture/runtime responsibility contracts unless another accepted source already defines an equivalent Domain concept**. They are not permission to create new canonical tables or generic semantic roots.

---

## 3. Source corpus

### Product / North Star

Primary product authority:

- `docs/product/product-identity-and-north-star.md`
- `docs/product/v1-adaptive-intelligence-and-future-social.md`
- `docs/product/v1-global-search-and-command.md`
- `docs/product/v1-execution-status.md`
- `docs/product/v1-confirmation-and-reminders.md`
- `docs/product/v1-goal-and-program-lifecycle.md`
- `docs/product/v1-scheduling-flexibility.md`
- `docs/product/v1-work-context-and-meeting-lifecycle.md`
- `docs/product/v1-user-context-and-safety.md`
- `docs/product/v1-data-history-and-privacy.md`
- `docs/product/v1-learning-context-and-ai-boundary.md`

Primary simulation evidence:

- `docs/product/feature-discovery-simulation-2026-08.md`
- `docs/product/multi-actor-collaboration-discovery-simulation-2026-08.md`
- `docs/product/multi-actor-collaboration-research-2026-08.md`

### Semantic / architecture authority

- `docs/domain/README.md`
- `docs/logical-model/README.md`
- `docs/logical-model/whole-logical-model-v1.md`
- `docs/physical-model/README.md`
- `docs/architecture/dante-ai-foundation.md`
- `docs/architecture/ai-production-engineering-state-of-the-art-2026.md`
- `docs/architecture/system-overview.md`

### Persistence authority

- `docs/database/README.md`
- `docs/database/dictionary/README.md`
- current Alembic / SQLAlchemy / PostgreSQL executable truth
- `docs/decisions/ADR-010-postgresql-persistence-constitution.md`

Simulation/research evidence may reveal an architectural gap. It does not silently rewrite an accepted semantic meaning.

---

## 4. Non-negotiable inherited invariants

AI-02.1 carries forward at least the following rules:

```text
DANTE != chatbot
DANTE != model
DANTE != provider
DANTE != chat transcript

MODEL != canonical truth
MODEL != authorization engine
MODEL != durable workflow engine
MODEL != database
MODEL != effect success

PostgreSQL = sole canonical persistence / material-history authority

Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
Responsibility != Participation

Possibility != Goal != Proposal != Decision != Plan != Activity
Occurrence != Schedule != Session != Actual
Actual != Observation != Outcome
Evidence != Provenance
Version != Reconciliation

AI inference != confirmed fact
AI confidence != Confirmation
provider state != canonical DANTE state
derived projection != canonical truth
absence / unknown != false

MaterialStateRef != provider revision / ETag / MVCC token
idempotency != semantic identity
search index != source of truth
telemetry != audit
```

No reengineering change in this phase is accepted if it obtains convenience by collapsing one of these distinctions.

---

## 5. Product capability obligations

The North Star expresses the non-mandatory operating idea:

```text
UNDERSTAND
→ DISCOVER
→ ORCHESTRATE
→ DECIDE
→ PLAN & COORDINATE
→ ACT
→ OBSERVE
→ LEARN & ADAPT
```

AI-02.1 translates that product language into architecture obligations without turning it into eight services or eight agents.

DANTE must be able to support, in combinations rather than isolation:

```text
natural-language understanding
structured DANTE-native query
open-world explanation / research
current-state and historical reasoning
permission-aware information access
deterministic calculation
constraint solving / scheduling
scenario simulation
multi-object replanning
proposal / decision support
governed mutation
external-provider effects
verification / reconciliation
proactivity / watches / scheduled work
long-running and durable work
multimodal / document / artifact flows
multi-actor / delegated / represented action
selective disclosure
uncertainty and conflicting evidence
learning without truth laundering
future model/provider replacement
```

A simple request must remain simple. The architecture must not require the expensive path merely because the platform can support the expensive path.

---

## 6. First simulation pressure-test summary

The first pass intentionally covered ordinary and structurally difficult cases.

| Scenario family | Result | Architectural consequence |
|---|---|---|
| deterministic historical question, e.g. monthly running total | PASS | model may be skipped; semantic query + deterministic compute is sufficient |
| simple natural-language command, e.g. create appointment | PASS | language interpretation must terminate in governed application operation |
| compare three realistic ways to add a new Goal | GAP FOUND | first-class hypothetical/simulation workspace required |
| illness week requiring selective pause/replan | GAP FOUND | compound governed ChangeSet / EffectGraph required |
| elapsed scheduled item with unknown outcome | PARTIAL | proactivity/attention responsibility required; elapsed time remains not completion |
| persistent unresolved work after chat closes | PASS WITH CLARIFICATION | persist through correct Domain semantics, not `AIReviewItem` or transcript ownership |
| imported professional/source document | PASS | artifact + provenance + candidate/acceptance path already fits |
| privacy-preserving coordination | GAP FOUND | recipient-aware Disclosure Projection must be distinct from Context Projection |
| caregiver / conflicting multi-actor evidence | PASS | existing Subject/Actor/Authority/Visibility/Reconciliation semantics survive |
| meeting transcript → decisions/commitments/tasks | PASS | extracted outputs remain candidates until resolved into existing semantic owners |
| provider timeout after external mutation attempt | PASS STRONG | outcome-unknown + verification/reconciliation remains required |
| multi-week proactive watch | PARTIAL | durable trigger/evaluation + attention policy required; model must not be the timer |
| future rich general-purpose conversation | GAP FOUND | Interaction Session + dual open-world/DANTE-native path must become first-class |
| stable structured access for future intelligence | GAP FOUND | Semantic Query / Projection Gateway required |

This scorecard does not close the phase. It records what the first pass taught us.

---

## 7. Reengineering decision 01 — Interaction Session is first-class

### Problem

`Session != Run != Worker` was already a production-engineering rule, but the future DANTE product requires a stronger user-facing interaction boundary.

A conversation may contain many pieces of work. A piece of work may outlive the conversation. A background run may later return into a conversation or another surface.

Therefore:

```text
Interaction Session != Run != Worker
```

### Interaction Session responsibility

An Interaction Session may own noncanonical interaction state such as:

```text
conversation turn continuity
current surface / presentation context
currently attached artifacts
temporary referents and conversational deixis
streaming presentation state
session-local user choices that have not been promoted elsewhere
```

It must not own canonical DANTE truth merely because that truth was discussed in the session.

### Required lifecycle

```text
Interaction Session
  ├─ Run A → completed
  ├─ Run B → completed
  ├─ Run C → suspended / durable
  └─ later Run D
```

A Run may finish while the Session continues.

A Run may survive the Session when the work has its own legitimate durable lifecycle, for example:

```text
research job
watch / condition monitoring
approval wait
booking workflow
external callback
```

Closing the UI surface must not silently cancel work unless the work contract says it should.

---

## 8. Reengineering decision 02 — dual intelligence path

A future DANTE intelligence must not become unable to answer general questions merely because the product has a structured Domain.

Two paths are therefore required:

```text
DANTE-NATIVE PATH
structured life state
history
planning
resources
relationships
constraints
semantic queries
governed effects

OPEN-WORLD PATH
general explanation
research
web information
documents
content
code
multimodal reasoning
creative / analytical work
```

They are not two products and do not require two independent agent platforms.

They must be composable inside the same Execution Kernel.

Example:

```text
"Explain how to photograph the Milky Way
and find the best evenings in my next two months."

open-world photography knowledge
+
DANTE calendar / location / commitments
+
external astronomy/weather information
+
constraint evaluation
→ one result
```

The architecture must not force a request to choose exactly one world when the useful answer spans both.

---

## 9. Reengineering decision 03 — Semantic Query / Projection Gateway

### Problem

Future intelligence needs stable access to DANTE meaning without being coupled to database tables or requiring the Context Engine to invent arbitrary SQL for every task.

### Responsibility

The Semantic Query / Projection Gateway exposes application-owned, permission-aware semantic projections such as:

```text
current commitments
Goal trajectory
workload in a period
open commitments involving a Person
current material state of a Program
safe availability projection
Meeting-series continuity
planned-vs-actual history
unresolved confirmations
resource availability
```

Conceptually:

```text
Intelligence
    │
    ▼
Semantic Query / Projection Gateway
    │
    ▼
Application / Domain query contracts
    │
    ▼
PostgreSQL / accepted projections
```

### Non-goals

The gateway is not:

```text
a universal Entity API
a generic graph database abstraction
raw SQL access for the model
a second Domain model
a vector-search replacement
a reason to expose every table to AI
```

It should reuse owner-specific application semantics and existing projection rules.

### Fast path

The gateway enables a structurally cheap route:

```text
request
→ semantic interpretation
→ semantic query
→ deterministic aggregation
→ result
```

No model call is required after interpretation when the answer is deterministic.

---

## 10. Reengineering decision 04 — Context Engine remains distinct

The Context Engine is not renamed into the Semantic Query Gateway.

The responsibilities are different.

### Semantic Query / Projection Gateway

Best for:

```text
structured DANTE-native state
current material facts
owner-specific history
known relationships
validated projections
```

### Context Engine

Best for assembling reasoning material from sources such as:

```text
unstructured notes
documents
artifacts
web results
external content
conversation context
retrieval results
prior noncanonical working material
```

The Context Engine remains scope-aware, provenance-aware, purpose-aware and budgeted.

Detailed Context / Retrieval / Memory design remains AI-03. AI-02.1 only fixes the responsibility boundary necessary to avoid conflating structured application query with general retrieval.

---

## 11. Reengineering decision 05 — Simulation / Hypothetical State Workspace

### Product requirement

DANTE must compare futures before applying meaningful structural changes.

Examples:

```text
add Japanese study without sacrificing protected sleep
compare three travel plans
simulate a new job schedule
see what a week of illness changes
compare two training programs
move all flexible meetings out of Wednesday
```

### Architectural rule

A hypothetical future is not canonical state.

```text
CANONICAL MATERIAL STATE
        │
        ├──── Scenario A overlay
        ├──── Scenario B overlay
        └──── Scenario C overlay
```

The architecture must not duplicate the whole database for every scenario.

A scenario workspace conceptually contains:

```text
basis material-state references
hypothetical changes
assumptions
constraints
external assumptions / forecasts
solver/model outputs
derived metrics
violations / conflicts
comparison evidence
```

### State class

Default classification:

```text
transient / derived technical state
```

A scenario becoming materially meaningful does not imply that the whole workspace becomes a new canonical object. Individual results may later be retained through the correct existing semantic owner, for example Proposal, Possibility, Decision rationale or another already accepted family when genuinely applicable.

### Staleness

Every consequential scenario is evaluated against a basis.

If material state changes before a user accepts a scenario:

```text
stale basis
→ re-read
→ re-evaluate
→ show changed consequences
```

A scenario is never authorization to apply a plan built against obsolete material state.

---

## 12. Reengineering decision 06 — ChangeSet / Effect Graph

### Problem

One user intention may legitimately require several coordinated domain/application operations.

Example:

```text
"I'm ill this week. Pause training, lighten study,
but do not move my medical appointment."
```

Potential operations:

```text
set temporary mode
pause Program A
suspend future generated occurrences
replan study workload
preserve protected Event B
```

Treating this as one opaque tool call loses too much structure. Treating each effect independently loses the overall decision and dependency model.

### ChangeSet responsibility

A ChangeSet / EffectGraph may carry:

```text
objective
basis material state
ordered/related operations
dependency edges
protected invariants
expected-state requirements
atomic groups
external-effect boundaries
preview information
approval binding
rollback availability
compensation rules
partial-outcome state
reconciliation requirements
```

### Relationship to Effect Runtime

ChangeSet does not replace the governed effect contract.

```text
ChangeSet
    │
    ├─ Effect A
    ├─ Effect B
    ├─ Effect C
    └─ Effect D
          │
          ▼
EffectIntent
→ EffectPermit
→ EffectAttempt
→ EffectReceipt
→ Verification / Reconciliation
```

Each consequential operation remains independently governed where required.

### Atomicity

When all operations belong to one legitimate application transaction boundary, normal database atomicity may apply.

When a ChangeSet crosses provider/system boundaries:

```text
all-or-nothing may be impossible
```

The correct state may therefore be:

```text
PARTIALLY_APPLIED
OUTCOME_UNKNOWN
RECONCILIATION_REQUIRED
COMPENSATION_PENDING
```

The architecture must never manufacture total success from partial external completion.

---

## 13. Reengineering decision 07 — Verifier / Auditor primitive

The first pressure-test confirms the production-research conclusion:

```text
MODEL CLAIM
"I completed X"

!=

VERIFIED STATE
"X is demonstrably true according to the relevant evidence"
```

Verification belongs inside the execution model rather than as an optional afterthought.

Potential verifiers include:

```text
schema validation
SQL / state reread
MaterialState verification
provider reread
receipt verification
constraint solver validation
filesystem diff
hash / integrity validation
test execution
DOM / accessibility inspection
independent semantic verification only when deterministic evidence is insufficient
```

A conceptual `VerificationReceipt` may record runtime evidence about what was checked and what result was established.

It is not automatically a new canonical Domain owner.

Verification does not replace Confirmation, Observation, Evidence or Reconciliation. Those retain their accepted semantic meanings.

---

## 14. Reengineering decision 08 — Proactivity / Attention boundary

### Problem

A trigger tells DANTE that something happened or should be evaluated. It does not determine whether the user should be interrupted.

The product requires proactive behavior without constant notification noise.

### Responsibility

Conceptually:

```text
Signal
  ↓
Relevance
  ↓
Materiality
  ↓
Urgency
  ↓
Attention Policy
  ↓
┌────────┬────────┬────────┬────────────┬──────────┐
│        │        │        │            │          │
silent  review   notify   start work   escalate
```

Inputs may include:

```text
user policy
quiet hours
current mode
risk/consequence
repetition / deduplication
whether the issue blocks future work
whether the user already saw it
confidence / uncertainty
expiration
recipient/context
```

### Distinction from Trigger

```text
Trigger
= something is due / changed / true enough to evaluate

Attention
= what should happen to the user's attention because of it
```

### Distinction from notification transport

The Attention boundary selects the product response. Push/email/in-app delivery is a downstream channel concern.

### Review Queue

Review Queue remains a product aggregation surface, not a generic AI persistence store.

Persistent unresolved matters must use the correct existing semantics when they deserve persistence, for example:

```text
Proposal
Request
Confirmation need
Reconciliation
Decision requiring resolution
unresolved candidate under an existing owner
```

Do not introduce a universal `AIReviewItem` or store unresolved product obligations only in a chat transcript.

---

## 15. Reengineering decision 09 — Context Projection != Disclosure Projection

### Problem

DANTE may legitimately process information that it must not disclose to a recipient.

Example:

```text
private calendar source
"medical appointment 19:00"
        ↓ authorized computation
safe availability consequence
"unavailable 19:00–20:00"
        ↓ recipient
```

### Context Projection

Answers:

> What information may this reasoning operation consume for this purpose?

### Disclosure Projection

Answers:

> What representation may this recipient receive from the result?

These are not the same decision.

```text
source state
   │
   ├─ ContextProjection(model/runtime)
   │
   └─ DisclosureProjection(recipient/surface)
```

The disclosure step may deliberately remove source details while preserving an authorized consequence.

### Relationship to policy

Policy remains responsible for whether processing/disclosure is legitimate.

Projection is responsible for **which representation** is safe and semantically adequate.

This distinction prevents a binary allow/deny egress check from forcing either unnecessary disclosure or unusable denial.

---

## 16. Information-flow and derived-output rule

The production research strengthens the need to propagate trust properties through derived material.

At minimum, reasoning material may carry conceptual properties such as:

```text
confidentiality class
integrity / trust class
instruction authority
source/provenance lineage
```

Derived output does not automatically reset those properties merely because a model generated new wording.

For example:

```text
PRIVATE DANTE STATE
+
UNTRUSTED WEB CONTENT
        ↓
GENERATED SUMMARY
```

must not become implicitly:

```text
PUBLIC + TRUSTED
```

Dynamic decisions such as:

```text
may process for purpose P?
may disclose to recipient R?
may send to provider Z?
```

remain policy decisions at use time rather than frozen intrinsic labels that duplicate Authority/Visibility/Consent semantics.

---

## 17. Reengineering decision 10 — ModelTarget + HarnessProfile

DANTE does not plan to train a foundation model or operate a large always-on frontier inference fleet.

Current project constraints remain:

```text
NO foundation-model training
NO DANTE-owned frontier model
NO fine-tuning requirement as baseline
NO large always-on self-hosted frontier-model fleet
NO GPU cluster as baseline

API-FIRST frontier intelligence
provider/model replaceability mandatory
small/local inference optional and benchmark-gated
```

Because DANTE does not control model weights, much of the controllable quality surface lives in the harness.

Therefore separate:

```text
ModelTarget
from
HarnessProfile
```

A HarnessProfile may version provider/model-specific choices such as:

```text
instruction shape
context strategy
reasoning configuration
structured-output mode
provider-native tool semantics
prompt/cache behavior
continuation/compaction behavior
model-specific capability projection
```

Provider independence does not mean reducing every model to a lowest-common-denominator `generate(prompt) -> string` interface.

Application contracts remain stable while provider-native strengths may be used behind versioned adapters/harnesses.

---

## 18. Execution Kernel v0.2

After the first simulation pass, the current responsibility map is:

```text
┌───────────────────────────────────────────────────────────────┐
│                     INTERACTION EDGE                          │
│ Web · Mobile · Voice · Capture · API · External AI           │
└────────────────────────────┬──────────────────────────────────┘
                             │
                             ▼
                    INTERACTION SESSION
                             │
                             ▼
                        WORK INTAKE
                             │
                  Semantic Interpretation
                             │
                             ▼
                    EXECUTION KERNEL
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
 SEMANTIC QUERY           CONTEXT             SCENARIO
 / PROJECTION             ENGINE              WORKSPACE
        │                    │                    │
        └────────────────────┼────────────────────┘
                             ▼
                      REASONING LAYER
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
       Models          Deterministic         Solver
   + HarnessProfile       Compute
          │                  │                  │
          └──────────────────┼──────────────────┘
                             ▼
                    CAPABILITY RUNTIME
                             │
                             ▼
                    VERIFIER / AUDITOR
                             │
                             ▼
                 CHANGESET / EFFECT GRAPH
                             │
                             ▼
                      EFFECT RUNTIME
                             │
                             ▼
                  APPLICATION / DOMAIN
                             │
                             ▼
                        PostgreSQL
```

Cross-cutting responsibilities:

```text
Policy / Authority / AuthZ / Consent / Visibility
Information flow
Provider eligibility
Autonomy
Proactivity / Attention
Run / durability
Artifact handling
Result / disclosure / presentation
Control Plane
Resource governance
Observability
Audit / execution evidence
Evals
```

This is a responsibility architecture, not a deployment diagram.

---

## 19. Responsibility boundary != microservice

AI-02.1 explicitly rejects architecture theatre.

The previous diagram does **not** imply services named:

```text
semantic-query-service
simulation-service
attention-service
verification-service
disclosure-service
```

A valid first implementation can remain inside the accepted capability-first modular monolith, for example conceptually:

```text
apps/backend/src/dante/
  ...
  intelligence/
    interaction
    intake
    execution
    query
    context
    simulation
    models
    capabilities
    verification
    effects
    attention
    results
```

Exact module placement remains an implementation decision and is not authorized by this document.

Extraction into independent deployment units requires measured isolation, scaling, availability, hardware or operational evidence.

---

## 20. End-to-end behavioral model

A representative high-level path is:

```text
1. receive interaction / event / trigger
2. resolve principal / actor / represented party / purpose
3. classify work and risk
4. choose structural fast path when possible
5. resolve authorized semantic state
6. assemble only necessary contextual material
7. evaluate information-flow/provider eligibility
8. choose model/compute/solver/capabilities as needed
9. reason / calculate / simulate
10. verify material intermediate claims when consequential
11. produce Result / Proposal / ChangeSet as appropriate
12. re-read material state before consequential execution when freshness matters
13. re-evaluate policy / Authority / AuthZ after long waits or approvals
14. issue bounded EffectPermits
15. execute governed effects
16. verify / reconcile receipts and ambiguous outcomes
17. materialize accepted canonical effects only through application/domain operations
18. apply recipient-aware disclosure projection
19. render result through the current interaction surface
20. retain only state justified by the correct semantic/runtime owner
```

Not every request uses every step.

A simple deterministic query may be:

```text
1 → 4 → 5 → deterministic compute → 18 → 19
```

The architecture must preserve that cheap path.

---

## 21. Compound change semantics

A consequential compound flow should conceptually support:

```text
User request
   ↓
Interpretation
   ↓
Current MaterialState basis
   ↓
Scenario / consequence analysis
   ↓
ChangeSet preview
   ↓
Approval where required
   ↓
RE-READ current state
   ↓
RE-EVALUATE Authority / AuthZ / policy
   ↓
Bind final EffectPermits
   ↓
Execute effect graph
   ↓
Verify receipts
   ↓
Reconcile ambiguity/partial completion
   ↓
Canonical result + truthful status
```

Approval is not permission to execute indefinitely against stale state.

If state materially changed while awaiting approval, DANTE must re-evaluate rather than blindly dispatch the old plan.

---

## 22. Proactive / watch flow

Representative watch:

> Notify me when there is a good astrophotography evening and I am actually free.

Correct architecture:

```text
Watch definition / accepted condition
        ↓
scheduled or condition-driven evaluation
        ↓
external astronomy/weather signals
        ↓
deterministic filters
        ↓
current DANTE availability / constraints
        ↓
reasoning only if needed
        ↓
Attention policy
        ↓
notify / review / remain silent
```

Incorrect architecture:

```text
LLM process waits for three weeks
```

Durability belongs to the runtime/workflow boundary when the workload requires crash-safe waiting. Intelligence is invoked when evaluation requires intelligence.

---

## 23. Multi-actor reasoning

The architecture must preserve real roles instead of collapsing everything into `user_id`.

Potentially distinct roles include:

```text
Account holder
Principal
Actor
represented party
Subject
responsible party
performer
participant
observer
recorder
Authority holder
recipient
external non-DANTE participant
provider/system of record
```

A future prompt/context/capability contract must carry enough role information for the material operation.

A private source may be processed to create a safe shared consequence without exposing the source.

A participant may see a result without having Authority to change it.

An Authority holder may exist without a DANTE Account.

These are inherited semantic requirements, not optional AI features.

---

## 24. Epistemic flow

DANTE must distinguish:

```text
source material
observation/assertion
inference
candidate interpretation
proposal
confirmation
accepted current state
actual outcome
reconciliation
```

Representative meeting extraction:

```text
transcript
   ↓
model extraction
   ↓
candidate decision
candidate commitment
candidate task
   ↓
validation / resolution / confirmation where appropriate
   ↓
existing semantic owners
```

Do not create a universal `memory_fact` or `ai_fact` table merely to store everything the model said.

---

## 25. External effects and ambiguous outcomes

The effect contract remains one of the strongest surviving parts of the architecture.

```text
EffectIntent
→ EffectPermit
→ EffectAttempt
→ EffectReceipt
→ Verification
→ Reconciliation when needed
```

Example:

```text
DANTE asks provider to move appointment
provider times out
```

The correct result may be:

```text
OUTCOME_UNKNOWN
```

not `FAILED` and not `SUCCESS`.

Next action may be provider reread/reconciliation.

Blind retry is forbidden when the first attempt may already have produced an external effect.

---

## 26. Review and human-resolution semantics

Human attention is not a substitute for semantics.

If an issue survives a Session, it should survive through an appropriate durable owner.

Examples:

```text
AI proposal needing approval
→ Proposal / applicable decision flow

conflicting provider/current state
→ Reconciliation

unknown past execution
→ applicable Confirmation / unresolved outcome semantics

request awaiting another party
→ Request / participation/responsibility semantics as applicable
```

UI may aggregate these into Review Queue without making Review Queue the semantic owner.

---

## 27. Future rich conversational intelligence acceptance criterion

AI-02.1 treats future general-purpose conversational intelligence as a mandatory extensibility test.

The target is not to build a frontier chatbot today.

The target is to ensure that DANTE can later host substantially richer intelligence without architectural replacement.

A future surface may eventually include:

```text
text
voice
image
camera
PDF/document work
web research
general Q&A
creative work
code
analysis
artifacts
long-running research
DANTE-aware planning
DANTE actions
external systems
specialist intelligence
```

### Required invariant

More capable intelligence must be able to plug into DANTE without inheriting ownership of:

```text
canonical memory
canonical application state
Domain semantics
Authority
Visibility
accepted-effect rules
material history
```

Therefore the preferred dependency direction is:

```text
future frontier intelligence
        ↓
DANTE Intelligence contracts
        ↓
Application / Domain
        ↓
canonical life state
```

not:

```text
future model/provider
=
new DANTE database
+ new authority model
+ new memory truth
+ new business logic
```

### Provider replacement

A future model with much stronger reasoning should improve DANTE by replacing or augmenting a cognitive component, not by requiring migration of the product's semantic truth into that provider's thread/memory model.

---

## 28. External AI / external-agent symmetry

DANTE must support both directions without architectural inversion:

```text
AI inside DANTE
→ DANTE invokes provider/model capabilities

DANTE inside external AI
→ external assistant invokes explicitly exposed DANTE capabilities
```

An external AI client may receive bounded read/propose/act capabilities through protocols such as MCP/A2A or another future adapter when product strategy justifies it.

External protocol adapters must not become internal Domain contracts.

External agents do not inherit user Authority merely because they possess a technical connection.

Delegation, principal identity, purpose, scope and effect policy remain explicit.

---

## 29. What remains intentionally open

AI-02.1 v0.2 does not decide:

```text
exact provider/model set
primary vs secondary provider
model gateway product
agent SDK/framework
exact Execution Kernel implementation
conversation persistence schema
memory persistence schema
embedding strategy
vector-index strategy
retrieval ranking
context compaction implementation
sandbox provider
policy engine product
learned router
local-model family/size
exact autonomy UX
exact durable-runtime activation per workload
exact Attention scoring/rules
exact ScenarioWorkspace representation
exact ChangeSet physical persistence, if any
exact Interaction Session persistence, if any
```

Many of these belong partly or primarily to AI-03 or later implementation phases.

---

## 30. Explicit anti-patterns after reengineering

Do not implement:

```text
one giant agent loop owning the product
raw model access to PostgreSQL
raw model access to arbitrary provider credentials
provider conversation thread as DANTE memory authority
one generic AIAction table
one universal memory_fact table
one universal AIReviewItem table
one generic Scenario entity promoted to Domain without semantic proof
one opaque mega-tool for compound mutation
one approval token valid forever despite stale state
one Context Engine that dumps the whole user history into every request
one egress allow/deny check that ignores safe derived projections
one background LLM process acting as scheduler/timer
one model call for deterministic arithmetic/aggregation by default
one learned router before DANTE has representative outcome data
one service/container per architecture box
```

---

## 31. First-pass architecture scorecard

```text
CORE PRINCIPLES                         PASS
Domain compatibility                    PASS
PostgreSQL canonical authority          PASS
Deterministic-first execution           PASS
Provider/model replaceability           PASS
Effect safety / ambiguous outcomes      PASS
Multi-actor semantic compatibility      PASS
Durable-work separation                 PASS
Epistemic integrity                     PASS

Scenario reasoning                      GAP → FIX IDENTIFIED
Compound multi-object mutation          GAP → FIX IDENTIFIED
Proactivity / attention                 GAP → FIX IDENTIFIED
Recipient disclosure                    GAP → FIX IDENTIFIED
Structured semantic access              GAP → FIX IDENTIFIED
Future rich conversation                GAP → FIX IDENTIFIED
```

The identified fixes are the responsibility boundaries recorded in this document.

They have not yet earned final acceptance because the architecture has not passed the next compound adversarial simulation round.

---

## 32. Remaining AI-02.1 acceptance work

Before AI-02.1 can close, the v0.2 model must undergo a more aggressive compound pressure-test.

The next scenarios must combine multiple failure dimensions at the same time rather than testing one clean concern per case.

Required classes include at least:

```text
multi-actor + privacy + stale state
provider side effect + timeout + retry temptation
long approval wait + changed Authority
external untrusted content + sensitive DANTE context + outbound effect
multi-step replan + partially failed external operation
long-running watch + changing user constraints
conflicting evidence from multiple actors/providers
participant without DANTE account
revoked permission during active Run
model/provider outage during compound work
cancellation during streaming / execution
budget/resource exhaustion mid-run
artifact/document deletion while derived state still exists
concurrent user edit during scenario approval
future frontier-chat mixed open-world + DANTE-native task
```

At least one deliberately hostile end-to-end scenario should combine many of these simultaneously.

### Example hostile scenario seed

```text
four-person trip
+ one participant does not use DANTE
+ private calendars
+ selective availability disclosure
+ shared budget
+ flight/hotel providers
+ untrusted external travel content
+ one participant cancels
+ booking provider times out after mutation
+ user changes decision during reconciliation
+ DANTE must replan without rewriting history
+ no private reason may leak to the other participants
```

The architecture should survive without introducing scenario-specific semantic patches.

---

## 33. Regression checklist for the next pressure-test

Every future AI-02.1 scenario must check:

```text
[ ] no accepted Domain distinction collapsed
[ ] no provider state promoted to canonical truth
[ ] no inference presented as Confirmation
[ ] no history rewritten to match the current plan
[ ] no stale material state silently overwritten
[ ] no effect declared successful without sufficient evidence
[ ] no blind retry across an ambiguous external effect
[ ] no Authority inferred from technical capability
[ ] no Visibility used as Authority
[ ] no private source disclosed merely because its consequence is usable
[ ] no other actor collapsed into account holder/user
[ ] no unresolved durable work trapped only in chat state
[ ] no hypothetical scenario treated as current reality
[ ] no ChangeSet hides partial completion
[ ] no unnecessary frontier-model call for deterministic work
[ ] no unnecessary durable/sandbox/multi-agent complexity
[ ] no new technology activated without a concrete trigger
[ ] no new generic persistence root created for convenience
[ ] no future rich-chat capability forces redesign of Domain/application core
```

Any failure must be classified as:

```text
local implementation issue
architecture responsibility gap
semantic contradiction
closed-model reopen candidate
technology limitation
product requirement conflict
```

Do not reopen the widest layer first.

---

## 34. AI-03 gate

AI-03 owns detailed:

```text
CONTEXT
RETRIEVAL
MEMORY
```

AI-03 remains deliberately after AI-02.1 because context/memory choices depend on the structural intelligence responsibilities fixed here.

AI-03 must not be used to repair an unresolved architecture gap that belongs to AI-02.1.

Before AI-03 starts, AI-02.1 must at minimum establish that:

```text
Interaction Session boundary is coherent
DANTE-native/open-world composition is coherent
Semantic Query / Context split is coherent
Scenario Workspace does not create a second truth
ChangeSet/Effect interaction preserves WL-H obligations
Attention/proactivity does not fabricate outcomes
Disclosure Projection preserves privacy/Visibility semantics
future frontier-chat extensibility survives
compound adversarial scenarios do not require semantic collapse
```

Only then should detailed memory admission, retrieval strategy, embeddings, indexes, conversation history and lifecycle be selected.

---

## 35. Current phase verdict

AI-02.1 v0.2 produces a stronger architecture than the pre-simulation model.

The central thesis remains intact:

> **DANTE is a domain-centered intelligence platform around replaceable cognition, not a model-centric application.**

The first serious product pressure-test did not invalidate the architecture. It exposed missing first-class responsibilities around hypothetical state, compound change, attention, disclosure, structured semantic access and conversational lifecycle.

Those gaps now have bounded fixes that preserve the accepted Domain/Logical/Physical/PostgreSQL model rather than bypassing it.

Current status therefore remains:

```text
AI-02.1
ACTIVE
REENGINEERED TO v0.2
FIRST SIMULATION PASS COMPLETE
FINAL ADVERSARIAL PRESSURE-TEST NOT YET COMPLETE
NOT CLOSED

AI-03
NOT STARTED
BLOCKED UNTIL AI-02.1 STRUCTURAL ACCEPTANCE
```

No runtime, provider, backend implementation or database PASS is claimed by this document.
