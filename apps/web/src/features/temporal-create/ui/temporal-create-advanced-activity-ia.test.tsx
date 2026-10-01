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
  it('shows the new Activity workspace without exposing unsupported authoring as editable truth', () => {
    openAdvanced();

    expect(screen.getByRole('heading', { name: 'Riferimento orario' })).toBeTruthy();
    expect(screen.getByRole('heading', { name: 'Struttura' })).toBeTruthy();
    expect(screen.getByRole('heading', { name: 'Pianificazione' })).toBeTruthy();
    expect(screen.getByRole('heading', { name: 'Esecuzione' })).toBeTruthy();
    expect(screen.getByRole('heading', { name: 'Realtà ed esito' })).toBeTruthy();
    expect(screen.getByRole('heading', { name: 'Verifica esito' })).toBeTruthy();
    expect(screen.getByRole('heading', { name: 'Descrizione' })).toBeTruthy();

    expect(screen.queryByRole('heading', { name: 'Organizzazione' })).toBeNull();

    const split = screen.getByRole('button', { name: 'Suddivisa' });
    expect((split as HTMLButtonElement).disabled).toBe(true);

    const protect = screen.getByRole('button', {
      name: 'Proteggi collocazione, da collegare',
    });
    expect((protect as HTMLButtonElement).disabled).toBe(true);

    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi' }));
    const structureMenu = screen.getByRole('menu', {
      name: 'Aggiungi alla struttura',
    });
    expect(
      (within(structureMenu).getByRole('menuitem', {
        name: /Sotto-attività/,
      }) as HTMLButtonElement).disabled,
    ).toBe(true);
    expect(
      (within(structureMenu).getByRole('menuitem', {
        name: /Sessione/,
      }) as HTMLButtonElement).disabled,
    ).toBe(true);

    expect(screen.getByLabelText('Descrizione avanzata')).toBeTruthy();
  });
});