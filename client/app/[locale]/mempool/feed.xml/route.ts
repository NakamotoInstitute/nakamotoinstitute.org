import { getMempoolFeed } from "@/lib/api/mempool";

export async function GET(
  _request: Request,
  { params: { locale } }: LocaleParams,
) {
  const content = await getMempoolFeed(locale, "rss");

  return new Response(content, {
    headers: {
      "Content-Type": "application/rss+xml",
      "Content-Disposition": 'attachment; filename="feed.xml"',
    },
  });
}
