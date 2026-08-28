import { useState } from 'react';
import { useTranslation } from 'react-i18next';

import { AISurface } from './ai-surface/ai-surface';
import { CentralStage } from './central-stage/central-stage';
import { ContextRail } from './context-rail/context-rail';
import { GlobalTopbar } from './global-topbar/global-topbar';
import { DayContextStrip } from './orientation/day-context-strip';
import { Orientation } from './orientation/orientation';
import { TimelineSurface } from './timeline/timeline-surface';

export function HomeShell() {
  const { t } = useTranslation('common');
  const [isAiCollapsed, setIsAiCollapsed] = useState(false);
  const [isTimelineExpanded, setIsTimelineExpanded] = useState(false);

  return (
    <div
      className="home-shell"
      data-home-region="shell"
      data-home-ai-state={isAiCollapsed ? 'collapsed' : 'expanded'}
      data-home-timeline-state={isTimelineExpanded ? 'expanded' : 'normal'}
    >
      <GlobalTopbar />

      <main
        className="home-main"
        aria-label={t(($) => $.common.home.shell.mainLabel)}
      >
        <section className="home-hero" data-home-layout="hero">
          <DayContextStrip />

          <div className="home-hero-body">
            <AISurface
              collapsed={isAiCollapsed}
              onToggleCollapsed={() => setIsAiCollapsed((value) => !value)}
            />

            <div
              className="home-upper-workspace"
              data-home-layout="upper-workspace"
            >
              <Orientation />
              <CentralStage />
            </div>
          </div>
        </section>

        <section
          className="home-today-layout"
          data-home-layout="today"
          data-expanded={isTimelineExpanded ? 'true' : 'false'}
        >
          <TimelineSurface
            expanded={isTimelineExpanded}
            onToggleExpanded={() =>
              setIsTimelineExpanded((value) => !value)
            }
          />
          <ContextRail />
        </section>
      </main>
    </div>
  );
}
