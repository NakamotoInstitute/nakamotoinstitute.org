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
    <article className="border-t border-dashed border-taupe-light py-4 last:border-b">
      <header>
        <h2 className="font-bold md:text-xl">
          <Link
            className="text-cardinal hover:underline"
            href={urls(locale).podcast.episode(episode.slug)}
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
