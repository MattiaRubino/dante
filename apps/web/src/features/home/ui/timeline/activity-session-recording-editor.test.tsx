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

function setClock(
  card: HTMLElement,
  interval: number,
  edge: 'Inizio' | 'Fine',
  date: string,
  time: string,
) {
  const label = `Intervallo ${interval}`;
  const dateLabel = `${label} · Data ${edge === 'Inizio' ? 'inizio' : 'fine'}`;
  const dateTrigger = within(card).getByRole('button', {
    name: new RegExp(`^${dateLabel}:`),
  });
  if (dateTrigger.getAttribute('data-temporal-date') !== date) {
    fireEvent.click(dateTrigger);
    const picker = screen.getByRole('dialog', { name: dateLabel });
    const day = picker.querySelector<HTMLButtonElement>(
      `button[data-temporal-date="${date}"]`,
    );
    expect(day).not.toBeNull();
    fireEvent.click(day!);
  }
  fireEvent.change(
    within(card).getByRole('textbox', { name: `${label} · ${edge}: ore` }),
    {
      target: { value: time.slice(0, 2) },
    },
  );
  fireEvent.change(
    within(card).getByRole('textbox', { name: `${label} · ${edge}: minuti` }),
    { target: { value: time.slice(3) } },
  );
}

const fetchPath = (input: RequestInfo | URL): string =>
  typeof input === 'string'
    ? input
    : input instanceof URL
      ? input.href
      : input.url;
const mockResponse = (body: unknown, init?: ResponseInit): Promise<Response> =>
  Promise.resolve(Response.json(body, init));

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe('Activity Session recording editor', () => {
  it('does not expose the action without a configured or historical Session', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn((input: RequestInfo | URL) =>
        mockResponse(
          fetchPath(input).endsWith('/children')
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

  it('exposes a configured main Session even if the recordings endpoint is unavailable', async () => {
    const fetcher = vi.fn((input: RequestInfo | URL) => {
      const path = fetchPath(input);
      if (path.endsWith('/children'))
        return mockResponse({
          parent_activity_ref: ACTIVITY,
          session_capture_mode: 'live',
          schedules: [],
        });
      if (path.endsWith('/sessions'))
        return mockResponse({ detail: 'Unavailable' }, { status: 503 });
      throw new Error(`Unexpected request: ${path}`);
    });
    vi.stubGlobal('fetch', fetcher);
    expect(await activityHasSessionRecordings(ACTIVITY)).toBe(true);
    expect(
      fetcher.mock.calls.some(([path]) =>
        fetchPath(path).endsWith('/sessions/editor'),
      ),
    ).toBe(false);
  });

  it('exposes planned Sessions without depending on the editor endpoint', async () => {
    const fetcher = vi.fn((input: RequestInfo | URL) => {
      const path = fetchPath(input);
      if (path.endsWith('/children'))
        return mockResponse({
          parent_activity_ref: ACTIVITY,
          session_capture_mode: 'disabled',
          schedules: [
            {
              schedule_ref: MAIN,
              role_code: 'planned',
              presentation_order: 1,
              display_name: 'Sessione 1',
            },
          ],
        });
      if (path.endsWith('/sessions')) return mockResponse([]);
      throw new Error(`Unexpected request: ${path}`);
    });
    vi.stubGlobal('fetch', fetcher);
    expect(await activityHasSessionRecordings(ACTIVITY)).toBe(true);
    expect(fetcher).toHaveBeenCalledTimes(2);
  });

  it('exposes historical attempts even when capture is disabled now', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn((input: RequestInfo | URL) =>
        mockResponse(
          fetchPath(input).endsWith('/children')
            ? {
                parent_activity_ref: ACTIVITY,
                session_capture_mode: 'disabled',
                schedules: [],
              }
            : [{ session_ref: MAIN }],
        ),
      ),
    );
    expect(await activityHasSessionRecordings(ACTIVITY)).toBe(true);
  });

  it('records the main attempt once and then offers correction on the same factual identity', async () => {
    let recorded: unknown[] = [];
    const submitted: Record<string, unknown>[] = [];
    const fetcher = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const path = fetchPath(input);
      if (path.endsWith('/children')) {
        return mockResponse({
          parent_activity_ref: ACTIVITY,
          session_capture_mode: 'record_and_live',
          schedules: [],
        });
      }
      if (path.endsWith('/sessions/editor') && init?.method === 'POST') {
        const body = JSON.parse(
          typeof init.body === 'string' ? init.body : '',
        ) as Record<string, unknown>;
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
        return mockResponse({});
      }
      if (path.endsWith('/sessions/editor')) return mockResponse(recorded);
      if (path.endsWith('/auth/session'))
        return mockResponse({ csrf_token: 'test' });
      throw new Error(`Unexpected request: ${path}`);
    });
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
    const yesterday = new Date(Date.now() - 86_400_000)
      .toISOString()
      .slice(0, 10);
    setClock(card!, 1, 'Inizio', yesterday, '09:00');
    setClock(card!, 1, 'Fine', yesterday, '10:00');
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
      within(recordedCard!).getByRole('button', {
        name: /Aggiungi intervallo/,
      }),
    );
    expect(
      within(recordedCard!)
        .getByRole('button', { name: /^Intervallo 1 · Data inizio:/ })
        .getAttribute('data-temporal-date'),
    ).toBe(yesterday);
    setClock(recordedCard!, 1, 'Fine', yesterday, '09:20');
    setClock(recordedCard!, 2, 'Inizio', yesterday, '09:30');
    setClock(recordedCard!, 2, 'Fine', yesterday, '09:40');
    fireEvent.click(
      within(recordedCard!).getByRole('button', {
        name: /Aggiungi intervallo/,
      }),
    );
    setClock(recordedCard!, 3, 'Inizio', yesterday, '09:50');
    setClock(recordedCard!, 3, 'Fine', yesterday, '10:00');
    fireEvent.click(
      within(recordedCard!).getByRole('button', {
        name: 'Salva registrazione',
      }),
    );
    await waitFor(() => expect(submitted).toHaveLength(2));
    expect(submitted[1]?.session_ref).toBe(MAIN);
    expect(submitted[1]?.pause_ranges).toHaveLength(2);
    expect(submitted[1]?.pause_ranges).toEqual([
      {
        started_at: `${yesterday}T09:20:00.000Z`,
        ended_at: `${yesterday}T09:30:00.000Z`,
      },
      {
        started_at: `${yesterday}T09:40:00.000Z`,
        ended_at: `${yesterday}T09:50:00.000Z`,
      },
    ]);
  });

  it('preserves which repeated local hour was recorded during the autumn clock change', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn((input: RequestInfo | URL) =>
        mockResponse(
          fetchPath(input).endsWith('/children')
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
      screen.getByLabelText('Intervallo 1 · Inizio · occorrenza dell’ora'),
    ).toHaveProperty('value', 'earlier');
  });

  it('shows the main and child recordings on one time axis and rejects a child outside the active parent', async () => {
    const yesterday = new Date(Date.now() - 86_400_000)
      .toISOString()
      .slice(0, 10);
    const fetcher = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const path = fetchPath(input);
      if (path.endsWith('/children'))
        return mockResponse({
          parent_activity_ref: ACTIVITY,
          session_capture_mode: 'record_and_live',
          schedules: [
            {
              schedule_ref: MAIN,
              role_code: 'planned',
              presentation_order: 1,
              display_name: 'Lettura',
            },
          ],
        });
      if (path.endsWith('/sessions/editor') && !init?.method)
        return mockResponse([
          {
            session_ref: 'parent',
            planned_schedule_ref: null,
            timing_material_state_ref: 'parent-state',
            started_at: `${yesterday}T09:00:00Z`,
            ended_at: `${yesterday}T10:00:00Z`,
            pause_ranges: [
              {
                started_at: `${yesterday}T09:20:00Z`,
                ended_at: `${yesterday}T09:30:00Z`,
              },
              {
                started_at: `${yesterday}T09:40:00Z`,
                ended_at: `${yesterday}T09:45:00Z`,
              },
            ],
          },
        ]);
      throw new Error(`Unexpected request: ${path}`);
    });
    vi.stubGlobal('fetch', fetcher);
    render(
      <ActivitySessionRecordingEditor
        activityRef={ACTIVITY}
        activityTitle="Scrivere"
        timeZone="Etc/UTC"
        onClose={vi.fn()}
      />,
    );
    expect(
      await screen.findByLabelText(
        'Intervalli delle Sessioni sulla stessa scala oraria',
      ),
    ).toBeTruthy();
    expect(screen.getAllByRole('button', { name: '+ Sessione' })).toHaveLength(
      3,
    );
    fireEvent.click(screen.getAllByRole('button', { name: '+ Sessione' })[0]!);
    fireEvent.click(screen.getByRole('button', { name: 'Lettura' }));
    const child = screen
      .getByText('Lettura', { selector: 'h3' })
      .closest('article')!;
    setClock(child, 1, 'Inizio', yesterday, '09:15');
    setClock(child, 1, 'Fine', yesterday, '09:35');
    fireEvent.click(
      within(child).getByRole('button', { name: 'Salva registrazione' }),
    );
    expect(within(child).getByRole('alert').textContent).toContain(
      'tratti attivi',
    );
    expect(
      within(child)
        .getByRole('button', { name: /^Intervallo 1 · Data fine:/ })
        .getAttribute('aria-invalid'),
    ).toBe('true');
    expect(fetcher.mock.calls.some(([, init]) => init?.method === 'POST')).toBe(
      false,
    );
  });
});
