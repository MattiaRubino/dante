# DANTE — Frontend Quality Gates v0

- Status: **CURRENT PRE-PRODUCTION QUALITY BASELINE**

A render that looks correct at one width is not a frontend PASS.

## Gate classes

### Q0 — contract/static

- machine-readable contracts parse;
- contract versions agree;
- fixture identities are unique;
- required states/events/invariants exist;
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

### Q2 — responsive geometry

Current Home desktop guard matrix:

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

Golden screenshots and bounding-box assertions are complementary: screenshots catch visual drift; geometry assertions explain it.

### Q3 — visual regression

Accepted surfaces receive stable screenshot baselines for defined viewport/state combinations. Deliberate changes update baselines only with reviewed visual scope; a changed baseline is not automatically a pass.

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

### Q7 — security/supply chain

When `apps/web` exists:

- dependency lock/reproducibility;
- dependency review/static analysis as applicable;
- no secrets in client bundle/source;
- CSP/XSS/CSRF/session controls according to deployment architecture;
- immutable/traceable release artifact;
- source-map/error-reporting privacy review.

## CI activation rule

A future workflow/check becomes a protected-main required check only after it exists, runs on relevant PRs, emits a stable context and its failure genuinely means merge must stop. This follows repository engineering-safety policy.

## Current executable guard

`tests/prototypes/frontend-preprod-contracts.py` is intentionally stdlib-only and checks the v0 machine-readable contracts/fixtures for drift. It is an early guard, not a substitute for the future production test stack.
