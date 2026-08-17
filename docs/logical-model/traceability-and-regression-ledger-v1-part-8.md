<!-- LIFEOS-CANONICAL-CONTINUATION document="traceability-and-regression-ledger-v1.md" follows="traceability-and-regression-ledger-v1-part-7.md" -->
> **Canonical continuation of the Logical Model traceability / invariant / regression ledger.** Earlier invariant IDs remain active. This continuation records Slice F — Relationships / Multi-Actor / Governance hardening and closes the A+B+C+D+E governance/privacy carry-forward replay.

# Slice F — Traceability and Regression Ledger

## Invariant ledger

### INV-F001 — Specific semantic relation owner beats generic edge convenience

**Domain owners / sources:** Membership, Participation, Responsibility, Coordination Stewardship, Contribution, Interpersonal Relationship, Ownership, Possession, Authority, Consent, Agreement, Visibility, Representation.  
**Logical disposition:** relation-profiled LR-03/direct-or-qualified typed relation; no universal semantic Relationship root.  
**Required query:** can reverse mapping recover the exact semantic family when endpoints are identical?  
**Proving tests:** F-REL-01..03.  
**Attacking mutations:** MUT-F01, MUT-F02.  
**Regression class:** R3 WHOLE-LOGICAL.  
**Status:** PASS WITH HARDENING.

### INV-F002 — Relation addressability does not require RelationRef

**Domain owners / sources:** Slice A ReferenceAddress, Slice D MaterialStateRef, qualified relation families.  
**Logical disposition:** direct typed relation when simple; LR-02 + ScopedRecordRef + MaterialStateRef when material.  
**Required query:** can a consequential relation state be addressed historically without creating a universal identity hierarchy?  
**Proving tests:** F-REL-02/03.  
**Attacking mutation:** MUT-F03.  
**Regression class:** R3 A↔D↔F.  
**Status:** PASS.

### INV-F003 — Actor remains contextual agency, not wrapper identity

**Domain owners / sources:** Actor, Person, Collective, Representation, Provenance.  
**Logical disposition:** Actor eligibility/role semantics; concrete action-role relation retained; no ActorRef.  
**Required query:** who/what acted without equating Person, Account or Principal?  
**Proving tests:** F-REP-01/03.  
**Attacking mutations:** MUT-F04, MUT-F38.  
**Regression class:** R3 A↔D↔F.  
**Status:** PASS.

### INV-F004 — Collective identity remains independent from member set and member personal state

**Domain owners / sources:** Collective, Membership, Agreement, Decision, Responsibility.  
**Logical disposition:** Collective NativeRef; membership/state relations external to identity.  
**Required query:** can Collective continuity and collective action/Agreement be reconstructed without rewriting each member?  
**Proving tests:** F-COL-01..03, F-AGR-04.  
**Attacking mutations:** MUT-F23, MUT-F24.  
**Regression class:** R3 A↔B↔D↔F.  
**Status:** PASS WITH HARDENING.

### INV-F005 — Membership has no automatic governance or participation consequences

**Domain owners / sources:** Membership, Participation, Authority, Visibility, Agreement, Consent.  
**Logical disposition:** specific typed relation; downstream policy may use Membership as an input but not semantic equality.  
**Required query:** can a member lack participation, Authority, Visibility and Consent independently?  
**Proving tests:** F-MEM-01..04.  
**Attacking mutations:** MUT-F05..08, MUT-F33.  
**Regression class:** R3 F + A/security projection.  
**Status:** PASS.

### INV-F006 — Interpersonal Relationship does not manufacture governance

**Domain owners / sources:** Interpersonal Relationship, Authority, Visibility, Consent.  
**Logical disposition:** bounded Person-to-Person LR-03 family with kind-specific inverse/symmetry rules only where justified.  
**Required query:** can `manager`, `friend`, `partner`, `parent` remain contextual relationship meaning without implicit powers?  
**Proving tests:** F-REL-04..06.  
**Attacking mutations:** MUT-F09..11.  
**Regression class:** R3 F.  
**Status:** PASS.

### INV-F007 — Responsibility, performer and Coordination Stewardship remain distinct

**Domain owners / sources:** Responsibility, Activity/Actual, Coordination Stewardship.  
**Logical disposition:** independent typed relations/history.  
**Required query:** who was accountable, expected to perform, actually performed and carried coordination burden?  
**Proving tests:** F-RESP-01/02, F-STEW-01/02.  
**Attacking mutations:** MUT-F12, MUT-F13.  
**Regression class:** R3 B↔C↔F.  
**Status:** PASS.

### INV-F008 — Participation does not establish Contribution

**Domain owners / sources:** Participation, Contribution, Actual.  
**Logical disposition:** separate relation families; Contribution grounded in actual meaningful input/work.  
**Required query:** who was present/involved versus who materially contributed?  
**Proving tests:** F-PART-01..03, F-CONTR-01.  
**Attacking mutation:** MUT-F14.  
**Regression class:** R2 C↔F, promoted to final R3 replay.  
**Status:** PASS.

### INV-F009 — Ownership and Possession remain independent from Authority/Allocation

**Domain owners / sources:** Ownership, Possession, Asset, Resource Allocation, Authority, Visibility.  
**Logical disposition:** separate LR-03 families over continuing Asset identity.  
**Required query:** who owns, who possesses, who is allocated and who may govern/view?  
**Proving tests:** F-OWN-01/02.  
**Attacking mutations:** MUT-F15, MUT-F16.  
**Regression class:** R3 A↔E↔F.  
**Status:** PASS.

### INV-F010 — Authority is bounded domain governance, not Visibility or technical permission

**Domain owners / sources:** Authority, Visibility, Account/Principal boundary, Decision, policy.  
**Logical disposition:** LR-03/LR-02 explicit Authority + LR-05 basis + LR-08 Effective Authority where derived.  
**Required query:** who may legitimately make effect E effective on target/facet/version V at T?  
**Proving tests:** F-AUTH-01..05.  
**Attacking mutations:** MUT-F17, MUT-F18, MUT-F31, MUT-F32, MUT-F34.  
**Regression class:** R3 A↔B↔D↔F.  
**Status:** PASS WITH HARDENING.

### INV-F011 — Historical Authority basis is action-time/material-state sensitive

**Domain owners / sources:** Authority, Version, MaterialStateRef, Provenance, Representation.  
**Logical disposition:** consequential historical effect binds/reconstructs applicable Authority/policy state at action/effect time.  
**Required query:** was Actor A legitimately empowered when historical effect E became effective?  
**Proving tests:** F-AUTH-02, F-REP-04.  
**Attacking mutation:** MUT-F27.  
**Regression class:** R3 D↔F; WD-03.  
**Status:** PASS WITH HARDENING.

### INV-F012 — Consent remains action/target/scope/purpose/context/time/material-state sensitive

**Domain owners / sources:** Consent, Visibility, Authority, Agreement, Version.  
**Logical disposition:** LR-03 + material LR-02/ScopedRecordRef/MaterialStateRef when consequential.  
**Required query:** what exactly was permitted, by whom, for what purpose and target state, and was it applicable then?  
**Proving tests:** F-CONS-01..05.  
**Attacking mutations:** MUT-F19, MUT-F20, MUT-F28.  
**Regression class:** R3 D↔F.  
**Status:** PASS WITH HARDENING.

### INV-F013 — Agreement requires materially aligned common terms, not pairwise relatedness

**Domain owners / sources:** Agreement, Collective, Version, Decision.  
**Logical disposition:** LR-02 n-ary Agreement record + typed party assent + material terms-state binding.  
**Required query:** which parties assented to the same materially specific terms/version?  
**Proving tests:** F-AGR-01..05.  
**Attacking mutations:** MUT-F21, MUT-F22, MUT-F23.  
**Regression class:** R3 B↔D↔F.  
**Status:** PASS WITH HARDENING.

### INV-F014 — Visibility is independently scoped to endpoint, relation, projection and source

**Domain owners / sources:** Visibility, Provenance, all relation families.  
**Logical disposition:** LR-03/LR-02 explicit visibility where material + LR-05 policy + LR-08 Effective Visibility.  
**Required query:** what exact representation may recipient R receive without exposing hidden relation/source/provenance?  
**Proving tests:** F-VIS-01..05, F-PRIV-01/02.  
**Attacking mutations:** MUT-F29, MUT-F30.  
**Regression class:** R3 A↔D↔E↔F.  
**Status:** PASS WITH HARDENING.

### INV-F015 — Representation preserves actual Actor separately from represented party and legitimacy basis

**Domain owners / sources:** Representation, Actor, Authority, Consent, Account/Principal, Provenance.  
**Logical disposition:** action-scoped LR-03; material LR-02 when consequential.  
**Required query:** who actually acted, for whom, under which basis and technical Principal?  
**Proving tests:** F-REP-01..04.  
**Attacking mutations:** MUT-F25, MUT-F26, MUT-F38.  
**Regression class:** R3 A↔D↔F.  
**Status:** PASS WITH HARDENING.

### INV-F016 — Domain governance != technical authorization decision

**Domain owners / sources:** Authority, Visibility, Consent, Agreement, Membership, Representation; security Principal/runtime policy boundary.  
**Logical disposition:** canonical governance projected into replaceable technical AuthZ request/store/engine.  
**Required query:** can runtime allow/deny be explained without being treated as canonical Authority truth?  
**Proving tests:** F-AUTH-03/04, F-REP-03.  
**Attacking mutations:** MUT-F31, MUT-F32, MUT-F37, MUT-F38.  
**Regression class:** R3 F + WD-05.  
**Status:** PASS WITH HARDENING.

### INV-F017 — Delayed consequential effect cannot rely indefinitely on stale authorization

**Domain owners / sources:** Authority, Consent/Visibility where applicable, Decision/operation, Version/MaterialState.  
**Logical disposition:** effect-time revalidation or explicitly valid immutable authorization/effect binding; exact mechanism deferred.  
**Required query:** was the governance basis still applicable when the delayed effect became effective?  
**Proving test:** F-AUTH-06.  
**Attacking mutation:** MUT-F35.  
**Regression class:** R3 C↔D↔F; WD-03/WD-05.  
**Status:** PASS WITH HARDENING.

### INV-F018 — Unknown/conflicting relation/governance state remains representable

**Domain owners / sources:** Reconciliation, Evidence, Provenance, relation/governance families.  
**Logical disposition:** explicit unknown/unresolved/conflict states; no universal winner.  
**Required query:** what is established versus merely asserted, unknown, refused, withdrawn or contradicted?  
**Proving tests:** F-UNK-01/02, F-CONFLICT-01/02.  
**Attacking mutation:** MUT-F36.  
**Regression class:** R3 D↔F.  
**Status:** PASS.

## Trace matrix

| TRACE ID | DOMAIN OWNER / INVARIANT | LOGICAL DISPOSITION | REQUIRED QUERY / OPERATION | TESTS | OTHER SLICES | VERDICT |
|---|---|---|---|---|---|---|
| TR-F-01 | specific relation ownership | LR-03 + relation-profiled Reference Contract | recover exact relation family | F-REL-01..03 | A,D | PASS |
| TR-F-02 | relation material state | LR-02 + ScopedRecordRef/MaterialStateRef | relation state at T | F-REL-03 | A,D | PASS |
| TR-F-03 | Actor attribution | contextual Actor + specific role | who actually acted? | F-REP-01/03 | A,D | PASS |
| TR-F-04 | Collective/Membership | NativeRef + LR-03 Membership | member set / collective state at T | F-COL-01..03, F-MEM-* | A,B,D | PASS |
| TR-F-05 | Responsibility/Stewardship | independent LR-03 families | accountable vs coordinator vs performer | F-RESP-*, F-STEW-* | B,C | PASS |
| TR-F-06 | Participation/Contribution | independent LR-03 families | involved vs materially contributed | F-PART-*, F-CONTR-* | C | PASS |
| TR-F-07 | Ownership/Possession | independent LR-03 families | owner vs holder vs allocated | F-OWN-* | A,E | PASS |
| TR-F-08 | Authority | LR-03/LR-02 + LR-05 + LR-08 | legitimate effect basis at T | F-AUTH-* | B,D | PASS WITH HARDENING |
| TR-F-09 | Consent | material scoped relation/state | exact permitted use at T | F-CONS-* | D | PASS WITH HARDENING |
| TR-F-10 | Agreement | LR-02 n-ary + terms MaterialStateRef | common terms/parties | F-AGR-* | B,D | PASS WITH HARDENING |
| TR-F-11 | Visibility | endpoint/relation/projection/source policy | safe recipient projection | F-VIS-*, F-PRIV-* | A,D,E | PASS WITH HARDENING |
| TR-F-12 | Representation | LR-03 action-scoped + material basis | actor / represented / authority / principal | F-REP-* | A,D | PASS WITH HARDENING |
| TR-F-13 | domain vs AuthZ | downstream projection/adapter | explain allow/deny vs domain governance | F-AUTH-03/04 | A,F | PASS WITH HARDENING |
| TR-F-14 | stale AuthZ | effect-time governance binding | delayed effect still valid? | F-AUTH-06 | C,D | PASS WITH HARDENING |
| TR-F-15 | conflict/unknown | Evidence/Provenance/Reconciliation | established vs unresolved | F-UNK-*, F-CONFLICT-* | D | PASS |

## Mutation coverage

```text
TOTAL MUTATIONS 38
REJECTED        38
FAIL             0
```

The permanent mutation IDs are `MUT-F01..MUT-F38` in `test-corpus-v1-part-8.md`.

## Counterfactual coverage

```text
TOTAL COUNTERFACTUAL PAIRS 22
DISTINGUISHABLE            22
FAIL                        0
```

The permanent counterfactual IDs are `CF-F01..CF-F22` in `test-corpus-v1-part-8.md`.

## A+B+C+D+E carry-forward closure

The previous cumulative checkpoint required Slice F to replay:

```text
private source -> shared feasibility consequence
Resource Allocation of Person != Consent / Agreement / Responsibility / Participation
collective/shared resource decision != every member endorsement
Authority to allocate/claim != Ownership / Possession
Visibility of Allocation/Claim != private Requirement/feasibility source
actor-specific projections over one shared resource reality
historical participation/access != current Authority/Visibility
```

Result:

```text
7 / 7 PASS
```

`INV-ABCDE010` is no longer merely `F REPLAY`; the selective-disclosure architecture is now explicitly represented and becomes an R3 whole-logical obligation.

## R3 whole-logical promotion

The following are mandatory for final A+B+C+D+E+F replay:

```text
INV-F001
INV-F002
INV-F003
INV-F004
INV-F005
INV-F006
INV-F007
INV-F009
INV-F010
INV-F011
INV-F012
INV-F013
INV-F014
INV-F015
INV-F016
INV-F017
INV-F018
```

`INV-F008` is also replayed in the final whole-logical corpus because Contribution/Participation crosses reality and multi-actor semantics even though it is locally R2.

## WD-03 carry-forward

Slice F adds explicit historical reconstruction obligations for:

```text
relation material state
Membership/quorum basis
Authority action-time basis
Consent applicability/withdrawal
Agreement terms/version
Visibility applicability/disclosure
Representation actor/represented/basis
stale/delayed authorization
```

Final whole-logical validation must prove these compose with A-E history without requiring current-state substitution.

## WD-05 carry-forward

Physical/API pressure must prove the logical distinctions survive:

```text
owner-specific relation tables
shared typed edge infrastructure where safe
qualified relation records
MaterialStateRef history
ReBAC/ABAC projection stores
runtime policy engines
capability mechanisms
```

without turning any physical convenience into universal semantic ontology.

## Current counters

```text
Slice F trace entries required       15
Slice F trace entries closed         15
Slice F unresolved                    0

Slice F invariants                   18
Slice F invariant failures            0

Mutation tests                       38
Mutation failures                     0

Counterfactual pairs                 22
Counterfactual failures               0

A-E carry-forward tests               7
A-E carry-forward failures            0

Domain reopen required                0
```

Remote activation remains pending exact Git QA and a separately gated closure record.