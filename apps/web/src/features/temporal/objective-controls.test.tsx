// @vitest-environment jsdom
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';

import type { ObjectiveView } from './remote-reality-objective-data-source';
import { ObjectiveControls } from './objective-controls';

const source = vi.hoisted(() => ({
  listObjectives: vi.fn(),
  recordResult: vi.fn(),
}));

vi.mock('./remote-reality-objective-data-source', () => ({
  createRemoteRealityObjectiveDataSource: () => source,
}));

const quantity: ObjectiveView = {
  objectiveRef: 'objective-1',
  label: 'Quanti chilometri?',
  resultKind: 'quantity',
  comparatorCode: 'gte',
  targetValue: 10,
  targetMin: null,
  targetMax: null,
  unitCode: 'km',
  presentationOrder: 0,
  observationRef: null,
  observedBoolean: null,
  observedNumeric: null,
  qualitativeCode: null,
  evaluationStateRef: null,
  assessmentCode: null,
};

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

it('keeps the Inspector mounted when entering and recording a numeric observation', async () => {
  source.listObjectives.mockResolvedValue([quantity]);
  source.recordResult.mockResolvedValue(quantity);

  render(<ObjectiveControls kind="activity" subjectRef="activity-1" />);
  const input = await screen.findByRole('spinbutton', {
    name: 'Valore reale per Quanti chilometri?',
  });
  fireEvent.change(input, { target: { value: '8' } });

  expect(input).toHaveProperty('value', '8');
  fireEvent.click(screen.getByRole('button', { name: 'Registra' }));
  await waitFor(() =>
    expect(source.recordResult).toHaveBeenCalledWith(
      'objective-1',
      expect.objectContaining({ observedNumeric: 8 }),
    ),
  );
  expect(screen.getByRole('region', { name: 'Obiettivi' })).toBeTruthy();
});
