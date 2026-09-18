import { PrimaryScreenFrame } from '../../src/ui/navigation/PrimaryScreenFrame';
import { SectionPlaceholder } from '../../src/ui/navigation/SectionPlaceholder';

export default function WorldsRoute() {
  return (
    <PrimaryScreenFrame active="worlds" title="Worlds">
      <SectionPlaceholder
        eyebrow="PRIMARY SURFACE"
        title="Worlds"
        copy="Worlds is established as a top-level destination. Its real information architecture and data behavior remain owned by the future Worlds vertical."
      />
    </PrimaryScreenFrame>
  );
}
