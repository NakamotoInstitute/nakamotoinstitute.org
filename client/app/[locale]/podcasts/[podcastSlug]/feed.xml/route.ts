import { getPodcastFeed, getPodcasts } from "@/lib/api/podcasts";
import { getLocaleParams } from "@/lib/i18n/utils";

export const dynamic = "force-static";
export const dynamicParams = false;

export async function GET(
  _: Request,
  { params }: { params: Promise<{ podcastSlug: string }> },
) {
  const { podcastSlug } = await params;
  const content = await getPodcastFeed(podcastSlug);

  return new Response(content, {
    headers: {
      "Content-Type": "application/rss+xml",
      "Content-Disposition": 'attachment; filename="feed.xml"',
    },
  });
}

export async function generateStaticParams() {
  const podcasts = await getPodcasts();
  return getLocaleParams((locale) =>
    podcasts
      .filter((p) => !p.externalFeed)
      .map((p) => ({ locale, podcastSlug: p.slug })),
  );
}
