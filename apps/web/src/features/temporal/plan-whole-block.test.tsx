import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import type { PlanDependency } from './remote-plan-dependency-data-source';
import type { PlanWork } from './remote-plan-work-data-source';

const PLAN = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d';
const STATE = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617e';
const NEXT = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617f';
const RECORD = '0199a8c0-5e74-7bc0-8ad0-a2f403f56180';
const MIX = '0199a8c0-5e74-7bc0-8ad0-a2f403f56181';
const RECORD_ACTIVITY = '0199a8c0-5e74-7bc0-8ad0-a2f403f56182';
const MIX_ACTIVITY = '0199a8c0-5e74-7bc0-8ad0-a2f403f56183';

const initial: PlanWork = {
  planRef: PLAN, stateRef: STATE, title: 'Album',
  createdAt: '2026-09-29T12:00:00Z', replayed: false,
  steps: [
    { stepRef: RECORD, position: 0, title: 'Record', activityRef: RECORD_ACTIVITY,
      divisible: null, maxPlannedSlices: null, mergeCompatible: null, executionStrengthCode: null },
    { stepRef: MIX, position: 1, title: 'Mix', activityRef: MIX_ACTIVITY,
      divisible: null, maxPlannedSlices: null, mergeCompatible: null, executionStrengthCode: null },
  ],
};
const relation: PlanDependency = {
  dependencyRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f56184', planRef: PLAN,
  prerequisiteStepRef: RECORD, prerequisiteActivityRef: RECORD_ACTIVITY,
  dependentStepRef: MIX, dependentActivityRef: MIX_ACTIVITY,
  stateRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f56185',
  purposeCode: 'dependent_activity_admissibility',
  qualifierCode: 'actual_occurred', dispositionCode: null,
  active: true, recordedAt: '2026-09-29T12:01:00Z',
  evaluationCode: 'unknown', cycle: false, replayed: false,
};

const { listPlans, replacePlan, listDependencies, createDependency, assess } = vi.hoisted(() => ({
  listPlans: vi.fn(), replacePlan: vi.fn(), listDependencies: vi.fn(),
  createDependency: vi.fn(), assess: vi.fn(),
}));
vi.mock('./remote-plan-work-data-source', async (importOriginal) => {
  const original = await importOriginal<typeof import('./remote-plan-work-data-source')>();
  return { ...original, createRemotePlanWorkDataSource: () => ({
    list: listPlans, replace: replacePlan, create: vi.fn(),
  }) };
});
vi.mock('./remote-plan-dependency-data-source', () => ({
  createRemotePlanDependencyDataSource: () => ({
    list: listDependencies, create: createDependency, revise: vi.fn(),
  }),
}));
vi.mock('./remote-plan-execution-data-source', () => ({
  createRemotePlanExecutionDataSource: () => ({ assess }),
}));

import { PlanWorkPanel } from './plan-work-panel';

describe('B13 whole Plan panel', () => {
  afterEach(cleanup);
  beforeEach(() => {
    let accepted = initial;
    let currentRelation: PlanDependency | null = null;
    listPlans.mockReset().mockImplementation(async () => [accepted]);
    replacePlan.mockReset().mockImplementation(async (
      _prior: PlanWork, _title: string, steps: PlanWork['steps'],
    ) => {
      accepted = { ...accepted, stateRef: NEXT, steps };
      return accepted;
    });
    listDependencies.mockReset().mockImplementation(async () => currentRelation ? [currentRelation] : []);
    createDependency.mockReset().mockImplementation(async () => {
      currentRelation = relation;
      return relation;
    });
    assess.mockReset().mockResolvedValue({
      basis: 'explicit_proposed_slices', proposedCount: 1,
      countStatus: 'satisfied', countReason: 'within_proposed_count_limit',
      mergeStatus: 'not_requested', mergeReason: 'no_pair',
      mergedTemporalStatus: null, mergedTemporalRules: [], sliceAssessments: [],
    });
  });

  it('retains Dependency direction and Step policy through a shared Plan revision and reload', async () => {
    render(<PlanWorkPanel />);
    fireEvent.click(screen.getByText('Plan e Step'));
    fireEvent.change(await screen.findByLabelText('Step prerequisito'), {
      target: { value: RECORD },
    });
    fireEvent.change(screen.getByLabelText('Step dipendente'), { target: { value: MIX } });
    fireEvent.click(screen.getByRole('button', { name: 'Crea Dependency' }));
    await waitFor(() => expect(createDependency).toHaveBeenCalledOnce());
    expect(createDependency.mock.calls[0]?.[1]).toMatchObject({
      prerequisiteStepRef: RECORD, dependentStepRef: MIX,
      qualifierCode: 'actual_occurred',
    });
    expect(await screen.findByText(/Record → Mix/)).toBeTruthy();

    fireEvent.change(screen.getByLabelText('Step collegato'), { target: { value: MIX } });
    fireEvent.change(screen.getByLabelText(/Massimo segmenti proposti/), {
      target: { value: '2' },
    });
    fireEvent.click(screen.getByLabelText('Consenti unione di segmenti contigui compatibili'));
    fireEvent.click(screen.getByRole('button', { name: 'Salva policy nello Step' }));
    await waitFor(() => expect(replacePlan).toHaveBeenCalledOnce());
    expect(replacePlan.mock.calls[0]?.[0].stateRef).toBe(STATE);
    expect(replacePlan.mock.calls[0]?.[2][1]).toMatchObject({
      stepRef: MIX, maxPlannedSlices: 2, mergeCompatible: true,
      executionStrengthCode: 'hard',
    });
    await waitFor(() => expect(listPlans).toHaveBeenCalledTimes(2));
    fireEvent.click(screen.getByRole('button', { name: 'Ricarica Plan' }));
    await waitFor(() => expect(listPlans).toHaveBeenCalledTimes(3));
    fireEvent.change(screen.getByLabelText('Step collegato'), { target: { value: MIX } });
    expect(screen.getByText(/Policy corrente: divisibile, massimo 2/)).toBeTruthy();
    expect(screen.getByText(/Record → Mix/)).toBeTruthy();

    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi segmento' }));
    fireEvent.change(screen.getByLabelText('Inizio'), {
      target: { value: '2026-10-01T10:00' },
    });
    fireEvent.change(screen.getByLabelText('Fine'), {
      target: { value: '2026-10-01T11:00' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Valuta proposta' }));
    await waitFor(() => expect(assess).toHaveBeenCalledOnce());
    expect(assess.mock.calls[0]?.[0]).toMatchObject({ planRef: PLAN, stateRef: NEXT });
    expect(assess.mock.calls[0]?.[1]).toBe(MIX);
    expect(replacePlan).toHaveBeenCalledOnce();
  });
});
