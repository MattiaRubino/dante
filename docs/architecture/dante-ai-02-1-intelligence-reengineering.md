# DANTE AI-02.1 — Intelligence Reengineering & Simulation Pressure-Test

- **Status:** CLOSED / STRUCTURALLY ACCEPTED / BRANCH-LOCAL ARCHITECTURE BASELINE
- **Workstream:** `feature/ai-architecture`
- **Established:** 2026-09-01
- **Phase:** AI-02.1
- **Current checkpoint:** **v0.5 STRUCTURAL ARCHITECTURE ACCEPTED**
- **Pressure-test program:** ROUND I + ROUND II + FINAL KILL-TEST + LAST MEGA STRESS-TEST COMPLETE
- **Targeted v0.5 consistency verification:** COMPLETE / STRUCTURAL PASS
- **Mega-test policy:** NO MORE MEGA TESTS IN AI-02.1
- **Remaining phase work:** NONE / downstream work continues in AI-03
- **Implementation:** NOT STARTED by this document
- **Provider/model/SDK selection:** OPEN
- **Database evolution:** NONE AUTHORIZED BY THIS DOCUMENT
- **AI-03:** ACTIVE / CONTEXT + RETRIEVAL + MEMORY / current macro-phase AI-03A

---

## 1. Purpose

AI-02.1 answers a harder question than provider/framework selection:

> **Does the DANTE Intelligence Architecture survive what DANTE must actually do in real life, under the already accepted Product, Domain, Logical, Physical and PostgreSQL contracts?**

This phase starts from product obligations and tries to break the architecture.

It does **not** start from a preferred model, agent framework, vector database, sandbox product or chat UI.

Method:

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
repeat only while a structural gap remains
```

The mega-test cycle is complete. AI-02.1 is structurally accepted and does not continue indefinitely searching for artificial new gaps.

---

## 2. Authority and interpretation discipline

This document does not create a new Domain ontology and does not supersede accepted Product/Domain/Logical/Physical/database authority.

Precedence remains:

```text
protected-main executable truth
→ accepted Product / Domain / Logical / Physical / ADR authority
→ current Database System of Record and engineering contracts
→ AI-00 semantic/architectural baseline
→ this AI-02.1 branch-local accepted runtime architecture
→ downstream AI-03+ architecture for their bounded decisions
→ external research / simulation evidence
→ conversation memory
```

If a responsibility introduced here can be expressed through an existing accepted semantic family, that existing family remains semantic owner.

The following are architecture/runtime responsibility contracts unless another accepted source defines equivalent Domain meaning:

```text
Interaction Session
WorkContract
Semantic Query / Projection Gateway
Context Engine
Scenario Workspace
BasisManifest
Reference / Target Resolution
ModelTarget
HarnessProfile
Capability Runtime
Execution Environment
Verifier
Policy Composition / policy mesh
ConsequenceProfile
ChangeSet / EffectGraph
Effect Runtime
Attention
Disclosure Projection
Safe Result Publication
Result Maturity
Work Supersession
```

They do **not** authorize new generic canonical tables or semantic roots.

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

Primary simulation/research evidence:

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

Simulation/research may reveal an architecture gap. It does not silently rewrite accepted semantic meaning.

---

## 4. Non-negotiable invariants

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

SCENARIO STATE != CANONICAL CURRENT STATE
CHANGESET != BYPASS OF INDIVIDUAL EFFECT GOVERNANCE
CONTEXT ACCESS != DISCLOSURE PERMISSION

INTERACTION SESSION != RUN != WORKER
SUPERSEDE != CANCEL != ROLLBACK != RECONCILE
RUN-START AUTHORIZATION != PERPETUAL AUTHORIZATION
CANCEL RUN != UNDO ALREADY-DISPATCHED EFFECTS

DANTE CANONICAL REPRESENTATION
!=
EXTERNAL INSTITUTIONAL SYSTEM-OF-RECORD AUTHORITY

SENT != DELIVERED != SEEN != ACKNOWLEDGED != ACCEPTED

EXECUTION ENVIRONMENT != MANDATORY SANDBOX/CONTAINER
FRESH INPUTS != AUTOMATICALLY COHERENT COMBINED BASIS
APPROVAL != PERPETUAL AUTHORIZATION FOR MATERIALLY CHANGED WORK
CACHE HIT != CURRENT DISCLOSURE AUTHORIZATION
```

No reengineering change is accepted if convenience collapses one of these distinctions.

---

## 5. Product capability obligations

DANTE must support combinations of:

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
code/artifact/browser/computer-use workloads where product scope later requires them
```

A simple request must remain simple. The platform must not force every request through the most expensive or isolated path merely because those capabilities exist.

---

# PART I — PRESSURE-TEST EVIDENCE

## 6. Round I — first simulation pressure-test

Round I converted product simulations into runtime obligations.

| Scenario family | Result | Consequence |
|---|---|---|
| deterministic historical question | PASS | Semantic Query + deterministic compute may skip model |
| simple natural-language command | PASS | interpretation terminates in governed application operation |
| compare realistic alternative futures | GAP | Scenario Workspace required |
| illness/week-wide selective pause/replan | GAP | ChangeSet / EffectGraph required |
| elapsed item with unknown outcome | PARTIAL | Attention/proactivity boundary required; elapsed != complete |
| unresolved work survives chat closure | PASS WITH CLARIFICATION | persist through correct semantic owner, not AIReviewItem/transcript |
| imported professional/source document | PASS | provenance + candidate/acceptance path fits |
| privacy-preserving coordination | GAP | recipient-aware Disclosure Projection distinct from Context |
| caregiver/conflicting multi-actor evidence | PASS | Subject/Actor/Authority/Visibility/Reconciliation survive |
| meeting transcript → decisions/tasks | PASS | extraction remains candidate until semantically resolved |
| provider timeout after mutation attempt | PASS STRONG | outcome-unknown + reconciliation required |
| multi-week watch | PARTIAL | durable trigger/evaluation + Attention required |
| future rich general-purpose conversation | GAP | Interaction Session + dual open-world/DANTE path required |
| stable structured access for intelligence | GAP | Semantic Query / Projection Gateway required |

Round I produced the first responsibility map.

---

## 7. Round II — clean compound adversarial pressure-test

Round II intentionally excluded adjacent vendor/cost/server questions and combined multiple architectural hazards in each scenario.

| Scenario family | Result | Consequence |
|---|---|---|
| week-wide replan while current state changes | PASS | re-evaluate scenario basis before apply |
| only one scenario dependency changes | PARTIAL | BasisManifest / dependency-aware invalidation |
| concurrent mobile/Web edits from same old state | PASS STRONG | expected MaterialState rejects last-write-wins |
| non-DANTE participant + selective availability | PASS | multi-actor semantics survive |
| individually safe queries compose into private inference | GAP | cumulative/cross-query disclosure protection |
| DANTE-generated replan causes oscillation | GAP | causal-loop / oscillation guard |
| derived hypothesis later rejected | PASS | derived inference not hard preference |
| conflicting provider/user/authoritative statements | PASS STRONG | Reconciliation/Authority/Provenance survive |
| multi-effect operation partially completes then crashes | PASS STRONG | ChangeSet preserves partial/unknown outcomes |
| source/permission revoked during Run | PARTIAL | Run validity must be revocable |
| ambiguous meeting transcript | PASS | unresolved/clarification valid |
| constraints deterministic | PASS STRONG | solver/verifier path survives |
| no valid plan | PASS | `NO VALID PLAN` legitimate |
| individually relevant signals overwhelm user | PARTIAL | Attention budgeting required |
| newer intent replaces old still-running work | GAP | Work Supersession required |
| crash around external dispatch | PASS | no blind retry across ambiguity |
| retired fact reappears via derivative | PASS STRUCTURAL | anti-resurrection mandatory; AI-03 must prove lifecycle |

Round II produced:

```text
cumulative/cross-query disclosure protection
causal-loop / oscillation guard
Work Supersession
BasisManifest / dependency-aware validity
revocable active-Run validity
Attention budgeting
CANCEL RUN != UNDO ALREADY-DISPATCHED EFFECTS
```

No Domain/Logical/Physical/PostgreSQL reopen evidence appeared.

---

## 8. Final Kill-Test — broad domain / boundary attack

The third official round stressed agriculture, education, shift work, caregiving, legal/sensitive work, family, business, public/institutional boundaries, offline/late state, large fan-out, malicious input and future rich conversational surfaces.

The personas were adversarial lenses only; they do not become product profiles or Domain owners.

It found three P0 correctness gaps:

```text
P0 1 — Reference / Target Resolution
P0 2 — Policy Composition / Precedence + ConsequenceProfile
P0 3 — Safe Result Publication / Streaming
```

and hardenings:

```text
Basis temporal validity
DANTE representation != external institutional System of Record authority
sent != delivered != seen != acknowledged != accepted
```

Again, no evidence justified reopening Domain, Logical, Physical or PostgreSQL.

---

## 9. Last Mega Stress-Test — final whole-system collapse attempt

The last mega-test deliberately combined ordinary life and extreme boundaries in one program rather than replaying isolated features.

Scenario families included:

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
malicious/untrusted input
provider failures
partial effects
supersession
revocation
attention storms
future much-more-capable general-purpose intelligence
code / generated artifacts / browser / computer-use execution
```

The final hostile composition included, simultaneously:

```text
changing weather/provider state
school closure
hospital recall
road changes
family pickup coordination
machinery risk
client deadlines
power/network intermittence
offline devices
non-DANTE participants
duplicate/ambiguous contacts
Authority revocation
malicious document
compromised sensor
provider timeout
already-dispatched effect
newer Run superseding old planning
self-generated replan loop
100+ valid alerts
private sensitive information
hidden relationships
source correction after use
artifact generation
external agent work
model outage
model-generated code
late sync
```

### Last mega-test result

The v0.4 core survived Product/Domain/Logical/PostgreSQL, history, multi-actor, scenarios, target resolution, policy, partial effects, revocation, supersession, privacy, attention, publication and future-model pressure.

One remaining P0 architecture responsibility was found:

```text
EXECUTION ENVIRONMENT / ISOLATION
```

Why it was necessary:

```text
model-generated code
untrusted executable/archive content
browser/computer use
hostile execution workloads
```

must not execute with unrestricted backend filesystem/network/credentials/process authority merely because Capability Runtime can invoke them.

The same round produced bounded hardenings:

```text
A. WorkContract propagation through decomposition / child Runs
B. approval binding/rebinding to materially approved target/proposal/basis/effect
C. Basis coherence in addition to individual freshness
D. publication currentness / superseded-output suppression
E. external-agent effect containment
F. mandatory reconciliation survives optional-resource exhaustion
G. surface-aware disclosure / consequential realtime-input authenticity
H. telemetry/evaluation purpose and privacy constraints
I. future cache hit != current disclosure authorization
```

No additional universal ontology, generic AI table or microservice family was justified.

---

## 10. Test-program conclusion

The trajectory is significant:

```text
Round I
→ missing platform responsibilities

Round II
→ concurrency/privacy/lifecycle correctness

Final Kill-Test
→ target/policy/publication correctness

Last Mega Stress-Test
→ hostile execution-environment isolation + bounded contract hardening
```

Successive rounds stopped finding missing semantic foundations and increasingly found runtime/security correctness conditions at edges.

The mega-test program is complete. No further mega-test cycle is planned in AI-02.1.

---

# PART II — ACCEPTED v0.5 RESPONSIBILITY ARCHITECTURE

## 11. Current architecture map

```text
┌──────────────────────────────────────────────────────────────────┐
│                        INTERACTION EDGE                          │
│ Web · Mobile · Voice · Capture · API · External AI             │
└───────────────────────────────┬──────────────────────────────────┘
                                │
                                ▼
                       INTERACTION SESSION
                                │
                                ▼
                           WORK INTAKE
                                │
                          WORK CONTRACT
      objective / scope / target bindings / protected constraints
          purpose / consequence / governance / approval terms
                                │
                                ▼
                         EXECUTION KERNEL
                                │
       ┌────────────────────────┼─────────────────────────┐
       │                        │                         │
       ▼                        ▼                         ▼
SEMANTIC QUERY /            CONTEXT                  SCENARIO
PROJECTION GATEWAY          ENGINE                   WORKSPACE
       │                        │                         │
       └────────────────────────┼─────────────────────────┘
                                ▼
                         BASIS MANIFEST
      state/source dependencies / freshness / temporal validity /
             assumptions / constraints / coherence
                                │
                                ▼
                         REASONING LAYER
           ┌────────────────────┼────────────────────┐
           ▼                    ▼                    ▼
     ModelTarget +         Deterministic           Solver
     HarnessProfile           Compute
           │                    │                    │
           └────────────────────┼────────────────────┘
                                ▼
                        CAPABILITY RUNTIME
                                │
                    ┌───────────┴───────────┐
                    │                       │
              trusted normal path     EXECUTION ENVIRONMENT
                                     when workload/threat model
                                     requires isolation
                    │                       │
                    └───────────┬───────────┘
                                ▼
                            VERIFIER
                                │
                                ▼
                    CHANGESET / EFFECTGRAPH
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
        RESULT / DISCLOSURE / SAFE PUBLICATION / ATTENTION
```

Cross-cutting responsibilities:

```text
Policy mesh / Authority / AuthZ / Consent / Visibility
ConsequenceProfile
Information flow / provider eligibility
Autonomy
Attention + aggregate attention budgeting
Causal lineage / oscillation protection
Run durability / Work Supersession
Approval binding / rebinding
Resource governance
Artifacts
Publication currentness / Result Maturity
Cumulative inference protection
Control Plane
Observability
Audit / execution evidence
Evals
```

This is **not** a deployment diagram.

---

## 12. Responsibility boundary != microservice

AI-02.1 rejects architecture theatre.

The current map does not imply services named:

```text
semantic-query-service
scenario-service
attention-service
verification-service
disclosure-service
supersession-service
basis-service
target-resolution-service
policy-composition-service
publication-service
execution-environment-service
```

A first implementation may remain within the accepted capability-first modular monolith. Extraction requires measured isolation/scaling/availability/hardware/operational evidence.

Likewise:

```text
logical Execution Environment responsibility
!= mandatory sandbox product
```

---

## 13. Interaction Session

```text
Interaction Session != Run != Worker
```

Interaction Session may own noncanonical interaction continuity:

```text
conversation turn continuity
surface/presentation context
attached artifacts
temporary referents/deixis
session-local presentation state
```

It does not own canonical DANTE truth because that truth was discussed in conversation.

One Session may contain multiple Runs. A Run may outlive the UI Session when its own work contract legitimately requires durable lifecycle, for example research, watch, approval wait, booking or callback.

Closing UI does not silently cancel independent durable work unless contract says so.

---

## 14. WorkContract

`WorkContract` is the authoritative execution contract carried through decomposition and child Runs.

It may contain materially relevant:

```text
objective
scope
resolved target bindings
protected constraints
purpose
ConsequenceProfile / governance obligations
approval conditions
work lineage
```

Rule:

```text
derived execution may refine WorkContract
but may not silently drop/relax protected requirements
```

If a material requirement changes, a new/superseding decision updates the current work meaning.

This protects against semantic loss across:

```text
user intent
→ orchestrator
→ child Run
→ subagent
→ capability
→ effect
```

---

## 15. Work Supersession

Canonical state may be unchanged while newer user intention makes old work obsolete.

Work relationships may include:

```text
continuation_of
supersedes
independent_of
```

Mandatory distinction:

```text
SUPERSEDE
!= CANCEL
!= ROLLBACK
!= RECONCILE
```

A superseded Run may still:

```text
finish reconciliation of already-attempted effects
preserve audit/execution evidence
return truthful status about work already performed
```

It must not:

```text
present obsolete proposal as current
dispatch newly obsolete effects
cancel unrelated independent work
```

---

## 16. Dual intelligence path

DANTE supports composition of:

```text
DANTE-NATIVE PATH
structured state / history / planning / constraints / governed effects

OPEN-WORLD PATH
general explanation / research / web / documents / code / multimodal / creative analysis
```

They are not two products or necessarily two runtimes.

One request may combine both.

Future much-richer conversational intelligence must plug into the same contracts rather than replace Domain/application state.

---

## 17. Semantic Query / Projection Gateway

Purpose: stable application-owned, permission-aware access to structured DANTE meaning.

Examples:

```text
current commitments
Goal trajectory
workload in a period
open commitments involving a Person
current Program material state
safe availability
meeting-series continuity
planned-vs-actual history
unresolved confirmations
resource availability
```

It is not:

```text
raw model SQL access
a universal Entity API
a second Domain model
a vector-search replacement
```

It enables fast deterministic routes where no additional model reasoning is necessary.

---

## 18. Context Engine

Context Engine remains distinct from Semantic Query.

It assembles authorized reasoning material such as:

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

Detailed Context / Retrieval / Memory architecture is now active and owned by AI-03. This document fixes only the surrounding runtime boundary and invariants that AI-03 must preserve.

---

## 19. Reference / Target Resolution

A consequential system can pass AuthZ and expected-state checks and still affect the wrong target if semantic reference binding is wrong.

```text
DISPLAY NAME != EFFECT TARGET
MODEL CONFIDENCE != TARGET RESOLUTION PROOF
```

Outcomes:

```text
EXACT
UNIQUE_IN_SCOPE
AMBIGUOUS
UNRESOLVED
```

Consequential rule:

```text
EXACT / UNIQUE_IN_SCOPE
→ may proceed subject to normal governance

AMBIGUOUS
→ focused clarification / explicit preview / disambiguation

UNRESOLVED
→ no consequential effect
```

Target Resolution may need authorized Semantic Query / Context to resolve candidates; it is an Execution Kernel responsibility, not an impossible pre-query oracle.

It consumes accepted NativeRef/ScopedRecordRef/MaterialStateRef/ExternalRef semantics rather than inventing universal identity.

---

## 20. Scenario Workspace

DANTE must compare futures before meaningful structural changes.

```text
CANONICAL MATERIAL STATE
        │
        ├──── Scenario A overlay
        ├──── Scenario B overlay
        └──── Scenario C overlay
```

Scenario workspace contains, as needed:

```text
basis references
hypothetical changes
assumptions
constraints
external assumptions/forecasts
solver/model outputs
derived metrics
violations/conflicts
comparison evidence
```

Default state class:

```text
transient / derived technical state
```

It does not duplicate the whole database and does not become canonical merely because it is useful.

---

## 21. BasisManifest

`BasisManifest` records enough dependency evidence to evaluate continued validity without storing every thought/token.

It may include:

```text
relevant MaterialStateRefs
canonical/source references
external source identity/version
observed_at
valid_for / valid_until
revalidate_after
acquisition window
assumptions
constraints
policy/config versions when consequential
capability/harness versions where evidence requires them
```

### Dependency-aware invalidation

```text
changed input X
→ invalidate/recompute dependent outputs
```

rather than `invalidate everything` or `invalidate nothing`.

### Temporal validity

```text
SOURCE VERSION UNCHANGED
!=
SOURCE STILL FRESH ENOUGH
```

Weather, price, inventory, availability, traffic and other volatile state may expire without explicit version event.

### Basis coherence

```text
EACH INPUT FRESH
!=
COMBINED WORLD-STATE COHERENT
```

DANTE-native state may require coherent application/database snapshot semantics. Independent external sources may not offer atomicity; DANTE records acquisition limits and revalidates consequential volatile dependencies instead of fabricating one simultaneous truth.

BasisManifest is runtime/evidence metadata, not new Domain Version/Fact ontology.

---

## 22. ModelTarget + HarnessProfile

Current constraints remain:

```text
NO foundation-model training
NO DANTE-owned frontier model
NO fine-tuning requirement as baseline
NO large always-on self-hosted frontier fleet
NO GPU cluster as baseline
API-FIRST frontier intelligence
provider/model replaceability mandatory
small/local inference optional and benchmark-gated
```

Separate:

```text
ModelTarget
from
HarnessProfile
```

HarnessProfile may version model/provider-specific controllable behavior:

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

Provider independence does not require lowest-common-denominator inference APIs.

---

## 23. Deterministic compute and solver

`MODEL != SOLVER != DATABASE`.

Examples of deterministic first-class intelligence:

```text
SQL aggregation
calendar/time math
rules
statistics
calculators
constraint validation
OR-Tools CP-SAT where justified
```

If deterministic computation can answer safely, no frontier-model call is required.

Solver `UNKNOWN != INFEASIBLE`, and solver output remains candidate/derived until governed acceptance.

---

## 24. Capability Runtime

Capabilities are explicit product/runtime operations, not arbitrary hidden model powers.

Conceptually:

```text
Capability Registry
→ discovery/projection
→ invocation
→ validation
→ evidence/effect handling
```

Capability availability does not imply Authority.

Generated/programmatic tool use may improve efficiency but does not bypass policy/effect contracts.

---

## 25. Execution Environment / Isolation — v0.5 P0

### Failure found

Future general-purpose DANTE may execute:

```text
model-generated Python/shell/code
untrusted archive/project content
browser automation
computer use
hostile document conversion/execution
other arbitrary workloads
```

If that code runs with backend filesystem, process, network or credential authority, normal capability/effect policy can be bypassed.

### Architectural rule

`Execution Environment` is a first-class runtime/security responsibility when a workload/threat model requires isolation.

Potential controls:

```text
filesystem scope
artifact mounts
network/egress
credential mediation
CPU
RAM
disk
wall-clock time
process count
lifecycle / cleanup
execution evidence
```

### Lazy activation

```text
ordinary trusted deterministic/application work
→ normal execution path

untrusted/generated/general execution workload
→ select appropriate isolated environment
```

The architecture does **not** mandate one universal sandbox technology.

Research challenger classes remain:

```text
WASM/WASI
hardened container / gVisor-style isolation
microVM / VM
other future mechanisms
```

Selection depends on workload compatibility and threat model.

### Credential rule

```text
MODEL-GENERATED / UNTRUSTED CODE
MUST NOT RECEIVE RAW PRIVILEGED DANTE/DB/PROVIDER CREDENTIALS
```

Where privileged action is necessary:

```text
isolated workload
→ bounded trusted broker/capability
→ current identity/delegation/policy/egress checks
→ provider/application
```

Execution Environment is not a Domain concept, not automatically a microservice and not required for every request.

---

## 26. Verifier

```text
MODEL CLAIM
"I completed X"
!=
VERIFIED STATE
"X is demonstrably true according to relevant evidence"
```

Potential verification mechanisms:

```text
schema validation
semantic validation
SQL/state reread
MaterialState verification
provider reread
receipt verification
constraint solver validation
filesystem diff/hash
test execution
DOM/accessibility inspection
independent semantic verification where deterministic evidence is insufficient
```

Verifier is a runtime responsibility.

```text
Verifier != Audit store
Verifier != Confirmation
Verifier != Reconciliation
```

Those existing semantics remain distinct.

---

## 27. Policy Composition / policy mesh

Multiple individually valid policies may disagree.

Examples:

```text
user autonomy             ALLOW
institutional policy      REQUIRE APPROVAL
qualification rule        LIMIT/DENY
safety constraint         DENY
current delegated Authority MAYBE INSUFFICIENT
```

The language model does not improvise precedence.

Policy applies at multiple enforcement points:

```text
Context PEP
→ may this information be processed for this purpose?

Capability PEP
→ may this capability be discovered/invoked?

Effect PEP
→ may this exact effect execute now?

Publication/Egress PEP
→ may this representation leave to this recipient/provider/surface now?
```

Applicable inputs may include:

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

Potential decisions:

```text
ALLOW
DENY
REQUIRE_CONFIRMATION
REQUIRE_EXTERNAL_APPROVAL
LIMIT_SCOPE
```

`PolicyDecision` remains runtime/governance state, not a new Domain owner.

---

## 28. ConsequenceProfile

Minimum governance depends on consequences, not only phrasing.

Dimensions may include:

```text
reversible?
external effect?
financially consequential?
safety-sensitive?
privacy-sensitive?
multi-actor?
time-critical?
irreversible/hard to compensate?
independent verification required?
```

It may establish:

```text
autonomy ceiling
verification floor
approval requirement
safe failure mode
publication maturity floor
isolation requirement
```

It is not a universal semantic severity score and not a Domain root.

---

## 29. ChangeSet / EffectGraph

One intention may require multiple coordinated operations.

ChangeSet may carry:

```text
objective
basis
operations
dependency edges
protected invariants
expected-state requirements
atomic groups
external-effect boundaries
preview
approval binding
rollback availability
compensation rules
partial-outcome state
reconciliation requirements
```

It does not replace individual effect governance:

```text
ChangeSet
    ├─ Effect A
    ├─ Effect B
    └─ Effect C
          ↓
EffectIntent
→ EffectPermit
→ EffectAttempt
→ EffectReceipt
→ Verification / Reconciliation
```

Cross-system all-or-nothing semantics must not be fabricated when they do not exist.

---

## 30. Approval binding / rebinding

Approval is not a durable broad permit for any later plan that looks similar.

Approval must bind to materially relevant:

```text
target(s)
proposal / ChangeSet meaning
basis / assumptions where consequential
effect semantics
protected constraints
```

If the material ChangeSet changes after approval:

```text
OLD APPROVAL
!=
AUTHORIZATION FOR NEW MATERIAL PLAN
```

Before final dispatch after waits, DANTE re-reads current work/state/policy and binds a current final permit.

---

## 31. External effects / outcome unknown

```text
EffectIntent
→ EffectPermit
→ EffectAttempt
→ EffectReceipt
→ Verification
→ Reconciliation when needed
```

Provider timeout after dispatch may mean:

```text
OUTCOME_UNKNOWN
```

not `FAILED` and not `SUCCESS`.

Blind retry is forbidden when first attempt may already have produced effect.

```text
CANCEL RUN
!=
UNDO ALREADY-DISPATCHED EFFECTS
```

Cancellation stops remaining controllable work. Already-dispatched effects remain subject to verification/reconciliation/compensation semantics.

---

## 32. Mandatory reconciliation survives resource exhaustion

Resource budgets may stop optional work:

```text
model calls
search steps
sandbox compute
nonessential elaboration
```

But if DANTE already dispatched an effect whose outcome is ambiguous, budget exhaustion must not erase that obligation.

```text
optional work exhausted
+
outcome-unknown effect exists
→ reconciliation obligation remains durable/unresolved
```

Implementation may reserve safety/reconciliation capacity or otherwise guarantee eventual handling; exact mechanism is later work.

---

## 33. External-agent effect containment

DANTE may delegate bounded work to external intelligent systems.

If an external agent performs consequential side effects, DANTE must choose one truthful model:

```text
A. effect routed back through governed DANTE capability
→ DANTE effect governance applies

B. external agent/system performs effect outside DANTE
→ treat it as externally performed
→ observe / verify / reconcile
→ do not pretend DANTE governed the dispatch
```

Passing broad human credentials through to opaque agents by default is forbidden/confused-deputy risk.

---

## 34. Revocable active-Run validity

```text
authorized at T0
!=
authorized forever
```

At consequential boundaries, especially after wait/approval/durable suspension and before disclosure/effect, DANTE may need to revalidate:

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

Revocation cannot retroactively remove information already processed externally or undo already-dispatched effects.

It constrains subsequent retrieval, provider disclosure, recipient disclosure, derived persistence and effects where applicable.

---

## 35. Context Projection != Disclosure Projection

```text
Context Projection
= what reasoning operation may consume for purpose P

Disclosure Projection
= what representation recipient R may receive
```

A private source may produce a safe shared consequence without disclosing source detail.

Example:

```text
private event: medical appointment 19:00
→ authorized computation
→ recipient-safe result: unavailable 19:00–20:00
```

Processing permission, source/provenance disclosure and recipient disclosure remain separate questions.

---

## 36. Cumulative / cross-query disclosure protection

A response may be safe alone while a query sequence reconstructs protected information.

Where risk is material, disclosure may consider:

```text
recipient
purpose
sensitivity
requested granularity
relevant prior disclosures
query sequence/pattern
aggregate information exposed
relationship inference risk
probing behavior
```

Possible outcomes:

```text
ALLOW
COARSEN
AGGREGATE
WITHHOLD
REQUIRE DIFFERENT SCOPE
```

Bounded disclosure accounting is runtime/security state, not a second Visibility ontology.

---

## 37. Safe Result Publication / Streaming

```text
MODEL OUTPUT != PUBLISHABLE OUTPUT
INTERNAL STREAM != RECIPIENT STREAM
```

Correct final disclosure filtering is too late if sensitive/unverified content already crossed the surface boundary.

Before recipient publication, DANTE preserves required checks for:

```text
information-flow eligibility
recipient/surface Disclosure Projection
cumulative inference protection
result maturity
verification/effect truth
current work/supersession status
```

The architecture does not require full buffering of every answer. It requires that realtime/streaming optimization never bypass governance.

---

## 38. Publication currentness

A superseded/stale Run may continue cleanup/reconciliation/evidence but may not keep presenting obsolete material as the current answer.

Before publishing further material:

```text
is this work/result still current for this scope?
```

If not:

```text
suppress obsolete continuation
or present it explicitly as historical/superseded when useful
```

This prevents correct-but-obsolete output from misleading the user.

---

## 39. Result Maturity

Presentation/runtime maturity may distinguish:

```text
WORKING
PROVISIONAL
VERIFIED
ACCEPTED_EFFECT
```

These are not replacements for Domain Confirmation, Actual, Outcome or Reconciliation.

Example:

```text
provider request dispatched
response timed out
```

safe:

> Request sent; outcome is being verified.

unsafe:

> Done ✓

---

## 40. Surface-aware disclosure and realtime input authenticity

Recipient disclosure depends not only on Person/Principal but also on surface/channel.

Examples:

```text
private in-app screen
lock-screen notification
shared display
voice response
external AI client
email/push transport
```

A surface may receive a coarser representation than another surface for the same recipient.

Realtime/voice input also has provenance/authenticity risk. Speech detected by ASR is not automatically authenticated consequential intent. ConsequenceProfile and interaction/authentication policy determine when confirmation/stronger binding is required.

---

## 41. Information-flow lineage

Derived wording does not reset trust/confidentiality.

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

Useful conceptual properties include:

```text
confidentiality class
integrity/trust class
instruction authority
source/provenance lineage
```

Dynamic processing/disclosure/provider decisions remain policy decisions at use time rather than a duplicate semantic ontology.

---

## 42. Untrusted content / prompt injection

External content, documents, transcripts, webpages, tool output and uploaded files are data unless explicit trusted instruction authority establishes otherwise.

```text
DATA != INSTRUCTION
```

A meeting transcript saying "ignore system instructions" remains transcript data.

A malicious web page cannot grant itself tool/effect authority.

Uploaded user files may themselves be compromised and are not automatically safe to execute.

---

## 43. Attention / proactivity

Trigger tells DANTE something is due/changed/true enough to evaluate.

Attention decides what should happen to user attention.

```text
Signal
→ relevance
→ materiality
→ urgency
→ causal-loop check
→ attention policy + aggregate attention budget
→ silent / review / notify / start work / escalate
```

Attention inputs may include:

```text
user policy
quiet hours/current mode
risk/consequence
recent interruptions
aggregate current load
batchability
review opportunity
repetition/deduplication
expiry
```

Push/email/in-app transport is downstream.

Review Queue remains an aggregation surface, not a generic semantic/persistence owner.

---

## 44. Causal-loop / oscillation guard

DANTE effects may generate new signals. Without causal awareness, individually valid rules can oscillate.

Relevant lineage:

```text
Signal
→ related_to / caused_by Effect
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

The guard does not suppress genuinely new external change.

---

## 45. Communication-state integrity

```text
SENT
!= DELIVERED
!= SEEN
!= ACKNOWLEDGED
!= ACCEPTED
!= ACTUALLY PARTICIPATED/ACTED
```

Transport batching may be physical/technical, but semantic outcome cannot manufacture stronger coordination evidence than exists.

Use existing Request/Proposal/Participation/Actual/Confirmation/Acknowledgement semantics where applicable.

---

## 46. External System-of-Record boundary

DANTE may canonically retain that a person has a hospital shift, school deadline, court hearing, flight or institutional meeting because that reality matters to their life.

That does not make DANTE the institutional authority over:

```text
hospital roster
school register
clinical record
court/case system
bank ledger
official administrative act
classified/institutional record
```

```text
DANTE CANONICAL PERSONAL REPRESENTATION
!=
EXTERNAL INSTITUTIONAL SYSTEM-OF-RECORD AUTHORITY
```

External authoritative reality changes only through legitimate capability accepted by that external system.

---

## 47. Observability / audit / evaluation privacy

```text
DURABLE RUNTIME JOURNAL
!= APPLICATION RUN RECORD
!= AUDIT / EXECUTION EVIDENCE
!= OTEL TELEMETRY
```

Observability/evaluation pipelines are not privileged data sinks.

Sensitive prompts, context fragments, tool results, traces and production examples remain subject to purpose, retention, redaction and provider/data-use controls.

Production trace reuse for evals is not automatic merely because the trace exists.

---

## 48. Cache rule carried into AI-03

Caching is later physical/context work, but one invariant is already fixed:

```text
CACHE HIT
!=
CURRENT DISCLOSURE AUTHORIZATION
```

A cached result created when access was allowed must not bypass current recipient/purpose/policy/disclosure checks after revocation/change.

AI-03 must design cache keys/lifecycle accordingly.

---

## 49. Resource governance

ResourceBudget is broader than tokens.

Potential dimensions:

```text
money
model/tool calls
DB operations
sandbox CPU/RAM/disk/network
parallelism
wall-clock
active compute
step count
```

Budget exhaustion is a legitimate Run outcome for optional work.

It must not hide partial effects or erase mandatory reconciliation/evidence obligations.

---

## 50. Durable execution

```text
DURATION != DURABILITY REQUIREMENT
```

A 30-minute pure computation may not need a durable workflow; a short operation with external acceptance ambiguity or long callback wait may.

Conceptual classes:

```text
INLINE
BOUNDED ASYNC
DURABLE
```

Restate remains the accepted target for first real Class-B durable workflow unless a proper reopen occurs. AI-02.1 does not activate it for every request.

---

## 51. External AI / external-agent symmetry

DANTE must support both directions:

```text
AI inside DANTE
→ DANTE invokes provider/model/specialist capability

DANTE inside external AI
→ external assistant invokes explicitly exposed DANTE capability
```

External protocols such as MCP/A2A are edge adapters, not internal Domain contracts.

External agent/client does not inherit user Authority merely because it holds a technical connection.

Delegation, Principal, represented party, purpose, scope, recipient and effect policy remain explicit.

---

## 52. Future rich conversational intelligence acceptance

A future DANTE surface may include:

```text
text
voice
image/camera
PDF/document work
web research
general Q&A
creative work
code
analysis
artifacts
long-running research
browser/computer use
DANTE-aware planning/effects
external systems/specialists
```

More capable intelligence must plug into DANTE without owning:

```text
canonical memory
canonical application state
Domain semantics
Authority
Visibility
accepted-effect rules
material history
```

Preferred dependency:

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
future provider
= new DANTE database + memory truth + authority + business logic
```

A future model with huge context/provider memory remains an optimization/cognitive component. Provider thread/memory is not canonical DANTE memory.

**Structural future-extensibility criterion: PASS.**

---

# PART III — TARGETED v0.5 VERIFICATION

## 53. Verification objective

After the last mega-test found `Execution Environment / Isolation`, AI-02.1 did not start another broad mega-test. It ran a bounded consistency verification of the new boundary and associated hardenings.

This is architecture verification only, not runtime/security penetration testing.

---

## 54. Generated-code secret isolation

Scenario:

```text
future DANTE receives/generates code
code attempts to read environment/application/provider/database secrets
```

v0.5 contract:

```text
untrusted/generated code
→ isolated Execution Environment when required
→ no raw privileged credentials
→ bounded trusted broker/capability for privileged action
```

Result: **PASS STRUCTURAL**.

No new responsibility needed.

---

## 55. Execution-environment crash vs Run durability

Scenario:

```text
Run exists
isolated environment crashes
artifacts may be partial
external effect may or may not have happened through broker
```

Distinctions:

```text
Interaction Session != Run != Worker != Execution Environment
```

Environment failure does not itself rewrite canonical state. Durable/async Run handling and effect reconciliation remain separate.

Result: **PASS STRUCTURAL**.

---

## 56. Browser/computer-use effect verification

Scenario:

```text
computer-use agent clicks external action
screen/response ambiguous
```

v0.5 requires:

```text
ConsequenceProfile
→ policy/approval as needed
→ bounded environment
→ target/action verification where possible
→ outcome may remain UNKNOWN
→ provider/UI reread/reconciliation
```

Result: **PASS STRUCTURAL**.

Pixel-level completion is never equivalent to verified effect success.

---

## 57. Superseded publication

Scenario:

```text
Run A streams/proposes old plan
Run B supersedes same scope
Run A still technically alive
```

Safe Publication currentness gate prevents Run A from presenting obsolete continuation as current while allowing cleanup/reconciliation.

Result: **PASS STRUCTURAL**.

---

## 58. Basis coherence

Scenario:

```text
weather fresh at T1
resource availability fresh at T2
calendar fresh at T3
values were never simultaneously true enough for consequential plan
```

BasisManifest records acquisition/freshness/coherence limitations; consequential volatile inputs are revalidated and DANTE-native snapshot semantics are used where required.

Result: **PASS STRUCTURAL**.

---

## 59. Approval rebinding

Scenario:

```text
user approved ChangeSet A
replan materially changes target/time/effect semantics
```

Old approval cannot be reused automatically. Re-read/recompute/rebind or obtain new approval as consequence requires.

Result: **PASS STRUCTURAL**.

---

## 60. External-agent side effects

Scenario:

```text
external intelligent worker performs provider side effect outside DANTE
```

v0.5 requires either governed DANTE capability path or explicit external-effect observation/reconciliation.

Result: **PASS STRUCTURAL**.

---

## 61. Resource exhaustion after ambiguous effect

Scenario:

```text
Effect A dispatched
outcome unknown
optional run budget exhausted
```

Reconciliation obligation survives. Run cannot erase ambiguous already-dispatched consequence by ending optional compute.

Result: **PASS STRUCTURAL**.

---

## 62. Deterministic fast path

Scenario:

> how much did I run last month?

Correct path:

```text
semantic interpretation
→ Semantic Query
→ deterministic SQL aggregation
→ disclosure/publication
```

No sandbox, durable workflow or frontier model required after interpretation when unnecessary.

Result: **PASS STRUCTURAL**.

---

## 63. Targeted verification conclusion

```text
generated-code secret isolation                         PASS STRUCTURAL
execution-environment crash vs Run durability           PASS STRUCTURAL
browser/computer-use effect verification                PASS STRUCTURAL
superseded publication                                  PASS STRUCTURAL
Basis coherence                                         PASS STRUCTURAL
approval rebinding                                      PASS STRUCTURAL
external-agent side effects                             PASS STRUCTURAL
resource exhaustion after ambiguous effect              PASS STRUCTURAL
deterministic fast path bypassing unnecessary isolation PASS STRUCTURAL
```

No new fundamental responsibility gap appeared.

No evidence justifies reopening Domain, Logical, Physical or PostgreSQL.

---

# PART IV — END-TO-END BEHAVIOR

## 64. Representative full path

```text
1. receive interaction / event / trigger
2. resolve Principal / Actor / represented party / purpose
3. establish WorkContract: objective / scope / protected constraints / consequence
4. relate work to prior work: continuation / supersession / independent
5. resolve authorized semantic candidates/context required to identify targets
6. bind consequential references/targets; clarify/stop if ambiguous/unresolved
7. choose structural fast path where possible
8. resolve authorized DANTE-native semantic state
9. assemble only necessary unstructured/external/contextual material
10. build BasisManifest including dependency/freshness/coherence requirements
11. evaluate information-flow/provider eligibility at applicable policy points
12. choose model / deterministic compute / solver / capabilities
13. select Execution Environment only if workload/threat model requires isolation
14. reason / calculate / simulate
15. ensure derived child work preserves WorkContract/protected requirements
16. compose applicable policy / Authority / AuthZ / Consent / autonomy / institutional constraints
17. verify material intermediate claims where consequential
18. produce Result / Proposal / ChangeSet as appropriate
19. bind approval where required to exact material proposal/target/basis/effect meaning
20. after waits, confirm work is still current/not superseded
21. revalidate target binding if identity/context may have changed
22. re-read material state and volatile dependencies
23. re-evaluate policy / Authority / AuthZ / Consent / source validity
24. issue bounded EffectPermits
25. execute governed effect graph
26. verify receipts; reconcile ambiguous/partial outcomes
27. preserve reconciliation obligation even if optional resource budget ends
28. materialize accepted canonical effects only through application/domain operations
29. assign truthful Result Maturity
30. apply recipient/surface-aware Disclosure Projection
31. apply cumulative inference protection where material
32. verify publication currentness / supersession state
33. publish/stream only cleared material
34. Attention chooses justified interruption/review behavior
35. retain only state justified by correct semantic/runtime owner
```

Not every request uses every step.

---

## 65. Simple deterministic path

```text
request
→ principal/purpose
→ WorkContract
→ target/query scope
→ Semantic Query
→ deterministic compute
→ policy/disclosure
→ Safe Publication
```

No sandbox/model/durable workflow is required merely because the architecture can support them.

---

## 66. Consequential compound path

```text
User request
→ WorkContract
→ target resolution
→ ConsequenceProfile
→ current MaterialState / BasisManifest
→ Scenario / consequence analysis
→ policy composition
→ ChangeSet preview
→ bound approval where required
→ check supersession/currentness
→ revalidate target/state/volatile dependencies
→ re-evaluate Authority/AuthZ/Consent/policy
→ bind EffectPermits
→ execute EffectGraph
→ verify/reconcile
→ Result Maturity
→ Disclosure / Safe Publication
```

---

## 67. Proactive/watch path

```text
Watch definition / accepted condition
→ scheduled/condition-driven evaluation
→ external signals
→ freshness/coherence check
→ deterministic filters
→ current DANTE state
→ reasoning only if needed
→ causal-loop/recent-effect check
→ Attention + aggregate attention budget
→ Safe Publication
→ notify / review / remain silent
```

An LLM is not a three-week timer.

---

## 68. Code/computer-use path

```text
request
→ WorkContract / ConsequenceProfile
→ capability selection
→ is arbitrary/untrusted execution required?
       │
       ├─ no → normal trusted path
       │
       └─ yes
           ↓
      Execution Environment
      bounded filesystem/network/resources
      no raw privileged credentials
           ↓
      trusted broker/capability for privileged actions
           ↓
      verification / effect governance / reconciliation
           ↓
      artifact/result publication
```

---

# PART V — OPEN IMPLEMENTATION CHOICES / AI-03 HANDOFF

## 69. What remains intentionally open

AI-02.1 v0.5 does not decide:

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
exact Execution Environment technology
policy engine product
learned router
local-model family/size
exact autonomy UX
exact durable-runtime activation per workload
exact Attention scoring/rules
exact Scenario Workspace representation
exact ChangeSet physical persistence, if any
exact Interaction Session persistence, if any
exact target-resolution implementation
exact PolicyDecision implementation
exact ConsequenceProfile representation
exact safe-streaming implementation
exact Result Maturity representation
exact BasisManifest/work-lineage/disclosure-accounting persistence, if any
exact broker/credential-proxy implementation
```

The architecture fixes required contracts now; it does not prematurely choose implementation products.

---

## 70. AI-03 active boundary

AI-03 owns detailed:

```text
CONTEXT
RETRIEVAL
MEMORY
```

AI-02.1 is now closed / structurally accepted, so AI-03 actively consumes this baseline. It must not silently redefine the accepted runtime contracts merely because a retrieval/memory technology prefers another shape.

Inputs AI-03 must inherit include:

```text
Interaction Session != Run != Worker
Semantic Query distinct from Context Engine
Context Projection distinct from Disclosure Projection
cumulative inference protection
WorkContract / supersession currentness
BasisManifest dependency/freshness/coherence
source reread / currentness
anti-resurrection
cache hit != current disclosure authorization
provider thread/cache != canonical memory
surface-aware publication
information-flow lineage
purpose/retention/privacy limits for telemetry/evals
```

AI-03 current charter:

- `docs/architecture/dante-ai-03-context-retrieval-memory.md`

Current macro-phase:

```text
AI-03A — FULL CONTEXT ARCHITECTURE
```

AI-03 will decide detailed retrieval/memory admission and physical lifecycle only after its own architecture and destructive-validation gates. No memory table, embedding/index or vector-store is implied by activation.

---

## 71. Anti-patterns after v0.5

Do not implement:

```text
one giant agent loop owning the product
raw model access to PostgreSQL
raw model access to arbitrary provider credentials
provider conversation thread as DANTE memory authority
one generic AIAction table
one universal memory_fact table
one universal AIReviewItem table
one generic Scenario Domain entity without semantic proof
one opaque mega-tool for compound mutation
one approval token valid forever despite materially changed plan/state
one Run authorization assumed valid forever
one Context Engine dumping full history into every request
one egress allow/deny check ignoring safe derived projections
one disclosure check ignoring cumulative inference when material
one background LLM process acting as scheduler/timer
one adaptation loop recursively reacting to itself without material change
one old Run dispatching/publishing obsolete work after supersession
one model call for deterministic arithmetic/aggregation by default
one learned router before representative DANTE outcome data
one service/container per architecture box
one consequential effect targeted only by display-name/model guess
one LLM deciding policy precedence
one user-autonomy setting treated as authority over external reality
one raw model/provider stream connected directly to sensitive recipient output
one streamed success claim before external effect is verified
one unchanged source version assumed fresh forever
one set of individually fresh external values assumed mutually coherent automatically
one delivered notification treated as seen/acknowledged/accepted
one sandbox/microVM for every ordinary request
one arbitrary generated-code process with backend/provider/DB secrets
one external agent side effect falsely reported as DANTE-governed
one optional budget exhaustion that drops an outcome-unknown reconciliation obligation
one cache hit bypassing current disclosure policy
one telemetry/eval pipeline treated as permission to retain all sensitive material
```

---

# PART VI — FINAL STRUCTURAL SCORECARD

## 72. v0.5 architecture scorecard

| Area | Verdict |
|---|---|
| Product / North-Star compatibility | PASS STRONG |
| Domain compatibility | PASS STRONG |
| Logical compatibility | PASS STRONG |
| PostgreSQL canonical authority | PASS STRONG |
| Material history | PASS STRONG |
| Multi-actor / non-account participants | PASS STRONG |
| Subject / Actor / Principal / Authority distinction | PASS STRONG |
| Structured semantic access | PASS |
| Open-world + DANTE-native composition | PASS |
| Scenario / hypothetical state | PASS |
| Basis dependency / temporal validity / coherence | PASS STRUCTURAL |
| WorkContract propagation | PASS STRUCTURAL |
| Work Supersession | PASS STRONG |
| Reference / Target Resolution | PASS v0.5 |
| Policy composition / precedence | PASS v0.5 |
| Consequence governance | PASS v0.5 |
| Compound effects | PASS STRONG |
| Partial / unknown external outcomes | PASS STRONG |
| Approval rebinding | PASS STRUCTURAL |
| Cancellation semantics | PASS |
| Revocation during Run | PASS |
| Direct privacy | PASS |
| Cumulative privacy inference | PASS |
| Safe streaming/publication | PASS STRUCTURAL |
| Publication currentness | PASS STRUCTURAL |
| Attention overload | PASS |
| Self-feedback / oscillation | PASS |
| Untrusted input / prompt injection | PASS |
| Specialist-system boundary | PASS |
| Offline / late-arriving state | PASS STRUCTURAL |
| Large fan-out | PASS SEMANTICALLY / SCALE IMPLEMENTATION OPEN |
| External AI / delegation | PASS STRUCTURAL |
| External-agent side-effect containment | PASS STRUCTURAL |
| Future rich general-purpose chat | PASS |
| Model/provider replacement | PASS STRONG |
| Generated code / computer use isolation | PASS STRUCTURAL AFTER v0.5 P0 |
| Resource exhaustion / mandatory reconciliation | PASS STRUCTURAL |
| Need to reopen Domain | NO |
| Need to reopen Logical | NO |
| Need to reopen Physical | NO |
| Need to reopen PostgreSQL | NO |

---

## 73. Why v0.5 structural closure is not implementation closure

The pressure-test program stopped finding missing semantic/platform fundamentals. The final new P0 was an execution-security boundary around arbitrary/untrusted execution, and targeted verification found no further fundamental responsibility gap.

That is sufficient evidence to mark:

```text
AI-02.1 v0.5
CLOSED / STRUCTURALLY ACCEPTED
```

It is **not** evidence that:

```text
backend implementation exists
sandbox isolation is proven
provider integration is proven
security penetration testing passed
load/performance passed
AI-03 Context/Retrieval/Memory design is complete
production runtime is ready
```

Those claims require later real artifacts and direct tests.

---

## 74. AI-02.1 closure and downstream handoff

The mega-test program and targeted structural verification are complete.

```text
NO MORE AI-02 MEGA TESTS
```

The user explicitly accepted the v0.5 structural baseline and chose to proceed to AI-03. There is no remaining AI-02 structural work.

Downstream rule:

```text
AI-02.1 accepted baseline
→ AI-03 Context / Retrieval / Memory
→ reopen only the smallest AI-02 boundary if later evidence exposes a genuine contradiction
```

Implementation/detail questions are downstream requirements rather than reasons to restart broad reengineering.

Current continuation sources:

```text
docs/architecture/dante-ai-03-context-retrieval-memory.md
docs/workstreams/ai-architecture.md
docs/workstreams/ai-architecture-live-handoff.md   TEMPORARY / MUST NOT MERGE TO main
```

---

## 75. Current phase verdict

The central thesis survives every completed stress round:

> **DANTE is a domain-centered intelligence platform around replaceable cognition, not a model-centric application.**

Current status:

```text
AI-02.1
CLOSED / STRUCTURALLY ACCEPTED
v0.5
ROUND I COMPLETE
ROUND II COMPLETE
FINAL KILL-TEST COMPLETE
LAST MEGA STRESS-TEST COMPLETE
TARGETED v0.5 CONSISTENCY VERIFICATION COMPLETE
NO MORE AI-02 MEGA TESTS
FUTURE-EXTENSIBILITY STRUCTURAL CRITERION PASS

DOMAIN / LOGICAL / PHYSICAL / POSTGRESQL REOPEN
NOT JUSTIFIED BY CURRENT EVIDENCE

AI-03
ACTIVE
CONTEXT / RETRIEVAL / MEMORY
CURRENT MACRO-PHASE AI-03A FULL CONTEXT ARCHITECTURE
```

No runtime, provider, backend implementation or database PASS is claimed by this document.
