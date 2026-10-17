import { fetchRequestUrl } from '../../test-support/fetch-request';
// @vitest-environment jsdom

import { act, cleanup, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { ActivityPlannedSessionsCardDetail } from './activity-planned-sessions-card-detail';
import { invalidateTemporalPlanningRead } from './timeline-invalidation';

const ACTIVITY = '0199a8c0-6e72-7cd1-9be1-b3f51406728e';
const ENVELOPE = '0199a8c0-6e72-7cd1-9be1-b3f514067290';
const SESSION_A = '0199a8c0-6e72-7cd1-9be1-b3f514067291';
const SESSION_B = '0199a8c0-6e72-7cd1-9be1-b3f514067292';

describe('Activity planned Sessions card detail', () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it('renders only Activity-owned named Sessions without calendar times', async () => {
    const fetchFn = vi.fn<typeof fetch>((input) =>
      Promise.resolve(
        Response.json(
          fetchRequestUrl(input).endsWith('/sessions')
            ? []
            : {
          parent_activity_ref: ACTIVITY,
          session_capture_mode: 'disabled',
          child_guard_mode: 'none',
          schedules: [
            {
              schedule_ref: ENVELOPE,
              role_code: 'envelope',
              presentation_order: 0,
              display_name: null,
              temporal_form: 'named_zone_local',
              starts_local_at: '2026-10-04T18:00:00',
              ends_local_at: '2026-10-04T21:00:00',
            },
            {
              schedule_ref: SESSION_A,
              role_code: 'planned',
              presentation_order: 1,
              display_name: 'Teoria',
              temporal_form: 'named_zone_local',
              starts_local_at: '2026-10-04T18:00:00',
              ends_local_at: '2026-10-04T19:00:00',
            },
            {
              schedule_ref: SESSION_B,
              role_code: 'planned',
              presentation_order: 2,
              display_name: 'Esercizi',
              temporal_form: 'named_zone_local',
              starts_local_at: '2026-10-04T20:00:00',
              ends_local_at: '2026-10-04T21:00:00',
            },
          ],
          children: [],
        },
        ),
      ),
    );
    vi.stubGlobal('fetch', fetchFn);

    const { container } = render(
      <ActivityPlannedSessionsCardDetail activityRef={ACTIVITY} visible />,
    );

    expect(await screen.findByText('Teoria')).toBeTruthy();
    expect(screen.getByText('Esercizi')).toBeTruthy();
    expect(screen.queryByText('18:00–19:00')).toBeNull();
    expect(screen.queryByText('20:00–21:00')).toBeNull();
    const rows = container.querySelectorAll(
      '.timeline-activity-planned-sessions__row',
    );
    expect(rows).toHaveLength(2);
    for (const row of rows) {
      expect(row.querySelector('[aria-label="Avvia"]')).toBeNull();
      expect(row.querySelector('[aria-label="Termina"]')).toBeNull();
    }
    expect(screen.getAllByText('Avvia prima la principale')).toHaveLength(2);
    expect(
      container.querySelectorAll('[data-activity-planned-sessions]'),
    ).toHaveLength(1);
    expect(fetchRequestUrl(fetchFn.mock.calls[0]?.[0])).toContain(
      `/activities/${ACTIVITY}/children`,
    );
  });

  it('shows Play only while main is active and replaces it with review on Stop', async () => {
    let mainStopped = false;
    const children = {
      parent_activity_ref: ACTIVITY,
      schedules: [
        { schedule_ref: SESSION_A, role_code: 'planned', presentation_order: 1, display_name: 'Teoria' },
        { schedule_ref: SESSION_B, role_code: 'planned', presentation_order: 2, display_name: 'Esercizi' },
      ],
    };
    const main = () => ({
      session_ref: '0199a8c0-6e72-7cd1-9be1-b3f514067293',
      planned_schedule_ref: null,
      subject_native_ref: ACTIVITY,
      timing_material_state_ref: '0199a8c0-6e72-7cd1-9be1-b3f514067294',
      started_at: '2026-10-17T19:00:00Z',
      ended_at: mainStopped ? '2026-10-17T19:05:00Z' : null,
      evaluated_at: '2026-10-17T19:05:00Z',
      open: !mainStopped,
      replayed: false,
      paused: false,
      elapsed_seconds: 300,
      active_seconds: 300,
      paused_seconds: 0,
      duration_evaluations: [],
    });
    const fetchFn = vi.fn<typeof fetch>((input) =>
      Promise.resolve(
        Response.json(fetchRequestUrl(input).endsWith('/sessions') ? [main()] : children),
      ),
    );
    vi.stubGlobal('fetch', fetchFn);
    const { container } = render(
      <ActivityPlannedSessionsCardDetail activityRef={ACTIVITY} visible />,
    );
    await screen.findByText('Teoria');
    await act(async () => {
      await Promise.resolve();
      await Promise.resolve();
    });
    expect(
      container.querySelectorAll('[aria-label="Avvia"]'),
    ).toHaveLength(2);

    mainStopped = true;
    act(() =>
      window.dispatchEvent(
        new CustomEvent('dante:session-changed', { detail: ACTIVITY }),
      ),
    );
    expect(await screen.findAllByText('Da verificare')).toHaveLength(2);
    expect(container.querySelectorAll('[aria-label="Avvia"]')).toHaveLength(0);
  });

  it('does not fetch or render nested detail while the Activity card is closed', () => {
    const fetchFn = vi.fn<typeof fetch>();
    vi.stubGlobal('fetch', fetchFn);

    const { container } = render(
      <ActivityPlannedSessionsCardDetail
        activityRef={ACTIVITY}
        visible={false}
      />,
    );

    expect(fetchFn).not.toHaveBeenCalled();
    expect(
      container.querySelector('[data-activity-planned-sessions]'),
    ).toBeNull();
  });

  it('updates the card indicator after Modifica adds an internal Session', async () => {
    let planned = false;
    const fetchFn = vi.fn<typeof fetch>(() =>
      Promise.resolve(
        Response.json({
          parent_activity_ref: ACTIVITY,
          schedules: planned
            ? [
                {
                  schedule_ref: SESSION_A,
                  role_code: 'planned',
                  presentation_order: 1,
                  display_name: 'Nuova',
                },
              ]
            : [],
        }),
      ),
    );
    vi.stubGlobal('fetch', fetchFn);
    const { container } = render(
      <ActivityPlannedSessionsCardDetail
        activityRef={ACTIVITY}
        visible
        variant="indicator"
      />,
    );
    await act(async () => {
      await Promise.resolve();
    });
    expect(
      container.querySelector('[data-activity-planned-sessions]'),
    ).toBeNull();
    planned = true;
    act(() => invalidateTemporalPlanningRead());
    expect(await screen.findByLabelText('1 sessioni pianificate')).toBeTruthy();
    expect(fetchFn).toHaveBeenCalledTimes(2);
  });
});
