# DANTE — World Focus B1 Product Revision Checkpoint

**Status:** B1 PRODUCT REVISION IN PROGRESS — AUTOMATED GATES PENDING / USER ACCEPTANCE PENDING  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`  
**Authority:** `world-focus-product-contract.md`

## Revision purpose

B1 originally exposed a World-level temporal Lens before a concrete World output required it. WR0/WR1/WR2 demonstrated that this made a query mechanism visible before its product value was understandable.

The revision therefore applies the current Product Contract directly:

```text
first-open World
= orientation + truthful available product value
!= universal time filter
```

## Code disposition

The revision removes the unaccepted temporal Lens implementation rather than hiding dead infrastructure:

```text
visible segmented/select Lens        REMOVE
World fixture Lens capability        REMOVE
URL `time` parsing/navigation         REMOVE
Lens model/tests                      REMOVE
Lens-specific E2E                     REMOVE
Lens-only Session snapshot            REMOVE
```

The active World remains route-owned. A future World Session/cursor is reintroduced only when a real Continuity, Insight, Explore or other interaction needs transient cross-step context.

B1 retains and validates the visible Orientation capability:

```text
World identity
World title
concise description
frozen shell/workspace integration
entry/exit lifecycle
loading/error/unavailable behavior
responsive containment
accessibility
```

No B2 or later product vertical is authorized by this checkpoint. After automated gates pass, B1 still requires the normal user functional/visual acceptance gate.
