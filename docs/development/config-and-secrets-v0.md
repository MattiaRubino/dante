# Configuration and Secrets v0

- Status: **Engineering Foundation branch baseline — pending closure**
- Scope: application configuration, credentials, secret handling and environment identity

## 1. Core rule

Configuration is explicit, typed, environment-scoped and validated before an application accepts work.

Secrets are external runtime inputs. They are never source code, defaults, generated client data or documentation examples.

```text
CONFIGURATION
controls deployed behavior within accepted architecture

SECRET
credential/key/token/private material that grants capability or access

PUBLIC CLIENT CONFIG
anything delivered to browser/mobile; never considered secret
```

## 2. Environment identity

Every deployed/runtime process knows its environment explicitly.

Canonical generic values:

```text
local
dev
uat
prod
test
```

`test` is an execution context for automated tests, not a promotion environment.

The backend configuration surface uses a DANTE-specific namespace/prefix so host environments cannot accidentally collide with generic variables.

At minimum deployed server processes expose validated equivalents of:

```text
DANTE_ENV
DANTE_RELEASE_SHA
DANTE_BUILD_ID
```

A public application version/release identifier may also be exposed for diagnostics.

## 3. Backend configuration

Backend configuration uses `pydantic-settings` as the typed boundary.

Rules:

- one composed settings object or small clearly-owned settings groups are built at process bootstrap;
- environment variables are parsed/validated exactly once at startup where practical;
- invalid/missing required values fail fast before serving requests/jobs;
- settings are treated as immutable after bootstrap;
- configuration is injected into components rather than imported from process globals throughout the codebase;
- business rules are not encoded as scattered `if env == "prod"` checks.

Environment-specific behavior belongs behind explicit configuration/capability boundaries.

## 4. TypeScript configuration

Web/mobile configuration has separate server-only and client-visible boundaries.

### Web

Next.js code must make the server/browser distinction explicit.

- server-only values may include secrets and are never imported into browser-safe modules;
- values embedded/exposed to browser JavaScript are public;
- browser-visible configuration is runtime/schema validated where practical;
- client config must not become a second authority for security/governance.

### Mobile

Every value packaged into a mobile binary/update is considered extractable/public.

```text
API endpoint
public provider app ID
feature exposure identifier
= may be client config

API secret
service-account key
private signing secret
backend provider token
= MUST NOT be mobile config
```

Signing credentials are build/release secrets, not application runtime data.

## 5. Local environment files

Each application may provide its own committed example file when scaffolded:

```text
apps/api/.env.example
apps/web/.env.example
apps/mobile/.env.example
```

Examples contain:

- variable names;
- safe dummy/non-secret values where useful;
- comments explaining required vs optional behavior.

They do not contain real DEV/UAT/PROD values.

Local developer secret/value files are ignored, e.g. ecosystem-appropriate `.env.local`/`.env.*.local` files.

The exact ignore pattern is defined during scaffold to avoid accidentally ignoring committed example/config contracts.

## 6. Configuration precedence

Keep precedence small and predictable.

Recommended server baseline:

```text
code default for safe non-environment-specific value
        ↓ overridden by
local ignored env file (LOCAL only, when used)
        ↓ overridden by
process/environment injected value
```

Deployed DEV/UAT/PROD do not depend on repository `.env` files.

Secrets from a provider secret manager/CI environment are injected into the process/platform environment or mounted through an explicitly supported secret interface.

Avoid multi-layer YAML/TOML/env inheritance trees that make it difficult to know which value won.

## 7. Safe defaults

A default is allowed only when being wrong cannot silently weaken security, privacy, durability or environment isolation.

Examples of values that should generally **not** have a permissive PROD fallback:

- database URL/credential;
- token/signing secret;
- allowed trusted origin/host policy;
- encryption key;
- production provider endpoint/credential;
- environment identifier;
- destructive maintenance switches.

Missing critical configuration causes startup/preflight failure.

## 8. Secret classes

Future secrets should be classified by owner and consequence, for example:

```text
DATABASE
PostgreSQL application/migration/admin credentials

IDENTITY / AUTH
signing/verifier/provider credentials

OBJECT
R2 access credentials

RECOVERY
AWS backup credentials

OBSERVABILITY
Grafana/telemetry exporter credentials

INTEGRATION
provider-specific OAuth/API credentials

CI / RELEASE
artifact registry, signing, store/release credentials
```

This classification does not authorize or create those credentials now.

## 9. Least privilege

Different workloads receive different credentials where privilege differs materially.

Examples once implemented:

- normal API runtime does not receive database superuser capability;
- migration job may receive DDL capability that normal runtime lacks;
- read-only operational tooling uses read-only credentials where practical;
- backup credentials cannot become normal application credentials;
- DEV/UAT credentials cannot access PROD state;
- CI PR jobs do not receive PROD deployment credentials.

Credentials are scoped to the narrowest resource/action/environment practical.

## 10. CI/cloud identity

GitHub Actions uses OIDC/federated identity with external providers where the provider supports a secure practical integration.

Benefits adopted as policy:

- avoid long-lived static cloud keys in GitHub secrets;
- trust can bind repository/ref/environment/workflow claims;
- short-lived credentials are issued only for the job that needs them.

Where a provider cannot use GitHub OIDC safely, environment-scoped GitHub secrets or provider-native secret integration may be used as the bounded fallback.

Fallback static credentials require:

- least privilege;
- explicit environment ownership;
- rotation procedure;
- no exposure to PR jobs;
- revocation path.

## 11. GitHub Environments

Deployment credentials/variables are scoped through GitHub Environments when workflows are created:

```text
dev
uat
prod
```

A workflow job must reference the intended environment before it can access that environment's protected secrets/variables.

Environment protections are not substitutes for repository branch protection; source integration and deployment authorization remain separate gates.

## 12. Secret managers

The exact runtime secret manager depends on the compute/deployment provider, which is not yet selected.

Engineering Foundation therefore fixes the interface requirements, not a fake provider choice:

- environment isolation;
- encryption at rest/in transit under provider guarantees;
- auditable access where supported;
- least-privilege workload identity;
- rotation/update without committing source changes;
- version/revocation behavior suitable for the secret class.

Production does not use a checked-in encrypted secret file merely because plaintext is hidden.

## 13. Database credentials

At implementation time, separate logical roles should be created where privilege separation is useful:

```text
runtime application role
migration/deployment role
administrative/operator role
replication/sync role when PowerSync activates
backup/recovery role when recovery activates
```

Exact PostgreSQL grants/roles are part of implementation, not this foundation document.

Connection strings are secrets if they embed credentials.

## 14. Provider OAuth/user tokens

Integration Hub credentials/tokens tied to a user/provider account are application data with their own privacy/security lifecycle; they are not generic deployment secrets.

Their eventual persistence must preserve:

- account/principal ownership;
- provider/canonical separation;
- token encryption/protection requirements;
- revocation/refresh semantics;
- retention/deletion rules;
- no leakage into logs/traces/errors.

Engineering Foundation does not decide their concrete schema.

## 15. Logging/redaction

Secrets must never be logged by default.

Configuration objects implement redacted representations where tooling could otherwise print sensitive values.

Forbidden logging patterns:

```text
entire environment dump
full settings object with secrets
Authorization headers
cookies/session tokens
OAuth refresh tokens
raw provider credentials
raw database DSN with password
private signing/encryption keys
```

Operational diagnostics log bounded metadata such as provider name, environment, resource class, correlation ID and safe error category instead.

## 16. CI logs/artifacts

Workflows must not echo secrets or place them into durable artifacts.

Rules when CI exists:

- shell tracing that prints commands/values is disabled around sensitive operations;
- generated config artifacts are checked for secret content before upload where risk exists;
- test fixtures use synthetic credentials;
- PR jobs are designed to succeed without production secrets;
- Dependabot/untrusted PR execution does not receive normal repository secrets.

## 17. Client-side public config

A browser/mobile config variable naming convention must make public exposure explicit.

Framework prefixes such as `NEXT_PUBLIC_*` or `EXPO_PUBLIC_*`, if used, are treated as disclosure labels, not protection mechanisms.

A review should be able to answer:

```text
Can this value be read by any user who receives the client?
YES -> public config is acceptable if intended
NO  -> it cannot be placed in the client bundle
```

## 18. Runtime public configuration for web

Where practical, public environment-specific web values should be delivered at runtime through a controlled configuration endpoint/document so the same immutable web/server artifact can move between environments.

If Next.js/hosting implementation makes a build-time public value materially simpler/safer, environment-specific builds may be accepted as an explicit artifact distinction rather than hiding the difference.

## 19. Feature flags and operational switches

No feature-flag provider is selected by Engineering Foundation.

If feature flags activate later:

- they are typed/owned;
- flags do not bypass Authority/AuthZ/governance;
- a flag cannot redefine canonical semantics silently;
- stale flags have cleanup ownership;
- security-critical access is not protected only by client-side flags.

Emergency/maintenance switches with destructive consequence require explicit authorization and auditability.

## 20. Key/encryption material

Application encryption/signing key design belongs to the security/Auth implementation boundary.

Foundation rules:

- keys are not committed;
- separate environments use separate key material;
- rotation/versioning must be possible without losing historical readability where the use case requires it;
- key IDs/versions may be persisted when needed, secret key bytes are not;
- client-local encryption keys use platform secure storage appropriate to the mobile offline design when that PSV activates.

## 21. Secret rotation

Every long-lived secret introduced must eventually have:

- owner;
- scope;
- creation mechanism;
- rotation mechanism;
- revocation mechanism;
- consumers;
- incident replacement procedure.

Rotation is tested for high-consequence credentials before production dependence becomes material.

## 22. Repository policy

Repository files must never contain:

- production/private keys;
- real service-account files;
- live `.env` files;
- personal access tokens;
- real user/provider tokens;
- copied production database dumps;
- credentials embedded in URLs/examples;
- secrets hidden in test snapshots/fixtures.

Secret-scanning/push-protection controls complement review; they do not make committing secrets acceptable.

## 23. Configuration change discipline

A material config contract change ships like code:

- reviewed manifest/settings model change;
- example/documentation update;
- tests for validation/default behavior;
- environment rollout consideration;
- backward-compatible rollout when old/new artifact overlap is possible.

Renaming a required variable without a migration/overlap plan can break a build-once promotion just as surely as an API break.

## 24. Validation

Once scaffold exists, automated tests should cover at minimum:

- required settings fail when absent;
- invalid environment enum rejects;
- secret fields are redacted from representations/logging helpers;
- client public config schema rejects malformed values;
- server-only config cannot be imported into browser bundle through architecture/build checks where feasible;
- environment-specific dangerous defaults are absent.

## 25. Deferred provider choices

The following remain intentionally deferred until their actual implementation boundary:

```text
runtime secret-manager vendor
Auth/signing key provider
CI-to-R2 federation mechanism
CI-to-AWS recovery identity
mobile signing credential store
app-store secret handling
```

The provider choice may vary; the contract above does not.
