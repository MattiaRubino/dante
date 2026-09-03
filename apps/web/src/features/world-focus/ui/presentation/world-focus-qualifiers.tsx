import type {
  ComponentPropsWithoutRef,
  ReactNode,
} from 'react';

type WorldFocusQualifierGroupProps = ComponentPropsWithoutRef<'div'> &
  Readonly<{
    children: ReactNode;
  }>;

export function WorldFocusQualifierGroup({
  children,
  className,
  ...groupProps
}: WorldFocusQualifierGroupProps) {
  const groupClassName = ['world-focus-qualifier-group', className]
    .filter(Boolean)
    .join(' ');

  return (
    <div
      {...groupProps}
      className={groupClassName}
      data-world-focus-qualifier-group="true"
    >
      {children}
    </div>
  );
}

type WorldFocusQualifierProps = Omit<
  ComponentPropsWithoutRef<'span'>,
  'children'
> &
  Readonly<{
    axis: string;
    state: string;
    children: ReactNode;
  }>;

export function WorldFocusQualifier({
  axis,
  state,
  children,
  className,
  ...qualifierProps
}: WorldFocusQualifierProps) {
  const qualifierClassName = ['world-focus-qualifier', className]
    .filter(Boolean)
    .join(' ');

  return (
    <span
      {...qualifierProps}
      className={qualifierClassName}
      data-world-focus-qualifier-axis={axis}
      data-world-focus-qualifier-state={state}
    >
      {children}
    </span>
  );
}
