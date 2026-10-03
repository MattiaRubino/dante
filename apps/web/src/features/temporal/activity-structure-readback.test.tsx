// @vitest-environment jsdom

import { cleanup, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { ActivityStructureReadback } from './activity-structure-readback';

vi.mock('./session-subject-controls', () => ({
  SessionSubjectControls: (props: Record<string, unknown>) => (
    <div
      data-testid="session-capture"
      data-subject={String(props.subjectRef)}
      data-live={String(props.allowLive)}
      data-manual={String(props.allowManual)}
    />
  ),
}));

const PARENT = '0199a8c0-6e72-7cd1-9be1-b3f51406728e';
const CHILD = '0199a8c0-6e72-7cd1-9be1-b3f51406728f';

describe('Activity structure after reload', () => {
  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it('reads current children, modes and Schedules without creating future Sessions', async () => {
    const fetchFn = vi.fn<typeof fetch>(async () =>
      Response.json({
        parent_activity_ref: PARENT,
        session_capture_mode: 'live',
        child_guard_mode: 'confirm',
        schedules: [
          {
            schedule_ref: PARENT,
            temporal_form: 'absolute',
            starts_at: '2026-10-02T08:00:00Z',
            ends_at: '2026-10-02T11:00:00Z',
          },
        ],
        children: [
          {
            child_activity_ref: CHILD,
            child_title: 'Fase uno',
            requirement_code: 'required',
            presentation_order: 1,
            session_capture_mode: 'record',
            schedules: [
              {
                schedule_ref: CHILD,
                temporal_form: 'absolute',
                starts_at: '2026-10-02T09:00:00Z',
                ends_at: '2026-10-02T09:30:00Z',
              },
            ],
          },
        ],
      }),
    );
    vi.stubGlobal('fetch', fetchFn);
    render(<ActivityStructureReadback activityRef={PARENT} />);

    await screen.findByText(/Fase uno · required/);
    expect(
      screen.getByText(/Sessioni: live · Figli richiesti: confirm/),
    ).toBeTruthy();
    expect(screen.getByText(/2026-10-02T08:00:00Z/)).toBeTruthy();
    expect(screen.getByTestId('session-capture').dataset.live).toBe('true');
    const child = screen.getByText(/Fase uno · required/);
    child.click();
    await waitFor(() =>
      expect(screen.getAllByTestId('session-capture')).toHaveLength(2),
    );
    const manual = screen.getAllByTestId('session-capture')[1];
    expect(manual?.dataset.subject).toBe(CHILD);
    expect(manual?.dataset.live).toBe('false');
    expect(manual?.dataset.manual).toBe('true');
    expect(String(fetchFn.mock.calls[0]?.[0])).toContain(
      `/activities/${PARENT}/children`,
    );
  });
});
