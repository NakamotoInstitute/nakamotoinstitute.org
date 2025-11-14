import { NextRequest, NextResponse } from "next/server";

import { defaultLocale, locales } from "@/i18n";

/**
 * Extract locale prefix from pathname (first segment after /)
 * Returns undefined if no locale prefix or not a valid locale
 */
function getLocalePrefix(pathname: string): Locale | undefined {
  const firstSegment = pathname.split("/")[1];
  return locales.includes(firstSegment as Locale)
    ? (firstSegment as Locale)
    : undefined;
}

/**
 * Resolve the locale for this request
 * If path has valid locale prefix, use it; otherwise use default
 */
function resolveLocale(pathname: string): Locale {
  return getLocalePrefix(pathname) ?? defaultLocale;
}

/**
 * i18n routing middleware
 *
 * Routing rules:
 * 1. Root path (/) → rewrite to /en (default locale)
 * 2. Path without locale (/library/) → rewrite to /en/library/ (default) or redirect to /es/library/ (non-default)
 * 3. Path with default locale (/en/library/) → redirect to /library/ (strip default locale)
 * 4. Path with non-default locale (/es/library/) → pass through (already correct)
 */
export function i18nRoutingProxy(request: NextRequest) {
  const { pathname, search } = request.nextUrl;
  const locale = resolveLocale(pathname);
  const localePrefix = getLocalePrefix(pathname);
  const isDefaultLocale = locale === defaultLocale;

  // Helper to build path with query params
  const withSearch = (path: string) => (search ? `${path}${search}` : path);

  // Case 1: Root path → rewrite to /en (or default locale)
  if (pathname === "/") {
    return NextResponse.rewrite(new URL(withSearch(`/${locale}`), request.url));
  }

  // Case 2: Path has locale prefix
  if (localePrefix) {
    // Case 2a: Default locale prefix (/en/...) → redirect to remove it
    if (isDefaultLocale) {
      const pathWithoutLocale = pathname.replace(`/${localePrefix}`, "") || "/";
      return NextResponse.redirect(
        new URL(withSearch(pathWithoutLocale), request.url),
      );
    }

    // Case 2b: Non-default locale prefix (/es/...) → pass through
    return NextResponse.next();
  }

  // Case 3: No locale prefix
  // Case 3a: Default locale → rewrite to add /en prefix
  if (isDefaultLocale) {
    return NextResponse.rewrite(
      new URL(withSearch(`/${locale}${pathname}`), request.url),
    );
  }

  // Case 3b: Non-default locale → redirect to add locale prefix
  return NextResponse.redirect(
    new URL(withSearch(`/${locale}${pathname}`), request.url),
  );
}
