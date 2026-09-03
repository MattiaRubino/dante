# DANTE Email Platform — Local SES UAT Runbook

- **Status:** CURRENT / REPRODUCIBLE LOCAL UAT PROCEDURE
- **Last reconciled:** 2026-09-03
- **Platform authority:** `../architecture/email-platform.md`
- **Current first consumer:** Access/Auth
- **Target provider/region for current UAT:** Amazon SES API v2 / `eu-west-3` (Paris)

## 1. Purpose

This runbook makes the real DANTE → SES → mailbox acceptance flow reproducible from a fresh local/WSL environment.

It deliberately separates:

```text
repository code/config
local developer authentication
AWS account/provider state
real mailbox evidence
```

No AWS access key, secret key, session token or console credential belongs in the repository, `.env.example`, frontend configuration, screenshots or chat transcripts.

The DANTE runtime uses the standard AWS credential provider chain. For local UAT, the preferred path is browser-based `aws login` with temporary credentials rather than long-lived static access keys.

## 2. AWS CLI baseline

`aws login` requires AWS CLI v2 `>= 2.32.0`.

Current DANTE UAT baseline observed on 2026-09-03:

```text
AWS CLI tested version: 2.36.38
platform: Linux x86_64 / WSL2 / Ubuntu 24.x
user-local install root: ~/.local/share/aws-cli
user-local binary:       ~/.local/bin/aws
```

DANTE does not rely on Ubuntu `apt` or snap for this prerequisite because those channels may expose an older or independently updated version. The repository bootstrap uses the official AWS user-local installer and validates the minimum version.

Run from repository root:

```bash
bash tooling/bootstrap-aws-cli-local.sh
```

The bootstrap is idempotent for an existing valid install. It always addresses the binary by absolute user-local path, so the current shell does not depend on a refreshed `PATH`.

Verification:

```bash
$HOME/.local/bin/aws --version
```

If a developer chooses to expose the binary on `PATH`, this is shell configuration only and is not required by the runbook:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## 3. Local AWS login profile

Use a dedicated profile for DANTE UAT:

```text
dante-uat
```

Authenticate with temporary console-derived credentials:

```bash
$HOME/.local/bin/aws login \
  --profile dante-uat \
  --region eu-west-3
```

If WSL/browser callback handling is unavailable, use the AWS-supported remote flow instead:

```bash
$HOME/.local/bin/aws login \
  --remote \
  --profile dante-uat \
  --region eu-west-3
```

The IAM principal used for this login must be explicitly authorized for local-development sign-in and for the narrow SES UAT operations it needs. Do not use a root account as the normal DANTE development path.

The login session is temporary. Re-run `aws login` when it expires. Cached login credentials remain outside the repository under the normal AWS CLI user configuration/cache locations.

To end the session explicitly:

```bash
$HOME/.local/bin/aws logout --profile dante-uat
```

## 4. Provider preflight

Before starting the full DANTE stack, prove all three external prerequisites:

```text
1. named AWS profile resolves temporary credentials
2. selected principal can call AWS
3. SES sender identity is verified in eu-west-3
```

Set only non-secret UAT routing values:

```bash
export DANTE_UAT_AWS_PROFILE=dante-uat
export DANTE_UAT_SES_REGION=eu-west-3
export DANTE_UAT_SES_FROM_ADDRESS='<verified-sender-address>'
```

Then run from `apps/backend`:

```bash
uv run --locked python ../../tooling/email-platform-aws-preflight.py
```

Expected result:

```text
SES PREFLIGHT PASS
profile: dante-uat
region: eu-west-3
sender identity: <verified-sender-address>
verification: SUCCESS
```

This preflight performs no email send. It proves credential/profile resolution and SES sender identity state only.

## 5. Full DANTE SES UAT

The real UAT must exercise the DANTE durable Email Platform, not a direct SES console send and not the retired process-memory SMTP dispatcher.

Environment posture:

```bash
export AWS_PROFILE=dante-uat
export DANTE_UAT_ENABLE_SES=true
export DANTE_UAT_SEED_ACCOUNT=false
export DANTE_UAT_SES_REGION=eu-west-3
export DANTE_UAT_SES_FROM_ADDRESS='<verified-sender-address>'
export DANTE_UAT_ACCOUNT_EMAIL='<verified-recipient-address-if-SES-sandbox-requires-it>'
```

Optional configuration-set routing is explicit only when the target configuration set already exists:

```bash
export DANTE_UAT_SES_CONFIGURATION_SET='<configuration-set-name>'
```

Run the real local full-stack harness from `apps/backend`:

```bash
uv run --locked python ../../tooling/serve-access-auth-local-uat.py
```

The harness provisions disposable PostgreSQL, migrates to the repository Alembic head, starts the DANTE backend and Web surface, enables the durable Email Platform, selects `EmailTransport.SES`, and uses the standard AWS credential chain inherited from `AWS_PROFILE`.

## 6. Acceptance sequence

The current Access/Auth consumer acceptance is:

```text
fresh disposable database
→ signup through DANTE UI/API
→ EmailIntent committed with signup challenge
→ durable worker claims intent
→ SES API v2 accepts message
→ mailbox receives verification email
→ user verifies signup
→ request password recovery through DANTE
→ recovery EmailIntent committed
→ SES accepts recovery message
→ mailbox receives recovery email
→ complete reset
→ password-reset security notification emitted
```

Provider console test-send alone does not satisfy this gate.

## 7. Database evidence after real send

For accepted messages, DANTE must retain safe lifecycle evidence while sensitive payload material is wiped.

Expected high-level state:

```text
email_delivery_intent.dispatch_state_code = provider_accepted
email_delivery_attempt.result_code       = provider_accepted
provider_message_id                      = present
sensitive_key_id                         = NULL
sensitive_nonce                          = NULL
sensitive_ciphertext                     = NULL
sensitive_wiped_at                       = present
```

A provider acceptance is not equivalent to inbox delivery. Mailbox receipt is a separate UAT observation.

## 8. Security rules

Permanent rules for local provider UAT:

```text
no root credential as normal development path
no long-lived AWS key committed to repo
no AWS secret in DANTE config files
no credentials in frontend/public runtime
no OTP/recovery secret in logs
no blind send retry after ambiguous network outcome
use named profile dante-uat
use temporary aws login credentials where available
logout/expire local credentials after UAT
```

## 9. Reproducibility source map

Repository-owned pieces:

```text
tooling/bootstrap-aws-cli-local.sh
tooling/email-platform-aws-preflight.py
tooling/serve-access-auth-local-uat.py
docs/development/email-platform-local-uat.md
docs/architecture/email-platform.md
```

External state that cannot be encoded in Git:

```text
AWS account
IAM principal and permissions
SES region
verified sender identity
SES sandbox/production-account status
verified recipient when sandbox rules require it
mailbox delivery observation
```

These external dependencies must always be re-proven by the preflight/UAT instead of being assumed from old screenshots or a prior session.

## 10. Version-update policy

`2.36.38` is the current tested AWS CLI baseline, not a forever product dependency.

When changing the baseline:

```text
1. install/update via official AWS distribution
2. require version >= 2.32.0 while aws login remains the selected auth flow
3. rerun profile login + SES preflight
4. rerun real DANTE SES UAT if credential/provider behavior changed materially
5. update TESTED_VERSION in tooling/bootstrap-aws-cli-local.sh
6. update this runbook in the same reviewed change
```

Do not silently change the documented baseline without rerunning the relevant acceptance proof.
