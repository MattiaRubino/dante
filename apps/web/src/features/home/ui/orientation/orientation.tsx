import { useTranslation } from 'react-i18next';

export function Orientation() {
  const { t } = useTranslation('common');

  return (
    <section
      className="home-orientation"
      data-home-region="orientation"
      aria-label={t(($) => $.common.home.orientation.title)}
    >
      <h1 className="home-visually-hidden">
        {t(($) => $.common.home.orientation.title)}
      </h1>

      <article className="home-orientation-now" data-home-orientation="now-next">
        <span>{t(($) => $.common.home.orientation.nowNext)}</span>
        <strong aria-hidden="true">14:57</strong>
        <span className="home-orientation-line" aria-hidden="true" />
      </article>

      <article
        className="home-orientation-highlight"
        data-home-orientation="highlight"
      >
        <span>{t(($) => $.common.home.orientation.highlight)}</span>
        <strong aria-hidden="true" />
        <span className="home-orientation-line" aria-hidden="true" />
      </article>

      <article className="home-orientation-for-you" data-home-orientation="for-you">
        <span>{t(($) => $.common.home.orientation.forYou)}</span>
        <strong aria-hidden="true" />
        <span className="home-orientation-line" aria-hidden="true" />
      </article>
    </section>
  );
}
