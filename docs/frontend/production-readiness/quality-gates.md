# DANTE — Frontend Quality Gates v0

- Status: **CURRENT PRE-PRODUCTION QUALITY BASELINE**

A render that looks correct at one width is not a frontend PASS.

## Change-control invariant — frozen behavior

Once the user explicitly accepts a frontend behavior or visual state, that behavior becomes **FROZEN** until the user explicitly authorizes a change.

Frozen means:

- refactors, bug fixes, performance work and cleanup may change implementation but not the accepted observable contract;
- an intentional change to interaction semantics, layout, hierarchy, visual treatment, information density or navigation requires explicit user approval **before the first production write**;
- regression tests protecting a frozen behavior must not be weakened, deleted or rewritten merely to match a new accidental behavior;
- if a regression is discovered while implementing another feature, restore the frozen contract first; redesigning the contract is a separate approved scope;
- CI green is necessary but not sufficient: the user remains the final visual/manual acceptance gate for changes that affect an accepted surface.

For direct feature-branch work, the assistant must not ask the user to pull/test a new frontend commit until the relevant automated gates have completed successfully. A broken build, typecheck or known regression test must be caught before handoff whenever the repository CI can execute it.

The required execution sequence for frozen surfaces is:

```text
scope + frozen-contract check
→ implementation
→ static/unit/component/E2E gates
→ CI green
→ user local/manual gate
→ explicit acceptance
→ freeze updated contract
```

A deliberate contract change follows the same sequence but starts with explicit user authorization and records which frozen expectations are being replaced.

## Whole-Home H0 structural freeze

The accepted Home macro-composition is governed by:

- `docs/frontend/home/home-structural-contract.md`;
- `prototypes/frontend/shared/contracts/home-structure.contract.json`;
- `prototypes/frontend/shared/contracts/home-shell-responsive.matrix.json`.

This H0 boundary sits above child-surface contracts. A Timeline, AI, Mondi, Segnali, Capture, Resolution or responsive bug-fix scope must consume the Home skeleton rather than silently renegotiate it.

An intentional change to Home region ownership, hierarchy, macro composition, structural breakpoints or cross-region expansion/collapse behavior requires explicit user approval before production writes and a deliberate H0 contract version/change.

## Gate classes

### Q0 — contract/static

- machine-readable contracts parse;
- contract versions agree;
- fixture identities are unique;
- required states/events/invariants exist;
- Whole-Home H0 region ownership and responsive-mode contracts agree;
- touched localization/token/registry/contract documentation remains synchronized;
- lint/type/build checks apply when the production toolchain exists.

### Q1 — component/behavior

For each durable component/state:

- loading/ready/empty/partial/full/overflow/error/unavailable as applicable;
- deterministic selection/navigation;
- pointer + keyboard behavior;
- focus ownership/restoration;
- no console errors;
- no event duplication/leaked listeners.

Accepted interaction sequences become executable regression contracts. The tests should assert user-visible semantics rather than incidental implementation details.

For the frozen Whole-Home skeleton, Q1 also verifies that required regions remain in the real React tree under the approved owners and that Home does not re-own the Global AppShell/Topbar.

### Q2 — responsive geometry

There are two complementary Home guard matrices.

#### Stage matrix

```text
viewport widths: 1856, 1600, 1366, 1200, 1024, 901
AI states:       expanded, collapsed
stage modes:     continuity, signals
cartesian cases: 24
```

At minimum verify:

- no unexpected page horizontal overflow;
- stage outer bounding box is mode-independent;
- selector/nav anchors do not move on mode switch;
- AI collapse/expand remains reversible;
- timeline/context rail remain outside stage geometry ownership;
- Continuity target items fit the desktop matrix;
- Signals shows at most 3 complete visible items.

#### Whole-Home H0 pressure matrix

```text
pressure widths:
1856, 1600, 1366, 1200, 1121, 1120, 1024, 901, 900, 760, 390

macro modes:
H0-WIDE        >= 1121
H0-COMPRESSED  901..1120
H0-COMPACT     <= 900
```

At minimum verify:

- shared AppShell/Topbar exists outside Home ownership;
- every required Home region remains present exactly once in the runtime tree;
- no unexpected horizontal page overflow at pressure/boundary widths;
- H0-WIDE keeps AI beside Upper Workspace and Timeline beside Context Rail;
- H0-COMPRESSED keeps AI beside Upper Workspace, hides the current web rail representation and gives Timeline the available Today width;
- H0-COMPACT stacks AI above Upper Workspace and Orientation above Central Stage;
- AI collapse/expand is geometrically reversible at representative desktop widths;
- Stage mode switch cannot reauthor Whole-Home macro geometry;
- Timeline expansion at supported wide widths may consume Today rail space but cannot reauthor Hero geometry.

Golden screenshots and bounding-box assertions are complementary: screenshots catch visual drift; geometry assertions explain it.

### Q3 — visual regression

Accepted surfaces receive stable screenshot baselines for defined viewport/state combinations. Deliberate changes update baselines only with reviewed visual scope; a changed baseline is not automatically a pass.

A screenshot baseline is evidence, not authority by itself: it may only be updated when the corresponding visual change was intentionally approved.

### Q4 — accessibility

Before production readiness:

- semantic controls;
- full keyboard operation where interactive;
- visible focus;
- correct accessible names/roles/states;
- modal/popover focus containment/restoration;
- reduced-motion handling;
- contrast audit;
- automated accessibility scan plus manual critical-path check.

Target production conformance is WCAG 2.2 AA unless a later explicit product requirement is stricter.

### Q5 — integration

With real API availability:

- runtime contract validation;
- backend/client contract tests;
- auth/authz cases;
- stale/conflict/concurrency cases;
- cancellation/retry behavior;
- degraded/unavailable backend behavior;
- timezone/locale cases.

### Q6 — performance

Budgets are measured before becoming numeric gates. Production client must track at least:

- route/startup payload and code splitting;
- interaction responsiveness;
- long tasks/main-thread blocking;
- layout shift;
- render frequency on dense surfaces;
- image/font/network cost;
- memory/leak behavior in long-running sessions.

Do not invent arbitrary thresholds before the production renderer exists; establish baselines then promote meaningful budgets to blocking gates.

Performance optimization is not allowed to silently alter frozen interaction or visual behavior. If maintaining the contract is impossible, the trade-off is raised as an explicit product decision before implementation.

### Q7 — security/supply chain

When `apps/web` exists:

- dependency lock/reproducibility;
- dependency review/static analysis as applicable;
- no secrets in client bundle/source;
- CSP/XSS/CSRF/session controls according to deployment architecture;
- immutable/traceable release artifact;
- source-map/error-reporting privacy review.

## CI activation rule

A workflow/check becomes a protected-main required check only after it exists, runs on relevant PRs, emits a stable context and its failure genuinely means merge must stop. This follows repository engineering-safety policy.

Active feature branches that receive direct implementation commits should run the relevant frontend CI as well. The purpose is to catch regressions before manual validation, not only at final merge time.

## Current executable guards

- `tests/prototypes/frontend-preprod-contracts.py` checks Stage and Whole-Home machine-readable contracts/fixtures for drift.
- `apps/web/src/features/home/ui/home-page.test.tsx` protects the real React Home ownership tree and AppShell boundary.
- `apps/web/e2e/home-structure.spec.ts` protects H0 Whole-Home pressure-width geometry, macro responsive modes and cross-region invariants.
- `apps/web/e2e/timeline-interactions.spec.ts` protects the current Home Timeline interaction and geometry contract.
- `feature/home-react` runs Frontend CI on push while the Home workstream is active.
- the frozen Home Timeline interaction suite is also executed in Firefox in CI because pointer/focus behavior is browser-sensitive.

These guards complement each other; none is a substitute for the final user acceptance gate.
