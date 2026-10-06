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
  it('keeps Activity planning compact and exposes only root capabilities', () => {
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

    const protection = titleRow?.querySelector<HTMLButtonElement>(
      '[data-placement-protection="activity"]',
    );
    if (!protection) throw new Error('Expected placement protection.');

    expect(protection.getAttribute('aria-label')).toBe('Blocca spostamenti');
    expect(protection.getAttribute('aria-pressed')).toBe('false');
    fireEvent.click(protection);
    expect(protection.getAttribute('aria-pressed')).toBe('true');
    expect(protection.getAttribute('aria-label')).toBe('Sblocca spostamenti');

    expect(
      titleRow?.querySelector('[data-reality-policy="activity"]'),
    ).toBeNull();

    const rootReality = document.querySelector<HTMLElement>(
      '[data-reality-policy="activity"]',
    );
    if (!rootReality) throw new Error('Expected Activity occurrence review.');

    const noReview = within(rootReality).getByRole('radio', {
      name: 'Nessuna verifica',
    });
    const askAtEnd = within(rootReality).getByRole('radio', {
      name: 'Chiedi al termine',
    });
    const autoConfirm = within(rootReality).getByRole('radio', {
      name: 'Conferma automatica',
    });

    expect(noReview.getAttribute('aria-checked')).toBe('true');
    fireEvent.click(askAtEnd);
    expect(askAtEnd.getAttribute('aria-checked')).toBe('true');
    fireEvent.click(autoConfirm);
    expect(autoConfirm.getAttribute('aria-checked')).toBe('true');
    expect(screen.getByText('Svolgimento e obiettivi')).toBeTruthy();
    expect(
      screen.getByRole('button', { name: 'Aggiungi obiettivo' }),
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

  it('expands Activity repeat immediately below Ripeti and uses direct ending choices', () => {
    openAdvanced();

    const repeatRow = document.querySelector<HTMLElement>(
      '.temporal-create-u2-repeat',
    );
    const repeatSelect = repeatRow?.querySelector<HTMLSelectElement>('select');
    if (!repeatRow || !repeatSelect) {
      throw new Error('Expected Activity repeat selector.');
    }

    fireEvent.change(repeatSelect, { target: { value: 'custom' } });

    const repeatDetails = document.querySelector<HTMLElement>(
      '[data-create-recurrence-owner="routine"]',
    );
    if (!repeatDetails) throw new Error('Expected Activity repeat details.');

    expect(repeatRow.nextElementSibling).toBe(repeatDetails);
    expect(within(repeatDetails).getByText('Ripetizione')).toBeTruthy();

    const ending = within(repeatDetails).getByRole('radiogroup', {
      name: 'Fine ripetizione',
    });
    expect(within(ending).getByRole('radio', { name: 'Mai' })).toBeTruthy();
    expect(within(ending).getByRole('radio', { name: 'Data' })).toBeTruthy();

    const after = within(ending).getByRole('radio', { name: 'Dopo' });
    fireEvent.click(after);

    expect(within(ending).getByLabelText('Numero di occorrenze')).toBeTruthy();
    expect(within(ending).getByText('occorrenze')).toBeTruthy();
    expect(within(ending).queryByText('Dopo un numero di volte')).toBeNull();
  });
});
