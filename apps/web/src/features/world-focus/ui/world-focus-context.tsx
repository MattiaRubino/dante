import { useTranslation } from 'react-i18next';

import type { WorldFocusIdentityDescriptor } from '../model/world-focus-identity';

type WorldFocusContextProps = Readonly<{
  identity: WorldFocusIdentityDescriptor;
}>;

export function WorldFocusContext({ identity }: WorldFocusContextProps) {
  const { t } = useTranslation('common');

  return (
    <header
      className="world-focus-context"
      data-world-focus-context="true"
      data-world-focus-context-id={identity.id}
    >
      <div className="world-focus-context-copy">
        <p className="world-focus-context-kicker">
          {t(($) => $.common.worldFocus.kicker)}
        </p>
        <h1 className="world-focus-context-title">{identity.label}</h1>
        <p className="world-focus-context-description">
          {identity.description}
        </p>
      </div>
    </header>
  );
}
