# Timeline / Temporal-Operational — B11-A Advanced Recurrence Scope

- **Status:** B11-A APPROVED / IN PROGRESS
- **Date:** 2026-09-26
- **Branch:** `feature/timeline-temporal-operational`
- **Entering completed frontier:** B10 ✅ CLOSED / PROVEN
- **Entering DB frontier:** PostgreSQL / Alembic `20260926_80`
- **CI / Actions:** not authorized; direct local proof is user-run

B11-A extends the already proven B06 recurrence capability. It does not reopen B06 and does not introduce a generic RRULE/automation engine.

## 1. Exact owned scope

B11-A activates the two recurrence families that B06 explicitly deferred because they require Session/Actual/reality anchors:

1. **completion-relative recurrence**;
2. **anchor-stream-relative recurrence**.

All B06 families and invariants remain authoritative:

```text
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Session != Actual != Outcome

generated/future Occurrence != happened fact
projection != canonical truth
idempotency operation id != Domain identity
```

B11-A must reuse the B06 owner model, immutable Recurrence MaterialState/history, bounded checkpoint, stable Occurrence identity, reconciliation rules and Routine/Event source semantics. It must not create a second recurrence root or a browser-owned projection store.

## 2. Completion-relative recurrence

Canonical meaning follows `docs/domain/concepts/recurrence.md`:

```text
qualifying Actual / reviewed reality fact
        ↓ + elapsed offset
next expected Occurrence
```

The first supported B11-A completion anchor is an explicit qualifying **Actual completion/reality state** attached to the source occurrence/reality chain. `scheduled end`, expected Occurrence end and a mere Session lifecycle transition are not substitutes for Actual completion.

The chain is sequential. Without a qualifying completion anchor, the next dependent expected Occurrence is not independently fabricated from the original calendar/elapsed seed. Completion-relative recurrence therefore must not silently degrade into a fixed calendar series.

A correction to reality does not rewrite already accepted/materialized Occurrence history. Current accepted reality may affect future projection/checkpoint decisions only under the explicit B11-A reconciliation contract.

## 3. Anchor-stream-relative recurrence

Canonical meaning follows `docs/domain/concepts/recurrence.md`:

```text
qualifying anchor A ── relation / elapsed offset ──> related Occurrence A
qualifying anchor B ── relation / elapsed offset ──> related Occurrence B
```

This is a deterministic repeated mapping from a defined stream of qualifying canonical anchors. Each qualifying anchor independently owns the generation provenance of its related Occurrence.

The anchor stream is not copied timestamp authority. B11-A must preserve enough canonical anchor identity/provenance to make replay, uniqueness and correction behavior deterministic. The implementation may support reviewed temporal/reality anchor kinds only; it must not become arbitrary IF/THEN automation, threshold evaluation or a generic trigger engine.

## 4. Persistence decision

B11-A may add a forward-only migration starting at `_81` only where durable canonical recurrence semantics or exact anchor provenance cannot be represented by the published B06/B10 schema.

Published migrations through `_80` are immutable.

Any added persistence must remain typed and narrow. No generic JSON rule payload, polymorphic ungoverned `(kind,id)` edge, copied provider timestamp authority or universal `Anchor` entity is approved by this scope.

## 5. Checkpoint and generation rules

B11-A preserves the B06 checkpoint contract:

- bounded half-open request horizon;
- backend-only mutation; Timeline GET never performs hidden generation;
- deterministic replay/idempotency;
- canonical Occurrence identity distinct from operation id;
- no fake Activity, Schedule, Session, Actual or Outcome materialization;
- retained independent history is not deleted by recurrence correction;
- Routine and Event remain the only approved Recurrence owners unless a later reviewed scope explicitly changes that authority.

Additional B11-A requirements:

- completion-relative generation is blocked until the qualifying canonical reality anchor exists;
- anchor-stream generation is one deterministic mapping per qualifying anchor coordinate/provenance;
- anchor identity/provenance participates in uniqueness strongly enough that two distinct qualifying anchors cannot collapse into one Occurrence;
- replay of the same accepted anchor set cannot duplicate Occurrences;
- corrected anchors cannot silently rewrite already materialized independent history.

## 6. Public vertical

B11-A is not complete until the capability is aligned through the full owned vertical where applicable:

```text
Domain authority
→ Logical / Physical / PostgreSQL
→ SQLAlchemy / runtime evaluator
→ Dictionary / DB docs
→ API / OpenAPI
→ generated client
→ web authoring/read path
→ focused regressions
```

Generated API-client files are produced by the repository generator locally and are never hand-edited remotely.

## 7. Explicitly out of scope

B11-A does not include:

- arbitrary trigger/state/threshold automation;
- B11-B conditional behavior;
- B11-C Reminder intent/delivery;
- general workflow or policy engine;
- AI-selected anchors/effects;
- provider/offline sync;
- B12 Plan/Step/Dependency;
- B14 solver/replanning;
- B15 generalized Visibility/AuthZ;
- reinterpretation of Session end as Actual completion.

## 8. Closure proof

B11-A closure requires direct local proof covering at least:

- completion-relative blocked without qualifying reality anchor;
- a qualifying Actual/reality completion yields the expected relative Occurrence;
- Session/scheduled end alone does not qualify as completion;
- anchor-stream produces one correctly related Occurrence per qualifying canonical anchor;
- exact anchor provenance/identity and deterministic replay;
- no duplicate generation under replay/concurrency contract;
- correction/revision retains independent historical Occurrences and does not silently rewrite reality;
- Routine/Event reuse and B06 checkpoint regressions;
- OpenAPI/generated-client contract and web typecheck/tests for the exposed authoring path.

Only after those proofs may this document become `B11-A ✅ CLOSED / PROVEN` and the workstream move to B11-B.
