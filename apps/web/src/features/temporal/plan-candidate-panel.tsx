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

export function PlanCandidatePanel({ plan, stepRef, title }: {
  plan: PlanWork; stepRef: string; title: string;
}) {
  const source = useMemo(() => createRemotePlanCandidateDataSource(), []);
  const admissionSource = useMemo(() => createRemotePlanAdmissionDataSource(), []);
  const [result, setResult] = useState<PlanCandidates | null>(null);
  const [selected, setSelected] = useState<ReviewedAlternative | null>(null);
  const [admission, setAdmission] = useState<Admission | null>(null);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);
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
          {result.movementPolicyStatus !== 'automatic' ? (
            <p>Movement Policy: {result.movementPolicyStatus === 'blocked' ? 'movimento automatico bloccato' : 'non presente'}. Ogni eventuale modifica richiede una verifica separata.</p>
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
