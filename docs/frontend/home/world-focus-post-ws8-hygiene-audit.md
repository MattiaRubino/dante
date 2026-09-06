# DANTE — World Focus Post-WS8 Coherence / Hygiene Audit

**Status:** CLOSED / APPLIED — LOCAL POST-CLOSURE HYGIENE + PRE-M0 REGRESSION HARDENING, WS0–WS8 NOT REOPENED  
**Date:** 2026-09-02  
**Branch:** `feature/home-react`  
**Initial pre-scope:** `7b1a862e02475f9ecb8efcfb1111a9eca526a827`

This audit answered a different question from substrate convergence:

> Does the repository still contain stale live routing, runtime-local lifecycle bugs, orphaned scaffolding or superseded implementation residue that contradicts the state we claim?

It did not replace WS8 falsification evidence. A final red-first pre-M0 gate was then added to attack the cleaned runtime boundary before M0 was allowed to start.

---

## 1. Scope reviewed

```text
branch-level current checkpoint / handoff
World Focus current checkpoint / evidence map
WS7 executable harness evidence
WS8 stateful + mutation + confirmation evidence
World Focus model/application/UI ownership
route-backed Home -> World Focus entry
finite module/surface registries
workspace reducer/allocation contracts
D1 contextual DANTE entry boundary
visual frame / WebGL candidate residue
explicit deprecated frontend debt
Home/AppShell cross-owner residue found during coherence review
```

The audit distinguished:

```text
semantic/substrate contradiction
runtime-local bug
live-authority documentation drift
orphaned/premature scaffold
superseded dead implementation residue
cross-workstream deprecated debt
```

---

## 2. Closure result

The WS0–WS8 substrate closure still holds.

No evidence required:

```text
new L1 primitive
new World ownership layer
new generic root
page-per-World architecture
AI-required basic World path
new Domain/Logical/Physical interpretation
new privacy/disclosure architecture
new backend owner
```

Therefore WS0–WS8 were not reopened.

---

## 3. Findings HYG-01..HYG-07

### HYG-01 — unknown popover fallback pointer barrier — FIXED

An unregistered `popover` fallback could become a full-area physical click barrier even though the allocation contract considered the main World interactive.

Fix preserved pointer-transparent overlay behavior while keeping the local dismiss control interactive. Regression coverage was added.

### HYG-02 — unused persisted motion preference — REMOVED

The exported/localStorage `immersive | instant` scaffold had no active runtime consumer. It and its tests/exports were removed. The real WebGL renderer continues to honor `prefers-reduced-motion` independently.

### HYG-03 / HYG-04 — superseded visual residue — REMOVED

Removed V2/V3 visual-frame CSS and dead SVG corona/halo/thread/orbit/particle styling no longer emitted by the active V4 candidate renderer. WF0/WF-G3 remained untouched.

### HYG-05 — stale live branch routing — FIXED

Branch-level live docs still pointed to `D2 NEXT` while World Focus authority had moved through WS8. Live routing was synchronized.

### HYG-06 — World switch retained stale route-entry provenance — FIXED

A reused `WorldFocusPage` instance could retain an older World's transient entry provenance/close policy. Entry resolution was rebound to `world.id + source` and a rerender regression test added.

### HYG-07 — Global Topbar Review owner cleanup — REMOVED

The disabled legacy Review control, fake badge `3`, unused icon/CSS/i18n and open-decision/registry residue were removed by the AppShell/Home owner. No replacement global Review workflow was invented and Context Rail Resolution was not promoted into the Topbar.

---

## 4. HYG-08 — transient route-handoff resurrection

### Discovery method

Immediately before M0, an independent red-first falsification file was introduced:

```text
apps/web/src/features/world-focus/model/world-focus-pre-m0-falsification.test.ts
```

It attacked the actual transient route handoff with five lifecycle cases rather than replaying WS7/WS8 substrate vectors.

Test-only discovery commit:

```text
798170e0c1ad12e0263364ab5c542a6ffe3d5e06
```

Quality reached unit tests and reported:

```text
new falsification file: 5 tests
2 failed / 3 passed
whole web suite: 2 failed / 227 passed
```

The two failures were both stale-handoff resurrection attacks.

### Root cause

`readWorldFocusEntry(worldId, source)` returned `null` on a World/source mismatch but retained the pending entry.

Therefore:

```text
prime music/home
-> read travel/worlds (mismatch => null)
-> old music/home handoff still pending
-> later read music/home within TTL
-> stale opener origin resurrected
```

The same problem existed for a same-World/different-source mismatch.

### Fix

Mismatch is now terminal for the pending transient handoff:

```text
worldId/source mismatch
-> pendingEntry = null
-> return null
```

Fix HEAD:

```text
7c9feab50c6e2a04a9a3b1e36c92958362dba704
```

The adversarial test was not modified.

Validation:

```text
Frontend CI 33664655614 — PASS
```

Passed:

```text
contract drift
format/lint/typecheck
architecture/generated-source checks
unit tests
production build
diff/repository-mutation checks
Mobile Bundle
Chromium Web E2E
Firefox frozen Timeline contract
Frontend CI Gate
```

Classification:

```text
runtime-local transient route lifecycle bug
new substrate class        NO
WS0–WS8 reopen             NO
backend owner              NO
```

Detailed authority:

`world-focus-pre-m0-falsification-review.md`

---

## 5. Evidence truth

Semantic WS8 closure evidence remains:

```text
HEAD 88db899391a3a41e23e76177d4896a657232b5eb
Frontend CI 33639741630 PASS — attempt 1
```

Later hygiene/falsification evidence is separate branch-state validation and does not rewrite that historical proof point.

Pre-M0 final regression evidence:

```text
RED discovery commit 798170e0c1ad12e0263364ab5c542a6ffe3d5e06
FIX HEAD             7c9feab50c6e2a04a9a3b1e36c92958362dba704
FIX CI               33664655614 PASS
```

---

## 6. Final disposition

```text
WS0–WS8 semantic/substrate closure        HOLDS
HYG-01 unknown-popover pointer barrier    FIXED
HYG-02 orphaned motion preference         REMOVED
HYG-03 V2/V3 visual CSS                   REMOVED
HYG-04 legacy SVG visual CSS              REMOVED
HYG-05 stale live D2 routing              FIXED
HYG-06 stale World-switch provenance      FIXED
HYG-07 Global Topbar Review debt          REMOVED
HYG-08 transient handoff resurrection     FIXED + ADVERSARIAL REGRESSION
PRE-M0 falsification                      CLOSED / PASS
M0                                        ACTIVE
M1–M7                                     BLOCKED UNTIL M0 CLOSES
backend                                   NOT STARTED
```

The repository is materially more coherent without manufacturing new product capability or changing closed substrate semantics.
