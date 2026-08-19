# Configuration and Secrets v0

- Status: **CLOSED / ACCEPTED BACKEND BASELINE**
- Scope: backend configuration, runtime identity, credentials, secret handling and environment isolation
- Frontend/web/mobile configuration: **DEFERRED to dedicated frontend workstream**

## 1. Decision

DANTE backend configuration is explicit, typed, environment-scoped and validated before the process accepts work.

Secrets are external security material. They are not source code, ordinary defaults, repository examples, image build arguments or canonical product/domain state.

Target hierarchy:

```text
MINIMIZE SECRETS
        ↓
WORKLOAD / FEDERATED IDENTITY where supported
        ↓
PROVIDER SECRET MANAGER for remaining secret material
        ↓
LEAST-PRIVILEGE RUNTIME ACCESS
        ↓
ROTATION + REVOCATION + AUDIT
```

The contract is provider-neutral.

## 2. Configuration classes

DANTE distinguishes:

```text
NON-SECRET DEPLOYMENT CONFIG
safe-to-disclose runtime/deployment behavior

SECRET
credential/private key/token material whose disclosure grants capability

BUILD / RELEASE IDENTITY
Git SHA, build ID, release/version, artifact identity

DOMAIN / BUSINESS CONFIGURATION
governed product rules/state that belong to canonical application data
```

Domain/business semantics do not drift into environment variables merely because they are configurable.

## 3. Environment identity

Promotion environments:

```text
LOCAL
DEV
UAT
PROD
```

Automated tests may use a test execution context, but TEST is not a fifth promotion environment.

Every backend process knows environment/release identity explicitly. The implementation uses a DANTE namespace and exposes validated equivalents of at least:

```text
DANTE_ENV
DANTE_RELEASE_SHA
DANTE_BUILD_ID
```

`DANTE_ENV` is a closed enum, not an arbitrary string.

## 4. Typed backend configuration

Use **pydantic-settings** as the typed bootstrap boundary.

Rules:

- construct one composed settings object or a small set of clearly owned settings groups during bootstrap;
- validate before requests/jobs are accepted;
- fail fast on required missing values;
- fail fast on malformed values;
- fail fast on dangerous cross-field/environment combinations;
- treat validated settings as immutable runtime state;
- inject configuration into components rather than reading process globals throughout the codebase;
- forbid scattered `if env == "prod"` business logic.

Exact module split is implementation-owned.

## 5. Safe defaults

A default is allowed only when an incorrect default cannot silently weaken security, privacy, durability or environment isolation.

Critical values normally have no permissive PROD fallback, including:

- environment identity;
- DB credential/resource identity;
- token/signing/encryption material;
- production provider identity/credential;
- destructive maintenance switches;
- security-relevant trusted-host/origin policy.

## 6. Cross-field safety invariants

Configuration validation rejects dangerous combinations, not only malformed scalar values.

Examples:

```text
PROD + debug enabled                       → REJECT
PROD + LOCAL/synthetic DB credential       → REJECT
PROD + DEV/UAT resource identity           → REJECT
DEV/UAT + PROD credential/resource binding → REJECT
unknown DANTE_ENV                           → REJECT
```

Provider-specific identifiers are validated once providers exist.

## 7. LOCAL configuration

Target backend shape:

```text
apps/backend/.env.example    COMMITTED; safe contract/example only
apps/backend/.env.local      IGNORED; LOCAL values only
```

`.env.example` contains names, safe dummy values where useful and required/optional guidance. It never contains live DEV/UAT/PROD credentials.

LOCAL credentials are synthetic and restricted to LOCAL resources.

## 8. Remote configuration

DEV/UAT/PROD do not depend on manually maintained repository `.env` files or ad-hoc files edited over SSH.

Non-secret configuration is supplied through deployment/IaC/platform configuration.

Secrets use the provider-native secret-management path chosen with the hosting platform.

The provider is deferred; the required properties are fixed.

## 9. Secret-manager requirements

A production-capable secret manager must provide, as applicable:

- encryption in transit/at rest under provider guarantees;
- fine-grained IAM/RBAC;
- environment isolation;
- workload/service identity integration;
- versioning;
- controlled rotation/revocation;
- auditable access/administration;
- safe disable/delete/recovery lifecycle;
- automation suitable for deployment/IaC;
- regional/data-residency controls where required.

A checked-in encrypted file is not the normal runtime secret-management system.

## 10. Secret delivery order

For remote environments prefer:

```text
1. eliminate stored secret through workload/managed identity
2. runtime retrieves required secret from provider manager using workload identity
3. provider-native secure secret projection/injection where direct retrieval is impractical
4. environment-variable injection only as a bounded fallback where runtime/provider requires it
```

Secrets are not baked into Docker `ENV`/`ARG`, OCI layers or committed deployment manifests.

Environment variables remain normal for non-sensitive configuration.

## 11. Workload identity

DANTE prefers identity over stored credentials.

Examples when supported:

- runtime workload identity → secret manager/cloud service;
- GitHub Actions OIDC → cloud deployment identity;
- provider-native managed identity → provider resource.

Trust policy is scoped to the narrow repository/workflow/environment/resource claims needed.

## 12. GitHub deployment identity

GitHub Actions uses OIDC/federated identity for cloud providers where a secure practical integration exists.

Benefits accepted as policy:

- avoid long-lived static cloud keys in GitHub;
- bind trust to repository/ref/environment/workflow claims;
- issue short-lived credentials only for the job needing them.

Static credentials are fallback only and require least privilege, environment ownership, rotation/revocation, no PR exposure and an incident replacement path.

## 13. GitHub Environments

When deployment workflows exist:

```text
dev
uat
prod
```

GitHub Environments scope deployment control/variables/secrets/protection as supported.

They complement, not replace, protected source integration and provider-side environment isolation.

## 14. Environment separation

Each remote environment receives independent identities/credentials/secrets.

```text
DEV credential --X--> PROD
UAT credential --X--> PROD
```

A lower environment must not receive production privilege for convenience.

## 15. PostgreSQL credential classes

At implementation, separate responsibilities where privilege differs materially:

```text
owner
migrator/deployment
runtime application
replication/sync when active
backup/recovery when active
```

Normal API runtime does not receive schema-owner/superuser capability merely to simplify deployment.

Connection strings are secrets if they embed credentials.

## 16. Provider/user tokens

OAuth/provider tokens tied to a DANTE user/account are **application data with a governed privacy/security lifecycle**, not generic deployment secrets.

Their eventual design must preserve ownership, provider/canonical separation, encryption/protection, refresh/revocation semantics, retention/deletion and non-leakage into logs/traces/errors.

Concrete schema/Auth design is deferred.

## 17. Logging and redaction

Forbidden by default:

```text
full environment dumps
settings objects exposing secret fields
Authorization headers
cookies/session tokens
OAuth refresh tokens
raw provider credentials
raw DB DSN with password
private signing/encryption keys
```

Operational logs use bounded metadata such as environment, provider class, correlation ID and safe error category.

Settings representations/helpers redact secret fields.

## 18. CI logs/artifacts

CI must not echo secrets or persist them in artifacts.

Rules:

- disable shell tracing around sensitive operations;
- do not upload generated config artifacts containing secrets;
- use synthetic credentials in ordinary tests;
- design PR validation to run without PROD secrets;
- untrusted/Dependabot PR execution receives no deployment credentials.

## 19. Rotation/revocation

Every long-lived secret introduced eventually has:

- owner;
- scope;
- creation mechanism;
- consumers;
- rotation mechanism;
- revocation mechanism;
- incident replacement procedure.

High-consequence rotation is tested before production dependence becomes material.

## 20. Repository policy

Never commit:

- private/production keys;
- live service-account files;
- live `.env` files;
- PATs;
- real provider/user tokens;
- raw production DB dumps;
- credentials hidden in examples/URLs/test snapshots.

Secret scanning/push protection complements this rule; it does not make secret commits acceptable.

## 21. Configuration change discipline

Material config-contract changes ship like code:

- reviewed settings-model/manifest change;
- example/documentation update;
- validation/default tests;
- rollout/backward-compatibility consideration;
- old/new artifact overlap handling where relevant.

Renaming a required variable without overlap/migration planning can break immutable promotion just like an API incompatibility.

## 22. Validation once scaffold exists

At minimum test:

- required settings missing → fail;
- invalid environment → fail;
- dangerous PROD combinations → fail;
- secret representations remain redacted;
- LOCAL example/config remains safe;
- runtime and migrator identity contracts are distinct when DB roles exist.

## 23. Deferred provider choices

Deferred until their implementation boundary:

```text
runtime secret-manager vendor
cloud workload-identity implementation
Auth/signing key provider
CI-to-R2 identity mechanism
CI-to-AWS recovery identity
frontend/mobile config/signing secret handling
```

The provider may vary; this contract does not.
