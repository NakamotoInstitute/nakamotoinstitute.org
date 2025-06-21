import { Metadata } from "next";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getPodcast, getPodcasts } from "@/lib/api/podcasts";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { externalUrls, urls } from "@/lib/urls";

import { EpisodeListing } from "../components/EpisodeListing";
import { LinkList } from "../components/LinkList";

export const dynamicParams = false;

export async function generateMetadata(
  props: LocaleParams<{ podcastSlug: string }>,
): Promise<Metadata> {
  const params = await props.params;

  const { locale, podcastSlug } = params;

  const podcast = await getPodcast(podcastSlug);
  const generateHref = (l: Locale) => urls(l).podcasts.show(podcastSlug);
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    title: podcast.name,
    alternates: {
      canonical: urls(locale).podcasts.show(podcastSlug),
      languages,
    },
  };
}

export default async function PodcastIndex(
  props: LocaleParams<{ podcastSlug: string }>,
) {
  const params = await props.params;

  const { locale, podcastSlug } = params;

  const { t } = await i18nTranslation(locale);
  const podcast = await getPodcast(podcastSlug);
  const generateHref = (l: Locale) => urls(l).podcasts.show(podcastSlug);

  return (
    <PageLayout
      t={t}
      locale={locale}
      generateHref={generateHref}
      breadcrumbs={[
        { label: t("podcasts"), href: urls(locale).podcasts.index },
        { label: podcast.name, href: urls(locale).podcasts.show(podcastSlug) },
      ]}
    >
      <PageHeader title={podcast.name} />
      {podcast.defunct ? (
        <p className="border-taupe-light border-t border-dashed py-4">
          {t("podcast_defunct")}
        </p>
      ) : null}
      <section>
        <div className="border-taupe-light border-t border-dashed py-4">
          <LinkList
            title={t("listen")}
            links={[
              podcast.spotifyUrl
                ? {
                    href: podcast.spotifyUrl,
                    label: t("spotify"),
                  }
                : false,
              podcast.applePodcastsUrl
                ? {
                    href: podcast.applePodcastsUrl,
                    label: t("apple_podcasts"),
                  }
                : false,
              podcast.fountainUrl
                ? {
                    href: podcast.fountainUrl,
                    label: t("fountain"),
                  }
                : false,
              {
                href:
                  podcast.externalFeed ??
                  urls(locale).podcasts.rss(podcastSlug),
                label: t("rss_feed"),
              },
            ]}
          />

          {(podcast.onYoutube || podcast.onRumble) && (
            <LinkList
              className="max-md:mt-4"
              title={t("watch")}
              links={[
                podcast.onYoutube && {
                  href: externalUrls.youtube.channel,
                  label: t("youtube"),
                },
                podcast.onRumble && {
                  href: externalUrls.rumble.channel,
                  label: t("rumble"),
                },
              ]}
            />
          )}
        </div>
      </section>
      <section>
        {podcast.episodes.map((e) => (
          <EpisodeListing
            key={e.slug}
            locale={locale}
            episode={e}
            podcastSlug={podcastSlug}
          />
        ))}
      </section>
    </PageLayout>
  );
}

export async function generateStaticParams() {
  const podcasts = await getPodcasts();
  return getLocaleParams((locale) =>
    podcasts.map((p) => ({
      locale,
      podcastSlug: p.slug,
    })),
  );
}
