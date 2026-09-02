# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Current phase:** PRE-AI05 CROSS-PHASE HARDENING + WHOLE-CHAIN RETEST
- **AI-02.1 / AI-03 / AI-04:** CLOSED / STRUCTURALLY ACCEPTED
- **PRE-AI05 hardening:** CANDIDATE / PRE05-H01..H18
- **Retest history:** first FAIL bounded → H15-H16; second full FAIL bounded → H17-H18
- **Fresh retest after H17-H18:** NOT YET EXECUTED
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

Only if PASS:

```text
mark PRE-AI05 accepted
→ global current-truth reconciliation
→ AI-05 current
```

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

## 3. PRE05-H01..H18

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
```

H17 requires current scoped-autonomy revalidation before an autonomous consequential dispatch after waits/replanning/material changes/policy changes.

H18 requires truthful notification transport state and E14 coverage for timeout/unknown/replay/deduplication.

## 4. Current E01..E14 coverage

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

## 5. Fresh hostile retest set

```text
1 own-effect loop without new material delta
2 own-effect loop + genuine new external change
3 attention storm under quiet hours
4 urgent material signal under high attention pressure
5 cumulative protected inference inside one interaction
6 cumulative protected inference across separate Runs
7 same recipient across private/lock/shared/voice surfaces
8 known related sinks compose protected information
9 AUTO_WITHIN_SCOPE then Authority/AuthZ revoked
10 AUTO_WITHIN_SCOPE then autonomy alone changes to PROPOSE_ONLY
11 PROPOSE_ONLY with mutation technically available
12 attention silent while background work eligible
13 attention notify while consequential work ineligible
14 notification decision + transport timeout/unknown delivery
15 duplicate/replayed notification transport event
16 commercial quota exhausted during optional proactive work
17 quota exhausted after outcome-unknown effect
18 failover with context/capability contraction
19 continuation after policy/tool/Harness change
20 stale callback after supersession
21 provider/cache memory after deletion/revocation
22 auxiliary router/verifier/judge as governed recipient
23 model outage while deterministic route remains valid
24 proactive Run + autonomy change + failover + surface change + quota pressure
25 private source + cumulative disclosure + deletion + old cache/restore + new Run
```

PASS requires no unexplained responsibility gap or hidden safety downgrade.

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