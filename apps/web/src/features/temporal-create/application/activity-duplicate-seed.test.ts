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
  reminderLeadMinutes: 15,
  reminderScheduleRef: 'envelope',
  reminderStateRef: 'reminder-state',
  childGuardMode: 'none',
  objectives: [
    {
      objectiveRef: 'objective',
      label: 'Finire',
      resultKind: 'quantity',
      comparatorCode: 'gte',
      targetValue: 3,
      targetMin: null,
      targetMax: null,
      unitCode: 'pagine',
      presentationOrder: 0,
      observationRef: null,
      observedBoolean: null,
      observedNumeric: null,
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
        { id: 'new-objective', label: 'Finire', targetValue: '3' },
      ]);
    } finally {
      vi.unstubAllGlobals();
    }
  });
});
