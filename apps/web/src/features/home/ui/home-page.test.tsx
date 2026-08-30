import {
  cleanup,
  fireEvent,
  render,
  screen,
  within,
} from '@testing-library/react';
import {
  afterAll,
  afterEach,
  beforeAll,
  describe,
  expect,
  it,
  vi,
} from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { HomePage } from './home-page';

beforeAll(async () => {
  vi.stubGlobal(
    'ResizeObserver',
    class ResizeObserverStub {
      observe() {}
      unobserve() {}
      disconnect() {}
    },
  );
  vi.stubGlobal(
    'matchMedia',
    vi.fn().mockImplementation((query: string) => ({
      matches: true,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  );
  vi.stubGlobal('innerWidth', 1440);
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

afterAll(() => {
  vi.unstubAllGlobals();
});

describe('HomePage M1 visual materialization', () => {
  it('keeps Home-owned regions in the real React tree without owning the global app bar', () => {
    const { container } = render(<HomePage />);

    expect(screen.getByRole('main', { name: 'Home DANTE' })).toBeTruthy();
    expect(
      screen.getByRole('region', { name: 'Contesto della giornata' }),
    ).toBeTruthy();

    const homeShell = container.querySelector('[data-home-region="shell"]');
    expect(homeShell?.getAttribute('data-home-visual-source')).toBe('b2-v27');
    expect(container.querySelector('[data-app-region="topbar"]')).toBeNull();

    for (const region of [
      'orientation',
      'ai-surface',
      'central-stage',
      'timeline',
      'context-rail',
    ]) {
      expect(
        container.querySelector(`[data-home-region="${region}"]`),
      ).toBeTruthy();
    }
  });

  it('materializes the accepted DANTE Home instead of an iframe bridge', () => {
    const { container } = render(<HomePage />);

    expect(container.querySelector('iframe')).toBeNull();
    expect(screen.getByText('Ora e prossimo')).toBeTruthy();
    expect(screen.getByText('In evidenza')).toBeTruthy();
    expect(screen.getByText('Per te')).toBeTruthy();
    expect(screen.getAllByText('Corpo').length).toBeGreaterThan(0);
    expect(screen.getByText('Cattura')).toBeTruthy();
    expect(screen.getByText('Da risolvere')).toBeTruthy();
  });

  it('renders the preferred profile name only when an identity is supplied', () => {
    const { rerender } = render(
      <HomePage preferredName="  Mattia   Rubino  " />,
    );

    expect(screen.getByText('Mattia Rubino')).toBeTruthy();

    rerender(<HomePage />);
    expect(screen.queryByText('Mattia Rubino')).toBeNull();
  });

  it('keeps the day context anchored to local today when timeline navigation changes', () => {
    const { container } = render(<HomePage viewedDateIso="2000-01-01" />);
    const dayTitle = container.querySelector(
      '.day-context-trigger-copy > strong',
    );

    expect(dayTitle?.textContent?.startsWith('Oggi · ')).toBe(true);
  });

  it('keeps weekly weather selection local and restores trigger focus on Escape', () => {
    const onViewedDateChange = vi.fn();
    const { container } = render(
      <HomePage onViewedDateChange={onViewedDateChange} />,
    );
    const trigger = container.querySelector(
      '.day-context-trigger',
    ) as HTMLButtonElement;
    const triggerText = trigger.textContent;

    fireEvent.click(trigger);
    const forecast = screen.getByRole('list', {
      name: 'Previsioni per sette giorni',
    });
    const forecastButtons = within(forecast).getAllByRole('button');
    fireEvent.click(forecastButtons[1]!);

    expect(forecastButtons[1]?.getAttribute('aria-current')).toBe('date');
    expect(trigger.textContent).toBe(triggerText);
    expect(onViewedDateChange).not.toHaveBeenCalled();

    fireEvent.keyDown(document, { key: 'Escape' });
    expect(
      screen.queryByRole('region', { name: 'Meteo della settimana' }),
    ).toBeNull();
    expect(document.activeElement).toBe(trigger);
  });

  it('closes the weekly weather disclosure on outside pointer input', () => {
    const { container } = render(<HomePage />);
    const trigger = container.querySelector(
      '.day-context-trigger',
    ) as HTMLButtonElement;

    fireEvent.click(trigger);
    expect(
      screen.getByRole('region', { name: 'Meteo della settimana' }),
    ).toBeTruthy();

    fireEvent.pointerDown(document.body);
    expect(
      screen.queryByRole('region', { name: 'Meteo della settimana' }),
    ).toBeNull();
  });

  it('supports the contracted local AI, stage and timeline states', () => {
    const { container } = render(<HomePage />);
    const shell = container.querySelector('[data-home-region="shell"]');

    expect(shell?.getAttribute('data-home-ai-state')).toBe('expanded');
    expect(shell?.getAttribute('data-home-timeline-state')).toBe('normal');

    fireEvent.click(
      screen.getByRole('button', { name: 'Comprimi assistente' }),
    );
    expect(shell?.getAttribute('data-home-ai-state')).toBe('collapsed');

    const stage = container.querySelector('[data-home-region="central-stage"]');
    const stageScope = within(stage as HTMLElement);
    fireEvent.click(
      stageScope.getByRole('button', { name: 'Proiezione successiva' }),
    );
    expect(stage?.getAttribute('data-home-stage-mode')).toBe('signals');
    expect(stageScope.getByRole('region', { name: 'Sintesi' })).toBeTruthy();
    expect(stageScope.getByText('FOCUS')).toBeTruthy();
    expect(stageScope.getByText('SONNO')).toBeTruthy();
    expect(stageScope.getByText('SPESA')).toBeTruthy();

    fireEvent.click(screen.getByRole('button', { name: 'Espandi timeline' }));
    expect(shell?.getAttribute('data-home-timeline-state')).toBe('expanded');
  });
});
