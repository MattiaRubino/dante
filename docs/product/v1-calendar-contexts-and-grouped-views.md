# LifeOS V1 — Calendar Contexts and Grouped Views

## Principle

LifeOS should support a unified personal schedule without forcing every item into one visually crowded stream.

Users can organise planning items into calendars or life areas such as Personal, Work, Family, Study, Health, or custom areas. The same data can then be viewed chronologically, grouped by area, or filtered to a selected focus.

This document defines the product capability and data model only. It does not select a final visual layout, navigation pattern, column structure, card design, or mobile interaction. Those decisions remain open until the frontend prototype phase.

## Calendar or area versus sharing

Calendar context and sharing are separate concepts.

- Personal and Work are examples of calendars or life areas.
- Shared is a property of an item and its participants, not a mandatory third calendar.

An item can therefore be:

- Personal and private;
- Personal and shared;
- Work and private;
- Work and shared.

A shared canonical item may be assigned to a different local calendar by each participant. For example, the same dinner may be in one participant's Personal calendar and another participant's Family calendar. Shared facts remain common, while local organisation remains participant-specific.

## Default and custom calendars

A new account may begin with a small set of suggested calendars such as:

- Personal;
- Work.

Additional calendars are optional and user-defined. Examples include:

- Family;
- Study;
- Health and training;
- Travel;
- Creative projects;
- a specific client, course, or long-running project.

LifeOS must not force a large fixed taxonomy. Users can rename, reorder, archive, hide, or create calendars as their life requires.

Each planning item has one primary calendar or area for organisation. It may also carry tags, links to goals and programs, participants, and other contextual relationships without being duplicated across calendars.

## Required viewing capabilities

The same canonical schedule must support at least these logical capabilities:

- a unified chronological view of all selected calendars;
- grouping by calendar or life area;
- temporary focus on one calendar or a selected combination;
- inclusion or exclusion of shared items as a filter;
- preservation of user-selected visibility and ordering preferences.

These are functional requirements, not prescribed interface layouts.

A grouped view should help users inspect a dense day without searching through one long mixed stream. A focus view should make it possible to inspect combinations such as Work only, Personal and Family, all shared items, or everything except selected calendars.

Saved focus presets may be added later without changing the underlying model.

## Frontend decision deferred

The exact presentation is intentionally undecided.

During the frontend phase, the user and product team will evaluate alternatives using realistic light and busy schedules. Possible solutions may include sections, lanes, columns, compact summaries, filters, or other patterns, but none is selected by this document.

The prototype must determine separately for web and mobile:

- how calendars are expanded, collapsed, combined, or focused;
- how dense schedules remain readable;
- how hidden conflicts are surfaced;
- how all-day, flexible, and unscheduled items are represented;
- how the user's preferred view is retained.

No implementation should treat an example presentation discussed during product planning as a fixed requirement.

## Global schedule awareness

Grouping must not fragment scheduling logic.

LifeOS still evaluates the entire selected schedule when checking:

- time conflicts;
- workload;
- travel time;
- protected time;
- fixed commitments;
- replanning consequences;
- availability across calendars.

A conflict between a Work meeting and a Personal appointment must be visible even when the two items are displayed in separate groups or one group is collapsed.

Collapsed or filtered views must therefore surface important hidden conflicts and affected-item counts.

## All-day, flexible, and unscheduled items

Not every item fits a strict timeline. Grouped and focused capabilities must also account for:

- all-day items;
- flexible activities with a valid window;
- tasks due today but not yet scheduled;
- items awaiting confirmation;
- suggested or provisional placements.

Their exact presentation remains a frontend decision. Their underlying calendar assignment remains unchanged.

## External calendars

Imported or synchronised calendars can map to LifeOS calendars or remain distinct sources.

Examples:

- a connected company calendar maps to Work;
- a private Google calendar maps to Personal;
- a family calendar remains a separate Family area;
- multiple external calendars can be combined in one LifeOS focus without merging or duplicating their source records.

Source identity and synchronisation metadata remain separate from the user's local organisational calendar.

## Recognition and accessibility

Calendars may have user-selected colours, names, icons, or ordering to improve recognition. These are capabilities to evaluate during frontend design, not a fixed visual specification.

Colour must never be the only indicator. Shared status, item type, priority, and execution state also require accessible distinctions.

## Recommended product behaviour

1. provide Personal and Work as optional starting calendars;
2. allow practical custom calendars or life areas;
3. keep sharing separate from calendar assignment;
4. assign each item one primary calendar while supporting tags and links;
5. support unified, grouped, and focused inspection over the same canonical data;
6. preserve global conflict and workload detection across every visible or hidden group;
7. allow each participant to organise a shared item in their own local calendar;
8. leave the concrete web and mobile visualisation open until prototype review;
9. avoid duplicating an item merely because it appears in several views or relationships.
