import { useCallback, useEffect, useMemo, useState } from 'react';

import {
  createRemoteTemporalOrganizationDataSource,
  TemporalOrganizationError,
  type LifeArea,
  type OrganizationKind,
  type OrganizationSnapshot,
  type ProductTag,
} from '../../../temporal/remote-organization';
import {
  invalidateTemporalTimelineRead,
  subscribeTemporalTimelineInvalidation,
} from '../../../temporal/timeline-invalidation';
import type { TimelineGroup } from './model/timeline-types';

import './timeline-organization.css';

export const LEGACY_UNASSIGNED_GROUP = 'legacy-unassigned';

export function canonicalOrganizationGroups(snapshot: OrganizationSnapshot): readonly TimelineGroup[] {
  const areas = [...snapshot.areas].sort((a, b) => a.sortOrder - b.sortOrder);
  const groups: TimelineGroup[] = areas.map((item) => ({
    id: item.ref,
    label: item.name,
    tone: 'personal',
    hidden: item.hidden,
    archived: item.archived,
  }));
  // Legacy rows are explicit and always discoverable: never infer "Personal".
  if (snapshot.unassigned.length || snapshot.assignments.length === 0) {
    groups.push({ id: LEGACY_UNASSIGNED_GROUP, label: 'Senza Life Area', tone: 'personal' });
  }
  return Object.freeze(groups);
}

export function useTimelineOrganization(enabled: boolean) {
  const [snapshot, setSnapshot] = useState<OrganizationSnapshot | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [revision, setRevision] = useState(0);
  const source = useMemo(() => createRemoteTemporalOrganizationDataSource(), []);
  const refresh = useCallback(() => setRevision((value) => value + 1), []);

  useEffect(() => {
    if (!enabled) return;
    return subscribeTemporalTimelineInvalidation(refresh);
  }, [enabled, refresh]);

  useEffect(() => {
    if (!enabled) return;
    let cancelled = false;
    void source.load().then(
      (result) => {
        if (cancelled) return;
        setSnapshot(result);
        setError(null);
      },
      (reason: unknown) => {
        if (cancelled) return;
        setError(reason instanceof Error ? reason.message : 'Organizzazione non disponibile.');
      },
    );
    return () => { cancelled = true; };
  }, [enabled, revision, source]);

  return { snapshot, error, source, refresh } as const;
}

type Item = Readonly<{ kind: OrganizationKind; itemRef: string }>;
type Source = ReturnType<typeof createRemoteTemporalOrganizationDataSource>;

export function TimelineOrganizationPanel({
  snapshot,
  error,
  source,
  onRefresh,
  selectedItem,
}: Readonly<{
  snapshot: OrganizationSnapshot | null;
  error: string | null;
  source: Source;
  onRefresh: () => void;
  selectedItem: Item | null;
}>) {
  const [open, setOpen] = useState(false);
  const [areaName, setAreaName] = useState('');
  const [tagName, setTagName] = useState('');
  const [notice, setNotice] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  async function apply(operation: () => Promise<unknown>) {
    if (pending) return;
    setPending(true);
    setNotice(null);
    try {
      await operation();
      onRefresh();
      invalidateTemporalTimelineRead();
    } catch (reason) {
      const failure = reason instanceof TemporalOrganizationError && reason.status === 409
        ? 'I dati sono cambiati. Aggiorna e riprova.'
        : reason instanceof Error ? reason.message : 'Operazione non disponibile.';
      setNotice(failure);
      onRefresh();
    } finally {
      setPending(false);
    }
  }

  const areas = snapshot?.areas ?? [];
  const tags = snapshot?.tags ?? [];
  const chosenTags = new Set(
    snapshot?.tagEdges.filter((edge) =>
      edge.kind === selectedItem?.kind && edge.itemRef === selectedItem.itemRef,
    ).map((edge) => edge.tagRef) ?? [],
  );
  const selectedAssignment = snapshot?.assignments.find(
    (edge) => edge.kind === selectedItem?.kind && edge.itemRef === selectedItem.itemRef,
  );

  const ordered = [...areas].sort((a, b) => a.sortOrder - b.sortOrder);
  function move(area: LifeArea, delta: number) {
    const current = ordered.findIndex((item) => item.ref === area.ref);
    const next = current + delta;
    if (current < 0 || next < 0 || next >= ordered.length) return;
    const reordered = [...ordered];
    [reordered[current], reordered[next]] = [reordered[next]!, reordered[current]!];
    void apply(() => source.reorderAreas(reordered));
  }

  function renameArea(area: LifeArea) {
    const name = window.prompt('Nuovo nome Life Area', area.name)?.trim();
    if (name && name !== area.name) void apply(() => source.renameArea(area, name));
  }

  function renameTag(tag: ProductTag) {
    const name = window.prompt('Nuovo nome Tag', tag.name)?.trim();
    if (name && name !== tag.name) void apply(() => source.renameTag(tag, name));
  }

  return (
    <div className="timeline-organization">
      <button type="button" onClick={() => setOpen(!open)} aria-expanded={open} aria-controls="timeline-organization-panel">
        Life Area e Tag
      </button>
      {open && (
        <section id="timeline-organization-panel" aria-label="Organizzazione Timeline">
          {error && <p role="alert">{error} <button type="button" onClick={onRefresh}>Riprova</button></p>}
          {notice && <p role="alert">{notice}</p>}
          {!snapshot && !error && <p role="status">Caricamento Life Area…</p>}
          <h3>Life Area</h3>
          <form onSubmit={(event) => {
            event.preventDefault();
            const name = areaName.trim();
            if (!name) return;
            void apply(async () => { await source.createArea(name); setAreaName(''); });
          }}>
            <label>Nuova Life Area <input maxLength={100} value={areaName} onChange={(event) => setAreaName(event.target.value)} /></label>
            <button type="submit" disabled={pending || !snapshot}>Crea</button>
          </form>
          <ul>
            {ordered.map((area) => (
              <li key={area.ref}>
                <span>{area.name}{area.archived ? ' · archiviata' : ''}{area.hidden ? ' · nascosta' : ''}</span>
                {!area.archived && <>
                  <button type="button" disabled={pending} onClick={() => renameArea(area)} aria-label={`Rinomina ${area.name}`}>Rinomina</button>
                  <button type="button" disabled={pending} onClick={() => void apply(() => source.setAreaHidden(area, !area.hidden))} aria-label={`${area.hidden ? 'Mostra' : 'Nascondi'} ${area.name}`}>{area.hidden ? 'Mostra' : 'Nascondi'}</button>
                  <button type="button" disabled={pending} onClick={() => void apply(() => source.archiveArea(area))} aria-label={`Archivia ${area.name}`}>Archivia</button>
                </>}
                <button type="button" disabled={pending || ordered[0]?.ref === area.ref} onClick={() => move(area, -1)} aria-label={`Sposta ${area.name} prima`}>↑</button>
                <button type="button" disabled={pending || ordered.at(-1)?.ref === area.ref} onClick={() => move(area, 1)} aria-label={`Sposta ${area.name} dopo`}>↓</button>
              </li>
            ))}
          </ul>
          <h3>Tag secondari</h3>
          <form onSubmit={(event) => {
            event.preventDefault();
            const name = tagName.trim();
            if (!name) return;
            void apply(async () => { await source.createTag(name); setTagName(''); });
          }}>
            <label>Nuovo Tag <input maxLength={100} value={tagName} onChange={(event) => setTagName(event.target.value)} /></label>
            <button type="submit" disabled={pending || !snapshot}>Crea</button>
          </form>
          <ul>{tags.map((tag) => (
            <li key={tag.ref}>
              <span>{tag.name}{tag.archived ? ' · archiviato' : ''}</span>
              {!tag.archived && <>
                <button type="button" disabled={pending} onClick={() => renameTag(tag)}>Rinomina</button>
                <button type="button" disabled={pending} onClick={() => void apply(() => source.archiveTag(tag))}>Archivia</button>
              </>}
              {selectedItem && (chosenTags.has(tag.ref) || !tag.archived) && (
                <label>
                  <input type="checkbox" disabled={pending} checked={chosenTags.has(tag.ref)} onChange={(event) => void apply(() => source.setItemTag(selectedItem, tag.ref, event.target.checked))} />
                  {selectedItem.kind === 'event' ? 'Evento' : 'Attività'}: {tag.name}
                </label>
              )}
            </li>
          ))}</ul>
          {selectedItem && <section aria-label="Life Area dell’elemento">
            <h3>Life Area dell’elemento</h3>
            <label>Assegna a
              <select value={selectedAssignment?.areaRef ?? ''} disabled={pending} onChange={(event) => void apply(() => source.assignItem(selectedItem, event.target.value, selectedAssignment?.revision ?? 0))}>
                <option value="" disabled>Senza Life Area (legacy)</option>
                {areas.filter((area) => !area.archived || area.ref === selectedAssignment?.areaRef).map((area) => (
                  <option key={area.ref} value={area.ref} disabled={area.archived}>{area.name}{area.archived ? ' (archiviata)' : ''}</option>
                ))}
              </select>
            </label>
          </section>}
          {snapshot?.unassigned.length ? <section aria-label="Elementi legacy senza Life Area">
            <h3>Da organizzare ({snapshot.unassigned.length})</h3>
            <ul>{snapshot.unassigned.map((item) => (
              <li key={`${item.kind}:${item.itemRef}`}>
                <span>{item.kind === 'event' ? 'Evento' : 'Attività'} · {item.title}</span>
                <label>Assegna a
                  <select value="" disabled={pending} onChange={(event) => void apply(() => source.assignItem(item, event.target.value, 0))}>
                    <option value="" disabled>Seleziona Life Area</option>
                    {areas.filter((area) => !area.archived).map((area) => (
                      <option key={area.ref} value={area.ref}>{area.name}</option>
                    ))}
                  </select>
                </label>
              </li>
            ))}</ul>
          </section> : null}
        </section>
      )}
    </div>
  );
}
