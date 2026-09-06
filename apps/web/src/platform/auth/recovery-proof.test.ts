import { describe, expect, it, vi } from 'vitest';

import { captureRecoveryProof } from './recovery-proof';

const RECOVERY_REF = '019d0000-0000-7000-8000-000000000004';

function location(search: string, hash: string) {
  return { pathname: '/', search, hash } as Pick<
    Location,
    'pathname' | 'search' | 'hash'
  >;
}

function history() {
  return {
    state: { preserved: true },
    replaceState: vi.fn(),
  } as unknown as Pick<History, 'state' | 'replaceState'>;
}

describe('recovery proof bootstrap boundary', () => {
  it('captures a valid UUIDv7 proof, scrubs the fragment, then clears the recovery handle', () => {
    const browserHistory = history();
    const store = captureRecoveryProof(
      location(`?recovery=${RECOVERY_REF}&lang=it`, '#high-entropy-secret'),
      browserHistory,
    );

    expect(store.peek()).toEqual({
      password_recovery_ref: RECOVERY_REF,
      secret: 'high-entropy-secret',
    });
    expect(browserHistory.replaceState).toHaveBeenNthCalledWith(
      1,
      { preserved: true },
      '',
      `/?recovery=${RECOVERY_REF}&lang=it`,
    );

    store.clear();
    expect(store.peek()).toBeNull();
    expect(browserHistory.replaceState).toHaveBeenNthCalledWith(
      2,
      { preserved: true },
      '',
      '/?lang=it',
    );
  });

  it('scrubs malformed or ambiguous recovery fragments without retaining a bearer', () => {
    const browserHistory = history();
    const store = captureRecoveryProof(
      location(`?recovery=${RECOVERY_REF}&recovery=${RECOVERY_REF}`, '#secret'),
      browserHistory,
    );

    expect(store.peek()).toBeNull();
    expect(browserHistory.replaceState).toHaveBeenCalledOnce();
  });

  it('does not erase unrelated application fragments or query parameters', () => {
    const browserHistory = history();
    const store = captureRecoveryProof(
      location('?lang=it', '#settings'),
      browserHistory,
    );

    expect(store.peek()).toBeNull();
    expect(browserHistory.replaceState).not.toHaveBeenCalled();

    store.clear();
    expect(browserHistory.replaceState).not.toHaveBeenCalled();
  });
});
