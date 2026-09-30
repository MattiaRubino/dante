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

export function TemporalCreateU2DraftProvider({
  fields,
  resetKey,
  onDraftChange,
  children,
}: Readonly<{
  fields: TemporalCreateFields;
  resetKey: string | number;
  onDraftChange: (draft: TemporalCreateU2AuthoringDraft) => void;
  children: ReactNode;
}>) {
  const [state, setState] = useState(() =>
    createTemporalCreateU2AuthoringDraft(fields),
  );

  useEffect(() => {
    const next = createTemporalCreateU2AuthoringDraft(fields);
    setState(next);
    onDraftChange(next);
    // resetKey intentionally owns lifecycle boundaries; ordinary field edits
    // must not erase staged Life Area/color intent.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [resetKey]);

  useEffect(() => {
    setState((current) => {
      const endDate = normalizeTemporalCreateU2EndDate(
        fields.date,
        current.endDate,
      );
      if (endDate === current.endDate) return current;
      const next = patchTemporalCreateU2AuthoringDraft(current, { endDate });
      onDraftChange(next);
      return next;
    });
  }, [fields.date, onDraftChange]);

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

  return <U2DraftContext.Provider value={value}>{children}</U2DraftContext.Provider>;
}

export function useTemporalCreateU2Draft(): U2DraftContextValue {
  const value = useContext(U2DraftContext);
  if (value === null) {
    throw new Error('TemporalCreateU2DraftProvider is required.');
  }
  return value;
}
