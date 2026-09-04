# DANTE — Project Status

- **Status:** CURRENT PROTECTED-MAIN TRUTH
- **Last reconciled:** 2026-09-04
- **Access/Auth + Email + Recovery integration merge:** `5f76ec54ad78542f137e8730e904f805d9e59e56` (PR #52)
- **Recovery↔Email reopen hardening merge:** `c67a18c24a6cf22b003ffd2c14243af53fec5077` (PR #55)
- **Current Alembic head:** `20260904_17`
- **Current macro state:** **ACCESS/AUTH M1–M5 + SHARED EMAIL + RECOVERY CLOSED / INTEGRATED**
- **LOCAL Recovery gates:** **CP07 DATABASE-LOCAL PASS / CP08 APPLICATION+EMAIL REOPEN PASS**
- **Next bounded integration:** `feature/platform-observability`

## 1. Current state

```text
Product / North Star                       CURRENT
Domain / Logical / Physical                CLOSED
Engineering + Frontend + Backend CP1–CP6  CLOSED / ACCEPTED
PostgreSQL                                 18.6

Access M1–M5                               CLOSED / INTEGRATED
local password/passkey UAT                 PASS
real Windows Hello UAT                     PASS
real Google UAT                            PASS
real Apple registered-domain UAT           BOUNDED DEFERRED / NON-BLOCKING

Shared Email Platform                      CLOSED / INTEGRATED / OWNERSHIP VERIFIED
real SES signup UAT                        PASS
real SES recovery UAT                      PASS
real reset-notification UAT                PASS

PostgreSQL Recovery                        CLOSED / INTEGRATED
Alembic                                    20260904_17
protected-main DB                          88/5/16/76/172/89/270
database-local CP07                        PASS
Email/application reopen CP08              PASS
post-merge Backend CI                      PASS
post-merge Frontend CI                     PASS

feature/platform-observability             CLOSED / OPERATIONAL PASS / NEXT INTEGRATION
M6 Native Mobile                           FUTURE / OPTIONAL
later Access/M7 maturity                   FUTURE
```

Apple is not reported as PASS. Real Apple external acceptance remains a future enablement prerequisite when its external account/domain prerequisites exist.

The historical CP07 run proves the LOCAL PostgreSQL/database-local and MaterialState recovery scope it actually executed. It did not directly prove Email quarantine-before-worker-resume ordering. That historical limitation remains part of the evidence record; it was closed forward by PR #55 and the real CP08 rehearsal rather than by widening or rewriting CP07.

Remote backup provider activation and production/cloud recovery remain **NOT CLAIMED**.

## 2. Current database truth

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

`20260904_17` performs no schema mutation. It joins the two accepted forward histories without rewriting either one.

The current cross-representation database contract has passed real PostgreSQL reconciliation across Dictionary, SQLAlchemy mappings, Alembic and the live catalog. PR #55 changes Recovery/Email replay handling and acceptance tooling, not the database topology or Alembic head.

## 3. Integration and acceptance evidence

### PR #52 / historical CP07

Implementation proof HEAD:

```text
81639c61478b476c995652d0060dde8f53aef089
```

On that exact implementation state:

```text
Dependency Review   PASS
Frontend CI         PASS
Backend Quality     PASS
Backend PostgreSQL  PASS
Backend CI Gate     PASS
CP07 database-local PASS
```

The historical CP07 rehearsal directly proved:

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

CP07 did **not** directly execute Email `quarantine_after_restore()` before Email workers resume. That limitation is retained as historical evidence and must not be erased from the CP07 record.

PR #52 merged the final candidate into protected `main`:

```text
old main       fe87d3c8a71f0c56d9acf5e8acbcdb274b18f282
candidate      6cee5506d404d0684b0679aca54c03f0ca433c72
merge commit   5f76ec54ad78542f137e8730e904f805d9e59e56
merge tree     b610ece4fbfa0049749bb8454345a96a0385e6e5
```

The merge tree is identical to the accepted final candidate tree. Push CI on the exact merge commit passed Backend Quality, real PostgreSQL acceptance, Backend CI Gate, Frontend Quality, Web E2E, Mobile Bundle and Frontend CI Gate.

### PR #55 / CP08 forward closure

PR #55 hardened the recovery/reopen boundary without rewriting PR #52 or CP07. Exact proof head:

```text
1a5a7f1fbbdc1e5723d58fa90721a8693cce49e9
```

Mandatory CI on that head passed Dependency Review, Frontend CI, Backend Quality, Backend PostgreSQL (`154 passed, 250 deselected`) and Backend CI Gate.

The real disposable LOCAL CP08 rehearsal then proved:

```text
PITR to earlier sendable Email state                  PASS
restored pending / claimed / retryable_failure        PHYSICALLY RESURRECTED
Email workers during reconciliation                   STOPPED
provider I/O during reconciliation                    NOT EXERCISED
sendable restored intents → recovery_quarantined      PASS
restored in_progress attempt → ambiguous              PASS
claim / retry state cleared                           PASS
sensitive delivery material wiped                     PASS
second reconciliation                                 IDEMPOTENT / 0 FURTHER QUARANTINES
claimable Email work after reconciliation             0
APPLICATION / EMAIL REOPEN                            PASS
```

PR #55 merged at `c67a18c24a6cf22b003ffd2c14243af53fec5077`.

Durable pre-merge and CP07 evidence remains in `workstreams/access-auth-integration-acceptance-2026-09-04.md`. Consolidated Access branch chronology is archived at `archive/branches/2026-09-feature-access-auth.md` and is non-authoritative.

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

The Email Platform is reusable DANTE infrastructure. Access/Auth owns message meaning/templates; the platform owns durable delivery lifecycle, encryption, claim/lease, retry/ambiguity policy, providers, feedback, suppression and privacy-minimized observability.

The shared-ownership refactor and forward vocabulary migration are integrated on protected `main`. Accepted real SES evidence remains in `development/email-platform-acceptance-2026-09-03.md`. Production sender-domain/DNS/reputation/workload-identity deployment remains a separate gate.

Post-restore quarantine is now part of the accepted fail-closed recovery/reopen path. Restored sendable work is not authority to replay; CP08 directly proved quarantine, sensitive wipe, idempotent reconciliation and zero claimable Email work before application/Email reopen.

## 6. Current gate

Access/Auth + Email + Recovery is **CLOSED / INTEGRATED** for the accepted LOCAL and application-reopen scope. There is no active Access integration candidate and no outstanding Recovery↔Email CP08 remediation.

Current continuation:

```text
enriched protected main
→ integrate into feature/platform-observability
→ rerun Observability release/integration gates
→ protected-main Observability PR
→ future bounded workstreams from enriched main
```

## 7. Documentation/workstream closure

Access/Auth M1–M5 is no longer an active workstream authority after PR #52.

```text
live/session handoffs                     ABSENT
active Access workstream authority        RETIRED
obsolete execution-plan overlay          RETIRED
single consolidated branch history       archive/branches/2026-09-feature-access-auth.md
retained dated M5/integration records     EVIDENCE / VALIDATION ONLY
current Access/Email truth                subsystem references + executable repository
```

This follows `development/documentation-lifecycle-policy.md`: current truth stays current, at most one branch-history narrative is retained when useful, and historical evidence never overrides executable/current-reference truth.

## 8. Integration safety

```text
no rebase/history rewrite
no force push
no direct protected-main write
applied migrations immutable
no blind Alembic flattening
no schema claim without Dictionary/mapping/migration/PG/test parity
no PASS without executed evidence
no application reopen claim from database-only recovery evidence
no production/cloud recovery claim from LOCAL proof
```

## 9. Authority

1. executable code / migrations / tests / real PostgreSQL
2. Product / Domain / Logical / Physical / constitutions / ADRs
3. current subsystem references
4. this status + roadmap
5. durable evidence / Git chronology
6. conversation memory
