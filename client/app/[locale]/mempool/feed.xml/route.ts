import { Locale, api } from "@/lib/api";

export const dynamic = "force-static";

export async function GET(
  _request: Request,
  ctx: RouteContext<"/[locale]/mempool/feed.xml">,
) {
  const { locale } = await ctx.params;
  const { data: content = "" } = await api.mempool.generateFeed({
    query: { locale: locale as Locale, format: "rss" },
  });

  return new Response(content, {
    headers: {
      "Content-Type": "application/rss+xml",
      "Content-Disposition": 'attachment; filename="feed.xml"',
    },
  });
}
