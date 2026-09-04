# DANTE Internal Changelog

This changelog records significant project-state and architecture milestones. It is not a replacement for Git history and intentionally avoids duplicating every commit.

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