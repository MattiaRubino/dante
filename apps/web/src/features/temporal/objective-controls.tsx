import { useCallback, useEffect, useMemo, useState } from 'react';

import {
  createRemoteRealityObjectiveDataSource,
  type ObjectiveAssessment,
  type ObjectiveView,
  type RealitySubjectKind,
} from './remote-reality-objective-data-source';

import './objective-controls.css';

function operationId(): string {
  return crypto.randomUUID();
}

function assessmentLabel(value: ObjectiveAssessment | null): string {
  switch (value) {
    case 'satisfied':
      return 'Raggiunto';
    case 'partial':
      return 'Parziale';
    case 'not_satisfied':
      return 'Non raggiunto';
    case 'indeterminate':
      return 'Non valutabile';
    case 'unknown':
      return 'Sconosciuto';
    default:
      return 'Da verificare';
  }
}

function targetLabel(objective: ObjectiveView): string {
  const unit = objective.unitCode ? ` ${objective.unitCode}` : '';
  if (objective.resultKind === 'quantity') {
    const comparator =
      objective.comparatorCode === 'gte'
        ? '≥'
        : objective.comparatorCode === 'lte'
          ? '≤'
          : '=';
    return `${comparator} ${objective.targetValue ?? ''}${unit}`;
  }
  if (objective.resultKind === 'range') {
    return `${objective.targetMin ?? ''}–${objective.targetMax ?? ''}${unit}`;
  }
  if (objective.resultKind === 'boolean') return 'Sì / No';
  return 'Valutazione';
}

export function ObjectiveControls({
  kind,
  subjectRef,
  onRecorded,
}: Readonly<{
  kind: RealitySubjectKind;
  subjectRef: string;
  onRecorded?: () => void;
}>) {
  const source = useMemo(
    () => createRemoteRealityObjectiveDataSource(globalThis.fetch),
    [],
  );
  const [objectives, setObjectives] = useState<readonly ObjectiveView[]>([]);
  const [values, setValues] = useState<Record<string, string>>({});
  const [pendingRef, setPendingRef] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const reload = useCallback(async () => {
    const items = await source.listObjectives(kind, subjectRef);
    setObjectives(items);
  }, [kind, source, subjectRef]);

  useEffect(() => {
    let cancelled = false;
    void source
      .listObjectives(kind, subjectRef)
      .then((items) => {
        if (!cancelled) setObjectives(items);
      })
      .catch(() => {
        if (!cancelled) setMessage('Obiettivi non disponibili.');
      });
    return () => {
      cancelled = true;
    };
  }, [kind, source, subjectRef]);

  const save = (
    objective: ObjectiveView,
    command: Parameters<typeof source.recordResult>[1],
  ) => {
    setPendingRef(objective.objectiveRef);
    setMessage(null);
    void source
      .recordResult(objective.objectiveRef, command)
      .then(() => reload())
      .then(() => onRecorded?.())
      .catch((error: unknown) =>
        setMessage(
          error instanceof Error
            ? error.message
            : 'Risultato obiettivo non salvato.',
        ),
      )
      .finally(() => setPendingRef(null));
  };

  if (objectives.length === 0 && message === null) return null;

  return (
    <section
      className="timeline-objective-controls"
      data-timeline-objectives={subjectRef}
      aria-label="Obiettivi"
    >
      <strong>Obiettivi</strong>
      {objectives.map((objective) => {
        const pending = pendingRef === objective.objectiveRef;
        const currentValue = values[objective.objectiveRef] ?? '';
        return (
          <div className="timeline-objective-controls__item" key={objective.objectiveRef}>
            <div className="timeline-objective-controls__summary">
              <span>{objective.label}</span>
              <small>{targetLabel(objective)}</small>
              <em>{assessmentLabel(objective.assessmentCode)}</em>
            </div>

            {objective.resultKind === 'boolean' ? (
              <div className="timeline-objective-controls__actions">
                <button
                  type="button"
                  disabled={pending}
                  onClick={() =>
                    save(objective, {
                      operationId: operationId(),
                      observedBoolean: true,
                    })
                  }
                >
                  Sì
                </button>
                <button
                  type="button"
                  disabled={pending}
                  onClick={() =>
                    save(objective, {
                      operationId: operationId(),
                      observedBoolean: false,
                    })
                  }
                >
                  No
                </button>
              </div>
            ) : null}

            {objective.resultKind === 'quantity' ||
            objective.resultKind === 'range' ? (
              <div className="timeline-objective-controls__value">
                <input
                  type="number"
                  step="any"
                  value={currentValue}
                  aria-label={`Valore reale per ${objective.label}`}
                  onChange={(event) => {
                    const value = event.currentTarget.value;
                    setValues((current) => ({
                      ...current,
                      [objective.objectiveRef]: value,
                    }));
                  }}
                />
                {objective.unitCode ? <span>{objective.unitCode}</span> : null}
                <button
                  type="button"
                  disabled={pending || currentValue.trim() === '' || !Number.isFinite(Number(currentValue))}
                  onClick={() =>
                    save(objective, {
                      operationId: operationId(),
                      observedNumeric: Number(currentValue),
                    })
                  }
                >
                  Registra
                </button>
              </div>
            ) : null}

            {objective.resultKind === 'qualitative' ? (
              <select
                aria-label={`Valutazione per ${objective.label}`}
                disabled={pending}
                value=""
                onChange={(event) => {
                  const assessment = event.currentTarget
                    .value as ObjectiveAssessment;
                  if (!assessment) return;
                  save(objective, {
                    operationId: operationId(),
                    qualitativeCode: assessment,
                    assessmentCode: assessment,
                  });
                }}
              >
                <option value="">Valuta…</option>
                <option value="satisfied">Raggiunto</option>
                <option value="partial">Parziale</option>
                <option value="not_satisfied">Non raggiunto</option>
                <option value="indeterminate">Non valutabile</option>
              </select>
            ) : null}

            {objective.observationRef !== null ? (
              <small className="timeline-objective-controls__observation">
                {objective.observedNumeric !== null
                  ? `Valore reale: ${objective.observedNumeric}${objective.unitCode ? ` ${objective.unitCode}` : ''}`
                  : objective.observedBoolean !== null
                    ? `Valore reale: ${objective.observedBoolean ? 'Sì' : 'No'}`
                    : objective.qualitativeCode !== null
                      ? `Valutazione registrata: ${assessmentLabel(objective.assessmentCode)}`
                      : null}
              </small>
            ) : null}
          </div>
        );
      })}
      {message ? <span role="alert">{message}</span> : null}
    </section>
  );
}
