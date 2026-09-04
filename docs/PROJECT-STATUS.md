# DANTE — Project Status

- **Status:** CURRENT INTEGRATION-CANDIDATE TRUTH / READY FOR PROTECTED-MAIN MERGE
- **Last reconciled:** 2026-09-04
- **Protected `main`:** Recovery integrated at Alembic `20260830_09`
- **Integration candidate:** `integration/access-auth-main-20260904`
- **Accepted candidate proof HEAD:** `81639c61478b476c995652d0060dde8f53aef089`
- **Current candidate Alembic head:** `20260904_17`
- **Current macro state:** **M5 CLOSED / COMBINED INTEGRATION QA PASS**

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

Shared Email Platform                      CLOSED / ACCEPTED / OWNERSHIP VERIFIED
real SES signup UAT                        PASS
real SES recovery UAT                      PASS
real reset-notification UAT                PASS

Protected-main Recovery                    MERGED INTO CANDIDATE
Combined Alembic                           20260904_17
Combined candidate CI                      PASS
CP07 whole LOCAL recovery rehearsal        PASS
Integration candidate                      READY FOR PROTECTED-MAIN MERGE

M6 Native Mobile                           FUTURE / OPTIONAL
later Access/M7 maturity                   FUTURE
```

Apple is not reported as PASS. Real Apple external acceptance remains a future enablement prerequisite when its external account/domain prerequisites exist.

CP07 proves only the documented LOCAL PostgreSQL operator recovery scope. Remote backup provider activation and production/cloud recovery are not claimed.

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

## 3. Combined acceptance evidence

Exact accepted candidate:

```text
branch             integration/access-auth-main-20260904
upstream           origin/integration/access-auth-main-20260904
proof HEAD         81639c61478b476c995652d0060dde8f53aef089
```

GitHub Actions on that exact HEAD:

```text
Dependency Review  PASS
Frontend CI        PASS
Backend Quality    PASS
Backend PostgreSQL PASS
Backend CI Gate    PASS
```

The 2026-09-04 CP07 whole LOCAL operator rehearsal on that exact HEAD additionally proved:

```text
Alembic head                                  20260904_17
topology                                      88|5|16|76|172|89|270|0|0|0
A before target / B after target              PASS
old protected X physical resurrection         PROVEN
suppression-ledger reconciliation             PASS
payload reinsertion after retirement          REJECTED
DATABASE LOCAL REOPEN                         PASS
derived/object gates                          NOT_ACTIVATED / NO FALSE PASS
remote provider                               TBD / NOT ACTIVATED
production/cloud recovery                     NOT CLAIMED
```

Durable evidence: `workstreams/access-auth-integration-acceptance-2026-09-04.md`.

## 4. Frozen Access/Auth constitution

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

## 5. Shared Email Platform

The Email Platform is reusable DANTE infrastructure. Access/Auth owns its own message meaning/templates; the platform owns durable delivery lifecycle, encryption, claim/lease, retry/ambiguity policy, providers, feedback, suppression and observability.

The shared-ownership refactor and forward vocabulary migration are accepted on the combined candidate through the current static/unit/PostgreSQL regression and exact-HEAD CI. Accepted real SES evidence remains in `development/email-platform-acceptance-2026-09-03.md`. Production sender-domain/DNS/reputation/workload-identity deployment remains a separate gate.

## 6. Current gate

Feature expansion remains frozen. The candidate acceptance gate is **PASS** for its declared integration scope.

Remaining work before branch retirement is procedural integration only:

```text
reconcile current documentation to measured candidate truth
verify protected main has not advanced unexpectedly
review exact documentation-only acceptance commit
require fresh CI on that commit
mark PR #52 ready
merge through protected-main PR flow
verify the resulting main commit/tree and CI
reconcile current docs from candidate wording to protected-main wording
only then retire the integration branch
```

If `main` changes before merge, stop and re-integrate the new main delta forward; rerun every affected acceptance gate, including CP07 when the database/recovery contract is affected.

## 7. Integration safety

```text
no rebase/history rewrite
no force push
no direct protected-main write
applied migrations immutable
no blind Alembic flattening
no schema claim without Dictionary/mapping/migration/PG/test parity
no PASS without executed evidence
no production/cloud recovery claim from LOCAL CP07
```

## 8. Authority

1. executable code / migrations / tests / real PostgreSQL
2. Product / Domain / Logical / Physical / constitutions / ADRs
3. current subsystem references
4. this status + roadmap
5. durable evidence / Git chronology
6. conversation memory
