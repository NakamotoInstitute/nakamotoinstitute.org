import { getMempoolFeed } from "@/lib/api/mempool";

export const dynamic = "force-static";

export async function GET(
  _request: Request,
  ctx: RouteContext<"/[locale]/mempool/feed.xml">,
) {
  const { locale } = await ctx.params;
  const content = await getMempoolFeed(locale as Locale, "rss");

  return new Response(content, {
    headers: {
      "Content-Type": "application/rss+xml",
      "Content-Disposition": 'attachment; filename="feed.xml"',
    },
  });
}
