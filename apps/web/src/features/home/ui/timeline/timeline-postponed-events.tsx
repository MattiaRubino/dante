import type { LifeArea } from '../../../temporal/remote-organization';

/**
 * B14 product consolidation: postponed Events now live in the same canonical
 * `Da collocare` tray as unplaced Activities and never-placed Events.
 *
 * Keep this compatibility component mounted until the broader Timeline cleanup
 * removes the historical import from TimelineSurface; rendering a second panel
 * would duplicate one canonical state in two product surfaces.
 */
export function TimelinePostponedEventsPanel({
  enabled: _enabled,
  areas: _areas,
}: Readonly<{
  enabled: boolean;
  areas: readonly LifeArea[];
}>) {
  return null;
}
