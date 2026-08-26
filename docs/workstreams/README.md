> **CURRENT MAIN + CP6 RECONCILIATION — 2026-08-26**
> Protected `main` anchor imported by this alignment is `87fe668c2ade78b17e0326d635e4d7a67920ae8a`. Its post-merge truth is preserved: frontend materialization/integration is **CLOSED / INTEGRATED via PR #28**, deterministic Frontend CI compatibility repair is integrated via PR #37, and the clean Home B2 v27 React handoff is integrated via PR #36. The main-only frontend contracts, fixtures, tokens and pre-production guard remain byte-identical to that protected-main anchor.
> Backend CP6 is independently **CLOSED / CONCRETE POSTGRESQL DATABASE PASS**. Accepted implementation HEAD is `22bbc078391d52c43665474bf465593d6225106e`; closure-documentation branch anchor before this alignment is `8c33c897ff57cfff9130fe00db1854470aa06bb5`; persistent LOCAL PostgreSQL 18.6 is at Alembic `20260826_08`; verified topology remains `68 tables / 5 views / 14 routines / 75 triggers / 95 indexes / 68 FKs / 120 CHECKs`.
> This overlay supersedes only contradictory **current status, routing, branch and next-step prose** later in this file. Historical evidence, accepted architecture, frontend product contracts, failed-run/repair evidence and phase-time records remain historical truth and are not rewritten. The aligned feature branch is only a candidate for protected-main integration: **no final merge into `main` is authorized by this overlay**. Protected-main integration still requires the normal PR, current-head required checks and a separate final merge gate.

> **CURRENT INTEGRATION RECONCILIATION — 2026-08-24**  
> Frontend materialization integration is **CLOSED / INTEGRATED via merged PR #28** (`f1aacb0724088e0b4b086008a5219c2fba5ce0cf`). `frontend-materialization.md` remains CLOSED/PASS evidence and `frontend-materialization-integration.md` remains durable integration/accepted-risk/future-activation evidence, but neither is a pending merge workstream now. The active backend continuation is `logical-postgresql.md`: branch current with `main`, CP6-03 ACTIVE, Checkpoint J / DB-U23 CLOSED, Parts 1–8 active, `DB-U08 / DB-U15 / DB-U21` OPEN, exact next block = **FINAL ACTUAL POSTGRESQL OBJECT INVENTORY**, Gate 03 not earned, CP6-04 not authorized. Any later PR #28 READY/ACTIVE wording is preserved pre-merge status.  

# Workstream Handoffs

Each active or pending-integration workstream has one operational handoff. It is the safest continuation entry point for that scope.

## Current workstreams

- [`today-home.md`](today-home.md) — separate Phase-4 Home/Today UX/product-structure workstream; prototype/UX authority only, not production engineering authority.

No frontend materialization/integration workstream is currently active. New frontend/product/security/backend work starts from current `main` under a fresh bounded branch and gate.

## Completed / integrated or closed evidence workstreams

- [`frontend-materialization-integration.md`](frontend-materialization-integration.md) — **CLOSED / INTEGRATED VIA PR #28**; protected-main integration-hardening record, Dependency Review accepted-risk lifecycle, Frontend CI Gate calibration/promotion evidence and durable future-activation register.
- [`frontend-materialization.md`](frontend-materialization.md) — **CLOSED / PASS — FM-00..FM-07 COMPLETE AT THEIR STATED SCOPES**; direct Web/Mobile/tooling/shared-package/CI/fresh-materialization evidence. The closed branch is evidence source, not a reusable work branch.
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
FRONTEND MATERIALIZATION     CLOSED / PASS / integrated
FRONTEND PR #28              CLOSED / MERGED
FRONTEND CI GATE CALIBRATION COMPLETE
FRONTEND CI GATE PROMOTION   OWNER-CONFIRMED APPLIED / DIRECT API READBACK UNAVAILABLE
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

## Frontend integration closure record

```text
final PR head        a6607ceabd35f874dc9e5f63fe8f57f71a92bf80
prior main           fd3bc8dd918cf6aadeff4572221af68612c3cb42
protected-main merge f1aacb0724088e0b4b086008a5219c2fba5ce0cf
PR #28               MERGED
merge parentage      PASS
merged tree identity PASS
exact-head hosted CI PASS
push-main CI         DIRECT READBACK UNAVAILABLE
```

The integration branch was observed absent after merge; no manual branch deletion was performed during the merge operation.

## Operational rule

`main` remains integrated authority. Newer unmerged branch truth is bounded to its active workstream until merge.

Before continuation:

1. read development operating/safety rules;
2. verify exact Git relation/PRE-SCOPE;
3. read the complete applicable current or closed handoff;
4. consume applicable closed model/Foundation/ADR authorities;
5. distinguish selected/installed/configured/directly validated states;
6. update the active handoff on every substantive slice.

## Frontend continuation

Do not reopen general stack/architecture selection by default.

There is no remaining PR #28 merge sequence. Future continuation is trigger-based:

```text
repository-security maturation
-> CodeQL default setup evaluation under a fresh explicit gate

backend next
-> Concrete Logical -> PostgreSQL under a fresh bounded workstream

product next
-> first real vertical slice
-> activate only capabilities actually consumed
```

The future-activation register in `frontend-materialization-integration.md` must be consulted when the first real vertical/UI/form/API/offline/deployment/release/security/pre-PROD/scale trigger occurs.

Durable architecture changes belong in current specs/ADRs, not only handoff text. Historical sources never override later current truth.
