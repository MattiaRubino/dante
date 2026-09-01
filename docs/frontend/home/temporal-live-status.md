# DANTE — Temporal Workstream Live Status

**Status:** ACTIVE / C1 COMPLETE-CANDIDATE HARDENING — NOT USER-ACCEPTED  
**Date:** 2026-09-01  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`  
**Worktree:** `/home/mattia/projects/dante-timeline`  
**Integration target:** `feature/home-react`  
**Current implementation checkpoint:** `4ca8de311e10fb03a4d5fd47903ebe4396271d95`

## Live authority

This file is the live status for the isolated Timeline / Temporal Create workstream.

For `feature/home-timeline` it supersedes stale operational metadata in the generic Home `current-checkpoint.md` and `production-depth-handoff.md`, which remain historical/parallel documents for `feature/home-react`.

A continuation must read, in order:

1. `docs/frontend/home/temporal-create-handoff.md`;
2. `docs/frontend/home/temporal-create-c1-engineering-checkpoint.md`;
3. `docs/frontend/home/temporal-create-c1-scope-amendment.md`;
4. `docs/frontend/home/temporal-create-q0-approval.md`;
5. `docs/frontend/home/temporal-create-q0-contract.md`;
6. `docs/frontend/home/temporal-frontend-roadmap.md`;
7. `docs/frontend/home/temporal-f0-contract.md`;
8. `docs/frontend/home/timeline-t1-frozen-contract.md`;
9. `docs/frontend/home/temporal-experience-architecture.md`.

When older documents conflict about C1 scope, the **C1 scope amendment wins**.

## Stable closed foundations

Do not reopen casually:

- H0 Whole Home structural baseline;
- T1/T1-A Timeline hardening;
- T1-B continuous temporal navigation / relative scrubber;
- F0 temporal application foundation on `7034b9b0d100709785ebe96e3816aab3e7b1d1f8`;
- permanent temporal distinctions such as Schedule / Occurrence / Session / Actual / Proposal;
- frontend application model != DTO != Domain != persistence;
- ports/adapters boundary;
- no fake backend/provider/AI/voice success.

## C1 product target

C1 is the complete pre-backend Create capability, not merely a compact popup:

```text
Quick Create
+
Expanded Create
+
Full Create / deep authoring
+
truthful external-vertical handoffs
```

All levels share one structured draft/application path.

## Current implemented surface

The branch now contains a complete-candidate implementation of the amended C1 scope, including:

- Activity and Event as distinct creation semantics;
- title-first Quick Create;
- timed, all-day and unscheduled forms;
- date/start/end/duration;
- floating-local and named-zone/zoned time semantics;
- context/life-area assignment from the available Timeline groups;
- notes/tags;
- progressive Quick -> Expanded -> Full authoring;
- Activity scheduling constraints including fixed/open/window/preferred/deadline intent where supported;
- movement/replanning policy;
- expected duration, split/session structure and minimum-session controls;
- recurrence specification;
- confirmation/outcome policy seams;
- Event location, availability and visibility;
- participant/resource/conference intent as truthful provider handoff only;
- explicit handoff for object types owned by other verticals instead of flattening them into Activity/Event;
- deterministic validation and invalid-control focus;
- F0-backed local command execution;
- local rich specification records kept separate from the minimal Timeline projection;
- candidate preview, applied Timeline projection, reveal/focus and Undo;
- contextual Create from Timeline double-click and Shift-drag range gesture;
- responsive/mobile full editor;
- IT/EN i18n and accessibility checks.

## Hardening completed after the first expanded implementation

Recent audit work found and fixed issues that must not be reintroduced:

1. **Architecture cycles:** shared Create UI types were moved out of component-to-component imports; dependency-cruiser is clean.
2. **i18n/accessibility contract drift:** tests now use the current semantic labels such as `Durata prevista / Expected duration`; recurrence controls are unambiguous.
3. **Shift-drag E2E determinism:** the test now brings the target day section into the viewport and measures current geometry before using raw mouse coordinates. Do not revert to stale/off-screen bounding boxes.
4. **Mobile sub-pixel tolerance:** full-screen width assertions tolerate browser floating-point fractions while the real horizontal-overflow invariant remains strict.
5. **DST correctness:** Event end/duration helpers now distinguish floating vs zoned semantics. Zoned calculations use real Instants in the IANA zone, with explicit Europe/Rome spring-forward and fall-back coverage plus multi-day coverage.
6. **Rich-intent idempotency:** F0 already protects the minimal projection command; C1 now also fingerprints the complete rich Create intent. Exact retries are accepted, while the same `operationId` with changed rich metadata is rejected side-effect-free.
7. **Timeline Create projection performance:** collision/layout preparation was changed from repeated `slice/filter/find` work to single-pass O(n) slot counting with cached group/day lookups.

The detailed implementation record is `temporal-create-c1-engineering-checkpoint.md`.

## Current CI truth

The only implementation checkpoint currently eligible to become the C1 automated candidate is:

`4ca8de311e10fb03a4d5fd47903ebe4396271d95`

Frontend CI run:

- run ID: `33539539640`;
- run number: `410`.

At the documentation checkpoint:

- **Quality:** PASS, including contract drift, active-workstream format, lint, typecheck, architecture, generated-source drift, unit tests, production build, diff check and repository mutation check;
- **Mobile Bundle:** PASS, including Expo compatibility and Android Hermes bundle smoke;
- **Web E2E:** still in progress at the time this checkpoint was written;
- **Frontend CI Gate:** therefore not yet claimable as final PASS.

The immediately preceding implementation run confirmed both Chromium and the frozen Firefox Timeline contract after the gesture/mobile fixes, but that run was superseded by later hardening commits. It is useful evidence only; it is **not** the final closure gate for `4ca8de31...`.

Documentation-sync commits after `4ca8de31...` may move branch HEAD. Treat `4ca8de31...` as the implementation checkpoint and docs-only descendants separately until a later code change creates a new implementation checkpoint.

## Remaining C1 closure work

Before asking for user acceptance:

1. finish the full CI on the latest implementation/docs descendant and require Quality + Mobile + Chromium + Firefox + final gate green;
2. inspect any remaining failure from logs instead of weakening tests/contracts;
3. complete the bundle/critical-path audit; only lazy-load Expanded/Full if the split is clean and measurably useful;
4. perform a final static audit for semantics, cleanup, focus, responsive behavior and repeated-use performance;
5. give the user an exact manual verification protocol covering Quick, Expanded, Full, Activity, Event, unscheduled/all-day/zoned cases, contextual gestures, Undo and mobile;
6. wait for explicit user PASS;
7. only then freeze C1 and move to C2 Card -> Detail.

## Stop line

Still outside C1:

- real API transport;
- PostgreSQL persistence;
- canonical server IDs;
- auth/ACL enforcement;
- external provider writes/sync/invitations/conferencing;
- notification delivery;
- authoritative solver runtime;
- multi-device reconciliation;
- AI runtime;
- voice runtime.

## Delivery rule

Continue internal C1 hardening continuously. Do not move to C2 merely because automated tests are green. The next phase starts only after the coherent complete C1 system is manually tested and explicitly approved by the user.
