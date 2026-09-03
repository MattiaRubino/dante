# DANTE Email Platform — Real SES Acceptance Evidence — 2026-09-03

- **Status:** OBSERVED / ACCEPTED ENGINEERING + REAL-PROVIDER UAT EVIDENCE
- **Date:** 2026-09-03
- **Branch:** `feature/access-auth`
- **Platform authority:** `../architecture/email-platform.md`
- **Runbook:** `email-platform-local-uat.md`
- **Provider:** Amazon SES API v2
- **UAT region:** `eu-west-3` (Paris)
- **Current first consumer:** Access/Auth

## 1. Claim level

This document records evidence that was directly observed during the final Email Platform UAT. It is not a production-deployment acceptance record.

The accepted claim is:

```text
DANTE shared Email Platform
→ durable PostgreSQL intent/attempt lifecycle
→ Amazon SES API v2
→ real Internet mailbox
→ Access/Auth signup + password-recovery flows

ENGINEERING + REAL-PROVIDER UAT: PASS
```

The following remain separate production gates:

```text
DANTE-controlled sender domain/subdomain
DKIM / SPF / DMARC
production workload identity / IAM posture
SES production-account/reputation/quota posture
live provider-feedback cloud ingress wiring
operational traffic/reputation segmentation
privacy/legal/subprocessor deployment review where required
```

## 2. Repository / static evidence immediately before UAT

Observed on the branch during the closure sequence:

```text
uv lock --check                                  PASS
ruff format --check                              PASS
ruff check                                       PASS
targeted mypy src                                PASS
backend non-PostgreSQL regression                234 PASS
focused PostgreSQL Email/Auth acceptance         10 PASS
Email Platform unit/SES semantics                9 / 9 PASS
uv build                                         PASS
```

The AWS browser-login credential provider dependency is repository-locked through the backend UAT dependency set (`botocore[crt]` / resolved `awscrt==0.36.0` in the observed lock).

## 3. Reproducible AWS local-UAT posture

Observed prerequisite:

```text
AWS CLI              2.36.38
minimum for flow      >= 2.32.0
binary                ~/.local/bin/aws
profile               dante-uat
region                eu-west-3
```

Dedicated IAM topology used for UAT:

```text
IAM user              dante-uat
IAM group             dante-local-uat
access key             NONE

Group policies:
  SignInLocalDevelopmentAccess
  DanteUatSesVerifiedIdentity
```

The customer-managed SES policy is least-privilege for the verified UAT identity and grants only:

```text
ses:GetEmailIdentity
ses:SendEmail
```

The normal UAT principal was explicitly verified as a non-root IAM user. Root was used only during one-time IAM bootstrap and was logged out before the accepted UAT path.

## 4. SES preflight — observed PASS

The repository preflight resolved the named profile through Botocore and observed:

```text
SES PREFLIGHT PASS
profile: dante-uat
principal: arn:aws:iam::<account>:user/dante-uat
region: eu-west-3
verification: SUCCESS
```

The exact account number and personal sender address are intentionally not repeated in this durable document.

This preflight proved:

```text
named AWS profile usable
principal not root
SES region reachable
sender identity verified in selected region
```

It did not itself count as email delivery acceptance.

## 5. Defect found by real UAT and closed

The first real DANTE signup attempt correctly staged durable email work but did not reach SES because Botocore's browser-login credential refresh created its internal `signin` client without a region.

Observed runtime symptom:

```text
botocore.exceptions.NoRegionError: You must specify a region.
auth.email_delivery_result provider=ses outcome=ambiguous attempt=1
```

This was useful failure-model evidence: DANTE classified the uncertain provider attempt as `ambiguous` and did not blind-retry the security message.

Root cause:

```text
SES adapter supplied region to the SES client
but browser-login credential refresh needed session-level region context
```

Fix:

```text
SesEmailProvider now creates a boto3.Session(region_name=settings.ses_region)
and creates the SES v2 client from that session.
```

A focused unit test now proves region propagation to the session. Post-fix Email Platform unit/SES suite: `9 passed`.

## 6. Real signup UAT — PASS

Observed end-to-end sequence:

```text
fresh disposable PostgreSQL 18.6
→ DANTE Web signup
→ password-signup challenge created
→ signup-verification EmailIntent committed
→ durable worker claimed intent
→ Amazon SES API v2 accepted send
→ real mailbox received DANTE verification email
→ user entered received OTP in DANTE
→ verification succeeded
→ Account created
```

Observed safe runtime evidence:

```text
auth.email_delivery_result
provider=ses
outcome=provider_accepted
attempt=1
```

Mailbox receipt and successful OTP consumption were manually observed.

## 7. Real password-recovery UAT — PASS

Observed sequence:

```text
unauthenticated browser
→ Password dimenticata / recovery request
→ password-recovery EmailIntent committed
→ SES provider accepted attempt 1
→ real mailbox received recovery email
→ recovery URL opened DANTE reset surface
→ new password accepted
→ reset completed
```

The recovery email rendered both the security purpose and bounded expiry notice correctly. During this UAT the message landed in the mailbox spam/junk folder; this is not considered a functional failure because the current UAT sender is not yet the final DANTE domain with production DNS/reputation controls.

## 8. Post-reset security semantics — PASS

Directly observed:

```text
reset did NOT auto-login the user
existing prior AuthSession was revoked
refreshing the previously authenticated browser returned to signin
a password-reset security notification was emitted
real mailbox received the password-changed notification
```

Observed safe runtime evidence included two additional SES sends:

```text
password_recovery           → provider_accepted / attempt 1
password_reset_notification → provider_accepted / attempt 1
```

This proves the Access/Auth consumer integration for recovery/reset notification through the shared Email Platform.

## 9. Direct PostgreSQL evidence — PASS

Before the disposable UAT database was destroyed, direct PostgreSQL inspection observed exactly three accepted intents:

```text
signup_verification
password_recovery
password_reset_notification
```

For every row:

```text
dispatch_state_code = provider_accepted
attempt_count       = 1
accepted_at         = present
sensitive_key_id    = NULL
sensitive_nonce     = NULL
sensitive_ciphertext= NULL
sensitive_wiped_at  = present
```

Corresponding `email_delivery_attempt` rows observed:

```text
provider_code            = ses
attempt_number            = 1
result_code               = provider_accepted
provider_message_id       = present
error_code                = NULL
```

Therefore the final live UAT directly proved provider correlation plus terminal sensitive-payload wipe in canonical PostgreSQL state.

## 10. What was not claimed

The final live UAT did **not** manually re-open the exact same consumed recovery link a second time because the mailbox message had already been removed before that check was requested.

Therefore the precise accepted statement is:

```text
recovery link was received and successfully consumed once in live UAT
same-link replay rejection was NOT re-observed manually in this final live run
```

Do not rewrite this as a manually observed replay PASS.

Likewise, the final UAT did not prove:

```text
production-domain deliverability
DKIM/SPF/DMARC
SES provider feedback ingestion from live AWS cloud events
hard-bounce/complaint live Internet event delivery
production quota/reputation behavior
Apple Private Email Relay production-domain acceptance
```

Those are separate deployment/operations gates and do not reopen the shared Email Platform implementation.

## 11. Acceptance conclusion

As of 2026-09-03:

```text
Email Platform architecture                    ACCEPTED
PostgreSQL durable implementation              ACCEPTED
Access/Auth transactional integration          ACCEPTED
SES API v2 adapter                             ACCEPTED
retry/ambiguity semantics                      ACCEPTED
sensitive payload protection/wipe              ACCEPTED
automated PostgreSQL/unit acceptance           PASS
real DANTE → SES signup UAT                     PASS
real DANTE → SES password recovery UAT          PASS
real password-reset notification UAT           PASS
session revocation after reset                 PASS
local UAT reproducibility                      MATERIALIZED

EMAIL PLATFORM ENGINEERING WORKSTREAM           CLOSED
PRODUCTION EMAIL DEPLOYMENT                     SEPARATE / NOT YET ACCEPTED
```

Future DANTE consumers may reuse the platform under the extension contract in `../architecture/email-platform.md`; they do not reopen this Access/Auth acceptance unless they introduce new platform requirements.