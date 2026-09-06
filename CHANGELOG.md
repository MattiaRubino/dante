# DANTE Internal Changelog

This changelog records significant project-state and architecture milestones. It is not a replacement for Git history and intentionally avoids duplicating every commit.

## 2026-09-04

### Recovery↔Email post-restore hardening

- Closed the post-PR-#52 Email replay/reopen evidence gap forward through PR #55 without rewriting historical CP07 evidence or Alembic history.
- Hardened restored Email delivery state so `pending`, `claimed` and `retryable_failure` work is quarantined before outbound workers resume; restored `in_progress` attempts become `ambiguous` rather than authoritative active work.
- Mandatory CI on proof head `1a5a7f1fbbdc1e5723d58fa90721a8693cce49e9` passed Dependency Review, Frontend CI, Backend Quality, Backend PostgreSQL (`154 passed, 250 deselected`) and Backend CI Gate.
- Executed the real disposable LOCAL CP08 rehearsal: full backup → PITR to an earlier sendable Email state → physical resurrection → fail-closed Email quarantine → sensitive-material wipe → idempotent second reconciliation → `0` claimable Email work → `APPLICATION / EMAIL REOPEN = PASS`.
- Merged PR #55 into protected `main` at `c67a18c24a6cf22b003ffd2c14243af53fec5077`.
- PR #55 did not change the Alembic head or database topology; protected-main database truth remains PostgreSQL 18.6 / `20260904_17` / `88|5|16|76|172|89|270`.
- Remote backup-provider activation and production/cloud recovery remain unclaimed separate gates.

### Access/Auth + Email + Recovery protected-main integration

- Integrated protected-main Recovery into the isolated Access/Auth candidate through PR #51 without rebasing or rewriting either accepted history.
- Preserved Recovery `20260830_09` and Access/Auth + Email through `20260904_16` as sibling forward histories and joined them with no-DDL Alembic merge revision `20260904_17`.
- Accepted implementation proof HEAD `81639c61478b476c995652d0060dde8f53aef089` passed Dependency Review, Frontend CI, Backend Quality, real PostgreSQL acceptance and Backend CI Gate.
- Executed the CP07 whole LOCAL recovery rehearsal against the integrated `20260904_17 / 88|5|16|76|172|89|270` contract; deterministic PITR, anti-resurrection reconciliation, payload-reinsertion rejection and `DATABASE LOCAL REOPEN = PASS` were directly proved.
- Reconciled pre-merge current documentation and retained exact candidate/CP07 evidence in `docs/workstreams/access-auth-integration-acceptance-2026-09-04.md`.
- Merged PR #52 into protected `main` at `5f76ec54ad78542f137e8730e904f805d9e59e56`.
- Verified the PR #52 merge commit has exactly two parents — prior main `fe87d3c8a71f0c56d9acf5e8acbcdb274b18f282` and final candidate `6cee5506d404d0684b0679aca54c03f0ca433c72` — and that its tree `b610ece4fbfa0049749bb8454345a96a0385e6e5` is identical to the final candidate tree.
- Verified post-merge Backend Quality, real PostgreSQL acceptance, Backend CI Gate, Frontend Quality, Web E2E, Mobile Bundle and Frontend CI Gate all passed on the exact merge commit.
- Protected `main` now owns PostgreSQL 18.6 at Alembic `20260904_17` with 88 tables, 5 views, 16 routines, 76 triggers, 172 physical indexes, 89 foreign keys and 270 CHECK constraints.
- Access/Auth M1–M5, Recovery and the shared Email Platform are now closed/integrated on protected main. Apple real registered-domain UAT remains bounded deferred; production/cloud recovery and production Email sender/domain deployment remain unclaimed separate gates.
- The next bounded integration is `feature/platform-observability`, which must absorb the enriched protected main and rerun its own integration/release gates.

## 2026-09-02

### Access/Auth M5 engineering + live UAT reconciliation

- Completed the Group-4 Web engineering gate with canonical format/typecheck/lint/architecture checks, 68/68 Web unit/component tests and 60/60 Auth Playwright tests across the canonical Chromium/Firefox/WebKit HTTPS suite.
- Performed live password/session/security-management UAT.
- Performed real Windows Hello WebAuthn registration, reauthentication and passwordless signin UAT.
- Proved backend anti-lockout by removing the password while a passkey remained and verifying that removal of the final passkey was rejected with `auth.authenticator_removal_blocked`.
- Re-established the password and proved a fresh logout/login with the restored credential.
- Found and repaired an AuthSession rotation/read race, a cross-chunk remote-error classification problem and the browser WebAuthn `options.publicKey` envelope mismatch; retained regression tests.
- Configured and executed real Google Identity Services UAT. A third-party-mailbox Google Account correctly required direct DANTE mailbox proof before Account creation.
- Direct PostgreSQL inspection proved one active passwordless Google-created Account, verified EmailIdentity, active Google ExternalIdentity keyed by issuer+subject, zero PasswordCredential and an active canonical AuthSession.
- Added strictly opt-in real-SMTP configuration capability to the local UAT runner at `9c0587af...`; loopback SMTP remains the deterministic default. No production email provider has been selected.
- Reconciled current status/roadmap/workstream documentation and classified the older Group-4 live handoff as historical.
- External benchmark/deprecation review found the current Google GIS/FedCM button path, Google `sub` identity authority and WebAuthn/FIDO2 direction aligned with current provider/standards guidance. Main remaining product-security maturity gaps are session/device management, security-event alerts, real email delivery and Apple real UAT.

## 2026-08-23

### Frontend materialization and protected-main integration

- Closed frontend materialization FM-00..FM-07 at their stated direct-evidence scopes.
- Integrated the closed frontend materialization and bounded integration hardening into protected `main` through PR #28.
- Final PR head: `a6607ceabd35f874dc9e5f63fe8f57f71a92bf80`.
- Protected-main merge commit: `f1aacb0724088e0b4b086008a5219c2fba5ce0cf`.
- Verified the merge commit has exactly two parents: prior `main` `fd3bc8dd918cf6aadeff4572221af68612c3cb42` and PR head `a6607ceabd35f874dc9e5f63fe8f57f71a92bf80`.
- Verified the merged tree contains the exact accepted PR tree with no file delta between the PR head and merged `main` tree.
- PR exact-head Dependency Review, Backend CI and Frontend CI completed successfully, including `Backend CI Gate` and `Frontend CI Gate`.
- Frontend integration is now **CLOSED / INTEGRATED**. Future capabilities remain trigger-activated rather than placeholder-installed.

## 2026-08-18

### Product naming

- Established **DANTE** as the current product/app name.
- `LifeOS` remains the previous working/project name in historical evidence, Git history and existing technical/repository identifiers where preserving chronology or compatibility matters.
- The rename is naming-only: Product North Star, Domain Model, Logical Model and Physical Model semantics remain unchanged.

## 2026-08-10

### Project governance and handoff

- Established `main` as the single integrated source of truth.
- Defined DEV/UAT/PROD as deployment environments rather than permanent Git branches.
- Added repository-first handoff rules for humans and AI agents.
- Added global `PROJECT-STATUS`, roadmap and per-workstream operational handoffs.
- Consolidated detailed V1 product-definition documents into the canonical documentation path without deleting historical documentation/history.

### Data, AI and integrations architecture

- Accepted the hybrid personal data model: typed relational core + metadata/JSONB + graph-like personal relationship layer + provenance + audit/version history.
- Confirmed shared-schema/workspace ownership rather than per-user tables/databases.
- Defined progressive formalization for unpredictable life domains.
- Defined Assets, Capabilities and Requirements as reusable planning concepts.
- Defined AI semantic ingestion: AI proposes structured entities/relations/actions; DANTE validates and persists.
- Confirmed DANTE owns canonical memory/state while AI remains provider-replaceable.
- Defined Context Builder and provider-neutral Tool API / MCP-compatible direction.
- Defined Integration Hub, provenance, deduplication and raw-versus-derived data principles.

## Earlier foundation

Earlier product, architecture and UX decisions remain available in repository documentation and Git history. This file intentionally does not duplicate every prior decision.
