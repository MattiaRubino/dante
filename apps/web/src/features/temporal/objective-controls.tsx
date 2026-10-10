import { type FocusEvent, useCallback, useEffect, useMemo, useRef, useState } from 'react';

import {
  createRemoteRealityObjectiveDataSource,
  type ObjectiveAssessment,
  type ObjectiveInputDraftView,
  type ObjectiveInputPayload,
  type ObjectiveView,
  type RealitySubjectKind,
} from './remote-reality-objective-data-source';

import './objective-controls.css';

const newOperation = () => crypto.randomUUID();

function assessmentLabel(value: ObjectiveAssessment | null): string {
  switch (value) {
    case 'satisfied': return 'Raggiunto';
    case 'partial': return 'Parziale';
    case 'not_satisfied': return 'Non raggiunto';
    case 'indeterminate': return 'Non valutabile';
    case 'unknown': return 'Sconosciuto';
    default: return 'Da verificare';
  }
}

function targetLabel(objective: ObjectiveView): string {
  const unit = objective.unitCode ? ` ${objective.unitCode}` : '';
  if (objective.resultKind === 'quantity') {
    const comparator = objective.comparatorCode === 'gte' ? '≥'
      : objective.comparatorCode === 'lte' ? '≤' : '=';
    return `${comparator} ${objective.targetValue ?? ''}${unit}`;
  }
  if (objective.resultKind === 'range') {
    return `${objective.targetMin ?? ''}–${objective.targetMax ?? ''}${unit}`;
  }
  return objective.resultKind === 'boolean' ? 'Sì / No' : 'Valutazione';
}

function fromDraft(objective: ObjectiveView, input?: ObjectiveInputDraftView): string {
  if (!input) return '';
  if (objective.resultKind === 'boolean') {
    return input.payload.observed_boolean === true ? 'true'
      : input.payload.observed_boolean === false ? 'false' : '';
  }
  if (objective.resultKind === 'qualitative') return input.payload.qualitative_code ?? '';
  return input.payload.observed_numeric == null ? '' : String(input.payload.observed_numeric);
}

function payloadFrom(objective: ObjectiveView, value: string): ObjectiveInputPayload | null {
  if (objective.resultKind === 'boolean') {
    return value === 'true' || value === 'false'
      ? { observed_boolean: value === 'true' } : null;
  }
  if (objective.resultKind === 'qualitative') {
    if (!['satisfied', 'partial', 'not_satisfied', 'indeterminate'].includes(value)) return null;
    return {
      qualitative_code: value,
      assessment_code: value as ObjectiveAssessment,
    };
  }
  const n = Number(value);
  return value.trim() && Number.isFinite(n)
    ? { observed_numeric: n } : null;
}

function ObjectiveInputRow({
  objective, initialDraft, source, onConfirmed,
}: Readonly<{
  objective: ObjectiveView;
  initialDraft: ObjectiveInputDraftView | undefined;
  source: ReturnType<typeof createRemoteRealityObjectiveDataSource>;
  onConfirmed: () => void;
}>) {
  const [draft, setDraft] = useState(initialDraft);
  const [entry, setEntry] = useState(() => fromDraft(objective, initialDraft));
  const [busy, setBusy] = useState<'saving' | 'confirming' | null>(null);
  const [error, setError] = useState<string | null>(null);
  const lock = useRef(false);
  const confirmed = objective.observationRef !== null || draft?.confirmedAt != null;
  const validPayload = useMemo(
    () => payloadFrom(objective, entry), [objective, entry],
  );
  const savedEntry = fromDraft(objective, draft);
  const dirty = !!validPayload && entry !== savedEntry;

  const persist = useCallback(async (payload: ObjectiveInputPayload) => {
    lock.current = true;
    setBusy('saving');
    setError(null);
    try {
      const next = await source.stageObjectiveInput(
        objective.objectiveRef, payload, draft?.revision ?? null, newOperation(),
      );
      setDraft(next);
      return next;
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Bozza non salvata.');
      throw cause;
    } finally {
      lock.current = false;
      setBusy(null);
    }
  }, [draft, objective.objectiveRef, source]);

  useEffect(() => {
    if (confirmed || !dirty || !validPayload || busy !== null) return;
    const timer = window.setTimeout(() => {
      if (lock.current) return;
      void persist(validPayload).catch(() => undefined);
    }, 650);
    return () => window.clearTimeout(timer);
  }, [dirty, validPayload, confirmed, busy, persist]);

  const saveOnBlur = (event: FocusEvent<HTMLInputElement | HTMLSelectElement>) => {
    const nextFocus = event.relatedTarget as HTMLElement | null;
    if (nextFocus?.getAttribute('data-confirm-objective') === objective.objectiveRef) return;
    if (validPayload && dirty && !lock.current) {
      void persist(validPayload).catch(() => undefined);
    }
  };

  const confirm = async () => {
    if (!validPayload || lock.current || confirmed) return;
    setError(null);
    try {
      const saved = dirty || !draft
        ? await persist(validPayload)
        : draft;
      lock.current = true;
      setBusy('confirming');
      await source.confirmObjectiveInput(
        objective.objectiveRef, saved.revision, newOperation(),
      );
      onConfirmed();
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : 'Conferma non riuscita.');
    } finally {
      lock.current = false;
      setBusy(null);
    }
  };

  return (
    <div className="timeline-objective-controls__item" data-objective-ref={objective.objectiveRef}>
      <div className="timeline-objective-controls__summary">
        <span>{objective.label}</span>
        <small>{targetLabel(objective)}</small>
        <em>{assessmentLabel(objective.assessmentCode)}</em>
      </div>
      {confirmed ? (
        <small className="timeline-objective-controls__observation">
          Valore confermato · {objective.observedNumeric !== null
            ? `${objective.observedNumeric}${objective.unitCode ? ` ${objective.unitCode}` : ''}`
            : objective.observedBoolean !== null
              ? objective.observedBoolean ? 'Sì' : 'No'
              : objective.qualitativeCode
                ? assessmentLabel(objective.assessmentCode) : 'Registrato'}
        </small>
      ) : (
        <div className="timeline-objective-controls__value">
          {objective.resultKind === 'boolean' ? (
            <select aria-label={`Valore per ${objective.label}`}
              value={entry} disabled={busy !== null}
              onBlur={saveOnBlur}
              onChange={(event) => { setEntry(event.target.value); }}>
              <option value="">Scegli…</option>
              <option value="true">Sì</option>
              <option value="false">No</option>
            </select>
          ) : objective.resultKind === 'qualitative' ? (
            <select aria-label={`Valutazione per ${objective.label}`}
              value={entry} disabled={busy !== null}
              onBlur={saveOnBlur}
              onChange={(event) => { setEntry(event.target.value); }}>
              <option value="">Valuta…</option>
              <option value="satisfied">Raggiunto</option>
              <option value="partial">Parziale</option>
              <option value="not_satisfied">Non raggiunto</option>
              <option value="indeterminate">Non valutabile</option>
            </select>
          ) : (
            <>
              <input type="number" step="any" value={entry}
                disabled={busy !== null}
                onBlur={saveOnBlur}
                aria-label={`Valore reale per ${objective.label}`}
                onChange={(event) => { setEntry(event.target.value); }} />
              {objective.unitCode ? <span>{objective.unitCode}</span> : null}
            </>
          )}
          <button type="button" data-confirm-objective={objective.objectiveRef}
            title="Conferma definitivamente questo valore"
            aria-label={`Conferma obiettivo ${objective.label}`}
            disabled={!validPayload || busy !== null} onClick={() => void confirm()}>
            ✓ Conferma
          </button>
        </div>
      )}
      {!confirmed && draft && <small aria-live="polite">
        {busy === 'saving' ? 'Salvataggio bozza…'
          : busy === 'confirming' ? 'Conferma…'
          : dirty ? 'Modifica non ancora salvata'
          : 'Bozza salvata · non confermata'}
      </small>}
      {error && <small role="alert">{error}</small>}
    </div>
  );
}

export function ObjectiveControls({
  kind, subjectRef, onRecorded,
}: Readonly<{
  kind: RealitySubjectKind;
  subjectRef: string;
  onRecorded?: () => void;
}>) {
  const source = useMemo(
    () => createRemoteRealityObjectiveDataSource(globalThis.fetch), [],
  );
  const [objectives, setObjectives] = useState<readonly ObjectiveView[]>([]);
  const [drafts, setDrafts] = useState<readonly ObjectiveInputDraftView[]>([]);
  const [message, setMessage] = useState<string | null>(null);

  const reload = useCallback(async () => {
    const [items, staged] = await Promise.all([
      source.listObjectives(kind, subjectRef),
      source.listObjectiveInputDrafts(),
    ]);
    setObjectives(items);
    setDrafts(staged);
    setMessage(null);
  }, [kind, source, subjectRef]);

  useEffect(() => {
    let cancelled = false;
    void Promise.all([
      source.listObjectives(kind, subjectRef),
      source.listObjectiveInputDrafts(),
    ]).then(([items, staged]) => {
      if (cancelled) return;
      setObjectives(items);
      setDrafts(staged);
    }).catch(() => {
      if (!cancelled) setMessage('Obiettivi non disponibili.');
    });
    return () => { cancelled = true; };
  }, [kind, source, subjectRef]);

  const confirmed = () => {
    void reload().then(() => onRecorded?.()).catch(() => {
      setMessage('Risultato confermato, ma aggiornamento non disponibile.');
    });
  };

  if (objectives.length === 0 && message === null) return null;

  return (
    <section className="timeline-objective-controls"
      data-timeline-objectives={subjectRef} aria-label="Obiettivi">
      <strong>Obiettivi</strong>
      {objectives.map((objective) => (
        <ObjectiveInputRow
          key={objective.objectiveRef} objective={objective}
          initialDraft={drafts.find((d) => d.objectiveRef === objective.objectiveRef)}
          source={source} onConfirmed={confirmed}
        />
      ))}
      {message ? <span role="alert">{message}</span> : null}
    </section>
  );
}
