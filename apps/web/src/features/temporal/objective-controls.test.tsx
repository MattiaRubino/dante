// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';

import type { ObjectiveView } from './remote-reality-objective-data-source';
import { ObjectiveControls } from './objective-controls';

const source = vi.hoisted(() => ({
  listObjectives: vi.fn(),
  listObjectiveInputDrafts: vi.fn(),
  stageObjectiveInput: vi.fn(),
  confirmObjectiveInput: vi.fn(),
}));

vi.mock('./remote-reality-objective-data-source', () => ({
  createRemoteRealityObjectiveDataSource: () => source,
}));

const quantity: ObjectiveView = {
  objectiveRef: 'objective-1',
  label: 'Quanti chilometri?',
  resultKind: 'quantity', comparatorCode: 'gte', targetValue: 10,
  targetMin: null, targetMax: null, unitCode: 'km', presentationOrder: 0,
  observationRef: null, observedBoolean: null, observedNumeric: null,
  qualitativeCode: null, evaluationStateRef: null, assessmentCode: null,
};

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

it('persists a provisional value, confirms explicitly, and never records on mere typing', async () => {
  let accepted = false;
  source.listObjectives.mockImplementation(async () => [
    accepted ? { ...quantity, observationRef: 'observation-1', observedNumeric: 8,
      assessmentCode: 'partial' } : quantity,
  ]);
  source.listObjectiveInputDrafts.mockResolvedValue([]);
  source.stageObjectiveInput.mockImplementation(async () => ({
    objectiveRef: quantity.objectiveRef, revision: 1,
    payload: { observed_numeric: 8 }, confirmedAt: null,
    updatedAt: '2026-10-10T19:00:00Z',
  }));
  source.confirmObjectiveInput.mockImplementation(async () => {
    accepted = true;
  });

  render(<ObjectiveControls kind="activity" subjectRef="activity-1" />);
  const input = await screen.findByRole('spinbutton', {
    name: 'Valore reale per Quanti chilometri?',
  });
  fireEvent.change(input, { target: { value: '8' } });
  expect(input).toHaveProperty('value', '8');
  expect(source.confirmObjectiveInput).not.toHaveBeenCalled();

  await waitFor(() =>
    expect(source.stageObjectiveInput).toHaveBeenCalledWith(
      'objective-1', { observed_numeric: 8 }, null, expect.any(String),
    ),
  );
  await screen.findByText('Bozza salvata · non confermata');
  expect(source.confirmObjectiveInput).not.toHaveBeenCalled();

  fireEvent.click(screen.getByRole('button', {
    name: 'Conferma obiettivo Quanti chilometri?',
  }));
  await waitFor(() =>
    expect(source.confirmObjectiveInput).toHaveBeenCalledWith(
      'objective-1', 1, expect.any(String),
    ),
  );
  await screen.findByText('Valore confermato · 8 km');
  expect(screen.getByRole('region', { name: 'Obiettivi' })).toBeTruthy();
});

it('loads a previously staged value without falsely confirming it', async () => {
  source.listObjectives.mockResolvedValue([quantity]);
  source.listObjectiveInputDrafts.mockResolvedValue([{
    objectiveRef: quantity.objectiveRef, revision: 3,
    payload: { observed_numeric: 7 }, confirmedAt: null,
    updatedAt: '2026-10-10T19:00:00Z',
  }]);
  render(<ObjectiveControls kind="activity" subjectRef="activity-1" />);
  const input = await screen.findByRole('spinbutton', {
    name: 'Valore reale per Quanti chilometri?',
  });
  await waitFor(() => expect(input).toHaveProperty('value', '7'));
  expect(screen.getByText('Bozza salvata · non confermata')).toBeTruthy();
  expect(source.confirmObjectiveInput).not.toHaveBeenCalled();
});
