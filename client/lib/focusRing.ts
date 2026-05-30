/**
 * Shared keyboard-focus treatments for the search UI.
 *
 * The site defines no global :focus-visible style, so interactive elements fall
 * back to the browser default (a blue ring). These tokens replace it with the
 * site's cardinal accent, shown only to keyboard users via :focus-visible so
 * pointer interactions stay unadorned.
 */

/** Cardinal ring hugging buttons and pill-shaped controls. */
export const focusRing =
  "focus-visible:outline-hidden focus-visible:ring-2 focus-visible:ring-cardinal";

/**
 * Inset variant for full-bleed controls (e.g. a flush, edge-to-edge button)
 * whose outer ring would be clipped by a rounded container.
 */
export const focusRingInset =
  "focus-visible:outline-hidden focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-cardinal";

/** Cardinal underline for text links — wraps gracefully across line breaks. */
export const focusUnderline =
  "focus-visible:outline-hidden focus-visible:underline focus-visible:decoration-cardinal focus-visible:decoration-2 focus-visible:underline-offset-2";
