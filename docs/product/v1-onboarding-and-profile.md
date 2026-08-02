# LifeOS V1 — Onboarding and Progressive Profile

## Principle

Account creation should be fast and should not begin with a long questionnaire.

The user can register, sign in, and enter LifeOS immediately. A lightweight setup follows account creation, while deeper profile information is collected progressively only when it becomes useful or when the user chooses to provide it.

## Account entry

The initial account flow should require only what is necessary to create and secure the account, such as:

- authentication details;
- acceptance of required terms and privacy information;
- locale and timezone when they cannot be determined reliably;
- any mandatory account-security step.

The user should not be blocked by a broad lifestyle, health, productivity, or preference questionnaire before seeing the product.

## Lightweight initial setup

After account creation, LifeOS may ask for a small set of operational basics that materially improve the first calendar experience, for example:

- name or preferred display name;
- timezone and language;
- ordinary working or unavailable hours;
- typical sleep or quiet hours when the user wants them considered;
- default notification behaviour;
- whether to start from an empty calendar, import existing data, or create a first activity or goal.

The setup remains skippable where legally and technically possible. Missing information can be completed later.

## Progressive profiling

LifeOS gathers additional information contextually instead of asking everything at once.

Examples:

- when creating a training program, ask about availability, equipment, injuries, and active restrictions only if relevant;
- when creating a nutrition plan, ask about allergies, dietary restrictions, preferences, and existing professional instructions only if relevant;
- when creating a language plan, ask about current level, available time, preferred method, and target only if needed;
- when repeated scheduling conflicts appear, suggest adding or correcting availability rules;
- when the user rejects the same type of proposal repeatedly, ask whether that choice should become a reusable preference.

Contextual questions should be short, explain why the information matters, and avoid repeating facts already stored.

## Advanced profile mode

Settings include an optional advanced profile area where the user can proactively enter, review, and organise detailed information without waiting for a contextual prompt.

The advanced profile may include sections such as:

- identity and locale;
- recurring availability and protected time;
- notification and review preferences;
- goals and priorities;
- work, study, family, travel, and personal routines;
- health, dietary, accessibility, and rehabilitation constraints;
- equipment, locations, budget, and resources;
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
3. provide a few useful basics;
4. build the profile naturally through real use;
5. use advanced settings when the user wants complete manual control.
