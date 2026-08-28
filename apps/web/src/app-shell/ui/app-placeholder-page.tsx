type AppPlaceholderPageProps = {
  eyebrow: string;
  title: string;
  description: string;
  status: string;
};

export function AppPlaceholderPage({
  eyebrow,
  title,
  description,
  status,
}: AppPlaceholderPageProps) {
  return (
    <main className="app-placeholder-page" data-app-placeholder="true">
      <section className="app-placeholder-card" aria-labelledby="app-placeholder-title">
        <span className="app-dialog-kicker">{eyebrow}</span>
        <h1 id="app-placeholder-title">{title}</h1>
        <p>{description}</p>
        <div className="app-placeholder-state" role="status">
          <span aria-hidden="true" />
          <strong>{status}</strong>
        </div>
      </section>
    </main>
  );
}
