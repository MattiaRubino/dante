# Timeline / Temporal-Operational — B06 Routine / Recurrence / Occurrence Execution Plan

- **Status:** B06-A/B/C ✅ CLOSED / PROVEN — B06-D 🔒 APPROVED / IN PROGRESS
- **Date:** 2026-09-22
- **Branch:** `feature/timeline-temporal-operational`
- **Entering completed frontier:** B05 ✅ CLOSED / PROVEN at `11b182a`
- **Entering candidate DB:** PostgreSQL 18.6 / Alembic `20260921_48` / `129|5|62|90|254|185|366|0|0|0`
- **CI / Actions:** not authorized; direct local proof is user-run

This is the B06 authority required by the current roadmap. It activates the already materialized CP6 Routine/Event Recurrence and Occurrence-generation substrate as a product capability. It does **not** reinterpret a repeated Activity as a Routine and does not let the browser manufacture canonical future state.

## 1. Authority and non-negotiable semantic firewall

Authority is the accepted Domain concepts `Routine`, `Recurrence` and `Occurrence`, logical Time/Reality slice LR-01/LR-05, CP6-M04/M05/M06/M07, the frozen vertical inventory section B06 and the current map/roadmap.

```text
Activity != Event != Routine
Routine != Recurrence
Recurrence != Occurrence
Occurrence != Schedule
Schedule != Session != Actual != Outcome

generated Occurrence != materialized fake Activity
Occurrence identity != current time != current Schedule != provider instance identity
idempotency operation id != Routine/Event/Occurrence identity
projection != canonical truth
```

- A **Routine** is the durable self-owned repeated behavioral/execution policy. Its title, source lifecycle and product organization belong to the Routine source.
- A **Recurrence** is an immutable owner-bound generation MaterialState. Owners are exactly Routine and Event; there is no generic recurrence root and no Activity recurrence.
- An **Occurrence** is the stable identity of one generated or explicit expected instance. It may be virtual before a meaningful interaction; once materialized it retains source, governing state and generation coordinate.
- A **Schedule** is an optional accepted placement of one materialized Occurrence. It does not identify the Occurrence and cannot replace its generation provenance.
- A recurring Event stays an Event source. A Routine never becomes an Event merely because it has a time.

## 2. B06 fixed behavior contract

### 2.1 Mutation scopes

| User intent | Canonical effect | Must not do |
|---|---|---|
| **Modify this Occurrence** | Materialize/locate that one instance and apply a typed occurrence exception or optional Schedule change. | Mutate the Recurrence or other Occurrences. |
| **Modify this and subsequent** | Create a later immutable Recurrence MaterialState with an explicit effective boundary. Existing historical provenance remains attached to its old state. | Rewrite prior material states or silently delete materialized future history. |
| **Modify whole series/source** | Change Routine/Event source metadata or source lifecycle under its own guarded operation. | Retroactively replace historical generation semantics. |
| **Skip Occurrence** | Persist a non-execution exception/disposition on the identified Occurrence. | Delete it, create a fake Actual/Outcome, or end the Routine. |
| **Pause/end Routine** | Stop future generation at an explicit source-lifecycle boundary. | Delete the Routine, erase Occurrences, or reinterpret past expectations as skipped. |

There is no public semantic `delete occurrence` operation. Structural exclusion means the rule does not generate a virtual candidate; it is distinct from a generated, materialized Occurrence that was later skipped.

### 2.2 Recurrence families and exact temporal meaning

B06 activates all and only the four CP6-materialized families:

```text
calendar_wall_clock
elapsed_interval
quota_per_period
cyclic_positional
```

- Calendar/wall-clock retains pattern anchor, explicit effective range, interval/selectors, clock basis and, when named-zone, IANA zone.
- Elapsed uses an absolute anchor and elapsed duration; it is not a disguised wall-clock rule.
- Quota retains amount, period frame, week start where relevant and zone/frame; it does not fabricate a weekday, exact clock time or ordinal.
- Cyclic retains anchor, cycle length/unit and explicit positions.
- Ranges are `open`, `until_boundary` or `expected_count`; count is expected Occurrence count, never completion count.
- Completion-relative and anchor-stream-relative are excluded: they require Session/Actual anchors and remain B11.

For named-zone calendar rules B06 persists an explicit DST policy with no library default:

```text
nonexistent local wall time (spring gap) → structural non-generation for that civil candidate
ambiguous local wall time (fall overlap) → exactly one explicitly selected resolution: earlier | later
```

`floating_local` has no hidden named-zone resolution; `absolute_utc` and `elapsed_interval` do not gain wall-clock semantics. A local date/time must never be silently converted between these forms.

### 2.3 Checkpoint, materialization and range reads

Canonical flow is fixed:

```text
source + current/effective Recurrence state
→ backend evaluator
→ idempotent bounded materialization checkpoint
→ canonical Occurrences
→ bounded range query
→ Timeline projection
```

The checkpoint is a mutating, idempotent backend command; the Timeline `GET` remains a read and never performs hidden generation. It accepts a half-open local-date range constrained to the existing Timeline maximum of 62 days, the effective actor timezone and a stable operation id/fingerprint. It locks the exact source recurrence/current-generation namespaces in deterministic order. CP6 Role-13 remains the final DB validator for exact source family, governing MaterialState and coordinate membership/uniqueness.

A single checkpoint is additionally capped at 10,000 evaluated Occurrences. Exceeding that bound rejects and rolls back the whole operation; the caller must narrow the requested horizon. This operational cap does not alter the 62-day semantic range contract.

Repeated or concurrent checkpoints for the same accepted intent return the same canonical Occurrence identities; they cannot insert duplicates. A virtual candidate is identified only by its typed source + governing MaterialState + family coordinate. No generic `VirtualRef` is introduced. The checkpoint may create rows only inside the bounded requested horizon; it never pre-creates an infinite series.

Timeline range semantics are also fixed:

- ranges are `[start_date, end_date_exclusive)` in authenticated effective timezone;
- expected coordinate and accepted Schedule placement are separately projected;
- an accepted Occurrence Schedule yields one item, not an extra duplicate beside its expected instance;
- quota expectations remain period/flexible truth, not timed cards fabricated by the UI;
- current source Life Area/Tags are inherited for product grouping; no cloned per-Occurrence organization record is created;
- virtual future may be regenerated after a structural revision; an Occurrence carrying Schedule, skip/exception or other independent history is retained and explicitly reconciled.

## 3. Persistence/API application rules

Existing CP6 tables and integrity triggers are reused; they are not rebuilt or bypassed. B06 adds only real application gaps: self-owned Routine product/lifecycle records and receipts, occurrence exception/checkpoint receipts, explicit DST policy persistence, and typed bounded capabilities needed to expose them.

Every durable write follows:

```text
forward-only Alembic
→ SQLAlchemy row mapping
→ Dictionary objects/scope
→ exact database catalog / owner / ACL proof
→ security-definer application operation with self scope, CAS and immutable receipt
→ FastAPI operation with stable temporal_* operationId
→ exported OpenAPI + generated client
→ frontend refetch of canonical truth
```

No raw CP6 runtime-table write becomes a product API. No generic JSON recurrence payload, polymorphic `(kind,id)` source edge, ambient timezone, hidden retry or frontend ID generator is permitted.

## 4. Complete execution slices

| Slice | Complete owned outcome | Closure proof |
|---|---|---|
| **B06-A — Routine source core** ✅ | Self-owned Routine identity, source title/lifecycle (`active`, `paused`, `ended`), atomic Life Area/source Tag integration, immutable create/lifecycle receipts and public source reads. Because CP6 forbids a bare Routine owner, creation also atomically establishes a distinct mandatory initial daily floating-local Recurrence companion from caller-supplied start date and optional wall time; it is not a defaulted Schedule or an Occurrence. | **PROVEN:** 26 selected direct PostgreSQL/catalog regressions passed; exported OpenAPI/client generation and API-client typecheck passed. Closure: `timeline-temporal-operational-b06-a-closure-2026-09-21.md`. |
| **B06-B — Recurrence authoring** ✅ | Guarded Routine and Event recurrence create/read/revise operations for all four CP6 families; immutable state/history/effective-boundary semantics; explicit persisted named-zone DST policy. No Occurrence, Activity/Event instance, Schedule or Timeline materialization. | **PROVEN at `_54`:** `1` canonical fingerprint test + `28` selected PostgreSQL/catalog regressions; prior API contract and API-client typecheck passed. Closure: `timeline-temporal-operational-b06-b-closure-2026-09-22.md`. |
| **B06-C — Occurrence checkpoint and scope** ✅ | Bounded backend evaluator/checkpoint, canonical materialization, explicit extra, one-instance exception/skip, structural exclusion and this-vs-future reconciliation. | **PROVEN at `_55`:** generated/client gate, `22` selected evaluator/API/OpenAPI tests, selected `41`-test PostgreSQL/catalog/ACL set and focused `3`-test post-fix rerun. Closure: `timeline-temporal-operational-b06-c-closure-2026-09-22.md`. |
| **B06-D — shared Schedule, Timeline and functional UI** | Occurrence enters the existing shared Schedule capability and bounded Timeline query; real creation/edit/read flows for Routine and recurring Event. | Schedule identity/history regression, no duplicated Timeline items or fake quota time, backend transport and browser refetch proof. |
| **B06-E — whole-block closure** | Reconcile all B06 evidence, docs, DB inventory and user walkthrough. | Direct local PostgreSQL/API/frontend regressions plus real-stack manual Routine/Event recurring walkthrough; no CI/Actions. |

Each letter is completed as one whole slice. No artificial `B06-A1/A2/...` delivery split is used.

## 5. Required proof matrix and stop-line

Required direct tests cover all four families; named-zone DST gap/overlap; floating/absolute separation; quota without invented time; half-open 62-day range limit; self isolation; lifecycle; CAS; operation-id collision/replay; concurrent duplicate checkpoint prevention; exact CP6 provenance; explicit extra; skip versus structural exclusion; this occurrence versus this-and-future versus source update; revision retention; Routine/Event reuse; Occurrence Schedule and Timeline behavior; generated OpenAPI/client and frontend remote/refetch paths.

The user runs local PostgreSQL, typecheck, Vitest and real-stack manual proof. No CI/Actions is dispatched by this plan.

B06 stops before Session/Actual/Outcome, responsibility/participation, completion-/anchor-relative recurrence, reminders, solver/replanning, provider/offline synchronization, analytics and the broad B07 UI/UX redesign. B06 UI is limited to the real authoring/read/edit paths needed to prove the capability.
