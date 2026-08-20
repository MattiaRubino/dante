# DANTE — Web Production Handoff v0

- Status: **PRE-SCAFFOLD HANDOFF CONTRACT**
- Production path: `apps/web`
- `apps/web` implementation: **NOT STARTED BY THIS SCOPE**

## 1. Goal

Make the future production-web step primarily an implementation/scaffold operation rather than a product-behavior rediscovery.

## 2. Existing architecture truth

- DANTE uses one monorepo with `apps/backend`, `apps/web`, `apps/mobile` boundaries.
- `docs/decisions/ADR-001-client-platforms.md` currently records React + Next.js for web and Expo/React Native for mobile as an accepted client-platform direction.
- the later Engineering Foundation explicitly deferred exact frontend runtime/package-manager/task/test/release details to the frontend workstream.

This foundation does **not** supersede ADR-001. Before production scaffold, re-read current main and either confirm it or explicitly supersede it through ADR governance if requirements/evidence materially changed.

## 3. Production-scaffold decision gate

Before creating `apps/web`, select/pin from current supported evidence:

- exact web framework/runtime line consistent with current ADR;
- Node runtime policy;
- package manager + lockfile policy;
- workspace/task-graph strategy if actually needed;
- TypeScript strictness baseline;
- lint/format policy;
- unit/component/integration/E2E/visual test tools;
- runtime schema/contract tooling;
- server-state/data client;
- styling/token integration;
- Storybook/component-workbench decision if useful;
- observability/error-reporting boundary;
- production build/deploy artifact model.

Choose the smallest professional stack that satisfies DANTE requirements; do not add enterprise tooling without a real need.

## 4. Migration inputs that must already exist

A surface is considered ready to migrate when it has:

```text
accepted visual/interaction oracle
+ stable technical IDs
+ component responsibility map
+ state/event contract
+ view-model/data-source boundary
+ fixtures
+ responsive/accessibility contract
+ regression expectations
```

The monolithic HTML is evidence/oracle, not the production source architecture.

## 5. Recommended migration sequence

```text
production scaffold + CI
→ shared tokens/localization/contracts
→ application shell
→ one vertical Home slice with mock adapter
→ same slice against real backend contract
→ remaining Home components
→ end-to-end/visual/accessibility/performance hardening
→ other surfaces
```

Do not port historical CSS cascade wholesale. Rebuild component styles from accepted semantics/tokens while comparing against the oracle.

## 6. Backend integration handoff

Production web must depend on a typed transport/client boundary, not backend internals. Mock and real adapters should feed equivalent frontend view models so a feature can move from synthetic to real data without changing rendering semantics.

The real backend/API scope owns endpoint/envelope/auth/concurrency details. Frontend requirements discovered here become explicit API requirements, not guessed routes.

## 7. Definition of rapid migration

“Rapid” means the framework conversion does **not** reopen already accepted:

- user jobs;
- state meaning;
- action semantics;
- responsive invariants;
- terminology;
- data ownership boundaries.

It does not mean skipping production tests/security/accessibility or mechanically translating DOM nodes one-to-one.
