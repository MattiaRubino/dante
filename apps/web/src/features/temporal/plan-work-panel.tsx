import { useEffect, useMemo, useRef, useState } from 'react';
import { PlanDependencyPanel } from './plan-dependency-panel';
import { PlanExecutionPanel } from './plan-execution-panel';

import {
  createRemotePlanWorkDataSource,
  newPlanStepRef,
  type PlanStep,
  type PlanWork,
} from './remote-plan-work-data-source';
import {
  subscribePlanActivityIntent,
  type PlanActivityIntent,
} from './plan-work-intent';
import './plan-work-panel.css';

function message(error: unknown): string {
  return error instanceof Error && error.message.trim()
    ? error.message : 'Operazione sul Plan non riuscita.';
}

export function PlanWorkPanel() {
  const source = useMemo(() => createRemotePlanWorkDataSource(), []);
  const [plans, setPlans] = useState<readonly PlanWork[]>([]);
  const [selectedRef, setSelectedRef] = useState<string | null>(null);
  const [planTitle, setPlanTitle] = useState('');
  const [stepTitle, setStepTitle] = useState('');
  const [activityIntent, setActivityIntent] = useState<PlanActivityIntent | null>(null);
  const [targetStepRef, setTargetStepRef] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [pending, setPending] = useState(false);
  const attempt = useRef<{ fingerprint: string; id: string } | null>(null);
  const pendingStep = useRef<{ fingerprint: string; ref: string } | null>(null);
  const panelRef = useRef<HTMLDetailsElement | null>(null);
  const current = plans.find((item) => item.planRef === selectedRef) ?? null;
  const unlinkedSteps = current?.steps.filter((item) => item.activityRef === null) ?? [];
  const alreadyLinked = current?.steps.find((item) =>
    item.activityRef === activityIntent?.activityRef);
  const matchingStep = unlinkedSteps.find((item) =>
    item.title.trim().toLocaleLowerCase() === activityIntent?.title.trim().toLocaleLowerCase());
  const selectedTarget = targetStepRef || matchingStep?.stepRef || 'new';

  const reload = async () => {
    const items = await source.list();
    setPlans(items);
    setSelectedRef((previous) =>
      previous !== null && items.some((item) => item.planRef === previous)
        ? previous : (items[0]?.planRef ?? null));
  };

  useEffect(() => {
    let active = true;
    void source.list().then((items) => {
      if (!active) return;
      setPlans(items);
      setSelectedRef(items[0]?.planRef ?? null);
      setLoading(false);
    }).catch((cause: unknown) => {
      if (active) {
        setError(message(cause));
        setLoading(false);
      }
    });
    return () => { active = false; };
  }, [source]);

  useEffect(() => subscribePlanActivityIntent((intent) => {
    setActivityIntent(intent);
    setTargetStepRef('');
    setPlanTitle((previous) => previous.trim() || `Plan ${intent.title}`);
    if (panelRef.current !== null) panelRef.current.open = true;
    requestAnimationFrame(() => panelRef.current?.scrollIntoView?.({
      behavior: 'smooth', block: 'start',
    }));
  }), []);

  const run = async (
    fingerprint: string,
    write: (operationId: string) => Promise<PlanWork>,
    success: string,
    onSuccess?: () => void,
  ) => {
    if (pending) return;
    const prior = attempt.current;
    const id = prior?.fingerprint === fingerprint ? prior.id : crypto.randomUUID();
    attempt.current = { fingerprint, id };
    setPending(true);
    setError(null);
    setStatus(null);
    try {
      const result = await write(id);
      attempt.current = null;
      pendingStep.current = null;
      await reload();
      setSelectedRef(result.planRef);
      setStatus(success);
      onSuccess?.();
    } catch (cause) {
      setError(message(cause));
    } finally {
      setPending(false);
    }
  };

  const create = () => {
    const title = planTitle.trim();
    if (!title) return;
    void run(JSON.stringify(['create', title]), (id) => source.create(title, id),
      'Plan creato.');
  };

  const replace = (
    steps: readonly Omit<PlanStep, 'position'>[],
    success: string,
    onSuccess?: () => void,
  ) => {
    if (current === null) return;
    const plan = current;
    void run(
      JSON.stringify(['replace', plan.planRef, plan.stateRef, plan.title, steps]),
      (id) => source.replace(plan, plan.title, steps, id),
      success,
      onSuccess,
    );
  };

  const addStep = () => {
    if (current === null || !stepTitle.trim()) return;
    const fingerprint = JSON.stringify([current.planRef, current.stateRef, stepTitle.trim()]);
    const ref = pendingStep.current?.fingerprint === fingerprint
      ? pendingStep.current.ref : newPlanStepRef();
    pendingStep.current = { fingerprint, ref };
    replace([...current.steps, {
      stepRef: ref, title: stepTitle.trim(), activityRef: null,
      divisible: null, maxPlannedSlices: null, mergeCompatible: null,
      executionStrengthCode: null,
    }], 'Step aggiunto.', () => setStepTitle(''));
  };

  const addSelectedActivity = () => {
    if (current === null || activityIntent === null || alreadyLinked !== undefined) return;
    const intent = activityIntent;
    const target = unlinkedSteps.find((item) => item.stepRef === selectedTarget);
    if (target !== undefined) {
      replace(current.steps.map((item) => item.stepRef === target.stepRef
        ? { ...item, activityRef: intent.activityRef } : item),
      `Attività “${intent.title}” collegata allo Step “${target.title}”.`,
      () => { setActivityIntent(null); setTargetStepRef(''); });
      return;
    }
    const fingerprint = JSON.stringify([
      current.planRef, current.stateRef, intent.activityRef,
    ]);
    const ref = pendingStep.current?.fingerprint === fingerprint
      ? pendingStep.current.ref : newPlanStepRef();
    pendingStep.current = { fingerprint, ref };
    replace([...current.steps, {
      stepRef: ref, title: intent.title, activityRef: intent.activityRef,
      divisible: null, maxPlannedSlices: null, mergeCompatible: null,
      executionStrengthCode: null,
    }], `Step “${intent.title}” aggiunto e collegato.`, () => {
      setActivityIntent(null);
      setTargetStepRef('');
    });
  };

  const moveStep = (index: number, direction: -1 | 1) => {
    if (current === null) return;
    const next = [...current.steps];
    const other = index + direction;
    if (other < 0 || other >= next.length) return;
    [next[index], next[other]] = [next[other]!, next[index]!];
    replace(next, 'Ordine aggiornato.');
  };

  const unlinkActivity = (stepRef: string) => {
    if (current === null) return;
    replace(
      current.steps.map((item) => item.stepRef === stepRef
        ? {
            ...item, activityRef: null, divisible: null, maxPlannedSlices: null,
            mergeCompatible: null, executionStrengthCode: null,
          }
        : item),
      'Attività scollegata.',
    );
  };

  return (
    <details ref={panelRef} className="plan-work-panel">
      <summary>Plan e Step</summary>
      <div className="plan-work-panel__body">
        {loading ? <p>Caricamento Plan…</p> : (
          <>
            <button type="button" disabled={pending} onClick={() => {
              void reload().then(() => setError(null)).catch((cause: unknown) =>
                setError(message(cause)));
            }}>Ricarica Plan</button>
            <label>
              Nuovo Plan
              <input value={planTitle} maxLength={300} disabled={pending}
                onChange={(event) => setPlanTitle(event.currentTarget.value)} />
            </label>
            <button type="button" disabled={pending || !planTitle.trim()} onClick={create}>
              Crea Plan
            </button>
            {activityIntent !== null ? (
              <p role="status">
                Attività selezionata: <strong>{activityIntent.title}</strong>.
                {current === null
                  ? ' Crea o seleziona un Plan, poi aggiungila con +.'
                  : alreadyLinked !== undefined
                    ? ` Già collegata allo Step “${alreadyLinked.title}”.`
                    : matchingStep !== undefined
                      ? ` Collega lo Step esistente “${matchingStep.title}”.`
                      : ' Scegli uno Step esistente oppure aggiungine uno nuovo.'}
                <button type="button" disabled={pending} onClick={() => setActivityIntent(null)}>
                  Annulla selezione
                </button>
              </p>
            ) : null}
            {plans.length > 0 ? (
              <label>
                Plan corrente
                <select value={selectedRef ?? ''} disabled={pending}
                  onChange={(event) => {
                    setSelectedRef(event.currentTarget.value);
                    setTargetStepRef('');
                  }}>
                  {plans.map((item) => (
                    <option key={item.planRef} value={item.planRef}>{item.title}</option>
                  ))}
                </select>
              </label>
            ) : <p>Nessun Plan creato.</p>}
            {current !== null ? (
              <section>
                <strong>{current.title}</strong>
                <ol>
                  {current.steps.map((item, index) => (
                    <li key={item.stepRef}>
                      <span>{item.title}</span>
                      <small>{item.activityRef !== null
                        ? ' · Attività collegata' : ' · nessuna Attività collegata'}</small>
                      {item.activityRef !== null ? (
                        <button type="button" aria-label={`Scollega attività da ${item.title}`}
                          disabled={pending} onClick={() => unlinkActivity(item.stepRef)}>
                          Scollega
                        </button>
                      ) : null}
                      <button type="button" aria-label={`Sposta su ${item.title}`}
                        disabled={pending || index === 0}
                        onClick={() => moveStep(index, -1)}>↑</button>
                      <button type="button" aria-label={`Sposta giù ${item.title}`}
                        disabled={pending || index === current.steps.length - 1}
                        onClick={() => moveStep(index, 1)}>↓</button>
                      <button type="button" aria-label={`Rimuovi ${item.title}`}
                        disabled={pending}
                        onClick={() => replace(
                          current.steps.filter((other) => other.stepRef !== item.stepRef),
                          'Step rimosso dal Plan.',
                        )}>Rimuovi</button>
                    </li>
                  ))}
                </ol>
                <label>
                  Nuovo Step
                  <input value={stepTitle} maxLength={300} disabled={pending}
                    onChange={(event) => setStepTitle(event.currentTarget.value)} />
                </label>
                <button type="button" disabled={pending || !stepTitle.trim() ||
                  current.steps.length >= 1000} onClick={addStep}>Aggiungi Step</button>
                {activityIntent !== null ? (
                  alreadyLinked === undefined ? (
                    <>
                      {unlinkedSteps.length > 0 ? (
                        <label>Destinazione dell’Attività
                          <select value={selectedTarget} disabled={pending}
                            onChange={(event) => setTargetStepRef(event.currentTarget.value)}>
                            <option value="new">Nuovo Step “{activityIntent.title}”</option>
                            {unlinkedSteps.map((item) => (
                              <option key={item.stepRef} value={item.stepRef}>
                                Step esistente “{item.title}”
                              </option>
                            ))}
                          </select>
                        </label>
                      ) : null}
                      <button type="button"
                        disabled={pending || (selectedTarget === 'new' && current.steps.length >= 1000)}
                        onClick={addSelectedActivity}>
                        {selectedTarget === 'new'
                          ? `+ Aggiungi “${activityIntent.title}” al Plan`
                          : `Collega “${activityIntent.title}” allo Step esistente`}
                      </button>
                    </>
                  ) : null
                ) : (
                  <p>Apri un’Activity nel Planning Tray e premi il suo titolo per aggiungerla qui.</p>
                )}
                <PlanDependencyPanel key={`${current.planRef}:${current.stateRef}`} plan={current} />
                <PlanExecutionPanel key={`execution:${current.planRef}:${current.stateRef}`}
                  plan={current} pending={pending}
                  update={(stepRef, policy) => replace(current.steps.map((item) =>
                    item.stepRef === stepRef ? { ...item, ...policy } : item),
                  policy.divisible === null ? 'Policy ritirata.' : 'Policy aggiornata.')} />
              </section>
            ) : null}
          </>
        )}
        {error !== null ? <p role="alert">{error}</p> : null}
        {status !== null ? <p role="status">{status}</p> : null}
      </div>
    </details>
  );
}
