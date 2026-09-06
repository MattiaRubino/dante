# DANTE — Temporal F0 Application Foundation Contract

**Status:** ACCEPTED / CLOSED — LOCAL + CI PASS
**Date:** 2026-09-01
**Owner workstream:** `feature/home-timeline`
**Integration target:** `feature/home-react`
**Scope:** frontend temporal application boundary only; no new visible feature
**Closure commit:** `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`
**Closure CI:** Frontend CI #213 — Quality PASS, Mobile Bundle PASS, Chromium Web E2E PASS, frozen Timeline Firefox contract PASS, Frontend CI Gate PASS

## Purpose

F0 establishes the smallest production-grade application seam that later
temporal capabilities can consume without binding UI to Timeline prototype
state, backend DTOs, persistence rows, AI providers or fake networking.

F0 is deliberately **deep but narrow**.

```text
manual UI / keyboard / future voice / governed AI
                         │
                         ▼
                 TYPED COMMAND
                         │
              validation / precondition
                         │
                         ▼
              TEMPORAL WORKSPACE PORT
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
 deterministic local adapter      future real adapter
          │                             │
          └──────── truthful result ────┘
                         │
                         ▼
                 projection consumers
```

## Non-collapse invariants

```text
ViewModel != application projection != DTO != DB row
date-only != floating local != zoned exact time != absolute instant
source/intention != accepted placement
Schedule/placement != Session != Actual
proposal != accepted effect
pending != success != rejection != infrastructure failure
no-op != mutation
retry != duplicate effect
Undo != blind overwrite of newer truth
```

F0 intentionally does not model Session, Actual, recurrence rules or proposals
yet. It reserves capability seams so later verticals can add those semantics
without flattening every item into one universal object.

## Temporal semantics

F0 uses `@dante/time` / Temporal values directly.

Supported placement forms:

- `date-span`: timezone-free dates, exclusive end;
- `floating-local`: wall-clock `PlainDateTime` with no invented zone;
- `zoned`: exact time + IANA zone via `ZonedDateTime`;
- `absolute`: exact `Instant`;
- `null`: no accepted placement yet.

No form is silently converted into another. Zoned range validation compares
exact instants, including across DST transitions.

## Clock

Time is a dependency, not a hidden global assumption.

- `systemTemporalClock` is the production/system adapter.
- `createFixedTemporalClock` gives deterministic tests/prototype anchoring.
- callers can request `today` in an explicit zone.

The accepted prototype date can therefore remain deterministic without
teaching UI code that the real world is permanently 2026-08-04.

## Identity, retries and concurrency

F0 separates projection id, operation id and Undo token.

`operationId` is an idempotency key: retrying the exact same operation does
not duplicate the effect. Reusing one operation id for a different command
type or a different payload/envelope is rejected as an idempotency-key
collision rather than returning an unrelated cached result.

Mutations after creation carry an expected projection revision. Stale writes
reject instead of overwriting newer truth.

Projection ids are frontend/application references. They do not claim to be
canonical PostgreSQL UUIDv7 identities.

## Command/query boundary

Current F0 commands:

- create projection;
- replace accepted placement;
- remove projection;
- Undo reversible operation.

Every command carries operation id, input source and exact issued-at instant.

Current queries:

- get projection;
- list deterministic workspace snapshot.

The TypeScript port correlates each query with its exact result type, so a
`list` consumer receives a statically known snapshot result rather than a
broad union requiring casts.

Range/window queries are deferred until a real consumer defines timezone,
pagination and horizon semantics.

## Truthful operation lifecycle

Result states:

```text
applied
no-op
rejected
failed
```

`rejected` is deterministic application refusal such as validation,
not-found, stale revision or Undo conflict.

`failed` is reserved for future transport/infrastructure failure.

`pending` is a lifecycle state, never fake success.

The local adapter is async-shaped but has no fake delay, fake HTTP or fake
server.

## Undo and reconciliation

Applied reversible mutations may return an opaque Undo token.

Undo is guarded by the exact revision/state produced by the original mutation.
If newer truth exists, it rejects with `undo-conflict`. Restoration creates a
new monotonic revision; it never rewinds a version counter.

Applied local operations report reconciliation `confirmed`. The shared result
contract also reserves `adjusted` and `conflict` for a future authoritative
adapter without pretending they happen locally.

## Draft and validation

F0 owns only universal mechanics:

- immutable baseline/current draft;
- dirty tracking;
- reset/commit;
- machine-readable validation codes/paths;
- deterministic issue ordering.

Quick Add owns its future fields and product rules.

## Capability seams

A projection advertises only applicable capabilities:

- placement;
- recurrence;
- execution;
- actual;
- confirmation;
- replanning;
- history;
- notes.

This supports future progressive disclosure without making every item expose
every semantic axis.

## Port and local adapter

Consumers target `TemporalWorkspacePort`.

The deterministic in-memory adapter is:

- async-shaped for future adapter swap;
- idempotent by operation id;
- revision guarded;
- observable via subscription;
- side-effect free on rejection/no-op;
- protected against stale Undo;
- isolated from subscriber rendering exceptions;
- no localStorage;
- no fake network;
- no backend DTO;
- no PostgreSQL coupling.

## External design pressure incorporated

F0 follows established patterns without copying another product's data model:

- TC39 Temporal: semantic distinction between date-only, local wall-clock,
  zoned and exact time;
- Google Calendar: stable recurring-instance identity survives movement,
  reinforcing identity/provenance separation;
- Microsoft Graph: client transaction id prevents duplicate create effects on
  retries, reinforcing operation idempotency;
- Sunsama: planned and actual time remain separate;
- Reclaim: tasks/habits/focus-time have different scheduling semantics rather
  than one generic calendar row.

These reinforce existing DANTE Domain decisions; they do not replace them.

## Explicit non-goals

F0 does not:

- implement Quick Add UI;
- change current Timeline rendering/scrolling/interactions;
- migrate accepted T1 drag/time editing into the new pipeline;
- expand recurrence;
- implement Session / Actual / completion;
- implement solver/replanning;
- add AI or voice behavior;
- invent API DTOs;
- mirror DB tables;
- persist mock data;
- change Home/H0 structure.

## Acceptance gate — CLOSED

F0 closure evidence:

1. existing Home/Timeline behavior remained unchanged — PASS;
2. all temporal forms round-trip without semantic collapse — PASS;
3. fixed clock is deterministic across zones — PASS;
4. invalid ranges reject — PASS;
5. retries are idempotent — PASS;
6. stale revisions reject — PASS;
7. no-op does not fabricate mutation/Undo — PASS;
8. Undo cannot overwrite newer truth — PASS;
9. revisions remain monotonic after Undo — PASS;
10. snapshots are deterministic — PASS;
11. subscribers fire only on applied mutations — PASS;
12. subscriber failure cannot corrupt committed state — PASS;
13. temporal capability has no React/Timeline dependency — PASS;
14. no fake transport/storage/DB coupling exists — PASS;
15. full frontend CI passes — PASS on Frontend CI #213 after rerun of an unrelated Access first-Tab focus flake;
16. user explicitly approved F0 before Quick Add begins — PASS on 2026-09-01.

F0 is therefore closed. Further changes require demonstrated need from a later capability or backend integration rather than speculative expansion.
