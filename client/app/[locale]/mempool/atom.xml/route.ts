import { notFound } from "next/navigation";

import { isLocale } from "@/i18n";
import { api } from "@/lib/api";
import { getLocaleParams } from "@/lib/i18n/utils";

// Prerender at build like every other route. Without generateStaticParams
// this rendered lazily at runtime, where fetch reads Vercel's Data Cache —
// which persists across deployments, so the feed kept serving pre-deploy
// API output (stale feeds, 2026-07).
export const dynamic = "force-static";
export const dynamicParams = false;

export async function generateStaticParams() {
  return getLocaleParams();
}

export async function GET(
  _request: Request,
  ctx: RouteContext<"/[locale]/mempool/atom.xml">,
) {
  const { locale } = await ctx.params;
  if (!isLocale(locale)) notFound();
  const result = await api.mempool.generateFeed({
    query: { locale, format: "atom" },
  });
  const { data: content, error, response } = result;
  if (content === undefined) {
    if (response?.status === 404) notFound();
    throw error instanceof Error
      ? error
      : new Error("Failed to generate mempool Atom feed");
  }

  return new Response(content, {
    headers: {
      "Content-Type": "application/atom+xml",
      "Content-Disposition": 'attachment; filename="atom.xml"',
    },
  });
}
