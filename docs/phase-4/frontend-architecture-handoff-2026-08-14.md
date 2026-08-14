# LifeOS — Frontend Architecture Handoff — 2026-08-14

**Status:** operational handoff / continuity checkpoint  
**Branch:** `prototype/phase-4-today-home`  
**Authority:** this document does **not** create or override canonical product/domain/interaction decisions. It records the current frontend-architecture exploration state, rejected experiments, methodological corrections, and the exact continuation rules so a new chat/agent does not reconstruct the work incorrectly.

---

## 1. Why this handoff exists

The frontend architecture exploration reached a point where several strong product/interaction principles had been established, multiple architecture families had been compared, and cross-domain patterns had been mined. During the latest continuation, however, several **reactive frontend mockups** incorrectly converted analytical capabilities into UI containers/pages and then over-corrected in the opposite direction.

The user explicitly requested that this state be saved so the next conversation does **not**:

- repeat the same exploration from scratch;
- treat recent failed mockups as accepted architecture;
- invent new absolute rules that were never approved;
- confuse a domain/product capability with a mandatory or forbidden page;
- react to the latest objection by flipping the architecture;
- spend many messages on theory without showing concrete frontend when visual validation is needed.

This handoff is therefore the practical continuation checkpoint.

---

# 2. Mandatory source hierarchy before continuing

Before changing architecture or prototype, re-read the current sources rather than relying on chat memory alone.

Primary frontend/product sources on `prototype/phase-4-today-home`:

1. `docs/phase-4/interaction-architecture-decisions-v0.md`
2. `docs/phase-4/interaction-architecture-guide-v0.md`
3. `docs/phase-4/frontend-architecture-requirements-v0.md`
4. `docs/phase-4/cross-platform-interaction-rule-v0.md`
5. `docs/product/product-identity-and-north-star.md`
6. current Domain & Product Language Map on `feature/domain-model`
7. `docs/phase-4/home-shell-v11.md`
8. `docs/phase-4/frontend-master.md`
9. `docs/phase-4/today-v21.md`
10. `docs/phase-4/home-today-integrated-v1.md`
11. the exact restorable prototype archives and regression tests referenced by those docs.

Important distinction:

- **Home Shell v11 / Today v21 / Home-Today Integrated v1 are real existing frontend assets and accepted implementation checkpoints.**
- They are **not automatically the final LifeOS information architecture**.
- They must be used as concrete assets/evidence, not as a source from which the final architecture is blindly derived.

---

# 3. Current product/interaction contract that remains valid

The following principles remain the basis of the frontend exploration unless explicitly reopened through the normal decision process.

## 3.1 UI does not mirror the domain model automatically

A domain concept does not require a dedicated visible UI object or page. Conversely, a useful UI noun/view/page does not automatically justify a new domain primitive.

This means:

```text
Goal exists
!=
there must be a Goals tab

Asset exists
!=
there must be an Assets tab
```

But it also means the opposite is **not prohibited**. If a dedicated Goals or Assets surface is demonstrably the best frontend solution for a real recurring need, it may exist.

Correct rule:

> **No automatic 1:1 mapping. No automatic prohibition either.**

## 3.2 One LifeOS reality, multiple projections

The same underlying reality may be projected differently for current situation, time, planning, inspection, comparison, history, deep reasoning, etc. A projection is not a duplicate truth store.

## 3.3 Time is foundational but not sovereign

Time is a strong and likely highly visible projection, but LifeOS cannot reduce all meaningful reality to calendar placement.

## 3.4 Current situation is broader than timeline

Opening LifeOS without a specific question must be able to orient the user to materially relevant current reality, not merely show the next calendar block.

## 3.5 AI/NL is a transversal interaction layer

AI is not required to be a central Chat page, but a Chat page/workspace is also **not forbidden**.

The intended capability is broader:

- AI can operate on current context;
- AI can resolve intent while GUI resolves target/scope;
- AI can generate/open structured UI when text is insufficient;
- GUI can continue/edit/confirm/correct AI-started work;
- AI can continue/reason over GUI-started work;
- consequential changes remain inspectable, scoped, authorized, historical and reversible.

Correct rule:

> **AI must not be reduced to “a chatbot bolted onto the app”; this does not imply that conversational surfaces are forbidden.**

## 3.6 GUI remains first-class

Frequent, stateful, precision-sensitive and important operations must remain usable and understandable without requiring AI. AI-off core operation must remain credible.

## 3.7 Adaptive UI must use a controlled grammar

Adaptation may change content/composition, not create an unlearnable interaction language. Stable semantics, authority, scope, confirmation, privacy and reversibility still apply.

## 3.8 Recoverability matters even when attention is suppressed

Something not surfaced now must not become effectively lost. Search/AI recall cannot be the only durable recovery mechanism when a structured non-AI route is warranted.

## 3.9 Mobile-first stress test, not mobile-only design

The interaction contract belongs to LifeOS, then is represented appropriately on mobile and web. Web may exploit depth/space; mobile should not become a crippled capture-only companion.

---

# 4. Architecture exploration already completed

Do **not** restart this from zero.

Five analytical architecture candidates/families were developed and stress-tested.

## A — Stable Spine + Contextual Intelligence

Core idea: a small predictable backbone for recurring needs, with contextual/adaptive intelligence handling long-tail and complex work.

Important result from evaluation: A satisfied the accepted interaction contract with the least structural deformation among the macro-shell candidates.

Risk: if badly implemented, it becomes a conventional multi-module app/dashboard.

## B — Unified Adaptive Workspace

Core idea: a highly adaptive workspace inside a very small stable shell.

Strengths: focus, disruption handling, mobile, deep contextual work.

Risk identified: to satisfy predictability, AI-off operation, stable recovery and recurring access, B needs enough stable anchors/fallback compositions that it tends to converge toward A-like structure.

## C — Dual Interaction Model

Core idea: GUI/direct manipulation and AI/NL/intent are two first-class interaction languages over the same reality and operations.

Major conclusion: **C is not a complete macro information architecture by itself.** It is a cross-cutting interaction-language model.

This remains a strong candidate property for any final architecture.

## D — Universal Reality Access / Context Stack

Derived from command palettes, global retrieval, selection-context, peek/inspect and action patterns.

Core capabilities:

```text
Find / Ask / Command / Capture
        ↓
      Target
        ↓
   Peek / Actions
        ↓
Contextual surface
```

Major conclusion: D is a powerful **global access model**, especially for long-tail retrieval/action/recoverability, but is weak as the sole orientation/navigation architecture.

## E — Context Workspaces / Scenes

Derived from task-oriented workspaces, contextual inspectors, multiple projections and composed deep-work environments.

Major conclusion: E is excellent for **deep contextual work**, comparison, planning, reasoning and structured AI output, especially on web, but should not automatically become the entire everyday shell.

---

# 5. Critical structural realization from the A/B/C/D/E comparison

A/B/C/D/E are **not all alternatives at the same architectural level**.

Current useful classification:

```text
MACRO SHELL
A vs B

INTERACTION LANGUAGE
C

GLOBAL ACCESS / RECOVERY MODEL
D

DEEP CONTEXTUAL WORK MODEL
E
```

This classification remains valuable.

A preliminary synthesis was considered:

```text
small stable structure
        +
selective adaptive behavior
        +
GUI ↔ AI equivalence
        +
universal retrieval/action
        +
contextual deep workspaces
```

However, **the exact shell/navigation resulting from that synthesis is NOT approved**.

---

# 6. What went wrong in the latest continuation

This section is crucial. The following must not be inherited as decisions.

## 6.1 Incorrect jump: capability → stable page/anchor

The exploration identified recurring needs such as:

- orientation/current situation;
- time;
- continuity/resume;
- retrieval;
- capture;
- reasoning/adaptation.

A subsequent derivation incorrectly moved too quickly toward:

```text
Orientation
Time
Continuity
+ Global Access
```

as a presumed `3 + 1` stable structure.

That was **not sufficiently demonstrated**.

The resulting frontend experiment made `Continuity` behave like a catalog/container of ongoing life things. This recreated many of the problems previously associated with `World`/Projects-like universal containers.

Therefore:

> **Continuity is still a real user need/capability family, but whether it deserves a dedicated page, destination, projection, embedded surface, global view, or combination is OPEN.**

## 6.2 Failed mockups

Three standalone HTML experiments were created during the conversation outside the repository.

They must be treated as **DISCARDED EXPERIMENTS, NOT ARCHITECTURAL REFERENCES**.

### Failed experiment v1

- Continuity became a grid/list of cards.
- It resembled a project manager.
- Add/capture was not naturally present.

### Failed experiment v2

- Added a dominant `Aggiungi / racconta / chiedi` field.
- Continuity still behaved like a universal container/catalog.
- AI/NL started to feel like a chat/search bar bolted over a management interface.

### Failed experiment v3

- Reactively removed Continuity and reduced the shell toward `Situazione + Tempo + Find + Add`.
- This was the opposite error: a reaction to criticism rather than an evidence-based architecture decision.
- It is **not approved** and must not be continued as if it were the new direction.

No repository prototype or canonical document was modified by these mockups.

## 6.3 The methodological failure

The assistant repeatedly did this:

```text
user raises a valid objection
        ↓
assistant immediately flips direction
```

Example:

```text
"Continuity looks like World"
        ↓
incorrect reaction:
"then Continuity should not be a stable destination"
```

Correct behavior must instead be:

```text
objection
   ↓
check against requirements + accepted decisions + scenario tests + candidate architectures
   ↓
FAIL / COST / RISK / UNKNOWN / still PASS
```

The architecture changes only if the evidence warrants it.

---

# 7. Objectivity protocol — mandatory from now on

Every material frontend conclusion must be labelled mentally or explicitly as one of these four states.

## DECIDED / DOCUMENTED

Actually accepted or explicitly documented in authoritative project sources.

## EVIDENCE

Observed in an existing prototype, regression test, user scenario, benchmark, or validated interaction.

## DEDUCTION

A reasoned conclusion derived from evidence. It may be strong, but it is not the same as a decision.

## OPEN HYPOTHESIS

A candidate solution that still needs comparison or prototype validation.

Do **not** silently promote DEDUCTION or HYPOTHESIS into DECIDED.

Do **not** demote a documented decision because a new mockup looks awkward; first verify whether the mockup is simply a bad implementation of the decision.

---

# 8. Important correction about pages, sections and dedicated surfaces

There is **no project rule** saying any of the following are forbidden:

```text
Orientation → page
Time → page
Continuity → page
AI → chat
Assets → section
Goals → page
People → section
```

There is also no rule saying they are required.

The actual principle is:

> **A page/section/surface must exist because it improves a demonstrated user need enough to justify a stable place in the product — not merely because the underlying concept exists in the model.**

Therefore all of the following remain possible if evidence supports them:

- dedicated Home/orientation page;
- dedicated Calendar/Time workspace;
- dedicated continuity/resume surface;
- dedicated Assets/People/Documents/Goals surface;
- full-screen AI conversation;
- contextual AI only;
- both conversational and direct GUI forms;
- integrated surfaces;
- separate surfaces;
- hybrid navigation.

The decision must come from the total product contract and comparative testing, not ideology such as “fewer pages is always better” or “traditional navigation is always bad.”

---

# 9. `World` status

The term `World` must **not** be reintroduced as a new architectural noun or universal life container during this exploration.

Historical Home Shell v11 includes `Mondi/Worlds`. That is an existing accepted prototype checkpoint and must be preserved as historical/frontend evidence.

But the current architecture exploration has explicitly rejected using `World` as an assumed semantic answer to “what are the things in a person’s life?”.

Do not rename the same container to `Continuity`, `Context`, `Life`, `Area`, or another word and pretend the problem is solved.

If a universal container is proposed again, it must be independently justified from user needs and domain semantics.

---

# 10. Existing frontend baseline — what is actually real today

## Home Shell v11

`docs/phase-4/home-shell-v11.md` is an accepted visual/interaction checkpoint.

Its documented shell includes historically:

```text
LifeOS | + Crea     Home | Mondi | Oggi     Cerca | Review | Grid | Profilo
```

and a three-zone Home hero:

- greeting + compact conversational assistant;
- central Worlds/Stats spatial stage;
- contextual right rail.

It also freezes interaction details such as carousel behavior, contextual rail, Search, `+ Crea`, compact chat and surface switching.

Important: this is **real accepted frontend work**, but some concepts/nouns inside it may no longer be appropriate as final architecture after the later interaction-architecture study.

## Today v21

`docs/phase-4/today-v21.md` and `docs/phase-4/frontend-master.md` remain authoritative for the mature timeline behavior.

Examples of preserved behavior include:

- 24-hour timeline;
- density mapping;
- overlap lanes;
- stable groups;
- filtering without geometry changes;
- grouped expansion and conditional horizontal scroll;
- drag/move/undo behavior;
- current-time line;
- focus/detail/subtasks;
- semantic zoom;
- anchored time picker;
- manual minute precision;
- progressive multi-day navigation.

Do not casually replace this with a generic calendar mockup.

## Home/Today Integrated v1

This remains a working integrated baseline/reference asset. It must not be treated as the final architecture merely because it exists, but it should be inspected before designing alternatives so valuable interaction work is not accidentally discarded.

---

# 11. Concrete frontend work is REQUIRED during architecture exploration

The user explicitly rejected an architecture process that stays only in prose for dozens of messages.

Therefore:

> **Frontend/HTML prototypes are valid and desirable as architectural test instruments.**

The correction is not “stop making HTML”.

The correction is:

> **Do not make arbitrary HTML that invents an architecture merely to visualize something.**

A valid prototype iteration should state what it is testing and which existing evidence it preserves.

Good pattern:

```text
candidate architecture / unresolved question
        ↓
concrete HTML interaction
        ↓
run real scenarios
        ↓
identify what passes / breaks
        ↓
compare against alternative at similar depth
```

Bad pattern:

```text
abstract discussion
        ↓
random mockup
        ↓
mockup aesthetics accidentally become architecture
```

---

# 12. Original comparative method to preserve

The stronger process before the failed mockups was:

```text
accepted requirements / scenarios
        ↓
multiple genuinely different architecture candidates
        ↓
same stress cases / same constraints
        ↓
PASS / COST / RISK / FAIL / UNKNOWN
        ↓
targeted benchmark only for unresolved questions
        ↓
possible synthesis
        ↓
prototype concretely
        ↓
try to break it
        ↓
select / document
```

Do not prematurely blend alternatives before understanding their trade-offs.

After A/B/C/D/E, synthesis is allowed as a hypothesis, but it must still be minimized and stress-tested rather than treated as a winner.

---

# 13. Cross-domain patterns already mined and still useful

These are transferable mechanics, not architectures to clone:

- universal retrieval → target → valid actions;
- selection establishes context;
- Peek/inspect without losing current context;
- one reality shown through multiple task-dependent projections;
- task-oriented workspace rather than entity-oriented page when appropriate;
- composed context can be recoverable presentation state;
- active/current reality may persist above navigation;
- AI reasoning should resolve toward known LifeOS operations/scope/parameters rather than opaque arbitrary writes.

Sources/pattern families included command palettes, Finder/Quick Look, Linear, Photoshop/Unity inspectors, Ableton/Notion projections, Blender/DaVinci workspaces, Arc/Miro/Salesforce-style context compositions, Live Activities, and Shortcuts-like action composition.

Do not inherit those products’ information architecture wholesale.

---

# 14. Stress scenarios that should continue to be used

Any serious frontend candidate should be exercised against at least these cases:

1. Open LifeOS with no specific question.
2. Gym/activity in five minutes: start / skip / move.
3. Natural-language equivalent of the same operation (`Oggi palestra niente`).
4. Material disruption (`Sto male questa settimana`).
5. Vague desire (`Prima o poi vorrei andare in Giappone`).
6. Resume that vague desire months later.
7. Ask a factual cross-domain question (`Quanto ho speso per la Giulietta?`).
8. Explore the same reality without AI.
9. Ask why LifeOS made/recommends a material adaptation.
10. Private cause / shareable consequence / multi-person case.
11. Many simultaneous continuities (roughly 30 or more).
12. GUI-heavy user.
13. Conversation-heavy user.
14. AI unavailable.
15. Mobile routine use.
16. Web deep analysis.
17. Long-lived account with roughly ten years of data.
18. Simple user who should not pay complexity cost.
19. Extreme/power user who needs deep inspection and recovery.

A candidate that looks good in one hero screen but fails these traces is not enough.

---

# 15. Immediate continuation rule

When this handoff is picked up in a new chat/agent:

1. Re-read the authoritative docs listed above.
2. Restore/inspect the actual Home v11 / Today v21 / integrated frontend artifacts rather than approximating them from prose.
3. Do not treat the discarded v1/v2/v3 mockups as candidates.
4. Resume from the A/B/C/D/E comparative state.
5. Be objective: distinguish DECIDED / EVIDENCE / DEDUCTION / HYPOTHESIS.
6. Do not invent absolute rules about pages, sections, chat, AI, Assets, Time, Continuity, Home, etc.
7. Do not automatically preserve historical `Worlds` just because Home v11 contains it.
8. Do not automatically remove historical frontend work because later architecture principles are broader.
9. Use the real frontend as reusable evidence/assets, then compare what to keep/change.
10. Produce concrete frontend/HTML early enough to validate architecture, but only after stating the hypothesis being tested and what existing capability is preserved.
11. When the user raises an objection, stress-test the current proposal instead of immediately agreeing and reversing it.
12. No repository prototype mutation unless explicitly authorized for that iteration; standalone experiments are acceptable for review.

---

# 16. Suggested next working format

A useful next iteration should not start by naming pages. It should start from **candidate architectures and concrete interaction traces**, then allow pages/surfaces/navigation to emerge where justified.

For each candidate/prototype, record:

```text
HYPOTHESIS
what this frontend structure is testing

PRESERVES
which accepted requirements / existing frontend capabilities remain intact

CHANGES
what the candidate changes relative to existing Home/Today

SCENARIO TRACE
what the user actually clicks/types/sees

PASS / COST / RISK / FAIL / UNKNOWN
result against the same scenario set

DEFORMATION TEST
what had to be added to make the candidate satisfy the contract
```

Then compare alternatives before selecting or hybridizing.

---

# 17. Final warning for continuation

Do not collapse the project into either extreme:

```text
traditional app:
function → dedicated module/page automatically
```

or

```text
anti-page ideology:
everything → one adaptive surface / AI / search
```

Neither is a project principle.

The goal is to derive the frontend that best lets a person understand, shape, act on and recover their real life while preserving the accepted LifeOS semantics and interaction guardrails.

**The architecture is still open. The exploration is advanced, not reset.**
