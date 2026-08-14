# Reconciliation / Source Precedence v0

**Status:** Current accepted baseline — PASS WITH HARDENING; hardenings incorporated; post-write QA PASS  
**Validated:** 2026-08-13  
**Validation standard:** Domain Validation Methodology v3  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`  
**Pre-scope validated baseline:** `f2c28d0f4fe6ec6afe1b5934ec4279422a09605a`

## Canonical definition

> **Reconciliation is the contextual cross-cutting reasoning/process capability through which LifeOS handles materially competing states, assertions or interpretations concerning the same bounded target, question or facet while preserving their identity, Version, Provenance, Evidence, Actor and Authority context. Reconciliation applies an explicit bounded resolution basis where one exists and may select, combine, correct, supersede, escalate, defer or intentionally retain conflict unresolved. Reconciliation does not itself establish objective truth, own the resulting domain state, or create universal source precedence.**

Canonical question:

> **Which materially competing states or assertions concern this bounded target/question, what applicable resolution basis exists, and what — if anything — becomes the current/effective interpretation without rewriting history?**

Classification:

```text
RECONCILIATION
CANONICAL CROSS-CUTTING REASONING / PROCESS CAPABILITY

✅ competing materially relevant states/assertions
✅ bounded target/question/facet/context
✅ explicit applicable resolution basis
✅ deterministic, human, policy or specialist resolution paths
✅ unresolved conflict as valid state
✅ history-preserving correction/supersession
✅ may yield a Decision or new material Version when appropriate

CONFLICT
✅ contextual/derived condition
❌ universal native entity/root

SOURCE PRECEDENCE
✅ contextual bounded policy/basis when justified
❌ universal source ranking
❌ source identity
❌ objective truth

RECONCILIATION
❌ universal aggregate root/entity
❌ Decision
❌ Authority
❌ Actual
❌ Version
❌ Provenance
❌ Evidence
❌ technical merge/sync/CRDT
❌ last-write-wins
```

---

# 1. Why Reconciliation exists

Version v0 established that LifeOS can preserve distinct materially relevant states and the semantic actions bound to them. It deliberately does not determine which state becomes current, effective or preferred when materially competing states/assertions exist.

The accepted model already contains repeated conflict pressure across Observation, Actual, Outcome, Confirmation, provider imports, Schedule, Evidence, AI proposals and concurrent/offline Versions.

Without a common Reconciliation discipline, LifeOS is pushed toward weak alternatives: silent last-write-wins, newest-source-wins, provider-always-wins, user-always-wins, Authority mistaken for objective truth, Decision required for every conflict, Provenance/source used as a winner rule, or incompatible family-specific conflict handling.

Reconciliation provides the cross-cutting discipline while leaving the actual resulting state in the affected domain concept.

---

# 2. Reconciliation is a process/capability, not a universal root

LifeOS does not need a universal `Reconciliation` object for every conflict or correction.

Reconciliation may be implicit and deterministic in low-consequence cases, explicitly policy-driven, assisted by AI, performed through a bounded Decision, deferred to an external specialist system, or left unresolved.

> **The semantic capability is canonical; a universal independent Reconciliation entity/root is not.**

A qualified persisted reconciliation record may later be justified where the resolution itself has material history, Authority, rationale, Evidence, audit or privacy consequences. That does not make it mandatory everywhere.

---

# 3. Conflict detection is not conflict resolution

Two states may be materially divergent without LifeOS yet knowing what should happen.

```text
Base S1
├─ S2A
└─ S2B
```

Detecting that `S2A` and `S2B` compete is distinct from selecting, merging or rejecting either.

> **Conflict detection != conflict resolution.**

This permits a valid state such as:

```text
conflict = known
resolution = unresolved
```

without fabricating certainty.

---

# 4. Unresolved conflict is valid reality

LifeOS must preserve ambiguity when no sufficient bounded basis exists.

Examples include two credible sensors that disagree, two actors reporting incompatible facts, two providers disagreeing without an authoritative one for the relevant facet, imported state conflicting with a correction whose status is uncertain, or offline edits that cannot be safely merged.

> **No sufficient resolution basis is itself a valid outcome of reconciliation; LifeOS may preserve conflict unresolved.**

Unresolved conflict must not be silently converted into latest-wins, creator-wins, manager-wins, provider-wins, user-wins, average-wins or AI-confidence-wins.

---

# 5. Source identity, Provenance, Authority and truth are distinct

A source can be known without being authoritative. A source can be authoritative for one bounded facet without being authoritative for all facts. A creator/recorder can have Provenance significance without governance power. An Actor can have Authority to make a state effective without proving the resulting state is objectively true in every epistemic sense.

```text
source identity
!= Provenance
!= Authority
!= source precedence
!= objective truth
```

> **Source precedence must always be bounded to the relevant target/facet/purpose/context/time and applicable policy; it is never a universal rank attached to the source.**

---

# 6. Version boundary

Version answers which materially relevant states exist and which state a semantic action concerned. Reconciliation answers how materially competing states/assertions are handled, under what bounded basis, and what remains current/effective or unresolved.

```text
Version != Reconciliation
```

Reconciliation may consume Version state and may produce a new material state/Version. If compatible facets from S2A and S2B are safely combined into S3, Version preserves S1/S2A/S2B/S3 while Provenance explains how S3 arose.

---

# 7. Provenance boundary

Provenance explains origin/evolution: who/what produced a state, from which source, through which process. Reconciliation uses that lineage as possible Evidence/context but does not reduce to it.

```text
Provenance != winner rule
source lineage != source precedence
```

A newer provider record may have excellent Provenance and still not automatically supersede another valid state.

---

# 8. Evidence boundary

Evidence may support, contradict or weaken competing interpretations. Reconciliation may consider Evidence, but Evidence itself does not decide the current state.

```text
Evidence != Reconciliation result
```

Two high-quality pieces of Evidence may remain contradictory. Reconciliation may preserve that unresolved conflict rather than manufacture an average or arbitrary winner.

---

# 9. Authority boundary

Authority answers who/what may legitimately make a bounded effect effective. Reconciliation may require Authority to establish a resulting current/effective state, but:

```text
Authority != objective truth
Authority != source precedence automatically
Authority != Reconciliation
```

An authorized result does not erase competing historical assertions or manufacture universal truth.

---

# 10. Decision boundary

Decision is one possible path inside a reconciliation process, but not every reconciliation requires a human Decision.

Valid deterministic paths may include normalized-unit equivalence, explicit bounded source-of-record policy, automatic stale-base rejection before semantic effect, or combining independent non-conflicting facets.

> **Reconciliation may culminate in or consume a Decision, but Reconciliation != Decision and deterministic authorized resolution must not fabricate a human Decision.**

---

# 11. Actual, Observation and Outcome

Actual may have competing assertions before a current contextual realization is established. Reconciliation can help establish which assertion/state is accepted for a bounded context without becoming Actual itself.

Two Observations can legitimately conflict; reconciliation may keep both unresolved, prefer a bounded specialist source, identify one as a correction/duplicate where justified, construct a derived interpretation where the owning domain permits, or escalate to a human/specialist resolution. It must not silently average or overwrite by recency.

A later authoritative or better-supported state may change the current Outcome without rewriting historical evaluation. Reconciliation remains distinct from Outcome.

---

# 12. Schedule / provider conflicts

Schedule often receives external updates. Provider recency is not a canonical winner rule.

```text
provider candidate state
+ current LifeOS Schedule state
+ Version / Provenance / applicable Authority or source policy
→ reconciliation
→ current Schedule or unresolved conflict
```

Schedule owns the resulting accepted temporal assignment.

---

# 13. Concurrent/offline divergence

Non-linear Version history is valid.

```text
S1
├─ S2A offline
└─ S2B provider/other actor
```

Reconciliation may merge independent non-conflicting facets, reject stale mutation, preserve both branches unresolved, ask for human/specialist resolution, or construct S3 under explicit policy.

> **Last-write-wins is not a canonical LifeOS reconciliation policy.**

Technical CRDT/OT/merge algorithms remain implementation-stage concerns and cannot decide domain materiality, Authority or truth by themselves.

---

# 14. Source precedence

Source precedence is valid only as bounded policy/basis. A specialist system may be source of record for one bounded facet; a user may be authoritative for a private preference; a provider calendar may be authoritative for provider-owned cancellation but not unrelated private annotations.

Canonical rules:

1. source precedence is contextual;
2. it may vary by target/facet/purpose/time;
3. it may depend on Authority/policy/specialist ownership;
4. it does not make the source universally truthful;
5. it must be explainable where consequence warrants;
6. absence of applicable precedence may leave conflict unresolved.

Rejected: provider > user always, user > provider always, creator > everyone, manager > everyone, newest > older, most updates > fewer updates, highest AI confidence > others.

---

# 15. Specialist source-of-record boundary

LifeOS may recognize an external specialist system as authoritative for a bounded fact/state while remaining a personal coordination layer. This does not mean LifeOS copies the specialist system's entire workflow or assigns it universal precedence.

> **External source-of-record status is bounded specialist policy, not a kernel-wide source hierarchy.**

---

# 16. Multi-actor, Representation and common ground

Shared reality may contain different Actor positions. A later authoritative Decision may establish current shared state without rewriting historical assertions as though all actors agreed.

```text
shared reconciled result
!= Agreement
!= Consent
!= every Actor's stance
```

A representative may participate in reconciliation while acting for another party. Actual Actor, represented party, applicable Authority/delegation basis and material states remain distinct. Representation does not itself establish source precedence or result validity.

---

# 17. Visibility and privacy

A reconciled current result may be visible while conflict, private sources, Evidence, rationale or rejected states remain hidden.

```text
visible result
!= visible conflict history
!= visible private source
!= visible resolution rationale
```

> **Reconciliation state, competing sources, Evidence, rationale and history have independently governed Visibility.**

---

# 18. AI boundary

AI may detect likely conflicts, compare material states, classify potentially independent/non-conflicting changes, surface applicable source/Authority policy, explain safe visible differences, propose a resolution, request human/specialist Decision, or identify that conflict should remain unresolved.

AI must not make recency/confidence the universal winner rule, fabricate human Decision, exceed applicable Authority/policy, expose hidden conflict/source information, silently rewrite Actor assertions, hide unresolved divergence to produce a neat answer, or apply stale-base resolution after material change without re-evaluation.

> **AI recommendation or confidence is Evidence/proposal input, not universal source precedence or Authority.**

---

# 19. Reversal and correction

A reconciliation result may later be corrected or superseded. Historical resolution and the material state it established remain reconstructible where required.

```text
later resolution != earlier resolution never existed
```

Version and Provenance preserve state/result lineage. Reconciliation does not rewrite past actors' knowledge or basis.

---

# 20. Product simplicity

Most users should not see `Reconciliation`, `Source Precedence` or conflict graphs in ordinary use.

Natural UI may be:

```text
This changed somewhere else
Keep mine
Use updated value
Review conflict
Both changes can be kept
Needs review
```

High-consequence/power-user surfaces may expose competing values/states, sources, material differences, applicable source-of-record policy, Actor/Authority context, resulting Decision and historical resolutions.

> **Low-consequence deterministic reconciliation should normally remain product-invisible.**

---

# 21. Core invariants

1. Reconciliation is a cross-cutting reasoning/process capability, not a universal native entity/root.
2. Conflict detection != conflict resolution.
3. Unresolved conflict is a valid state.
4. Competing material states/assertions remain reconstructible.
5. There is no universal source priority.
6. Newer != truer or more authoritative.
7. Source identity != Authority != truth.
8. Source precedence is target/facet/purpose/context/time scoped.
9. Version identifies competing states; it does not reconcile them.
10. Provenance explains origin; it does not choose a winner.
11. Evidence may support/contradict without determining result by itself.
12. Authority legitimizes bounded effect; it does not manufacture objective truth.
13. Decision is one possible reconciliation path, not mandatory for every reconciliation.
14. Deterministic authorized reconciliation may occur without fabricated human Decision.
15. Effective/current state remains owned by the affected domain concept.
16. A reconciliation result may create a new material Version with predecessors preserved.
17. Non-conflicting changes may be combined only where semantically safe.
18. Last-write-wins is not a canonical LifeOS rule.
19. User-always-wins is rejected.
20. Provider-always-wins is rejected.
21. Specialist source-of-record precedence is bounded to its actual authoritative context.
22. Actor stances, Acknowledgement, Agreement and Consent remain separate from reconciliation result.
23. Conflict/source/basis Visibility is independently governed.
24. AI may detect/explain/propose but cannot silently exceed policy/Authority.
25. Technical merge/CRDT/ETag/MVCC != domain Reconciliation.
26. Correction/reversal preserves prior resolution/assertion history.
27. Reconciliation does not merge native identities; entity deduplication/merge-split is separate.
28. Reconciliation persistence/formality is consequence-sensitive.

---

# 22. Rejected alternatives

```text
universal Reconciliation entity/root
universal Conflict entity/root
universal SourcePrecedence entity/rank
global source priority list
last-write-wins as canonical policy
newest-source-wins
provider-always-wins
user-always-wins
creator-always-wins
manager-always-wins
AI-confidence-wins
source = Authority
source = truth
Provenance = reconciliation
Decision required for every reconciliation
Authority = truth
technical CRDT/merge result = domain truth
silent overwrite of competing assertions
forced averaging of conflicting observations
```

---

# 23. Adjacent Dependency Sweep

Resolved semantic boundaries:

```text
Actual ↔ competing assertions ↔ Reconciliation
Version ↔ divergent states ↔ Reconciliation
Decision ↔ Reconciliation
Authority ↔ Reconciliation
Provenance ↔ Source Precedence
Evidence ↔ Reconciliation
Confirmation conflict ↔ Reconciliation
Observation conflict/correction ↔ Reconciliation
Outcome correction ↔ Reconciliation
Schedule/provider conflict ↔ Reconciliation
offline/concurrent divergence ↔ domain reconciliation
technical merge/concurrency ↔ domain reconciliation
AI stale-base conflict ↔ Reconciliation
```

SAFE DEFERRED owners remain: exact per-domain/source precedence policy; GoalCriterion/evaluation; Proposal/request identity; Trigger/conditional policy; CRDT/OT/merge implementation; native-entity duplicate merge/split; specialist source-of-record mappings; collective/quorum resolution; Principal/AuthN/AuthZ enforcement; retention/audit; physical representation/API.

Every SAFE DEFERRED item is executable through the normative validation checkpoint with explicit owner, reopening trigger and rerun tests.

```text
REOPEN                         0
unclassified material items    0
```

---

# 24. Persistence/API implications without physical commitment

Future modeling must be able, where consequence requires, to answer which material states/assertions conflict, what bounded target/facet/question they compete about, what Version/Provenance/Actor/source context applies, what bounded source/Authority/policy basis was considered, whether conflict was resolved/deferred/unresolved, whether a Decision occurred, which state/result became current/effective in the owning concept, whether a new material Version was produced, which predecessors were preserved and what conflict/rationale/source history a viewer may see.

Not pre-approved:

```text
reconciliations table
conflicts table
source_priority column
winner_source_id
last-write-wins trigger
generic merge JSON
universal state machine
CRDT/OT
one workflow engine
one source-precedence service
```

---

# 25. Reopening triggers

Reopen if Decision + Authority + Version + Provenance can absorb reconciliation without loss, a universal persistent lifecycle proves independently necessary, purpose-specific precedence requires a stronger common policy concept, native identity merge/split must be owned here, sync implementation forces technical merge into the semantic family, whole-domain regression shows excess ambiguity/cost, or simple-user flows require visible reconciliation machinery too often.

Implementation convenience or provider vocabulary alone is not sufficient reason to reopen.

---

# 26. Current validation position

Normative validation checkpoint:

- `../checkpoints/reconciliation-source-precedence-v0-validation.md`

```text
RECONCILIATION / SOURCE PRECEDENCE v0
PASS WITH HARDENING

CORE gate                       PASS WITH HARDENING
Multi-Actor gate                PASS WITH HARDENING
Cross-Concept gate              PASS WITH HARDENING
REOPEN                          0
unclassified material items     0
```

The hardenings above are incorporated and retested. The approved 28-path propagation and final post-write QA are complete; Reconciliation / Source Precedence v0 is the current accepted branch baseline.