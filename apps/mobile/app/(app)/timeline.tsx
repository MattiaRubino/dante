import { PrimaryScreenFrame } from '../../src/ui/navigation/PrimaryScreenFrame';
import { SectionPlaceholder } from '../../src/ui/navigation/SectionPlaceholder';

export default function TimelineRoute() {
  return (
    <PrimaryScreenFrame active="timeline" title="Timeline">
      <SectionPlaceholder
        eyebrow="PRIMARY SURFACE"
        title="Timeline"
        copy="The Timeline has a permanent place in the Mobile shell, but temporal data, calendar behavior and mutations remain deferred to the canonical Temporal vertical."
      />
    </PrimaryScreenFrame>
  );
}
