import { Temporal } from '@dante/time';
import { describe, expect, it, vi } from 'vitest';

import { createRemoteTemporalAuthoringDataSource } from './remote-authoring-data-source';

const ACTIVITY_REF = '0199a8c0-6e72-7cd1-9be1-b3f51406728e';
const SCHEDULE_REF = '0199a8c0-6e72-7cd1-9be1-b3f51406728f';
const MATERIAL_REF = '0199a8c0-7e73-7de2-8cf2-c4062517839f';

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function authenticatedSession() {
  return jsonResponse({ authenticated: true, csrf_token: 'csrf-u2' });
}

describe('remote U2 authoring data source', () => {
  it('authors an unassigned Activity with metadata and an explicit multi-day placement', async () => {
    const fetchFn = vi
      .fn<typeof fetch>()
      .mockResolvedValueOnce(authenticatedSession())
      .mockResolvedValueOnce(
        jsonResponse(
          {
            activity_ref: ACTIVITY_REF,
            title: 'Viaggio',
            created_at: '2026-09-30T18:00:00Z',
            description: 'Tratta notturna',
            location: 'Roma',
            color_code: '#FF7A00',
            life_area_ref: null,
            life_area_assignment_revision: null,
            life_area_color_code: null,
            life_area_revision: null,
            schedule: {
              schedule_ref: SCHEDULE_REF,
              placement_material_state_ref: MATERIAL_REF,
              placement: {
                kind: 'floating_local_interval',
                starts_local_at: '2026-09-30T23:30:00',
                ends_local_at: '2026-10-02T01:00:00',
              },
            },
            replayed: false,
          },
          201,
        ),
      );
    const source = createRemoteTemporalAuthoringDataSource(fetchFn);

    const result = await source.authorActivity({
      operationId: 'u2-activity-1',
      title: 'Viaggio',
      description: 'Tratta notturna',
      location: 'Roma',
      itemColorCode: '#FF7A00',
      placement: {
        kind: 'floating-local-interval',
        startsLocalAt: Temporal.PlainDateTime.from('2026-09-30T23:30'),
        endsLocalAt: Temporal.PlainDateTime.from('2026-10-02T01:00'),
      },
    });

    expect(result.item.lifeAreaRef).toBeNull();
    expect(result.item.description).toBe('Tratta notturna');
    expect(result.item.location).toBe('Roma');
    expect(result.item.colorCode).toBe('#FF7A00');
    expect(result.schedule?.placement.kind).toBe('floating-local-interval');

    const [, request] = fetchFn.mock.calls[1] ?? [];
    expect(request?.method).toBe('POST');
    expect((request?.headers as Headers).get('X-Dante-CSRF')).toBe('csrf-u2');
    expect(JSON.parse(String(request?.body))).toEqual({
      operation_id: 'u2-activity-1',
      title: 'Viaggio',
      description: 'Tratta notturna',
      location: 'Roma',
      item_color_code: '#FF7A00',
      life_area: null,
      placement: {
        kind: 'floating_local_interval',
        starts_local_at: '2026-09-30T23:30:00',
        ends_local_at: '2026-10-02T01:00:00',
      },
    });
  });

  it('authors an Event with a staged new Life Area only in the accepted command', async () => {
    const fetchFn = vi
      .fn<typeof fetch>()
      .mockResolvedValueOnce(authenticatedSession())
      .mockResolvedValueOnce(
        jsonResponse(
          {
            event_ref: ACTIVITY_REF,
            title: 'Workshop',
            created_at: '2026-09-30T18:00:00Z',
            description: null,
            location: 'Studio',
            color_code: null,
            life_area_ref: SCHEDULE_REF,
            life_area_assignment_revision: 1,
            life_area_color_code: '#8A4FFF',
            life_area_revision: 2,
            agenda_revision: 1,
            agenda_parts: ['Decisioni'],
            schedule: null,
            replayed: false,
          },
          201,
        ),
      );
    const source = createRemoteTemporalAuthoringDataSource(fetchFn);

    const result = await source.authorEvent({
      operationId: 'u2-event-1',
      title: 'Workshop',
      location: 'Studio',
      lifeArea: { newName: 'Lavoro', colorCode: '#8A4FFF' },
      agendaParts: ['Decisioni'],
    });

    expect(result.item.lifeAreaRef).toBe(SCHEDULE_REF);
    expect(result.item.lifeAreaColorCode).toBe('#8A4FFF');
    expect(result.agendaParts).toEqual(['Decisioni']);
    expect(JSON.parse(String(fetchFn.mock.calls[1]?.[1]?.body)).life_area).toEqual({
      new_name: 'Lavoro',
      color_code: '#8A4FFF',
    });
  });
});
