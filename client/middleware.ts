import { NextRequest, NextResponse } from "next/server";

import { i18nRoutingMiddleware } from "@/lib/middleware/i18n";
import { subdomainRouting } from "@/lib/middleware/subdomains";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const domainRewrite = subdomainRouting(request);

  const isRpowRequest = /^\/finney\/rpow\/.+/i.test(pathname);

  if (!domainRewrite && isRpowRequest) {
    return NextResponse.next();
  }

  if (pathname === "/sitemap.xml") {
    if (domainRewrite) {
      return NextResponse.rewrite(
        new URL(`${domainRewrite.path}/sitemap.xml`, request.url),
      );
    }
    return NextResponse.next();
  }

  return i18nRoutingMiddleware(request);
}

export const config = {
  // Skip all paths that should not be localized.
  matcher: [
    "/((?!api/|_next/|_vercel/|\\.well-known/|favicon\\.ico$|satoshinakamoto\\.asc$).*)",
  ],
};
