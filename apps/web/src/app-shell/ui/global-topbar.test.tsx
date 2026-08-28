import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import {
  Outlet,
  RouterProvider,
  createMemoryHistory,
  createRootRoute,
  createRoute,
  createRouter,
} from '@tanstack/react-router';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../bootstrap/i18n';
import { GlobalTopbar } from './global-topbar';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

async function renderTopbar(initialPath = '/home') {
  const rootRoute = createRootRoute({
    component: () => (
      <>
        <GlobalTopbar />
        <Outlet />
      </>
    ),
  });

  const routes = [
    createRoute({
      getParentRoute: () => rootRoute,
      path: '/home',
      component: () => <div>Home route</div>,
    }),
    createRoute({
      getParentRoute: () => rootRoute,
      path: '/worlds',
      component: () => <div>Worlds route</div>,
    }),
    createRoute({
      getParentRoute: () => rootRoute,
      path: '/today',
      component: () => <div>Today route</div>,
    }),
    createRoute({
      getParentRoute: () => rootRoute,
      path: '/profile',
      component: () => <div>Profile route</div>,
    }),
    createRoute({
      getParentRoute: () => rootRoute,
      path: '/settings',
      component: () => <div>Settings route</div>,
    }),
  ];

  const router = createRouter({
    routeTree: rootRoute.addChildren(routes),
    history: createMemoryHistory({ initialEntries: [initialPath] }),
  });

  await router.load();
  render(<RouterProvider router={router} />);
  return router;
}

describe('GlobalTopbar', () => {
  it('navigates through real application destinations', async () => {
    const router = await renderTopbar();

    fireEvent.click(screen.getByRole('link', { name: 'Mondi' }));
    await waitFor(() => expect(router.state.location.pathname).toBe('/worlds'));

    fireEvent.click(screen.getByRole('link', { name: 'Oggi' }));
    await waitFor(() => expect(router.state.location.pathname).toBe('/today'));
  });

  it('opens keyboard-first search and navigates the selected local result', async () => {
    const router = await renderTopbar();

    fireEvent.keyDown(document, { key: 'k', ctrlKey: true });
    expect(
      await screen.findByRole('dialog', { name: 'Cerca in DANTE' }),
    ).toBeTruthy();

    const input = screen.getByRole('combobox', { name: 'Cerca in DANTE' });
    fireEvent.change(input, { target: { value: 'oggi' } });
    fireEvent.keyDown(input, { key: 'Enter' });

    await waitFor(() => expect(router.state.location.pathname).toBe('/today'));
    expect(screen.queryByRole('dialog', { name: 'Cerca in DANTE' })).toBeNull();
  });

  it('supports slash search without hijacking editable controls', async () => {
    await renderTopbar();

    const editor = document.createElement('input');
    document.body.append(editor);
    editor.focus();

    fireEvent.keyDown(editor, { key: '/' });
    expect(screen.queryByRole('dialog', { name: 'Cerca in DANTE' })).toBeNull();

    editor.remove();
    fireEvent.keyDown(document, { key: '/' });
    expect(
      await screen.findByRole('dialog', { name: 'Cerca in DANTE' }),
    ).toBeTruthy();
  });

  it('restores search focus and starts each command session clean', async () => {
    await renderTopbar();

    const trigger = screen.getByRole('button', { name: 'Cerca in DANTE' });
    trigger.focus();
    fireEvent.click(trigger);

    const input = await screen.findByRole('combobox', {
      name: 'Cerca in DANTE',
    });
    fireEvent.change(input, { target: { value: 'mondi' } });
    expect((input as HTMLInputElement).value).toBe('mondi');

    fireEvent.keyDown(document, { key: 'Escape' });
    await waitFor(() => expect(document.activeElement).toBe(trigger));

    fireEvent.click(trigger);
    const reopenedInput = await screen.findByRole('combobox', {
      name: 'Cerca in DANTE',
    });
    expect((reopenedInput as HTMLInputElement).value).toBe('');
  });

  it('keeps create truthful and exposes launcher/account shells without fake writes', async () => {
    await renderTopbar();

    fireEvent.click(screen.getByRole('button', { name: 'Crea' }));
    expect(screen.getByRole('menu', { name: 'Crea' })).toBeTruthy();
    expect(
      screen
        .getByRole('menuitem', { name: /Evento/ })
        .getAttribute('aria-disabled'),
    ).toBe('true');

    fireEvent.click(screen.getByRole('button', { name: 'Apri launcher' }));
    expect(screen.getByRole('menu', { name: 'Launcher DANTE' })).toBeTruthy();

    fireEvent.click(screen.getByRole('button', { name: 'Account' }));
    expect(screen.getByRole('menu', { name: 'Menu account' })).toBeTruthy();
    expect(
      screen
        .getByRole('menuitem', { name: /Esci/ })
        .getAttribute('aria-disabled'),
    ).toBe('true');
  });

  it('closes a menu with Escape and restores focus to its trigger', async () => {
    await renderTopbar();

    const trigger = screen.getByRole('button', { name: 'Account' });
    fireEvent.click(trigger);
    expect(screen.getByRole('menu', { name: 'Menu account' })).toBeTruthy();

    fireEvent.keyDown(document, { key: 'Escape' });
    expect(screen.queryByRole('menu', { name: 'Menu account' })).toBeNull();
    expect(document.activeElement).toBe(trigger);
  });
});
