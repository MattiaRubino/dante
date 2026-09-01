import { createElement, type PropsWithChildren } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { act, cleanup, renderHook } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { webAuthRemote } from '../../../platform/auth/web-auth-remote';
import {
  authenticationMethodsQueryKey,
  useEstablishPasswordMutation,
  useRemovePasswordMutation,
} from './auth-methods';
import { authSessionQueryKey } from './auth-session';

const authenticatedSession = {
  authenticated: true as const,
  account_ref: '00000000-0000-4000-8000-000000000001',
  auth_session_ref: '00000000-0000-4000-8000-000000000002',
  recent_auth_at: '2026-09-01T20:00:00Z',
  expires_at: '2026-10-01T20:00:00Z',
  csrf_token: 'rotated-csrf-token',
};

function createHarness() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });

  function Wrapper({ children }: PropsWithChildren) {
    return createElement(QueryClientProvider, { client: queryClient }, children);
  }

  return { queryClient, Wrapper };
}

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe('Authentication methods application mutations', () => {
  it('establishes a password with the current CSRF token, rotates session cache, and invalidates method state', async () => {
    const establishSpy = vi
      .spyOn(webAuthRemote, 'establishPassword')
      .mockResolvedValue(authenticatedSession);
    const { queryClient, Wrapper } = createHarness();
    const invalidateSpy = vi.spyOn(queryClient, 'invalidateQueries');
    const { result } = renderHook(() => useEstablishPasswordMutation(), {
      wrapper: Wrapper,
    });

    await act(async () => {
      await result.current.mutateAsync({
        newPassword: 'correct horse battery staple',
        csrfToken: 'current-csrf-token',
      });
    });

    expect(establishSpy).toHaveBeenCalledWith(
      { new_password: 'correct horse battery staple' },
      'current-csrf-token',
    );
    expect(queryClient.getQueryData(authSessionQueryKey)).toEqual(
      authenticatedSession,
    );
    expect(invalidateSpy).toHaveBeenCalledWith({
      queryKey: authenticationMethodsQueryKey,
    });
  });

  it('removes a password through the governed mutation and refreshes both session and methods caches', async () => {
    const removeSpy = vi
      .spyOn(webAuthRemote, 'removePassword')
      .mockResolvedValue(authenticatedSession);
    const { queryClient, Wrapper } = createHarness();
    const invalidateSpy = vi.spyOn(queryClient, 'invalidateQueries');
    const { result } = renderHook(() => useRemovePasswordMutation(), {
      wrapper: Wrapper,
    });

    await act(async () => {
      await result.current.mutateAsync({ csrfToken: 'current-csrf-token' });
    });

    expect(removeSpy).toHaveBeenCalledWith('current-csrf-token');
    expect(queryClient.getQueryData(authSessionQueryKey)).toEqual(
      authenticatedSession,
    );
    expect(invalidateSpy).toHaveBeenCalledWith({
      queryKey: authenticationMethodsQueryKey,
    });
  });
});
