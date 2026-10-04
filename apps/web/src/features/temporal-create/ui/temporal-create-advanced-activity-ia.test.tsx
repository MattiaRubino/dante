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
  it('keeps planned Sessions independent and exposes compact outcome confirmation', () => {
    openAdvanced();

    expect(
      screen.getByRole('heading', { name: 'Riferimento orario' }),
    ).toBeTruthy();
    expect(
      screen.getByRole('heading', { name: 'Pianificazione' }),
    ).toBeTruthy();
    expect(screen.queryByRole('button', { name: 'Realtà' })).toBeNull();
    expect(screen.queryByText('Gestione manuale')).toBeNull();
    expect(screen.getByRole('heading', { name: 'Descrizione' })).toBeTruthy();

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
    expect(
      within(rootOutcome).queryByText('Ricordami alla fine'),
    ).toBeNull();

    fireEvent.click(rootOutcomeCheckbox);
    expect(rootOutcomeCheckbox.checked).toBe(true);
    expect(
      within(rootOutcome).getByRole('radio', { name: 'Ricordami alla fine' }),
    ).toBeTruthy();
    const autoConfirm = within(rootOutcome).getByRole('radio', {
      name: 'Conferma automaticamente',
    }) as HTMLInputElement;
    expect(autoConfirm.checked).toBe(false);
    fireEvent.click(autoConfirm);
    expect(autoConfirm.checked).toBe(true);

    const tree = document.querySelector<HTMLElement>(
      '[data-create-activity-structure]',
    );
    if (!tree) throw new Error('Expected Activity tree.');
    const rootActions = tree.querySelector<HTMLElement>(
      '.temporal-create-activity-tree__root-actions',
    );
    if (!rootActions) throw new Error('Expected root add actions.');
    expect(
      within(rootActions).getByRole('button', { name: 'Sessione' }),
    ).toBeTruthy();
    expect(
      within(rootActions).getByRole('button', { name: 'Sotto-attività' }),
    ).toBeTruthy();
    expect(
      screen.queryByRole('button', { name: 'Aggiungi alla struttura' }),
    ).toBeNull();

    fireEvent.click(
      within(rootActions).getByRole('button', { name: 'Sessione' }),
    );
    expect(screen.getByLabelText('Nome Sessione')).toBeTruthy();
    expect(document.querySelector('[data-create-planned-session]')).toBeTruthy();
    expect(rootCapabilityCheckbox.checked).toBe(false);

    fireEvent.click(
      within(rootActions).getByRole('button', { name: 'Sotto-attività' }),
    );
    const child = document.querySelector<HTMLElement>('[data-create-subactivity]');
    if (!child) throw new Error('Expected Sub-Activity.');
    fireEvent.change(within(child).getByLabelText('Titolo sotto-attività'), {
      target: { value: 'Prima fase' },
    });

    const childCapability = child.querySelector<HTMLElement>(
      '[data-session-capability="sub-activity"]',
    );
    if (!childCapability)
      throw new Error('Expected Sub-Activity Session capability.');
    const childCapabilityCheckbox = within(childCapability).getByRole(
      'checkbox',
    ) as HTMLInputElement;
    expect(childCapabilityCheckbox.checked).toBe(false);

    const childOutcome = child.querySelector<HTMLElement>(
      '[data-outcome-confirmation="sub-activity"]',
    );
    if (!childOutcome)
      throw new Error('Expected Sub-Activity outcome confirmation.');
    const childOutcomeCheckbox = within(childOutcome).getByRole('checkbox', {
      name: 'Conferma esito',
    }) as HTMLInputElement;
    expect(childOutcomeCheckbox.checked).toBe(false);
    expect(within(child).queryByText('Richiesta')).toBeNull();
    expect(within(child).queryByText('Facoltativa')).toBeNull();

    fireEvent.click(childOutcomeCheckbox);
    expect(childOutcomeCheckbox.checked).toBe(true);
    expect(
      within(childOutcome).getByRole('radio', { name: 'Ricordami alla fine' }),
    ).toBeTruthy();
    expect(
      within(childOutcome).getByRole('radio', {
        name: 'Conferma automaticamente',
      }),
    ).toBeTruthy();
    const countsForParent = within(childOutcome).getByRole('checkbox', {
      name: 'Conta per l’esito dell’attività principale',
    }) as HTMLInputElement;
    expect(countsForParent.checked).toBe(true);
    fireEvent.click(countsForParent);
    expect(countsForParent.checked).toBe(false);

    const childTime = within(child).getByRole('button', { name: 'Orario' });
    fireEvent.click(childTime);
    expect(child.querySelector('[data-create-subactivity-time]')).toBeTruthy();

    const childAddSession = within(child).getByRole('button', {
      name: 'Sessione',
    });
    fireEvent.click(childAddSession);
    expect(child.querySelector('[data-create-owner]')).toBeTruthy();
    expect(childCapabilityCheckbox.checked).toBe(false);

    fireEvent.click(rootCapabilityCheckbox);
    fireEvent.click(childCapabilityCheckbox);
    expect(rootCapabilityCheckbox.checked).toBe(true);
    expect(childCapabilityCheckbox.checked).toBe(true);

    expect(screen.queryByRole('button', { name: 'Avvia' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Pausa' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Riprendi' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Termina' })).toBeNull();

    const split = screen.getByRole('button', { name: 'Suddivisa' });
    expect((split as HTMLButtonElement).disabled).toBe(true);

    const protect = screen.getByRole('button', {
      name: 'Proteggi collocazione, da collegare',
    });
    expect((protect as HTMLButtonElement).disabled).toBe(true);

    expect(screen.getByLabelText('Descrizione avanzata')).toBeTruthy();
  });
});
