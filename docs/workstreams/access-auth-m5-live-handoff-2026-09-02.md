# DANTE — Access/Auth M5 Live Handoff — 2026-09-02

- **Class:** HISTORICAL BRANCH-OPERATIONAL HANDOFF
- **Status:** SUPERSEDED / DO NOT USE AS CURRENT PROGRESS AUTHORITY
- **Original date:** 2026-09-02
- **Superseded:** 2026-09-03 after Email Platform materialization and real SES UAT
- **Branch:** `feature/access-auth`
- **Repository:** `MattiaRubino/dante`

This file originally served as a temporary save-game while M5 external email work was still open.

Its phase-time statements such as:

```text
Email Platform not materialized
Alembic head 20260831_13
83-table branch catalog
production email provider qualification open
real Internet email UAT open
process-owned SMTP queue as current email implementation
preferred SES Milan target
```

are **historical evidence only** and are no longer current repository truth.

Do not use this file to continue the branch.

## Current continuation authority

Start instead at:

```text
docs/PROJECT-STATUS.md
docs/ROADMAP.md
docs/workstreams/access-auth.md
docs/architecture/README.md
docs/architecture/email-platform.md
docs/architecture/access-auth-email-delivery.md
docs/decisions/ADR-012-email-delivery-platform.md
docs/database/README.md
docs/database/access-auth.md
docs/development/email-platform-local-uat.md
docs/development/email-platform-acceptance-2026-09-03.md
```

Then verify the live `feature/access-auth` remote HEAD before any write.

## Superseding Email Platform state

As of the 2026-09-03 reconciliation:

```text
shared Email Platform architecture          ACCEPTED
Email Platform persistence                  MATERIALIZED
Email Platform Alembic head                 20260903_15
Amazon SES API v2 adapter                   ACCEPTED
Email automated/PostgreSQL acceptance       PASS
real DANTE signup → SES → mailbox           PASS
real DANTE recovery → SES → mailbox         PASS
real reset-notification → SES → mailbox     PASS
post-reset no-auto-login                    PASS
prior AuthSession revocation                PASS
provider MessageId + secret wipe DB proof   PASS
Email Platform engineering work             CLOSED
```

The exact same consumed recovery URL was not manually reopened a second time in the final live run; current acceptance evidence records that explicit non-claim instead of manufacturing a PASS.

Production sender-domain/DKIM/SPF/DMARC, workload identity, SES production posture and live cloud feedback ingress remain separate deployment gates. They do not make the shared Email Platform engineering work open again.

## Current database truth

```text
PostgreSQL          18.6
Alembic             20260903_15
87 tables
5 views
15 routines
75 triggers
170 physical indexes
88 foreign keys
267 CHECK constraints
```

## Permanent branch safety

Historical status changed; branch safety did not.

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not write protected `main`, rebase, force-push or touch unrelated branches/worktrees without explicit authorization.

`SELECTED != IMPLEMENTED != AUTOMATED PASS != REAL UAT != PRODUCTION DEPLOYED` remains binding.
