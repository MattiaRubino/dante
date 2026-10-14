/** Assert the rendered control type before reading control-specific state. */
export function domElement<T extends HTMLElement>(
  element: HTMLElement,
  constructor: new () => T,
): T {
  if (!(element instanceof constructor)) {
    throw new Error(`Expected ${constructor.name}, got ${element.tagName}.`);
  }
  return element;
}
