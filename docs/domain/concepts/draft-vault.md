# Draft Vault — Bozze (B14 candidate domain contract)

**Status:** B14 source branch candidate, user-defined semantics, pending PostgreSQL and real-app acceptance.
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
- **Move an already-created Activity:** build a new snapshot, then retire the
  original using the canonical guarded owner capability; a history/series/child
  veto protects facts. On failure, remove the staged snapshot or present a
  concrete double-presence warning if rollback cleanup also fails.
- **Already-created Event:** there is currently no equivalent owner-scoped,
  history-safe Event retirement. Copy into vault is possible but **must not be
  mislabeled as Move**; retirement requires a separate accepted capability.

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
