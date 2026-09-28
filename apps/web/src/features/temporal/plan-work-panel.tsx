import { useEffect, useMemo, useRef, useState } from 'react';

import {
  createRemotePlanWorkDataSource,
  newPlanStepRef,
  type PlanStep,
  type PlanWork,
} from './remote-plan-work-data-source';
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
  const [linkStepRef, setLinkStepRef] = useState('');
  const [linkActivityRef, setLinkActivityRef] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [pending, setPending] = useState(false);
  const attempt = useRef<{ fingerprint: string; id: string } | null>(null);
  const pendingStep = useRef<{ fingerprint: string; ref: string } | null>(null);
  const current = plans.find((item) => item.planRef === selectedRef) ?? null;

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
    steps: readonly Pick<PlanStep, 'stepRef' | 'title' | 'activityRef'>[],
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
    }], 'Step aggiunto.', () => setStepTitle(''));
  };

  const moveStep = (index: number, direction: -1 | 1) => {
    if (current === null) return;
    const next = [...current.steps];
    const other = index + direction;
    if (other < 0 || other >= next.length) return;
    [next[index], next[other]] = [next[other]!, next[index]!];
    replace(next, 'Ordine aggiornato.');
  };

  const linkActivity = () => {
    if (current === null || !linkStepRef) return;
    const reference = linkActivityRef.trim() || null;
    replace(
      current.steps.map((item) => item.stepRef === linkStepRef
        ? { ...item, activityRef: reference } : item),
      reference === null ? 'Attività scollegata.' : 'Attività collegata.',
      () => setLinkActivityRef(''),
    );
  };

  return (
    <details className="plan-work-panel">
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
            {plans.length > 0 ? (
              <label>
                Plan corrente
                <select value={selectedRef ?? ''} disabled={pending}
                  onChange={(event) => setSelectedRef(event.currentTarget.value)}>
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
                      {item.activityRef !== null ? <small> · Attività collegata</small> : null}
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
                {current.steps.length > 0 ? (
                  <>
                    <label>
                      Step da collegare
                      <select value={linkStepRef} disabled={pending}
                        onChange={(event) => setLinkStepRef(event.currentTarget.value)}>
                        <option value="">Seleziona Step</option>
                        {current.steps.map((item) => (
                          <option key={item.stepRef} value={item.stepRef}>{item.title}</option>
                        ))}
                      </select>
                    </label>
                    <label>
                      Riferimento Attività esistente (facoltativo)
                      <input value={linkActivityRef} disabled={pending}
                        placeholder="UUID dell’Attività"
                        onChange={(event) => setLinkActivityRef(event.currentTarget.value)} />
                    </label>
                    <button type="button" disabled={pending || !linkStepRef}
                      onClick={linkActivity}>Aggiorna collegamento</button>
                  </>
                ) : null}
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
