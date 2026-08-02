# LifeOS V1 — Onboarding and Progressive Profile

## Principle

Account creation should be fast and should not begin with a long questionnaire.

The user can register, sign in, and enter LifeOS immediately. A lightweight setup follows account creation, while deeper profile information is collected progressively when it becomes useful, required for a specific function, or voluntarily supplied by the user.

Skippable onboarding does not mean that every feature must operate with missing information. LifeOS can require the minimum relevant data before creating a plan or recommendation that would otherwise be unreliable, incompatible, or unsafe.

## Three levels of required information

LifeOS distinguishes between three levels.

### 1. Account-required information

This is the minimum needed to create, secure, and operate the account, such as:

- authentication details;
- acceptance of required terms and privacy information;
- locale, language, and timezone when they cannot be determined reliably;
- age confirmation or date of birth when required for eligibility, legal, or product-safety reasons;
- any mandatory account-security step.

The user should not be blocked by a broad lifestyle, health, productivity, or preference questionnaire before seeing the product.

### 2. Function-required information

Some information becomes mandatory only when the user requests a feature that genuinely depends on it.

Examples include:

- a personalised training plan may require age, current level, available equipment, injuries, active rehabilitation restrictions, and relevant physiological data;
- a nutrition or meal plan may require allergies, coeliac status, dietary restrictions, foods to avoid, and other active constraints relevant to the request;
- a stargazing or astrophotography plan may require location, available camera or phone, lenses, tripod, tracking equipment, transport limits, and the user's willingness to acquire or rent missing equipment;
- a travel plan may require dates, departure area, budget, transport constraints, and accessibility needs;
- a language program may require current level, available time, target, and preferred or required learning format.

LifeOS asks only for the fields needed by the selected function. It explains why each required answer matters.

A valid answer may be a concrete value, “none”, “unknown”, or “prefer not to provide” when the feature can still proceed safely with reduced personalisation. When essential information is withheld or unknown, LifeOS should either offer a more general version, preserve the missing assumption visibly, or decline the specific personalised action.

### 3. Optional enrichment

All other information remains optional and can be added progressively or through advanced settings to improve planning quality, analytics, automation, and convenience.

## Identity and physiological data

LifeOS should not treat sex, gender identity, age, height, weight, or similar information as universally interchangeable or universally necessary.

The product should request the specific information required by the current use case. For example:

- display identity may use the user's chosen name and optional gender information;
- age or date of birth may be relevant to eligibility, recovery, training load, or age-specific guidance;
- sex assigned at birth or other physiological information may be requested only when a calculation or plan materially depends on it;
- height, weight, body measurements, or fitness level should be required only for functions that use them.

The interface should explain the purpose and avoid forcing unrelated sensitive fields into ordinary calendar use.

## Lightweight initial setup

After account creation, LifeOS may ask for a small set of operational basics that materially improve the first calendar experience, for example:

- name or preferred display name;
- timezone and language;
- age or date of birth when included in the selected minimum profile;
- ordinary working or unavailable hours;
- typical sleep or quiet hours when the user wants them considered;
- default notification behaviour;
- whether to start from an empty calendar, import existing data, or create a first activity or goal.

Optional steps can be skipped. Fields required for the account or the selected first feature cannot be skipped without reducing or blocking that feature.

## Contextual information gates

Before LifeOS creates a structured plan, it performs a short context check.

The check determines:

1. which data the requested function needs;
2. which required data is already stored and still active;
3. which data is missing, uncertain, or contradictory;
4. whether the request can proceed fully, proceed in a reduced general mode, or must wait for clarification.

Examples:

### Astrophotography

The user asks to plan a night photographing the Milky Way. LifeOS checks location, date, travel availability, camera or phone, lenses, tripod, and other relevant equipment. If no camera is available, it should not silently schedule a camera-dependent workflow. It can instead propose a phone-compatible plan, an observation-only activity, equipment rental, or a preparation task.

### Nutrition

The user asks for a meal plan. LifeOS checks active allergies, coeliac status, dietary restrictions, foods to avoid, existing professional instructions, and other relevant constraints. Missing safety-critical answers must be resolved before presenting a personalised plan as compatible.

### Training

The user asks for a running plan. LifeOS checks age, current ability, equipment, injuries, rehabilitation restrictions, current workload, and available days. A known restriction against running blocks an incompatible proposal.

## Progressive profiling

LifeOS gathers additional information contextually instead of asking everything at once.

Examples:

- when creating a training program, ask about availability, equipment, current level, injuries, and active restrictions only if relevant;
- when creating a nutrition plan, ask about allergies, dietary restrictions, preferences, and existing professional instructions only if relevant;
- when creating a language plan, ask about current level, available time, preferred method, and target only if needed;
- when repeated scheduling conflicts appear, suggest adding or correcting availability rules;
- when the user rejects the same type of proposal repeatedly, ask whether that choice should become a reusable preference.

Contextual questions should be short, explain why the information matters, and avoid repeating facts already stored.

## Advanced profile mode

Settings include an optional advanced profile area where the user can proactively enter, review, and organise detailed information without waiting for a contextual prompt.

The advanced profile may include sections such as:

- identity, age, locale, and relevant physiological information;
- recurring availability and protected time;
- notification and review preferences;
- goals and priorities;
- work, study, family, travel, and personal routines;
- health, dietary, accessibility, and rehabilitation constraints;
- equipment, locations, transport, budget, and resources;
- learning preferences and current skill levels;
- planning, flexibility, confirmation, and replanning defaults;
- privacy, retention, sharing, and integration settings.

Advanced mode should expose more control without making ordinary use feel technical or overwhelming.

## Profile data model

Profile information should not be stored as one opaque biography. Each fact or rule should be structured and include, where relevant:

- value;
- category and scope;
- source;
- confirmation status;
- creation and update time;
- validity or expiry;
- sensitivity level;
- whether it is active, temporary, or archived;
- whether the user allows reuse in other domains.

This allows LifeOS to retrieve only the context needed for the current task and to resolve conflicts between old and new information.

## User control

The user can:

- skip optional onboarding steps;
- complete setup later;
- understand which fields are required for the account or current function;
- open advanced profile mode at any time;
- edit, deactivate, archive, or delete individual facts and rules;
- see why a contextual question is being asked;
- decide whether a one-time answer becomes a reusable preference;
- reset a profile section without deleting the whole account;
- export their profile and history.

LifeOS should never silently turn every isolated answer or temporary situation into a permanent personal rule.

## Product outcome

The intended experience is:

1. create the account quickly;
2. enter the product immediately;
3. provide a small operational baseline;
4. provide additional mandatory data only when a requested feature genuinely needs it;
5. build the rest of the profile naturally through real use;
6. use advanced settings when the user wants complete manual control.