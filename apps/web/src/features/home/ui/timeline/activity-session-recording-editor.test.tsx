// @vitest-environment jsdom
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import {
  activityHasSessionRecordings,
  ActivitySessionRecordingEditor,
} from './activity-session-recording-editor';

const ACTIVITY = '019b0000-0000-7000-8000-000000000001';
const MAIN = '019b0000-0000-7000-8000-000000000002';

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe('Activity Session recording editor', () => {
  it('does not expose the action without a configured or historical Session', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async (input: RequestInfo | URL) =>
        Response.json(
          String(input).endsWith('/children')
            ? {
                parent_activity_ref: ACTIVITY,
                session_capture_mode: 'disabled',
                schedules: [],
              }
            : [],
        ),
      ),
    );
    expect(await activityHasSessionRecordings(ACTIVITY)).toBe(false);
  });

  it('records the main attempt once and then offers correction on the same factual identity', async () => {
    let recorded: unknown[] = [];
    const submitted: Record<string, unknown>[] = [];
    const fetcher = vi.fn(
      async (input: RequestInfo | URL, init?: RequestInit) => {
        const path = String(input);
        if (path.endsWith('/children')) {
          return Response.json({
            parent_activity_ref: ACTIVITY,
            session_capture_mode: 'record_and_live',
            schedules: [],
          });
        }
        if (path.endsWith('/sessions/editor') && init?.method === 'POST') {
          const body = JSON.parse(String(init.body)) as Record<string, unknown>;
          submitted.push(body);
          recorded = [
            {
              session_ref: MAIN,
              planned_schedule_ref: null,
              timing_material_state_ref: '019b0000-0000-7000-8000-000000000003',
              started_at: body.started_at,
              ended_at: body.ended_at,
              pause_ranges: body.pause_ranges,
            },
          ];
          return Response.json({});
        }
        if (path.endsWith('/sessions/editor')) return Response.json(recorded);
        if (path.endsWith('/auth/session'))
          return Response.json({ csrf_token: 'test' });
        throw new Error(`Unexpected request: ${path}`);
      },
    );
    vi.stubGlobal('fetch', fetcher);
    render(
      <ActivitySessionRecordingEditor
        activityRef={ACTIVITY}
        activityTitle="Scrivere"
        timeZone="Etc/UTC"
        onClose={vi.fn()}
      />,
    );
    const row = await screen.findByText('Sessione attività');
    const card = row.closest('article');
    expect(card).not.toBeNull();
    fireEvent.click(within(card!).getByRole('button', { name: 'Registra' }));
    fireEvent.change(
      within(card!).getByLabelText('Sessione attività · Inizio'),
      {
        target: { value: '2020-01-01T09:00:00' },
      },
    );
    fireEvent.change(within(card!).getByLabelText('Sessione attività · Fine'), {
      target: { value: '2020-01-01T10:00:00' },
    });
    fireEvent.click(
      within(card!).getByRole('button', { name: 'Salva registrazione' }),
    );
    const correct = await screen.findByRole('button', { name: 'Correggi' });
    const recordedCard = correct.closest('article');
    expect(recordedCard).not.toBeNull();
    expect(
      within(recordedCard!).queryByRole('button', { name: 'Registra' }),
    ).toBeNull();
    expect(submitted).toHaveLength(1);
    expect(submitted[0]?.session_ref).toBeNull();
    fireEvent.click(correct);
    fireEvent.click(
      within(recordedCard!).getByRole('button', { name: '+ Pausa' }),
    );
    const pauseStart = within(recordedCard!).getByLabelText('Pausa 1 · Da');
    const pauseEnd = within(recordedCard!).getByLabelText('Pausa 1 · A');
    expect(
      within(recordedCard!).getByLabelText('Sessione attività · Inizio'),
    ).toHaveProperty('value', '2020-01-01T09:00');
    fireEvent.change(pauseStart, { target: { value: '2020-01-01T09:20' } });
    fireEvent.change(pauseEnd, { target: { value: '2020-01-01T09:30' } });
    fireEvent.click(
      within(recordedCard!).getByRole('button', {
        name: 'Salva registrazione',
      }),
    );
    await waitFor(() => expect(submitted).toHaveLength(2));
    expect(submitted[1]?.session_ref).toBe(MAIN);
    expect(submitted[1]?.pause_ranges).toHaveLength(1);
  });

  it('preserves which repeated local hour was recorded during the autumn clock change', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async (input: RequestInfo | URL) =>
        Response.json(
          String(input).endsWith('/children')
            ? {
                parent_activity_ref: ACTIVITY,
                session_capture_mode: 'record_and_live',
                schedules: [],
              }
            : [
                {
                  session_ref: MAIN,
                  planned_schedule_ref: null,
                  timing_material_state_ref:
                    '019b0000-0000-7000-8000-000000000003',
                  started_at: '2020-10-25T00:30:00Z',
                  ended_at: '2020-10-25T02:30:00Z',
                  pause_ranges: [],
                },
              ],
        ),
      ),
    );
    render(
      <ActivitySessionRecordingEditor
        activityRef={ACTIVITY}
        activityTitle="Scrivere"
        timeZone="Europe/Rome"
        onClose={vi.fn()}
      />,
    );
    fireEvent.click(await screen.findByRole('button', { name: 'Correggi' }));
    expect(
      screen.getByLabelText('Sessione attività · Inizio · occorrenza dell’ora'),
    ).toHaveProperty('value', 'earlier');
  });
});
