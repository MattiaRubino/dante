# Timeline / Temporal-Operational — B01 isolated `userTest`

- **Status:** READY FOR MANUAL EXECUTION — NOT YET APPROVED
- **Workstream branch:** `feature/timeline-temporal-operational`
- **Purpose:** manual B01 Activity acceptance only
- **Data class:** disposable synthetic test data; never personal/production data

## 1. Why this exists

B01 requires a manual product-surface proof that the real `+` path creates one canonical unplaced Activity, that the same Activity survives reload through the real read path, that discarding a draft does not delete canonical data, and that a real backend/database failure is shown as failure rather than fake success.

The protocol reuses the accepted Access/Auth full-stack harness:

```text
production web build
→ HTTPS Vite preview
→ real FastAPI
→ real dante_runtime role
→ fresh migrated PostgreSQL 18.6
→ synthetic account only
```

The database/container is disposable and exists only for the run.

## 2. Preconditions

Run from the repository root with `feature/timeline-temporal-operational` checked out and clean.

The candidate must include the B01 `_19` Activity schema and its reconciled Database Dictionary/current-catalog gates. Automated proof is evidence for readiness; it does **not** replace this manual protocol.

The canonical PostgreSQL image must already exist. If it does not, build it once with:

```bash
docker compose -f infra/compose/local.yaml build postgres
```

Do not point this protocol at a normal local DANTE database, staging or production.

## 3. Start the isolated stack

Use one control id for the entire manual run:

```bash
export DANTE_E2E_CONTROL_ID=temporal-b01-usertest
uv run --project apps/backend python tooling/run-access-auth-stack.py
```

Wait for the full-stack-ready message, then open:

```text
https://127.0.0.1:4173
```

The local certificate is intentionally self-signed.

Synthetic credentials:

```text
email:    synthetic.user@example.com
password: correct horse battery staple
```

## 4. Manual proof A — canonical Activity create and reload

1. Sign in with the synthetic account and open `/home`.
2. Press the **Timeline `+`** (`Aggiungi alla timeline`), not any unrelated add control elsewhere in Home.
3. Verify `Attività` is selected by default.
4. Verify the Activity is on the `Da collocare` path and that no editable `Durata prevista` / `durationMinutes` control is exposed for this B01 canonical path.
5. Enter a unique title, for example `B01 manual canonical activity`.
6. Press `Aggiungi` once.
7. Open `Attività da collocare` / Planning Tray.
8. Verify exactly one card with that title exists and that it is not rendered as a Timeline Event.
9. Reload the browser.
10. Open Planning Tray again.
11. Verify the same Activity is still present exactly once.

Expected semantic result:

```text
one accepted CreateActivity
→ one canonical Activity identity
→ unplaced Planning Tray projection
→ reload/refetch preserves the same Activity
→ no duplicate projection
```

B01 intentionally does **not** author canonical estimated effort. A visible duration on an unplaced Activity would imply persistence that B01 does not yet provide. Estimated effort remains a future Activity capability and must stay distinct from future Schedule duration and from Session/Actual duration.

Do not place the Activity on the Timeline in B01; real Schedule mutation belongs to B02.

## 5. Manual proof B — dirty draft discard is not Activity deletion

1. With proof A's canonical Activity still present, open the Timeline `+` again.
2. Type a different title, for example `B01 draft da scartare`.
3. Close/discard the Create surface without submitting.
4. Reopen Planning Tray.

Expected result:

- no Activity named `B01 draft da scartare` exists;
- proof A's canonical Activity still exists exactly once;
- discarding local draft state does not delete/cancel an already canonical Activity.

Canonical boundary:

```text
draft discard
!=
Activity delete/cancel
```

## 6. Manual proof C — real create failure remains failure

Keep the stack running. In a second terminal use the same control id:

```bash
export DANTE_E2E_CONTROL_ID=temporal-b01-usertest
uv run --project apps/backend python tooling/access-auth-e2e-control.py database-stop
```

Back in the product UI:

1. open the Timeline `+`;
2. keep `Attività` selected on the `Da collocare` path;
3. enter a valid unique title, for example `B01 errore reale`;
4. press `Aggiungi` once.

Expected result while PostgreSQL is stopped:

- creation is not reported as applied;
- no canonical Activity card is manufactured locally;
- the user sees a truthful failure/error state;
- the draft remains recoverable rather than being silently treated as durable data.

Restart the disposable database:

```bash
uv run --project apps/backend python tooling/access-auth-e2e-control.py database-start
```

Return to `/home` and verify the failed title did not appear as a silently successful Activity.

This proof does not require inventing a browser-side retry success path. A later explicit retry may be exercised only through the real Create operation.

## 7. Staged macro-class boundary

While the B01 Create surface is open, verify that unfinished macro classes do not pretend to be available persistent operations. `Event`, `Routine` and Session recording must remain staged/disabled or otherwise incapable of fake success until their roadmap blocks activate them.

## 8. Cleanup

1. ensure the disposable database is running if proof C stopped it;
2. return to the terminal running `run-access-auth-stack.py`;
3. press `Ctrl+C` once;
4. wait for the harness cleanup to complete.

If the harness was killed before cleanup, remove only this run's explicitly labelled container:

```bash
docker ps -aq \
  --filter "label=dante.e2e.control_id=${DANTE_E2E_CONTROL_ID}" \
  | xargs -r docker rm -f
```

Do not use an unscoped prune/remove command.

## 9. Approval semantics

Automated E2E green is evidence, but it is not manual approval. Database/Dictionary reconciliation green is also automated engineering evidence, not user approval.

Approve B01 manual acceptance only after proofs A, B, C and the staged macro-class check have been visually inspected on the current candidate.

Approval token:

```text
B01 userTest — APPROVED
```

Until that explicit result is recorded, `[B01-T08]` remains open. Until both current-candidate engineering reconciliation and `[B01-T08]` are complete, B01 remains formally **IN PROGRESS** under the roadmap Definition of Done; do not label it green merely because an earlier targeted E2E passed.
