import { instantToZonedDateTime, parseInstant } from '@dante/time';
import { createFileRoute } from '@tanstack/react-router';
import { useTranslation } from 'react-i18next';

export const Route = createFileRoute('/')({
  component: WebRuntimeReady,
});

function WebRuntimeReady() {
  const { t } = useTranslation('common');
  const temporalProbe = instantToZonedDateTime(
    parseInstant('2026-08-22T18:00:00Z'),
    'Europe/Rome',
  ).toString();

  return (
    <main className="runtime-shell">
      <section className="runtime-card" aria-labelledby="runtime-title">
        <p className="runtime-eyebrow">
          {t(($) => $.common.runtime.web.eyebrow)}
        </p>
        <h1 id="runtime-title">{t(($) => $.common.runtime.web.title)}</h1>
        <p className="runtime-copy">
          {t(($) => $.common.runtime.web.description)}
        </p>
        <dl className="runtime-status">
          <div>
            <dt>{t(($) => $.common.runtime.labels.route)}</dt>
            <dd>/</dd>
          </div>
          <div>
            <dt>{t(($) => $.common.runtime.labels.purpose)}</dt>
            <dd>
              {t(($) => $.common.runtime.web.purpose)}
              <br />
              <code>{temporalProbe}</code>
            </dd>
          </div>
        </dl>
      </section>
    </main>
  );
}
