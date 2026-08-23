# Workstream Handoffs

Each active or pending-integration workstream has one operational handoff. It is the safest continuation entry point for that scope.

## Current / pending-integration workstreams

- [`frontend-materialization-integration.md`](frontend-materialization-integration.md) — **ACTIVE / PR #28**; integrates the already-closed frontend materialization into current `main`, owns integration hardening, Dependency Review accepted-risk lifecycle, Frontend CI Gate calibration and the durable future-activation register.
- [`today-home.md`](today-home.md) — separate Phase-4 Home/Today UX/product-structure workstream; prototype/UX authority only, not production engineering authority.

## Completed / integrated or closed evidence workstreams

- [`frontend-materialization.md`](frontend-materialization.md) — **CLOSED / PASS — FM-00..FM-07 COMPLETE AT THEIR STATED SCOPES**; direct Web/Mobile/tooling/shared-package/CI/fresh-materialization evidence. The closed branch is evidence source, not the current integration work branch.
- [`backend-scaffold.md`](backend-scaffold.md) — **CLOSED / DIRECT QA PASS / integrated via PR #24**; CP1-CP5 backend scaffold evidence and protected-main integration record.
- [`frontend-foundation.md`](frontend-foundation.md) — **DESIGN / ARCHITECTURE CLOSED / ACCEPTED / FINAL REVIEW PASS / integrated via PR #22**.
- [`engineering-foundation.md`](engineering-foundation.md) — **CLOSED / ACCEPTED / FINAL REVIEW PASS / integrated via PR #21**.
- [`physical-model.md`](physical-model.md) — **TARGET ARCHITECTURE CLOSED / SELECTED / ACCEPTED / integrated via PR #15**; specialist activation/direct validation remains capability-triggered.
- [`pre-physical-coherence.md`](pre-physical-coherence.md) — **DEFINITIVE CLOSED / FINAL QA PASS / integrated via PR #13 / post-merge aligned via PR #14**.
- [`domain-model.md`](domain-model.md) and continuations — historical operational record for CLOSED Domain Model integrated via PR #10.
- Logical Model workstream documents/continuations — historical operational record for CLOSED Logical Model integrated via PR #11.

## Historical / superseded planning handoffs

- [`backend-foundation.md`](backend-foundation.md) — historical pre-Engineering-Foundation planning; not current implementation authority.

## Current carry-forward rule

```text
PHYSICAL TARGET              CLOSED / ACCEPTED
ENGINEERING FOUNDATION v0    CLOSED / ACCEPTED
FRONTEND FOUNDATION          CLOSED / ACCEPTED / integrated
BACKEND SCAFFOLD             CLOSED / DIRECT QA PASS / integrated
FRONTEND MATERIALIZATION     CLOSED / PASS
FRONTEND PR #28              ACTIVE integration hardening
SELECTED != IMPLEMENTED
SELECTED != DIRECT PASS
```

Version-sensitive claims require current evidence. Later direct materialization evidence qualifies older design-time version wording without reopening unrelated architecture.

Current examples:

```text
Temporal implementation      temporal-polyfill 1.0.4
Gesture Handler              2.32.0 under Expo SDK 57
Web E2E path                 apps/web/e2e/
```

## Operational rule

`main` remains integrated authority. Newer unmerged branch truth is bounded to its active workstream until merge.

Before continuation:

1. read development operating/safety rules;
2. verify exact Git relation/PRE-SCOPE;
3. read the complete active handoff;
4. consume applicable closed model/Foundation/ADR authorities;
5. distinguish selected/installed/configured/directly validated states;
6. update the active handoff on every substantive slice.

## Frontend continuation

Do not reopen general stack/architecture selection by default.

Current sequence:

```text
PR #28 current-truth reconciliation
-> PR CI green
-> Frontend CI Gate deliberate-red calibration
-> recovery green
-> optional separate required-check promotion
-> final protected-main merge review
```

The future-activation register in `frontend-materialization-integration.md` must be consulted when the first real vertical/UI/form/API/offline/deployment/release/security/pre-PROD/scale trigger occurs.

Durable architecture changes belong in current specs/ADRs, not only handoff text. Historical sources never override later current truth.