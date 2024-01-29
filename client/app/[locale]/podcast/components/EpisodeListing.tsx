import Link from "next/link";

import { Episode } from "@/lib/api/schemas/podcast";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";

type EpisodeListingProps = {
  locale: Locale;
  episode: Episode;
};

export function EpisodeListing({ locale, episode }: EpisodeListingProps) {
  return (
    <article className="border-b border-solid py-4 first:pt-0 last:border-b-0">
      <header>
        <h2 className="text-2xl">
          <Link href={urls(locale).podcast.episode(episode.slug)}>
            {episode.title}
          </Link>
        </h2>
        <p>
          <time dateTime={episode.date.toISOString()}>
            {formatDate(locale, episode.date)}
          </time>
        </p>
      </header>
      <section>{episode.summary}</section>
    </article>
  );
}
