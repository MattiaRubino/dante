export type PlanActivityIntent = Readonly<{
  activityRef: string;
  title: string;
}>;

const EVENT = 'dante:open-plan-for-activity';

export function openPlanForActivity(intent: PlanActivityIntent): void {
  globalThis.dispatchEvent(new CustomEvent<PlanActivityIntent>(EVENT, { detail: intent }));
}

export function subscribePlanActivityIntent(
  listener: (intent: PlanActivityIntent) => void,
): () => void {
  const receive = (event: Event) => {
    if (!(event instanceof CustomEvent) ||
        typeof event.detail !== 'object' || event.detail === null) {
      return;
    }
    const detail = event.detail as Record<string, unknown>;
    if (typeof detail.activityRef !== 'string' || typeof detail.title !== 'string') return;
    listener(Object.freeze({
      activityRef: detail.activityRef,
      title: detail.title,
    }));
  };
  globalThis.addEventListener(EVENT, receive);
  return () => globalThis.removeEventListener(EVENT, receive);
}
