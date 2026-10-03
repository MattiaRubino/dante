import { describe, expect, it } from 'vitest';

import { createTemporalCreateFields } from '../model/temporal-create-session';
import {
  createTemporalCreateU2AuthoringDraft,
  patchTemporalCreateU2AuthoringDraft,
} from '../model/temporal-create-u2-authoring';
import {
  buildTemporalCreateU2Request,
  temporalCreateU2QuickIntentSupported,
  validateTemporalCreateU2QuickFields,
} from './temporal-create-u2-submit';

describe('U2 Quick Create submit mapping', () => {
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
        agendaParts: Object.freeze(['Revisione', 'Decisioni']),
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

  it('authors a Session minimum with children in the same Activity command', () => {
    const baseline = createTemporalCreateFields({
      kind: 'activity',
      date: '2026-10-20',
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
            plannedSlices: [],
          },
        ],
      },
    });
    expect(temporalCreateU2QuickIntentSupported(fields)).toBe(true);
    const mapped = buildTemporalCreateU2Request(fields, draft, 'u6:minimum');
    if (mapped.kind !== 'activity')
      throw new Error('Expected Activity request.');
    expect(mapped.request.minimumSessionDurationMicroseconds).toBe(
      1_500_000_000,
    );
    expect(mapped.request.children?.[0]?.title).toBe('Prepare');
    const unsupported = createTemporalCreateFields({
      ...fields,
      execution: { ...fields.execution, maxSessions: 3 },
    });
    expect(temporalCreateU2QuickIntentSupported(unsupported)).toBe(false);
  });
});
