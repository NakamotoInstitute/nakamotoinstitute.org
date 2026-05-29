import { NextRequest, NextResponse } from "next/server";

import { defaultLocale, isLocale } from "@/i18n";
import { api, type SearchResponse } from "@/lib/api";
import { rateLimit } from "@/lib/rateLimit";
import { searchResultHref } from "@/lib/searchResultHref";

export const dynamic = "force-dynamic";

const CATEGORIES = [
  "satoshi",
  "library",
  "mempool",
  "authors",
  "podcasts",
] as const;

// NUL + C0/C1 control characters. Normal whitespace (tab/newline/CR etc.)
// is already collapsed to single spaces before this test runs, so any
// control char that survives is genuinely disallowed input.
const CONTROL_CHARS = new RegExp(
  `[${String.fromCharCode(0)}-${String.fromCharCode(0x1f)}${String.fromCharCode(0x7f)}-${String.fromCharCode(0x9f)}]`,
);

function emptyResult(q: string): SearchResponse {
  return {
    query: q,
    total: 0,
    countsByCategory: {
      satoshi: 0,
      library: 0,
      mempool: 0,
      authors: 0,
      podcasts: 0,
    },
    results: [],
  };
}

export async function GET(req: NextRequest) {
  const { allowed, retryAfter } = rateLimit(req);
  if (!allowed) {
    return NextResponse.json(
      { error: "rate_limited" },
      {
        status: 429,
        headers: {
          "Retry-After": String(retryAfter),
          "Cache-Control": "no-store",
        },
      },
    );
  }

  const sp = req.nextUrl.searchParams;

  const q = (sp.get("q") ?? "").normalize("NFC").replace(/\s+/g, " ").trim();
  if (q.length === 0) {
    return NextResponse.json(emptyResult(q), {
      headers: { "Cache-Control": "no-store" },
    });
  }
  if (q.length > 100 || CONTROL_CHARS.test(q)) {
    return NextResponse.json(
      { error: "bad_query" },
      { status: 400, headers: { "Cache-Control": "no-store" } },
    );
  }

  const localeRaw = sp.get("locale") ?? defaultLocale;
  const locale = isLocale(localeRaw) ? localeRaw : defaultLocale;

  const categoryRaw = sp.get("category");
  const category = CATEGORIES.includes(
    categoryRaw as (typeof CATEGORIES)[number],
  )
    ? categoryRaw!
    : undefined;

  const page = Math.min(
    Math.max(parseInt(sp.get("page") ?? "1", 10) || 1, 1),
    200,
  );

  // `cache: "no-store"` overrides the shared client's production `force-cache`:
  // search responses must never be cached (they go stale after an index rebuild
  // and would balloon the data cache, one entry per distinct query). The abort
  // signal is a backstop above the backend's own 3s statement_timeout so a hung
  // or unreachable backend can't hold the request to the platform limit; a thrown
  // fetch (network error / timeout) degrades to the empty 502 contract, never a 500.
  const result = await api.search
    .search({
      query: { q, locale, category, page },
      cache: "no-store",
      signal: AbortSignal.timeout(5000),
    })
    .catch(() => null);

  if (!result || result.error || !result.data) {
    return NextResponse.json(emptyResult(q), {
      status: 502,
      headers: { "Cache-Control": "no-store" },
    });
  }

  const { data } = result;

  // Enrich each result with a server-built href so the client palette never
  // imports urls() (which reads server-only env and cannot run in the browser).
  const results = data.results.map((item) => ({
    ...item,
    href: searchResultHref(locale, item),
  }));

  return NextResponse.json(
    { ...data, results },
    { headers: { "Cache-Control": "no-store" } },
  );
}
