<!-- LIFEOS-CANONICAL-CONTINUATION document="decision-and-assumption-register-v1.md" follows="decision-and-assumption-register-v1-part-7.md" -->
> **Canonical continuation of the Logical Model Decision and Assumption Register v1.** Earlier decisions/assumptions remain active unless explicitly superseded. This continuation records Slice F — Relationships / Multi-Actor / Governance decisions, rejected alternatives and physical deferrals.

# Slice F — Decision Register

## DEC-F001 — Select Layered Typed Relations & Governance Model

**Decision:** use specific semantic relation families constrained by relation-profiled Reference Contracts, direct relations in simple cases, qualified LR-02 material relation records when consequence requires, and a separate downstream technical authorization projection.

**Why selected:** this candidate preserves Domain relation specificity, simple-case compactness, historical reconstructibility, selective disclosure, n-ary Agreement semantics and replaceable authorization technology without reintroducing a universal `Relationship` root.

**Rejected alternatives:** F-A, F-D, F-E, F-F, F-G as complete Logical Models; F-B remains a strong Physical Model ingredient.

**Regression impact:** R3 WHOLE-LOGICAL.

**Reopen trigger:** stronger evidence shows specific semantic families cannot share the current logical mechanisms without excessive duplication or loss of referential/governance integrity.

**Status:** RETAIN + HARDEN.

## DEC-F002 — No universal semantic Relationship/Edge root

**Decision:** LifeOS will not use one canonical `Relationship(from,type,to,payload)` object as the semantic owner/fallback for all relation families.

**Why selected:** current accepted relations have materially different arity, lifecycle, history, governance, visibility, inverse/symmetry and material-state requirements.

**Rejected alternative:** universal generic graph/edge ontology.

**Trace/tests:** INV-F001; F-REL-*; MUT-F01/02.

**Status:** REJECT GENERIC ROOT.

## DEC-F003 — No universal RelationRef

**Decision:** existing `ScopedRecordRef` and `MaterialStateRef` are sufficient for current qualified relation/history addressability.

**Why selected:** adding RelationRef would create an unnecessary generic identity hierarchy and blur direct versus materially stateful relations.

**Rejected alternative:** every relation receives independent RelationRef identity.

**Trace/tests:** INV-F002; F-REL-02/03; MUT-F03.

**Reopen trigger:** a concrete relation family proves it needs an independently justified native/specialist identity contract not expressible through LR-02 + ScopedRecordRef.

**Status:** RETAIN.

## DEC-F004 — Harden Reference Contract with relation profile

**Decision:** extend Reference Contract semantics to describe, where applicable, endpoint roles, eligible reference families, arity/cardinality, direction/inverse/symmetry/transitivity, scope/facet/action/purpose, material-state binding, lifecycle, provenance, visibility and governance basis.

**Why selected:** type/eligibility and relation-specific semantics must remain deterministic even if physical storage reuses common edge machinery.

**Rejected alternative:** relation meaning encoded primarily in `type` strings/payload conventions.

**Status:** RETAIN + HARDEN.

## DEC-F005 — Direct relation vs qualified material relation is consequence-sensitive

**Decision:** allow compact direct typed relations when semantically complete; escalate to LR-02 material record + ScopedRecordRef/MaterialStateRef when history/scope/governance/provenance/visibility becomes consequential.

**Why selected:** avoids both over-modeling simple cases and silent historical mutability in consequential cases.

**Rejected alternatives:** mandatory relation object everywhere; permanently unqualified edge everywhere.

**Trace/tests:** INV-F002; F-REL-02/03.

**Status:** RETAIN + HARDEN.

## DEC-F006 — Actor remains contextual role/capability

**Decision:** no ActorRef or Actor wrapper identity. Preserve concrete actor-role relations where known.

**Why selected:** Actor is agency semantics, not native identity; Person/Collective/system identity remains separately owned.

**Rejected alternatives:** Actor superclass/entity; Principal/Account used as semantic Actor by default.

**Trace/tests:** INV-F003; F-REP-01/03; MUT-F04/MUT-F38.

**Status:** RETAIN.

## DEC-F007 — Membership does not imply participation or governance

**Decision:** Membership is a specific relation family and may be an input to bounded policy, but it does not itself establish Participation, Authority, Visibility, Agreement or Consent.

**Why selected:** Domain and external benchmark evidence both reject automatic group-membership authorization semantics.

**Rejected alternatives:** member => participant; member => can-view/can-edit; provider security group => canonical Membership/Authority automatically.

**Trace/tests:** INV-F005; F-MEM-*; MUT-F05..08, MUT-F33.

**Status:** RETAIN.

## DEC-F008 — Agreement is n-ary and materially terms/version-bound when material

**Decision:** represent material Agreement as an LR-02 contextual record whose party assent relations bind to the same materially specific terms state.

**Why selected:** pairwise relatedness cannot prove common assent to one terms/version state; amendments must not silently inherit assent.

**Rejected alternatives:** N pairwise `agreed_with` edges; Agreement as generic status on Decision; Agreement = Consent.

**Trace/tests:** INV-F013; F-AGR-*; MUT-F21..23.

**Status:** RETAIN + HARDEN.

## DEC-F009 — Consent receives strong material binding when consequential

**Decision:** Consent may use LR-03 semantics but consequential Consent requires material representation capable of preserving giver, action/use/exposure, target, scope, purpose, context, time, target/terms material state and withdrawal/revocation history.

**Why selected:** Consent applicability cannot be reconstructed truthfully from a generic `allowed=true` or current mutable target state.

**Rejected alternatives:** Consent = Visibility; Consent = technical Permission; global yes/no consent flag.

**Trace/tests:** INV-F012; F-CONS-*; MUT-F19/20/28.

**Status:** RETAIN + HARDEN.

## DEC-F010 — Authority may be explicit or derived, but action-time basis must be reconstructible

**Decision:** Authority can be represented by explicit relation/material state and/or derived from typed policy/specification; Effective Authority may be LR-08. Consequential historical effects must retain/reconstruct applicable action-time governance basis.

**Why selected:** materializing every permission is unnecessary, while using only current policy to explain historical actions is false.

**Rejected alternatives:** one permission row per possible action universally; current Authority as historical truth; technical allow as Authority.

**Trace/tests:** INV-F010/F011; F-AUTH-*.

**Status:** RETAIN + HARDEN.

## DEC-F011 — Visibility is independently projection/relation/source scoped

**Decision:** Visibility may govern an endpoint representation, relationship existence/kind/state/history, derived projection and supporting source/Evidence independently.

**Why selected:** shared reality requires safe selective disclosure without per-user object duplication or source leakage.

**Rejected alternatives:** whole-object ACL only; endpoint visibility implies edge visibility; projection visibility implies source visibility.

**Trace/tests:** INV-F014; F-VIS-*; F-PRIV-*; MUT-F29/30.

**Status:** RETAIN + HARDEN.

## DEC-F012 — Representation preserves actual Actor, represented party and legitimacy basis separately

**Decision:** action-scoped Representation must not rewrite represented party as actual Actor and does not itself manufacture Authority.

**Why selected:** attribution, representation and legitimacy answer different questions; Principal/Account are also separate security contexts.

**Rejected alternatives:** impersonation-style actor overwrite; Representation = Authority; Principal = Actor.

**Trace/tests:** INV-F015; F-REP-*; MUT-F25/26/38.

**Status:** RETAIN + HARDEN.

## DEC-F013 — Domain governance is separate from technical authorization

**Decision:** canonical Authority/Consent/Visibility/Agreement/Membership/Representation state projects into a replaceable technical AuthZ layer. Runtime `allow/deny` never becomes canonical governance truth by identity.

**Why selected:** policy decisions may depend on technical boundaries/device/session/account context beyond domain legitimacy, and misconfiguration can technically allow operations lacking domain Authority.

**Rejected alternatives:** AuthZ tuple/policy store as canonical domain source; ALLOW = Authority; DENY = no Authority.

**Trace/tests:** INV-F016; F-AUTH-03/04; MUT-F31/32/37.

**Status:** RETAIN + HARDEN.

## DEC-F014 — Authorization engine remains replaceable

**Decision:** do not select OpenFGA, Cedar, OPA/Rego, capability credentials or a custom engine at Logical Model stage.

**Why selected:** all are plausible technical mechanisms with different strengths; none should dictate LifeOS ontology before Physical Model/runtime constraints are validated.

**Retained candidates:** ReBAC, typed policy/ABAC, policy decision engine, capabilities, hybrid.

**Status:** STAGE-DEFERRED PHYSICAL/RUNTIME.

## DEC-F015 — Delayed consequential effects must handle stale authorization

**Decision:** a prior technical allow does not remain automatically sufficient after governance state changes. Runtime must either revalidate near effect time or use an explicitly valid immutable authorization/effect binding whose semantics permit delayed execution.

**Why selected:** prevents time-of-check/time-of-use corruption after revocation/withdrawal/policy changes.

**Rejected alternative:** queue carries permanent `authorized=true` flag detached from later governance.

**Trace/tests:** INV-F017; F-AUTH-06; MUT-F35.

**Status:** RETAIN + HARDEN.

## DEC-F016 — Unknown/conflicting governance remains first-class uncertainty

**Decision:** preserve unknown, unresolved, conflicting assertion, explicit prohibition/refusal and withdrawn/revoked prior state as distinct where material.

**Why selected:** default-deny enforcement must not falsify domain state; imported/provider/AI assertions cannot receive universal precedence.

**Rejected alternative:** newest/provider/creator/manager/highest-confidence automatic winner.

**Trace/tests:** INV-F018; F-UNK-*; F-CONFLICT-*; MUT-F36.

**Status:** RETAIN.

# Slice F — Assumption Register

## ASM-F001 — Current ReferenceAddress families remain sufficient for relation/governance state

**Statement:** `NativeRef`, `ScopedRecordRef` and `MaterialStateRef` can represent current Slice F addressing without a new RelationRef family.

**Evidence:** direct/qualified relation replay; Agreement/Consent/Authority/Visibility historical tests; Slice A/D architecture.

**Stability:** STABLE at Logical Model level.

**If false:** introduce the narrowest owner-specific addressing contract proven necessary; do not default to universal RelationRef.

**Refresh trigger:** Physical Model cannot enforce/reconstruct qualified relation references without semantic ambiguity.

## ASM-F002 — A shared technical relation substrate can preserve semantic owner typing

**Statement:** future physical design may reuse edge/reference infrastructure while preserving specific relation-family constraints and reverse mapping.

**Evidence:** relation-profiled Reference Contract provides logical constraints; fully owner-specific tables remain fallback.

**Stability:** EVOLVING physically.

**If false:** prefer owner-specific relation structures.

**Refresh trigger:** shared substrate repeatedly requires untyped payloads, invalid cross-family joins or semantic type switches in application code.

## ASM-F003 — Effective Authority/Visibility can remain derived by default

**Statement:** most effective permission/exposure results need not become canonical rows if their material basis is reconstructible when consequential.

**Evidence:** existing LR-08 pattern; policy-engine benchmarks; simple-case compactness.

**Stability:** EVOLVING.

**If false:** materialize bounded effective-governance snapshots for additional consequential workflows.

**Refresh trigger:** repeated audit/concurrency requirements make recomputation insufficient.

## ASM-F004 — Agreement common-ground state benefits from LR-02 rather than native identity

**Statement:** Agreement requires stable contextual address/history but not new global/native identity semantics.

**Evidence:** current party/terms/history scenarios reconstruct through ScopedRecordRef/MaterialStateRef.

**Stability:** STABLE.

**If false:** only reopen after a concrete product workflow proves independent cross-context Agreement identity/lifecycle not expressible as contextual record.

## ASM-F005 — Consent consequence threshold can stay selective

**Statement:** not every low-consequence UI permission interaction needs a heavyweight material record; material governance consequences do.

**Evidence:** simple/worst-case pressure and existing consequence-sensitive methodology.

**Stability:** EVOLVING.

**If false:** strengthen Consent materialization policy while preserving semantic separation.

**Refresh trigger:** privacy/compliance scope requires universal auditability for additional Consent classes.

## ASM-F006 — Technical authorization will remain replaceable

**Statement:** ReBAC/ABAC/capability engines can consume canonical LifeOS projections without becoming canonical source truth.

**Evidence:** Zanzibar/OpenFGA/Cedar/OPA/capability benchmark separation.

**Stability:** STABLE logical intent; EVOLVING implementation.

**If false:** a future engine may become a physical source for a bounded technical state, but domain relation/governance semantics must still reverse-map explicitly.

**Refresh trigger:** runtime consistency/performance requires authoritative security state not derivable safely from canonical sources.

## ASM-F007 — Effect-time revalidation/binding is physically feasible

**Statement:** future runtime can prevent stale authorization on consequential delayed effects through revalidation, immutable grants/capabilities, transaction/binding techniques or hybrid.

**Evidence:** mature authorization/capability mechanisms; no logical contradiction found.

**Stability:** EVOLVING pending Physical Model.

**If false:** Physical Model must introduce stronger transaction/governance coupling before implementation authorization.

**Refresh trigger:** concurrency/distributed execution design proves a reliable effect-time check/binding impossible with chosen architecture.

## ASM-F008 — Selective relation/source Visibility can be enforced without per-recipient data duplication

**Statement:** one shared canonical reality can support recipient-specific projections at endpoint/relation/source levels.

**Evidence:** accepted Visibility domain semantics; LR-08 projection pattern; F privacy replay.

**Stability:** STABLE logically, EVOLVING physically.

**If false:** Physical Model must improve projection/policy indexing; duplicating canonical reality per recipient remains disallowed unless a separate product referent truly exists.

**Refresh trigger:** performance/security model cannot produce bounded projections without source leakage.

# Rejected-alternative register additions

```text
ALT-F01 Universal semantic Relationship / Edge root
REJECT — semantic-free relation_type/payload escape hatch

ALT-F02 Fully owner-specific logical relation structures only
VIABLE STRONG ALTERNATIVE / PHYSICAL INGREDIENT
RETEST if shared LR-03/Reference Contract machinery causes semantic leakage

ALT-F03 Universal RelationRef
REJECT — unnecessary identity hierarchy; ScopedRecordRef/MaterialStateRef sufficient

ALT-F04 ReBAC tuple store as canonical LifeOS ontology
REJECT LOGICALLY — retain as AuthZ projection/enforcement candidate

ALT-F05 ABAC/policy language as canonical LifeOS ontology
REJECT LOGICALLY — retain as policy/enforcement candidate

ALT-F06 Universal capability/grant ledger
REJECT AS COMPLETE MODEL — retain bounded delegation mechanism

ALT-F07 Universal governance event-log ontology
REJECT LOGICALLY — retain event/history technique as possible physical mechanism

ALT-F08 Pairwise Agreement edges
REJECT — cannot prove common materially specific terms/version

ALT-F09 Membership-derived universal Authority/Visibility
REJECT — downstream policy consequence only where explicitly justified

ALT-F10 Technical ALLOW/DENY as domain Authority truth
REJECT — enforcement decision != semantic governance state
```

# Stage-deferred Physical / Runtime decisions

```text
DEFER-F01 relation table strategy: owner-specific vs shared typed-edge vs hybrid
DEFER-F02 qualified relation record PK/FK/index shape
DEFER-F03 MaterialStateRef persistence/indexing for governance history
DEFER-F04 public/API representation of relation identifiers
DEFER-F05 AuthN Principal model/runtime persistence
DEFER-F06 ReBAC vs Cedar/ABAC vs OPA vs custom/hybrid engine selection
DEFER-F07 canonical-to-AuthZ projection store/cache strategy
DEFER-F08 consistency model / invalidation / authorization cache strategy
DEFER-F09 delayed-action revalidation vs immutable grant/binding implementation
DEFER-F10 capability/token/delegation credential format
DEFER-F11 technical decision-log schema/retention
DEFER-F12 field/facet/projection-level Visibility enforcement strategy
DEFER-F13 SQL RLS / application enforcement / policy sidecar split
DEFER-F14 runtime representation/on-behalf-of token/session mechanics
```

# Slice F decision integrity counters

```text
accepted decisions                    16
material assumptions                   8
rejected/retained alternatives        10
stage-deferred physical/runtime       14
unclassified material decisions        0
unregistered material assumptions      0
rejected candidates without rationale  0
unsafe physical deferrals              0
Domain reopen required                  0
```

No decision in this continuation authorizes SQL/schema/API/AuthN/AuthZ runtime implementation, selects an authorization vendor, or changes `main`.