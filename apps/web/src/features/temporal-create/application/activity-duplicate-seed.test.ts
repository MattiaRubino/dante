import { describe, expect, it, vi } from 'vitest';

import type { ActivityProfile } from '../../temporal/remote-activity-inspector';
import type { ActivityEditSettings } from '../../temporal/remote-activity-edit-settings';
import { buildActivityDuplicateSeed } from './activity-duplicate-seed';

const profile: ActivityProfile = {
  activityRef: 'activity',
  title: 'Lavoro',
  description: 'Note',
  location: 'Studio',
  colorCode: '#123456',
  revision: 2,
};
const settings: ActivityEditSettings = {
  capture: { mode: 'record_and_live', stateRef: 'capture' },
  reality: { mode: 'review_on_end', stateRef: 'reality' },
  lifeAreaRef: 'area',
  placementProtected: true,
  placementLockRevision: 2,
  placementLockScheduleRef: 'envelope',
  reminderLeadMinutes: 15,
  reminderScheduleRef: 'envelope',
  reminderStateRef: 'reminder-state',
  childGuardMode: 'none',
  objectives: [
    {
      objectiveRef: 'objective',
      verificationMode: 'review_on_end',
      label: 'Finire',
      resultKind: 'quantity',
      comparatorCode: 'gte',
      targetValue: 3,
      targetMin: null,
      targetMax: null,
      unitCode: 'pagine',
      presentationOrder: 0,
      observationRef: 'old-observation',
      observedBoolean: null,
      observedNumeric: 3,
      qualitativeCode: null,
      evaluationStateRef: null,
      assessmentCode: null,
    },
  ],
  schedules: [
    {
      scheduleRef: 'envelope',
      role: 'envelope',
      name: null,
      order: 0,
      placementStateRef: 'state',
      temporalForm: 'named_zone_local',
      start: '2026-10-07T09:00:00',
      end: '2026-10-07T12:00:00',
      zoneId: 'Europe/Rome',
    },
    {
      scheduleRef: 'first',
      role: 'interval',
      name: null,
      order: 1,
      placementStateRef: 'state',
      temporalForm: 'named_zone_local',
      start: '2026-10-07T09:00:00',
      end: '2026-10-07T10:00:00',
      zoneId: 'Europe/Rome',
    },
    {
      scheduleRef: 'second',
      role: 'interval',
      name: null,
      order: 2,
      placementStateRef: 'state',
      temporalForm: 'named_zone_local',
      start: '2026-10-07T11:00:00',
      end: '2026-10-07T12:00:00',
      zoneId: 'Europe/Rome',
    },
    {
      scheduleRef: 'session',
      role: 'planned',
      name: 'Revisione',
      order: 1,
      placementStateRef: 'state',
      temporalForm: 'named_zone_local',
      start: '2026-10-07T11:00:00',
      end: '2026-10-07T11:30:00',
      zoneId: 'Europe/Rome',
    },
  ],
};

describe('Activity duplicate draft', () => {
  it('prefills the Create intent with distinct intervals, planned sessions and objectives', () => {
    vi.stubGlobal('crypto', {
      randomUUID: vi
        .fn()
        .mockReturnValueOnce('new-interval')
        .mockReturnValueOnce('new-session')
        .mockReturnValueOnce('new-objective'),
    });
    try {
      const copied = buildActivityDuplicateSeed(profile, settings);
      expect(copied.fields).toMatchObject({
        title: 'Lavoro',
        notes: 'Note',
        contextId: 'area',
        date: '2026-10-07',
        startTime: '09:00',
        durationMinutes: 60,
        timeZoneId: 'Europe/Rome',
        confirmation: { reminderLeadMinutes: 15 },
        event: { location: 'Studio' },
      });
      expect(copied.advanced.activityStructure).toMatchObject({
        captureMode: 'record_and_live',
        placementProtected: true,
        activityIntervals: [{ id: 'new-interval', startTime: '11:00' }],
        plannedSlices: [{ id: 'new-session', title: 'Revisione' }],
      });
      expect(copied.advanced.objectives).toMatchObject([
        {
          id: 'new-objective',
          label: 'Finire',
          targetValue: '3',
          verificationMode: 'review_on_end',
        },
      ]);
      expect(copied.advanced.objectives?.[0]).not.toHaveProperty(
        'objectiveRef',
      );
      expect(copied.advanced.objectives?.[0]).not.toHaveProperty(
        'observedNumeric',
      );
      expect(copied.advanced.objectives?.[0]).not.toHaveProperty(
        'observationRef',
      );
      expect(copied.advanced.activityStructure?.plannedSlices).toMatchObject([
        { title: 'Revisione', timeEnabled: false },
      ]);
    } finally {
      vi.unstubAllGlobals();
    }
  });

  it('duplicates an all-day Activity with untimed named Sessions without changing its day range', () => {
    vi.stubGlobal('crypto', {
      randomUUID: vi.fn()
        .mockReturnValueOnce('copied-session-a')
        .mockReturnValueOnce('copied-session-b')
        .mockReturnValueOnce('copied-objective'),
    });
    try {
      const allDay: ActivityEditSettings = {
        ...settings,
        schedules: [
          {
            scheduleRef: 'all-day-envelope',
            role: 'envelope',
            name: null,
            order: 0,
            placementStateRef: 'all-day-state',
            temporalForm: 'date_span',
            start: '2026-11-16',
            end: '2026-11-18',
            zoneId: null,
          },
          {
            scheduleRef: 'planned-one',
            role: 'planned',
            name: 'Ripasso',
            order: 2,
            placementStateRef: null,
            temporalForm: null,
            start: null,
            end: null,
            zoneId: null,
          },
          {
            scheduleRef: 'planned-two',
            role: 'planned',
            name: 'Lettura',
            order: 1,
            placementStateRef: null,
            temporalForm: null,
            start: null,
            end: null,
            zoneId: null,
          },
        ],
      };
      const seed = buildActivityDuplicateSeed(profile, allDay);
      expect(seed.fields).toMatchObject({
        kind: 'activity',
        title: 'Lavoro',
        timeSemantics: 'all-day',
        date: '2026-11-16',
        contextId: 'area',
      });
      expect(seed.fields).not.toHaveProperty('startTime');
      expect(seed.fields).not.toHaveProperty('durationMinutes');
      expect(seed.advanced.endDate).toBe('2026-11-17');
      expect(seed.advanced.activityStructure?.placementProtected).toBe(true);
      expect(seed.advanced.activityStructure?.activityIntervals).toEqual([]);
      expect(seed.advanced.activityStructure?.plannedSlices).toMatchObject([
        { title: 'Lettura', timeEnabled: false },
        { title: 'Ripasso', timeEnabled: false },
      ]);
      expect(seed.advanced.activityStructure?.plannedSlices).toHaveLength(2);
      expect(seed.advanced.objectives?.map((row) => row.label)).toEqual([
        'Finire',
      ]);
      expect(seed.advanced.objectives?.[0]).not.toHaveProperty('objectiveRef');
      expect(seed.advanced.objectives?.[0]).not.toHaveProperty('observationRef');
    } finally {
      vi.unstubAllGlobals();
    }
  });

  it('rejects inconsistent date-span Activities with separate time intervals', () => {
    const invalid: ActivityEditSettings = {
      ...settings,
      schedules: [
        {
          scheduleRef: 'all-day-envelope',
          role: 'envelope',
          name: null,
          order: 0,
          placementStateRef: 'date-state',
          temporalForm: 'date_span',
          start: '2026-11-16',
          end: '2026-11-18',
          zoneId: null,
        },
        {
          scheduleRef: 'interval',
          role: 'interval',
          name: null,
          order: 1,
          placementStateRef: 'interval-state',
          temporalForm: 'named_zone_local',
          start: '2026-11-16T09:00:00',
          end: '2026-11-16T10:00:00',
          zoneId: 'Europe/Rome',
        },
      ],
    };
    expect(() => buildActivityDuplicateSeed(profile, invalid)).toThrow(
      'L’intervallo a giorni non è duplicabile in questa forma.',
    );
  });
});
