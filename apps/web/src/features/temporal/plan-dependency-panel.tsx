import { useEffect, useMemo, useRef, useState } from 'react';

import type { PlanWork } from './remote-plan-work-data-source';
import {
  createRemotePlanDependencyDataSource,
  type PlanDependency,
  type PlanDependencyIntent,
} from './remote-plan-dependency-data-source';

function message(error: unknown): string {
  return error instanceof Error && error.message.trim()
    ? error.message : 'Operazione Dependency non riuscita.';
}

const EVALUATION: Record<NonNullable<PlanDependency['evaluationCode']>, string> = {
  satisfied: 'soddisfatta',
  unsatisfied: 'non soddisfatta',
  unknown: 'sconosciuta',
};

export function PlanDependencyPanel({ plan }: { plan: PlanWork }) {
  const source = useMemo(() => createRemotePlanDependencyDataSource(), []);
  const [items, setItems] = useState<readonly PlanDependency[]>([]);
  const [selectedRef, setSelectedRef] = useState('');
  const [prerequisite, setPrerequisite] = useState('');
  const [dependent, setDependent] = useState('');
  const [kind, setKind] = useState<PlanDependencyIntent['qualifierCode']>('actual_occurred');
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(true);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const attempt = useRef<{ fingerprint: string; id: string } | null>(null);
  const linked = plan.steps.filter((step) => step.activityRef !== null);
  const selected = items.find((item) => item.dependencyRef === selectedRef && item.active);

  const reload = async () => {
    const next = await source.list(plan.planRef);
    setItems(next);
    return next;
  };

  useEffect(() => {
    let active = true;
    void source.list(plan.planRef).then((next) => {
      if (!active) return;
      setItems(next);
      setLoading(false);
    }).catch((cause: unknown) => {
      if (active) {
        setError(message(cause));
        setLoading(false);
      }
    });
    return () => { active = false; };
  }, [plan.planRef, plan.stateRef, source]);

  const select = (ref: string) => {
    setSelectedRef(ref);
    const item = items.find((candidate) => candidate.dependencyRef === ref);
    setPrerequisite(item?.prerequisiteStepRef ?? '');
    setDependent(item?.dependentStepRef ?? '');
    setKind(item?.qualifierCode ?? 'actual_occurred');
    setCode(item?.dispositionCode ?? '');
    attempt.current = null;
  };

  const intent: PlanDependencyIntent = {
    prerequisiteStepRef: prerequisite,
    dependentStepRef: dependent,
    qualifierCode: kind,
    dispositionCode: kind === 'outcome_code' ? code : null,
  };
  const admissible = prerequisite !== '' && dependent !== '' &&
    prerequisite !== dependent &&
    linked.some((step) => step.stepRef === prerequisite) &&
    linked.some((step) => step.stepRef === dependent) &&
    (kind === 'actual_occurred' || /^[a-z0-9][a-z0-9._:-]{0,119}$/.test(code));

  const run = (
    action: 'create' | 'revise' | 'retire',
    current: PlanDependency | undefined,
  ) => {
    if (pending || (action !== 'retire' && !admissible) ||
        (action !== 'create' && current === undefined)) return;
    const fingerprint = JSON.stringify([
      action, plan.planRef, current?.dependencyRef, current?.stateRef, intent,
    ]);
    const prior = attempt.current;
    const id = prior?.fingerprint === fingerprint ? prior.id : crypto.randomUUID();
    attempt.current = { fingerprint, id };
    setPending(true);
    setError(null);
    setStatus(null);
    void (async () => {
      try {
        const result = action === 'create'
          ? await source.create(plan.planRef, intent, id)
          : await source.revise(current!, {
            prerequisiteStepRef: current!.prerequisiteStepRef,
            dependentStepRef: current!.dependentStepRef,
            qualifierCode: action === 'retire' ? current!.qualifierCode : kind,
            dispositionCode: action === 'retire' ? current!.dispositionCode : intent.dispositionCode,
          }, action !== 'retire', id);
        attempt.current = null;
        await reload();
        setSelectedRef(result.active ? result.dependencyRef : '');
        setStatus(action === 'retire' ? 'Dependency ritirata.' :
          action === 'revise' ? 'Condizione aggiornata.' : 'Dependency creata.');
      } catch (cause) {
        setError(message(cause));
      } finally {
        setPending(false);
      }
    })();
  };

  return (
    <section className="plan-dependency-panel" aria-label="Dependency qualificate del Plan">
      <h3>Dependency qualificate</h3>
      <p>Le condizioni riguardano le Attività collegate agli Step di questo Plan.</p>
      <button type="button" disabled={pending} onClick={() => {
        void reload().then(() => setError(null)).catch((cause: unknown) =>
          setError(message(cause)));
      }}>Ricarica Dependency</button>
      {loading ? <p>Caricamento Dependency…</p> : (
        <>
          <ul>
            {items.filter((item) => item.active).map((item) => {
              const before = plan.steps.find((step) => step.stepRef === item.prerequisiteStepRef);
              const after = plan.steps.find((step) => step.stepRef === item.dependentStepRef);
              return (
                <li key={item.dependencyRef}>
                  <strong>{before?.title ?? 'Step'} → {after?.title ?? 'Step'}</strong>
                  <span> · {item.qualifierCode === 'actual_occurred'
                    ? 'Actual avvenuto' : `Outcome = ${item.dispositionCode}`}</span>
                  <span> · {item.evaluationCode === null ? 'non applicabile'
                    : EVALUATION[item.evaluationCode]}</span>
                  {item.cycle ? <span> · Ciclo nel Plan</span> : null}
                  <button type="button" disabled={pending}
                    onClick={() => select(item.dependencyRef)}>Modifica</button>
                </li>
              );
            })}
          </ul>
          {linked.length < 2 ? (
            <p>Collega almeno due Step ad Attività distinte per creare una Dependency.</p>
          ) : (
            <>
              {selected !== undefined ? (
                <p>Modifica la condizione della relazione selezionata.</p>
              ) : null}
              <label>
                Step prerequisito
                <select value={prerequisite} disabled={pending || selected !== undefined}
                  onChange={(event) => setPrerequisite(event.currentTarget.value)}>
                  <option value="">Seleziona Step</option>
                  {linked.map((step) => (
                    <option key={step.stepRef} value={step.stepRef}>{step.title}</option>
                  ))}
                </select>
              </label>
              <label>
                Step dipendente
                <select value={dependent} disabled={pending || selected !== undefined}
                  onChange={(event) => setDependent(event.currentTarget.value)}>
                  <option value="">Seleziona Step</option>
                  {linked.map((step) => (
                    <option key={step.stepRef} value={step.stepRef}>{step.title}</option>
                  ))}
                </select>
              </label>
              <label>
                Condizione prerequisita
                <select value={kind} disabled={pending}
                  onChange={(event) =>
                    setKind(event.currentTarget.value as PlanDependencyIntent['qualifierCode'])}>
                  <option value="actual_occurred">Actual avvenuto</option>
                  <option value="outcome_code">Outcome con codice esatto</option>
                </select>
              </label>
              {kind === 'outcome_code' ? (
                <label>
                  Codice Outcome
                  <input value={code} maxLength={120} disabled={pending}
                    onChange={(event) => setCode(event.currentTarget.value)} />
                </label>
              ) : null}
              {selected === undefined ? (
                <button type="button" disabled={pending || !admissible}
                  onClick={() => run('create', undefined)}>Crea Dependency</button>
              ) : (
                <>
                  <button type="button" disabled={pending || !admissible}
                    onClick={() => run('revise', selected)}>Aggiorna condizione</button>
                  <button type="button" disabled={pending}
                    onClick={() => run('retire', selected)}>Ritira Dependency</button>
                  <button type="button" disabled={pending} onClick={() => select('')}>
                    Nuova Dependency
                  </button>
                </>
              )}
            </>
          )}
        </>
      )}
      {error !== null ? <p role="alert">{error}</p> : null}
      {status !== null ? <p role="status">{status}</p> : null}
    </section>
  );
}
