import { NextRequest, NextResponse } from "next/server";

import { i18nRoutingProxy } from "@/lib/proxy/i18n";
import { subdomainRouting } from "@/lib/proxy/subdomains";

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Detect subdomain mapping (but don't apply yet)
  const subdomainResult = subdomainRouting(request);

  // RPOW bypass - only serve on main domain (no subdomain mapping)
  const isRpowRequest = /^\/finney\/rpow\/.+/i.test(pathname);
  if (!subdomainResult.mapping && isRpowRequest) {
    return NextResponse.next();
  }

  // Sitemap - subdomain-specific routing
  if (pathname === "/sitemap.xml") {
    if (subdomainResult.mapping) {
      return NextResponse.rewrite(
        new URL(`/en${subdomainResult.mapping.path}/sitemap.xml`, request.url),
      );
    }
    return NextResponse.next();
  }

  // Run i18n routing on original path (before subdomain prefix)
  const i18nResponse = i18nRoutingProxy(request);

  // If subdomain mapping exists, insert subdomain path after locale
  if (subdomainResult.mapping) {
    // If i18n returned a redirect, pass it through
    if (
      i18nResponse instanceof NextResponse &&
      i18nResponse.status >= 300 &&
      i18nResponse.status < 400
    ) {
      return i18nResponse;
    }

    const rewriteHeader = i18nResponse?.headers.get("x-middleware-rewrite");

    // Determine the path to transform (either from rewrite header or original)
    const pathToTransform = rewriteHeader
      ? new URL(rewriteHeader).pathname
      : request.nextUrl.pathname;

    // Insert subdomain path after locale: /en/foo -> /en/satoshi/foo
    const parts = pathToTransform.split("/").filter(Boolean);
    if (parts.length > 0) {
      // Insert subdomain path after first segment (locale)
      parts.splice(1, 0, subdomainResult.mapping.path.replace(/^\//, ""));
      const newPathname = `/${parts.join("/")}`;
      // Preserve query params
      const search = request.nextUrl.search;
      return NextResponse.rewrite(new URL(newPathname + search, request.url));
    } else {
      // Root path, just add subdomain
      return NextResponse.rewrite(
        new URL(subdomainResult.mapping.path, request.url),
      );
    }
  }

  return i18nResponse;
}

export const config = {
  // Skip all paths that should not be localized.
  matcher: [
    "/((?!api/|_next/|_vercel/|\\.well-known/|favicon\\.ico$|icon\\.png$|apple-icon.png$|manifest\\.webmanifest$|satoshinakamoto\\.asc$).*)",
  ],
};
