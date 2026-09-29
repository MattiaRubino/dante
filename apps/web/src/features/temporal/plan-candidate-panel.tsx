import { useMemo, useState } from 'react';

import type { PlanWork } from './remote-plan-work-data-source';
import {
  createRemotePlanCandidateDataSource,
  type PlanCandidates,
} from './remote-plan-candidate-data-source';

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
  const [result, setResult] = useState<PlanCandidates | null>(null);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const search = () => {
    if (pending) return;
    setPending(true);
    setResult(null);
    setError(null);
    void source.search(plan, stepRef)
      .then(setResult)
      .catch((cause: unknown) => setError(
        cause instanceof Error ? cause.message : 'Alternative non disponibili.',
      ))
      .finally(() => setPending(false));
  };
  return (
    <div aria-label={`Alternative per ${title}`}>
      <button type="button" disabled={pending} onClick={search}>
        {pending ? 'Ricerca in corso…' : `Cerca alternative vicine per ${title}`}
      </button>
      {error !== null ? <p role="alert">{error}</p> : null}
      {result !== null ? (
        <div role="status">
          <p>Disponibilità e capacità non valutate. Queste sono solo alternative da esaminare: nessuna Schedule viene modificata.</p>
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
                </li>
              ))}
            </ol>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}
