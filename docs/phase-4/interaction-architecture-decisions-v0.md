# LifeOS — Phase 4 Interaction Architecture Decisions v0

> Incremental decision log for the Phase 4 Interaction Architecture Contract.
>
> This file complements `docs/phase-4/interaction-architecture-guide-v0.md` and `docs/phase-4/cross-platform-interaction-rule-v0.md` on `prototype/phase-4-today-home`.
>
> During principle-by-principle review, this file is the authoritative acceptance-status log. The longer research guide remains the full rationale/evidence document and will be reconciled after the contract review, avoiding risky full-file rewrites after every single discussion step.

---

## 0. Status

| Field | Value |
|---|---|
| Product | LifeOS — Personal Operating System |
| Phase | 4 — frontend prototyping and UX validation |
| Workstream | Interaction Architecture |
| Status | **IN PROGRESS — incremental accepted-decision log** |
| Date | 2026-08-14 |
| Branch | `prototype/phase-4-today-home` |
| UI mutation authorized | **No** |

This file records only decisions explicitly accepted in discussion. Anything not listed as accepted remains open/draft even if it appears in the research guide.

---

# Cross-platform rule

## CP-01 — One LifeOS, multiple surfaces

**ACCEPTED — 2026-08-14**

LifeOS is one personal system expressed through multiple surfaces, not separate Web and Mobile products that merely synchronize data.

- durable semantics, history, state transitions, scope, provenance, authority and privacy remain coherent across surfaces;
- capabilities belong to LifeOS first, while each surface chooses an appropriate representation;
- architecture is validated mobile-primary but not mobile-only;
- the working hypothesis that routine use may be predominantly mobile (roughly 85%) is not a validated product metric and must not be treated as one;
- Mobile and Web may emphasize different affordances without creating different semantic products.

---

# Accepted Interaction Architecture principles

## IA-01 — The persistent model is richer than the persistent UI

**ACCEPTED — 2026-08-14**

Existing in the model does not grant an entity a permanent surface.

A Person, Asset, Preference, Relationship, Observation, Source or similar internal concept must not automatically create navigation/UI. Knowledge can remain internal, become a contextual reference, become an object of attention, or gain an on-demand view when useful.

---

## IA-02 — Stability belongs to recurring user needs, not entity types

**ACCEPTED — 2026-08-14**

The predictable part of LifeOS should serve recurring interaction needs rather than mirror Domain Model primitives.

Do not derive primary navigation by listing internal entity types.

Which recurring needs deserve persistent top-level access remains an Information Architecture question, not settled by this principle.

---

## IA-03 — One reality, multiple projections

**ACCEPTED — 2026-08-14**

LifeOS maintains one persistent semantic reality that can be exposed through multiple projections and surfaces.

Calendar, history, attention, Actual, trajectory, contextual/on-demand views, natural-language interaction, Web and Mobile must not behave like disconnected copies.

Changes to semantic reality must remain coherent across projections, while each projection may independently choose what to show, omit, emphasize or aggregate.

Presentation/view state must not become a competing source of semantic truth.

Open: how much visual continuity is required between projections remains to be determined later.

---

## IA-04 — Time is primary but not sovereign

**ACCEPTED — 2026-08-14**

Time is a first-class dimension and one of LifeOS's strongest operational projections, but it is not the universal container of the personal model.

- persistent realities may exist without schedules or calendar blocks;
- temporal projections must distinguish what is planned from what exists or actually happened;
- changing a schedule must not automatically change identity, purpose or historical truth;
- Today/Calendar may remain among the strongest operational surfaces without becoming the container of LifeOS.

Open: how deadlines, windows, availability, temporal constraints and other non-block temporal realities should be represented inside temporal projections remains unresolved.

---

## IA-05 — Current situation is broader than the timeline

**ACCEPTED — 2026-08-14**

Current situation is not equivalent to the current calendar timeline.

LifeOS may surface a small set of contextually relevant facts, changes, constraints, risks, mismatches between expected and observed reality, dependencies or unresolved matters when they materially change what the user needs to understand, decide or do in the near term.

### Invariants

- do not force all situational relevance into calendar blocks;
- situational relevance is **consequence-driven, not data-driven**;
- do not turn current situation into a permanent dashboard of every available metric, status or inferred signal;
- the system may use much more context internally than it exposes;
- Mobile may compress situational orientation more aggressively than Web without changing the underlying semantics.

### Does not imply

This does **not** establish a screen, navigation item or product noun called `Situation`, `Now`, `Home` or similar.

Whether current situation becomes one dedicated surface, part of another surface, an adaptive composition, or several coordinated projections remains open for later Information Architecture work.

---

## IA-06 — Natural language is a global interaction layer

**ACCEPTED — 2026-08-14**

Natural language is a global interaction layer over LifeOS's structured reality.

From relevant contexts, users must be able to naturally ask, report, correct, express intentions, negotiate exceptions and request changes without first classifying their input into Domain Model objects or navigating to a technical form.

### Invariants

- natural-language interaction operates on the **same semantic reality** as GUI interaction;
- `global` does not mean that LifeOS must be organized around one permanent Chat page or one infinite transcript;
- the current surface/context may help resolve likely referents and meaning;
- materially consequential ambiguity must not justify silent broad changes: LifeOS should clarify, preview or narrow scope when needed;
- a conversational question does not automatically create persistent state;
- when a conversation changes durable reality, the resulting semantic state/history must become product truth rather than existing only inside the transcript;
- the user does not need to classify input as Goal, Plan, Activity, Preference, Person relationship, Observation or another internal concept before communicating it;
- Mobile and Web share the capability even if their concrete input affordances later differ.

### Does not imply

- every operation must be conversational;
- all AI reasoning must be implemented natively inside LifeOS v0;
- a dedicated conversational workspace is forbidden;
- proactive behavior or notification policy is decided by this principle.

---

## IA-07 — GUI remains a first-class interaction language

**ACCEPTED — 2026-08-14**

GUI remains a first-class interaction language for understanding, inspecting and directly controlling LifeOS.

Frequent, state-oriented or precision-sensitive operations must have usable structured interaction paths and must not depend exclusively on AI prompting.

### Invariants

- the user must be able to understand essential LifeOS state without having to ask an AI what is happening;
- direct manipulation should remain available where it is clearer or faster than conversation, such as precise scheduling, scope selection, state inspection, comparison, undo and correction;
- AI output that changes LifeOS must become inspectable structured state rather than remaining only an opaque conversational claim;
- Mobile must not solve limited screen space by forcing routine control into prompting; core frequent actions still require good touch-oriented GUI paths;
- AI unavailability must not remove the user's ability to understand and control the operational core.

### Does not imply

- every possible natural-language intent needs a dedicated button, form or screen;
- GUI must replicate arbitrary composite reasoning workflows manually;
- conversational/AI interaction is secondary or optional in the wider product experience.

Novel, ambiguous or highly composite reasoning tasks may legitimately be much better served by natural language/AI while still producing controllable LifeOS state.

---

## IA-08 — Natural language and GUI are semantically equivalent where capabilities overlap

**ACCEPTED — 2026-08-14**

When different interaction channels resolve to the same user intent, target and scope, they must converge on the same LifeOS semantic operation and underlying reality.

GUI, native AI and external AI must not create competing meanings or privileged state-transition paths.

### Invariants

- equivalence applies to semantic meaning, not identical interaction steps or presentation;
- once intent, target and scope are resolved, the same operation must follow the same validation, authority, provenance, consequential-confirmation, history and reversibility rules regardless of channel;
- natural-language interaction must not create a parallel `chat state` when the same fact or action has a structured LifeOS meaning;
- native or external AI must not gain privileged direct-write semantics that bypass LifeOS state-transition rules;
- equivalent reads must interrogate the same underlying reality and filters, even when Mobile, Web or conversational presentation differs;
- natural language may require interpretation or clarification before semantic equivalence can be established, while GUI controls may make scope explicit earlier;
- an ambiguous command must not be treated as equivalent to a precise GUI action until the ambiguity that materially affects meaning is resolved.

### Does not imply

Semantic equivalence does **not** require interaction symmetry.

A novel, ambiguous or highly composite natural-language request does not need a one-to-one GUI representation with every possible parameter exposed as controls. AI may interpret a complex request, produce a structured proposal, and then use GUI for inspection, adjustment or confirmation.

Working shorthand:

> **Semantic equivalence where capabilities overlap; not interaction symmetry everywhere.**

---

## IA-09 — Adaptive UI uses a controlled interaction grammar

**ACCEPTED — 2026-08-14**

Adaptive and contextual UI must operate through a controlled interaction grammar.

LifeOS may dynamically select, combine, order, emphasize or suppress approved presentation primitives according to context, while core semantics and interaction meaning remain stable and predictable.

### Invariants

- content may be highly adaptive;
- composition may adapt within an approved grammar of components/patterns;
- core states, scope, authority, confirmation, privacy, reversibility and interaction semantics must not be reinvented by generated/contextual UI;
- adaptation may change relevance, density, ordering, grouping and emphasis, but must not continuously relocate or reinterpret fundamental interaction anchors;
- progressive disclosure is allowed and encouraged, but contextual filtering must not make underlying information irretrievable or uncontrollable;
- users must be able to deepen, expand or inspect beyond the initially surfaced subset when useful;
- operational generated UI should use approved components/patterns rather than arbitrary newly invented controls or semantics;
- purely explanatory/non-operational content may allow substantially more generative freedom;
- Mobile and Web may compose the same grammar at different density and depth;
- when AI is unavailable, standard/predefined compositions must preserve the essential semantic and control paths.

### Does not imply

- every screen has a fixed layout;
- contextual/on-demand views are forbidden from being novel compositions;
- the product may never evolve its component grammar;
- every hidden item must always be shown simultaneously.

Working shorthand:

> **The page may be new; the interaction language must remain learnable.**

---

## IA-10 — Contextual views may be ephemeral

**ACCEPTED — 2026-08-14**

LifeOS may create a focused contextual projection for a temporary question, situation, decision or investigation without creating a permanent application destination.

Ephemerality applies to the presentation, not to durable semantic changes produced through it.

### Invariants

- contextual views operate on the same underlying LifeOS reality rather than detached copies of state;
- a temporary view may disappear while durable corrections, decisions, Plan changes, Schedule changes, Actuals, provenance and history produced through it remain persistent where semantically appropriate;
- contextual views may originate from natural-language requests, search, direct navigation, situational surfacing, LifeOS proposals, drill-down or other interaction paths;
- temporary/contextual presentation must not automatically create new permanent navigation, sections or product nouns;
- an ephemeral surface must still make its current context understandable and preserve clear return/back behavior;
- consequential actions performed through an ephemeral view must remain inspectable and historically traceable after the view disappears;
- Mobile and Web may express the same contextual view at different depth or density without creating different underlying meaning.

### Does not imply

- contextual views are disposable copies of data;
- temporary presentation means semantic changes are temporary;
- recurring views can never become persistent;
- a contextual view must originate from AI or conversation.

### Open question

A recurring contextual view may eventually deserve to become user-saved or more persistent, but the criteria and UX for that promotion remain unresolved.

Keep conceptually distinct:

```text
ephemeral contextual view
→ user-saved view
→ persistent product surface
```

Repeated use alone must not silently promote a temporary view into permanent product structure.

---

# V0 AI delivery / external-reasoning strategy

## V0-AI-01 — External deep reasoning is an allowed extension path

**WORKING V0 DELIVERY DECISION — 2026-08-14**

This is an implementation/product-delivery assumption, **not an Interaction Architecture invariant**.

For v0, LifeOS does not need to natively host every long-form AI discussion, large reasoning workflow or complex plan-generation session.

The preferred external-reasoning model is **scoped retrieval through controlled LifeOS APIs/tools**, not a broad export of the user's personal model.

A practical initial model may be:

1. LifeOS handles lightweight/contextual interaction and structured state where appropriate;
2. deeper discussions, extensive reasoning or large plan/program generation may use an external AI service/tool such as ChatGPT, Claude or another compatible system;
3. when supported, the external AI obtains only the relevant LifeOS context it needs by calling controlled APIs/tools on demand — for example current state, the relevant Plan, constraints, recent Actuals or other scoped information;
4. the external AI may request additional context progressively as the reasoning requires it rather than receiving the entire personal model up front;
5. proposed results return to LifeOS through structured integration when available;
6. pasted text, files or explicit export/import remain valid fallback paths when direct tool/API integration is unavailable;
7. returned results are interpreted into LifeOS's own structured model with provenance and, where consequential, user review/confirmation;
8. future versions may move more reasoning natively inside LifeOS when cost, quality and sustainability justify it;
9. external-AI interoperability should remain possible even if native AI later becomes comprehensive.

### Important boundary

LifeOS remains the authoritative owner of persistent personal state. External AI systems are reasoning/interaction clients over controlled LifeOS context, not alternative sources of canonical personal truth.

A temporary limitation in native AI capability or cost must not define LifeOS's permanent interaction architecture.

Likewise, an external AI transcript/output is not automatically authoritative LifeOS state. Durable changes must be translated into LifeOS semantics with appropriate provenance, scope and confirmation.

### Privacy / context boundary to preserve later

External AI access should be **scoped and purpose-relevant**. The architecture should support controlled retrieval of the information necessary for the current reasoning task rather than silently exposing the complete personal model.

The exact authentication, permissions, tool contracts, context-request UX and provider-specific implementation remain later integration/security decisions.

---

# Contract validation after forward review

After all candidate Interaction Architecture principles have been reviewed from IA-01 through the final principle, do **not** immediately derive Information Architecture.

A mandatory whole-contract validation pass comes first.

## Pass A — Forward coherence review

Read the accepted contract from beginning to end and check:

- whether later principles contradict or weaken earlier ones;
- whether two principles are duplicates that should be merged;
- whether an accepted invariant has acquired an unintended consequence as later principles were added;
- whether important evidence from the corpus is no longer represented;
- whether Web/Mobile, GUI/NL, AI-on/AI-off and single-/multi-actor behavior remain coherent.

## Pass B — Reverse reasoning review

Then reason **from the desired final experience back toward the foundations** rather than only from IA-01 forward.

For representative end states and user outcomes, ask:

```text
What must the user be able to understand / decide / do here?
        ↓
What surface or interaction capability would make that possible?
        ↓
What semantic behavior must exist underneath?
        ↓
Which accepted IA principle guarantees it?
        ↓
Does that principle depend coherently on the earlier foundations?
```

Also read the accepted principles in reverse order and test whether each one still makes sense when treated as a consequence of the principles beneath it.

The reverse pass is specifically intended to detect:

- missing architectural guarantees;
- principles accepted individually that do not compose well as a system;
- assumptions that only work in the forward explanation;
- unnecessary principles;
- circular reasoning;
- desktop-centric or AI-centric leakage;
- gaps between the North Star and the resulting interaction behavior.

## Pass C — Adversarial contradiction pass

Actively try to disprove the contract using the corpus and the agreed stress cases rather than trying to make every case fit.

If a case requires a special-screen exception merely to save the architecture, reopen the relevant principle instead of hiding the failure in later UI design.

## Gate

Only after Forward + Reverse + Adversarial review is coherent enough should the workstream proceed to full interaction traces and then derive Information Architecture.

---

# Review position

Accepted through: **IA-10**.

Next principle for discussion: **IA-11 — Unresolved state is not attention policy**.

Final whole-contract validation is already required after the last principle: forward review → reverse reasoning → adversarial contradiction pass.

No frontend/prototype mutation is authorized by these decisions.
