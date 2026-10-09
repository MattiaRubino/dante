import { describe, expect, it, vi } from 'vitest';

import { createRemoteActivityEditSettings } from './remote-activity-edit-settings';

const ref = '0199a111-1111-7111-8111-111111111111';
const response = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });

describe('Activity editor settings remote contract', () => {
  it('exits a stalled core save with an Italian retry message', async () => {
    vi.useFakeTimers();
    try {
      const fetchFn = vi.fn((input: RequestInfo | URL) => {
        if (String(input).endsWith('/auth/session'))
          return Promise.resolve(response({ authenticated: true, csrf_token: 'token' }));
        return new Promise<Response>(() => undefined);
      }) as unknown as typeof fetch;
      const source = createRemoteActivityEditSettings(fetchFn);
      const settings = {
        capture: { mode: 'disabled' as const, stateRef: null },
        reality: { mode: 'manual' as const, stateRef: null },
        schedules: [], objectives: [], lifeAreaRef: null,
        placementProtected: false, placementLockRevision: null,
        placementLockScheduleRef: null, reminderLeadMinutes: null,
        reminderScheduleRef: null, reminderStateRef: null, childGuardMode: 'none' as const,
      };
      const save = source.saveCore({ activityRef: ref, title: 'Prima',
        description: null, location: null, colorCode: null, revision: 0 },
      settings, { profile: { title: 'Dopo', description: null,
        location: null, colorCode: null } }, 'op');
      const failed = expect(save).rejects.toThrow('Salvataggio troppo lento');
      await vi.advanceTimersByTimeAsync(20_001);
      await failed;
    } finally {
      vi.useRealTimers();
    }
  });

  it('loads one snapshot and saves core changes in one guarded request', async () => {
    const paths: string[] = [];
    const requests: Record<string, unknown>[] = [];
    const fetchFn = vi.fn(
      (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
        const path =
          typeof input === 'string'
            ? input
            : input instanceof URL
              ? input.href
              : input.url;
        paths.push(path);
        if (init?.method === 'PUT') {
          if (typeof init.body !== 'string') throw new Error('Expected JSON body');
          expect(new Headers(init.headers).get('X-Dante-CSRF')).toBe('token');
          requests.push(JSON.parse(init.body) as Record<string, unknown>);
          return Promise.resolve(response({
            profile: { activity_ref: ref, title: 'Dopo', description: null,
              location: null, color_code: null, revision: 2 },
            capture: { activity_ref: ref, mode_code: 'live', state_ref: 'new-capture' },
            reality: { subject_kind: 'activity', subject_native_ref: ref,
              mode_code: 'review_on_end', state_ref: 'new-reality' },
            reminder: { schedule_ref: 'schedule', material_state_ref: 'new-reminder',
              enabled: true, lead_minutes: 30 },
          }));
        }
        if (path.endsWith('/auth/session'))
          return Promise.resolve(
            response({ authenticated: true, csrf_token: 'token' }),
          );
        if (path.endsWith('/edit-snapshot'))
          return Promise.resolve(
            response({
              activity_ref: ref,
              execution_policy: { activity_ref: ref, mode_code: 'disabled', state_ref: 'old-capture' },
              reality_policy: { subject_kind: 'activity', subject_native_ref: ref,
                mode_code: 'manual', state_ref: 'old-reality' },
              child_guard_mode: 'none',
              life_area_ref: null,
              objectives: [],
              placement_lock: null,
              reminder: { schedule_ref: 'schedule', material_state_ref: 'old-reminder',
                enabled: true, lead_minutes: 15 },
              schedules: [
                {
                  schedule_ref: 'schedule',
                  role_code: 'envelope',
                  display_name: 'Mattina',
                  presentation_order: 1,
                  placement_material_state_ref: 'placement',
                  temporal_form: 'named_zone_local',
                  zone_id: 'Europe/Rome',
                  starts_local_at: '2026-10-07T09:00:00',
                  ends_local_at: '2026-10-07T10:00:00',
                },
              ],
            }),
          );
        throw new Error(`Unexpected path ${path}`);
      },
    );
    const source = createRemoteActivityEditSettings(fetchFn);
    const settings = await source.load(ref);
    expect(paths).toEqual([`/api/v1/temporal/activities/${ref}/edit-snapshot`]);
    expect(settings.schedules[0]).toMatchObject({
      role: 'envelope',
      name: 'Mattina',
      start: '2026-10-07T09:00:00',
    });
    const saved = await source.saveCore({ activityRef: ref, title: 'Prima',
      description: null, location: null, colorCode: null, revision: 1 },
    settings, { profile: { title: 'Dopo', description: null, location: null,
      colorCode: null }, capture: 'live', reality: 'review_on_end',
      reminderLeadMinutes: 30 }, 'edit-op');
    expect(saved.profile).toMatchObject({ title: 'Dopo', revision: 2 });
    expect(saved.settings.capture).toEqual({ mode: 'live', stateRef: 'new-capture' });
    expect(saved.settings.reminderStateRef).toBe('new-reminder');
    expect(requests[0]).toEqual({
      operation_id: 'edit-op',
      profile: { expected_revision: 1, title: 'Dopo', description: null,
        location: null, color_code: null },
      capture: { mode_code: 'live', expected_state_ref: 'old-capture' },
      reality: { mode_code: 'review_on_end', expected_state_ref: 'old-reality' },
      reminder: { schedule_ref: 'schedule', expected_state_ref: 'old-reminder',
        enabled: true, lead_minutes: 30 },
    });
  });

  it('updates Activity placement protection through the canonical CAS endpoint', async () => {
    const received: Record<string, unknown>[] = [];
    const fetchFn = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const path = typeof input === 'string' ? input :
        input instanceof URL ? input.href : input.url;
      if (path.endsWith('/edit-snapshot')) return Promise.resolve(response({
        activity_ref: ref,
        execution_policy: { activity_ref: ref, mode_code: 'disabled', state_ref: null },
        reality_policy: { subject_kind: 'activity', subject_native_ref: ref,
          mode_code: 'manual', state_ref: null },
        child_guard_mode: 'none',
        life_area_ref: null,
        objectives: [],
        placement_lock: { schedule_ref: 'schedule', locked: false, revision: 3 },
        reminder: null,
        schedules: [{ schedule_ref: 'schedule', role_code: 'envelope',
          display_name: null, presentation_order: 0,
          placement_material_state_ref: 'state', temporal_form: 'named_zone_local',
          zone_id: 'Europe/Rome', starts_local_at: '2026-10-08T09:00:00',
          ends_local_at: '2026-10-08T10:00:00' }],
      }));
      if (path.endsWith('/auth/session'))
        return Promise.resolve(response({ authenticated: true, csrf_token: 'token' }));
      if (path.endsWith('/placement-lock') && init?.method === 'PUT') {
        received.push(JSON.parse(String(init.body)) as Record<string, unknown>);
        expect(new Headers(init.headers).get('X-Dante-CSRF')).toBe('token');
        return Promise.resolve(response({
          schedule_ref: 'schedule', locked: true, revision: 4,
          updated_at: '2026-10-08T09:00:00Z', replayed: false,
        }));
      }
      throw new Error(`Unexpected path: ${path}`);
    });
    const source = createRemoteActivityEditSettings(fetchFn);
    const before = await source.load(ref);
    expect(before.placementLockRevision).toBe(3);
    const after = await source.setPlacementProtected(before, true);
    expect(received).toEqual([{ locked: true, expected_revision: 3 }]);
    expect(after.placementProtected).toBe(true);
    expect(after.placementLockRevision).toBe(4);
  });

  it('reassigns the Life Area using its current canonical revision', async () => {
    const requests: Record<string, unknown>[] = [];
    const fetchFn = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const path = typeof input === 'string' ? input :
        input instanceof URL ? input.href : input.url;
      if (path.endsWith('/life-areas')) return Promise.resolve(response([
        { life_area_ref: 'area-1', name: 'Lavoro', archived: false },
        { life_area_ref: 'area-2', name: 'Personale', archived: true },
      ]));
      if (path.endsWith('/life-area-assignments')) return Promise.resolve(response([
        { subject_kind: 'activity', subject_native_ref: ref,
          life_area_ref: 'area-2', assignment_revision: 7 },
      ]));
      if (path.endsWith('/auth/session'))
        return Promise.resolve(response({ authenticated: true, csrf_token: 'token' }));
      if (path.endsWith(`/life-area-assignments/activities/${ref}`) && init?.method === 'PUT') {
        expect(new Headers(init.headers).get('X-Dante-CSRF')).toBe('token');
        requests.push(JSON.parse(String(init.body)) as Record<string, unknown>);
        return Promise.resolve(response({
          subject_kind: 'activity', subject_native_ref: ref,
          life_area_ref: 'area-1', assignment_revision: 8,
        }));
      }
      throw new Error(`Unexpected path: ${path}`);
    });
    const source = createRemoteActivityEditSettings(fetchFn);
    const choice = await source.loadLifeAreaChoice(ref);
    expect(choice.currentRef).toBe('area-2');
    expect(choice.options).toEqual([{ ref: 'area-1', name: 'Lavoro' }]);
    const saved = await source.assignLifeArea(ref, choice, 'area-1', 'edit-area-op');
    expect(requests).toEqual([{
      operation_id: 'edit-area-op',
      life_area_ref: 'area-1',
      expected_assignment_revision: 7,
    }]);
    expect(saved.currentRef).toBe('area-1');
    expect(saved.currentRevision).toBe(8);
  });


  it('sends complete interval retain/remove/add intent to coordinated preview', async () => {
    const requests: Record<string, unknown>[] = [];
    const fetchFn = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const path = typeof input === 'string' ? input :
        input instanceof URL ? input.href : input.url;
      if (path.endsWith('/auth/session'))
        return Promise.resolve(response({ authenticated: true, csrf_token: 'token' }));
      if (path.endsWith('/replan-preview') && init?.method === 'POST') {
        requests.push(JSON.parse(String(init.body)) as Record<string, unknown>);
        return Promise.resolve(response({ activity_ref: ref, changes: [] }));
      }
      throw new Error(`Unexpected path: ${path}`);
    });
    const source = createRemoteActivityEditSettings(fetchFn);
    const current = {
      capture: { mode: 'disabled' as const, stateRef: null },
      reality: { mode: 'manual' as const, stateRef: null },
      schedules: [
        { scheduleRef: 'keep', role: 'interval' as const, name: null, order: 1,
          placementStateRef: 'keep-state', temporalForm: 'named_zone_local',
          start: '2026-10-09T09:00:00', end: '2026-10-09T10:00:00',
          zoneId: 'Europe/Rome' },
        { scheduleRef: 'remove', role: 'interval' as const, name: null, order: 2,
          placementStateRef: 'remove-state', temporalForm: 'named_zone_local',
          start: '2026-10-09T11:00:00', end: '2026-10-09T12:00:00',
          zoneId: 'Europe/Rome' },
      ],
      objectives: [], lifeAreaRef: null,
      placementProtected: false, placementLockRevision: null,
      placementLockScheduleRef: null, reminderLeadMinutes: null,
      reminderScheduleRef: null, reminderStateRef: null, childGuardMode: 'none' as const,
    };
    await source.previewReplan(ref, current, {
      times: {
        keep: { start: '2026-10-09T09:00:00', end: '2026-10-09T10:00:00' },
        remove: { start: '2026-10-09T11:00:00', end: '2026-10-09T12:00:00' },
      },
      removedIntervals: ['remove'],
      newIntervals: [{ clientRef: 'new-interval', start: '2026-10-09T10:00',
        end: '2026-10-09T11:00' }],
      removedPlanned: [], newPlanned: [],
    }, 'replan-interval');
    expect(requests).toEqual([{
      operation_id: 'replan-interval',
      intervals: [{ schedule_ref: 'keep', expected_material_state_ref: 'keep-state',
        starts_local_at: '2026-10-09T09:00:00', ends_local_at: '2026-10-09T10:00:00' }],
      remove_intervals: [{ schedule_ref: 'remove',
        expected_material_state_ref: 'remove-state',
        starts_local_at: '2026-10-09T11:00:00', ends_local_at: '2026-10-09T12:00:00' }],
      new_intervals: [{ client_ref: 'new-interval',
        starts_local_at: '2026-10-09T10:00', ends_local_at: '2026-10-09T11:00' }],
      planned_sessions: [], place_planned_sessions: [], remove_planned_sessions: [], new_planned_sessions: [],
    }]);
  });

  it('revises the envelope directly when an Activity has no role intervals', async () => {
    const requests: Record<string, unknown>[] = [];
    const fetchFn = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const path = typeof input === 'string' ? input :
        input instanceof URL ? input.href : input.url;
      if (path.endsWith('/auth/session'))
        return Promise.resolve(response({ authenticated: true, csrf_token: 'token' }));
      if (path.endsWith('/replan-preview')) {
        requests.push(JSON.parse(String(init?.body)) as Record<string, unknown>);
        return Promise.resolve(response({ activity_ref: ref, changes: [] }));
      }
      throw new Error(`Unexpected path: ${path}`);
    });
    const source = createRemoteActivityEditSettings(fetchFn);
    const envelope = { scheduleRef: 'envelope', role: 'envelope' as const,
      name: null, order: 0, placementStateRef: 'state',
      temporalForm: 'named_zone_local', zoneId: 'Europe/Rome',
      start: '2026-10-09T09:00:00', end: '2026-10-09T12:00:00' };
    const settings = {
      capture: { mode: 'disabled' as const, stateRef: null },
      reality: { mode: 'manual' as const, stateRef: null },
      schedules: [envelope], objectives: [], lifeAreaRef: null,
      placementProtected: false, placementLockRevision: null,
      placementLockScheduleRef: null, reminderLeadMinutes: null,
      reminderScheduleRef: null, reminderStateRef: null, childGuardMode: 'none' as const,
    };
    await source.previewReplan(ref, settings, {
      times: { envelope: { start: '2026-10-09T10:00', end: '2026-10-09T13:00' } },
      removedIntervals: [], newIntervals: [], removedPlanned: [], newPlanned: [],
    }, 'replan-envelope');
    expect(requests[0]?.envelope).toEqual({
      schedule_ref: 'envelope', expected_material_state_ref: 'state',
      starts_local_at: '2026-10-09T10:00', ends_local_at: '2026-10-09T13:00',
    });
    expect(requests[0]?.intervals).toEqual([]);
  });


  it('authors an Objective through the canonical self-scoped endpoint', async () => {
    const received: Record<string, unknown>[] = [];
    const fetchFn = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const path = typeof input === 'string' ? input :
        input instanceof URL ? input.href : input.url;
      if (path.endsWith('/auth/session')) {
        return Promise.resolve(response({ authenticated: true, csrf_token: 'token' }));
      }
      if (path.endsWith(`/activities/${ref}/objectives`) && init?.method === 'POST') {
        expect(new Headers(init.headers).get('X-Dante-CSRF')).toBe('token');
        received.push(JSON.parse(String(init.body)) as Record<string, unknown>);
        return Promise.resolve(response({
          objective_ref: 'created-objective', label: '10 km',
          result_kind: 'quantity', comparator_code: 'gte',
          target_value: 10, target_min: null, target_max: null,
          unit_code: 'km', presentation_order: 3,
          observation_ref: null, observed_boolean: null, observed_numeric: null,
          qualitative_code: null, evaluation_state_ref: null,
          assessment_code: null,
        }));
      }
      throw new Error(`Unexpected path: ${path}`);
    });
    const source = createRemoteActivityEditSettings(fetchFn);
    const settings = {
      capture: { mode: 'disabled' as const, stateRef: null },
      reality: { mode: 'manual' as const, stateRef: null },
      schedules: [], objectives: [{
        objectiveRef: 'previous', label: 'Prima', resultKind: 'boolean' as const,
        comparatorCode: null, targetValue: null, targetMin: null, targetMax: null,
        unitCode: null, presentationOrder: 2, observationRef: null,
        observedBoolean: null, observedNumeric: null, qualitativeCode: null,
        evaluationStateRef: null, assessmentCode: null,
      }],
      lifeAreaRef: null, placementProtected: false, placementLockRevision: null,
      placementLockScheduleRef: null, reminderLeadMinutes: null,
      reminderScheduleRef: null, reminderStateRef: null, childGuardMode: 'none' as const,
    };
    const saved = await source.addObjective(ref, settings, {
      label: '10 km', resultKind: 'quantity', comparatorCode: 'gte',
      targetValue: 10, targetMin: null, targetMax: null, unitCode: 'km',
    }, 'add-objective-op');
    expect(received).toEqual([{
      operation_id: 'add-objective-op', label: '10 km',
      result_kind: 'quantity', comparator_code: 'gte',
      target_value: 10, target_min: null, target_max: null,
      unit_code: 'km', presentation_order: 3,
    }]);
    expect(saved.objectives.map((row) => row.objectiveRef))
      .toEqual(['previous', 'created-objective']);
    expect(settings.objectives).toHaveLength(1);
  });


  it('explicitly unassigns a primary Life Area with the existing revision', async () => {
    const requests: unknown[] = [];
    const fetchFn = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const path = typeof input === 'string' ? input :
        input instanceof URL ? input.href : input.url;
      if (path.endsWith('/life-areas')) {
        return Promise.resolve(response([{ life_area_ref: 'area-1',
          name: 'Lavoro', archived: false }]));
      }
      if (path.endsWith('/life-area-assignments')) {
        return Promise.resolve(response([{
          subject_kind: 'activity', subject_native_ref: ref,
          life_area_ref: 'area-1', assignment_revision: 4,
        }]));
      }
      if (path.endsWith('/auth/session')) {
        return Promise.resolve(response({ authenticated: true, csrf_token: 'token' }));
      }
      if (path.endsWith('/life-area-assignments/activities/' + ref) && init?.method === 'PUT') {
        requests.push(JSON.parse(String(init.body)) as unknown);
        return Promise.resolve(response({ subject_kind: 'activity', subject_native_ref: ref,
          life_area_ref: null, assignment_revision: 5, replayed: false }));
      }
      throw new Error('Unexpected request ' + path);
    });
    const source = createRemoteActivityEditSettings(fetchFn);
    const current = await source.loadLifeAreaChoice(ref);
    expect(current).toMatchObject({ currentRef: 'area-1', currentRevision: 4 });
    const updated = await source.assignLifeArea(ref, current, null, 'unassign-op');
    expect(updated).toMatchObject({ currentRef: null, currentRevision: 5 });
    expect(requests).toEqual([{ operation_id: 'unassign-op', life_area_ref: null,
      expected_assignment_revision: 4 }]);
  });

  it('revises only an existing planned Session display name with CAS', async () => {
    const requests: unknown[] = [];
    const scheduleRef = '0199a111-1111-7111-8111-222222222222';
    const fetchFn = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const path = typeof input === 'string' ? input :
        input instanceof URL ? input.href : input.url;
      if (path.endsWith('/auth/session')) {
        return Promise.resolve(response({ authenticated: true, csrf_token: 'token' }));
      }
      if (path.endsWith('/planned-sessions/' + scheduleRef + '/name') && init?.method === 'PUT') {
        requests.push(JSON.parse(String(init.body)) as unknown);
        return Promise.resolve(response({
          schedule_ref: scheduleRef, display_name: 'Ripasso', replayed: false,
        }));
      }
      throw new Error('Unexpected request ' + path);
    });
    const source = createRemoteActivityEditSettings(fetchFn);
    const saved = await source.revisePlannedName(ref, scheduleRef, 'Lettura', 'Ripasso');
    expect(saved).toBe('Ripasso');
    expect(requests).toEqual([{ expected_name: 'Lettura', name: 'Ripasso' }]);
  });

});
