import { createWebFetch } from '../../platform/api/web-fetch';

const UUID_V7 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export type ResponsibilitySubjectKind = 'activity' | 'event';
export type ParticipationRequirement = 'required' | 'optional';

export type TemporalResponsibilityView = Readonly<{
  subjectKind: ResponsibilitySubjectKind;
  subjectNativeRef: string;
  responsiblePersonRef: string | null;
  responsibleIsSelf: boolean;
  establishedAt: string | null;
  replayed: boolean;
}>;

export type TemporalExpectedParticipationView = Readonly<{
  eventRef: string;
  participantPersonRef: string;
  participantIsSelf: boolean;
  requirementCode: ParticipationRequirement | null;
  establishedAt: string | null;
  replayed: boolean;
}>;

export class TemporalResponsibilityRemoteError extends Error {
  constructor(
    readonly kind: 'transport' | 'http' | 'protocol' | 'authentication',
    message: string,
    readonly status: number | null = null,
    readonly code: string | null = null,
  ) {
    super(message);
    this.name = 'TemporalResponsibilityRemoteError';
  }
}

function record(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new TemporalResponsibilityRemoteError(
      'protocol',
      'Invalid Responsibility response.',
    );
  }
  return value as Record<string, unknown>;
}

function uuid(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new TemporalResponsibilityRemoteError(
      'protocol',
      `${field} must be a UUIDv7.`,
    );
  }
  return value.toLowerCase();
}

function optionalUuid(value: unknown, field: string): string | null {
  return value === null ? null : uuid(value, field);
}

function optionalText(value: unknown, field: string): string | null {
  if (value === null) {
    return null;
  }
  if (typeof value !== 'string') {
    throw new TemporalResponsibilityRemoteError('protocol', `${field} must be text.`);
  }
  return value;
}

function requirement(
  value: unknown,
  field: string,
): ParticipationRequirement | null {
  if (value === null) {
    return null;
  }
  if (value !== 'required' && value !== 'optional') {
    throw new TemporalResponsibilityRemoteError(
      'protocol',
      `${field} must be required or optional.`,
    );
  }
  return value;
}

function responsibility(value: unknown): TemporalResponsibilityView {
  const payload = record(value);
  const kind = payload.subject_kind;
  if (kind !== 'activity' && kind !== 'event') {
    throw new TemporalResponsibilityRemoteError(
      'protocol',
      'subject_kind must be activity or event.',
    );
  }
  if (
    typeof payload.replayed !== 'boolean' ||
    typeof payload.responsible_is_self !== 'boolean'
  ) {
    throw new TemporalResponsibilityRemoteError(
      'protocol',
      'Invalid Responsibility replay state.',
    );
  }
  return Object.freeze({
    subjectKind: kind,
    subjectNativeRef: uuid(payload.subject_native_ref, 'subject_native_ref'),
    responsiblePersonRef: optionalUuid(
      payload.responsible_person_ref,
      'responsible_person_ref',
    ),
    responsibleIsSelf: payload.responsible_is_self,
    establishedAt: optionalText(payload.established_at, 'established_at'),
    replayed: payload.replayed,
  });
}

function participation(value: unknown): TemporalExpectedParticipationView {
  const payload = record(value);
  if (
    typeof payload.replayed !== 'boolean' ||
    typeof payload.participant_is_self !== 'boolean'
  ) {
    throw new TemporalResponsibilityRemoteError(
      'protocol',
      'Invalid Participation replay state.',
    );
  }
  return Object.freeze({
    eventRef: uuid(payload.event_ref, 'event_ref'),
    participantPersonRef: uuid(
      payload.participant_person_ref,
      'participant_person_ref',
    ),
    participantIsSelf: payload.participant_is_self,
    requirementCode: requirement(payload.requirement_code, 'requirement_code'),
    establishedAt: optionalText(payload.established_at, 'established_at'),
    replayed: payload.replayed,
  });
}

export function createRemoteTemporalResponsibilityDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const webFetch = createWebFetch(fetchFn);

  async function csrf(): Promise<string> {
    const response = await webFetch('/api/v1/auth/session');
    const payload = record(await response.json());
    if (
      !response.ok ||
      payload.authenticated !== true ||
      typeof payload.csrf_token !== 'string' ||
      !payload.csrf_token
    ) {
      throw new TemporalResponsibilityRemoteError(
        'authentication',
        'Authoring requires an authenticated browser session.',
        response.status,
      );
    }
    return payload.csrf_token;
  }

  async function send(
    path: string,
    method: 'GET' | 'PUT',
    body?: unknown,
  ): Promise<unknown> {
    const headers = new Headers();
    if (method === 'PUT') {
      headers.set('Content-Type', 'application/json');
      headers.set('X-Dante-CSRF', await csrf());
    }
    const response = await webFetch(path, {
      method,
      headers,
      ...(body === undefined ? {} : { body: JSON.stringify(body) }),
    });
    const value: unknown = await response.json();
    if (!response.ok) {
      const problem = record(value);
      throw new TemporalResponsibilityRemoteError(
        'http',
        typeof problem.detail === 'string'
          ? problem.detail
          : 'Authoring command rejected.',
        response.status,
        typeof problem.code === 'string' ? problem.code : null,
      );
    }
    return value;
  }

  function subjectPath(kind: ResponsibilitySubjectKind, ref: string): string {
    const collection = kind === 'activity' ? 'activities' : 'events';
    return `/api/v1/temporal/${collection}/${encodeURIComponent(ref)}/responsibility`;
  }

  return Object.freeze({
    async getResponsibility(
      kind: ResponsibilitySubjectKind,
      subjectRef: string,
    ): Promise<TemporalResponsibilityView> {
      return responsibility(await send(subjectPath(kind, subjectRef), 'GET'));
    },
    async setResponsibility(
      kind: ResponsibilitySubjectKind,
      subjectRef: string,
      command: Readonly<{
        operationId: string;
        holder: 'self' | null;
        expectedHolder: 'self' | null;
      }>,
    ): Promise<TemporalResponsibilityView> {
      return responsibility(
        await send(subjectPath(kind, subjectRef), 'PUT', {
          operation_id: command.operationId,
          holder: command.holder,
          expected_holder: command.expectedHolder,
        }),
      );
    },
    async listExpectedParticipation(
      eventRef: string,
    ): Promise<TemporalExpectedParticipationView[]> {
      const value = await send(
        `/api/v1/temporal/events/${encodeURIComponent(eventRef)}/expected-participation`,
        'GET',
      );
      if (!Array.isArray(value)) {
        throw new TemporalResponsibilityRemoteError(
          'protocol',
          'Expected Participation list must be an array.',
        );
      }
      return value.map(participation);
    },
    async setExpectedParticipation(
      eventRef: string,
      command: Readonly<{
        operationId: string;
        requirementCode: ParticipationRequirement | null;
        expectedRequirementCode: ParticipationRequirement | null;
      }>,
    ): Promise<TemporalExpectedParticipationView> {
      return participation(
        await send(
          `/api/v1/temporal/events/${encodeURIComponent(eventRef)}/expected-participation`,
          'PUT',
          {
            operation_id: command.operationId,
            participant: 'self',
            requirement_code: command.requirementCode,
            expected_requirement_code: command.expectedRequirementCode,
          },
        ),
      );
    },
  });
}
