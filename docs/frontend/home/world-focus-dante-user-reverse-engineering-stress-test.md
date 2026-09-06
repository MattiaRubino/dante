# DANTE — World Focus DANTE ↔ User Reverse Engineering Mega Stress Test

**Status:** WR1 COMPLETE — MATERIAL GAPS FOUND / WR2 REQUIRED BEFORE FREEZE  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`  
**Parents:** `world-focus-product-reverse-engineering-stress-test.md`, `world-focus-product-reverse-engineering-stress-matrix.md`, `world-focus-platform-contract.md`  
**Scope:** determine what a World must represent to the user and to DANTE, how contextual intelligence should consume the World, what the World should produce with and without DANTE, and whether the existing product/platform contracts are sufficient before implementation resumes.

---

# 0. Why WR1 exists

WR0 established a strong product definition:

> A World is a user-recognizable continuity context for a significant part of reality.

and the working compass:

> **Understand this part of my life and continue from here.**

WR1 asks the next question:

> **What must that context mean to DANTE, and how must DANTE appear to the user inside it without turning the World into a chatbot, hidden AI memory, generic container or unsafe scope boundary?**

This is deliberately independent from the current B1 visible temporal Lens implementation.

No new UI implementation is authorized by WR1.

---

# 1. Existing authority consumed

## 1.1 Product identity

DANTE is not a chatbot. It maintains structured context, history and relationships, helps understand and compare, orchestrates across life, distinguishes planned from actual, and may act through governed capabilities while preserving user authority.

## 1.2 Domain / Logical / Physical

The accepted kernel requires:

```text
product/UI terminology != automatic ontology
AI inference != canonical truth
provider state != canonical truth
planned != actual
Observation != Actual
Authority != Visibility
absence != false
```

A World therefore cannot become a semantic owner merely because DANTE needs a convenient context label.

## 1.3 AI / Context / Runtime boundary

The current AI boundary distinguishes:

```text
canonical state
material history
retrieved context
derived context
live external context
candidate/unresolved state
transient LLM working context
```

The Context Builder must be purpose-aware, disclosure-aware and minimized.

Therefore:

```text
World != AI memory
World != prompt dump
World != authorization scope
World != permission to retrieve everything related to a label
```

## 1.4 Governed operation boundary

AI output, tool calls and operation execution are separate.

The World may provide interaction context for an action proposal, but:

```text
World context != Authority
AI proposal != Decision
AI tool call != governed effect
request accepted != effect completed
```

## 1.5 Existing World Focus platform contract

The existing platform already allows World Focus to supply bounded interaction context such as:

```text
active World identity/context reference
current World Lens
selected module/source reference
current exploration reference
entry/surface context
```

and explicitly requires the authoritative Context Engine/application layer to reconstruct and filter usable context.

WR1 tests whether that is product-complete enough.

---

# 2. External reverse engineering — AI close to durable context

Current products show a strong trend toward keeping AI close to an enduring workspace rather than forcing every interaction to start from a blank chat.

## ChatGPT Projects

Projects group long-running chats, files, instructions and memory so the user can return without restating context.

Transferable lesson:

```text
continuity context reduces re-entry cost for both user and AI
```

Reject:

```text
World = collection of chats/files
World memory = DANTE canonical memory
```

DANTE has richer structured truth and governance than a project chat container.

## Linear Project + Agent

Linear keeps project overview, updates, documents and issue context together. Its current Agent can work from the broader workspace context, and recurring agent jobs can run from that context.

Transferable lesson:

```text
AI becomes much more useful when it operates next to structured current work
and can return results into the durable application surface
```

Reject:

```text
agent sees workspace -> agent may act on everything in workspace
```

DANTE must retain its independent disclosure and governed-effect boundaries.

## Notion AI / Agents

Notion places AI directly inside pages, databases and workspace context; outputs can persist as normal workspace material rather than disappearing in one chat thread.

Transferable lesson:

```text
intelligence should be embedded in the place where the underlying reality is understood and continued
```

Reject:

```text
AI-generated workspace content automatically becomes accepted personal truth
```

---

# 3. Dual-role hypothesis

A useful World has two simultaneous roles.

## USER ROLE

For the user:

> **A World is a low-reentry-cost surface for understanding and continuing a meaningful context.**

It should reduce:

```text
where was I?
what matters here?
what changed?
what comes next?
what needs attention?
what evidence is this based on?
what can I do now?
```

## DANTE ROLE

For DANTE:

> **A World is a bounded contextual coordinate that biases relevance and interaction toward one user-recognizable continuity context.**

It may help DANTE know:

```text
which continuity context the user is in
what surface/question the user is currently looking at
what is selected
what scope/lens is active
which source/detail the user means by “this”
which presentation-level context is likely relevant
```

It must not directly decide:

```text
what data is authorized
what canonical facts exist
what other Worlds are inaccessible
what operation may execute
what inference is true
```

**Initial verdict:** the dual-role hypothesis survives.

---

# 4. The critical distinction: World scope vs usable DANTE context

A dangerous design would be:

```text
World = Music
-> retrieve everything tagged Music
-> send it to model
```

This fails privacy, performance, relevance, overlap and semantic ownership.

The required flow is closer to:

```text
WORLD / SURFACE CONTEXT
    ↓  contextual hint only
PURPOSE / USER REQUEST
    ↓
PRINCIPAL + ACTOR + DISCLOSURE
    ↓
CONTEXT BUILDER / APPLICATION CAPABILITIES
    ↓
BOUNDED AUTHORIZED CONTEXT
    ↓
DANTE REASONING
```

A World is therefore a **contextual prior**, not a complete retrieval specification.

---

# 5. Simulation method

Each scenario is replayed in four modes:

```text
A. without DANTE
B. with DANTE answering/explaining
C. with DANTE proactively surfacing something
D. with DANTE proposing/performing a consequential action
```

The test asks:

1. What must the user see without AI?
2. What additional value can DANTE create?
3. What context does DANTE need?
4. What context must DANTE not assume?
5. What must be visible as fact vs inference vs proposal?
6. Does cross-World reasoning become necessary?
7. What breaks if AI/provider/context is unavailable?

---

# 6. Deep simulation A — Music

## Without DANTE

The World should still expose enough to understand and continue:

```text
active creative/release continuity
meaningful resume point
next milestone/release
material change
source/artifact access
```

The user should not need AI to know what is going on.

## With DANTE — user asks

> “Cosa dovrei riprendere?”

DANTE may compare current active work, recent material state, deadlines and user-owned priorities.

Good answer:

```text
recommend one or two grounded candidates
explain why
show source basis
allow direct resume/explore
```

Bad answer:

```text
latest timestamp wins
AI invents “most important” with no basis
AI treats no recent Session as no progress
```

## Proactive DANTE

Potentially useful:

- one release materially at risk;
- meaningful stale creative thread;
- new external performance fact;
- a newly realistic opportunity.

Must not produce generic “insights” merely because the World is open.

## Consequential action

> “Sposta la release di due settimane e ripianifica.”

World context helps identify likely target, but target, current state, authority, affected plans and cross-life conflicts must be reconstructed through governed application semantics.

**Result:** World improves ambiguity resolution and continuity, but is not enough to authorize or execute.

---

# 7. Deep simulation B — Travel disruption

User is inside `Japan Trip`.

## Without DANTE

World should show:

```text
next segment
material provider change
booking/source facts
document/readiness issue
```

## With DANTE

> “Che faccio adesso?”

DANTE needs:

```text
current itinerary state
provider change
accepted bookings
participant context
constraints
possibly finance/calendar/work context
```

A World-only hard boundary fails if the best alternative conflicts with Work or exceeds a real Finance constraint.

DANTE therefore needs permission to **escalate beyond the current World when purpose requires cross-life reasoning**.

The answer should make that broader basis understandable rather than silently importing unrelated life data.

**Material gap found:** current World contracts do not make cross-World escalation explicit enough.

---

# 8. Deep simulation C — Finance

## Without DANTE

Current situation, meaningful changes, reconciliation/freshness and drill-down should remain useful.

## With DANTE

> “Posso permettermi il viaggio senza compromettere il resto?”

This is not a Finance-only or Travel-only question.

DANTE needs scoped orchestration across:

```text
Finance
Travel
other commitments/goals
possibly Work/time constraints
```

A UI concept of `activeWorldId=finance` must not trap reasoning.

At the same time, DANTE must not use unrelated sensitive context merely because global data exists.

**Required rule:** World provides default relevance, user purpose determines whether authorized scope expands.

---

# 9. Deep simulation D — Study

User asks:

> “Sono davvero in ritardo?”

DANTE must distinguish:

```text
planned Sessions
actual Sessions
assessment Outcomes/Observations
Goal method
current deadline
```

A generated statement like “sei al 68%” is invalid if no accepted progress method supports it.

World value:

- supplies learning continuity and currently visible trajectory/question;
- makes deictic follow-up possible: “perché?”, “mostrami i test”, “e se rimando l'esame?”.

**Gap found:** session contract mentions selection but does not yet explicitly define a stable interaction-context/cursor contract for deictic AI follow-ups.

---

# 10. Deep simulation E — Relationship / qualitative

User opens a relationship-centered World.

## Without DANTE

Potential value:

```text
shared commitments
important context/history
next meaningful event
promises/follow-up
```

## With DANTE

> “C'è qualcosa che sto trascurando?”

DANTE may identify grounded unresolved commitments or repeated postponement, but must not infer relationship quality from message counts or frequency.

Proactive behavior should be very conservative.

**Result:** DANTE visibility/proactivity must be sensitivity and consequence-aware, not one universal “AI insight region”.

---

# 11. Deep simulation F — Vehicle

User asks:

> “È il momento di fare il tagliando?”

Possible basis:

```text
accepted maintenance plan
mileage Observation/source
last service history
calendar deadline
manufacturer/professional source if present
```

DANTE can explain basis and options.

If user asks to book service, provider interaction becomes a governed effect and may require external action/reconciliation.

World helps target the car and local context but does not replace target resolution or provider state.

---

# 12. Deep simulation G — sensitive Body/Wellbeing

User asks:

> “Perché questo dato è peggiorato?”

DANTE must be able to say:

```text
I can show the observed change
I can show relevant correlated history
I cannot establish causation from this evidence
```

The World context cannot authorize disclosure of every sensitive record in that broader life area.

Recipient, purpose and sensitivity remain independent inputs to Context Builder.

**Result:** World is never a security container.

---

# 13. Deep simulation H — shared/multi-actor World

A shared trip/project contains canonical shared facts plus private overlays.

User asks:

> “Perché Luca non può venire?”

Even if DANTE knows Luca's private reason in some authorized context elsewhere, the current recipient may not be allowed to see it.

World membership/shared context is insufficient for disclosure.

Safe answer may expose only:

```text
Luca is unavailable / participation changed
```

if that is the allowed shared fact.

**Result:** user/DANTE World context must consume a disclosure-safe projection, not rely on React hiding.

---

# 14. Deep simulation I — unknown future World

User creates a World named `Orto 2027`.

DANTE cannot assume:

```text
World name -> agriculture ontology
```

It needs explicit bounded product/context definition or known linked application capabilities before it can safely reason about scope.

The current `World Descriptor` contract is mostly display identity/theme/profile.

**Material gap found:** the product needs a clearer **World relevance definition** without turning it into canonical membership or a generic query language.

---

# 15. Deep simulation J — same reality in several Worlds

One Iceland trip appears in:

```text
Travel
Photography
Finance
Family
```

User asks inside Photography:

> “Quanto mi costa questa uscita?”

The selected trip can be used as a contextual anchor, but cost source remains Finance/application semantics.

DANTE should not duplicate the trip or infer that Finance projection belongs canonically to Photography.

This reinforces:

```text
World relevance != ownership
World context may compose references to realities owned elsewhere
```

---

# 16. Deep simulation K — AI unavailable

World opens while AI provider is unavailable.

Expected:

```text
orientation works
continuity works
next/attention based on deterministic application projections works
Explore works
manual actions work
DANTE-only surfaces degrade locally
```

If the World becomes blank without LLM output, the design fails.

**Result:** the primary first-open situational picture must be application/projection-driven, not generated by an LLM on every open.

---

# 17. Deep simulation L — stale provider

World UI shows accepted itinerary plus stale airline update.

DANTE receives a user question.

The answer must not silently treat provider stale data as current canonical truth.

UI and DANTE need compatible basis/freshness information.

**Material gap found:** the contract needs stronger **coherent basis / context snapshot semantics** between visible projection and contextual DANTE interaction.

---

# 18. Deep simulation M — World switch during streaming

User asks in Music:

> “Cosa devo riprendere?”

then immediately switches to Finance.

The Music run may continue technically, but it must not stream its result into Finance or acquire Finance interaction context merely because the same UI shell exists.

The run retains its original context basis; the new page session has a different interaction generation.

B0/B1 request-generation foundation helps, but the DANTE interaction contract must explicitly bind a run/result to the initiating context snapshot.

---

# 19. Deep simulation N — consequential action after navigation

User asks inside Travel:

> “Prenota l'alternativa.”

A preview is shown. User navigates away. Provider price/state changes.

Later confirmation must not blindly execute the stale preview.

Governed operation contract already requires material target/freshness revalidation.

World UI lifecycle must not own durable effect truth.

**Result:** existing effect architecture holds.

---

# 20. What DANTE should represent to the user inside a World

DANTE should not appear as one undifferentiated AI blob.

The user must be able to distinguish at least these product-result classes:

## A — grounded answer/explanation

```text
what / why / compare / summarize
```

No mutation implied.

## B — derived insight / observation

A DANTE/application interpretation over evidence.

Must retain basis, uncertainty and provenance where material.

## C — candidate / unresolved interpretation

Something DANTE thinks may be true or relevant but is not accepted fact.

## D — scenario / recommendation

A possible direction or comparison, still not a Decision.

## E — proposal

A materially specific suggested change the user can inspect/accept/reject.

## F — governed action state / receipt

What was requested, admitted, attempted, committed, externally applied, conflicted or remains uncertain/reconciling.

These may share visual infrastructure later, but must not collapse semantically into `AI response`.

---

# 21. How visible should DANTE be?

One permanent chat box is not required for every World.

A useful presentation ladder is:

```text
QUIET
no AI surface unless user invokes it

CONTEXTUAL
small relevant question/entry point

INSIGHT
bounded evidence-backed result

PROPOSAL
explicit candidate change with consequence/basis

ACTION STATE
truthful operation/result surface
```

These are presentation modes, not new Domain or autonomy enums.

Proactivity should depend on material value and accepted product/autonomy policy.

Hard rejects:

```text
AI commentary on every open
AI fills empty space
random “insights” to appear intelligent
hidden autonomous mutation
mandatory conversation before manual exploration
```

---

# 22. DANTE as deictic/contextual interaction

One of the strongest World benefits is that the user should be able to say:

```text
“questa”
“perché?”
“confrontalo con prima”
“continua da qui”
“aprimi la fonte”
“spostalo”
“e se invece faccio X?”
```

without restating the World, selected item and current surface every turn.

This requires a bounded **interaction context cursor** conceptually including:

```text
active World context reference
current selected projection/source reference
current Explore/Insight reference where applicable
current Lens/query scope where applicable
entry/surface context
interaction generation
```

The client supplies references/hints. The authoritative application/Context Builder reconstructs what may actually be used.

---

# 23. Cross-World orchestration rule

DANTE's identity depends on connecting life, so a World must not create an AI silo.

Default behavior:

```text
inside a World
-> strongly bias retrieval/reasoning toward that continuity context
```

But when the user's purpose materially requires broader reasoning:

```text
World context
+ explicit/current question
-> Context Builder may expand to other authorized relevant realities
```

Examples:

```text
Travel -> Finance for affordability
Music -> Calendar/Work for release feasibility
Study -> Work/Capacity for exam plan
Vehicle -> Finance for repair trade-off
```

The user-facing result should disclose the meaningful broader basis where doing so improves comprehension/trust.

Hard reject:

```text
activeWorldId = hard retrieval ACL
```

and also:

```text
World question = permission to search whole life
```

---

# 24. Home ↔ World ↔ DANTE attention routing

The same material issue may be relevant globally and locally.

Example:

```text
Home: “Release at risk”
Music World: exact blocker, basis, affected artifact and options
```

This is different information altitude, not duplicate truth.

DANTE proactivity should route:

```text
cross-life significance -> Home / global attention
scoped explanation/action -> World
```

The same underlying attention identity should be correlate-able so dismissal/resolution does not create contradictory duplicates.

**Gap found:** this cross-surface attention identity/routing is not yet explicit enough in the World contract.

---

# 25. World opening output vs AI-generated brief

A tempting design is:

```text
open World
-> ask LLM to summarize everything
-> show generated brief
```

**REJECT as primary architecture.**

Reasons:

- AI unavailable would destroy first-screen value;
- latency/cost on every open;
- stale/misaligned basis;
- non-deterministic layout/content;
- disclosure risk;
- false confidence in generated interpretation.

Better:

```text
application produces bounded deterministic question-oriented projections
-> composition selects highest-value answers
-> optional DANTE narrative/Insight may explain/refine on demand
```

A concise opening summary may exist, but its semantic facts/basis must come from governed projections rather than an unconstrained prompt over “the whole World”.

---

# 26. Material gaps discovered by WR1

## G1 — World relevance definition is under-specified

Existing `World Descriptor` strongly defines presentation identity but does not yet define enough about **why this World exists / what stable relevance it represents** for DANTE and application projection selection.

Need a bounded product/application relevance contract that does not become:

```text
universal membership list
generic edge table
arbitrary SQL/query expression
canonical ownership
```

## G2 — User-visible projection and DANTE context basis need stronger coherence

When user asks “why this?”, DANTE should reason from a compatible basis with what the user is seeing, or explicitly refresh/explain a changed basis.

Need context-snapshot/generation/freshness semantics.

## G3 — Cross-World escalation is not explicit enough

World should bias, not trap, DANTE.

Need a clear escalation/minimization rule.

## G4 — DANTE presence/proactivity inside World is under-specified

Need separation among quiet entry, Insight, Proposal and action/result surfaces; no universal AI commentary.

## G5 — Interaction/deictic context cursor needs explicit contract

Current session has selection/exploration references but contextual AI follow-up should consume a deliberately bounded cursor with generation ownership.

## G6 — Cross-surface attention routing needs explicit identity/altitude semantics

Home and World may show the same issue at different depth without duplicate or contradictory attention state.

## G7 — Initial first-open answer generation needs an explicit non-LLM rule

The current composition resolver direction supports this, but the product contract should state that core opening value comes from application projections; AI augmentation is optional.

---

# 27. Architecture verdict after WR1

## Domain / Logical / Physical

**HOLDS. No reopen.**

The gaps are product/application/context-contract gaps, not missing Domain owners.

## Intelligence architecture

**HOLDS WITH WORLD-SPECIFIC HARDENINGS.**

Existing Context Builder, result classification and governed operation boundaries are the right owners.

## World Focus platform

**HOLDS, but WR1 gaps must be incorporated before product freeze.**

## B1

```text
implementation           PASS
automated gates          PASS
product acceptance       BLOCKED
visible global Lens      not accepted as universal first-screen control
session/race foundations provisionally retained
```

---

# 28. Required WR2 gap-closure test

Before saving a final World product contract, WR2 must attempt to close G1..G7 and then rerun adversarial cases for:

```text
unknown World
cross-World affordability/conflict
same reality in several Worlds
multi-actor selective disclosure
stale provider
AI unavailable
World switch during stream
consequential action after navigation
empty/dormant/completed World
background/proactive DANTE event
user-created World with vague name
user customizes stable composition
Home attention -> World detail
```

If WR2 opens a new structural gap, another iteration is required.

If WR2 closes G1..G7 without introducing a material contradiction, the result may be saved as the current World Product Contract before B1 is revised and implementation resumes.
