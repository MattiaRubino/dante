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

vi.mock('../../../temporal/actual-realization-controls', () => ({
  ActualRealizationControls: ({
    kind,
    subjectRef,
    onRecorded,
  }: {
    kind: string;
    subjectRef: string;
    onRecorded: () => void;
  }) => (
    <div data-testid="actual-realization-owner">
      <span>{`${kind}:${subjectRef}`}</span>
      <button type="button" onClick={onRecorded}>
        Realtà B10 registrata
      </button>
    </div>
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
  summary: 'An accepted Outcome has an open reconciliation decision.',
  effective_at: '2026-10-04T08:30:00Z',
  reconciliation_ref: '019a45a2-7180-7000-8000-000000000002',
  outcome_ref: '019a45a2-7180-7000-8000-000000000003',
  purpose_code: 'review.personal',
  session_ref: null,
  session_timing_material_state_ref: null,
  actions: ['open_reconciliation'],
};

const realizationReviewItem = {
  reason_code: 'realization_review',
  subject_kind: 'activity',
  subject_ref: '019a45a2-7180-7000-8000-000000000011',
  title: 'Allenamento forza',
  summary:
    'A real Session ended and this Activity asks you to record what happened.',
  effective_at: '2026-10-04T10:00:00Z',
  reconciliation_ref: null,
  outcome_ref: null,
  purpose_code: 'activity.policy.review',
  session_ref: '019a45a2-7180-7000-8000-000000000012',
  session_timing_material_state_ref:
    '019a45a2-7180-7000-8000-000000000013',
  actions: ['record_realization'],
};

describe('Home resolution rail', () => {
  it('derives reconciliation cards from the canonical queue and refreshes after the owner action', async () => {
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
    expect(within(panel).getByText('Decisione')).toBeTruthy();
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

  it('routes a real Session review to the Actual owner and removes it after reality is recorded', async () => {
    let open = true;
    const fetchFn = vi.fn(async (input: RequestInfo | URL) => {
      expect(String(input)).toContain('/api/v1/temporal/resolution-queue');
      return Response.json(
        open
          ? { items: [realizationReviewItem], count: 1 }
          : { items: [], count: 0 },
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
      expect(within(panel).getByText('Allenamento forza')).toBeTruthy(),
    );
    expect(within(panel).getByText('Realtà')).toBeTruthy();
    expect(
      within(panel).getByText('Sessione conclusa · registra cosa è successo.'),
    ).toBeTruthy();

    fireEvent.click(within(panel).getByRole('button', { name: 'Risolvi' }));
    expect(screen.getByTestId('actual-realization-owner').textContent).toContain(
      `activity:${realizationReviewItem.subject_ref}`,
    );
    expect(
      screen.queryByRole('button', { name: 'Decisione B10 registrata' }),
    ).toBeNull();

    open = false;
    fireEvent.click(
      screen.getByRole('button', { name: 'Realtà B10 registrata' }),
    );
    await waitFor(() =>
      expect(within(panel).queryByText('Allenamento forza')).toBeNull(),
    );
    expect(within(panel).getByLabelText('0 elementi aperti').textContent).toBe(
      '0',
    );
  });
});
