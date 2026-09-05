import { cleanup, fireEvent, render, screen } from '@testing-library/react';
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
import type { HomeWorldOpenIntent } from '../model/home-world-focus';
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

function pointerActivate(element: HTMLElement, pointerId = 1) {
  fireEvent.pointerDown(element, {
    pointerId,
    pointerType: 'mouse',
    button: 0,
    clientX: 100,
    clientY: 100,
  });
  fireEvent.pointerUp(element, {
    pointerId,
    pointerType: 'mouse',
    button: 0,
    clientX: 100,
    clientY: 100,
  });
}

describe('Home World Focus entry', () => {
  it('uses a stable two-activation gesture instead of native dblclick', () => {
    const onOpenWorldFocus = vi.fn<(intent: HomeWorldOpenIntent) => void>();
    render(<HomePage onOpenWorldFocus={onOpenWorldFocus} />);

    const music = screen.getByRole('listitem', { name: 'Musica' });

    pointerActivate(music, 1);
    expect(onOpenWorldFocus).not.toHaveBeenCalled();
    expect(music.getAttribute('aria-current')).toBe('true');

    pointerActivate(music, 2);
    expect(onOpenWorldFocus).toHaveBeenCalledTimes(1);

    const intent = onOpenWorldFocus.mock.calls[0]?.[0];
    expect(intent).toBeDefined();
    if (intent === undefined) {
      throw new Error('Expected a World Focus open intent');
    }

    expect(intent.label).toBe('Musica');
    expect(Number.isFinite(intent.origin.left)).toBe(true);
    expect(Number.isFinite(intent.origin.top)).toBe(true);
    expect(Number.isFinite(intent.origin.width)).toBe(true);
    expect(Number.isFinite(intent.origin.height)).toBe(true);
  });

  it('does not open the initially centered World on the first activation', () => {
    const onOpenWorldFocus = vi.fn<(intent: HomeWorldOpenIntent) => void>();
    render(<HomePage onOpenWorldFocus={onOpenWorldFocus} />);

    const body = screen.getByRole('listitem', { name: 'Corpo' });
    expect(body.getAttribute('aria-current')).toBe('true');

    pointerActivate(body, 1);
    expect(onOpenWorldFocus).not.toHaveBeenCalled();

    pointerActivate(body, 2);
    expect(onOpenWorldFocus).toHaveBeenCalledTimes(1);
  });

  it('keeps keyboard activation on the same select-first/open-second contract', () => {
    const onOpenWorldFocus = vi.fn<(intent: HomeWorldOpenIntent) => void>();
    render(<HomePage onOpenWorldFocus={onOpenWorldFocus} />);

    const music = screen.getByRole('listitem', { name: 'Musica' });

    fireEvent.click(music, { detail: 0 });
    expect(music.getAttribute('aria-current')).toBe('true');
    expect(onOpenWorldFocus).not.toHaveBeenCalled();

    fireEvent.click(music, { detail: 0 });
    expect(onOpenWorldFocus).toHaveBeenCalledTimes(1);
  });
});
