# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B08 SESSION RUNTIME ✅ CLOSED — user-reported local gate and real-app walkthrough complete
- **Reconciled:** 2026-09-24
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Live execution ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Current candidate Alembic frontier:** `20260924_65`
- **Candidate topology B08-C local proof recorded:** `150|5|99|93|292|236|418|0|0|0`
- **Last proven candidate DB frontier:** B08-C / `20260924_65`
- **CI:** no CI/GitHub Actions unless explicitly authorized; user runs local tests

Read this first after a context reset.

---

# 1. Exact current position

```text
B00–B06 ✅ CLOSED / PROVEN
B07     ⏸ DEFERRED
B08     ✅ CLOSED / USER-REPORTED 2026-09-24
B08-A   ✅ CLOSED / USER-REPORTED VIA B08-B
B08-B   ✅ CLOSED / USER-REPORTED 2026-09-24
B08-C   ✅ CLOSED / PROVEN — local automated gate 2026-09-24
B08-D   ✅ CLOSED / USER-REPORTED — automated gate and real-app walkthrough
B09–B12 ⬜ NOT STARTED
B15     ⬜ NOT STARTED
```

B08-A and B08-B are treated as closed based on the user’s B08-B closure report. Exact test logs are not committed; preserve consolidated evidence in B08-D.

---

# 2. Why B08-A was reopened

The first B08-A closure was premature. Audit found two real defects:

```text
1. START endpoint family was not enforced at the DB boundary.
   Activity route could pass an Occurrence NativeRef and vice versa.

2. END mutated session_timing_absolute in place.
   That violated the MaterialState immutability contract and made replay depend
   on whatever timing state happened to be current later.
```

Both are repaired forward-only; no applied migration was edited.

---

# 3. Current B08-A source truth

```text
20260924_58
  Session execution subject + bounded START/LIST/GET/END

20260924_59
  start_self_session(..., requested_subject_family, requested_subject_native_ref)
  exact Activity/Occurrence family check against native_address.owner_family

20260924_60
  end_self_session(..., expected_state, requested_resulting_state)
  END creates a new immutable session.timing MaterialState
  expected state remains unchanged historical truth
  native current binding + history advance atomically
  session_end_operation stores resulting_material_state_ref
  replay returns the exact produced state
  any candidate `_58` in-place END data is repaired forward-only
```

Topology expected at `_60`:

```text
148 tables
5 views
94 routines
93 triggers
290 indexes
230 FKs
414 CHECKs
0 enum/domain/sequence/materialized/partitioned/RLS
```

---

# 4. Product path now present

```text
Activity   → START → read/reload → END
Occurrence → START → read/reload → END
```

Also present:

```text
scheduled Activity/Occurrence Session controls on Timeline
unplaced Activity Session controls in Planning Tray
```

An unplaced Activity may start a Session directly. **Never create a fake Schedule to enable START.**

Permanent forbidden effects:

```text
START does not create Schedule
END does not complete Activity
END does not resolve Occurrence
END does not create Actual
END does not create Outcome
```

---

# 5. B08-C proof record

The user completed the focused local gate on 2026-09-24:

```text
`pnpm generated:check` PASS
API-client typecheck PASS
web typecheck PASS
focused Session/Create Vitest: 35 passed
focused backend unit/API proof: 15 passed
focused PostgreSQL B08-C/B04/catalog proof: 14 passed
```

The user confirmed Pause, Resume and END now work in the real app after the HTTP fix. Further dogfood exposed two UI defects: selecting a splittable Session silently converted a timed Activity to unplaced, and the Planning Tray Schedule duration used a five-minute input step (26 minutes admitted, 30 minutes rejected with 26/31 as nearby valid values). A follow-up candidate preserves explicit timed placement, establishes its accepted Schedule after constrained Activity creation, uses one-minute controls and reads the Planning Tray from canonical unplaced Activities. User-run reproof is pending.

---

# 6. B08-D user-run closure gate

B08-D is closed from the user's local output and real-app confirmation on 2026-09-24. The focused Web suite passed **58 tests** and the backend PostgreSQL/unit/API command passed **31 tests**. Generated sources and API-client typecheck passed. The first web typecheck exposed six TypeScript errors in the Planning Tray compatibility prop and the post-Schedule projection narrowing; they were repaired in commits `711abed2` and `5cde1039`. The user then confirmed the follow-up typecheck and dogfood pass.

The real-app walkthrough now confirms: START, PAUSE, RESUME and END work; a timed splittable Activity keeps its selected date/time and appears in Timeline; an unplaced Activity remains in Da collocare; and Schedule duration accepts whole-minute values, including 30, without the prior 26/31 five-minute-step warning. TC-009 remains soft and does not block transitions.

From repository root:

```bash
pnpm generated:check
pnpm --filter @dante/api-client typecheck
pnpm --filter @dante/web typecheck
pnpm --filter @dante/web exec vitest run \
  src/features/temporal/session-subject-controls.test.tsx \
  src/features/temporal/remote-session-data-source.test.ts \
  src/features/temporal-create/application/temporal-create-b04-runtime.test.ts \
  src/features/temporal-create/model/temporal-create-session.test.ts \
  src/features/temporal-create/ui/temporal-create-activity-fields.test.tsx
```

From `apps/backend`, with the local PostgreSQL integration environment used for B08-C:

```bash
uv run --locked pytest -q --no-cov \
  tests/integration/database/test_b08_a_session_catalog.py \
  tests/integration/database/test_current_catalog.py \
  tests/integration/database/test_database_current_catalog.py \
  tests/integration/temporal/test_b08_a_session_runtime.py \
  tests/integration/temporal/test_b08_b_session_pause_resume.py \
  tests/integration/temporal/test_b08_c_session_minimum_duration.py \
  tests/integration/temporal/test_b08_d_session_workflow.py \
  tests/test_b08_c_session_duration_evaluation.py \
  tests/test_temporal_constraint_api.py \
  tests/test_b08_a_session_authority_freeze.py
```

Then perform **one** real-stack walkthrough in the authenticated app; record observed SessionRefs, displayed states and any failure:

```text
1. Create a splittable Activity with an active Session minimum longer than the
   walkthrough (e.g. 45 minutes); leave the Activity without Schedule.
2. In Planning Tray START; inspect its SessionRef and the pending TC-009 minimum.
   Reload (F5): same SessionRef, running, Activity still unplaced.
3. PAUSE and reload: same SessionRef, paused, active time stops growing;
   Termina is unavailable. RESUME and reload: same SessionRef, running.
4. END before the threshold: same SessionRef, violated soft minimum; no block.
   Reload: ended state persists. START again: a distinct SessionRef with a fresh
   pending evaluation, not a sum of the two Sessions.
5. On a scheduled Activity, START → reload → PAUSE → RESUME → END. Its accepted
   Schedule placement stays the same; Session time is not placement time.
6. On an eligible Occurrence, START → reload → PAUSE → RESUME → END.
   No inherited Activity TC-009 appears; the Occurrence remains unresolved.
7. Confirm no fabricated Schedule for the unplaced Activity or Occurrence,
   no Activity completion, and no Actual or Outcome from any Session END.
```

The UI need not expose internal identifiers. Capture SessionRefs and canonical Schedule/Actual/Outcome evidence through authenticated API or DB inspection where the UI does not show them. Mark B08-D and B08 closed only after receiving the user's actual automated outputs and walkthrough observations; record evidence in map/roadmap/handoff without claiming unobserved results.

---

# 7. Collaboration discipline

- user runs tests locally; assistant does not run them
- no CI/GitHub Actions unless explicitly authorized
- push changes frequently
- current docs must distinguish candidate truth from proven/protected-main truth
- B07 later consolidates UI; interim B08 UI only needs to be truthful and functional

---

# 8. Fresh-chat recovery

```text
1. this handoff
2. timeline-temporal-operational-roadmap.md
3. timeline-temporal-operational-map.md
4. docs/database/timeline-temporal-operational.md
```

**Exact next action:** Begin B09 Responsibility / Participation from the B08-closed frontier. Contract history remains in `timeline-temporal-operational-b08-c-implementation-freeze.md`.
