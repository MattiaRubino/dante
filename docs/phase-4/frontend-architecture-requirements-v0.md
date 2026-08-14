# LifeOS — Frontend Architecture Requirements v0

**Status:** Working synthesis — not yet Information Architecture  
**Date:** 2026-08-14  
**Branch:** `prototype/phase-4-today-home`  
**UI / prototype mutation authorized:** **No**

## Purpose

This document translates the accepted Interaction Architecture direction and the validated simulation-derived usage patterns into frontend requirements.

It does **not** define final navigation, Home, Today, top-level sections, visual design, component styling or final Mobile/Web layouts.

The purpose is to establish what the frontend must make possible before deciding which permanent surfaces or navigation anchors should exist.

---

# 1. Evidence basis

Primary inputs:

- `docs/product/feature-discovery-simulation-2026-08.md`
- `docs/product/multi-actor-collaboration-discovery-simulation-2026-08.md`
- `docs/product/multi-actor-collaboration-research-2026-08.md`
- `docs/product/product-identity-and-north-star.md`
- `docs/domain/language-map.md`
- `docs/phase-4/interaction-architecture-decisions-v0.md`
- `docs/phase-4/cross-platform-interaction-rule-v0.md`

The simulation documents are used as behavioral evidence, not as authority for old UI nouns or historical feature bundles.

---

# 2. Recurrent real-use families

The reviewed corpus and interaction traces converge on five broad usage families.

## 2.1 Daily / Immediate

The user needs to:

- understand the current situation quickly;
- understand what is happening now / next;
- act on current or imminent things with low friction;
- report what actually happened;
- react when something changes during the day.

Frontend implications:

- predictable orientation access;
- strong temporal projection;
- quick actions for current/imminent items;
- low-friction Actual capture;
- contextual escalation when a simple action has wider consequences.

## 2.2 Continuity

The user needs to:

- resume something they are carrying forward;
- understand where they are and what changed;
- see the next relevant element where one exists;
- preserve context across pauses;
- let something become dormant without losing it.

Frontend implications:

- reliable continuation/resume;
- persistent but non-current reality must remain recoverable;
- continuity cannot depend only on Calendar or AI conversation;
- long-lived pursuits must not require the user to understand internal Goal / Plan / Activity distinctions.

## 2.3 Capture + Retrieval

The user needs to:

- tell LifeOS something without classifying it first;
- use specialized structured capture where repetition makes it faster;
- retrieve something later without remembering the internal type or storage location;
- inspect found information structurally;
- correct durable knowledge and inspect provenance when relevant.

Frontend implications:

- general-purpose communication/capture path;
- specialized quick forms for repetitive structured inputs;
- semantic retrieval over durable LifeOS reality;
- contextual inspection after retrieval;
- hidden/dormant does not mean irretrievable;
- retrieval must scale without turning the UI into a Domain Model browser.

## 2.4 Disruption + Adaptation

The user needs to:

- express local exceptions;
- change scope explicitly when consequential;
- understand what a disruption affects;
- preview wider changes before applying them;
- preserve history while adapting the future;
- distinguish proposal from applied state;
- let LifeOS act within prior authority where appropriate.

Frontend implications:

- impact inspection;
- scope controls;
- preview / proposal patterns;
- reversible changes where appropriate;
- history that preserves previous planned and Actual reality;
- interaction depth should increase with consequence depth.

## 2.5 Deep / Contextual

The user needs to:

- investigate a specific question deeply;
- compare planned vs Actual;
- inspect cost, trajectory, history or evidence;
- understand why LifeOS is suggesting something;
- compare options and make complex decisions;
- work with large amounts of information without permanent navigation for every possible question.

Frontend implications:

- rich contextual/on-demand surfaces;
- structured outputs rather than AI text only;
- drill-down to underlying data and provenance where material;
- controlled composition from a stable interaction grammar;
- contextual views may be temporary without making their durable effects temporary.

---

# 3. Core frontend capability requirements

The frontend must support the following capabilities regardless of final navigation.

| Capability | Requirement | Expected exposure characteristic |
|---|---|---|
| Orientation | Understand current situation, what matters, what is next and meaningful changes | Predictable / stable access |
| Time | Inspect temporal reality, planned items and relevant temporal constraints | Primary stable projection |
| Communication / Capture | Tell, ask, report, correct or express intent with low friction | Global / rapid access |
| Continuation | Resume long-lived or carried-forward realities | Predictable access |
| Action / Adaptation | Act, modify, report Actual and negotiate exceptions | Strongly contextual + quick actions |
| Retrieval / Inspection | Find and inspect durable reality regardless of current visibility | Global recoverability |
| Resolution / Review | Intentionally inspect unresolved, uncertain or pending matters | Recoverable aggregation; exact surface unresolved |

These capability names are architecture working labels, **not proposed navigation labels**.

---

# 4. Frontend strata

A useful current model is three interacting strata rather than a product composed only of fixed pages.

## 4.1 Stable Access / Orientation

Purpose:

- provide predictable entry points and mental-model anchors;
- ensure important recurring needs are not dependent on generated UI;
- preserve operational usability when AI is unavailable.

Candidate capabilities requiring predictable access include:

- orientation;
- time;
- communication/capture;
- continuation;
- retrieval.

This does **not** mean five top-level tabs.

## 4.2 Operational / Contextual Layer

Purpose:

- let the user act directly on the current thing;
- keep ordinary operations shallow;
- escalate only when scope or consequences require it.

Examples of pattern families to validate:

- Start / Stop / Done / Partial / Skip;
- modify / move / cancel;
- scope selection;
- contextual capture;
- proposal / apply / modify / reject;
- undo / correction;
- resume / continue;
- inspect / deepen.

## 4.3 Adaptive / Deep Surfaces

Purpose:

- answer complex questions without pre-building a permanent page for every query or domain;
- support comparison, investigation, reasoning and high-information-density work.

Potential controlled grammar families include:

- summary;
- list;
- timeline;
- comparison;
- table;
- chart;
- status;
- history;
- evidence/provenance;
- options;
- impact;
- proposal;
- preview;
- filters;
- drill-down;
- contextual actions.

This is a working grammar family list, not yet a canonical component library.

---

# 5. Cross-cutting interaction layers

## Natural language / AI

Natural language and AI operate across all frontend strata rather than as a separate semantic product.

They may:

- retrieve;
- interpret;
- summarize;
- reason;
- compare;
- propose;
- request structured LifeOS operations.

When durable state changes, the result must become inspectable LifeOS state rather than transcript-only state.

## Multi-actor

Multi-actor behavior should normally extend the same interaction architecture rather than create a separate product mode.

Additional constraints include:

- participant-specific views;
- shared fact vs personal overlay;
- scoped visibility;
- authority/responsibility;
- proposal/acknowledgement/confirmation where appropriate;
- private cause may remain hidden while shareable consequence is exposed.

---

# 6. Mobile / Web implications

## Mobile-primary stress condition

Routine mobile flows should favor:

```text
look
→ understand
→ one/few actions
→ continue life
```

Mobile must be particularly strong for:

- orientation;
- current/next temporal awareness;
- quick Actual capture;
- quick actions;
- capture/communication;
- disruption acknowledgement and first response;
- fast resume.

## Web strength

Web may use additional space for:

- planning;
- comparison;
- history;
- timelines;
- analytics;
- multi-object inspection;
- complex adaptation;
- deep contextual/reasoning work.

This difference is representational, not semantic.

---

# 7. Frontend design guardrails derived from the traces

1. **Interaction depth grows with consequence depth.**
   A low-consequence operation should remain shallow; broader or higher-impact changes may require scope, preview and explanation.

2. **Not surfaced does not mean forgotten.**
   Durable non-current reality remains intentionally recoverable.

3. **Proposal is not state.**
   Generated/recommended changes must not visually masquerade as already-applied reality.

4. **Adapt the future without rewriting the past.**
   New planning must preserve historical Planned / Actual distinctions where relevant.

5. **Recoverability without ontology exposure.**
   LifeOS should make rich reality retrievable without forcing a permanent UI hierarchy matching Domain Model types.

6. **Structured depth after conversational entry.**
   Natural language may be the fastest way into a question, but meaningful inspection should be able to become structured UI.

7. **Simple users must not pay for expert complexity.**
   Progressive disclosure is required for the same architecture to support lightweight and high-complexity use.

---

# 8. Questions now appropriate for Information Architecture

The following questions are now mature enough to discuss:

1. Which capabilities require persistent/predictable anchors rather than contextual-only access?
2. What is the relationship between current-situation orientation and Today / Calendar?
3. How should the user access long-lived carried-forward realities without making Goal / Plan / Project taxonomy the navigation model?
4. What is the global retrieval mechanism and how does it transition into contextual views?
5. What is the persistent role of communication/capture in Mobile and Web?
6. Does unresolved/review need a stable destination, an on-demand aggregation, or both?
7. Which interaction anchors must remain visually stable even when surrounding content adapts?
8. Which controlled UI grammar primitives are universal enough to standardize before visual design?

These questions must be answered from user needs and interaction traces, not by mirroring the Domain Model.

---

# 9. Immediate next step

Derive the **stable frontend anchors and first Information Architecture candidates** from the requirements above.

Do not yet mutate the approved Home + Today frontend baseline.

The first architecture decision should establish which recurring capabilities need predictable product-level access; only then should those capabilities be mapped to concrete Mobile/Web navigation or surfaces.
