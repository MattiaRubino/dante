# Workstream Handoffs

Each active/pending-integration workstream has one operational handoff. It is the safest continuation entry point.

## Current / pending-integration workstreams

- [`frontend-materialization.md`](frontend-materialization.md) — **ACTIVE on `feature/frontend-materialization`; FM-00 workstation preflight NOT RUN; no manifests/apps/dependencies materialized yet**.
- [`today-home.md`](today-home.md) — separate Phase-4 Home/Today UX/product-structure workstream; prototype/UX authority only, not production engineering authority.

## Completed / integrated workstreams

- [`frontend-foundation.md`](frontend-foundation.md) — **DESIGN / ARCHITECTURE CLOSED / ACCEPTED / FINAL REVIEW PASS / integrated via PR #22**; former `feature/frontend-foundation` branch merged/auto-deleted; production frontend direct validation remains carried by the active materialization workstream.
- [`engineering-foundation.md`](engineering-foundation.md) — **CLOSED / ACCEPTED / FINAL REVIEW PASS / integrated via PR #21**.
- [`physical-model.md`](physical-model.md) — **TARGET ARCHITECTURE CLOSED / SELECTED / ACCEPTED / integrated via PR #15**; direct selected-stack implementation validation remains carried forward/not started where applicable.
- [`pre-physical-coherence.md`](pre-physical-coherence.md) — **DEFINITIVE CLOSED / FINAL QA PASS / integrated via PR #13 / post-merge aligned via PR #14**.
- [`domain-model.md`](domain-model.md) and continuations — historical operational record for CLOSED Domain Model integrated via PR #10.
- Logical Model workstream documents/continuations — historical operational record for CLOSED Logical Model integrated via PR #11.

## Historical / superseded planning handoffs

- [`backend-foundation.md`](backend-foundation.md) — historical pre-Engineering-Foundation planning; not current implementation authority.

## Carry-forward rule

```text
PHYSICAL TARGET                CLOSED / ACCEPTED
ENGINEERING FOUNDATION v0      CLOSED / ACCEPTED
FRONTEND FOUNDATION            DESIGN/ARCHITECTURE CLOSED / ACCEPTED / FINAL REVIEW PASS
FRONTEND MAIN INTEGRATION      COMPLETE VIA PR #22
FRONTEND MATERIALIZATION       ACTIVE
FM-00 WORKSTATION PREFLIGHT    NOT RUN
PRODUCTION FRONTEND SCAFFOLD   NOT STARTED
DIRECT HG PASS                 0
FRONTEND DIRECT VALIDATION     NOT RUN
SELECTED != INSTALLED
INSTALLED != CONFIGURED
CONFIGURED != DIRECT PASS
```

Version-sensitive claims require current primary-source verification when material. Implementation/reopen requires fresh exact scope.

## Operational rule

The handoff is the workstream save-game. Current `main` remains integrated authority; newer unmerged branch truth is bounded to its active workstream until merge.

Before continuation read development operating/safety rules, verify current Git relation, read complete applicable specs/ADRs and consume closed model/Engineering authorities.

For the active frontend workstream:

```text
frontend-materialization.md
↓
../development/frontend-local-development.md
↓
FM-00 read-only workstation preflight
↓
review evidence
↓
only then FM-01 installation/runtime work
```

Do not restart general frontend stack/architecture selection without concrete contradictory evidence. Do not begin Access/Home production implementation as a substitute for materialization validation.

Durable architecture changes belong in appropriate current specs/ADRs, not only handoff text. Historical sources never override later current truth.
