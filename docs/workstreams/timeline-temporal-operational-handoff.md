# Timeline / Temporal-Operational — Workstream Handoff

- **Status:** B08 SESSION RUNTIME 🟡 — B08-A SOURCE REPAIRED / AWAITING USER PROOF
- **Reconciled:** 2026-09-24
- **Branch:** `feature/timeline-temporal-operational`
- **Roadmap authority:** `docs/workstreams/timeline-temporal-operational-roadmap.md`
- **Live execution ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **DB overlay:** `docs/database/timeline-temporal-operational.md`
- **Current candidate Alembic frontier:** `20260924_60`
- **Candidate topology awaiting proof:** `148|5|94|93|290|230|414|0|0|0`
- **Last proven DB frontier:** B06 / `20260923_57`
- **CI:** no CI/GitHub Actions unless explicitly authorized; user runs local tests

Read this first after a context reset.

---

# 1. Exact current position

```text
B00–B06 ✅ CLOSED / PROVEN
B07     ⏸ DEFERRED
B08     🟡 IN PROGRESS
B08-A   🟡 IMPLEMENTED / REPAIRED / AWAITING PROOF
B08-B   ⬜ BLOCKED BY B08-A
B08-C-D ⬜ BLOCKED
B09–B12 ⬜ NOT STARTED
B15     ⬜ NOT STARTED
```

Do **not** start B08-B before B08-A local + manual proof passes.

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

# 5. Exact proof to run next

From the repo after pulling the branch, user runs the focused automated bundle. Required gates include:

```text
Alembic upgrade to `20260924_60`
B08-A Session catalog proof
B08-A Activity/Occurrence runtime proof
whole current DB catalog/Dictionary proof
relevant Session API/OpenAPI proof
generated:check
API-client typecheck
web typecheck
remote Session datasource Vitest
relevant Timeline/Planning Tray focused Vitest
```

Then real-stack manual proof:

```text
1. create/use an Activity with no Schedule
2. START Session from Planning Tray
3. verify Activity is still unplaced / no Schedule fabricated
4. F5 → same Session still running
5. END → Session closes
6. START again → new SessionRef
7. scheduled Activity START/F5/END
8. eligible Occurrence START/F5/END
9. verify Schedule unchanged
10. verify no completion / Actual / Outcome appeared
```

Only after accepted evidence:

```text
B08-A ✅ CLOSED / PROVEN
B08-B ← NEXT
```

---

# 6. Collaboration discipline

- user runs tests locally; assistant does not run them
- no CI/GitHub Actions unless explicitly authorized
- push changes frequently
- current docs must distinguish candidate truth from proven/protected-main truth
- B07 later consolidates UI; interim B08 UI only needs to be truthful and functional

---

# 7. Fresh-chat recovery

```text
1. this handoff
2. timeline-temporal-operational-roadmap.md
3. timeline-temporal-operational-map.md
4. docs/database/timeline-temporal-operational.md
```

**Exact next action:** user proof of repaired B08-A at `_60`; no B08-B implementation before that.
