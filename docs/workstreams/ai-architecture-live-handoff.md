# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Current phase:** PRE-AI05 CROSS-PHASE HARDENING + WHOLE-CHAIN RETEST
- **AI-02.1 / AI-03 / AI-04:** CLOSED / STRUCTURALLY ACCEPTED
- **PRE-AI05 hardening:** CANDIDATE / PRE05-H01..H19
- **Retest history:** first FAIL bounded → H15-H16; second full FAIL bounded → H17-H18; third full FAIL bounded → H19
- **Fresh retest after H19:** NOT YET EXECUTED
- **AI-05:** NEXT ONLY AFTER PRE-AI05 PASS + CURRENT-TRUTH RECONCILIATION
- **Refreshed:** 2026-09-02
- **Current branch HEAD:** FETCH LIVE before every write

Repository truth outranks this temporary handoff.

## 1. Resume sequence

```text
feature/ai-architecture
→ read accepted AI-00/02/03/04 authority
→ read docs/architecture/dante-ai-pre05-cross-phase-hardening.md
→ restart full AI-01→AI-04 destructive retest from zero
→ reverse-order retest
→ refreshed 2026 state-of-the-art regression check
```

Only if PASS: mark PRE-AI05 accepted → global current-truth reconciliation → AI-05 current.

## 2. Closed architecture truth

```text
AI-03A  C01..C33
AI-03B  B01..B35
AI-03C  MAT-01..MAT-15
AI-04A  A01..A30 / EV01..EV20
AI-04B  RT-01..RT-31
AI-04C  PA-01..PA-61
AI-04 whole  WP-01..WP-22
```

Provider/model selection remains OPEN. No implementation/API/DB PASS exists.

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
H18 Attention/Notify decision != SENT != DELIVERED != SEEN != ACKNOWLEDGED != ACCEPTED
H19 SOURCE CONTENT/LIFECYCLE != PRIOR DISCLOSURE OCCURRENCE
```

H19 allows only minimum non-content security/accounting state needed to prevent cumulative re-disclosure after source deletion; it has its own justified purpose/lifetime, is not Context/Memory/source evidence, and cannot reconstruct or resurrect deleted content.

## 4. Core eval coverage

```text
E01 deterministic/model avoidance
E02 target resolution
E03 extraction
E04 query/history/absence
E05 context/privacy/cumulative disclosure
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

## 5. Fresh hostile retest focus

All prior cases must be rerun. Compound privacy pressure now explicitly tests:

```text
private source
→ prior safe disclosure
→ source deletion/revocation
→ stale cache/backup restore
→ new Run
→ source remains ineligible
→ minimum prior-exposure safety accounting may remain independently eligible
→ no cumulative leak / no source resurrection
```

Also retest autonomy-only revocation, notification UNKNOWN/replay, proactive+failover+surface+quota pressure and deterministic operation during model outage.

## 6. Current non-claims

```text
PRE-AI05 PASS                    NO
AI-05 STARTED                    NO
PROVIDER/MODEL/SDK SELECTED      NO
DIRECT PROVIDER EVAL             NO
IMPLEMENTATION                   NO
POSTGRESQL/ALEMBIC CHANGE        NO
```

## 7. Git discipline

Before every remote write: exact BRANCH / PRE-SCOPE / CREATE / UPDATE / DELETE / PURPOSE / OUT-OF-SCOPE gate, then refetch HEAD. After writes compare PRE-SCOPE..HEAD and prove path scope.

## 8. Handoff lifecycle

This file is temporary and MUST NOT merge to protected `main`. Before integration: propagate durable truth → verify coverage → DELETE this file.