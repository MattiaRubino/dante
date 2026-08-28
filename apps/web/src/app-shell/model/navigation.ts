export type AppDestinationId =
  | 'home'
  | 'worlds'
  | 'today'
  | 'profile'
  | 'settings';

export type AppDestinationPath =
  | '/home'
  | '/worlds'
  | '/today'
  | '/profile'
  | '/settings';

export type AppDestination = {
  id: AppDestinationId;
  to: AppDestinationPath;
  placement: 'primary' | 'account';
  searchable: boolean;
};

const HOME_DESTINATION = {
  id: 'home',
  to: '/home',
  placement: 'primary',
  searchable: true,
} as const;
const WORLDS_DESTINATION = {
  id: 'worlds',
  to: '/worlds',
  placement: 'primary',
  searchable: true,
} as const;
const TODAY_DESTINATION = {
  id: 'today',
  to: '/today',
  placement: 'primary',
  searchable: true,
} as const;
const PROFILE_DESTINATION = {
  id: 'profile',
  to: '/profile',
  placement: 'account',
  searchable: true,
} as const;
const SETTINGS_DESTINATION = {
  id: 'settings',
  to: '/settings',
  placement: 'account',
  searchable: true,
} as const;

export const PRIMARY_DESTINATIONS = [
  HOME_DESTINATION,
  WORLDS_DESTINATION,
  TODAY_DESTINATION,
] as const;

export const APP_DESTINATIONS = [
  ...PRIMARY_DESTINATIONS,
  PROFILE_DESTINATION,
  SETTINGS_DESTINATION,
] as const satisfies readonly AppDestination[];

export const LAUNCHER_DESTINATIONS = PRIMARY_DESTINATIONS;

export function getDestination(id: AppDestinationId) {
  const destination = APP_DESTINATIONS.find((item) => item.id === id);

  if (!destination) {
    throw new Error(`Unknown app destination: ${id}`);
  }

  return destination;
}
