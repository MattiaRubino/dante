# B11 — Final real-app acceptance gate

- **Date:** 2026-09-27
- **Branch:** `feature/timeline-temporal-operational`
- **Status:** REMEDIATION PUBLISHED; user-run real-app walkthrough must restart
- **Entering frontier:** B11-A/B/C/D CLOSED / PROVEN; `_86` exact catalog and automated integration gate passed locally
- **Exit:** close parent B11 only after observed acceptance is recorded

This is the single product walkthrough for B11, after B11-D. Use the local disposable harness and a real authenticated Home/Timeline/Create surface. PostgreSQL remains the canonical authority; check persisted behavior after reload. No GitHub Actions/CI.

## 2026-09-28 observed Create boundary

The first real-app attempt exposed a Create defect: a recurring Event with `Senza Life Area` was allowed to reach `Aggiungi`, then failed only with the generic message `Non è stato possibile applicare la creazione. La bozza è ancora qui.` Recurring Event/Routine authoring requires a canonical Life Area. The app now blocks submission before any backend call, focuses `Life Area` and displays: `Per creare una ricorrenza, seleziona una Life Area.` The first walkthrough attempt is therefore not an acceptance result; use a real Life Area for each recurring Event/Routine in the rerun.

## Start the isolated app

From the user's local worktree:

```bash
cd ~/projects/dante
git pull --ff-only origin feature/timeline-temporal-operational
export DANTE_E2E_CONTROL_ID=temporal-b11-realapp
uv run --project apps/backend python tooling/run-access-auth-stack.py
```

Wait for the harness to report ready, then open `https://127.0.0.1:4173` and sign in with the synthetic harness account (`synthetic.user@example.com`, password `correct horse battery staple`). The local certificate is self-signed. The harness manages a disposable database; keep it running throughout the walkthrough.

## Observe and report

1. **Advanced Recurrence (B11-A).** Use a self-owned Routine or Event and its Occurrence in Timeline. Configure completion-relative and anchor-stream-relative recurrence where the product controls expose them. Verify that an explicit qualifying Actual/anchor produces the dependent Occurrence and replay or reload does not duplicate it. Verify that absence of a qualifying Actual does not fabricate completion-relative history. Recurrence controls should address the typed Routine/Event source while Actual controls address the Occurrence.
2. **Conditional behavior (B11-B).** On a self-owned Activity, Event, or Occurrence, configure an `actual_realization` Condition. Evaluate before an Actual: expect `indeterminate/withhold`. Record an explicit Actual and evaluate again: expect `satisfied/allow` with evidence tied to the exact realization MaterialState. Correct Actual and verify the earlier evaluation remains historical evidence, not silently reinterpreted; evaluation must not create or mutate Schedule/Actual implicitly.
3. **Personal Schedule Reminder (B11-C).** Create an admissible exact-start Schedule with Reminder intent, then inspect its derived due state on Timeline. Reload, revise or withdraw the Schedule, and verify the reminder derives from the accepted Schedule and becomes unavailable when its exact start is unavailable. Configure/disable from an existing Schedule. If Create reports partial success after subject/Schedule creation, retry the reminder configuration and verify the subject is not duplicated; report whether this branch was actually exercised.
4. **Cross-capability chain (B11-D).** On the same Routine/Event → Occurrence path, observe the Condition, accepted Schedule and Reminder, then record Actual and reevaluate. Reload and switch between subjects. Verify the selected Occurrence's Actual/Condition and the source Routine/Event's Recurrence stay distinct; Reminder and Condition do not silently mutate one another or replace canonical PostgreSQL state.

Report each numbered observation as pass/fail/not exercised and include the first visible error or unexpected behavior. In particular, state whether Create partial-success retry and anchor-stream recurrence were exercised. A capability that the current UI cannot reach is an open acceptance finding, not an assumed pass. Close B11 only after reviewing those observations and recording the final result in roadmap, map, handoff and B11 closure evidence.
