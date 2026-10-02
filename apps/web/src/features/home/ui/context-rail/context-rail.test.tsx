import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { ContextRail } from './context-rail';

vi.mock('../../../temporal/reconciliation-controls', () => ({
  ReconciliationControls: ({ onRecorded }: { onRecorded: () => void }) => (
    <button type="button" onClick={onRecorded}>
      Decisione B10 registrata
    </button>
  ),
}));

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

const openItem = {
  reason_code: 'reconciliation_open',
  subject_kind: 'activity',
  subject_ref: '019a45a2-7180-7000-8000-000000000001',
  title: 'Preparare le slide',
  reconciliation_ref: '019a45a2-7180-7000-8000-000000000002',
  outcome_ref: '019a45a2-7180-7000-8000-000000000003',
  purpose_code: 'review.personal',
};

describe('Home resolution rail', () => {
  it('derives the count and cards from the canonical queue and refreshes after an owner action', async () => {
    let open = true;
    const fetchFn = vi.fn(async (input: RequestInfo | URL) => {
      expect(String(input)).toContain('/api/v1/temporal/resolution-queue');
      return Response.json(
        open ? { items: [openItem], count: 1 } : { items: [], count: 0 },
      );
    });
    vi.stubGlobal('fetch', fetchFn);

    const { container } = render(<ContextRail />);
    const panel = container.querySelector<HTMLElement>(
      '[data-home-context="resolution"]',
    );
    expect(panel).not.toBeNull();
    if (!panel) throw new Error('Resolution panel absent.');
    await waitFor(() =>
      expect(within(panel).getByText('Preparare le slide')).toBeTruthy(),
    );
    expect(within(panel).getByLabelText('1 elementi aperti').textContent).toBe(
      '1',
    );
    expect(within(panel).queryByText('Revisione concept')).toBeNull();

    fireEvent.click(within(panel).getByRole('button', { name: 'Risolvi' }));
    open = false;
    fireEvent.click(
      screen.getByRole('button', { name: 'Decisione B10 registrata' }),
    );
    await waitFor(() =>
      expect(within(panel).queryByText('Preparare le slide')).toBeNull(),
    );
    expect(within(panel).getByLabelText('0 elementi aperti').textContent).toBe(
      '0',
    );
  });
});
