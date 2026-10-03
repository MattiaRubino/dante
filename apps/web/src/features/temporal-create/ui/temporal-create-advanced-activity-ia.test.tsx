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
  it('keeps the Activity tree under the title and writes Session execution intent', () => {
    openAdvanced();

    expect(
      screen.getByRole('heading', { name: 'Riferimento orario' }),
    ).toBeTruthy();
    expect(
      screen.getByRole('heading', { name: 'Pianificazione' }),
    ).toBeTruthy();
    const reality = screen.getByRole('button', { name: 'Realtà' });
    expect(reality.closest('.temporal-create-title-row')).toBeTruthy();
    fireEvent.click(reality);
    expect(
      screen.getByRole('heading', { name: 'Verifica esito' }),
    ).toBeTruthy();
    expect(screen.getByRole('heading', { name: 'Descrizione' })).toBeTruthy();

    expect(screen.queryByRole('heading', { name: 'Struttura' })).toBeNull();
    expect(
      screen.queryByRole('heading', { name: 'Organizzazione' }),
    ).toBeNull();

    const title = screen.getByPlaceholderText('Titolo');
    expect(title.closest('.temporal-create-title-row')).toBeTruthy();
    expect(
      document.querySelector('[data-create-activity-structure]'),
    ).toBeTruthy();
    expect(
      document.querySelector('[data-create-structure-actions]'),
    ).toBeTruthy();

    fireEvent.click(
      screen.getByRole('button', { name: 'Aggiungi alla struttura' }),
    );
    const structureMenu = screen.getByRole('menu', {
      name: 'Aggiungi alla struttura',
    });
    const addChild = within(structureMenu).getByRole('menuitem', {
      name: 'Sotto-attività',
    }) as HTMLButtonElement;
    expect(addChild.disabled).toBe(false);
    fireEvent.click(addChild);
    expect(document.querySelector('[data-create-subactivity]')).toBeTruthy();
    fireEvent.change(screen.getByLabelText('Titolo sotto-attività'), {
      target: { value: 'Prima fase' },
    });
    fireEvent.click(
      screen.getByRole('button', { name: 'Aggiungi alla struttura' }),
    );

    const addSession = within(
      screen.getByRole('menu', { name: 'Aggiungi alla struttura' }),
    ).getByRole('menuitem', {
      name: 'Sessione',
    }) as HTMLButtonElement;
    expect(addSession.disabled).toBe(false);
    fireEvent.click(addSession);

    const sessionToggle = document.querySelector(
      '[data-create-structure-actions]',
    );
    if (!sessionToggle)
      throw new Error('Expected Session control beside the title.');
    expect(
      (
        within(sessionToggle as HTMLElement).getByRole(
          'checkbox',
        ) as HTMLInputElement
      ).checked,
    ).toBe(true);
    expect(
      document.querySelector('[data-create-structure-session]'),
    ).toBeNull();
    expect(
      document.querySelector(
        '[data-create-path="execution.minSessionMinutes"]',
      ),
    ).toBeNull();

    expect(screen.queryByRole('button', { name: 'Avvia' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Pausa' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Riprendi' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Termina' })).toBeNull();

    fireEvent.click(within(sessionToggle as HTMLElement).getByRole('checkbox'));
    expect(
      (
        within(sessionToggle as HTMLElement).getByRole(
          'checkbox',
        ) as HTMLInputElement
      ).checked,
    ).toBe(false);

    const split = screen.getByRole('button', { name: 'Suddivisa' });
    expect((split as HTMLButtonElement).disabled).toBe(true);

    const protect = screen.getByRole('button', {
      name: 'Proteggi collocazione, da collegare',
    });
    expect((protect as HTMLButtonElement).disabled).toBe(true);

    expect(screen.getByLabelText('Descrizione avanzata')).toBeTruthy();
  });
});
