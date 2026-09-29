import { useMemo, useState } from 'react';
import type { PlanStep, PlanWork } from './remote-plan-work-data-source';
import {
  createRemotePlanExecutionDataSource,
  type ExecutionAssessment,
} from './remote-plan-execution-data-source';

type DraftSlice = { ref: string; start: string; end: string };

export function PlanExecutionPanel({
  plan, pending, update,
}: {
  plan: PlanWork;
  pending: boolean;
  update: (stepRef: string, policy: Pick<PlanStep,
    'divisible' | 'maxPlannedSlices' | 'mergeCompatible' | 'executionStrengthCode'>) => void;
}) {
  const source = useMemo(() => createRemotePlanExecutionDataSource(), []);
  const linked = plan.steps.filter((item) => item.activityRef !== null);
  const [stepRef, setStepRef] = useState(linked[0]?.stepRef ?? '');
  const selected = linked.find((item) => item.stepRef === stepRef) ?? linked[0];
  const [divisible, setDivisible] = useState(linked[0]?.divisible ?? true);
  const [maximum, setMaximum] = useState(linked[0]?.maxPlannedSlices?.toString() ?? '');
  const [merge, setMerge] = useState(linked[0]?.mergeCompatible ?? false);
  const [strength, setStrength] = useState<'hard' | 'soft'>(
    linked[0]?.executionStrengthCode ?? 'hard',
  );
  const [slices, setSlices] = useState<DraftSlice[]>([]);
  const [pair, setPair] = useState(false);
  const [assessment, setAssessment] = useState<ExecutionAssessment | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [evaluating, setEvaluating] = useState(false);

  const select = (ref: string) => {
    setStepRef(ref);
    const item = linked.find((candidate) => candidate.stepRef === ref);
    setDivisible(item?.divisible ?? true);
    setMaximum(item?.maxPlannedSlices?.toString() ?? '');
    setMerge(item?.mergeCompatible ?? false);
    setStrength(item?.executionStrengthCode ?? 'hard');
    setAssessment(null);
  };
  const save = () => {
    if (selected === undefined) return;
    const count = maximum === '' ? null : Number(maximum);
    if ((divisible && count !== null && (!Number.isInteger(count) || count < 2 || count > 100)) ||
        (!divisible && (merge || count !== 1))) {
      setError('Limite incoerente: indivisibile richiede massimo 1 e nessuna unione; divisibile richiede almeno 2.');
      return;
    }
    setError(null);
    update(selected.stepRef, {
      divisible, maxPlannedSlices: count, mergeCompatible: merge,
      executionStrengthCode: strength,
    });
  };
  const assess = () => {
    if (selected === undefined || evaluating) return;
    let proposed;
    try {
      proposed = slices.map((item) => ({
        sliceRef: item.ref,
        startsAt: new Date(item.start).toISOString(),
        endsAt: new Date(item.end).toISOString(),
      }));
    } catch {
      setError('Inserisci date valide per ogni segmento.');
      return;
    }
    if (proposed.some((item) => item.endsAt <= item.startsAt)) {
      setError('Ogni segmento richiede una fine successiva all’inizio.');
      return;
    }
    setEvaluating(true);
    setError(null);
    setAssessment(null);
    void source.assess(plan, selected.stepRef, proposed,
      pair && proposed.length >= 2 ? [proposed[0]!.sliceRef, proposed[1]!.sliceRef] : null)
      .then(setAssessment)
      .catch((cause: unknown) => setError(cause instanceof Error ? cause.message : 'Valutazione non riuscita.'))
      .finally(() => setEvaluating(false));
  };
  return (
    <section aria-label="Struttura di esecuzione del Plan">
      <h3>Struttura di esecuzione</h3>
      <p>La policy vale soltanto per lo Step di questo Plan. I segmenti proposti non sono Session registrate né Schedule accettate.</p>
      {selected === undefined ? <p>Collega uno Step a un’Attività per configurare l’esecuzione.</p> : <>
        <label>Step collegato
          <select value={selected.stepRef} onChange={(event) => select(event.currentTarget.value)}>
            {linked.map((item) => <option key={item.stepRef} value={item.stepRef}>{item.title}</option>)}
          </select>
        </label>
        <p>Policy corrente: {selected.divisible === null ? 'non configurata' :
          `${selected.divisible ? 'divisibile' : 'indivisibile'}, massimo ${selected.maxPlannedSlices ?? 'senza limite'}, ` +
          `unione ${selected.mergeCompatible ? 'consentita' : 'vietata'}, ${selected.executionStrengthCode}`}</p>
        <label><input type="checkbox" checked={divisible} disabled={pending}
          onChange={(event) => {
            setDivisible(event.currentTarget.checked);
            if (!event.currentTarget.checked) { setMaximum('1'); setMerge(false); }
          }} />Divisibile</label>
        <label>Massimo segmenti proposti (vuoto = senza limite)
          <input type="number" min={divisible ? 2 : 1} max={100} value={maximum}
            disabled={pending || !divisible} onChange={(event) => setMaximum(event.currentTarget.value)} />
        </label>
        <label><input type="checkbox" checked={merge} disabled={pending || !divisible}
          onChange={(event) => setMerge(event.currentTarget.checked)} />Consenti unione di segmenti contigui compatibili</label>
        <label>Forza
          <select value={strength} disabled={pending}
            onChange={(event) => setStrength(event.currentTarget.value as 'hard' | 'soft')}>
            <option value="hard">Hard</option><option value="soft">Soft</option>
          </select>
        </label>
        <button type="button" disabled={pending} onClick={save}>Salva policy nello Step</button>
        {selected.divisible !== null ? <button type="button" disabled={pending}
          onClick={() => update(selected.stepRef, {
            divisible: null, maxPlannedSlices: null, mergeCompatible: null,
            executionStrengthCode: null,
          })}>Ritira policy</button> : null}
        <h4>Valuta segmenti proposti</h4>
        {slices.map((item, index) => <div key={item.ref}>
          <span>Segmento {index + 1}</span>
          <label>Inizio <input type="datetime-local" value={item.start}
            onChange={(event) => setSlices(slices.map((row) => row.ref === item.ref
              ? { ...row, start: event.currentTarget.value } : row))} /></label>
          <label>Fine <input type="datetime-local" value={item.end}
            onChange={(event) => setSlices(slices.map((row) => row.ref === item.ref
              ? { ...row, end: event.currentTarget.value } : row))} /></label>
          <button type="button" onClick={() => setSlices(slices.filter((row) => row.ref !== item.ref))}>Rimuovi</button>
        </div>)}
        <button type="button" disabled={slices.length >= 100}
          onClick={() => setSlices([...slices, { ref: crypto.randomUUID(), start: '', end: '' }])}>
          Aggiungi segmento
        </button>
        <label><input type="checkbox" checked={pair} disabled={slices.length < 2}
          onChange={(event) => setPair(event.currentTarget.checked)} />Valuta unione dei primi due</label>
        <button type="button" disabled={evaluating || slices.some((item) => !item.start || !item.end)}
          onClick={assess}>Valuta proposta</button>
        {assessment !== null ? <div role="status">
          <p>Snapshot proposto: {assessment.proposedCount} segmenti. Limite: {assessment.countStatus} ({assessment.countReason}).</p>
          <p>Unione: {assessment.mergeStatus} ({assessment.mergeReason}){assessment.mergedTemporalStatus
            ? `; Temporal Constraint: ${assessment.mergedTemporalStatus}` : ''}.</p>
          <ul>{assessment.mergedTemporalRules.map((rule) => <li key={rule.constraintRef}>
            Unione · {rule.strength} · {rule.constrainedFacet} · {rule.evaluation} ({rule.reasonCode})
          </li>)}</ul>
          <ul>{assessment.sliceAssessments.map((item, index) => <li key={item.sliceRef}>
            Segmento {index + 1}: Temporal Constraint {item.temporalStatus}
            <ul>{item.temporalRules.map((rule) => <li key={rule.constraintRef}>
              {rule.strength} · {rule.constrainedFacet} · {rule.evaluation} ({rule.reasonCode})
            </li>)}</ul>
          </li>)}</ul>
        </div> : null}
      </>}
      <p>Durata e altri vincoli temporali dell’Attività si configurano nei Temporal Constraint. Spaziatura, preparazione e recupero non sono editabili qui.</p>
      {error !== null ? <p role="alert">{error}</p> : null}
    </section>
  );
}
