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

describe('Home World Focus entry', () => {
  it('opens only when the selected World is activated again', () => {
    const onOpenWorldFocus = vi.fn();
    render(<HomePage onOpenWorldFocus={onOpenWorldFocus} />);

    const music = screen.getByRole('listitem', { name: 'Musica' });

    fireEvent.click(music);
    expect(onOpenWorldFocus).not.toHaveBeenCalled();
    expect(music.getAttribute('aria-current')).toBe('true');

    fireEvent.click(music);
    expect(onOpenWorldFocus).toHaveBeenCalledTimes(1);
    expect(onOpenWorldFocus).toHaveBeenCalledWith({
      label: 'Musica',
      origin: {
        left: expect.any(Number),
        top: expect.any(Number),
        width: expect.any(Number),
        height: expect.any(Number),
      },
    });
  });
});
