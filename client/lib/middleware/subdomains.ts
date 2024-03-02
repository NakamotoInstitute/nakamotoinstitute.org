import { NextRequest } from "next/server";

import { domainToPathMapping } from "@/middleware";

const combinePath = (...parts: (string | undefined)[]) =>
  parts
    .filter((part) => part !== undefined)
    .map((part, i) => {
      if (i > 0) {
        part = part?.replace(/^\/+/, "");
      }
      if (i < parts.length - 1) {
        part = part?.replace(/\/+$/, "");
      }
      return part;
    })
    .join("/");

export const subdomainRouting = (request: NextRequest) => {
  const [domain] = request?.headers?.get("host")?.split(":") ?? [];
  const domainRewrite = domainToPathMapping.find(
    (map) => map.domain === domain,
  );
  if (domainRewrite) {
    request.nextUrl.pathname = combinePath(
      domainRewrite.path,
      request.nextUrl.pathname,
    );
  }
  return domainRewrite;
};
