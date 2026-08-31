# DANTE — Whole Home Structural Contract H0

**Status:** **FROZEN — USER-AUTHORIZED STRUCTURAL BASELINE**  
**Date:** 2026-08-31  
**Branch:** `feature/home-react`  
**Pre-scope HEAD:** `eaa835ab075ef4906d5f33f0a578f8a2b63e469d`  
**Scope:** Home macro-composition, region ownership, structural responsive modes and cross-region invariants  
**Out of scope:** redesign of any Home surface, Timeline internals, World Focus internals, backend/API semantics, feature-specific visual polish

This contract turns the already accepted Home macro-layout into an explicit change-control boundary. It exists to make structural regressions fail loudly instead of being discovered later while working on a child feature.

It does **not** freeze incidental DOM shape or every CSS value. Internal refactors remain allowed when they preserve the observable structural contract and all regression guards remain green.

---

## 1. Change-control rule

The Home structural baseline is frozen.

A change requires **explicit user approval before the first production write** when it intentionally changes any of the following:

- region presence or removal;
- region parent/ownership;
- macro order or hierarchy;
- wide/compressed/compact composition mode;
- structural breakpoint ownership;
- whether two regions are side-by-side versus stacked;
- whether a region participates in Home geometry;
- cross-region expansion/collapse behavior;
- the relationship between Home and the shared AppShell;
- the rule that a child surface may not redefine geometry owned by its parent.

Regression guards protecting this contract must not be weakened, deleted, skipped or rewritten merely to make accidental drift pass.

A bug fix or internal refactor may proceed without reopening H0 only if the observable structural contract remains equivalent.

---

## 2. Authority hierarchy

When documents or implementation details disagree, use this precedence for Home macro structure:

```text
1. this Whole Home Structural Contract
2. machine-readable home-structure.contract.json
3. machine-readable home-shell-responsive.matrix.json
4. accepted surface contracts / UI registry
5. current React implementation
6. historical prototype/reference material
```

Feature-specific contracts remain authoritative **inside** their owned region. They may not silently redefine this Home-level hierarchy.

The shared Global AppShell/Topbar remains outside Home feature ownership and keeps its own contract.

---

## 3. Frozen ownership tree

```text
APP SHELL / GLOBAL TOPBAR                  owner: app-shell
└── ROUTE OUTLET
    └── HOME                               owner: home.shell
        ├── HERO                           owner: home.shell
        │   ├── DAY CONTEXT / DAY ROUTE   owner: home.dayContext
        │   └── HERO BODY                 owner: home.shell
        │       ├── AI SURFACE             owner: home.aiSurface
        │       └── UPPER WORKSPACE        owner: home.shell
        │           ├── ORIENTATION        owner: home.orientation
        │           │   ├── Ora / Prossimo
        │           │   ├── In evidenza
        │           │   └── Per te
        │           └── CENTRAL STAGE      owner: home.stage
        │               ├── Mondi
        │               └── Segnali
        └── TODAY WORKSPACE                owner: home.shell
            ├── TIMELINE                   owner: home.timeline
            └── CONTEXT RAIL               owner: home.contextRail
                ├── Capture
                └── Resolution
```

### Permanent ownership consequences

- AppShell/Topbar may frame Home but is not a child Home component and must not be reimplemented inside Home.
- `home.shell` owns macro composition between Day Context, AI, Upper Workspace, Timeline and Context Rail.
- `home.upperWorkspace` owns the relationship between Orientation and Central Stage.
- `home.stage` owns its own outer geometry; Mondi/Segnali own only inner projection layout.
- `home.timeline` owns Timeline internals but may not move/restructure unrelated Home regions.
- `home.contextRail` is a sibling of Timeline inside the Today workspace, not a child of Timeline.
- Capture and Resolution are two responsibilities inside one Context Rail capability; they must not become independent floating Home regions without an approved contract change.

---

## 4. Frozen macro responsibilities

### Day Context / Day Route

Owns environmental/current-day context and the accepted day-route presentation. It does not become a second global navigation bar and does not own the geometry of AI, Orientation, Stage or Today workspace.

### AI Surface

Owns conversational interaction. Expanded/collapsed state may reallocate **its approved Home-shell share** but must not change the semantic identity or ownership of other Home regions.

### Orientation

Owns the distinct current-situation responsibilities:

- Ora / Prossimo;
- In evidenza;
- Per te.

Content/name refinement inside a future bounded pass is allowed where already marked WORKING, but collapsing these responsibilities into one generic feed is a structural/product change.

### Central Stage

Owns the shared read/navigate/open projection workspace. Mondi/Segnali mode changes may alter inner projection content but must not change Stage outer bounds or move unrelated Home regions.

### Timeline

Owns the primary temporal projection. H0 freezes only its place in Home and its relationship with Context Rail; Timeline internal controls/cards/temporal behavior are governed by Timeline-specific contracts.

### Context Rail

Owns the integrated secondary capability beside Timeline on wide desktop:

```text
USER -> DANTE     Capture
DANTE -> USER     Resolution
```

It must remain subordinate to the Today/Timeline workspace and must not become a generic notifications/dashboard/feed region.

---

## 5. Frozen structural state transitions

### AI expanded ↔ collapsed

Allowed:

- HomeShell reallocates horizontal/upper-workspace space according to the approved responsive mode;
- Central Stage and Orientation adapt to the real container they receive.

Required:

- round-trip expand → collapse → expand is geometrically reversible within normal rendering tolerance;
- Timeline/Context Rail ownership remains unchanged;
- Stage mode semantics remain unchanged;
- no duplicate responsive implementation per Stage projection.

Forbidden:

- a child projection changing Home-shell columns;
- permanent geometry drift after the round trip;
- moving Timeline into the hero/upper workspace.

### Central Stage mode change

Allowed:

- inner Mondi/Segnali rendering changes.

Required:

- same Stage outer bounding box for the same Home state;
- same Stage selector/navigation ownership;
- no movement of AI, Orientation, Timeline or Context Rail caused solely by mode switch.

### Timeline normal ↔ expanded

Allowed on widths where the expansion control exists:

- Context Rail yields its Today-workspace width;
- Timeline consumes that released Today-workspace width.

Required:

- Hero/Day Context/AI/Orientation/Central Stage geometry is not reauthored by Timeline expansion;
- Context Rail remains the same capability rather than being reparented into Timeline;
- returning to normal restores the previous macro composition.

### World Focus entry

Opening a World is a route transition to the World Focus surface. World Focus must not be implemented as a Home overlay that redefines Home macro geometry.

---

## 6. Responsive structural modes

The Home uses **structural modes**, not per-component viewport improvisation.

### H0-WIDE — width >= 1121 px

Macro contract:

```text
Hero:
AI Surface  |  Upper Workspace

Today:
Timeline    |  Context Rail
```

Required:

- Context Rail participates in the visible Today layout;
- Timeline expansion may make the rail yield;
- AI expanded/collapsed remains a HomeShell-owned composition change;
- no unexpected horizontal page overflow.

### H0-COMPRESSED — 901–1120 px

Macro contract:

```text
Hero:
AI Surface  |  Upper Workspace

Today:
Timeline full available width
Context Rail not visible in this web composition
```

Required:

- Context Rail capability is **not deleted from the product model** merely because this web representation hides it;
- Timeline must not create a replacement ad-hoc rail implementation;
- Timeline expansion affordance that depends on a visible side rail is not required here;
- no unexpected horizontal page overflow.

A later approved compact representation of Capture/Resolution may replace the hidden state without reopening H0-WIDE.

### H0-COMPACT — width <= 900 px

Macro contract:

```text
Hero:
AI Surface
↓
Upper Workspace
    Orientation stacked
    ↓
    Central Stage

Today:
Timeline full available width
Context Rail not visible in this current web composition
```

Required:

- AI is above the Upper Workspace;
- Orientation becomes a vertical composition before Central Stage;
- Stage remains a distinct owned region;
- no unexpected horizontal page overflow;
- AppShell remains outside Home ownership.

The current compact web composition is a frontend representation, not a declaration that Capture/Resolution are desktop-only product capabilities.

---

## 7. Geometry anchors and tuning policy

The following current values are accepted **macro anchors** and are machine-readable in `home-structure.contract.json`:

- wide/compressed boundary: `1120 / 1121 px`;
- compressed/compact boundary: `900 / 901 px`;
- wide Context Rail nominal width: `306 px`;
- wide Today Timeline/Rail nominal gap: `16 px`;
- default Home outer inset: `34 px`;
- compressed Home outer inset used by the current implementation: `24 px`;
- desktop hero baseline height: `650 px`.

They are not permission to duplicate raw numbers across unrelated components.

The implementation may have secondary **tuning breakpoints** (currently 1240, 1180, 1100 and 980 px) for search/control density, AI width, world sizing or similar inner compression. These are implementation details as long as they do not create a fourth macro Home composition or violate H0-WIDE / H0-COMPRESSED / H0-COMPACT.

Changing a macro breakpoint or macro anchor enough to alter accepted regional proportions requires explicit change control. Small token-level polish that preserves the accepted visual geometry may be handled in a bounded visual scope with regression evidence.

---

## 8. Forbidden structural drift

The following must fail review/tests rather than silently ship:

- Home reintroduces its own GlobalTopbar;
- AI, Orientation, Central Stage, Timeline or Context Rail disappears from the React tree without an approved product change;
- Context Rail becomes a Timeline child;
- Orientation becomes a Central Stage child;
- Mondi/Segnali projection CSS changes Stage outer bounds;
- Timeline expansion moves/rebuilds the Hero;
- AI collapse permanently changes unrelated Today geometry;
- a new viewport-specific patch creates an undocumented macro composition;
- hidden compact functionality is treated as deleted product capability;
- a Stage item/add control participates in Home outer geometry;
- a World Focus visual is mounted over Home as the structural destination;
- accidental horizontal page overflow is introduced at contracted pressure widths;
- regression snapshots/contracts are updated merely because unintended drift occurred.

---

## 9. What remains intentionally open

H0 does **not** freeze backend/product semantics that are already deferred elsewhere, including:

- Global Create persistence/entities;
- remote/personal-data Search;
- real AI send/voice/attachment provider behavior;
- Timeline Quick Add command/persistence semantics;
- Capture persistence/upload/history integration;
- Resolution mutation/confirmation backend semantics;
- Mondi/Segnali management APIs;
- authenticated Access → AppShell handoff details;
- future compact/mobile representation of capabilities currently hidden by the web layout;
- microcopy/icons/microspacing that do not alter the structural contract.

Open feature semantics are not permission to change Home macro ownership.

---

## 10. Executable guards

H0 is protected by complementary layers:

### Q0 — machine-readable contract drift

- `prototypes/frontend/shared/contracts/home-structure.contract.json`
- `prototypes/frontend/shared/contracts/home-shell-responsive.matrix.json`
- `tests/prototypes/frontend-preprod-contracts.py`

These guard versioning, region ownership, structural breakpoints, state invariants and prohibited ownership collapse.

### Q1 — React structural ownership

`apps/web/src/features/home/ui/home-page.test.tsx` protects required Home regions in the real React tree and verifies that the Global AppShell is not Home-owned.

### Q2 — browser geometry / pressure widths

`apps/web/e2e/home-structure.spec.ts` protects:

- required regions at runtime;
- Topbar outside Home;
- no page horizontal overflow at pressure/boundary widths;
- H0-WIDE Timeline + Context Rail sibling geometry;
- H0-COMPRESSED full-width Timeline with hidden rail;
- H0-COMPACT AI/Upper Workspace stacking;
- AI collapse/expand reversibility at representative desktop widths.

These guards assert structural relationships, not incidental pixel-perfect child implementation.

---

## 11. Required gate for future Home structural changes

Any intentionally structural change must follow:

```text
explicit user approval
→ update H0 contract + machine contract deliberately
→ implementation
→ Q0/Q1/Q2 + relevant surface tests
→ production build / CI
→ user visual/manual validation
→ new accepted baseline
```

A green CI run without explicit approval does not authorize a structural redesign.

---

## 12. H0 closure meaning

Once H0 guards are green, child-surface work may continue one bounded production-depth pass at a time.

The working rule becomes:

> **Child features consume the Home skeleton; they do not renegotiate it.**

If later product learning genuinely requires a better Home skeleton, reopen H0 intentionally. Do not smuggle the redesign through a Timeline, AI, Mondi, Capture or responsive bug-fix commit.
