# Frontend Materialization Integration Hardening

- Status: **ACTIVE — PR #28 / DEPENDENCY-REVIEW ACCEPTED-RISK REPAIR**
- Branch: `chore/frontend-materialization-integration`
- Main base: `fd3bc8dd918cf6aadeff4572221af68612c3cb42`
- Closed frontend source: `893edbbb5fd91377da71c0cc398ab9febdef06f3`
- Integration merge commit: `a4a5fb6a4a65db3f69f25ca52e128f4494c1b623`
- Integration hardening commit: `23ca32cb76e9ec2fde2cf73ecc94e9d5f8456df3`
- Pull request: `#28` (draft)
- Frontend materialization source status: **CLOSED / PASS**

## 1. Purpose

This workstream integrates the already-closed frontend materialization into current `main` without rewriting its evidence history, then performs only the bounded hardening required before the protected-main PR.

The integration branch is created from current `main`. The closed frontend materialization commit remains immutable evidence and is carried as a real merge parent rather than rebased or squashed away.

```text
closed frontend evidence
!=
integration reconciliation
!=
protected-main merge
```

## 2. Integration invariants

- current `main` is the starting truth for backend, repository governance and CURRENT documentation;
- `feature/frontend-materialization` is the implementation/evidence source for the closed frontend workstream;
- overlapping files are reconciled semantically; no side wins merely because Git can choose it mechanically;
- backend CP1..CP5 and protected-main backend controls must not regress;
- frontend FM-00..FM-07 evidence must not be weakened or relabelled;
- the React/ReactDOM workspace peer diagnostic remains known/non-blocking unless new evidence changes its cause;
- no `nodeLinker`, hoisting or peer-suppression workaround is introduced in this scope;
- no product vertical is implemented in this scope.

## 3. Integration hardening findings

The post-materialization review identified these bounded repairs before PR:

1. include `apps/mobile/src/**/*.ts(x)` explicitly in the Mobile TypeScript project;
2. make Expo dependency compatibility (`expo install --check`) a reusable root command and CI gate;
3. make CI repository-immutability checking include untracked residue, not only tracked diffs;
4. add a stable aggregate `Frontend CI Gate` above `Quality`, `Web E2E` and `Mobile Bundle`;
5. use workflow-level `permissions: {}` and grant only `contents: read` to checkout jobs;
6. make the pnpm 24-hour minimum release age explicit repository policy;
7. add the real npm/pnpm workspace to Dependabot alongside uv and GitHub Actions;
8. reconcile specification drift discovered through direct materialization evidence;
9. reconcile stale CURRENT documentation against both the integrated backend state and the closed frontend materialization state.

## 4. Direct materialization evidence that remains authoritative

The closed frontend source already proved, at its stated scopes:

- Node 24.19.0 / pnpm 11.22.0 / TypeScript 6.0.3 strict workspace;
- Web React/Vite/TanStack Router production build and Chromium production-preview E2E;
- Expo SDK 57 / React Native 0.86 Android Hermes bundle smoke;
- stronger prior direct Android emulator/Metro/Hermes runtime evidence;
- deterministic generated-source checks;
- dependency/cycle architecture checks;
- shared `@dante/design-tokens`, `@dante/i18n`, `@dante/time` packages;
- Vitest unit baseline;
- GitHub-hosted Frontend CI;
- fresh-clone/fresh-store/fresh-browser FM-07 clean materialization with zero repository residue after `.turbo/` hygiene repair.

Integration hardening does not retroactively turn untested future capabilities into PASS.

## 5. Combined-candidate validation target

Before protected-main merge authorization, the combined candidate must prove:

```text
frozen frontend install
format
lint
strict TypeScript
architecture/cycle rules
generated-source drift
unit tests
Web production build
Web E2E
Expo dependency compatibility
Android Hermes bundle smoke
repository tracked + untracked cleanliness
Backend CI
Dependency Review
Frontend CI
Frontend CI Gate
```

The PR must be current with `main` and must preserve the repository ruleset semantics.

The first real PR #28 combined run on integration-hardening commit `23ca32cb76e9ec2fde2cf73ecc94e9d5f8456df3` observed:

```text
Backend CI          PASS
Frontend CI         PASS
Quality             PASS
Web E2E             PASS
Mobile Bundle       PASS
Frontend CI Gate    PASS
Dependency Review   FAIL
```

The Dependency Review failure is not classified as a frontend runtime/test regression. It identified two high-severity advisories on the transitive build/development dependency `image-size@1.2.1` introduced by the selected Expo/Metro toolchain.

## 6. Dependency Review accepted-risk exception

### 6.1 Proven dependency path

PR #28 Dependency Review and lockfile readback prove the relevant chain:

```text
Expo SDK 57
-> @expo/metro 56.0.0
-> metro 0.84.4
-> image-size 1.2.1
```

The failing advisories are:

```text
GHSA-5p2g-fcmc-qvqq
JXL / HEIF parser denial of service through infinite loops

GHSA-w3rx-r6r6-pgpr
ICNS parser denial of service through an infinite loop
```

At the 2026-08-23 review boundary, no installable patched `image-size` release was available for these advisories. Forcing an unqualified Metro/Expo graph override would therefore trade a known bounded tooling risk for an unvalidated framework/runtime compatibility change.

### 6.2 Exposure classification

The vulnerable package is reached by Metro build/development asset processing. It is not a DANTE production server request-processing dependency and is not a deployed application runtime dependency exposed as a generic image-parsing endpoint.

Current bounded exposure/mitigation:

```text
input boundary              repository / PR-controlled frontend assets
GitHub token                contents: read only
PROD/deployment secrets     absent
Mobile CI                   timeout-minutes: 20
selected Expo/Metro graph   retained / directly validated
```

This does not make the advisories harmless; it makes the accepted exposure materially narrower than changing the framework dependency graph without qualification.

### 6.3 Exception policy

Dependency Review remains fail-closed at the existing repository policy:

```text
fail-on-severity: moderate
fail-on-scopes: runtime, development, unknown
```

Only these exact advisories are temporarily allowed:

```text
GHSA-5p2g-fcmc-qvqq
GHSA-w3rx-r6r6-pgpr
```

No `warn-only`, severity reduction, scope reduction or global vulnerability bypass is authorized.

Accepted-risk review deadline:

```text
2026-09-23
```

Remove the exception earlier when either condition becomes true:

```text
Expo/Metro no longer resolves a vulnerable image-size version
OR
a patched/replacement upstream path becomes available and passes DANTE qualification
```

The dependency-update/security review path must re-check these advisory IDs rather than carrying the exception indefinitely.

## 7. Frontend CI Gate calibration

`Frontend CI Gate` is introduced as the stable aggregate context but is **not** promoted to a required main check merely because the YAML exists.

Required-check promotion protocol:

```text
real PR context observed
-> green
-> controlled deliberate red proving failure propagation
-> recovery green
-> only then ruleset promotion in a separate explicit mutation
```

The first real green `Frontend CI Gate` context has now been observed on PR #28. Deliberate-red and recovery-green calibration remain pending.

## 8. Future activation register

The following capabilities are deliberately **not** materialized merely for completeness. Each has an activation trigger. When the trigger first becomes real, the owning workstream must reopen this register and either materialize the capability or record evidence for a different decision.

### First real product vertical

- qualify `eslint-config-expo` and current React Hooks lint rules;
- extend executable architecture enforcement to feature public APIs and app-local `ui/` / `platform/` direction when those boundaries contain real code;
- establish Web component-test baseline for real components;
- establish React Native Testing Library baseline when a real Mobile feature consumer exists.

### First real product UI / design-system surface

- adopt WCAG 2.2 AA as Web accessibility target;
- add automated accessibility checks (for example axe) on representative UI;
- activate Storybook only when reusable DANTE UI components justify an isolated catalog;
- activate visual regression only after stable visual surfaces exist.

### First real form

- qualify TanStack Form + Zod against the actual form semantics and platform consumers.

### First remote product API

- materialize FastAPI OpenAPI -> Orval generation;
- create `@dante/api-client` only with real generated transport consumers;
- activate TanStack Query for remote-request state;
- add deterministic generated-transport drift checks;
- keep authentication storage/session mechanics outside generated transport code.

### First Mobile offline operation

- activate PowerSync and the selected encrypted SQLite path;
- qualify OP-SQLite/SQLCipher/runtime compatibility at the then-current supported versions;
- implement identity-scoped local database/key lifecycle;
- prove offline staging -> backend accept/reject -> reconciliation semantics;
- add conflict/rejection/retry tests for the concrete operation.

### First shared DEV / Web deployment

- materialize versioned Zod-validated public runtime config;
- activate selected Cloudflare Web delivery boundary;
- activate Sentry behind bounded app/platform observability adapters;
- validate source maps and privacy-minimized telemetry.

### First Mobile release candidate

- activate EAS Build / Submit / Update at the real release boundary;
- add Maestro for critical Mobile flows where it provides meaningful device evidence;
- perform signed-device validation;
- perform iOS validation when iOS becomes an activated release target rather than inferring it from Android.

### Post-integration security maturation

- activate GitHub CodeQL default setup after the integrated TypeScript + Python source is on `main`;
- observe real CodeQL contexts/results before considering required-check promotion;
- apply OWASP ASVS/MASVS-derived checks at concrete Auth/session/storage/network/release boundaries rather than as a ceremonial checklist.

### Pre-production maturity

- broaden critical Web E2E to Firefox/WebKit when browser support becomes release-relevant;
- define and measure Web performance/Core Web Vitals budgets on representative product pages;
- add SBOM/provenance/attestation controls if the real release chain requires them;
- define a dependency-license policy before commercial/public distribution requires enforcement;
- add `SECURITY.md` and vulnerability-intake process before public production release;
- run explicit privacy/security threat review for activated Auth, local personal-data storage, sync and release surfaces.

### Scale-triggered only

Do not introduce these before measured organizational/runtime need:

- Turborepo remote cache;
- merge queue;
- CODEOWNERS / required human reviewers;
- generic feature-flag infrastructure;
- large browser/device farms.

## 9. Explicitly out of scope

- Access/Home product implementation;
- backend business-schema implementation;
- PowerSync activation now;
- TanStack Query/Form activation now;
- Orval generation now;
- Sentry/Cloudflare/EAS activation now;
- CodeQL activation now;
- required-check ruleset mutation;
- merge into `main` without separate final authorization;
- React version changes or peer-warning suppression;
- pnpm hoisting/nodeLinker changes;
- speculative shared packages or empty architecture directories;
- global vulnerability suppression or weakening Dependency Review policy.

## 10. Exit condition

This workstream can close only when the combined branch is semantically reconciled, the applicable combined candidate validation is green, the real PR contexts have been observed, the deliberate-red/recovery calibration for `Frontend CI Gate` is complete, and durable CURRENT documentation is coherent with the integrated backend + frontend state.
