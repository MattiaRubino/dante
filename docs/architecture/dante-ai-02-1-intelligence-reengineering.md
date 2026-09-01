# DANTE AI-02.1 — Intelligence Reengineering & Simulation Pressure-Test

- **Status:** ACTIVE / BRANCH-LOCAL ARCHITECTURE CHECKPOINT / NOT CLOSED
- **Workstream:** `feature/ai-architecture`
- **Established:** 2026-09-01
- **Phase:** AI-02.1
- **Current checkpoint:** v0.3 / TWO PRESSURE-TEST ROUNDS COMPLETE / FINAL KILL-TEST STILL REQUIRED
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

This document records the current **v0.3 checkpoint after two distinct simulation/adversarial pressure-test rounds**. It is not the final AI-02.1 closure record.

The pressure-test record must remain methodologically clean. Questions about concrete provider pricing, model/server selection or other later implementation choices may be useful adjacent discussion, but they are not counted as evidence for the official adversarial round unless the scenario itself is testing an architecture obligation.

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
BasisManifest
Work Supersession
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

## 6. Round I — first simulation pressure-test summary

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

This scorecard did not close the phase. It produced the v0.2 responsibility map that Round II then attacked more aggressively.

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

## 18. Execution Kernel v0.3

After two pressure-test rounds, the current responsibility map is:

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
                 objective / scope / lineage
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
                    BASIS / DEPENDENCIES
                             │
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
Proactivity / Attention + attention budgeting
Causal lineage / oscillation protection
Run / durability / work supersession
Basis validity / dependency-aware invalidation
Artifact handling
Result / disclosure / cumulative inference protection
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
supersession-service
basis-service
oscillation-service
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
3. classify work, objective, scope and risk
4. relate work to prior work: continuation / supersession / independent
5. choose structural fast path when possible
6. resolve authorized semantic state
7. assemble only necessary contextual material
8. record the consequential basis/dependencies required for later validity checks
9. evaluate information-flow/provider eligibility
10. choose model/compute/solver/capabilities as needed
11. reason / calculate / simulate
12. verify material intermediate claims when consequential
13. produce Result / Proposal / ChangeSet as appropriate
14. check that work is still semantically current and not superseded
15. re-read material state before consequential execution when freshness matters
16. re-evaluate policy / Authority / AuthZ / Consent / source validity after long waits or approvals
17. issue bounded EffectPermits
18. execute governed effects
19. verify / reconcile receipts and ambiguous outcomes
20. materialize accepted canonical effects only through application/domain operations
21. apply recipient-aware disclosure projection, including bounded cumulative inference protection when required
22. render result through the current interaction surface
23. retain only state justified by the correct semantic/runtime owner
```

Not every request uses every step.

A simple deterministic query may be:

```text
1 → 5 → 6 → deterministic compute → 21 → 22
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
CHECK work is still current / not superseded
   ↓
RE-READ current state
   ↓
RE-EVALUATE Authority / AuthZ / Consent / policy / source validity
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

If newer work supersedes the objective/scope before dispatch, obsolete not-yet-dispatched effects must not execute merely because an older Run remains technically alive.

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
causal-loop / recent-effect check
        ↓
Attention policy + attention budget
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

Cancellation is also precise:

```text
CANCEL RUN
!=
UNDO ALREADY-DISPATCHED EFFECTS
```

Cancelling a Run stops future executable work that the cancellation contract still controls. Already-dispatched effects remain subject to receipt verification, reconciliation and explicit compensation/reversal semantics where supported. DANTE must not report them as undone merely because the originating Run was cancelled.

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

This pre-existing extensibility requirement is retained, but the official Round II pressure-test below is intentionally independent from later questions about which external AI products/protocols to activate.

---

## 29. What remains intentionally open

AI-02.1 v0.3 does not decide:

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
exact physical representation, if any, for BasisManifest/work lineage/disclosure accounting
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
one Run authorization assumed valid forever
one Context Engine that dumps the whole user history into every request
one egress allow/deny check that ignores safe derived projections
one disclosure check that ignores cumulative inference when that risk is material
one background LLM process acting as scheduler/timer
one adaptation loop that recursively reacts to its own effects without material change
one old Run dispatching obsolete work after a newer intent superseded it
one model call for deterministic arithmetic/aggregation by default
one learned router before DANTE has representative outcome data
one service/container per architecture box
```

---

## 31. Round I architecture scorecard

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

Round I produced the v0.2 responsibility map. Round II then tested those fixes under concurrency, revocation, cumulative privacy risk, feedback loops, superseding intent and partial external execution.

---

## 31.1 Round II — clean compound adversarial pressure-test

Round II is the second official AI-02.1 pressure-test. It was intentionally kept separate from adjacent questions about concrete provider/model pricing, local-model/server selection or product-specific external-AI activation.

The test combined real DANTE concerns rather than evaluating one clean feature at a time.

| Scenario family | Result | Consequence |
|---|---|---|
| week-wide replan while calendar/current state changes | PASS | scenario basis + expected MaterialState survive; re-evaluate before apply |
| three scenarios where only one dependency changes | PARTIAL | BasisManifest/dependency-aware invalidation required |
| concurrent mobile/Web edits from same old state | PASS STRONG | expected MaterialState rejects last-write-wins |
| five-person coordination with non-DANTE participant and selective availability | PASS | existing multi-actor semantics survive |
| individually safe availability queries compose into a private inference | GAP FOUND | cumulative/cross-query disclosure protection required |
| DANTE-generated replan triggers another replan and oscillates | GAP FOUND | causal-loop/oscillation guard required |
| derived hypothesis later rejected by user | PASS | inference remains derived, not hard canonical preference |
| conflicting authoritative/provider/user statements | PASS STRONG | Authority/Provenance/Reconciliation remain sufficient |
| multi-effect operation succeeds partially then crashes | PASS STRONG | ChangeSet + Effect states preserve partial/unknown outcome |
| source/permission revoked during active Run | PARTIAL | active-run validity must be revocable/revalidated |
| ambiguous meeting transcript | PASS | unresolved candidate/clarification is valid result |
| request has constraints with deterministic validity | PASS STRONG | solver/verifier path survives |
| no valid plan exists | PASS | `NO VALID PLAN` is legitimate result |
| many individually useful proactive signals overwhelm user | PARTIAL | Attention must budget aggregate interruption load |
| newer user intent semantically replaces older still-running work | GAP FOUND | Work Supersession first-class required |
| crash around external dispatch ambiguity | PASS | durable effect boundary + no blind retry survive |
| corrected/retired fact later reappears via old derived material | PASS STRUCTURAL | anti-resurrection remains mandatory; AI-03 must prove lifecycle |
| visible endpoints accidentally imply hidden private relationship | PASS SEMANTIC / HARDENING | reinforces cumulative inference control |
| external report corrected after having influenced a decision | PASS STRONG | historical/provider/current distinction survives |
| hostile combined scenario with stale basis + revocation + partial effect + superseding work | PASS ONLY WITH v0.3 HARDENINGS | no Domain/Logical reopen required |

### Round II high-level verdict

```text
NO semantic contradiction found
NO Domain reopen evidence
NO Logical reopen evidence
NO Physical/PostgreSQL reopen evidence

3 architecture gaps found:
1 cumulative/cross-query disclosure inference
2 causal-loop / oscillation protection
3 work supersession

3 contract hardenings found:
1 BasisManifest / dependency-aware validity
2 revocable active-Run authorization/data validity
3 aggregate Attention budgeting

1 effect lifecycle clarification:
CANCEL RUN != UNDO ALREADY-DISPATCHED EFFECTS
```

---

## 31.2 v0.3 hardening — cumulative / cross-query disclosure protection

### Problem

A response may be safe in isolation while a sequence of authorized responses allows a recipient to infer information they were never authorized to receive.

Example:

```text
recipient may learn:
"unavailable 19:00–20:00"

but may not learn:
private event type/reason
or a hidden relationship between two participants
```

Repeated narrow queries can reveal more than any single response.

Therefore Disclosure Projection is not always stateless.

Where inference risk is material, disclosure may consider:

```text
recipient
purpose
sensitivity
requested granularity
relevant prior disclosures
query sequence/pattern
aggregate information already exposed
relationship inference risk
rate / probing behavior
```

Potential outcomes include:

```text
ALLOW
COARSEN
AGGREGATE
WITHHOLD
REQUIRE DIFFERENT SCOPE
```

This does not create a universal privacy-memory ontology or a second Visibility truth.

Any disclosure accounting is bounded runtime/security state whose only purpose is to enforce already valid disclosure/Visibility constraints against composition attacks.

The existing semantic invariant remains:

```text
visible endpoint A
+
visible endpoint B
!=
visible relationship A↔B
```

---

## 31.3 v0.3 hardening — causal-loop / oscillation guard

### Problem

DANTE may legitimately create an effect that produces a new signal. If the system cannot distinguish external change from its own recent adaptation, multiple individually valid rules can oscillate indefinitely.

Example:

```text
move training to Tuesday
→ Tuesday becomes overloaded
→ move to Wednesday
→ recovery rule reacts
→ move back to Tuesday
→ repeat
```

Relevant causal lineage must therefore be available when proactivity/replanning evaluates a signal:

```text
Signal
→ caused_by / related_to Effect
→ Effect belongs to Run
→ Run may originate from Watch / Rule / prior adaptation
```

Bounded protections may include:

```text
minimum material delta
hysteresis
cooldown
recent-effect awareness
duplicate/symmetric adaptation detection
bounded adaptation depth
```

The guard must not suppress a genuinely new external change merely because related DANTE work happened recently.

The decision is therefore not "never react to our own effect". It is:

> do not recursively re-adapt when no sufficiently material new reality justifies another change.

---

## 31.4 v0.3 hardening — Work Supersession

### Problem

Canonical state may remain unchanged while the user's newer intention makes an older Run's pending proposal obsolete.

Example:

```text
Run A:
"organize next week"

Run B one minute later:
"wait — the priority is now finishing the project"
```

Expected MaterialState alone cannot detect this because the database may not have changed yet.

Work Intake / Run lifecycle must therefore support bounded work relationships such as:

```text
objective
scope
continuation_of?
supersedes?
independent_of?
```

The distinction is mandatory:

```text
SUPERSEDE
!= CANCEL
!= ROLLBACK
!= RECONCILE
```

A superseded Run may still need to:

```text
finish reconciliation of already-attempted effects
preserve audit/execution evidence
return truthful status about work already performed
```

but it must not:

```text
present an obsolete proposal as the current recommendation
dispatch not-yet-dispatched work that the newer intent invalidated
silently cancel unrelated independent Runs
```

Supersession must be scope-aware. A new weekly-planning objective does not automatically supersede an unrelated flight watch or research Run.

---

## 31.5 v0.3 hardening — Execution / Reasoning BasisManifest

### Problem

A scenario, plan or consequential result may depend on multiple inputs, not one global snapshot.

A conceptual `BasisManifest` may therefore capture enough dependency evidence to evaluate continued validity:

```text
relevant MaterialStateRefs
relevant canonical/source references
external source identity/version/freshness
assumptions used
constraints used
policy/config versions where consequential
capability/harness versions where consequential to reproducibility
```

The purpose is not to store every token or every transient thought.

The purpose is to support:

```text
what changed?
which result depended on it?
what must be recomputed?
what remains valid?
```

Preferred behavior:

```text
changed input X
→ invalidate/recompute dependent outputs
```

instead of either:

```text
invalidate everything
```

or:

```text
invalidate nothing
```

BasisManifest is runtime/evidence metadata, not a new canonical Domain owner and not a substitute for owner-specific MaterialState history.

---

## 31.6 v0.3 hardening — active Run validity is revocable

Authorization and data eligibility are not frozen forever at Run start.

```text
authorized at T0
!=
authorized forever
```

At consequential boundaries, especially after waits/approvals/durable suspension or before disclosure/effect, the runtime must be able to revalidate as applicable:

```text
Authority
AuthZ
Consent
Visibility
purpose / processing eligibility
source validity
source retirement/deletion
expected MaterialState
work supersession/currentness
```

Revocation cannot retroactively remove information already processed by an external provider or undo an already-dispatched effect.

It can and must constrain subsequent behavior, including where applicable:

```text
new retrieval/use
new provider disclosure
new recipient disclosure
new derived persistence
new consequential effect
```

This preserves both honest system limits and forward enforcement.

---

## 31.7 v0.3 hardening — Attention is a budgeted user resource

A system can be wrong at product level while every single notification is individually relevant.

Therefore Attention evaluates not only:

```text
is this signal relevant/material/urgent?
```

but also:

```text
given everything else asking for attention now,
should this interrupt the user in this form and at this time?
```

Inputs may include:

```text
attention budget
interruption cost
recent interruptions
aggregate current load
batchability
review opportunity
urgency/materiality
expiry
user policy
quiet hours/current mode
```

Ten moderate signals may become one review instead of ten interruptions.

Attention budgeting is a responsibility refinement of the existing Attention boundary, not a new service or semantic persistence root.

---

## 32. Remaining AI-02.1 acceptance work

Before AI-02.1 can close, the v0.3 model must undergo a final, more aggressive **kill-test**.

The next round must target the new hardenings directly rather than merely replaying the previous scenarios.

It must combine multiple failure dimensions at the same time, including at least:

```text
multi-actor + privacy + cumulative inference probing
stale scenario basis + dependency-local invalidation
provider side effect + timeout + retry temptation
long approval wait + changed Authority/Consent
revoked permission during active Run
superseding user intent while older Run is waiting or streaming
causal feedback loop produced by DANTE's own prior effects
Attention overload from multiple simultaneous watches
external untrusted content + sensitive DANTE context + outbound effect
multi-step replan + partially failed external operation
conflicting evidence from multiple actors/providers
participant without DANTE account
model/provider outage during compound work
cancellation during streaming / execution
budget/resource exhaustion mid-run
artifact/document deletion while derived state still exists
concurrent user edit during scenario approval
future frontier-chat mixed open-world + DANTE-native task
```

At least one deliberately hostile end-to-end scenario must combine many of these simultaneously.

### Required hostile seed for Round III

```text
shared multi-person plan
+ at least one non-DANTE participant
+ private actor-scoped context
+ repeated probing that could infer hidden information
+ one scenario built from several independent MaterialState/source dependencies
+ DANTE performs a bounded adaptation
+ that adaptation produces a new signal capable of causing oscillation
+ user starts a newer Run that supersedes only part of the old objective
+ Authority/Consent changes while one Run is suspended
+ one external effect has already been dispatched and times out
+ another effect has not yet been dispatched
+ one source used by the scenario is corrected/retired
+ process crashes and resumes
+ user attention is already saturated by other valid signals
+ DANTE must recover without rewriting history, leaking private information,
  duplicating an external effect, applying obsolete work or entering a replan loop
```

The architecture should survive without introducing scenario-specific semantic patches.

---

## 33. Regression checklist for the final kill-test

Every remaining AI-02.1 scenario must check:

```text
[ ] no accepted Domain distinction collapsed
[ ] no provider state promoted to canonical truth
[ ] no inference presented as Confirmation
[ ] no history rewritten to match the current plan
[ ] no stale material state silently overwritten
[ ] no stale Basis dependency ignored
[ ] no unrelated output invalidated without reason when dependency-local validation is possible
[ ] no effect declared successful without sufficient evidence
[ ] no blind retry across an ambiguous external effect
[ ] cancel Run not represented as undo of already-dispatched effects
[ ] no Authority inferred from technical capability
[ ] no Visibility used as Authority
[ ] no active Run assumes Authority/AuthZ/Consent remains valid forever
[ ] no private source disclosed merely because its consequence is usable
[ ] no cumulative query sequence reconstructs protected information without bounded control
[ ] visible endpoints do not imply an unauthorized hidden relationship
[ ] no other actor collapsed into account holder/user
[ ] no unresolved durable work trapped only in chat state
[ ] no hypothetical scenario treated as current reality
[ ] no ChangeSet hides partial completion
[ ] no superseded Run presents obsolete proposal as current
[ ] no superseded Run dispatches newly obsolete effects
[ ] no newer Run accidentally cancels independent work
[ ] no DANTE adaptation recursively triggers itself without material new reality
[ ] no user attention flood from individually-valid signals when batching/suppression is appropriate
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
BasisManifest/dependency invalidation is coherent
ChangeSet/Effect interaction preserves WL-H obligations
Work Supersession does not corrupt independent work or already-attempted effects
Attention/proactivity does not fabricate outcomes or self-oscillate
Attention load can be bounded across multiple signals
Disclosure Projection preserves privacy/Visibility semantics across single and cumulative queries
active-Run authorization/data validity can be revoked/revalidated
future frontier-chat extensibility survives
final compound adversarial kill-test does not require semantic collapse
```

Only then should detailed memory admission, retrieval strategy, embeddings, indexes, conversation history and lifecycle be selected.

---

## 35. Current phase verdict

AI-02.1 v0.3 is stronger than v0.2 and is the current branch-local architecture checkpoint.

The central thesis remains intact:

> **DANTE is a domain-centered intelligence platform around replaceable cognition, not a model-centric application.**

Round I exposed missing first-class responsibilities around hypothetical state, compound change, attention, disclosure, structured semantic access and conversational lifecycle.

Round II then attacked the reengineered model under concurrency, cumulative privacy inference, self-generated feedback, revocation, superseding intent, partial effects, crashes, corrections and multi-actor pressure. It found three further architecture gaps and three bounded contract hardenings, all repairable inside the intelligence/runtime responsibility model without reopening Domain, Logical, Physical or PostgreSQL.

Current v0.3 additions are therefore:

```text
cumulative / cross-query disclosure protection
causal-loop / oscillation guard
Work Supersession
BasisManifest + dependency-aware invalidation
revocable active-Run validity
Attention budgeting
cancel Run != undo dispatched effects
```

These remain responsibility contracts, not automatic microservices, tables or new Domain owners.

Current status:

```text
AI-02.1
ACTIVE
REENGINEERED TO v0.3
ROUND I COMPLETE
ROUND II COMPLETE
FINAL KILL-TEST STILL REQUIRED
NOT CLOSED

DOMAIN / LOGICAL / PHYSICAL / POSTGRESQL REOPEN
NOT JUSTIFIED BY CURRENT PRESSURE-TEST EVIDENCE

AI-03
NOT STARTED
BLOCKED UNTIL AI-02.1 STRUCTURAL ACCEPTANCE
```

No runtime, provider, backend implementation or database PASS is claimed by this document.
