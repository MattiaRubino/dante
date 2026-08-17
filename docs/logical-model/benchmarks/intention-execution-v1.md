# LifeOS Logical Model — Slice B Intention / Execution External Benchmark v1

**Date:** 2026-08-17  
**Status:** benchmark evidence for Slice-B accepted candidate; remote activation conditional on full Slice-B QA  
**Policy:** `../external-benchmark-policy-v1.md`

---

## 1. Research objective

This benchmark asks which external mechanisms help LifeOS preserve the accepted distinctions among candidate future, adopted intent, strategy, action, expected occurrence, request/proposal, decision, dependency, material revision and actual effect.

External systems are evidence, not ontology authority.

For every mechanism the transfer rule is:

```text
SOURCE
PROBLEM
MECHANISM
INVARIANT / INSIGHT
LIMITATION / ANTI-PATTERN
LIFEOS DISPOSITION
REOPEN IMPACT
```

The benchmark deliberately includes personal/work-management products, infrastructure, workflow engines, healthcare, procurement/change review and standards so LifeOS is not optimized around one product category.

---

## 2. Terraform — proposed change != applied state

**Source:** HashiCorp Terraform CLI `plan` documentation  
https://developer.hashicorp.com/terraform/cli/commands/plan

**Problem:** determine what changes would be made before mutating managed infrastructure.

**Mechanism:** Terraform creates an execution plan describing proposed actions; speculative plans do not apply changes.

**Transferable insight:**

```text
proposed plan/change
!= applied change
!= resulting state
```

**LifeOS disposition:** supports strict separation among Proposal, Decision/authorization, Plan material change and later effect/Actual.

**Limitation:** infrastructure desired-state reconciliation is much narrower than personal intention/execution semantics.

**Reopen impact:** none; reinforces existing Domain boundaries.

---

## 3. Kubernetes — desired state != observed/current state

**Source:** Kubernetes Objects / object spec and status  
https://kubernetes.io/docs/concepts/overview/working-with-objects/

**Problem:** controllers need a desired configuration while the system may currently differ from it.

**Mechanism:** object `spec` expresses desired state and `status` describes current state; controllers work toward reconciliation.

**Transferable insight:**

```text
intended/desired
!= actual/current
```

**LifeOS disposition:** strong support for preserving Goal/Plan/Activity/Routine intention independently from Actual/Outcome.

**Anti-copy rule:** LifeOS must **not** adopt `spec/status` as a universal metamodel. Possibility, Proposal, Request, Decision, Milestone and Dependency are not merely desired-state specs.

**Reopen impact:** none.

---

## 4. Apache Airflow — definition != run != task instance

**Source:** Apache Airflow Dag Runs  
https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html

**Problem:** execute a durable workflow definition repeatedly while preserving individual execution state.

**Mechanism:** DAG definition is separate from Dag Run; tasks have task instances for particular runs.

**Transferable insight:**

```text
definition / execution structure
!= specific run / instance
```

**LifeOS disposition:** reinforces Plan/Routine definition versus Occurrence/execution separation and rejects the pattern of advancing one recurring object forever.

**Limitation:** Airflow is an execution engine and assumes workflow semantics far stronger than LifeOS kernel semantics.

**Reopen impact:** none.

---

## 5. AWS Step Functions — definition/version/alias != execution

**Sources:** AWS Step Functions versions and aliases / execution behavior  
https://docs.aws.amazon.com/step-functions/latest/dg/concepts-state-machine-version.html  
https://docs.aws.amazon.com/step-functions/latest/dg/concepts-state-machine-alias.html

**Problem:** change workflow definitions without losing which version governed an execution.

**Mechanism:** state machines can publish immutable versions and aliases; executions can be associated with the qualified version/alias used to start them.

**Transferable insight:**

```text
definition
!= material revision/version
!= execution
```

**LifeOS disposition:** where consequential, an Occurrence/execution must be able to identify which material Plan/Routine/Policy state governed it.

**Anti-copy rule:** LifeOS is not a universal workflow/state-machine engine.

**Reopen impact:** none; creates Slice-D/C hardening obligation only.

---

## 6. Google Cloud Workflows — workflow revision != execution

**Sources:** Google Cloud Workflows executions/revisions  
https://cloud.google.com/workflows/docs/executions  
https://cloud.google.com/workflows/docs/managing-workflows

**Problem:** run changing workflow definitions while preserving execution identity and revision context.

**Mechanism:** workflow deployments create revisions; executions are distinct runs.

**Transferable insight:** same definition/revision/execution separation as Step Functions.

**LifeOS disposition:** corroborating evidence for material-governing-state references without requiring a workflow ontology.

**Reopen impact:** none.

---

## 7. GitHub protected-branch review — approval can become stale

**Source:** GitHub protected branch / pull-request review documentation  
https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches

**Problem:** prevent approval of one reviewed change set from automatically authorizing materially changed content.

**Mechanism:** repositories can require approvals and dismiss stale approvals after new commits/change-set changes.

**Transferable insight:**

```text
approval / Decision
must remain attributable to what was materially reviewed
```

**LifeOS disposition:** Proposal/Decision may bind a specific material target state/version. Material target change may require a new applicability/Decision check.

**Limitation:** pull-request review is a specific collaboration workflow, not a universal Decision lifecycle.

**Reopen impact:** none; hardens Slice B and Slice D/F obligations.

---

## 8. SAP approval workflow — material change can restart approval

**Source family:** SAP S/4HANA flexible workflow documentation for purchasing/order approval; current product documentation reviewed during Slice-B research.

**Problem:** an already-approved business object can change in ways that invalidate the basis of approval.

**Mechanism:** workflow/restart conditions can require reapproval when relevant fields change.

**Transferable insight:** approval is not a timeless boolean attached to an owner identity.

**LifeOS disposition:** supports material-equivalence/version-bound Decision applicability.

**Limitation:** exact SAP workflow behavior is configuration/product-specific and remains `CURRENT PRODUCT BEHAVIOR`, not permanent LifeOS semantics.

**Reopen impact:** none.

---

## 9. FHIR — Goal / CarePlan / Request / Task remain separate

**Sources:** HL7 FHIR R5  
https://hl7.org/fhir/R5/goal.html  
https://hl7.org/fhir/R5/careplan.html  
https://hl7.org/fhir/R5/request.html  
https://hl7.org/fhir/R5/task.html

**Problem:** healthcare needs to distinguish desired outcomes, plans of care, requests/orders and fulfilment/task tracking.

**Mechanism:** separate resource families encode distinct roles/lifecycles.

**Transferable insight:**

```text
desired result
!= plan
!= request/order
!= fulfilment/task
```

**LifeOS disposition:** supports Goal/Plan/Request/Activity separation.

**Anti-copy rule:** FHIR intent/status taxonomies are specialist healthcare semantics and must not become universal LifeOS lifecycle enums.

**Reopen impact:** none.

---

## 10. Jira Product Discovery — idea/discovery != delivery work

**Source:** Atlassian Jira Product Discovery documentation  
https://support.atlassian.com/jira-product-discovery/

**Problem:** preserve product ideas/insights before or independently from delivery execution.

**Mechanism:** product-discovery ideas/insights can later link to Jira delivery work.

**Transferable insight:**

```text
candidate / discovery object
!= adopted delivery work
```

**LifeOS disposition:** reinforces Possibility being a real pre-commitment owner rather than a status of Goal/Activity.

**Limitation:** product-management workflow states such as idea status are not LifeOS ontology.

**Reopen impact:** none.

---

## 11. Aha! — ideas / initiatives / features as separate product postures

**Source:** Aha! support/product documentation  
https://support.aha.io/aha-roadmaps/support-articles/ideas/

**Problem:** move from feedback/idea capture into strategic prioritization and delivery without treating every idea as committed work.

**Mechanism:** separate product objects and links across discovery/strategy/delivery layers.

**Transferable insight:** useful corroboration for candidate-future versus adopted/execution semantics.

**Limitation:** Aha! taxonomy is a product-management ontology and is not copied.

**Reopen impact:** none.

---

## 12. Motion — task constraints != derived calendar placement

**Source:** Motion help/product documentation reviewed during Slice-B research  
https://help.usemotion.com/

**Problem:** dynamically allocate work into calendar time as priorities/deadlines/availability change.

**Mechanism:** Task carries work constraints such as duration, priority, deadline and scheduling settings; calendar placement can be recalculated.

**Transferable insight:**

```text
Activity/task intention + constraints
!= current Schedule placement
```

**LifeOS disposition:** supports Activity/Event/Schedule separation and derived scheduling.

**Limitation:** Motion's task model is intentionally product-specific and simpler than LifeOS semantic ownership.

**Reopen impact:** none.

---

## 13. Reclaim — recurring habit policy != conflict resolution instance

**Source:** Reclaim.ai help documentation  
https://help.reclaim.ai/

**Problem:** recurring flexible habits must survive conflicts through move/shorten/skip/defend behavior.

**Mechanism:** recurring habit/event policy plus scheduling/conflict rules controls individual calendar placements.

**Transferable insight:**

```text
repeated-behavior policy
!= conflict policy
!= individual scheduled instance
```

**LifeOS disposition:** supports Routine/Recurrence/Occurrence/Schedule separation.

**Negative evidence:** earlier task/calendar products that infer completed work from elapsed scheduled blocks are rejected by LifeOS:

```text
elapsed scheduled block != Actual automatically
```

**Reopen impact:** none.

---

## 14. Todoist — recurring-task advancement is a useful product simplification, not kernel truth

**Source:** Todoist recurring-date documentation  
https://www.todoist.com/help/articles/introduction-to-recurring-dates-YUYVJJAV

**Problem:** make personal recurring tasks easy to operate.

**Mechanism:** completing a recurring task advances it to the next recurrence.

**Transferable insight:** excellent negative benchmark for LifeOS kernel design.

**LifeOS disposition:** reject one mutable recurring Activity whose date is repeatedly advanced as the canonical historical representation when occurrence identity/history matters.

```text
Routine policy
!= generated occurrence
!= Actual
```

**Reopen impact:** none.

---

## 15. iCalendar RFC 5545 — no universal status vocabulary even inside one standard

**Source:** RFC 5545  
https://www.rfc-editor.org/rfc/rfc5545

**Problem:** interoperable calendar/task/journal representation.

**Mechanism:** VEVENT, VTODO and VJOURNAL use different allowed `STATUS` values.

**Transferable insight:** even a deliberately general standard does not assume that one status vocabulary means the same thing for all object families.

**LifeOS disposition:** reinforces owner-specific lifecycle/disposition and rejects one universal canonical `status` field.

**Anti-copy rule:** RFC 5545 remains interoperability evidence; LifeOS does not reshape its Domain Model merely to mirror iCalendar.

**Reopen impact:** none.

---

## 16. Stripe PaymentIntent — rich single-object lifecycle can be correct inside a specialist boundary

**Source:** Stripe PaymentIntent lifecycle  
https://docs.stripe.com/payments/paymentintents/lifecycle

**Problem:** payment processing needs a durable intent object across authentication, confirmation and payment states.

**Mechanism:** one specialist PaymentIntent owns a rich bounded lifecycle.

**Transferable insight:** a rich lifecycle is not intrinsically an anti-pattern when one specialist owner genuinely owns those invariants.

**LifeOS disposition:** reinforces a crucial non-dogmatic rule:

```text
reject universal generic lifecycle
!= reject specialist owner-specific lifecycle
```

**Reopen impact:** none; supports specialist-boundary discipline.

---

## 17. Notion — generic properties/relations are flexible but not sufficient as canonical semantics

**Source:** Notion help/API data-model documentation  
https://developers.notion.com/reference/property-object

**Problem:** allow users to model arbitrary information with databases/properties/relations.

**Mechanism:** generic property types, relation properties and rollups.

**Transferable insight:** useful for extension metadata, user-configurable views and derived/read-model layers.

**Negative benchmark:** required LifeOS owner/lifecycle meaning must not disappear into arbitrary property/JSON structures merely because they are flexible.

**Reopen impact:** none.

---

## 18. BPMN / DMN — process flow and decision logic are useful specialist mechanisms, not LifeOS roots

**Sources:** OMG BPMN / DMN specifications  
https://www.omg.org/bpmn/  
https://www.omg.org/dmn/

**Problem:** formally represent executable/business processes and decision logic.

**Transferable insight:** process flow, conditional policy and decision evaluation can be independently useful structures.

**LifeOS disposition:** no universal `WorkflowNode`, `Process`, `Rule`, `Condition` or `DecisionTable` root is introduced. Such structures may appear in bounded specialist/automation layers if later justified.

**Reopen impact:** none.

---

## 19. Consolidated benchmark findings

The external evidence converges on several transferable principles:

```text
candidate/discovery != commitment
proposal != applied change
intent/desired state != actual/current state
strategy/definition != run/execution
material revision matters to approval/execution provenance
request/order != fulfilment/result
recurring policy != individual instance
one generic status vocabulary is not structurally necessary
specialist rich lifecycle may be correct inside a bounded owner
```

It does **not** justify:

```text
universal WorkItem
universal WorkflowNode
global parent hierarchy
universal status enum
universal spec/status object
universal event sourcing
provider/product taxonomy as LifeOS ontology
```

---

## 20. LifeOS disposition

Selected synthesis:

```text
Layered Typed Intention & Execution Model
```

with:

```text
typed semantic owners
owner-specific lifecycle/material state
separate material Version pressure
selective Proposal/Request/Decision materialization
typed Dependency
separate later Occurrence/Schedule/Actual
explicit provenance/authority boundaries
non-canonical derived operational projections
```

The model is intentionally not copied from any one benchmark.

---

## 21. Freshness / refresh requirement

Stable standards/infrastructure sources may be reused subject to version relevance. Mutable product behavior must be rechecked if it materially influences later decisions.

Mandatory refresh points:

```text
Slice C when recurrence/schedule products materially influence representation
Slice D when approval/version/history mechanisms are finalized
Slice F when collaboration/governance behavior is finalized
Whole-Logical final regression for load-bearing external claims
```

No current Slice-B PASS depends materially on one volatile vendor behavior alone.

---

## 22. Reopen impact

```text
DOMAIN REOPEN EVIDENCE FROM BENCHMARK   0
LOGICAL STRUCTURAL BLOCKER              0

BENCHMARK VERDICT
supports selected candidate with hardening
```
