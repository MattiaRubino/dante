# LifeOS — Phase 4 Cross-Platform Interaction Rule v0

> Working cross-platform rule for the Phase 4 Interaction Architecture workstream.
>
> This document complements `docs/phase-4/interaction-architecture-guide-v0.md` on the `prototype/phase-4-today-home` branch.
>
> It does **not** define final Web or Mobile information architecture, navigation, visual design, or implementation technology.

---

## 0. Status

| Field | Value |
|---|---|
| Product | LifeOS — Personal Operating System |
| Phase | 4 — frontend prototyping and UX validation |
| Workstream | Interaction Architecture |
| Status | **IN PROGRESS — working cross-platform rule** |
| Date | 2026-08-14 |
| Branch | `prototype/phase-4-today-home` |
| Related guide | `docs/phase-4/interaction-architecture-guide-v0.md` |
| UI mutation authorized | **No** |

Nothing in this file fixes final mobile or web UI. It records a design constraint to use while the Interaction Architecture Contract is being validated.

---

# 1. Core cross-platform rule

> **LifeOS is one personal system expressed through multiple surfaces, not separate Web and Mobile products that merely synchronize data.**

The durable semantic reality, history, state transitions, scope rules, provenance, authority, privacy and interaction meaning must remain consistent across surfaces.

Web and Mobile may represent the same reality differently because their affordances, available space and usage contexts differ.

Therefore:

```text
same LifeOS reality / semantics
              ↓
      multiple surfaces
       ↙             ↘
   Mobile             Web
```

A capability belongs to LifeOS first. A surface then decides how to expose that capability appropriately.

---

# 2. Mobile-primary, not mobile-only

A current product hypothesis is that real-world LifeOS usage may happen predominantly on mobile — potentially around **85% of routine interaction**.

This is a **working product hypothesis**, not a validated usage statistic. It must not be promoted to a canonical metric until real product analytics or user evidence exists.

It is nevertheless strong enough to prevent desktop-centric architecture decisions during Phase 4.

Working principle:

> **Validate the interaction architecture against realistic mobile use before relying on additional desktop space.**

This does not mean that LifeOS capabilities should be restricted by device.

Avoid rigid rules such as:

```text
Mobile = capture only
Web = planning only
```

A user may plan a complex trip entirely from a phone or perform a quick correction from Web.

The distinction is one of **surface affordance and emphasis**, not separate semantic capability sets.

---

# 3. Likely surface affordances — working hypotheses

These are tendencies to validate, not capability boundaries.

## Mobile tends to favor

- immediate interaction;
- interaction while moving or inside the real-world context;
- natural-language and voice input;
- camera/document/photo capture;
- quick Actual reporting;
- quick confirmations/corrections;
- contextual questions;
- rapid local replanning;
- notifications and time-sensitive attention;
- location/device-context-aware interactions;
- short decision loops.

Examples:

```text
"I only did half the workout."
"I skipped this."
"Move this to tomorrow."
"I'm ill this week, lighten things."
"Should I bring an umbrella?"
"I spent €80 on fuel."
```

These interactions should not require navigating through the domain ontology before communicating the real-world fact or change.

## Web tends to favor

- high information density;
- broader temporal views;
- comparison of alternatives;
- complex planning and orchestration;
- many simultaneous initiatives;
- historical analysis;
- bulk reorganization;
- multi-panel inspection;
- deeper editing and review.

These tendencies do **not** make the corresponding capabilities unavailable on Mobile.

---

# 4. Cross-device continuity

A LifeOS interaction may begin on one surface and continue on another without translation into a different conceptual model.

Example:

```text
MOBILE
"One day I'd like to go to Japan next year."
        ↓
LifeOS preserves the intention

WEB — later
"Let's seriously explore Japan."
        ↓
richer feasibility / period / budget / constraints view

MOBILE — during the trip
        ↓
current situation / tickets / weather / next movement /
quick questions / disruption handling
```

The user is not moving between three products or three copies of the same object.

They are interacting with the **same persistent LifeOS reality** through surfaces optimized for different contexts.

---

# 5. Architecture test rule

For every candidate interaction principle and every major interaction trace, ask:

> **Is this a LifeOS principle, or are we accidentally describing a desktop interface?**

A future architecture should fail review if it only works because a large desktop canvas hides excessive hierarchy or interaction complexity.

Working validation rule:

> **Every core interaction trace must work coherently on a realistic mobile surface first; Web may then exploit additional space and density without changing the underlying semantics.**

This does not require identical click/tap counts, layouts or navigation structures.

It requires semantic and behavioral continuity.

---

# 6. Relationship to the Interaction Architecture Contract

The following existing draft principles are naturally cross-platform:

- IA-01 — persistent model richer than persistent UI;
- IA-02 — stability belongs to recurring user needs, not entity types;
- IA-03 — one reality, multiple projections;
- IA-06 — natural language as a global interaction layer;
- IA-07 — GUI remains first-class;
- IA-08 — natural language and GUI remain semantically equivalent;
- IA-09 — adaptive UI uses a controlled grammar;
- IA-11 — unresolved state is separate from attention policy;
- IA-16 — modification scope must remain explicit when consequential;
- IA-17 — attention and autonomy are separate axes;
- IA-19 — essential operation remains possible without AI.

Cross-platform design should not weaken any of these invariants.

---

# 7. Additional cross-platform invariant candidate

## IA-20 — One semantic system, surface-specific interaction

### Principle
Web and Mobile operate on one LifeOS semantic reality while adapting interaction and presentation to their respective affordances.

### Invariant
A state transition must not acquire a different meaning because it was performed from Mobile rather than Web.

Examples:

```text
"Skip only today"
```

must have the same scope and history whether expressed via voice on Mobile or a structured control on Web.

```text
"I completed only half"
```

must represent the same Actual semantics regardless of surface.

### Does not imply

- identical layouts;
- identical navigation;
- identical interaction counts;
- feature parity at every implementation milestone;
- a responsive Web UI being automatically sufficient as the Mobile product.

### Open questions

- Which interactions require device-specific controls or affordances?
- Which mobile integrations should become first-class later (voice, camera, location, notifications, widgets, share sheet, etc.)?
- Which Web affordances justify richer persistent views?
- What is the minimum cross-device continuity required for interrupted workflows?

---

# 8. Updated interaction-trace validation

When the Phase 4 interaction traces begin, each major trace should record two additional questions after the existing seven:

```text
8. How does this interaction work on Mobile without relying on desktop space?
9. How can Web exploit additional space without changing the semantic result?
```

For high-frequency real-world traces, Mobile should be tested first.

Priority mobile-primary traces include:

- partial workout completion;
- skipped activity;
- quick rescheduling;
- temporary capacity reduction;
- contextual question;
- quick fact/expense capture;
- correction of an inference;
- unresolved confirmation response;
- local Plan renegotiation;
- disruption while outside the home/office.

Complex traces must still be tested on both surfaces.

---

# 9. Development sequencing

Cross-platform architecture does not require simultaneous full UI implementation.

The current working sequence is:

```text
Interaction Architecture Contract — cross-platform
        ↓
Interaction traces — Mobile + Web
        ↓
Information Architecture derivation for both surfaces
        ↓
Web design / implementation first
        ↓
Dedicated Mobile design / implementation
```

This sequence intentionally avoids two opposite mistakes:

1. designing a desktop product first and shrinking it later;
2. doubling Phase 4 design/implementation work before the common interaction model is stable.

---

# 10. Working conclusion

> **LifeOS should be architected cross-platform from the semantic and interaction level, validated mobile-first where real-world usage is likely to be dominant, and later expressed through independently designed Web and Mobile interfaces that preserve the same underlying reality and behavioral meaning.**

Status: **working Phase 4 rule, pending validation through the Interaction Architecture Contract and interaction traces.**
