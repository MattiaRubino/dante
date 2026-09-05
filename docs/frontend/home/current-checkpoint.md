# DANTE — Home / Temporal Current Checkpoint

**Status:** **PRE-PR INTEGRATION CANDIDATE / H0-T1-F0 FROZEN / C1 OPEN / C2 BLOCKED**  
**Reconciled:** 2026-09-05  
**Candidate branch:** `feature/home-timeline`  
**Current `main` integrated through:** `7bc7c0136cb5579528be1e2be0e71a6399004f90`  
**Pre-closure technical checkpoint:** `d8b1aa65d5d2651702bd790be3843234ad9f86da`  
**PR state:** NOT OPENED

This is the current navigation document for Home, AppShell, Timeline, Temporal Create and World Focus. Dated handoff files are retired pointers only. Durable contracts and current code/tests outrank historical branch instructions.

## 1. Integration state

`feature/home-timeline` has been reconciled with the current `main` baseline rather than rebased or rewritten.

The candidate contains current platform work from `main`, including the current PostgreSQL/backend/Auth/Recovery/Email/Observability/OpenAPI baseline, plus the Home/Temporal frontend workstream:

```text
current main platform
+
AppShell / Home
+
Timeline T1
+
Temporal F0
+
Temporal Create C1 candidate
+
World Focus pre-backend frontend
=
feature/home-timeline integration candidate
```

The generated TanStack route tree has been regenerated through the real Vite/TanStack generator after route reconciliation. Temporary diagnostic instrumentation used to recover that generated output is not present in the final tree.

No PR is created by this checkpoint. The next repository action is external/editor review of the candidate; PR creation remains a separate explicit action.

## 2. Authority / status matrix

### H0 — Whole Home structure

**FROZEN.**

Macro composition, ownership and responsive structural modes remain change-controlled by `home-structural-contract.md`.

### P1 — Global AppShell / Topbar

**FROZEN for accepted implementation scope.**

Shared AppShell ownership, route outlet, inline Search grammar, launcher/create/account shells and accepted visual baseline remain intact. Access `/` and `/security` continue to coexist with application routes without moving Auth semantics into Home.

The current AppShell account presentation is still intentionally neutral and is not yet bound to the full current Access/Auth session capability. Do not fake identity/logout just because the backend capability now exists.

### T1 — Timeline

**FROZEN.**

Preserve the accepted continuous temporal viewport, semantic anchoring, Now, zoom/density, custom focus/drag, first-gesture correctness, precise time edit, move + Undo, all-day geometry, expanded Context behavior and Firefox regression contract.

Timeline remains a consumer of normalized projections, not raw DB rows or provider SDK objects.

### F0 — Temporal application foundation

**CLOSED / FROZEN.**

Preserve typed temporal identities, placement forms, Clock, operation IDs/idempotency, revisions, stale-write rejection, guarded Undo, subscriptions and deterministic local adapter semantics.

F0 is not a fake backend. The future real adapter must replace the local adapter through the existing application seam.

### C1 — Manual Temporal Create

**OPEN.**

The implementation candidate includes the substantial C1 frontend foundation, including:

- title-first Activity/Event creation;
- timed/all-day/unplaced Activity placement;
- timed/all-day Event placement;
- Routine-backed user-facing Activity repeat;
- Event-owned recurrence;
- all four CP6 recurrence families in custom authoring;
- Planning Tray behavior for unplaced Activity;
- real per-day all-day lane behavior;
- Event Agenda/internal parts;
- simple floating/draggable desktop Create;
- larger floating Advanced surface;
- dirty-draft close/discard protection;
- Home/Timeline coexistence while Create is open.

C1 is **not frozen** and has **not** received the explicit final manual approval token:

`C1 MANUAL PASS — APPROVED`

Branch integration, automated green checks or a later PR merge do not manufacture that product approval.

### C2 — Card → Structured Detail

**BLOCKED until C1 closes.**

Do not start opportunistic C2 work merely because the branch is being integrated.

### World Focus

World Focus remains a real pre-backend frontend architecture/candidate, not permission to invent canonical World persistence or backend/API semantics.

Use `world-focus-architecture.md` and `world-focus-frontend-roadmap.md` for the durable pre-backend contract. Branch labels in the original 2026-08 records are provenance, not current operating instructions.

## 3. Temporal semantic stop lines

Permanent distinctions remain:

```text
Activity != Event != Routine
Schedule != Occurrence != Session != Actual
planned/intended != happened
recurrence specification != generated Occurrence
Context != appearance
manual Create != AI/NL/voice
Timeline ViewModel != application model != DTO != DB row
provider state != canonical DANTE state
```

Current C1 authors recurrence intent only. It must not synthesize canonical future Occurrences in browser state.

The future end-to-end bridge remains:

```text
canonical temporal sources
→ backend/application temporal range query
→ normalized Timeline projection
→ existing Timeline engine
```

## 4. Validation rule

Live validation authority is the current GitHub Actions state for the exact candidate HEAD. Historical run IDs in dated checkpoint documents are evidence only and must not be promoted to current truth after branch reconciliation.

The pre-closure technical checkpoint already demonstrated that the merged route set can pass frontend contract drift, lint, typecheck, architecture and generated-source checks after the real route-tree regeneration. Final review must still use the CI result attached to the final documentation-closure HEAD.

## 5. Current read order

For current work/review read:

1. `docs/frontend/README.md`
2. `docs/frontend/home/current-checkpoint.md`
3. `docs/frontend/home/home-structural-contract.md`
4. `docs/frontend/home/temporal-frontend-roadmap.md`
5. `docs/frontend/home/temporal-f0-contract.md`
6. `docs/frontend/home/timeline-t1-frozen-contract.md`
7. `docs/frontend/home/temporal-create-c1-manual-acceptance.md`
8. `docs/frontend/home/world-focus-architecture.md`
9. `docs/frontend/home/world-focus-frontend-roadmap.md`
10. `docs/frontend/open-decisions.md`
11. `docs/frontend/ui-registry.md`
12. current implementation/tests under `apps/web/` and shared packages.

For historical workstream context use `docs/archive/branches/2026-09-feature-home-timeline.md` and dated evidence documents only.

## 6. Immediate next action

Do not start a new feature from this checkpoint.

Sequence:

```text
final branch CI
→ editor/reviewer inspection
→ fix only concrete review findings if any
→ explicit user authorization for PR
→ PR to main
```

Stop before PR creation unless the user explicitly authorizes it.
