import { getPodcastFeed } from "@/lib/api/podcast";

export const dynamic = "force-static";

export async function GET() {
  const content = await getPodcastFeed();

  return new Response(content, {
    headers: {
      "Content-Type": "application/rss+xml",
      "Content-Disposition": 'attachment; filename="feed.xml"',
    },
  });
}
