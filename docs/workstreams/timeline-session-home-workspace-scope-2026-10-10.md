# B14 — Session independence, Home three views and Objective confirmation

**Status: APPROVED FEATURE / CODE CANDIDATE PUBLISHED / LOCAL GATE AND REAL APP ACCEPTANCE OPEN.**
**Branch:** `feature/timeline-temporal-operational`
**Date:** 2026-10-10
**Domain authority:** `docs/domain/decisions/activity-session-live-timeline-v1.md` §8
**Database authority:** `docs/database/timeline-temporal-operational.md`
**Current Alembic candidate head:** `20261010_141`

## Accepted product and implementation

- A named planned Session has a canonical owner and can start independently of the optional generic Activity live clock; it is never an invented second main Session. When generic main is enabled, child Start/Resume still requires it running, main Pause/Stop cascades atomically, main Resume never auto-resumes children. Existing Session and Schedule history is immutable; unfinished planned work is not auto-marked skipped or completed. Trusted planned Start is not directly EXECUTABLE by runtime/PUBLIC.
- The Session desk is attached to the right-inner edge of the Timeline and dismissible/reopenable from its toolbar icon; first exact-time preview is five minutes early; Stop retires an ended row instead of re-showing Ready within the same planned interval. One real/presented Activity card survives.
- `ContextRail` has one fixed right column with three pages and touch/keyboard navigation: `Conclusi` shows factually ended real Sessions and accepted occurred Actuals only (a Session Stop is not an Activity completion); `Da verificare` retains B10 policy-derived reality/outcome/objective queue; `Obiettivi` groups truly unobserved Objectives by canonical Activity/Event/Occurrence owner. History is bounded to 90 days and at most 40 displayed rows (100 hard cap in API); this initial implementation does **not** yet support user-controlled pagination beyond this bounded page. No unbounded table scans permitted.
- One actor-owned provisional Objective value is persisted by CAS and does NOT write Observation/Evaluation/Result. After an explicit ✓ Conferma, PostgreSQL atomically writes the canonical ObjectiveResult and durable receipt using operation replay/CAS. Same `ObjectiveControls` is used in Inspector and Home; correction of confirmed Results uses preexisting correction capability, not a draft overwrite.
- Source forward migrations: `_139` provisional inputs, `_140` History/Objective reads, `_141` trusted independent planned Start and desk inclusion. Expected exact catalog 238 tables, 5 views, 228 routines, 103 triggers, 485 indexes, 421 foreign keys and 596 CHECK. Confirm through PostgreSQL exact-catalog gate, do not infer proof from this document.

## Proof boundary / one local gate

**Not tested on user's WSL at this head.** Prior 7/7 green tests apply to `_138`, not this integrated candidate. Pull with ff-only, then run **only** `bash tooling/verify-b14-session-home-workspace-local.sh` once and send the summary plus logs of any red gate. Script performs: Python Syntax/Ruff/unit, migrated real PostgreSQL owner isolation/replay/catalog, API generation/check and client TS, Web TS/ESLint/targeted Vitest, real-browser Session panel test. Script never runs CI, pushes, resets or cleans. Preserve newly generated OpenAPI/Orval files; publish only after green.

**Real-app acceptance then required:** launch usual `run-access-auth-stack.py`, test Activity with internal Session but no main, main+internal Pausa/Riprendi/Stop, -5min preview and moving into window, truthful finished work list after Stop, no synthetic completed Activity, three tabs/swap, an unconfirmed Objective value survives refresh/restart of persistent database, explicit ✓ creates accepted ObjectiveResult visible in Inspector and removed from pending rail, keyboard/mobile at 390px and dense Timeline overlap. The standard E2E stack may use an ephemeral database (restarted stack resets test data); test persistence within one running stack plus real persistent database separately, not after teardown of disposable Postgres.

## Explicitly not silently expanded

No synthetic Session or Actual for unstarted work. No automatic Objective success from Session Stop. No generic completion authority from planned Event end. No Event-to-Bozze Move parity, no new CI, no rewrites of published migration files, and no background monitoring. Current Home list is bounded; full paginated historical browser and any opt-in overdue reminders are separate later tasks. Keep B14/B15 open until user confirms the real UI.
