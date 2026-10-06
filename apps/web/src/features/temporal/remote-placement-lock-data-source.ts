import { createWebFetch } from '../../platform/api/web-fetch';

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export type PlacementLockState = Readonly<{
  scheduleRef: string;
  locked: boolean;
  revision: number;
}>;

export class PlacementLockRemoteError extends Error {
  constructor(readonly status: number | null, readonly code: string | null, message: string) {
    super(message);
    this.name = 'PlacementLockRemoteError';
  }
}

function object(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) {
    throw new PlacementLockRemoteError(null, null, 'Invalid placement lock response.');
  }
  return value as Record<string, unknown>;
}

function state(value: unknown): PlacementLockState {
  const row = object(value);
  if (
    typeof row.schedule_ref !== 'string' || !UUID.test(row.schedule_ref) ||
    typeof row.locked !== 'boolean' ||
    !Number.isSafeInteger(row.revision) || Number(row.revision) < 0
  ) {
    throw new PlacementLockRemoteError(null, null, 'Invalid placement lock state.');
  }
  return Object.freeze({
    scheduleRef: row.schedule_ref.toLowerCase(),
    locked: row.locked,
    revision: Number(row.revision),
  });
}

export function createRemotePlacementLockDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const webFetch = createWebFetch(fetchFn);
  async function request(scheduleRef: string, locked?: boolean, expectedRevision?: number | null) {
    if (!UUID.test(scheduleRef)) {
      throw new PlacementLockRemoteError(null, null, 'Invalid Schedule reference.');
    }
    const url = `/api/v1/temporal/schedules/${encodeURIComponent(scheduleRef)}/placement-lock`;
    const session = locked === undefined ? null : object(await (await webFetch('/api/v1/auth/session')).json());
    if (session !== null && (session.authenticated !== true || typeof session.csrf_token !== 'string')) {
      throw new PlacementLockRemoteError(401, null, 'Placement lock requires an authenticated session.');
    }
    let response: Response;
    try {
      response = await webFetch(url, locked === undefined ? undefined : {
        method: 'PUT',
        headers: new Headers({
          'Content-Type': 'application/json',
          'X-Dante-CSRF': String(session?.csrf_token),
        }),
        body: JSON.stringify({ locked, expected_revision: expectedRevision ?? null }),
      });
    } catch (error) {
      throw new PlacementLockRemoteError(null, null, error instanceof Error ? error.message : 'Placement lock unavailable.');
    }
    const payload = object(await response.json());
    if (!response.ok) {
      throw new PlacementLockRemoteError(
        response.status, typeof payload.code === 'string' ? payload.code : null,
        typeof payload.detail === 'string' ? payload.detail : 'Placement lock request rejected.',
      );
    }
    return state(payload);
  }
  return Object.freeze({
    get: (scheduleRef: string): Promise<PlacementLockState> => request(scheduleRef),
    lock: (scheduleRef: string): Promise<PlacementLockState> => request(scheduleRef, true, null),
    set: (scheduleRef: string, locked: boolean, expectedRevision: number | null): Promise<PlacementLockState> =>
      request(scheduleRef, locked, expectedRevision),
    unlock: (scheduleRef: string, revision: number): Promise<PlacementLockState> => request(scheduleRef, false, revision),
  });
}
