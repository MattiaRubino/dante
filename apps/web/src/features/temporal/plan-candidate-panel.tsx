import { useMemo, useState } from 'react';

import type { PlanWork } from './remote-plan-work-data-source';
import {
  createRemotePlanCandidateDataSource,
  type PlanCandidates,
} from './remote-plan-candidate-data-source';
import {
  createRemotePlanAdmissionDataSource,
  type Admission,
  type ReviewedAlternative,
} from './remote-plan-admission-data-source';
import { createRemotePlanReplanningSetupDataSource } from './remote-plan-replanning-setup-data-source';

const REASONS: Record<string, string> = {
  linked_absolute_schedule_required: 'Serve uno Step collegato a una sola Schedule corrente.',
  absolute_interval_required: 'La Schedule deve avere un intervallo assoluto.',
  prerequisite_unknown: 'Un prerequisito è sconosciuto. Verificalo prima di cercare alternative.',
  prerequisite_unsatisfied: 'Un prerequisito non è soddisfatto.',
  hard_rule_not_evaluable: 'Un vincolo hard non è valutabile per questi intervalli.',
  no_fixed_duration_grid_candidate: 'Nessun intervallo nel modello: 24 ore, passi di 15 minuti e durata invariata.',
  solver_unresolved: 'Il calcolo non ha dato una conclusione. Riprova.',
};

function format(iso: string): string {
  return new Intl.DateTimeFormat('it-IT', {
    dateStyle: 'medium', timeStyle: 'short',
  }).format(new Date(iso));
}

export function PlanCandidatePanel({ plan, stepRef, activityRef, title }: {
  plan: PlanWork; stepRef: string; activityRef: string; title: string;
}) {
  const source = useMemo(() => createRemotePlanCandidateDataSource(), []);
  const admissionSource = useMemo(() => createRemotePlanAdmissionDataSource(), []);
  const setupSource = useMemo(() => createRemotePlanReplanningSetupDataSource(), []);
  const [result, setResult] = useState<PlanCandidates | null>(null);
  const [selected, setSelected] = useState<ReviewedAlternative | null>(null);
  const [admission, setAdmission] = useState<Admission | null>(null);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [earliest, setEarliest] = useState('');
  const [constraintSaved, setConstraintSaved] = useState(false);
  const [policySaved, setPolicySaved] = useState(false);
  const configure = (kind: 'constraint' | 'policy') => {
    if (pending || result?.scheduleRef === null || result === null) return;
    if (kind === 'constraint' && (
      !Number.isFinite(Date.parse(earliest)) ||
      result.currentStartsAt === null ||
      Date.parse(earliest) <= Date.parse(result.currentStartsAt)
    )) {
      setError('Scegli una data e ora dopo l’inizio attuale di questa Attività.');
      return;
    }
    setPending(true);
    setError(null);
    const action = kind === 'policy'
      ? setupSource.requireConfirmation(result.scheduleRef, result.policyStateRef)
      : setupSource.setEarliestStart(activityRef, new Date(earliest).toISOString());
    void action.then(async () => {
      if (kind === 'constraint') setConstraintSaved(true);
      else setPolicySaved(true);
      setSelected(null);
      setAdmission(null);
      setResult(await source.search(plan, stepRef));
    }).catch((cause: unknown) => setError(
      cause instanceof Error ? cause.message : 'Configurazione non disponibile.',
    )).finally(() => setPending(false));
  };
  const search = () => {
    if (pending) return;
    setPending(true);
    setResult(null);
    setSelected(null);
    setAdmission(null);
    setError(null);
    void source.search(plan, stepRef)
      .then(setResult)
      .catch((cause: unknown) => setError(
        cause instanceof Error ? cause.message : 'Alternative non disponibili.',
      ))
      .finally(() => setPending(false));
  };
  const submit = (confirmation: boolean) => {
    if (pending || result === null || selected === null) return;
    if (confirmation && admission?.proposalRef === null) return;
    setPending(true);
    setError(null);
    const action = confirmation && admission?.proposalRef
      ? admissionSource.confirm(plan, stepRef, result, selected, admission.proposalRef)
      : admissionSource.request(plan, stepRef, result, selected);
    void action.then(async (value) => {
      setAdmission(value);
      if (value.kind === 'committed') {
        setSelected(null);
        setResult(null);
        setResult(await source.search(plan, stepRef));
      }
    }).catch((cause: unknown) => setError(
      cause instanceof Error ? cause.message : 'Spostamento non disponibile.',
    )).finally(() => setPending(false));
  };
  return (
    <div aria-label={`Alternative per ${title}`}>
      <button type="button" disabled={pending} onClick={search}>
        {pending ? 'Ricerca in corso…' : `Cerca alternative vicine per ${title}`}
      </button>
      {error !== null ? <p role="alert">{error}</p> : null}
      {admission?.kind === 'committed' ? (
        <p role="status">Spostamento registrato. {result?.currentStartsAt && result.currentEndsAt
          ? `Schedule attuale: ${format(result.currentStartsAt)} – ${format(result.currentEndsAt)}.`
          : 'Aggiornamento della Schedule in corso.'}</p>
      ) : null}
      {result !== null ? (
        <div role="status">
          <p>Disponibilità e capacità non valutate. La ricerca mostra alternative senza modificare la Schedule.</p>
          {typeof result.currentStartsAt === 'string' &&
          typeof result.scheduleRef === 'string' ? (
            <section aria-label={`Regole di spostamento per ${title}`}>
              <h4>Regole per {title}</h4>
              <p>Inizio attuale: {format(result.currentStartsAt)}.</p>
              <label>Inizio non prima di{' '}
                <input type="datetime-local" value={earliest}
                  onChange={(event) => setEarliest(event.currentTarget.value)} />
              </label>{' '}
              <button type="button" disabled={pending || constraintSaved}
                onClick={() => configure('constraint')}>Imposta vincolo hard</button>
              {constraintSaved ? <p>Vincolo registrato. Riesegui Analizza conflitti per leggere la situazione corrente.</p> : null}
              {result.movementPolicyStatus !== 'automatic' ? (
                <button type="button" disabled={pending} onClick={() => configure('policy')}>
                  Consenti spostamento con conferma
                </button>
              ) : null}
              {policySaved ? <p>Movement Policy registrata con conferma esplicita.</p> : null}
            </section>
          ) : null}
          {result.movementPolicyStatus !== 'automatic' ? (
            <p>Movement Policy: {result.movementPolicyStatus === 'blocked' ? 'movimento automatico bloccato' : 'non presente'}.</p>
          ) : null}
          {result.basisStatus !== 'supported' || result.solverStatus !== 'OPTIMAL' ? (
            <p>{REASONS[result.reasonCode] ?? 'Il risultato non è conclusivo per le regole supportate.'}</p>
          ) : null}
          {result.candidates.length > 0 ? (
            <ol>
              {result.candidates.map((item) => (
                <li key={item.startsAt}>
                  {format(item.startsAt)} – {format(item.endsAt)}
                  {item.softViolations > 0 ? ` · ${item.softViolations} vincoli soft non soddisfatti` : ''}
                  {result.policyStateRef !== null &&
                  result.movementPolicyStatus === 'automatic' &&
                  result.solverStatus === 'OPTIMAL' ? (
                    <button type="button" disabled={pending || admission !== null}
                      onClick={() => {
                        setSelected({
                          startsAt: item.startsAt, endsAt: item.endsAt,
                          operationId: crypto.randomUUID(),
                        });
                        setAdmission(null);
                      }}>
                      Rivedi questa alternativa
                    </button>
                  ) : null}
                </li>
              ))}
            </ol>
          ) : null}
          {selected !== null ? (
            <section aria-label={`Revisione spostamento per ${title}`}>
              <h4>Rivedi lo spostamento di {title}</h4>
              <p>Attuale: {result.currentStartsAt ? format(result.currentStartsAt) : 'sconosciuto'} – {result.currentEndsAt ? format(result.currentEndsAt) : 'sconosciuto'}</p>
              <p>Alternativa: {format(selected.startsAt)} – {format(selected.endsAt)}</p>
              <p>Disponibilità e capacità non valutate. Lo spostamento sarà ricontrollato prima dell’effetto.</p>
              {admission?.kind === 'pending_confirmation' ? (
                <>
                  <p>Proposta in attesa: la Schedule non è cambiata.</p>
                  <button type="button" disabled={pending} onClick={() => submit(true)}>
                    {pending ? 'Conferma in corso…' : 'Conferma lo spostamento'}
                  </button>
                </>
              ) : (
                <button type="button" disabled={pending} onClick={() => submit(false)}>
                  {pending ? 'Invio in corso…' : 'Richiedi questo spostamento'}
                </button>
              )}
            </section>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}
