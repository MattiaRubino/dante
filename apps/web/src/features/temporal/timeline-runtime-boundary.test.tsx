import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
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
    const source: TemporalTimelineDataSource = {
      loadWindow: vi.fn(() => pending.promise),
    };
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
    expect(source.loadWindow).toHaveBeenCalledTimes(1);

    await act(async () => pending.resolve(emptyWindow()));

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
    const source: TemporalTimelineDataSource = {
      loadWindow: vi.fn(() => Promise.reject(new Error('offline'))),
    };

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
    const source: TemporalTimelineDataSource = {
      loadWindow: vi
        .fn()
        .mockImplementationOnce(() => first.promise)
        .mockImplementationOnce(() => Promise.resolve(emptyWindow())),
    };

    render(
      <TemporalTimelineRuntimeBoundary
        viewedDateIso="2026-09-04"
        dataSource={source}
        mode="production"
      >
        <div>product-shell</div>
      </TemporalTimelineRuntimeBoundary>,
    );

    await act(async () => first.reject(new Error('offline')));
    expect(await screen.findByRole('alert')).toBeTruthy();
    expect(source.loadWindow).toHaveBeenCalledTimes(1);

    fireEvent.click(screen.getByRole('button', { name: 'Riprova' }));

    await waitFor(() => {
      expect(source.loadWindow).toHaveBeenCalledTimes(2);
      expect(screen.queryByRole('alert')).toBeNull();
    });
  });

  it('keeps frozen UI regression tests explicitly outside the real transport path', () => {
    const source: TemporalTimelineDataSource = {
      loadWindow: vi.fn(() => Promise.resolve(emptyWindow())),
    };

    render(
      <TemporalTimelineRuntimeBoundary dataSource={source} mode="test">
        <div>fixture-product-shell</div>
      </TemporalTimelineRuntimeBoundary>,
    );

    expect(screen.getByText('fixture-product-shell')).toBeTruthy();
    expect(screen.queryByRole('status')).toBeNull();
    expect(screen.queryByRole('alert')).toBeNull();
    expect(source.loadWindow).not.toHaveBeenCalled();
  });
});
