# LifeOS Agent Operating Manual

- Status: Accepted project workflow
- Established: 2026-08-15
- Last updated: 2026-08-17
- Audience: ChatGPT, Claude, Codex, other AI agents, and human contributors
- Purpose: mandatory bootstrap and execution standard for safe continuation of LifeOS work across separate sessions

## 1. Why this manual exists

LifeOS must not depend on one conversation remembering the project correctly. A new chat or agent must be able to resume from the repository, understand what is authoritative, identify the exact active workstream state, and make changes without silently overwriting accepted work or inventing new conventions.

This manual complements:

- `operating-rules.md`;
- `documentation-and-handoff.md`;
- `branching-and-environments.md`;
- the active workstream handoff;
- workstream-specific methodologies and checkpoints.

When this manual and an older generic workflow statement differ in precision, use the stricter current rule unless a higher-authority accepted source explicitly supersedes it.

## 2. Mandatory new-session bootstrap

Before proposing or performing project changes, reconstruct current state from the repository rather than asking the user to restate prior chats.

Read and verify, in this order:

```text
root README.md
→ docs/README.md
→ docs/PROJECT-STATUS.md
→ docs/development/agent-operating-manual.md
→ docs/development/operating-rules.md
→ docs/development/documentation-and-handoff.md
→ docs/development/branching-and-environments.md
→ active docs/workstreams/<workstream>.md logical document
→ current architecture/model index and linked current sources
→ relevant ADRs / methodologies / evidence
→ relevant implementation / tests
→ current Git branch/ref and relation to main
```

Do not infer that a file is current merely because it is detailed, old, marked Accepted, or recently mentioned in conversation.

If a canonical historical/evidence document is physically split, read all required parts when that evidence is material to the task.

## 3. Source precedence

When sources conflict, use this order unless a newer accepted decision explicitly supersedes it:

1. current `main` code/migrations/tests and current accepted model/ADR decisions;
2. current durable product/domain/logical/architecture documentation on `main`;
3. active workstream handoff for newer bounded branch-local work;
4. other explicit current active-branch sources inside that workstream;
5. historical evidence, merged/closed branches and Git history;
6. conversation memory.

Conversation context is useful for orientation but cannot override verifiable repository truth.

A branch may contain newer unmerged truth inside its bounded workstream. It is not a second global source of truth.

## 4. Branch and environment discipline

- `main` is the single integrated project truth.
- Normal work occurs on a bounded active branch.
- Reuse the active workstream branch when its handoff identifies one.
- DEV, UAT and PROD are deployment environments, not long-lived Git branches.
- Do not work directly on `main` unless an explicitly approved exceptional repair requires it.
- Do not force-push/rewrite shared history merely for cleanliness.
- Main synchronization is its own scope when not required for the bounded task.

## 5. Exact Git write gate — mandatory

Before any remote Git write, present an exact write gate and obtain explicit user approval.

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

1. path scope is exact, not approximate;
2. CREATE/UPDATE/DELETE are distinguished;
3. approved PRE-SCOPE SHA is part of approval;
4. approval applies only to that gate;
5. approval is consumed only after the approved work is written and QA-verified cleanly.

Before the first real approved write, re-fetch the active branch HEAD:

```text
current HEAD == approved PRE-SCOPE
→ proceed

current HEAD != approved PRE-SCOPE
→ STOP
→ inspect
→ re-gate if required
```

Never silently continue on a moved branch.

A failed/no-op call or same-SHA ref write does not count as a repository content change.

## 6. Scope integrity during writes

After approval:

- write only approved paths;
- do not add opportunistic fixes outside the gate;
- do not change nearby files merely for convenience;
- do not turn an implementation concern into schema/API/architecture change without a new scope;
- if an approved path is the wrong canonical destination, STOP before writing it and re-gate;
- if an unexpected dependency requires another physical path, STOP/re-gate rather than expanding silently.

Repository state, not tool intent, determines completion.

## 7. Mandatory post-write QA

Every Git write scope is verified against its approved PRE-SCOPE.

At minimum prove:

```text
expected changed physical paths == actual changed physical paths
expected CREATE == actual added paths
expected UPDATE == actual modified paths
expected DELETE == actual deleted paths
out-of-scope paths == 0
branch relation/ahead/behind is as expected
main protection holds where required
```

Any extra physical path is a QA failure until explained and explicitly accepted.

For multi-step scopes, intermediate mini-QA is encouraged after high-risk groups, but final QA covers the entire approved scope.

Do not declare `DONE`, `PASS`, `CLOSED` or equivalent from memory/intended writes. Use remote repository evidence.

If the native compare endpoint is unavailable, do **not** report it as PASS. Verify the equivalent property through remote refs, bounded linear commit chain, per-commit changed paths/status and payload readback; record the fallback honestly.

When a checkpoint/handoff has a post-write marker, update it only after the actual QA result exists.

## 8. Documentation is implementation

Repository documentation is a required project artifact.

Durable decisions, exact continuation state, meaningful validation results and important reopen/dependency state must not exist only in chat.

The active workstream handoff is the live save-game and should make replaying the conversation unnecessary.

At meaningful milestones record, as applicable:

- branch;
- validated/current commit;
- last completed milestone;
- exact current task and next action;
- approved/current scope;
- current sources of truth;
- validation already performed;
- failures/blockers/tool incidents that affect continuation;
- safe deferred dependencies/reopen triggers;
- decisions that must not be casually reopened.

## 9. Current truth vs historical evidence — mandatory distinction

**Current specifications are not chronological logs.**

Use this classification:

```text
CURRENT SPECIFICATION
= current truth only

ADR
= decision rationale + explicit current status/supersession

HISTORICAL / VALIDATION EVIDENCE
= truthful chronology at the time it was produced

GIT / PR HISTORY
= recoverable historical file/change record
```

### 9.1 Current specification rule

Current product/architecture/status/roadmap/handoff documents should contain the current accepted result needed for correct execution.

When current truth changes:

- replace obsolete prose rather than stacking `A → later B → later C` explanations into the current specification;
- keep only historical context that is necessary to understand current semantics or an active constraint;
- repair navigation/references so new agents enter current truth directly.

### 9.2 Historical/evidence rule

Historical checkpoints, validation records, research evidence and truthful transition logs must not be rewritten to pretend they knew later decisions.

Chronology belongs there when chronology is the evidence.

### 9.3 ADR rule

ADRs preserve material rationale and explicit supersession/qualification. They may retain the original decision/rationale while clearly stating the current status and replacement authority.

### 9.4 Knowledge-coverage gate before replace/delete

Before replacing or deleting a stale current document, classify every meaningful statement.

Disposition categories may include:

```text
KEEP IN CURRENT TRUTH
MOVE TO ANOTHER CURRENT SOURCE
KEEP AS ADR/RATIONALE
KEEP AS EVIDENCE/CHECKPOINT
DEFER AS EXPLICIT REQUIREMENT
SUPERSEDED — GIT HISTORY SUFFICIENT
DUPLICATE / NO CONTINUING VALUE
```

A stale current document may be removed from the working tree only when:

```text
unclassified meaningful content = 0
valid requirement lost = 0
current truth represented = PASS
rationale worth retaining mapped = PASS
references/navigation repaired = PASS
```

Do not keep obsolete files merely to make the repository a museum. Do not delete them before coverage proves useful knowledge is safe.

## 10. Large-document and tool-limit discipline

Tool/context limits never justify knowledge loss.

Never truncate or replace a large canonical/current document with partial content merely because a connector cannot return/write it conveniently.

If complete-file replacement is required:

1. verify the complete current payload can be reconstructed safely;
2. preserve all still-valid content and make the intended bounded edit;
3. if complete reconstruction is unsafe, do not perform a risky partial replacement;
4. use a canonical split/continuation only where the logical document genuinely requires chronological/evidence continuity or size/tool-limit handling;
5. when splitting only because of size/tool limits, preserve the complete intended logical payload losslessly across the physical parts — **do not summarize, condense, paraphrase away, omit, reorder or silently clean up substantive content as part of the split**;
6. if semantic/current-truth cleanup is needed as well, treat that cleanup as a separate content operation with its own justified scope; the physical split itself remains lossless;
7. if no safe route exists, STOP and report the exact tool limitation.

Do not repeatedly retry the same failure without new information.

## 11. Canonical split-document rule

A physical split does **not** create multiple logical documents.

```text
README.md
README-part-2.md
README-part-3.md
= 1 logical document / 3 physical paths
```

### 11.1 Logical-document counting

Count the split set as one logical document.

### 11.2 Physical-path counting

Git gates and QA enumerate every physical path independently.

### 11.3 Canonical split contract

Use the repository `LIFEOS-CANONICAL-SPLIT` / `LIFEOS-CANONICAL-PAYLOAD` convention or an explicitly compatible continuation form where required.

All parts together carry the logical document's evidence/authority as defined by the document type.

### 11.4 Size / tool-limit split — lossless partition only

When the reason for splitting is file size, connector limits, write limits or another transport/tooling constraint:

```text
1 complete logical payload
→ physical partition only
→ all canonical parts together reconstruct the complete intended payload
```

The split operation itself MUST NOT:

- summarize;
- condense;
- replace earlier detailed content with a shorter recap;
- paraphrase substantive content merely to reduce size;
- omit requirements/evidence/decisions;
- reorder content in a way that changes meaning or chronology;
- hide semantic cleanup or supersession inside the split.

Split markers/navigation metadata may be added as required, but the substantive payload is preserved losslessly.

If the content itself also needs revision, first define/approve the semantic/current-truth edit as such; do not call a summary/rewrite a `split`.

### 11.5 Chronological / evidence continuation

For chronological/evidence split documents, downstream amendments belong after the previous final payload, normally in the last/new continuation part. Do not append a newer event into an earlier part and falsify chronology.

A chronological/evidence continuation may legitimately add new later evidence; this is different from a size/tool-limit split of one already-defined payload.

### 11.6 Current specifications should not split merely to preserve obsolete history

If a current specification can be rewritten cleanly to current truth, do that through a deliberate current-truth edit. A split/continuation is not a reason to carry stale current prose forever, and a current-truth rewrite must not be disguised as a lossless split.

## 12. Git/tool failure behavior

Distinguish:

```text
project/semantic problem
!= repository-state problem
!= Git conflict/SHA problem
!= connector/tool capability limit
!= local network/environment limit
```

For non-trivial failures:

1. stop blind retries;
2. report attempted operation and concrete error/status;
3. verify whether the write landed;
4. state which writes exist and which do not;
5. state current verified branch/HEAD if available;
6. confirm repository integrity where possible;
7. preserve remaining scope;
8. use only safe alternatives.

Never claim success from an attempted call alone.

## 13. Freshness and supersession

Current indexes/handoffs must point to the newest current truth.

Historical evidence may record legitimate earlier `SAFE DEFERRED`, HOLD, READY or other stage states; those states do not override later explicit closure/current sources.

Do not inherit an old candidate ranking or roadmap after the model changes. Re-evaluate from the accepted current baseline when methodology requires it.

Do not preselect the next candidate during closure unless the user included it in scope.

## 14. Domain Model special protocol

For Core Domain Model / Domain Atlas work, `docs/domain/validation-methodology-v3.md` and `docs/domain/validation-execution-template-v3.md` remain mandatory for any separately authorized new validation/reopen unless explicitly superseded.

Required conceptual pipeline:

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

Every material neighbor in the Adjacent Dependency Sweep is classified. `SAFE DEFERRED` requires reason, owner/stage, exact reopening trigger and tests to rerun.

`PASS WITH HARDENING` is not complete until required hardenings are incorporated and retested/propagated as required.

Do not jump from semantic validation directly into SQL/migrations/API/Auth/Physical/provider implementation without a separate approved scope.

## 15. No ontology by convenience

Do not create generic roots/tables/entities merely because implementation looks more uniform.

Do not add schema/API/provider/cross-cutting convention only because an AI suggested it or an external standard uses it.

External products/standards are evidence. Adapt useful patterns while preserving accepted LifeOS semantics.

## 16. Communication during long work

For long multi-tool operations, provide concise substantive updates such as:

- HEAD verified;
- X/Y approved paths written;
- unexpected dependency found;
- fallback QA in progress;
- compare/path QA matches scope.

Do not spam low-level narration.

When the user already supplied an answer/approval, do not ask again.

## 17. Completion language must match evidence

Use precise state language:

```text
validated semantically
written remotely
propagated
QA pending
QA PASS
closed
blocked by tool
```

Do not collapse these into vague `done`.

## 18. Handoff minimum for a new chat

The active workstream must allow recovery of:

```text
repository
active branch
current verified HEAD
main baseline if relevant
current logical workstream state
last completed milestone
current incomplete scope
exact remaining physical paths
known failed/no-op writes / tool limits
validation verdicts
REOPEN / unclassified state
important deferred dependencies
next exact safe action
explicit out-of-scope boundaries
```

A new chat should normally read this instead of asking the user to reconstruct prior conversations.

## 19. Final operating principle

Prefer truthful partial completion over risky or falsely complete work.

```text
understand current truth
→ define exact scope
→ obtain approval
→ verify PRE-SCOPE
→ execute only approved work
→ preserve useful knowledge and truthful evidence
→ keep current specifications current
→ verify remote result
→ document continuation state
```

If a tool prevents a safe step, stop at the safe boundary, explain the blocker precisely and leave the repository recoverable.
