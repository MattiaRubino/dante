import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import type { WorldFocusContinuityReader } from '../application/world-focus-continuity';
import type { WorldFocusContinuityReadResult } from '../model/world-focus-continuity';
import type { WorldFocusId } from '../model/world-focus-identity';
import { WorldFocusContinuity } from './world-focus-continuity';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

function readyResult(
  worldId: WorldFocusId,
  title: string,
): Extract<WorldFocusContinuityReadResult, Readonly<{ status: 'ready' }>> {
  return {
    status: 'ready',
    projection: {
      schemaVersion: 1,
      worldId,
      orderedItems: [
        {
          key: `${worldId}-item`,
          title,
          context: 'Project',
          checkpoint: 'Checkpoint',
          threadReference: { kind: 'project', key: `${worldId}-thread` },
          checkpointReference: {
            kind: 'checkpoint',
            key: `${worldId}-checkpoint`,
          },
          continuationReference: null,
          presentationState: 'active',
        },
      ],
    },
  };
}

function deferred<Value>() {
  let resolve!: (value: Value) => void;
  let reject!: (reason?: unknown) => void;
  const promise = new Promise<Value>((resolvePromise, rejectPromise) => {
    resolve = resolvePromise;
    reject = rejectPromise;
  });
  return { promise, resolve, reject };
}

describe('World Focus B2 Continuity UI', () => {
  it('renders ordered source-backed continuity through the shared M2 grammar without inventing a Resume CTA', async () => {
    render(<WorldFocusContinuity worldId="music" />);

    expect(await screen.findByText('Neon Static')).toBeTruthy();
    expect(screen.getByText('Master v3')).toBeTruthy();
    expect(screen.getByText('Attivo')).toBeTruthy();
    expect(
      document.querySelector(
        '.world-focus-continuity[data-world-focus-presentation="section"]',
      ),
    ).toBeTruthy();
    expect(
      document.querySelector(
        '.world-focus-continuity [data-world-focus-state="active"]',
      ),
    ).toBeTruthy();
    expect(screen.queryByRole('button', { name: /riprendi/i })).toBeNull();
  });

  it('omits the section for a genuinely empty World', async () => {
    render(<WorldFocusContinuity worldId="finance" />);

    await waitFor(() => {
      expect(
        screen.queryByRole('heading', { name: 'In movimento' }),
      ).toBeNull();
    });
  });

  it('keeps partial and stale data visible with truthful qualification', async () => {
    const partialReader: WorldFocusContinuityReader = () =>
      Promise.resolve({
        status: 'partial',
        projection: readyResult('music', 'Partial thread').projection,
        reasonCode: 'source-partial',
      });
    const { rerender } = render(
      <WorldFocusContinuity worldId="music" reader={partialReader} />,
    );

    expect(await screen.findByText('Partial thread')).toBeTruthy();
    expect(
      screen.getByText(
        'Alcune informazioni di continuità non sono disponibili.',
      ),
    ).toBeTruthy();

    const staleReader: WorldFocusContinuityReader = () =>
      Promise.resolve({
        status: 'stale',
        projection: readyResult('music', 'Stale thread').projection,
        asOf: '2026-09-01T08:00:00Z',
      });
    rerender(<WorldFocusContinuity worldId="music" reader={staleReader} />);

    expect(await screen.findByText('Stale thread')).toBeTruthy();
    expect(
      screen.getByText('Questa vista usa informazioni non aggiornate.'),
    ).toBeTruthy();
  });

  it('contains unexpected failures locally and retries with a new read', async () => {
    let attempt = 0;
    const reader: WorldFocusContinuityReader = () => {
      attempt += 1;
      return attempt === 1
        ? Promise.reject(new Error('private-adapter-detail'))
        : Promise.resolve(readyResult('music', 'Recovered thread'));
    };

    render(<WorldFocusContinuity worldId="music" reader={reader} />);

    expect(
      await screen.findByText(
        'Non riesco a recuperare ciò che è in movimento.',
      ),
    ).toBeTruthy();
    expect(screen.queryByText('private-adapter-detail')).toBeNull();

    fireEvent.click(screen.getByRole('button', { name: 'Riprova' }));
    expect(await screen.findByText('Recovered thread')).toBeTruthy();
    expect(attempt).toBe(2);
  });

  it('does not let a late result from the previous World overwrite the active one', async () => {
    const music = deferred<WorldFocusContinuityReadResult>();
    const travel = deferred<WorldFocusContinuityReadResult>();
    const readerMock = vi.fn((worldId: WorldFocusId) =>
      worldId === 'music' ? music.promise : travel.promise,
    );
    const reader: WorldFocusContinuityReader = readerMock;

    const { rerender } = render(
      <WorldFocusContinuity worldId="music" reader={reader} />,
    );
    await waitFor(() => expect(readerMock).toHaveBeenCalledTimes(1));

    rerender(<WorldFocusContinuity worldId="travel" reader={reader} />);
    await waitFor(() => expect(readerMock).toHaveBeenCalledTimes(2));

    music.resolve(readyResult('music', 'Late music thread'));
    travel.resolve(readyResult('travel', 'Japan 2027'));

    expect(await screen.findByText('Japan 2027')).toBeTruthy();
    expect(screen.queryByText('Late music thread')).toBeNull();
  });
});
