import { useCallback, useEffect, useMemo, useState } from 'react';

import './advanced-recurrence-controls.css';

import {
  createRemoteTemporalAdvancedRecurrenceDataSource,
  type AdvancedRecurrenceAnchorMode,
  type AdvancedRecurrenceAnchorSourceKind,
  type AdvancedRecurrenceOwnerKind,
  type AdvancedRecurrenceView,
} from './remote-advanced-recurrence-data-source';

function operationId(): string {
  return crypto.randomUUID();
}

function rejection(fallback: string, error: unknown): string {
  if (error instanceof Error && error.message.trim()) return `${fallback} ${error.message}`;
  return fallback;
}

function localDateTime(value: string): string {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '';
  const offset = date.getTimezoneOffset() * 60_000;
  return new Date(date.getTime() - offset).toISOString().slice(0, 16);
}

function initialDateTime(): string {
  return localDateTime(new Date().toISOString());
}

export function AdvancedRecurrenceControls({
  ownerKind,
  sourceRef,
}: Readonly<{ ownerKind: AdvancedRecurrenceOwnerKind; sourceRef: string }>) {
  const source = useMemo(
    () => createRemoteTemporalAdvancedRecurrenceDataSource(globalThis.fetch),
    [],
  );
  const [currentStateRef, setCurrentStateRef] = useState<string | null>(null);
  const [advanced, setAdvanced] = useState<AdvancedRecurrenceView | null>(null);
  const [loaded, setLoaded] = useState(false);
  const [pending, setPending] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [mode, setMode] = useState<AdvancedRecurrenceAnchorMode>('previous_completion');
  const [delay, setDelay] = useState('3600');
  const [effectiveFrom, setEffectiveFrom] = useState(initialDateTime);
  const [anchorFamily, setAnchorFamily] =
    useState<AdvancedRecurrenceAnchorSourceKind>('routine');
  const [anchorRef, setAnchorRef] = useState('');

  const applyLoaded = useCallback((value: AdvancedRecurrenceView | null, stateRef: string | null) => {
    setCurrentStateRef(stateRef);
    setAdvanced(value);
    setLoadError(null);
    if (value !== null) {
      setMode(value.anchorModeCode);
      setDelay(value.elapsedSeconds);
      setEffectiveFrom(localDateTime(value.effectiveFrom));
      setAnchorFamily(value.anchorSourceFamily ?? 'routine');
      setAnchorRef(value.anchorSourceNativeRef ?? '');
    }
    setLoaded(true);
  }, []);

  const reload = useCallback(async () => {
    const result = await source.load(ownerKind, sourceRef);
    applyLoaded(result.advanced, result.currentMaterialStateRef);
    return result;
  }, [applyLoaded, ownerKind, source, sourceRef]);

  useEffect(() => {
    let cancelled = false;
    setLoaded(false);
    setLoadError(null);
    setMessage(null);
    void source
      .load(ownerKind, sourceRef)
      .then((result) => {
        if (!cancelled) applyLoaded(result.advanced, result.currentMaterialStateRef);
      })
      .catch((error: unknown) => {
        if (!cancelled) {
          setLoaded(true);
          setLoadError(rejection('Recurrence avanzata non disponibile.', error));
        }
      });
    return () => {
      cancelled = true;
    };
  }, [applyLoaded, ownerKind, source, sourceRef]);

  const save = () => {
    if (currentStateRef === null) {
      setMessage('Questa sorgente non ha una Recurrence canonica da convertire.');
      return;
    }
    if (!delay.trim() || Number(delay) <= 0) {
      setMessage('Il ritardo deve essere maggiore di zero.');
      return;
    }
    const instant = new Date(effectiveFrom);
    if (!effectiveFrom || Number.isNaN(instant.getTime())) {
      setMessage('Imposta un inizio valido per la Recurrence.');
      return;
    }
    if (mode === 'anchor_stream' && anchorRef.trim().length === 0) {
      setMessage('La Recurrence anchor-stream richiede il riferimento della sorgente anchor.');
      return;
    }

    setPending(true);
    setMessage(null);
    void source
      .replace(ownerKind, sourceRef, {
        operationId: operationId(),
        expectedMaterialStateRef: currentStateRef,
        effectiveFrom: instant.toISOString(),
        elapsedSeconds: delay.trim(),
        anchorModeCode: mode,
        anchorSourceFamily: mode === 'anchor_stream' ? anchorFamily : null,
        anchorSourceNativeRef: mode === 'anchor_stream' ? anchorRef.trim() : null,
      })
      .then((saved) => {
        applyLoaded(saved, saved.materialStateRef);
        setMessage('Recurrence avanzata salvata.');
      })
      .catch((error: unknown) =>
        reload()
          .catch(() => undefined)
          .then(() => setMessage(rejection('Aggiornamento Recurrence rifiutato.', error))),
      )
      .finally(() => setPending(false));
  };

  const state = !loaded
    ? 'Recurrence avanzata: caricamento…'
    : loadError !== null
      ? 'Recurrence avanzata: lettura non disponibile'
    : currentStateRef === null
      ? 'Recurrence avanzata: sorgente non ricorrente'
      : advanced === null
        ? 'Recurrence avanzata: non configurata'
        : advanced.anchorModeCode === 'previous_completion'
          ? `Recurrence avanzata: dopo il completamento · ${advanced.elapsedSeconds}s`
          : `Recurrence avanzata: anchor stream · ${advanced.elapsedSeconds}s`;

  return (
    <section className="timeline-advanced-recurrence" data-advanced-recurrence-owner={`${ownerKind}:${sourceRef}`}>
      <strong>Recurrence avanzata</strong>
      <p data-advanced-recurrence-state>{state}</p>
      <label>
        Regola
        <select
          aria-label="Regola Recurrence avanzata"
          value={mode}
          disabled={pending || !loaded || currentStateRef === null}
          onChange={(event) => setMode(event.currentTarget.value as AdvancedRecurrenceAnchorMode)}
        >
          <option value="previous_completion">Dopo il completamento precedente</option>
          <option value="anchor_stream">Dopo un'altra Routine / Event</option>
        </select>
      </label>
      <label>
        Ritardo (secondi)
        <input
          aria-label="Ritardo Recurrence avanzata in secondi"
          type="number"
          min="0.000001"
          step="0.000001"
          value={delay}
          disabled={pending || !loaded || currentStateRef === null}
          onChange={(event) => setDelay(event.currentTarget.value)}
        />
      </label>
      <label>
        Attiva da
        <input
          aria-label="Inizio Recurrence avanzata"
          type="datetime-local"
          value={effectiveFrom}
          disabled={pending || !loaded || currentStateRef === null}
          onChange={(event) => setEffectiveFrom(event.currentTarget.value)}
        />
      </label>
      {mode === 'anchor_stream' ? (
        <div className="timeline-advanced-recurrence__anchor">
          <label>
            Tipo anchor
            <select
              aria-label="Tipo sorgente anchor"
              value={anchorFamily}
              disabled={pending || !loaded || currentStateRef === null}
              onChange={(event) =>
                setAnchorFamily(event.currentTarget.value as AdvancedRecurrenceAnchorSourceKind)
              }
            >
              <option value="routine">Routine</option>
              <option value="event">Event</option>
            </select>
          </label>
          <label>
            Riferimento anchor
            <input
              aria-label="Riferimento sorgente anchor"
              value={anchorRef}
              disabled={pending || !loaded || currentStateRef === null}
              onChange={(event) => setAnchorRef(event.currentTarget.value)}
              placeholder="UUID della Routine o Event"
            />
          </label>
        </div>
      ) : null}
      <button
        type="button"
        disabled={pending || !loaded || currentStateRef === null}
        onClick={save}
      >
        Salva Recurrence avanzata
      </button>
      <small>
        La regola usa solo completamenti Actual. Le Occurrence già materializzate mantengono
        l'Actual MaterialState che le ha generate anche dopo una correzione successiva.
      </small>
      {loadError === null ? null : <span role="alert">{loadError}</span>}
      {message === null ? null : message === 'Recurrence avanzata salvata.' ? (
        <span role="status">{message}</span>
      ) : (
        <span role="alert">{message}</span>
      )}
    </section>
  );
}
