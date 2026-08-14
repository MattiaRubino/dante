# LifeOS — Phase 4 Interaction Architecture Guide v0

> Working research and decision guide for Phase 4 interaction architecture.
>
> This document does **not** define final navigation, Home, information architecture, visual design, or a canonical UI vocabulary. It records the evidence, current synthesis, architectural candidates, draft invariants, open questions, and the process that must be completed before the frontend baseline is changed.

---

## 0. Status

| Field | Value |
|---|---|
| Product | LifeOS — Personal Operating System |
| Phase | 4 — frontend prototyping and UX validation |
| Workstream | Interaction Architecture |
| Document | `interaction-architecture-guide-v0.md` |
| Status | **IN PROGRESS — research synthesis / decision guide** |
| Date | 2026-08-14 |
| Branch | `prototype/phase-4-today-home` |
| Canonical product identity | `docs/product/product-identity-and-north-star.md` on `main` |
| Current frontend baseline | Home + Today Integrated v1 — preserved checkpoint |
| UI mutation allowed by this document | **No** — discussion and validation first |

### Status rule

Nothing in this document becomes an accepted interaction contract merely because it appears here.

Use the following interpretation:

- **Evidence** — supported by the LifeOS corpus and/or external research.
- **Working inference** — current design conclusion derived from the evidence.
- **Open decision** — intentionally unresolved and still to be discussed.
- **Accepted later** — only after explicit review/approval and status update.

---

# 1. Why this document exists

Phase 4 reached a point where continuing to refine the existing Home/Today prototype without first resolving the interaction architecture would risk optimizing the wrong structure.

The current frontend is valuable and must remain restorable, but it is no longer treated as product truth.

The purpose of this guide is therefore to answer a more fundamental question before further visual design:

> **How should a personal operating system let a person understand, interrogate, modify, negotiate and act on a rich model of real life without becoming a task manager, calendar, database UI, static dashboard or generic chatbot?**

The intended sequence from this point is:

```text
research evidence
      ↓
interaction architecture contract
      ↓
interaction traces
      ↓
information architecture
      ↓
navigation / surfaces
      ↓
wireflows
      ↓
stress test
      ↓
visual UX / prototype revision
```

Do **not** reverse this sequence by starting from a Home layout and fitting product semantics into it.

---

# 2. Primary LifeOS evidence used

The interaction-architecture research is grounded first in the existing LifeOS documentation rather than in competitor products.

Primary corpus:

1. `docs/product/feature-discovery-simulation-2026-08.md`
2. `docs/product/multi-actor-collaboration-discovery-simulation-2026-08.md`
3. `docs/product/multi-actor-collaboration-research-2026-08.md`
4. `docs/product/product-identity-and-north-star.md`

The first three documents are treated as a **corpus of scenarios, needs, failure modes and behavioral evidence**.

They are **not** automatically authoritative for current Domain Model terminology. Some terminology and older structural hypotheses predate the accepted Domain Atlas work and must not be silently promoted into current ontology or UI vocabulary.

The North Star is the current product-identity constraint.

### Evidence hierarchy for this workstream

When interpreting this guide:

1. accepted Product Identity / North Star;
2. accepted current Domain Atlas semantics where relevant;
3. this Phase 4 research synthesis;
4. historical Phase 4 prototype decisions;
5. older product hypotheses.

A historical UI noun must never override a later accepted product/domain meaning.

---

# 3. Important working constraints already established

## 3.1 Internal model does not imply visible UI

LifeOS may know much more than it shows.

The existence of an internal concept such as Person, Asset, Preference, Relationship, Observation, Evidence, Provenance or Source does **not** justify a permanent page, card, navigation item or visible hierarchy.

Example:

```text
User: "I own an Alfa Giulietta."
```

LifeOS may store this as durable structured knowledge while showing nothing.

Later:

```text
User: "How much has the car cost me this year?"
```

LifeOS may compose an on-demand view centered on the car, costs, maintenance, insurance, history and related information.

This does **not** imply a permanent navigation hierarchy such as:

```text
Assets → Vehicles → Alfa Giulietta
```

Core rule:

> **The UI exposes what is useful in the current situation, not the ontology that makes the answer possible.**

---

## 3.2 Working exposure distinction

The previous generic word "visible" was too ambiguous. Use the following distinction during UX reasoning:

### Internal knowledge
LifeOS knows/stores something. No UI is implied.

### Contextual reference
An internal entity is used to explain or contextualize another thing that is currently relevant.

Example:

```text
Service due — Alfa Giulietta — September
```

The object of attention is the service deadline, not necessarily the Asset itself.

### Object of attention
The thing the person actually needs to understand, decide or act on now.

### Dedicated on-demand view
An underlying entity becomes the temporary center of a view because the user explicitly needs to inspect it as a whole.

These four cases must not be collapsed into one generic idea of "visibility".

---

## 3.3 Communication is central but is not assumed to be a Chat page

The corpus and subsequent discussion strongly support natural communication as a cross-cutting interaction mechanism.

A user must be able to naturally communicate things such as:

```text
"I didn't go to the gym today."
"I only did half the workout."
"I'm ill this week, lighten things."
"I don't want the planned lunch today; find a lighter alternative."
"One day I'd like to go to Japan."
"I changed my mind."
"Luca is my brother."
"Should I bring an umbrella to Rome tomorrow?"
"Don't ask me every time."
```

These statements can represent very different semantics:

- a fact;
- an Actual;
- partial execution;
- a temporary capacity change;
- a local Plan renegotiation;
- a vague intention;
- a contextual relationship;
- an ephemeral question;
- a policy change.

The person should not need to classify the statement before communicating it.

Working principle:

> **Natural language should be investigated as a global layer for access, interrogation and modification of the same structured reality controlled by the GUI — not as a second disconnected reality owned by an AI chat.**

---

## 3.4 Planned is not Actual

The interaction architecture must preserve at least the following distinctions:

```text
planned
≠ actual
≠ outcome
≠ evidence / confirmation
```

A scheduled item passing in time does not prove that it happened.

Binary completion is insufficient for many cases.

The experience must be able to represent, when relevant:

- completed;
- skipped;
- partially completed;
- unknown;
- deferred;
- disputed;
- externally confirmed;
- contradicted by another source;
- awaiting confirmation.

The UI should expose complexity only when needed, but the architecture must not destroy these distinctions underneath.

---

## 3.5 Plans are negotiable with reality

LifeOS is not expected to treat a Plan as a static instruction sheet.

Example:

```text
Plan: lunch = pasta e fagioli
User: "Today I want something lighter."
```

This does not necessarily mean:

- delete the Plan;
- rewrite the full program;
- abandon the underlying Goal;
- manually edit several forms.

It can mean:

> adapt one execution while preserving the wider plan and its provenance.

The same mechanism must generalize across health, study, travel, work, projects and other contexts.

---

## 3.6 Time is a primary projection, not the container of LifeOS

Today/Calendar remains extremely important.

However:

```text
what exists in LifeOS
≠
what currently occupies a time block
```

Examples:

- a song exists without a mix session today;
- a car exists without a service appointment today;
- a Goal exists before scheduling;
- an idea may have no deadline;
- a relationship exists independently of the latest meeting;
- a vague future desire may intentionally have no operational date.

Working principle:

> **Calendar / Today are temporal-operational projections of LifeOS, not LifeOS itself.**

---

## 3.7 `World` is not part of the current working vocabulary

The historical prototype may contain a `Worlds` label.

For current interaction-architecture work:

- do not use `World` as a conceptual primitive;
- do not redefine it;
- do not replace it with another invented umbrella noun prematurely;
- first understand the recurring UX need, then derive product labels later.

---

# 4. Cross-corpus UX needs that repeatedly emerged

The first synthesis across the single-user, multi-actor and research corpus identified the following recurring needs.

| Recurring need | Frequency / structural importance | Likely exposure pattern |
|---|---:|---|
| Communicate something to LifeOS | Very high | Global |
| Ask a contextual question | Very high | Global |
| Understand the current situation | Very high | Strong orientation surface(s) |
| Understand time / what is planned | Very high | Primary temporal projection |
| Continue something over time | Very high | Stable access, exact form unresolved |
| Handle unresolved matters | Very high | Cross-cutting state + aggregation when useful |
| Adapt when reality changes | Very high | Cross-cutting action |
| Compare intended vs observed reality | Very high | Contextual / review-oriented |
| Receive relevant opportunities or risks | High | Relevance-dependent |
| Inspect a specific context deeply | High | On demand |
| Inspect/correct hidden personal knowledge | Necessary | Secondary control/transparency surface |
| Coordinate shared reality with other actors | Structurally important | Contextual, not necessarily a separate mode |
| Inspect provenance/history | Important | On demand, stronger in consequential contexts |

This is more useful for architecture than mapping navigation directly to Domain Model nouns.

---

# 5. Deep Research study — 2026-08-14

A dedicated Deep Research pass was run after the internal corpus was analyzed.

The research covered:

- mixed-initiative interaction;
- human-AI collaboration;
- proactive assistants;
- attention and interruption management;
- situational awareness;
- prospective memory / open loops;
- personal information management;
- contextual and ambient computing;
- progressive disclosure;
- adaptive/contextual UI;
- generative UI;
- human-in-the-loop automation;
- intention / goal / planning systems;
- natural language vs direct manipulation;
- longitudinal personal systems;
- multi-actor coordination and privacy;
- contemporary product patterns and failure modes.

Relevant external evidence included work and guidance from Microsoft Research / HAX, Apple Human Interface Guidelines, Google Research / A2UI, and current product patterns such as Todoist, Notion, Reclaim, Motion and Sunsama.

The research did **not** treat these products as templates to copy.

The main research conclusion was:

> **LifeOS needs stable semantics and adaptive presentation.**

The strongest recommendation was a hybrid interaction architecture described for research purposes as:

> **Stable Spine + Adaptive Contexts**

This label is a research shorthand, not proposed product naming.

---

# 6. Four architectural paradigms evaluated

The research compared four structurally different interaction architectures.

## A. Situational Command Center

### Core idea
The primary experience answers:

> What is happening and what matters now?

Time, changes, open loops, constraints, risks and upcoming items converge into a stable orientation surface.

### Strengths

- very strong daily orientation;
- strong disruption handling;
- strong planned-vs-actual support;
- resilient without AI;
- easy mental model for "open LifeOS and understand now".

### Structural failure mode

If expanded to cover distant intentions, history, persistent knowledge, discovery, assets, people and many simultaneous initiatives, the current-situation surface can absorb everything and become an infinite dashboard.

---

## B. Conversational Generative Canvas

### Core idea
Natural language is primary and LifeOS generates the most appropriate UI for each request.

### Strengths

- excellent for vague input;
- excellent for exceptions and unanticipated requests;
- very low classification burden;
- strong contextual/on-demand UI potential.

### Structural failure mode

- weak when AI is unavailable;
- weak for GUI-heavy users;
- weak for systematic scanning and persistent state comprehension;
- generated controls may become unpredictable;
- risks turning the user into a permanent reviewer of AI output;
- risks becoming a chatbot with temporary widgets rather than an operating system.

---

## C. Intent & Trajectory First

### Core idea
The primary continuity of the system is what the person wants, must, or is trying to make happen over time.

### Strengths

- excellent for vague desire → structured pursuit → Plan → execution → Actual → history;
- strong for long-running change;
- strong for competing intentions and orchestration;
- very aligned with the North Star loop.

### Structural failure mode

A large amount of real life does not deserve to become a trajectory.

Examples:

- one dentist appointment;
- tomorrow's weather question;
- a bill;
- one dinner;
- a maintenance event;
- "Luca is my brother";
- an isolated medication dose.

If everything becomes a trajectory, LifeOS becomes a universal project manager.

---

## D. Stable Spine + Adaptive Contexts

### Core idea
LifeOS exposes a small number of predictable interaction/orientation mechanisms while allowing specific contextual views to emerge only when useful.

Natural language is global.

Persistent structure, time, continuation and unresolved state remain understandable through stable semantics.

Specific situations can compose contextual UI from a controlled vocabulary of components and actions.

### Why it currently performs best

It does not need to change its fundamental unit when the domain changes.

It can support:

- simple appointments;
- vague desires;
- long Plans;
- Actual vs planned;
- contextual questions;
- hidden knowledge;
- on-demand asset/person views;
- multi-actor shared reality;
- high consequence provenance;
- GUI-heavy use;
- conversation-heavy use;
- AI-off fallback;
- hundreds of simultaneous elements.

### Structural risk

Its success depends on discipline.

If the stable layer grows too much:

> dashboard / database UI.

If the adaptive layer becomes too unconstrained:

> chatbot / generative chaos.

The purpose of the Interaction Architecture Contract is precisely to constrain this boundary.

---

# 7. Current working recommendation

The strongest current inference is:

> **Design one persistent structured personal reality with a small set of stable interaction mechanisms, multiple projections, contextual/on-demand surfaces, and natural language capable of interrogating and modifying that same reality.**

This should **not** be misread as:

```text
Home + Chat + Goals + Calendar + Inbox + generated pages
```

That would be a feature bundle, not an architecture.

The architectural principle is:

> **The same reality can be oriented, interrogated, modified and projected in different forms; a form becomes persistent only when persistence itself creates value.**

The other three architectures are not discarded completely.

Instead:

- Situation-first should strongly influence everyday orientation.
- Conversation-first should influence the communication layer.
- Trajectory-first should influence continuity from intention to execution/history.
- Stable + adaptive acts as the broader architecture that prevents any one of them from becoming totalizing.

---

# 8. Draft Interaction Architecture Contract — candidate invariants

**Status: WORKING DRAFT. Review principle by principle; accepted decisions are marked explicitly below.**

## IA-01 — The persistent model is richer than the persistent UI

### Decision
**ACCEPTED — 2026-08-14**

### Principle
Existing in the model does not grant an entity a permanent surface.

### Invariant
A Person, Asset, Preference, Relationship, Observation, Source or similar internal concept must not automatically create navigation/UI.

### Does not imply
Hidden forever.

Knowledge can become contextual, on-demand, inspectable and correctable.

---

## IA-02 — Stability belongs to recurring user needs, not entity types

### Decision
**ACCEPTED — 2026-08-14**

### Principle
The predictable part of LifeOS should serve recurring interaction needs.

Examples of needs:

- orient;
- communicate;
- continue;
- resolve;
- inspect;
- correct.

### Invariant
Do not design primary navigation simply by listing domain primitives.

### Open question
Which of these needs deserve persistent top-level access versus contextual access?

---

## IA-03 — One reality, multiple projections

### Decision
**ACCEPTED — 2026-08-14**

### Principle
LifeOS maintains one persistent semantic reality that can be exposed through multiple projections and surfaces.

Calendar, history, attention, Actual, trajectory, search results, contextual views, natural-language interaction, Web and Mobile must not behave like disconnected copies.

### Invariant
Changes to semantic reality must remain coherent across projections, while each projection may independently choose what to show, omit, emphasize or aggregate.

Presentation state must not become a competing source of truth.

### Does not imply
Every projection must show the same information or expose the same level of detail.

### Open question
How much visual continuity is required between projections so the user perceives semantic continuity without exposing the underlying domain graph?

---

## IA-04 — Time is primary but not sovereign

### Decision
**ACCEPTED — 2026-08-14**

### Principle
Time is a first-class dimension and one of LifeOS's strongest operational projections, but it is not the universal container of the personal model.

Persistent realities may exist without scheduling.

### Invariant
A persistent thing must be able to exist without a schedule or calendar block.

Temporal projections must preserve the distinction between what is planned in time and what actually exists or happened.

Changing the schedule of something must not automatically change its identity, purpose or historical truth.

### Does not imply
Calendar is secondary or weak.

Today/Calendar may remain one of the strongest operational surfaces in the product, with different presentation affordances across Mobile and Web.

### Open question
How much temporally relevant reality that is not a classic calendar block — deadlines, windows, availability, temporal constraints, dependency timing, "by Friday" risk — should appear inside temporal projections?

Do not answer this by forcing every temporal fact into a scheduled block.

---

## IA-05 — Current situation is broader than the timeline

### Principle
"What is happening now?" can include more than scheduled items.

Relevant categories can include:

- now / next;
- meaningful changes;
- current capacity/constraints;
- blocking dependencies;
- risks;
- observed reality vs expected reality;
- unresolved matters requiring attention.

### Invariant
Do not force all situational relevance into calendar blocks.

### Open question
Whether current situation is one dedicated surface or multiple coordinated projections remains unresolved.

---

## IA-06 — Natural language is a global interaction layer

### Principle
The user may communicate facts, questions, exceptions, corrections and changes naturally from the current context.

### Invariant
Natural language must operate on the same structured reality as the GUI.

### Does not imply
Every task requires a conversation.

### Does not imply
A dedicated AI Chat page is forbidden; only that it must not become a separate semantic universe or the only way to use LifeOS.

---

## IA-07 — GUI remains a first-class language

### Principle
The user must be able to scan, compare, manipulate and correct structured state directly.

### Invariant
Core frequent or precision-sensitive operations cannot depend exclusively on prompting an AI.

### Rationale
Persistent state comprehension, direct manipulation and AI-off resilience require non-conversational paths.

---

## IA-08 — Natural language and GUI must be semantically equivalent

### Principle
Two interaction modes expressing the same intent should produce the same scope, state transition and history.

Example:

```text
NL: "Skip only today."
GUI: equivalent one-occurrence control
```

Both must modify the same semantics.

### Invariant
No separate "chat state" and "app state".

---

## IA-09 — Adaptive UI must use a controlled grammar

### Principle
LifeOS may compose contextual summaries, comparisons, timelines, charts, options, evidence panels or controls.

### Invariant
Generated/contextual UI must not invent new meanings for core states, authority, privacy, confirmation or scope.

### Open question
How much layout variability is acceptable before the mental model becomes unstable?

---

## IA-10 — Contextual views may be ephemeral

### Principle
A request may generate a useful view without creating a permanent destination.

Example:

```text
"How much has the Giulietta cost me this year?"
```

can create a temporary aggregate surface.

### Open question
When should a recurring contextual view become savable or persistent?

---

## IA-11 — Unresolved state is not attention policy

### Principle
Something can remain semantically unresolved without being shown continuously.

Keep separate:

```text
unresolved
≠ show now
≠ notify
≠ interrupt
```

### Invariant
An open loop ignored for a week must not require a week of notification harassment.

### Open question
How should unresolved items aggregate when the user wants a complete review?

---

## IA-12 — Intention structure develops progressively

### Principle
A vague desire may remain vague.

Structure is added when it creates value.

Possible progression:

```text
vague desire
→ stronger intention
→ feasibility / constraints
→ optional Goal
→ optional Plan
→ activities / schedule
→ Actual
→ outcome / history
```

Not every item must traverse every stage.

### Invariant
The user must not be forced through an ontology wizard.

---

## IA-13 — Internal ontology is not required user vocabulary

### Principle
The domain may remain precise underneath while product interaction stays natural.

### Invariant
A user should not need to decide whether a statement is technically an Intention, Goal or Plan before expressing it.

---

## IA-14 — Planned, Actual, Outcome and Evidence remain distinct

### Principle
The UI may simplify these distinctions contextually, but the architecture must preserve them.

### Invariant
Passing time or checking a box cannot be the only mechanism for establishing reality.

---

## IA-15 — Hidden knowledge must remain inspectable and correctable

### Principle
Not showing internal knowledge by default must not make it uncontrollable.

### Invariant
The user must be able, when appropriate, to ask things like:

```text
"What do you know about my car?"
"Why are you suggesting this?"
"What are you assuming here?"
"That preference is wrong."
```

### Open question
What transparency/control surface best supports this without creating a raw database settings UI?

---

## IA-16 — Modification scope must be explicit when consequential or ambiguous

### Principle
The same intent can apply at different scopes.

Examples:

```text
only today
this week
this occurrence
this series
this Plan
until I say otherwise
across all affected commitments
```

### Invariant
LifeOS must not silently infer a broad consequential scope when ambiguity materially changes the result.

---

## IA-17 — Attention and autonomy are separate axes

### Working attention scale

```text
P0 — LifeOS knows it
P1 — uses it when asked
P2 — surfaces it in relevant context
P3 — places it in an attention surface
P4 — actively interrupts
```

### Working autonomy scale

```text
A0 — informs
A1 — suggests
A2 — prepares
A3 — executes after confirmation
A4 — executes within prior authorization / reversible policy
```

### Invariant
Importance to show and permission to act must not be represented by one shared scale.

### Status
This scale is a working design inference, not yet canonical policy.

---

## IA-18 — Shared reality and personal context remain separable

### Principle
Multi-actor LifeOS should support shared facts while preserving independent personal models, private consequences and authority boundaries.

### Invariant
A shared event does not require merging every participant into one common workspace or exposing private reasons.

Example:

```text
Private fact:
A is unavailable 18:30–19:30 for a private reason.

Shareable consequence:
20:00 works.
```

### Does not imply
A permanent top-level Collaboration mode.

---

## IA-19 — The operational core must remain useful without AI

### Principle
AI can dramatically improve LifeOS, but must not be the only route to essential state and control.

### Invariant
Without AI, the user must still be able to understand and perform essential operations such as:

- inspect current state;
- use the calendar/time projection;
- inspect important unresolved matters;
- inspect history;
- make core modifications;
- correct important data.

### Open question
The exact minimum AI-off capability contract remains to be defined.

---

# 9. Interaction traces required before Information Architecture

Before deciding Home, navigation or top-level surfaces, the candidate contract must be tested through complete interaction traces rather than isolated screenshots.

Recommended trace set:

1. **"One day I'd like to go to Japan."**
   - persistence without taskification;
   - no forced Goal/Plan.

2. **Import a professional diet → "today let's change lunch."**
   - external Plan provenance;
   - local adaptation;
   - source integrity;
   - no accidental Plan destruction.

3. **Gym scheduled → skipped.**
   - planned ≠ Actual;
   - unresolved consequences.

4. **Gym scheduled → only half completed.**
   - partial execution;
   - no forced yes/no.

5. **"Don't ask me every time."**
   - change confirmation policy rather than current record only.

6. **"I'm ill this week, lighten things."**
   - temporary global capacity reduction;
   - cross-context orchestration;
   - explicit scope and consequences.

7. **"Should I bring an umbrella to Rome tomorrow?"**
   - contextual ephemeral question;
   - no required persistent object.

8. **"I own an Alfa Giulietta" → months later "how much has it cost me?"**
   - invisible knowledge;
   - contextual aggregate UI;
   - no required permanent Asset section.

9. **"Luca is my brother" → later organize dinner with Luca.**
   - invisible Person/Relationship knowledge becoming contextually useful.

10. **40 competing intentions with insufficient capacity.**
    - orchestration;
    - ability to say not everything fits;
    - defer / resize / stop instead of simply ranking all tasks.

11. **Incorrect inferred preference.**
    - inferred ≠ declared;
    - easy correction;
    - downstream behavior update.

12. **Imported source conflicts with user-declared information.**
    - provenance;
    - uncertainty;
    - conflict preservation rather than silent overwrite.

13. **Open loop ignored for several days.**
    - unresolved remains unresolved;
    - attention delivery can decay/defer without losing state.

14. **Multi-actor change with a private cause.**
    - use private constraint;
    - expose only shareable consequence.

15. **Same major workflow — GUI only.**
    - no dependence on natural language.

16. **Same major workflow — mostly conversational.**
    - no forced navigation bureaucracy.

17. **AI unavailable.**
    - operational core survives.

18. **Hundreds of simultaneous elements and many active initiatives.**
    - progressive disclosure;
    - retrieval;
    - no dashboard collapse.

### Trace review template

Every trace should document the same seven questions:

```text
1. Where does the interaction start?
2. What is visible to the user?
3. What knowledge/context is used but not shown?
4. What semantic state changes?
5. What consequences follow?
6. What remains open or uncertain?
7. How can the user correct, undo, narrow or change their mind?
```

If a trace breaks the architecture, revise the contract before inventing a special-case screen.

---

# 10. What must not be decided yet

This workstream intentionally does **not** yet fix:

- final Home semantics;
- whether Home exists in its current form;
- final navigation;
- number of primary sections;
- names of future surfaces;
- replacement for the historical `Worlds` label;
- whether open-loop aggregation deserves a persistent destination;
- whether current situation is one surface or several coordinated projections;
- exact shape of contextual/generated UI;
- visual design;
- card layout;
- typography;
- color system;
- animation;
- final notification policy;
- exact autonomy thresholds;
- exact fallback experience without AI.

Do not turn this research guide into premature Information Architecture.

---

# 11. Relationship to the current Phase 4 frontend baseline

The existing Home + Today Integrated v1 remains the approved/restorable frontend checkpoint.

This guide does not invalidate the quality of that work.

It changes only its architectural status:

> **The existing prototype is evidence and reusable design work, not a constraint on the final interaction architecture.**

Until explicitly approved otherwise:

- do not modify the integrated baseline as part of this research work;
- do not delete historical Phase 4 artifacts;
- do not silently reinterpret current UI labels as new architecture decisions;
- do not use the current Home to constrain research alternatives;
- do not use the current `Worlds` section as an authoritative concept.

When the interaction architecture and later Information Architecture are validated, compare the prototype element-by-element using:

```text
KEEP
REINTERPRET
CHANGE
REMOVE
ADD
```

Only then begin a new frontend iteration.

---

# 12. External research directions and reference families

The Deep Research synthesis consulted primary/official evidence in the following families:

- Microsoft Research — mixed-initiative interaction;
- Microsoft HAX — Guidelines for Human-AI Interaction;
- Microsoft Research — AI Instruments / direct manipulation with AI;
- Microsoft Research — Ironies of Generative AI;
- Microsoft Research — attention-sensitive alerting and notification deferral;
- Microsoft Research — context-sensitive reminding;
- Microsoft Research — Magentic-UI / human-in-the-loop agentic systems;
- Apple Human Interface Guidelines — Machine Learning / Generative AI / Alerts / Notification interruption levels;
- Google Research — generative UI;
- Google A2UI — controlled agent-driven interface composition;
- Personal Information Management / activity-centered research;
- contemporary product patterns including Todoist, Notion, Reclaim, Motion and Sunsama.

These references support general interaction principles; they do not define LifeOS product decisions.

---

# 13. Current open product decisions

The following questions should be resolved through discussion + traces before Information Architecture:

1. **What precisely belongs to the stable spine?**
   - semantic rules only?
   - global communication?
   - orientation access?
   - persistent destinations?

2. **What is the exact relationship between Current Situation and Today/Calendar?**

3. **How should long-lived pursuits be exposed without forcing the user to understand Goal vs Plan vs intention?**

4. **Do open loops need a permanent aggregated destination, or only contextual surfacing plus an on-demand review?**

5. **How does a contextual view become persistent when repeated use makes persistence valuable?**

6. **How much generative/adaptive layout variation is compatible with a stable mental model?**

7. **How should hidden knowledge/inferences become inspectable without exposing a raw database?**

8. **What is the minimum non-AI interaction contract?**

9. **What are the practical attention and autonomy policies?**

10. **What interaction semantics are universal enough to become stable product grammar?**

---

# 14. Immediate next step

Do **not** draw Home yet.

The immediate next task is:

> **Review the draft Interaction Architecture Contract principle by principle and decide what is accepted, rejected, modified or still open.**

Recommended discussion format for each principle:

```text
PRINCIPLE
Why it exists

INVARIANT
What future UX must not violate

DOES NOT IMPLY
Misreadings to prevent

EXAMPLES
Concrete LifeOS scenarios

OPEN QUESTION
What is intentionally unresolved

DECISION
Accept / modify / reject / keep open
```

After the contract is stable enough, run the interaction traces in Section 9.

Only after those traces hold should Phase 4 derive Information Architecture and later return to visual frontend work.

---

# 15. One-sentence working direction

> **LifeOS should not be designed as pages corresponding to its internal model, nor as an AI chat added beside those pages; it should be designed as one structured personal reality with a small predictable interaction grammar, multiple projections, contextual/adaptive surfaces, and natural language operating on that same reality.**

This is the current strongest research-backed direction.

It remains a **working Phase 4 inference** until explicitly accepted through the review process above.
