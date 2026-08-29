import './home.css';
import './home-m1.css';
import './home-skin.css';

import { HomeShell } from './home-shell';

type HomePageProps = Readonly<{
  viewedDateIso?: string | undefined;
  onViewedDateChange?: ((isoDate: string | undefined) => void) | undefined;
}>;

export function HomePage(props: HomePageProps) {
  return <HomeShell {...props} />;
}
