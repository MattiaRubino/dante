# DANTE — Temporal Create C1 Manual Findings — 2026-09-02

**Status:** SUPERSEDED HISTORICAL MANUAL FINDINGS  
**Branch:** `feature/home-timeline`  
**Historical automated-green descendant before this review:** `9abc891f21a4166859617bb6211e0a23ca6dd36e` / Frontend CI #539 FULL PASS  
**Superseded for current product decisions:** by the 2026-09-03 and especially 2026-09-04 findings/live status.

This file is preserved for archaeology. It must not override later product decisions. In particular, the old centered/maximized Full/Advanced target was later superseded by the 2026-09-04 floating/non-modal decision.

## 1. Historical findings

### M1 — Newly created timed items were visually present but interaction-inert

The review found that accepted Create projections visually resembled Timeline cards while bypassing the frozen T1 interaction grammar. The required correction was to materialize accepted items through the normal Timeline interaction path rather than duplicating drag/edit behavior in a Create-only portal.

This was subsequently addressed by native Timeline materialization/identity-based Undo integration.

### M2 — Context selector was fixture-derived

The review required a truthful local Context authoring/presentation boundary rather than treating fixture labels as canonical domain ownership. Context and appearance must remain separate.

### M3 — Full editor spatial model was rejected

The then-current right-side drawer was rejected. A centered/maximized replacement was proposed at this historical stage, but **that proposal itself was later superseded on 2026-09-04** by the current larger floating/non-modal Advanced direction.

### M4 — Back navigation was not discoverable

Long/deep authoring required a persistent reachable way back without draft loss. Current Advanced retains a reachable return-to-simple path.

### M5 — Appearance depth was insufficient

The review required presentation-owned tone/appearance metadata without polluting domain semantics.

### M6 — Neighboring-product benchmarking was required

Create patterns were re-audited against mature calendar/task/planning products while retaining DANTE-specific semantic distinctions.

### M7 — Simple authoring needed spatial freedom

The user needed to move the desktop Create surface to inspect Timeline underneath. Current simple Create is floating/draggable and Timeline remains interactive.

## 2. Durable guardrails

- manual Create remains separate from AI/NLP/voice;
- direct Activity-owned recurrence remains forbidden; current user-facing Activity Repeat is Routine-backed;
- Event recurrence retains the four CP6 families;
- no API/DB/provider success is faked;
- accepted items use normal interactive Timeline paths;
- Domain/Logical closure is not reopened for visual convenience;
- Context/appearance remain explicit presentation/application boundaries until owned backend semantics exist.

## 3. Current authority

Read current truth in:

1. `temporal-live-status.md`;
2. `temporal-create-c1-manual-findings-2026-09-04.md`;
3. `temporal-create-handoff.md`;
4. `temporal-create-c1-scope-amendment.md`;
5. `temporal-create-c1-traceability.md`;
6. `temporal-frontend-roadmap.md`.

C1 remains open until explicit final manual approval.
