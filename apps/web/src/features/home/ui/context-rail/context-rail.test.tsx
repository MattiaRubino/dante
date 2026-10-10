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

vi.mock('../../../temporal/objective-controls', () => ({
  ObjectiveControls: ({
    kind,
    subjectRef,
    onRecorded,
  }: {
    kind: string;
    subjectRef: string;
    onRecorded: () => void;
  }) => (
    <div data-testid="objective-owner">
      <span>{`${kind}:${subjectRef}`}</span>
      <button type="button" onClick={onRecorded}>Obiettivo valutato</button>
    </div>
  ),
}));

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
    sessionBasis,
  }: {
    kind: string;
    subjectRef: string;
    onRecorded: () => void;
    sessionBasis?: { sessionRef: string; sessionTimingMaterialStateRef: string };
  }) => (
    <div data-testid="actual-realization-owner">
      <span>{`${kind}:${subjectRef}`}</span>
      <span>{sessionBasis?.sessionRef ?? 'no-session'}</span>
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
    const fetchFn = vi.fn((input: RequestInfo | URL) => {
      if (!(typeof input === 'string' ? input : input instanceof URL ? input.href : input.url).includes('/resolution-queue')) return Promise.resolve(Response.json([]));
      return Promise.resolve(Response.json(
        open ? { items: [openItem], count: 1 } : { items: [], count: 0 },
      ));
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
    expect(within(panel).getByLabelText('1 elementi da verificare').textContent).toBe(
      '1',
    );
    expect(within(panel).getByText('Decisione')).toBeTruthy();
    expect(within(panel).queryByText('Revisione concept')).toBeNull();

    fireEvent.click(within(panel).getByRole('button', { name: 'Apri decisione: Preparare le slide' }));
    open = false;
    fireEvent.click(
      screen.getByRole('button', { name: 'Decisione B10 registrata' }),
    );
    await waitFor(() =>
      expect(within(panel).queryByText('Preparare le slide')).toBeNull(),
    );
    expect(within(panel).getByLabelText('0 elementi da verificare').textContent).toBe(
      '0',
    );
  });

  it('routes a real Session review to the Actual owner and removes it after reality is recorded', async () => {
    let open = true;
    const fetchFn = vi.fn((input: RequestInfo | URL) => {
      if (!(typeof input === 'string' ? input : input instanceof URL ? input.href : input.url).includes('/resolution-queue')) return Promise.resolve(Response.json([]));
      return Promise.resolve(Response.json(
        open
          ? { items: [realizationReviewItem], count: 1 }
          : { items: [], count: 0 },
      ));
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

    expect(screen.getByTestId('actual-realization-owner').textContent).toContain(
      `activity:${realizationReviewItem.subject_ref}`,
    );
    expect(screen.getByTestId('actual-realization-owner').textContent).toContain(
      realizationReviewItem.session_ref,
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
    expect(within(panel).getByLabelText('0 elementi da verificare').textContent).toBe(
      '0',
    );
  });
  it('opens pending Event Objectives through their canonical owner and refreshes after assessment', async () => {
    const objectiveReviewItem = {
      reason_code: 'objective_review',
      subject_kind: 'event',
      subject_ref: '019a45a2-7180-7000-8000-000000000021',
      title: 'Gara',
      summary: 'One or more Objectives are ready for assessment.',
      effective_at: '2026-10-04T12:00:00Z',
      reconciliation_ref: null,
      outcome_ref: null,
      purpose_code: 'objective.review',
      session_ref: null,
      session_timing_material_state_ref: null,
      actions: ['open_objectives'],
    };
    let open = true;
    vi.stubGlobal('fetch', vi.fn((input: RequestInfo | URL) =>
      Promise.resolve(Response.json((typeof input === 'string' ? input : input instanceof URL ? input.href : input.url).includes('/resolution-queue')
        ? open ? { items: [objectiveReviewItem], count: 1 }
          : { items: [], count: 0 }
        : [])),
    ));

    const { container } = render(<ContextRail />);
    const panel = container.querySelector<HTMLElement>('[data-home-context="resolution"]');
    if (!panel) throw new Error('Resolution panel absent.');
    await waitFor(() => expect(within(panel).getByText('Gara')).toBeTruthy());
    fireEvent.click(within(panel).getByRole('button', { name: 'Valuta obiettivi: Gara' }));
    expect(screen.getByTestId('objective-owner').textContent).toContain(
      `event:${objectiveReviewItem.subject_ref}`,
    );
    open = false;
    fireEvent.click(screen.getByRole('button', { name: 'Obiettivo valutato' }));
    await waitFor(() => expect(within(panel).queryByText('Gara')).toBeNull());
  });

});


it('switches three views and only opens one selected Objective owner', async () => {
  const objectiveItem = {
    objective_ref: '019a45a2-7180-7000-8000-000000000031',
    subject_kind: 'activity',
    subject_ref: '019a45a2-7180-7000-8000-000000000032',
    subject_title: 'Studio inglese',
    label: 'Vocaboli',
    result_kind: 'quantity',
    presentation_order: 1,
    draft_revision: 1,
    draft_updated_at: '2026-10-10T17:00:00Z',
  };
  vi.stubGlobal('fetch', vi.fn((input: RequestInfo | URL) => {
    const uri = (typeof input === 'string' ? input : input instanceof URL ? input.href : input.url);
    return Promise.resolve(Response.json(
      uri.includes('/resolution-queue') ? { items: [], count: 0 } :
      uri.includes('/finished-work') ? [{
        subject_kind: 'activity', subject_ref: objectiveItem.subject_ref,
        session_ref: '019a45a2-7180-7000-8000-000000000033',
        title: 'Studio inglese', started_at: '2026-10-10T16:00:00Z',
        ended_at: '2026-10-10T17:00:00Z', record_kind: 'session_ended',
      }] :
      uri.includes('/objective-work') ? [objectiveItem] : [],
    ));
  }));
  render(<ContextRail />);
  fireEvent.click(screen.getByRole('tab', { name: 'Conclusi' }));
  await screen.findByText('Sessione conclusa');
  expect(screen.getByText('Studio inglese')).toBeTruthy();
  fireEvent.click(screen.getByRole('tab', { name: 'Obiettivi' }));
  await screen.findByText('Vocaboli');
  expect(screen.getByText('Bozza salvata')).toBeTruthy();
  fireEvent.click(screen.getByRole('button', { name: 'Compila obiettivi' }));
  expect(screen.getByTestId('objective-owner').textContent).toContain(
    `activity:${objectiveItem.subject_ref}`,
  );
});
