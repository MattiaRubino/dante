import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { createTemporalCreateFields } from '../model/temporal-create-session';
import { TemporalCreateActivityFields } from './temporal-create-activity-fields';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

describe('TemporalCreateActivityFields', () => {
  it('accepts whole-minute Session minimum values without five-minute steps', () => {
    const onPatch = vi.fn();
    const initial = createTemporalCreateFields({
      kind: 'activity',
      date: '2026-09-24',
      timeSemantics: 'unscheduled',
      timeZoneId: 'Europe/Rome',
      contextId: 'personale',
    });
    const fields = createTemporalCreateFields({
      ...initial,
      execution: { ...initial.execution, sessionMode: 'splittable' },
    });

    const { container } = render(
      <TemporalCreateActivityFields
        fields={fields}
        depth="full"
        onPatch={onPatch}
        renderError={() => null}
      />,
    );
    const minimum = container.querySelector<HTMLInputElement>(
      '[data-create-path="execution.minSessionMinutes"]',
    );
    expect(minimum?.min).toBe('1');
    expect(minimum?.step).toBe('1');
    if (minimum === null) {
      throw new Error('Expected Session minimum input.');
    }
    fireEvent.change(minimum, { target: { value: '26' } });
    expect(onPatch).toHaveBeenCalledWith({
      execution: { ...fields.execution, minSessionMinutes: 26 },
    });
  });

  it('moves a timed Activity to Da collocare when Session minimum is enabled', () => {
    const onPatch = vi.fn();
    const fields = createTemporalCreateFields({
      kind: 'activity',
      date: '2026-09-24',
      timeSemantics: 'timed',
      timeZoneId: 'Europe/Rome',
      contextId: 'personale',
    });

    render(
      <TemporalCreateActivityFields
        fields={fields}
        depth="full"
        onPatch={onPatch}
        renderError={() => null}
      />,
    );

    fireEvent.change(screen.getByDisplayValue('Una sessione'), {
      target: { value: 'splittable' },
    });

    expect(onPatch).toHaveBeenCalledWith({
      timeSemantics: 'unscheduled',
      scheduling: {
        ...fields.scheduling,
        constraintKind: 'none',
        fallbackPolicy: 'inherit',
      },
      execution: { ...fields.execution, sessionMode: 'splittable' },
    });
  });
});
