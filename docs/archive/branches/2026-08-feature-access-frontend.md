# Branch history — feature/access-frontend

> Historical branch record. **NON-AUTHORITATIVE for current project state.**
> Current truth lives in current project/frontend documentation, code, tests and later full-stack Access/Auth contracts.

## Identity

- Repository: `MattiaRubino/dante`
- Branch: `feature/access-frontend`
- Workstream: Access frontend — production pre-backend materialization and release hardening
- Frozen design input: `prototype/access-system` at `469b68370e80185fa8a16d5335845e402ee1de3b`
- Main-reconciliation commit: `1df54bcb2d584efece68cbf349ac9e87eb3a93c7`
- Integration PR: recorded by the branch closure PR after this history record is created

## Purpose

The branch converted the approved Access cross-platform design/specification into a production-shaped Web frontend without inventing a fake authentication backend. It established the complete frontend-owned state graph, production copy/localization, accessibility and responsive behavior, while deliberately stopping backend-authoritative transitions until the real Auth vertical exists.

The branch does **not** claim that the whole Access/Auth product vertical is complete. Its closure means the pre-backend frontend materialization is accepted and can become the baseline consumed by the later full-stack Auth vertical.

## Milestones

```text
AF-01D  shell completion / professional polish      PASS
AF-02A  complete pre-backend frontend state graph   PASS
AF-02B  downstream surface hardening                PASS
AF-03A  release-hardening viewport matrix           PASS
```

### AF-01D

Accepted the production Web shell, final IT/EN hero copy, locale behavior, password visibility, brand-stage composition, accessibility foundations and responsive desktop/narrow/phone direction.

### AF-02A

Materialized the approved Access state inventory and orthogonal transport conditions without creating a fake Auth service. Frontend-owned navigation can advance locally; backend-authoritative transitions remain safely blocked as `backend-required` internally and never fabricate success.

### AF-02B

Hardened all downstream surfaces including verification, recovery/reset, provider pending/error, account linking, reauthentication, setup and first-run choices. Final accepted evidence included:

```text
Playwright reachable E2E             10 / 10 PASS
Web unit/component tests             17 / 17 PASS
workspace typecheck                   5 / 5 PASS
architecture                         PASS
generated sources                    PASS / deterministic
Web production build                 PASS
axe desktop downstream inventory     PASS
axe phone verify/reset/setup-start   PASS
390px horizontal overflow            PASS
```

### AF-03A

Expanded release hardening across the representative viewport matrix, English text pressure, reduced motion, accessibility and overflow behavior.

At commit `9b649464915e9d3e89cc2383539f5da156f69361`, the full automated frontend gate was proven green, including 21/21 release-matrix E2E checks. A final one-line visual refinement then reduced the large-desktop auth-card maximum from 509px to 480px in commit `78b767a963fbc06bc93fa3d4d3160cb08f0c320e`; exact delta/readback and final 1440x900 + 1024x768 visual review were accepted. No claim is made that the entire automated suite was rerun after that one-line visual-only patch.

This distinction is retained deliberately rather than rewriting evidence as stronger than it was.

## Main reconciliation

Before closure, the branch was reconciled with protected `main` at `117cf282917e45483f7ee7037e27795d65a07052` through merge commit:

```text
1df54bcb2d584efece68cbf349ac9e87eb3a93c7
```

The reconciliation used no rebase and no force push. A three-way audit from merge-base `87fe668c2ade78b17e0326d635e4d7a67920ae8a` showed zero path overlap between files changed by Access and files changed by the newer main line. The merged tree therefore preserved the Access delta while taking the current CP6/backend/database/infra/documentation baseline from main.

## Final frontend baseline

The accepted materialization includes:

- full Web Access state/surface inventory;
- DANTE A3.4 desktop visual direction;
- M1.2 + PRG-0 retained as mobile design authority, not native implementation;
- canonical Access invariants and state graph;
- IT/EN localization;
- local safe validation and browser offline handling;
- Testing Library, Playwright and axe coverage;
- design-token/architecture/generated-output gates;
- production-responsive release pressure;
- no fake backend-success path.

Current durable frontend truth is consolidated in:

- `docs/frontend/access.md`
- current `apps/web` Access implementation/tests
- shared current design-token/i18n contracts

## Explicit non-claims at branch closure

The branch did not implement or prove:

```text
real backend Auth
real provider transaction validation
real verification/recovery mutation
real sessions / revocation / reauth backend
stable Auth OpenAPI and generated binding
full-stack Auth E2E
native Mobile Access
real legal destinations
real authenticated Home handoff
```

Those move forward to a new full-stack product vertical created from protected `main` after this branch is integrated.

## Documentation disposition

The active-branch files:

- `docs/workstreams/access-frontend.md`
- `docs/workstreams/access-frontend-live-handoff.md`

were branch-operational/current-while-active artifacts. Before protected-main integration their meaningful payload was classified as follows:

```text
current Access frontend truth       -> docs/frontend/access.md + code/tests
accepted milestone/evidence         -> this branch history + Git commits
product/security invariants         -> docs/frontend/access.md
future full-stack requirements      -> docs/frontend/access.md + ROADMAP/PROJECT-STATUS
cross-chat continuity mechanics     -> Git history only
superseded branch-routing prose     -> discarded
```

The two workstream/handoff files are therefore removed rather than copied into `main` as permanent operational history.

## Integration evidence

Protected-main integration is allowed only through the final branch PR after both Frontend CI and Backend CI are green on the final PR head. The PR/merge record is the authoritative integration evidence; this historical document intentionally does not predict a merge commit SHA before GitHub creates it.
