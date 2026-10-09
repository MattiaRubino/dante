import type {
  ObjectiveComparator,
  ObjectiveKind,
  ObjectiveSeriesEditState,
  ObjectiveView,
} from '../../../temporal/remote-reality-objective-data-source';

export type ActivityObjectiveDraft = Readonly<{
  id: string;
  objectiveRef: string | null;
  operationId: string;
  revisionBasis: number | null;
  label: string;
  resultKind: ObjectiveKind;
  comparatorCode: ObjectiveComparator | null;
  targetValue: string;
  targetMin: string;
  targetMax: string;
  unitCode: string;
  presentationOrder: number;
  scope: 'only_this' | 'this_and_following';
  seriesState: ObjectiveSeriesEditState | null;
  original: ObjectiveView | null;
}>;

export function existingObjectiveDraft(view: ObjectiveView): ActivityObjectiveDraft {
  return {
    id: view.objectiveRef,
    objectiveRef: view.objectiveRef,
    operationId: crypto.randomUUID(),
    revisionBasis: null,
    label: view.label,
    resultKind: view.resultKind,
    comparatorCode: view.comparatorCode,
    targetValue: view.targetValue?.toString() ?? '',
    targetMin: view.targetMin?.toString() ?? '',
    targetMax: view.targetMax?.toString() ?? '',
    unitCode: view.unitCode ?? '',
    presentationOrder: view.presentationOrder,
    scope: 'only_this',
    seriesState: null,
    original: view,
  };
}

export function newObjectiveDraft(order: number): ActivityObjectiveDraft {
  return {
    id: crypto.randomUUID(),
    objectiveRef: null,
    operationId: crypto.randomUUID(),
    revisionBasis: null,
    label: '',
    resultKind: 'boolean',
    comparatorCode: null,
    targetValue: '',
    targetMin: '',
    targetMax: '',
    unitCode: '',
    presentationOrder: order,
    scope: 'only_this',
    seriesState: null,
    original: null,
  };
}

export function objectiveData(draft: ActivityObjectiveDraft) {
  const numeric = (value: string) =>
    value.trim() && Number.isFinite(Number(value)) ? Number(value) : null;
  const kind = draft.resultKind;
  return {
    label: draft.label.trim(),
    resultKind: kind,
    comparatorCode: kind === 'quantity' ? draft.comparatorCode ?? 'gte' :
      kind === 'range' ? 'between' as const : null,
    targetValue: kind === 'quantity' ? numeric(draft.targetValue) : null,
    targetMin: kind === 'range' ? numeric(draft.targetMin) : null,
    targetMax: kind === 'range' ? numeric(draft.targetMax) : null,
    unitCode: ['quantity', 'range'].includes(kind) ? draft.unitCode.trim() || null : null,
    presentationOrder: draft.presentationOrder,
  };
}

export function objectiveChanged(draft: ActivityObjectiveDraft): boolean {
  if (!draft.original) return true;
  const definition = objectiveData(draft);
  const original = draft.original;
  return definition.label !== original.label ||
    definition.resultKind !== original.resultKind ||
    definition.comparatorCode !== original.comparatorCode ||
    definition.targetValue !== original.targetValue ||
    definition.targetMin !== original.targetMin ||
    definition.targetMax !== original.targetMax ||
    definition.unitCode !== original.unitCode ||
    definition.presentationOrder !== original.presentationOrder;
}

export function objectiveDraftError(draft: ActivityObjectiveDraft): string | null {
  const data = objectiveData(draft);
  if (!data.label || data.label.length > 300) return 'Inserisci un nome obiettivo valido.';
  if (data.unitCode && data.unitCode.length > 40) return 'Unità di misura troppo lunga.';
  if (data.resultKind === 'quantity' &&
    (data.targetValue === null || !['eq', 'gte', 'lte'].includes(data.comparatorCode ?? ''))) {
    return 'Inserisci un valore numerico e un confronto validi.';
  }
  if (data.resultKind === 'range' &&
    (data.targetMin === null || data.targetMax === null || data.targetMin > data.targetMax)) {
    return 'L’intervallo numerico non è valido.';
  }
  return null;
}

export function ActivityObjectiveRow({
  row, disabled, onInspect, onChange, onRemove,
}: Readonly<{
  row: ActivityObjectiveDraft;
  disabled: boolean;
  onInspect: () => void;
  onChange: (patch: Partial<ActivityObjectiveDraft>) => void;
  onRemove: () => void;
}>) {
  const title = row.label.trim() || 'Nuovo obiettivo';
  return (
    <div className="timeline-activity-editor__objective-row" onFocusCapture={onInspect}>
      <div className="timeline-activity-editor__objective-head">
        <input type="text" className="timeline-activity-editor__objective-name"
          aria-label="Nome obiettivo" placeholder="Nome obiettivo"
          maxLength={300} value={row.label} disabled={disabled}
          onChange={(event) => onChange({ label: event.target.value })} />
        <button type="button" className="timeline-activity-editor__objective-remove"
          aria-label={`Rimuovi obiettivo ${title}`} title="Rimuovi obiettivo"
          onClick={onRemove} disabled={disabled}>×</button>
      </div>
      <div className="timeline-activity-editor__objective-fields">
        <label>Tipo obiettivo
          <select value={row.resultKind} disabled={disabled}
            onChange={(event) => {
              const kind = event.target.value as ObjectiveKind;
              onChange({
                resultKind: kind,
                comparatorCode: kind === 'quantity' ? 'gte' :
                  kind === 'range' ? 'between' : null,
                targetValue: '', targetMin: '', targetMax: '', unitCode: '',
              });
            }}>
            <option value="boolean">Sì / No</option>
            <option value="quantity">Quantità</option>
            <option value="qualitative">Qualitativo</option>
            <option value="range">Intervallo numerico</option>
          </select>
        </label>
        {row.resultKind === 'quantity' ? (
          <div className="timeline-activity-editor__fields">
            <label>Confronto obiettivo
              <select value={row.comparatorCode ?? 'gte'} disabled={disabled}
                onChange={(event) => onChange({
                  comparatorCode: event.target.value as ObjectiveComparator,
                })}>
                <option value="eq">Uguale a</option>
                <option value="gte">Almeno</option>
                <option value="lte">Al massimo</option>
              </select>
            </label>
            <label>Valore obiettivo
              <input type="number" step="any" value={row.targetValue} disabled={disabled}
                onChange={(event) => onChange({ targetValue: event.target.value })} />
            </label>
          </div>
        ) : null}
        {row.resultKind === 'range' ? (
          <div className="timeline-activity-editor__fields">
            <label>Minimo obiettivo
              <input type="number" step="any" value={row.targetMin} disabled={disabled}
                onChange={(event) => onChange({ targetMin: event.target.value })} />
            </label>
            <label>Massimo obiettivo
              <input type="number" step="any" value={row.targetMax} disabled={disabled}
                onChange={(event) => onChange({ targetMax: event.target.value })} />
            </label>
          </div>
        ) : null}
        {['quantity', 'range'].includes(row.resultKind) ? (
          <label>Unità di misura
            <input maxLength={40} value={row.unitCode} disabled={disabled}
              onChange={(event) => onChange({ unitCode: event.target.value })} />
          </label>
        ) : null}
        {row.seriesState ? (
          <fieldset>
            <legend>Ambito modifica obiettivo</legend>
            <label>
              <input type="radio" name={`objective-scope-${row.id}`}
                checked={row.scope === 'only_this'}
                onChange={() => onChange({ scope: 'only_this' })} />
              Solo questa
            </label>
            <label>
              <input type="radio" name={`objective-scope-${row.id}`}
                checked={row.scope === 'this_and_following'}
                onChange={() => onChange({ scope: 'this_and_following' })} />
              Questa e le prossime
            </label>
          </fieldset>
        ) : null}
        {row.original?.observationRef ? (
          <p role="status">Questo obiettivo ha risultati registrati: lo storico viene conservato e
            la rimozione non è consentita.</p>
        ) : null}
      </div>
    </div>
  );
}
