import { useState } from 'react';
import { createRoot } from 'react-dom/client';
import '../../src/bootstrap/i18n';
import '../../src/features/home/ui/home.css';
import '../../src/features/home/ui/timeline/timeline-tokens.css';
import { TimelineSurface } from '../../src/features/home/ui/timeline/timeline-surface';
import { TemporalTimelineRuntimeBoundary } from '../../src/features/temporal/timeline-runtime-boundary';

function Fixture() {
  const [expanded, setExpanded] = useState(false);
  return (
    <TemporalTimelineRuntimeBoundary mode="test">
      <TimelineSurface
        expanded={expanded}
        onExpandedChange={setExpanded}
        onExpansionProgress={() => undefined}
        sessionPanelEnabled
      />
    </TemporalTimelineRuntimeBoundary>
  );
}

createRoot(document.getElementById('root')!).render(<Fixture />);
