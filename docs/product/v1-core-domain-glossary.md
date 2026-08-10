# LifeOS V1 — Core Domain Glossary

## Purpose

This glossary defines the canonical meaning of the main product concepts. It prevents calendar, project, program, routine, module, sharing, and source terminology from becoming interchangeable during design and implementation.

## Planning item

A planning item is the shared foundation for something that may appear in time, require reminders, carry notes or links, participate in scheduling, or produce history.

Planning items use explicit types. The shared foundation does not mean every type has the same fields, states, or behaviour.

## Event

An event represents something expected to occur at a date, time, or all-day period.

Examples include an appointment, meeting, dinner, flight, ceremony, call, or external commitment.

Events are generally time-centred. Some events may have preparation, travel, attendance, outcomes, or follow-up, but ordinary events do not require completion tracking.

## Activity or task

An activity represents work or action the user intends to perform.

It may be fixed, flexible, deadline-constrained, measurable, divisible, optional, or connected to another structure.

A task is an activity whose main purpose is completing a defined piece of work. The interface may use either term according to context without creating separate unrelated models.

## Reminder

A reminder is a lightweight prompt to remember information or perform a small action.

It may remain independent or point to another object. It should not require the complete behaviour of an activity when a simple notification is sufficient.

## Calendar block

A calendar block reserves or protects time without necessarily representing a concrete outcome.

Examples include focus time, unavailable time, travel buffer, recovery, preparation, or a placeholder.

## Routine

A routine is a reusable rule or pattern that generates or guides recurring activity.

It expresses repeated behaviour such as training every Monday, reviewing the week on Sunday, or taking a regular break.

A routine is not simply a list of already materialised occurrences. Individual occurrences can be changed without rewriting the entire routine.

## Goal

A goal describes a result or direction the user wants to reach.

Examples include reaching spoken English B2, completing a release, improving fitness, saving a target amount, or organising a trip.

A goal may exist without a detailed plan. It can be supported by several programs, projects, routines, and independent activities.

## Program

A program is an organised path intended to produce progress through phases, sessions, rules, milestones, or progression logic.

Programs are suited to structured development over time, such as a language-learning plan, training cycle, rehabilitation plan, study curriculum, or staged personal-development plan.

A program may adapt, pause, version, finish, or be replaced while preserving the historical structure that governed past execution.

## Project

A project is a finite body of coordinated work intended to deliver one or more concrete outputs.

Examples include publishing an album, developing LifeOS, moving house, organising a large event, preparing a professional release, or completing a client deliverable.

A project may contain milestones, tasks, meetings, decisions, documents, dependencies, and deadlines. Unlike a routine, it is not primarily repetitive. Unlike a program, it does not necessarily use progression or repeated sessions. Unlike a goal, it describes the organised work and deliverables rather than only the desired result.

Projects in personal V1 remain user-managed structures. Team assignment, enterprise workflows, and shared project administration are deferred.

## Milestone

A milestone marks a meaningful checkpoint, decision, delivery, or achievement inside a goal, program, or project.

It may have a date or condition but does not need to contain all the execution behaviour of an activity.

## Calendar or life area

A calendar or life area is the user's primary organisational context for an item, such as Personal, Work, Family, Study, Health, or a custom area.

It affects organisation, filtering, visibility, defaults, and analysis. It does not define whether the item is shared.

Each item has one primary calendar or area and may also use tags and links.

## Module

A module is a domain-specific capability that extends the common LifeOS foundation.

Examples may include training, nutrition, learning, travel, finance, creative work, or another specialised domain.

A module may add measurements, rules, views, integrations, or templates. It does not replace common calendar, activity, goal, program, project, history, privacy, or user-control concepts.

## Tag

A tag is a lightweight reusable label used for filtering or organisation.

Tags do not establish ownership, lifecycle, scheduling rules, or canonical parent relationships.

## Person-related commitment

A person-related commitment is a personal item whose meaning involves another person, such as replying, delivering something, keeping a promise, or following up.

It does not require the other person to have a LifeOS account and is not automatically a shared item.

## Shared item

A shared item has canonical facts used by more than one participant, plus participant-specific state.

Sharing is independent from calendar assignment. Each participant may organise the same item in a different local calendar while preserving common shared facts.

Complete account-to-account sharing is outside the first personal V1 release, but the model must not prevent it.

## Participant

A participant is a person or account associated with an event or activity.

Participant data can include attendance state, personal reminders, local organisation, private notes, confirmation, and permissions where supported.

A referenced external person does not automatically become a registered participant.

## Source

A source identifies where data originated, such as direct user entry, uploaded file, external calendar, email, meeting provider, imported professional plan, or AI proposal.

Source identity remains separate from the user's local calendar, object type, and sharing state.

## Provenance

Provenance explains how a value, result, decision, or change entered the system and how reliable or confirmed it is.

Examples include user-confirmed, imported, automatically applied by an approved rule, inferred and awaiting confirmation, or proposed by AI and approved by the user.

## Temporary mode

A temporary mode is a time-bounded override to normal context and planning behaviour, such as holiday, illness, travel, exams, intense work, or reduced availability.

It changes selected rules temporarily without rewriting the user's long-term profile.

## Inbox item

An inbox item is captured information that has not yet been fully classified or scheduled.

It may later become an event, activity, reminder, goal, program, project, constraint, personal fact, document, note, or remain unresolved.

## Decision record

A decision record preserves what was decided, why, when it becomes effective, who or what proposed it, who approved it, and which objects were affected.

It is distinct from a generic note because it supports explanation, history, comparison, and future reasoning.

## Canonical distinction summary

- a calendar or life area answers **where this belongs in the user's organisation**;
- a type answers **what this object is**;
- a goal answers **what result is wanted**;
- a project answers **what finite work and deliverables must be coordinated**;
- a program answers **what structured progression should be followed**;
- a routine answers **what pattern should recur**;
- a module answers **which specialised domain rules apply**;
- a source answers **where the information came from**;
- sharing answers **who participates in the same canonical item**;
- tags answer **how the user wants to label and find it**.
