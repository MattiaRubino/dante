import { describe, expect, it } from 'vitest';

import {
  DANTE_TIME_ZONE_HEADER_NAME,
  WEB_CLIENT_HEADER_NAME,
  createWebFetch,
} from './web-fetch';

describe('governed Web transport', () => {
  it('adds same-origin credentials, client proof and current device timezone', async () => {
    let captured: RequestInit | undefined;
    const fetchFn: typeof globalThis.fetch = (_input, init) => {
      captured = init;
      return Promise.resolve(new Response(null, { status: 204 }));
    };

    const webFetch = createWebFetch(fetchFn, () => 'Europe/Rome');
    await webFetch('/api/v1/example', {
      method: 'GET',
      headers: { 'X-Existing': 'value' },
    });

    expect(captured?.credentials).toBe('same-origin');
    const headers = new Headers(captured?.headers);
    expect(headers.get('Accept')).toBe(
      'application/json, application/problem+json',
    );
    expect(headers.get(WEB_CLIENT_HEADER_NAME)).toBe('web');
    expect(headers.get(DANTE_TIME_ZONE_HEADER_NAME)).toBe('Europe/Rome');
    expect(headers.get('X-Existing')).toBe('value');
  });

  it('preserves Request headers and overlays init headers before governance', async () => {
    let captured: RequestInit | undefined;
    const fetchFn: typeof globalThis.fetch = (_input, init) => {
      captured = init;
      return Promise.resolve(new Response(null, { status: 204 }));
    };
    const request = new Request('https://example.test/api/v1/example', {
      headers: {
        'X-From-Request': 'request-value',
        'X-Overlay': 'request-value',
        'X-Dante-Time-Zone': 'Not/AZone',
      },
    });

    const webFetch = createWebFetch(fetchFn, () => 'America/New_York');
    await webFetch(request, {
      headers: {
        'X-From-Init': 'init-value',
        'X-Overlay': 'init-value',
      },
    });

    const headers = new Headers(captured?.headers);
    expect(headers.get('X-From-Request')).toBe('request-value');
    expect(headers.get('X-From-Init')).toBe('init-value');
    expect(headers.get('X-Overlay')).toBe('init-value');
    expect(headers.get(DANTE_TIME_ZONE_HEADER_NAME)).toBe('America/New_York');
    expect(headers.get(WEB_CLIENT_HEADER_NAME)).toBe('web');
  });

  it('fails before transport when device timezone detection fails', () => {
    let called = false;
    const fetchFn: typeof globalThis.fetch = () => {
      called = true;
      return Promise.resolve(new Response(null, { status: 204 }));
    };
    const webFetch = createWebFetch(fetchFn, () => {
      throw new RangeError('invalid timezone');
    });

    expect(() => webFetch('/api/v1/example')).toThrow('invalid timezone');
    expect(called).toBe(false);
  });
});
