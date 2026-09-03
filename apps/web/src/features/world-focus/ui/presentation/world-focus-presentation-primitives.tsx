import {
  useId,
  type ComponentPropsWithoutRef,
  type ReactNode,
} from 'react';

import './world-focus-presentation.css';

type WorldFocusPresentationSectionProps = Omit<
  ComponentPropsWithoutRef<'section'>,
  'children' | 'title'
> &
  Readonly<{
    title: string;
    qualification?: string | null;
    children: ReactNode;
  }>;

export function WorldFocusPresentationSection({
  title,
  qualification = null,
  children,
  className,
  ...sectionProps
}: WorldFocusPresentationSectionProps) {
  const headingId = useId();
  const sectionClassName = [
    'world-focus-presentation-section',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <section
      {...sectionProps}
      className={sectionClassName}
      aria-labelledby={headingId}
      data-world-focus-presentation="section"
    >
      <div className="world-focus-presentation-heading">
        <h2 className="world-focus-presentation-title" id={headingId}>
          {title}
        </h2>
        {qualification === null ? null : (
          <p className="world-focus-presentation-qualification" role="status">
            {qualification}
          </p>
        )}
      </div>
      {children}
    </section>
  );
}

type WorldFocusPresentationSubsectionProps = Omit<
  ComponentPropsWithoutRef<'div'>,
  'children' | 'title'
> &
  Readonly<{
    title: string;
    children: ReactNode;
  }>;

export function WorldFocusPresentationSubsection({
  title,
  children,
  className,
  ...groupProps
}: WorldFocusPresentationSubsectionProps) {
  const headingId = useId();
  const groupClassName = ['world-focus-presentation-subsection', className]
    .filter(Boolean)
    .join(' ');

  return (
    <div
      {...groupProps}
      className={groupClassName}
      role="group"
      aria-labelledby={headingId}
    >
      <h3 className="world-focus-presentation-subheading" id={headingId}>
        {title}
      </h3>
      {children}
    </div>
  );
}

type WorldFocusPresentationStateProps = Readonly<{
  state: string;
  children: ReactNode;
}>;

export function WorldFocusPresentationState({
  state,
  children,
}: WorldFocusPresentationStateProps) {
  return (
    <span
      className="world-focus-presentation-state"
      data-world-focus-state={state}
    >
      {children}
    </span>
  );
}
