import { describe, expect, it, vi } from 'vitest';

import {
  createRemoteTemporalOrganizationDataSource,
  TemporalOrganizationError,
} from './remote-organization';

const AREA_REF = '0199a8c0-6e71-7bc0-8ad0-a2f403f5617d';
const EVENT_REF = '0199a8c0-6e72-7bc0-8ad0-a2f403f5617d';
const TAG_REF = '0199a8c0-6e73-7bc0-8ad0-a2f403f5617d';

function response(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

describe('remote temporal organization data source', () => {
  it('reads the separate actor-local catalogs and typed relations without inventing an area', async () => {
    const fetchFn = vi.fn<typeof globalThis.fetch>((input, init) => {
      expect(new Headers(init?.headers).get('X-Dante-Client')).toBe('web');
      switch (input) {
        case '/api/v1/temporal/life-areas':
          return Promise.resolve(
            response([
              {
                life_area_ref: AREA_REF,
                name: 'Lavoro',
                revision: 2,
                sort_order: 0,
                archived: false,
                hidden: true,
                icon_code: null,
                color_code: null,
              },
            ]),
          );
        case '/api/v1/temporal/life-area-assignments':
          return Promise.resolve(
            response([
              {
                subject_kind: 'event',
                subject_native_ref: EVENT_REF,
                life_area_ref: AREA_REF,
                assignment_revision: 1,
              },
            ]),
          );
        case '/api/v1/temporal/life-area-assignments/unassigned':
          return Promise.resolve(response([]));
        case '/api/v1/temporal/tags':
          return Promise.resolve(
            response([
              {
                tag_ref: TAG_REF,
                name: 'Importante',
                revision: 1,
                archived: false,
              },
            ]),
          );
        case '/api/v1/temporal/tags/assignments':
          return Promise.resolve(
            response([
              {
                subject_kind: 'event',
                subject_native_ref: EVENT_REF,
                tag_ref: TAG_REF,
              },
            ]),
          );
        default:
          throw new Error(`unexpected request ${String(input)}`);
      }
    });

    const snapshot =
      await createRemoteTemporalOrganizationDataSource(fetchFn).load();

    expect(snapshot.areas).toEqual([
      expect.objectContaining({ ref: AREA_REF, hidden: true }),
    ]);
    expect(snapshot.assignments).toEqual([
      expect.objectContaining({
        kind: 'event',
        itemRef: EVENT_REF,
        areaRef: AREA_REF,
      }),
    ]);
    expect(snapshot.tags).toEqual([expect.objectContaining({ ref: TAG_REF })]);
    expect(snapshot.tagEdges).toEqual([
      expect.objectContaining({ tagRef: TAG_REF }),
    ]);
    expect(fetchFn).toHaveBeenCalledTimes(5);
  });

  it('uses the governed CSRF boundary for an actor-local Life Area mutation', async () => {
    const fetchFn = vi.fn<typeof globalThis.fetch>((input, init) => {
      if (input === '/api/v1/auth/session') {
        return Promise.resolve(
          response({ authenticated: true, csrf_token: 'csrf-b05-d' }),
        );
      }
      expect(input).toBe('/api/v1/temporal/life-areas');
      expect(init?.method).toBe('POST');
      expect(new Headers(init?.headers).get('X-Dante-CSRF')).toBe('csrf-b05-d');
      expect(JSON.parse(String(init?.body))).toMatchObject({ name: 'Salute' });
      return Promise.resolve(
        response(
          {
            life_area_ref: AREA_REF,
            name: 'Salute',
            revision: 1,
            sort_order: 0,
            archived: false,
            hidden: false,
            icon_code: null,
            color_code: null,
          },
          201,
        ),
      );
    });

    await expect(
      createRemoteTemporalOrganizationDataSource(fetchFn).createArea('Salute'),
    ).resolves.toMatchObject({ ref: AREA_REF, name: 'Salute' });
  });

  it('rejects a malformed actor-local identity at the protocol boundary', async () => {
    const source = createRemoteTemporalOrganizationDataSource(
      vi.fn<typeof globalThis.fetch>(() => Promise.resolve(response([]))),
    );
    await expect(
      source.assignItem({ kind: 'event', itemRef: EVENT_REF }, 'not-a-uuid', 0),
    ).rejects.toBeInstanceOf(TemporalOrganizationError);
  });
});
