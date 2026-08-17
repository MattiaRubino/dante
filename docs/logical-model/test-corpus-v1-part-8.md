<!-- LIFEOS-CANONICAL-CONTINUATION document="test-corpus-v1.md" follows="test-corpus-v1-part-7.md" -->
> **Canonical continuation of the single Logical Model Test Corpus v1 document.** Earlier corpus families remain active. This continuation adds Slice F — Relationships / Multi-Actor / Governance tests and promotes the relevant A+B+C+D+E carry-forward cases to permanent R3 obligations.

# Slice F — Relationships / Multi-Actor / Governance corpus

## F-REL-01 — Same endpoints, different relation families

Person Anna and Activity A have all of:

```text
Anna requested A
Anna is responsible for A
Anna actually performed A
Anna has Authority to cancel A
```

Expected:

```text
four independently recoverable semantics
no generic edge type as sole semantic owner
```

## F-REL-02 — Direct simple relation remains compact

Person Luca is a member of Household H. No independent membership role/history/governance is material.

Expected:

```text
direct typed Membership relation allowed
no mandatory standalone Membership object
no RelationRef
```

## F-REL-03 — Relation escalates when consequential

Later the exact start/end and role of Luca's Membership determines quorum eligibility for a consequential Decision.

Expected:

```text
Membership becomes materially reconstructible
ScopedRecordRef / MaterialStateRef may address exact state
historical eligible-set basis survives later membership change
```

## F-REL-04 — Interpersonal relation does not create governance

```text
Marco is Mattia's manager
```

Expected:

```text
Interpersonal Relationship established
Authority absent unless separately established
Visibility absent unless separately established
```

## F-REL-05 — Perspective-sensitive friendship

A records B as friend; B has not asserted the inverse.

Expected:

```text
actor-scoped/perspective-sensitive relation representable
no forced symmetry
```

## F-REL-06 — No transitive friendship inference

```text
friend(A,B)
friend(B,C)
```

Expected:

```text
friend(A,C) not inferred
```

## F-COL-01 — Collective continuity across membership change

Household H has Anna and Luca. Sara joins later.

Expected:

```text
same Collective where identity invariants hold
Membership history changes
Collective identity not replaced solely by member-set change
```

## F-COL-02 — Member action not Collective action

Anna individually accepts Proposal P while a member of Collective C.

Expected:

```text
Anna action retained
no automatic Collective Decision/Agreement/Consent
```

## F-COL-03 — Collective bears Responsibility

Collective Household H is responsible for ensuring rent is paid; Anna individually has responsibility for initiating transfer.

Expected:

```text
Collective Responsibility retained separately
Anna individual Responsibility retained separately
other members not rewritten as personally responsible
```

## F-MEM-01 — Member but not participant

Person is member of Team C but not involved in Event E.

Expected:

```text
Membership yes
Participation absent
```

## F-MEM-02 — Participant but not member

External Person joins one Event of Collective C without becoming member.

Expected:

```text
Participation yes
Membership absent
```

## F-MEM-03 — Membership without Authority

Person is member of Collective C but cannot modify Collective schedule.

Expected:

```text
Membership yes
Authority no/absent according to established state
```

## F-MEM-04 — Provider security group is not canonical Membership automatically

SCIM/IdP says Account A belongs to provider Group G.

Expected:

```text
provider membership retained as External/provider state
canonical Membership only if reconciliation/equivalence is established
no automatic Authority
```

## F-PART-01 — Accepted but absent

Anna accepts invitation, then does not attend.

Expected:

```text
response history = accepted
Actual participation absent / established absence only if evidence supports it
no rewrite to declined
```

## F-PART-02 — Declined but attended

Luca declines and later participates.

Expected:

```text
declined response retained
Actual participation retained
```

## F-PART-03 — Participation without Contribution

Person attends meeting but contributes no material work/input.

Expected:

```text
Participation yes
Contribution absent
```

## F-CONTR-01 — Contribution without final performer identity

Anna drafts analysis; Luca performs final submission.

Expected:

```text
Anna Contribution retained
Luca performer retained
no collapse
```

## F-RESP-01 — Responsibility vs expected performer

Manager responsible; analyst expected performer.

Expected:

```text
Responsibility(manager)
expected performer(analyst)
```

## F-RESP-02 — Actual performer differs

Analyst becomes unavailable; Marco performs.

Expected:

```text
Responsibility history retained
expected performer history retained
Actual performer Marco
```

## F-STEW-01 — Steward differs from responsible Actor

Child responsible for taking recycling out; parent carries reminder/monitoring burden.

Expected:

```text
Responsibility Child
Coordination Stewardship Parent
```

## F-STEW-02 — One reminder does not transfer Stewardship

Sara is current Steward. Anna sends one reminder.

Expected:

```text
actual reminder action by Anna
Stewardship remains Sara
```

## F-OWN-01 — Owner vs possessor

Owner lends camera to Luca.

Expected:

```text
Ownership remains owner
Possession becomes Luca
Asset identity unchanged
```

## F-OWN-02 — Ownership does not imply Authority/Visibility

Owner lacks a specific governance/disclosure permission in a bounded workflow.

Expected:

```text
Ownership preserved
Authority/Visibility evaluated separately
```

## F-AUTH-01 — Bounded Authority

Anna may reschedule Event E but may not disclose private medical source S.

Expected:

```text
Authority(reschedule E) yes
Authority(disclose S) absent/no depending on established state
```

## F-AUTH-02 — Historical Authority survives revocation history

```text
T1 A1 effective
T2 Anna validly changes target
T3 A1 revoked
```

Historical query at T2.

Expected:

```text
T2 effect reconstructs A1 as applicable then
current A1 revoked
revoked != never existed
```

## F-AUTH-03 — Technical deny while Domain Authority exists

Anna has Domain Authority but request originates from compromised session/device and security policy denies.

Expected:

```text
Domain Authority yes
technical decision deny
no semantic contradiction
```

## F-AUTH-04 — Technical allow without legitimate Domain Authority

Misconfigured runtime policy allows Principal P to call operation, but domain Authority for effect E is absent.

Expected:

```text
technical allow does not manufacture Domain Authority
canonical effect must not rely solely on allow
```

## F-AUTH-05 — AI optimization does not create Authority

AI ranks one option as best.

Expected:

```text
ranking/proposal retained
Authority absent unless separately established
```

## F-AUTH-06 — Delayed action after revocation

```text
T1 Authority valid
T2 AuthZ allow
T3 Authority revoked
T4 queued effect executes
```

Expected:

```text
T2 allow not permanently sufficient for T4
revalidate or use explicitly valid immutable authorization/effect binding
```

## F-CONS-01 — Consent before action

Anna consents to sharing one photo, but no share has happened.

Expected:

```text
Consent exists
Disclosure/Actual action absent
```

## F-CONS-02 — Withdrawal does not erase historical use

```text
T1 Consent granted
T2 permitted disclosure occurs
T3 Consent withdrawn
```

Expected:

```text
future applicability changed
T1/T2 remain historical truth
```

## F-CONS-03 — Material scope change

Consent applies to scope/version v1. v2 materially expands data/purpose.

Expected:

```text
v1 Consent not auto-applied to v2
```

## F-CONS-04 — Consent != Visibility

Consent allows a use but current product flow has not exposed the data to recipient R.

Expected:

```text
Consent yes
Visibility to R not inferred
```

## F-CONS-05 — Consent != Authority

Person consents to one bounded use but does not grant general governance power.

Expected:

```text
Consent retained
Authority not inferred
```

## F-AGR-01 — Same terms establish Agreement

Anna, Luca and Marco each assent to material terms state T3.

Expected:

```text
one Agreement common-ground record bound to T3
party assent relations all reference T3
```

## F-AGR-02 — Different terms do not establish shared Agreement

Anna assents T3; Luca assents materially different T4.

Expected:

```text
no shared Agreement for T3/T4 pair
```

## F-AGR-03 — Material amendment requires renewed assent

Existing Agreement A on T3. Terms change materially to T4.

Expected:

```text
historical Agreement T3 retained
T4 not agreed until applicable parties assent
```

## F-AGR-04 — Collective Agreement != member Agreement

Collective C validly becomes Agreement party under its governance.

Expected:

```text
Collective party state retained
members not rewritten as personally agreed
```

## F-AGR-05 — Pairwise edges are insufficient

Three parties have pairwise `agreed_with` links but no shared material terms binding.

Expected:

```text
cannot conclude Agreement
```

## F-VIS-01 — Endpoints visible, relation hidden

Person Anna and Event E visible; Participation(Anna,E) hidden.

Expected:

```text
both endpoints visible
relation not exposed
```

## F-VIS-02 — Relation existence visible, kind hidden

Recipient may know Person A is connected to Person B but not whether relation is partner/caregiver/etc.

Expected:

```text
bounded relation projection possible
kind remains hidden
```

## F-VIS-03 — Result visible, private source hidden

Private therapy Event causes shared `Unavailable 18:30–19:30` projection.

Expected:

```text
projection visible
source Event hidden
```

## F-VIS-04 — Relation visible, Evidence hidden

Interpersonal relation is visible but private supporting message history is not.

Expected:

```text
relation visible
Evidence/Provenance hidden
```

## F-VIS-05 — Revocation does not erase knowledge history

Recipient viewed data at T1; Visibility revoked at T2.

Expected:

```text
future LifeOS exposure disabled
historical disclosure/view not rewritten
human knowledge not claimed erased
```

## F-REP-01 — Actor differs from represented party

Assistant Luca schedules for Anna.

Expected:

```text
actual Actor Luca
represented party Anna
```

Forbidden:

```text
Anna recorded as actual Actor
```

## F-REP-02 — Representation without Authority

Luca claims to act for Anna but lacks applicable Authority.

Expected:

```text
Representation/attempt attribution may be recorded
legitimacy/effect not inferred
```

## F-REP-03 — Principal differs from Actor

AI agent acts semantically; service Principal authenticates request.

Expected:

```text
Actor AI
Principal service credential
```

## F-REP-04 — Authority expires after valid represented action

T1 delegated Authority valid; T2 representative acts; T3 delegation revoked.

Expected:

```text
T2 action remains reconstructible as valid then
current Authority revoked
```

## F-PRIV-01 — Private source used for safe consequence

AI may use authorized private health constraint to produce shared `not available` result.

Expected:

```text
internal use allowed under applicable governance
shared consequence bounded
private source not disclosed
```

## F-PRIV-02 — Identity linkage remains hidden

Private reconciliation proves two provider records belong to same Person, preventing duplicate participant/resource counting.

Expected:

```text
correct internal computation
identity linkage not exposed without Visibility
```

## F-UNK-01 — Unknown Membership

Provider data incomplete.

Expected:

```text
unknown/unresolved Membership
!= explicit non-member
```

## F-UNK-02 — No applicable Authority grant found

Expected:

```text
enforcement may fail closed
but domain state is not rewritten as explicit prohibition unless established
```

## F-CONFLICT-01 — Conflicting relationship assertions

Two sources disagree whether A is caregiver for B.

Expected:

```text
conflict retained/reconciled through Evidence/Provenance/Authority
no newest-source automatic winner
```

## F-CONFLICT-02 — Conflicting Authority claims

Two providers assert different governance roles.

Expected:

```text
both assertions/evidence retained as applicable
canonical Authority not selected by provider rank alone
```

# Slice F mutation matrix

Reject implementations that introduce:

```text
MUT-F01  every relation -> generic Relationship row
MUT-F02  generic relation_type becomes semantic fallback
MUT-F03  create universal RelationRef
MUT-F04  Actor gets wrapper identity
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
MUT-F27  current Authority used for historical action
MUT-F28  revoked Consent erases historical permitted use
MUT-F29  endpoint Visibility exposes relation
MUT-F30  relation Visibility exposes private Evidence
MUT-F31  technical ALLOW creates domain Authority
MUT-F32  technical DENY deletes domain Authority
MUT-F33  security group = domain Membership automatically
MUT-F34  AI confidence/capability = Authority
MUT-F35  queued ALLOW remains permanently valid after governance change
MUT-F36  newest relation assertion wins universally
MUT-F37  AuthZ tuple store becomes canonical domain source truth
MUT-F38  policy-engine Principal becomes semantic Actor identity
```

Expected:

```text
38 / 38 REJECTED
```

# Slice F counterfactual matrix

The model must distinguish:

```text
CF-F01  member / participant
CF-F02  participant / contributor
CF-F03  responsible / performer
CF-F04  responsible / steward
CF-F05  owner / possessor
CF-F06  can see / can govern
CF-F07  can govern / can see private basis
CF-F08  Consent exists / action happened
CF-F09  Visibility exists / recipient viewed
CF-F10  Agreement / individual Consent
CF-F11  Collective Agreement / member personal Agreement
CF-F12  member action / Collective action
CF-F13  actual Actor / represented party
CF-F14  Representation / Authority
CF-F15  historical Authority / current Authority
CF-F16  Consent v1 / materially expanded target v2
CF-F17  endpoint Visibility / relation Visibility
CF-F18  relation Visibility / Evidence/source Visibility
CF-F19  Principal / Actor
CF-F20  technical allow / domain Authority
CF-F21  technical deny / domain absence of Authority
CF-F22  unknown relation / explicit no relation
```

Expected:

```text
22 / 22 DISTINGUISHABLE
```

# Slice F simple / worst-case pair

## Simple

```text
Household H
Anna member
Luca member
Anna responsible for one chore
```

Expected:

```text
compact typed relations
no graph bureaucracy
no mandatory policy-engine objects
```

## Worst case

```text
shared household + external caregiver
private health source
Collective membership changes
Agreement on shared terms
Consent for bounded disclosure
Representation by AI/service
Authority delegated then revoked
relation existence visible but kind hidden
shared unavailable projection from private source
queued action checked before governance change
historical audit after provider correction
```

Expected:

```text
one shared reality
specific relation families preserved
actual Actor / represented party / Principal separate
historical material governance basis reconstructible
Visibility bounded at projection/relation/source level
Consent/Agreement/Authority independent
runtime AuthZ replaceable
no universal Relationship root
```

# Integrated A+B+C+D+E carry-forward replay

The following cumulative obligations are now permanently replayed through F:

```text
ABCDE-PRIV-01 private health cause -> shared unavailable result          PASS
ABCDE-PRIV-02 private identity/source link affects feasibility           PASS
Resource Allocation of Person != Consent/Agreement/Responsibility        PASS
shared Decision/Allocation != every member endorsement                   PASS
Authority to allocate/claim != Ownership/Possession                      PASS
Allocation/Claim visibility != private Requirement/source visibility     PASS
different actors see different projections over one shared reality       PASS
historical actor participation/access != current Authority/Visibility    PASS
```

# R3 promotion

The following Slice F families are permanent `R3 WHOLE-LOGICAL` obligations:

```text
Agreement terms/material-state binding
Authority action-time reconstruction
Consent withdrawal/material-scope reconstruction
relation-level selective Visibility
Representation actual Actor / represented party / basis
Domain governance != technical authorization
stale/delayed authorization handling
Membership/Collective non-implication boundaries
```

No Slice F test authorizes a Physical Model or runtime AuthZ implementation.