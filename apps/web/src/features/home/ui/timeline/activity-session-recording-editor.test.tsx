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

  it('records the main once and corrects its intervals with the same Session identity', async () => {
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
      if (path.endsWith('/sessions/editor/batch') && init?.method === 'POST') {
        const body = JSON.parse(
          typeof init.body === 'string' ? init.body : '',
        ) as { commands: Record<string, unknown>[] };
        expect(body.commands).toHaveLength(1);
        const command = body.commands[0]!;
        submitted.push(command);
        recorded = [
          {
            session_ref: MAIN,
            planned_schedule_ref: null,
            timing_material_state_ref: '019b0000-0000-7000-8000-000000000003',
            started_at: command.started_at,
            ended_at: command.ended_at,
            pause_ranges: command.pause_ranges,
          },
        ];
        return mockResponse(recorded);
      }
      if (path.endsWith('/sessions/editor')) return mockResponse(recorded);
      if (path.endsWith('/auth/session'))
        return mockResponse({ csrf_token: 'test' });
      throw new Error('Unexpected request: ' + path);
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
    const main = await screen.findByText('Sessione attività');
    const group = main.closest<HTMLElement>(
      'section.timeline-session-editor__group',
    );
    expect(group).not.toBeNull();
    const yesterday = new Date(Date.now() - 86_400_000)
      .toISOString()
      .slice(0, 10);
    setClock(group!, 1, 'Inizio', yesterday, '09:00');
    setClock(group!, 1, 'Fine', yesterday, '10:00');
    fireEvent.click(
      screen.getByRole('button', { name: 'Salva registrazioni' }),
    );
    const correct = await screen.findByRole('button', { name: 'Correggi' });
    expect(submitted).toHaveLength(1);
    expect(submitted[0]?.session_ref).toBeNull();
    fireEvent.click(correct);
    fireEvent.click(
      within(group!).getByRole('button', { name: /Aggiungi intervallo/ }),
    );
    expect(
      within(group!)
        .getByRole('button', { name: /^Intervallo 1 · Data inizio:/ })
        .getAttribute('data-temporal-date'),
    ).toBe(yesterday);
    setClock(group!, 1, 'Fine', yesterday, '09:20');
    setClock(group!, 2, 'Inizio', yesterday, '09:30');
    setClock(group!, 2, 'Fine', yesterday, '09:40');
    fireEvent.click(
      within(group!).getByRole('button', { name: /Aggiungi intervallo/ }),
    );
    setClock(group!, 3, 'Inizio', yesterday, '09:50');
    setClock(group!, 3, 'Fine', yesterday, '10:00');
    fireEvent.click(
      screen.getByRole('button', { name: 'Salva registrazioni' }),
    );
    await waitFor(() => expect(submitted).toHaveLength(2));
    expect(submitted[1]?.session_ref).toBe(MAIN);
    expect(submitted[1]?.pause_ranges).toEqual([
      {
        started_at: yesterday + 'T09:20:00.000Z',
        ended_at: yesterday + 'T09:30:00.000Z',
      },
      {
        started_at: yesterday + 'T09:40:00.000Z',
        ended_at: yesterday + 'T09:50:00.000Z',
      },
    ]);
  });

  it('keeps Add available when the last interval ends now and refuses overlap only on Save', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn((input: RequestInfo | URL) => {
        const path = fetchPath(input);
        if (path.endsWith('/children'))
          return mockResponse({
            parent_activity_ref: ACTIVITY,
            session_capture_mode: 'record_and_live',
            schedules: [],
          });
        if (path.endsWith('/sessions/editor')) return mockResponse([]);
        throw new Error('Unexpected request: ' + path);
      }),
    );
    render(
      <ActivitySessionRecordingEditor
        activityRef={ACTIVITY}
        activityTitle="Scrivere"
        timeZone="Etc/UTC"
        onClose={vi.fn()}
      />,
    );
    const group = (
      await screen.findByText('Sessione attività')
    ).closest<HTMLElement>('section.timeline-session-editor__group')!;
    fireEvent.click(
      within(group).getByRole('button', { name: /Aggiungi intervallo/ }),
    );
    expect(
      group.querySelectorAll('.timeline-session-editor__parent-interval'),
    ).toHaveLength(2);
    expect(screen.queryByRole('alert')).toBeNull();
    fireEvent.click(
      screen.getByRole('button', { name: 'Salva registrazioni' }),
    );
    expect(within(group).getByText(/ordinati e separati/)).toBeTruthy();
    expect(
      group.querySelectorAll(
        '.timeline-session-editor__interval[data-invalid]',
      ),
    ).toHaveLength(1);

    const yesterday = new Date(Date.now() - 86_400_000)
      .toISOString()
      .slice(0, 10);
    setClock(group, 1, 'Inizio', yesterday, '09:00');
    setClock(group, 1, 'Fine', yesterday, '09:15');
    setClock(group, 2, 'Inizio', yesterday, '09:20');
    setClock(group, 2, 'Fine', yesterday, '09:30');
    expect(
      group.querySelectorAll('.timeline-session-editor__parent-interval'),
    ).toHaveLength(2);
    expect(screen.queryByRole('alert')).toBeNull();
  });

  it('adds a second editable child row even when the first fills its main interval', async () => {
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
      if (path.endsWith('/sessions/editor')) return mockResponse([]);
      if (init?.method === 'POST')
        throw new Error('Invalid child must not be submitted');
      throw new Error('Unexpected request: ' + path);
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
    const group = (
      await screen.findByText('Sessione attività')
    ).closest<HTMLElement>('section.timeline-session-editor__group')!;
    setClock(group, 1, 'Inizio', yesterday, '09:00');
    setClock(group, 1, 'Fine', yesterday, '09:30');
    fireEvent.click(
      within(group).getByRole('button', { name: /Registra sessione/ }),
    );
    fireEvent.click(within(group).getByRole('button', { name: 'Lettura' }));
    const child = within(group)
      .getByText('Lettura', { selector: 'h3' })
      .closest('article')!;
    fireEvent.click(
      within(child).getByRole('button', { name: /Aggiungi intervallo/ }),
    );
    expect(within(child).getByText('Intervallo 2')).toBeTruthy();
    expect(screen.queryByRole('alert')).toBeNull();
    fireEvent.click(
      screen.getByRole('button', { name: 'Salva registrazioni' }),
    );
    expect(within(child).getByText(/ordinati e separati/)).toBeTruthy();
    expect(fetcher.mock.calls.some(([, init]) => init?.method === 'POST')).toBe(
      false,
    );
    setClock(child, 1, 'Fine', yesterday, '09:10');
    setClock(child, 2, 'Inizio', yesterday, '09:15');
    setClock(child, 2, 'Fine', yesterday, '09:25');
    expect(screen.queryByRole('alert')).toBeNull();
  });

  it('keeps the same draft and operation when canonical readback is incomplete', async () => {
    const yesterday = new Date(Date.now() - 86_400_000)
      .toISOString()
      .slice(0, 10);
    const submitted: string[] = [];
    let written: Record<string, unknown> | null = null;
    let readsAfterWrite = 0;
    const onSaved = vi.fn();
    vi.stubGlobal(
      'fetch',
      vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
        const path = fetchPath(input);
        if (path.endsWith('/children'))
          return mockResponse({
            parent_activity_ref: ACTIVITY,
            session_capture_mode: 'record_and_live',
            schedules: [],
          });
        if (path.endsWith('/auth/session'))
          return mockResponse({ csrf_token: 'test' });
        if (
          path.endsWith('/sessions/editor/batch') &&
          init?.method === 'POST'
        ) {
          const command = (
            JSON.parse(typeof init.body === 'string' ? init.body : '') as {
              commands: Array<Record<string, unknown>>;
            }
          ).commands[0]!;
          submitted.push(String(command.operation_id));
          written = {
            ...command,
            session_ref: MAIN,
            timing_material_state_ref: '019b0000-0000-7000-8000-000000000003',
          };
          return mockResponse([written]);
        }
        if (path.endsWith('/sessions/editor')) {
          if (!written) return mockResponse([]);
          readsAfterWrite += 1;
          return mockResponse(readsAfterWrite === 1 ? [] : [written]);
        }
        throw new Error('Unexpected request: ' + path);
      }),
    );
    render(
      <ActivitySessionRecordingEditor
        activityRef={ACTIVITY}
        activityTitle="Scrivere"
        timeZone="Etc/UTC"
        onClose={vi.fn()}
        onSaved={onSaved}
      />,
    );
    const group = (
      await screen.findByText('Sessione attività')
    ).closest<HTMLElement>('section.timeline-session-editor__group')!;
    setClock(group, 1, 'Inizio', yesterday, '09:00');
    setClock(group, 1, 'Fine', yesterday, '09:30');
    fireEvent.click(
      screen.getByRole('button', { name: 'Salva registrazioni' }),
    );
    await screen.findByText(/Registrazione non confermata dalla rilettura/);
    expect(
      group.querySelectorAll('.timeline-session-editor__parent-interval'),
    ).toHaveLength(1);
    expect(onSaved).not.toHaveBeenCalled();
    fireEvent.click(
      screen.getByRole('button', { name: 'Salva registrazioni' }),
    );
    await waitFor(() => expect(onSaved).toHaveBeenCalledOnce());
    expect(submitted).toHaveLength(2);
    expect(submitted[1]).toBe(submitted[0]);
  });

  it('preserves the repeated local hour when correcting a recorded Session', async () => {
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

  it('configures a child before saving its main, then submits one atomic group', async () => {
    const yesterday = new Date(Date.now() - 86_400_000)
      .toISOString()
      .slice(0, 10);
    const sent: Record<string, unknown>[][] = [];
    let records: Record<string, unknown>[] = [];
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
      if (path.endsWith('/sessions/editor/batch') && init?.method === 'POST') {
        const body = JSON.parse(
          typeof init.body === 'string' ? init.body : '',
        ) as {
          commands: Record<string, unknown>[];
        };
        sent.push(body.commands);
        records = body.commands.map((command, index) => ({
          session_ref: index ? MAIN : '019b0000-0000-7000-8000-000000000004',
          planned_schedule_ref: command.planned_schedule_ref,
          timing_material_state_ref: '019b0000-0000-7000-8000-000000000005',
          started_at: command.started_at,
          ended_at: command.ended_at,
          pause_ranges: command.pause_ranges,
        }));
        return mockResponse(records);
      }
      if (path.endsWith('/sessions/editor')) return mockResponse(records);
      if (path.endsWith('/auth/session'))
        return mockResponse({ csrf_token: 'test' });
      throw new Error('Unexpected request: ' + path);
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
    const main = await screen.findByText('Sessione attività');
    const group = main.closest<HTMLElement>(
      'section.timeline-session-editor__group',
    )!;
    setClock(group, 1, 'Inizio', yesterday, '09:00');
    setClock(group, 1, 'Fine', yesterday, '10:00');
    fireEvent.click(
      within(group).getByRole('button', { name: /Registra sessione/ }),
    );
    fireEvent.click(within(group).getByRole('button', { name: 'Lettura' }));
    const child = within(group)
      .getByText('Lettura', { selector: 'h3' })
      .closest('article')!;
    setClock(child, 1, 'Inizio', yesterday, '09:15');
    setClock(child, 1, 'Fine', yesterday, '09:35');
    fireEvent.click(
      screen.getByRole('button', { name: 'Salva registrazioni' }),
    );
    await waitFor(() => expect(sent).toHaveLength(1));
    expect(sent[0]).toHaveLength(2);
    expect(sent[0]?.[0]?.planned_schedule_ref).toBeNull();
    expect(sent[0]?.[1]?.planned_schedule_ref).toBe(MAIN);
    expect(sent[0]?.[0]?.session_ref).toBeNull();
    expect(sent[0]?.[1]?.session_ref).toBeNull();
    await waitFor(() =>
      expect(
        within(group).getAllByRole('button', { name: 'Correggi' }),
      ).toHaveLength(2),
    );
  });

  it('clamps a child outside the parent and localizes the warning to its interval', async () => {
    const yesterday = new Date(Date.now() - 86_400_000)
      .toISOString()
      .slice(0, 10);
    const fetcher = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      void init;
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
      if (path.endsWith('/sessions/editor'))
        return mockResponse([
          {
            session_ref: 'parent',
            planned_schedule_ref: null,
            timing_material_state_ref: 'parent-state',
            started_at: yesterday + 'T09:00:00Z',
            ended_at: yesterday + 'T10:00:00Z',
            pause_ranges: [
              {
                started_at: yesterday + 'T09:20:00Z',
                ended_at: yesterday + 'T09:30:00Z',
              },
            ],
          },
        ]);
      throw new Error('Unexpected request: ' + path);
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
    const options = await screen.findAllByRole('button', {
      name: /Registra sessione/,
    });
    expect(options).toHaveLength(2);
    fireEvent.click(options[0]!);
    fireEvent.click(screen.getByRole('button', { name: 'Lettura' }));
    const child = screen
      .getByText('Lettura', { selector: 'h3' })
      .closest('article')!;
    setClock(child, 1, 'Inizio', yesterday, '09:15');
    setClock(child, 1, 'Fine', yesterday, '09:35');
    expect(
      within(child).getByText(/Orario riportato entro i limiti/),
    ).toBeTruthy();
    expect(child.querySelector('[data-invalid]')).not.toBeNull();
    expect(fetcher.mock.calls.some(([, init]) => init?.method === 'POST')).toBe(
      false,
    );
  });

  it('treats three unrecorded named Sessions as independent editable blocks when main is disabled', async () => {
    const planned = [
      MAIN,
      '019b0000-0000-7000-8000-000000000006',
      '019b0000-0000-7000-8000-000000000007',
    ];
    const submissions: Record<string, unknown>[][] = [];
    let stored: Record<string, unknown>[] = [];
    const fetcher = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const path = fetchPath(input);
      if (path.endsWith('/children'))
        return mockResponse({
          parent_activity_ref: ACTIVITY,
          session_capture_mode: 'disabled',
          schedules: planned.map((schedule_ref, index) => ({
            schedule_ref,
            role_code: 'planned',
            presentation_order: index + 1,
            display_name: 'Sessione ' + (index + 1),
          })),
        });
      if (path.endsWith('/sessions/editor/batch') && init?.method === 'POST') {
        const payload = JSON.parse(
          typeof init.body === 'string' ? init.body : '',
        ) as {
          commands: Record<string, unknown>[];
        };
        submissions.push(payload.commands);
        stored = payload.commands.map((command, index) => ({
          session_ref: planned[index],
          planned_schedule_ref: command.planned_schedule_ref,
          timing_material_state_ref: planned[index],
          started_at: command.started_at,
          ended_at: command.ended_at,
          pause_ranges: command.pause_ranges,
        }));
        return mockResponse(stored);
      }
      if (path.endsWith('/sessions/editor')) return mockResponse(stored);
      if (path.endsWith('/auth/session'))
        return mockResponse({ csrf_token: 'test' });
      throw new Error('Unexpected request: ' + path);
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
    const independent = await screen.findByText('Sessione 1');
    const list = independent.closest('.timeline-session-editor__independent');
    expect(list).not.toBeNull();
    const yesterday = new Date(Date.now() - 86_400_000)
      .toISOString()
      .slice(0, 10);
    for (const [index, title] of [
      'Sessione 1',
      'Sessione 2',
      'Sessione 3',
    ].entries()) {
      const card = within(list as HTMLElement)
        .getByText(title, { selector: 'h3' })
        .closest('article')!;
      setClock(card, 1, 'Inizio', yesterday, '09:00');
      setClock(card, 1, 'Fine', yesterday, '10:00');
      expect(index).toBeGreaterThanOrEqual(0);
    }
    fireEvent.click(
      screen.getByRole('button', { name: 'Salva registrazioni' }),
    );
    await waitFor(() => expect(submissions).toHaveLength(1));
    expect(submissions[0]).toHaveLength(3);
    expect(
      submissions[0]!.map((command) => command.planned_schedule_ref),
    ).toEqual(planned);
  });

  it('resumes one child in both main intervals, persists a single paused attempt, and keeps Save outside the scroller', async () => {
    const yesterday = new Date(Date.now() - 86_400_000)
      .toISOString()
      .slice(0, 10);
    const onSaved = vi.fn();
    const onClose = vi.fn();
    const posted: Array<{ commands: Array<Record<string, unknown>> }> = [];
    let stored: Record<string, unknown>[] = [];
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
      if (path.endsWith('/auth/session'))
        return mockResponse({ csrf_token: 'test' });
      if (path.endsWith('/sessions/editor/batch') && init?.method === 'POST') {
        const request = JSON.parse(
          typeof init.body === 'string' ? init.body : '',
        ) as {
          commands: Array<Record<string, unknown>>;
        };
        posted.push(request);
        stored = request.commands.map((command, index) => ({
          session_ref:
            index === 0
              ? '019b0000-0000-7000-8000-000000000004'
              : '019b0000-0000-7000-8000-000000000005',
          timing_material_state_ref:
            index === 0
              ? '019b0000-0000-7000-8000-000000000006'
              : '019b0000-0000-7000-8000-000000000007',
          planned_schedule_ref: command.planned_schedule_ref,
          started_at: command.started_at,
          ended_at: command.ended_at,
          pause_ranges: command.pause_ranges,
        }));
        return mockResponse(stored);
      }
      if (path.endsWith('/sessions/editor')) return mockResponse(stored);
      throw new Error('Unexpected request: ' + path);
    });
    vi.stubGlobal('fetch', fetcher);
    render(
      <ActivitySessionRecordingEditor
        activityRef={ACTIVITY}
        activityTitle="test1"
        timeZone="Etc/UTC"
        onClose={onClose}
        onSaved={onSaved}
      />,
    );
    const mainTitle = await screen.findByText('Sessione attività');
    const group = mainTitle.closest<HTMLElement>(
      'section.timeline-session-editor__group',
    )!;
    setClock(group, 1, 'Inizio', yesterday, '09:00');
    setClock(group, 1, 'Fine', yesterday, '09:15');
    fireEvent.click(
      within(group).getByRole('button', { name: /Aggiungi intervallo/ }),
    );
    setClock(group, 2, 'Inizio', yesterday, '09:20');
    setClock(group, 2, 'Fine', yesterday, '09:35');
    const parents = group.querySelectorAll<HTMLElement>(
      '.timeline-session-editor__parent-interval',
    );
    expect(parents).toHaveLength(2);

    fireEvent.click(
      within(parents[0]!).getByRole('button', { name: /Registra sessione/ }),
    );
    fireEvent.click(
      within(parents[0]!).getByRole('button', { name: 'Lettura' }),
    );
    const firstChild =
      parents[0]!.querySelector<HTMLElement>('article.is-child')!;
    setClock(firstChild, 1, 'Inizio', yesterday, '09:02');
    setClock(firstChild, 1, 'Fine', yesterday, '09:12');

    fireEvent.click(
      within(parents[1]!).getByRole('button', { name: /Registra sessione/ }),
    );
    fireEvent.click(
      within(parents[1]!).getByRole('button', { name: 'Lettura · Riprendi' }),
    );
    const secondChild =
      parents[1]!.querySelector<HTMLElement>('article.is-child')!;
    expect(secondChild).not.toBeNull();
    setClock(secondChild, 2, 'Inizio', yesterday, '09:22');
    setClock(secondChild, 2, 'Fine', yesterday, '09:32');
    expect(parents[0]!.querySelectorAll('article.is-child')).toHaveLength(1);
    expect(parents[1]!.querySelectorAll('article.is-child')).toHaveLength(1);
    expect(group.querySelectorAll('article.is-child')).toHaveLength(2);

    const region = screen.getByRole('region', {
      name: 'Intervalli e Sessioni',
    });
    const save = screen.getByRole('button', { name: 'Salva registrazioni' });
    expect(region.contains(save)).toBe(false);
    expect(save.closest('footer')?.className).toContain(
      'timeline-session-editor__footer',
    );
    fireEvent.click(save);
    await waitFor(() => expect(onSaved).toHaveBeenCalledOnce());
    expect(onClose).not.toHaveBeenCalled();
    expect(posted).toHaveLength(1);
    expect(posted[0]!.commands).toHaveLength(2);
    expect(posted[0]!.commands[0]!.planned_schedule_ref).toBeNull();
    expect(posted[0]!.commands[1]!.planned_schedule_ref).toBe(MAIN);
    expect(posted[0]!.commands[1]!.pause_ranges).toEqual([
      {
        started_at: yesterday + 'T09:12:00.000Z',
        ended_at: yesterday + 'T09:22:00.000Z',
      },
    ]);
    expect(stored).toHaveLength(2);
    expect(group.querySelectorAll('article.is-child')).toHaveLength(2);
  });

  it('continues an already recorded child across a parent pause by correcting the same attempt', async () => {
    const yesterday = new Date(Date.now() - 86_400_000)
      .toISOString()
      .slice(0, 10);
    const mainRef = '019b0000-0000-7000-8000-000000000004';
    const childRef = '019b0000-0000-7000-8000-000000000005';
    const mainState = '019b0000-0000-7000-8000-000000000006';
    const childState = '019b0000-0000-7000-8000-000000000007';
    const onSaved = vi.fn();
    const parent = {
      session_ref: mainRef,
      timing_material_state_ref: mainState,
      planned_schedule_ref: null,
      started_at: yesterday + 'T09:00:00Z',
      ended_at: yesterday + 'T09:35:00Z',
      pause_ranges: [
        {
          started_at: yesterday + 'T09:15:00Z',
          ended_at: yesterday + 'T09:20:00Z',
        },
      ],
    };
    let records: Record<string, unknown>[] = [
      parent,
      {
        session_ref: childRef,
        timing_material_state_ref: childState,
        planned_schedule_ref: MAIN,
        started_at: yesterday + 'T09:02:00Z',
        ended_at: yesterday + 'T09:12:00Z',
        pause_ranges: [],
      },
    ];
    const corrections: Array<Record<string, unknown>> = [];
    vi.stubGlobal(
      'fetch',
      vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
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
        if (path.endsWith('/auth/session'))
          return mockResponse({ csrf_token: 'test' });
        if (
          path.endsWith('/sessions/editor/batch') &&
          init?.method === 'POST'
        ) {
          const payload = JSON.parse(
            typeof init.body === 'string' ? init.body : '',
          ) as {
            commands: Array<Record<string, unknown>>;
          };
          expect(payload.commands).toHaveLength(1);
          corrections.push(payload.commands[0]!);
          records = [
            parent,
            {
              ...payload.commands[0]!,
              session_ref: childRef,
              timing_material_state_ref: '019b0000-0000-7000-8000-000000000008',
            },
          ];
          return mockResponse(records.slice(1));
        }
        if (path.endsWith('/sessions/editor')) return mockResponse(records);
        throw new Error('Unexpected request: ' + path);
      }),
    );
    render(
      <ActivitySessionRecordingEditor
        activityRef={ACTIVITY}
        activityTitle="test1"
        timeZone="Etc/UTC"
        onClose={vi.fn()}
        onSaved={onSaved}
      />,
    );
    const first = await screen.findByText('Sessione attività');
    const group = first.closest<HTMLElement>(
      'section.timeline-session-editor__group',
    )!;
    const parents = group.querySelectorAll<HTMLElement>(
      '.timeline-session-editor__parent-interval',
    );
    expect(parents).toHaveLength(2);
    expect(parents[0]!.querySelectorAll('article.is-child')).toHaveLength(1);
    expect(parents[1]!.querySelectorAll('article.is-child')).toHaveLength(0);
    fireEvent.click(
      within(parents[1]!).getByRole('button', { name: /Registra sessione/ }),
    );
    fireEvent.click(
      within(parents[1]!).getByRole('button', { name: 'Lettura · Riprendi' }),
    );
    const secondChild =
      parents[1]!.querySelector<HTMLElement>('article.is-child')!;
    expect(secondChild).not.toBeNull();
    setClock(secondChild, 2, 'Inizio', yesterday, '09:22');
    setClock(secondChild, 2, 'Fine', yesterday, '09:32');
    fireEvent.click(
      screen.getByRole('button', { name: 'Salva registrazioni' }),
    );
    await waitFor(() => expect(onSaved).toHaveBeenCalledOnce());
    expect(corrections).toHaveLength(1);
    expect(corrections[0]?.session_ref).toBe(childRef);
    expect(corrections[0]?.expected_material_state_ref).toBe(childState);
    expect(corrections[0]?.pause_ranges).toHaveLength(1);
    expect(records).toHaveLength(2);
    expect(group.querySelectorAll('article.is-child')).toHaveLength(2);
  });
});
