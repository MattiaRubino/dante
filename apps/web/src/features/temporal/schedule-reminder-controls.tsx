import { useEffect, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';

import {
  createRemoteScheduleReminderDataSource,
  type ScheduleReminderView,
} from './remote-schedule-reminder-data-source';

const REMINDER_LEADS = [0, 5, 15, 30, 60, 120, 1440] as const;

export function ScheduleReminderControls({ scheduleRef, hideWhenAbsent = false }: Readonly<{ scheduleRef: string; hideWhenAbsent?: boolean }>) {
  const { t } = useTranslation('common');
  const [source] = useState(() => createRemoteScheduleReminderDataSource());
  const [current, setCurrent] = useState<ScheduleReminderView | null>(null);
  const [enabled, setEnabled] = useState(true);
  const [leadMinutes, setLeadMinutes] = useState(15);
  const [loading, setLoading] = useState(true);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState(false);
  const [readFailed, setReadFailed] = useState(false);
  const [reload, setReload] = useState(0);
  const attemptRef = useRef<{ fingerprint: string; operationId: string } | null>(null);

  useEffect(() => {
    let active = true;
    setLoading(true);
    setCurrent(null);
    setError(false);
    setReadFailed(false);
    attemptRef.current = null;
    void source.get(scheduleRef).then((value) => {
      if (!active) return;
      setCurrent(value);
      setEnabled(value?.enabled ?? true);
      setLeadMinutes(value?.leadMinutes ?? 15);
      setLoading(false);
    }).catch(() => {
      if (active) {
        setError(true);
        setReadFailed(true);
        setLoading(false);
      }
    });
    return () => { active = false; };
  }, [scheduleRef, source, reload]);

  const save = async () => {
    if (pending || loading || readFailed) return;
    const fingerprint = JSON.stringify([scheduleRef, current?.materialStateRef ?? null, enabled, leadMinutes]);
    const prior = attemptRef.current;
    const operationId = prior?.fingerprint === fingerprint
      ? prior.operationId : crypto.randomUUID();
    attemptRef.current = { fingerprint, operationId };
    setPending(true);
    setError(false);
    try {
      const value = await source.configure(scheduleRef, {
        operationId,
        expectedMaterialStateRef: current?.materialStateRef ?? null,
        enabled,
        leadMinutes,
      });
      setCurrent(value);
      attemptRef.current = null;
    } catch {
      setError(true);
    } finally {
      setPending(false);
    }
  };

  if (hideWhenAbsent && (loading || (!readFailed && current === null))) return null;

  return (
    <div className="timeline-reminder-controls" data-schedule-reminder={scheduleRef}>
      <strong>{t(($) => $.common.home.timeline.detail.reminder.title)}</strong>
      {loading ? <span>{t(($) => $.common.home.timeline.detail.reminder.loading)}</span> : readFailed ? (
        <button type="button" onClick={() => setReload((value) => value + 1)}>
          {t(($) => $.common.home.timeline.detail.reminder.retryRead)}
        </button>
      ) : (
        <>
          <label>
            <input type="checkbox" checked={enabled} disabled={pending}
              onChange={(event) => setEnabled(event.currentTarget.checked)} />
            {t(($) => $.common.home.timeline.detail.reminder.enabled)}
          </label>
          <label>
            {t(($) => $.common.home.timeline.detail.reminder.lead)}
            <select value={leadMinutes} disabled={pending}
              onChange={(event) => setLeadMinutes(Number(event.currentTarget.value))}>
              {[...new Set<number>([...REMINDER_LEADS, leadMinutes])].sort((a, b) => a - b)
                .map((minutes) => <option key={minutes} value={minutes}>{minutes}</option>)}
            </select>
          </label>
          <button type="button" disabled={pending} onClick={() => void save()}>
            {t(($) => $.common.home.timeline.detail.reminder.save)}
          </button>
          {current ? <span role="status">
            {t(($) => $.common.home.timeline.detail.reminder[current.disposition])}
            {current.dueAt ? ` · ${new Date(current.dueAt).toLocaleString()}` : ''}
          </span> : null}
        </>
      )}
      {error ? <span role="alert">{t(($) => $.common.home.timeline.detail.reminder.error)}</span> : null}
    </div>
  );
}
