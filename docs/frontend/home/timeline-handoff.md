# DANTE — Timeline / Temporal Handoff

**Status:** CURRENT HANDOFF — T1 USER ACCEPTED / FROZEN  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`

Use this file when a new chat must continue the Timeline / temporal workstream without rediscovering accepted behavior.

## 1. Product thesis

DANTE temporal UX must preserve rich semantics while remaining operationally simple.

```text
rich temporal semantics underneath
-> progressive disclosure
-> simple user interaction
```

The product is not a generic calendar and must not collapse:

```text
Goal into Event/Session
Schedule into execution
planned into actual
recurrence source into one occurrence
proposal into accepted plan
provider acknowledgement into canonical completion
```

## 2. Surface model

The accepted direction contains at least:

```text
HOME TIMELINE
operational temporal lens

FULL TEMPORAL WORKSPACE
planning/management lens

SHARED CONTEXTUAL DETAIL
same underlying temporal reality where applicable

GLOBAL / CONTEXTUAL DANTE
alternative interaction entry into the same semantic operations
```

These surfaces may use purpose-built renderers. They must not create competing temporal semantics or stores.

## 3. Home Timeline T1 status

T1 is user accepted and frozen.

Frozen behavior is defined only by:

`docs/frontend/home/timeline-t1-frozen-contract.md`

Key protected interaction grammar:

- card body owns focus/select + custom drag;
- first drag gesture works even when another card is focused;
- clicking another card while one owns focus performs deselect-first;
- title/time/subitems keep explicit action semantics;
- drag does not fall back to browser-native behavior;
- completed drag does not trigger accidental post-drag focus behavior;
- Escape/cancel/visibility/window deactivation cleans up correctly;
- drag movement follows accepted move + undo grammar;
- expanded groups and compact overlaps preserve frozen geometry/alignment.

Do not alter these observables without explicit user approval.

## 4. Active temporal architecture

`temporal-experience-architecture.md` is the product/system architecture authority for future temporal work.

It establishes:

- Home Timeline + full-page temporal workspace as projections of one capability;
- progressive disclosure from card to deeper detail/resolution;
- shared semantic intents for manual/AI/future voice entry;
- planned vs actual preservation;
- flexible/unscheduled/candidate temporal realities;
- recurrence/occurrence distinctions;
- adaptive replanning with smallest valid scope;
- Contextual Detail as shared capability rather than a universal optional-field monster;
- backend/API stop line for the frontend phase.

## 5. Roadmap status

`temporal-frontend-roadmap.md` remains the current temporal planning roadmap.

Current sequencing state:

```text
T0   contract/scenario oracle       complete enough to support T1
T1   parity + interaction hardening FROZEN / USER ACCEPTED
T2   application core               next only when temporal workstream resumes
T3+  future pre-backend slices      not started
```

The roadmap is not permission to work on T2+ in parallel with the currently active World Focus workstream.

## 6. Engineering rules

- no component direct HTTP;
- no backend DTO/persistence leakage;
- no universal `Thing/Event` frontend collapse;
- no Home/full-page duplicate temporal state model;
- use `@dante/time` / current time abstractions rather than stringly ad-hoc dates;
- preserve keyboard/pointer parity;
- preserve undo/recovery where the accepted operation supports it;
- keep semantic state separate from visual convenience;
- do not fake persistence or provider success;
- use explicit ports/adapters only when a concrete vertical requires them.

## 7. Required gate for future work

For a future temporal mini-vertical:

```text
authority re-read
-> scenario pressure
-> architecture decision
-> full frontend implementation
-> type/lint/architecture/unit/build
-> browser/E2E + Firefox where pointer/focus relevant
-> manual/visual review
-> explicit user acceptance
-> freeze
```

## 8. Read order

1. `timeline-current-checkpoint.md`
2. `timeline-handoff.md`
3. `timeline-t1-frozen-contract.md`
4. `temporal-experience-architecture.md`
5. `temporal-frontend-roadmap.md`
6. relevant Home structural/product contracts
7. current implementation/tests

When semantic changes are proposed, also re-read the exact current Domain/Logical/Physical/Database and Intelligence/effect authorities affected by the change.
