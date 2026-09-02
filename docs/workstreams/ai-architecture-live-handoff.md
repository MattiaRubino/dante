# DANTE AI Architecture — Live Handoff

- **Status:** TEMPORARY / BRANCH-OPERATIONAL SAVE-GAME
- **MUST NOT MERGE TO PROTECTED `main`**
- **Branch:** `feature/ai-architecture`
- **Current phase:** PRE-AI05 CROSS-PHASE HARDENING + WHOLE-CHAIN RETEST
- **AI-02.1:** CLOSED / STRUCTURALLY ACCEPTED
- **AI-03:** CLOSED / STRUCTURALLY ACCEPTED
- **AI-04:** CLOSED / STRUCTURALLY ACCEPTED
- **PRE-AI05 hardening:** CANDIDATE / PRE05-H01..H16
- **First post-materialization retest:** FAIL BOUNDED / H15-H16 ADDED
- **Full retest after H15-H16:** NOT YET EXECUTED
- **AI-05:** NEXT ONLY AFTER PRE-AI05 PASS + CURRENT-TRUTH RECONCILIATION
- **Refreshed:** 2026-09-02
- **Current branch HEAD:** FETCH LIVE before every write

Repository truth outranks this temporary handoff.

---

## 1. Resume sequence

```text
feature/ai-architecture
→ read accepted AI-00/02/03/04 authority
→ read docs/architecture/dante-ai-pre05-cross-phase-hardening.md
→ restart whole AI-01→AI-04 destructive retest from zero
→ reverse-order retest
→ refreshed 2026 state-of-the-art regression check
```

If and only if PASS:

```text
mark PRE-AI05 accepted
→ global current-truth reconciliation
→ AI-05 current
```

Do not restart AI-02/03/04 wholesale unless the retest exposes a concrete contradiction requiring the smallest affected reopen.

---

## 2. Mandatory AI sources

```text
docs/architecture/dante-ai-foundation.md
docs/architecture/ai-production-engineering-state-of-the-art-2026.md
docs/architecture/dante-ai-02-1-intelligence-reengineering.md
docs/architecture/dante-ai-03-context-retrieval-memory.md
docs/architecture/dante-ai-03a-full-context-architecture.md
docs/architecture/dante-ai-03b-retrieval-memory-architecture.md
docs/architecture/dante-ai-03c-destructive-validation-materialization-blueprint.md
docs/architecture/dante-ai-04-productionization-architecture.md
docs/architecture/dante-ai-04a-direct-eval-specification.md
docs/architecture/dante-ai-04b-concrete-runtime-capability-architecture.md
docs/architecture/dante-ai-04c-production-assurance-control-plane-operations.md
docs/architecture/dante-ai-04-whole-phase-destructive-acceptance.md
docs/architecture/dante-ai-pre05-cross-phase-hardening.md
```

Use Product/North Star and accepted Domain/Logical/Physical/PostgreSQL only as upstream semantic contracts. Do not audit unrelated active branch topology during this PRE-AI05 retest.

---

## 3. Accepted closure truth

```text
AI-03A  C01..C33
AI-03B  B01..B35
AI-03C  MAT-01..MAT-15
AI-04A  A01..A30 / EV01..EV20
AI-04B  RT-01..RT-31
AI-04C  PA-01..PA-61
AI-04 whole  WP-01..WP-22
```

Provider/model selection remains OPEN.

---

## 4. PRE05-H01..H16

```text
H01 AttentionBudget != ResourceBudget != commercial/provider quota
H02 trigger fired != material change/current work eligibility
H03 causal-loop / oscillation safety is production-critical
H04 DANTE-E14 proactive/Attention/loop safety is core eval
H05 cumulative disclosure may span related work
H06 recipient != surface != channel
H07 scoped autonomy is policy ceiling, not Authority/AuthZ/approval
H08 unsafe autonomy and excessive over-asking are graded separately
H09 current-tree eval coverage is E01..E14
H10 AI-01 old ModelTarget shorthand is historical terminology
H11 WP route composition outranks older AI-04B local sequence
H12 old pre-Physical AI/context boundary is historical in current navigation
H13 formal IFC/leakage-budget/ACS implementations remain challengers
H14 commercial tier cannot buy weaker attention/autonomy/privacy safety
H15 AttentionDecision != proactive Work Admission != Effect authorization
H16 cumulative disclosure may span Runs/Interactions/surfaces/known related sinks
```

The first post-write retest found H15 and H16. They are materialized now. Full retest must restart from zero.

---

## 5. Core eval families now required by current tree

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
E12 failure/currentness/supersession/failover
E13 open-world research/grounding
E14 proactivity/Attention/causal-loop safety
```

No provider API key is required for this architecture retest.

---

## 6. Required hostile retest set

```text
1 own-effect loop without new material delta
2 own-effect loop + genuine new external change
3 attention storm under quiet hours
4 urgent material signal under high attention pressure
5 cumulative protected inference inside one interaction
6 cumulative protected inference across separate Runs
7 same recipient across private/lock/shared/voice surfaces
8 known related sinks compose protected information
9 AUTO_WITHIN_SCOPE then current Authority/AuthZ revoked
10 PROPOSE_ONLY with mutation technically available
11 attention silent while background work is otherwise eligible
12 attention notify while consequential work is ineligible
13 commercial quota exhausted during optional proactive work
14 quota exhausted after outcome-unknown effect
15 failover with context/capability contraction
16 continuation after policy/tool/Harness change
17 stale callback after supersession
18 provider/cache memory after deletion/revocation
19 auxiliary router/verifier/judge as governed recipient
20 deterministic route during model outage
```

PASS requires no unexplained responsibility gap and no hidden safety downgrade.

---

## 7. Current non-claims

```text
PRE-AI05 CANDIDATE MATERIALIZED       YES
FIRST RETEST                          FAIL BOUNDED
H15-H16 MATERIALIZED                  YES
FULL RETEST AFTER H15-H16             NO
PRE-AI05 PASS                         NO
AI-05 STARTED                         NO
PROVIDER/MODEL/SDK SELECTED           NO
DIRECT PROVIDER EVAL                  NO
IMPLEMENTATION                        NO
POSTGRESQL/ALEMBIC CHANGE             NO
FORMAL IFC / ATTENTION ENGINE         NO
```

---

## 8. Git discipline

Before every remote write: exact BRANCH / PRE-SCOPE / CREATE / UPDATE / DELETE / PURPOSE / OUT-OF-SCOPE gate, then refetch HEAD. After writes, compare PRE-SCOPE..HEAD and prove path scope.

---

## 9. Handoff lifecycle

This file is temporary and MUST NOT merge to protected `main`.

Before integration:

```text
propagate durable truth
→ verify coverage
→ DELETE THIS FILE
```
