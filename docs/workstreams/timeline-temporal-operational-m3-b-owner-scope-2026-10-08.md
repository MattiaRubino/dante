# DANTE B14 / M3-B — owner-domain edit scope, temporal forms and UI integrity

Date: 2026-10-08. Source of truth: `feature/timeline-temporal-operational`, revision `20261008_127`. **This is a bounded current-state/negative-guard design record, not a claim that recurring propagation is implemented or that the M3-B new tests have passed.**

## Established source contracts

1. Domain: `docs/domain/concepts/activity.md`, `occurrence.md`, `recurrence.md`, `schedule.md`, `session.md` and `docs/database/activity-subactivity-session-contract.md`. Routine, Recurrence, Occurrence, Schedule, Session and Actual are different identities. A recorded fact cannot be erased by renaming a planned Session. A moved/skipped/generated Occurrence retains identity independent of its current timestamp.
2. **Already verified M1:** `20261008_123_b14_occurrence_profile_edit.py` source-locked, idempotent, bounded selected/future edits of title/description/location/color, with source recurrence CAS; future materialization reads `get_self_occurrence_profile_patch`.
3. **Already verified M2:** `20261008_126_b14_scoped_objective_definition.py` stable generated template-slot policy; selected/future definitions are read through source policy and new future materializations inherit edits without synthesizing recorded Observations.
4. **Already verified M3-A:** `20261008_127_b14_m3_residual_editor.py`: primary Life Area can be explicitly unassigned on an owned Activity/Event with durable revision/operation replay; a *planned* Activity Session's `activity_schedule_role.display_name` may be revised with expected-name CAS on the same `schedule_ref`; retirement refuses historical Session/Actual/Objective facts.
5. **Existing Reminder and core settings:** `activity_edit_snapshot_api.py` owns capture/reality/reminder core mutations, `schedule_reminder_api.py` owns typed Schedule Reminder state, and `activity_replan_api.py` owns coordinated interval/planned-Session replan. Do not introduce parallel APIs for already-covered commands.

## Exactly where source-derived recurring scope is missing

| Field | Individual accepted mutation | Source policy for selected+future | Future materialization source |
|---|---|---|---|
| Title, description, location, color | Activity profile | M1 verified | `get_self_occurrence_profile_patch` |
| Objective definition | Logical Objective revision | M2 verified using stable objective template slot | M2 effective source-policy reads |
| Primary Life Area | `assign_self_activity_life_area` / Event analog, owner/CAS | **Not implemented.** A naive per-instance loop is not atomic and cannot cover future unmaterialized instances | Routine Activity materializer currently reads `life_area_ref` from `list_self_routines`; Event has its own owner model |
| Planned Session display name | `revise_self_planned_session_name` on existing Schedule role | **Not implemented.** Needs trusted template-root planned-slot provenance; `presentation_order` alone is not proof of origin, and child planned Sessions are distinct | Routine materializer currently creates names from `routine_occurrence_policy.activity_template.planned_slices[].name` |
| Capture / Reality / Reminder / Schedule | Independently owned guarded edit & temporal capabilities | **No general generated-series command proven**; keep selected-only rather than suggesting future coverage | Routine/Event policy and checkpoint paths have separate truth and must not be rewritten by a local save |

A correct future M3 source edit must prove owner and generated provenance, serialize under source/recurrence authority, CAS accepted source policy, check the complete bounded M1 inventory, reject protected future Actual, Observation, individual override, skip and Schedule/Session exceptions, and append an immutable policy receipt. Scope must always include the clicked item and only later *future* compatible instances; other past instances must not change. New future generated instances must inherit accepted policy through checkpoint/materialization. Any bulk DML/loop of individual HTTP mutation endpoints is **not** a substitute.

## M3-B implemented fail-closed UI improvements (new, pending user test)

- `activity-edit-panel.tsx` treats a planned Session's *unsaved display name* as an independent dirty state. Both general save and replan preview/apply are disabled until the name is saved or discarded; a successful replan resets planned-name draft baselines.
- For generated recurring Activities the scope radio is visible for metadata, Life Area or planned Session name edits. For *only owner-domain* drafts the unsupported `Questa e le prossime` choice is disabled with a direct explanation, while `Solo questa` retains its already-verified API path. A mixed recurring profile/domain draft does not quietly save half the changes.
- Unsupported Schedule temporal forms (other than existing supported local interval shapes with full coordinates) receive an explicit non-conversion message. A planned Session's label can still be changed without moving its Schedule.
- A `temporal.activity_profile.recorded_truth` retirement 409 gives a specific explanation and never invalidates Timeline as if deletion succeeded.
- Vitest additions cover unsaved name loss, name/replan conflict, owner-domain-only recurring scope, unsupported absolute form and historic-truth refusal.

## Open M3-B source-policy work and acceptance

**Not complete:** actual atomic source/template following-scope for primary Life Area and stable planned Session name; all recurrence owner parity and guarded future-checkpoint inheritance; any missing temporal policy edit surface after a complete owner inventory. These require schema/API/ORM/Dictionary integration and PostgreSQL coverage, not just an enabled button. Until then, following-scope cannot be advertised as supported for these fields.

**Current gate to run only after code changes:** Web typecheck + focused Vitest for the new UI guards and remote error mapping, with existing B14 M1/M2/M3-A regression where impacted. No database revision from this bounded UI hardening; exact schema remains `20261008_127`, `234/5/208/103/477/414/586`. User runs all tests locally in `~/projects/dante`; no GitHub Actions or CI. M4 Event Inspector and faithful Duplica, M5 real-app acceptance and B15 remain open.

## 2026-10-08 — M3-B user local gate and Web test repair (pending rerun)

User pulled `71117ae5` and ran consolidated `/tmp/dante-m3b-gate.qlpPBc` on `~/projects/dante`. **Verified green locally:** `SYNTAX=0`, `RUFF=0`, `POSTGRES=0` (including the new negative-future-checkpoint test plus M2/M3-A regressions and exact DB catalog), `GENERATED_CHECK=0`, `API_TYPECHECK=0`. **Two Web-only failures:** `WEB_TYPECHECK=2` (`activity-inspector-actions.test.tsx:662`: array index `getAllByLabelText('Inizio')[0]` typed `HTMLElement | undefined` under strict no-unsafe-index) and `VITEST=1` (35 passed, one test failed at :717 because selected-only Life Area was *already* correctly preventing `this_and_following` and showing the general "Life Area e nomi delle Session pianificate si salvano soltanto per questa istanza" explanatory paragraph, whereas the test incorrectly expected the conditional warning shown only after an unsupported scope selection). This is **not** a PostgreSQL/schema regression.

**Code correction published:** `23daae86`, only `apps/web/src/features/home/ui/timeline/activity-inspector-actions.test.tsx`. Add explicit nonnull array index for first `Inizio` input (the Testing Library `getAllBy...` contract throws if there are zero elements) and assert the exact, reachable selected-only scope guidance. The guarded UI behavior, persistence, recurring source policy and DB code are unchanged. Remote HEAD verified at `23daae86029462c33213070ca855cb72e2e44aa8` before this documentation update. **Next action:** user runs just `pnpm --filter @dante/web typecheck` and the four M3-B focused Vitest files after `git pull --ff-only`. No reason to re-run passing PG and generated-client checks for this test-only change; no regenerated client needed. **M3-B guard subvertical NOT closed until local Web recheck passes.** This does not close the separate, unimplemented source/template `Questa e le prossime` policy for Life Area/planned Session names; full M3, M4/M5 and B15 still OPEN. No CI/Actions.
