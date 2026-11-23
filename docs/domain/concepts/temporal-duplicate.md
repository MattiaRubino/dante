# Temporal Duplicate (Duplica) — source-to-Create contract

**Scope:** Duplicate from accepted Activity/Event, duplicate an inert Draft,
resume a Draft, and save or submit the resulting Advanced Create form.
**Canonical companion:** [Draft Vault](./draft-vault.md).
This is a *configuration copy*, not a copy of accepted identity or historical
facts. The active Timeline branch is `feature/timeline-temporal-operational`.

## 1. Definition and command distinction

`Duplica` means **read source configuration, prepare a new Advanced Create
form, then let the user explicitly choose Salva bozza or Aggiungi**.

It does **not** automatically save the new Draft, create a new Activity/Event,
restart a Session, allocate recurrence occurrences, or remove the source.
`Sposta in Bozze` is a separate destructive command; do not implement
Duplicate as a Move or vice versa.

| Origin | Result of Duplica click | First persistence |
|---|---|---|
| Accepted standalone Activity | Full Advanced Create, prefilling supported Activity configuration | User chooses Add or Save Draft |
| Accepted standalone Event | Full Advanced Create, prefilling supported Event configuration | User chooses Add or Save Draft |
| Selected recurring Event Occurrence | Full Advanced Create from **effective selected occurrence** where supported | New independent identity only |
| Recurring series source | Guarded; must use a supported selected instance scope | No silent flattened series |
| Existing inert Draft | Full Advanced Create; no old Draft identity inherited | User Save creates **new** Draft |
| Quick Create partially filled form | `Salva bozza` persists proposal | Resume later opens **full** Advanced Create |

`Riprendi` is different from `Duplica Bozza`: Resume retains the Draft
ref/revision for subsequent Save; Duplicate creates a new Draft ref only if
user saves it. Both must show **the same** Advanced Create controls and
validation rules.

## 2. Source of truth, identity and side effects

### 2.1 Read path

- Activity: `ActivityInspectorActions` requests saved
  Activity profile and Edit settings, including selected Life Area, stored
  interval/planned-Session schedules, capture/reality policies and Objective
  definitions. Converter:
  `buildActivityDuplicateSeed(profile, settings)`.
- Event: `EventInspectorActions` reads canonical Event details, selected
  schedule/placement, Event agenda, expected participation and person display
  labels, reality mode, Objective definitions and supported reminder.
  Converter:
  `buildEventDuplicateSeed(event, placement, participants, reality,
  objectives, reminder)`.
- For a selected recurring Event occurrence, resolve occurrence context
  and local overrides; never accidentally load the source head as the
  effective requested instance.
- Compose `TemporalCreateFieldSeed` with default Create fields using
  `applyTemporalCreateFieldSeed`; merge supported `advanced` values into
  the normal `TemporalCreateU2AuthoringDraft`. Reopen the **full**
  `TemporalCreateComposer`, not a duplicate-specific editor.
- For `Sposta in Bozze`, seed-to-snapshot conversion may be used, but the
  subsequent owner confirmation and hard delete are a **different backend
  action** with its own eligibility and CAS requirements.

### 2.2 Identity invariants

Source `activity_ref`, `event_ref`, Series/Occurrence identifiers,
Schedule refs and revisions, Session attempt refs, observation refs and
current execution state are **not new identity seeds**. User requests for
Add get new canonical refs under accepted authoring. Source cannot be
modified simply by editing a duplicate form; Cancel does not write.
The new accepted item and original are independent: later edits do not
synchronize them or modify any historical Draft.

### 2.3 Runtime truth is not duplicable

Do not copy active/paused/completed Session attempts, actual work duration,
Objective observed values/assessments, participant attendance,
notifications already delivered, real completion state, inspection/verification
history, or temporal migration history. Preserve supported **definitions**
so user can configure fresh operational behavior on a new subject.
No copied user-visible card is executable until Add commits.

## 3. Activity fields and structural mapping

| Field group | Duplicate form behavior |
|---|---|
| Title | Prefill existing accepted title; user may change before Add |
| Notes / location | Copy descriptive values |
| Life Area | Reference existing Area and its accepted style where available; revalidate if stale |
| Item color | Copy supported color intent; not historic runtime color |
| Time / date / zone | Derive from accepted primary interval/envelope, or all-day span |
| Activity intervals | Sort by canonical order, convert to dated local windows |
| Planned Sessions | Copy names/order; treat as **definitions**, never actual attempts |
| Capture/reality mode | Copy supported policy fields into new Advanced Create |
| Objectives | Copy labels, comparator, target/bounds, units and verification mode only |
| Reminder | Copy configured lead time if supported |
| Child Activities | **Not** duplicated as an Activity subtree |

### 3.1 Interval selection and placement

Select saved `role='interval'` schedules sorted by `order`. If none,
use the `envelope` or lone uncategorized schedule. The primary window
initializes form date/start/duration/time mode. Remaining intervals become
additional `activityIntervals` form records, with **new client ids**.
The canonical Create validator must check end-after-start,
containment and no overlaps.

A local window requires valid `start`/`end`,
`floating_local` or `named_zone_local` temporal form, and positive
duration. If intervals have mismatched form/zone, **fail closed** with the
existing "intervalli hanno fusi diversi" error rather than guessing.
A date-span envelope mixed with time intervals is refused. All-day
`date_span` uses the accepted exclusive end converted to the form's
inclusive end.

No accepted source Schedule ID is reused as an identity for a duplicate.

### 3.2 Session definitions (important fidelity boundary)

The current `buildActivityDuplicateSeed` maps planned schedules by order,
preserves their names (or generated `Sessione N` fallback) and supplies
**`timeEnabled:false`**, so copied named Sessions are **unplaced** by
default. Their source clock times are *not* reconstructed. This is an
explicitly known limitation to expose in tests; do not describe it as
preserving all clock settings.

The new Activity can still define capture mode, edit/assign times,
start independent Session attempts after Add and use the original
Activity/Session control rules. No historical attempts migrate.
When planned schedules exist without an accepted reference envelope,
the converter refuses a false "successful duplicate".

A fully all-day Activity can contain independent *unplaced* named Sessions;
preserve their names and order without inventing times.

### 3.3 Objective definitions

Each supported Objective receives a fresh local form id and copies:
`label`, `resultKind`, `comparatorCode`, `targetValue`,
`targetMin`, `targetMax`, `unitCode` and `verificationMode`.
Confirmed `observationRef`, observed number/boolean/text, assessment and
verification truth are **not** copied. Creating a new Activity applies
canonical Objective definition validation and saved targets; it must never
recreate the original's completed results.

## 4. Event fields and placement mapping

Event copying includes accepted title, notes, location, Life Area reference,
item color, Event agenda lines, intended participants, reality policy,
Objective *definitions* and supported reminder lead time.

- **Date span:** validate exclusive end > start; convert to inclusive
  `allDayEndDate` in Create. Agenda order must not change.
- **Coarse period:** preserve date and `coarsePeriod` where supported.
- **Named-zone local:** preserve local start, duration, zone and verified
  DST disambiguation. Check that resolved instants actually agree with the
  original placement. If contradictory DST choices would be needed,
  **reject** rather than silently choosing earlier/later.
- **Floating local:** preserve local times and duration without introducing
  a named zone.
- **Absolute UTC:** currently **rejected by the converter**: no automatic
  lossy translation into zoned Create.
- **Precision:** the converter only accepts whole-minute zero-subsecond
  times and positive safe integer duration. Invalid precision is a user-
  visible fail-closed result.
- **Participants:** each expected participant must resolve to a current
  person/display label; missing referents fail closed, not silently removed.
  Attendance *history* is never copied.
- **Session boundary:** Event drafts must keep Activity Session structure at
  its disabled/default values; don't attach Activity capture or planned
  Sessions to Events.

Saved Event duplicate does not preserve a recorded Objective value, attendance
fact, existing Event accepted Schedule ref, Recurrence identity or permission
to change the original.

## 5. Draft duplication, editor transitions, and persistence

For `Duplica Bozza` the source is already `DraftVaultSnapshot`, so avoid
converting it through accepted Activity/Event read models. Rehydrate
`fields` and `advanced` exactly as saved, forcing the full Advanced
Create surface; do not use the stored `surface` to open Quick Create.
The selected Draft's `draft_ref` and revision are **not** assigned to
the new form. The source remains in the Vault unchanged.

For `Riprendi`, retain `draft_ref`, revision and current snapshot; Save
performs CAS on the same Draft. For both, Add is the standard accepted authoring
path; only after it commits may it consume the source Draft. A failed
Add preserves the source Draft. A failed consumption after accepted Add
offers deletion-only retry, not another Add.

Saving a duplicated form creates one new inert Draft and consumes **one**
of the owner's 100 Draft slots; opening/cancelling does not. At 100/100,
the server responds `409 temporal.drafts.capacity`. The capacity popup
must not erase form input; saving a resumed existing Draft remains legal.

### 5.1 Separation of Copy, Move and Delete

| Operation | Original | Runtime history | New accepted subject | Vault capacity |
|---|---|---|---|---|
| Duplica, then Cancel | Unchanged | Unchanged | None | None |
| Duplica, then Save Draft | Unchanged | Unchanged | None | +1 |
| Duplica, then Add | Unchanged | Unchanged | New native ref | None |
| Riprendi, then Save | Existing Draft updated | N/A | None | Unchanged |
| Riprendi, then Add | Draft consumed if possible | N/A | New native ref | -1 |
| Sposta in Bozze | **Hard deleted after consent** | **Hard deleted** | None | +1 |
| Elimina Bozza | No native effect | N/A | None | -1 |

This table is normative for UI, backend, and tests: never interchange the
semantics because both paths prefill the same Create form.

## 6. Recurring source / occurrence and series rules

A recurrence is not a stack of independent one-off accepted objects.
A generated occurrence can carry effective local exceptions. The selected
occurrence must be read under correct source scope and current revision.
On the currently supported Event path, an insufficient occurrence context
results in an explicit error; series source cannot be implicitly duplicated
as a one-off without supported resolution.

`Sposta in Bozze` never applies to a recurring source/Occurrence/Routine
instance even if its Inspector otherwise offers Duplica. A **new** Draft may
contain *recurrence intent*, but saving that intent does not generate actual
occurrences; Add activates normal Series rules (including 730 chunking
when relevant).

Scope editing rules `Solo questa` and `Questa e le prossime` apply to
accepted recurring products, not a Draft stored in the Vault.

## 7. Atomicity, stale source and error discipline

- Duplicate is read-only until an explicit Save Draft or Add; no partial
  native command is allowed during inspection or conversion.
- If source local intervals are incompatible, schedule precision unsupported,
  participant referent missing, Life Area stale or recurrence/occurrence scope
  unresolved: show a concrete error, keep original and allow user correction.
- `Sposta` adds an independent destructive path: fingerprint/CAS preview,
  conditional red warning, second confirmation for actual facts and one
  serializable save+hard delete. Neither a failed capacity check nor a
  stale fingerprint may partially delete the original.
- CAS on saved Draft protects concurrent editors. Event/Activity own
  revision and fingerprint scopes must not be inferred from a Draft's ref.
- A persisted Draft's jsonb object-key order is not semantic: canonical
  authorization and validation compare field values structurally.
- No retries that re-create already accepted products after a later Draft
  removal failure.

## 8. Test matrix and known evidence

**Focused unit tests** cover seed field conversion, Event DST/absolute/coarse
cases, Activity intervals and planned Session labels, and form/CAS behavior
in corresponding `temporal-create`, `activity-inspector-actions` and
`event-inspector-actions` suites.

**PostgreSQL** `test_draft_vault.py`: owner ACL, revisions/replay, Move
atomicity, 100 Draft cap, one-user concurrency, update and deletion capacity.

**New E2E (separate suite, untouched originals):**
Activity→Duplicate→Draft→Add; Event→Duplicate→Draft→Add;
mixed Area/time/Session/Objective config; recurring exclusion;
100 mixed Drafts and search/scroll; Draft Resume/Duplicate/Delete;
recorded Session/Objective hard Move; Event recorded outcomes;
stale fingerprints, quota and rollback. Read accepted backend state
where tests have access, not only transient success toasts.

**Known gap:** scheduled planned-Session times are not recreated in duplicate
seeds. Track any discovered incompatibilities as explicit open issues;
do not silently change validation to obtain green tests.

**Acceptance:** Complete only after typecheck, focused unit/PostgreSQL,
new E2E, owner browser review and relevant documentation agree. Earlier
passing runs are evidence only for their specific commit.
