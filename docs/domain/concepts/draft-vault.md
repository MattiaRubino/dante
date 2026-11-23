# Draft Vault — Bozze (B14 candidate domain contract)

**Status:** B14 operational contract; standalone Activity/Event destructive move requires owner-local PostgreSQL, UI and browser acceptance on the final commit.
**Date:** 2026-10-09
**Source workstream:** `feature/timeline-temporal-operational`

## Meaning

A **Draft** is a stored, inert configuration under the author's own scope, not an Activity,
Event, Routine, Occurrence, Schedule, Session, Actual, or Observation. A draft is like a
**cassaforte**: it records what the user may decide to insert later. Simply storing,
opening, or duplicating it must not reserve time, create accepted product subjects,
start an execution, notify, or generate recurrence occurrences.

A draft may contain *proposed* dates, planned Sessions, Objectives, Life Area,
reminders, or participant intent. These are only form values, **not accepted
operational facts**. That remains true even when the form is complete.

Current supported draft types are Activity and Event. Timer and Alarm are future
draft kinds, not prematurely supported or activated.

## Commands and transitions

- **Save draft:** persist one versioned snapshot of the shared Quick/Advanced
  Create form, even if partly filled. This does not invoke product authoring.
- **Resume:** open the same Create editor and exact saved field configuration.
  Save revisions under optimistic concurrency control.
- **Duplicate:** open the same configuration with a new draft identity; the
  source draft stays in the vault.
- **Add:** explicitly author the chosen Activity/Event through existing accepted
  domain commands; consume the source draft only after successful authoring.
  Never replay creation if only draft consumption failed.
- **Delete:** remove only an inert draft owned by the actor under exact revision.
- **Duplicate an existing Activity/Event:** opens the existing Create composer
  with a clean configuration. Selecting **Salva bozza** there copies it into
  the Vault without changing the original. The separate **Copia in Bozze**
  Inspector command is removed, not merely hidden.
- **Move an existing standalone Activity/Event:** only after an explicit
  centered destructive confirmation. The owner-scoped backend command
  atomically saves the inert snapshot **and hard-deletes the original native
  subject, Sessions, recorded attempts, Objective Observations/Results,
  execution/participation facts and other dependent historical records**
  using the same canonical deletion routine as **Elimina definitivamente**.
  The draft preserves the planning, definitions, Area, intended participants
  and recurrence settings only; it never includes live timers, attempts,
  actual result values or accepted progress. The original disappears from
  Timeline and the saved configuration appears in Bozze.
- **No partial transfer:** preview captures current owner, revision and
  destructive CAS fingerprint. The backend verifies them in the same
  SERIALIZABLE transaction as Vault save and canonical hard-delete. A stale
  source/Session fingerprint, failed permission check or SQL error rolls back
  both writes: **no orphaned draft and no partial deletion**. Cancel makes
  no write; a failed confirmation leaves the original available for review.
  An Activity with child Activities is excluded until a graph-preserving move
  is explicitly designed. Planned child Sessions are not Activity children
  and remain part of the draft's planned configuration.
- **Active/paused/completed and recorded facts:** never a silent move.
  The centered popup clearly warns that all active/paused/completed Sessions
  and recorded Objective results will be permanently removed if confirmed.
  For Event it warns about recorded Objective/participation facts without
  introducing Activity Session controls. The action is allowed even when
  these facts exist because it is an explicitly confirmed **hard deletion**,
  not the historically guarded **retire** command.
- **Recurrence guard:** hide **Sposta in Bozze** for a recurring source,
  individual generated Occurrence and materialized Routine Activity; owner
  backend checks fail closed even if a client bypasses the UI. No recurrence
  source, occurrence, exception or already-accepted historical record is
  repackaged as an ordinary single draft.

## Coexistence with existing “Da collocare” data

The preexisting planning tray contains real, canonical Activity/Event identities
without accepted placement or with postponement history. Such rows **cannot be
reclassified as inert drafts just by renaming the UI**. Preserve these records
and all underlying Schedule/Actual facts. Any conversion to drafts requires an
owner-authoritative move and appropriate historical veto; no automatic bulk
migration of product rows into vault storage.

## Structural constraints

The vault occupies the existing Home actions/panel ownership. It must not
change Home H0 geometry, Timeline data invariants, or M5 Activity editing.
Do not add a new template system, auto-reuse semantics, or synchronizing live
instances with their source draft.

## Acceptance

PostgreSQL Dictionary/ACL/CAS and migration; API schema/CSRF; Quick and
Advanced Save; durable reload; resume/edit; duplicate (source retained);
explicit Add and consumption; deletion; legacy canonical records preserved;
historical veto; no operational creation until confirmation; real-app
screenshots. Unproven points remain open, never relabeled CLOSED.

**Legacy access:** canonical unplaced/postponed records remain accessible through a distinct ‘Elementi già creati’ placement manager launched from the Bozze panel; its controls do not operate on inert drafts.
