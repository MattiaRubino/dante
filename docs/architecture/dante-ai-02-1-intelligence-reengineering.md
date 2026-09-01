# DANTE AI-02.1 — Intelligence Reengineering & Simulation Pressure-Test

- **Status:** ACTIVE / BRANCH-LOCAL ARCHITECTURE CHECKPOINT / NOT CLOSED
- **Workstream:** `feature/ai-architecture`
- **Established:** 2026-09-01
- **Phase:** AI-02.1
- **Current checkpoint:** v0.4 / ROUND I + ROUND II + FINAL KILL-TEST COMPLETE / ONE LAST MEGA STRESS-TEST REQUIRED
- **Scope:** pressure-test and reengineer the DANTE Intelligence Architecture against actual product obligations before AI-03
- **Implementation:** NOT STARTED by this document
- **Provider/model/SDK selection:** OPEN
- **Database evolution:** NONE AUTHORIZED BY THIS DOCUMENT
- **AI-03:** BLOCKED until AI-02.1 completes its remaining architecture acceptance work

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

This document records the current **v0.4 checkpoint after three distinct architecture pressure-test rounds**:

```text
Round I
→ broad North-Star / product simulation pass

Round II
→ clean compound adversarial pressure-test

Final Kill-Test
→ deep cross-domain / multi-actor / failure-oriented stress pass
```

AI-02.1 is still not closed. One final deliberately broad mega stress-test remains before the phase can be considered for structural acceptance. After that mega-test, any residual narrow edge case is handled by a targeted verification rather than restarting an indefinite sequence of mega-tests.

The pressure-test record must remain methodologically clean. Questions about concrete provider pricing, model/server selection or other later implementation choices may be useful adjacent discussion, but they are not counted as evidence for an official adversarial round unless the scenario itself is testing an architecture obligation.

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
Reference / Target Resolution
PolicyDecision
ConsequenceProfile
Result Publication / Result Maturity
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

## 4. Non-negotiable inherited and reengineering invariants

AI-02.1 carries forward at least the following rules:

```text
DANTE != chatbot
DANTE != model
DANTE != provider
DANTE != chat transcript

MODEL != canonical truth
MODEL != authorization engine
MODEL != policy-precedence authority
MODEL != durable workflow engine
MODEL != database
MODEL != effect success
MODEL OUTPUT != PUBLISHABLE OUTPUT
INTERNAL STREAM != RECIPIENT STREAM

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

DISPLAY NAME != EFFECT TARGET
AMBIGUOUS TARGET != RESOLVED TARGET

DANTE CANONICAL REPRESENTATION
!=
EXTERNAL INSTITUTIONAL SYSTEM-OF-RECORD AUTHORITY

SENT != DELIVERED != SEEN != ACKNOWLEDGED != ACCEPTED
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

## 18. Execution Kernel v0.4

After three pressure-test rounds, the current responsibility map is:

```text
┌─────────────────────────────────────────────────────────────────┐
│                       INTERACTION EDGE                          │
│ Web · Mobile · Voice · Capture · API · External AI             │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
                      INTERACTION SESSION
                               │
                               ▼
                          WORK INTAKE
              objective / scope / lineage / consequence
                               │
                     Semantic Interpretation
                               │
                               ▼
               REFERENCE / TARGET RESOLUTION
                               │
                     exact / unique / ambiguous
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
              source freshness / temporal validity
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
                POLICY COMPOSITION / CONSEQUENCE
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
                               │
                               ▼
             RESULT / DISCLOSURE / PUBLICATION
```

Cross-cutting responsibilities:

```text
Policy / Authority / AuthZ / Consent / Visibility
Policy composition / precedence / obligations
Consequence classification
Information flow
Provider eligibility
Autonomy
Proactivity / Attention + attention budgeting
Causal lineage / oscillation protection
Run / durability / work supersession
Basis validity / temporal freshness / dependency-aware invalidation
Reference / target resolution integrity
Artifact handling
Result maturity / safe publication / disclosure
Cumulative inference protection
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
target-resolution-service
policy-composition-service
result-publication-service
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
3. classify work, objective, scope, consequence and risk
4. relate work to prior work: continuation / supersession / independent
5. resolve references/targets needed by the operation
6. if a consequential target is ambiguous or unresolved, clarify or stop
7. choose structural fast path when possible
8. resolve authorized semantic state
9. assemble only necessary contextual material
10. record consequential basis/dependencies and temporal freshness requirements
11. evaluate information-flow/provider eligibility
12. choose model/compute/solver/capabilities as needed
13. reason / calculate / simulate
14. compose applicable policy/Authority/AuthZ/Consent/autonomy/safety constraints
15. verify material intermediate claims when consequential
16. produce Result / Proposal / ChangeSet as appropriate
17. check that work is still semantically current and not superseded
18. revalidate target binding when target identity/context may have changed
19. re-read material state and time-sensitive sources before consequential execution when freshness matters
20. re-evaluate policy / Authority / AuthZ / Consent / source validity after long waits or approvals
21. issue bounded EffectPermits
22. execute governed effects
23. verify / reconcile receipts and ambiguous outcomes
24. materialize accepted canonical effects only through application/domain operations
25. assign truthful result maturity: working / provisional / verified / accepted-effect as applicable
26. apply recipient-aware disclosure projection, including bounded cumulative inference protection when required
27. publish/stream only material cleared for that recipient/surface at that maturity
28. render result through the current interaction surface
29. retain only state justified by the correct semantic/runtime owner
```

Not every request uses every step.

A simple deterministic query may be:

```text
1 → 2 → 3 → 5 → 7 → 8 → deterministic compute → 25 → 26 → 27 → 28
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
Reference / target resolution
   ↓
Consequence classification
   ↓
Current MaterialState / source basis
   ↓
Scenario / consequence analysis
   ↓
Policy composition
   ↓
ChangeSet preview
   ↓
Approval where required
   ↓
CHECK work is still current / not superseded
   ↓
RE-RESOLVE / REVALIDATE target where material
   ↓
RE-READ current state + time-sensitive dependencies
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
Truthful result maturity
   ↓
Safe disclosure/publication
```

Approval is not permission to execute indefinitely against stale state.

If state materially changed while awaiting approval, DANTE must re-evaluate rather than blindly dispatch the old plan.

If newer work supersedes the objective/scope before dispatch, obsolete not-yet-dispatched effects must not execute merely because an older Run remains technically alive.

If the target was ambiguous or its identity binding is no longer valid, an effect must not be dispatched merely because the language model remains confident.

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
temporal freshness check
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
safe result publication
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

The presentation layer must preserve the same truth. While an external result is unresolved, DANTE may say that the request was sent or is being verified; it must not stream or display a completed-success state that has not been established.

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

The same future-rich-chat acceptance now includes publication safety: richer token streaming, realtime voice or multimodal output must not gain a privileged path around disclosure, result-maturity or effect-verification rules.

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

This pre-existing extensibility requirement is retained, but the official pressure-test rounds are intentionally independent from later questions about which external AI products/protocols to activate.

---

## 29. What remains intentionally open

AI-02.1 v0.4 does not decide:

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
exact target-resolution implementation
exact PolicyDecision implementation
exact ConsequenceProfile implementation
exact safe-streaming implementation
exact result-maturity representation
exact physical representation, if any, for BasisManifest/work lineage/disclosure accounting
```

Many of these belong partly or primarily to AI-03 or later implementation phases.

The architecture decides the required contracts now; it does not prematurely choose the technology that will implement them.

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
one consequential effect targeted only by display-name/model guess
one LLM deciding policy precedence because multiple rules conflict
one user-autonomy setting treated as authority over external/institutional reality
one raw model/provider stream connected directly to a recipient when sensitive context is involved
one streamed success claim before an external effect is verified
one unchanged source version assumed fresh forever
one delivered notification treated as seen/acknowledged/accepted
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

## 31.8 Round III — Final Kill-Test

The third official pressure-test deliberately broadened the scenario corpus again and searched for rare cross-domain failures rather than replaying only the v0.3 hostile seed.

The personas/work domains were used as adversarial lenses only. They do not become product profiles, mandatory modules or Domain owners.

Representative scenario families included:

```text
farmer / small producer
nurse / shift worker
teacher + students + parents
student / researcher
caregiver
clinician in personal-organizer scope
field technician
legal professional
freelancer
shop operator
artisan
parent / guardian
older or low-digital participant
photographer / creator
software developer
manager
journalist / confidential-source work
traveller / group trip
athlete / coach
emergency worker
public official
extreme institutional / head-of-government stress boundary
malicious participant/input
large fan-out coordination
offline/late-arriving state
long multimodal chat
```

These were combined with:

```text
multi-actor identity
private actor-scoped context
ambiguous natural-language referents
same-name people/resources/documents
institutional constraints
conflicting policy sources
provider timeout
partial effect completion
crash/recovery
source correction/retirement
time-sensitive external data
cumulative disclosure probing
self-generated adaptation signals
superseding work
attention saturation
prompt injection
future rich realtime/streaming conversation
```

### Round III result

The v0.3 core continued to survive Domain, history, multi-actor, scenario, reconciliation, partial-effect, revocation, supersession, disclosure and oscillation stress.

The kill-test found three new P0 architecture gaps and three important hardenings:

```text
P0 GAP 1
Reference / Target Resolution

P0 GAP 2
Policy Composition / Precedence
+ ConsequenceProfile

P0 GAP 3
Safe Result Publication / Streaming

HARDENING A
BasisManifest temporal validity

HARDENING B
DANTE canonical representation
!= external institutional System of Record authority

HARDENING C
sent != delivered != seen != acknowledged != accepted
```

It found no evidence sufficient to reopen Domain, Logical, Physical or PostgreSQL.

---

## 31.9 v0.4 P0 — Reference / Target Resolution Gate

### Failure found

A system can pass expected-state and authorization checks and still act on the wrong real target if natural-language reference resolution is wrong.

Examples:

```text
"move the meeting with Luca"
"send it to Marco"
"use the big field"
"book the Panda"
"update Atlas"
"move dad's appointment"
```

may each resolve to more than one legitimate Person, Asset, Place, Content Artifact, Event or other owner.

Expected MaterialState protects against stale state. It does **not** prove that the correct semantic target was selected.

Therefore:

```text
DISPLAY NAME
!=
EFFECT TARGET
```

and:

```text
MODEL CONFIDENCE
!=
TARGET RESOLUTION PROOF
```

### Required target-resolution outcomes

A consequential reference must be classifiable as at least:

```text
EXACT
UNIQUE_IN_SCOPE
AMBIGUOUS
UNRESOLVED
```

A conceptual resolved-target contract may carry:

```text
canonical reference
owner/type semantics
resolution scope
resolution basis
ambiguity status
```

The exact physical/API representation remains open.

### Consequential rule

```text
EXACT / UNIQUE_IN_SCOPE
→ may proceed subject to normal governance

AMBIGUOUS
→ focused clarification / explicit preview / disambiguation

UNRESOLVED
→ no consequential effect
```

This is a Work Intake / semantic-interpretation correctness gate, not a new identity ontology.

NativeRef / ScopedRecordRef / MaterialStateRef / ExternalRef retain their accepted meanings.

---

## 31.10 v0.4 P0 — Policy Composition / Precedence + ConsequenceProfile

### Failure found

Several individually valid rules can disagree.

Example shift-swap scenario:

```text
user autonomy policy                 ALLOW
personal calendar/capacity           ALLOW
institutional staffing rule          REQUIRE APPROVAL
qualification constraint             LIMIT / DENY
minimum-rest safety constraint       DENY
current delegated Authority          MAYBE INSUFFICIENT
```

The model must not improvise which one wins.

### Policy composition responsibility

The runtime must be able to deterministically compose applicable:

```text
Authority
AuthZ
Consent
Visibility
user autonomy
hard constraints
safety rules
institutional/external constraints
purpose restrictions
provider/data eligibility
```

A conceptual `PolicyDecision` may return:

```text
ALLOW
DENY
REQUIRE_CONFIRMATION
REQUIRE_EXTERNAL_APPROVAL
LIMIT_SCOPE
```

with, when material:

```text
reasons
obligations
authority basis
policy/config versions
validity / expiry
```

`PolicyDecision` is not a new Domain owner and does not replace the semantic meaning of Authority, Consent or Visibility.

### User autonomy rule

```text
USER AUTONOMY
!=
UNIVERSAL OVERRIDE
```

A user may control DANTE's behavior inside the authority they actually possess. A personal preference does not rewrite an external institution's roster, a school's official record, a provider's current state or another person's rights.

### ConsequenceProfile

The kill-test also showed that minimum governance depends on the consequences of the work, not only on the natural-language intent.

A conceptual `ConsequenceProfile` may classify dimensions such as:

```text
reversible?
external effect?
financially consequential?
safety-sensitive?
privacy-sensitive?
multi-actor?
time-critical?
irreversible or hard to compensate?
independent verification required?
```

It may influence:

```text
autonomy ceiling
verification floor
approval requirement
safe failure mode
publication maturity
```

It is a runtime/governance contract, not a universal severity score and not a new semantic root.

---

## 31.11 v0.4 P0 — Safe Result Publication / Streaming Gate

### Failure found

A correct final Disclosure Projection is too late if sensitive or unverified material has already been streamed to the recipient.

Example:

```text
private source:
"medical appointment 19:00"

allowed recipient result:
"unavailable 19:00–20:00"
```

A raw model stream that begins publishing the private reason creates an irreversible disclosure before final filtering can run.

Therefore:

```text
MODEL OUTPUT
!=
PUBLISHABLE OUTPUT

INTERNAL STREAM
!=
RECIPIENT STREAM
```

### Publication responsibility

Before material reaches a recipient/surface, DANTE must preserve the required gates for:

```text
information-flow eligibility
recipient-aware Disclosure Projection
cumulative inference protection
result maturity
verification status
effect outcome truth
```

The exact safe-streaming mechanism remains an implementation choice. Depending on consequence/sensitivity, it may include buffering, constrained generation, staged publication, safe incremental projection or another mechanism that proves the same property.

The architecture does **not** require all text to be fully buffered. It requires that streaming optimization never bypass governance.

### Result maturity

Presentation may need to distinguish states such as:

```text
WORKING
PROVISIONAL
VERIFIED
ACCEPTED_EFFECT
```

These are presentation/runtime maturity concepts, not replacements for Domain Confirmation, Actual, Outcome or Reconciliation.

Example:

```text
provider mutation request sent
response timed out
```

safe publication:

```text
"Request sent; outcome is being verified."
```

unsafe publication:

```text
"Done ✓"
```

---

## 31.12 v0.4 hardening — temporal validity is part of Basis validity

A source may become unusable for a consequential decision even when no explicit update/version event has arrived.

Examples:

```text
weather forecast
price
inventory
availability
traffic
travel condition
live provider state
```

Therefore Basis validity may require temporal metadata such as:

```text
observed_at
source version where available
valid_for / valid_until
freshness requirement
revalidate_after
temporal scope
```

The rule is:

```text
SOURCE VERSION UNCHANGED
!=
SOURCE STILL FRESH ENOUGH
```

Temporal validity extends `BasisManifest`; it does not create another canonical time/version ontology.

---

## 31.13 v0.4 hardening — DANTE representation != external System of Record authority

DANTE may canonically retain that a person has a hospital shift, school deadline, court hearing, flight or institutional meeting because that reality matters to their life.

That does not mean DANTE becomes the authoritative institutional system that creates or governs that external reality.

Examples include:

```text
hospital roster
school register
clinical record
court/case system
banking ledger
official administrative act
institutional/classified record
```

Therefore:

```text
DANTE CANONICAL PERSONAL REPRESENTATION
!=
EXTERNAL INSTITUTIONAL SYSTEM-OF-RECORD AUTHORITY
```

A DANTE-side edit may change local planning or a proposal. It modifies the external authoritative reality only through a legitimate governed capability accepted by that external system.

This is consistent with the Product North Star requirement that DANTE may coordinate specialist systems without pretending to replace them.

---

## 31.14 v0.4 hardening — communication state must not collapse

Multi-actor coordination may require several distinct facts:

```text
SENT
DELIVERED
SEEN
ACKNOWLEDGED
ACCEPTED
ACTUALLY PARTICIPATED / ACTED
```

They are not interchangeable.

For example:

```text
message delivered
!=
parent knows/acknowledged school change

request seen
!=
participant accepted responsibility
```

DANTE may batch transport operations physically, but must not manufacture stronger coordination semantics than the evidence supports.

This reuses existing Request/Proposal/Participation/Actual/Confirmation semantics where applicable rather than creating one generic notification truth.

---

## 31.15 Round III architecture scorecard

| Area | Verdict after kill-test |
|---|---|
| Product / North-Star compatibility | PASS |
| Domain compatibility | PASS STRONG |
| Logical compatibility | PASS STRONG |
| PostgreSQL canonical authority | PASS STRONG |
| Material history | PASS |
| Multi-actor / non-account participants | PASS STRONG |
| Subject / Actor / Principal / Authority distinction | PASS STRONG |
| Scenario / hypothetical state | PASS |
| Work Supersession | PASS |
| Compound effects | PASS STRONG |
| Partial / unknown external outcomes | PASS STRONG |
| Crash / recovery semantics | PASS STRUCTURAL |
| Cancellation semantics | PASS |
| Revocation during Run | PASS |
| Direct privacy | PASS |
| Cumulative privacy inference | PASS AFTER v0.3 |
| Self-feedback / oscillation | PASS AFTER v0.3 |
| Attention overload | PASS AFTER v0.3 |
| Untrusted input / prompt injection boundary | PASS |
| Specialist-system boundary | PASS + EXPLICIT HARDENING |
| Offline / late-arriving state | PASS STRUCTURAL |
| Large fan-out | PASS SEMANTICALLY / IMPLEMENTATION SCALE OPEN |
| Reference / target resolution | P0 GAP → v0.4 CONTRACT ADDED |
| Policy composition / precedence | P0 GAP → v0.4 CONTRACT ADDED |
| Safe result publication / streaming | P0 GAP → v0.4 CONTRACT ADDED |
| Temporal source validity | HARDENING ADDED |
| Consequence classification | P0 HARDENING ADDED |
| Communication acknowledgement semantics | HARDENING ADDED |
| Need to reopen Domain | NO |
| Need to reopen Logical | NO |
| Need to reopen Physical | NO |
| Need to reopen PostgreSQL | NO |

The trajectory matters: successive rounds are now finding correctness conditions at execution/policy/publication boundaries rather than missing half of the platform or contradictions in the semantic core.

---

## 32. Remaining AI-02.1 acceptance work — one last mega stress-test

Before AI-02.1 can close, the v0.4 model must undergo **one final broad mega stress-test**.

This is intentionally the last mega-test in AI-02.1.

The goal is not to invent another gap by force. It is to attempt one last whole-system collapse of v0.4 across a very broad set of human situations and failure combinations.

After that mega-test:

```text
if a new fundamental responsibility gap appears
→ repair the smallest justified architecture boundary
→ perform targeted verification of that repair

if only bounded implementation/detail questions remain
→ do not restart another mega-test cycle
→ proceed to the explicitly required remaining pre-AI-03 review
```

The mega-test must exercise at least:

```text
single person
family / household
children / minors
older / low-digital participants
student / teacher / school coordination
caregiver / sensitive personal data
health/wellbeing planning without clinical-system substitution
shift / emergency work
freelancer / employee / manager
business / supplier / customer coordination
agriculture / field work / weather / resources
artisan / production
travel / cross-timezone work
creative / media / documents
legal / highly sensitive context
public-service / institutional boundary
very large multi-actor fan-out
non-DANTE participants
offline / multi-device / delayed sync
ambiguous identity/reference resolution
malicious/untrusted external content
cumulative privacy probing
policy conflicts and precedence
Authority/Consent revocation
stale material state
time-expiring external sources
source correction/retirement
partial external effects
ambiguous provider outcome
process crash / durable resume
cancellation after dispatch
work supersession
self-generated feedback loops
attention saturation
resource pressure
streaming / voice / multimodal output
future much-more-capable general-purpose conversational intelligence
```

The final hostile scenario should deliberately combine many of these rather than merely replaying independent examples.

The v0.4 architecture passes only if it can preserve, simultaneously:

```text
correct target identity
correct policy precedence
canonical/history integrity
no stale-state overwrite
no stale-source assumption
no blind retry
truthful partial/unknown outcome
scope-aware supersession
revocable permissions
no cross-query privacy reconstruction
no raw sensitive streaming
no false success publication
no self-oscillation
no attention storm
no specialist-system authority inflation
no collapse of sent/delivered/acknowledged/accepted
no Domain/Logical duplication for convenience
```

---

## 33. Regression checklist for the last mega stress-test

Every remaining AI-02.1 scenario must check:

```text
[ ] no accepted Domain distinction collapsed
[ ] no provider state promoted to canonical truth
[ ] no inference presented as Confirmation
[ ] no history rewritten to match the current plan
[ ] no stale material state silently overwritten
[ ] no stale Basis dependency ignored
[ ] no time-sensitive source assumed current merely because its version did not change
[ ] no unrelated output invalidated without reason when dependency-local validation is possible
[ ] no effect declared successful without sufficient evidence
[ ] no blind retry across an ambiguous external effect
[ ] cancel Run not represented as undo of already-dispatched effects
[ ] no Authority inferred from technical capability
[ ] no Visibility used as Authority
[ ] no active Run assumes Authority/AuthZ/Consent remains valid forever
[ ] user autonomy does not override external/institutional authority it does not own
[ ] policy precedence is not improvised by the language model
[ ] consequence level is sufficient to set governance/verification floor
[ ] no private source disclosed merely because its consequence is usable
[ ] no cumulative query sequence reconstructs protected information without bounded control
[ ] visible endpoints do not imply an unauthorized hidden relationship
[ ] no raw provider/model stream bypasses disclosure/information-flow checks
[ ] no provisional/unknown effect is published as verified success
[ ] no display-name or model guess becomes a consequential target without adequate resolution
[ ] ambiguous/unresolved target causes clarification/no effect
[ ] no other actor collapsed into account holder/user
[ ] no unresolved durable work trapped only in chat state
[ ] no hypothetical scenario treated as current reality
[ ] no ChangeSet hides partial completion
[ ] no superseded Run presents obsolete proposal as current
[ ] no superseded Run dispatches newly obsolete effects
[ ] no newer Run accidentally cancels independent work
[ ] no DANTE adaptation recursively triggers itself without material new reality
[ ] no user attention flood from individually-valid signals when batching/suppression is appropriate
[ ] DANTE representation does not claim institutional System-of-Record authority
[ ] sent/delivered/seen/acknowledged/accepted are not collapsed
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
Reference / Target Resolution is safe for consequential work
Scenario Workspace does not create a second truth
BasisManifest/dependency/temporal invalidation is coherent
Policy composition/precedence is coherent
ConsequenceProfile can establish minimum governance without becoming a universal score
ChangeSet/Effect interaction preserves WL-H obligations
Work Supersession does not corrupt independent work or already-attempted effects
Attention/proactivity does not fabricate outcomes or self-oscillate
Attention load can be bounded across multiple signals
Disclosure Projection preserves privacy/Visibility semantics across single and cumulative queries
Safe Result Publication prevents streaming/presentation from bypassing disclosure or verification
active-Run authorization/data validity can be revoked/revalidated
DANTE representation remains distinct from external institutional System-of-Record authority
communication state does not collapse sent/delivered/seen/acknowledged/accepted
future frontier-chat extensibility survives
the one last mega stress-test does not require semantic collapse
```

Only then should detailed memory admission, retrieval strategy, embeddings, indexes, conversation history and lifecycle be selected.

---

## 35. Current phase verdict

AI-02.1 v0.4 is the current branch-local architecture checkpoint.

The central thesis remains intact:

> **DANTE is a domain-centered intelligence platform around replaceable cognition, not a model-centric application.**

Round I exposed missing first-class responsibilities around hypothetical state, compound change, attention, disclosure, structured semantic access and conversational lifecycle.

Round II attacked the reengineered model under concurrency, cumulative privacy inference, self-generated feedback, revocation, superseding intent, partial effects, crashes, corrections and multi-actor pressure. It produced the v0.3 hardenings around cumulative disclosure, causal loops, Work Supersession, BasisManifest, revocable Run validity, Attention budgeting and cancellation semantics.

The Final Kill-Test broadened the attack again across agriculture, education, shift work, caregiving, legal/sensitive work, family, business, public/institutional boundaries, offline operation, large fan-out and future rich conversational surfaces. It found three P0 correctness gaps at the runtime edges:

```text
Reference / Target Resolution
Policy Composition / Precedence + ConsequenceProfile
Safe Result Publication / Streaming
```

and three additional hardenings:

```text
Basis temporal validity
DANTE representation != external institutional System of Record authority
sent != delivered != seen != acknowledged != accepted
```

All were repairable inside intelligence/runtime responsibility boundaries without creating new Domain owners or producing evidence sufficient to reopen Domain, Logical, Physical or PostgreSQL.

Current v0.4 includes all earlier contracts plus these additions.

Current status:

```text
AI-02.1
ACTIVE
REENGINEERED TO v0.4
ROUND I COMPLETE
ROUND II COMPLETE
FINAL KILL-TEST COMPLETE
ONE LAST MEGA STRESS-TEST REQUIRED
NOT CLOSED

DOMAIN / LOGICAL / PHYSICAL / POSTGRESQL REOPEN
NOT JUSTIFIED BY CURRENT PRESSURE-TEST EVIDENCE

AI-03
NOT STARTED
BLOCKED UNTIL AI-02.1 STRUCTURAL ACCEPTANCE
```

No runtime, provider, backend implementation or database PASS is claimed by this document.
