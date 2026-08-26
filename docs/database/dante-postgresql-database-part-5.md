# DANTE PostgreSQL Database — Architecture, Reference & Whole-Database Blueprint — Part 5

- **Status:** CP6-03 ACTIVE / CANONICAL CONTINUATION / GATE 03 NOT YET EARNED
- **Created:** 2026-08-23
- **Product:** DANTE
- **Database:** PostgreSQL 18 major family
- **Current repository patch:** PostgreSQL 18.6
- **Schema:** `dante`
- **Workstream:** `../workstreams/logical-postgresql.md`
- **Database documentation authority:** `README.md`
- **Part 1:** `dante-postgresql-database.md` — sections 1–30
- **Part 2:** `dante-postgresql-database-part-2.md` — section 31
- **Part 3:** `dante-postgresql-database-part-3.md` — section 32
- **Part 4:** `dante-postgresql-database-part-4.md` — section 33
- **Continuation numbering:** section 34 onward
- **Continuation anchor:** `bf19c1aed6ff45dba294815bcc75754d58d5dadb`
- **Implementation status:** business schema / business SQLAlchemy mappings / product vertical **NOT YET MATERIALIZED**

---

## Canonical continuity contract

This file is the canonical continuation of Parts 1–4. It does not replace, summarize or supersede any prior part as a whole.

```text
dante-postgresql-database.md
PART 1 / sections 1–30
+

dante-postgresql-database-part-2.md
PART 2 / section 31
+

dante-postgresql-database-part-3.md
PART 3 / section 32
+

dante-postgresql-database-part-4.md
PART 4 / section 33
+

dante-postgresql-database-part-5.md
PART 5 / section 34 onward
=

ONE CANONICAL HUMAN-READABLE
DANTE DATABASE ARCHITECTURE & REFERENCE
```

Readers, reviewers, migration planning, SQLAlchemy mapping review, Database Dictionary reconciliation, generated-reference checks, direct PostgreSQL proof planning and Gate-03 review MUST consume all active parts.

The preservation, no-summary, explicit-supersession and whole-database cumulative-audit rules already established remain fully applicable.

---

## 34. Consolidation checkpoint G — Agreement baseline disposition

### 34.1 Scope and authority

This checkpoint closes the final exact local CP6-03 blocker:

```text
AGR-U01
```

The decision is derived from the complete accumulated authority, including:

```text
Agreement / Consent Domain v0
Agreement / Consent validation checkpoint
Collective / Membership Agreement continuation
Representation / on-behalf-of downstream closure
Version / Material-State downstream closure
Logical Slice F — Relationships / Multi-Actor / Governance
Whole-Logical 57/57 representation model
CP6-01 persistence coverage Part 1 + Part 2
accepted PostgreSQL Physical mapping
CP6-02 Persistence Constitution / ADR-010
Part 1 sections 1–30, especially sections 25 and 26
Part 2 section 31
Part 3 section 32
Part 4 section 33
real CP3 PostgreSQL/Alembic/SQLAlchemy foundation
```

This checkpoint is physical/database closure only. It does not redefine Agreement semantics and does not introduce a Contract engine, a universal Assent root or generic terms payload.

The decisive semantic facts are:

```text
Agreement
= contextual multi-party mutual assent
  to the same materially specific terms/version
  in a bounded context

Agreement
!= Acknowledgement
!= one Actor's positive response
!= Decision
!= Authority
!= Responsibility
!= Consent
!= legal Contract
!= compliance
!= Actual
```

Agreement is consequence-sensitive: simple/low-consequence interaction need not become a durable independently addressable Agreement record merely because a user-facing flow says “agree”.

### 34.2 Why Agreement survives semantically

Agreement remains a necessary semantic capability because there are valid states that cannot be represented faithfully by existing neighboring concepts.

Examples:

```text
Anna and Luca assent to the same shift-swap terms
manager approval is still pending
→ Agreement exists
→ effective state change does not yet exist
```

```text
manager makes an authoritative Decision
one worker disagrees
→ Decision may exist
→ Agreement does not
```

```text
client and photographer agree on delivery terms
image-use Consent remains absent or narrower
→ Agreement exists
→ Consent remains independently evaluated
```

Removing Agreement would force incorrect collapse into response state, Decision, Authority, Responsibility, Consent or specialist Contract semantics.

Therefore this checkpoint does not remove Agreement from Domain/Logical authority.

### 34.3 Agreement is not an LR-01 native owner

Agreement remains LR-02 contextual n-ary semantics.

```text
Agreement
!= NativeRef owner
```

The accepted LR-01 native-owner count remains exactly 15.

A consequential Agreement may become independently addressable through a concrete ScopedRecordRef when the Agreement itself has material lifecycle/history/reference pressure.

A trivial low-consequence interaction may remain direct/derived or owned by the concrete response/workflow family when no independently reconstructible Agreement is required.

No universal Agreement identity is minted merely because a product button is labelled “Agree”.

### 34.4 Existing Part-1 topology — valid future contract, not baseline authorization

Part 1 correctly derived the topology required by a consequential material Agreement:

```text
Agreement contextual record
+
exact terms MaterialStateRef
+
N party-assent relations
```

Conceptually:

```text
Agreement A1
terms -> T1
party P1 -> assent to T1
party P2 -> assent to T1
...
```

This topology is retained as the future material Agreement contract.

However, the cumulative audit finds that the topology alone is insufficient to authorize baseline CP6-04 DDL because current accepted authority does not provide a bounded generic terms-bearing owner/facet contract that can safely populate `terms_material_state_ref`.

### 34.5 AGR-U01 — CLOSED with NO CP6 baseline Agreement DDL

The final baseline disposition is:

```text
AGR-U01
CLOSED

CP6-04 BASELINE AGREEMENT BUSINESS OBJECTS
0
```

CP6-04 MUST NOT create generic objects equivalent to:

```text
dante.agreement
dante.agreement_shared_assent_state
dante.agreement_party_assent
agreement scoped-address family
agreement.shared_assent MaterialState facet
agreement current-history table
generic Agreement current view
```

This is a final baseline non-materialization decision, not an unresolved TODO.

The first real consequential Agreement profile becomes an explicit future schema-evolution trigger.

### 34.6 Narrow supersession of Part 1

This checkpoint supersedes only the earlier **baseline materialization authorization** implied by Part 1 for:

```text
dante.agreement
dante.agreement_shared_assent_state
dante.agreement_party_assent
agreement scoped_address registration
agreement.shared_assent MaterialState registration
```

It does **not** supersede the valid future semantic/physical invariants already derived there:

```text
n-ary shared terms topology
same exact terms basis for all parties
material amendment requires new applicable assent
historical prior assent retained
Person / true Collective party support
party != actual representative Actor
Agreement != Consent / Decision / Authority / Actual
```

Part 1 remains canonical history of that derivation; section 34 narrows only what CP6-04 baseline may materialize.

### 34.7 The missing baseline fact: exact terms-bearing owner/facet eligibility

Part 1 correctly rejected the interpretation:

```text
terms_material_state_ref
→ any MaterialStateRef in DANTE
```

A MaterialStateRef proves one exact material semantic state exists. It does not prove that the state is meaningful as Agreement terms.

A concrete Agreement profile must define a bounded Reference Contract equivalent to:

```text
terms_material_state_ref
→ MaterialStateRef exists
→ owner/facet belongs to the explicit admitted terms-bearing set
```

Current accepted authority does not define one universal admitted set.

Therefore a baseline generic FK only to `material_state_address(material_state_ref)` would be structurally valid SQL but semantically invalid DANTE persistence.

### 34.8 No invented generic Agreement terms owner

CP6 MUST NOT solve the missing terms owner by inventing:

```text
dante.agreement_terms
dante.terms
dante.contract_terms
TermsRef
ContractRef
terms_payload jsonb
terms_text as universal canonical meaning
```

A future Agreement may bind terms expressed by a concrete typed state already owned by another bounded family, or by a future specialist profile that genuinely owns its terms semantics.

The first concrete profile decides that from real product/domain authority.

### 34.9 Candidate future terms-bearing families are not pre-authorized

Possible future contexts may include materially versioned states such as:

```text
a concrete Proposal profile
a concrete Content Artifact revision
service/delivery terms
coordination arrangement terms
specialist contractual/document terms
another accepted bounded terms-bearing family
```

These are examples of future pressure only.

This checkpoint does NOT pre-authorize any of them as a universal Agreement terms source.

Each real Agreement vertical must list its admitted owner/facet set explicitly and database-enforce eligibility.

### 34.10 Same materially specific terms is the central invariant

Agreement means the applicable parties assented to the same materially specific terms state.

Valid conceptual state:

```text
P1 assents to T1
P2 assents to T1
→ shared Agreement may be established
```

Invalid shared state:

```text
P1 assents to T1
P2 assents to T2
where T1 and T2 are materially different
→ no shared Agreement
```

A future physical Agreement profile MUST make it impossible to manufacture one shared Agreement state whose party rows refer to materially different terms bases.

The preferred topology continues to own the terms basis once at the shared Agreement material state rather than duplicating terms refs independently on each party row.

### 34.11 Minimum applicable party cardinality

A shared Agreement requires at least two distinct applicable parties.

Future consequential material Agreement contract:

```text
party count >= 2
```

A composite PK or unique key must reject duplicate party rows.

The exact database mechanism that proves `>= 2` by COMMIT may use a narrow deferred trigger/constraint function because ordinary row-local CHECK cannot count sibling rows.

No one-party `Agreement` row is accepted merely because the same storage shape could support it.

One-party bounded permission remains Consent or another family-specific declaration where applicable, not Agreement.

### 34.12 Applicable party set is profile-owned

Agreement requires an applicable party set, but CP6 does not invent a universal quorum engine.

Future profile must determine whether parties are:

```text
explicitly enumerated
policy-derived under a concrete bounded rule
true Collective party/parties
another accepted profile-specific set
```

No universal fields are introduced today for:

```text
quorum_count
majority_percent
unanimous boolean
vote_weight
party_group_id
```

Collective governance/quorum semantics remain separate and are introduced only when a concrete profile requires them.

### 34.13 Person and true Collective remain valid party families

The accepted future Agreement party contract retains:

```text
Person
Collective
```

as valid native party families where the concrete profile permits them.

A true Collective may be an Agreement party.

```text
Collective C
→ party to Agreement A
```

This does not expand C into current members and does not require every member to be a personal Agreement party.

### 34.14 Agreement party set != Collective identity

Multiple people agreeing to the same terms do not become a Collective merely because cardinality is greater than one.

Conversely:

```text
Collective party
!= set of all current members
```

The database must not infer Collective identity from Agreement party rows or infer Agreement party rows from Membership.

### 34.15 Member assent != Collective assent automatically

Canonical boundary:

```text
member assent
!= Collective assent automatically
```

Where a Collective is the true Agreement party, the concrete governance profile must define how a legitimate Collective action/assent becomes effective for that Collective.

That may involve Decision, Authority, Representation or another bounded governance basis.

CP6 does not universalize this into Agreement itself.

### 34.16 Collective Agreement != every member personally agreed

A valid future state may be:

```text
Collective C is Agreement party
```

without asserting:

```text
every Person member of C personally assented
```

The reverse is also not automatic.

This distinction must remain query-visible and historically reconstructible where the concrete profile materializes Agreement.

### 34.17 Silence, delivery, read state and Acknowledgement do not establish Agreement

Forbidden derivations:

```text
message delivered
→ Agreement

message read
→ Agreement

Acknowledgement exists
→ Agreement

no objection observed
→ Agreement
```

A future material Agreement profile must consume explicit assent semantics from the concrete workflow.

No baseline generic `accepted = true` field is introduced.

### 34.18 One Actor's positive response != multi-party Agreement

Family-specific positive response remains owned by the relevant family.

Examples:

```text
Participation accepted
Responsibility hand-off accepted
Proposal response accepted
```

A single positive response may contribute Evidence/basis toward a future Agreement profile, but does not itself establish mutual Agreement among all applicable parties.

No generic cross-domain Acceptance/Assent root is introduced.

### 34.19 Agreement != Decision

Agreement answers:

```text
which parties mutually assented to which materially specific terms?
```

Decision answers:

```text
which bounded question was resolved to what result?
```

A future database must permit:

```text
Agreement exists
Decision/effective approval absent
```

and:

```text
Decision exists
Agreement absent
```

No Agreement row may be inferred from Decision existence or result code.

### 34.20 Agreement != Authority

Mutual assent does not manufacture governance power.

```text
Agreement
!= Authority
```

A concrete effect may require Agreement as one basis plus separate Authority.

The governed-effect/provenance profile may reference the exact Agreement MaterialStateRef where consequence requires it, but Agreement does not become an authorization decision.

### 34.21 Agreement != Responsibility / resulting domain state

Agreement terms may establish or influence Responsibility, Schedule, allocation or other domain state.

Those resulting states remain owned by their concrete semantic families.

```text
Agreement terms
→ may be basis for effect

Agreement
!= resulting Responsibility
!= Schedule
!= Allocation
```

A future Agreement implementation must not duplicate resulting state as generic Agreement status/payload.

### 34.22 Agreement != Consent

Agreement is shared mutual terms semantics.

Consent is actor-scoped bounded permission.

```text
Agreement != Consent
```

A service Agreement can exist while image/data-use Consent is absent or narrower.

A unilateral Consent can exist without reciprocal Agreement.

No common generic `permission/assent` table is introduced to merge them.

### 34.23 Agreement != legal Contract

DANTE Agreement does not claim:

```text
legal enforceability
signature validity
jurisdictional validity
witness validity
contract-law status
capacity determination
```

Formal Contract/signature/legal lifecycle remains specialist integration/vertical work.

No baseline Agreement table may carry universal columns such as:

```text
legally_binding
signed_at
jurisdiction_code
enforceable
contract_status
```

### 34.24 Agreement != compliance / Actual

Agreement records shared assent, not what later happened.

```text
Agreement exists
!= obligations performed
!= scheduled work completed
!= Actual occurred
!= Outcome succeeded
```

A party may agree and later fail to perform.

Truthful Actual/Outcome history remains independently recorded.

### 34.25 Material amendment does not inherit prior Agreement

Canonical chronology:

```text
T1 terms state
P1/P2 assent
Agreement A(T1)

materially changed T2 terms
→ A(T1) remains historical
→ prior assent does not silently apply to T2
→ T2 requires renewed applicable assent
```

A future concrete profile must retain exact T1 basis and cannot implement amendment by mutating the terms pointer of the historical Agreement state.

### 34.26 Material equivalence is semantic, not technical revision equality

Agreement applicability depends on material terms meaning, not arbitrary storage revision.

Forbidden universal equivalence tests:

```text
same owner UUID
→ same terms

same provider revision
→ same terms

same ETag/hash
→ same terms

same content bytes
→ necessarily same Agreement meaning

new row
→ necessarily material Agreement amendment
```

A concrete terms-bearing family owns the definition of material equivalence for the Agreement purpose.

### 34.27 No universal terms hash

CP6 does not introduce:

```text
terms_hash
agreement_hash
material_equivalence_hash
```

as semantic truth.

Hashes may later assist technical deduplication/integrity under a concrete profile, but they do not decide whether an Agreement still applies after a change.

### 34.28 No universal Agreement lifecycle/status enum

Domain recognizes that an Agreement may later be amended, superseded, terminated, fulfilled, breached, disputed or rendered irrelevant.

Those are not accepted as one universal Agreement state machine.

CP6 MUST NOT introduce:

```text
agreement_status
active
terminated
fulfilled
breached
disputed
superseded
```

as a global enum merely to appear complete.

Concrete profiles own any lifecycle semantics they genuinely require.

### 34.29 Current no Agreement != Agreement never existed

The non-destructive history rule remains mandatory.

```text
no currently applicable Agreement
!= no historical Agreement ever existed
```

A future material Agreement profile must preserve historical exact terms/party assent basis after later cessation, termination, supersession or dispute where policy allows retention.

No historical Agreement state is overwritten into “inactive”.

### 34.30 Actual Actor != represented Agreement party

On-behalf-of assent requires three concepts to remain distinct:

```text
Agreement party
= party whose assent is required

actual Actor
= who actually performed the assent action

Representation / basis
= why/how that Actor acted for a distinct represented party
```

Example:

```text
Luca acts for Anna
Anna is the Agreement party
Luca is the actual Actor
```

Forbidden rewrite:

```text
party_native_ref = Luca
```

merely because Luca executed the action.

### 34.31 Representation does not prove Authority

A Representation record/action context describes acting on behalf of another referent.

It does not by row existence prove the Actor had Authority to make the assent effective for the represented party.

A consequential Agreement profile must preserve the applicable basis separately when that distinction is material.

```text
Representation
!= Authority
```

### 34.32 Principal / Account do not become Agreement party identity

Party identity remains domain identity/reference.

```text
Person != Account != Principal != Actor != Agreement party
```

A party may have no DANTE Account.

A technical Principal may perform an authenticated operation without becoming the semantic Agreement party.

Future provenance may retain Principal/security context when useful, but it does not replace party or Actor semantics.

### 34.33 No generic mandatory actor column on party rows

Part 1 correctly refused to add:

```text
actor_native_ref NOT NULL
```

merely to close AGR-U01.

The future profile must determine how assent actions are represented.

Possible concrete shapes may bind:

```text
party
actual Actor
represented party
Representation/Authority basis
recorded chronology
source/provenance
```

but only the real assent-action profile may decide which fields are mandatory and which reference families are admitted.

### 34.34 Provenance remains bounded and typed

Consequential Agreement assent must be able to preserve/reconstruct enough provenance to explain the accepted shared state.

Applicable future facts may include:

```text
actual Actor
represented party
Authority / Representation basis
recorded/accepted chronology
source artifact/state
proposal/terms state
operation correlation/idempotency where relevant
```

This does not authorize one universal Provenance graph or generic operation/event ontology.

The concrete Agreement profile consumes the existing bounded provenance doctrine.

### 34.35 Recorded chronology vs world/effective chronology

A future material Agreement may need to distinguish:

```text
when assent was performed/recorded
when the shared Agreement became applicable/effective
when a revision ceased to apply
```

Those axes are profile-specific.

CP6 does not introduce universal Agreement timestamps such as:

```text
agreed_at
valid_from
valid_until
terminated_at
```

without a concrete Agreement profile defining their exact meaning.

### 34.36 Agreement Visibility remains separate

Agreement existence, terms, party identities, private negotiation Evidence and provenance may have different Visibility.

```text
visible final Agreement
!= visible all private negotiation history
!= visible every supporting Evidence item
```

Agreement does not create blanket re-disclosure Authority.

A future material profile must declare its exact disclosure/query surfaces and applicable Visibility basis.

### 34.37 AI may propose, compare or summarize; it may not fabricate assent

AI may assist future Agreement workflows by:

```text
proposing terms
comparing terms versions
identifying mismatched responses
summarizing an authorized recorded Agreement
surfacing parties still requiring assent
```

AI must not:

```text
infer human Agreement from silence/behavior/probability
fabricate assent
expand a party's assent to changed terms
turn recommendation into Agreement
expose private negotiation merely because final Agreement is visible
```

No inferred/probabilistic Agreement row is accepted as canonical truth.

### 34.38 Why no baseline generic Agreement is the maximum non-speculative result

The accumulated design already determines **how** a consequential Agreement must behave, but not **which terms-bearing profile** exists in the CP6 baseline.

The missing fact is not a minor column-name choice.

It determines:

```text
terms ownership
terms type/shape
material equivalence
eligible party set
assent-action semantics
Representation/Authority basis
chronology
Visibility
query/index pressure
lifecycle
```

Creating a generic `agreement_ref + any MaterialStateRef + parties` schema would externalize these unanswered semantic questions into runtime application code and permit semantically invalid references.

Therefore non-materialization is stronger and safer than a placeholder shell.

### 34.39 Future consequential Agreement materialization trigger

The first real Agreement vertical/profile may introduce persistence only after it closes at least:

```text
exact Agreement purpose/context
exact independent-addressability requirement
exact terms-bearing owner/facet Reference Contract
exact terms payload ownership
exact material-equivalence rule
exact party Reference Contract
exact applicable-party / quorum semantics
exact minimum/maximum party cardinality if bounded
exact assent-action semantics
exact silence/no-response semantics
exact represented-party semantics
exact actual Actor Reference Contract
exact Representation/Authority basis where material
exact Principal/security provenance where useful
exact recorded/accepted/effective chronology
exact amendment/supersession/cessation semantics
exact Visibility/privacy surfaces
exact retention/redaction policy where applicable
exact currentness/history contract
exact concurrency / stale-state protection
exact indexes from real query pressure
exact runtime ACL/write operations
exact Alembic migration DAG placement
exact SQLAlchemy mapping shape
exact direct PostgreSQL positive/negative/concurrency tests
```

Only then may the concrete profile introduce Agreement tables/facets/associations.

### 34.40 Future material topology retained

When a concrete profile passes the trigger, the preferred topology remains conceptually:

```text
concrete Agreement contextual record
→ ScopedRecordRef when independently addressable/material

exact shared-assent/terms state
→ MaterialStateRef
→ exact admitted terms state

party relations
→ N typed party rows
→ all attached to the same Agreement material state
```

This is not a mandate for the exact historical Part-1 table names. The future profile may use more precise names once its concrete semantics are known.

### 34.41 Current-binding threshold remains profile-specific

Not every material Agreement necessarily needs one universal “current Agreement” pointer.

Possible future semantics include:

```text
one currently applicable Agreement revision
multiple simultaneously applicable bounded Agreements
historical Agreement with no current successor
parallel Agreements for different contexts
```

The concrete profile decides currentness ownership and uses the shared current-binding machinery only when the singular owner/facet contract genuinely applies.

No generic `agreement_current` view is accepted today.

### 34.42 Agreement history never floats to current terms

A historical material Agreement state must bind the exact terms state used at the time.

Forbidden:

```text
Agreement A1 stores terms owner identity only
→ later reads current terms state T2
→ historical A1 silently appears to mean T2
```

Material history must preserve exact MaterialStateRef where terms state matters.

### 34.43 No generic pairwise Agreement relation

Rejected physical representation:

```text
person_a
agreed_with
person_b
```

Pairwise edges cannot establish that an n-party set assented to the same materially specific terms.

For three parties, three pairwise positive edges do not prove one shared Agreement context or one common terms basis.

No universal Relationship table is introduced as fallback.

### 34.44 No generic semantic JSON fallback

Agreement semantics MUST NOT disappear into:

```text
terms_jsonb
party_jsonb
agreement_payload jsonb
metadata jsonb containing required party/terms meaning
```

Bounded low-consequence metadata may still use LR-10 JSONB where independently justified, but required terms/party/provenance semantics of a future material Agreement profile remain typed and constrained.

### 34.45 Migration-DAG consequence for CP6 baseline

Because Agreement has no CP6-04 baseline objects, the baseline migration DAG contains no Agreement node.

Specifically absent from the initial business materialization plan:

```text
agreement owner table migration
agreement scoped-family registration
agreement MaterialState facet registration
agreement shared-assent payload table
agreement party table
agreement history/current view
agreement indexes
agreement trigger functions
agreement ACL grants
```

A future Agreement vertical adds its migration after the concrete terms/party/provenance dependencies it actually requires.

### 34.46 SQLAlchemy consequence

CP6-04 MUST NOT create generic mapped classes equivalent to:

```text
Agreement
AgreementSharedAssentState
AgreementPartyAssent
AgreementTerms
```

merely because Part 1 once used those design handles.

The first real Agreement profile receives concrete model classes that reflect its actual schema.

No generic `ContextualEntity`, `AgreementBase`, `TermsBase` or repository/UoW abstraction is introduced for storage uniformity.

### 34.47 Database Dictionary consequence

The CP6 baseline Dictionary catalogs only real objects.

Therefore Agreement appears in the human-readable **non-materialized capability/disposition** register, not as a fake table/view dictionary entry.

No empty `dictionary/tables/agreement.*` file is created.

When a future Agreement profile materializes, the same schema change adds the corresponding Dictionary entries with exact semantic traceability.

### 34.48 DB-U15 index consequence

Agreement contributes zero indexes to the CP6 baseline final index inventory.

Potential future indexes such as:

```text
party lookup
terms state lookup
applicable/current Agreement lookup
history chronology
```

must be justified by the concrete Agreement query/write contract.

DANTE does not index a non-existent future family by speculation.

### 34.49 DB-U21 ACL consequence

Agreement contributes zero objects to the current baseline ACL matrix.

A future Agreement migration owns exact grants/revokes for its objects under the already-closed least-privilege direction.

Likely posture for immutable material Agreement state remains:

```text
SELECT as required
INSERT through accepted write path
ordinary UPDATE denied
ordinary DELETE denied unless a later reviewed lifecycle path exists
```

but the exact matrix is future-profile-specific and is not pre-granted now.

### 34.50 DB-U14 lifecycle consequence

The existing non-destructive lifecycle baseline remains sufficient.

No Agreement-specific soft-delete/tombstone/status columns are added.

Future Agreement retention/redaction/erasure requirements must preserve surviving ScopedRecordRef/MaterialStateRef/reference/history truth according to the concrete policy.

No `ON DELETE CASCADE` is introduced as a generic Agreement convenience.

### 34.51 Concurrency requirement for future material Agreement

A consequential material Agreement operation must not establish shared assent from stale terms or incomplete party state.

A concrete profile will need transaction-level proof for cases such as:

```text
P1 assents while terms T1 current
terms change to T2 concurrently
P2 assents
```

The operation must not accidentally produce one Agreement claiming both parties assented to T2 or one mixed state.

Expected-state MaterialStateRef checks, locks or SERIALIZABLE may be used depending on the actual invariant.

The mechanism is not selected until the concrete profile exists.

### 34.52 Direct PostgreSQL proof contract retained for future Agreement

A future concrete Agreement family must directly prove at least the applicable subset of:

```text
valid exact terms-bearing MaterialStateRef                       PASS
ineligible MaterialStateRef owner/facet                         REJECT
missing terms MaterialStateRef                                  REJECT
one party only by COMMIT                                        REJECT
two or more distinct applicable parties                         PASS
duplicate party                                                 REJECT
wrong party owner family                                        REJECT
all parties share the same exact parent terms state             PASS
material terms change does not reuse prior assent               PASS/REJECT AS APPROPRIATE
historical prior Agreement state retained                       PASS
member assent does not manufacture Collective assent            PASS
Collective assent does not manufacture member personal assent   PASS
representative Actor does not replace represented party         PASS
Representation row alone does not prove Authority               PASS
silence/read/Acknowledgement does not create Agreement           PASS
Decision existence does not create Agreement                    PASS
Agreement does not create Authority/Consent/Actual               PASS
historical Agreement does not float to current terms            PASS
ordinary UPDATE of immutable material state                     REJECT
ordinary DELETE of retained material history                    REJECT
stale terms/assent concurrent write                             CONFLICT/REJECT
unauthorized runtime mutation                                   REJECT
```

These tests are staged, not passed, because no Agreement baseline schema exists in CP6-04.

### 34.53 PG-R06 consequence

Physical proof obligation PG-R06 remains valid as a future material-governance evidence contract:

```text
n-ary common terms state
+
consequential Consent/Authority/Visibility bindings
remain reconstructible after amendment/revocation
```

This checkpoint does not falsely mark a real PostgreSQL PG-R06 Agreement test PASS.

Instead:

```text
CP6 baseline Agreement object absent by deliberate disposition
→ Agreement-specific direct proof not executable yet
→ future Agreement vertical activates PG-R06 Agreement materiality proof
```

### 34.54 No conflict with CP6-01

CP6-01 classified Agreement as:

```text
LR-02 n-ary contextual record + typed assent
material when consequential
remaining physical stage:
CP6-02 REL/MAT/PROV + Agreement vertical
```

Therefore this checkpoint is consistent with CP6-01.

The semantic/material contract is retained; baseline SQL is deferred to the first actual Agreement vertical because the concrete terms-bearing profile is not part of the current maximum non-speculative database.

### 34.55 No conflict with accepted Physical mapping

The accepted Physical mapping describes how **material Agreement** should be represented when it exists:

```text
one contextual Agreement
one exact terms MaterialStateRef
N party-role assent rows
```

It did not require a speculative Agreement row in the absence of a concrete terms-bearing profile.

Checkpoint G therefore narrows implementation timing without contradicting the mapping thesis.

### 34.56 No conflict with MaterialState topology

The shared MaterialState machinery remains unchanged.

Agreement does not require pre-registering a generic facet to prove that future Agreement can later own material state.

Future profile will add exactly the scoped family/facet it needs in the same reviewed migration as the actual Agreement payload.

No orphan `agreement.shared_assent` control registration exists in the baseline without a real payload family.

### 34.57 No conflict with ScopedRecordRef topology

`scoped_address` remains a bounded dispatcher whose accepted family set is the set of concrete scoped families that actually survive CP6-03.

Because Agreement is not materialized in CP6 baseline:

```text
scoped_family = agreement
```

is not registered now.

A future material Agreement profile adds the family atomically with its concrete owner table and integrity dispatch.

### 34.58 Non-materialized Agreement baseline inventory

Final CP6 baseline inventory contribution:

```text
Agreement canonical tables                    0
Agreement scoped-address families             0
Agreement MaterialState facets                0
Agreement current-binding/history objects     0
Agreement relation/party tables               0
Agreement types/enums/domains                 0
Agreement indexes                             0
Agreement triggers/functions                  0
Agreement SQLAlchemy mapped classes           0
Agreement runtime ACL objects                 0
Agreement Dictionary table/view entries       0
```

Agreement remains fully represented in semantic/documentation traceability as an intentionally non-materialized capability with a concrete future trigger.

### 34.59 Accumulated whole-database A/B/C audit

Checkpoint G was replayed against the complete accumulated blueprint, Domain/Logical/Physical authority, CP6-01/02 and the real CP3 foundation.

Classification:

```text
A — SOUND / RETAIN
Agreement as contextual n-ary same-terms semantics
Agreement != Consent / Decision / Authority / Responsibility / Actual
future exact terms MaterialStateRef basis
future >=2 party invariant
Person / true Collective party eligibility
material amendment requires renewed applicable assent
historical terms/assent reconstruction
party != actual representative Actor
Representation != Authority
no universal Relationship/Assent/Contract root
MaterialState exact-basis discipline
non-destructive history/lifecycle
migration-owned ACL direction

B — TOO EARLY / REQUIRES NARROWING
Part-1 dante.agreement baseline materialization
→ superseded for CP6-04 baseline

Part-1 agreement.shared_assent facet registration
→ superseded until a concrete Agreement profile exists

Part-1 agreement_party_assent baseline table
→ superseded until exact party/assent profile exists

Part-1 terms_material_state_ref could otherwise degrade into any MaterialStateRef
→ rejected; future bounded owner/facet eligibility mandatory

C — STRUCTURAL DEFECT / REPAIRED
no concrete baseline terms-bearing owner/facet family exists
while generic Agreement DDL would require one
→ repaired by final NO BASELINE DDL disposition

possible generic terms/Contract/JSON fallback
→ explicitly rejected

possible party overwrite by representative Actor
→ explicitly rejected

possible Agreement inferred from silence/Acknowledgement/Decision
→ explicitly rejected

possible universal lifecycle/status enum
→ explicitly rejected

C DEFECTS AFTER REPAIR
0
```

### 34.60 Whole-database regression result after Checkpoint G

```text
57 / 57 Domain concepts                              PASS
15 / 15 LR-01 native owners                         PASS
new native owner                                    0
NativeRef / ScopedRecordRef / MaterialStateRef      PASS
current-state binding                               PASS
material-history exact-basis discipline             PASS
no generic Entity                                   PASS
no generic Relationship                             PASS
no generic Assent/Acceptance                        PASS
no generic Contract                                 PASS
no semantic JSON fallback                           PASS
Agreement != Consent                                PASS
Agreement != Decision                               PASS
Agreement != Authority                              PASS
Agreement != Responsibility                         PASS
Agreement != Actual                                 PASS
Agreement party != actual Actor                     PASS
Collective != party-set cardinality                 PASS
member assent != Collective assent                  PASS
material terms revision != inherited assent         PASS
unknown/absence != explicit negative                PASS
DB-U14 lifecycle                                    PASS
DB-U15 index discipline                             COMPATIBLE / GLOBAL OPEN
DB-U21 ACL direction                                COMPATIBLE / GLOBAL OPEN
new unclassified material item                      0
C defects after repair                              0
```

No Domain, Logical, Physical, CP6-01 or CP6-02 reopening is required.

### 34.61 AGR-U01 closure

Final disposition:

```text
AGR-U01
CLOSED

BASELINE AGREEMENT DDL
NONE

FUTURE TRIGGER
first consequential Agreement profile with exact:
- terms-bearing owner/facet contract
- material equivalence
- party applicability
- assent action/provenance
- Representation/Authority basis
- chronology/currentness
- Visibility/lifecycle
- indexes/ACL/tests
```

This removes the last exact local CP6-03 blocker.

### 34.62 Local unresolved register — CLOSED TO ZERO

The complete local closure register is now:

```text
SCH-U01   CLOSED
SCH-U02   CLOSED
ACT-U01   CLOSED
OUT-U01   CLOSED
MIL-U01   CLOSED
AGR-U01   CLOSED
CRT-U01   CLOSED
EVL-U01   CLOSED
TC-U01    CLOSED
```

Therefore:

```text
LOCAL EXACT UNRESOLVED ITEMS
0

LOCAL EXACT OPEN
NONE
```

No local item is hidden under a generic fallback or placeholder schema.

### 34.63 Global unresolved register remains nine

Checkpoint G does not alter the global final-consolidation set:

```text
DB-U08
DB-U09
DB-U10
DB-U15
DB-U17
DB-U18
DB-U19
DB-U20
DB-U21

COUNT = 9
```

These are the only remaining classified CP6-03 blockers before final object-inventory freeze and Gate 03.

### 34.64 Global items are not implicitly closed by local-zero status

`LOCAL EXACT OPEN = 0` does not authorize business DDL.

The remaining global work still owns materially important final decisions:

```text
DB-U08  exact final PostgreSQL naming
DB-U09  Account baseline disposition
DB-U10  Principal/security persistence disposition
DB-U15  final index justification matrix
DB-U17  provider/integration baseline disposition
DB-U18  idempotency baseline disposition
DB-U19  transactional outbox baseline disposition
DB-U20  derived/search/vector baseline disposition
DB-U21  exact object-by-object runtime ACL matrix
```

No global item is converted into an implicit “later” note merely because the semantic-local register reached zero.

### 34.65 Gate 03 remains not earned

After Checkpoint G:

```text
LOCAL EXACT OPEN
0

GLOBAL DB-U OPEN
9

UNCLASSIFIED
0

FINAL OBJECT INVENTORY
NOT YET FROZEN

FINAL INDEX MATRIX
NOT YET FROZEN

FINAL ACL MATRIX
NOT YET FROZEN

FINAL MIGRATION DAG
NOT YET FROZEN

FINAL SQLALCHEMY MAPPING PLAN
NOT YET FROZEN

DATABASE DICTIONARY
NOT YET INITIALIZED WITH FINAL REAL OBJECT INVENTORY

FINAL DIRECT POSTGRESQL TEST PLAN
NOT YET FROZEN

GATE 03
NOT YET EARNED
```

No CP6-04 business schema creation is authorized by this checkpoint.

### 34.66 Next exact work block — global final consolidation

The next CP6-03 phase is no longer concept-by-concept local closure.

It is final global consolidation:

```text
DB-U08 / DB-U09 / DB-U10
DB-U15 / DB-U17 / DB-U18
DB-U19 / DB-U20 / DB-U21
```

The correct sequence must be derived from dependency pressure, but should culminate in:

```text
all global DB-U closed/classified
→ final exact PostgreSQL object inventory
→ deterministic final names
→ exact constraints/reference catalog
→ justified index catalog
→ exact object ACL matrix
→ migration DAG
→ SQLAlchemy mapping plan
→ machine-readable Database Dictionary
→ final direct PostgreSQL proof matrix
→ complete whole-database audit
→ GATE 03 decision
```

### 34.67 Explicit boundary before CP6-04

Even if the global consolidation reaches:

```text
GLOBAL DB-U OPEN = 0
LOCAL EXACT OPEN = 0
UNCLASSIFIED = 0
GATE 03 = EARNED
```

DANTE MUST NOT silently transition from blueprint to implementation.

The transition from:

```text
CP6-03
DESIGN / BLUEPRINT
```

to:

```text
CP6-04
REAL DATABASE MATERIALIZATION
Alembic + PostgreSQL DDL + SQLAlchemy + ACL + implementation tests
```

is an explicit human-visible boundary and requires a separate approved write gate.

Checkpoint G therefore closes local design work only.

### 34.68 Checkpoint G final register

```text
CONSOLIDATION CHECKPOINT G
AGREEMENT BASELINE DISPOSITION

PASS AFTER HARDENING

AGR-U01
CLOSED

FINAL CP6 BASELINE AGREEMENT DDL
NONE

FUTURE MATERIAL AGREEMENT CONTRACT
RETAINED

PART-1 BASELINE AGREEMENT MATERIALIZATION
NARROWLY SUPERSEDED

LOCAL EXACT UNRESOLVED ITEMS
0

LOCAL EXACT OPEN
NONE

GLOBAL UNRESOLVED DB-U ITEMS
9

UNCLASSIFIED NEW ITEMS
0

WHOLE ACCUMULATED DATABASE AUDIT
PASS AFTER REPAIR

CP6 BUSINESS DDL AUTHORIZED
NO

GATE 03
NOT YET EARNED
```

Checkpoint G is complete when this section is committed, remote-read back, and the branch delta is proven to contain only the authorized Part-5/README structural change.
