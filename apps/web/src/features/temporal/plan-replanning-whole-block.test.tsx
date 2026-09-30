import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';

import type { PlanWork } from './remote-plan-work-data-source';

const { diagnose, search, request, confirm, requireConfirmation, setEarliestStart } = vi.hoisted(() => ({
  diagnose: vi.fn(),
  search: vi.fn(),
  request: vi.fn(),
  confirm: vi.fn(),
  requireConfirmation: vi.fn(),
  setEarliestStart: vi.fn(),
}));
vi.mock('./remote-plan-conflict-data-source', () => ({
  createRemotePlanConflictDataSource: () => ({ diagnose }),
}));
vi.mock('./remote-plan-candidate-data-source', () => ({
  createRemotePlanCandidateDataSource: () => ({ search }),
}));
vi.mock('./remote-plan-admission-data-source', () => ({
  createRemotePlanAdmissionDataSource: () => ({ request, confirm }),
}));
vi.mock('./remote-plan-replanning-setup-data-source', () => ({
  createRemotePlanReplanningSetupDataSource: () => ({ requireConfirmation, setEarliestStart }),
}));

import { PlanConflictPanel } from './plan-conflict-panel';

const recordStep = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617f';
const mixStep = '0199a8c0-5e74-7bc0-8ad0-a2f403f56180';
const recordActivity = '0199a8c0-5e74-7bc0-8ad0-a2f403f56183';
const mixActivity = '0199a8c0-5e74-7bc0-8ad0-a2f403f56184';
const plan: PlanWork = {
  planRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d',
  stateRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f5617e',
  title: 'Album',
  createdAt: '2026-09-29T12:00:00Z',
  replayed: false,
  steps: [
    {
      stepRef: recordStep,
      position: 0,
      title: 'Record',
      activityRef: recordActivity,
      divisible: null,
      maxPlannedSlices: null,
      mergeCompatible: null,
      executionStrengthCode: null,
    },
    {
      stepRef: mixStep,
      position: 1,
      title: 'Mix',
      activityRef: mixActivity,
      divisible: null,
      maxPlannedSlices: null,
      mergeCompatible: null,
      executionStrengthCode: null,
    },
  ],
};
const placement = {
  scheduleRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f56185',
  materialStateRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f56186',
  temporalFormCode: 'absolute',
  startsAt: '2026-10-02T10:00:00Z',
  endsAt: '2026-10-02T11:00:00Z',
};
const base = {
  basisFingerprint: 'f'.repeat(64),
  scheduleRef: placement.scheduleRef,
  scheduleStateRef: placement.materialStateRef,
  policyStateRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f56187',
  currentStartsAt: placement.startsAt,
  currentEndsAt: placement.endsAt,
  movementPolicyStatus: 'automatic',
  capacityEvaluated: false,
};
const diagnosis = (evaluationCode: 'unknown' | 'satisfied') => ({
  planRef: plan.planRef,
  planStateRef: plan.stateRef,
  title: plan.title,
  capacityEvaluated: false,
  steps: [
    {
      stepRef: recordStep,
      title: 'Record',
      activityRef: recordActivity,
      diagnostics: ['unknown_basis'],
      placements: [],
      dependencies: [],
    },
    {
      stepRef: mixStep,
      title: 'Mix',
      activityRef: mixActivity,
      diagnostics:
        evaluationCode === 'unknown'
          ? ['known_hard_violation', 'unknown_basis']
          : ['known_hard_violation'],
      placements: [placement],
      dependencies: [
        {
          dependencyRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f56181',
          prerequisiteStepRef: recordStep,
          evaluationCode,
        },
      ],
    },
  ],
});

afterEach(() => {
  cleanup();
  diagnose.mockReset();
  search.mockReset();
  request.mockReset();
  confirm.mockReset();
  requireConfirmation.mockReset();
  setEarliestStart.mockReset();
});

it('traces unknown prerequisite, reviewed proposal, confirmation and refreshed Schedule', async () => {
  diagnose
    .mockResolvedValueOnce(diagnosis('unknown'))
    .mockResolvedValueOnce(diagnosis('satisfied'));
  search
    .mockResolvedValueOnce({
      ...base,
      basisStatus: 'unknown',
      reasonCode: 'prerequisite_unknown',
      solverStatus: null,
      candidates: [],
    })
    .mockResolvedValueOnce({
      ...base,
      basisStatus: 'supported',
      reasonCode: 'supported_rules_only',
      solverStatus: 'OPTIMAL',
      candidates: [
        {
          startsAt: '2026-10-02T11:00:00Z',
          endsAt: '2026-10-02T12:00:00Z',
          softViolations: 0,
        },
      ],
    })
    .mockResolvedValueOnce({
      ...base,
      currentStartsAt: '2026-10-02T11:00:00Z',
      currentEndsAt: '2026-10-02T12:00:00Z',
      basisStatus: 'supported',
      reasonCode: 'supported_rules_only',
      solverStatus: 'OPTIMAL',
      candidates: [],
    });
  request.mockResolvedValue({
    kind: 'pending_confirmation',
    proposalRef: 'proposal',
    replayed: false,
  });
  confirm.mockResolvedValue({
    kind: 'committed',
    proposalRef: 'proposal',
    replayed: false,
  });

  render(<PlanConflictPanel plan={plan} />);
  fireEvent.click(screen.getByRole('button', { name: 'Analizza conflitti' }));
  expect(await screen.findByText(/Dependency da Record/)).toBeTruthy();
  expect(screen.getByText(/sconosciuta/)).toBeTruthy();
  expect(
    screen.getByText(/collocazione corrente viola un vincolo/),
  ).toBeTruthy();
  fireEvent.click(
    screen.getByRole('button', { name: 'Cerca alternative vicine per Mix' }),
  );
  expect(await screen.findByText(/Un prerequisito è sconosciuto/)).toBeTruthy();
  expect(
    screen.queryByRole('button', { name: 'Rivedi questa alternativa' }),
  ).toBeNull();
  expect(request).not.toHaveBeenCalled();

  fireEvent.click(screen.getByRole('button', { name: 'Analizza conflitti' }));
  await waitFor(() => expect(diagnose).toHaveBeenCalledTimes(2));
  expect(await screen.findByText(/soddisfatta/)).toBeTruthy();
  fireEvent.click(
    screen.getByRole('button', { name: 'Cerca alternative vicine per Mix' }),
  );
  fireEvent.click(
    await screen.findByRole('button', { name: 'Rivedi questa alternativa' }),
  );
  expect(screen.getByText(/Attuale:/)).toBeTruthy();
  expect(screen.getByText(/Alternativa:/)).toBeTruthy();
  expect(
    screen.getAllByText(/Disponibilità e capacità non valutate/),
  ).toHaveLength(2);
  fireEvent.click(
    screen.getByRole('button', { name: 'Richiedi questo spostamento' }),
  );
  expect(
    await screen.findByText(/Proposta in attesa: la Schedule non è cambiata/),
  ).toBeTruthy();
  expect(confirm).not.toHaveBeenCalled();
  fireEvent.click(
    screen.getByRole('button', { name: 'Conferma lo spostamento' }),
  );
  await waitFor(() => expect(confirm).toHaveBeenCalledTimes(1));
  expect(await screen.findByText(/Schedule attuale:/)).toBeTruthy();
  expect(search).toHaveBeenCalledTimes(3);
  expect(request.mock.calls[0]?.[3]).toEqual(confirm.mock.calls[0]?.[3]);
});

it('shows unsupported placement and blocked Policy without offering review', async () => {
  const unsupported = diagnosis('satisfied');
  unsupported.steps[1]!.diagnostics = ['unsupported_placement'];
  unsupported.steps[1]!.placements = [
    { ...placement, temporalFormCode: 'floating_local' },
  ];
  diagnose
    .mockResolvedValueOnce(unsupported)
    .mockResolvedValueOnce(diagnosis('satisfied'));
  search.mockResolvedValueOnce({
    ...base,
    movementPolicyStatus: 'blocked',
    basisStatus: 'supported',
    reasonCode: 'supported_rules_only',
    solverStatus: 'OPTIMAL',
    candidates: [
      {
        startsAt: '2026-10-02T11:00:00Z',
        endsAt: '2026-10-02T12:00:00Z',
        softViolations: 0,
      },
    ],
  });
  render(<PlanConflictPanel plan={plan} />);
  fireEvent.click(screen.getByRole('button', { name: 'Analizza conflitti' }));
  expect(
    await screen.findByText(/Forma della collocazione non ancora supportata/),
  ).toBeTruthy();
  expect(
    screen.queryByRole('button', { name: /Cerca alternative vicine per Mix/ }),
  ).toBeNull();

  fireEvent.click(screen.getByRole('button', { name: 'Analizza conflitti' }));
  fireEvent.click(
    await screen.findByRole('button', {
      name: 'Cerca alternative vicine per Mix',
    }),
  );
  expect(await screen.findByText(/movimento automatico bloccato/)).toBeTruthy();
  expect(
    screen.queryByRole('button', { name: 'Rivedi questa alternativa' }),
  ).toBeNull();
  expect(request).not.toHaveBeenCalled();
});

it('configures a hard conflict and confirmation Policy by clicks before reviewed admission', async () => {
  diagnose.mockResolvedValue(diagnosis('satisfied'));
  const candidate = {
    ...base, basisStatus: 'supported', reasonCode: 'supported_rules_only',
    solverStatus: 'OPTIMAL', candidates: [{
      startsAt: '2026-10-02T11:00:00Z', endsAt: '2026-10-02T12:00:00Z',
      softViolations: 0,
    }],
  };
  search
    .mockResolvedValueOnce({ ...candidate, movementPolicyStatus: 'missing', policyStateRef: null })
    .mockResolvedValueOnce({ ...candidate, movementPolicyStatus: 'missing', policyStateRef: null })
    .mockResolvedValueOnce(candidate);
  setEarliestStart.mockResolvedValue(undefined);
  requireConfirmation.mockResolvedValue(undefined);
  render(<PlanConflictPanel plan={plan} />);
  fireEvent.click(screen.getByRole('button', { name: 'Analizza conflitti' }));
  fireEvent.click(await screen.findByRole('button', { name: 'Cerca alternative vicine per Mix' }));
  expect(await screen.findByRole('button', { name: 'Consenti spostamento con conferma' })).toBeTruthy();
  expect(screen.queryByRole('button', { name: 'Rivedi questa alternativa' })).toBeNull();
  const boundary = new Date(Date.parse(placement.startsAt) + 60 * 60 * 1000);
  const localBoundary = new Date(boundary.getTime() - boundary.getTimezoneOffset() * 60_000)
    .toISOString().slice(0, 16);
  fireEvent.change(screen.getByLabelText('Inizio non prima di'), {
    target: { value: localBoundary },
  });
  fireEvent.click(screen.getByRole('button', { name: 'Imposta vincolo hard' }));
  await waitFor(() => expect(setEarliestStart).toHaveBeenCalledWith(
    mixActivity, boundary.toISOString(),
  ));
  fireEvent.click(await screen.findByRole('button', {
    name: 'Consenti spostamento con conferma',
  }));
  await waitFor(() => expect(requireConfirmation).toHaveBeenCalledWith(placement.scheduleRef, null));
  expect(await screen.findByRole('button', { name: 'Rivedi questa alternativa' })).toBeTruthy();
  expect(request).not.toHaveBeenCalled();
});
