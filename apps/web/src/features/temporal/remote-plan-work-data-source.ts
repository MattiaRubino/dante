import { createWebFetch } from '../../platform/api/web-fetch';

const ENDPOINT = '/api/v1/temporal/plans';
const UUID_V7 = /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export type PlanStep = Readonly<{
  stepRef: string;
  title: string;
  position: number;
  activityRef: string | null;
}>;

export type PlanWork = Readonly<{
  planRef: string;
  stateRef: string;
  title: string;
  createdAt: string;
  steps: readonly PlanStep[];
  replayed: boolean;
}>;

function record(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new Error('Risposta Plan non valida.');
  }
  return value as Record<string, unknown>;
}

function uuid(value: unknown): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new Error('Riferimento Plan non valido.');
  }
  return value.toLowerCase();
}

function step(value: unknown): PlanStep {
  const row = record(value);
  if (typeof row.title !== 'string' || !row.title.trim() ||
      typeof row.position !== 'number' || !Number.isInteger(row.position) ||
      row.position < 0 || row.position >= 1000) {
    throw new Error('Step del Plan non valido.');
  }
  return Object.freeze({
    stepRef: uuid(row.step_ref),
    title: row.title,
    position: row.position,
    activityRef: row.activity_ref === null ? null : uuid(row.activity_ref),
  });
}

function plan(value: unknown): PlanWork {
  const row = record(value);
  if (typeof row.title !== 'string' || !row.title.trim() ||
      typeof row.created_at !== 'string' || !Number.isFinite(Date.parse(row.created_at)) ||
      !Array.isArray(row.steps) || typeof row.replayed !== 'boolean') {
    throw new Error('Struttura Plan non valida.');
  }
  const steps = row.steps.map(step);
  if (steps.some((item, index) => item.position !== index)) {
    throw new Error('Ordine del Plan non valido.');
  }
  return Object.freeze({
    planRef: uuid(row.plan_ref),
    stateRef: uuid(row.state_ref),
    title: row.title,
    createdAt: row.created_at,
    steps: Object.freeze(steps),
    replayed: row.replayed,
  });
}

async function errorMessage(response: Response): Promise<string> {
  try {
    const payload = record(await response.json());
    if (typeof payload.detail === 'string' && payload.detail.trim()) return payload.detail;
  } catch {
    // Preserve the HTTP status when a server returns an unreadable ProblemDetails.
  }
  return `Plan non disponibile (HTTP ${response.status}).`;
}

export function newPlanStepRef(): string {
  const bytes = crypto.getRandomValues(new Uint8Array(16));
  const milliseconds = BigInt(Date.now());
  for (let index = 0; index < 6; index += 1) {
    bytes[5 - index] = Number((milliseconds >> BigInt(index * 8)) & 0xffn);
  }
  bytes[6] = 0x70 | (bytes[6]! & 0x0f);
  bytes[8] = 0x80 | (bytes[8]! & 0x3f);
  const hex = Array.from(bytes, (byte) => byte.toString(16).padStart(2, '0')).join('');
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
}

export function createRemotePlanWorkDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const webFetch = createWebFetch(fetchFn);

  async function csrf(): Promise<string> {
    const response = await webFetch('/api/v1/auth/session');
    if (!response.ok) throw new Error('Sessione non disponibile.');
    const payload = record(await response.json());
    if (payload.authenticated !== true || typeof payload.csrf_token !== 'string' ||
        !payload.csrf_token) {
      throw new Error('Accedi prima di modificare un Plan.');
    }
    return payload.csrf_token;
  }

  async function mutation(
    endpoint: string, method: 'POST' | 'PUT', body: Record<string, unknown>,
  ): Promise<PlanWork> {
    const response = await webFetch(endpoint, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'X-Dante-CSRF': await csrf(),
      },
      body: JSON.stringify(body),
    });
    if (!response.ok) throw new Error(await errorMessage(response));
    return plan(await response.json());
  }

  return Object.freeze({
    async list(): Promise<readonly PlanWork[]> {
      const response = await webFetch(ENDPOINT);
      if (!response.ok) throw new Error(await errorMessage(response));
      const payload: unknown = await response.json();
      if (!Array.isArray(payload)) throw new Error('Elenco Plan non valido.');
      return Object.freeze(payload.map(plan));
    },
    async create(title: string, operationId: string): Promise<PlanWork> {
      return mutation(ENDPOINT, 'POST', { title: title.trim(), operation_id: operationId });
    },
    async replace(
      current: PlanWork, title: string, steps: readonly Pick<PlanStep, 'stepRef' | 'title' | 'activityRef'>[],
      operationId: string,
    ): Promise<PlanWork> {
      return mutation(`${ENDPOINT}/${encodeURIComponent(current.planRef)}`, 'PUT', {
        operation_id: operationId,
        expected_state_ref: current.stateRef,
        title: title.trim(),
        steps: steps.map((item) => ({
          step_ref: uuid(item.stepRef),
          title: item.title.trim(),
          activity_ref: item.activityRef === null ? null : uuid(item.activityRef),
        })),
      });
    },
  });
}
