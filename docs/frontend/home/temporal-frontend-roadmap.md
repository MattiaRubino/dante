# DANTE — Temporal Frontend Production-Depth Roadmap

**Status:** ACTIVE AUTHORITY — C1 MANUAL UX ITERATION / C2 BLOCKED  
**Reconciled:** 2026-09-04  
**Workstream:** `feature/home-timeline`  
**Worktree:** `/home/mattia/projects/dante-timeline`  
**Integration target:** `feature/home-react`  
**F0 closed:** `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`  
**Current code checkpoint:** `1e7b7752b69f006a4b632e2e2d3ef1522d30e95e`  
**Checkpoint CI:** #937 / `33905239085` — FULL GREEN

## 1. Frozen foundations

### H0 — FROZEN

Whole Home macro structure/breakpoints.

### T1 — FROZEN

Timeline engine behavior: continuous temporal window, semantic anchor, Now, zoom, density/overlap, custom drag/focus, time edit, move/Undo, expanded group geometry and Firefox regression contract.

### F0 — CLOSED/FROZEN

Typed temporal application seam: commands/results/queries, Clock, deterministic local adapter, placement semantics, operation IDs/idempotency, revisions, guarded Undo, subscriptions, no fake network/storage.

## 2. C1 — Manual Temporal Create

**Current state: OPEN.** Automated candidate is green, but product/manual refinement is still active.

### Completed foundation

- title-first Create;
- Activity/Event actionable type registry;
- timed/all-day/unplaced Activity semantics;
- timed/all-day Event semantics;
- Context and appearance remain distinct;
- base + Advanced disclosure;
- conditional execution/session controls;
- Event Agenda/internal parts;
- Planning Tray v2;
- per-day all-day v2;
- Event recurrence;
- user-facing Activity repeat represented as Routine-backed recurrence intent;
- recurrence ownership explicit;
- no browser canonical Occurrence generation;
- `Personalizzata…` recurrence entry integrated into `Ripeti`;
- simple Create floating/draggable on desktop;
- Advanced larger floating surface;
- Home/Timeline remains interactive while Create is open;
- explicit dirty-draft close/discard behavior.

### C1-P — Manual product polish — ACTIVE

From this point, work **one issue at a time**. Do not package several UX ideas together.

Current candidate to inspect manually:

```text
click +
→ simple floating Create at stable position
→ Timeline remains usable/scrollable
→ simple panel can be moved
→ Advanced opens as larger floating depth
→ no modal-style Home freeze
```

A simple-only left pin/dock mode has been discussed as a possible later improvement. It is not implemented and must not be assumed as decided.

### Recurrence stop line during C1

Do not “fix” repeated Activity/Event by synthesizing canonical future cards in the browser.

Current C1 authors the recurrence rule. Future vertical/backend work owns:

```text
Routine/Event recurrence
→ recurrence evaluator/checkpoint
→ canonical Occurrences
→ temporal range query
→ Timeline projections
```

The current local UI may therefore show the authored first/master placement while the real recurring series remains a future integration concern.

### C1 closure

C1 closes only when:

1. remaining user-selected UX foundation issues are resolved one-by-one;
2. final automated gates are green;
3. the user performs one coherent final manual pass;
4. the user explicitly says `C1 MANUAL PASS — APPROVED`.

Until then C1 is not frozen.

## 3. C2 — Card → Structured Detail

**BLOCKED until C1 closes.**

Once unblocked, C2 should connect Timeline cards to structured detail/edit while consuming F0/C1/T1 contracts rather than reinterpret them.

No opportunistic C2 work while C1 remains manually open.

## 4. Timeline read-model/backend bridge — later vertical work

The existing Timeline engine should remain a consumer.

Target architecture:

```text
canonical temporal sources
Activity / Event / Routine / Occurrence / provider data
                    ↓
        backend/application range query
                    ↓
         normalized Timeline read-model
                    ↓
             Timeline engine
```

This future bridge should provide date/window queries, pagination/horizon semantics, provenance/source identity, reconciliation and authoritative recurrence outputs without coupling rendering to DB rows or source-specific SDKs.

## 5. Later temporal verticals

After C1/C2, sequence should be driven by owning vertical needs rather than frontend mimicry. Expected work includes:

1. real temporal API/adapter and range/window query;
2. Routine vertical + recurrence evaluator/materialization;
3. Event backend/provider integration where authorized;
4. Reminder/notification intent and real delivery boundary;
5. Session runtime;
6. Actual/outcome runtime;
7. multi-device reconciliation;
8. DANTE intelligence/AI/voice inputs through governed downstream operations.

Order may be refined when those verticals begin, but permanent semantic distinctions cannot be collapsed.

## 6. Permanent boundaries

```text
Activity != Event != Routine
Schedule != Occurrence != Session != Actual
planned != happened
recurrence rule != generated Occurrence
Context != appearance
manual Create != AI/NL/voice
Timeline ViewModel != application model != DTO != DB row
```

C1 remains pre-backend/manual. No fake provider, persistence, solver, recurrence materialization or notification success.

## 7. Immediate next step

Do not autonomously start a new feature.

The user should first test the current floating/non-modal Create foundation. The next implementation scope is whichever **single** UX issue the user chooses after that check.
