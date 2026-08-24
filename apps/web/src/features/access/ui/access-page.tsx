import { AccessBrandStage } from './access-brand-stage';
import { AccessSignInPanel } from './access-sign-in-panel';
import '../access.css';

export function AccessPage() {
  return (
    <main className="access-page">
      <AccessBrandStage />
      <AccessSignInPanel />
    </main>
  );
}
