import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import type { PlanWork } from './remote-plan-work-data-source';

const PLAN = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d';
const STATE = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617e';
const first = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617f';
const second = '0199a8c0-5e74-7bc0-8ad0-a2f403f56180';
const current: PlanWork = {
  planRef: PLAN, stateRef: STATE, title: 'Album',
  createdAt: '2026-09-28T12:00:00Z', replayed: false,
  steps: [
    { stepRef: first, position: 0, title: 'Record', activityRef: null,
      divisible: null, maxPlannedSlices: null, mergeCompatible: null, executionStrengthCode: null },
    { stepRef: second, position: 1, title: 'Mix', activityRef: null,
      divisible: null, maxPlannedSlices: null, mergeCompatible: null, executionStrengthCode: null },
  ],
};

const { list, replace } = vi.hoisted(() => ({
  list: vi.fn<() => Promise<readonly PlanWork[]>>(),
  replace: vi.fn(),
}));
vi.mock('./remote-plan-work-data-source', async (importOriginal) => {
  const original = await importOriginal<typeof import('./remote-plan-work-data-source')>();
  return {
    ...original,
    createRemotePlanWorkDataSource: () => ({
      list, replace, create: vi.fn(),
    }),
  };
});
vi.mock('./remote-plan-dependency-data-source', () => ({
  createRemotePlanDependencyDataSource: () => ({
    list: vi.fn().mockResolvedValue([]),
    create: vi.fn(),
    revise: vi.fn(),
  }),
}));

import { PlanWorkPanel } from './plan-work-panel';

describe('Plan work panel', () => {
  afterEach(cleanup);
  beforeEach(() => {
    list.mockReset().mockResolvedValue([current]);
    replace.mockReset().mockResolvedValue({
      ...current,
      stateRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f56181',
      steps: [current.steps[1], current.steps[0]],
    });
  });

  it('keeps Step order as an explicit Plan revision', async () => {
    render(<PlanWorkPanel />);
    fireEvent.click(screen.getByText('Plan e Step'));
    fireEvent.click(await screen.findByRole('button', { name: 'Sposta giù Record' }));
    await waitFor(() => expect(replace).toHaveBeenCalledOnce());
    expect(replace.mock.calls[0]?.[0]).toMatchObject({ planRef: PLAN, stateRef: STATE });
    expect(replace.mock.calls[0]?.[2].map((step: { stepRef: string }) => step.stepRef))
      .toEqual([second, first]);
  });

  it('adds the Activity selected from Home as a linked Step without a UUID field', async () => {
    render(<PlanWorkPanel />);
    window.dispatchEvent(new CustomEvent('dante:open-plan-for-activity', {
      detail: {
        activityRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f5618a',
        title: 'Mix dalla Home',
      },
    }));
    const add = await screen.findByRole('button', {
      name: '+ Aggiungi “Mix dalla Home” al Plan',
    });
    expect(screen.getByText('Mix dalla Home', { selector: 'strong' })).toBeTruthy();
    fireEvent.click(add);
    await waitFor(() => expect(replace).toHaveBeenCalledOnce());
    expect(replace.mock.calls[0]?.[2].at(-1)).toMatchObject({
      title: 'Mix dalla Home',
      activityRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f5618a',
    });
    expect(screen.queryByText(/UUID dell’Attività/)).toBeNull();
  });
});
