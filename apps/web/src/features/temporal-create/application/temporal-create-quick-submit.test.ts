import { describe, expect, it } from 'vitest';

import { createTemporalCreateFields } from '../model/temporal-create-session';
import {
  createTemporalCreateU2AuthoringDraft,
  patchTemporalCreateU2AuthoringDraft,
} from '../model/temporal-create-u2-authoring';
import {
  buildTemporalCreateRecurringActivityTemplate,
  buildTemporalCreateObjectiveTemplates,
  buildTemporalCreateU2Request,
  temporalCreateU2QuickIntentSupported,
  temporalCreateRecurringEventSharedIntentSupported,
  validateTemporalCreateU2QuickFields,
  validateTemporalCreateU6Structure,
  validateTemporalCreateU6StructureIssue,
} from './temporal-create-u2-submit';

describe('minute-exact U2 submit mappings', () => {
  it.each(['activity', 'event'] as const)(
    'preserves 10:30–10:31 on the outgoing %s request',
    (kind) => {
      const fields = createTemporalCreateFields({
        kind,
        title: 'One minute exactly',
        date: '2026-10-16',
        startTime: '10:30',
        durationMinutes: 1,
      });
      const draft = createTemporalCreateU2AuthoringDraft(fields);
      expect(validateTemporalCreateU2QuickFields(fields)).toEqual([]);
      const result = buildTemporalCreateU2Request(
        fields,
        draft,
        `minute-precision:${kind}`,
      );
      expect(result.kind).toBe(kind);
      expect(result.request.placement?.kind).toBe('floating-local-interval');
      const placement = result.request.placement;
      if (placement?.kind !== 'floating-local-interval') {
        throw new Error('Expected canonical floating interval.');
      }
      expect(placement.startsLocalAt.toString()).toBe('2026-10-16T10:30:00');
      expect(placement.endsLocalAt.toString()).toBe('2026-10-16T10:31:00');
    },
  );

  it('preserves non-quarter-hour Activity interval boundaries in the authoring graph', () => {
    const fields = createTemporalCreateFields({
      kind: 'activity',
      title: 'Two precise occupied bands',
      date: '2026-10-16',
      startTime: '10:30',
      durationMinutes: 1,
    });
    const base = createTemporalCreateU2AuthoringDraft(fields);
    const draft = patchTemporalCreateU2AuthoringDraft(base, {
      activityStructure: {
        ...base.activityStructure,
        activityIntervals: [
          {
            id: 'extra-minute',
            date: '2026-10-16',
            startTime: '10:37',
            endDate: '2026-10-16',
            endTime: '10:38',
          },
        ],
      },
    });
    expect(validateTemporalCreateU6Structure(fields, draft)).toBeNull();
    const result = buildTemporalCreateU2Request(
      fields,
      draft,
      'minute-precision:bands',
    );
    if (result.kind !== 'activity') throw new Error('Expected Activity.');
    const placements = result.request.activityIntervals;
    expect(placements).toHaveLength(2);
    const boundaries = placements?.map((placement) => {
      if (placement.kind !== 'floating-local-interval') {
        throw new Error('Expected floating local Activity interval.');
      }
      return [
        placement.startsLocalAt.toString(),
        placement.endsLocalAt.toString(),
      ];
    });
    expect(boundaries).toEqual([
      ['2026-10-16T10:30:00', '2026-10-16T10:31:00'],
      ['2026-10-16T10:37:00', '2026-10-16T10:38:00'],
    ]);
  });
});

describe('U2 Quick Create submit mapping', () => {
  it('keeps an untimed named Session in every recurring Activity template', () => {
    const fields = createTemporalCreateFields({
      kind: 'activity',
      title: 'Raccolta',
      date: '2026-10-12',
      startTime: '10:15',
      durationMinutes: 30,
    });
    const base = createTemporalCreateU2AuthoringDraft(fields);
    const draft = patchTemporalCreateU2AuthoringDraft(base, {
      activityStructure: {
        ...base.activityStructure,
        plannedSlices: [
          {
            id: 'session',
            title: 'Cernita',
            timeEnabled: false,
            date: '2026-10-12',
            startTime: '',
            endTime: '',
          },
        ],
      },
    });
    expect(
      buildTemporalCreateRecurringActivityTemplate(fields, draft).template
        .planned_slices,
    ).toEqual([{ name: 'Cernita', time_enabled: false }]);
  });
  it('authors an unassigned Activity with canonical description, location and item colour', () => {
    const fields = createTemporalCreateFields({
      kind: 'activity',
      title: 'Passeggiata',
      date: '2026-09-30',
      startTime: '23:30',
      durationMinutes: 1530,
      contextId: '',
      notes: 'Lungo il fiume',
      event: {
        ...createTemporalCreateFields({ date: '2026-09-30' }).event,
        location: 'Lungofiume',
      },
    });
    const draft = patchTemporalCreateU2AuthoringDraft(
      createTemporalCreateU2AuthoringDraft(fields),
      { endDate: '2026-10-02', itemColorCode: '#12ABEF' },
    );

    expect(validateTemporalCreateU2QuickFields(fields)).toEqual([]);
    expect(temporalCreateU2QuickIntentSupported(fields)).toBe(true);

    const mapped = buildTemporalCreateU2Request(fields, draft, 'u2:activity');
    expect(mapped.kind).toBe('activity');
    if (mapped.kind !== 'activity')
      throw new Error('Expected Activity request.');
    expect(mapped.request.lifeArea).toBeUndefined();
    expect(mapped.request.itemColorCode).toBe('#12ABEF');
    expect(mapped.request.description).toBe('Lungo il fiume');
    expect(mapped.request.location).toBe('Lungofiume');
    expect(mapped.request.placement?.kind).toBe('floating-local-interval');
    if (mapped.request.placement?.kind !== 'floating-local-interval') {
      throw new Error('Expected floating placement.');
    }
    expect(mapped.request.placement.startsLocalAt.toString()).toBe(
      '2026-09-30T23:30:00',
    );
    expect(mapped.request.placement.endsLocalAt.toString()).toBe(
      '2026-10-02T01:00:00',
    );
  });

  it('creates a new Life Area only as part of the final authoring request', () => {
    const fields = createTemporalCreateFields({
      title: 'Studio',
      date: '2026-09-30',
      contextId: '',
    });
    const draft = patchTemporalCreateU2AuthoringDraft(
      createTemporalCreateU2AuthoringDraft(fields),
      {
        lifeArea: Object.freeze({
          kind: 'new' as const,
          name: 'Formazione',
          colorCode: '#8A4FFF',
        }),
      },
    );

    const mapped = buildTemporalCreateU2Request(fields, draft, 'u2:new-area');
    expect(mapped.request.lifeArea).toEqual({
      newName: 'Formazione',
      colorCode: '#8A4FFF',
    });
    expect(mapped.request.itemColorCode).toBeUndefined();
  });

  it('does not revise an existing Life Area colour until the user changed it', () => {
    const fields = createTemporalCreateFields({
      title: 'Palestra',
      date: '2026-09-30',
    });
    const base = createTemporalCreateU2AuthoringDraft(fields);
    const selected = patchTemporalCreateU2AuthoringDraft(base, {
      lifeArea: Object.freeze({
        kind: 'existing' as const,
        lifeAreaRef: '0199a111-1111-7111-8111-111111111111',
        label: 'Salute',
        expectedRevision: 7,
        colorCode: '#00AA55',
        colorChanged: false,
      }),
    });
    const unchanged = buildTemporalCreateU2Request(
      fields,
      selected,
      'u2:selected-area',
    );
    expect(unchanged.request.lifeArea).toEqual({
      lifeAreaRef: '0199a111-1111-7111-8111-111111111111',
    });

    if (selected.lifeArea.kind !== 'existing') {
      throw new Error('Expected existing Life Area draft.');
    }
    const edited = patchTemporalCreateU2AuthoringDraft(selected, {
      lifeArea: Object.freeze({
        ...selected.lifeArea,
        colorCode: '#FF8800',
        colorChanged: true,
      }),
    });
    const changed = buildTemporalCreateU2Request(
      fields,
      edited,
      'u2:edited-area',
    );
    expect(changed.request.lifeArea).toEqual({
      lifeAreaRef: '0199a111-1111-7111-8111-111111111111',
      expectedRevision: 7,
      colorCode: '#FF8800',
    });
  });

  it('maps Event location, description and agenda without changing Event identity', () => {
    const baseline = createTemporalCreateFields({
      kind: 'event',
      title: 'Workshop',
      date: '2026-09-30',
      notes: 'Decisioni di progetto',
    });
    const fields = createTemporalCreateFields({
      ...baseline,
      event: {
        ...baseline.event,
        location: 'Sala A',
        agendaParts: Object.freeze([' Revisione ', '', 'Decisioni', '   ']),
      },
    });
    const draft = createTemporalCreateU2AuthoringDraft(fields);

    const mapped = buildTemporalCreateU2Request(fields, draft, 'u2:event');
    expect(mapped.kind).toBe('event');
    if (mapped.kind !== 'event') throw new Error('Expected Event request.');
    expect(mapped.request.location).toBe('Sala A');
    expect(mapped.request.description).toBe('Decisioni di progetto');
    expect(mapped.request.agendaParts).toEqual(['Revisione', 'Decisioni']);
  });

  it('keeps all-day multi-day Events on canonical U2 after Start date changes', () => {
    const opened = createTemporalCreateFields({
      kind: 'event',
      title: 'Fiera',
      date: '2026-10-14',
    });
    const edited = createTemporalCreateFields({
      ...opened,
      date: '2026-10-15',
      timeSemantics: 'all-day',
      event: {
        ...opened.event,
        allDayEndDate: '2026-10-17',
      },
    });
    // Selecting a date does not edit inactive Scheduling dates; they retain
    // their 14 October defaults. This must not divert Event authoring to
    // the historical runtime before the canonical HTTP request.
    expect(edited.scheduling.windowStartDate).toBe('2026-10-14');
    expect(temporalCreateU2QuickIntentSupported(edited)).toBe(true);
    expect(temporalCreateRecurringEventSharedIntentSupported(edited)).toBe(
      true,
    );
    const mapped = buildTemporalCreateU2Request(
      edited,
      createTemporalCreateU2AuthoringDraft(edited),
      'u2:multi-day',
    );
    expect(mapped.kind).toBe('event');
    expect(mapped.request.placement?.kind).toBe('date-span');
    if (mapped.request.placement?.kind !== 'date-span') {
      throw new Error('Expected a canonical date-span');
    }
    expect(mapped.request.placement.startDate.toString()).toBe('2026-10-15');
    expect(mapped.request.placement.endDateExclusive.toString()).toBe(
      '2026-10-18',
    );

    // Do not mask an actual, material Scheduling policy change.
    const editedMovement = createTemporalCreateFields({
      ...edited,
      scheduling: { ...edited.scheduling, movementPolicy: 'locked' },
    });
    expect(temporalCreateU2QuickIntentSupported(editedMovement)).toBe(false);
  });

  it('keeps not-yet-migrated advanced intent on the historical runtime path', () => {
    const baseline = createTemporalCreateFields({
      title: 'Focus',
      date: '2026-09-30',
    });
    const recurring = createTemporalCreateFields({
      ...baseline,
      eventRecurrence: {
        ...baseline.eventRecurrence,
        owner: 'routine',
        patternKind: 'calendar-wall-clock',
        calendarFrequency: 'weekly',
        calendarInterval: 1,
        weekdays: Object.freeze(['WE' as const]),
      },
    });

    expect(temporalCreateU2QuickIntentSupported(baseline)).toBe(true);
    expect(temporalCreateU2QuickIntentSupported(recurring)).toBe(false);
  });

  it('authors a Session minimum and internal decomposition in the same Activity command', () => {
    const baseline = createTemporalCreateFields({
      kind: 'activity',
      date: '2026-10-20',
      startTime: '09:00',
      durationMinutes: 240,
    });
    const fields = createTemporalCreateFields({
      ...baseline,
      execution: {
        ...baseline.execution,
        sessionMode: 'splittable',
        minSessionMinutes: 25,
      },
    });
    const initial = createTemporalCreateU2AuthoringDraft(fields);
    const draft = patchTemporalCreateU2AuthoringDraft(initial, {
      activityStructure: {
        ...initial.activityStructure,
        children: [
          {
            id: 'child',
            title: 'Prepare',
            requirementCode: 'required',
            captureMode: 'live',
            scheduleEnabled: true,
            startDate: '2026-10-20',
            startTime: '10:00',
            endDate: '2026-10-20',
            endTime: '11:30',
            plannedSlices: [],
          },
        ],
      },
    });
    expect(validateTemporalCreateU6Structure(fields, draft)).toBeNull();
    expect(temporalCreateU2QuickIntentSupported(fields)).toBe(true);
    const mapped = buildTemporalCreateU2Request(fields, draft, 'u6:minimum');
    if (mapped.kind !== 'activity')
      throw new Error('Expected Activity request.');
    expect(mapped.request.minimumSessionDurationMicroseconds).toBe(
      1_500_000_000,
    );
    expect(mapped.request.children?.[0]?.title).toBe('Prepare');
    expect(mapped.request.children?.[0]?.placement?.kind).toBe(
      'floating-local-interval',
    );
    const unsupported = createTemporalCreateFields({
      ...fields,
      execution: { ...fields.execution, maxSessions: 3 },
    });
    expect(temporalCreateU2QuickIntentSupported(unsupported)).toBe(false);
  });

  it('serializes shared Objective forms without collapsing measurements into Outcome', () => {
    const fields = createTemporalCreateFields({
      kind: 'activity',
      date: '2026-10-20',
    });
    const initial = createTemporalCreateU2AuthoringDraft(fields);
    const draft = patchTemporalCreateU2AuthoringDraft(initial, {
      realityMode: 'review_on_end',
      objectives: Object.freeze([
        Object.freeze({
          id: 'distance',
          label: 'Correre 10 km',
          resultKind: 'quantity' as const,
          comparatorCode: 'gte' as const,
          targetValue: '10',
          targetMin: '',
          targetMax: '',
          unitCode: 'km',
        }),
        Object.freeze({
          id: 'quality',
          label: 'Tecnica',
          resultKind: 'qualitative' as const,
          comparatorCode: null,
          targetValue: '',
          targetMin: '',
          targetMax: '',
          unitCode: '',
        }),
      ]),
    });

    expect(buildTemporalCreateObjectiveTemplates(draft)).toEqual([
      {
        label: 'Correre 10 km',
        result_kind: 'quantity',
        comparator_code: 'gte',
        target_value: 10,
        target_min: null,
        target_max: null,
        unit_code: 'km',
        presentation_order: 0,
      },
      {
        label: 'Tecnica',
        result_kind: 'qualitative',
        comparator_code: null,
        target_value: null,
        target_min: null,
        target_max: null,
        unit_code: null,
        presentation_order: 1,
      },
    ]);
  });

  it('rejects empty numeric Objective targets instead of treating them as zero', () => {
    const fields = createTemporalCreateFields({
      kind: 'event',
      date: '2026-10-20',
    });
    const initial = createTemporalCreateU2AuthoringDraft(fields);
    const draft = patchTemporalCreateU2AuthoringDraft(initial, {
      objectives: Object.freeze([
        Object.freeze({
          id: 'count',
          label: 'Raccogli mele',
          resultKind: 'quantity' as const,
          comparatorCode: 'gte' as const,
          targetValue: '',
          targetMin: '',
          targetMax: '',
          unitCode: 'mele',
        }),
      ]),
    });

    expect(() => buildTemporalCreateObjectiveTemplates(draft)).toThrow(
      'inserisci un target numerico valido',
    );
  });

  it('rejects child ranges and ignores obsolete named Session clock fields in saved drafts', () => {
    const fields = createTemporalCreateFields({
      kind: 'activity',
      date: '2026-10-20',
      startTime: '09:00',
      durationMinutes: 120,
    });
    const initial = createTemporalCreateU2AuthoringDraft(fields);
    const outsideChild = patchTemporalCreateU2AuthoringDraft(initial, {
      activityStructure: {
        ...initial.activityStructure,
        children: [
          {
            id: 'child',
            title: 'Late child',
            requirementCode: 'required',
            captureMode: 'disabled',
            scheduleEnabled: true,
            startDate: '2026-10-20',
            startTime: '10:30',
            endDate: '2026-10-20',
            endTime: '11:30',
            plannedSlices: [],
          },
        ],
      },
    });
    expect(validateTemporalCreateU6Structure(fields, outsideChild)).toBe(
      'Internal Activity decomposition must stay inside the Activity time range.',
    );

    const outsideSession = patchTemporalCreateU2AuthoringDraft(initial, {
      activityStructure: {
        ...initial.activityStructure,
        plannedSlices: [
          {
            id: 'session',
            title: 'Overflow',
            timeEnabled: true,
            date: '2026-10-20',
            startTime: '10:30',
            endTime: '11:30',
          },
        ],
      },
    });
    expect(
      validateTemporalCreateU6Structure(fields, outsideSession),
    ).toBeNull();
    const migrated = buildTemporalCreateU2Request(
      fields,
      outsideSession,
      'old-draft',
    );
    if (migrated.kind !== 'activity') throw new Error('Expected Activity');
    expect(migrated.request.plannedSlices).toEqual([null]);

    const reversedSession = patchTemporalCreateU2AuthoringDraft(initial, {
      activityStructure: {
        ...initial.activityStructure,
        plannedSlices: [
          {
            ...outsideSession.activityStructure.plannedSlices[0]!,
            startTime: '10:30',
            endTime: '10:00',
          },
        ],
      },
    });
    expect(
      validateTemporalCreateU6StructureIssue(fields, reversedSession),
    ).toBeNull();
    const reversed = buildTemporalCreateU2Request(
      fields,
      reversedSession,
      'old-draft-reversed',
    );
    if (reversed.kind !== 'activity') throw new Error('Expected Activity');
    expect(reversed.request.plannedSlices).toEqual([null]);
  });
});
