import { detectDeviceTimeZone } from '@dante/time';

export const WEB_CLIENT_HEADER_NAME = 'X-Dante-Client';
export const WEB_CLIENT_HEADER_VALUE = 'web';
export const DANTE_TIME_ZONE_HEADER_NAME = 'X-Dante-Time-Zone';
export const ACCEPT_HEADER_VALUE = 'application/json, application/problem+json';

export type DeviceTimeZoneResolver = () => string;

function mergedRequestHeaders(
  input: RequestInfo | URL,
  init: RequestInit | undefined,
): Headers {
  const headers = new Headers(
    input instanceof Request ? input.headers : undefined,
  );
  if (init?.headers !== undefined) {
    new Headers(init.headers).forEach((value, name) => {
      headers.set(name, value);
    });
  }
  return headers;
}

function governedHeaders(
  input: RequestInfo | URL,
  init: RequestInit | undefined,
  resolveDeviceTimeZone: DeviceTimeZoneResolver,
): Headers {
  const headers = mergedRequestHeaders(input, init);
  headers.set('Accept', ACCEPT_HEADER_VALUE);
  headers.set(WEB_CLIENT_HEADER_NAME, WEB_CLIENT_HEADER_VALUE);
  headers.set(DANTE_TIME_ZONE_HEADER_NAME, resolveDeviceTimeZone());
  return headers;
}

export function createWebFetch(
  fetchFn: typeof globalThis.fetch,
  resolveDeviceTimeZone: DeviceTimeZoneResolver = detectDeviceTimeZone,
): typeof globalThis.fetch {
  return (input, init) =>
    fetchFn(input, {
      ...init,
      credentials: 'same-origin',
      headers: governedHeaders(input, init, resolveDeviceTimeZone),
    });
}
