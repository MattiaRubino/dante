# Slice F — Relationships / Multi-Actor / Governance — Validation Checkpoint v1

**Status:** Local validation complete — remote QA pending  
**Date:** 2026-08-17  
**Validation standard:** Logical Validation Methodology v1 + Stage-0H hardening

## 1. Scope verdict

Preferred candidate:

> **Layered Typed Relations & Governance Model**

Local verdict:

```text
PASS WITH HARDENING
DOMAIN REOPEN REQUIRED        0
NEW DOMAIN OWNER REQUIRED     0
A+B+C+D+E REGRESSION FAILURE  0
LOGICAL STRUCTURAL BLOCKER    0
```

This checkpoint is not remote-active until exact Git QA closure succeeds.

## 2. Candidate architectures compared

### F-A — Universal semantic Relationship / Edge

```text
Relationship(id, from, relation_type, to, payload)
```

**Verdict:** REJECTED LOGICAL CANDIDATE.

Reason: relation type and payload become semantic escape hatches; Agreement n-arity, Visibility surfaces, Consent scope/purpose, Authority effect scope and historical relation state become weakly typed or ad hoc.

### F-B — Fully owner-specific structures only

Every relation family receives a dedicated logical structure with no shared representation contract.

**Verdict:** VIABLE STRONG ALTERNATIVE / PHYSICAL INGREDIENT.

Strength: maximal type specificity and relational integrity.

Weakness: repeats addressing, history, provenance, lifecycle, visibility and material-state-binding machinery across families.

### F-C — Layered Typed Relations & Governance

Specific semantic relation families use relation-profiled Reference Contracts, direct representation in simple cases, qualified LR-02 material records where consequence requires, and existing ScopedRecordRef/MaterialStateRef for address/history.

Governance projects into a replaceable technical AuthZ layer.

**Verdict:** SELECTED — PASS WITH HARDENING.

### F-D — ReBAC graph as canonical LifeOS model

Zanzibar/OpenFGA-like user/relation/object tuples treated as source of all relationship truth.

**Verdict:** REJECTED AS DOMAIN MODEL; RETAINED AS AUTHORIZATION PROJECTION/ENFORCEMENT CANDIDATE.

Reason: authorization relationships are optimized for permission evaluation, not for preserving all LifeOS domain distinctions and n-ary/versioned/common-ground semantics.

### F-E — ABAC/policy language as canonical LifeOS model

Cedar/OPA-like policies become canonical semantic state.

**Verdict:** REJECTED AS DOMAIN MODEL; RETAINED AS POLICY/ENFORCEMENT CANDIDATE.

Reason: policy decision representations do not replace the domain facts on which policy depends.

### F-F — Universal capability/grant ledger

Every relationship/governance state becomes a delegable capability/grant.

**Verdict:** REJECTED AS COMPLETE MODEL; RETAINED FOR BOUNDED DELEGATION/AUTHORIZATION MECHANISMS.

### F-G — Universal governance event log

All governance state is reconstructed only from generic events.

**Verdict:** REJECTED AS LOGICAL ONTOLOGY; RETAINED AS POSSIBLE PHYSICAL HISTORY TECHNIQUE.

## 3. Required high-value query corpus

The preferred candidate must answer or support truthful reconstruction of at least:

1. Who is responsible for commitment X now and at historical time T?
2. Who is steward versus expected performer versus actual performer?
3. Who currently belongs to Collective C and who belonged at T?
4. Which Membership/material eligible set was used by historical collective Decision D?
5. Which interpersonal relation was current at T without assuming symmetry/transitivity?
6. Who actually participated versus who accepted or declined beforehand?
7. Who materially contributed versus merely participated?
8. Who currently owns versus possesses Asset A?
9. Does Actor A have Authority for effect E on target/facet/version V now and at T?
10. What basis/policy/material state established that Authority?
11. What bounded representation may recipient R see without exposing private sources?
12. Are endpoints visible while the relationship between them remains hidden?
13. Is relationship existence visible while relationship kind/history is hidden?
14. What Consent applies to action/use/exposure U for target X, purpose P, context C and material state V?
15. Was that Consent withdrawn or superseded after a historical permitted action?
16. Which parties assented to the same materially specific Agreement terms state?
17. Did a Collective agree, or did individual members personally agree?
18. Who actually acted, for whom, and under which Representation/Authority basis?
19. Which technical Principal executed a request without replacing semantic Actor attribution?
20. Why did runtime AuthZ allow or deny a request?
21. Does runtime allow/deny correspond to domain governance state or another security constraint?
22. Was a queued/delayed action still governed by an applicable basis at effect time?
23. Which relation/governance assertions are unresolved or conflicting rather than false?
24. Can AI use authorized private source state for a safe shared consequence without disclosing the source?

## 4. Falsification scenarios

```text
F-T01 member but not participant                                      PASS
F-T02 participant but not member                                      PASS
F-T03 participant but no material Contribution                       PASS
F-T04 responsible Actor differs from expected performer              PASS
F-T05 actual performer differs from responsible Actor                PASS
F-T06 Steward differs from responsible/performer                     PASS
F-T07 owner differs from possessor                                   PASS
F-T08 owned Asset not visible to owner under bounded policy          PASS
F-T09 interpersonal manager label without domain Authority           PASS
F-T10 friend relation actor-scoped / non-symmetric                   PASS
F-T11 both endpoints visible but relation hidden                     PASS
F-T12 relation visible but supporting Evidence hidden                PASS
F-T13 private source -> visible free/busy consequence                PASS
F-T14 Authority exists without technical access path                 PASS
F-T15 technical Principal allowed but no legitimate domain Authority PASS
F-T16 technical request denied while domain Authority still exists   PASS
F-T17 Consent exists before any exposure/action occurs               PASS
F-T18 Consent withdrawn after historical legitimate disclosure       PASS
F-T19 Consent to scope/version v1 not inherited by material v2       PASS
F-T20 Agreement parties assent to same terms v3                      PASS
F-T21 one party assents to v3, another to v4 -> no shared Agreement  PASS
F-T22 Collective Agreement != each member Agreement                  PASS
F-T23 member action != Collective action automatically               PASS
F-T24 representative acts for Person but Person not actual Actor     PASS
F-T25 Representation without sufficient Authority                    PASS
F-T26 Authority expires after historical valid represented action    PASS
F-T27 queued action checked before Authority revocation              PASS WITH HARDENING
F-T28 security-group membership != canonical Membership automatically PASS
F-T29 imported relationship label remains Evidence until accepted    PASS
F-T30 conflicting Authority claims remain unresolved                 PASS
F-T31 no applicable Visibility grant != explicit prohibition         PASS
F-T32 Collective membership changes after historical quorum          PASS
F-T33 direct simple relation stays compact                           PASS
F-T34 consequential relation escalates to material LR-02 state       PASS
F-T35 same endpoints carry multiple independent relation families    PASS
F-T36 solver/AI confidence does not create Authority                 PASS
F-T37 AI authorized to reason over source but not disclose source    PASS
F-T38 technical authz tuple store can be rebuilt from canonical state PASS
```

## 5. Mutation / destructive tests

The candidate must reject every mutation below:

```text
MUT-F01  every relation -> generic Relationship row
MUT-F02  generic relation_type becomes semantic fallback
MUT-F03  create universal RelationRef
MUT-F04  Actor receives wrapper identity
MUT-F05  Membership implies Participation
MUT-F06  Membership implies Authority
MUT-F07  Membership implies Visibility
MUT-F08  Membership implies Agreement/Consent
MUT-F09  interpersonal relationship implies Authority
MUT-F10  friend relation forced symmetric
MUT-F11  manager label implies governance power
MUT-F12  Responsibility = performer
MUT-F13  Responsibility = Coordination Stewardship
MUT-F14  Participation = Contribution
MUT-F15  Ownership = Authority
MUT-F16  Possession = Allocation
MUT-F17  Visibility = Authority
MUT-F18  Authority = Visibility
MUT-F19  Consent = Visibility
MUT-F20  Consent = technical Permission
MUT-F21  Agreement = N pairwise edges
MUT-F22  Agreement terms update preserves old assent automatically
MUT-F23  Collective Agreement expands to every member
MUT-F24  Collective action inferred from one member action
MUT-F25  Representation rewrites represented party as Actor
MUT-F26  Representation implies Authority
MUT-F27  current Authority used as historical action basis
MUT-F28  revoked Consent erases historical permitted use
MUT-F29  endpoint Visibility exposes relation automatically
MUT-F30  relation Visibility exposes private Evidence automatically
MUT-F31  technical ALLOW creates domain Authority
MUT-F32  technical DENY deletes domain Authority
MUT-F33  security group = domain Membership automatically
MUT-F34  AI confidence/capability = Authority
MUT-F35  queued ALLOW remains permanently valid after governance change
MUT-F36  newest relation assertion wins universally
MUT-F37  AuthZ tuple store becomes canonical domain source truth
MUT-F38  policy-engine Principal becomes semantic Actor identity
```

Expected and observed logical result:

```text
38 / 38 REJECTED
```

## 6. Counterfactual matrix

The model must distinguish all of the following:

```text
member                         != participant
participant                    != contributor
responsible                    != performer
responsible                    != steward
owner                          != possessor
can see                        != can govern/change
can govern/change              != can see private basis
Consent exists                 != action/exposure occurred
Visibility exists              != recipient actually viewed
Agreement                      != individual Consent
Collective Agreement           != member personal Agreement
member action                  != Collective action
actual Actor                   != represented party
Representation                 != Authority
Authority at T                 != Authority now
Consent to v1                  != Consent to materially expanded v2
endpoint visibility            != relation visibility
relation visibility            != source/Evidence visibility
technical Principal            != semantic Actor
technical allow                != semantic Authority
technical deny                 != semantic absence of Authority
unknown relation               != explicit no relation
```

Result: PASS.

## 7. Historical replay

Representative governance chronology:

```text
T0 Collective C exists
T1 Anna Membership active
T2 Anna receives bounded Authority A1 over effect E
T3 Anna grants/records bounded Consent C1 for purpose P / target state V1
T4 Luca receives Visibility of projection Q but not source S
T5 AI/service acts as actual Actor for Anna under Representation R1 and A1
T6 technical authorization allows request
T7 effect becomes effective and history binds applicable governance state
T8 A1 revoked
T9 C1 withdrawn for future use
T10 relation/terms/source states later corrected
T11 historical query
```

The model must reconstruct:

- actual Actor;
- represented party;
- Authority basis applicable then;
- Consent state/version/purpose applicable then where relevant;
- what recipient could see then;
- what private source remained hidden;
- resulting effective domain state;
- subsequent revocation/withdrawal/correction without rewriting T7.

Result: PASS WITH HARDENING.

## 8. Delayed-action / TOCTOU pressure

Case:

```text
T1 Authority valid
T2 AuthZ -> ALLOW
T3 Authority revoked
T4 queued operation attempts effect
```

Required outcome:

```text
T2 allow is not permanent semantic authorization for T4
```

A physical/runtime implementation must either:

- revalidate the materially applicable governance basis close to effect time; or
- preserve an explicit immutable authorization/effect binding whose semantics validly permit delayed execution.

Exact mechanism remains stage-deferred.

Result: PASS WITH HARDENING.

## 9. Multi-actor / privacy pressure

PASS with mandatory preservation of:

```text
shared canonical reality
+ actor-scoped relation/governance state
+ projection/source selective Visibility
+ relation-level Visibility
+ independent Consent/Authority/Agreement semantics
```

No per-user duplication of shared domain objects is required merely because actors have different access, stance, participation, relationship or governance state.

## 10. Product Reality pressure

### Household coordination

```text
Collective Household H
Anna Membership H
Luca Membership H
Activity Recycling
Responsibility Luca
Coordination Stewardship Anna
Event Appointment
Participation Anna accepted / Luca invited
private health source Anna
shared projection Unavailable
Visibility Luca -> projection only
Authority Anna -> bounded household replanning
Consent remains separate
```

Result: one shared reality, independent actor relations, no generic Relationship root.

### AI assistant acting for a user

```text
AI assistant       -> Actor
service credential -> Principal
Anna               -> represented party
Representation     -> AI acts for Anna
Authority          -> schedule appointments only
Consent            -> provider contact may be allowed, full private history may remain disallowed
Visibility         -> explanation exposes safe basis only
```

Result: Actor/Principal/Representation/Authority/Consent/Visibility remain separable.

### Agreement

```text
Trip terms state T3
Anna assent T3
Luca assent T3
Marco assent T3
-> Agreement A

terms materially change to T4
-> prior assent does not carry automatically
```

Result: requires n-ary/material-state-aware representation; pairwise generic edges fail.

## 11. External benchmark verdict

Primary/official benchmark set covers:

- Google Zanzibar;
- OpenFGA;
- Cedar;
- Open Policy Agent;
- SCIM RFC 7643;
- OAuth 2.0 Token Exchange RFC 8693;
- HL7 FHIR Consent;
- AWS IAM policy evaluation;
- Macaroons/contextual caveats.

Cross-source conclusion:

```text
relation/policy/capability machinery can be excellent authorization infrastructure
!=
that machinery is the canonical ontology for all LifeOS relationships/governance state
```

Result: PASS.

## 12. LM gate matrix

```text
LM-01 Semantic owner coverage                  PASS
LM-02 Identity/reference preservation          PASS
LM-03 Lifecycle/state separation               PASS WITH HARDENING
LM-04 Historical reconstruction / WD-03        PASS WITH HARDENING
LM-05 Relation/governance specificity          PASS WITH HARDENING
LM-06 Multi-actor/selective visibility         PASS WITH HARDENING
LM-07 Provenance/reconciliation                PASS WITH HARDENING
LM-08 Simple-case compactness                  PASS
LM-09 Specialist boundary                      PASS
LM-10 No semantic-free fallback                PASS
LM-11 Reverse mapping                          PASS
LM-12 High-value query feasibility             PASS
LM-13 Evolution/obsolescence resilience        PASS WITH HARDENING
LM-14 Scale/concurrency plausibility            PASS WITH HARDENING
LM-15 External benchmark/anti-pattern mining   PASS
LM-16 Persistence/API pressure / WD-05         PASS WITH HARDENING
LM-17 Traceability completeness                PASS
LM-18 Mutation / inverse-necessity survival    PASS
LM-19 Counterfactual distinguishability        PASS
LM-20 Decision / assumption integrity          PASS WITH HARDENING
LM-21 Cross-slice regression integrity         PASS
LM-22 Product Reality coherence                PASS
LM-23 Clean-room reconstructibility            PASS WITH HARDENING
```

## 13. WD-03 / WD-05 disposition

### WD-03 — historical reconstructibility

Slice F materially advances WD-03 by requiring historical binding of consequential relation/governance state, action-time Authority, Consent applicability, Agreement terms state, Visibility basis and Representation attribution.

It does not fully discharge whole-model WD-03; final A+B+C+D+E+F replay must verify integrated reconstructibility end to end.

### WD-05 — persistence/API pressure

Slice F preserves multiple viable physical strategies:

```text
owner-specific relation tables
shared typed edge infrastructure where safe
qualified relation records
MaterialStateRef-backed governance history
ReBAC/ABAC projection stores
capability mechanisms
hybrid
```

No physical implementation is selected. Final whole-logical replay must pressure the integrated model before Physical Model authorization.

## 14. Hardening package

```text
F-H01  no universal semantic Relationship/Edge root
F-H02  no universal RelationRef
F-H03  Reference Contract relation profile
F-H04  direct vs qualified material relation threshold
F-H05  Actor remains contextual; specific role precedence
F-H06  Membership non-implication boundaries
F-H07  Interpersonal Relationship non-governance boundary
F-H08  Responsibility/Stewardship/performer/Participation separation
F-H09  Participation != Contribution
F-H10  Ownership != Possession != Authority/Visibility
F-H11  Authority action-time basis reconstructibility
F-H12  Consent scope/purpose/target/time/material-state binding
F-H13  Agreement n-ary materially specific terms binding
F-H14  Collective state != member personal state
F-H15  relation/projection/source selective Visibility
F-H16  Representation preserves actual Actor + represented party + basis
F-H17  domain governance != technical AuthZ
F-H18  enforcement engine replaceability
F-H19  stale/delayed authorization cannot float indefinitely
F-H20  unknown/conflicting governance remains representable
```

## 15. Reverse mapping

Reverse mapping is deterministic for all current relation/governance owners. Technical AuthZ state maps only to the security/enforcement projection and never replaces the canonical semantic owner.

No generic semantic-free fallback is required.

## 16. Decision integrity

```text
unclassified material decisions        0
unregistered material assumptions      0
rejected candidates without rationale  0
unsafe physical deferrals              0
Domain reopen required                  0
```

## 17. Final local verdict

```text
SLICE F
RELATIONSHIPS / MULTI-ACTOR / GOVERNANCE

PREFERRED
Layered Typed Relations & Governance Model

PASS WITH HARDENING

REOPEN = 0
UNCLASSIFIED = 0
UNRESOLVED STRUCTURAL = 0
A-E REGRESSION FAILURE = 0

REMOTE QA
PENDING
```

The next permitted action after this local content is exact remote Git QA. Canonical ACTIVE/CLOSED status requires a separately gated closure record.