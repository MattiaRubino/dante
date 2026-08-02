# LifeOS V1 — Calendar Contexts and Grouped Views

## Principle

LifeOS should support a unified personal schedule without forcing every item into one visually crowded stream.

Users can organise planning items into calendars or life areas such as Personal, Work, Family, Study, Health, or custom areas. The same data can then be viewed chronologically, grouped by area, or filtered to a selected focus.

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

## Today and calendar view modes

The same schedule can be displayed through several view modes:

### Unified chronological view

All visible items appear in time order. This is useful when the user wants to understand the complete day and detect overlaps.

### Grouped-by-calendar view

Items are separated into expandable areas such as Work, Personal, Family, or Study.

This helps users inspect a dense day without searching through one long mixed list. A user can open the Work area to see meetings and work blocks, then open Personal to see meals, errands, training, or social plans.

### Focus view

The user can temporarily show only one calendar or a selected combination, such as:

- Work only;
- Personal and Family;
- all shared items;
- everything except archived or low-priority calendars.

Saved focus presets may be added later without changing the underlying model.

## Presentation across devices

The grouping behaviour is a product requirement, while the exact interface belongs to the prototype phase.

Likely presentation directions include:

- expandable stacked sections on smaller screens;
- parallel lanes or columns on wider screens;
- compact summaries for collapsed calendars;
- persistent user preference for the default Today view.

The V1 prototype should test which representation remains readable with both light and very busy schedules.

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

Not every item fits a strict timeline. Grouped views should also account for:

- all-day items;
- flexible activities with a valid window;
- tasks due today but not yet scheduled;
- items awaiting confirmation;
- suggested or provisional placements.

These may appear in dedicated summary regions or within their calendar area, depending on the final prototype. Their underlying calendar assignment remains unchanged.

## External calendars

Imported or synchronised calendars can map to LifeOS calendars or remain distinct sources.

Examples:

- a connected company calendar maps to Work;
- a private Google calendar maps to Personal;
- a family calendar remains a separate Family area;
- multiple external calendars can be combined in one LifeOS focus view without merging or duplicating their source records.

Source identity and synchronisation metadata remain separate from the user's local organisational calendar.

## Colours and recognition

Calendars may have user-selected colours, names, icons, or ordering to improve recognition. Colour is a visual aid, not the only indicator, so labels and accessible distinctions remain necessary.

Shared status, item type, priority, and execution state should not be encoded only through the calendar colour.

## Recommended default behaviour

1. provide Personal and Work as optional starting calendars;
2. allow unlimited practical custom calendars or life areas;
3. keep sharing separate from calendar assignment;
4. assign each item one primary calendar while supporting tags and links;
5. offer unified, grouped, and focused views over the same canonical data;
6. preserve global conflict and workload detection across every visible or hidden group;
7. allow each participant to organise a shared item in their own local calendar;
8. test stacked and lane-based grouped presentations during the prototype phase;
9. avoid duplicating an item merely because it appears in several views or relationships.
