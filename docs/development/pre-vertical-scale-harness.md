# Pre-Vertical Scale Harness

- **Status:** CURRENT / PRE-VERTICAL FOUNDATION / PV-03 A CLOSED / PASS
- **Scope:** deterministic product-independent scale/readiness fixtures plus bounded PostgreSQL convergence proof
- **Closure record:** `../workstreams/pre-vertical-foundation-closure-2026-09-06.md`

## Purpose

The pre-vertical foundation needs repeatable scale inputs before the first product vertical exists, but it must not invent the vertical's domain rows, workload model or performance budget.

The boundary is:

```text
scale fixture planning
!= mass login-account provisioning
!= product vertical fixtures
!= performance/load benchmark
!= canonical history/state model
```

The harness reuses the three PV-02 personas and the existing disposable PostgreSQL 18.6 acceptance harness. Building a scale plan is an in-memory operation and performs no database write.

## Profiles

The deterministic profiles are:

| Profile | Entries | Matrix repetitions |
|---|---:|---:|
| `small` | 12 | 1 |
| `medium` | 120 | 10 |
| `large` | 1200 | 100 |

Each 12-entry matrix contains exactly:

```text
3 PV-02 personas
x
4 synthetic history input shapes
=
12 fixture plans
```

The cardinalities are fixture sizes only. They are not throughput targets, concurrency budgets, latency targets, capacity claims or SLAs.

The plans are prefix-stable: `small` is the first 12 entries of `medium`, and `medium` is the first 120 entries of `large`. Increasing a test profile therefore does not rename earlier synthetic identities.

## Deterministic identity

Every fixture entry provides a stable synthetic:

- Account UUIDv7;
- self-Person UUIDv7 candidate;
- `example.com` email address;
- reference to one of the existing PV-02 persona specifications;
- one fixture-only history input shape.

The UUIDv7 timestamp bits remain fixture-construction detail only. UUID ordering is never chronology/currentness authority.

The scale planner deliberately contains no password, verifier or password-credential material. It does not run Argon2 and does not create hundreds or thousands of login-capable Accounts merely to fill a database.

## Synthetic history input shapes

The four labels are test-input shapes, not DANTE semantic/domain types:

- `metadata_free` — no explicit source timestamp metadata;
- `incomplete` — one explicit source instant;
- `corrected` — an earlier source instant plus a later correction-oriented source instant;
- `mixed` — three explicit fixed-age source instants spanning older, middle and recent fixture history.

Their `source_instants` are explicit timezone-aware UTC timestamps and are stored in ascending chronological order inside the fixture plan.

They do **not** introduce a generic Fact, Version, Event, Observation, MaterialState, relationship edge or database history schema. A future vertical must map only the fixture aspects relevant to its real operations and canonical owners.

## PostgreSQL acceptance boundary

The real PostgreSQL scale check stays deliberately bounded. The `small` profile supplies 12 deterministic self-Person candidates for concurrent first use of one active Account through the existing `dante.ensure_account_application_context(...)` runtime capability.

The proof requires all contenders to converge on:

```text
one Account
-> one account_application_context
-> one self Person
-> one Person native address
```

Candidate self-Person refs that lose the first-use race must not become extra Person/native-address rows.

This is a correctness/concurrency invariant check. Twelve contenders are derived from the `small` fixture size; they are not a declared production concurrency budget or performance target.

Observed acceptance:

```text
targeted real PostgreSQL scale/convergence test    PASS — 1 passed
full PostgreSQL 18.6 marked suite                  PASS — 165 passed
```

## Explicit exclusions

The Scale Harness does not create or redefine:

- Activity;
- Event;
- Routine;
- Occurrence;
- Session;
- Actual;
- Outcome;
- Observation;
- generic Facts/Versions/Rules/relationship edges;
- generic `(kind, uuid)` semantic references;
- generic JSON canonical payloads;
- product-specific workload distributions;
- latency/throughput/capacity budgets;
- a long-lived synthetic canary at this stage.

No new Alembic/schema, Access/Auth, CP1–CP6, frontend, Recovery, Email, Observability, Intelligence/Search or GitHub workflow change is owned by this harness.

## Relationship to whole-branch QA

PV-03 A Scale Harness implementation and targeted executable proof are closed. PV-03 B whole-branch local QA is also closed and green across backend/frontend/PostgreSQL acceptance.

The only remaining pre-vertical lifecycle is PV-03 C:

```text
final documentation cleanup
→ exact-head Recovery rehearsal
→ protected-main PR gates
→ merge commit + readback
→ branch retirement
```

There is no PV-04.

This file remains a durable development/testing reference after integration; it is not an active roadmap.
