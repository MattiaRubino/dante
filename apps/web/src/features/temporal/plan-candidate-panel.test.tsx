import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';

import type { PlanWork } from './remote-plan-work-data-source';

const { search } = vi.hoisted(() => ({ search: vi.fn() }));
const { request, confirm } = vi.hoisted(() => ({ request: vi.fn(), confirm: vi.fn() }));
vi.mock('./remote-plan-candidate-data-source', () => ({
  createRemotePlanCandidateDataSource: () => ({ search }),
}));
vi.mock('./remote-plan-admission-data-source', () => ({
  createRemotePlanAdmissionDataSource: () => ({ request, confirm }),
}));

import { PlanCandidatePanel } from './plan-candidate-panel';

const plan = {
  planRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d',
  stateRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f5617e',
  title: 'Album', steps: [],
} as unknown as PlanWork;
const stepRef = '0199a8c0-5e74-7bc0-8ad0-a2f403f56180';

afterEach(() => { cleanup(); search.mockReset(); request.mockReset(); confirm.mockReset(); });

it('shows bounded previews without an apply action or a claim of availability', async () => {
  search.mockResolvedValue({
    basisStatus: 'supported', reasonCode: 'supported_rules_only',
    solverStatus: 'OPTIMAL', movementPolicyStatus: 'blocked',
    capacityEvaluated: false,
    candidates: [{
      startsAt: '2026-10-01T11:00:00Z', endsAt: '2026-10-01T12:00:00Z',
      softViolations: 1,
    }],
  });
  render(<PlanCandidatePanel plan={plan} stepRef={stepRef} activityRef="activity" title="Mix" />);
  expect(search).not.toHaveBeenCalled();
  fireEvent.click(screen.getByRole('button', { name: 'Cerca alternative vicine per Mix' }));
  await waitFor(() => expect(search).toHaveBeenCalledWith(plan, stepRef));
  expect(await screen.findByText(/vincoli soft non soddisfatti/)).toBeTruthy();
  expect(screen.getByText(/Disponibilità e capacità non valutate/)).toBeTruthy();
  expect(screen.getByText(/movimento automatico bloccato/)).toBeTruthy();
  expect(screen.queryByRole('button', { name: /applica|accetta|sposta/i })).toBeNull();
});

it('keeps an unsatisfied prerequisite distinct from infeasibility', async () => {
  search.mockResolvedValue({
    basisStatus: 'blocked', reasonCode: 'prerequisite_unsatisfied',
    solverStatus: null, movementPolicyStatus: 'missing',
    capacityEvaluated: false, candidates: [],
  });
  render(<PlanCandidatePanel plan={plan} stepRef={stepRef} activityRef="activity" title="Mix" />);
  fireEvent.click(screen.getByRole('button', { name: 'Cerca alternative vicine per Mix' }));
  expect(await screen.findByText('Un prerequisito non è soddisfatto.')).toBeTruthy();
});

it('requires an explicit review and handles pending confirmation before a committed effect', async () => {
  search.mockResolvedValue({
    basisFingerprint: 'f'.repeat(64), scheduleRef: 'schedule',
    scheduleStateRef: 'placement', policyStateRef: 'policy',
    currentStartsAt: '2026-10-01T10:00:00Z',
    currentEndsAt: '2026-10-01T11:00:00Z',
    basisStatus: 'supported', reasonCode: 'supported_rules_only',
    solverStatus: 'OPTIMAL', movementPolicyStatus: 'automatic',
    capacityEvaluated: false,
    candidates: [{ startsAt: '2026-10-01T11:00:00Z',
      endsAt: '2026-10-01T12:00:00Z', softViolations: 0 }],
  });
  request.mockResolvedValue({ kind: 'pending_confirmation', proposalRef: 'proposal', replayed: false });
  confirm.mockResolvedValue({ kind: 'committed', proposalRef: 'proposal', replayed: false });
  render(<PlanCandidatePanel plan={plan} stepRef={stepRef} activityRef="activity" title="Mix" />);
  fireEvent.click(screen.getByRole('button', { name: 'Cerca alternative vicine per Mix' }));
  expect(await screen.findByRole('button', { name: 'Rivedi questa alternativa' })).toBeTruthy();
  expect(request).not.toHaveBeenCalled();
  fireEvent.click(screen.getByRole('button', { name: 'Rivedi questa alternativa' }));
  expect(screen.getByText(/Attuale:/)).toBeTruthy();
  expect(screen.getByText(/Alternativa:/)).toBeTruthy();
  fireEvent.click(screen.getByRole('button', { name: 'Richiedi questo spostamento' }));
  await waitFor(() => expect(request).toHaveBeenCalledTimes(1));
  expect(await screen.findByText(/Proposta in attesa/)).toBeTruthy();
  expect(confirm).not.toHaveBeenCalled();
  fireEvent.click(screen.getByRole('button', { name: 'Conferma lo spostamento' }));
  await waitFor(() => expect(confirm).toHaveBeenCalledTimes(1));
  expect(await screen.findByText(/Spostamento registrato/)).toBeTruthy();
  expect(confirm.mock.calls[0]?.[3]).toBe(request.mock.calls[0]?.[3]);
});
