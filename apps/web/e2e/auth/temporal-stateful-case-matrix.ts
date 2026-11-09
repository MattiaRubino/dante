/**
 * Approved v2 persona inventory: distinct multi-feature scenarios.
 * A failing scenario remains RED. Never weaken or omit a row to make a gate green.
 */
import type { Cadence, Subject } from './temporal-user-journey-support';

export type AreaMode = 'existing' | 'new' | 'none';
export type GoalKind = 'boolean' | 'quantity' | 'range' | 'qualitative';
export type PersonaPhase = 'one-off' | 'native-series' | 'converted-series';

type Base = Readonly<{
  id: string;
  kind: Subject;
  allDay: boolean;
  description: boolean;
  placementProtected: boolean;
  area: AreaMode;
  goalKinds: readonly GoalKind[];
}>;
export type EventCase = Base & Readonly<{
  kind: 'event';
  agendaCount: number;
}>;
export type ActivityCase = Base & Readonly<{
  kind: 'activity';
  intervalCount: number;
  plannedSessionCount: number;
}>;
export type PersonaCase = EventCase | ActivityCase;
export type RecurrenceCase = Readonly<{
  cadence: Exclude<Cadence, 'none'>;
  interval: number;
  monthlyOrdinal: boolean;
  repeatCount: number | null;
}>;

const goalOrder: readonly GoalKind[] = [
  'boolean', 'quantity', 'range', 'qualitative',
];

function goals(count: number, offset: number): readonly GoalKind[] {
  return Object.freeze(
    Array.from({ length: count }, (_, i) => goalOrder[(i + offset) % 4]!),
  );
}

// Every row has multiple fields. Rows 11-20 are deliberately high-density.
const eventRows: readonly Readonly<
  [number, number, AreaMode, boolean, boolean, boolean]
>[] = [
  [2, 1, 'existing', false, true, false],
  [3, 2, 'new', false, false, true],
  [4, 2, 'existing', true, true, false],
  [1, 3, 'none', false, true, true],
  [5, 1, 'new', false, true, false],
  [2, 3, 'new', true, true, true],
  [3, 2, 'existing', false, false, true],
  [4, 3, 'none', false, true, false],
  [5, 2, 'existing', true, true, true],
  [2, 4, 'new', false, true, true],
  [6, 4, 'existing', false, true, true],
  [7, 5, 'new', true, true, true],
  [8, 4, 'new', false, true, true],
  [5, 5, 'existing', false, true, true],
  [9, 3, 'new', false, true, true],
  [6, 4, 'existing', true, true, true],
  [7, 5, 'existing', false, true, true],
  [8, 5, 'new', false, true, true],
  [9, 5, 'new', true, true, true],
  [10, 5, 'existing', false, true, true],
];

const activityRows: readonly Readonly<
  [number, number, number, AreaMode, boolean, boolean, boolean]
>[] = [
  [2, 2, 2, 'existing', false, true, false],
  [3, 2, 2, 'new', false, false, true],
  [2, 3, 3, 'existing', false, true, true],
  [1, 3, 2, 'none', false, true, false],
  [4, 1, 3, 'new', false, true, true],
  [0, 2, 3, 'existing', true, true, true],
  [3, 4, 2, 'none', false, true, true],
  [2, 3, 4, 'new', false, true, false],
  [4, 4, 3, 'existing', false, false, true],
  [3, 5, 4, 'new', false, true, true],
  [5, 6, 4, 'existing', false, true, true],
  [5, 6, 5, 'new', false, true, true],
  [6, 7, 5, 'existing', false, true, true],
  [4, 7, 5, 'new', false, true, true],
  [6, 8, 4, 'existing', false, true, true],
  [0, 4, 5, 'new', true, true, true],
  [5, 8, 5, 'existing', false, true, true],
  [6, 8, 5, 'new', false, true, true],
  [7, 9, 5, 'existing', false, true, true],
  [7, 10, 5, 'new', false, true, true],
];

export const EVENT_CASES: readonly EventCase[] = Object.freeze(
  eventRows.map(([agendaCount, count, area, allDay, description,
                  placementProtected], index) => Object.freeze({
    id: 'E' + String(index + 1).padStart(2, '0'),
    kind: 'event' as const,
    allDay, description, placementProtected, area, agendaCount,
    goalKinds: goals(count, index),
  })),
);

export const ACTIVITY_CASES: readonly ActivityCase[] = Object.freeze(
  activityRows.map(([intervalCount, plannedSessionCount, count, area,
                     allDay, description, placementProtected], index) => Object.freeze({
    id: 'A' + String(index + 1).padStart(2, '0'),
    kind: 'activity' as const,
    allDay, description, placementProtected, area, intervalCount,
    plannedSessionCount, goalKinds: goals(count, index + 1),
  })),
);

export const PERSONA_CASES: readonly PersonaCase[] = Object.freeze([
  ...EVENT_CASES, ...ACTIVITY_CASES,
]);

const frequencies: readonly RecurrenceCase['cadence'][] = [
  'daily', 'weekly', 'monthly', 'custom', 'yearly',
];

export function recurrenceFor(persona: PersonaCase): RecurrenceCase {
  const index = Number(persona.id.slice(1)) - 1;
  if (!Number.isInteger(index) || index < 0 || index >= 20) {
    throw new Error('Unknown stateful case ' + persona.id);
  }
  const cadence = frequencies[index % frequencies.length]!;
  return Object.freeze({
    cadence,
    interval: cadence === 'custom' ? 2 : 1,
    monthlyOrdinal: cadence === 'monthly' && index % 2 === 0,
    repeatCount: index % 4 === 3 ? 5 : null,
  });
}

export function validatePersonaMatrix(): void {
  if (EVENT_CASES.length !== 20 || ACTIVITY_CASES.length !== 20) {
    throw new Error('Exactly 20 Event + 20 Activity configurations required.');
  }
  if (new Set(PERSONA_CASES.map((row) => row.id)).size !== 40) {
    throw new Error('Duplicated persona ID.');
  }
  for (const row of PERSONA_CASES) {
    if (!row.goalKinds.length || row.goalKinds.length > 5) {
      throw new Error(row.id + ': invalid Objective count');
    }
    if (row.kind === 'event') {
      if (row.agendaCount < 1 || row.agendaCount > 10) {
        throw new Error(row.id + ': invalid agenda count');
      }
    } else if (
      row.plannedSessionCount < 1 || row.plannedSessionCount > 10 ||
      (row.allDay && row.intervalCount !== 0) ||
      (!row.allDay && row.intervalCount < 1)
    ) {
      throw new Error(row.id + ': invalid Activity structure');
    }
  }
}
validatePersonaMatrix();
