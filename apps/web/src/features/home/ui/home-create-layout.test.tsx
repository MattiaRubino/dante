import { cleanup, fireEvent, render } from '@testing-library/react';
import { afterAll, afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { HomePage } from './home-page';
import { TIMELINE_POLICY } from './timeline/model/timeline-policy';

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

describe('Home U1 Create rail contract', () => {
  it('keeps Timeline and Context Rail as H0 siblings and reserves Create inside the rail', () => {
    const { container } = render(<HomePage />);
    const today = container.querySelector('[data-home-layout="today"]');
    const timeline = container.querySelector('[data-home-region="timeline"]');
    const rail = container.querySelector('[data-home-region="context-rail"]');
    const createHost = container.querySelector('[data-home-context-create-host]');

    expect(TIMELINE_POLICY.expansion.defaultContextRailWidthPx).toBe(475);
    expect(today).not.toBeNull();
    expect(timeline).not.toBeNull();
    expect(rail).not.toBeNull();
    expect(createHost).not.toBeNull();
    expect(today?.contains(timeline)).toBe(true);
    expect(today?.contains(rail)).toBe(true);
    expect(timeline?.contains(rail)).toBe(false);
    expect(rail?.contains(timeline)).toBe(false);
    expect(rail?.contains(createHost)).toBe(true);
    expect(rail?.querySelectorAll(':scope > section')).toHaveLength(2);
  });

  it('mounts Create in the Context Rail and restores the closed state for an untouched draft', () => {
    const { container } = render(<HomePage />);
    const quickAdd = container.querySelector<HTMLButtonElement>(
      '.dante-timeline-quick-add',
    );
    const rail = container.querySelector<HTMLElement>(
      '[data-home-region="context-rail"]',
    );
    const createHost = container.querySelector<HTMLElement>(
      '[data-home-context-create-host]',
    );

    if (!quickAdd || !rail || !createHost) {
      throw new Error('Expected U1 Home Create contract nodes.');
    }

    expect(quickAdd.disabled).toBe(false);
    expect(quickAdd.getAttribute('aria-expanded')).toBe('false');
    fireEvent.click(quickAdd);

    const composer = createHost.querySelector(
      '[data-temporal-create="composer"]',
    );
    const backdrop = createHost.querySelector<HTMLElement>(
      '[data-temporal-create="backdrop"]',
    );
    expect(composer).not.toBeNull();
    expect(backdrop).not.toBeNull();
    expect(rail.contains(composer)).toBe(true);
    expect(quickAdd.getAttribute('aria-expanded')).toBe('true');

    if (!backdrop) {
      throw new Error('Expected Create backdrop.');
    }
    fireEvent.pointerDown(backdrop);

    expect(quickAdd.getAttribute('aria-expanded')).toBe('false');
    expect(
      createHost.querySelector('[data-temporal-create="composer"]'),
    ).toBeNull();
  });
});
