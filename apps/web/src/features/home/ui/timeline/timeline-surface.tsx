import { useTranslation } from 'react-i18next';

type TimelineSurfaceProps = {
  expanded: boolean;
  onToggleExpanded: () => void;
};

const FOUNDATION_DAYS = ['L', 'M', 'M', 'G', 'V', 'S', 'D'] as const;
const FOUNDATION_HOURS = ['00', '06', '12', '18', '24'] as const;

export function TimelineSurface({
  expanded,
  onToggleExpanded,
}: TimelineSurfaceProps) {
  const { t } = useTranslation('common');

  return (
    <section
      className="home-timeline"
      data-home-region="timeline"
      data-home-timeline-state={expanded ? 'expanded' : 'normal'}
      aria-label={t(($) => $.common.home.timeline.label)}
    >
      <header className="home-timeline-head">
        <div className="home-timeline-title-zone">
          <span className="home-timeline-month-foundation" aria-hidden="true" />
          <h2>{t(($) => $.common.home.timeline.title)}</h2>
        </div>

        <div className="home-timeline-week" aria-hidden="true">
          {FOUNDATION_DAYS.map((day, index) => (
            <span className={index === 1 ? 'is-active' : ''} key={`${day}-${index}`}>
              <small>{day}</small>
              <strong>{index + 3}</strong>
            </span>
          ))}
        </div>

        <div className="home-timeline-actions-foundation" aria-hidden="true">
          <span />
          <span />
        </div>
      </header>

      <div className="home-timeline-frame" aria-hidden="true">
        <div className="home-timeline-ruler">
          {FOUNDATION_HOURS.map((hour) => (
            <span key={hour}>{hour}</span>
          ))}
        </div>

        <div className="home-timeline-grid-foundation">
          <span className="home-timeline-now-line" />
          <span className="home-timeline-event event-one" />
          <span className="home-timeline-event event-two" />
          <span className="home-timeline-event event-three" />
          <span className="home-timeline-event event-four" />
        </div>
      </div>

      <button
        className="home-timeline-expand-handle"
        type="button"
        onClick={onToggleExpanded}
        aria-label={t(($) =>
          expanded
            ? $.common.home.timeline.collapse
            : $.common.home.timeline.expand,
        )}
        aria-pressed={expanded}
      >
        <span aria-hidden="true">{expanded ? '‹' : '›'}</span>
      </button>
    </section>
  );
}
