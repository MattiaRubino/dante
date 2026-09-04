# DANTE — Project Status

- **Status:** CURRENT INTEGRATION-CANDIDATE TRUTH
- **Last reconciled:** 2026-09-04
- **Protected `main`:** Recovery integrated at Alembic `20260830_09`
- **Integration candidate:** `integration/access-auth-main-20260904`
- **Current candidate Alembic head:** `20260904_17`
- **Current macro state:** **M5 CLOSED / COMBINED INTEGRATION QA ACTIVE**

## 1. Current state

```text
Product / North Star                       CURRENT
Domain / Logical / Physical                CLOSED
Engineering + Frontend + Backend CP1–CP6  CLOSED / ACCEPTED
PostgreSQL                                 18.6

Access M1–M5                               CLOSED / ACCEPTED
local password/passkey UAT                 PASS
real Windows Hello UAT                     PASS
real Google UAT                            PASS
real Apple registered-domain UAT           BOUNDED DEFERRED / NON-BLOCKING

Shared Email Platform                      CLOSED / ACCEPTED
real SES signup UAT                        PASS
real SES recovery UAT                      PASS
real reset-notification UAT                PASS

Protected-main Recovery                    MERGED INTO CANDIDATE
Combined Alembic                           20260904_17
Combined integration QA                    ACTIVE

M6 Native Mobile                           FUTURE / OPTIONAL
later Access/M7 maturity                   FUTURE
```

Apple is not reported as PASS. Real Apple external acceptance remains a future enablement prerequisite when its external account/domain prerequisites exist.

## 2. Combined database truth

```text
PostgreSQL          18.6
Alembic             20260904_17
tables              88
views                5
routines             16
triggers             76
physical indexes     172
foreign keys         89
CHECK constraints    270
```

Migration graph:

```text
20260826_08
├── 20260830_09 Recovery
└── 20260827_09
    → 20260827_10
    → 20260829_11
    → 20260830_12
    → 20260831_13
    → 20260903_14
    → 20260903_15
    → 20260904_16 Access/Auth + Email

20260830_09 + 20260904_16
            ↓
        20260904_17
```

`20260904_17` performs no schema mutation. It only joins the two accepted histories.

## 3. Frozen Access/Auth constitution

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal runtime-derived
provider identity = issuer + subject
provider email != Account/link authority
provider token/assertion != DANTE AuthSession
passwordless Account valid
PasskeyCredential != Account
WebAuthn user_handle = opaque Account binding
method != factor != assurance
reauthentication != signin
```

## 4. Shared Email Platform

The Email Platform is reusable DANTE infrastructure. Access/Auth owns its own message meaning/templates; the platform owns durable delivery lifecycle, encryption, claim/lease, retry/ambiguity policy, providers, feedback, suppression and observability.

Accepted real SES evidence remains in `development/email-platform-acceptance-2026-09-03.md`. Production sender-domain/DNS/reputation/workload-identity deployment remains a separate gate.

## 5. Current gate

No M6/M7 feature expansion belongs in this candidate. Required acceptance is:

```text
single Alembic head 20260904_17
fresh DB → head
Access head 20260904_16 → merged head
Recovery head 20260830_09 → merged head
head → base → head
Alembic drift check
Dictionary ↔ SQLAlchemy ↔ live PostgreSQL
Recovery regression
Access/Auth regression
Email Platform regression
runtime ACL / least privilege
backend full regression
frontend/generated-client/build regression
Recovery whole-rehearsal recheck on the enriched baseline
```

## 6. Integration safety

```text
no rebase/history rewrite
no force push
no direct protected-main write
applied migrations immutable
no blind Alembic flattening
no schema claim without Dictionary/mapping/migration/PG/test parity
no PASS without executed evidence
```

## 7. Authority

1. executable code / migrations / tests / real PostgreSQL
2. Product / Domain / Logical / Physical / constitutions / ADRs
3. current subsystem references
4. this status + roadmap
5. historical evidence / Git chronology
6. conversation memory
