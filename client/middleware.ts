import { NextRequest, NextResponse } from "next/server";
import { i18nRoutingMiddleware, subdomainRouting } from "./lib/middleware";

const prodDomainToPathMapping = [
  {
    domain: process.env.SATOSHI_HOST as string,
    path: "/satoshi",
  },
];

const localDomainToPathMapping = [
  {
    domain: "satoshi.localhost",
    path: "/satoshi",
  },
];

export const domainToPathMapping = (() => {
  switch (process.env.VERCEL_ENV) {
    case "development":
      return localDomainToPathMapping;
    case "production":
      return prodDomainToPathMapping;
    default:
      return [];
  }
})();

export default function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const domainRewrite = subdomainRouting(request);

  const isRpowRequest = /^\/finney\/rpow\/.+/i.test(pathname);

  if (!domainRewrite && isRpowRequest) {
    return NextResponse.next();
  }

  return i18nRoutingMiddleware(request);
}

export const config = {
  // Skip all paths that should not be internationalized. This example skips the
  // folders "api", "_next" and all files with an extension (e.g. favicon.ico)
  matcher: [
    "/((?!api/|_next/static|_next/image|favicon.ico|img/|static/|satoshinakamoto.asc).*)",
  ],
};
