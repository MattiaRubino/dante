import { useTranslation } from 'react-i18next';

import type { WorldFocusWorld } from '../model/world-focus-fixtures';

type WorldFocusContextProps = Readonly<{
  world: WorldFocusWorld;
}>;

export function WorldFocusContext({ world }: WorldFocusContextProps) {
  const { t } = useTranslation('common');
  const label = t(($) => $.common.worldFocus.worlds[world.id].label);
  const description = t(
    ($) => $.common.worldFocus.worlds[world.id].description,
  );

  return (
    <header
      className="world-focus-context"
      data-world-focus-context="true"
      data-world-focus-context-id={world.id}
    >
      <div className="world-focus-context-copy">
        <p className="world-focus-context-kicker">
          {t(($) => $.common.worldFocus.kicker)}
        </p>
        <h1 className="world-focus-context-title">{label}</h1>
        <p className="world-focus-context-description">{description}</p>
      </div>
    </header>
  );
}
