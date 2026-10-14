// @vitest-environment jsdom

import { Temporal } from '@dante/time';
import {
  cleanup,
  fireEvent,
  render,
  screen,
  within,
} from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { TemporalCreateEntry } from './temporal-create-entry';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => cleanup());

function openAdvanced() {
  const view = render(
    <>
      <div data-home-context-create-host />
      <TemporalCreateEntry
        defaultDate={Temporal.PlainDate.from('2026-10-01')}
        contexts={[{ id: 'personale', label: 'Personale', tone: 'personal' }]}
        onPreview={() => undefined}
        onApplied={() => false}
        creationEnabled={false}
      />
    </>,
  );
  const trigger = view.container.querySelector<HTMLButtonElement>(
    '.dante-timeline-quick-add',
  );
  if (!trigger) throw new Error('Expected Create trigger');
  fireEvent.click(trigger);
  fireEvent.change(screen.getByPlaceholderText('Titolo'), {
    target: { value: 'Attività con Sessione' },
  });
  fireEvent.click(screen.getByRole('button', { name: /Opzioni avanzate/ }));
  return view;
}

function plannedSessionActions(): HTMLElement {
  const actions = document.querySelector<HTMLElement>(
    '.temporal-create-activity-tree__root-actions',
  );
  if (!actions) throw new Error('Expected planned Session actions');
  return actions;
}

describe('Activity Create current interval and planned Session controls', () => {
  it('keeps a named Session independent from Activity time controls', () => {
    openAdvanced();
    const actions = plannedSessionActions();
    fireEvent.click(within(actions).getByRole('button', { name: 'Sessione' }));
    const planned = document.querySelector<HTMLElement>(
      '[data-create-planned-session]',
    );
    if (!planned) throw new Error('Expected planned Session row');
    fireEvent.change(
      within(planned).getByRole('textbox', { name: 'Nome Sessione' }),
      {
        target: { value: 'Una prova breve' },
      },
    );
    expect(
      within(planned).queryByRole('button', { name: 'Orario' }),
    ).toBeNull();
    expect(
      planned.querySelector('[data-create-path$=".startTime"]'),
    ).toBeNull();
    expect(planned.querySelector('[data-create-path$=".endTime"]')).toBeNull();
    expect(within(planned).getByDisplayValue('Una prova breve')).toBeTruthy();
  });

  it('keeps Activity intervals and planned Sessions distinct when adding a second interval', () => {
    openAdvanced();
    fireEvent.click(
      screen.getByRole('button', { name: 'Aggiungi intervallo' }),
    );
    expect(
      document.querySelectorAll('[data-create-path="activityIntervals"]'),
    ).toHaveLength(1);
    const actions = plannedSessionActions();
    fireEvent.click(within(actions).getByRole('button', { name: 'Sessione' }));
    expect(
      document.querySelectorAll('[data-create-planned-session]'),
    ).toHaveLength(1);
    expect(
      document.querySelectorAll('[data-create-path="activityIntervals"]'),
    ).toHaveLength(1);
  });
});
