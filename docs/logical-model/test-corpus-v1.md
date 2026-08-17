# LifeOS Logical Model Test Corpus v1

**Status:** Stage-0H hardened normative foundation + Slice-A + Slice-B regression packages  
**Date:** 2026-08-17  
**Purpose:** minimum adversarial simulation corpus for Logical Model slices and final integrated regression

This corpus is a **minimum seed**, not a closed test suite. Every slice must add fresh scenarios that were not used to design the candidate representation.

The corpus intentionally mixes ordinary personal use, multi-actor use, provider conflict, specialist pressure, large history and simple cases.

---

## A. Identity / reference scenarios

### TC-A01 — Person without Account
A friend matters to the user's life, participates in an Event and later receives a Responsibility, but never creates a LifeOS account.

Must preserve:

```text
Person identity
!= Account
!= Actor capability by default
```

### TC-A02 — Account later linked to existing Person
An already-known Person later becomes a LifeOS user.

The logical model must not create a second human identity merely because an Account now exists.

### TC-A03 — Living Referent changes caregiver
One dog remains the same Living Referent while caregiver, responsible Actor, owner and Place change over time.

### TC-A04 — Asset changes possession
A camera remains one Asset while owner, possessor, storage Place and Resource role change.

### TC-A05 — Content Artifact moves provider
A document moves from one provider/storage object to another while its LifeOS Content Artifact identity remains continuous where materially the same artifact is preserved.

### TC-A06 — Place provider churn
A Place is first created manually, then matched to one external place provider, later rematched after provider ID/schema changes.

Provider identity must not become canonical Place identity.

### TC-A07 — Collective membership changes
A household/team-like Collective retains identity while ordinary membership changes over time.

The current member set must not become the Collective's identity.

### TC-A08 — Same provider identifier shape, different semantic owner
A provider exposes opaque IDs for a person profile, calendar event, place and file.

A shared technical reference mechanism must not imply that all four are one semantic superclass or that provider IDs become LifeOS canonical identities.

### TC-A09 — Person identity merge then correction
Two Person records are merged after strong evidence, then later evidence shows the merge was wrong.

The representation must support explaining the historical identity assertion and subsequent correction rather than silently rewriting all prior references.

### TC-A10 — Role without wrapper identity
The same Person is Subject in one context, Actor/recorder in another and Resource candidate in a third.

No independent Subject/Actor/Resource wrapper identity may be required merely to reference the roles.

---

## B. Intention / execution scenarios

### TC-B01 — Possibility remains inactive
"Maybe go to Japan" is retained for years, explored intermittently and never becomes a Goal.

No fake execution lifecycle may be required.

### TC-B02 — Possibility matures into Goal
A Possibility is explored, then intentionally adopted as a Goal, then receives a Plan.

Historical Possibility state must remain reconstructible; later adoption must not retroactively retype it.

### TC-B03 — Goal abandoned
A real Goal existed, had Activities and was later abandoned.

The system must not rewrite history into "it was only a Possibility".

### TC-B04 — Proposal rejected
LifeOS proposes an option; the user rejects it.

Proposal != Decision != Goal.

### TC-B05 — Decision changes Plan
A user decides to keep the same Goal but replaces the execution Plan entirely.

Goal identity must not depend on Plan identity.

### TC-B06 — Simple standalone Activity
"Buy milk" requires no Goal, Program or Project container.

Simple-user compactness must survive.

---

## C. Time / recurrence / reality scenarios

### TC-C01 — Recurring routine across DST
A recurring morning routine spans daylight-saving transitions and travel across time zones.

The logical representation must distinguish recurrence policy, intended local-time semantics, generated occurrence and current schedule placement.

### TC-C02 — Moved recurring instance
One recurring instance is moved to another day without changing the source recurrence rule.

The instance must remain identifiable as the same generated occurrence/exception context.

### TC-C03 — Deleted/skipped occurrence
One occurrence is intentionally skipped while future recurrence remains intact.

### TC-C04 — Schedule changed four times
An Activity is scheduled at 09:00, then 11:00, then tomorrow, then Friday.

Materially relevant prior accepted schedule placements must be reconstructible where consequence requires.

### TC-C05 — Scheduled but not done
A two-hour Session was scheduled and time elapsed, but the user says it did not occur.

```text
Schedule != Actual
elapsed calendar time != proof of execution
```

### TC-C06 — Done outside schedule
An Activity is actually completed at a different time from every scheduled Session.

### TC-C07 — Effort without Outcome
Two hours of study occurred, but there is no evidence that language proficiency improved.

```text
Actual effort != Outcome != Goal progress automatically
```

### TC-C08 — Outcome without planned path
A desired Outcome occurs unexpectedly without the intended Plan being executed.

---

## D. Observation / evidence / correction scenarios

### TC-D01 — User assertion vs device reading
A user reports 7h sleep while a device reports 6h12m.

The model must retain both source assertions and permit unresolved conflict.

### TC-D02 — Provider correction
A provider first reports one value, later corrects it.

Correction must not silently erase the fact that the earlier value was previously recorded/used.

### TC-D03 — AI inference not confirmed
AI infers that the user prefers evening workouts from historical behavior.

The inference may remain evidence/proposal/evaluation context but must not become a confirmed user Preference automatically.

### TC-D04 — Evidence supporting Decision
Multiple observations and documents support a Decision.

Evidence != Decision and Provenance != Evidence.

### TC-D05 — Source disappears
An external provider deletes or becomes unavailable after LifeOS already derived materially used information from it.

The model must preserve enough lineage/history to explain the existing canonical state where required.

### TC-D06 — Same source, different interpretation
The same document is interpreted differently after a parser/model improvement.

Source identity, extraction version, interpretation and current accepted state must remain distinguishable where material.

---

## E. Multi-actor / governance scenarios

### TC-E01 — Shared Possibility, different opinions
One shared Possibility concerns several people. One supports it, one opposes it, one has not seen it.

Shared object != shared endorsement.

### TC-E02 — Shared Decision with dissent
A group reaches an accepted Decision while one participant dissents.

Decision state must not erase Participation/opinion history.

### TC-E03 — Responsibility transfer
A Responsibility moves from Person A to Person B.

Historical accountability must remain reconstructible.

### TC-E04 — Expected vs actual participant
Person A is expected to perform an Activity; Person B actually performs it.

Responsibility/expectation != Participation/Actual.

### TC-E05 — Authority revoked
An Actor previously had Authority over a shared reality and later loses it.

Historical actions remain attributable without implying current Authority.

### TC-E06 — Private source, shared consequence
A private health fact makes the user unavailable. Others may see "unavailable" but not the private cause.

```text
Visibility(shared consequence)
!= Visibility(private source)
```

### TC-E07 — External participant
A meeting includes people who do not use LifeOS.

They remain representable without fake Accounts.

### TC-E08 — Ownership vs possession split
One Person owns an Asset while another possesses/uses it temporarily and a third is responsible for maintenance.

---

## F. Resources / capacity / values scenarios

### TC-F01 — Resource requirement unmet
A Plan requires a camera, car and two hours of daylight; one resource is unavailable.

Requirement, Resource identity, Availability and Allocation must not collapse.

### TC-F02 — Competing allocations
Two Plans compete for the same vehicle/time/capacity.

A logical design must express contention without pretending that planning conflict is actual physical impossibility in all cases.

### TC-F03 — Quantity with stable unit conversion
Distance is recorded in km and miles with a stable conversion basis.

### TC-F04 — MonetaryAmount conversion
EUR and USD amounts are compared using a rate valid at a specific basis/time.

Currency conversion must not be treated as timeless ordinary unit equivalence.

### TC-F05 — Capacity changes historically
A person's available weekly capacity changes during travel, illness or work peak.

Past planning rationale must remain explainable where material.

---

## G. Provider / integration / reconciliation scenarios

### TC-G01 — Calendar recurring-instance remap
An imported recurring calendar event has a parent series, one moved instance and one cancelled instance.

Provider recurrence identity must be reconcilable without replacing LifeOS recurrence/occurrence semantics.

### TC-G02 — Duplicate provider records
Two providers describe what appears to be the same real-world Event.

The system must allow match proposals and unresolved duplication without forced merge.

### TC-G03 — Provider ID replacement
A provider replaces an external identifier while the underlying external record is materially continuous.

### TC-G04 — Sync arrives out of order
A correction/change event arrives before an older provider payload because of asynchronous sync.

Recorded order != effective real-world order automatically.

### TC-G05 — Partial provider payload
A provider omits fields LifeOS previously knew.

Missing payload field must not automatically mean real-world fact is now absent.

### TC-G06 — Integration removed
A user disconnects a provider but keeps LifeOS-native state derived from previously imported information where retention is authorized.

---

## H. Specialist-boundary scenarios

### TC-H01 — Financial pending -> posted
A pending bank transaction disappears and a linked posted transaction appears with changed amount/name/date.

Test requirement:

```text
specialist Transaction lifecycle != generic Observation
provider lifecycle != universal LifeOS kernel lifecycle
```

### TC-H02 — Refund/correction
A posted financial transaction is later offset/refunded.

The general kernel must not invent accounting semantics it does not own.

### TC-H03 — Physical inventory discrepancy
Recorded stock says 10; physical count says 8; applying an adjustment creates a movement/history record in the specialist system.

Count Observation != Movement lifecycle.

### TC-H04 — Clinical observation
A health measurement can be represented/linked without forcing all clinical resource semantics into the LifeOS kernel.

### TC-H05 — Regulated specialist validity
An external professional document has legal/clinical validity that LifeOS may preserve as source/provenance but not recreate by editing its content.

---

## I. Scale / longevity scenarios

### TC-I01 — Ten years of recurrence
A daily routine produces thousands of occurrences and exceptions.

The logical model must not require eager permanent materialization of infinite future occurrences.

### TC-I02 — High-volume observations
A wearable contributes hundreds of thousands of observations over time.

The representation must not structurally require loading all history to answer current-state questions.

### TC-I03 — Large AI candidate set
AI generates 10,000 transient candidate futures during exploration.

Not every candidate becomes a persistent Possibility.

### TC-I04 — Long-lived relationship history
Ownership, possession, Authority and Responsibility change repeatedly across years.

Historical reconstruction must remain possible without treating current relations as the whole truth.

### TC-I05 — Provider migration
One integration provider is replaced by another without rewriting LifeOS native identities.

---

## J. Negative/product-anti-pattern scenarios

### TC-J01 — Calendar says it happened
A scheduling product treats elapsed calendar time as completed work.

LifeOS must reject the inference unless Actual/Evidence supports it.

### TC-J02 — Everything is a page/property
A flexible database can express arbitrary properties, but a required LifeOS semantic owner must not disappear into untyped canonical metadata.

### TC-J03 — Everything is a generic edge
A graph representation can link any two objects, but accepted relationship families must remain specifically typed and constrained.

### TC-J04 — Provider object becomes domain identity
A calendar event ID, file ID or place ID must not automatically become LifeOS canonical identity.

### TC-J05 — One universal status field
Different domain owners cannot share one generic lifecycle merely because UIs use labels such as open/active/done.

---

## K. Product Reality / cross-domain retrieval scenarios

These scenarios validate that LifeOS can connect relevant life context without turning every requested capability into a new Domain primitive.

### TC-K01 — Reading history -> later recommendation
The user records books, ratings/reviews, abandoned books and explicit likes/dislikes over years.

Later the user asks for a reading recommendation.

Must distinguish:

```text
user-declared evaluation/preference evidence
observed reading history
AI-derived taste/profile
current recommendation
```

AI inference must not rewrite the user's own historical statements.

### TC-K02 — Photography interest + eclipse discovery
LifeOS knows the user has an established photography interest. External data reveals a future eclipse relevant to the user's likely location/time.

The eclipse may become a `Possibility` worth surfacing, but not automatically a Goal, Decision, Plan or calendar commitment.

### TC-K03 — Photography equipment feasibility
For the same eclipse, LifeOS knows the user's tracked camera/lenses/filters/tripod and can compare them with activity requirements.

Must preserve:

```text
Asset identity
Resource role
Requirement
eligibility
availability
allocation
actual use
```

A suitable Asset is not automatically allocated or actually used.

### TC-K04 — Travel intention -> Rome plan
The user says they would like to go to Rome.

LifeOS must be able to keep this vague initially, evaluate constraints/options and later create more concrete Goal/Decision/Plan/Activities/Schedule only when justified.

### TC-K05 — Persistent personal fact becomes relevant later
A materially relevant user fact is established in one context. Months later a different workflow needs it.

The system must be able to retrieve the authorized, current/relevant state without treating raw chat history as the only memory source.

### TC-K06 — Health-relevant fact -> later diet planning
A health/specialist-relevant fact exists with source/history/visibility context. Later the user asks for food/diet planning.

LifeOS must use the relevant authorized context while preserving specialist/safety boundaries and not flattening the fact into an untyped Person property.

### TC-K07 — Weight/goal history -> later renewed goal
A user has prior weight Observations, previous Goals, plans, Actual behavior, Outcomes and periods where context changed. Months later they want to lose weight again.

The new evaluation may use history without rewriting old Goal/Plan/Outcome identity or claiming causation unsupported by Evidence.

### TC-K08 — Cross-domain knowledge retrieval without global leakage
An item learned in one life domain becomes useful in another. The retrieval engine may use it only if materially relevant and visible/authorized in the new context.

```text
stored != always surfaced
known internally != disclosure permitted
past fact != current fact automatically
AI inference != confirmed fact
```

---

## L. Mandatory mutation and counterfactual seed tests

### TC-L01 — Remove native Person identity
Attempt to model human continuity only with Account/contact/provider identities.

Expected: FAIL.

### TC-L02 — Universal Entity registry becomes semantic root
Use one technical reference registry and treat its common ID/type as proof that every referent is semantically one `Entity` kind.

Expected: FAIL.

### TC-L03 — Universal generic relation
Replace typed roles/relationships with `from -> related_to -> to` plus optional text/JSON.

Expected: FAIL.

### TC-L04 — Current-only state
Keep only the latest Responsibility/Schedule/provider mapping and overwrite previous accepted state.

Expected: FAIL where material history is required.

### TC-L05 — Provider-ID substitution
Use an external/provider ID as canonical Person/Asset/Place/Artifact identity.

Expected: FAIL.

### TC-L06 — Per-user duplication of shared object
Represent one shared Asset/Collective/Event/other reality as separate canonical copies solely because multiple actors view it.

Expected: FAIL when shared canonical identity is required.

### TC-L07 — Scheduled + done vs scheduled + not done
The representation must distinguish both without a derived guess.

### TC-L08 — Declared preference vs AI inference
Both may mention the same topic, but they must remain epistemically distinguishable.

### TC-L09 — Same Asset changed possession vs replacement Asset
Ordinary custody change preserves identity; physical replacement may require a different Asset identity.

### TC-L10 — Same Living Referent changed caregiver vs replacement organism
Care relation change preserves identity; a genuinely different organism must not inherit prior identity because name/container/owner is the same.

### TC-L11 — Same Artifact provider migration vs independent fork
Storage migration may preserve Artifact identity; an independent content lifecycle may create a new Artifact.

### TC-L12 — Existing Person gains Account vs new Person
Linking an Account to a represented human must not look identical to creating a genuinely new human referent.

---

# Mandatory high-value query corpus

Each integrated candidate must demonstrate logical feasibility for at least these questions:

1. What is currently planned for this Goal, and what was planned one month ago?
2. What actually happened versus what was scheduled?
3. Which source supports this canonical fact, and has that source been corrected?
4. What did LifeOS believe/accept at time T versus what is accepted now?
5. Who was responsible at time T, who actually participated, and who had Authority?
6. What can Actor X see without exposing private source causes?
7. Which provider records map to this LifeOS referent, including superseded mappings?
8. Which Possibilities have never been adopted as Goals?
9. Which Goal was created from a prior Possibility without retyping historical records?
10. Which recurring instance was moved or skipped without changing the recurrence policy?
11. Which resources are required/allocated and which are actually available?
12. What evidence and provenance contributed to a Decision/Outcome/Evaluation?
13. Can a simple appointment exist without artificial Goal/Plan scaffolding?
14. Can a specialist transaction/inventory record be linked without pretending it is a generic Observation lifecycle?
15. Can the current state be answered without replaying the entire lifetime history in application memory?
16. Which native referent does this typed role/reference point to, without a semantic Entity superclass?
17. Which external/provider identifiers currently or historically mapped to this LifeOS identity?
18. Can we explain an identity merge/split/correction without pretending the corrected mapping was always known?
19. Which personal facts/preferences are explicit, inferred, historical, current, source-backed or unresolved?
20. Which relevant cross-domain context may be used for this request under current Visibility/Authority?
21. Can LifeOS explain why a recommendation/opportunity was surfaced without converting the recommendation into user intent?
22. Can an equipment/resource feasibility check distinguish requirement, candidate, selection and actual use?

---

# Regression rule

A scenario that passes once remains in the regression set for every later slice whose changes could affect it.

If a later slice invalidates an earlier PASS, the earlier slice is reopened at the **logical** level first. Domain Atlas reopen requires the separate evidence bar in `validation-methodology-v1.md`.

Every material candidate must also use the mutation/counterfactual families defined in `traceability-and-regression-ledger-v1.md`. Product Reality examples are pressure tests and must be classified as Domain coverage, logical requirement, capability gap, specialist boundary or genuine targeted reopen evidence rather than being accepted as ontology by request.

---

## M. Slice A accepted regression expansion

These tests were added after the broad Slice-A benchmark and are permanent R3 regression pressure.

### TC-M01 — Opaque native key format changes

A future physical/API migration changes the serialized native identifier format.

Required:

```text
semantic owner/type remains recoverable through the contract
no business/domain logic depends on parsing the old format
```

### TC-M02 — Same external ID in different scopes

Two provider tenants/accounts expose the same raw external identifier string for different external records.

Required:

```text
ExternalRef includes sufficient provider/source scope
no false native merge
```

### TC-M03 — Pairwise security IDs for one Person

The same human authenticates through security contexts that legitimately expose different subject IDs.

Required:

```text
multiple security/provider identities may map to one Person
raw ID count != Person count
```

### TC-M04 — Provider migration bridge

A provider changes identifier namespace or an application transfers ownership and supplies an explicit migration/transfer mapping.

Required:

```text
old ExternalRef
-> migration/reconciliation evidence
-> new ExternalRef
-> same NativeRef where justified
```

Native identity must not be replaced merely because provider identity changes.

### TC-M05 — Wrong identity merge after six months

Two Person identities were resolved as one; hundreds of historical records were subsequently queried through the current resolution. New evidence proves the merge was wrong.

Required:

```text
reconciliation can be revoked/corrected
historical anchors remain addressable
records with uncertain redistribution may remain unresolved
```

### TC-M06 — Public correlation leakage

One internal Person appears in a work context and a private health context.

Required:

```text
shared internal identity
!= globally exposed identical handle
!= permission to reveal cross-context linkage
```

### TC-M07 — New native owner added years later

A future validated Domain owner gains independent native identity.

Required:

```text
new owner can participate in NativeRef/reference contracts
existing Person/Asset/Place/etc. identity semantics remain unchanged
```

### TC-M08 — Resource target without native identity

A Plan needs a fungible supply/service/pool that satisfies a Resource Requirement but does not independently justify kernel native identity.

Required:

```text
Resource target contract supports bounded non-NativeRef representation
no fake Entity/native identity is manufactured
```

### TC-M09 — Native identity vs version

A Decision cites the state of an Asset/Person/Artifact as known at T1; current state at T2 differs.

Required:

```text
NativeRef remains same referent
material state/version reference remains distinguishable
```

### TC-M10 — Friendly alias reused

A human-friendly label/key/name is retired and later reused for a different referent.

Required:

```text
alias/name reuse != native identity reuse
historical references remain resolvable to original native identity
```

### TC-M11 — Provider merge heuristic conflicts

Provider A and Provider B expose identifiers that look equivalent but maintain conflicting source truth.

Required:

```text
possible match remains reconciliation state
provider similarity does not force canonical merge
```

### TC-M12 — Reference-contract invalid target

A generic technical NativeRef points to a valid native identity whose owner family is not eligible for the containing semantic slot.

Required:

```text
technical target exists
BUT canonical relation is rejected by Reference Contract
```

### Additional Slice-A high-value queries

23. Given a raw/native handle, can the system recover the native owner family without parsing vendor-specific ID encoding?
24. Can two identical external-ID strings in different scopes map to different native identities safely?
25. Can one Person retain multiple Account/Principal/provider identities over time without identity duplication?
26. Can a current redirect/resolution be followed while still retrieving the exact historical identity reference originally recorded?
27. Can a wrong identity merge be reversed without a database-wide semantic rewrite?
28. Can a Reference Contract reject a technically valid but semantically ineligible NativeRef target?
29. Can a role target be represented when it validly lacks independent native identity?
30. Can an API/security layer expose context-scoped handles without duplicating the underlying native referent?

### Slice-A regression result at acceptance

```text
TC-M01..M12
PASS / PASS WITH explicitly stage-bound Slice-D/F dependencies

NEW DOMAIN REOPEN EVIDENCE
0
```

---

## N. Slice B accepted regression expansion

These scenarios are permanent Slice-B regression pressure and replay Slice-A identity/reference invariants where applicable.

### TC-N01 — Possibility adoption without retyping

A travel Possibility is retained for six months, evaluated repeatedly, then explicitly adopted as a Goal.

Required:

```text
Possibility P1 remains historically P1
Goal G1 is distinct identity
adoption/origin link connects them
pre-adoption history != Goal history
```

### TC-N02 — Possibility dismissed, later similar Goal

A Possibility is dismissed. Two years later the user adopts a materially similar Goal.

Required: similarity does not force identity equality or rewrite the earlier dismissal.

### TC-N03 — Goal abandoned then reconsidered

A Goal genuinely existed and was abandoned. Later the user reconsiders the same broad future.

Required: abandoned Goal history remains Goal history; later candidate/adoption identity is evaluated explicitly.

### TC-N04 — Minor Plan revision vs replacement Plan

Plan A changes one optional Activity and moves one review point. Later, a materially different strategy is adopted.

Required:

```text
minor revision may preserve Plan A identity
materially different strategy may create Plan B
Plan B links to predecessor/replacement relation
Goal identity may remain unchanged
```

### TC-N05 — One Plan supports multiple Goals

A health Plan supports fitness, weight and race-performance Goals.

Required: no one-parent hierarchy; support relation remains explicit.

### TC-N06 — Scheduled Activity vs Event

An Activity receives a fixed calendar placement. A separate appointment Event also exists at an exact time.

Required: exact scheduling does not retype Activity into Event.

### TC-N07 — Routine occurrence skipped

A Routine remains active while one generated occurrence is skipped and another is moved.

Required:

```text
Routine lifecycle unchanged by default
occurrence disposition independent
future recurrence remains intact
```

### TC-N08 — Milestone date passes without attainment

A milestone target date passes but the required criterion/evidence is not satisfied.

Required: date passage != attainment.

### TC-N09 — Proposal withdrawn without effect

An AI/user Proposal is shared, reviewed and then withdrawn before any target change.

Required: Proposal history persists; no Decision/effect is fabricated.

### TC-N10 — Request acknowledged but not fulfilled

A user requests a document from another person. The recipient acknowledges the Request but has not supplied the document.

Required:

```text
acknowledged != fulfilled
fulfilled != Actual automatically without owning reality semantics
```

### TC-N11 — Decision with zero effects

A group explicitly decides to keep the current Plan unchanged.

Required: Decision exists despite zero target mutation.

### TC-N12 — One Decision, multiple effects

A travel Decision authorizes a new Plan, several Activities and selected reservations/allocations.

Required: one Decision may link to multiple effects without becoming those effects.

### TC-N13 — Approval becomes stale after material edit

Plan candidate V3 is approved. Before activation, a material revision creates V4.

Required:

```text
approval of V3 != approval of V4 automatically
material-equivalence/applicability is explicit
```

### TC-N14 — Replacement Plan preserves governed history

Plan A governed two months of execution. It is replaced by Plan B.

Required: past execution remains attributable to Plan A/material state; current plan lookup returns Plan B.

### TC-N15 — Universal status projection challenge

Goal, Plan, Activity, Proposal and Routine are all displayed in one UI list.

Required: UI may derive normalized labels, but canonical owner lifecycle cannot be replaced by one universal status enum.

### TC-N16 — Temporal order without Dependency

Activity A is scheduled before Activity B only for convenience.

Required: no Dependency exists unless true prerequisite contingency is asserted.

### TC-N17 — Dependency current blocked state changes

B depends on milestone M. M becomes attained, then later attainment is corrected/revoked under evidence/version rules.

Required: current blocked/satisfied view is recomputed from applicable states; stale stored flag is not canonical truth.

### TC-N18 — Conditional Policy activation proposes change

A policy says: after two missed study Activities, propose a lighter revised Plan.

Required:

```text
policy activation != Decision
proposal != Plan replacement
later Decision/effect follows owning semantics
```

### TC-N19 — AI candidate ranked highly but never adopted

AI repeatedly recommends an opportunity and assigns high relevance.

Required: ranking/confidence != Goal adoption/preference/Decision.

### TC-N20 — Simple synchronous request without semantic ceremony

The user says: "Move this Activity to 16:00" and has authority over it.

Required: LifeOS may execute the bounded requested change without mandatory standalone Request+Proposal+Decision records unless independent lifecycle/history semantics require them.

Material change history still follows Schedule/Version rules where applicable.

### TC-N21 — Execution governed by historical Plan state

A Routine/Activity executes under Plan material state V2. Plan later changes to V3.

Required: later analysis can identify that the execution was governed by V2 where consequence requires.

### TC-N22 — Slice-A reference regression

Goal, Plan, Activity, Proposal and Decision records are referenced polymorphically by technical infrastructure.

Required:

```text
technical addressability != universal WorkItem/Entity ontology
Reference Contract still restricts semantic eligibility
NativeRef != Version
```

### Additional Slice-B high-value queries

31. Which retained Possibilities were never intentionally adopted?
32. Which Goal originated from a prior Possibility without retyping it?
33. Which Plans currently support a Goal, and which supported it at T?
34. Which Plan materially governed a historical execution/occurrence?
35. Which Plan replaced or continued another while Goal identity remained stable?
36. Which Proposal/Request/Decision targeted which material state/version?
37. What was proposed, what was decided and what effect actually followed?
38. Which Decisions had zero effects?
39. Which effects were produced under an already-authorized Conditional Policy rather than a fresh Decision?
40. Which Dependencies currently block a target, and from which prerequisite state is that derived?
41. Was a Milestone target date passed without semantic attainment?
42. Can one mixed UI/search projection show useful normalized status without making it canonical owner lifecycle?

### Slice-B regression result at acceptance

```text
TC-N01..N22
PASS / PASS WITH explicitly stage-bound Slice-C/D/F dependencies

SLICE-A REGRESSION FAILURE
0

NEW DOMAIN REOPEN EVIDENCE
0
```

---

## O. Integrated A+B cumulative regression expansion

These tests were added because the first mandatory cumulative checkpoint found issues that local Slice-A and Slice-B validation did not fully expose in isolation. They remain permanent regression pressure for every later slice that touches shared identity/reference/history/governance mechanisms.

### TC-O01 — Canonical Activity vs transient suggested action

AI proposes `call the mechanic tomorrow` during exploration. The user does not retain/adopt it. Later the user explicitly creates `Call mechanic` as an Activity.

Required:

```text
transient suggestion != canonical Activity
canonical persisted Activity -> stable LR-01 identity
```

The system must avoid both false persistence and storage-driven identity loss.

### TC-O02 — Canonical Event vs transient/import candidate

A provider payload looks event-like but remains unresolved/import-candidate state. Later reconciliation establishes a canonical Event.

Required:

```text
provider/transient candidate != Event automatically
canonical Event identity != provider ExternalRef
canonical persisted Event -> LR-01
```

### TC-O03 — Milestone address without NativeRef promotion

A Decision and Criterion both need to reference a persistent Milestone `Design approved`.

Required:

```text
Milestone may use ScopedRecordRef
Milestone does not become native referent/Entity merely because it is addressable
Reference Contract still constrains valid target semantics
```

### TC-O04 — Decision record address vs Decision material state

A materialized Decision D1 is later corrected/superseded. Another record must refer to:

1. the Decision semantic record itself; and
2. the material state of D1 that was reviewed at T.

Required:

```text
ScopedRecordRef(D1)
!= MaterialStateRef(D1, state-at-T)
```

Exact MaterialStateRef mechanism remains Slice D.

### TC-O05 — Direct personal instruction vs unauthorized shared mutation

Case A:

```text
user: "Move my private Activity to 16:00"
applicable governance: user controls it
```

Case B:

```text
user: "Move the company-wide Event to 16:00"
applicable governance: user lacks Authority
```

Required:

```text
explicit instruction may remove redundant confirmation in A
same linguistic form does not manufacture Authority in B
Request/instruction != Authority / Consent
```

### TC-O06 — Dependency on existence vs attainment

Activity A depends on Milestone M being **attained**, not merely existing.

Required:

```text
ReferenceAddress(M)
+
facet = attainment
+
condition = attained
```

The model must distinguish:

```text
M exists
!= M attained
```

without introducing one universal predicate language.

### TC-O07 — No standalone Request/Decision, but audit survives

The user directly instructs a permitted personal schedule change. No standalone Request or Decision record is materialized.

Required:

```text
no standalone semantic-act record
!= no history
```

Where consequential, later reconstruction can still identify the changed target state, actor/source, direct-instruction basis and applicable chronology under Slice-D/F mechanisms.

### TC-O08 — Possibility maturation lineage vs retyping

Possibility P1 is adopted into Goal G1.

Candidate A stores the same row and changes `kind=goal`.
Candidate B preserves P1 and G1 with typed adoption/origin lineage.

Required:

```text
Candidate A FAIL
Candidate B PASS
pre-adoption history remains truthful
```

### TC-O09 — Plan revision vs distinct replacement lineage

Plan A receives one ordinary operational edit, then months later strategy changes materially and Plan B replaces it.

Required:

```text
ordinary edit may remain Plan A material revision
Plan B may be distinct identity
Plan B --replacement/continuation--> Plan A
replacement lineage != Version identity automatically
```

### TC-O10 — Mechanism/technology reconsideration after new gap

A cumulative checkpoint exposes a representation gap in a previously accepted shared mechanism.

Required procedure:

```text
reopen current candidate set
reconsider strongest previously rejected-but-not-logically-impossible alternative
search for new plausible mechanisms
refresh current external structural/negative evidence where material
re-score trade-offs under new constraints
explicitly verdict RETAIN / HARDEN / REPLACE / BLOCKED
```

Expected failure:

```text
"keep current design because it already passed"
```

is not valid evidence.

### Integrated A+B high-value queries

43. Given a ReferenceAddress, which address space is it: NativeRef, ScopedRecordRef, MaterialStateRef or ExternalRef?
44. Can a Reference Contract reject a resolvable address because its variant/owner/facet is semantically ineligible?
45. Can a materialized Milestone/Proposal/Request/Decision be referenced stably without promoting it to native referent identity?
46. Can a caller distinguish a semantic-record address from the material state/version of that same record?
47. Can LifeOS determine whether an explicit instruction is sufficient to act without treating the instruction itself as Authority?
48. Can a Dependency identify the exact prerequisite facet/state/result/transition rather than only the whole endpoint?
49. Can a consequential target change remain auditable when no standalone Request/Decision record was justified?
50. Can Possibility→Goal and Plan-replacement lineage be queried without generic `related_to` semantics or identity retyping?
51. When an integrated hardening changes architecture constraints, can the repository reconstruct which mechanisms were reconsidered and why the current one still won or was replaced?

### Integrated A+B regression result

```text
TC-O01..O10
PASS / PASS WITH explicitly stage-bound Slice-D/F physical-history/governance dependencies

INTEGRATED MUTATION TESTS
10 / 10 PASS

INTEGRATED COUNTERFACTUAL FAMILIES
9 / 9 PASS

TECHNOLOGY / MECHANISM RECONSIDERATION
RETAIN + HARDEN

DOMAIN REOPEN REQUIRED
0
```
