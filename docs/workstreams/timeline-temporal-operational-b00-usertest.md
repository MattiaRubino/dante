# Timeline / Temporal-Operational — B00 isolated `userTest`

- **Status:** READY TO RUN — NOT YET APPROVED
- **Workstream branch:** `feature/timeline-temporal-operational`
- **Purpose:** manual B00 acceptance only
- **Data class:** disposable synthetic test data; never personal/production data

## 1. Why this exists

B00 requires a manual product-surface proof without using a developer's real account, a shared database or browser-only fake state.

The accepted Access/Auth full-stack harness already provides the correct isolation boundary, so B00 reuses it rather than creating a second manual stack.

The manual environment is:

```text
production web build
→ HTTPS Vite preview
→ real FastAPI
→ real dante_runtime role
→ fresh migrated PostgreSQL 18.6
→ synthetic account only
```

The database/container exists only for the run and is removed when the harness exits normally.

## 2. Preconditions

Run from the repository root with the workstream branch checked out.

The canonical PostgreSQL image must already exist:

```bash
docker compose -f infra/compose/local.yaml build postgres
```

Do not point this protocol at a normal local DANTE database, staging or production.

## 3. Start the isolated stack

Choose one control id for the entire manual run:

```bash
export DANTE_E2E_CONTROL_ID=temporal-b00-usertest
uv run --project apps/backend python tooling/run-access-auth-stack.py
```

Wait for the harness to report that the full stack is ready, then open:

```text
https://127.0.0.1:4173
```

The certificate is intentionally local/self-signed.

Synthetic credentials:

```text
email:    synthetic.user@example.com
password: correct horse battery staple
```

These credentials belong only to the disposable harness.

## 4. Manual proof A — real empty Timeline path

1. Sign in with the synthetic account.
2. Navigate to `/home`.
3. Wait for the temporal read to settle.
4. Verify that Home remains usable and Timeline does not show prototype cards such as `Redesign LifeOS — sessione focus`.
5. Verify there is no `Timeline non disponibile` error while PostgreSQL is healthy.

Expected semantic result:

```text
real authenticated read succeeds
AND
no legitimate temporal product rows exist yet
→ truthful empty Timeline
```

An empty Timeline is correct B00 behavior. Adding demo cards to make the screen look populated is a failure.

## 5. Manual proof B — Create must fail closed before B01

1. On `/home`, press Timeline `+`.
2. Enter a valid Activity title, for example `B00 manual truth check`.
3. Press `Aggiungi`.

Expected result:

- the draft stays open;
- the UI reports that creation could not be applied;
- no new Timeline card appears;
- retrying the same unsupported write does not manufacture local persistence.

This is deliberately the correct behavior until B01 activates the first authoritative Activity write operation.

```text
valid draft
!= accepted backend effect
```

## 6. Manual proof C — real backend/database outage and Retry

Keep the stack running. In a second terminal use the **same** control id:

```bash
export DANTE_E2E_CONTROL_ID=temporal-b00-usertest
uv run --project apps/backend python tooling/access-auth-e2e-control.py database-stop
```

Force a fresh temporal read, for example by opening another Timeline date or navigating to:

```text
/home?date=2034-02-17
```

Expected result while PostgreSQL is stopped:

- Timeline reports `Timeline non disponibile`;
- no fake cards replace the failure;
- the UI exposes `Riprova`;
- the failure is not represented as an empty-success response.

Restart the disposable database:

```bash
uv run --project apps/backend python tooling/access-auth-e2e-control.py database-start
```

Then press `Riprova` in the product UI.

Expected result:

- a new real request is made;
- Timeline returns to ready/empty state;
- no prototype cards appear.

## 7. Cleanup

Normal cleanup is explicit:

1. ensure the database has been restarted if proof C stopped it;
2. return to the terminal running `run-access-auth-stack.py`;
3. press `Ctrl+C` once;
4. wait for the process to exit.

The harness `finally` path stops the web/API helpers and removes its disposable PostgreSQL container.

If the harness process was killed abnormally and could not run its cleanup, remove **only** the container carrying this run's exact control label:

```bash
docker ps -aq \
  --filter "label=dante.e2e.control_id=${DANTE_E2E_CONTROL_ID}" \
  | xargs -r docker rm -f
```

Never use an unscoped `docker rm`/prune command as part of this protocol.

## 8. Approval semantics

Running the environment is not approval. Automated green is not manual approval. A PR merge is not manual approval.

Record the manual result only after all three proofs have been inspected on the current workstream candidate.

Approval token:

```text
B00 userTest — APPROVED
```

Until that explicit result is recorded, B00 manual acceptance remains open.
