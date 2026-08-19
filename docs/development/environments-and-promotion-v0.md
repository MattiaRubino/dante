# Environments and Promotion v0

- Status: **Engineering Foundation branch baseline — pending closure**
- Scope: LOCAL / DEV / UAT / PROD lifecycle, isolation and release promotion

## 1. Environment vocabulary

DANTE uses exactly these lifecycle concepts:

```text
LOCAL
individual developer execution context
not a remotely shared deployment stage

DEV
shared integration environment

UAT
production-like acceptance/release-candidate environment

PROD
real released environment and real user data
```

Optional **preview** environments may be created for pull requests/features when useful. Preview is ephemeral and not part of the durable promotion chain.

DEV/UAT/PROD are environments, **not Git branches**.

## 2. Source and deployment relationship

Protected `main` remains the only integrated source truth.

Normal flow:

```text
bounded feature/fix/chore branch
        ↓ PR + validation
protected main
        ↓ build immutable artifact
DEV
        ↓ select exact release candidate
UAT
        ↓ acceptance / release gates
PROD
```

A permanent `develop`, `staging` or `production` Git branch is not introduced.

Release state is represented by an exact commit/artifact/deployment record, not by maintaining parallel code histories.

## 3. LOCAL

LOCAL optimizes developer feedback while preserving production-relevant semantics where they matter.

Baseline:

- application processes run directly in the canonical developer environment for fast reload/debug where practical;
- stateful selected dependencies run through Docker Compose as they become active;
- PostgreSQL integration uses real PostgreSQL 18.4 and selected extensions, not SQLite substitution;
- synthetic fixtures only;
- local credentials are non-production and least-privilege;
- local `.env`-style files are ignored from Git;
- local state is disposable and rebuildable from migrations/seeds where applicable.

Windows server-side development uses WSL2/Linux semantics. Web/mobile platform tooling may run natively where appropriate.

LOCAL does not need to mirror every production service from day one. A selected specialist component is activated when the corresponding implementation capability requires it, subject to already-fixed Restate/recovery dormancy rules.

## 4. DEV

DEV is the first shared remote integration environment.

Purpose:

- validate accepted `main` integrations;
- exercise service-to-service/provider wiring;
- run shared integration/smoke tests;
- provide stable non-production endpoints for web/mobile integration;
- surface environment/configuration problems that local mocks cannot.

Rules:

- DEV deploys an accepted `main` artifact, never an arbitrary developer working tree;
- credentials and state are DEV-only;
- data is synthetic/test/demo data;
- production personal data is not copied into DEV as a convenience;
- destructive reset is allowed only through controlled DEV procedures;
- DEV outages do not justify relaxing PROD correctness/security boundaries in shared code.

Automatic deployment from accepted `main` is the target once stable CI/deployment exists. Before that automation exists, manual deployment remains traceable to exact commit/artifact identity.

## 5. UAT

UAT is the release-candidate acceptance environment, not a second development sandbox.

Purpose:

- end-to-end acceptance;
- realistic migration rehearsal;
- deployment/release rehearsal;
- provider integration verification;
- supported-client compatibility verification;
- applicable recovery/operability checks;
- final pre-production security/quality gates.

UAT should resemble PROD in topology/configuration behavior as far as practical without using production data or production credentials.

Required release-candidate identity:

```text
source commit SHA
build identifier
artifact/image digest where applicable
migration head/revision
client build identity where applicable
configuration/environment identity
```

A UAT PASS applies only to that exact release candidate and environment/configuration basis.

## 6. PROD

PROD contains real users, real data and released application state.

Rules:

- deploy only an accepted release candidate;
- use environment-scoped production identities/secrets;
- production state is not shared with DEV/UAT;
- migrations/deployments are auditable and serialized where required;
- observability/recovery/security controls activate according to accepted release requirements;
- emergency repair does not create a permanent alternate Git workflow;
- direct console/manual changes that materially alter infrastructure must be reconciled back into versioned desired state.

## 7. Environment isolation

Each remote environment is independently addressable and credentialed.

At minimum, where the provider supports separation:

```text
DEV database != UAT database != PROD database
DEV object namespace != UAT != PROD
DEV provider credentials != UAT != PROD
DEV secrets != UAT != PROD
DEV telemetry environment != UAT != PROD
```

Using separate schemas inside one production database as a substitute for environment isolation is not the default.

A lower environment must not possess broad production credentials “for convenience”.

## 8. Account/project isolation

Provider-specific account/project strategy is decided when each provider integration is implemented, but follows this preference order:

1. separate provider projects/accounts where isolation materially improves blast radius/security and is operationally reasonable;
2. otherwise provider-native environment namespaces/resources plus independent identities;
3. shared credential with environment-level branching only as an explicit exception where the provider makes stronger isolation unavailable or disproportionately harmful.

Any exception involving production privilege is documented and minimized.

## 9. Artifact identity

Deployable backend/server artifacts are immutable.

Preferred API identity:

```text
OCI image
repository/tag for human navigation
immutable digest for actual promotion/deploy identity
```

Never treat a mutable tag such as `latest` as sufficient release evidence.

Web artifact handling follows the hosting mechanism selected later, but the same principle applies: exact source/build/artifact identity must be traceable.

## 10. Build once, promote

For server/web targets, the default is:

```text
build artifact once
→ validate
→ deploy same artifact to DEV/UAT/PROD
→ inject environment-specific runtime configuration externally
```

This prevents environment-specific rebuild drift.

If a hosting platform fundamentally requires environment-specific compilation, that is an explicit exception and the builds must still be reproducible from the same locked source/toolchain with a recorded configuration identity.

## 11. Browser configuration consequence

Values compiled into browser JavaScript are public and often artifact-specific.

Therefore:

- secrets never use browser build-time variables;
- public runtime configuration should prefer a controlled runtime/public-config boundary where that preserves build-once promotion;
- environment-specific public values embedded at build time are allowed only when the hosting/client architecture requires it and the artifact identity records the difference.

This prevents a hidden “same version but different untracked web build” model.

## 12. Mobile promotion exception

Mobile distribution has different artifact constraints.

DEV/UAT/PROD mobile builds may require distinct:

- application/bundle identifiers;
- signing identities;
- deep-link schemes;
- provider application registrations;
- public environment endpoints;
- build profiles.

Therefore DANTE does **not** falsely claim that the same mobile binary is promoted unchanged across environments.

Professional invariant instead:

```text
same reviewed source commit
+ same locked dependency graph
+ explicit build profile
+ traceable build service/toolchain
+ environment-specific public configuration/signing
= reproducible mobile build identity
```

Production-grade mobile development uses Expo development builds. Production distribution uses explicit signed build/submission profiles when implemented.

Application identifiers should reserve clearly distinct non-production identities, e.g. conceptual `dev` / `uat` variants, while exact reverse-DNS identifiers are chosen during mobile scaffold.

## 13. Mobile OTA/update policy

Over-the-air JavaScript updates are not treated as a bypass around release governance.

Before EAS Update or another OTA mechanism becomes production-active, implementation must define:

- runtime compatibility policy;
- channel/environment isolation;
- rollout controls;
- rollback behavior;
- source/build traceability;
- migration/data compatibility;
- security approval path.

An OTA update that changes consequential behavior remains a release and must satisfy applicable tests/evaluation.

## 14. Release-candidate selection

UAT deployment is an explicit promotion of an existing successful build from `main`, not an implicit “whatever main is now”.

A newer commit landing on `main` does not mutate the identity of an in-flight release candidate.

If a fix is needed:

```text
new commit
→ new artifact
→ DEV verification
→ new UAT candidate
```

No patching binaries/containers in place.

## 15. Production release versioning

Before public semantic release versioning begins, commit SHA + build ID + artifact digest provide deployment identity.

When public release versioning begins:

- use repository tags such as `vX.Y.Z`;
- tag points to the exact accepted release commit;
- artifact metadata contains version + SHA;
- release notes/change record are generated/reviewed from actual merged changes;
- mobile store version/build numbers map back to source/build identity.

SemVer is a release-interface contract, not a reason to tag every development commit.

## 16. Database migration promotion

Migrations travel with the application source/artifact release but execute as a controlled release step.

Baseline release flow where a DB migration exists:

```text
migration chain validated in CI
→ DEV migrate + app deploy + smoke
→ UAT migration rehearsal + app deploy + E2E
→ PROD preflight
→ one serialized migration job
→ compatible application rollout
→ post-deploy verification
```

The exact order may vary for expand/migrate/contract changes, but application replicas do not independently run Alembic on boot.

## 17. Expand / migrate / contract

For changes that cannot tolerate an atomic stop-the-world rollout:

1. **expand** — add backward-compatible schema/capability;
2. **migrate** — move/backfill data while old/new readers remain valid;
3. **contract** — remove old shape only after every supported application/client no longer requires it.

This matters particularly because mobile clients may remain on older versions after a backend deploy.

A destructive DB migration that assumes every client updates instantly is not acceptable.

## 18. Rollback model

Rollback is capability-specific.

Possible actions:

- redeploy previous compatible application artifact;
- disable/rollback a feature through an approved control if one exists;
- issue a forward database repair migration;
- execute an accepted restore/recovery procedure for destructive data failure.

`alembic downgrade` is not a universal production rollback strategy.

Before a risky release, UAT/release evidence must state what rollback/forward-repair path actually exists.

## 19. Deployment concurrency

Per-environment deploy operations are serialized when concurrent execution could corrupt release state or race migrations.

GitHub Actions environment/job concurrency is used once workflows exist.

PR/test concurrency may cancel superseded runs to reduce waste, but a production deployment is never cancelled mid-critical mutation merely because a new commit appeared.

## 20. GitHub Environments

When deployment workflows are created, GitHub Environments are used for `dev`, `uat` and `prod` deployment boundaries.

They may scope:

- environment secrets/variables;
- allowed deployment sources;
- approval/protection rules;
- deployment history.

Protection strictness increases with consequence. PROD should require explicit promotion/approval when a meaningful release process exists.

Repository rules remain separately responsible for source integration safety.

## 21. Preview environments

Preview environments are optional and ephemeral.

Use when they materially help review web/API integration.

Rules:

- isolated non-production credentials/data;
- automatic expiration/cleanup where practical;
- no use as canonical shared DEV;
- no production secrets;
- no persistent personal test data that survives branch lifecycle without reason;
- preview deployment failure does not silently mutate DEV/UAT/PROD.

## 22. Data policy by environment

```text
LOCAL
synthetic/generated/developer-owned non-sensitive data

DEV
synthetic/shared test/demo data

UAT
representative synthetic/sanitized purpose-built acceptance data

PROD
real data under production privacy/security controls
```

Copying the production database into lower environments is forbidden by default.

If a future debugging need requires production-derived data, it needs an explicit privacy-safe sanitization/minimization process and separate authorization; it is never an ad-hoc dump.

## 23. Infrastructure drift

Once remote durable infrastructure is under IaC:

- intended state is code-reviewed;
- deployment plan/change is reviewable;
- emergency manual changes are documented and reconciled;
- drift detection is added when the chosen provider/IaC tooling supports useful reliable checks;
- secrets remain external to desired-state files.

## 24. Specialist service activation across environments

A selected service is not required to exist in all environments before its capability is implemented.

When a service activates, the implementation defines the minimal environment matrix needed for truthful validation.

Examples:

- PostgreSQL: LOCAL/DEV/UAT/PROD once backend persistence exists;
- R2: non-prod + PROD resources once real object handling exists;
- PowerSync: activation when mobile/offline slice arrives;
- Restate: remains dormant until fixed Class-B trigger;
- pgBackRest/S3: remains dormant in initial DEV; activates at the fixed recovery/production boundary or real rehearsal requirement.

Activation must preserve the accepted target and applicable PSV obligations.

## 25. Promotion gate principle

Every promotion claim is scoped to evidence actually executed.

```text
PR tests PASS
!= UAT PASS

UAT app E2E PASS
!= backup recovery PASS

migration rehearsal PASS
!= all PSV PASS

selected architecture
!= deployed component
```

Release checklists reference only validations applicable to the artifact/capabilities being released.
