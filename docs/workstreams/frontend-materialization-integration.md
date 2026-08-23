# Frontend Materialization Integration Hardening

- Status: **ACTIVE — PR #28 / RECOVERY GREEN RUN PENDING**
- Branch: `chore/frontend-materialization-integration`
- Main base at branch creation: `fd3bc8dd918cf6aadeff4572221af68612c3cb42`
- Closed frontend source: `893edbbb5fd91377da71c0cc398ab9febdef06f3`
- Integration merge commit: `a4a5fb6a4a65db3f69f25ca52e128f4494c1b623`
- Integration hardening commit: `23ca32cb76e9ec2fde2cf73ecc94e9d5f8456df3`
- First accepted-risk commit: `ca66541f3dc833e3c6fb0d67fe532651b880ce3a`
- Second accepted-risk / first fully-green combined candidate: `a91fbfc3dcce4ada128cd1c9ae0971eadb531e06`
- Current-truth reconciliation commit: `79b55b3a1986cc910af0ce84df411314e8453e80`
- Deliberate-red calibration commit: `6491b0dfdf4d6d005017b4a1f9a021976a0b9ff8`
- Recovery commit SHA: resolve from current branch HEAD after this commit; a commit cannot contain its own SHA.
- Pull request: `#28` (draft)
- Frontend materialization source status: **CLOSED / PASS**

## 1. Purpose

Integrate the already-closed frontend materialization into current protected-main truth without rewriting its evidence history, apply bounded integration hardening, calibrate the aggregate frontend CI gate, and reach a merge-ready combined candidate.

```text
closed frontend evidence
!=
integration reconciliation
!=
protected-main merge
```

## 2. Integration invariants

- current `main` is the starting authority for backend, repository governance and integrated CURRENT truth;
- `feature/frontend-materialization` remains immutable closed evidence for FM-00..FM-07;
- overlapping files are reconciled semantically rather than mechanically choosing one side;
- backend CP1..CP5 and protected-main controls must not regress;
- frontend FM-00..FM-07 evidence must not be weakened or relabelled;
- selected != installed != configured != directly validated;
- the known React/react-dom workspace peer diagnostic remains non-blocking unless new evidence changes its cause;
- no `nodeLinker`, hoisting, packageExtensions or peer-suppression workaround is introduced merely to silence diagnostics;
- no product vertical is implemented in this scope.

## 3. Integration hardening completed

This branch has materialized the bounded repairs found by the post-materialization review:

1. `apps/mobile/tsconfig.json` explicitly includes `src/**/*.ts` and `src/**/*.tsx`;
2. Expo dependency compatibility is a reusable root command and Mobile CI gate;
3. CI repository immutability rejects tracked **and untracked** residue;
4. stable aggregate `Frontend CI Gate` exists above `Quality`, `Web E2E`, `Mobile Bundle`;
5. Frontend CI uses workflow-level `permissions: {}` and grants only `contents: read` to checkout jobs;
6. pnpm 24-hour `minimumReleaseAge` is explicit repository policy;
7. Dependabot covers the npm/pnpm workspace alongside uv and GitHub Actions;
8. narrow Dependency Review accepted-risk exceptions are documented and time-bounded;
9. CURRENT documentation is reconciled against integrated backend + closed frontend materialization truth;
10. version-specific Frontend Foundation drift is qualified by later direct materialization evidence.

## 4. Closed frontend evidence authority

`docs/workstreams/frontend-materialization.md` remains the detailed FM evidence authority.

Directly proved at the stated scopes:

```text
Node 24.19.0 / pnpm 11.22.0 / TypeScript 6.0.3 strict
Web React 19.2.8 / React DOM 19.2.8 / Vite 8.2.1
TanStack Router 1.170.31
Expo SDK 57.x / clean resolve 57.0.15
React Native 0.86.2 / Mobile React 19.2.3
Gesture Handler 2.32.0 / Reanimated 4.5.1
@dante/design-tokens / @dante/i18n / @dante/time
Vitest 4.1.11 / Playwright 1.62.1
fresh frozen pnpm install
strict TypeScript
architecture graph 36 modules / 45 deps / 0 violations
generated-source drift
10 unit tests
Web production build + Chromium E2E
Android Hermes bundle smoke
Android emulator / Metro / Hermes runtime
Expo dependency compatibility
fresh Playwright bootstrap
zero tracked/untracked repository residue
GitHub-hosted Frontend CI
```

Integration hardening does not turn future capabilities into PASS.

## 5. Materialization qualification of design-time Foundation

Later direct evidence qualifies version-specific design-time wording:

```text
Temporal implementation    temporal-polyfill 1.0.4
Gesture Handler            2.32.0 under Expo SDK 57
Web E2E directory          apps/web/e2e/
Mobile React               19.2.3 / Expo compatibility PASS
Web React / React DOM      19.2.8 / 19.2.8
```

Therefore older design-time examples such as `@js-temporal/polyfill`, Gesture Handler “3 line” or `apps/web/tests/e2e/` do not override the directly validated implementation. This is a bounded qualification, not a wholesale architecture reopening.

## 6. Combined-candidate validation target

Before protected-main merge authorization the combined candidate must prove:

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
branch current with main
```

### 6.1 First fully-green combined candidate

Candidate `a91fbfc3dcce4ada128cd1c9ae0971eadb531e06` observed:

```text
Dependency Review   PASS
Backend CI          PASS
Frontend CI         PASS
Quality             PASS
Web E2E             PASS
Mobile Bundle       PASS
Frontend CI Gate    PASS
```

### 6.2 Current-truth reconciliation candidate

Commit `79b55b3a1986cc910af0ce84df411314e8453e80` reconciled stale CURRENT documentation and then earned the same full hosted green result:

```text
Dependency Review   PASS
Backend CI          PASS
Backend CI Gate     PASS
Frontend CI         PASS
Quality             PASS
Web E2E             PASS
Mobile Bundle       PASS
Frontend CI Gate    PASS
```

## 7. Dependency Review accepted-risk register

Dependency Review remains fail-closed:

```text
fail-on-severity: moderate
fail-on-scopes: runtime, development, unknown
```

No warn-only mode, severity reduction, scope reduction or global vulnerability bypass is authorized.

Temporarily allowed exact advisory IDs:

```text
GHSA-5p2g-fcmc-qvqq
GHSA-w3rx-r6r6-pgpr
GHSA-w5hq-g745-h8pq
```

Proven paths:

```text
Expo SDK 57
-> @expo/metro 56.0.0
-> metro 0.84.4
-> image-size 1.2.1

Expo SDK 57 tooling
-> @expo/config-plugins
-> xcode 3.0.1
-> uuid 7.0.3
```

Current exposure is bounded to frontend build/configuration tooling and repository/PR-controlled inputs; it is not a DANTE production server request-processing surface. DANTE does not directly call the affected uuid API. Direct iOS release validation is not currently activated.

Review deadline:

```text
2026-09-23
```

Remove or requalify earlier when the Expo/Metro/xcode dependency path no longer resolves the vulnerable package, a patched/replacement path passes DANTE qualification, or an affected DANTE/iOS boundary activates and changes the exposure classification.

## 8. Frontend CI Gate calibration

`Frontend CI Gate` is the stable aggregate context above all mandatory frontend jobs.

### 8.1 Real green — PASS

Observed on real PR #28 before deliberate-red calibration:

```text
Quality             PASS
Web E2E             PASS
Mobile Bundle       PASS
Frontend CI Gate    PASS
```

### 8.2 Controlled deliberate red — PASS

Calibration commit:

```text
6491b0dfdf4d6d005017b4a1f9a021976a0b9ff8
```

Temporary workflow-only step:

```text
Controlled Frontend CI Gate calibration failure
run: exit 1
```

Observed remote result:

```text
Quality             FAILURE — intentional calibration step
Web E2E             PASS
Mobile Bundle       PASS
Frontend CI Gate    FAILURE — mandatory upstream failure propagated
Backend CI          PASS
Dependency Review   PASS
```

This directly proves the aggregate gate fails when one mandatory frontend upstream fails while independent frontend and backend/security paths remain healthy.

No application code, dependency, security-policy weakening or production behavior was changed for the deliberate red.

### 8.3 Workflow restoration

The production workflow in this recovery commit restores the exact previously-green workflow blob:

```text
14626e696d91d3f184b58dac111cd88102832e91
```

The temporary deliberate-red step is removed and no other workflow behavior is changed.

Current calibration state after this commit is created:

```text
real context emitted       PASS
real PR green              PASS
deliberate red             PASS
exact workflow restoration DONE
recovery green             PENDING REMOTE RUN
required on main           NO
```

Required-check promotion remains a separate explicit repository-ruleset mutation after recovery green.

## 9. Current-truth reconciliation

Current durable truth now records:

```text
Backend CP1..CP5                  CLOSED / integrated via PR #24
Frontend Foundation              CLOSED / integrated via PR #22
Frontend Materialization         CLOSED / PASS
PR #28 Integration Hardening     ACTIVE
Frontend CI Gate                 emitted / green-before-calibration / deliberate-red proven / not required
Dependency Review                green with 3 exact temporary accepted-risk exceptions
Concrete business schema         NOT STARTED
Product verticals                NOT STARTED
Production deployment            NOT STARTED
```

Historical Foundation documents remain design-time evidence; current ADR/current-decision docs state how later materialization qualifies version-specific implementation details.

## 10. Future activation register

These capabilities are deliberately dormant until their trigger becomes real. The owning workstream must reopen this register at activation time.

### First real product vertical

- qualify `eslint-config-expo` and current React Hooks lint rules against the actual dependency graph;
- extend executable architecture enforcement to feature public APIs and app-local `ui/` / `platform/` direction when real code exists;
- establish Web component-test baseline for real components;
- establish React Native Testing Library baseline where a real Mobile feature consumer exists.

### First real product UI / design-system surface

- adopt WCAG 2.2 AA as the Web accessibility target;
- add representative automated accessibility checks such as axe;
- activate Storybook only when reusable DANTE UI components justify an isolated catalog;
- activate visual regression only after stable visual surfaces exist.

### First real form

- qualify TanStack Form + Zod against real form semantics and platform consumers.

### First remote product API

- materialize FastAPI OpenAPI -> Orval generation;
- create `@dante/api-client` only with real generated transport consumers;
- activate TanStack Query for request/response remote state;
- add deterministic generated-transport drift checks;
- keep Auth/session storage mechanics outside generated transport.

### First Mobile offline operation

- activate PowerSync and the selected encrypted SQLite path;
- qualify then-current OP-SQLite/SQLCipher/runtime compatibility;
- implement identity-scoped local database/key lifecycle;
- prove offline staging -> backend accept/reject -> reconciliation;
- add conflict/rejection/retry tests for the concrete operation.

### First shared DEV / Web deployment

- materialize versioned Zod-validated public runtime config;
- activate selected Cloudflare Web delivery boundary;
- activate Sentry behind bounded observability adapters;
- validate source maps and privacy-minimized telemetry.

### First Mobile release candidate

- activate EAS Build / Submit / Update;
- add Maestro for critical Mobile flows where it provides meaningful device evidence;
- perform signed-device validation;
- perform iOS direct validation when iOS becomes an activated release target.

### Post-integration security maturation

- activate GitHub CodeQL default setup after integrated TypeScript + Python source is on `main`;
- observe real CodeQL results/contexts before any required promotion;
- apply OWASP ASVS/MASVS-derived controls at concrete Auth/session/storage/network/release boundaries.

### Pre-production maturity

- broaden critical Web E2E to Firefox/WebKit when browser support becomes release-relevant;
- define representative Web performance/Core Web Vitals budgets;
- add SBOM/provenance/attestation controls if the release chain requires them;
- define dependency-license policy before commercial/public distribution requires enforcement;
- add `SECURITY.md` and vulnerability intake before public production release;
- run explicit privacy/security threat review for activated Auth, local personal-data storage, sync and release surfaces.

### Scale-triggered only

Do not introduce before measured organizational/runtime need:

- Turborepo remote cache;
- merge queue;
- CODEOWNERS / required human reviewers;
- generic feature-flag infrastructure;
- large browser/device farms.

## 11. Explicitly out of scope

- Access/Home product implementation;
- backend business-schema implementation;
- PowerSync activation now;
- TanStack Query/Form activation now;
- Orval generation now;
- Sentry/Cloudflare/EAS activation now;
- CodeQL activation now;
- main ruleset mutation in this recovery commit;
- merge into `main` without separate final authorization;
- React version changes or peer-warning suppression;
- pnpm hoisting/nodeLinker changes;
- unsupported dependency overrides;
- speculative shared packages or empty architecture directories;
- global vulnerability suppression.

## 12. Exit condition / exact next sequence

After this recovery commit:

```text
1. prove Recovery Green on PR #28
2. verify branch is current with main
3. if desired, open a separate explicit gate to promote Frontend CI Gate to required on main
4. perform final PR diff/current-docs/accepted-risk review
5. obtain separate protected-main merge authorization
```

After protected-main integration, CodeQL default setup is the next repository-security activation candidate. Product work may then begin through vertical slices, consulting the activation register rather than pre-installing every future large-app capability.
