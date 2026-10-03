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
  it('renders a bounded Activity tree with root actions at the bottom', () => {
    openAdvanced();

    expect(
      screen.getByRole('heading', { name: 'Riferimento orario' }),
    ).toBeTruthy();
    expect(
      screen.getByRole('heading', { name: 'Pianificazione' }),
    ).toBeTruthy();
    const reality = screen.getByRole('button', { name: 'Realtà' });
    expect(reality.closest('.temporal-create-title-row')).toBeTruthy();
    expect(screen.getByRole('heading', { name: 'Descrizione' })).toBeTruthy();

    const title = screen.getByPlaceholderText('Titolo');
    expect(title.closest('.temporal-create-title-row')).toBeTruthy();

    const tree = document.querySelector<HTMLElement>(
      '[data-create-activity-structure]',
    );
    if (!tree) throw new Error('Expected Activity tree.');
    const rootActions = tree.querySelector<HTMLElement>(
      '.temporal-create-activity-tree__root-actions',
    );
    if (!rootActions) throw new Error('Expected root add actions.');
    expect(within(rootActions).getByRole('button', { name: 'Sessione' })).toBeTruthy();
    expect(
      within(rootActions).getByRole('button', { name: 'Sotto-attività' }),
    ).toBeTruthy();
    expect(screen.queryByRole('button', { name: 'Aggiungi alla struttura' })).toBeNull();

    fireEvent.click(within(rootActions).getByRole('button', { name: 'Sessione' }));
    expect(screen.getByLabelText('Nome Sessione')).toBeTruthy();
    expect(document.querySelector('[data-create-planned-session]')).toBeTruthy();

    fireEvent.click(
      within(rootActions).getByRole('button', { name: 'Sotto-attività' }),
    );
    const child = document.querySelector<HTMLElement>('[data-create-subactivity]');
    if (!child) throw new Error('Expected Sub-Activity.');
    fireEvent.change(within(child).getByLabelText('Titolo sotto-attività'), {
      target: { value: 'Prima fase' },
    });

    const childTime = within(child).getByRole('button', { name: 'Orario' });
    fireEvent.click(childTime);
    expect(
      child.querySelector('[data-create-subactivity-time]'),
    ).toBeTruthy();

    const childAddSession = within(child).getByRole('button', {
      name: 'Sessione',
    });
    fireEvent.click(childAddSession);
    expect(child.querySelector('[data-create-owner]')).toBeTruthy();

    const sessionToggle = document.querySelector(
      '[data-create-structure-actions]',
    );
    if (!sessionToggle)
      throw new Error('Expected Session control beside the title.');
    expect(
      (
        within(sessionToggle as HTMLElement).getByRole('checkbox') as HTMLInputElement
      ).checked,
    ).toBe(true);

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
