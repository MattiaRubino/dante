# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B08 SESSION RUNTIME 🟡 — B08-D USER WALKTHROUGH FAILED; HTTP FIX PUBLISHED, REPROOF PENDING
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
B08     🟡 IN PROGRESS
B08-A   ✅ CLOSED / USER-REPORTED VIA B08-B
B08-B   ✅ CLOSED / USER-REPORTED 2026-09-24
B08-C   ✅ CLOSED / PROVEN — local automated gate 2026-09-24
B08-D   🟡 USER WALKTHROUGH FAILED — Pause/END 422; fix awaits local repro
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

The B08-D real-stack walkthrough exposed HTTP 422 on Pause and END despite the displayed five-minute minimum being met. The minimum is a soft read-time evaluation and must not block those commands. A targeted HTTP and authoring fix is published as a candidate; user-run local proof is still required.

---

# 6. B08-D user-run closure gate

The prepared regression is `test_b08_d_session_workflow.py` (PostgreSQL Activity/Occurrence and TC-009 across A/B/C) plus `session-subject-controls.test.tsx` (browser controls, pause reload and policy display). During the user's real-stack walkthrough, START succeeded, but PAUSE and END returned HTTP 422 (`One or more request fields are invalid.`), including after the soft minimum became satisfied. The HTTP command inherited strict validation that rejected the JSON string for `expected_material_state_ref` before the runtime could evaluate the Session. The candidate fix accepts a valid UUID string for this field, keeps invalid identifiers rejected, and allows arbitrary positive whole-minute minimum values (including 1, 26 and 31) instead of five-minute steps. No B08-D automated test output has yet been reported. Run the following local gate after pulling the published fix; the assistant does not run tests or activate CI.

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

**Exact next action:** User pulls the HTTP and authoring fix, runs the B08-D commands and repeats the walkthrough, including PAUSE and END after reload; capture actual results and close B08 only if both gates pass. Contract: `timeline-temporal-operational-b08-c-implementation-freeze.md`.
