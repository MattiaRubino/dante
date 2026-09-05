# Archived branch record — `feature/home-timeline`

**Status:** ARCHIVED HISTORY / NON-AUTHORITATIVE  
**Recorded:** 2026-09-05  
**Branch:** `feature/home-timeline`  
**Current `main` integrated through:** `7bc7c0136cb5579528be1e2be0e71a6399004f90`  
**Pre-documentation-closure technical head:** `d8b1aa65d5d2651702bd790be3843234ad9f86da`

This record preserves the branch/workstream history that used to be duplicated across several operational handoff documents. It is not current implementation authority.

## Purpose of the branch

The branch accumulated and hardened the production React Home/Temporal workstream while `main` continued to advance substantially in platform/backend/Auth/Recovery/Email/Observability/OpenAPI work.

The reconciliation target became:

```text
current main
+
AppShell / Home
+
Timeline T1
+
Temporal F0
+
Temporal Create C1 candidate
+
World Focus pre-backend frontend
```

The branch was reconciled by merging current `main` into `feature/home-timeline`, not by rebasing, resetting or rewriting history.

## Durable frontend milestones carried by the branch

- H0 Whole Home macro structure — frozen/change-controlled;
- P1 Global AppShell/Topbar — frozen for accepted implementation scope;
- T1 Home Timeline behavior — frozen;
- F0 typed Temporal application foundation — closed/frozen;
- C1 Manual Temporal Create — substantial frontend candidate implemented, but final manual product acceptance still OPEN;
- C2 Structured Detail — blocked until explicit C1 manual approval;
- World Focus — pre-backend frontend architecture/candidate only.

## Main reconciliation

By 2026-09-05, `main` had moved far beyond the branch creation point. The integration preserved current `main` as authority for backend/database/platform work and preserved the branch as authority for Home/Temporal-specific frontend work, with semantic reconciliation of shared frontend integration files.

The reconciled route set required regeneration of `apps/web/src/routeTree.gen.ts` through the real TanStack Router Vite plugin. The first post-merge CI correctly detected generated-source drift. Temporary diagnostic commits were then used to expose the exact generator output; the final tree restored the normal generated-source checker and committed the real generated route tree. Those diagnostic commits are branch-history artifacts only; no diagnostic behavior remains in the final tree.

## Retired operational documents

The following filenames remain only as minimal tombstones so historical references keep resolving:

- `docs/frontend/home/production-depth-handoff.md`
- `docs/frontend/home/temporal-create-handoff.md`
- `docs/frontend/home/temporal-live-status.md`
- `docs/frontend/home/world-focus-handoff.md`

Their former branch/worktree/SHA/database instructions must not be used as current authority.

Current authority begins at:

- `docs/frontend/README.md`;
- `docs/frontend/home/current-checkpoint.md`;
- `docs/frontend/home/temporal-frontend-roadmap.md`;
- the frozen H0/T1/F0 contracts;
- World Focus architecture/roadmap;
- current code/tests/CI.

## Important non-closure

Repository integration and product acceptance are separate.

At this record:

```text
C1 manual acceptance: OPEN
C2: BLOCKED
PR: NOT OPENED
```

Nothing in this archive record grants `C1 MANUAL PASS — APPROVED`.
