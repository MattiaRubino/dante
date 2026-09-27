import { createWebFetch } from '../../platform/api/web-fetch';

const UUID_V7 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export type AdvancedRecurrenceOwnerKind = 'routine' | 'event';
export type AdvancedRecurrenceAnchorMode = 'previous_completion' | 'anchor_stream';
export type AdvancedRecurrenceAnchorSourceKind = 'routine' | 'event';

export type AdvancedRecurrenceView = Readonly<{
  ownerKind: AdvancedRecurrenceOwnerKind;
  sourceRef: string;
  materialStateRef: string;
  effectiveFrom: string;
  elapsedSeconds: string;
  anchorModeCode: AdvancedRecurrenceAnchorMode;
  anchorSourceFamily: AdvancedRecurrenceAnchorSourceKind | null;
  anchorSourceNativeRef: string | null;
  replayed: boolean;
}>;

export type AdvancedRecurrenceLoadResult = Readonly<{
  currentMaterialStateRef: string | null;
  advanced: AdvancedRecurrenceView | null;
}>;

export type ReplaceAdvancedRecurrenceCommand = Readonly<{
  operationId: string;
  expectedMaterialStateRef: string;
  effectiveFrom: string;
  elapsedSeconds: string;
  anchorModeCode: AdvancedRecurrenceAnchorMode;
  anchorSourceFamily: AdvancedRecurrenceAnchorSourceKind | null;
  anchorSourceNativeRef: string | null;
}>;

export class TemporalAdvancedRecurrenceRemoteError extends Error {
  constructor(
    readonly kind: 'transport' | 'http' | 'protocol' | 'authentication',
    message: string,
    readonly status: number | null = null,
    readonly code: string | null = null,
  ) {
    super(message);
    this.name = 'TemporalAdvancedRecurrenceRemoteError';
  }
}

function record(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new TemporalAdvancedRecurrenceRemoteError(
      'protocol',
      'Invalid advanced Recurrence response.',
    );
  }
  return value as Record<string, unknown>;
}

function uuid(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new TemporalAdvancedRecurrenceRemoteError(
      'protocol',
      `${field} must be a UUIDv7.`,
    );
  }
  return value.toLowerCase();
}

function nullableUuid(value: unknown, field: string): string | null {
  return value === null ? null : uuid(value, field);
}

function path(owner: AdvancedRecurrenceOwnerKind, sourceRef: string): string {
  const collection = owner === 'routine' ? 'routines' : 'events';
  return `/api/v1/temporal/${collection}/${encodeURIComponent(sourceRef)}`;
}

function view(value: unknown): AdvancedRecurrenceView {
  const payload = record(value);
  if (payload.owner_kind !== 'routine' && payload.owner_kind !== 'event') {
    throw new TemporalAdvancedRecurrenceRemoteError('protocol', 'Invalid Recurrence owner.');
  }
  if (
    payload.anchor_mode_code !== 'previous_completion' &&
    payload.anchor_mode_code !== 'anchor_stream'
  ) {
    throw new TemporalAdvancedRecurrenceRemoteError(
      'protocol',
      'Invalid advanced Recurrence anchor mode.',
    );
  }
  if (
    payload.anchor_source_family !== null &&
    payload.anchor_source_family !== 'routine' &&
    payload.anchor_source_family !== 'event'
  ) {
    throw new TemporalAdvancedRecurrenceRemoteError(
      'protocol',
      'Invalid advanced Recurrence anchor source family.',
    );
  }
  if (typeof payload.effective_from !== 'string') {
    throw new TemporalAdvancedRecurrenceRemoteError(
      'protocol',
      'Invalid advanced Recurrence effective start.',
    );
  }
  if (typeof payload.elapsed_seconds !== 'string' && typeof payload.elapsed_seconds !== 'number') {
    throw new TemporalAdvancedRecurrenceRemoteError(
      'protocol',
      'Invalid advanced Recurrence delay.',
    );
  }
  if (typeof payload.replayed !== 'boolean') {
    throw new TemporalAdvancedRecurrenceRemoteError(
      'protocol',
      'Invalid advanced Recurrence replay state.',
    );
  }
  return Object.freeze({
    ownerKind: payload.owner_kind,
    sourceRef: uuid(payload.source_ref, 'source_ref'),
    materialStateRef: uuid(payload.material_state_ref, 'material_state_ref'),
    effectiveFrom: payload.effective_from,
    elapsedSeconds: String(payload.elapsed_seconds),
    anchorModeCode: payload.anchor_mode_code,
    anchorSourceFamily: payload.anchor_source_family,
    anchorSourceNativeRef: nullableUuid(
      payload.anchor_source_native_ref,
      'anchor_source_native_ref',
    ),
    replayed: payload.replayed,
  });
}

export function createRemoteTemporalAdvancedRecurrenceDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const webFetch = createWebFetch(fetchFn);

  async function problem(response: Response): Promise<TemporalAdvancedRecurrenceRemoteError> {
    let payload: Record<string, unknown> = {};
    try {
      payload = record(await response.json());
    } catch {
      return new TemporalAdvancedRecurrenceRemoteError(
        'http',
        'Advanced Recurrence command rejected.',
        response.status,
      );
    }
    return new TemporalAdvancedRecurrenceRemoteError(
      'http',
      typeof payload.detail === 'string'
        ? payload.detail
        : 'Advanced Recurrence command rejected.',
      response.status,
      typeof payload.code === 'string' ? payload.code : null,
    );
  }

  async function csrf(): Promise<string> {
    const response = await webFetch('/api/v1/auth/session');
    const payload = record(await response.json());
    if (
      !response.ok ||
      payload.authenticated !== true ||
      typeof payload.csrf_token !== 'string' ||
      payload.csrf_token.length === 0
    ) {
      throw new TemporalAdvancedRecurrenceRemoteError(
        'authentication',
        'Advanced Recurrence commands require an authenticated browser session.',
        response.status,
      );
    }
    return payload.csrf_token;
  }

  async function currentMaterialStateRef(
    owner: AdvancedRecurrenceOwnerKind,
    sourceRef: string,
  ): Promise<string | null> {
    const response = await webFetch(`${path(owner, sourceRef)}/recurrence`);
    if (!response.ok) throw await problem(response);
    const raw: unknown = await response.json();
    if (raw === null) return null;
    const payload = record(raw);
    return uuid(payload.material_state_ref, 'material_state_ref');
  }

  return Object.freeze({
    async load(
      owner: AdvancedRecurrenceOwnerKind,
      sourceRef: string,
    ): Promise<AdvancedRecurrenceLoadResult> {
      const stateRef = await currentMaterialStateRef(owner, sourceRef);
      if (stateRef === null) {
        return Object.freeze({ currentMaterialStateRef: null, advanced: null });
      }

      const response = await webFetch(`${path(owner, sourceRef)}/advanced-recurrence`);
      if (!response.ok) {
        const error = await problem(response);
        if (
          response.status === 404 &&
          error.code === 'temporal.advanced_recurrence.unavailable'
        ) {
          return Object.freeze({ currentMaterialStateRef: stateRef, advanced: null });
        }
        throw error;
      }
      const advanced = view(await response.json());
      return Object.freeze({
        currentMaterialStateRef: advanced.materialStateRef,
        advanced,
      });
    },

    async replace(
      owner: AdvancedRecurrenceOwnerKind,
      sourceRef: string,
      command: ReplaceAdvancedRecurrenceCommand,
    ): Promise<AdvancedRecurrenceView> {
      const response = await webFetch(`${path(owner, sourceRef)}/advanced-recurrence`, {
        method: 'PUT',
        headers: new Headers({
          'Content-Type': 'application/json',
          'X-Dante-CSRF': await csrf(),
        }),
        body: JSON.stringify({
          operation_id: command.operationId,
          expected_material_state_ref: command.expectedMaterialStateRef,
          range_kind: 'open',
          expected_occurrence_count: null,
          effective_from: command.effectiveFrom,
          effective_until: null,
          elapsed_seconds: command.elapsedSeconds,
          anchor_mode_code: command.anchorModeCode,
          anchor_source_family: command.anchorSourceFamily,
          anchor_source_native_ref: command.anchorSourceNativeRef,
        }),
      });
      if (!response.ok) throw await problem(response);
      return view(await response.json());
    },
  });
}
