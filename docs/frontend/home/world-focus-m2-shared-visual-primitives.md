# DANTE — World Focus M2 Shared Visual Primitive Layer

**Status:** M2 ACTIVE / M2-1 CLOSED / VALIDATED  
**Date:** 2026-09-03  
**Branch:** `feature/home-react`

This document is the bounded engineering record for M2. It does not replace the World Focus product/platform/structural contracts and it does not advance sequencing beyond evidence actually observed.

## 1. Scope

M2 renders semantics already earned by M1. It does not redefine semantic ownership.

Binding rules:

```text
primitive != card
renderer != semantic owner
Output Grammar family != mandatory visible module
reference key != display copy
responsive presentation != semantic rewrite
unknown/missing != false/zero
Comparison != Decision/winner/recommendation
Trajectory != fabricated chart/progress
reasonCode != user-facing explanation
```

Out of scope:

```text
M3 candidate resolution/customization/pin/hide/reorder
D2–D6 contextual DANTE
complete World composition
backend/API/DB/Alembic/AuthZ/provider runtime
real effects or model execution
Timeline/AppShell/Access collateral changes
```

## 2. M2-1 materialized owners

Shared presentation boundary:

```text
apps/web/src/features/world-focus/ui/presentation/
  world-focus-display-bindings.ts
  world-focus-presentation-primitives.tsx
  world-focus-presentation.css
```

Finite M1 work-semantic renderers:

```text
WP-02 Attention   -> world-focus-attention.tsx
WP-03 Comparison  -> world-focus-comparison.tsx
WP-04 Trajectory  -> world-focus-trajectory.tsx
```

Existing WP-01 Continuity is the real production vertical migrated onto the same presentation grammar:

```text
apps/web/src/features/world-focus/ui/world-focus-continuity.tsx
```

WP-02..WP-04 are deliberately not inserted into live World composition merely to demonstrate the renderers. Their unit tests exercise the real M1 semantic primitives directly and require exact display bindings.

## 3. Display binding boundary

`WorldFocusDisplayBinding` is presentation-only and must match the authoritative M1 `WorldFocusContextReference` it claims to render.

The boundary reconstructs bounded display-safe copy rather than treating semantic reference keys as labels.

Required behavior:

```text
exact reference match or fail closed
blank/invalid display labels rejected
internal reference keys never become fallback user copy
reasonCode remains non-display metadata
renderer cannot silently reorder semantic references
```

This keeps identity/reference ownership in M1 and presentation ownership in M2.

## 4. Shared presentation grammar

The shared layer provides semantic section/state structure and common styling only. It is not a universal `Card<T>` or data-driven widget engine.

Properties:

```text
semantic section heading ownership
textual state presentation
existing DANTE design tokens only
responsive/container-query adaptation
forced-colors support
no new UI library or second design system
```

The CSS is owned by the shared presentation primitive layer, not by Continuity, so future registered renderers do not depend on WP-01 mounting first.

## 5. Renderer contracts

### WP-02 Attention

Renders bounded display-safe matter/reason/resolution/state without exposing reference keys or `reasonCode`.

It does not manufacture urgency, notification semantics or authorization state.

### WP-03 Comparison

Preserves the semantic subject order and optional basis reference.

It does not infer:

```text
winner
ranking
recommendation
causality
Decision
```

A binding reorder relative to the semantic primitive fails closed.

### WP-04 Trajectory

Preserves subject, ordered known points, explicit missing positions, ordering basis and aggregation basis.

Missingness is rendered separately from known values:

```text
missing != zero
missing != false
missing != inferred value
```

The base renderer does not fabricate a chart merely because the primitive is Trajectory.

## 6. WP-01 Continuity vertical integration

Continuity retains its existing application/runtime behavior:

```text
same reader
same latest-read/cancellation protection
same ready/partial/stale/unavailable/error behavior
same sparse empty behavior
same no-fake-Resume rule
same World binding
```

Only its visual structure is migrated to the shared M2 presentation grammar.

This proves M2 is not an isolated showcase layer.

## 7. Localization

Finite visual labels are localized through the existing `@dante/i18n` resources for English and Italian.

Examples include finite renderer labels such as Attention state, Comparison mode, Trajectory axis/missingness and section copy.

Internal reference keys and `reasonCode` are not translated into user copy as an accidental fallback.

## 8. Red-first and correction evidence

The M2 tests were committed before the production owners. The observed red failed because the new presentation owners were unresolved, establishing a real red-first boundary.

```text
red HEAD 26adf872...
CI       33763229784 EXPECTED FAILURE
failure  Quality / Lint — unresolved M2 owners
```

Two later implementation failures were preserved and fixed at root cause:

```text
TypeScript 6 / noUncheckedIndexedAccess
  -> explicit fail-closed guards for indexed semantic references

isolated renderer test i18n environment
  -> initialize the real i18n instance in test harness
  -> semantic expectations unchanged
```

No hostile/semantic expectation was weakened.

## 9. Validated code baseline

Production baseline after the implementation fixes:

```text
HEAD 5e8aaba2477803e931a3394d90bbf01ff534f673
CI   33765049842 PASS

Frontend CI Gate  PASS
Quality           PASS
Web E2E           PASS
Mobile Bundle     PASS
Timeline Firefox  PASS

web test files    61 / 61 PASS
web unit tests    312 / 312 PASS
architecture      262 modules / 684 dependencies / 0 violations
generated         112 tokens / 3 deterministic files
```

## 10. Responsive pressure gate — VALIDATED

The real-browser pressure test was introduced at:

```text
HEAD b1504ed6c1587204cfb6fa7900c66109909201b0
```

Its first run was superseded operationally by the subsequent documentation commit while the same pressure test remained unchanged in the branch. The authoritative validation is therefore the later complete run:

```text
VALIDATED HEAD 2e639f108d5cb01e53395013a55346b7ac2e4294
CI             33781753823 PASS

Frontend CI Gate       PASS
Quality                PASS
Web E2E / Chromium     PASS
frozen Timeline Firefox PASS
Mobile Bundle          PASS
```

The E2E vertical checks Continuity inside the real World workspace at:

```text
720 px
719 px
390 px
```

For every pressure width it requires:

```text
shared M2 presentation marker present
Continuity remains inside workspace horizontal bounds
no document horizontal overflow
```

The same authoritative run confirms:

```text
web test files 61 / 61 PASS
web unit tests 312 / 312 PASS
architecture   262 modules / 684 dependencies / 0 violations
generated      112 tokens / 3 deterministic files
production build PASS
repository mutation check PASS
```

## 11. M2-1 closure result

M2-1 is closed only for the bounded layer materialized here:

```text
display-safe reference binding boundary
shared semantic presentation section/state grammar
WP-02 Attention renderer contract
WP-03 Comparison renderer contract
WP-04 Trajectory renderer contract
WP-01 Continuity migrated as a real production vertical
English/Italian finite presentation labels
responsive 720/719/390 pressure evidence
forced-colors presentation support
```

This does **not** mean all of M2 is closed. WP-02..WP-04 being available renderers does not mean they have been selected into a live World composition. That selection/composition work must remain evidence-driven and cannot be fabricated merely to exercise the components.

## 12. Current sequencing

```text
M1 + POST-M1 safety             CLOSED / VALIDATED
M2                              ACTIVE
M2-1 shared presentation layer  CLOSED / VALIDATED
M2 remaining visual work        NEXT WITHIN M2
M3                              BLOCKED BY M2
M4 D2–D6                        BLOCKED BY M3
M5                              BLOCKED BY M4
M6                              BLOCKED BY M5
M7                              BLOCKED BY M6
BACKEND                         BLOCKED UNTIL M7
```

Human/manual visual acceptance is not claimed by automated green. Integrated human visual/a11y/performance acceptance remains later sequencing work, especially M6.
