# DANTE — Project Status

- **Status:** CURRENT PROTECTED-MAIN TRUTH
- **Last reconciled:** 2026-09-04
- **Protected `main` integration merge:** `5f76ec54ad78542f137e8730e904f805d9e59e56`
- **Current Alembic head:** `20260904_17`
- **Current macro state:** **ACCESS/AUTH M1–M5 + SHARED EMAIL + RECOVERY CLOSED / INTEGRATED**
- **Post-merge remediation:** **EMAIL POST-RESTORE REOPEN GATE REQUIRED**
- **Next bounded integration after remediation:** `feature/platform-observability`

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
Email post-restore whole-flow gate         REMEDIATION REQUIRED
post-merge Backend CI                      PASS
post-merge Frontend CI                     PASS

feature/platform-observability             CLOSED / OPERATIONAL PASS / NEXT INTEGRATION AFTER REMEDIATION
M6 Native Mobile                           FUTURE / OPTIONAL
later Access/M7 maturity                   FUTURE
```

Apple is not reported as PASS. Real Apple external acceptance remains a future enablement prerequisite when its external account/domain prerequisites exist.

The historical CP07 run proves the LOCAL PostgreSQL/database-local and MaterialState recovery scope it actually executed. It does **not** directly prove that restored non-terminal EmailIntent rows are quarantined and wiped before Email workers resume. Application Email traffic reopen after PITR therefore remains blocked on a forward whole-flow remediation/proof. Remote backup provider activation and production/cloud recovery also remain not claimed.

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

The current cross-representation database contract has already passed real PostgreSQL reconciliation across Dictionary, SQLAlchemy mappings, Alembic and the live catalog. The outstanding post-merge finding is not a schema-convergence defect; it is restore/reopen orchestration and whole-flow evidence for Email.

## 3. Integration and acceptance evidence

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

It did **not** directly execute the following as part of that same restore/reopen sequence:

```text
restored non-terminal EmailIntent exists
→ Email workers remain stopped
→ quarantine_after_restore() executes
→ pending/claimed/retryable work becomes recovery_quarantined
→ sensitive delivery material is wiped
→ only then may Email workers/application traffic resume
```

The Email quarantine implementation and a focused real-PostgreSQL test exist, but focused component proof is not equivalent to a whole recovery ordering proof. This gap is being treated as a forward red remediation rather than rewriting the historical CP07 record.

PR #52 merged the final candidate into protected `main`:

```text
old main       fe87d3c8a71f0c56d9acf5e8acbcdb274b18f282
candidate      6cee5506d404d0684b0679aca54c03f0ca433c72
merge commit   5f76ec54ad78542f137e8730e904f805d9e59e56
merge tree     b610ece4fbfa0049749bb8454345a96a0385e6e5
```

The merge tree is identical to the accepted final candidate tree. Push CI on the exact merge commit passed Backend Quality, real PostgreSQL acceptance, Backend CI Gate, Frontend Quality, Web E2E, Mobile Bundle and Frontend CI Gate.

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

Post-restore quarantine is an existing platform capability, but the repository still needs one authoritative recovery/reopen ordering path and an end-to-end CP07 proof before application Email traffic reopen after PITR can be accepted.

## 6. Current gate

Access/Auth + Email + Recovery **schema/runtime integration is CLOSED / INTEGRATED**. There is no active Access integration candidate.

Before the next bounded platform integration is treated as the continuation baseline, close this post-merge safety item:

```text
restore target isolated
→ database/material anti-resurrection reconciliation
→ Email post-restore quarantine while workers are stopped
→ verify quarantine + sensitive wipe
→ whole-flow CP07 proof
→ application/Email reopen gate earned
```

Then continue:

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
