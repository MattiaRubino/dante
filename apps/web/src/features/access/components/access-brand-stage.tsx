import { useTranslation } from 'react-i18next';

import danteSymbolUrl from '../../../../../../assets/brand/logo/master/dante-symbol-master-v0.svg?url';
import danteWordmarkUrl from '../../../../../../assets/brand/wordmark/master/dante-wordmark-master-v0.svg?url';

export function AccessBrandStage() {
  const { t } = useTranslation('common');

  return (
    <section className="access-brand-stage" aria-labelledby="access-brand-title">
      <img
        className="access-brand-wordmark"
        src={danteWordmarkUrl}
        alt="DANTE"
      />

      <div className="access-brand-copy">
        <h1 id="access-brand-title">
          <span>{t(($) => $.access.stage.titleFirst)}</span>
          <span>{t(($) => $.access.stage.titleSecond)}</span>
        </h1>
        <p>{t(($) => $.access.stage.body)}</p>
      </div>

      <p className="access-brand-foot">{t(($) => $.access.stage.foot)}</p>

      <img
        className="access-brand-orbits"
        src={danteSymbolUrl}
        alt=""
        aria-hidden="true"
      />
    </section>
  );
}
