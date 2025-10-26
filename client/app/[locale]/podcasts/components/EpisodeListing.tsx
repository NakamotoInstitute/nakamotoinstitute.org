import Link from "next/link";

import { EpisodeBase } from "@/lib/api/schemas/podcasts";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";

type EpisodeListingProps = {
  locale: Locale;
  episode: EpisodeBase;
  podcastSlug: string;
};

export function EpisodeListing({
  locale,
  episode,
  podcastSlug,
}: EpisodeListingProps) {
  return (
    <article className="border-taupe-light border-t border-dashed py-4 last:border-b">
      <header>
        <h2 className="font-bold md:text-xl">
          <Link
            className="text-cardinal hover:underline"
            href={urls(locale).podcasts.episode(podcastSlug, episode.slug)}
          >
            {episode.title}
          </Link>
        </h2>
        <p className="small-caps">
          <time dateTime={episode.date.toISOString()}>
            {formatDate(locale, episode.date)}
          </time>
        </p>
      </header>
      <section className="my-2 italic">{episode.summary}</section>
    </article>
  );
}
