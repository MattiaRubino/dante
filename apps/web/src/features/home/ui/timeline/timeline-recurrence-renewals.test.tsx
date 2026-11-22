// @vitest-environment jsdom
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';

import { invalidateTemporalPlanningRead } from '../../../temporal/timeline-invalidation';
import { TimelineRecurrenceRenewals } from './timeline-recurrence-renewals';

const notice = {
  owner: 'routine',
  source_ref: '019b0000-0000-7000-8000-000000000001',
  title: 'Studio quotidiano',
  material_state_ref: '019b0000-0000-7000-8000-000000000002',
  allowed_count: 730,
  remaining_count: 30,
  revision: 0,
};

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

it.each([
  ['Continua', 'extend'],
  ['Termina', 'decline'],
] as const)(
  'offers %s for a pending open series and clears its notice',
  async (action, decision) => {
    const fetcher = vi
      .fn()
      .mockResolvedValueOnce(
        new Response(JSON.stringify([notice]), { status: 200 }),
      )
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({ authenticated: true, csrf_token: 'csrf' }),
          { status: 200 },
        ),
      )
      .mockResolvedValueOnce(new Response(null, { status: 204 }))
      .mockResolvedValueOnce(new Response(JSON.stringify([]), { status: 200 }));
    vi.stubGlobal('fetch', fetcher);
    render(
      <>
        <div className="dante-timeline-actions" />
        <TimelineRecurrenceRenewals />
      </>,
    );
    fireEvent.click(
      await screen.findByRole('button', { name: 'Serie da rinnovare: 1' }),
    );
    expect(screen.getByText('Studio quotidiano')).toBeTruthy();
    expect(screen.getByText(/30 occorrenze rimaste su 730/)).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: action }));
    await waitFor(() => expect(fetcher).toHaveBeenCalledTimes(4));
    const request = fetcher.mock.calls[2] as [string, RequestInit];
    expect(request[0]).toContain('/routine/');
    expect(JSON.parse(String(request[1].body))).toMatchObject({
      decision,
      expected_revision: 0,
      expected_material_state_ref: notice.material_state_ref,
    });
    await waitFor(() =>
      expect(
        screen.queryByRole('button', { name: 'Serie da rinnovare: 1' }),
      ).toBeNull(),
    );
  },
);

it('refreshes the remaining occurrence count without closing the renewal popup', async () => {
  let remaining = 30;
  const fetcher = vi.fn().mockImplementation(() =>
    Promise.resolve(
      new Response(JSON.stringify([{ ...notice, remaining_count: remaining }]), {
        status: 200,
      }),
    ),
  );
  vi.stubGlobal('fetch', fetcher);
  render(
    <>
      <div className="dante-timeline-actions" />
      <TimelineRecurrenceRenewals />
    </>,
  );
  fireEvent.click(
    await screen.findByRole('button', { name: 'Serie da rinnovare: 1' }),
  );
  expect(screen.getByText(/30 occorrenze rimaste su 730/)).toBeTruthy();
  remaining = 29;
  invalidateTemporalPlanningRead();
  await waitFor(() => {
    expect(screen.getByText(/29 occorrenze rimaste su 730/)).toBeTruthy();
  });
  expect(screen.getByRole('button', { name: 'Continua' })).toBeTruthy();
  expect(screen.getByRole('button', { name: 'Termina' })).toBeTruthy();
  expect(fetcher).toHaveBeenCalledTimes(2);
});
