# DANTE — World Focus M2 Shared Visual Primitive Layer

**Status:** M2 CLOSED / VALIDATED — M2-1 + M2-2 + FINAL HOSTILE CLOSURE PASS  
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
label max 512 characters
supportingText max 2048 characters
oversize display copy rejected; never silently truncated
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

## 8. M2-1 red-first and correction evidence

The M2-1 tests were committed before the production owners. The observed red failed because the new presentation owners were unresolved, establishing a real red-first boundary.

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

## 9. M2-1 validated code baseline

Production baseline after the implementation fixes:

```text
HEAD 5e8aaba2477803e931a3394d90bbf01ff534f673
CI   33765049842 PASS
```

Authoritative validation after responsive pressure:

```text
VALIDATED HEAD 2e639f108d5cb01e53395013a55346b7ac2e4294
CI             33781753823 PASS

Frontend CI Gate        PASS
Quality                 PASS
Web E2E / Chromium      PASS
frozen Timeline Firefox PASS
Mobile Bundle           PASS
web test files          61 / 61 PASS
web unit tests          312 / 312 PASS
architecture            262 modules / 684 dependencies / 0 violations
generated               112 tokens / 3 deterministic files
```

## 10. Responsive pressure gate — VALIDATED

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

Shared CSS additionally owns compact container adaptation and forced-colors treatment. Automated green is not recorded as human visual acceptance.

## 11. M2-1 closure result

M2-1 is closed for:

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

WP-02..WP-04 being available renderers does not mean they have been selected into live World composition.

## 12. M2-2 — truthfulness + direct Output Grammar visual layer

M2-2 reuses M2-1 instead of introducing another UI grammar. It materializes the remaining shared presentation obligations already earned by M1/M0:

```text
shared qualifier grammar
  textual axis + finite state
  quiet nominal states
  no color-only meaning

L2 presentation
  freshness
  validity
  coverage
  material-payload retirement

L3 presentation
  sanitized disclosure available/restricted/unavailable

L6 presentation
  effect state
  execution revalidation as an orthogonal axis

L8 presentation
  connectivity
  replay
  provider delivery
  request timing

O2 Situation renderer
O5 Next renderer
O8 Evidence / History renderer
```

Truthfulness constraints remain explicit:

```text
stale != invalid
retracted != stale
incomplete != empty
conflicted != winner
retired payload != missing reference
available disclosure != frontend authorization
restricted != unavailable
offline != content absent
provider lag != stale
timeout != semantic negative
partial-real != failed
reversed != compensated
execution revalidation != effect state
Evidence != Provenance != integrity attestation
reasonCode != display copy
reference key != display copy
```

Nominal basis/disclosure/sync states remain visually quiet. The renderer does not manufacture badge density merely because a state exists in the model.

`WorldFocusPresentationSubsection` adds accessible nested role ownership for O8 Evidence/History without creating a generic card/container ontology.

WP-01 Continuity uses the same qualifier grammar for its already-existing degraded read states:

```text
partial -> coverage / incomplete presentation qualifier
stale   -> freshness / stale presentation qualifier
```

Situation/Next/Evidence-History remain renderer contracts only. They are **not inserted into the live core composition** merely because the renderers exist.

## 13. M2-2 red-first and validation evidence

Red-first owner proof:

```text
RED HEAD 5374f77d7cf7b52ef87ce64315a606bc1d96cf0b
CI       33787162755 EXPECTED FAILURE

Lint       PASS
Typecheck  FAIL
failure    exactly 8 TS2307 unresolved M2-2 presentation owners
```

The eight tests fixed the obligations before production implementation:

```text
qualifier state must be visible text, not color-only
nominal truthfulness axes stay quiet
degraded L2 axes remain separate
no reasonCode/material reference leakage
disclosure available stays quiet and is not AuthZ
effect + execution revalidation remain orthogonal
sync axes remain independent
O2/O5 preserve semantic order through exact display bindings
O8 keeps Evidence / Provenance / Integrity / History as separate roles
missing display binding fails closed
```

Initial production:

```text
HEAD 78633df2b3b1949d5d7b3bc4e7c9ee3e01ebc6bb
```

Static pressure found one narrow i18n typing issue in disclosure presentation. It was corrected with explicit finite branching rather than a cast/`any` or weakened test:

```text
FIX HEAD b9856d497273d22face94fcd14f0deda853bbdb8
CI       33787905171 PASS
```

Final integration-regression code head:

```text
VALIDATED HEAD 26d79b0dcdeaac1cb094bf97b71e901003ac5fa5
CI             33788370490 PASS

Frontend CI Gate        PASS
Quality                 PASS
Web E2E / Chromium      PASS
frozen Timeline Firefox PASS
Mobile Bundle           PASS
production build        PASS
repository mutation     PASS
```

The final regression explicitly proves that Continuity partial/stale map to the shared `coverage/incomplete` and `freshness/stale` qualifier axes and that `reasonCode` remains absent from user-facing DOM. It also verifies accessible subsection ownership for nested Evidence/History roles.

## 14. M0 disposition audit after M2-2

Every known M0 shared visual renderer disposition assigned to M2 has a production owner:

```text
M0-19 WP-02 shared rendering                  M2-1 DONE
M0-21 WP-03 shared rendering                  M2-1 DONE
M0-23 WP-04 shared rendering                  M2-1 DONE
M0-28 shared Evidence / History affordance    M2-2 DONE
M0-42 shared effect presentation              M2-2 DONE
M0-49 WP shared renderer family               M2-1 DONE

O2 Situation visual presentation              M2-2 DONE
O5 Next visual presentation                   M2-2 DONE
O8 Evidence / History visual presentation     M2-2 DONE
L2/L3/L6/L8 shared truthfulness presentation  M2-2 DONE
```

This allowed the next step to be closure falsification rather than invention of another generic visual family.

## 15. M2 final hostile closure — RED

Final test owner:

```text
apps/web/src/features/world-focus/ui/presentation/
  world-focus-m2-final-falsification.test.tsx
```

Red-first evidence:

```text
HEAD 3adbd958ee3e3bf2fd55b7d2a2562dd6de5aa011
CI   33790674375 EXPECTED FAILURE

hostile file  4 PASS / 1 FAIL
web suite     331 PASS / 1 FAIL
Lint          PASS
Typecheck     PASS
Architecture PASS
Generated     PASS
Mobile        PASS
Chromium      PASS
```

The five hostile cases attacked:

```text
simultaneous degraded L2/L3/L6/L8 axes + protected-detail non-leakage
pathological display-copy bounds
unknown-future World through O2/O5/O8 + semantic order/role separation
convincing label bound to wrong semantic reference
combined nominal-state quietness
```

Four passed immediately. The sole failure was precise:

> The presentation boundary claimed bounded display-safe copy, but `createWorldFocusDisplayBinding()` accepted a 100,000-character label/supporting text.

No semantic-axis collapse, future-World failure, binding mismatch bug, reasonCode leakage or fake nominal density was found.

## 16. M2 final hostile closure — FIX / PASS

The hostile test was left unchanged. Only its existing direct owner was hardened:

```text
apps/web/src/features/world-focus/ui/presentation/world-focus-display-bindings.ts
```

Final bounds:

```text
label            <= 512 characters
supportingText   <= 2048 characters
blank            rejected
oversize         rejected
truncation       none
```

Final code evidence:

```text
HEAD e3865e0cde095acae7e3022815538f35ee0706ef
CI   33790953644 PASS

M2 hostile tests          5 / 5 PASS
web test files            70 / 70 PASS
web unit tests            332 / 332 PASS
architecture              279 modules / 770 dependencies / 0 violations
generated                 112 tokens / 3 deterministic files
Quality                   PASS
Mobile Bundle             PASS
Web E2E / Chromium        PASS
frozen Timeline Firefox   PASS
Frontend CI Gate          PASS
production build          PASS
repository mutation       PASS
```

Repository inspection also confirmed that the live core composition still mounts only Continuity; Situation/Next/Evidence-History and WP-02..04 were not injected merely to demonstrate renderer availability.

## 17. M2 closure disposition

M2 is **CLOSED / VALIDATED**.

Closure is justified by the combination of:

```text
all known frozen M0 M2 visual dispositions have owners
M2-1 responsive + forced-colors presentation foundation validated
M2-2 truthfulness/direct-output owners validated
final cross-axis/future-World/fail-closed/non-leakage/quietness hostile pressure validated
pathological copy gap found red-first and fixed under the existing owner
no fake live renderer mounting
no universal Card<T>/ProjectionEnvelope/page-per-World architecture
no M3 candidate/customization work pulled forward
no D2–D6 or backend authority pulled forward
```

Human/manual visual acceptance is still **not claimed**. Integrated human visual/a11y/performance acceptance remains later sequencing work, especially M6.

## 18. Current sequencing

```text
M1 + POST-M1 safety             CLOSED / VALIDATED
M2                              CLOSED / VALIDATED
M2-1 shared presentation layer  CLOSED / VALIDATED
M2-2 truthfulness/direct output CLOSED / VALIDATED
M2 final hostile closure        CLOSED / PASS
M3 Adaptive World Composition   NEXT
M4 D2–D6                        BLOCKED BY M3
M5                              BLOCKED BY M4
M6                              BLOCKED BY M5
M7                              BLOCKED BY M6
BACKEND                         BLOCKED UNTIL M7
```

M3 is not started by this document. A fresh bounded M3 gate requires explicit authorization.
