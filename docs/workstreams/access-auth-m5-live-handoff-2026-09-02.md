# DANTE — Access/Auth M5 Live Handoff — 2026-09-02

- **Class:** BRANCH-OPERATIONAL HANDOFF / TEMPORARY
- **Status:** CURRENT CONTINUATION AID FOR ACTIVE `feature/access-auth`
- **Must not merge to protected `main` unchanged:** YES — consolidate/remove under `../development/documentation-lifecycle-policy.md`
- **Repo:** `MattiaRubino/dante`
- **Branch:** `feature/access-auth`
- **Intended worktree:** `/home/mattia/projects/dante`
- **Remote branch HEAD immediately before this handoff commit:** `2e5889541045d47ebae4b5df5017bfa0e30596b0`
- **Reviewed product checkpoint:** `ab2716abe40de658d99d1908ba31c5d5744e3c57`
- **Real-SMTP UAT tooling checkpoint:** `9c0587af5891249d8a6e6b6a5d6e3af6934c6943`
- **Accepted Alembic head:** `20260831_13`

> This file is a save-game for the active branch, not a new authority that overrides current specs. Verify current remote HEAD before every write. Current durable truth starts at `../PROJECT-STATUS.md`, `../ROADMAP.md`, `access-auth.md`, `access-auth-m5-review-2026-09-02.md`, `../architecture/access-auth-email-delivery.md` and `../decisions/ADR-012-email-delivery-platform.md`.

## 1. Mission / quality bar

Continue the existing DANTE Access/Auth vertical. Do not restart it, reinterpret the Account/AuthSession model, or create parallel architecture.

Required level:

```text
large-product / enterprise-grade engineering
security-correct before convenient
PostgreSQL-authoritative
provider-neutral boundaries
high maintainability
high performance without speculative machinery
explicit failure semantics
real evidence, not checkbox PASS
professional UX comparable in maturity to major consumer/work apps
```

Methodological rules:

```text
SELECTED != IMPLEMENTED != DIRECT PASS
NO PASS WITHOUT EXECUTED EVIDENCE
DO NOT REOPEN ACCEPTED WORK WITHOUT DIRECT DEFECT EVIDENCE
VERSION-SENSITIVE CLAIMS REQUIRE CURRENT EVIDENCE
CURRENT DOCS > OLD HANDOFF > CHAT MEMORY
NEW CHAT != NEW BRANCH
```

During manual UAT, guide one action at a time. Do not dump long checklists on the user when a single click/command is enough.

## 2. Branch / repository safety

```text
repo:      MattiaRubino/dante
branch:    feature/access-auth
worktree:  /home/mattia/projects/dante
```

Do not touch without explicit topology authorization:

```text
main
feature/home-react
feature/access-frontend
/home/mattia/projects/dante-frontend
```

Forbidden shortcuts:

```text
merge to main
rebase
history rewrite
force push
protected-main direct write
unrelated branch/worktree changes
```

Before every repository write:

```text
1. state branch
2. state exact PRE-SCOPE remote SHA
3. state exact update/create paths
4. state purpose + explicit out-of-scope
5. race-check remote HEAD immediately before write
6. write only bounded paths
7. post-scope compare
8. do not call PASS until required evidence runs
```

A prior documentation reconciliation race occurred on 2026-09-02: remote moved while docs were being reviewed. The correct response was to stop, inspect the intervening commits, then continue above them. Preserve this behavior.

## 3. Permanent Auth constitution

Do not reopen these without concrete architecture/security evidence:

```text
Person != Account != Principal != Actor
AuthSession != DANTE Session
EmailIdentity != Account
PasswordCredential optional
Principal runtime-derived, never persisted
multiple AuthSessions normal
provider identity = issuer + subject
provider email != Account/link authority
provider auth != provider-data authorization
provider token/assertion != DANTE AuthSession
passwordless Account valid
PasskeyCredential != Account
WebAuthn user_handle = opaque Account binding
method != factor != assurance
reauthentication != signin
frontend/provider/browser completion != backend-authoritative success
```

Web posture:

```text
opaque server-authoritative session
Secure + HttpOnly host-only cookie
no browser JWT/localStorage/sessionStorage Auth authority
session-bound synchronizer CSRF
Origin + Fetch Metadata same-origin protection
recent-auth before sensitive authenticator mutations
backend remains final Auth success authority
```

## 4. Closed / accepted implementation state

```text
Product / North Star                       CURRENT
Domain / Logical / Physical                CLOSED
Engineering + Frontend + Backend CP1–CP6  CLOSED / ACCEPTED
Access pre-backend Web materialization     CLOSED / ACCEPTED

M1 Visual / UX Freeze                      CLOSED / ACCEPTED
M2 Auth Architecture Freeze                CLOSED / ACCEPTED
M3 Email/Password + AuthSession            CLOSED / ACCEPTED
M4 Signup/Verify/Recovery/Reset/Reauth     CLOSED / ACCEPTED

M5.1 architecture/external authority       COMPLETE
M5.2 persistence/API design                COMPLETE
M5-A persistence                           COMPLETE / POSTGRESQL PROVEN
M5-B provider/crypto/WebAuthn infra         COMPLETE / ENGINEERING PASS
M5-C Google backend                        COMPLETE / ENGINEERING PASS
M5-D Apple backend/grants/notifications    COMPLETE / ENGINEERING PASS
GROUP 1 lifecycle/passwordless             COMPLETE / ENGINEERING PASS
GROUP 2 passkeys                           COMPLETE / ENGINEERING PASS
GROUP 3 FastAPI/OpenAPI/generated client   COMPLETE / ENGINEERING PASS
GROUP 4 Access Web engineering QA          PASS
GROUP 4 local password/passkey UAT          PASS
GROUP 4 real Google UAT                    PASS

whole M5                                   ACTIVE / EXTERNAL ACCEPTANCE OPEN
```

Do not repeat giant M1–M5 implementation work unless a new defect demonstrates a need.

## 5. Final product-code automated evidence

Reviewed product checkpoint:

`ab2716abe40de658d99d1908ba31c5d5744e3c57`

Observed canonical gate:

```text
Prettier                                     PASS
TypeScript                                   PASS
ESLint                                       PASS
architecture/dependency-cruiser              PASS
Web unit/component tests                     68 / 68 PASS
Auth Playwright HTTPS                        60 / 60 PASS
Chromium                                     PASS through canonical suite
Firefox                                      PASS through canonical suite
WebKit                                       PASS through canonical suite
production Vite build                        PASS inside harness
```

This is the current final product-code gate after the WebAuthn regression fix.

Later `9c0587...` changed only local-UAT SMTP tooling and therefore requires its own targeted qualification, not another fake claim that the full product code changed.

## 6. Manual password/session/passkey UAT — LIVE PASS

Live user-driven UAT on disposable PostgreSQL proved:

```text
password signin                              PASS
logout                                       PASS
session authority across navigation          PASS
hard reload remains authenticated            PASS
password reauth                              PASS
rotated session bearer remains authoritative PASS

real Windows Hello passkey registration      PASS
native navigator.credentials.create path     PASS
backend FIDO2 verification                   PASS
PasskeyCredential persistence                PASS
passkey inventory                            PASS
passkey reauthentication                     PASS
anonymous/discoverable passkey signin        PASS
passkey rename + reload persistence           PASS

remove Password while Passkey remains        PASS
Account remains passkey-only                 PASS
attempt remove final Passkey                  BLOCKED CORRECTLY
backend code auth.authenticator_removal_blocked PASS
Italian anti-lockout explanation             PASS
re-establish Password                        PASS
fresh logout + password signin               PASS

direct PostgreSQL inspection                PASS
```

Passkey label observed during UAT:

`PC Mattia - Windows`

## 7. UAT defects found and closed

Manual UAT found real defects that earlier automation had not exposed.

### AuthSession rotation/read race

An in-flight `/session` read could overwrite freshly rotated authenticated state after a sensitive mutation.

Fix direction:

```text
mutation rotates/creates/revokes AuthSession authority
→ application boundary cancels exact in-flight session read
→ commits authoritative new state
```

Regression retained; live reauth → navigation → reload proved PASS.

### Cross-chunk remote-error identity

Lazy/chunk boundaries could undermine `instanceof`-style remote failure classification. Boundary was hardened and targeted tests retained.

### WebAuthn canonical envelope mismatch

Backend correctly returned:

```text
ceremony.options.publicKey
```

Browser adapter incorrectly read flattened options. Adapter/tests were corrected. Real Windows Hello then appeared and completed successfully.

Relevant product checkpoint after fix:

`ab2716abe40de658d99d1908ba31c5d5744e3c57`

Do not reopen these closed defects unless a regression is observed.

## 8. Real Google UAT — LIVE PASS

Google Cloud / Google Auth Platform was configured with a Web OAuth client for:

```text
https://localhost:4173
```

The actual DANTE flow used the official Google Identity Services rendered control.

Live observed chain:

```text
DANTE /google/begin
→ ExternalAuthTransaction + nonce
→ official Google account interaction
→ real Google ID token
→ DANTE backend JWK/signature/issuer/audience/nonce verification
→ issuer + subject identity resolution
→ Google third-party mailbox classification
→ DANTE mailbox verification challenge
→ Account creation
→ canonical AuthSession
→ authenticated onboarding
```

The selected Google account used a non-Gmail third-party mailbox. DANTE correctly did **not** treat Google authentication as automatic proof that Google controls that external mailbox. It required direct mailbox proof before Account establishment.

The mailbox proof in this run used loopback SMTP capture, therefore:

```text
real Google authentication               PASS
DANTE mailbox verification logic         PASS
real Internet email delivery             NOT PROVED
```

### Direct DB proof after Google UAT

Observed:

```text
Account                         1 / active
EmailIdentity                   verified
ExternalIdentity.provider_code  google
ExternalIdentity.issuer         https://accounts.google.com
ExternalIdentity.subject        present
ExternalIdentity.status         active
PasswordCredential              0
AuthSession                     ACTIVE
```

This proves a Google-created Account is genuinely passwordless and converges on the same canonical Account/AuthSession model.

### Google configuration incident

First attempt failed with:

`401 invalid_client`

Cause: one manually transcribed character in the public Google OAuth Client ID was wrong.

Exact-copying the Client ID resolved the issue without DANTE code change.

Classification:

```text
UAT/external configuration transcription error
!= DANTE code defect
!= missing client secret
!= OAuth architecture defect
```

The current GIS ID-token flow uses the public Web Client ID; the browser does not need the OAuth client secret.

## 9. Database truth

Current branch-local Access/Auth DB:

```text
PostgreSQL          18.6
Alembic             20260831_13
83 tables
5 views
15 routines
75 triggers
156 physical indexes
85 foreign keys
233 CHECK constraints
103 standalone Dictionary entries
```

`20260831_13` is the bounded authenticator-lifecycle ACL follow-up.

Email transactional-outbox/delivery-state tables do **not** exist yet. Do not add them informally; exact materialization must obey ADR-010 and Dictionary ↔ SQLAlchemy ↔ Alembic ↔ live PostgreSQL consistency.

## 10. Email architecture decision — CURRENT

On 2026-09-02 the outbound transactional/security email architecture was reviewed and the direction accepted.

Authority:

- `../decisions/ADR-012-email-delivery-platform.md`
- `../architecture/access-auth-email-delivery.md`

North Star:

```text
DANTE owns the email lifecycle.
A specialist provider owns last-mile Internet delivery.
```

Primary production delivery-adapter target:

```text
Amazon SES API v2
preferred initial region target: eu-south-1 Europe/Milan
```

This is a **selected target**, not a production PASS.

Target architecture:

```text
Auth / DANTE Feature
        │
        ├── canonical security/business state
        └── durable Email Intent
                 │
                 ▼
          PostgreSQL COMMIT
                 │
                 ▼
      Transactional Email Outbox
                 │
                 ▼
      bounded worker/orchestrator
                 │
                 ├── template + locale
                 ├── dedup/idempotency
                 ├── claim/lease
                 ├── retry/ambiguity policy
                 └── provider adapter
                           │
                           ▼
                     Amazon SES API v2
                           │
                           ▼
                    recipient network
                           │
                           ▼
          delivery/bounce/complaint events
                           │
                           ▼
             DANTE normalized event ingestion
                           │
                           ▼
       delivery state / suppression / metrics
```

`EmailDeliveryPort` remains the application-facing provider-neutral boundary.

## 11. Existing email implementation — keep, evolve, do not mislabel

Current executable email slice already has useful properties:

```text
EmailDeliveryPort                         IMPLEMENTED
typed security email commands            IMPLEMENTED
SmtpEmailDispatcher                      IMPLEMENTED
bounded asyncio.Queue                    IMPLEMENTED
fixed workers                            IMPLEMENTED
no blind SMTP retry                      IMPLEMENTED
bounded shutdown drain                   IMPLEMENTED
SMTP TLS/auth configuration              IMPLEMENTED
loopback SMTP capture                    IMPLEMENTED / CI
opt-in real SMTP local UAT               IMPLEMENTED at 9c0587af...
```

This is a good first slice and UAT adapter.

It is **not** the final enterprise Email Platform because:

```text
in-memory queue can lose committed intent on process death
SMTP accepted/send success != inbox delivery
no durable provider message state
no bounce/complaint event ingestion
no canonical suppression lifecycle
no durable retry/ambiguity state
no production sender DNS/reputation setup
```

Do not throw the implementation away; evolve behind the accepted boundary.

## 12. Email security invariants

```text
provider accepted != delivered
network timeout != definitely not sent
no blind retry after ambiguous send outcome
stable DANTE intent reference before external I/O
OTP/recovery proof never in normal logs
OTP/recovery proof never in metrics labels
OTP/recovery proof never in traces
no indefinite plaintext sensitive outbox payload
Auth/security open tracking OFF
Auth/security click tracking OFF
Auth/security link rewriting OFF
Auth/security marketing content FORBIDDEN
SPF + DKIM + DMARC required before production sender acceptance
Auth/security / product notifications / future marketing separable
```

Sensitive durable payload design is still open. It must have short TTL, minimal readable scope and explicit cleanup/erasure after provider acceptance or expiry. Envelope encryption or equivalent is a likely candidate, but the exact design must be threat-modeled and proved before implementation.

## 13. Retry / ambiguity doctrine

Do not reduce external email side effects to “retry on exception”.

```text
definitive pre-send/provider rejection
→ bounded retry/failover may be allowed

provider accepted / provider message ID returned
→ record acceptance; do not send another copy because feedback is pending

network timeout / ambiguous outcome
→ NO blind immediate retry
→ preserve uncertainty
→ reconcile through provider evidence where possible
→ otherwise use explicit purpose-specific policy
```

Provider failover later must be deterministic and duplicate-safe. Never send the same recovery intent through provider B just because SES outcome is unknown.

## 14. Feedback / suppression doctrine

Production platform must normalize at least:

```text
accepted/sent
delivered
delivery_delayed
bounced
complained
rejected
```

Hard bounce and complaint must be able to create a DANTE-owned delivery restriction/suppression.

This does not mean `EmailIdentity` becomes provider state or is deleted automatically.

Provider suppression infrastructure may help, but it does not replace canonical DANTE reasoning where product/security behavior depends on delivery eligibility.

## 15. Sender / reputation doctrine

Production Auth/security mail must use a DANTE-owned authenticated sender domain/subdomain.

Required baseline:

```text
SPF
DKIM
DMARC
```

Do not send production recovery/signup from a personal Gmail/Hotmail mailbox.

Traffic classes must be separable:

```text
Auth/security
ordinary DANTE product notifications
future marketing/bulk
```

Do not automatically buy dedicated IP infrastructure at low volume; activate scale machinery only when real volume/deliverability evidence requires it.

## 16. Why SES / external benchmark

The provider target is chosen for architectural fit, not a temporary free promotion.

Public directional evidence reviewed:

```text
Netflix
→ retired in-house email delivery in favor of Amazon SES
→ separates transactional/marketing reputation pools
→ consumes provider feedback

Fanatics
→ owns an internal email platform
→ uses SES as scalable delivery engine
→ preserves traffic segmentation/application control
```

This supports:

```text
DANTE platform ownership
+
external specialist delivery engine
```

Do not claim Notion/Linear or another product uses a specific provider without direct current public evidence.

## 17. Important current pricing correction

A previous research discussion used the older SES-specific `3,000 message charges/month free for 12 months` claim.

For **new AWS customers after July 21, 2026**, that SES-specific offer is no longer the current model. Current new-account economics use newer AWS pricing-plan/general Free Tier credit mechanics.

Therefore:

```text
DO NOT use 3,000/month as current DANTE SES economics
DO re-check current AWS pricing/credits during qualification/deployment
DO keep provider decision based on architecture/operations, not promotion
```

## 18. Exact next gate — DO NOT CODE YET

The next chat/work session should **research and qualify the provider/operational boundary first**.

Use current official sources and answer in depth:

```text
1. AWS account creation / billing / Free Tier pricing-plan posture in 2026
2. SES sandbox behavior and path to production access
3. eu-south-1 Milan exact SES API availability
4. current quotas / sending limits / increase process
5. verified identities and domain/subdomain setup
6. Easy DKIM/BYODKIM implications
7. SPF / MAIL FROM / DMARC alignment
8. Auth/security sender naming strategy
9. IAM least-privilege policy
10. workload identity / role strategy for likely deployment
11. AWS SDK / SES API v2 integration in Python 3.14/FastAPI environment
12. configuration sets / tags / stream segmentation
13. event destinations
14. SNS vs EventBridge for provider feedback ingestion
15. authenticity/idempotency/versioning of provider events
16. SES suppression/global suppression implications
17. provider retention/privacy/subprocessors/data residency
18. current SES cost at realistic DANTE volumes
19. current Postmark/Resend/Brevo/SendGrid alternatives only as comparison/reopen evidence
20. operational failure semantics and provider outages
21. exact manual UAT path without secrets in repo
22. exact threat model for transactional outbox + OTP/recovery payload protection
23. provider accepted/delivered/bounced/complained state model
24. failure-injection and production acceptance matrix
```

Do not implement the outbox, AWS SDK adapter, new migrations or event endpoints until this research produces a reviewed exact implementation scope.

## 19. After provider qualification

Then freeze the exact Email Platform implementation gate:

```text
logical model
physical persistence
Dictionary delta
SQLAlchemy/Alembic delta
ACL delta
worker claim/lease lifecycle
sensitive payload encryption/TTL/cleanup
SES API adapter
provider message ID state
provider event ingestion
suppression/restriction mapping
observability
failure tests
real inbox UAT
```

Every database change follows ADR-010/CP6 discipline:

```text
human reference
≈ Dictionary
≈ SQLAlchemy
≈ Alembic
≈ live PostgreSQL
≈ direct tests
```

No speculative Kafka/Redis/Celery/Temporal/extra database merely because email is asynchronous. PostgreSQL outbox is the accepted Class-A baseline.

## 20. Real Internet UAT still required

After implementation/provider setup, user wants real proof, not mocks:

```text
normal email/password signup
→ real verification mail delivered to actual inbox
→ OTP used successfully
→ Account/AuthSession DB verification

Google third-party mailbox enrollment
→ real DANTE verification mail delivered
→ provider Account completed
→ ExternalIdentity DB verification

password recovery
→ real recovery mail delivered
→ link consumed
→ URL secret scrubbed
→ password changed
→ all existing sessions revoked
→ fresh signin
→ password-change notification delivered
→ direct DB/provider-event verification
```

Do not substitute loopback capture for this final acceptance.

## 21. Apple status

Apple backend/grant/notification architecture is implemented/engineering-pass.

Real registered-domain UAT is deferred/open because the user currently has no Apple account available; later a family member may test.

Must preserve both relay domains:

```text
privaterelay.appleid.com
private.icloud.com
```

Future sender/domain setup for DANTE email must be compatible with Apple Private Email Relay registration requirements.

No fake Apple PASS.

## 22. M7 after M5 external acceptance

M7 planned maturity work:

```text
session/device inventory
revoke one session
revoke all other sessions
log out everywhere
new-login/security-event alerts
“this wasn't me” response
production observability/alerting
final accessibility/release/legal review
final authenticated Home handoff
bounded decomposition of large Security UI
```

Current authenticated Access branch landing is the accepted Access/onboarding return, not the final Home integration. Do not call missing Home navigation an M5 Auth defect.

The new Email Platform should later carry new-login/security-event messages instead of creating a second notification subsystem.

## 23. Current maintainability note

`access-security-page.tsx` is functionally accepted but has accumulated substantial orchestration/rendering responsibility.

Before expanding security UX deeply, split bounded password/provider/passkey/reauth sections while preserving current application/platform boundaries.

This is M7 maintainability hardening, not reason to reopen Auth architecture.

## 24. Current deprecation / contradiction results

2026-09-02 review found:

```text
Google GIS                         current
use_fedcm_for_button               current
use_fedcm_for_prompt               deprecated / DANTE does NOT use it
Google issuer+sub authority        current
WebAuthn/FIDO2                     current
residentKey API naming             still API-compatible; “discoverable credential” preferred prose
Apple relay dual-domain semantics  current

workstreams README M2/M3 state     stale → reconciled
technical-decisions old DB/Auth    stale → reconciled
old SES 3,000/month free claim     stale for new customers → corrected
```

Do not blindly “modernize” accepted code when the actual API remains current. Deprecation claims need official/version-current evidence.

## 25. Documentation read order for continuation

Read fully before changing implementation:

```text
README.md
PROJECT-STATUS.md
ROADMAP.md
development/agent-operating-manual.md
workstreams/access-auth.md
workstreams/access-auth-m5-review-2026-09-02.md
architecture/access-auth-email-delivery.md
decisions/ADR-012-email-delivery-platform.md
architecture/access-auth-architecture.md
architecture/access-auth-security-contract.md
architecture/access-auth-m5-contract.md
architecture/access-auth-m5-persistence-api-contract.md
decisions/ADR-010-postgresql-persistence-constitution.md
database/README.md
database/access-auth.md
frontend/access.md
```

Then verify live branch HEAD and inspect relevant implementation/tests before proposing writes.

## 26. Interaction style / user expectation

The user expects a high-level reviewer/engineer, not a yes-man.

Required behavior:

```text
be direct
explain real architectural tradeoffs
challenge weak choices with evidence
do not manufacture issues for activity
do not keep reopening already accepted work
do not use fake enterprise complexity
compare against large mature apps where public evidence is meaningful
separate public product behavior from unprovable internal architecture
prefer official sources for changing technical/provider claims
keep implementation clean enough that later changes are localized
performance/security/maintainability all matter
```

When UAT is interactive, one action at a time and interpret screenshots/output for the user rather than making them debug blindly.

## 27. Current safe first action in next chat

```text
NO CODE WRITE.
NO DB MIGRATION.
NO SES ACCOUNT CONFIGURATION YET UNLESS RESEARCH MAKES THE exact next step clear.
```

First:

1. verify current remote/local branch state;
2. consume the current docs above;
3. run deep up-to-date SES/email-provider operational research;
4. produce a qualification decision matrix + proposed exact implementation architecture;
5. identify any real contradictions with ADR-012;
6. only then request/execute the bounded implementation write gate.

If research confirms ADR-012, proceed to exact materialization design. If it exposes a material blocker, reopen only the smallest affected provider/architecture decision with evidence.

## 28. Handoff cleanup obligation

This file is temporary branch-operational material.

Before `feature/access-auth` is integrated into protected `main`:

```text
current truth → durable current docs/ADRs
important evidence → review/validation record
useful history → at most one consolidated branch history if justified
this live handoff → REMOVE
old 2026-08-29 live handoffs → REMOVE or archive only if knowledge-coverage justifies it
```

Do not merge a stack of live handoffs into `main`.
