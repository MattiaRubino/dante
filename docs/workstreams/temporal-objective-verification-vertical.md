# DANTE — Objective verification vertical (design and implementation contract)

Status: **IMPLEMENTATION CANDIDATE — TESTS PENDING**. The shared Create/Edit
Objective verification control, versioned persistence and source-scoped
inheritance are implemented on `feature/timeline-temporal-operational` using
migration `20261107_178`. Focused regression tests have been added, but
the new SHA has not yet passed PostgreSQL, TypeScript, browser and full gate
acceptance. Automatic assessment remains disabled without evidence sources.

## Product contract

The **Activity/Event occurrence completion** policy and **individual Objective
verification** are different facts. Completing an Activity or Event does not
prove any Objective was satisfied. Create/Edit now expose only the Objective
section and each Objective's independent verification choice. Legacy
occurrence-completion policy values remain persisted and are not silently reset
by visual changes or unrelated edits. Retiring that underlying policy requires
its own explicit Domain and persistence decision, not a frontend shortcut.

For each Objective, keep the current title field and result definition
(`Sì/No`, `Quantità`, `Intervallo`, `Qualitativo`) in the same layout and
with their established validation. To its right add **Verifica dell'obiettivo**
with the following independently configured policy:

- `none` — *Nessuna richiesta*: do not create a completion-time prompt for
  this Objective; later evidence recording remains possible.
- `review_on_end` — *Chiedi al termine*: when this concrete Activity/Event
  finishes, request this Objective's observed value. Keep stage/confirm and
  corrections distinct from the completion disposition.
- `auto_if_evidence` — *Valutazione automatica*: only when a supported,
  authoritative observation source can produce the actual value. Never
  synthesize a measurement, infer success from elapsed time, or confirm an
  Objective solely because its Activity/Event ended. Hide or disable this
  choice while the Objective has no valid source/capability.

**Do not reuse `auto_confirm_outcome`** as an Objective-level code. It is an
Activity/Event completion policy with different semantics.

The Objective rows use one shared renderer in Advanced Create, one-off
Activity Edit, one-off Event Edit, local occurrence Edit and recurring-series
Edit. Every row has the title and order/delete actions at top, current
result fields below left, verification policy below right, and the unchanged
`+ Aggiungi obiettivo` control beneath the ordered list. Keep an orderly
scaletta-style connecting spine for multiple Objectives. No duplicated help
paragraphs or `nessun risultato registrato` inside definition authoring.
On narrow *container* widths (not just screen widths), stack the result and
verification regions; do not arbitrarily wrap Unit while there is room.

## Canonical persistence and editing contract

`temporal_objective` is the Objective identity. Its definition revisions,
observations and evaluations are *not* the same as verification policy.
Persist Objective verification policy with its own versioned, owner-scoped
state and replay-safe operation identity, consistent with the repository's
CAS/serializable, SECURITY DEFINER and audit rules. Add API fields to Create,
list, definition/edit snapshots and recurring templates. No view-only field
that is silently discarded by Save is acceptable. Existing Objectives
default to `none` without changing historical facts.

- **One-off Create/Save:** mode for every new/updated Objective persists
  with the Objective edit in the enclosing authoring/aggregate transaction
  or its existing idempotent post-create finalization. The same operation ID
  must not replay under changed intent.
- **Solo questa:** update only the selected Objective instance's verification
  policy. Keep the source template, earlier/later occurrences, observations
  and evaluation history unchanged.
- **Questa e le prossime:** include the selected instance and all applicable
  later unprotected instances. Use the existing recurrence edit coordinate,
  canonical template-slot lineage, source-revision CAS and impact preview.
  Do not apply new policy retroactively to earlier occurrences; do not touch
  a future occurrence with protected/recorded facts without the existing
  conflict/review semantics.
- **Event first physical instance:** preserve its existing source Event
  identity; do not transform it into an unrelated Occurrence. Handle the
  legacy-first binding explicitly in policy reads and edits.
- **Newly materialized future occurrence:** inherit the effective policy
  revision for that occurrence's coordinate, not the latest source JSON for
  all dates. Materialized and nonmaterialized future instances must agree.
- **Recorded Objective:** existing Observation/Evaluation is immutable.
  A verification-policy edit does not erase, fabricate or re-evaluate facts
  by itself. Correction is a separate explicit operation.

The current `reality_review_policy` controls occurrence completion and is
not to be replaced or overloaded for individual Objective configuration.

## Existing implementation boundaries

- UI shared definition row:
  `apps/web/src/features/temporal-create/ui/temporal-objective-editor-row.tsx`;
  currently reused by `temporal-create-objectives.tsx`,
  `activity-objective-row.tsx` and recurring series Edit.
- Current completion policy:
  `temporal-create-reality-objectives-section.tsx`,
  Activity and Event editors, and `recurring-series-editor.tsx`.
- Create and finalization:
  `temporal-create-u2-submit.ts`,
  `temporal-create-reality-finalizer.ts`,
  `remote-recurring-authoring.ts`.
- REST application and Objective revisions:
  `apps/backend/src/dante/modules/temporal/reality_objective_api.py`.
- Canonical immutable Objective definition and recurring revisions:
  `20261008_125_b14_objective_corrections.py`,
  `20261008_126_b14_scoped_objective_definition.py` and newer scoped
  objective/recurrence migrations.
- Runtime Objective recording:
  `apps/web/src/features/temporal/objective-controls.tsx`.

Objective-level verification is backed by independent local revision and
accepted series history, with owner-scoped capabilities and transactional
Create/Edit saves. The existing Reality completion policy is unchanged.
Review-queue prompts require an unobserved Objective configured for
`review_on_end`. This is implementation status, **not test certification**.

## Mandatory acceptance and test matrix

1. New individual Activity and Event Objectives: all supported result kinds,
   all available review modes, save/reload/duplicate-safe operation replay.
2. Existing one-off Activity/Event: change only review mode, change both
   definition and review mode, stale CAS conflict, correct preservation of
   recorded Objective results.
3. Routine/Event recurrence: first physical source, selected Occurrence,
   `Solo questa`, `Questa e le prossime`, protected/recorded future item,
   DST and historical-coordinate boundaries, materialization before/after
   policy edit, no retroactive policy leakage.
4. Completion runtime: per-Objective prompts only for `review_on_end`,
   no invented auto-observation, independent Activity/Event completion truth,
   draft/confirmed result/correction behavior.
5. UI contract: same renderer and spacing in Advanced Create, Edit Activity,
   Edit Event and recurring-series Edit; no overflowing quantity/range fields
   on a 1040px modal, correct container-query fallback, keyboard/A11y labels.
6. Database: fresh/migrated schema head, Alembic drift, ownership/GRANT,
   dictionary and generated OpenAPI/client drift, source fingerprint replay.
7. Execute focused backend and Web suites plus real-browser acceptance first,
   then the repository's same-SHA 27-group parallel gate.

**Release gate:** do not mark the Objective verification vertical complete
until all of the above are verified. Do not run the full gate merely to certify
this design document.
