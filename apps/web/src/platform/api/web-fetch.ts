import { detectDeviceTimeZone } from '@dante/time';

export const WEB_CLIENT_HEADER_NAME = 'X-Dante-Client';
export const WEB_CLIENT_HEADER_VALUE = 'web';
export const DANTE_TIME_ZONE_HEADER_NAME = 'X-Dante-Time-Zone';
export const ACCEPT_HEADER_VALUE =
  'application/json, application/problem+json';

export type DeviceTimeZoneResolver = () => string;

function governedHeaders(
  headersInit: HeadersInit | undefined,
  resolveDeviceTimeZone: DeviceTimeZoneResolver,
): Headers {
  const headers = new Headers(headersInit);
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
      headers: governedHeaders(init?.headers, resolveDeviceTimeZone),
    });
}
