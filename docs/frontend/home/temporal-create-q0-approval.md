# DANTE — Temporal Create Q0 Approval Record

**Status:** APPROVED BASELINE / AMENDED BY ACTIVE C1 SCOPE EXPANSION
**Date:** 2026-09-01
**Owner workstream:** `feature/home-timeline`
**Base contract:** `docs/frontend/home/temporal-create-q0-contract.md`
**Active scope amendment:** `docs/frontend/home/temporal-create-c1-scope-amendment.md`
**Live status:** `docs/frontend/home/temporal-live-status.md`
**Current handoff:** `docs/frontend/home/temporal-create-handoff.md`
**Prerequisite:** F0 closed on `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`

The user explicitly approved Q0 on 2026-09-01 and authorized implementation of the complete C1 `+` / Create capability to production-oriented pre-backend depth.

The historical `FREEZE CANDIDATE — USER REVIEW REQUIRED` status line still present in the restored full Q0 text is not current operational status. This approval record supersedes that line.

## Delivery gate override — 2026-09-01

The user clarified that C1-A through C1-H are **internal engineering slices, not separate product approval gates**.

The active delivery rule is:

```text
internal C1 slices
= implementation/checklist boundaries

C1 complete
= one substantive user-facing approval gate
```

Therefore:

- implementation proceeds continuously across internal slices;
- each slice still receives automated tests, architecture checks and CI evidence appropriate to its risk;
- intermediate defects are corrected while work continues rather than forcing a user acceptance stop after every micro-step;
- the user performs substantive manual acceptance when the full `+` / Create system is coherent;
- an earlier user decision is requested only when a genuinely unresolved product/semantic choice cannot be resolved from accepted DANTE authority;
- real backend/API/DB/provider integration remains outside C1 and belongs to the later Timeline backend/external vertical.

## Scope expansion override — 2026-09-01

After manual review of the first complete compact composer, the user explicitly clarified that the intended deliverable is **not merely a bounded Quick Add form**. The required stop line is the maximum useful DANTE Create system before backend integration.

Therefore `temporal-create-c1-scope-amendment.md` now supersedes, where conflicting:

- the earlier bounded C1 scope in `temporal-create-q0-contract.md`;
- the C1 section of `temporal-frontend-roadmap.md`;
- any wording in this approval record that could be read as declaring the compact Quick Create implementation sufficient for closure.

The expanded target is:

```text
Quick Create
+
Expanded Create
+
Full Create editor / deep authoring
+
truthful external-vertical handoffs
```

all sharing one structured draft/application/command path.

This expansion does **not** authorize fake backend behavior, provider writes, server persistence, solver execution, AI runtime or voice runtime.

## Relationship to later C5/C7 phases

The scope amendment expands **creation-time authoring** of scheduling constraints, recurrence and replanning policy where authoritative.

It does not absorb all later temporal behavior:

- C5 still owns broader recurrence management and scheduling-flexibility interaction for existing items/occurrences;
- C7 still owns conflict/replanning proposal experience and future solver integration.

Create must author enough structure that those later phases do not require rewriting the creation model.

## Current implementation state

C1 is **OPEN / NOT USER-ACCEPTED**.

A strong compact Quick Create foundation exists, including Activity/Event, temporal forms, F0-backed command execution, preview, local projection, reveal, Undo, contextual invocation, responsive behavior and automated coverage.

Manual review established that this is only the first presentation layer of the required Create system. It must not be treated as the final C1 deliverable.

The current operational truth is recorded in `temporal-live-status.md` and the continuation procedure is recorded in `temporal-create-handoff.md`.

C1 may be marked CLOSED only after the expanded scope is implemented, all final automated gates are green on one coherent implementation checkpoint, and the user explicitly approves the complete Create system.
