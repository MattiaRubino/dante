# LifeOS V1 — Learning Context and AI Boundary

## Principle

LifeOS is not an educational content provider, teacher, tutor, language school, or course platform.

Its role is to organise learning commitments, courses, lessons, assignments, exams, study sessions, materials, deadlines, progress, and follow-up inside the user's broader life plan.

The product may help the user define what to do, when to do it, how much time is realistically available, and how to adapt the plan. It does not need to generate the lesson itself.

## Product boundary

LifeOS may support:

- courses or subjects;
- academic periods, semesters, exam sessions, and certification windows;
- lessons as calendar events;
- assignments and deliverables as tasks or projects;
- study sessions as activities;
- exam preparation as a program;
- passing an exam, reaching B2, or completing a certification as a goal;
- materials, syllabi, notes, links, and source documents;
- deadlines, prerequisites, credits, attempts, grades, and user-reported results;
- backwards planning from an exam or submission date;
- workload balancing across subjects and the rest of the user's calendar;
- replanning after missed lessons, delayed assignments, or changed exam dates;
- progress based on planned versus actual activity and user declarations.

LifeOS does not need to provide:

- complete lessons;
- continuous tutoring;
- unlimited explanations;
- original course content;
- automatic grading as an authority;
- a replacement for teachers, schools, universities, language platforms, or certified training providers;
- large-scale generation of quizzes, flashcards, summaries, and exercises as a default core service.

## Example

For a goal such as reaching spoken English B2, LifeOS can:

- collect the current level, target period, available time, preferred learning format, and existing resources;
- propose a structured weekly allocation;
- schedule conversation practice, listening, lessons, revision, and external course work;
- track whether sessions happened and whether the user reports progress;
- rebalance the program when work, travel, illness, or other commitments interfere;
- attach external resources and providers chosen by the user.

LifeOS does not need to conduct every conversation lesson, explain every grammar topic, or generate all teaching material itself.

## External intelligence and content providers

When deeper teaching or content assistance is useful, LifeOS should treat it as an optional external capability.

Possible modes include:

1. manual hand-off: the user opens ChatGPT or another service with a structured prompt or exported context from LifeOS;
2. return import: the user imports a plan, lesson outline, assignment help, or study material created elsewhere;
3. linked provider: a future integration sends only the user-approved context needed for a specific request and returns a traceable result;
4. ChatGPT-side companion: LifeOS exposes approved tools and data through an app or MCP integration so the user can work with LifeOS from inside ChatGPT;
5. optional API-backed assistance: LifeOS uses a paid AI API for bounded features with quotas, premium pricing, or another sustainable commercial model;
6. user-supplied provider credentials as an advanced option, if security, support, and user experience are acceptable.

No external provider output silently becomes confirmed educational truth, a completed activity, or a permanent user fact. Source, date, provider, and user approval remain traceable.

## Cost and business boundary

LifeOS must not assume that unlimited tutoring can be funded inside a low-cost calendar subscription.

High-volume educational generation can create substantial inference cost and support complexity. Therefore:

- the core product remains useful without continuous AI generation;
- basic planning can use deterministic logic, templates, structured rules, and manual provider workflows;
- expensive AI actions should be explicit, bounded, cached where appropriate, and separated from ordinary calendar use;
- commercial partnerships or bundled access may be explored later but are not a dependency for V1;
- the initial architecture must keep AI providers replaceable and optional.

## ChatGPT integration direction

Two different integration directions must remain distinct:

### ChatGPT inside LifeOS

A native conversational assistant embedded in LifeOS normally requires an API or another commercial provider agreement. It should be limited to product actions, planning, retrieval, and selected assistance rather than unlimited tutoring.

### LifeOS inside ChatGPT

LifeOS may expose authorised tools and data through an app or MCP-based integration. In this model, the user interacts from ChatGPT and ChatGPT can read or update LifeOS within explicit permissions.

This direction may reduce the need to reproduce a full teaching assistant inside the LifeOS interface, while keeping LifeOS as the structured source of plans, commitments, history, and user controls.

The final commercial and technical model must be validated against provider terms, plan availability, privacy requirements, and actual usage costs before launch.

## V1 scope

For V1, the learning module should focus on:

- structure and scheduling;
- course, subject, lesson, assignment, exam, and study context;
- plans, deadlines, materials, and progress;
- workload and capacity;
- import and export;
- links to external learning resources and providers;
- manual or lightweight AI-assisted planning where useful.

Continuous AI tutoring, content generation, automatic quiz creation, and deep subject instruction are not required for V1.

## Recommended position

LifeOS organises the learning journey; it does not need to become the school.

The product should know what the user is trying to learn, what commitments and materials exist, what must happen next, what fits realistically, and how the plan should change. Teaching content can remain with teachers, courses, books, platforms, and optional connected assistants.