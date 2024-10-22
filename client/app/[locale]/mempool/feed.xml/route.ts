import { getMempoolFeed } from "@/lib/api/mempool";

export const dynamic = "force-static";

export async function GET(_request: Request, props: LocaleParams) {
  const params = await props.params;

  const { locale } = params;

  const content = await getMempoolFeed(locale, "rss");

  return new Response(content, {
    headers: {
      "Content-Type": "application/rss+xml",
      "Content-Disposition": 'attachment; filename="feed.xml"',
    },
  });
}
