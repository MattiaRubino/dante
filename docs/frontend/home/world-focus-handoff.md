# DANTE — World Focus Handoff

**Status:** CURRENT DURABLE HANDOFF — M0 / M1 / POST-M1 SAFETY / M2 / M3 CLOSED — M4 ACTIVE / D2–D3 CLOSED / D4 PREFLIGHT NEXT  
**Date:** 2026-09-05  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This handoff lets a new chat/agent continue without reconstructing the workstream from conversation history. Read repository live before every write; this file defines current sequence and durable constraints, not a substitute for code inspection.

Read first:

```text
1. world-focus-current-checkpoint.md
2. world-focus-frontend-roadmap.md
3. world-focus-handoff.md
4. world-focus-evidence-index.md
5. current-checkpoint.md
6. world-focus-d3-deterministic-conversation-adapter-review.md
7. world-focus-d2-adaptive-conversation-surface-review.md
8. world-focus-m3-final-hostile-closure-review.md
9. world-focus-dante-spatial-presence-review.md
10. world-focus-d1-dante-entry-review.md
11. product/platform/structure/geometry contracts as needed
```

Older phase-time `NEXT` prose is evidence only unless adopted by current checkpoint authority.

## 1. Current sequence

```text
WF0 / WF-G3                                FROZEN / LOCKED
B0 / WR0–WR2 / B1 / B2                    CLOSED / VALIDATED AS RECORDED
Workspace Platform                         ENGINEERING CLOSED
D0                                         ACCEPTED
D1                                         CLOSED FOR SEQUENCING
WS0–WS8                                    CLOSED
M0                                         CLOSED
M1                                         CLOSED / VALIDATED
POST-M1 SAFETY                             CLOSED / PASS
M2                                         CLOSED / VALIDATED
M3                                         CLOSED / VALIDATED
M3-1                                       CLOSED / VALIDATED
M3-2                                       CLOSED / VALIDATED
PRE-M3-3                                   CLOSED / PASS
M3-3                                       CLOSED / VALIDATED
M3-4                                       CLOSED / VALIDATED
M3 final hostile closure                   CLOSED / PASS
M4 D2–D6                                   ACTIVE
D2 adaptive conversation surface           CLOSED / VALIDATED
D3 deterministic conversation adapter      CLOSED / VALIDATED
D4 contextual/deictic invocation           READ-ONLY PREFLIGHT NEXT
D5–D6                                      BLOCKED BY D4 SEQUENCE
M5–M7                                      BLOCKED BY SEQUENCE
BACKEND                                    BLOCKED UNTIL M7
human/manual visual acceptance             NOT PERFORMED
```

## 2. Product compass

DANTE:

> **Understand life. Shape what comes next.**

World Focus:

> **Understand this part of my life and continue from here.**

Core thesis:

> **A World is a shared coordinate system between user and DANTE, not a shared source of truth.**

World is not a Domain owner, folder, life taxonomy, DB partition, security boundary, AI memory bucket, chat room or mandatory Goal/KPI/time surface.

## 3. Permanent semantic barriers

```text
World != canonical Domain owner
World relevance != authorization
projection != canonical truth
reference exists != payload available != current != disclosable != fresh
Evidence != Provenance != integrity attestation
available disclosure != frontend AuthZ
offline != source absent
timeout != semantic negative
Proposal != Decision != effect
provider ACK != canonical completion
Comparison != Decision
missing trajectory position != zero
AI output != fact
client composition config != Domain state
client revision != backend persistence revision
renderer availability != mandatory mounting
adopt != semantic truth/AuthZ/persistence
presentation geometry != conversation identity
route presentation != automatically blocking interaction
context/selection != authorization
mounted frontend transcript != durable DANTE Run
cancelled/aborted request != semantic success
```

## 4. Closed M3 substrate

M1 owns non-visual production semantics/application seams. M2 owns bounded display-safe binding, presentation grammar, finite renderers and truthfulness qualifiers. Workspace Platform remains the only planning/packing/placement authority.

M3 owns revisioned client composition metadata, canonical draft transaction, meaningful opportunity extraction, candidate resolution, explicit manual Customize UX and live normal adaptive composition.

Canonical config:

```text
schemaVersion / revision / worldId / ordered entries
entry: instanceId / kind / visibility / pinned / prominenceOverride
```

Finite commands:

```text
adopt / pin / unpin / hide / show / move / promote / restore
```

One governed path:

```text
manual UI [M3-3] ----\
                       -> commands -> isolated DRAFT -> REVIEW/APPLY -> CONFIG
DANTE proposal [M4] --/
```

No hidden DANTE mutation route. `adopt` materializes composition metadata only. `restore` is base-relative. Apply requires World match, revision match and exact base snapshot. No implicit merge/rebase.

## 5. M3 closure anchor

```text
PRE-SCOPE 2e69b1dd0bda25beaecbc5e5baa26f8720a76ff1
HOSTILE   d9c30a3c6148469b347754eab07dc2ade9be4c52
CI        33951509083 / run #944 PASS
80 / 80 web test files
391 / 391 web unit tests
300 modules / 899 dependencies / 0 architecture violations
```

Detailed evidence:

```text
world-focus-m3-final-hostile-closure-review.md
world-focus-m3-4-integrated-adaptive-composition-review.md
```

## 6. D2 closed result

D2 materializes the accepted D0 adaptive spatial contract without creating a chatbot product or second surface engine.

```text
wide viable workspace
-> non-modal DANTE conversation sidecar

constrained/mobile workspace
-> route-owned focus surface below Global Topbar

wide explicit maximize
-> same surface identity sidecar -> route focus
-> restore returns same identity to adaptive presentation
```

Ownership:

```text
WorldFocusWorkspaceHost
-> still owns the one transient surface stack

existing Workspace allocator
-> still owns split viability and placement from actual measured workspace geometry

D2 presentation controller
-> owns only adaptive | focus presentation preference

route-owned surface layer
-> renders existing external placement through the same finite registry/error-boundary path
```

Important correction discovered by hostile regression:

```text
route presentation != interaction blocker
```

Generic route remains non-blocking. DANTE route-focus explicitly carries `blocksWorkspaceInteraction=true`; that law also prevents weaker late surfaces from taking authority over the route-focus interaction.

Final D2 evidence:

```text
PRE-SCOPE 0a0a43ac06f93d986674f8521e521dcc05ea2c1e
CODE/TEST  7b787766be83096e82eab1ac116b2704fae5f202
CI         33958677991 / run #969 PASS
82 / 82 web test files
399 / 399 web unit tests
305 modules / 929 dependencies / 0 architecture violations
```

Detailed evidence: `world-focus-d2-adaptive-conversation-surface-review.md`.

## 7. D3 closed result

D3 fills the D2 structural shell with deterministic typed conversation behavior while keeping all existing ownership boundaries intact.

```text
D1 composer submit
-> atomic handoff to the existing `dante:conversation` surface
-> D3 mounted transcript + typed request
-> deterministic pre-backend runtime seam
-> validated correlated answer | explanation
   OR truthful unavailable/error/cancelled/superseded
```

Application boundary:

```text
worldId
workspace generation
requestId
transient user input / bounded local history
locale
AbortSignal
```

A result must correlate to the exact request/World/generation and pass a fail-closed validator. Unexpected semantic widening is rejected rather than silently accepted.

Lifecycle:

```text
pending request + Cancel
-> abort
-> user turn remains
-> no response appended
-> late completion ignored

pending request + Workspace generation change
-> superseded / abort
-> old result cannot attach
```

The transcript is mounted frontend state only. It is not localStorage, server persistence, canonical World state or a durable DANTE Run.

D3 also closes the real focus lifecycle:

```text
composer -> conversation
-> no premature focus return to invoke

conversation close / Escape
-> exact original DANTE invoker receives focus
-> World route remains open
```

A unit test discovered that keeping the invoke inside D2's keyed idle/active presentation subtree remounted the DOM button and violated exact focus return. Stable invokes were moved outside the keyed presentation session; Workspace/D2 allocation ownership was not changed.

D3 browser coverage proves wide sidecar, 390px route-owned focus, maximize/restore identity continuity, no horizontal overflow, compact close target >=44px and automated axe checks.

Final D3 evidence:

```text
PRE-SCOPE 57520cf0570bc2be875e7140d066e45ddd9080d5
CODE/TEST  59c70af6005ee87918db7fe152c043699726e78c
CI         33963858340 / run #1009 PASS
84 / 84 web test files
410 / 410 web unit tests
311 modules / 963 dependencies / 0 architecture violations
Contracts / lint / typecheck / generated / build / diff / mutation PASS
Mobile / Chromium / frozen Timeline Firefox / Frontend CI Gate PASS
```

Final code/test compare is linear (`ahead 23`, `behind 0`) from the exact PRE-SCOPE and contains only 14 D3 code/test/i18n paths. No Workspace allocator/model, AppShell, Timeline, Access/Auth, generated route tree, backend/API/DB/Alembic/provider/LLM/persistence path changed.

Detailed evidence: `world-focus-d3-deterministic-conversation-adapter-review.md`.

## 8. D4 next read-only preflight

D4 owns bounded contextual/deictic invocation.

Before writes inspect live:

```text
D3 typed request/result boundary and mounted transcript lifecycle
D1/D2 interaction/surface ownership
existing World context-reference model and resolution seams
current disclosure/truth distinctions
selection/focus owners that may provide an explicit reference
current i18n/a11y/unit/browser harness
```

D4 must preserve:

```text
selection/context != authorization
context reference != canonical truth
reference exists != payload available != current != disclosable != fresh
DOM/component state != conversation payload
presentation geometry != conversation identity
D3 request correlation/generation guards remain authoritative
```

Initial bounded interaction pressure should cover explicit references such as:

```text
perché?
confronta con prima
aprimi la fonte
continua da qui
```

D4 must not serialize arbitrary DOM/source payload into conversation state. It should reuse bounded reference/disclosure owners and remain pre-backend.

Then state exact:

```text
PRE-SCOPE
CREATE
UPDATE
DELETE
RED-FIRST
OUT-OF-SCOPE
```

Do not pull D5–D6 or backend/provider semantics forward.

## 9. Remaining M4 sequence

```text
D4 contextual/deictic invocation with bounded references
-> D5 Insight presentation integration
-> D6 Proposal / confirmation / receipt presentation
```

DANTE proposals later reuse canonical app paths; they do not bypass manual capability or mutation governance.

## 10. Visual strategy agreed with user

```text
After M4: structural visual check only
M5: build contrasting complete Worlds
After M5: serious product/visual review
M6: visual polish + responsive + motion + a11y + performance
M7: frontend/backend seam freeze
```

Do not spend D4–D6 on unrelated cosmetic redesign.

## 11. Explicit out-of-scope

```text
NO backend/API/DB/Alembic/AuthZ/provider/LLM
NO localStorage fake persistence
NO durable server/cross-device persistence
NO Timeline/Access/Auth collateral work
NO GlobalTopbar ownership rewrite
NO WF0/WF-G3 macro geometry rewrite
NO D5–D6 hidden inside D4
NO arbitrary DOM/component payload serialization as DANTE context
NO generated route-tree edits unless a later explicitly-authorized route design proves unavoidable
NO history rewrite / force push
```

## 12. Human visual status

Automated browser coverage is green. Human/manual visual acceptance remains **NOT PERFORMED** and must not be inferred from CI.
