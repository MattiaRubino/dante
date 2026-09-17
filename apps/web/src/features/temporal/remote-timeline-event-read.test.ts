import { describe, expect, it, vi } from 'vitest';

import {
  TemporalTimelineRemoteError,
  createRemoteTemporalTimelineDataSource,
} from './remote-timeline-read';

function jsonResponse(body: unknown): Response {
  return new Response(JSON.stringify(body), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
}

const REQUEST = Object.freeze({
  startDate: '2026-09-17',
  endDateExclusive: '2026-09-22',
});

const EVENT = Object.freeze({
  kind: 'scheduled_event',
  event_ref: '0199a8c0-6e71-7bc0-8ad0-a2f403f5617d',
  schedule_ref: '0199a8c0-6e72-7bc0-8ad0-a2f403f5617d',
  placement_material_state_ref: '0199a8c0-6e73-7bc0-8ad0-a2f403f5617d',
  title: 'Conferenza',
});

function windowWith(item: unknown) {
  return {
    kind: 'window',
    start_date: REQUEST.startDate,
    end_date_exclusive: REQUEST.endDateExclusive,
    effective_zone_id: 'Europe/Rome',
    items: [item],
  };
}

describe('remote Event Timeline protocol', () => {
  it('parses scheduled_event while preserving Event identity distinctly from Activity', async () => {
    const source = createRemoteTemporalTimelineDataSource(
      vi.fn<typeof globalThis.fetch>(() =>
        Promise.resolve(
          jsonResponse(
            windowWith({
              ...EVENT,
              temporal_form: 'date_span',
              start_date: '2026-09-19',
              end_date_exclusive: '2026-09-22',
            }),
          ),
        ),
      ),
      () => 'Europe/Rome',
    );

    const result = await source.loadWindow(REQUEST);
    expect(result.kind).toBe('window');
    if (result.kind !== 'window') {
      throw new Error('Expected populated Timeline window.');
    }
    const [item] = result.items;
    expect(item).toMatchObject({
      kind: 'scheduled_event',
      eventRef: EVENT.event_ref,
      scheduleRef: EVENT.schedule_ref,
      placementMaterialStateRef: EVENT.placement_material_state_ref,
      temporalForm: 'date-span',
    });
    expect('activityRef' in (item ?? {})).toBe(false);
  });

  it('rejects Event payload carrying an Activity identity', async () => {
    const source = createRemoteTemporalTimelineDataSource(
      vi.fn<typeof globalThis.fetch>(() =>
        Promise.resolve(
          jsonResponse(
            windowWith({
              ...EVENT,
              activity_ref: '0199a8c0-7e74-7bc0-8ad0-a2f403f5617d',
              temporal_form: 'floating_local',
              starts_local_at: '2026-09-17T18:30:00',
              ends_local_at: '2026-09-17T20:00:00',
            }),
          ),
        ),
      ),
      () => 'Europe/Rome',
    );

    await expect(source.loadWindow(REQUEST)).rejects.toBeInstanceOf(
      TemporalTimelineRemoteError,
    );
  });

  it('rejects scheduled_event without its Event reference', async () => {
    const { event_ref: _eventRef, ...withoutEventRef } = EVENT;
    const source = createRemoteTemporalTimelineDataSource(
      vi.fn<typeof globalThis.fetch>(() =>
        Promise.resolve(
          jsonResponse(
            windowWith({
              ...withoutEventRef,
              temporal_form: 'floating_local',
              starts_local_at: '2026-09-17T18:30:00',
              ends_local_at: '2026-09-17T20:00:00',
            }),
          ),
        ),
      ),
      () => 'Europe/Rome',
    );

    await expect(source.loadWindow(REQUEST)).rejects.toBeInstanceOf(
      TemporalTimelineRemoteError,
    );
  });
});
