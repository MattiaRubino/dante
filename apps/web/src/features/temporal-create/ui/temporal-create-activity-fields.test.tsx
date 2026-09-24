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
