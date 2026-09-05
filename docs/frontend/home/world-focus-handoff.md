# DANTE — World Focus Handoff

**Status:** CURRENT DURABLE HANDOFF — M4 CLOSED / VALIDATED — MAIN RECONCILIATION NEXT  
**Date:** 2026-09-05  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-react`  
**Worktree:** `/home/mattia/projects/dante-frontend`

This handoff lets a new chat/agent continue without reconstructing the workstream from conversation history. Read repository live before every write.

Read first:

```text
1. world-focus-current-checkpoint.md
2. world-focus-frontend-roadmap.md
3. world-focus-handoff.md
4. world-focus-evidence-index.md
5. current-checkpoint.md
6. world-focus-m4-final-hostile-closure-review.md
7. world-focus-d6-governed-operation-review.md
8. world-focus-d5-insight-presentation-review.md
9. world-focus-d4-contextual-invocation-review.md
10. world-focus-d3-deterministic-conversation-adapter-review.md
11. world-focus-d2-adaptive-conversation-surface-review.md
12. world-focus-m3-final-hostile-closure-review.md
13. product/platform/structure/geometry contracts as needed
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
M3 final hostile closure                   CLOSED / PASS
M4 D2–D6                                   CLOSED / VALIDATED
D2 adaptive conversation surface           CLOSED / VALIDATED
D3 deterministic conversation adapter      CLOSED / VALIDATED
D4 contextual/deictic invocation           CLOSED / VALIDATED
D5 Insight presentation integration        CLOSED / VALIDATED
D6 Proposal/confirmation/receipt           CLOSED / VALIDATED
M4 final hostile closure                   CLOSED / PASS
MAIN RECONCILIATION / INTEGRATION          NEXT BEFORE M5
M5                                         NOT STARTED
M6–M7                                      BLOCKED BY SEQUENCE
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
AI output != fact
Comparison != Decision
conversation message != Insight
assistant prose != validated Insight
Insight != Proposal
Proposal != Decision
Decision != effect
confirmed != executed
Receipt != provider/runtime/canonical completion
provider ACK != canonical completion
client composition config != Domain state
presentation geometry != conversation identity
route presentation != automatically blocking interaction
context/selection != authorization
context reference != canonical truth
mounted frontend transcript != durable DANTE Run
cancelled/aborted request != semantic success
```

## 4. Closed platform foundation

Workspace Platform remains the only planning/packing/transient-placement authority. M1 owns non-visual production semantics/application seams. M2 owns bounded display-safe binding, presentation grammar, finite renderers and truthfulness qualifiers. M3 owns revisioned client composition metadata, canonical draft transaction, meaningful opportunity extraction, candidate resolution, explicit Customize UX and normal live adaptive composition.

M4 reuses those owners. It did not create a second Workspace, conversation or governed-operation state engine.

## 5. Closed M4 result

```text
D2
wide viable workspace -> non-modal DANTE sidecar
constrained/mobile -> route-owned DANTE focus
maximize/restore -> same conversation surface identity

D3
D1 composer
-> typed request bound to World + Workspace generation + requestId
-> deterministic local reader
-> validated answer | explanation or truthful technical state

D4
explicit semantic affordance
-> finite WorldFocusContextReferenceSet
-> same D1 composer
-> same D3 conversation

D5
current D3-owned assistant message
-> explicit Open as Insight
-> deterministic Insight reader
-> validated observation | pattern | change
-> standalone dante-insight surface

D6
current D5-owned Insight
-> Proposal
-> required blocking Confirmation
-> local confirmed | declined Decision
-> truthful local Receipt
```

Global invocation remains context-free. A context reference is neither authorization nor canonical truth. D5/D6 adapters cannot widen their source basis. Workspace-generation changes fail closed across pending/materialized DANTE artifacts.

## 6. M4 hostile closure — real findings

The final hostile pass found three owner-boundary leaks rather than merely confirming happy paths.

```text
A. D5 -> D6
RED   775281b8bdca5dd5cccb63be5ecb6d9ebabd5b2d / CI #1066
FIX   D6 derives exact current D5 Insight; caller cannot inject an Insight object
GREEN 929c5ad7a056ff172a915e5070e7d72c936e692d / CI #1071

B. D3 -> D5
RED   bf6caef751505d35cbfd694ce6f1d532409517f3 / CI #1076
FIX   D5 resolves exact assistant message from D3 owner by identity
GREEN e8b836f49ddb85a95e0ba6b9472b56f3f45d83eb / CI #1080

C. D4 -> D3
RED   8dd3572652bde94778ee230cf80437fc8e22a1b8 / CI #1085
FIX   D3 derives contextual seed from D4 owner; caller cannot substitute references
GREEN eccdc4d986a4880e9e45766900cb833b665d8cea / CI #1086
```

Final lifecycle matrix:

```text
HEAD 1b8ae1a3d953d85dcc14d513e512428d1f268c8d
CI   33990483780 / run #1087 PASS
Quality / Mobile / Chromium / Firefox / Frontend CI Gate PASS
```

Detailed authority: `world-focus-m4-final-hostile-closure-review.md`.

## 7. D6 closure evidence

```text
PRE-SCOPE 40dc630ba436317f89951e71c22172b2c3852558
VALID RED fb1d002712bcd9b4c8c0c5a23156a13abb71303b
RED CI    33974791760 / run #1058 EXPECTED FAILURE
GREEN     234eb159a5993db9b909880f58231a1e27cdefef
GREEN CI  33975428193 / run #1061 PASS
OWNER GREEN 929c5ad7a056ff172a915e5070e7d72c936e692d
OWNER CI    33986493932 / run #1071 PASS
```

D6 executes no real effect. Receipt truth is explicitly local and pre-backend.

Detailed authority: `world-focus-d6-governed-operation-review.md`.

## 8. Visual strategy and truth

```text
After M4: structural visual check only
M5: build contrasting complete Worlds
After M5: serious product/visual review
M6: visual polish + responsive + motion + a11y + performance
M7: frontend/backend seam freeze
```

Automated browser/structural/a11y coverage is green. Human/manual visual acceptance remains **NOT PERFORMED** and must not be inferred from CI.

## 9. Immediate continuation — do not start M5 yet

The next task is branch reconciliation/integration, not M5 feature work.

```text
freeze exact M4 documentation closure SHA
-> fetch current protected main
-> inspect divergence
-> reconcile main INTO feature/home-react under current authority
-> resolve conflicts by ownership/semantic authority
-> full repository QA
-> docs lifecycle cleanup
-> PR -> protected main
-> merge commit only
-> protected-main readback
-> archive/delete feature/home-react only after verified merge
-> fresh bounded M5 branch from integrated main
```

## 10. Explicit out-of-scope until a new gate

```text
NO M5 implementation
NO backend/API/DB/Alembic/AuthZ/provider/LLM
NO real effect execution
NO localStorage fake persistence
NO durable server/cross-device DANTE persistence
NO Timeline/Access/Auth collateral work
NO GlobalTopbar ownership rewrite
NO WF0/WF-G3 macro geometry rewrite
NO arbitrary DOM/component payload serialization as DANTE context
NO main write/merge/rebase/force-push without explicit integration authority
NO history rewrite
NO claim of human visual acceptance from automated green
```
