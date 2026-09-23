# AGENTS.md

Navigation for coding agents. This file is not a Dante manual and not a status record.

Existing documentation stays authoritative. Do not copy it here. Do not record the current branch, commit, checkpoint, Alembic revision, database counts, or next task in this file.

## Session start

Before any implementation edit, inspect the worktree again:

```text
git branch --show-current
git status
git diff --stat
git diff          # when the stat shows changes
```

Then discover and re-read the active workstream handoff, live implementation map, and execution plan under `docs/workstreams/`. Use the checked-out branch and those files. Do not treat a remembered chat, a stale index, or a status banner as the live frontier.

Re-read the Domain concept specs for the concepts this task touches, under `docs/domain/concepts/`.

For database work, read `docs/database/README.md` and the Dictionary entries for the objects touched. `docs/database/dictionary/scope.json` field `current_materialization` is the live count source. `expected_baseline` is not.

Read the implementation files and the tests that own the behavior before changing it.

## Which truth is which

```text
checked-out branch candidate
!= protected-main integrated truth
!= historical evidence
```

Code, migrations, Dictionary, mappings, and tests in this worktree are the candidate. Protected-main integration truth must be verified from the repository's authoritative protected-main source. Never assume the local `main` ref is current or equivalent to `origin/main`. `docs/PROJECT-STATUS.md` describes protected main, not this branch's checkpoint. Archive files, old closure banners, and evidence records do not override a later current source.

If authoritative sources disagree, stop and report the conflict. Do not guess.

## Where procedures live

Follow these documents. Do not restate them here.

- `docs/development/agent-operating-manual.md`
- `docs/development/operating-rules.md`
- `docs/development/documentation-and-handoff.md`
- `docs/development/documentation-lifecycle-policy.md`
- `docs/development/branching-and-environments.md`
- `CONTRIBUTING.md`

If a bootstrap list in those manuals stops at an old entry point, continue with the session-start reads above. Ignore frontier snapshots inside those manuals when a live handoff, map, database reference, or migration head disagrees. Use the manuals for procedure: write gates, documentation lifecycle, and evidence language.

## Stable safety rules

- Do not invent requirements.
- Do not silently resolve conflicting sources.
- PostgreSQL is the canonical persistence.
- Do not edit an applied migration. Corrections are new forward revisions.
- Do not hand-edit generated API client files under `packages/api-client/openapi/` or `packages/api-client/src/generated/`.
- Keep Temporal concepts distinct as defined in the Domain specs. Do not collapse Activity, Event, Routine, Recurrence, Occurrence, Schedule, Session, and Actual.
- Do not claim PASS unless the relevant test or validation was actually executed.
- Do not commit, push, rewrite history, or otherwise mutate Git state unless the user explicitly asks.
