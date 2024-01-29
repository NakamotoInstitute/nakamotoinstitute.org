import { NextRequest, NextResponse } from "next/server";

import { defaultLocale, locales } from "@/i18n";

// Portions of i18n middleware code adapted from next-intl
// https://github.com/amannn/next-intl
//
// MIT License
//
// Copyright (c) 2020 Jan Amann

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

function getPathnameToken(pathname: string, i: number) {
  return pathname?.split("/")[i];
}

function getLocaleFromPathname(pathname: string) {
  const localeCandidate = getPathnameToken(pathname, 1);
  const satoshiPath = localeCandidate === "satoshi";
  const pathLocale = satoshiPath
    ? getPathnameToken(pathname, 2)
    : localeCandidate;
  return { satoshiPath, pathLocale };
}

function resolveLocale(request: NextRequest) {
  let locale: Locale;
  const { pathLocale, ...rest } = getLocaleFromPathname(
    request.nextUrl.pathname,
  );
  if (locales.includes(pathLocale as Locale)) {
    locale = pathLocale as Locale;
  } else {
    locale = defaultLocale;
  }

  return { locale, ...rest };
}

export function i18nRoutingMiddleware(request: NextRequest) {
  const { locale } = resolveLocale(request);

  const isRoot = request.nextUrl.pathname === "/";
  const hasMatchedDefaultLocale = locale === defaultLocale;

  function rewrite(url: string) {
    return NextResponse.rewrite(new URL(url, request.url));
  }

  function redirect(url: string) {
    const urlObj = new URL(url, request.url);
    return NextResponse.redirect(urlObj.toString());
  }

  let response;

  if (isRoot) {
    let pathWithSearch = `/${locale}`;
    if (request.nextUrl.search) {
      pathWithSearch += request.nextUrl.search;
    }

    if (hasMatchedDefaultLocale) {
      response = NextResponse.rewrite(new URL(pathWithSearch, request.url));
    }
  } else {
    const { pathLocale: pathLocaleCandidate, satoshiPath } =
      getLocaleFromPathname(request.nextUrl.pathname);
    const pathLocale = locales.includes(pathLocaleCandidate as Locale)
      ? pathLocaleCandidate
      : undefined;
    const hasLocalePrefix = pathLocale !== undefined;

    let pathWithSearch = request.nextUrl.pathname;
    if (request.nextUrl.search) {
      pathWithSearch += request.nextUrl.search;
    }

    if (hasLocalePrefix) {
      const basePath = pathWithSearch.replace(`/${pathLocale}`, "") || "/";

      if (pathLocale === locale) {
        if (hasMatchedDefaultLocale) {
          response = redirect(basePath);
        } else {
          response = satoshiPath
            ? rewrite(pathWithSearch)
            : NextResponse.next();
        }
      }
    } else {
      if (hasMatchedDefaultLocale) {
        let rewriteUrl = `/${locale}${pathWithSearch}`;
        if (satoshiPath) {
          const parts = rewriteUrl.split("/");
          const temp = parts[1];
          parts[1] = parts[2];
          parts[2] = temp;
          rewriteUrl = parts.join("/");
        }
        response = rewrite(rewriteUrl);
      } else {
        response = redirect(`/${locale}${pathWithSearch}`);
      }
    }
  }

  return response;
}
