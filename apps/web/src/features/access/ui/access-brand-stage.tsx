import { useTranslation } from 'react-i18next';

import danteSymbolUrl from '../../../../../../assets/brand/logo/master/dante-symbol-master-v0.svg?url';

export function AccessBrandStage() {
  const { t } = useTranslation('common');

  return (
    <section
      className="access-brand-stage"
      aria-labelledby="access-brand-title"
    >
      <div className="access-brand-eyebrow">DANTE</div>

      <h2 id="access-brand-title">
        <span>{t(($) => $.common.access.stage.titleFirst)}</span>
        <br />
        <span>{t(($) => $.common.access.stage.titleSecond)}</span>
      </h2>

      <p className="access-brand-body">
        {t(($) => $.common.access.stage.body)}
      </p>

      <p className="access-brand-foot">
        {t(($) => $.common.access.stage.foot)}
      </p>

      <img
        className="access-brand-orbits"
        src={danteSymbolUrl}
        alt=""
        aria-hidden="true"
      />
    </section>
  );
}
