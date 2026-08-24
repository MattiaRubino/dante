# Frontend Materialization Integration Hardening

- Status: **ACTIVE — PR #28 / READY / RECOVERY GREEN PASS / REQUIRED-CHECK PROMOTION OWNER-CONFIRMED / FINAL MERGE GATE**
- Branch: `chore/frontend-materialization-integration`
- Main base at branch creation: `fd3bc8dd918cf6aadeff4572221af68612c3cb42`
- Closed frontend source: `893edbbb5fd91377da71c0cc398ab9febdef06f3`
- Integration merge commit: `a4a5fb6a4a65db3f69f25ca52e128f4494c1b623`
- Integration hardening commit: `23ca32cb76e9ec2fde2cf73ecc94e9d5f8456df3`
- First accepted-risk commit: `ca66541f3dc833e3c6fb0d67fe532651b880ce3a`
- First fully-green combined candidate: `a91fbfc3dcce4ada128cd1c9ae0971eadb531e06`
- Current-truth reconciliation commit: `79b55b3a1986cc910af0ce84df411314e8453e80`
- Deliberate-red calibration commit: `6491b0dfdf4d6d005017b4a1f9a021976a0b9ff8`
- Recovery-green commit: `02ee9034f37000819afb2c27b0bd826b128f69b5`
- Promotion-documentation commit: `c551185708936c052248b3bd9c2eebfc41a7d098`
- Pre-reconciliation final-doc head: `bdd6e08cbca4c19989502235855d52a620d29fb5`
- Pull request: `#28` — **OPEN / READY**
- Frontend materialization source status: **CLOSED / PASS**

## 1. Purpose

Integrate the closed frontend materialization into current protected-main truth without rewriting its evidence history, apply bounded integration hardening, calibrate the aggregate frontend CI gate and prepare a merge-ready candidate.

```text
closed frontend evidence
!=
integration reconciliation
!=
protected-main merge
```

## 2. Integration invariants

- current `main` remains the starting authority for integrated backend/repository truth;
- `feature/frontend-materialization` remains immutable closed evidence for FM-00..FM-07;
- overlaps are reconciled semantically;
- backend CP1..CP5 and existing protected-main controls must not regress;
- selected != installed != configured != directly validated;
- the known React/react-dom workspace peer diagnostic remains non-blocking unless new evidence changes its cause;
- no hoisting/nodeLinker/packageExtensions/peer-suppression workaround is introduced merely to silence diagnostics;
- no product vertical is implemented here.

## 3. Integration hardening completed

1. Mobile TypeScript explicitly covers `src/**/*.ts` and `src/**/*.tsx`;
2. Expo dependency compatibility is a reusable root command and Mobile CI gate;
3. CI repository immutability rejects tracked and untracked residue;
4. stable aggregate `Frontend CI Gate` exists above `Quality`, `Web E2E`, `Mobile Bundle`;
5. Frontend CI defaults to `permissions: {}` with `contents: read` only where needed;
6. pnpm 24-hour `minimumReleaseAge` is explicit repository policy;
7. Dependabot covers npm/pnpm alongside uv and GitHub Actions;
8. Dependency Review exceptions are exact, documented and time-bounded;
9. CURRENT docs are reconciled with backend + frontend reality;
10. design-time Foundation drift is explicitly qualified by later materialization evidence.

## 4. Closed frontend evidence authority

`docs/workstreams/frontend-materialization.md` remains the detailed FM evidence source.

Directly proved at stated scopes:

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

## 5. Materialization qualification of design-time Foundation

Current implementation authority at the validated scopes:

```text
Temporal implementation    temporal-polyfill 1.0.4
Gesture Handler            2.32.0 under Expo SDK 57
Web E2E directory          apps/web/e2e/
Mobile React               19.2.3 / Expo compatibility PASS
Web React / React DOM      19.2.8 / 19.2.8
```

Older design-time examples such as `@js-temporal/polyfill`, Gesture Handler “3 line” or `apps/web/tests/e2e/` do not override later direct evidence.

## 6. Combined-candidate evidence

### First fully-green combined candidate

Candidate `a91fbfc3dcce4ada128cd1c9ae0971eadb531e06`:

```text
Dependency Review   PASS
Backend CI          PASS
Frontend CI         PASS
Quality             PASS
Web E2E             PASS
Mobile Bundle       PASS
Frontend CI Gate    PASS
```

### Current-truth candidate

Commit `79b55b3a1986cc910af0ce84df411314e8453e80` earned:

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

### Promotion-documentation checkpoint

Branch HEAD `c551185708936c052248b3bd9c2eebfc41a7d098` remained current against `main`, mergeable, review-thread clean and green at the workflow level:

```text
Dependency Review   PASS
Backend CI          PASS
Frontend CI         PASS
```

### Pre-reconciliation final-doc checkpoint

Head `bdd6e08cbca4c19989502235855d52a620d29fb5` was directly observed:

```text
branch relation     47 ahead / 0 behind
PR                   OPEN / READY / mergeable
review threads       0
Dependency Review    PASS
Backend Quality      PASS
Backend PostgreSQL   PASS
Backend CI Gate      PASS
Frontend Quality     PASS
Web E2E              PASS
Mobile Bundle        PASS
Frontend CI Gate     PASS
```

Any later documentation-only head must independently satisfy the same applicable hosted-CI/currentness/mergeability/thread-clean gate before protected-main merge authorization. This wording deliberately avoids embedding a commit's own SHA into itself.

## 7. Dependency Review accepted-risk register

Dependency Review remains fail-closed:

```text
fail-on-severity: moderate
fail-on-scopes: runtime, development, unknown
```

Exact temporary advisories:

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

Exposure is bounded to frontend build/configuration tooling and repository/PR-controlled inputs, not a DANTE production server request surface. DANTE does not directly call the affected uuid API. Direct iOS release validation is not active.

Review deadline: **2026-09-23**.

Remove/requalify as soon as the dependency path no longer resolves the vulnerable package, a patched/replacement path passes qualification, or an activated DANTE/iOS boundary changes exposure.

## 8. Frontend CI Gate calibration — COMPLETE

### Real green

```text
Quality             PASS
Web E2E             PASS
Mobile Bundle       PASS
Frontend CI Gate    PASS
```

### Controlled deliberate red

Commit:

```text
6491b0dfdf4d6d005017b4a1f9a021976a0b9ff8
```

Temporary workflow-only step:

```text
Controlled Frontend CI Gate calibration failure
run: exit 1
```

Observed:

```text
Quality             FAILURE — intentional
Web E2E             PASS
Mobile Bundle       PASS
Frontend CI Gate    FAILURE — mandatory upstream failure propagated
Backend CI          PASS
Dependency Review   PASS
```

### Exact restore + recovery green

Recovery commit:

```text
02ee9034f37000819afb2c27b0bd826b128f69b5
```

Restored workflow blob:

```text
14626e696d91d3f184b58dac111cd88102832e91
```

Observed recovery:

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

Final calibration classification:

```text
real context emitted       PASS
real green                 PASS
deliberate red             PASS
failure propagation        PASS
exact restore              PASS
recovery green             PASS
eligible for promotion     YES
```

## 9. Required-check promotion

Promotion is approved for:

```text
Frontend CI Gate
integration_id: 15368
source: GitHub Actions
```

The branch-local canonical ruleset JSON contains:

```text
Backend CI Gate
Dependency Review
Frontend CI Gate
```

with strict branch-up-to-date policy preserved.

Administrative evidence boundary:

```text
desired ruleset definition in branch   UPDATED
GitHub ruleset UI application          OWNER-CONFIRMED APPLIED
connector direct ruleset readback       UNAVAILABLE
```

The repository owner confirmed applying the `Frontend CI Gate` ruleset promotion. Because the available GitHub connector does not expose direct ruleset readback, the setting is recorded as owner-confirmed rather than independently API-verified. This limitation does not erase the directly calibrated green/red/recovery evidence of the emitted check itself.

## 10. Current truth

```text
Backend CP1..CP5                  CLOSED / integrated via PR #24
Frontend Foundation              CLOSED / integrated via PR #22
Frontend Materialization         CLOSED / PASS
PR #28 Integration Hardening     ACTIVE / READY / final merge gate
Frontend CI Gate calibration     COMPLETE
Frontend CI Gate promotion       OWNER-CONFIRMED APPLIED / DIRECT API READBACK UNAVAILABLE
Dependency Review                GREEN with 3 exact temporary accepted-risk exceptions
Concrete business schema         NOT STARTED
Product verticals                NOT STARTED
Production deployment            NOT STARTED
```

## 11. Future activation register

These capabilities remain deliberately dormant until the corresponding trigger becomes real.

### First real product vertical

- qualify `eslint-config-expo` and current React Hooks lint rules against the actual dependency graph;
- extend executable architecture enforcement to feature public APIs and app-local `ui/` / `platform/` direction;
- establish Web component tests for real components;
- establish React Native Testing Library where a real Mobile feature consumer exists.

### First real product UI / design-system surface

- adopt WCAG 2.2 AA as Web accessibility target;
- add representative automated accessibility checks such as axe;
- activate Storybook only when reusable DANTE UI components justify it;
- activate visual regression only after stable visual surfaces exist.

### First real form

- qualify TanStack Form + Zod against real form semantics and platform consumers.

### First remote product API

- materialize FastAPI OpenAPI -> Orval generation;
- create `@dante/api-client` only with real consumers;
- activate TanStack Query for request/response state;
- add deterministic generated-transport drift checks;
- keep Auth/session storage outside generated transport.

### First Mobile offline operation

- activate PowerSync + selected encrypted SQLite path;
- qualify current OP-SQLite/SQLCipher/runtime compatibility;
- implement identity-scoped local DB/key lifecycle;
- prove offline staging -> backend accept/reject -> reconciliation;
- add conflict/rejection/retry tests.

### First shared DEV / Web deployment

- materialize versioned Zod-validated public runtime config;
- activate Cloudflare Web delivery;
- activate Sentry behind bounded observability adapters;
- validate source maps and privacy-minimized telemetry.

### First Mobile release candidate

- activate EAS Build / Submit / Update;
- add Maestro where it adds meaningful device evidence;
- perform signed-device validation;
- perform iOS direct validation when iOS becomes an active release target.

### Post-integration security maturation

- activate GitHub CodeQL default setup after TypeScript + Python are integrated on `main`;
- observe real CodeQL results/contexts before any required promotion;
- apply OWASP ASVS/MASVS-derived controls at concrete Auth/session/storage/network/release boundaries.

### Pre-production maturity

- broaden critical Web E2E to Firefox/WebKit when release-relevant;
- define representative Web performance/Core Web Vitals budgets;
- add SBOM/provenance/attestation controls if the release chain requires them;
- define dependency-license policy before commercial/public distribution requires enforcement;
- add `SECURITY.md` and vulnerability intake before public production release;
- run explicit privacy/security threat review for activated Auth, local data, sync and release surfaces.

### Scale-triggered only

Do not introduce before measured need:

- Turborepo remote cache;
- merge queue;
- CODEOWNERS / required human reviewers;
- generic feature-flag infrastructure;
- large browser/device farms.

## 12. Explicitly out of scope

- Access/Home implementation;
- concrete backend business schema;
- PowerSync, Query/Form, Orval, Sentry, Cloudflare, EAS activation now;
- CodeQL activation now;
- merging PR #28 without separate authorization;
- React/peer-warning workarounds;
- pnpm hoisting/nodeLinker changes;
- unsupported dependency overrides;
- global vulnerability suppression.

## 13. Exact next sequence

```text
1. verify hosted CI green on the exact current PR #28 head
2. confirm branch remains current with main
3. confirm PR remains mergeable and review-thread clean
4. confirm accepted-risk register remains valid
5. obtain separate protected-main merge authorization
```

After protected-main integration, CodeQL default setup is the next repository-security activation candidate. Product work then proceeds through vertical slices while consulting this activation register.
