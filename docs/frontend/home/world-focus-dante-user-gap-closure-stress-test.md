# DANTE — World Focus DANTE ↔ User Gap-Closure Stress Test

**Status:** WR2 COMPLETE — G1..G7 CLOSED / NO NEW STRUCTURAL GAP FOUND  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`  
**Parent:** `world-focus-dante-user-reverse-engineering-stress-test.md`  
**Purpose:** attempt to close WR1 gaps G1..G7, rerun adversarial simulations and determine whether the World product model is stable enough to save as the current pre-backend product contract.

---

# 0. Starting point

WR1 found seven material gaps while preserving the closed Domain/Logical/Physical and existing Intelligence/effect architecture.

```text
G1 World relevance definition under-specified
G2 visible projection / DANTE context basis coherence
G3 cross-World escalation
G4 DANTE presence/proactivity
G5 deictic interaction cursor
G6 cross-surface attention routing
G7 first-open value must not depend on LLM generation
```

WR2 is successful only if all seven can be closed without introducing:

```text
new canonical World ontology
generic relationship/membership model
whole-life prompt dump
AI-only World usability
World as ACL/security boundary
parallel intelligence runtime
page-per-World branching
```

---

# 1. Four-layer World context model

The strongest closure is to separate four things that are easy to accidentally collapse.

```text
1. WORLD IDENTITY / PURPOSE
2. STABLE WORLD RELEVANCE DEFINITION
3. CURRENT WORLD SESSION / INTERACTION CURSOR
4. AUTHORIZED PURPOSE-SCOPED DANTE CONTEXT
```

They are not interchangeable.

---

# 2. Layer 1 — World identity / purpose

User-facing meaning:

> Which continuity context am I entering?

Conceptually includes only product/presentation identity such as:

```text
world reference
user-recognizable name
optional concise purpose/description
presentation/theme profile
presentation lifecycle/config origin where needed
```

Examples:

```text
Music
Japan Trip 2027
My Car
English
Family
```

The name alone is never semantic proof.

`Orto 2027` is not automatically agriculture semantics merely because the text resembles a category.

---

# 3. Layer 2 — Stable World relevance definition

This closes G1.

The product needs a stable way to answer:

> **What kinds of DANTE reality are intentionally relevant to this continuity context?**

This is **presentation/application configuration**, not canonical membership.

Conceptual sources of stable relevance may include:

```text
explicit user-linked/selected anchors
approved typed capability/query configurations
system-default context configuration
user-approved DANTE proposals
application-derived stable configuration where product rules allow
```

Critical rules:

```text
World relevance != ownership
World relevance != universal generic edge
World relevance != arbitrary SQL/query
World relevance != authorization
World relevance != “all records whose label contains Music”
```

The exact persistence shape is deferred.

A future implementation may use typed application configuration and references to accepted owners/capabilities; it must not require a new universal Domain owner or generic relation table.

## Sparse/unknown rule

A World with only a name and no justified relevance configuration remains sparse.

DANTE may:

```text
ask/offer to link known context
propose a bounded relevance configuration
accept explicit user capture/import
```

It must not silently infer broad canonical membership from the label.

**G1 verdict: CLOSED.**

---

# 4. Layer 3 — current World session / interaction cursor

This closes G5.

The current frontend session owns only transient interaction context.

Conceptual `WorldInteractionCursor`:

```text
active World reference
interaction generation
current Lens/query scope when applicable
selected projection/module/source reference when applicable
current Insight/Explore reference when applicable
entry/surface context
```

Not included:

```text
raw DOM tree
serialized React state
full visible payloads
secrets
authorization decisions
canonical truth copied into client cursor
```

The cursor makes natural follow-up possible:

```text
“questa”
“perché?”
“continua”
“confronta con prima”
“aprimi la fonte”
```

The client passes references/hints. The authoritative application/Context Builder reconstructs usable context.

A DANTE run binds to its initiating cursor/generation. Navigating to another World does not rebind the existing run to the new World.

**G5 verdict: CLOSED.**

---

# 5. Layer 4 — authorized purpose-scoped DANTE context

This is the only context DANTE may treat as usable for the actual request.

Conceptual flow:

```text
World identity/purpose
+ stable relevance definition
+ current interaction cursor
+ actual user request/purpose
+ Principal / Actor / recipient
+ sensitivity/disclosure/governance
+ freshness/material basis
        ↓
Context Builder / application capabilities
        ↓
authorized minimized context
```

This context may contain canonical, historical, derived, provider and candidate inputs, but their categories remain distinct.

The World never bypasses this layer.

---

# 6. Coherent basis contract — G2 closure

The user must not see one state while DANTE silently reasons from an unrelated stale state without disclosure.

Required semantics:

## 6.1 Visible projection basis

Important visible projections retain as applicable:

```text
projection/request generation
basis/material state reference where needed
as-of/freshness
provider/source freshness where material
```

## 6.2 DANTE interaction basis

A contextual DANTE request references the current World/cursor/projection identity rather than copying raw values into the prompt as truth.

The application may then:

```text
reuse a compatible current projection basis
or
re-read/revalidate the necessary source state
```

## 6.3 Basis changed during answer

If refreshed context materially differs from what the user was looking at, the result should make the changed basis understandable where relevant rather than pretending it answered the old visible state.

Example:

```text
UI shows flight 10:30 as of 09:00
user asks “is this still on time?”
provider refresh returns 11:20
DANTE answer uses refreshed source
-> UI/result must not pretend the 10:30 state was still current
```

Exact DTO fields remain later API work.

**G2 verdict: CLOSED.**

---

# 7. Cross-World expansion contract — G3 closure

A World provides **default relevance bias**, not a reasoning prison.

## Default contextual mode

Inside a World:

```text
start with current World purpose/relevance
minimize unrelated retrieval
```

## Justified expansion

Expand beyond the World only when the user's task or a materially necessary dependency requires it and the context is authorized.

Examples:

```text
Travel affordability -> Finance
Music release feasibility -> Calendar/Work/Capacity
Study plan realism -> Work/Capacity
Vehicle repair decision -> Finance
```

## Explicit broad request

The user may explicitly ask for a whole-life comparison/orchestration. World presence still gives useful local context but does not override the broader request.

## User-facing basis

When cross-World context materially changes the conclusion, the answer should make the important broader basis visible enough to understand why.

Not required:

- expose internal retrieval plumbing;
- list every irrelevant record consulted;
- expose unauthorized context.

Hard rejects:

```text
activeWorldId = ACL
World question = permission to search all life
hidden unrelated sensitive retrieval “just in case”
```

**G3 verdict: CLOSED.**

---

# 8. DANTE presence contract — G4 closure

World Focus is useful without DANTE.

DANTE is integrated at increasing depth only when useful.

## P0 — QUIET

No persistent AI output required.

The World itself provides deterministic application/projected value.

## P1 — INVOKE

The user explicitly asks DANTE from the World or a contextual action.

## P2 — CONTEXTUAL ENTRY / SUGGESTED QUESTION

Small bounded affordance such as:

```text
“What changed?”
“Why is this at risk?”
“Compare these.”
```

Only when useful; not random prompt decoration.

## P3 — INSIGHT

Evidence-backed contextual result with appropriate basis/freshness/uncertainty.

## P4 — PROPOSAL

Specific suggested change/scenario, explicitly distinct from accepted Decision/effect.

## P5 — ACTION / RECEIPT

Governed operation and truthful execution/result state.

These are product presentation depths, not new Domain/autonomy owners.

## Proactivity admission

A proactive DANTE surface should require real material value such as:

```text
meaningful change
risk/blocker
important resumable context
time-sensitive opportunity
provider discrepancy
explicit recurring user need
```

and should remain bounded by product/autonomy/sensitivity policy.

No content is generated merely because an AI slot exists.

**G4 verdict: CLOSED.**

---

# 9. Cross-surface attention altitude — G6 closure

A material issue may appear in more than one product surface without creating duplicate truth.

Example:

```text
Home
“Japan flight changed”

Travel World
exact segment, old/new state, downstream conflicts, options and source
```

Rules:

```text
Home = cross-life compression
World = scoped expansion / explanation / continuation
```

The source/application layer should provide correlatable identity or semantic reference for the same attention matter when necessary.

World-local UI must not create an independent canonical `resolved/dismissed` truth merely to manage presentation.

Possible distinctions:

```text
dismiss this presentation
snooze where semantics permit
resolve underlying matter
acknowledge shared change
```

must remain semantically distinct.

Exact attention APIs/data model remain later vertical work.

**G6 verdict: CLOSED.**

---

# 10. First-open generation contract — G7 closure

Core World opening value is not an LLM completion.

Required path:

```text
bounded authorized application projections
        ↓
question/output classification
        ↓
initial composition resolver
        ↓
user-visible first screen
```

DANTE may then:

```text
explain
summarize
compare
answer
surface an Insight
propose
```

but does not own whether the World has a valid first screen.

A future concise narrative summary may be generated only as an optional derived presentation over bounded source projections, with truthful basis and graceful AI absence.

**G7 verdict: CLOSED.**

---

# 11. Re-stress: user customizes/hides a module

User removes a spending module from Finance.

Wrong inference:

```text
module hidden -> Finance data irrelevant to DANTE
```

Correct:

```text
CompositionConfig = what user wants displayed stably
World relevance = broader stable contextual definition
Context Builder = actual authorized data for current purpose
```

Therefore user personalization never silently edits canonical truth or the entire DANTE context universe.

The four-layer model survives.

---

# 12. Re-stress: unknown named World

User creates:

```text
Orto 2027
```

with no linked material.

Expected:

```text
World identity available
relevance definition sparse/empty
first screen remains sparse
DANTE does not infer agriculture records from name
user may link/capture/import context
DANTE may propose, never silently assert, a relevance configuration
```

PASS.

---

# 13. Re-stress: same reality in several Worlds

Iceland trip is relevant to Travel, Photography and Finance.

Stable relevance definitions may each reference/configure bounded projections around the same canonical reality.

No source duplication.

DANTE inside Photography may expand to Finance for a cost question only through purpose-scoped authorized retrieval.

PASS.

---

# 14. Re-stress: cross-World conflict

Inside Music:

> “Posso anticipare la release al 15?”

Local context suggests yes.

Cross-life state includes a non-movable Work commitment and travel.

If the question is feasibility, DANTE must consider materially relevant broader constraints.

Result may say:

```text
The Music plan itself can move,
but the 15th conflicts with accepted Work/Travel constraints.
```

The World is the starting coordinate, not the reasoning boundary.

PASS.

---

# 15. Re-stress: multi-actor privacy

Shared Family World contains a shared appointment plus another actor's private reason.

The user asks why the other actor changed participation.

Context Builder produces only disclosure-safe shared state.

World relevance does not expand Authority/Visibility.

PASS.

---

# 16. Re-stress: stale provider + visible state

Visible Travel projection and DANTE answer use compatible generation/freshness references.

If provider refresh changes the fact, the answer/result makes the new basis clear and the old visible projection can refresh.

Provider timeout remains unknown/unavailable, not `no change`.

PASS.

---

# 17. Re-stress: AI unavailable

No AI provider.

World still supplies:

```text
orientation
situation where available
continuity/resume
attention/next/change projections
Explore/source
manual actions
```

DANTE entry gracefully unavailable.

PASS.

---

# 18. Re-stress: World switch during DANTE run

Music request starts with cursor generation M12.

User navigates to Finance F13.

Rules:

```text
Music run remains bound to M12/context basis
it cannot stream into Finance as current-context content
Finance session owns F13
technical run lifetime != React component lifetime
```

If Music result is later persisted/available, its origin/context remains Music.

PASS.

---

# 19. Re-stress: consequential effect after navigation

Travel proposal was generated from basis T8.

User returns later and accepts after provider state changed.

Governed operation revalidates target/freshness/governance. Stale preview cannot become permanent authority.

World session does not own effect truth.

PASS.

---

# 20. Re-stress: background/proactive DANTE when World is closed

A relevant external change arrives while Travel World is not open.

World is not a runtime worker or queue.

Correct path:

```text
provider/application ingestion
-> canonical/provider/reconciliation semantics
-> authorized relevance/attention logic
-> Home/global attention if materially cross-life
-> Travel World contextual expansion when opened
```

A background DANTE process may use the same governed context/effect platform but does not require a mounted World session.

PASS.

---

# 21. Re-stress: dormant/completed/archived World

## Dormant

DANTE may answer/history-explore but should not manufacture guilt or activity.

## Completed finite World

First-open composition becomes history/outcome/artifact oriented. No fake next action.

## Archived/unpinned

Removing prominence does not delete relevance/canonical history automatically. Product policy may reduce proactive surfacing unless user asks.

PASS.

---

# 22. Re-stress: user modifies stable composition

User pins, reorders or removes modules.

DANTE:

- respects stable UI ownership;
- does not silently rearrange it;
- may surface bounded adaptive content separately;
- does not infer that hidden source reality is false/nonexistent;
- does not use composition as authorization.

PASS.

---

# 23. Re-stress: DANTE proposes a new World

DANTE observes repeated context around a new long-lived hobby.

Allowed:

```text
“Would you like a World for Astrophotography?”
```

with a proposed bounded relevance/configuration basis.

Not allowed:

```text
auto-create World
move/copy canonical realities
mark observed behavior as confirmed preference
```

PASS.

---

# 24. Result taxonomy for World DANTE surfaces

WR2 freezes the product-level distinction:

```text
FACT / SOURCE-BACKED PROJECTION
- application/canonical/provider-derived presentation
- not “AI content” merely because AI can discuss it

DANTE ANSWER / EXPLANATION
- grounded response

DANTE INSIGHT
- derived interpretation with basis/uncertainty

CANDIDATE / UNRESOLVED
- possible interpretation, not accepted fact

SCENARIO / RECOMMENDATION
- possible direction, not Decision

PROPOSAL
- materially specific candidate change

GOVERNED EFFECT / RECEIPT
- admitted/attempted/committed/provider/reconciliation result axes
```

The UI may use different visual treatments later, but semantic separation is mandatory.

---

# 25. What the World represents to the user

A World should represent:

> **a comprehensible current picture of one continuity context, with enough history and affordances to resume, understand change, inspect evidence and continue.**

It should not represent:

```text
all data in a category
all history at once
AI's opinion of the user
a score of that life area
a static dashboard template
```

---

# 26. What the World represents to DANTE

A World should represent:

> **a user-recognizable contextual coordinate and stable relevance profile that helps DANTE start from the right local context while the authoritative Context Builder still determines the minimized, permitted and fresh context for the actual purpose.**

It is therefore useful to DANTE for:

```text
relevance prior
ambiguity/deictic resolution
continuity across interactions
retrieval starting point
source/detail context
scoped Insight
proposal target framing
returning results to the correct surface
```

It is not useful as:

```text
canonical storage partition
security boundary
unrestricted retrieval namespace
agent memory database
automatic operation scope
```

---

# 27. Shared-coordinate-system thesis

The strongest combined thesis after WR0+WR1+WR2 is:

> **A World is a shared coordinate system between the user and DANTE for one meaningful continuity context — not a shared source of truth.**

The user gets orientation/continuity.

DANTE gets bounded contextual orientation.

Both ultimately rely on the same authoritative DANTE reality and application boundaries.

---

# 28. Remaining open decisions — bounded, not structural gaps

The following remain intentionally deferred:

```text
exact persisted World profile/schema
exact World creation/management UI
exact typed relevance-selector vocabulary
exact first shipped World default compositions
exact ranking weights/thresholds
exact proactive DANTE thresholds/cooldowns
exact visual form of DANTE entry/Insight/Proposal
exact API DTOs/endpoints
exact context-generation token/field names
exact attention correlation implementation
exact custom Lens UI
```

These can be decided in their owning mini-verticals without changing the product thesis.

---

# 29. New-gap scan

WR2 specifically searched for contradictions in:

```text
World creation
World deletion/archive
same reality / multiple Worlds
hidden module vs DANTE relevance
cross-World reasoning
multi-actor privacy
AI unavailable
provider stale
out-of-order AI result
background agent work
consequential effect after navigation
unknown future World
completed/dormant World
```

Result:

```text
NEW DOMAIN GAP                 0
NEW LOGICAL GAP                0
NEW PHYSICAL/DB GAP            0
NEW INTELLIGENCE ARCH GAP      0
NEW WORLD PRODUCT STRUCTURAL   0
WR1 MATERIAL GAPS CLOSED       7 / 7
```

No further mega reverse-engineering iteration is required before saving the current product contract.

---

# 30. WR2 verdict

```text
WR0 World definition                     HOLDS
WR0 Output Grammar                       HOLDS
WR1 dual user/DANTE role                 HOLDS
WR1 G1..G7                               CLOSED
Domain / Logical / Physical              HOLDS
AI Context Builder boundary              HOLDS
Governed operation boundary              HOLDS
World Focus platform architecture         HOLDS WITH PRODUCT HARDENING
Global first-screen temporal Lens         NOT UNIVERSAL
Core World first-open AI dependency       REJECTED
Cross-World DANTE orchestration           REQUIRED WHEN PURPOSE JUSTIFIES
```

The current model is stable enough to save as the pre-backend **World Product Contract**.
