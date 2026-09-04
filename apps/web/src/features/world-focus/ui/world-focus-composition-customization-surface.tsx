import { useEffect, useId, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';

import type { WorldFocusCompositionOpportunity } from '../application/world-focus-composition-opportunities';
import type { WorldFocusCompositionConfigEntry } from '../model/world-focus-composition-config';
import {
  useWorldFocusCompositionCustomization,
} from './world-focus-composition-customization-context';

function opportunityLabel(
  kind: string,
  t: ReturnType<typeof useTranslation<'common'>>['t'],
): string {
  switch (kind) {
    case 'situation':
      return t(($) => $.common.worldFocus.customization.kinds.situation);
    case 'continuity':
      return t(($) => $.common.worldFocus.customization.kinds.continuity);
    case 'attention':
      return t(($) => $.common.worldFocus.customization.kinds.attention);
    case 'next':
      return t(($) => $.common.worldFocus.customization.kinds.next);
    case 'comparison':
      return t(($) => $.common.worldFocus.customization.kinds.comparison);
    case 'trajectory':
      return t(($) => $.common.worldFocus.customization.kinds.trajectory);
    case 'evidence-history':
      return t(($) => $.common.worldFocus.customization.kinds.evidenceHistory);
    default:
      return t(($) => $.common.worldFocus.customization.kinds.other);
  }
}

function instanceQualifier(entry: Readonly<{ instanceId: string; kind: string }>): string | null {
  if (!['attention', 'comparison', 'trajectory'].includes(entry.kind)) return null;
  const separator = entry.instanceId.indexOf(':');
  if (separator < 0 || separator === entry.instanceId.length - 1) return null;
  return entry.instanceId.slice(separator + 1);
}

export function WorldFocusCompositionCustomizationSurface() {
  const { t } = useTranslation('common');
  const customization = useWorldFocusCompositionCustomization();
  const dialogRef = useRef<HTMLDivElement | null>(null);
  const rowRefs = useRef(new Map<string, HTMLLIElement>());
  const [announcement, setAnnouncement] = useState('');
  const headingId = useId();
  const draft = customization.draft;

  useEffect(() => {
    dialogRef.current?.focus({ preventScroll: true });
  }, []);

  if (draft === null) return null;

  const entries = draft.workingConfig.entries;
  const opportunitySet =
    customization.opportunities.status === 'ready'
      ? customization.opportunities.set
      : null;
  const opportunityById = new Map(
    opportunitySet?.opportunities.map((opportunity) => [
      opportunity.instanceId,
      opportunity,
    ]) ?? [],
  );
  const configuredIds = new Set(entries.map((entry) => entry.instanceId));
  const availableToAdopt =
    opportunitySet?.opportunities.filter(
      (opportunity) => !configuredIds.has(opportunity.instanceId),
    ) ?? [];

  const executeMove = (
    entry: WorldFocusCompositionConfigEntry,
    index: number,
    direction: 'up' | 'down',
  ) => {
    const beforeInstanceId =
      direction === 'up'
        ? entries[index - 1]?.instanceId ?? null
        : entries[index + 2]?.instanceId ?? null;
    const nextPosition = direction === 'up' ? index : index + 2;

    if (
      customization.execute({
        source: 'manual',
        type: 'move',
        instanceId: entry.instanceId,
        beforeInstanceId,
      })
    ) {
      const label = opportunityLabel(entry.kind, t);
      setAnnouncement(
        t(($) => $.common.worldFocus.customization.moved, {
          item: label,
          position: nextPosition,
          total: entries.length,
        }),
      );
      queueMicrotask(() => {
        rowRefs.current.get(entry.instanceId)?.focus({ preventScroll: true });
      });
    }
  };

  const adopt = (opportunity: WorldFocusCompositionOpportunity) => {
    customization.execute({
      source: 'manual',
      type: 'adopt',
      opportunity,
    });
  };

  return (
    <div
      ref={dialogRef}
      className="world-focus-composition-customization"
      role="dialog"
      aria-modal="false"
      aria-labelledby={headingId}
      tabIndex={-1}
      data-world-focus-customization-dirty={customization.isDirty}
      data-world-focus-customization-revision={customization.acceptedConfig.revision}
    >
      <header className="world-focus-composition-customization-header">
        <div>
          <p className="world-focus-composition-customization-kicker">
            {t(($) => $.common.worldFocus.customization.kicker)}
          </p>
          <h2 id={headingId} className="world-focus-composition-customization-title">
            {t(($) => $.common.worldFocus.customization.title, {
              world: customization.worldLabel,
            })}
          </h2>
          <p className="world-focus-composition-customization-meta">
            {t(($) => $.common.worldFocus.customization.revision, {
              revision: customization.acceptedConfig.revision,
            })}
            {' · '}
            {customization.isDirty
              ? t(($) => $.common.worldFocus.customization.changed)
              : t(($) => $.common.worldFocus.customization.unchanged)}
          </p>
        </div>
      </header>

      <div className="world-focus-composition-customization-body">
        {customization.issue === null ? null : (
          <p className="world-focus-composition-customization-alert" role="alert">
            {customization.issue.status === 'revision-conflict'
              ? t(($) => $.common.worldFocus.customization.conflict)
              : t(($) => $.common.worldFocus.customization.invalid)}
          </p>
        )}

        <section aria-labelledby={`${headingId}-configured`}>
          <h3 id={`${headingId}-configured`} className="world-focus-composition-customization-section-title">
            {t(($) => $.common.worldFocus.customization.configuredTitle)}
          </h3>
          {entries.length === 0 ? (
            <p className="world-focus-composition-customization-empty">
              {t(($) => $.common.worldFocus.customization.configuredEmpty)}
            </p>
          ) : (
            <ol className="world-focus-composition-customization-list">
              {entries.map((entry, index) => {
                const label = opportunityLabel(entry.kind, t);
                const qualifier = instanceQualifier(entry);
                const unavailable =
                  opportunitySet !== null && !opportunityById.has(entry.instanceId);
                return (
                  <li
                    key={entry.instanceId}
                    ref={(node) => {
                      if (node === null) rowRefs.current.delete(entry.instanceId);
                      else rowRefs.current.set(entry.instanceId, node);
                    }}
                    className="world-focus-composition-customization-entry"
                    tabIndex={-1}
                    aria-label={t(($) => $.common.worldFocus.customization.position, {
                      item: label,
                      position: index + 1,
                      total: entries.length,
                    })}
                    data-world-focus-customization-entry={entry.instanceId}
                  >
                    <div className="world-focus-composition-customization-entry-copy">
                      <p className="world-focus-composition-customization-entry-title">
                        {label}
                      </p>
                      {qualifier === null ? null : (
                        <p className="world-focus-composition-customization-entry-id">
                          {qualifier}
                        </p>
                      )}
                      <div className="world-focus-composition-customization-tags">
                        {entry.pinned ? (
                          <span>{t(($) => $.common.worldFocus.customization.states.pinned)}</span>
                        ) : null}
                        {entry.visibility === 'hidden' ? (
                          <span>{t(($) => $.common.worldFocus.customization.states.hidden)}</span>
                        ) : null}
                        {entry.prominenceOverride === 'lead' ? (
                          <span>{t(($) => $.common.worldFocus.customization.states.lead)}</span>
                        ) : null}
                        {unavailable ? (
                          <span>{t(($) => $.common.worldFocus.customization.states.unavailable)}</span>
                        ) : null}
                      </div>
                    </div>

                    <div className="world-focus-composition-customization-actions">
                      <button
                        type="button"
                        onClick={() =>
                          customization.execute({
                            source: 'manual',
                            type: entry.pinned ? 'unpin' : 'pin',
                            instanceId: entry.instanceId,
                          })
                        }
                      >
                        {entry.pinned
                          ? t(($) => $.common.worldFocus.customization.unpin)
                          : t(($) => $.common.worldFocus.customization.pin)}
                      </button>
                      <button
                        type="button"
                        onClick={() =>
                          customization.execute({
                            source: 'manual',
                            type: entry.visibility === 'hidden' ? 'show' : 'hide',
                            instanceId: entry.instanceId,
                          })
                        }
                      >
                        {entry.visibility === 'hidden'
                          ? t(($) => $.common.worldFocus.customization.show)
                          : t(($) => $.common.worldFocus.customization.hide)}
                      </button>
                      <button
                        type="button"
                        disabled={index === 0}
                        onClick={() => executeMove(entry, index, 'up')}
                      >
                        {t(($) => $.common.worldFocus.customization.moveUp)}
                      </button>
                      <button
                        type="button"
                        disabled={index === entries.length - 1}
                        onClick={() => executeMove(entry, index, 'down')}
                      >
                        {t(($) => $.common.worldFocus.customization.moveDown)}
                      </button>
                      <button
                        type="button"
                        disabled={entry.prominenceOverride === 'lead'}
                        onClick={() =>
                          customization.execute({
                            source: 'manual',
                            type: 'promote',
                            instanceId: entry.instanceId,
                          })
                        }
                      >
                        {t(($) => $.common.worldFocus.customization.promote)}
                      </button>
                      <button
                        type="button"
                        onClick={() =>
                          customization.execute({
                            source: 'manual',
                            type: 'restore',
                            instanceId: entry.instanceId,
                          })
                        }
                      >
                        {t(($) => $.common.worldFocus.customization.restore)}
                      </button>
                    </div>
                  </li>
                );
              })}
            </ol>
          )}
        </section>

        <section aria-labelledby={`${headingId}-available`}>
          <h3 id={`${headingId}-available`} className="world-focus-composition-customization-section-title">
            {t(($) => $.common.worldFocus.customization.opportunitiesTitle)}
          </h3>
          {customization.opportunities.status === 'loading' ? (
            <p className="world-focus-composition-customization-empty" role="status">
              {t(($) => $.common.worldFocus.customization.opportunitiesLoading)}
            </p>
          ) : customization.opportunities.status === 'error' ? (
            <div className="world-focus-composition-customization-retry-row">
              <p role="alert">
                {t(($) => $.common.worldFocus.customization.opportunitiesError)}
              </p>
              <button type="button" onClick={customization.retryOpportunities}>
                {t(($) => $.common.worldFocus.customization.retry)}
              </button>
            </div>
          ) : customization.opportunities.status === 'ready' &&
            availableToAdopt.length > 0 ? (
            <ul className="world-focus-composition-customization-opportunities">
              {availableToAdopt.map((opportunity) => {
                const label = opportunityLabel(opportunity.kind, t);
                const qualifier = instanceQualifier(opportunity);
                return (
                  <li key={opportunity.instanceId}>
                    <div>
                      <p>{label}</p>
                      {qualifier === null ? null : <span>{qualifier}</span>}
                    </div>
                    <button type="button" onClick={() => adopt(opportunity)}>
                      {t(($) => $.common.worldFocus.customization.add, { item: label })}
                    </button>
                  </li>
                );
              })}
            </ul>
          ) : customization.opportunities.status === 'ready' ? (
            <p className="world-focus-composition-customization-empty">
              {t(($) => $.common.worldFocus.customization.opportunitiesEmpty)}
            </p>
          ) : null}
        </section>
      </div>

      <p className="world-focus-composition-customization-live" aria-live="polite" aria-atomic="true">
        {announcement}
      </p>

      <footer className="world-focus-composition-customization-footer">
        <button type="button" onClick={customization.cancel}>
          {t(($) => $.common.worldFocus.customization.cancel)}
        </button>
        <button type="button" disabled={!customization.isDirty} onClick={customization.apply}>
          {t(($) => $.common.worldFocus.customization.apply)}
        </button>
      </footer>
    </div>
  );
}
