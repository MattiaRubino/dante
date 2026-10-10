// @vitest-environment jsdom
/* eslint-disable @typescript-eslint/require-await -- Fetch doubles intentionally resolve asynchronously. */
import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { useSessionPanel } from '../../../temporal/use-session-panel';
import { invalidateTemporalTimelineRead } from '../../../temporal/timeline-invalidation';
import { useSessionPanelPresentation } from './timeline-session-panel';

const activity = '0199a111-1111-7111-8111-111111111111';
const planned = '0199a222-2222-7222-8222-222222222222';
const session = '0199a333-3333-7333-8333-333333333333';
const state = '0199a444-4444-7444-8444-444444444444';
const nextState = '0199a555-5555-7555-8555-555555555555';
const now = '2026-10-09T10:00:00Z';
const requestPath = (input: RequestInfo | URL) =>
  input instanceof Request ? input.url : input.toString();
const requestBody = (init?: RequestInit) =>
  JSON.parse(typeof init?.body === 'string' ? init.body : '{}') as Record<
    string,
    unknown
  >;

function Harness({ enabled = true }: { enabled?: boolean }) {
  const controller = useSessionPanel(enabled);
  const view = useSessionPanelPresentation(controller);
  return (
    <section>
      <nav>{view.control}</nav>
    </section>
  );
}

const row = () => ({
  planned_schedule_ref: planned,
  name: 'Ripasso',
  starts_at: null,
  execution: null,
});
function feed(rows: unknown[] = [row()]) {
  return {
    evaluated_at: now,
    next_change_at: null,
    groups: rows.length
      ? [{ activity_ref: activity, title: 'Studio', rows }]
      : [],
  };
}

function runtime(paused = false, open = true) {
  return {
    session_ref: session,
    subject_native_ref: activity,
    timing_material_state_ref: paused ? nextState : state,
    planned_schedule_ref: planned,
    started_at: now,
    ended_at: open ? null : now,
    open,
    replayed: false,
    paused,
    evaluated_at: now,
    elapsed_seconds: 0,
    paused_seconds: 0,
    active_seconds: 0,
    duration_evaluations: [],
  };
}

beforeEach(() => {
  Object.defineProperty(document, 'visibilityState', {
    configurable: true,
    value: 'visible',
  });
});
afterEach(() => {
  cleanup();
  vi.useRealTimers();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

describe('Timeline Session panel integration', () => {
  it('shows a Session immediately after an accepted placement invalidation', async () => {
    let current = feed([]);
    const fetcher = vi.fn(async () => Response.json(current));
    vi.stubGlobal('fetch', fetcher);
    render(<Harness />);
    await waitFor(() => expect(fetcher).toHaveBeenCalledOnce());
    current = feed();
    act(() => invalidateTemporalTimelineRead());
    expect(
      await screen.findByRole('button', { name: 'Avvia · Ripasso' }),
    ).toBeTruthy();
    expect(fetcher).toHaveBeenCalledTimes(2);
  });

  it('groups sessions, opens on arrival, preserves dismissal and restores keyboard focus', async () => {
    let current = feed([]);
    const fetcher = vi.fn(async () => Response.json(current));
    vi.stubGlobal('fetch', fetcher);
    render(<Harness />);
    await waitFor(() => expect(fetcher).toHaveBeenCalledOnce());
    expect(screen.queryByRole('complementary')).toBeNull();
    current = feed([
      row(),
      { ...row(), planned_schedule_ref: state, name: 'Esercizi' },
    ]);
    fireEvent(window, new Event('focus'));
    expect(await screen.findByRole('complementary')).toBeTruthy();
    expect(screen.getAllByRole('region', { name: 'Studio' })).toHaveLength(1);
    expect(screen.getAllByRole('listitem')).toHaveLength(2);
    const trigger = screen.getByRole('button', {
      name: 'Sessioni disponibili · 2',
    });
    expect(trigger.getAttribute('data-timeline-tooltip')).toBe('Sessioni');
    expect(screen.getByRole('complementary').parentElement).toBe(
      trigger.parentElement,
    );
    fireEvent.keyDown(screen.getByRole('complementary'), { key: 'Escape' });
    expect(screen.queryByRole('complementary')).toBeNull();
    expect(document.activeElement).toBe(trigger);
    fireEvent(window, new Event('focus'));
    await waitFor(() =>
      expect(fetcher.mock.calls.length).toBeGreaterThanOrEqual(3),
    );
    expect(screen.queryByRole('complementary')).toBeNull();
    fireEvent.click(trigger);
    expect(screen.getByRole('complementary')).toBeTruthy();
  });

  it('executes start → pause → resume → stop with CSRF and accepted CAS; reads once per panel, not per row', async () => {
    let execution: null | {
      session_ref: string;
      timing_material_state_ref: string;
      paused: boolean;
    } = null;
    const commands: { path: string; body: Record<string, unknown> }[] = [];
    const fetcher = vi.fn(
      async (input: RequestInfo | URL, init?: RequestInit) => {
        const path = requestPath(input);
        if (path.endsWith('/session-panel'))
          return Response.json(feed([{ ...row(), execution }]));
        if (path === '/api/v1/auth/session')
          return Response.json({ authenticated: true, csrf_token: 'csrf' });
        expect(new Headers(init?.headers).get('X-Dante-CSRF')).toBe('csrf');
        const body = requestBody(init);
        commands.push({ path, body });
        const result = runtime(path.endsWith('/pause'), !path.endsWith('/end'));
        execution = result.open
          ? {
              session_ref: result.session_ref,
              timing_material_state_ref: result.timing_material_state_ref,
              paused: result.paused,
            }
          : null;
        return Response.json(result);
      },
    );
    vi.stubGlobal('fetch', fetcher);
    render(<Harness />);
    fireEvent.click(
      await screen.findByRole('button', { name: 'Avvia · Ripasso' }),
    );
    fireEvent.click(
      await screen.findByRole('button', { name: 'Pausa · Ripasso' }),
    );
    fireEvent.click(
      await screen.findByRole('button', { name: 'Riprendi · Ripasso' }),
    );
    await screen.findByRole('button', { name: 'Pausa · Ripasso' });
    fireEvent.click(screen.getByRole('button', { name: 'Termina · Ripasso' }));
    await screen.findByRole('button', { name: 'Avvia · Ripasso' });
    expect(commands.map((c) => c.path)).toEqual([
      `/api/v1/temporal/activities/${activity}/planned-sessions/${planned}/sessions`,
      `/api/v1/temporal/sessions/${session}/pause`,
      `/api/v1/temporal/sessions/${session}/resume`,
      `/api/v1/temporal/sessions/${session}/end`,
    ]);
    expect(commands[1]?.body.expected_material_state_ref).toBe(state);
    expect(commands[2]?.body.expected_material_state_ref).toBe(nextState);
    expect(new Set(commands.map((c) => c.body.operation_id)).size).toBe(4);
    expect(
      fetcher.mock.calls.some(([path]) =>
        /\/children$|\/execution-policy$/.test(requestPath(path)),
      ),
    ).toBe(false);
  });

  it('prevents duplicate clicks and preserves the operation ID after an uncertain failure', async () => {
    let release: (value: Response) => void = () => undefined;
    const ids: string[] = [];
    const fetcher = vi.fn(
      async (input: RequestInfo | URL, init?: RequestInit) => {
        if (requestPath(input).endsWith('/session-panel'))
          return Response.json(feed());
        if (requestPath(input).endsWith('/auth/session'))
          return Response.json({ authenticated: true, csrf_token: 'csrf' });
        const operation = requestBody(init).operation_id;
        if (typeof operation !== 'string')
          throw new Error('Missing operation ID');
        ids.push(operation);
        return new Promise<Response>((resolve) => {
          release = resolve;
        });
      },
    );
    vi.stubGlobal('fetch', fetcher);
    render(<Harness />);
    const play = await screen.findByRole('button', { name: 'Avvia · Ripasso' });
    fireEvent.click(play);
    fireEvent.click(play);
    await waitFor(() => expect(ids).toHaveLength(1));
    expect(play.hasAttribute('disabled')).toBe(true);
    await act(async () =>
      release(
        Response.json(
          { detail: 'Conflitto: aggiorna e riprova.' },
          { status: 409 },
        ),
      ),
    );
    expect(await screen.findByRole('alert')).toBeTruthy();
    await waitFor(() => expect(play.hasAttribute('disabled')).toBe(false));
    fireEvent.click(play);
    await waitFor(() => expect(ids).toHaveLength(2));
    expect(ids[1]).toBe(ids[0]);
    await act(async () => release(Response.json(runtime())));
  });

  it('shows read failure with retry, keeps stale rows visible but disables commands', async () => {
    let fail = false;
    vi.stubGlobal(
      'fetch',
      vi.fn(async () =>
        fail ? Response.json({}, { status: 503 }) : Response.json(feed()),
      ),
    );
    render(<Harness />);
    await screen.findByRole('button', { name: 'Avvia · Ripasso' });
    fail = true;
    fireEvent(window, new Event('focus'));
    expect(await screen.findByRole('alert')).toBeTruthy();
    expect(
      screen
        .getByRole('button', { name: 'Avvia · Ripasso' })
        .hasAttribute('disabled'),
    ).toBe(true);
    fail = false;
    fireEvent.click(screen.getByRole('button', { name: 'Riprova' }));
    await waitFor(() => expect(screen.queryByRole('alert')).toBeNull());
  });

  it('refreshes at the server boundary without relying on the device date and suspends hidden polling', async () => {
    vi.useFakeTimers();
    const fetcher = vi.fn(async () =>
      Response.json({ ...feed(), next_change_at: '2026-10-09T10:00:02Z' }),
    );
    vi.stubGlobal('fetch', fetcher);
    const view = render(<Harness />);
    await act(async () => {
      await vi.advanceTimersByTimeAsync(0);
    });
    expect(fetcher).toHaveBeenCalledOnce();
    await act(async () => {
      await vi.advanceTimersByTimeAsync(1999);
    });
    expect(fetcher).toHaveBeenCalledOnce();
    await act(async () => {
      await vi.advanceTimersByTimeAsync(1);
    });
    expect(fetcher).toHaveBeenCalledTimes(2);
    Object.defineProperty(document, 'visibilityState', {
      configurable: true,
      value: 'hidden',
    });
    fireEvent(document, new Event('visibilitychange'));
    await act(async () => {
      await vi.advanceTimersByTimeAsync(60_000);
    });
    expect(fetcher).toHaveBeenCalledTimes(2);
    Object.defineProperty(document, 'visibilityState', {
      configurable: true,
      value: 'visible',
    });
    fireEvent(document, new Event('visibilitychange'));
    await act(async () => {
      await vi.advanceTimersByTimeAsync(0);
    });
    expect(fetcher).toHaveBeenCalledTimes(3);
    view.unmount();
    await act(async () => {
      await vi.advanceTimersByTimeAsync(60_000);
    });
    expect(fetcher).toHaveBeenCalledTimes(3);
  });

  it('does not activate network reads in the frozen fixture boundary', () => {
    const fetcher = vi.fn();
    vi.stubGlobal('fetch', fetcher);
    render(<Harness enabled={false} />);
    expect(fetcher).not.toHaveBeenCalled();
  });
  it('shows a timed internal in the five-minute preview but blocks premature Play', async () => {
    const fetcher = vi.fn(async () => Response.json(feed([
      {
        planned_schedule_ref: null, name: 'Sessione attività',
        starts_at: null, execution: null,
      },
      { ...row(), starts_at: '2026-10-09T10:05:00Z' },
    ])));
    vi.stubGlobal('fetch', fetcher);
    render(<Harness />);
    const internal = await screen.findByRole('button', { name: 'Avvia · Ripasso' });
    expect(internal.disabled).toBe(true);
    expect(screen.getByText('Imminente · attende orario')).toBeTruthy();
    expect(screen.getByRole('button', { name: 'Avvia · Sessione attività' }).disabled)
      .toBe(false);
    expect(fetcher).toHaveBeenCalledOnce();
  });

  it('keeps Stop enabled but forbids internal Resume while the main is paused', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => Response.json(feed([
      {
        planned_schedule_ref: null, name: 'Sessione attività',
        starts_at: null,
        execution: { session_ref: 'main', timing_material_state_ref: state, paused: true },
      },
      {
        ...row(),
        execution: { session_ref: session, timing_material_state_ref: nextState, paused: true },
      },
    ]))));
    render(<Harness />);
    const resume = await screen.findByRole('button', { name: 'Riprendi · Ripasso' });
    expect(resume.disabled).toBe(true);
    expect(screen.getByRole('button', { name: 'Termina · Ripasso' }).disabled)
      .toBe(false);
    expect(screen.getByRole('button', { name: 'Riprendi · Sessione attività' }).disabled)
      .toBe(false);
  });

});
