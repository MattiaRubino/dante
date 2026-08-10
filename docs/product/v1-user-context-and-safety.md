# LifeOS V1 — User Context, Memory, and Safety Constraints

## Principle

LifeOS maintains a structured and editable picture of the user so new plans are compatible with information already provided.

The system should not treat every request as if it came from a new anonymous user. Before proposing a plan, it must consult relevant active context such as health constraints, dietary restrictions, injuries, rehabilitation plans, allergies, availability, equipment, preferences, current programs, and previous decisions.

This is contextual planning, not unrestricted collection of everything the user has ever said.

## Types of stored context

Relevant user context may include:

- explicit personal facts supplied by the user;
- preferences and dislikes;
- hard constraints and prohibitions;
- health, accessibility, dietary, or rehabilitation information;
- current goals, routines, programs, and commitments;
- available time, locations, equipment, budget, and resources;
- imported plans and professional instructions;
- prior user decisions and reusable planning rules;
- historical activity and outcome records;
- temporary conditions with an expiry or review date.

Each item should include enough metadata to understand what it means and whether it is still valid.

## Provenance and reliability

Stored context should record its source, for example:

- explicitly entered by the user;
- extracted from an uploaded file;
- imported from an integration;
- derived from a previous program or activity;
- suggested by the system and confirmed by the user;
- inferred but not yet confirmed.

Explicit user statements and confirmed professional instructions take priority over unconfirmed inference.

LifeOS must not silently convert a weak inference into a permanent medical, dietary, or personal fact.

## Active constraints

Some context acts as a hard planning constraint. Examples include:

- coeliac disease or another declared food restriction;
- a declared allergy;
- a rehabilitation restriction that forbids running or impact activity;
- a medical or professional plan that limits load, movements, ingredients, timing, or progression;
- inaccessible locations or unavailable equipment;
- dates during which an activity is prohibited.

Before generating or importing a related plan, LifeOS must check these constraints and reject or flag incompatible proposals.

For example, a meal plan must not include gluten when an active coeliac constraint is known. A fitness plan must not introduce running when an active rehabilitation restriction excludes it.

## Conflicts and uncertainty

When new information conflicts with stored context, LifeOS should not guess silently. It should identify the conflict and ask for a resolution, for example:

- whether an old restriction is no longer active;
- whether a professional plan has been replaced;
- whether a one-time exception should remain temporary;
- which of two incompatible instructions has priority.

When a safety-relevant fact is uncertain or incomplete, the system should choose the cautious option and request clarification before applying the plan.

## Scope-aware retrieval

LifeOS should consult the context relevant to the current task rather than dumping the user's entire history into every interaction.

Examples:

- nutrition planning retrieves dietary restrictions, allergies, current nutrition plans, preferences, and relevant health constraints;
- training planning retrieves injuries, rehabilitation rules, fitness level, equipment, recovery requirements, and current workload;
- travel planning retrieves availability, budget, mobility constraints, preferences, and existing calendar commitments;
- language planning retrieves current level, target, available study time, prior progress, and preferred learning method.

This keeps planning accurate while reducing unnecessary exposure of unrelated personal information.

## User control and privacy

The user must be able to:

- view the stored profile and active constraints;
- correct, deactivate, or delete individual facts;
- mark information as temporary;
- see where a fact came from;
- decide whether an imported document contributes reusable profile information;
- prevent a sensitive item from being reused outside its intended scope;
- export or delete their stored data.

Sensitive information should be protected with stricter access controls and should not be exposed in shared events, shared workspaces, exports, notifications, or assistant responses unless required and authorised.

## Planning behaviour

Before presenting a new plan, LifeOS should:

1. identify the domain and relevant context;
2. retrieve active constraints and current commitments;
3. check the proposal for conflicts;
4. preserve confirmed professional instructions when applicable;
5. flag uncertainty or incompatibility;
6. show important assumptions and constraints in the preview;
7. require user approval before inserting a complex plan.

## User authority

The user's explicit update remains authoritative. If the user says that a restriction has changed, an activity was completed, or a result was achieved, LifeOS records the update without demanding proof.

For high-impact or safety-relevant changes, LifeOS may ask the user to confirm the intended meaning, but it should not require external evidence merely to manage the user's own plan.