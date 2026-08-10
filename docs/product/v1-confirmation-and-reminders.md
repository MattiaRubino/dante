# LifeOS V1 — Confirmation, Reminders, and Automatic Outcomes

## Principle

LifeOS must be proactive without becoming intrusive. Confirmation and reminder behaviour is configurable at several levels so the user can choose how much attention each type of item requires.

## Configuration hierarchy

Confirmation behaviour can be defined at:

1. global default level;
2. category or module level;
3. routine or program level;
4. individual planning-item level.

More specific settings override broader defaults.

## Outcome policy after an item ends

When an item reaches the end of its scheduled window without an explicit user update, LifeOS can apply one of these policies:

- ask immediately;
- ask later in the day;
- include it in an end-of-day review;
- include it in a weekly review;
- leave it as unconfirmed without notifying;
- mark it completed automatically;
- mark it not completed automatically;
- infer a provisional result from trusted integrations or measurable data, then request confirmation only when uncertain.

Automatic completion must never be the hidden universal default. It is suitable only when the user explicitly chooses it for a category, routine, program, or item where non-response reasonably means completion.

## Review cadence

The user can configure review moments such as:

- after an important item;
- at a chosen end-of-day time;
- on selected days of the week;
- at the end of the week;
- at the end of a routine or program cycle;
- only when unresolved items affect future planning.

A review groups unresolved items into one concise interaction instead of sending a separate notification for every item.

## Default behaviour proposal

The initial recommended defaults are:

- fixed appointments and ordinary events: no completion question unless they require an outcome or follow-up;
- important activities and program steps: ask at end of day if still unconfirmed;
- lightweight recurring habits: collect into the daily review;
- low-value or informational items: remain unconfirmed silently;
- automatic completion: disabled by default and enabled explicitly by the user;
- weekly review: surface unresolved items that still affect statistics, goals, or future plans.

These are product defaults, not hard rules.

## Fast confirmation

When confirmation is needed, LifeOS offers quick outcomes such as:

- completed;
- partially completed;
- skipped;
- not completed;
- postponed;
- replaced;
- cancelled.

Activities with measurable outcomes can also capture actual duration, quantity, distance, progress, or a short note.

## Notification control

The user can configure:

- whether confirmation prompts use push notifications, in-app prompts, or review summaries only;
- quiet hours;
- maximum reminder repetition;
- priority thresholds;
- whether missed confirmation should trigger replanning;
- whether similar items inherit the same choice in future.

LifeOS should learn explicit rules the user chooses, but should not silently convert a one-time response into a permanent preference.

## Examples

### Automatic completion

The user configures a simple medication reminder or routine checkpoint so that no response means completed. LifeOS marks it completed after the allowed window and records that the result was automatic rather than directly confirmed.

### End-of-day review

Several ordinary activities remain unresolved. At the configured review time, LifeOS asks about them together instead of sending repeated notifications during the day.

### Weekly review

Low-priority recurring activities are not confirmed daily. At the end of the week, LifeOS asks only about unresolved items that materially affect progress or future planning.

### Important item

A high-priority training session ends without confirmation. LifeOS requests an outcome because the result changes recovery, workload, and the remaining program.
