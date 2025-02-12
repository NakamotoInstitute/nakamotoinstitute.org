import { Metadata } from "next";
import Link from "next/link";

import { ButtonLink } from "@/app/components/Button";
import { PageLayout } from "@/app/components/PageLayout";
import { Rehype } from "@/app/components/Rehype";
import { locales } from "@/i18n";
import { getEpisode, getEpisodes } from "@/lib/api/podcasts";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { externalUrls, urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";

export const dynamicParams = false;

const makeGenerateHref =
  (podcastSlug: string, episodeSlug: string) => (l: Locale) =>
    urls(l).podcasts.episode(podcastSlug, episodeSlug);

export async function generateMetadata(
  props: LocaleParams<{ podcastSlug: string; episodeSlug: string }>,
): Promise<Metadata> {
  const params = await props.params;

  const { locale, podcastSlug, episodeSlug } = params;

  const episode = await getEpisode(podcastSlug, episodeSlug);
  const generateHref = makeGenerateHref(podcastSlug, episodeSlug);
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    title: episode.title,
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function EpisodeDetail(
  props: LocaleParams<{ podcastSlug: string; episodeSlug: string }>,
) {
  const params = await props.params;

  const { locale, podcastSlug, episodeSlug } = params;

  const { t } = await i18nTranslation(locale);
  const episode = await getEpisode(podcastSlug, episodeSlug);
  const generateHref = makeGenerateHref(podcastSlug, episodeSlug);

  return (
    <PageLayout
      t={t}
      locale={locale}
      generateHref={generateHref}
      breadcrumbs={[
        { label: t("podcasts"), href: urls(locale).podcasts.index },
        {
          label: episode.podcast.name,
          href: urls(locale).podcasts.show(episode.podcast.slug),
        },
        {
          label: episode.title,
          href: urls(locale).podcasts.episode(
            episode.podcast.slug,
            episode.slug,
          ),
        },
      ]}
    >
      <header className="mx-auto text-center">
        <h2 className="mb-4 text-2xl leading-[1.1] small-caps md:mb-6 md:text-4xl">
          {t("episode_number", { number: episode.episodeNumber })}
        </h2>
        <h1 className="mb-4 text-4xl font-medium leading-[1.1] md:mb-6 md:text-7xl">
          {episode.title}
        </h1>
        <p className="text-xl font-bold opacity-60 small-caps md:text-2xl">
          <time dateTime={episode.date.toISOString()}>
            {formatDate(locale, episode.date)}
          </time>
        </p>
      </header>
      <hr className="mx-auto mb-4 mt-7 w-12 md:mt-18" />
      <ul className="mx-auto flex justify-center gap-4">
        {episode.podcast.applePodcastsUrl && (
          <li>
            <Link className="underline" href={episode.podcast.applePodcastsUrl}>
              {t("apple_podcasts")}
            </Link>
          </li>
        )}
        {episode.podcast.spotifyUrl && (
          <li>
            <Link className="underline" href={episode.podcast.spotifyUrl}>
              Spotify
            </Link>
          </li>
        )}
        <li>
          <Link
            className="underline"
            href={
              episode.podcast.externalFeed ??
              urls(locale).podcasts.rss(episode.podcast.slug)
            }
          >
            {t("rss")}
          </Link>
        </li>
        <li>
          <Link
            className="underline"
            href={
              episode.mp3Url ??
              urls(locale).podcasts.episodeMp3(
                episode.podcast.slug,
                episode.slug,
              )
            }
          >
            {t("download_mp3")}
          </Link>
        </li>
      </ul>
      <hr className="mx-auto mb-7 mt-4 w-12 md:mb-18" />
      <section className="prose mx-auto">
        <Rehype>{episode.content}</Rehype>
        {episode.youtubeId && (
          <iframe
            className="aspect-video w-full"
            src={externalUrls.youtube.embed(episode.youtubeId)}
            allowFullScreen
          ></iframe>
        )}
        {episode.rumbleId && (
          <p className="text-center">
            <ButtonLink
              className="no-underline"
              href={externalUrls.rumble.link(episode.rumbleId)}
            >
              Watch on Rumble
            </ButtonLink>
          </p>
        )}
      </section>
    </PageLayout>
  );
}

export async function generateStaticParams() {
  const episodes = await getEpisodes();
  return getLocaleParams((locale) =>
    episodes.map((e) => ({
      locale,
      podcastSlug: e.podcastSlug,
      episodeSlug: e.episodeSlug,
    })),
  );
}
