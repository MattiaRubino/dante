# Configuration and Secrets v0

- Status: **APPROVED BACKEND BLOCK — Engineering Foundation remains open**
- Scope: backend application configuration, runtime identity, credentials, secret handling and environment isolation
- Frontend/web/mobile configuration: **DEFERRED to the dedicated frontend workstream/branch**

## 1. Decision

DANTE backend configuration is explicit, typed, environment-scoped and validated before the process accepts work.

Secrets are external security material. They are not source code, ordinary configuration defaults, repository examples, image build arguments or product/domain state.

The target hierarchy is:

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

This contract is provider-neutral. AWS, Azure, GCP or another hosting provider may implement it differently without changing DANTE's architectural rule.

## 2. Configuration classes

DANTE distinguishes four classes.

```text
NON-SECRET DEPLOYMENT CONFIG
runtime behavior that is safe to disclose, e.g. environment identity,
ports, non-sensitive endpoints, bounded timeouts and telemetry mode

SECRET
credential, private key, token or other material whose disclosure grants
capability or access

BUILD / RELEASE IDENTITY
Git SHA, build ID, release/version and artifact identity

DOMAIN / BUSINESS CONFIGURATION
product rules or governed state that belongs to canonical application data
rather than infrastructure configuration
```

Domain/business semantics must not drift into environment variables merely because they are configurable.

## 3. Environment identity

Promotion environments remain:

```text
LOCAL
DEV
UAT
PROD
```

Automated tests may use an explicit test execution context, but `TEST` is not a fifth promotion environment.

Every backend process knows its environment and release identity explicitly. The implementation uses a DANTE-specific namespace and exposes validated equivalents of at least:

```text
DANTE_ENV
DANTE_RELEASE_SHA
DANTE_BUILD_ID
```

`DANTE_ENV` is a closed enum, not an arbitrary string.

## 4. Typed backend configuration

Backend configuration uses **pydantic-settings** as the typed bootstrap boundary.

Rules:

- one composed settings object or a small set of clearly owned settings groups is constructed during bootstrap;
- parsing and validation occur before requests/jobs are accepted;
- required missing values fail fast;
- malformed values fail fast;
- cross-field/environment safety rules fail fast;
- validated settings are treated as immutable runtime state;
- components receive configuration explicitly instead of reading process globals throughout the codebase;
- scattered `if env == "prod"` business logic is forbidden.

Safe grouping may include, for example:

```text
AppSettings
DatabaseSettings
ObservabilitySettings
SecuritySettings
ProviderSettings
```

The final class/module split belongs to implementation, not this foundation.

## 5. Safe defaults

A default is allowed only when an incorrect default cannot silently weaken security, privacy, durability or environment isolation.

Critical values normally have no permissive PROD fallback, including:

- environment identity;
- database identity/credential source;
- token/signing/encryption material;
- trusted-host/origin policy where security-relevant;
- production provider identity/credential source;
- destructive maintenance switches.

A PROD process must not start merely because a dangerous value fell back to a development default.

## 6. Cross-field safety invariants

Configuration validation must be able to reject dangerous combinations, not only malformed individual values.

Examples:

```text
PROD + debug enabled                         -> REJECT
PROD + LOCAL/synthetic database credential   -> REJECT
PROD + DEV/UAT resource identity              -> REJECT
DEV/UAT + PROD credential/resource binding    -> REJECT
unknown DANTE_ENV                             -> REJECT
```

Provider-specific resource identifiers are validated once those providers exist.

## 7. LOCAL configuration

LOCAL may use an ignored dotenv file for developer convenience.

Backend target shape:

```text
apps/backend/.env.example    COMMITTED, safe contract/example only
apps/backend/.env.local      IGNORED, local developer values only
```

`.env.example` contains variable names, safe dummy values where useful and required/optional guidance. It never contains live DEV/UAT/PROD credentials.

LOCAL credentials are synthetic and restricted to LOCAL resources.

## 8. Remote configuration

DEV/UAT/PROD do not depend on manually maintained repository `.env` files or ad-hoc files edited over SSH.

Non-secret configuration is supplied through the deployment/IaC/platform configuration mechanism selected for the environment.

Secrets use the provider-native secret-management path selected with the hosting platform.

The exact vendor is deferred until the compute/provider decision; the required capabilities are fixed here.

## 9. Secret-manager requirements

A production-capable secret manager must provide, as applicable:

- encryption in transit and at rest under provider guarantees;
- fine-grained IAM/RBAC;
- environment isolation;
- workload/service identity integration;
- secret versioning;
- controlled rotation and revocation;
- auditability of secret access and administration;
- safe recovery/disable/delete lifecycle;
- automation interfaces suitable for IaC/deployment;
- regional/data-residency controls where DANTE requirements demand them.

A checked-in encrypted file is not a substitute for a runtime secret-management system.

## 10. Secret delivery — strongest available mechanism

For remote environments, the preferred order is:

```text
1. eliminate the secret through workload/managed identity
2. runtime retrieves the required secret from the provider secret manager
   using its workload identity
3. provider-native secret projection/injection when direct retrieval is not
   practical and the mechanism has an acceptable exposure model
4. environment-variable injection only as a bounded fallback when the runtime
   or provider requires it
```

Secrets are **not** hard-coded through Docker `ENV`/`ARG`, baked into OCI images or committed to deployment manifests.

Environment variables remain the normal mechanism for non-sensitive configuration.

## 11. Workload identity and the bootstrap-secret rule

DANTE prefers identity over stored credentials.

Where supported, a runtime authenticates to its cloud/provider through a managed/workload identity rather than through a long-lived service-account key.

The system must avoid the circular anti-pattern:

```text
store a permanent secret
        ↓
only so the application can authenticate
        ↓
to the secret manager
```

Provider-native managed identity, workload identity federation or equivalent short-lived identity is preferred.

## 12. GitHub deployment identity

Future GitHub Actions deployments use **OIDC/federated identity** with the target provider where secure practical support exists.

Target flow:

```text
GitHub Actions job
        ↓ OIDC claim
provider trust policy
        ↓
short-lived deployment credential
        ↓
DEV / UAT / PROD deployment
```

Trust policy must be scoped to the expected repository/ref/workflow/environment claims rather than accepting any token from GitHub.

Long-lived cloud deployment keys in GitHub are a fallback only when federation is genuinely unavailable.

## 13. GitHub is not the canonical runtime-secret store

GitHub Environments are the deployment control plane for `dev`, `uat` and `prod` when remote deployment activates.

GitHub environment secrets may be used for bounded bootstrap/integration cases that cannot use federation, but the normal DANTE model is:

```text
GitHub
source + workflow + deployment authorization

provider secret manager
runtime secret authority
```

Production runtime credentials are not duplicated into GitHub merely because GitHub can store secrets.

## 14. Environment isolation

DEV, UAT and PROD have separate secret and identity boundaries.

```text
DEV identity  -> DEV resources/secrets only
UAT identity  -> UAT resources/secrets only
PROD identity -> PROD resources/secrets only
```

A DEV/UAT credential must not authenticate to PROD by design.

When the hosting provider is selected, this rule maps onto its native account/subscription/project/security boundary and secret-store model.

## 15. Separate consumers, separate privileges

Secrets/identities are scoped to the narrowest consumer and action practical.

Database roles already approved by the persistence block remain logically separated:

```text
owner
migration/deployment
runtime application
replication/sync when PowerSync activates
backup/recovery when recovery activates
```

Normal backend runtime does not receive schema-owner or migration privileges.

The same principle applies to object storage, provider integrations, observability and future release/signing operations.

## 16. Minimize human access

Humans should not routinely read production secret values merely because they administer the repository.

Target rules:

- machine workloads consume machine secrets;
- administrative access is least-privilege and auditable;
- privileged human access uses MFA/JIT/approval controls where the selected provider supports them and the risk justifies them;
- break-glass access, if required later, is explicit, tightly restricted, logged and followed by credential review/rotation.

This remains proportionate to DANTE's actual team size while preserving the enterprise boundary.

## 17. Rotation, revocation and versioning

Every long-lived secret introduced must have:

- owner;
- purpose and scope;
- consumers;
- creation mechanism;
- rotation mechanism;
- revocation mechanism;
- incident replacement procedure;
- audit source.

Automatic rotation is preferred where technically safe.

Where a secret manager supports versioned secrets, deployments should use deliberate version behavior rather than relying blindly on an unbounded `latest` reference when rollback/reproducibility requires a known version.

High-consequence rotation must be tested before production dependence becomes material.

When a platform can replace a static credential with a short-lived/dynamic credential without unacceptable operational cost, prefer the short-lived form.

## 18. Zero-downtime rotation readiness

Consumers of rotatable credentials must not force an outage merely because a secret changes.

Depending on the provider/resource, the implementation may use:

- dual/alternating credentials;
- overlapping validity windows;
- connection refresh/retry;
- staged rollout;
- workload identity instead of a rotatable static secret.

The concrete mechanism is selected per secret class.

## 19. Audit and monitoring

Secret lifecycle events and accesses are auditable where the provider supports it.

Operational evidence should be able to answer, within provider capability:

```text
who/what accessed the secret?
when?
from which workload/environment?
who changed permissions?
when was it rotated/disabled/revoked?
```

Suspicious or high-consequence secret-management events become security-monitoring inputs when remote operations activate.

## 20. Logging and redaction

Secrets must never be logged by default.

Forbidden examples include:

```text
full environment dump
full settings object containing secrets
Authorization headers
cookies/session tokens
OAuth refresh tokens
raw provider credentials
raw database DSN containing a password
private signing/encryption keys
```

Configuration/credential wrappers expose redacted representations where diagnostics could otherwise leak values.

Operational logs use bounded metadata such as environment, provider/resource class, release identity, correlation ID and safe error category.

## 21. CI logs and artifacts

CI/CD must not echo secrets or persist them into artifacts.

When workflows exist:

- PR validation succeeds without production secrets;
- untrusted/fork/Dependabot code does not receive privileged deployment material;
- shell tracing is disabled around sensitive operations;
- generated/uploaded artifacts are checked against accidental secret inclusion where risk exists;
- production secrets are not exposed merely to run ordinary tests.

## 22. Repository policy

Git must never contain:

- production/private keys;
- real service-account credential files;
- live `.env` files;
- personal access tokens;
- user/provider OAuth tokens;
- credentials embedded in URLs/examples;
- copied production database dumps;
- secrets hidden in fixtures, snapshots, build args or generated files.

Secret scanning and push protection complement this rule; they do not make committing secrets acceptable.

## 23. Provider/user tokens are application data, not deployment secrets

OAuth/provider tokens tied to a DANTE user or Integration Hub account have a separate governed application-data lifecycle.

They are not generic environment secrets.

Their future persistence must preserve ownership, provider/canonical separation, encryption/protection, refresh/revocation semantics, retention/deletion and no leakage to logs/traces/errors.

Concrete schema and Auth implementation remain out of scope here.

## 24. Encryption/signing material

Concrete Auth/signing/encryption key design remains deferred to its implementation boundary.

Foundation requirements are already fixed:

- key bytes are never committed;
- environments use separate key material;
- rotation/versioning must be possible;
- historical readability/verification must survive rotation when the use case requires it;
- persisted key identifiers/versions may identify material without persisting secret bytes;
- provider KMS/HSM use is selected only when the actual key/use-case boundary exists.

## 25. Configuration precedence

Precedence remains small and deterministic.

For backend non-secret configuration:

```text
safe code default
        ↓ overridden by
LOCAL ignored dotenv value, LOCAL only
        ↓ overridden by
explicit process/deployment configuration
```

Remote secret resolution is deliberately separate from generic configuration precedence.

Avoid deep YAML/TOML/env inheritance trees where the winning value is difficult to prove.

## 26. Configuration changes ship like code

A material configuration-contract change requires:

- reviewed settings-model change;
- safe example/documentation update;
- validation/default tests;
- environment rollout consideration;
- compatibility period where old/new artifacts can overlap.

Renaming a required configuration key without an overlap/migration plan is treated as a release-breaking change.

## 27. Validation obligations

Once backend scaffold exists, automated tests cover at minimum:

- required configuration fails when absent;
- invalid environment enum rejects;
- dangerous PROD cross-field combinations reject;
- settings remain bounded/immutable after bootstrap;
- secret-bearing types/representations redact values;
- safe defaults do not weaken PROD behavior;
- LOCAL dotenv behavior does not become a remote deployment dependency.

Provider integration tests are added when a real secret manager/workload identity exists.

## 28. Deferred concrete choices

The following are intentionally deferred until the corresponding implementation boundary:

```text
cloud / compute provider
provider secret-manager product
provider managed/workload identity mechanism
exact remote configuration service/IaC mechanism
Auth/signing/encryption provider
CI-to-R2 federation mechanism
CI-to-AWS recovery identity
```

The provider may vary; the security contract above does not.

## 29. Primary-source security basis

This approved contract was rechecked on 2026-08-19 against current primary/authoritative guidance:

- OWASP Secrets Management Cheat Sheet:
  `https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html`
- GitHub deployment hardening / OIDC:
  `https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments`
- AWS Secrets Manager best practices:
  `https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html`
- Google Cloud Secret Manager best practices:
  `https://cloud.google.com/secret-manager/docs/best-practices`
- Azure secrets / managed identity / Key Vault guidance:
  `https://learn.microsoft.com/azure/security/fundamentals/secrets-best-practices`
  `https://learn.microsoft.com/azure/key-vault/general/secure-key-vault`

The common enterprise pattern across these sources is reflected here: minimize stored secrets, prefer workload identity, isolate environments, apply least privilege, use a dedicated secret manager, automate rotation/revocation where possible, audit access and prevent secrets from entering source/logs/artifacts.
