import type { ErrorComponentProps } from '@tanstack/react-router';
import { useTranslation } from 'react-i18next';

import './world-focus-states.css';

/**
 * Route-level failure surface. It intentionally never prints raw error text:
 * transport/render details belong to observability, not to user-visible copy.
 */
export function WorldFocusRouteError({ reset }: ErrorComponentProps) {
  const { t } = useTranslation('common');

  return (
    <main className="world-focus-route-error" data-world-focus-route-error>
      <section
        className="world-focus-route-error-card"
        role="alert"
        aria-labelledby="world-focus-route-error-title"
      >
        <h1 id="world-focus-route-error-title">
          {t(($) => $.common.worldFocus.states.routeErrorTitle)}
        </h1>
        <p>{t(($) => $.common.worldFocus.states.routeErrorBody)}</p>
        <button type="button" onClick={reset}>
          {t(($) => $.common.worldFocus.states.retry)}
        </button>
      </section>
    </main>
  );
}
