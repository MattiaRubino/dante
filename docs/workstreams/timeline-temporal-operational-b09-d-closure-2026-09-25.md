# B09-D — Responsibility / Participation whole-block closure record

- **Branch:** `feature/timeline-temporal-operational`
- **Baseline:** B09-C proven at Alembic `20260925_69`, topology `158|5|109|93|303|254|433`
- **State:** AUTOMATED PROOF PASSED — user real-app proof pending
- **Scope:** B09-A typed roles + B09-B guarded authoring + B09-C owner-local non-Account Persons

## Accepted contract

B09 models one current responsible Person on an Activity or Event and required/optional expected participation of Persons in an Event. These are independent relations over existing subjects. An owner may register a native Person without creating an Account, provide an owner-local display label, correct that label under revision control, assign/remove Responsibility and establish/change/remove expected Event Participation. Authenticated API and Timeline controls must read back canonical results.

B09 establishes no invitation delivery, acceptance/decline workflow, Account collaboration, shared calendar authority, Actual attendance, Event Actual, Outcome or completion. Home `+` participant email textareas are owned by B14; they must not be represented as native Person references until that boundary is resolved.

## Existing proven substrate

- B09-A `_66`: three typed role relations; PostgreSQL and Dictionary/catalog proof.
- B09-B `_67`–`_68`: guarded, replay-safe role mutations and Timeline authoring.
- B09-C `_69`: owner-local Person catalog, immutable create/rename receipts, NativeAddress and no Account; user-run generated check, typechecks, 7 web, 11 backend OpenAPI/API and 18 PostgreSQL tests passed on 2026-09-25. Client generated artifacts committed at `875aaf48`.

## B09-D integrated proof

The added API/PostgreSQL test `tests/integration/temporal/test_b09_d_whole_block.py` exercises:

1. Two authenticated Accounts and one native Person referent without an Account.
2. Person creation, exact replay, operation-id reuse rejection, rename and stale revision rejection.
3. Owner-local listing and the second Account's inability to read/mutate the first Account's Person or subjects.
4. Activity and Event Responsibility, Event expected Participation, readback, requirement change, clear and remove.
5. Responsibility and Participation independence, durable native identity, and zero Actual and Session creation.

The UI test extends `responsibility-controls.test.tsx` with a created Person, label correction, persisted Responsibility and expected Participation, followed by both removals.

**Automated B09-D result (user-run, 2026-09-25):** web typecheck exit 0; focused responsibility controls and remote source tests 8 passed across 2 files (exit 0); focused PostgreSQL B09-D/B09-C/B09-B/B09-A/current-catalog suite 18 passed (exit 0). The checkout reported no changes in `git status --short`. These results validate the candidate branch only.

## User real-app verification — required before whole-B09 closure

**State:** PENDING USER REPORT. The user explicitly requested this verification at the end of B09-D before closing B09. B15 will still perform the separate whole-vertical regression.

Run the app using the existing local backend/web workflow, then:

1. Create an Activity and an Event in a Life Area, place both on Timeline and open each detail; neither needs a Session or Actual.
2. Create a Person named Anna from the role controls. Confirm Anna appears as a selectable Person after a refresh, without signing Anna in.
3. Assign Anna Responsibility for the Activity and Event. Refresh both: the holder remains Anna. Correct Anna's local name and confirm both labels follow the correction.
4. On the Event set Anna's expected Participation to required, switch it to optional and refresh. Confirm Responsibility stays unchanged. Remove expected Participation and confirm the Event shows none after refresh.
5. Remove Event Responsibility and confirm Activity Responsibility stays with Anna. Verify the Event continues to exist and no actual attendance/completion is presented as a consequence.
6. If two authenticated Accounts are available, confirm the second Account cannot see Anna or edit the first Account's Activity/Event. The automated PostgreSQL test separately proves the access and identity boundary.

Record observed behavior and any failure precisely. No screenshot or test output may be pre-labelled PASS.

## Closure decision

B09-D and B09 as a whole close only after focused automated proof and the user's real-app result are recorded. The local candidate branch remains separate from protected-main integration. B10 follows whole-B09 closure.
