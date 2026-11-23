# Draft Vault (Bozze) — canonical operational contract

**Scope:** DANTE LifeOS Timeline, Activity/Event authoring, inspector, persistence,
and deletion. **Status:** implemented paths described below; owner acceptance,
PostgreSQL capacity migration `20261123_189`, and new E2E must pass before
calling the contract fully verified. This document defines the required
behavior, not proof that every detail has already passed production testing.

Related contract: [Duplicate (Duplica)](./temporal-duplicate.md).
Implementation anchors: `timeline-draft-vault.tsx`,
`temporal-create-entry.tsx`, `remote-draft-vault.ts`,
`draft_vault_api.py`, `20261009_134_b14_draft_vault.py`, and
`20261123_189_draft_vault_owner_capacity.py`.

## 1. Terms and non-negotiable invariants

A **Draft (Bozza)** is a versioned, *inert* proposal to create an Activity or
Event. It has its own `draft_ref`; it is **not** a Schedule, accepted Activity,
Event, Session attempt, Recurrence or a pre-existing unplaced native subject.

- A Draft reserves no calendar slot, owns no accepted Activity/Event identity,
  cannot be played/paused/stopped, executes no reminder, and generates no
  recurrence occurrence. Saving one never mutates an existing native subject.
- Its configuration may contain suggested date and time, full-day ranges,
  Life Area, coloring, interval definitions, Session definitions, Objectives,
  Event agenda/participants, reminder/confirmation and recurrence *intent*.
- Drafts do **not** carry actual runtime state: Session attempts, actual
  start/stop/pause times, recorded Objective observations and assessments,
  actual participation, execution progress, notification dispatch history.
- Both `Riprendi` and `Duplica` open the **same real full Advanced Create**
  used by a new Activity/Event; there is no separate Draft editor. The saved
  `surface` records origin but **does not dictate** the resumed editor surface.
- Existing accepted Activity/Event identities are never recycled when
  duplicating or turning a Draft into a newly accepted subject.
- The backend, not the UI counter, is authoritative for ownership, revisions,
  capacity and the atomic Move operation.

## 2. Model, ownership and persistence

`dante.temporal_draft_vault` contains
`draft_ref` (UUID, PK), `owner_person_ref`, `subject_kind` (Activity/Event),
`title`, `payload` (jsonb), `revision`, `last_operation_id`,
`created_at`, `updated_at`. The visible UI title may be a fallback while
the persisted `title` is truly empty.

The version-1 payload contains exactly the structural concepts:
`{ version: 1, fields, advanced, surface }`. `fields` is the shared Create
form state; `advanced` is the complete U2/Activity/Event authoring draft;
`surface` records where it was saved (quick/expanded/full). Rehydration must
not depend on jsonb object-key order. Draft identity and revision live *outside*
the payload and do not become Event/Activity identities.

Validation boundaries: title up to **300 characters** (zero allowed);
serialized payload up to **128 KiB**; supported kinds Activity/Event;
payload version and embedded kind must match the request. Malformed payloads
must fail instead of silently dropping unsupported fields. Backend functions
are SECURITY DEFINER, only accessible to the authorized actor through
the approved runtime capabilities; other actors cannot list/edit/delete them.

### 2.1 Per-owner capacity

**100 total Drafts per user**, shared across both kinds. No split allowance
(e.g. 100 Activities plus 100 Events). Count is per owner, not global.

- New Save, Duplicate→Save and atomic Move→Draft consume one slot.
- Revision of the **same Draft** and idempotent replay do not consume a new
  slot, including when the Vault already has 100 entries.
- Resume, inspect, cancel, and Duplicate *before saving* do not consume a slot.
- Delete or successful Add followed by removal of the source Draft frees a slot.
- At 100/100, no 101st Draft: the database's BEFORE INSERT gate
  `enforce_temporal_draft_vault_capacity` checks the count under a
  **per-owner transactional advisory lock**. Concurrent requests cannot treat
  a stale UI count as permission. A separate owner's quota is unaffected.
- This applies to both plain Save and Move (same SQL insertion path). On Move,
  failure rolls back the enclosing SERIALIZABLE transaction; the original,
  all its factual records and all existing Drafts remain unchanged.
- SQLSTATE `PZ101` becomes HTTP **409**,
  code `temporal.drafts.capacity`; client shows a small
  **Spazio Bozze esaurito** alert explaining what to delete. Closing this
  alert must **not discard** the Create form/Inspector.
- The Vault header shows `N/100`; an optimistic client-only disable must
  never replace server enforcement.
- At present the list endpoint returns the complete owner Vault; if quota
  is ever raised substantially, investigate pagination/virtualization first.

**Cap reached:** "Hai raggiunto il limite di 100 Bozze. Elimina una Bozza
prima di salvarne un’altra." This is a capacity error, not a stale-revision
or unknown server failure. A new attempt after freeing space is allowed.

## 3. Command and lifecycle state machine

| User action | Source before | Accepted product mutation | Draft mutation | After |
|---|---|---|---|---|
| Salva bozza (new) | Create Advanced/Quick | None | Insert, new ref/revision 1 | One inert Draft |
| Salva bozza (Resume) | Existing Draft | None | CAS update, revision +1 | Same Draft identity |
| Riprendi | Existing Draft | None | None until save | Full Advanced Create prefilled |
| Duplica Bozza | Existing Draft | None | None until save | Full Advanced Create, **new** Draft identity if saved |
| Duplica Activity/Event | Native subject | None | None until save | Full Advanced Create, **new** subject on Add |
| Aggiungi from Draft | Existing Draft | Create native subject | Remove old Draft after Add commits | Native subject only |
| Annulla / close without save | Any editing state | None | None | Source unchanged |
| Elimina Bozza | Existing Draft | None | Delete under exact revision CAS | Slot freed |
| Sposta in Bozze | Standalone native subject | Atomic **hard delete** | Atomic insert in same TX | Only new inert Draft |
| Declined/failed Move | Native subject | None | None | Original and facts remain |

The `Aggiungi` path reuses the same canonical Activity/Event authoring
validation and domain operations as normal Create, including date/time and
timezone rules, Life Area, Objective definitions and recap. A stored Draft
is **not** proof that its values are still valid today: missing Area,
changed revisions, invalid timezone forms, unsupported saved options or
broken references must be reported without silently truncating the request.
A failed Add leaves the saved Draft available.

**Partial success:** if native creation has committed but deletion of the
source Draft fails, the UI offers retry of **Draft removal only**. It must
never submit the already accepted Activity/Event again.

### 3.1 Authoring states: no privileged Draft mode

Saving incomplete values is legitimate: no required title, incomplete dates
or planned definitions are allowed to remain proposals. The same values must
pass normal Create validation before becoming accepted records.

Resuming a snapshot from Quick Create forces full Advanced Create; all
planned sections are editable using their normal controls. When saved
after Resume, the same Draft ref/revision advances. Duplicate of a Draft
does **not** reuse its ref or revision and cannot overwrite the source.

## 4. Content semantics

### 4.1 Life Area and appearance

A Draft can refer to an existing Life Area or propose a new one in its
advanced authoring configuration; this does not create the Area on Save.
Saved color/appearance is an intent, not a guaranteed current catalog value.
On Add, use canonical Life Area resolution, accepted revision and ownership
checks. New Area creation and its chosen color belong to accepted authoring;
a Draft is not itself a new Area. Duplicating from a native subject records
the selected existing Area identity and presentation values where supported.

### 4.2 Dates, timezones, intervals, all-day

Persist field semantics (timed, all-day, unscheduled/coarse where supported),
date, start/end, duration and time-zone choice as proposed values. No accepted
Schedule is created until Add. DST ambiguity and end-timezone restrictions
must be revalidated at Add. Multiple Activity intervals preserve their order
and obey non-overlap/time containment rules in the canonical Create pipeline.
All-day end-date is inclusive in the form; canonical stored date spans may
use an exclusive end, so conversion is deliberate.

### 4.3 Session definitions versus runtime history

A new Activity Draft may contain capture mode, Session names/order, planned
Sessions and Activity intervals; these are editable **definitions** only.
Saved Session attempts (active, paused, completed) are never copied. Runtime
controls must not appear on Vault cards and cannot start Draft Sessions.

For **Duplica from an existing Activity**, the current converter explicitly
sets `timeEnabled=false` on copied planned Sessions while preserving
names/order. This is a **known fidelity limitation**: do not claim that
scheduled clock times of these Sessions survive duplication. The E2E
acceptance suite should expose and track it. A missing reference interval
may cause a fail-closed duplication error. Child Activities are **not**
automatically flattened into Drafts.

### 4.4 Objectives and confirmed results

Definition fields (label, result kind, comparator, target/bounds, units,
verification mode) are copied into form configuration. Recorded observations,
their values, verified outcomes, progress and assessment identities are
excluded, including when duplicating an Activity/Event with historical
recordings. When moving an original, those **factual records are hard-deleted**
after explicit destructive consent. A new accepted subject must start without
inheriting old actual results.

### 4.5 Event-specific data

Event agenda lines, location, intended participants, reality mode and
supported reminders are proposed configuration. Participation history is
not a Draft fact. Agenda order matters. Events cannot own Activity Session
capture structures. Unsupported legacy/absolute time forms fail closed
rather than producing a partially specified Event.

### 4.6 Recurrence boundaries

Drafts may contain **unapplied recurrence intent**, but Save/Duplicate/Resume
cannot generate recurring instances or allocate the 730-occurence allowance.
On Add, the normal recurring Create path and its existing limits, DST,
"Mai", "Dopo X" and "Data" rules apply. Moving a **recurring source**,
generated Occurrence, materialized Routine Activity or series exception
to an ordinary one-off Draft is forbidden. The UI hides the Move action and
the backend rejects attempted bypasses. Duplication of a **selected recurring
Occurrence**, when supported by its converter, must read the selected effective
instance and its overrides, not the series head. The new draft never reuses
the old series or occurrence identity.

## 5. Move from an existing Activity/Event

**Eligible:** stand-alone owner Activity/Event only; Activity with child
Activities is excluded. Planned child Session definitions are not child
Activities, but factual Session attempts are destructive history.

**Inspector review:** clicking `Sposta in Bozze` replaces the entire
normal Inspector body (title/date, Session controls, Objectives, Agenda)
with `Spostare nelle Bozze?`, brief explanation and **Annulla /
Sposta in Bozze**. No second popup for a clean subject. Annulla restores
the Inspector and original state.

**Destructive recorded facts:** if active/paused/completed Session attempts
or recorded Objectives exist, the Move action is red and opens a
**second loss confirmation**. Its final button is
`Elimina registrazioni e sposta`. Neither initial nor secondary Cancel
writes or erases anything. Never report a clean move when such facts exist.
Events show recorded Objective risk, not Activity Session controls.

**Commit:** preview reads owner/ref, current revision and fingerprint.
Backend `POST /api/v1/temporal/drafts/move/{source_ref}` opens one
**SERIALIZABLE** transaction. It checks standalone scope, current profile
revision/fingerprint and owner; inserts the inert snapshot using the same
capacity-gated save function; runs canonical hard deletion of original
and dependents. Failure anywhere rolls back **both** the draft and deletion.
There is no client sequence of PUT Draft then DELETE Original.

On successful commit, local removal callback suppresses the original card
*before* read model invalidation. A short-lived native-subject tombstone
filters stale timed/all-day projections for the current Timeline view.
Only then does the Vault notification refresh the list. No card removal
or tombstone is allowed on API error or invalid success receipt.

## 6. Vault UI and search contract

- Vault panel attached to the Timeline actions with `Bozze` trigger and
  item count badge; separate from accepted unplaced product management.
- Compact cards show Activity/Event marker, title or fallback, proposed
  schedule label, `Riprendi`, `Duplica`, `Elimina`; **no runtime controls**.
- Full list sorted server-side by `updated_at DESC, draft_ref` and
  filtered locally; search input and header **stay fixed**. Only list body
  scrolls. Desktop body max-height: `min(440px, 100dvh - 220px)`,
  `overflow-y:auto`, scrollbars and stable gutter. Mobile panel stays
  inside viewport, no horizontal overflow.
- Search is trim/case insensitive over the **display label**. Empty stored
  title displays `Senza titolo`, and searches for `senza titolo` and
  `senza nome` find it, without changing its persisted empty title.
  A substring search also matches any actually named Draft.
- Search resets when reopening the panel, so an old filter cannot make a
  populated Vault appear empty. Empty search returns all Drafts.
- Header shows `N/100`. Search and scroll behavior must remain responsive
  at full capacity, tested with 100 mixed Activity/Event items.
- Deleting a Draft requires explicit in-panel confirmation and exact
  optimistic revision; failure keeps that Draft visible. Removing a Draft
  does not affect any accepted Activity/Event.

## 7. Error and concurrency matrix

| Condition | User-visible behavior | Data invariant |
|---|---|---|
| 100/100 on new Save | Dedicated capacity popup | Form preserved; no Draft 101 |
| 100/100 on Move | Dedicated capacity popup in review | Original + actual records intact |
| Two concurrent inserts near 100 | One succeeds, other fails or retries at server | Never exceed 100 |
| CAS stale revision `409` | Reopen/refresh message | No overwriting newer Draft |
| Stale Move fingerprint | Reopen Inspector/reconfirm | No partial transfer |
| Unavailable Area/participant | Explicit validation; edit form | No silent drop |
| Creation fails | Create error; Draft remains | No accepted native product |
| Add committed, Draft delete fails | Retry consume-only | No duplicate Activity/Event |
| Invalid success receipt | Report response as invalid | No premature local removal |
| Offline/service error | Retryable message, no false success | Keep original data |
| Attempt to Move a series/Occurrence | Action hidden; server rejects bypass | Series and its facts intact |

## 8. API and test anchors

- `GET /api/v1/temporal/drafts`: owner-scoped, no-store, full list.
- `PUT /api/v1/temporal/drafts/{draft_ref}`: CSRF, operation id,
  optional expected revision, 128 KiB / kind checks, capacity on insert.
- `POST /api/v1/temporal/drafts/move/{source_ref}`: CSRF, fingerprint
  and optional profile revision, atomic save + hard delete, owner capacity.
- `DELETE /api/v1/temporal/drafts/{draft_ref}?expected_revision=N`:
  CAS removal of inert row, no native effects.

**Unit/component:** `remote-draft-vault.test.ts`,
`timeline-draft-vault.test.tsx`,
`temporal-create-draft-vault.test.tsx`,
`vault-move-confirmation.test.tsx`,
`activity-inspector-actions.test.tsx`, `event-inspector-actions.test.tsx`,
`draft-vault-capacity-dialog.test.tsx`.

**PostgreSQL integration:** `test_draft_vault.py` verifies owner/CAS,
idempotency, atomic Move, cap/update/delete and concurrency. New quota
checks are **unverified until owner WSL Postgres tests**.

**E2E:** new separate suites must test complete UI workflows, mixed advanced
fields, real/non-auth backends where appropriate, 100-item scroll/search and
capacity, recurrence exclusion, recorded history loss and rollback. Do not
modify older E2E suites merely to satisfy the new target count.

## 9. Explicit limitations and follow-ups

The existing duplicated planned Session converter intentionally returns
`timeEnabled=false`, so scheduled Session clocks from the source are not
currently copied. Some legacy absolute/DST forms fail closed. Existing
`Da collocare` accepted native subjects **must not** silently migrate to
inert Drafts. A Draft is not a live synchronized template: editing an
accepted subject never mutates historical Drafts or duplicates.
Any unverified screenshot/real-stack observation remains an open test,
not a resolved architectural guarantee.
