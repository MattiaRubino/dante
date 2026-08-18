# Dante — Product Identity and North Star

**Status:** Accepted — current living product definition  
**Date:** 2026-08-13  
**Last identity-name update:** 2026-08-18  
**Nature:** Living Product Definition  
**Scope:** product identity, mission, foundational capabilities, boundaries and principles

**Current product/app name:** **Dante**  
**Previous working/project name:** `LifeOS`  
**Rename continuity:** `LifeOS` references in historical evidence, Git history and existing technical/repository identifiers refer to the same product lineage. This rename is naming-only and does not change the Product North Star, Domain Model, Logical Model or Physical Model semantics.

---

## 1. Purpose of this document

This document defines **what Dante is, what problem it exists to address, and which principles define its identity**.

It does not define in detail how those capabilities must be implemented. It therefore does not fix final navigation, UI layout, exact autonomy levels, notification frequency, pricing, AI providers, technical schemas, or the feature set of a specific release.

This is a **Living Product Definition**: it represents the best current shared definition of Dante and should guide product decisions while it remains valid.

It is not immutable. It may change when new evidence, simulations, real-world usage, technical constraints, commercial needs, or a better understanding of the product show that part of the definition should evolve.

Meaningful changes should be deliberate, documented and versioned rather than emerging accidentally from the implementation of one feature.

For kernel terminology and semantic distinctions, the current accepted **Domain Atlas** remains authoritative. This document governs product identity and overall product intent.

---

## 2. Definition of Dante

> **Dante is a personal operating system designed to help people understand, organize and improve their real life by turning intentions, needs and possibilities into outcomes they can realistically pursue.**
>
> **It maintains a structured, updateable representation of the user's situation, history, resources, constraints, commitments and relevant context; connects different parts of life; identifies opportunities and problems; helps compare alternatives; orchestrates competing demands and available capacity; builds and coordinates realistic paths; helps carry them out; observes what actually happens; and uses that knowledge to adapt what comes next.**
>
> **Dante does not seek to maximize productivity or take control away from the person. Its purpose is to reduce the distance between what a person wants, needs or could do and what they can realistically make happen, while respecting reality, history, safety, privacy and user authority.**

Internal product compass:

> **Understand life. Shape what comes next.**

This is not necessarily approved public marketing copy.

---

## 3. The problem Dante addresses

Real life is not naturally divided into calendars, tasks, Goals, notes, work, health, finance, relationships, hobbies and projects.

Those divisions mostly come from the tools used to manage life.

The same person may simultaneously have work, obligations, people to coordinate with, aspirations, personal activities, creative projects, financial concerns, things to maintain, learning paths, travel, routines, disruptions and many undeveloped ideas.

All of these draw from limited resources:

**time, attention, capacity, energy, money, people, tools and opportunities.**

They are also not independent. One choice may support several parts of life, conflict with others, or materially change what becomes realistic next.

A calendar mainly represents **when** something happens.

A task manager mainly represents **what needs to be done**.

A Goal tracker mainly represents **what outcome is desired**.

A note system mainly represents **what should be retained**.

A specialist application may represent one particular domain very well.

Dante aims to address **the system formed by all of these realities and the relationships between them**.

> **The mission of Dante is to help a person understand, coordinate and progressively shape their life as an interconnected system rather than forcing them to manage it as a collection of isolated tools and information.**

---

## 4. Life, not the task, is the center of the model

Dante must not reduce everything to a task, Event or Calendar item.

Meaningful persistent realities can exist even when they require no immediate action.

A person, vehicle, home, field, trip, song, document, course, Goal, Program, piece of equipment, animal, plant, project, relationship, idea or accumulated history may remain meaningful independently of what is scheduled today.

A vehicle is not the same thing as its next service appointment.

A song is not the same thing as the mixing Session scheduled at 18:00.

An English-learning path is not the same thing as Tuesday's lesson.

A Goal is not the same thing as the Activities created to pursue it.

> **Time is a foundational dimension of Dante, but it is not the container of the whole of life.**

At the same time, Dante must not impose structure where structure is unnecessary.

A simple appointment may remain a simple appointment without requiring a Goal, Project or Program.

---

## 5. The operating idea of Dante

Dante can be described through a set of capabilities that work together:

> **UNDERSTAND → DISCOVER → ORCHESTRATE → DECIDE → PLAN & COORDINATE → ACT → OBSERVE → LEARN & ADAPT**

This is not a mandatory workflow.

Not every situation requires every capability, and this document does not determine how autonomous or proactive Dante should be when using them.

A simple request should be allowed to remain simple.

### Understand

Dante builds enough structured context over time to understand the user's relevant situation.

When useful, that context may include intentions, commitments, Goals, Plans, Routines, resources, availability, capacity, Constraints, preferences, people, persistent personal information, previous Decisions, observed data, Outcomes and history.

This knowledge allows different parts of Dante to avoid starting from zero every time.

### Discover

Dante may identify possibilities, opportunities, changes or problems that become relevant to the user even when they were not already entered as tasks.

It may, for example, connect interests, objectives, availability and external reality.

An upcoming astronomical event may become relevant to someone interested in astrophotography.

An event may matter because of a known interest.

An old aspiration may become more realistic because circumstances changed.

A trajectory may reveal a problem before it becomes urgent.

> **A possibility discovered by Dante remains a possibility. It does not automatically become an action, a Decision or a permanent user preference.**

### Orchestrate

Dante should be able to consider multiple parts of life at the same time.

A person may have dozens of ideas, commitments, Goals and responsibilities. The role of the system is not simply to place all of them on a calendar.

Dante may help determine:

- what can coexist;
- what conflicts;
- what depends on something else;
- what can be combined;
- what should be protected;
- what can be postponed;
- what can be reduced;
- what may need to be paused;
- what is not realistically sustainable at the same time.

Orchestration is therefore not the independent optimization of every area.

> **Dante seeks coherence across the whole of life relative to the person's chosen direction and real limitations.**

A correct conclusion may simply be:

> **Not everything fits.**

### Decide

Dante may help the user compare alternatives and understand their consequences, costs, benefits, dependencies, incompatibilities, uncertainty and possible effects on the rest of life.

It may propose or recommend a direction.

A Dante proposal is not automatically a user Decision, and a Decision is not automatically what will actually happen.

### Plan & Coordinate

Dante may progressively turn something vague into a path that can actually be pursued.

An intention may evolve into a clearer desired result, a feasibility assessment, a Plan, optional Milestones, Activities, Sessions, Events, Schedules and other structures when those structures are useful.

Complexity should emerge when it produces value.

Dante should also be able to coordinate, when relevant, time, people, resources, Constraints, dependencies and external systems.

### Act

Dante does not necessarily have to stop at planning.

When an appropriate capability exists, it may help turn a Decision into concrete action.

It may modify its own state, organize activities, plan, replan, coordinate, prepare operations toward connected systems or carry out other permitted actions.

This document does not determine **how far** Dante should act autonomously.

Autonomy levels, required confirmations and authorization rules are defined separately according to context and consequence.

### Observe

Dante must distinguish what was planned from what actually happened.

A scheduled Session does not prove that the Session occurred.

Two elapsed hours do not prove that an Activity was completed.

Completion does not automatically prove that the desired Outcome was achieved.

> **Dante should represent reality instead of automatically making reality match the plan.**

Material history should not be silently rewritten to match current state.

### Learn & Adapt

Structured history can make Dante progressively more useful.

The system may detect patterns, improve estimates, identify recurring problems, compare planned and actual behavior, and propose future changes.

However:

**an observed pattern is not automatically a preference;  
a correlation does not prove causation;  
an AI inference is not a confirmed fact.**

When the evidence is insufficient, Dante may correctly leave things unchanged.

---

## 6. From intention to reality

Dante should be able to work with something before the user has turned it into a precise Goal.

Examples:

- “I want to learn English.”
- “One day I would like to go to Japan.”
- “I would like to publish an album.”
- “I want to change jobs.”
- “I would like to improve the yield of this field.”

A desire should not be immediately converted into a list of tasks.

Dante may first help understand it:

- what it actually means;
- how important it is;
- what it requires;
- which resources already exist;
- what is missing;
- which alternatives exist;
- which Constraints matter;
- how realistic it is;
- what a useful first step could be.

An idea may also remain inactive or mature over time.

> **Dante does not promise to make the user's dreams come true. It seeks to reduce the distance between what a person would like and what they can concretely begin to build, within the limits of reality and their actual possibilities.**

---

## 7. Managing overall complexity

Dante should support both people with very little to manage and people with very large amounts of activity and context.

A person may simultaneously have:

- non-negotiable obligations;
- important Goals;
- ideas;
- projects;
- routines;
- desires;
- people;
- things to maintain;
- financial constraints;
- exceptional periods;
- unexpected opportunities.

Not everything has to be active at the same time.

Dante should be able to help distinguish:

- what matters now;
- what can wait;
- what is incompatible;
- what can be combined;
- what needs protection;
- what is no longer worth maintaining.

The success of orchestration is not measured by the amount of material fitted into a plan.

> **Doing less may be better than planning everything.**

---

## 8. Effort, Execution, Outcome and Progress

Dante must preserve a foundational distinction:

> **Effort ≠ Execution ≠ Outcome ≠ Goal Progress**

For example:

> “I studied English for two hours.”

This may demonstrate two hours of Effort and the execution of a Session.

It does not automatically demonstrate improvement toward B2 proficiency.

If the Goal were to accumulate `100 hours of practice`, the hours would directly represent part of the target.

If the Goal were `reach B2 level`, time spent would be only one contributor to evaluating progress.

Dante may therefore use different progress sources depending on the nature of the Goal, including Quantity, Milestones, Outcomes, assessments, external evidence, user declarations, actual activity or other appropriate indicators.

> **Dante must not manufacture progress percentages merely to create the appearance that something is advancing.**

---

## 9. Measure without judging the person

Dante may use data, metrics, statistics, trends, comparisons and sophisticated indicators.

Their purpose should be to help understand something concrete.

The identity of Dante does not include:

- a universal `Life Score`;
- punitive streaks;
- a universal formula for a “correct life”;
- the assumption that more activity automatically means a better life;
- optimization whose purpose is to occupy every available minute.

Dante may say:

> “You slept less this month.”

> “This Goal is off trajectory.”

> “You are spending significantly more time than expected on this Activity.”

It should not collapse all of that into:

> “Your life is 71/100.”

---

## 10. External information, programs and knowledge

The user's life contains information created outside Dante.

Dante should be able to use it.

Examples may include:

- a course;
- learning materials;
- a diet;
- a training program;
- a rehabilitation program;
- a work-shift schedule;
- a travel itinerary;
- a maintenance program;
- a document;
- a checklist;
- a plan created by a professional or another system.

Dante may transform this information into structured operational context.

It may extract elements, retain them, connect them to the user's life, distribute them in time and follow their execution.

Where relevant, it should preserve:

**source, authorship and the nature of the original information.**

A later modification proposed by Dante must not appear as though it had been approved by the original author.

---

## 11. Dante, specialist tools and AI

Dante does not need to own every specialist capability required by human life.

It may help organize an English-learning path without necessarily being the tutor that teaches the language.

It may use a professional diet without being the professional who created it.

It may coordinate a specialist path without replacing the person or system that owns that expertise.

Specialist execution may happen through professionals, external software, services, integrations, external AI, or native Dante capabilities.

> **The fact that a capability already exists elsewhere does not make it unsuitable for Dante.**

If a capability is coherent with the product and implementing it directly produces enough value, Dante may provide it natively.

The choice between a **native capability, external integration, or both** is a product decision rather than an ideological limitation.

The same principle applies to AI.

Dante may use AI systems deeply, but:

> **Dante is not equivalent to a chatbot or to a specific AI model.**

The durable value of the product should continue to exist through structured context, history, relationships, Decisions, Constraints, Outcomes and integrations even when providers and models change.

The depth of native AI capability may evolve over time according to quality, usefulness, economic sustainability, safety and product strategy.

---

## 12. Dante may include many product categories without being reducible to one of them

Dante may also be an advanced calendar.

It may also be a task manager.

It may include Goal tracking.

It may include analytics.

It may include asset management.

It may use conversational AI.

It may include collaboration, project-management, data-recording, tracking and many other capabilities.

The point is not to exclude those categories.

> **The point is that none of them, taken individually, defines Dante.**

Calendar mainly represents a temporal dimension.

Tasks represent actions.

Goals represent desired outcomes.

Statistics represent observable aspects.

AI may provide reasoning and interaction.

Dante emerges from the way these and other capabilities are connected inside a coherent representation of the user's life.

---

## 13. Personal-first, not personal-only

Dante starts from the individual and their personal perspective.

But real life contains other people regardless of whether those people use Dante.

Friends, family members, colleagues, clients, professionals, patients, teachers, collaborators or other people may be relevant to what the user is managing.

Future Dante may support shared realities such as meetings, families, groups, teams, shifts, responsibilities, shared activities, common resources and other multi-actor scenarios.

This does not mean that Dante should automatically merge several people's personal systems into one workspace.

> **The direction is to coordinate shared reality while preserving, where needed, independence, personal perspectives, privacy, Responsibility, Participation, Authority and Visibility.**

A relevant person should be representable in Dante reality even without owning a Dante account.

---

## 14. Capability boundaries

Future capabilities may be thought about through broad categories.

These categories are **guidance, not rigid taxonomies or closed lists**.

### Core Identity

Capabilities without which Dante would lose its identity, including:

- structured understanding of context;
- connection between different parts of life;
- orchestration;
- planning and adaptation;
- distinction between planned and actual reality;
- history;
- user control;
- the ability to integrate external reality and information.

### Native Capabilities

Capabilities that Dante may provide directly when doing so is useful.

The set of native capabilities may grow over time.

### Connected Capabilities

Capabilities performed wholly or partly by people, services, applications, devices or external AI and coordinated by Dante.

### Domain Extensions

More specialized experiences built on the common Dante foundation to support particular life contexts.

They do not form a predefined taxonomy.

Learning, travel, creative work, home, vehicles, sport or agriculture are only examples of possible contexts.

### Out of Bounds

Behaviors or capabilities are incompatible with the identity of Dante when they:

- deliberately contradict foundational product principles;
- falsify reality, history, Authority, consent or progress;
- require Dante to become a system incompatible with its mission;
- introduce unjustifiable harm or risk relative to the value produced.

> **The simple fact that a capability already exists in another application is not a reason to exclude it from Dante.**

---

## 15. Personal context, privacy and information use

To be genuinely useful, Dante should be able to build **sufficiently rich personal context over time**.

Persistent information may have value across several parts of life.

For example, knowing that a person is lactose intolerant may matter when considering restaurants, travel, shopping, recipes or food-related planning.

Privacy does not require Dante to repeatedly forget useful information.

It requires the collection, retention, use, access and sharing of information to be governed appropriately.

> **Possessing information does not imply using it indiscriminately.**

Dante may reuse information across contexts when doing so genuinely benefits the user.

But the fact that Dante knows something does not mean it should always show it, use it for every Decision, share it with other people or reveal its cause when that is unnecessary.

> **Knowledge availability and entitlement to disclosure are different concepts.**

---

## 16. Personal autonomy and safety

Dante should not impose one universal view of success, productivity, balance, relationships, career, health or lifestyle.

Within appropriate limits, the user determines what matters to them.

Dante may support very different personal directions without turning preferences into moral judgments.

That principle does not mean absolute neutrality toward every possible request.

> **Not imposing an ideal life does not mean indiscriminately assisting every objective.**

Dante maintains appropriate safety, responsibility and policy guardrails.

It may therefore limit, refuse or redirect assistance that would facilitate serious harm, abuse, coercion, illegal behavior or other activity incompatible with applicable product policies.

Specific operational safety policies are defined separately from this product identity.

---

## 17. What Dante must not become

Dante must not evolve into:

- **a system that globally judges the quality or worth of a person;**
- **an engagement machine designed primarily to maximize time in app, notification volume or dependence on the product;**
- **a surveillance system that uses contextual understanding to improperly control other people;**
- **an optimization engine that assumes more productivity, more activity or more occupied time is automatically better;**
- **a system that invents Progress, Outcomes or certainty to make the experience feel more reassuring;**
- **a system that treats AI inference as confirmed fact;**
- **a system that silently rewrites the past to fit the present;**
- **a system that arbitrarily removes user control over material Decisions;**
- **a system that imposes a particular conception of a good life;**
- **a system that accumulates personal information without a product justification or appropriate controls.**

---

## 18. Foundational principles

### User Authority

The person remains the central authority over Decisions affecting their own life, within appropriate safety, legal and contextual boundaries.

### Reality Before Appearance

Dante should prefer an imperfect but truthful representation over a reassuring but false one.

### Historical Integrity

What actually happened is not silently rewritten because the plan or current state changed.

### Sustainable Reality

Free space on a calendar does not automatically equal real capacity.

### Orchestration Over Fragmentation

Where useful, Dante should connect different parts of life rather than create additional isolated silos.

### Progressive Complexity

Simple problems should remain simple.

Complexity should be exposed when it is genuinely useful.

### Rich Context With Controlled Use

Dante may build rich personal context, but its use and exposure should be governed appropriately.

### Source Integrity

Information originating from users, professionals, external systems or AI should retain appropriate Provenance when materially relevant.

### Honest Uncertainty

Dante should not pretend to know what it does not know.

### No Universal Life Ideology

Dante does not define one universal formula for a correct life.

### Safety

Assistance remains subject to appropriate limits intended to prevent harm, abuse and uses incompatible with product policies.

### Evolvability

The identity should be clear enough to guide the product and open enough to allow the product to evolve.

---

## 19. Evolution of this North Star

This document is not a complete list of everything Dante may eventually do.

It does not define every future feature.

It does not determine which domains Dante must support.

It does not define the maximum level of autonomy or intelligence Dante may eventually reach.

It does not define a final interface structure.

It defines **the current product direction**.

New capabilities may emerge from simulations, real use, research, technological progress or new needs.

A new capability should not be rejected merely because it was not imagined in this document.

Likewise, a capability described today may later be reduced, reframed or removed if it proves incoherent or insufficiently useful.

> **The North Star should prevent Dante from losing its identity, not prevent it from evolving.**

---

## 20. Summary

Dante starts from one premise:

> **A person's life is an interconnected system, not a collection of applications.**

The product should progressively understand that system, retain its history, connect its parts, identify possibilities and problems, help manage complexity, transform intentions into realistic paths, coordinate people and resources when useful, help act, observe reality and adapt what comes next.

It may be a calendar, planner, task manager, Goal system, analytics platform, AI assistant, coordination system and much more.

But it is not reducible to any one of those elements.

> **Dante exists to help a person turn what they want, need or could do into something they can genuinely understand, organize and progressively make happen, while keeping the different parts of life connected rather than managing them as separate worlds.**
