# DANTE — World Focus B2 Continuity / Resume Review

**Status:** ANALYSIS COMPLETE — IMPLEMENTATION AUTHORIZED / PRE-BACKEND  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`  
**Product authority:** `world-focus-product-contract.md`  
**Method:** `world-focus-delivery-methodology.md`

---

# 1. Vertical purpose

B2 is the first real World Focus content vertical after the shell/foundation and Orientation work.

It answers World Output Grammar O3:

> **What is in motion and where can I continue?**

The user-facing product goal is not to show “recent activity”. It is to reduce re-entry cost into meaningful unfinished continuity.

Internal compass:

```text
open World
-> understand what is genuinely still alive
-> recover the last meaningful checkpoint
-> know what is worth continuing
```

This vertical remains pre-backend. It must establish the complete frontend/application contract and a deterministic scenario adapter without pretending that a real API, database, provider or DANTE runtime already exists.

---

# 2. Reverse-engineering result

The central distinction is:

```text
RECENT != RESUMABLE
LAST VIEWED != LAST MEANINGFUL CHECKPOINT
OPEN != IN MOTION
UNFINISHED != IMPORTANT
AI-GUESSED RELEVANCE != CONTINUITY FACT
```

A continuity item is justified only when there is enough application evidence to represent a recognizable ongoing thread plus a meaningful checkpoint.

A continuity projection is a presentation/application projection. It is not a new Domain owner and does not create canonical World membership.

---

# 3. External product pattern review

The comparison is used for implementation/product lessons, not copied product semantics.

## Figma — Recents

Figma Recents makes recently opened files easy to revisit. Useful lesson: reduce retrieval/re-entry friction with a compact bounded list.

Rejected inference: a recently viewed file is not automatically the best thing to resume.

Reference: https://help.figma.com/hc/en-us/articles/14381406380183-Guide-to-the-file-browser

## Notion — Home / Recents / Continue where you left off

Notion exposes recently visited pages and can restore the tabs from the previous app session. Useful lesson: session restoration and semantic work continuity are distinct product concepts.

Rejected inference: browser/app tabs are not DANTE continuity truth.

References:
- https://www.notion.com/it/help/home-and-my-tasks
- https://www.notion.com/help/account-settings

## YouTube — resume position

YouTube persists an explicit progress position and resumes partially watched content from that checkpoint. Useful lesson: a resume affordance is strongest when the checkpoint is concrete and trustworthy.

Rejected inference: DANTE continuity is not always a single scalar progress position.

Reference: https://support.google.com/youtube/answer/7174115

## Linear — project status, milestones and updates

Linear combines explicit lifecycle/status, milestones and structured updates. Its project status is not automatically rewritten merely because underlying issues look complete. Useful lesson: continuity and lifecycle should use authoritative/explicit state rather than optimistic UI inference.

References:
- https://linear.app/docs/project-overview
- https://linear.app/docs/project-status
- https://linear.app/docs/initiative-and-project-updates

## TripIt — phase-dependent continuation

TripIt changes what is relevant around an upcoming/active trip and prioritizes the travel plan needed at the moment. Useful lesson: continuity depends on lifecycle/context; a planning checkpoint and an active-trip “next segment” are different questions.

References:
- https://help.tripit.com/en/support/solutions/articles/103000063427/
- https://help.tripit.com/en/support/solutions/articles/103000063288-widget-for-iphone-and-ipad

## Spotify — Recent activity

Spotify provides useful recent-listening history. Useful lesson: recency is valuable evidence/navigation, but by itself does not prove unfinished continuity.

Reference: https://support.spotify.com/it/article/recent-activity/

---

# 4. Product semantics

## 4.1 Continuity item

A first-open continuity item must have:

```text
recognizable thread identity
+ meaningful current/unfinished state
+ meaningful checkpoint
```

It may additionally have:

```text
bounded context label
continuity presentation state
freshness/provenance metadata
future continuation target/capability
```

The first implementation does **not** invent a continuation CTA when no real frontend destination/capability exists.

Therefore:

```text
“where can I continue?”
can be answered truthfully before
“execute the continuation action”
is implemented.
```

A future real continuation action can be attached only when an actual route/capability exists.

## 4.2 Meaningful checkpoint

A checkpoint is not `lastViewedAt`.

Possible future authoritative/application bases include:

```text
last meaningful Session
last material artifact/version
accepted Decision
confirmed plan step
explicit progress marker
provider-backed current state
bounded application state transition
```

B2 scenario fixtures represent checkpoint labels only; they do not claim backend provenance.

## 4.3 Continuity state

B2 needs only a small presentation vocabulary:

```text
active
paused
blocked
```

This is a projection vocabulary, not a replacement for Domain statuses.

Rules:

```text
active  -> continuation remains live
paused  -> continuity exists without fake urgency
blocked -> still continuity, but resolution may outrank resume later
```

`blocked` does not automatically become an Attention item in B2. O4 will own Attention semantics later.

## 4.4 Ordered output

The application/projection boundary owns ordering. React does not calculate a generic “relevance score”.

Potential future ranking inputs remain:

```text
explicit user importance
resumability value
material consequence
meaningful checkpoint recency
current intent
confidence/provenance quality
```

Pure recency and AI score alone are rejected.

---

# 5. Cross-World pressure test

## Music

Strong continuity case.

Examples:

```text
active release
unfinished song
last meaningful artifact/session
```

The surface may show several threads.

## Travel

Planning phase can have continuity:

```text
Japan 2027
planning checkpoint
```

During an active trip, “next flight/segment” belongs primarily to O5 Next, not O3 Resume.

## Study

Strong continuity case when there is an explicit course/path/thread and a known checkpoint.

## Projects / Work

Strong continuity case for explicit ongoing work.

## Finance

Must **not** manufacture a resume item from recent transactions. A real unfinished review/reconciliation/planning flow may become continuity later.

Initial deterministic scenario: empty.

## Relationships

Must not infer that a relationship/person needs “resuming” from inactivity or message recency. Explicit commitments or shared ongoing plans could qualify later.

Initial deterministic scenario: empty.

## Routine

Upcoming recurring execution is primarily Next/Situation. A routine redesign or explicitly unfinished review could be continuity, but none is invented in the initial scenario.

Initial deterministic scenario: empty.

## Body / Wellness

No generic “resume your health” projection. Only explicit ongoing bounded programs/processes would qualify.

Initial deterministic scenario: empty.

## Unknown future World

Empty is valid. No generic fallback item is fabricated.

---

# 6. DANTE pressure test

## Without DANTE / LLM unavailable

Continuity remains fully usable from application projections.

Hard requirement:

```text
AI unavailable
!=
Continuity unavailable
```

## With DANTE

Future DANTE may:

```text
explain why a continuity thread matters
compare two active threads
answer “where was I?” with evidence
suggest a next step
propose a change
```

But it does not create source-backed continuity facts merely by saying them.

Possible uncertain AI interpretation belongs to Candidate/Insight semantics, not silently inside the source-backed Continuity list.

## Cross-World

Continuity remains scoped to the active World. DANTE may later expand context for a real question, but B2 does not retrieve across Worlds.

---

# 7. Privacy / multi-actor rules

The projection reaching React must already be disclosure-safe.

Permanent rules:

```text
hidden UI != authorization
shared fact != private overlay
absence != false
recent activity != permission to expose private context
```

B2 does not introduce client-side ACL logic or redact after rendering.

---

# 8. First UI decision

The first surface is deliberately **not another dashboard card grid**.

Use a flat, restrained section integrated into the existing workspace:

```text
MONDO
Musica
...

IN MOVIMENTO

Neon Static
Release · Master v3

Glass Signal
Song · Arrangement draft
```

Principles:

```text
one section
bounded ordered rows
no carousel
no nested scroll
no giant KPI
no progress percentage unless semantically real
no fake Resume button
no decorative empty cards
```

The section is omitted when the result is genuinely empty.

This means Finance/Relationships/Routine may correctly show only Orientation in the first deterministic scenario.

---

# 9. Responsive direction

Wide workspace:

```text
section title
row: identity/context ---------------- checkpoint/state
```

Compact workspace:

```text
section title
row stacked vertically
```

Use container queries because World Focus already owns a container-query-ready workspace.

No viewport JS branching.

---

# 10. Accessibility contract

- semantic section heading;
- ordered content exposed as a list;
- no interaction semantics on non-interactive rows;
- no hover-only information;
- status/freshness text available to assistive tech;
- retry is a real button when applicable;
- loading uses a local status without stealing focus;
- no color-only active/paused/blocked distinction;
- 200% zoom and compact containment required;
- axe plus keyboard/manual review.

---

# 11. State model

The Continuity surface must distinguish:

```text
loading
ready
empty
partial
stale
error
unavailable
```

Rules:

```text
empty       -> section omitted; no fake placeholder
partial     -> render known items + truthful local qualification
stale       -> render known items + freshness qualification
error       -> local failure only; World remains usable
unavailable -> local truthful unavailable state; retry only if retryable
```

Provider failure never becomes `empty`.

---

# 12. Application architecture

B2 introduces the first intent-specific read boundary.

It explicitly does **not** add a generic repository/data service.

Target:

```text
WorldFocusContinuityReadPort
        |
        +-- deterministic scenario adapter (now)
        +-- real application/API adapter (future backend vertical)
```

The port returns a bounded Continuity result, not arbitrary World JSON.

The existing `WorldFocusLatestReadCoordinator` owns latest-only frontend reads so a late result from World A cannot attach to World B.

No global store is required.

No TanStack Query dependency is required for this first bounded read.

No new schema library is required; the existing adapter-boundary validation contract remains available.

---

# 13. Projection contract direction

B2 projection data is renderer-facing and intentionally narrow.

Conceptual shape:

```text
WorldContinuityProjection
  schemaVersion
  worldId
  orderedItems[]

WorldContinuityItem
  key
  title
  context
  checkpoint
  presentationState
```

Expected read result is a finite union for ready/empty/partial/stale/unavailable.

Unexpected failures are converted at the application/UI boundary into local `error` state without leaking raw errors.

No canonical entity is copied into this model as canonical truth.

---

# 14. Deterministic scenario adapter

Initial positive fixtures:

```text
music     -> 2 continuity threads
travel    -> 1 planning thread
study     -> 1 learning thread
work      -> 1 explicit work thread
projects  -> 2 project threads
```

Initial valid empty fixtures:

```text
body
finance
relationships
growth
routine
```

The fixture catalog is development/pre-backend product evidence only.

It is not a backend DTO, DB row model or Domain membership list.

---

# 15. Race / resilience tests

Mandatory B2 tests:

```text
A resolves after switch to B -> A cannot commit
abort on superseded read
empty != unavailable
stale renders data rather than false empty
partial keeps usable known items
unexpected error stays module-local
retry starts a new generation
World remains usable if Continuity fails
```

---

# 16. Browser / product tests

At minimum:

```text
Music shows bounded In movimento content
Travel shows planning continuity without pretending “next segment” is Resume
Study shows explicit checkpoint
Finance does not fabricate recent-transaction continuity
Relationships does not fabricate social KPI/resume
Routine remains sparse when no explicit unfinished thread exists
390px remains contained
wide workspace remains restrained
axe A/AA
```

User visual/functional acceptance remains mandatory before B3/next vertical.

---

# 17. Performance

Continuity is first-open high-value content, so its frontend read must be small and bounded.

Rules:

```text
no request per row
no unbounded history
no heavy chart dependency
no eager specialist bundle
no animation required for comprehension
```

A small feature-local performance measure may be added for Continuity read-to-usable once the implementation provides a stable measurement point.

---

# 18. Explicit rejects

```text
recently viewed = resume
sort by timestamp only
AI chooses continuity list without source basis
one resume item mandatory per World
fake Resume CTA
progress percent invented for all items
universal task status model
World-wide generic entity JSON
request per continuity row
client ACL/redaction layer
global state store for one bounded read
carousel hidden behind horizontal gestures
nested scroll
```

---

# 19. Acceptance definition

B2 is complete only when:

```text
semantic contract closed
comparison/research recorded
intent-specific application port implemented
deterministic adapter implemented
real visible Continuity surface implemented
empty/partial/stale/error/unavailable behavior implemented
latest-only race semantics tested
responsive/a11y/performance reviewed
full frontend gates pass
real-browser review passes
user functional/visual gate passes
```

Only then may the next World Focus vertical begin.
