# LifeOS Agent Operating Manual

- Status: Accepted project workflow
- Established: 2026-08-15
- Audience: ChatGPT, Claude, Codex, other AI agents, and human contributors
- Purpose: mandatory bootstrap and execution standard for safe continuation of LifeOS work across separate sessions

## 1. Why this manual exists

LifeOS must not depend on one conversation remembering the project correctly. A new chat or agent must be able to resume from the repository, understand what is authoritative, identify the exact active workstream state, and make changes without silently overwriting accepted work or inventing new conventions.

This manual consolidates the stricter operating standard reached during the Domain Model workstream. It complements, and does not replace, the repository's existing workflow documents:

- `operating-rules.md`;
- `documentation-and-handoff.md`;
- `branching-and-environments.md`;
- the active workstream handoff;
- workstream-specific methodologies and checkpoints.

When this manual and an older generic workflow statement differ in precision, use the stricter rule unless a higher-authority current source explicitly supersedes it.

## 2. Mandatory new-session bootstrap

Before proposing or performing project changes, a new agent must reconstruct the current state from the repository rather than asking the user to restate prior chats.

Read and verify, in this order:

```text
root README.md
→ docs/README.md
→ docs/PROJECT-STATUS.md
→ docs/development/agent-operating-manual.md
→ docs/development/operating-rules.md
→ docs/development/documentation-and-handoff.md
→ docs/development/branching-and-environments.md
→ active docs/workstreams/<workstream>.md canonical document
→ linked accepted product / architecture / ADR / methodology docs
→ relevant implementation / tests / checkpoints
→ current Git branch/ref and compare against main when relevant
```

Do not infer that a file is current merely because it is detailed or recently mentioned in conversation.

If the active workstream document is physically split, read all canonical parts required to reconstruct the logical document, including the latest continuation part.

## 3. Source precedence

When sources conflict, use this authority order unless a newer accepted decision explicitly supersedes it:

1. current `main` code, migrations, tests and accepted ADRs;
2. current durable documentation on `main`;
3. active workstream handoff for newer unmerged branch-local work;
4. other explicit active-branch current documents/checkpoints;
5. merged/closed branches and Git history;
6. conversation memory.

Conversation context is useful for orientation but is not allowed to override verifiable repository truth.

A newer branch-local workstream amendment may legitimately be newer than `main` inside that workstream's bounded scope. That does not make the branch authoritative for unrelated project areas.

## 4. Branch and environment discipline

- `main` is the single integrated project truth.
- Normal work occurs on a bounded active branch.
- Reuse the active workstream branch when its handoff identifies one; do not create helper branches without a concrete reason.
- DEV, UAT and PROD are environments, not long-lived Git branches.
- Do not work directly on `main` unless an explicitly approved exceptional repair requires it.
- Do not force-push or rewrite shared history merely for cleanliness.
- Main synchronization is its own scope when it is not required for the bounded task. Do not smuggle it into unrelated work.

## 5. Exact Git write gate — mandatory

Before any remote Git write, present an exact write gate and obtain explicit user approval.

The gate must contain:

```text
BRANCH
<exact branch>

PRE-SCOPE
<exact current commit SHA>

CREATE
<exact paths>

UPDATE
<exact paths>

DELETE
<exact paths>

PURPOSE
<what this scope accomplishes>

EXPLICITLY OUT OF SCOPE
<what will not be touched>
```

Rules:

1. path scope must be exact, not approximate;
2. CREATE / UPDATE / DELETE must be distinguished;
3. the approved pre-scope SHA is part of the approval;
4. approval applies only to that gate;
5. an approval is consumed only after the approved work has been written and QA-verified cleanly.

Before the first write after approval, re-fetch the active branch HEAD.

```text
current HEAD == approved PRE-SCOPE
→ proceed

current HEAD != approved PRE-SCOPE
→ STOP
→ inspect the change
→ issue a new gate if needed
```

Never silently continue on a moved branch.

## 6. Scope integrity during writes

After approval:

- write only approved paths;
- do not add an opportunistic fix outside the gate;
- do not modify a nearby file merely because it would be convenient;
- do not convert an implementation concern into a schema/API/architecture change without a new scope;
- if an approved path is discovered to be the wrong physical/canonical destination, STOP before writing that path and re-gate the correction;
- if an unexpected dependency requires another file, STOP and re-gate rather than silently expanding scope.

A failed/no-op write does not mean the intended change exists. Repository state, not tool intent, determines completion.

## 7. Mandatory post-write QA

Every Git write scope must be verified against its approved pre-scope.

At minimum verify:

```text
expected changed physical paths == actual changed physical paths
expected CREATE == actual added paths
expected UPDATE == actual modified paths
expected DELETE == actual deleted paths
out-of-scope paths == 0
branch remains ahead/behind as expected
```

Any extra physical path is a QA failure until explained and explicitly accepted.

For a multi-step scope, intermediate mini-QA is encouraged after high-risk groups of writes, but final QA must compare the entire approved scope.

Do not declare `DONE`, `PASS`, `CLOSED`, or an equivalent status from memory or intended writes. Use the remote repository compare/result as evidence.

When a checkpoint has an explicit post-write marker, update it only after the actual QA result exists.

## 8. Documentation is implementation

Repository documentation is a required project artifact, not cleanup after code/design work.

Durable decisions, exact operational continuation state, meaningful validation results, and important reopen/dependency state must not exist only in chat.

The active workstream handoff is the live save-game. It should allow another agent to resume without replaying the conversation.

At meaningful milestones record, as applicable:

- exact branch;
- last validated/current commit;
- last completed milestone;
- exact current task;
- exact next action;
- approved/current scope;
- important source-of-truth files;
- validations already performed;
- failures or blockers;
- safe deferred dependencies and reopening triggers;
- decisions that must not be casually reopened.

If critical continuation information exists only in chat, the handoff is incomplete.

## 9. Historical preservation rule

Historical reasoning is evidence and must not be rewritten merely to make current documentation look cleaner.

Default behavior:

- preserve accepted historical checkpoints;
- preserve rejected alternatives, hardenings, examples, deferred items and earlier status when they accurately describe the state at that time;
- add later closure/amendment sections that explain what changed downstream;
- distinguish historical validation state from current semantic authority;
- never make an old checkpoint falsely appear to have known a later decision.

Use append/current-amendment semantics when chronology matters.

Delete historical content only when there is a concrete correctness, security, legal or maintenance reason and the deletion is explicitly in scope.

## 10. Large-document and tool-limit discipline

Tool/context limits never justify knowledge loss.

Never truncate, summarize away, compress away or replace a large canonical document with partial content merely because a connector cannot return or write it conveniently.

If a connector requires complete-file replacement:

1. verify that the complete current file can be reconstructed safely;
2. if it can, preserve the full payload and make the intended bounded edit;
3. if it cannot, do not attempt a risky partial replacement;
4. prefer a canonical physical split/continuation when that preserves the logical document safely;
5. if no safe write route exists, STOP and report the exact tool limitation.

Do not repeatedly retry the same failing Git operation without new information.

## 11. Canonical split-document rule

A physical split does **not** create multiple logical documents.

Example:

```text
README.md
README-part-2.md
README-part-3.md
README-part-4.md
```

means:

```text
1 logical canonical document
4 physical Git paths
```

This distinction is mandatory in all planning and QA.

### 11.1 Logical-document counting

When describing the domain/documentation model, count the split set as one document.

Do not inflate document/concept counts because a canonical payload was physically split for size/tool reasons.

### 11.2 Physical-path counting

For Git write gates and Git QA, every physical path still counts independently because exact repository changes must be auditable.

Therefore reports should distinguish, where relevant:

```text
logical documents affected
physical paths changed
```

### 11.3 Canonical split contract

A canonical split should use the repository's `LIFEOS-CANONICAL-SPLIT` / `LIFEOS-CANONICAL-PAYLOAD` convention or an explicitly compatible continuation form.

All parts together carry canonical authority. A part is not a summary/reference substitute for the others.

### 11.4 Chronology

For an already split chronological document, new downstream amendments belong after the previous final payload: normally the last physical part, or a newly created continuation part when the last part has become operationally too large.

Do not append a new 2026 amendment to Part 1 if Parts 2–3 contain later preserved history; doing so falsifies chronology.

### 11.5 Extending an existing split

If a split document needs a new part because the final part is too large:

- treat the new part as continuation of the same logical document;
- preserve all previous parts;
- update navigation/total markers when it can be done safely;
- if a connector limitation makes historical marker rewrites unsafe, use an explicit canonical continuation amendment rather than rewriting large preserved payloads blindly;
- document the physical continuation clearly so future agents know the complete logical reading order.

## 12. Git/tool failure behavior

When Git, GitHub, connector, network or another execution tool fails, distinguish the failure type from project semantics.

Use this classification:

```text
project / semantic problem
!= repository state problem
!= Git conflict / SHA problem
!= connector/tool capability limit
!= local environment/network limit
```

Do not turn a connector limitation into a project-design change.

If a non-trivial Git/tool problem occurs:

1. stop repeated blind retries;
2. report the exact attempted operation;
3. report the concrete error/status (`409`, `404`, SHA mismatch, truncation, unsupported operation, network failure, etc.);
4. state which writes actually landed and which did not;
5. state the current verified branch/HEAD if available;
6. state whether existing repository content remains intact;
7. state the remaining scope;
8. propose only safe alternatives.

Never claim a write succeeded merely because the tool call was attempted.

## 13. Current truth versus historical evidence

When downstream work resolves an earlier deferred dependency:

- keep the earlier SAFE DEFERRED record as historical evidence;
- add a downstream closure stating that the dependency is now resolved;
- do not erase the fact that it was legitimately deferred earlier;
- ensure current indexes/handoffs identify the newer accepted state.

Historical checkpoint wording does not override newer explicit amendments.

## 14. Freshness and candidate selection

Do not inherit an old ranking as a roadmap after the model changes.

Where a workstream uses candidate scoring/re-scoring, re-score from the new accepted baseline after every meaningful milestone when the methodology requires it.

Do not preselect the next candidate during closure of the current one unless the user explicitly includes that in scope.

## 15. Domain Model special protocol

For Core Domain Model / Domain Atlas work, `docs/domain/validation-methodology-v3.md` is the mandatory current validation standard and `docs/domain/validation-execution-template-v3.md` is the mandatory execution template for new validations unless explicitly superseded.

The required ordered pipeline is conceptually:

```text
fresh candidate selection / re-score
↓
problem + evidence formation
↓
EV evidence gates
↓
smallest surviving candidate
↓
identity / independence / boundaries / deferrals
↓
CORE semantic gate
↓
MA multi-actor gate
↓
XCON cross-concept gate
↓
Adjacent Dependency Sweep
↓
RESOLVED / SAFE DEFERRED / REOPEN
↓
adversarial log
reopening/dependency register
regression additions
↓
verdict
↓
documentation propagation analysis
↓
STOP BEFORE GIT WRITE
```

Allowed verdict vocabulary is controlled by the methodology. A `PASS WITH HARDENING` is not considered complete until required hardenings are incorporated and retested/propagated as required.

Every material neighbor in the Adjacent Dependency Sweep must be classified. `SAFE DEFERRED` is not shorthand for "later"; it must include why it is non-blocking, owner/stage, exact reopening trigger, and tests to rerun.

Do not jump from semantic validation directly into SQL, migrations, API, auth, physical persistence or provider contracts unless that separate implementation scope has been explicitly approved.

## 16. No ontology by convenience

Do not create generic roots/tables/entities merely because they make implementation look uniform.

Do not add a schema/API/provider/cross-cutting convention only because an AI suggested it or an external standard uses it.

External products/standards are evidence. Adapt useful separation patterns, reject irrelevant ontology, and preserve LifeOS's accepted semantics.

## 17. Communication during long work

For long multi-tool operations, give concise progress updates so the user can see what has actually happened and can interrupt if needed.

Useful updates report substantive state such as:

- HEAD verified;
- split path corrected;
- X/Y approved paths written;
- compare matches expected scope;
- blocker discovered.

Do not spam low-level tool narration.

When the user has already supplied an answer or approval, do not ask the same question again.

## 18. Completion language must match evidence

Use precise status language:

```text
validated semantically
written remotely
propagated
QA pending
QA PASS
closed
blocked by tool
```

Do not collapse these into one vague "done".

For example, a concept can be semantically `PASS WITH HARDENING` while propagation QA is still pending. That must remain visible until the repository proves closure.

## 19. Handoff minimum for a new chat

Before ending or switching sessions, the active workstream should make it possible to recover:

```text
repository
active branch
current verified HEAD
main baseline if relevant
logical workstream state
last completed milestone
current incomplete scope
exact remaining physical paths
known failed writes / tool limits
validation verdicts
REOPEN / unclassified state
important deferred dependencies
next exact safe action
explicit out-of-scope boundaries
```

A new chat should normally be able to read this information instead of asking the user to reconstruct prior conversations.

## 20. Final operating principle

Prefer a truthful partial completion over a risky or falsely complete one.

The safe order is:

```text
understand current truth
→ define exact scope
→ obtain approval
→ verify pre-scope
→ execute only approved work
→ preserve history
→ verify remote result
→ document continuation state
```

If a tool prevents a safe step, stop at the safe boundary, explain the blocker precisely, and leave the repository in a recoverable state.
