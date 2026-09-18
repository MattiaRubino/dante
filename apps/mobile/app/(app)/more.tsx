import { PrimaryScreenFrame } from '../../src/ui/navigation/PrimaryScreenFrame';
import { SectionPlaceholder } from '../../src/ui/navigation/SectionPlaceholder';

export default function MoreRoute() {
  return (
    <PrimaryScreenFrame active="more" title="More">
      <SectionPlaceholder
        eyebrow="SECONDARY"
        title="More"
        copy="Account, profile, settings and other secondary destinations belong here rather than competing with DANTE's three primary surfaces."
      />
    </PrimaryScreenFrame>
  );
}
