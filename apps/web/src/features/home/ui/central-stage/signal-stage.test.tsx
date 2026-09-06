import { cleanup, render, screen } from '@testing-library/react';
import { afterAll, afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import { SignalStage } from './signal-stage';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

afterAll(async () => {
  await i18n.changeLanguage('it');
});

describe('SignalStage', () => {
  it('uses the Signals vocabulary and localized Italian accessibility copy', async () => {
    await i18n.changeLanguage('it');
    const { container } = render(<SignalStage />);

    expect(screen.getByRole('region', { name: 'Segnali' })).toBeTruthy();
    expect(
      screen.getByRole('button', { name: 'Segnale precedente' }),
    ).toBeTruthy();
    expect(
      screen.getByRole('button', { name: 'Segnale successivo' }),
    ).toBeTruthy();
    expect(
      screen.getByRole('img', { name: 'Andamento del sonno' }),
    ).toBeTruthy();
    expect(screen.getByText('questa settimana')).toBeTruthy();
    expect(container.querySelector('.home-signal-stage')).toBeTruthy();
    expect(container.querySelector('.home-signal-track')).toBeTruthy();
    expect(container.querySelector('.home-stats-stage')).toBeNull();
    expect(container.querySelector('.home-stats-track')).toBeNull();
  });

  it('renders the same fixture semantics in English without Italian residue', async () => {
    await i18n.changeLanguage('en');
    render(<SignalStage />);

    expect(screen.getByRole('region', { name: 'Signals' })).toBeTruthy();
    expect(
      screen.getByRole('button', { name: 'Previous signal' }),
    ).toBeTruthy();
    expect(screen.getByRole('button', { name: 'Next signal' })).toBeTruthy();
    expect(screen.getByRole('img', { name: 'Sleep trend' })).toBeTruthy();
    expect(screen.getByText('this week')).toBeTruthy();
    expect(screen.getByText('SLEEP')).toBeTruthy();
    expect(screen.getByText('SPEND')).toBeTruthy();
    expect(screen.queryByText('questa settimana')).toBeNull();
    expect(screen.queryByText('SONNO')).toBeNull();
    expect(screen.queryByText('SPESA')).toBeNull();
  });
});
