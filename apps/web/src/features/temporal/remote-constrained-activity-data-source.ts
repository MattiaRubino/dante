import { Temporal } from '@dante/time';

import { createWebFetch } from '../../platform/api/web-fetch';
import type {
  TemporalActivityConstraintRuleInput,
  TemporalConstrainedActivityCreateRequest,
  TemporalConstrainedActivityCreateResult,
  TemporalConstrainedActivityDataSource,
} from './activity-data-source';
import { TemporalActivityRemoteError } from './remote-activity-data-source';

const SESSION_ENDPOINT = '/api/v1/auth/session';
const CONSTRAINED_ACTIVITY_ENDPOINT = '/api/v1/temporal/activities/constrained';
const CSRF_HEADER_NAME = 'X-Dante-CSRF';
const UUID_V7 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function parseUuidV7(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new TemporalActivityRemoteError(
      'protocol',
      `${field} must be a canonical UUIDv7 string.`,
    );
  }
  return value.toLowerCase();
}

function parseInstant(value: unknown, field: string) {
  if (typeof value !== 'string') {
    throw new TemporalActivityRemoteError(
      'protocol',
      `${field} must be an absolute timestamp.`,
    );
  }
  try {
    return Temporal.Instant.from(value);
  } catch {
    throw new TemporalActivityRemoteError(
      'protocol',
      `${field} must be an absolute timestamp.`,
    );
  }
}

function serializeRule(rule: TemporalActivityConstraintRuleInput) {
  if (rule.family === 'window') {
    return {
      family: 'window',
      relationship: rule.relationship,
      constrained_facet: rule.constrainedFacet,
      strength: rule.strength,
      temporal_form: 'absolute',
      starts_at: rule.startsAt.toString(),
      ends_at: rule.endsAt.toString(),
    } as const;
  }
  return {
    family: 'boundary',
    boundary_kind: rule.boundaryKind,
    constrained_facet: rule.constrainedFacet,
    strength: rule.strength,
    temporal_form: 'absolute',
    boundary_at: rule.boundaryAt.toString(),
  } as const;
}

function validateRequest(request: TemporalConstrainedActivityCreateRequest): void {
  if (!request.operationId.trim() || request.operationId.trim().length > 200) {
    throw new RangeError(
      'Activity operation id must contain 1 to 200 characters.',
    );
  }
  if (!request.title.trim() || request.title.trim().length > 300) {
    throw new RangeError('Activity title must contain 1 to 300 characters.');
  }
  if (request.rules.length < 1 || request.rules.length > 4) {
    throw new RangeError('Constrained Activity requires 1 to 4 rules.');
  }
  for (const rule of request.rules) {
    if (rule.family === 'window') {
      if (Temporal.Instant.compare(rule.startsAt, rule.endsAt) >= 0) {
        throw new RangeError('Constraint window must be a positive interval.');
      }
    }
  }
}

async function json(response: Response, label: string): Promise<unknown> {
  try {
    return await response.json();
  } catch {
    throw new TemporalActivityRemoteError(
      'protocol',
      `${label} is not valid JSON.`,
      response.status,
    );
  }
}

function problemCode(payload: unknown): string | null {
  return isRecord(payload) && typeof payload.code === 'string'
    ? payload.code
    : null;
}

async function csrfToken(
  webFetch: typeof globalThis.fetch,
  signal?: AbortSignal,
): Promise<string> {
  let response: Response;
  try {
    response = await webFetch(
      SESSION_ENDPOINT,
      signal === undefined ? undefined : { signal },
    );
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') {
      throw error;
    }
    throw new TemporalActivityRemoteError(
      'transport',
      'Constrained Activity request could not reach DANTE.',
    );
  }
  const payload = await json(response, 'Auth session response');
  if (
    !response.ok ||
    !isRecord(payload) ||
    payload.authenticated !== true ||
    typeof payload.csrf_token !== 'string' ||
    payload.csrf_token.length === 0
  ) {
    throw new TemporalActivityRemoteError(
      'authentication',
      'Constrained Activity mutation requires an authenticated browser session.',
      response.status,
      problemCode(payload),
    );
  }
  return payload.csrf_token;
}

function parseResponse(payload: unknown): TemporalConstrainedActivityCreateResult {
  if (
    !isRecord(payload) ||
    !isRecord(payload.activity) ||
    !Array.isArray(payload.constraints) ||
    typeof payload.replayed !== 'boolean'
  ) {
    throw new TemporalActivityRemoteError(
      'protocol',
      'Constrained Activity response has an unsupported representation.',
    );
  }
  const activity = payload.activity;
  if (
    typeof activity.title !== 'string' ||
    typeof activity.replayed !== 'boolean'
  ) {
    throw new TemporalActivityRemoteError(
      'protocol',
      'Constrained Activity response contains an invalid Activity.',
    );
  }
  const constraints = payload.constraints.map((item, index) => {
    if (!isRecord(item)) {
      throw new TemporalActivityRemoteError(
        'protocol',
        `Constraint ${index} is not an object.`,
      );
    }
    return Object.freeze({
      constraintRef: parseUuidV7(item.constraint_ref, `constraints[${index}].constraint_ref`),
      materialStateRef: parseUuidV7(
        item.material_state_ref,
        `constraints[${index}].material_state_ref`,
      ),
    });
  });
  if (constraints.length < 1 || constraints.length > 4) {
    throw new TemporalActivityRemoteError(
      'protocol',
      'Constrained Activity response returned an invalid constraint count.',
    );
  }
  return Object.freeze({
    activity: Object.freeze({
      activityRef: parseUuidV7(activity.activity_ref, 'activity.activity_ref'),
      title: activity.title,
      createdAt: parseInstant(activity.created_at, 'activity.created_at'),
    }),
    constraints: Object.freeze(constraints),
    replayed: payload.replayed,
  });
}

export function createRemoteTemporalConstrainedActivityDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
): TemporalConstrainedActivityDataSource {
  const webFetch = createWebFetch(fetchFn);
  return Object.freeze({
    async createConstrainedActivity(
      request: TemporalConstrainedActivityCreateRequest,
      signal?: AbortSignal,
    ): Promise<TemporalConstrainedActivityCreateResult> {
      validateRequest(request);
      const csrf = await csrfToken(webFetch, signal);
      let response: Response;
      try {
        response = await webFetch(CONSTRAINED_ACTIVITY_ENDPOINT, {
          method: 'POST',
          headers: new Headers({
            'Content-Type': 'application/json',
            [CSRF_HEADER_NAME]: csrf,
          }),
          body: JSON.stringify({
            operation_id: request.operationId.trim(),
            title: request.title.trim(),
            ...(request.lifeAreaRef === undefined ? {} : { life_area_ref: request.lifeAreaRef }),
            rules: request.rules.map(serializeRule),
          }),
          ...(signal === undefined ? {} : { signal }),
        });
      } catch (error) {
        if (error instanceof DOMException && error.name === 'AbortError') {
          throw error;
        }
        throw new TemporalActivityRemoteError(
          'transport',
          'Constrained Activity request could not reach DANTE.',
        );
      }
      const payload = await json(response, 'Create Constrained Activity response');
      if (!response.ok) {
        throw new TemporalActivityRemoteError(
          'http',
          `Create Constrained Activity failed with HTTP ${response.status}.`,
          response.status,
          problemCode(payload),
        );
      }
      return parseResponse(payload);
    },
  });
}
