import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react';

import type { TemporalCreateFields } from '../model/temporal-create-session';
import {
  createTemporalCreateU2AuthoringDraft,
  normalizeTemporalCreateU2EndDate,
  patchTemporalCreateU2AuthoringDraft,
  type TemporalCreateU2AuthoringDraft,
} from '../model/temporal-create-u2-authoring';

type U2DraftContextValue = Readonly<{
  draft: TemporalCreateU2AuthoringDraft;
  patch: (patch: Partial<TemporalCreateU2AuthoringDraft>) => void;
}>;

const U2DraftContext = createContext<U2DraftContextValue | null>(null);

type TemporalCreateU2DraftProviderProps = Readonly<{
  fields: TemporalCreateFields;
  resetKey: string | number;
  initialDraft?: TemporalCreateU2AuthoringDraft;
  onDraftChange: (draft: TemporalCreateU2AuthoringDraft) => void;
  children: ReactNode;
}>;

export function TemporalCreateU2DraftProvider(props: TemporalCreateU2DraftProviderProps) {
  // Reset only on a true baseline transition. Ordinary field edits must not
  // discard staged Life Area, color, or activity structure intentions.
  return <TemporalCreateU2DraftProviderInstance key={props.resetKey} {...props} />;
}

function TemporalCreateU2DraftProviderInstance({
  fields,
  initialDraft,
  onDraftChange,
  children,
}: TemporalCreateU2DraftProviderProps) {
  const [state, setState] = useState(
    () => initialDraft ?? createTemporalCreateU2AuthoringDraft(fields),
  );

  const [previousDate, setPreviousDate] = useState(fields.date);

  // React's guarded render-time adjustment keeps the draft's end date in
  // sync with an externally reseeded start date without the extra effect
  // render. It never resets Life Area or other authored draft fields.
  if (previousDate !== fields.date) {
    setPreviousDate(fields.date);
    const endDate = normalizeTemporalCreateU2EndDate(fields.date, state.endDate);
    if (endDate !== state.endDate) {
      setState(patchTemporalCreateU2AuthoringDraft(state, { endDate }));
    }
  }

  // Communicate the committed draft (including the initial keyed mount and
  // date normalization) only after render. The patch callback below still
  // notifies synchronously for user edits before a subsequent Submit click.
  useEffect(() => {
    onDraftChange(state);
  }, [state, onDraftChange]);

  const value = useMemo<U2DraftContextValue>(
    () => ({
      draft: state,
      patch: (patch) => {
        setState((current) => {
          const next = patchTemporalCreateU2AuthoringDraft(current, patch);
          onDraftChange(next);
          return next;
        });
      },
    }),
    [onDraftChange, state],
  );

  return (
    <U2DraftContext.Provider value={value}>{children}</U2DraftContext.Provider>
  );
}

export function useTemporalCreateU2Draft(): U2DraftContextValue {
  const value = useContext(U2DraftContext);
  if (value === null) {
    throw new Error('TemporalCreateU2DraftProvider is required.');
  }
  return value;
}
