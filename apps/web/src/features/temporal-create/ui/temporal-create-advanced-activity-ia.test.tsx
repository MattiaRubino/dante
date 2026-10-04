// @vitest-environment jsdom

import { Temporal } from '@dante/time';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { TemporalCreateEntry } from './temporal-create-entry';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

function openAdvanced() {
  const rendered = render(
    <>
      <div data-home-context-create-host />
      <TemporalCreateEntry
        defaultDate={Temporal.PlainDate.from('2026-10-01')}
        contexts={[
          {
            id: 'personale',
            label: 'Personale',
            tone: 'personal',
          },
        ]}
        onPreview={() => undefined}
        onApplied={() => false}
        creationEnabled={false}
      />
    </>,
  );

  const quickAdd = rendered.container.querySelector<HTMLButtonElement>(
    '.dante-timeline-quick-add',
  );
  if (!quickAdd) throw new Error('Expected Create trigger.');
  fireEvent.click(quickAdd);
  fireEvent.change(screen.getByPlaceholderText('Titolo'), {
    target: { value: 'Scrivere articolo' },
  });
  fireEvent.click(screen.getByRole('button', { name: /Opzioni avanzate/ }));
}

describe('Temporal Create Advanced Activity IA', () => {
  it('keeps Activity planning compact and does not expose Sub-Activities', () => {
    openAdvanced();

    const title = screen.getByPlaceholderText('Titolo');
    const titleRow = title.closest('.temporal-create-title-row');
    expect(titleRow).toBeTruthy();

    const rootCapability = titleRow?.querySelector<HTMLElement>(
      '[data-session-capability="activity"]',
    );
    if (!rootCapability) throw new Error('Expected root Session capability.');
    const rootCapabilityCheckbox = within(rootCapability).getByRole(
      'checkbox',
    ) as HTMLInputElement;
    expect(rootCapabilityCheckbox.checked).toBe(false);

    const rootOutcome = titleRow?.querySelector<HTMLElement>(
      '[data-outcome-confirmation="activity"]',
    );
    if (!rootOutcome) throw new Error('Expected root outcome confirmation.');
    const rootOutcomeCheckbox = within(rootOutcome).getByRole('checkbox', {
      name: 'Conferma esito',
    }) as HTMLInputElement;
    expect(rootOutcomeCheckbox.checked).toBe(false);

    fireEvent.click(rootOutcomeCheckbox);
    expect(
      within(rootOutcome).getByRole('radio', { name: 'Ricordami alla fine' }),
    ).toBeTruthy();
    expect(
      within(rootOutcome).getByRole('radio', {
        name: 'Conferma automaticamente',
      }),
    ).toBeTruthy();

    const tree = document.querySelector<HTMLElement>(
      '[data-create-activity-structure]',
    );
    if (!tree) throw new Error('Expected Activity planning tree.');
    const rootActions = tree.querySelector<HTMLElement>(
      '.temporal-create-activity-tree__root-actions',
    );
    if (!rootActions) throw new Error('Expected root add actions.');

    expect(
      within(rootActions).getByRole('button', { name: 'Sessione' }),
    ).toBeTruthy();
    expect(
      screen.queryByRole('button', { name: 'Sotto-attività' }),
    ).toBeNull();
    expect(document.querySelector('[data-create-subactivity]')).toBeNull();

    fireEvent.click(
      within(rootActions).getByRole('button', { name: 'Sessione' }),
    );
    expect(screen.getByLabelText('Nome Sessione')).toBeTruthy();
    expect(document.querySelector('[data-create-planned-session]')).toBeTruthy();
    expect(rootCapabilityCheckbox.checked).toBe(false);

    fireEvent.click(rootCapabilityCheckbox);
    expect(rootCapabilityCheckbox.checked).toBe(true);

    expect(
      screen.queryByRole('button', {
        name: 'Proteggi collocazione, da collegare',
      }),
    ).toBeNull();

    expect(screen.queryByRole('button', { name: 'Avvia' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Pausa' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Riprendi' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Termina' })).toBeNull();
  });
});
