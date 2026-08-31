# DANTE AI Foundation — AI-00 Semantic and Architectural Baseline

- **Status:** CURRENT BRANCH-LOCAL DESIGN BASELINE / NON-IMPLEMENTATION
- **Workstream:** `feature/ai-architecture`
- **Established:** 2026-08-31
- **Baseline:** protected `main` / branch PRE-SCOPE `fe87d3c8a71f0c56d9acf5e8acbcdb274b18f282`
- **Scope:** consolidate the already-accepted Product, Domain, Logical, Physical and PostgreSQL implications that any future DANTE AI architecture must preserve
- **Implementation:** NOT STARTED by this document
- **Provider/model/SDK selection:** OPEN
- **Database evolution:** NONE AUTHORIZED BY THIS DOCUMENT

---

## 1. Purpose

DANTE already contains substantial AI-relevant product and semantic design. This document brings that material into one current architectural baseline so future AI work does not have to reconstruct the same constraints from scattered sources or accidentally reinterpret the closed Domain / Logical / Physical model.

This document answers:

> **What must be true about DANTE AI before we decide its conversational form, model/provider stack, agent runtime, memory implementation, tool architecture or database changes?**

It deliberately does **not** answer yet:

- which model or provider should be used;
- whether OpenAI, Anthropic, another provider, local models or a multi-provider strategy should be selected;
- whether a specific agent SDK/framework should be adopted;
- the final chat/voice/UI interaction model;
- the physical conversation/memory schema;
- the final tool registry;
- the exact autonomy UX;
- which AI-generated intermediate states deserve persistence;
- whether new database structures are required.

Those are downstream decisions and must consume this baseline rather than redefine it for convenience.

---

## 2. Authority and interpretation discipline

This file is a **consolidation and architectural derivation**, not a new Domain ontology.

Statements are interpreted in three classes:

```text
INHERITED
already fixed by current Product / Domain / Logical / Physical / DB authority

DERIVED
architectural consequence that follows from those accepted constraints
but is not itself a new Domain primitive

OPEN
future AI-specific choice that remains intentionally undecided
```

Precedence remains the normal DANTE order:

```text
protected-main executable truth
→ accepted Product / Domain / Logical / Physical / ADR authority
→ current Database System of Record and engineering contracts
→ this branch-local AI consolidation for its bounded scope
→ historical evidence
→ conversation memory
```

If this file ever conflicts with a higher-authority accepted source, the higher authority wins and this file must be reconciled.

Closed semantics are not reopened because an AI provider, ORM, vector store, SDK or agent framework would prefer a simpler shape.

---

## 3. Source corpus consolidated here

### Product / North Star

Primary current product authority:

- `docs/product/product-identity-and-north-star.md`
- `docs/product/scope.md`
- `docs/product/v1-adaptive-intelligence-and-future-social.md`
- applicable current product specifications under `docs/product/`

Key product discovery evidence:

- `docs/product/feature-discovery-simulation-2026-08.md`
- `docs/product/multi-actor-collaboration-discovery-simulation-2026-08.md`

Research/simulation is evidence, not automatic Domain truth. The closed Domain/Logical model remains the semantic authority where discovery findings were later promoted and validated.

### Domain / Logical

Primary semantic sources include:

- `docs/domain/README.md`
- `docs/domain/concepts/possibility.md`
- `docs/domain/concepts/proposal.md`
- `docs/domain/concepts/request.md`
- `docs/domain/concepts/decision.md`
- `docs/domain/concepts/confirmation.md`
- `docs/domain/concepts/acknowledgement.md`
- `docs/domain/concepts/observation.md`
- `docs/domain/concepts/evidence.md`
- `docs/domain/concepts/provenance.md`
- `docs/domain/concepts/reconciliation.md`
- `docs/domain/concepts/criterion-evaluation.md`
- `docs/domain/concepts/actual.md`
- `docs/domain/concepts/authority.md`
- `docs/domain/concepts/visibility.md`
- `docs/logical-model/README.md`
- `docs/logical-model/whole-logical-model-v1.md`

The Logical Model remains CLOSED / 57 of 57 / remote-QA PASS. `WL-H01..WL-H12` remain implementation regression obligations.

### Physical / PostgreSQL

Primary physical and materialized sources:

- `docs/physical-model/README.md`
- `docs/physical-model/pm-02-primary-mapping-overview-v1.md`
- `docs/physical-model/mappings/postgresql-18.4-v1.md` — historical exact mapping design within the selected PostgreSQL 18 major family
- `docs/development/backend-cp6-01-concrete-persistence-coverage.md`
- `docs/development/backend-cp6-01-concrete-persistence-coverage-part-2.md`
- `docs/development/backend-cp6-02-postgresql-persistence-constitution.md`
- `docs/decisions/ADR-010-postgresql-persistence-constitution.md`
- `docs/database/README.md`
- `docs/database/dictionary/README.md`
- current Alembic / SQLAlchemy / PostgreSQL executable truth

Current protected-main database baseline consumed by this document:

```text
PostgreSQL           18.6
Alembic              20260830_09
schema               dante

tables               69
views                  5
routines              15
triggers              76
physical indexes      97
foreign keys           69
CHECK constraints     123

custom enum/domain      0
sequences               0
materialized views      0
RLS policies            0
```

Current recovery/lifecycle evolution is integrated. Remote backup provider remains TBD / not activated and production/cloud recovery is not claimed.

Permanent DB consistency invariant remains:

```text
Database Architecture & Reference
≈ Database Dictionary
≈ SQLAlchemy metadata / mappings
≈ Alembic head
≈ real PostgreSQL schema
```

This AI workstream must not create a parallel source of canonical truth that bypasses that invariant.

---

## 4. Product identity of DANTE AI

### INHERITED — DANTE is not a chatbot or a model

The Product North Star explicitly requires that DANTE may use AI deeply without being equivalent to a chatbot or to a specific AI model.

Durable product value must remain in DANTE's structured representation of life:

- context;
- history;
- relationships;
- Possibilities;
- Goals and Plans;
- Decisions;
- Constraints;
- Actuals / Observations / Outcomes;
- Authority / Visibility;
- provenance;
- integrations and executable capabilities.

Therefore:

```text
DANTE AI != one LLM
DANTE AI != one provider
DANTE AI != chat transcript
DANTE AI != autonomous mutation engine
```

### DERIVED — the model is a replaceable cognitive component

A future model/provider may contribute language understanding, reasoning, extraction, generation, planning support and tool selection, but DANTE owns:

```text
semantic meaning
canonical state
product policy
authority / visibility boundaries
application capabilities
persistence contracts
history and provenance
accepted-effect rules
```

Provider/model replacement must not redefine those concepts.

---

## 5. DANTE cognitive loop

The Product North Star uses the non-mandatory operating concept:

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

This is **not** a required technical pipeline and does not imply eight services or eight agents.

It is, however, a useful semantic map for future AI behavior.

### UNDERSTAND

Potential inputs include authorized current state, history, provenance, Observations, relationships, commitments, constraints and relevant external/provider information.

The AI may form an interpretation, but:

```text
interpretation != canonical truth
```

### DISCOVER

DANTE may surface a problem, opportunity, pattern or candidate future.

A system-discovered candidate may become a noncanonical candidate or, when intentionally retained under the accepted semantic rules, a canonical Possibility.

```text
AI discovery != user preference
AI discovery != user intent
AI discovery != Goal
AI discovery != Decision
```

### ORCHESTRATE

DANTE may compare constraints, capacity, dependencies, resources, schedules, competing possibilities, criteria and scenarios.

Solver/model output is input to reasoning, not accepted effect by itself.

### DECIDE

Decision has existing bounded semantics. The AI may support a Decision by presenting alternatives, Evidence, rationale or scenario effects, but:

```text
AI recommendation != Decision
Decision != Authority
Decision != resulting domain state
```

### PLAN & COORDINATE

DANTE may help construct or revise Goals, Plans, Activities, Events, Routines, Schedules, Responsibility, Participation and resource coordination while preserving their distinct ownership and history.

### ACT

Execution must occur through governed DANTE application capabilities and provider boundaries.

```text
LLM output != database mutation
LLM tool request != accepted effect
```

### OBSERVE

What happened is represented through the appropriate existing semantics such as Actual, Session, Observation, Outcome, Participation and Confirmation where applicable.

Planned time elapsing does not fabricate Actual or completion.

### LEARN & ADAPT

DANTE may derive patterns and propose adaptation, but observed behavior does not silently overwrite declared preference and correlation does not prove causation.

When evidence is insufficient, a correct DANTE behavior is to leave state unchanged, preserve uncertainty or ask for clarification/Confirmation.

---

## 6. Semantic boundaries the AI must preserve

The AI architecture must use the existing semantic language instead of creating a parallel set of generic `AIThing`, `AIAction`, `AIState` or `memory_fact` meanings.

| Semantic family | What it means for AI | What AI must not collapse it into |
|---|---|---|
| Possibility | candidate future retained for consideration | Goal, user preference, Decision, Plan |
| Proposal | materially specific candidate put forward for consideration | effective state, Decision, Agreement |
| Request | bounded ask for action/information/response/change | resulting effect or fulfillment |
| Decision | bounded question resolved to a result | Authority, mutation, Actual |
| Confirmation | contextual attestation toward a specific target/version | truth, AI confidence, Authority |
| Acknowledgement | explicit taking-notice of target/version/change | acceptance, Confirmation, comprehension |
| Observation | measured/perceived/reported/derived fact/assertion | universal fact store, Actual, Outcome |
| Evidence | contextual evaluative use of information | source record itself, truth |
| Provenance | how a material record/version came to exist/change | truth, Authority, rationale |
| Reconciliation | handling of materially competing states/assertions | latest-wins, AI-confidence-wins, universal merge record |
| Criterion/Evaluation | rule + bounded assessment over Evidence | universal progress score, automatic effect |
| Actual | realization of a specific expectation/intention | Observation, Session, generic reality row |
| Authority | legitimate bounded governance capability | Account, Actor, technical AuthZ, AI capability |
| Visibility | bounded information exposure capability | Authority, arbitrary downstream use |

The existing non-collapse rules remain binding, including:

```text
Possibility != Goal != Proposal != Decision != Plan != Activity
Occurrence != Schedule != Session != Actual
Actual != Observation != Outcome
Evidence != Provenance
Version != Reconciliation
Authority != Visibility
Responsibility != Participation
provider state != canonical state
derived projection != canonical truth
```

---

## 7. AI as Actor without fabricated identity or authority

### INHERITED

Existing Provenance/Domain semantics allow an AI/system to materially act as proposer, transformer, importer or corrector where Actor semantics genuinely apply.

That does **not** turn the AI into:

```text
Person
Account
Principal
Authority
```

A future AI action must preserve the actual human/system/provider roles involved. For example:

```text
source document
→ OCR provider
→ AI extraction/model
→ structured candidate
→ user correction
→ accepted canonical record
```

The accepted record must not be represented as though the user directly authored the original extracted value.

Where consequence warrants it, provenance may need model/rule/version identifiers, source material-state references, transformation basis and correcting/confirming Actor context.

---

## 8. Epistemic integrity: knowing, inferring and accepting are different

DANTE must preserve honest uncertainty.

### INHERITED

```text
AI inference != confirmed fact
AI confidence != Confirmation
source identity != truth
Provenance != truth
Authority != objective truth
absence / unknown != explicit negative
```

An AI-generated interpretation can be high-confidence and still remain noncanonical or unresolved.

A future reasoning result may be represented transiently, as a derived projection, as an unresolved/candidate interpretation, as a material Evaluation, as a Proposal, as a Possibility, or through another specific semantic family depending on what it actually means.

No one universal `AI result` persistence root is pre-approved.

### Correct uncertainty is a valid result

DANTE may truthfully conclude:

```text
unknown
insufficient evidence
conflict known / unresolved
needs confirmation
no safe action
no change recommended
```

It must not manufacture a winner merely to appear decisive.

---

## 9. Canonical and noncanonical state layers

The accepted Physical Model already distinguishes:

```text
canonical DANTE state
material historical state
derived / projection state
external / provider state
unresolved / candidate state
runtime / security state
transient computation state
```

### DERIVED AI placement

Most model computation naturally begins outside canonical truth:

```text
transient reasoning
→ derived interpretation / candidate / unresolved state
→ applicable semantic review/governance
→ canonical effect only when the owning domain operation legitimately establishes it
```

This is the central architectural barrier against accidental AI truth laundering.

### Important CP6 precedent

The CP6 persistence coverage explicitly preserves:

```text
AI candidate before acceptance
→ noncanonical

Possibility retained canonically under its actual semantics
→ native Possibility identity may exist
```

Therefore an AI generation does not deserve canonical persistence merely because it exists, and a meaningful retained Possibility does not have to remain trapped in a chat transcript merely because it originated from AI.

---

## 10. Context construction is an authorization/disclosure problem, not only retrieval

The multi-actor simulation establishes a recurring product structure:

```text
shared canonical reality
+
actor-scoped personal overlays
+
selective disclosure
```

One shared fact may have different personal meaning, visibility, responsibility and planning consequences for different actors.

### INHERITED Visibility rules

```text
Visibility(projection) != Visibility(source)
visible endpoint A + visible endpoint B != visible relationship A↔B
can see != can govern
not visible != nonexistent
Visibility != arbitrary data-use permission
```

A private source may produce a safe visible consequence.

Example:

```text
PRIVATE SOURCE
personal event / reason
        ↓ authorized computation
DERIVED PROJECTION
Unavailable 18:30–19:30
        ↓
recipient-visible
```

The AI may be allowed to process private context for a bounded purpose without being allowed to disclose the private source or its provenance to the recipient.

### DERIVED context gate

Future DANTE context construction must distinguish at least conceptually:

```text
may process this information for purpose P
may expose this representation to recipient R
may expose its source/provenance
may use it to evaluate or plan
may propose an effect
may make or request a governed mutation
```

The exact security implementation is OPEN. The semantic distinction is not.

---

## 11. Multi-actor reasoning must not collapse everybody into `user`

The collaboration simulation repeatedly establishes that real coordination may involve:

- a subject different from the account holder;
- an actor different from the subject;
- a recorder different from the observer;
- a responsible party different from the performer;
- a participant without Authority;
- an Authority holder without a DANTE Account;
- a non-DANTE participant;
- a representative acting on behalf of someone else;
- private sources whose consequence can be shared without the source;
- specialist systems of record that DANTE coordinates around rather than replaces.

Therefore future AI prompts, context objects, tools and provenance must not reduce material operations to a single ambiguous `user_id` when those roles differ.

---

## 12. Proposal, Request, Decision and effect form a governance chain — not one tool call

Natural-language commands often contain semantics richer than the text itself.

Example:

```text
"Maybe move English to 18:30"
→ may express a candidate / Possibility / Proposal context

"Move English to 18:30"
→ Request for a bounded change

"I decided to keep it at 17:00"
→ may establish a Decision under the applicable context

Schedule current accepted state
→ remains owned by Schedule

Actual later execution
→ remains separate again
```

The model may help interpret the language, but the application/domain layer owns the effective transition.

### DERIVED tool-effect classification

A useful engineering classification remains:

```text
READ
retrieve/inspect authorized state

PROPOSE
produce a candidate without making it effective

ACT
request a governed application capability that may produce an effect
```

This classification is **not** a replacement ontology for Possibility/Proposal/Request/Decision/etc. It is an implementation-level effect classification for future tool/runtime design.

---

## 13. Authority, technical AuthZ and AI autonomy are separate

### INHERITED

```text
Actor != Authority
Account != Authority
Principal != Authority
technical authorization != Domain Authority
can see != can govern
may propose != may make effective
```

An AI may reason or propose without possessing Authority to enact a shared-domain change.

### INHERITED product autonomy direction

The adaptive-intelligence product work already rejects one universal AI permission level and identifies scoped autonomy such as:

```text
1. suggestions only
2. propose changes + require confirmation
3. automatically apply minor changes inside approved limits
4. manage a defined scope autonomously under explicit constraints
```

### DERIVED autonomy policy dimensions

A future policy may need to vary by:

```text
actor / principal context
target capability
item/type/domain
scope / calendar / program / routine / individual item
material consequence
change magnitude
shared vs private effect
authority basis
visibility/disclosure implications
time window
risk or provider side effect
```

The exact policy model is OPEN.

A global `ai_autonomy=true` flag is not an adequate semantic design.

---

## 14. Consequential mutation must survive stale reasoning

AI reasoning can take long enough for current state to change underneath it.

The accepted PostgreSQL physical contract already addresses stale consequential mutation through expected material state.

Conceptual operation:

```text
1. locate current semantic owner / facet
2. verify current MaterialStateRef == expected MaterialStateRef
3. enforce required invariant coordination / locking
4. establish the new owner-specific material state
5. update current accepted binding atomically
6. write bounded provenance / idempotency metadata where applicable
7. commit
```

Mismatch means:

```text
conflict
→ re-read / re-evaluate / reconcile
```

not:

```text
model reasoned from old state
→ silently overwrite new reality
```

Future AI tools that can make consequential changes must consume normal application mutation contracts and cannot bypass expected-state/concurrency semantics.

---

## 15. Reconciliation and the future Resolution surface

Reconciliation already permits:

- detect competing states without resolving them;
- keep conflict unresolved;
- select under an explicit bounded basis;
- combine compatible facets;
- correct or supersede while preserving history;
- escalate to a human/specialist;
- use a Decision where a bounded resolution itself matters;
- use deterministic authorized policy without fabricating a human Decision.

Rejected universal winner rules include:

```text
latest wins
provider always wins
user always wins
creator always wins
manager always wins
highest AI confidence wins
```

### DERIVED product implication

A future Home `Resolution` surface should not be defined as merely an AI inbox or notification center.

AI may:

```text
detect a conflict
explain competing states
retrieve relevant Evidence / Provenance
propose a resolution
ask for Confirmation or Decision
assist reconciliation
```

but:

```text
AI != Reconciliation result
Resolution UI != AI ontology
```

The final frontend form remains downstream scope.

---

## 16. Memory: DANTE must not create a second truth database

### INHERITED constraint

PostgreSQL remains the sole canonical persistence and material-history authority for DANTE.

Search, embeddings, conversation caches, provider threads, agent sessions, model context, derived summaries and runtime journals cannot become a second canonical reality merely because they are convenient to query.

### DERIVED memory classes to preserve conceptually

Future AI architecture will likely need to distinguish at least:

```text
canonical DANTE state
material history
conversation transcript / communication context
working context for one reasoning run
retrieved source material
derived summary / projection
AI inference / candidate interpretation
user-declared preference
observed behavior pattern
retained canonical Possibility / other real domain object
provider/runtime session state
```

These are not pre-approved database tables.

The memory architecture remains OPEN, but any implementation must preserve:

```text
summary != source
embedding != source truth
conversation statement != automatically canonical domain fact
observed pattern != declared preference
AI memory != Authority
provider thread state != DANTE canonical history
```

---

## 17. Provenance, explanation and historical integrity

DANTE must be able to preserve materially useful lineage without retaining everything forever.

AI-mediated extraction and transformation must not hide its origin.

Where material, future AI provenance may need to answer:

```text
which source/material state was used?
which model/rule/version transformed it?
which Actor/system proposed or changed it?
what was the user's later correction/Confirmation/Decision?
what Authority/policy basis governed the effect?
what expected state was the operation based on?
which result became canonical and which remained provider/runtime state?
```

Decision rationale remains distinct from Provenance.

Historical correction must not rewrite earlier lineage to look as though the corrected value had always been known.

Retention/minimization also remains binding: provenance is not a backdoor archive for deleted sensitive payloads.

---

## 18. Execution architecture implications

No new runtime is selected by this document.

The accepted Physical stack already establishes trigger-based capability boundaries:

```text
normal backend/application transaction
→ ordinary bounded synchronous work

PostgreSQL transactional outbox
→ real Class-A bounded asynchronous requirement

Restate
→ real Class-B durable workflow requirement
```

Restate was selected as a target for workflows that genuinely need durable progress across waits/callbacks/human approval/provider uncertainty. It is not automatically activated for every AI response.

If AI eventually drives a workflow such as:

```text
propose provider action
→ wait for user approval
→ hours later execute
→ provider timeout / unknown result
→ reconcile
```

then durable workflow infrastructure may be justified.

Even there:

```text
Restate journal != Decision
Restate journal != Confirmation
Restate journal != Actual
provider outcome != canonical DANTE truth
```

The owning DANTE semantics remain in PostgreSQL/application boundaries.

---

## 19. Solver, retrieval and deterministic systems are peers in reasoning — not truth shortcuts

DANTE AI is expected to combine more than an LLM.

Potential reasoning inputs/capabilities may include:

- deterministic queries;
- PostgreSQL FTS / `pg_trgm` / `unaccent`;
- pgvector-backed semantic retrieval when a real use case activates it;
- rules / Criteria / constraints;
- OR-Tools CP-SAT for justified planning/optimization capabilities;
- provider APIs;
- specialist tools;
- external AI;
- human input.

But:

```text
retrieval rank != truth
embedding similarity != Evidence weight automatically
solver UNKNOWN != INFEASIBLE
solver output != accepted plan
provider state != canonical state
model confidence != Confirmation
```

The exact reasoning/orchestration runtime remains OPEN.

---

## 20. Findings from the personal feature-discovery simulation

The personal simulation repeatedly produced reusable pressure for:

- low-friction capture;
- planned vs actual separation;
- longitudinal observations/history;
- review queues for ambiguity or incomplete classification;
- scenario comparison before meaningful replanning;
- realistic capacity rather than filling every free minute;
- criteria/evaluation-backed progress rather than fabricated percentages;
- adaptive planning;
- triggers / conditional behavior;
- explainability / reversible changes;
- external information and specialist boundaries;
- user control over what becomes durable.

### AI implication

DANTE AI must be able to help turn unstructured input and fragmented context into structured candidates **without pretending classification is already accepted truth**.

It must also be able to operate when the best result is:

```text
capture now
classify later
ask for review
leave unresolved
propose rather than apply
```

---

## 21. Findings from the multi-actor collaboration simulation

The multi-actor simulation repeatedly produced:

- shared canonical facts + personal overlays;
- participant state distinct from actual participation;
- proposal distinct from confirmation/effective state;
- responsibility distinct from assignment/performance/authority;
- coordination without exposing full calendars;
- selective disclosure;
- external/non-DANTE participants;
- temporary substitution without history rewrite;
- role-specific views;
- shared resources/capacity/prerequisites;
- authoritative external facts distinct from personal planning targets;
- changes that may require acknowledgement;
- conflicting evidence / unresolved state;
- specialist-system boundaries;
- personal autonomy around shared commitments.

### AI implication

DANTE AI cannot assume:

```text
one user
one view
one truth source
one authority
one visibility scope
one globally valid interpretation
```

Context, explanation, proposal and action must be recipient-, purpose-, scope- and authority-aware.

---

## 22. Database / CP6 non-regression contract for AI

AI implementation must consume the current database instead of creating a convenience ontology beside it.

### Reference families remain exactly distinct

```text
NativeRef
ScopedRecordRef
MaterialStateRef
ExternalRef
```

No generic `AIRef` or universal `kind + uuid` identity root is justified by AI needs alone.

### Existing PostgreSQL thesis remains binding

```text
owner-specific canonical tables/families
+ owner-specific material-state/history
+ specific typed relations
+ bounded technical address/control structures only where genuinely required
+ separate provider / projection / runtime concerns
```

Rejected as AI shortcuts:

```text
universal Entity / Thing table
universal Relationship / edge table
universal Fact table
universal AI memory fact table as canonical truth
EAV/property bag for required semantics
JSONB required-semantic escape hatch
universal event-log ontology
provider thread as canonical history
vector store as canonical knowledge database
```

### Same-change rule remains binding

If future AI work genuinely requires a structural DB change, that future reviewed change must reconcile as applicable:

```text
Alembic migration
SQLAlchemy metadata/mappings
Database Dictionary
human-readable Database Architecture & Reference
direct database tests
recovery/operational harnesses affected by head/topology
current documentation
```

Applied migrations remain immutable.

This AI-00 document authorizes **none** of those changes.

---

## 23. Recovery / retention implications for AI

The current database includes explicit MaterialState retirement/redaction and anti-resurrection behavior.

Future AI features must not accidentally reintroduce protected information through:

- embeddings;
- conversation summaries;
- provider threads;
- tool caches;
- traces;
- derived search indexes;
- runtime journals;
- reconstructed prompt context.

### DERIVED requirement

Any persisted AI-derived representation that can retain protected semantic payload must eventually participate in an explicit retention/redaction/anti-resurrection design appropriate to its storage and threat boundary.

The exact design is OPEN because no AI persistence is yet selected.

The existing recovery suppression ledger remains technical DR evidence only and must not be repurposed as AI/domain memory.

---

## 24. Security, privacy and inference-leakage obligations

`WL-H11` and `WL-H12` remain especially important for AI:

```text
consequential AuthZ provenance
non-interference / inference leakage
```

AI adds pressure because a response can disclose information indirectly even when the raw row is not returned.

Future design must pressure at least:

- hidden-source leakage through summaries;
- existence leakage through counts/ranking/phrasing;
- relationship leakage;
- provenance leakage;
- cross-person/cross-scope context contamination;
- unauthorized secondary use;
- tool output injection into later reasoning;
- untrusted external content influencing tool/action decisions;
- traces/logs retaining sensitive prompts/tool results.

Exact prompt-injection defenses, data-use policies, trace redaction and provider retention controls are **OPEN AI-security design**. They must be evaluated before production activation rather than assumed solved by an SDK.

---

## 25. Observability, cost and evaluation

No AI quality/runtime claim is made yet.

Future implementation must distinguish at least:

```text
model success != task success
tool call success != canonical effect success
canonical mutation success != provider side-effect success
latency != usefulness
low token cost != good decision
high confidence != semantic correctness
```

Likely future evidence dimensions include:

- response/tool latency;
- token/model cost;
- retrieval quality;
- tool selection correctness;
- authorization/visibility policy correctness;
- structured-output validity;
- stale-state conflict handling;
- hallucinated state/action rate;
- clarification/abstention quality;
- proposal acceptance/rejection patterns;
- canonical effect correctness;
- provider reconciliation outcomes;
- privacy/inference leakage tests;
- regression evals over DANTE scenarios.

Exact metrics, eval framework and tracing stack are OPEN.

---

## 26. AI-00 inherited/derived invariants

The following form the current AI foundation and must be treated as regression constraints unless a higher-authority accepted decision deliberately supersedes them.

1. **DANTE is not a chatbot and not a specific AI model/provider.**
2. **PostgreSQL remains the sole canonical persistence + material-history authority.**
3. **AI/solver/provider output is not an accepted canonical effect.**
4. **AI inference is not a confirmed fact.**
5. **AI confidence is not Confirmation.**
6. **AI-discovered candidate is not automatically user intent, preference, Goal or Decision.**
7. **Possibility, Proposal, Request, Decision, effective state and Actual remain distinct.**
8. **Observation, Evidence, Provenance and Confirmation remain distinct.**
9. **Source identity / Provenance / Authority / truth remain distinct.**
10. **Unknown, insufficient evidence and unresolved conflict are legitimate states.**
11. **No universal latest-wins / provider-wins / user-wins / AI-confidence-wins policy.**
12. **AI/system may act contextually without becoming Person, Account, Principal or Authority.**
13. **Autonomy is scoped and governed, not a global boolean.**
14. **Processing permission, Visibility/disclosure and Authority to mutate are separate questions.**
15. **Projection visibility does not imply source visibility.**
16. **Shared canonical reality may coexist with actor-scoped private overlays.**
17. **Consequential mutation must honor expected-state/material-state conflict semantics.**
18. **Provider/runtime/conversation/vector state must not silently become canonical DANTE truth.**
19. **AI-mediated lineage must not launder source/model/provider/user roles.**
20. **Historical correction must not rewrite past state or provenance.**
21. **DANTE may correctly abstain, defer, ask, propose or leave conflict unresolved.**
22. **Specialist systems can remain bounded sources of record; DANTE need not replace them.**
23. **AI implementation does not justify universal Entity/Relationship/Fact/memory ontologies.**
24. **Retention/redaction/privacy requirements apply to AI-derived persistence too if such persistence is later introduced.**

---

## 27. Explicitly open AI architecture questions

The following are not decided by AI-00:

### Product / interaction

- Is DANTE primarily one persistent conversational presence, several contextual surfaces, command/search plus chat, or a hybrid?
- How do Home AI, Capture and Resolution relate without becoming one overloaded inbox?
- How much should AI act proactively vs only on request?
- How should DANTE expose uncertainty, proposals, rationale, sources and pending actions?
- What should voice, attachments and multimodal interaction mean?

### Model/provider strategy

- OpenAI vs Anthropic vs others vs multi-provider;
- direct APIs vs provider agent SDKs;
- model routing / fallback;
- structured output guarantees;
- multimodal and real-time requirements;
- provider data-retention / regional / privacy posture;
- local models where justified.

### Runtime / agent architecture

- one orchestrator vs specialist agents;
- who owns the tool loop;
- model-directed vs deterministic routing;
- interruption/cancellation;
- durable workflow activation criteria;
- bounded parallelism;
- retry/reconciliation semantics;
- provider-independent internal contracts.

### Context / retrieval

- context assembly contract;
- search/retrieval ranking;
- semantic retrieval activation;
- freshness and MaterialState basis;
- privacy-aware retrieval/projection;
- attachment/document ingestion.

### Conversation / memory

- conversation/thread identity;
- turn/message persistence;
- working memory;
- summaries;
- long-term remembered information;
- what deserves canonical promotion;
- retention/deletion;
- embeddings/index lifecycle;
- portability across model providers.

### Tools / authority

- concrete tool/capability registry;
- effect classes and risk tiers;
- confirmation/autonomy policy;
- authority and technical AuthZ enforcement points;
- idempotency / expected-state envelopes;
- provider side-effect reconciliation.

### Safety / quality

- prompt-injection and untrusted-content boundary;
- output validation;
- trace privacy;
- eval datasets;
- red-team cases;
- latency/cost budgets;
- model/provider failover behavior.

None of these may be closed from provider marketing or framework convenience alone.

---

## 28. Forbidden shortcuts entering later AI design

The following should be treated as immediate design smells unless backed by a new, explicit, validated requirement:

```text
"put everything in a vector DB"
"the LLM decides if the user is authorized"
"model confidence above X means true"
"store every AI thought forever"
"every suggestion becomes a Possibility row"
"every chat statement becomes memory"
"latest value wins"
"provider calendar always wins"
"user always wins"
"one global autonomy level"
"one generic AI action table"
"one generic memory fact table"
"one giant agent with direct DB write access"
"one agent per domain because agent frameworks support handoffs"
"SDK trace contains everything by default"
"if the model saw private data it may explain it"
"if a tool succeeded the canonical effect succeeded"
```

DANTE should prefer the smallest truthful architecture that preserves the accepted semantics.

---

## 29. Working architectural hypothesis — not yet a frozen implementation

The evidence currently supports the following conceptual shape:

```text
                DANTE CANONICAL WORLD
                     PostgreSQL
                         │
                  authorized access
                         ▼
                 CONTEXT CONSTRUCTION
     identity / purpose / Visibility / material basis
      current state / history / provenance / sources
                         │
                         ▼
                 DANTE REASONING
          model(s) + deterministic capabilities
       retrieval + rules + solvers + provider tools
                         │
          ┌──────────────┼───────────────┐
          ▼              ▼               ▼
       answer       interpretation    discovery
                     evaluation      candidate
                         │
                         ▼
                NONCANONICAL SPACE
          transient / derived / unresolved
                         │
               proposal / request path
                         │
                         ▼
                 GOVERNANCE GATE
       Authority / policy / Visibility / AuthZ
      Confirmation / Decision where semantically real
           expected MaterialState / idempotency
                         │
                    permitted?
                  ┌──────┴──────┐
                  │             │
                 no            yes
                  │             │
           preserve/defer      ▼
                         application capability
                               │
                               ▼
                        CANONICAL EFFECT
                           PostgreSQL
                               │
                               ▼
                Actual / Observation / Outcome /
                  provider result / reconciliation
                               │
                               ▼
                         LEARN & ADAPT
                               ↺
```

This is a **conceptual guardrail**, not a service diagram and not a commitment to a particular agent framework.

---

## 30. Next workstream step

The next recommended phase is **AI-01 — DANTE Interaction / Product Form Research**.

Its purpose is not implementation. It should determine how users should actually experience this intelligence before we choose runtime/provider architecture.

AI-01 should compare high-quality current AI interaction patterns, including as relevant:

- ChatGPT;
- Claude;
- other materially relevant conversational/agent products;
- command/search assistants;
- proactive assistants;
- multimodal/voice interaction;
- tool/action confirmation UX;
- source/rationale exposure;
- persistent context and memory UX;
- background/durable task interaction;
- interruption/correction/retry behavior.

The benchmark must distinguish:

```text
pattern worth learning from
!= product requirement
!= semantic authority
!= architecture decision
```

The goal is to determine the **form of DANTE** that best expresses the already-defined DANTE semantics, not to clone another chatbot.

Only after that product-form work should the workstream move into provider/model/runtime/tool/memory technology selection and implementation blueprints.

---

## 31. Closure state of AI-00

AI-00 establishes a consolidated foundation only.

```text
Product role                           BASELINED
Domain/Logical semantic constraints    CONSOLIDATED
Physical/DB constraints                CONSOLIDATED
AI canonicality boundary               BASELINED
Authority/Visibility boundary          BASELINED
AI provenance boundary                 BASELINED
Scoped autonomy direction              INHERITED
Stale-state mutation boundary          INHERITED
Provider/model selection               OPEN
Conversation/memory physical model     OPEN
Tool/runtime implementation            OPEN
Frontend interaction form              NEXT / AI-01
Database evolution                     NOT AUTHORIZED
Backend implementation                 NOT STARTED
```

The workstream must preserve this distinction between **architecture understanding** and **implementation proof** throughout later phases.
