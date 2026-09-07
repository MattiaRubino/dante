import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../bootstrap/i18n';
import type {
  TemporalTimelineDataSource,
  TemporalTimelineWindow,
} from './timeline-read';
import { TemporalTimelineRuntimeBoundary } from './timeline-runtime-boundary';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

function deferred<T>() {
  let resolve!: (value: T) => void;
  let reject!: (reason?: unknown) => void;
  const promise = new Promise<T>((resolvePromise, rejectPromise) => {
    resolve = resolvePromise;
    reject = rejectPromise;
  });
  return { promise, resolve, reject };
}

function emptyWindow(): TemporalTimelineWindow {
  return {
    kind: 'empty',
    startDate: '2026-08-28',
    endDateExclusive: '2026-10-10',
    effectiveZoneId: 'Europe/Rome',
  };
}

describe('TemporalTimelineRuntimeBoundary', () => {
  it('keeps the product visible while truthfully exposing an in-flight real read', async () => {
    const pending = deferred<TemporalTimelineWindow>();
    const loadWindow = vi.fn<TemporalTimelineDataSource['loadWindow']>(
      () => pending.promise,
    );
    const source: TemporalTimelineDataSource = { loadWindow };
    const { container } = render(
      <TemporalTimelineRuntimeBoundary
        viewedDateIso="2026-09-04"
        dataSource={source}
        mode="production"
      >
        <div>product-shell</div>
      </TemporalTimelineRuntimeBoundary>,
    );

    expect(screen.getByText('product-shell')).toBeTruthy();
    expect(screen.getByRole('status').textContent).toContain(
      'Caricamento timeline',
    );
    expect(loadWindow).toHaveBeenCalledTimes(1);

    await act(async () => {
      pending.resolve(emptyWindow());
      await pending.promise;
    });

    await waitFor(() => {
      expect(screen.queryByRole('status')).toBeNull();
    });
    expect(
      container.querySelector('[data-temporal-read-state="ready"]'),
    ).toBeTruthy();
    expect(
      container
        .querySelector('[data-temporal-read-state="ready"]')
        ?.getAttribute('data-temporal-effective-zone'),
    ).toBe('Europe/Rome');
  });

  it('surfaces backend failure instead of replacing it with fake Timeline success', async () => {
    const loadWindow = vi.fn<TemporalTimelineDataSource['loadWindow']>(() =>
      Promise.reject(new Error('offline')),
    );
    const source: TemporalTimelineDataSource = { loadWindow };

    render(
      <TemporalTimelineRuntimeBoundary
        viewedDateIso="2026-09-04"
        dataSource={source}
        mode="production"
      >
        <div>product-shell</div>
      </TemporalTimelineRuntimeBoundary>,
    );

    const alert = await screen.findByRole('alert');
    expect(alert.textContent).toContain('Timeline non disponibile');
    expect(alert.textContent).toContain('Nessun dato finto');
    expect(screen.getByText('product-shell')).toBeTruthy();
  });

  it('retries the same governed read only after an explicit user retry', async () => {
    const first = deferred<TemporalTimelineWindow>();
    const loadWindow = vi
      .fn<TemporalTimelineDataSource['loadWindow']>()
      .mockImplementationOnce(() => first.promise)
      .mockImplementationOnce(() => Promise.resolve(emptyWindow()));
    const source: TemporalTimelineDataSource = { loadWindow };

    render(
      <TemporalTimelineRuntimeBoundary
        viewedDateIso="2026-09-04"
        dataSource={source}
        mode="production"
      >
        <div>product-shell</div>
      </TemporalTimelineRuntimeBoundary>,
    );

    await act(async () => {
      first.reject(new Error('offline'));
      await first.promise.catch(() => undefined);
    });
    expect(await screen.findByRole('alert')).toBeTruthy();
    expect(loadWindow).toHaveBeenCalledTimes(1);

    fireEvent.click(screen.getByRole('button', { name: 'Riprova' }));

    await waitFor(() => {
      expect(loadWindow).toHaveBeenCalledTimes(2);
      expect(screen.queryByRole('alert')).toBeNull();
    });
  });

  it('keeps frozen UI regression tests explicitly outside the real transport path', () => {
    const loadWindow = vi.fn<TemporalTimelineDataSource['loadWindow']>(() =>
      Promise.resolve(emptyWindow()),
    );
    const source: TemporalTimelineDataSource = { loadWindow };

    render(
      <TemporalTimelineRuntimeBoundary dataSource={source} mode="test">
        <div>fixture-product-shell</div>
      </TemporalTimelineRuntimeBoundary>,
    );

    expect(screen.getByText('fixture-product-shell')).toBeTruthy();
    expect(screen.queryByRole('status')).toBeNull();
    expect(screen.queryByRole('alert')).toBeNull();
    expect(loadWindow).not.toHaveBeenCalled();
  });
});
