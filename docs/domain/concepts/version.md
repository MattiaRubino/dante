# Version / Material-State v0

**Status:** Proposed baseline — PASS WITH HARDENING; post-write QA pending  
**Validated:** 2026-08-13  
**Validation standard:** Domain Validation Methodology v3  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`  
**Pre-scope validated baseline:** `1008aeb0367de4ae73a8e8d41a76aee9e0493f34`

## Canonical definition

> **Version / Material-State is the cross-cutting semantic capability through which LifeOS can identify and reconstruct a materially relevant state of an otherwise stable domain target, bind semantic actions, attestations, permissions, evaluations or decisions to the state they actually concerned, and determine — according to the owning semantic purpose — whether a later state remains materially equivalent for that use. Version does not define target identity, explain lineage, choose canonical state, decide reconciliation, or turn every technical write into a domain revision.**

Canonical question:

> **Which materially relevant state of this target did this semantic act or evaluation concern, and does a later state remain equivalent for that specific purpose?**

Classification:

```text
VERSION / MATERIAL-STATE
CANONICAL CROSS-CUTTING SEMANTIC CAPABILITY / DISCIPLINE

✅ stable target with reconstructible materially relevant states
✅ target-state binding for semantic actions/evaluations
✅ historical applicability
✅ consequence-sensitive materiality
✅ concurrent/divergent states where reality requires them
✅ direct, derived or qualified representation according to consequence

MATERIAL EQUIVALENCE
✅ contextual / purpose-specific applicability determination
❌ universal object-wide equality flag

VERSION
❌ native entity/root
❌ target identity
❌ every database update
❌ updated_at
❌ ETag / MVCC / optimistic-lock token
❌ provider revision identifier
❌ content hash
❌ Provenance
❌ Decision / Authority / reconciliation
❌ mandatory global sequence
```

---

# 1. Why Version / Material-State exists

The accepted Domain Atlas repeatedly needs to preserve the state to which another semantic fact applied.

Examples already present in the current model include:

```text
Acknowledgement(target v1)
Confirmation(target v1)
Decision(proposal v1)
Agreement(terms v1)
Consent(scope/purpose v1)
Participation response(invitation/occurrence state v1)
Responsibility hand-off response(request v1)
Representation(action against state v1)
Evidence(evaluation using source/rule state v1)
Occurrence(generated under Routine/Recurrence policy v1)
```

A later material change must not silently rewrite those facts as though they concerned the new state.

Without a common Version / Material-State discipline, LifeOS is pushed toward one of two failures:

1. every concept invents a separate incompatible version mechanism; or
2. implementations use the latest row/value and lose what actors actually saw, accepted, confirmed, agreed, permitted, decided, evaluated or acted against.

The semantic capability is therefore real even though a universal `Version` entity/root is not justified.

---

# 2. Stable target identity versus state identity

A target may remain the same domain identity while its state changes materially.

```text
Event E17
Schedule state S1 = 15:00
Schedule state S2 = 16:00
```

The Event need not become another Event merely because its Schedule changed.

Likewise:

```text
Observation O17
v1 = 76.4 kg
v2 = 66.4 kg after correction
```

may remain one Observation identity if the correction concerns the same observational act.

Canonical rule:

> **Target identity and material-state identity are distinct questions. Ordinary revision of state does not automatically create a new target identity.**

The inverse is equally important: Version must not be used to hide a genuine identity replacement.

```text
Milestone
B1 reached
```

redefined as:

```text
Milestone
C1 reached
```

may no longer be the same checkpoint at all. The owning concept decides whether continuity survives.

Canonical identity guardrail:

> **If a change destroys the owning concept's identity invariants, the result may require replacement/new identity rather than another Version. Version cannot manufacture continuity.**

---

# 3. Material state versus technical revision

Not every persistence change is a material domain revision.

Example:

```text
Schedule
15:00
label: "Project review"
```

A spelling/capitalization correction may cause a database update, a new API ETag or a provider revision while leaving the semantic state relevant to an Acknowledgement unchanged.

Therefore:

```text
technical revision
!= material domain revision
```

Canonical rule:

> **LifeOS material-state semantics must not be derived solely from database-write count, `updated_at`, row version, ETag, MVCC token, provider revision identifier or content hash.**

Those mechanisms may support implementation integrity later; they do not define semantic materiality.

---

# 4. Materiality is purpose-specific

Material equivalence is not universally object-wide.

A change may be material for one semantic relation and irrelevant for another.

Example:

```text
Event
Schedule changes 15:00 -> 16:00
```

This may be material for:

- Acknowledgement of the changed time;
- Participation response where availability depends on the time;
- Schedule-specific Decision/Approval.

It may be irrelevant to:

- a previously confirmed Event title;
- Consent covering an unrelated bounded image use;
- another independent relationship attached to the Event.

Likewise a private source note may change while an authorized free/busy projection remains semantically identical.

Canonical rule:

> **Material equivalence is evaluated relative to the owning semantic purpose, target facet/scope and consequence; LifeOS must not reduce it to one universal `material_changed=true` flag for the entire object.**

---

# 5. State binding

Where another semantic fact depends on a particular target state, the binding must remain reconstructible.

Examples:

```text
Ack A1 -> Schedule state S1
Confirmation C1 -> Observation state O1
Agreement G1 -> terms state T1
Consent C2 -> scope/purpose state P1
Decision D1 -> proposal state P4
Evidence E1 -> source/rule states used by evaluation
```

This does not require every relationship to expose a visible version number or every API to carry a universal `version_id` field.

Canonical rule:

> **State binding is semantic; exact persistence can be direct, derived or qualified as long as material historical applicability remains losslessly reconstructible.**

---

# 6. Acknowledgement and Confirmation

Acknowledgement already requires explicit recognition of a specific target/material version/change.

Confirmation already binds an attestation to a specific target/version.

Version v0 closes the common deferred question:

```text
Ack(v1)
materially changed target v2
→ Ack(v1) remains historical
→ no automatic Ack(v2)
```

and:

```text
Confirmation(v1)
materially changed target v2
→ Confirmation(v1) remains historical
→ no automatic Confirmation(v2)
```

A non-material change for the relevant purpose may preserve applicability without fabricating a new human action.

```text
Version != Acknowledgement
Version != Confirmation
```

---

# 7. Agreement and Consent

Agreement requires materially aligned terms among applicable parties.

Consent is bounded by action/use/exposure, target, scope, purpose and context.

Version v0 makes their amendment rules reusable:

```text
Agreement terms v1
price = EUR 100

terms v2
price = EUR 120
```

Prior Agreement does not silently apply to materially changed terms.

Similarly:

```text
Consent v1
use free/busy
purpose Trip A coordination

scope/purpose v2
use full calendar history
purpose unrelated AI training
```

does not inherit Consent v1.

A formatting or non-material presentation change may remain equivalent for the relevant assent/permission purpose.

```text
Version != Agreement
Version != Consent
```

---

# 8. Participation and Responsibility workflows

Participation response may concern a materially specific invitation, occurrence or shared-event state.

```text
accepted at 15:00
```

must not automatically become:

```text
accepted at 23:00 after material reschedule
```

Responsibility hand-off behaves similarly:

```text
handoff request v1
scope A
```

may receive a response that does not apply to:

```text
handoff request v2
scope A + materially different duties
```

Canonical rule:

> **Family-specific responses bind to the materially relevant request/participation state they concerned; a later material change requires the owning family/policy to determine renewed response or continued applicability.**

Version does not create a generic Acceptance primitive.

---

# 9. Decision, Approval and Authority

Decision records a bounded resolution. Authority records who/what may legitimately make a bounded effect effective.

Version identifies which target/proposal/rule state those semantics concerned.

```text
Decision D1 approves Proposal P4
Proposal materially revised to P5
```

does not mean:

```text
P5 is approved by D1
```

Likewise a historical Authority basis may depend on a materially specific policy/scope state.

```text
Version != Decision
Version != Approval
Version != Authority
```

Version does not determine whether a state is canonical or effective; the owning domain semantics plus applicable Authority/Decision/policy do that.

---

# 10. Actual, Observation and Outcome correction

A correction may preserve target identity while producing a materially different state.

Example:

```text
Observation O17 v1
76.4 kg

Correction
Observation O17 v2
66.4 kg
```

A previous Confirmation/Evidence evaluation may remain correctly bound to v1 historically even though the current Observation state is v2.

Likewise Actual or Outcome may be corrected after later authoritative information arrives.

Canonical rule:

> **Current corrected state must not falsify which material state existed or was used earlier.**

Version does not decide which conflicting assertion should become current; reconciliation/Authority/Decision own that question.

---

# 11. Evidence and evaluation history

Evidence is contextual evaluative use. Historical evaluation can become false to history if source or rule updates are treated as though they always existed.

Example:

```text
Evaluation E1 at T1
source Observation O-v1
criterion/rule R-v1
result = satisfied

later
Observation corrected to O-v2
rule changed to R-v2
```

A current evaluation may use O-v2/R-v2 while historical E1 must remain explainable under O-v1/R-v1 where consequence requires it.

Canonical rule:

> **Material evaluation history must bind to or reconstruct the material source/rule states actually used at evaluation time.**

This does not require every transient query aggregate to become a persisted Version object.

---

# 12. Provenance boundary

Provenance answers:

> how did this record/material state come to exist or change?

Version answers:

> which materially relevant state are we referring to, and what later state is equivalent for this purpose?

Therefore:

```text
Version != Provenance
```

Provenance may explain that:

```text
state v2
was derived/corrected from v1
by Actor A
using source B
```

without Version becoming lineage itself.

A Version/material state may have Provenance.

---

# 13. Routine / Recurrence / Occurrence

Effective future policy changes must not rewrite the rule under which earlier Occurrences existed.

Example:

```text
Routine / Recurrence state v1
Mon/Wed/Fri 18:00

Occurrence O1 generated under v1
Occurrence O2 generated under v1

later policy state v2
future Wednesday -> 20:00
```

O1/O2 remain explainable under v1. Future candidate Occurrences may derive from v2 according to the applicable effective boundary.

Canonical rule:

> **An Occurrence must retain enough source/material-state context to explain which recurring/generative policy governed its existence when that distinction matters.**

A one-off Occurrence exception remains distinct from a source-policy Version change.

---

# 14. Schedule revisions

Schedule already requires reconstructible accepted-placement history.

Version v0 does not replace Schedule history; it supplies the general state discipline used by consumers of Schedule state.

```text
Schedule S1 15:00
Schedule S2 16:00
Actual 16:12
```

must remain distinguishable.

A consumer may bind to S1, S2 or another material facet without using Actual as a replacement Version.

```text
Version != Schedule
Version != Actual
```

---

# 15. Milestone redefinition and identity guard

Milestone target dates, labels and supporting Evidence may change while checkpoint identity survives.

But a materially redefined checkpoint may cross the identity boundary.

Example:

```text
Milestone
B1 reached
```

changed into:

```text
Milestone
C1 reached
```

is not automatically `Milestone v2`.

Canonical rule:

> **Version can represent revision only while the owning concept's identity remains coherent. Materiality is not a license to preserve identity through semantic replacement.**

---

# 16. Concurrent and divergent states

LifeOS must not assume all material history is one clean linear edit chain.

Example:

```text
Base state S1

Actor A offline -> state S2A
Actor B/provider -> state S2B
```

Both may be historically real states derived from S1.

The system must not silently claim that the later received write superseded the other merely because of arrival order.

Canonical rule:

> **Version/material-state semantics must permit concurrent or divergent states where reality produces them; no universal last-write-wins or globally linear history invariant is accepted.**

Whether states are merged, one becomes current, both remain unresolved, or specialist authority decides is a reconciliation/policy question.

---

# 17. Provider versions and synchronization

External providers may expose:

- revision IDs;
- sequence numbers;
- ETags;
- sync tokens;
- timestamps;
- provider history identifiers.

These are integration/provenance/concurrency inputs.

```text
provider revision
!= LifeOS material-state identity automatically
```

One provider revision may contain no semantic change relevant to LifeOS. Conversely, several provider-level changes may collectively produce one LifeOS material change.

Provider identifiers may be retained for reconciliation/mapping without becoming native LifeOS Version identity.

---

# 18. Technical concurrency boundary

HTTP conditional requests, ETags, database row versions and MVCC may later help prevent stale writes or lost updates.

They answer a technical question such as:

> is this write based on the storage representation I expect?

Version/material equivalence answers a semantic question:

> does the human/domain action still apply to the materially relevant state?

Therefore:

```text
optimistic-lock token != semantic Version
```

A future API may carry both technical concurrency and domain-state references where needed.

No physical strategy is selected here.

---

# 19. AI / automated-change boundary

AI may:

- compare material states;
- summarize changes;
- propose a change against a known base state;
- identify likely material differences;
- ask for renewed Acknowledgement/Agreement/Consent/Approval where required;
- support reconciliation without deciding it unless authorized policy permits.

AI must not:

- apply a stale-base proposal blindly after the target materially changed;
- infer that prior human assent/permission/acknowledgement transfers to a materially different state;
- use content similarity/hash equality as universal material-equivalence proof;
- hide a concurrent divergent state to create false certainty;
- leak hidden source changes while explaining why an exposed projection changed or did not change.

Canonical rule:

> **Where material, an AI/system proposal or action must preserve the base state it reasoned against and re-evaluate applicability if that state diverges before effect.**

---

# 20. Visibility and privacy of history

Current target Visibility does not automatically expose full Version history.

```text
visible current projection
!= visible historical source states
!= visible change rationale
!= visible actor/provenance chain
```

Likewise a recipient may legitimately see that a shared result changed without seeing the private source difference that caused it.

Canonical rule:

> **Version/history Visibility is independently governed; material-state history must not become a privacy bypass.**

---

# 21. Retention / deletion / redaction

Historical reconstructibility does not require indefinite retention of every sensitive payload.

Privacy/retention policy may require:

- deletion;
- anonymization;
- redaction;
- tombstone/minimal historical reference;
- specialist-source retention instead of LifeOS payload duplication.

Version v0 requires semantic integrity, not a backdoor archive.

Canonical rule:

> **A durable reference that a prior material state existed does not by itself justify retaining the full sensitive contents of that state forever.**

Exact retention classes remain downstream privacy/logical-model work.

---

# 22. Simple UI versus kernel precision

Ordinary users should usually see natural change/history language:

```text
Changed from 15:00 to 16:00
Updated terms
Changed after you confirmed
Review changes
Restore previous value
```

rather than ontology terminology or version numbers.

High-consequence/power-user flows may expose:

- state/revision identifier where useful;
- material changes;
- who/what acted;
- semantic actions bound to an earlier state;
- conflicting versions;
- effective periods;
- history/provenance.

Kernel precision must not create routine version-management bureaucracy.

---

# 23. External benchmark disposition

External standards/products are evidence, not design authority.

Current benchmark conclusions:

```text
HL7 FHIR technical record version vs business version separation
→ BORROW / boundary evidence

FHIR rule that server meta.versionId changes on resource update
→ ANTI-PATTERN if treated as LifeOS semantic materiality

W3C PROV revision relationship / revision lineage
→ ADAPT

W3C PROV as complete LifeOS Version ontology
→ NOT APPLICABLE

HTTP ETag / If-Match stale-write protection
→ ADAPT for future technical concurrency

ETag as LifeOS domain material Version
→ NOT APPLICABLE

Git reconstructible snapshots / parent history
→ ADAPT as history evidence

Git-style universal commit DAG for every LifeOS object
→ ANTI-PATTERN
```

A strong external lesson is consistent across domains: **technical revision, business/domain revision, identity, lineage and concurrency are related but not identical concerns.**

---

# 24. Core invariants

1. **Version / Material-State is a cross-cutting semantic capability/discipline, not native identity/root.**
2. **Target identity != target material state.**
3. **A new material state does not automatically mean a new target identity.**
4. **Version cannot preserve identity after the owning concept's identity invariants fail.**
5. **Not every persistence write is a material domain revision.**
6. **Technical record version != semantic material Version.**
7. **Provider revision != LifeOS material Version automatically.**
8. **ETag/MVCC/optimistic-lock token != semantic material Version.**
9. **Content/hash equality != universal material equivalence.**
10. **Materiality is purpose/family/facet scoped where necessary.**
11. **An irrelevant facet change must not invalidate unrelated semantic actions automatically.**
12. **Semantic actions/evaluations bind to the material target state they actually concerned where consequence requires it.**
13. **A material change does not inherit prior Acknowledgement, Confirmation, Agreement, Consent, Decision, family-specific response or equivalent semantic state by default.**
14. **A non-material equivalent change may preserve applicability without fabricating a new human action.**
15. **Current state != historical state.**
16. **Version != Provenance.**
17. **Version != Decision / Approval / Authority.**
18. **Version != reconciliation/source precedence.**
19. **Version history need not be universally linear.**
20. **Version identifiers need not encode chronological or semantic ordering.**
21. **The owning domain + applicable Authority/Decision/policy owns current/effective-state selection.**
22. **Projection Version/materiality != hidden source Version/materiality automatically.**
23. **Material evaluation history may require source/rule state binding.**
24. **AI proposals/actions preserve their material base state where consequence requires it.**
25. **Stale-base AI/system changes must be re-evaluated after material divergence.**
26. **Version/history Visibility is independently governed.**
27. **Historical integrity does not justify indefinite sensitive-payload retention.**
28. **Snapshots/deltas/event sourcing/effective-dated rows remain physical choices.**
29. **No universal `versions` table, polymorphic Version root or event-sourcing mandate is pre-approved.**
30. **Version persistence/formality is consequence-sensitive.**

---

# 25. Rejected alternatives

Rejected:

```text
universal Version entity/root
global Version superclass for every domain object
one semantic version integer on every record
every database write = new material Version
updated_at = Version
ETag/MVCC token = domain Version
provider revision = LifeOS Version
content hash = material equivalence
one global material_changed flag
universal strictly linear history
universal last-write-wins
Version = Provenance
Version = Decision
Version = Authority
Version = reconciliation
Version = Audit log
mandatory event sourcing
mandatory snapshot row for every change
full historical payload retained forever
AI similarity = material-equivalence proof
```

---

# 26. Adjacent Dependency Sweep

## RESOLVED

- Version ↔ target identity: target continuity and state continuity are distinct.
- Version ↔ technical revision: storage revision does not define semantic materiality.
- Version ↔ provider revision: external revision is mapping/provenance input, not native semantic identity.
- Version ↔ ETag/MVCC: concurrency support != domain state semantics.
- material equivalence ↔ hash/content equality: similarity/equality is insufficient as a universal semantic rule.
- Version ↔ Provenance: state reference != lineage.
- Version ↔ Decision/Approval: state identification != resolution.
- Version ↔ Authority: state identification != legitimate governance power.
- Version ↔ reconciliation: identifying divergence != selecting/merging current interpretation.
- Acknowledgement/Confirmation target binding: exact material state can remain reconstructible.
- Agreement/Consent applicability: assent/permission remains bound to material terms/scope/purpose.
- Participation/Responsibility response applicability: response remains tied to the materially relevant request/state.
- Evidence historical basis: evaluation may bind to source/rule state without duplicating source truth.
- Routine/Recurrence/Occurrence policy history: prior Occurrences remain attributable to prior governing state.
- Schedule revision history: historical/current placements remain distinguishable.
- Milestone Version vs identity replacement: Version applies only while Milestone identity remains coherent.

## SAFE DEFERRED

### Per-family material-equivalence rules

**Owner:** owning concept/product policy + logical model.  
**Why safe:** Version v0 fixes purpose-specific materiality and forbids global equality shortcuts.  
**Reopening trigger:** a family cannot determine whether prior semantic state remains applicable after change without changing Version semantics.  
**Tests:** CORE-02/04/09/13, MA-05/06/11/12/17, XCON-03/04.

### Branch / merge / source-precedence mechanics

**Owner:** reconciliation + logical model.  
**Why safe:** divergent states can coexist without universal last-write-wins; Version need not decide the winner.  
**Reopening trigger:** concurrent/offline/provider conflicts cannot be reconstructed without collapsing Version into reconciliation.  
**Tests:** CORE-02/09/10/13, MA-06/11/12/17/18, XCON-02/03.

### Exact effective dating

**Owner:** Time + logical model.  
**Why safe:** action-time/current/history distinctions are canonical while storage remains open.  
**Reopening trigger:** system cannot determine which material state governed an action/evaluation at time T.  
**Tests:** CORE-02/09/13, MA-11, XCON-03.

### Provider version mapping

**Owner:** integration + Provenance.  
**Why safe:** provider IDs are explicitly non-authoritative for LifeOS identity/materiality.  
**Reopening trigger:** provider synchronization cannot avoid false duplicate/overwrite without changing native Version identity.  
**Tests:** CORE-02/09/10/13, MA-09/12/18, XCON-01/03.

### Retention / deletion / tombstone / redaction

**Owner:** privacy/retention/logical model.  
**Why safe:** semantic history does not mandate payload retention.  
**Reopening trigger:** required historical applicability cannot coexist with deletion/minimization requirements.  
**Tests:** CORE-02/09/10, MA-07/08/11/13, XCON-03.

### Versioned evaluation / rule snapshots

**Owner:** GoalCriterion / Trigger / evaluation reasoning.  
**Why safe:** source/rule state binding is required only where historical reproducibility matters.  
**Reopening trigger:** evaluation history cannot be explained without a stronger universal rule-Version primitive.  
**Tests:** CORE-02/04/09/10/13, MA-17/18, XCON-03/04.

### Identity-replacement threshold

**Owner:** each native/contextual concept.  
**Why safe:** Version explicitly defers continuity to owning identity invariants.  
**Reopening trigger:** ordinary workflows cannot decide revision-vs-replacement locally without a common stronger identity transition concept.  
**Tests:** CORE-03/04/06/09, XCON-01/03/04.

```text
REOPEN                         0
unclassified material items    0
```

---

# 27. Persistence / API implications without physical commitment

Future logical modeling must be able, where material, to support combinations of:

- stable target identity;
- material-state reference or reconstructible state key;
- semantic action/evaluation bound to that state;
- current versus historical state;
- effective/recorded/revision timing where relevant;
- correction/supersession/replacement distinction;
- concurrent/divergent states;
- state Provenance;
- provider mapping;
- independent Visibility/retention;
- technical concurrency validator separately where needed.

This review does **not** pre-approve:

```text
versions table
version_id on every table
universal polymorphic version_target JSON
monotonic integer version
immutable snapshot per write
event sourcing
CRDT
last-write-wins
Git-like DAG
universal effective_from/effective_to on every record
one ETag shared with domain semantics
```

Implementation must preserve semantics without forcing one storage mechanism across unrelated domains.

---

# 28. Reopening triggers

Reopen Version / Material-State v0 if later evidence shows that:

1. semantic state binding is fully reducible to Provenance/current-record history without information loss or duplicated per-family mechanisms;
2. purpose-specific materiality cannot be represented without one stronger common equivalence concept;
3. target identity and Version cannot remain separated in ordinary LifeOS workflows;
4. concurrent/offline/provider divergence requires Version itself to own reconciliation/merge semantics;
5. privacy/retention makes required historical applicability impossible without changing the semantic contract;
6. whole-domain regression shows that Version introduces more cross-cutting complexity than independently owned revision semantics;
7. logical/persistence pressure proves that direct/derived/qualified state references cannot preserve the accepted invariants.

Vocabulary or database convenience alone is never sufficient reason to reopen.

---

# 29. Current validation position

Normative validation checkpoint:

- `../checkpoints/version-material-equivalence-v0-validation.md`

Read-only V3 result before this write:

```text
VERSION / MATERIAL EQUIVALENCE v0
PASS WITH HARDENING

CORE gate                       PASS WITH HARDENING
Multi-Actor gate                PASS WITH HARDENING
Cross-Concept gate              PASS WITH HARDENING
REOPEN                          0
unclassified material items     0
```

The hardenings above are incorporated into this candidate baseline. Canonical acceptance still depends on completing the approved documentation propagation and post-write QA against pre-scope commit `1008aeb0367de4ae73a8e8d41a76aee9e0493f34`.
