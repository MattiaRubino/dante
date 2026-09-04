# DANTE — Temporal Create C1 Re-architecture — 2026-09-03

**Status:** SUPERSEDED HISTORICAL PRODUCT RECORD  
**Superseded:** 2026-09-04 by `temporal-create-c1-manual-findings-2026-09-04.md` and `temporal-live-status.md`  
**Branch:** `feature/home-timeline`

## Purpose

This file preserves the product reasoning that followed the 2026-09-03 manual fail. It is no longer the live operational authority and must not override later 2026-09-04 decisions.

The durable conclusions from this re-architecture remain valid:

```text
USER INTENT
→ SENSIBLE DEFAULT
→ ONLY RELEVANT CONTROLS
→ CONDITIONAL DISCLOSURE
→ ADVANCED DEPTH ON DEMAND
→ DANTE SEMANTICS UNDER THE HOOD
```

Permanent semantic boundaries remain:

```text
Activity != Event != Routine
Schedule != Occurrence != Session != Actual
planned/intended != happened
recurrence specification != generated Occurrence
Context != appearance
provider intent != provider execution
frontend projection != canonical backend identity
manual Create != AI/NL/voice input
```

## Historical decisions retained

The 2026-09-03 pass established:

- title-first Create;
- extensible actionable type registry;
- Activity/Event common paths without wizard tax;
- base + `Opzioni avanzate` instead of user-visible Quick/Expanded/Full;
- Activity placement independent from execution/session structure;
- Planning Tray as home for unplaced Activity;
- per-day all-day lane rather than global strip or fake 24-hour timed event;
- Event recurrence with CP6-deep custom grammar;
- Event Agenda/internal parts rather than a generic nested domain entity;
- no fake Reminder/provider/runtime success.

## 2026-09-04 superseding corrections

Where this historical document previously described different UX, use the current authority instead:

- Advanced is now a **larger floating non-modal desktop surface**, not the old centered modal/workspace target;
- Home/Timeline remains interactive while Create is open;
- simple desktop Create opens floating at a stable position and is draggable;
- `Personalizzata…` is part of the `Ripeti` selector rather than a separate customization control;
- user-facing Activity repeat is allowed only as explicit **Routine-backed recurrence intent**; direct Activity-owned recurrence remains forbidden;
- canonical recurring Occurrences remain backend-owned and are not fabricated by C1;
- Planning Tray one-card drag/no-scrim behavior and Event Agenda/all-day v2 are already implemented;
- a possible simple-only left pin/dock is only a future idea, not implemented authority.

## Current authority

Read instead:

1. `temporal-live-status.md`;
2. `temporal-create-c1-manual-findings-2026-09-04.md`;
3. `temporal-create-handoff.md`;
4. `temporal-create-c1-scope-amendment.md`;
5. `temporal-create-c1-traceability.md`;
6. `temporal-frontend-roadmap.md`.

Historical implementation SHAs and CI runs from 2026-09-03 remain useful for archaeology only. Current branch/checkpoint status belongs in `temporal-live-status.md`.
