# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Current phase:** GLOBAL CURRENT-TRUTH RECONCILIATION
- **AI-02.1 / AI-03 / AI-04:** CLOSED / STRUCTURALLY ACCEPTED
- **PRE-AI05 hardening:** CLOSED / STRUCTURALLY ACCEPTED / PRE05-H01..H19
- **Fresh retest after H19:** PASS / 26 OF 26 STRUCTURAL CASES
- **Reverse-order retest:** PASS
- **2026 state-of-the-art regression:** PASS
- **Current core eval families:** DANTE-E01..DANTE-E14
- **AI-05:** NEXT / BECOMES CURRENT AFTER GLOBAL RECONCILIATION
- **Refreshed:** 2026-09-02
- **Current branch HEAD:** FETCH LIVE before every write

Repository truth outranks this temporary handoff.

## 1. Resume sequence

```text
feature/ai-architecture
→ PRE-AI05 H01..H19 already CLOSED
→ current exact action = GLOBAL CURRENT-TRUTH RECONCILIATION
→ then AI-05 Whole-System Acceptance + Implementation Blueprint
→ then actual AI implementation workstream(s)
```

Do not restart AI-02/03/04/PRE-AI05 redesign without concrete contradictory downstream evidence.

## 2. Closed architecture truth

```text
AI-03A       C01..C33
AI-03B       B01..B35
AI-03C       MAT-01..MAT-15
AI-04A       A01..A30 / EV01..EV20
AI-04B       RT-01..RT-31
AI-04C       PA-01..PA-61
AI-04 whole  WP-01..WP-22
PRE-AI05     H01..H19
```

Provider/model selection remains OPEN. No implementation/API/DB/direct-provider PASS exists.

## 3. PRE05-H01..H19

```text
H01 AttentionBudget != ResourceBudget != commercial/provider quota
H02 trigger fired != material change/current work eligibility
H03 causal-loop / oscillation safety is production-critical
H04 DANTE-E14 proactive/Attention/loop safety is core eval
H05 cumulative disclosure may span related work
H06 recipient != surface != channel
H07 scoped autonomy is policy ceiling, not Authority/AuthZ/approval
H08 unsafe autonomy and excessive over-asking are graded separately
H09 current-tree eval coverage E01..E14
H10 AI-01 old ModelTarget shorthand is historical terminology
H11 WP route composition outranks older AI-04B local sequence
H12 old pre-Physical AI/context boundary is historical in current navigation
H13 formal IFC/leakage-budget/ACS implementations remain challengers
H14 commercial tier cannot buy weaker attention/autonomy/privacy safety
H15 AttentionDecision != proactive Work Admission != Effect authorization
H16 cumulative disclosure may span Runs/Interactions/surfaces/known related sinks
H17 RUN-START AUTONOMY != PERPETUAL AUTONOMY
H18 NOTIFY != SENT != DELIVERED != SEEN != ACKNOWLEDGED != ACCEPTED
H19 SOURCE CONTENT/FUTURE ELIGIBILITY != PRIOR DISCLOSURE OCCURRENCE
```

H19 allows only minimum non-content security/accounting state needed to prevent cumulative re-disclosure after source deletion when its independent protection purpose still applies. It is not Context/Memory/source evidence and cannot reconstruct or resurrect deleted content.

## 4. Core eval coverage

```text
E01 deterministic/model avoidance
E02 target resolution
E03 extraction
E04 query/history/absence
E05 context/privacy/Reality Scope/cumulative disclosure
E06 planning/replanning/scenario
E07 document/long-context/multimodal
E08 tool/capability use
E09 consequential effect/scoped autonomy
E10 multi-actor/delegation/surface disclosure
E11 adaptive memory/learning
E12 currentness/failure/supersession/failover
E13 open-world research/grounding
E14 proactivity/Attention/causal-loop/notification truth
```

## 5. Acceptance evidence

```text
fresh full AI-01→AI-04 + H01..H19 retest     PASS / 26 OF 26
compound collision retest                    PASS
reverse PRE05→04→03→02→01                   PASS
refreshed 2026 state-of-the-art regression   PASS
```

Structural evidence only.

## 6. Current exact action

```text
GLOBAL CURRENT-TRUTH RECONCILIATION
```

Expected current truth after the bounded global gate:

```text
AI-04 CLOSED / STRUCTURALLY ACCEPTED
PRE-AI05 CLOSED / H01..H19
DANTE-E01..E14 current
old ai-context-runtime-boundaries.md classified HISTORICAL in navigation
AI-05 CURRENT / Whole-System Acceptance + Implementation Blueprint
```

No provider/model/API/backend/database implementation claim may be added.

## 7. Current non-claims

```text
PRE-AI05 PASS                    YES / STRUCTURAL
AI-05 SUBSTANTIVE DESIGN         NOT YET STARTED
PROVIDER/MODEL/SDK SELECTED      NO
DIRECT PROVIDER EVAL             NO
PRODUCTION CAPACITY PASS         NO
IMPLEMENTATION                   NO
POSTGRESQL/ALEMBIC CHANGE        NO
```

## 8. Git discipline

Before every remote write: exact BRANCH / PRE-SCOPE / CREATE / UPDATE / DELETE / PURPOSE / OUT-OF-SCOPE gate, then refetch HEAD. After writes compare PRE-SCOPE..HEAD and prove path scope.

## 9. Handoff lifecycle

This file is temporary and MUST NOT merge to protected `main`. Before integration: propagate durable truth → verify coverage → DELETE this file.