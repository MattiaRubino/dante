import { createWebFetch } from '../../../platform/api/web-fetch';
import type { TemporalCreateFields, TemporalCreateSurface } from '../model/temporal-create-session';
import type { TemporalCreateU2AuthoringDraft } from '../model/temporal-create-u2-authoring';

export type DraftVaultSnapshot = Readonly<{
  version: 1;
  fields: TemporalCreateFields;
  advanced: TemporalCreateU2AuthoringDraft;
  surface: TemporalCreateSurface;
}>;

export type DraftVaultItem = Readonly<{
  draftRef: string;
  subjectKind: 'activity' | 'event';
  title: string;
  payload: DraftVaultSnapshot;
  revision: number;
  createdAt: string;
  updatedAt: string;
}>;

function parseItem(value: unknown): DraftVaultItem {
  if (!value || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error('Bozza non valida.');
  }
  const item = value as Record<string, unknown>;
  const payload = item.payload as Record<string, unknown> | null;
  if (typeof item.draft_ref !== 'string' ||
      (item.subject_kind !== 'activity' && item.subject_kind !== 'event') ||
      typeof item.title !== 'string' ||
      typeof item.revision !== 'number' || !Number.isSafeInteger(item.revision) ||
      typeof item.created_at !== 'string' ||
      typeof item.updated_at !== 'string' ||
      !payload || payload.version !== 1 ||
      !payload.fields || typeof payload.fields !== 'object' ||
      !payload.advanced || typeof payload.advanced !== 'object' ||
      (payload.fields as Record<string, unknown>).kind !== item.subject_kind) {
    throw new Error('La bozza salvata non è compatibile con questo editor.');
  }
  return Object.freeze({
    draftRef: item.draft_ref,
    subjectKind: item.subject_kind,
    title: item.title,
    payload: payload as unknown as DraftVaultSnapshot,
    revision: item.revision as number,
    createdAt: item.created_at,
    updatedAt: item.updated_at,
  });
}

export function createRemoteDraftVault(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const request = createWebFetch(fetchFn);
  const url = '/api/v1/temporal/drafts';

  async function csrf(): Promise<string> {
    const response = await request('/api/v1/auth/session');
    if (!response.ok) throw new Error('Sessione scaduta.');
    const session = await response.json() as Record<string, unknown>;
    if (session.authenticated !== true || typeof session.csrf_token !== 'string') {
      throw new Error('Sessione non autenticata.');
    }
    return session.csrf_token;
  }

  return Object.freeze({
    async list(): Promise<readonly DraftVaultItem[]> {
      const response = await request(url);
      if (!response.ok) throw new Error('Impossibile caricare le Bozze.');
      const raw: unknown = await response.json();
      if (!Array.isArray(raw)) throw new Error('Elenco Bozze non valido.');
      return Object.freeze(raw.map(parseItem));
    },

    async save(
      snapshot: DraftVaultSnapshot,
      basis: Readonly<{ draftRef: string; revision: number | null; operationId: string }>,
    ): Promise<DraftVaultItem> {
      const response = await request(`${url}/${encodeURIComponent(basis.draftRef)}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 'X-Dante-CSRF': await csrf() },
        body: JSON.stringify({
          draft_ref: basis.draftRef,
          operation_id: basis.operationId,
          expected_revision: basis.revision,
          subject_kind: snapshot.fields.kind,
          title: snapshot.fields.title.trim(),
          payload: snapshot,
        }),
      });
      if (!response.ok) throw new Error(response.status === 409
        ? 'La bozza è cambiata. Riaprila e riprova.'
        : 'Non è stato possibile salvare la bozza.');
      return parseItem(await response.json());
    },

    async remove(item: DraftVaultItem): Promise<void> {
      const response = await request(
        `${url}/${encodeURIComponent(item.draftRef)}?expected_revision=${item.revision}`,
        { method: 'DELETE', headers: { 'X-Dante-CSRF': await csrf() } },
      );
      if (!response.ok) throw new Error(response.status === 409
        ? 'La bozza è cambiata. Aggiorna il box Bozze.'
        : 'Non è stato possibile eliminare la bozza.');
    },
  });
}

export const DRAFT_VAULT_UPDATED = 'dante:draft-vault-updated';

export function notifyDraftVaultUpdated(): void {
  if (typeof window !== 'undefined') window.dispatchEvent(new Event(DRAFT_VAULT_UPDATED));
}
