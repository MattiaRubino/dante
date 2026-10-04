// @vitest-environment jsdom

import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { ActivityPlannedSessionsCardDetail } from './activity-planned-sessions-card-detail';

const ACTIVITY = '0199a8c0-6e72-7cd1-9be1-b3f51406728e';
const ENVELOPE = '0199a8c0-6e72-7cd1-9be1-b3f514067290';
const SESSION_A = '0199a8c0-6e72-7cd1-9be1-b3f514067291';
const SESSION_B = '0199a8c0-6e72-7cd1-9be1-b3f514067292';

describe('Activity planned Sessions card detail', () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it('renders only Activity-owned planned schedules as nested card detail', async () => {
    const fetchFn = vi.fn<typeof fetch>(async () =>
      Response.json({
        parent_activity_ref: ACTIVITY,
        session_capture_mode: 'live',
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
      }),
    );
    vi.stubGlobal('fetch', fetchFn);

    const { container } = render(
      <ActivityPlannedSessionsCardDetail activityRef={ACTIVITY} visible />,
    );

    expect(await screen.findByText('Teoria')).toBeTruthy();
    expect(screen.getByText('Esercizi')).toBeTruthy();
    expect(screen.getByText('18:00–19:00')).toBeTruthy();
    expect(screen.getByText('20:00–21:00')).toBeTruthy();
    expect(container.querySelectorAll('[data-activity-planned-sessions]')).toHaveLength(1);
    expect(String(fetchFn.mock.calls[0]?.[0])).toContain(
      `/activities/${ACTIVITY}/children`,
    );
  });

  it('does not fetch or render nested detail while the Activity card is closed', () => {
    const fetchFn = vi.fn<typeof fetch>();
    vi.stubGlobal('fetch', fetchFn);

    const { container } = render(
      <ActivityPlannedSessionsCardDetail activityRef={ACTIVITY} visible={false} />,
    );

    expect(fetchFn).not.toHaveBeenCalled();
    expect(container.querySelector('[data-activity-planned-sessions]')).toBeNull();
  });
});
