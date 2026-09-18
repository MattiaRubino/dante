import { PrimaryScreenFrame } from '../../src/ui/navigation/PrimaryScreenFrame';
import { SectionPlaceholder } from '../../src/ui/navigation/SectionPlaceholder';

export default function HomeRoute() {
  return (
    <PrimaryScreenFrame active="home" title="Home">
      <SectionPlaceholder
        eyebrow="PRIMARY SURFACE"
        title="Home"
        copy="Home is reserved for the first information a DANTE user should understand or act on. Its product hierarchy will be designed in the dedicated Home block, not guessed here."
      />
    </PrimaryScreenFrame>
  );
}
