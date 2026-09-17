import { createContext, type ReactNode, useContext } from 'react';

import type { TimelineCanonicalScheduleBasis } from './model/timeline-types';

export type TimelineCanonicalActions = Readonly<{
  pendingScheduleRef: string | null;
  unschedule: (basis: TimelineCanonicalScheduleBasis) => void;
}>;

const TimelineCanonicalActionsContext =
  createContext<TimelineCanonicalActions | null>(null);

export function TimelineCanonicalActionsProvider({
  actions,
  children,
}: Readonly<{
  actions: TimelineCanonicalActions;
  children: ReactNode;
}>) {
  return (
    <TimelineCanonicalActionsContext.Provider value={actions}>
      {children}
    </TimelineCanonicalActionsContext.Provider>
  );
}

export function useTimelineCanonicalActions(): TimelineCanonicalActions | null {
  return useContext(TimelineCanonicalActionsContext);
}
