import './home.css';
import './home-m1.css';
import './home-skin.css';
import './home-u1-layout.css';
import './central-stage/central-stage-m1-geometry.css';

import { TimelineTruthInspector } from '../../temporal/timeline-truth-inspector';
import { PlanWorkPanel } from '../../temporal/plan-work-panel';
import { TemporalTimelineRuntimeBoundary } from '../../temporal/timeline-runtime-boundary';
import type { HomeWorldOpenIntent } from '../model/home-world-focus';
import { HomeShell } from './home-shell';

type HomePageProps = Readonly<{
  viewedDateIso?: string | undefined;
  preferredName?: string | undefined;
  onViewedDateChange?: ((isoDate: string | undefined) => void) | undefined;
  onOpenWorldFocus?: ((intent: HomeWorldOpenIntent) => void) | undefined;
}>;

export function HomePage(props: HomePageProps) {
  return (
    <TemporalTimelineRuntimeBoundary viewedDateIso={props.viewedDateIso}>
      <HomeShell {...props} />
      <TimelineTruthInspector />
      <PlanWorkPanel />
    </TemporalTimelineRuntimeBoundary>
  );
}
