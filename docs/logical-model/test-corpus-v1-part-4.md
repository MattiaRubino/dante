<!-- LIFEOS-CANONICAL-CONTINUATION document="test-corpus-v1.md" follows="test-corpus-v1-part-3.md" -->
> **Canonical continuation of `test-corpus-v1.md`.** This physical file is Part 4 of the same logical corpus and adds Slice-D Evidence / Knowledge / History regression pressure.

# R. Slice D — Evidence / Knowledge / History regression corpus

## TC-R01 — Observation correction versus re-observation

Observation O1 is corrected from 66.4 kg to 65.8 kg for the same observational act.

Required:

```text
same Observation NativeRef
new MaterialStateRef
prior state reconstructible
```

A later independent measurement creates a new Observation.

## TC-R02 — Provider assertion does not establish Actual

Provider reports an Activity completed while user/device evidence conflicts.

Required:

```text
provider source preserved
conflict may remain unresolved
no automatic provider-wins Actual
```

## TC-R03 — Historical Evaluation basis

Evaluation E1 used Observation O1/S1 and Criterion C1. Later O1 is corrected to S2 and Criterion becomes C2.

Required:

```text
E1 remains reconstructible under S1/C1
current reevaluation may use S2/C2
```

## TC-R04 — MaterialStateRef versus ETag

Provider changes ETag without material semantic change.

Required:

```text
new ETag != automatic new MaterialStateRef
```

## TC-R05 — Divergent material states

Base S1 diverges into S2A and S2B offline/provider.

Required:

```text
both states attributable/reconstructible
no forced linear history
no last-write-wins rule
```

## TC-R06 — Evidence reused in several contexts

One Observation is used as supporting Evidence for Criterion A and contradictory Evidence for Criterion B.

Required:

```text
one source identity
multiple contextual Evidence uses
no duplicated source payload
```

## TC-R07 — Missing Evidence

Only two workouts are visible for a three-workout criterion, but source coverage is incomplete.

Required:

```text
unknown / insufficient Evidence valid
missing != failure
```

## TC-R08 — Confirmation binds material state

Actor confirms target S1. Target later changes materially to S2.

Required:

```text
Confirmation remains about S1
no silent inheritance to S2
```

## TC-R09 — Acknowledgement versus telemetry

Message was delivered/opened but actor never explicitly acknowledged.

Required:

```text
delivery/read telemetry != Acknowledgement
```

## TC-R10 — AI extraction lineage

PDF -> OCR -> AI extraction -> candidate -> user correction -> accepted state.

Required:

```text
Provenance retains materially relevant steps
user correction != original user authorship
AI confidence != truth
```

## TC-R11 — Current versus then-known

World event occurs T1, provider import arrives T3, correction arrives T5.

Required queries:

```text
current interpretation of T1
what LifeOS knew at T2
what LifeOS accepted at T4
why current differs
```

## TC-R12 — Current-state performance

Years of history exist for one target.

Required:

```text
current state query possible without application replay of entire lifetime
history still reconstructible
```

## TC-R13 — Private Evidence / shareable consequence

Private health information influences shared scheduling feasibility.

Required:

```text
shareable bounded result
without source/Evidence/Provenance disclosure
```

## TC-R14 — High-frequency telemetry

A wearable produces millions of samples.

Required:

```text
no semantic requirement for one Observation per raw tick
specialist/source-native series permitted
selected/derived observations may remain canonical
```

## TC-R15 — Transient Evaluation

Dashboard recalculates progress every refresh.

Required:

```text
no durable Evaluation row required for every tick
```

## TC-R16 — Consequential Evaluation

A material Decision later relies on an Evaluation.

Required:

```text
historical assessment basis/material states reconstructible
materialized LR-02 snapshot allowed/required by consequence
```

## TC-R17 — Reconciliation unresolved

Two credible Observations disagree and no bounded precedence exists.

Required:

```text
conflict preserved
current resolution may remain unresolved
```

## TC-R18 — Reconciliation reversed

A bounded resolution selects state A; later better evidence reverses it to B.

Required:

```text
prior resolution remains history
current owner state changes without falsifying old basis
```

## TC-R19 — Source redaction

Sensitive upstream payload must later be deleted/redacted.

Required:

```text
retention policy may remove payload
historical semantic reference remains honest where required
no backdoor indefinite archive
```

## TC-R20 — Current knowledge projection

User explicitly says they like photography; later AI infers astrophotography interest.

Required:

```text
explicit != inferred
projection can expose both safely
projection != canonical source of truth
```

## TC-R21 — Ongoing celiac context

User reports celiac disease/intolerance and the accepted source/state treats it as ongoing.

Required:

```text
current knowledge projection marks it applicable now
self-report provenance preserved
not silently promoted to specialist diagnosis
```

## TC-R22 — Specialist update to celiac context

Later specialist evidence materially changes/refines the accepted interpretation.

Required:

```text
new current material state
prior self-report remains historical source
no silent provenance laundering
```

## TC-R23 — Broken-leg episode resolves

Fracture/injury state begins at T1 and is later established resolved/healed at T2.

Required:

```text
history remains
current applicability after T2 is false/inactive according to owner semantics
old episode does not remain an active planning constraint
```

## TC-R24 — Fever as point Observation

Temperature/fever-related measurement is captured at T1 only.

Required:

```text
effective time/period preserved
point Observation does not become ongoing condition automatically
```

## TC-R25 — Fever episode

A continuing symptom/condition episode is explicitly represented across an interval.

Required:

```text
bounded/ongoing episode semantics separate from individual measurements
later resolution does not delete history
```

## TC-R26 — Unknown end

A condition/state is known to have started but no reliable end/resolution is known.

Required:

```text
unknown-ended != universally permanent
retrieval exposes uncertainty/owner-specific applicability honestly
```

## TC-R27 — Intermittent/recurrent applicability

A condition/state recurs intermittently.

Required:

```text
recurrent/intermittent != continuously active
history can express episodes/pattern according to owner semantics
```

## TC-R28 — Old temporary state and current recommendation

A past fever or healed fracture exists in history while LifeOS plans an unrelated present activity.

Required:

```text
historical retrieval possible
current reasoning does not treat old temporary state as active without basis
```

## TC-R29 — Cross-domain memory months later

Information captured in one domain becomes pertinent months later in another workflow.

Required:

```text
retrievable by semantic relevance
source/material-state/applicability/visibility retained
no generic fact-store ownership required
```

## TC-R30 — Verification without universal result root

A target is assessed under Verification purpose.

Required:

```text
Criterion/Evaluation semantics sufficient
no universal VerificationResult owner required
```

---

# S. Slice-D destructive mutations

The following mutations must remain rejected:

```text
MUT-D01 Observation -> universal Fact
MUT-D02 Observation identity = subject+property+time+value
MUT-D03 provider revision = MaterialStateRef
MUT-D04 universal sequential semantic version
MUT-D05 state reference without target/facet contract
MUT-D06 newest state always wins
MUT-D07 correction overwrites history
MUT-D08 Evidence duplicates source
MUT-D09 Evidence intrinsic=true flag
MUT-D10 Evidence exists => target true
MUT-D11 missing Evidence => failure
MUT-D12 universal confidence/evidence score
MUT-D13 Provenance = source string
MUT-D14 Provenance = audit log
MUT-D15 Provenance = truth/Authority
MUT-D16 universal confirmed boolean
MUT-D17 read/delivery => Acknowledgement
MUT-D18 universal VerificationResult
MUT-D19 persist every transient Evaluation
MUT-D20 never persist consequential Evaluation
MUT-D21 current rule rewrites historical Evaluation
MUT-D22 Reconciliation = last-write-wins
MUT-D23 Reconciliation owns target current state
MUT-D24 universal event/bitemporal Fact ontology
MUT-D25 knowledge projection becomes canonical store
MUT-D26 AI inference automatically canonical
MUT-D27 one Observation per raw sensor tick universally
MUT-D28 visible result exposes private Evidence/Provenance
MUT-D29 history justifies sensitive retention forever
MUT-D30 ETag/MVCC = semantic Version
MUT-D31 old temporary condition remains current forever
MUT-D32 missing end = permanent
MUT-D33 resolution deletes historical episode
MUT-D34 point Observation = continuing condition
```

All are permanent regression candidates after Slice-D activation.

---

# T. Slice-D counterfactual families

```text
CF-D01 corrected Observation vs new observation
CF-D02 provider assertion vs established Actual
CF-D03 verifiable credential vs substantively true claim
CF-D04 source fact vs Evidence use
CF-D05 support vs contradiction by same source
CF-D06 historical Evaluation vs current reevaluation
CF-D07 Acknowledgement vs Confirmation
CF-D08 Confirmation of S1 vs S2
CF-D09 unresolved conflict vs resolved current interpretation
CF-D10 current truth about T vs what was known at K
CF-D11 provider revision vs semantic material change
CF-D12 private Evidence vs disclosure permission
CF-D13 raw telemetry vs canonical selected Observation
CF-D14 transient vs consequential Evaluation
CF-D15 ongoing vs resolved historical condition
CF-D16 unknown end vs permanent/ongoing semantics
CF-D17 point fever Observation vs fever episode
CF-D18 intermittent/recurrent vs continuously active
```

Later slices must replay affected families.

---

# U. Forward pressure

Slice E must replay:

```text
resource/value state history
current applicability of availability/capacity/constraints
Observation/value history without fact-store collapse
```

Slice F must replay:

```text
private Evidence / shared consequence
actor-scoped Confirmation/Acknowledgement
Authority != truth
Visibility of current projection != Visibility of history/source
```

Whole-Logical must replay all D tests before WD-03 final discharge.