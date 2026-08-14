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

# Review position

Accepted through: **IA-05**.

Next principle for discussion: **IA-06 — Natural language is a global interaction layer**.

No frontend/prototype mutation is authorized by these decisions.
