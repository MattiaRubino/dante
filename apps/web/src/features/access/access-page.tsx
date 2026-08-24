import { AccessBrandStage } from './components/access-brand-stage';
import { AccessSignInPanel } from './components/access-sign-in-panel';
import './access.css';

export function AccessPage() {
  return (
    <main className="access-page">
      <AccessBrandStage />
      <AccessSignInPanel />
    </main>
  );
}
