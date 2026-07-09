import { notFound } from "next/navigation";

import { isLocale } from "@/i18n";
import { api } from "@/lib/api";

export const dynamic = "force-static";

export async function GET(
  _request: Request,
  ctx: RouteContext<"/[locale]/mempool/feed.xml">,
) {
  const { locale } = await ctx.params;
  if (!isLocale(locale)) notFound();
  const result = await api.mempool.generateFeed({
    query: { locale, format: "rss" },
  });
  const { data: content, error, response } = result;
  if (content === undefined) {
    if (response?.status === 404) notFound();
    throw error instanceof Error
      ? error
      : new Error("Failed to generate mempool RSS feed");
  }

  return new Response(content, {
    headers: {
      "Content-Type": "application/rss+xml",
      "Content-Disposition": 'attachment; filename="feed.xml"',
    },
  });
}
