import { createFileRoute } from '@tanstack/react-router';

export const Route = createFileRoute('/')({
  component: WebRuntimeReady,
});

function WebRuntimeReady() {
  return (
    <main className="runtime-shell">
      <section className="runtime-card" aria-labelledby="runtime-title">
        <p className="runtime-eyebrow">DANTE Web</p>
        <h1 id="runtime-title">Frontend runtime ready</h1>
        <p className="runtime-copy">
          Minimal React, Vite, and TanStack Router scaffold. Product UI is not
          materialized in this checkpoint.
        </p>
        <dl className="runtime-status">
          <div>
            <dt>Route</dt>
            <dd>/</dd>
          </div>
          <div>
            <dt>Purpose</dt>
            <dd>FM-03 diagnostic scaffold</dd>
          </div>
        </dl>
      </section>
    </main>
  );
}
