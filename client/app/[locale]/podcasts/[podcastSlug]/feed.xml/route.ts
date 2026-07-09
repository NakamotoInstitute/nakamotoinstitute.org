import { notFound } from "next/navigation";

import { PodcastBase, api } from "@/lib/api";
import { getLocaleParams } from "@/lib/i18n/utils";

export const dynamic = "force-static";
export const dynamicParams = false;

export async function GET(
  _: Request,
  { params }: { params: Promise<{ podcastSlug: string }> },
) {
  const { podcastSlug } = await params;
  const result = await api.podcasts.generateFeed({
    path: { podcast_slug: podcastSlug },
  });
  const { data: content, error, response } = result;
  if (content === undefined) {
    if (response?.status === 404) notFound();
    throw error instanceof Error ? error : new Error("Failed to generate podcast feed");
  }

  return new Response(content, {
    headers: {
      "Content-Type": "application/rss+xml",
      "Content-Disposition": 'attachment; filename="feed.xml"',
    },
  });
}

export async function generateStaticParams() {
  const { data: podcasts } = await api.podcasts.getPodcasts();
  return getLocaleParams((locale) =>
    (podcasts ?? [])
      .filter((p: PodcastBase) => !p.externalFeed)
      .map((p: PodcastBase) => ({ locale, podcastSlug: p.slug })),
  );
}
