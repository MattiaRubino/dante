# Draft Vault + Duplica: new E2E acceptance matrix (2026-11-23)

**Branch:** `feature/timeline-temporal-operational`.
**Status:** 10 newly authored Playwright tests, **NOT RUN** on WSL at time of
publication. These tests do not edit, skip or weaken any older E2E suites.
**Domain contracts:** `docs/domain/concepts/draft-vault.md` and
`docs/domain/concepts/temporal-duplicate.md`.

## 1. Strategy and coverage boundaries

Two new files target different trust boundaries:

1. **7 authenticated, real-stack scenarios**
   in `apps/web/e2e/auth/draft-vault-real-lifecycle.spec.ts`.
   The UI is real, every API request goes to the actual backend/PostgreSQL,
   and the tests read canonical owner data to verify identity and history.
   Each scenario uses one independent preseeded synthetic account,
   `signedInPersona(..., 103..109)`, partitioned by Chromium, Firefox and
   WebKit (accounts 411..417 etc.), avoiding existing persona slots.
2. **3 non-auth, deterministic browser stress scenarios**
   in `apps/web/e2e/draft-vault-new-stress.spec.ts`.
   Playwright routes the Draft owner API to a scoped in-memory fixture
   solely to generate 100 diverse rows efficiently and test UI/CSS without
   100 manual creations. The mock does **not** claim to prove backend
   concurrency/atomicity; PostgreSQL integration does.

Do **not** count a passing mocked status as proof that hard deletion is
atomic. Conversely, do not spend tens of minutes manually clicking 100
Save forms just to test scrolling.

## 2. New E2E scenarios

| ID | Boundary | Workflow and assertions |
|---|---|---|
| **DV-REAL-01** | Real stack | Create rich Activity with new Area/color, multiple intervals, planned Sessions and Objectives; verify backend, open real Inspector Duplica, Save as a new Draft, verify original unchanged, Resume via Vault, Add a new Activity, verify new refs, copied definitions and Draft consumed |
| **DV-REAL-02** | Real stack | Create rich Event with new Life Area/color, Agenda and Objectives; Inspector Duplica → Draft → Resume → Add; verify Agenda order, Objective definitions, original identity retained and Draft consumed |
| **DV-REAL-03** | Real stack | Create live-capable Activity with planned Sessions, start and pause main Session, read real Session attempt, Move to Vault with a **red destructive review** and second confirmation; Cancel first, then commit and prove original gone and snapshot has no runtime/session/observation facts |
| **DV-REAL-04** | Real stack | Create Event with boolean Objective, confirm result via Work/Obiettivi, read `observation_ref`, attempt Move and cancel loss warning, verify result still there, accept, verify original removed and Draft contains definition without recorded result |
| **DV-REAL-05** | Real stack | Create recurring Activity and recurring Event using real Create, inspect selected occurrence/source, ensure standalone `Sposta in Bozze` absent and no inert Draft silently created |
| **DV-REAL-06** | Real stack | Fill Vault to 100 via authenticated save API, check header `100/100`, attempt Create→Save Draft 101, inspect quota popup and preserved title, delete one Draft, retry without retyping, verify 100 rows including the new Draft |
| **DV-REAL-07** | Real stack | Create original Event, fill Vault 100, attempt `Sposta in Bozze`, assert HTTP `409 temporal.drafts.capacity`, popup, original and Objectives still readable, no orphan new Draft; delete one, repeat with fresh preview and assert successful atomic Move |
| **DV-STRESS-08** | Mocked Draft API + real browser CSS | Populate 100 mixed Activity/Event cards, varied all-day/timed/untitled configurations. Verify bounded list scroll, stationary search, both untitled aliases, filter results, cancellation and real deletion, count update and mobile viewport geometry |
| **DV-STRESS-09** | Mocked owner capacity + real browser | At 100, Save a new Create proposal and verify popup and preserved unsaved text; free one slot, retry, verify 100; duplicate another Draft at 100 and verify second quota popup, original Draft intact |
| **DV-STRESS-10** | Mocked owner API + real browser | Populate eight mixed advanced snapshots with Agenda, planned Sessions, colors and Objectives. Resume Activity and CAS update same ref, duplicate Event and Save a new identity, verify source unchanged, delete copy with cancel+confirm, verify no Play/Pause controls in Vault |

**Explicit expected coverage limitation:** DV-REAL-03 records a main Session
and preserves planned child *definitions*. It does not yet claim simultaneous
recording of multiple child Session attempts. That higher-density recording
scenario should be added after the real runtime's child Session controls
are confirmed, rather than fabricating test data. DV-REAL-04 independently
covers recorded Objective destruction.

## 3. Production invariants each E2E must protect

- Source identity cannot be reassigned by Duplicate/Resume or an abandoned form.
- Original remains unchanged after duplicate and failed Move.
- Accepted Add consumes Draft *after* native creation and must never replay
  native authoring if only Draft removal fails.
- Scheduled Session *definitions* may copy; actual attempts, observations,
  assessments and timer states never copy into a Draft.
- Full Vault blocks **new inserts** but not same-ref updates, removal or
  creating an Activity/Event from an existing Draft.
- Two concurrent PostgreSQL insertions cannot push a user beyond 100;
  this is explicitly tested in the new `test_draft_vault.py` integration
  case, not asserted from the UI alone.
- Recurring sources and occurrences cannot use one-off Move.
- Title-less Drafts are persisted with empty title; search aliases are
  presentation-only.
- Timeline uses short-lived tombstones after committed hard Move; a failed
  Move never hides the original.
- Full Advanced Create is used on Resume and Duplicate, regardless of the
  old Draft's saved Quick/Full surface.

## 4. Setup, execution and isolation

The DB quota migration is Alembic
`20261123_189_draft_vault_owner_capacity.py` and must be applied before
real-stack tests. Run the normal repository database verification gate first.

From repository root:

```bash
cd ~/projects/dante
git pull --ff-only origin feature/timeline-temporal-operational
uv run alembic upgrade head

pnpm --filter @dante/web typecheck
pnpm --filter @dante/web exec vitest run \
  src/features/temporal-create/application/remote-draft-vault-capacity.test.ts \
  src/features/temporal-create/ui/draft-vault-capacity-dialog.test.tsx \
  src/features/home/ui/timeline/timeline-draft-vault.test.tsx

uv run --project apps/backend pytest \
  apps/backend/tests/integration/temporal/test_draft_vault.py -m postgres -q
```

Run the **new** browser files independently:

```bash
pnpm --filter @dante/web exec playwright test \
  e2e/draft-vault-new-stress.spec.ts

pnpm --filter @dante/web exec playwright test \
  --config playwright.auth.config.ts \
  e2e/auth/draft-vault-real-lifecycle.spec.ts
```

If a backend fixture needs the repository's dedicated PostgreSQL runtime,
run its documented local test environment (Docker, migrations, isolated
test cluster) before running pytest. Do not substitute the mock E2E for
real-stack results.

### Avoid cross-run pollution

Authenticated tests use dedicated accounts, `uniqueTitle`, owner-only API,
and an explicit Vault cleanup helper before/after scenarios. Each Draft has
its own UUID and revision, never a shared hardcoded ref. The non-auth
stress fixture exists only inside one browser test and does not persist.
Real-stack accepted Activity/Event subjects may remain as unique synthetic
records; never point test requests at production accounts.

### Failure diagnostics

Preserve Playwright traces on failure. Distinguish **test fixture errors**,
expected product validation, API/DB failures and CSS viewport bugs. A
failed test must stay RED; do not add `test.skip`, `test.fail`, sleeps,
or loosen cardinality checks to hide it. Capture failing scenario ID,
browser, API status/code, first relevant assertion and DB evidence.

The 10 tests become accepted only after WSL TypeScript/Prettier, migration,
unit/integration and new Playwright runs are all green, then optional
owner browser review. No test result is asserted in this document before
the corresponding gate has run.
