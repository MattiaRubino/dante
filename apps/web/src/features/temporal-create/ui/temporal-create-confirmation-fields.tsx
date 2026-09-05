import { useTranslation } from 'react-i18next';

import type { TemporalCreateFields } from '../model/temporal-create-session';
import {
  TEMPORAL_CREATE_REMINDER_OPTIONS,
  temporalCreateDurationLabel,
} from './temporal-create-field-shared';

type TemporalCreateConfirmationFieldsProps = Readonly<{
  fields: TemporalCreateFields;
  onPatch: (patch: Partial<TemporalCreateFields>) => void;
  renderError: (path: string) => React.ReactNode;
}>;

export function TemporalCreateConfirmationFields({
  fields,
  onPatch,
  renderError,
}: TemporalCreateConfirmationFieldsProps) {
  const { t } = useTranslation('common');
  const confirmation = fields.confirmation;
  const patchConfirmation = (
    patch: Partial<TemporalCreateFields['confirmation']>,
  ) => onPatch({ confirmation: { ...confirmation, ...patch } });

  return (
    <section
      className="temporal-create-section"
      aria-labelledby="temporal-create-confirmation-only-heading"
    >
      <div className="temporal-create-section__heading">
        <div>
          <h3 id="temporal-create-confirmation-only-heading">
            {t(($) => $.common.home.timeline.create.confirmation.title)}
          </h3>
          <p>
            {t(($) => $.common.home.timeline.create.confirmation.description)}
          </p>
        </div>
      </div>

      <div className="temporal-create-grid two">
        <label className="temporal-create-control">
          <span>
            {t(($) => $.common.home.timeline.create.confirmation.outcome)}
          </span>
          <select
            value={confirmation.outcomePolicy}
            onChange={(event) =>
              patchConfirmation({
                outcomePolicy: event.currentTarget
                  .value as TemporalCreateFields['confirmation']['outcomePolicy'],
              })
            }
          >
            <option value="inherit">
              {t(($) => $.common.home.timeline.create.confirmation.inherit)}
            </option>
            <option value="ask-immediately">
              {t(
                ($) =>
                  $.common.home.timeline.create.confirmation.askImmediately,
              )}
            </option>
            <option value="ask-later">
              {t(($) => $.common.home.timeline.create.confirmation.askLater)}
            </option>
            <option value="daily-review">
              {t(($) => $.common.home.timeline.create.confirmation.dailyReview)}
            </option>
            <option value="weekly-review">
              {t(
                ($) => $.common.home.timeline.create.confirmation.weeklyReview,
              )}
            </option>
            <option value="silent">
              {t(($) => $.common.home.timeline.create.confirmation.silent)}
            </option>
            <option value="auto-complete">
              {t(
                ($) => $.common.home.timeline.create.confirmation.autoComplete,
              )}
            </option>
            <option value="auto-not-completed">
              {t(
                ($) =>
                  $.common.home.timeline.create.confirmation.autoNotCompleted,
              )}
            </option>
            <option value="infer-provisional">
              {t(
                ($) =>
                  $.common.home.timeline.create.confirmation.inferProvisional,
              )}
            </option>
          </select>
        </label>

        <label className="temporal-create-control">
          <span>
            {t(($) => $.common.home.timeline.create.confirmation.reminder)}
          </span>
          <select
            aria-label={t(
              ($) => $.common.home.timeline.create.confirmation.reminder,
            )}
            data-create-path="confirmation.reminderLeadMinutes"
            value={
              confirmation.reminderLeadMinutes === null
                ? 'none'
                : String(confirmation.reminderLeadMinutes)
            }
            onChange={(event) =>
              patchConfirmation({
                reminderLeadMinutes:
                  event.currentTarget.value === 'none'
                    ? null
                    : Number(event.currentTarget.value),
              })
            }
          >
            {TEMPORAL_CREATE_REMINDER_OPTIONS.map((minutes) => (
              <option
                key={minutes === null ? 'none' : minutes}
                value={minutes === null ? 'none' : minutes}
              >
                {minutes === null
                  ? t(
                      ($) =>
                        $.common.home.timeline.create.confirmation.noReminder,
                    )
                  : minutes === 0
                    ? t(
                        ($) =>
                          $.common.home.timeline.create.confirmation.atStart,
                      )
                    : t(
                        ($) =>
                          $.common.home.timeline.create.confirmation.before,
                        {
                          value: temporalCreateDurationLabel(minutes),
                        },
                      )}
              </option>
            ))}
          </select>
          {renderError('confirmation.reminderLeadMinutes')}
        </label>
      </div>

      {confirmation.outcomePolicy === 'infer-provisional' ? (
        <p className="temporal-create-truth-note">
          {t(($) => $.common.home.timeline.create.confirmation.inferNote)}
        </p>
      ) : null}
      <p className="temporal-create-truth-note">
        {t(($) => $.common.home.timeline.create.confirmation.deliveryNote)}
      </p>
    </section>
  );
}
