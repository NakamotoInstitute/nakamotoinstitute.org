import clsx from "clsx";
import { TFunction } from "i18next";
import Link from "next/link";

import { Chip } from "@/app/components/Chip";
import { BasePodcast } from "@/lib/api/schemas/podcasts";
import { urls } from "@/lib/urls";

type PodcastListingProps = {
  podcast: BasePodcast;
  className?: string;
  locale: Locale;
  t: TFunction<string, string>;
};

export async function PodcastListing({
  podcast,
  className,
  locale,
  t,
}: PodcastListingProps) {
  return (
    <article
      className={clsx(
        "border-t border-dashed border-taupe-light py-4 last:border-b",
        className,
      )}
    >
      <div className="flex items-center gap-2">
        <h2 className="font-bold md:text-xl">
          <Link
            className="text-cardinal hover:underline"
            href={urls(locale).podcasts.show(podcast.slug)}
          >
            {podcast.name}
          </Link>
        </h2>
        {podcast.defunct && <Chip>{t("defunct")}</Chip>}
      </div>
      <p>{podcast.description}</p>
    </article>
  );
}
