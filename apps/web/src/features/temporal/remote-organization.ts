import { createWebFetch } from '../../platform/api/web-fetch';

export type OrganizationKind = 'activity' | 'event';
export type LifeArea = Readonly<{
  ref: string;
  name: string;
  revision: number;
  sortOrder: number;
  archived: boolean;
  hidden: boolean;
  iconCode: string | null;
  colorCode: string | null;
}>;
export type LifeAreaAssignment = Readonly<{
  kind: OrganizationKind;
  itemRef: string;
  areaRef: string;
  revision: number;
}>;
export type UnassignedItem = Readonly<{
  kind: OrganizationKind;
  itemRef: string;
  title: string;
}>;
export type ProductTag = Readonly<{
  ref: string;
  name: string;
  revision: number;
  archived: boolean;
}>;
export type ProductTagEdge = Readonly<{
  kind: OrganizationKind;
  itemRef: string;
  tagRef: string;
}>;
export type OrganizationSnapshot = Readonly<{
  areas: readonly LifeArea[];
  assignments: readonly LifeAreaAssignment[];
  unassigned: readonly UnassignedItem[];
  tags: readonly ProductTag[];
  tagEdges: readonly ProductTagEdge[];
}>;

const UUID_V7 = /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export class TemporalOrganizationError extends Error {
  constructor(message: string, readonly status: number | null = null, readonly code: string | null = null) {
    super(message);
    this.name = 'TemporalOrganizationError';
  }
}

function record(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new TemporalOrganizationError('Invalid organization response.');
  }
  return value as Record<string, unknown>;
}

function uuid(value: unknown): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new TemporalOrganizationError('Invalid organization identity.');
  }
  return value.toLowerCase();
}

function kind(value: unknown): OrganizationKind {
  if (value !== 'activity' && value !== 'event') {
    throw new TemporalOrganizationError('Invalid organization item kind.');
  }
  return value;
}

function label(value: unknown): string {
  if (typeof value !== 'string' || !value.trim()) {
    throw new TemporalOrganizationError('Invalid organization label.');
  }
  return value;
}

function revision(value: unknown): number {
  if (typeof value !== 'number' || !Number.isSafeInteger(value) || value < 0) {
    throw new TemporalOrganizationError('Invalid organization revision.');
  }
  return value;
}

function boolean(value: unknown): boolean {
  if (typeof value !== 'boolean') {
    throw new TemporalOrganizationError('Invalid organization state.');
  }
  return value;
}

function nullable(value: unknown): string | null {
  if (value !== null && typeof value !== 'string') {
    throw new TemporalOrganizationError('Invalid organization appearance.');
  }
  return value;
}

function list<T>(value: unknown, parse: (row: unknown) => T): readonly T[] {
  if (!Array.isArray(value)) {
    throw new TemporalOrganizationError('Invalid organization collection.');
  }
  return Object.freeze(value.map(parse));
}

function area(value: unknown): LifeArea {
  const row = record(value);
  return Object.freeze({
    ref: uuid(row.life_area_ref),
    name: label(row.name),
    revision: revision(row.revision),
    sortOrder: revision(row.sort_order),
    archived: boolean(row.archived),
    hidden: boolean(row.hidden),
    iconCode: nullable(row.icon_code),
    colorCode: nullable(row.color_code),
  });
}

function assignment(value: unknown): LifeAreaAssignment {
  const row = record(value);
  return Object.freeze({
    kind: kind(row.subject_kind),
    itemRef: uuid(row.subject_native_ref),
    areaRef: uuid(row.life_area_ref),
    revision: revision(row.assignment_revision),
  });
}

function unassigned(value: unknown): UnassignedItem {
  const row = record(value);
  return Object.freeze({
    kind: kind(row.subject_kind),
    itemRef: uuid(row.subject_native_ref),
    title: label(row.title),
  });
}

function tag(value: unknown): ProductTag {
  const row = record(value);
  return Object.freeze({
    ref: uuid(row.tag_ref),
    name: label(row.name),
    revision: revision(row.revision),
    archived: boolean(row.archived),
  });
}

function edge(value: unknown): ProductTagEdge {
  const row = record(value);
  return Object.freeze({
    kind: kind(row.subject_kind),
    itemRef: uuid(row.subject_native_ref),
    tagRef: uuid(row.tag_ref),
  });
}

/** Actor-local LR-12 metadata. Mutations never modify Schedule/conflict truth. */
export function createRemoteTemporalOrganizationDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const webFetch = createWebFetch(fetchFn);

  async function request(path: string, init?: RequestInit): Promise<unknown> {
    const response = await webFetch(path, init);
    let value: unknown;
    try {
      value = await response.json();
    } catch {
      throw new TemporalOrganizationError('Invalid organization JSON.', response.status);
    }
    if (!response.ok) {
      const problem = record(value);
      throw new TemporalOrganizationError(
        typeof problem.detail === 'string' ? problem.detail : 'Organization unavailable.',
        response.status,
        typeof problem.code === 'string' ? problem.code : null,
      );
    }
    return value;
  }

  async function mutate(path: string, method: string, payload: unknown): Promise<unknown> {
    const session = record(await request('/api/v1/auth/session'));
    if (session.authenticated !== true || typeof session.csrf_token !== 'string' || !session.csrf_token) {
      throw new TemporalOrganizationError('Organization requires an authenticated session.', 401);
    }
    return request(path, {
      method,
      headers: new Headers({
        'Content-Type': 'application/json',
        'X-Dante-CSRF': session.csrf_token,
      }),
      body: JSON.stringify(payload),
    });
  }

  return Object.freeze({
    async load(): Promise<OrganizationSnapshot> {
      const [areas, assignments, unassignedItems, tags, edges] = await Promise.all([
        request('/api/v1/temporal/life-areas'),
        request('/api/v1/temporal/life-area-assignments'),
        request('/api/v1/temporal/life-area-assignments/unassigned'),
        request('/api/v1/temporal/tags'),
        request('/api/v1/temporal/tags/assignments'),
      ]);
      return Object.freeze({
        areas: list(areas, area), assignments: list(assignments, assignment),
        unassigned: list(unassignedItems, unassigned), tags: list(tags, tag),
        tagEdges: list(edges, edge),
      });
    },
    async createArea(name: string): Promise<LifeArea> {
      return area(await mutate('/api/v1/temporal/life-areas', 'POST', {
        operation_id: crypto.randomUUID(), name,
      }));
    },
    async renameArea(current: LifeArea, name: string): Promise<void> {
      await mutate(`/api/v1/temporal/life-areas/${current.ref}/name`, 'PATCH', {
        operation_id: crypto.randomUUID(), expected_revision: current.revision, name,
      });
    },
    async setAreaHidden(current: LifeArea, hidden: boolean): Promise<void> {
      await mutate(`/api/v1/temporal/life-areas/${current.ref}/visibility`, 'PUT', {
        operation_id: crypto.randomUUID(), expected_revision: current.revision, hidden,
      });
    },
    async setAreaAppearance(current: LifeArea, iconCode: string | null, colorCode: string | null): Promise<void> {
      await mutate(`/api/v1/temporal/life-areas/${current.ref}/appearance`, 'PUT', {
        operation_id: crypto.randomUUID(), expected_revision: current.revision,
        icon_code: iconCode, color_code: colorCode,
      });
    },
    async archiveArea(current: LifeArea): Promise<void> {
      await mutate(`/api/v1/temporal/life-areas/${current.ref}/archive`, 'POST', {
        operation_id: crypto.randomUUID(), expected_revision: current.revision,
      });
    },
    async reorderAreas(areas: readonly LifeArea[]): Promise<void> {
      await mutate('/api/v1/temporal/life-areas/order', 'PUT', {
        operation_id: crypto.randomUUID(),
        entries: areas.map((item) => ({ life_area_ref: item.ref, expected_revision: item.revision })),
      });
    },
    async assignItem(item: Pick<UnassignedItem, 'kind' | 'itemRef'>, areaRef: string, expectedRevision: number): Promise<void> {
      await mutate(`/api/v1/temporal/life-area-assignments/${item.kind === 'activity' ? 'activities' : 'events'}/${item.itemRef}`, 'PUT', {
        operation_id: crypto.randomUUID(), life_area_ref: uuid(areaRef),
        expected_assignment_revision: expectedRevision,
      });
    },
    async createTag(name: string): Promise<ProductTag> {
      return tag(await mutate('/api/v1/temporal/tags', 'POST', {
        operation_id: crypto.randomUUID(), name,
      }));
    },
    async renameTag(current: ProductTag, name: string): Promise<void> {
      await mutate(`/api/v1/temporal/tags/${current.ref}/name`, 'PUT', {
        operation_id: crypto.randomUUID(), expected_revision: current.revision, name,
      });
    },
    async archiveTag(current: ProductTag): Promise<void> {
      await mutate(`/api/v1/temporal/tags/${current.ref}/archive`, 'POST', {
        operation_id: crypto.randomUUID(), expected_revision: current.revision,
      });
    },
    async setItemTag(item: Pick<UnassignedItem, 'kind' | 'itemRef'>, tagRef: string, attached: boolean): Promise<void> {
      await mutate(`/api/v1/temporal/${item.kind === 'activity' ? 'activities' : 'events'}/${item.itemRef}/tags/${uuid(tagRef)}/${attached ? 'attach' : 'detach'}`, 'POST', {
        operation_id: crypto.randomUUID(),
      });
    },
  });
}
