import { useMemo, useState } from 'react';

import type { PlanWork } from './remote-plan-work-data-source';
import { PlanCandidatePanel } from './plan-candidate-panel';
import {
  createRemotePlanConflictDataSource,
  type DiagnosticCode,
  type PlanDiagnosis,
} from './remote-plan-conflict-data-source';

const REASONS: Record<DiagnosticCode, string> = {
  unlinked_step:
    'Step senza Attività collegata: nessuna collocazione da analizzare.',
  unknown_basis:
    'Informazioni mancanti o sconosciute: non posso concludere che sia libero.',
  multiple_current_placements:
    'Più collocazioni correnti: analisi non univoca.',
  unsupported_placement:
    'Forma della collocazione non ancora supportata da questa diagnosi.',
  known_hard_violation:
    'La collocazione corrente viola un vincolo temporale hard.',
  dependency_cycle: 'Ciclo nelle Dependency: verifica le relazioni del Plan.',
  blocked_prerequisite:
    'Prerequisito non soddisfatto: lo Step dipendente è bloccato.',
  no_known_conflict_in_supported_rules:
    'Nessuna violazione nelle regole valutate.',
};

const EVALUATION = {
  satisfied: 'soddisfatta',
  unsatisfied: 'non soddisfatta',
  unknown: 'sconosciuta',
} as const;

export function PlanConflictPanel({ plan }: { plan: PlanWork }) {
  const source = useMemo(() => createRemotePlanConflictDataSource(), []);
  const [diagnosis, setDiagnosis] = useState<PlanDiagnosis | null>(null);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const inspect = () => {
    if (pending) return;
    setPending(true);
    setError(null);
    setDiagnosis(null);
    void source
      .diagnose(plan)
      .then(setDiagnosis)
      .catch((cause: unknown) =>
        setError(
          cause instanceof Error ? cause.message : 'Diagnosi non disponibile.',
        ),
      )
      .finally(() => setPending(false));
  };

  return (
    <section aria-label="Diagnosi conflitti del Plan">
      <h3>Conflitti del Plan</h3>
      <p>
        Legge la situazione corrente. Non sposta Attività e non crea Schedule.
      </p>
      <button type="button" disabled={pending} onClick={inspect}>
        {pending ? 'Analisi in corso…' : 'Analizza conflitti'}
      </button>
      {error !== null ? <p role="alert">{error}</p> : null}
      {diagnosis !== null ? (
        <div role="status">
          <p>
            Plan analizzato: {diagnosis.title}. La disponibilità e la capacità
            non sono valutate.
          </p>
          {diagnosis.steps.length === 0 ? (
            <p>Il Plan non ha Step.</p>
          ) : (
            <ol>
              {diagnosis.steps.map((step) => (
                <li key={step.stepRef}>
                  <strong>{step.title}</strong>
                  <ul>
                    {step.diagnostics.map((code) => (
                      <li key={code}>{REASONS[code]}</li>
                    ))}
                  </ul>
                  {step.dependencies.map((dependency) => (
                    <p key={dependency.dependencyRef}>
                      Dependency da{' '}
                      {plan.steps.find(
                        (item) =>
                          item.stepRef === dependency.prerequisiteStepRef,
                      )?.title ?? 'Step prerequisito'}
                      :{' '}
                      {dependency.evaluationCode === null
                        ? 'non applicabile'
                        : EVALUATION[dependency.evaluationCode]}
                      .
                    </p>
                  ))}
                  {step.activityRef !== null && step.placements?.length === 1 &&
                  step.placements[0]?.temporalFormCode === 'absolute' ? (
                    <PlanCandidatePanel plan={plan} stepRef={step.stepRef} title={step.title} />
                  ) : null}
                </li>
              ))}
            </ol>
          )}
          <small>
            “Nessuna violazione” riguarda solo le regole supportate; non prova
            che uno spazio sia libero.
          </small>
        </div>
      ) : null}
    </section>
  );
}
