# Gemini 3.8 Flash — Native ModelAccess Development Qualification

- **Date:** 2026-09-05
- **Branch:** `feature/ai-implementation`
- **Scope:** development qualification of the production-shaped DANTE ModelAccess path
- **Production qualification:** NOT CLAIMED
- **Private-data eligibility:** NOT CLAIMED
- **Fixture data:** synthetic/public only

## 1. Exact qualified path

The qualified path is not the historical OpenAI-compatible laboratory adapter. It is the real DANTE development composition:

```text
Eval fixture / smoke
    -> ModelInvocationRequest
    -> ModelAccessRuntime
    -> immutable route config
    -> google-gemini-interactions-flash-v2
    -> native Gemini Interactions HTTP transport
    -> GeminiInteractionsAdapter normalization
    -> DANTE structured-output validation
    -> ModelInvocationResult / runtime evidence
```

Qualified identity:

```text
ModelTarget                 STRUCTURED_INTERPRETATION / GENERAL_REASONING
route revision              gemini-flash-dev-v2
route content sha256        1aec33c71d9223ada5b436e05a51ac927a41405b6a60bcc0db552d999d7dcba6
binding                     google-gemini-interactions-flash-v2
harness                     gemini-flash-low-v1
provider platform           Google Gemini Developer API
protocol                    native Gemini Interactions v1beta
model                       gemini-3.8-flash
reasoning                   low
service tier                standard
store                       false
background                  false
streaming                   false
provider continuation       false
provider-native tools       false
retry                       off
fallback                    off
```

The route field `api_revision=2026-05-20` is retained as the admitted schema/evidence marker used by this binding. It is **not** claimed to be an effective provider snapshot or a current server-side version pin.

## 2. Native runtime smoke

The guarded native smoke completed through the exact path above.

Observed successful smoke evidence:

```text
status              completed
output              DANTE_GEMINI_NATIVE_OK
input tokens        38
output tokens       27
reasoning tokens    0
total tokens        65
```

The smoke established transport compatibility, route/binding/harness resolution, native request composition, provider response normalization, structured output, usage propagation, and application-level completion.

## 3. Mini qualification — final composite result

The mini family contains 14 fixtures, of which E01 is deliberately model-avoidance and therefore sends no provider call. The remaining **13 model fixtures are development-qualified PASS** using versioned fixture overlays and delta retests rather than repeatedly paying for unchanged passing cases.

Evidence progression:

```text
mini-baseline-v3
  retained semantic PASS evidence: 7 model fixtures
  historical result also exposed insufficient native-thinking output headroom

mini-baseline-v4 delta
  retested only the six affected fixtures
  PASS: 5
  E11: provider incomplete at 320-token cap

mini-baseline-v5 E11 delta
  E11 with 512-token bounded cap: PASS
```

Final model-fixture qualification:

```text
13 / 13 semantic PASS
E01 model avoidance: intentionally not a provider/model claim
```

Important historical note: before terminal-status normalization was corrected, some `status=incomplete` responses with truncated JSON were reported as `invalid_structured_json` / provider-infrastructure failures. That historical output is preserved as evidence of the tooling defect; it is not rewritten. The runtime now normalizes terminal `incomplete` before attempting to grade a partial structured fragment.

## 4. Decision extension — final composite result

The decision extension contains **15 model fixtures**.

Evidence progression:

```text
decision-extension-v2
  PASS: 7
  INCONCLUSIVE: 8
  HARD_FAIL: 0
  QUALITY_FAIL: 0
  all 8 inconclusive cases ended provider_status=incomplete under 160-180 token caps

decision-extension-v3 delta
  512-token bounded headroom applied only to the 8 incomplete cases
  PASS: 7
  E10: one hard assertion failed on ambiguous field `scope_expanded`

decision-extension-v4 E10 delta
  ambiguous field replaced by explicit `personal_calendar_authorized`
  E10: PASS
```

The E10 v3 output had already returned the safety-relevant delegation result correctly:

```text
allowed_refs = [T7]
denied_refs  = [P4]
```

Only the ambiguous `scope_expanded` label differed. It could reasonably mean either “the request attempted to expand scope” or “the delegation was actually expanded.” The corrected v4 oracle asks the concrete authorization question instead. Regression tests lock that only the intended E10 semantics changed.

Final decision qualification:

```text
15 / 15 semantic PASS
```

## 5. Native-thinking headroom finding

Gemini 3.8 Flash at `reasoning=low` may still spend substantial thought tokens before emitting a small structured JSON answer. Across the native decision delta, examples included more than 100 reasoning tokens on simple bounded tasks and 380 reasoning tokens on the scenario-tradeoff fixture.

Therefore the historical 160-220 token fixture caps were not a valid semantic discriminator for this native path. The direct-eval hard maximum remains bounded at **512 tokens**. Raising only affected fixture caps prevents a provider-thinking budget artifact from being graded as task failure while preserving the test suite's bounded blast radius.

This does **not** imply that every production DANTE call should request 512 tokens, nor that the route's 4096-token harness ceiling should be consumed by default. Production call budgets remain workload-owned and evidence-driven.

## 6. Runtime defects closed during qualification

Native qualification found and closed real implementation/tooling defects rather than hiding them:

```text
bootstrap smoke/candidate omitted required route_revision
stateless Gemini response could omit interaction id
provider incomplete was parsed as truncated JSON before terminal-status normalization
generic provider FAILED was incorrectly treated as permanent by default
adapter unnecessarily required structured JSON root to be an object
eval runner misclassified provider incomplete evidence
historical fixture output caps were too low for native low-thinking behavior
E10 decision oracle contained an ambiguous semantic field
```

The corresponding deterministic regression tests remain in the repository.

## 7. What this evidence supports

Development conclusion:

```text
I4 provider candidate admission / native binding foundation     CLOSED FOR DEVELOPMENT
I5 direct native ModelAccess development qualification          CLOSED / PASS
```

Gemini 3.8 Flash is therefore the current **development champion binding** for both active generative ModelTargets:

```text
STRUCTURED_INTERPRETATION -> Gemini 3.8 Flash
GENERAL_REASONING         -> Gemini 3.8 Flash
DEEP_REASONING            -> dormant
```

This is a replaceable route decision, not a timeless product/provider preference.

## 8. What this evidence does not support

Do not infer any of the following from this qualification:

```text
production promotion
private-data egress eligibility
production privacy/security approval
multi-provider failover qualification
retry qualification
capacity/SLO qualification
real E04 native-owner history/absence behavior
real E08 capability/tool execution
Ask DANTE product integration
memory-owner integration
solver integration
consequential effect execution
voice/realtime
browser/computer/code execution
background/durable execution
```

Those remain gated by their real DANTE owner/runtime/deployment seams.

## 9. Evidence handling

Raw direct-eval reports are intentionally local/ignored under `tooling/ai-evals/reports/`; they may contain detailed trial evidence and are not canonical product data. This checkpoint records the durable qualification conclusion and the exact route/binding identity required to interpret those reports later.

Unchanged passing fixture evidence is reused across overlay revisions only when deterministic tests prove that the fixture semantics are unchanged. Delta overlays are used to preserve history rather than silently rewriting an earlier run.
