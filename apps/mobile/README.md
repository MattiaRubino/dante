# DANTE Mobile

DANTE Mobile is the first-class native client for DANTE. The current delivery target is Android; iOS remains an architectural target and must not be made unnecessarily expensive by Android-only application design.

This directory is governed by the repository-level frontend decisions, especially ADR-008 and ADR-009. The Mobile app does not redefine canonical DANTE domain truth, authorization, persistence, or accepted-effect semantics.

## Current posture

- Android-first development and validation.
- iOS-compatible by design; iOS release work is dormant until activated.
- React Native + Expo + TypeScript.
- Expo Router owns navigation adapters; routes stay thin.
- Product implementation is feature-first when real features exist.
- DANTE UI and platform integration remain app-local.
- Backend/PostgreSQL remain canonical state/effect authority.
- Offline, auth, API generation, query/form state, observability, EAS release and other capabilities activate only when a real milestone requires them.
- Production-oriented development will move from Expo Go probes to a DANTE development build.

## Branch boundary

During the parallel Mobile workstream, the default write boundary is:

```text
apps/mobile/**
```

Everything outside this directory is read-only unless a new explicit scope is approved. In particular, root lockfiles, shared packages, backend, Web, repository CI and root documentation are not modified implicitly.

A requirement that crosses this boundary is a checkpoint, not permission to work around the boundary locally.

## Documentation

- [`docs/TECHNICAL_BASELINE.md`](docs/TECHNICAL_BASELINE.md) — selected technology posture and version policy.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — Mobile application boundaries and dependency rules.
- [`docs/ROADMAP.md`](docs/ROADMAP.md) — staged Mobile workstream and completion gates.
- [`docs/QUALITY.md`](docs/QUALITY.md) — production-quality expectations.
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — local Mobile decision log and reopen triggers.

## Source layout

```text
app/              Expo Router route adapters
src/bootstrap/    application composition and startup
src/features/     real product capability ownership
src/ui/           DANTE Mobile UI primitives and system
src/platform/     Android/iOS/device integrations
src/testing/      Mobile-specific test support
```

Directories are created only when they own real responsibilities. Do not add generic `services`, `utils`, `hooks`, `stores`, `models`, or `components` dumping grounds at the application root.

## Development rule

Work one bounded milestone at a time:

1. define the behavior and boundary;
2. implement the smallest complete slice;
3. validate it with evidence;
4. record any changed decision;
5. close it before opening the next slice.

The objective is not to accumulate screens quickly. It is to build a maintainable, native-feeling DANTE client whose behavior remains truthful to the product model.