import { NextRequest } from "next/server";

import { domainToPathMapping } from "@/lib/urls";

const combinePath = (...parts: (string | undefined)[]) =>
  parts
    .filter((part) => part !== undefined)
    .map((part, i) => {
      if (i > 0) {
        part = part.replace(/^\/+/, "");
      }
      if (i < parts.length - 1) {
        part = part.replace(/\/+$/, "");
      }
      return part;
    })
    .join("/");

export type SubdomainRoutingResult = {
  mapping: (typeof domainToPathMapping)[number] | null;
  newPathname: string;
};

export const subdomainRouting = (
  request: NextRequest,
): SubdomainRoutingResult => {
  const [domain] = request.headers.get("host")?.split(":") ?? [];
  const mapping = domainToPathMapping.find((map) => map.domain === domain);

  if (mapping) {
    const newPathname = combinePath(mapping.path, request.nextUrl.pathname);
    return { mapping, newPathname };
  }

  return { mapping: null, newPathname: request.nextUrl.pathname };
};
