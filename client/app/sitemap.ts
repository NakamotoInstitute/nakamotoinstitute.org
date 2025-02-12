import type { MetadataRoute } from "next";

import { locales } from "@/i18n";
import { getAuthorParams } from "@/lib/api/authors";
import { getLibraryDocs } from "@/lib/api/library";
import { getMempoolPosts, getMempoolSeriesParams } from "@/lib/api/mempool";
import { getEpisodes, getPodcasts } from "@/lib/api/podcasts";
import { urls } from "@/lib/urls";
import { LocalizedUrlObject, createLocalizedUrlObject } from "@/utils/sitemap";
import { formatLocale } from "@/utils/strings";

async function getAuthorUrls(): Promise<MetadataRoute.Sitemap> {
  const authors = await getAuthorParams();
  const cleanedAuthors = authors.reduce(
    (acc, author) => {
      if (!acc[author.slug]) {
        acc[author.slug] = [];
      }
      if (author.locale !== "en") {
        acc[author.slug].push(author.locale);
      }
      return acc;
    },
    {} as { [slug: string]: Locale[] },
  );

  return Object.entries(cleanedAuthors).map(([slug, langs]) => ({
    url: urls("en").authors.detail(slug),
    alternates: {
      languages: langs.reduce(
        (obj, lang) => {
          obj[formatLocale(lang)] = urls(lang).authors.detail(slug);
          return obj;
        },
        langs.length > 0
          ? ({ en: urls("en").authors.detail(slug) } as LocalizedUrlObject)
          : ({} as LocalizedUrlObject),
      ),
    },
  }));
}

async function getLibraryUrls(): Promise<MetadataRoute.Sitemap> {
  const libraryDocs = await getLibraryDocs("en");
  return libraryDocs.flatMap((doc) => {
    const urlMap: MetadataRoute.Sitemap = [
      {
        url: urls("en").library.doc(doc.slug),
        alternates: {
          languages: doc.translations.reduce(
            (obj, translation) => {
              obj[formatLocale(translation.locale)] = urls(
                translation.locale,
              ).library.doc(translation.slug);
              return obj;
            },
            doc.translations.length > 0
              ? ({ en: urls("en").library.doc(doc.slug) } as LocalizedUrlObject)
              : ({} as LocalizedUrlObject),
          ),
        },
      },
    ];

    doc.nodes?.forEach((node) => {
      urlMap.push({
        url: urls("en").library.docNode(doc.slug, node.slug),
      });
    });

    return urlMap;
  });
}

async function getMempoolUrls(): Promise<MetadataRoute.Sitemap> {
  const mempoolPosts = await getMempoolPosts("en");
  return mempoolPosts.map((post) => ({
    url: urls("en").mempool.post(post.slug),
    alternates: {
      languages: post.translations.reduce(
        (obj, translation) => {
          obj[formatLocale(translation.locale)] = urls(
            translation.locale,
          ).mempool.post(translation.slug);
          return obj;
        },
        post.translations.length > 0
          ? ({ en: urls("en").mempool.post(post.slug) } as LocalizedUrlObject)
          : ({} as LocalizedUrlObject),
      ),
    },
  }));
}

async function getMempoolSeriesUrls(): Promise<MetadataRoute.Sitemap> {
  const mempoolSeries = await getMempoolSeriesParams();
  return mempoolSeries.map((series) => ({
    url: urls("en").mempool.seriesDetail(series.slug),
  }));
}

async function getPodcastsUrls(): Promise<MetadataRoute.Sitemap> {
  const podcasts = await getPodcasts();
  return podcasts.map((podcast) => ({
    url: urls("en").podcasts.show(podcast.slug),
    alternates: {
      languages: locales.reduce(
        (obj, locale) => {
          obj[formatLocale(locale)] = urls(locale).podcasts.show(podcast.slug);
          return obj;
        },
        { en: urls("en").podcasts.show(podcast.slug) } as LocalizedUrlObject,
      ),
    },
  }));
}

async function getPodcastEpisodesUrls(): Promise<MetadataRoute.Sitemap> {
  const episodes = await getEpisodes();
  return episodes.map((episode) => ({
    url: urls("en").podcasts.episode(episode.podcastSlug, episode.episodeSlug),
    alternates: {
      languages: locales.reduce(
        (obj, locale) => {
          obj[formatLocale(locale)] = urls(locale).podcasts.episode(
            episode.podcastSlug,
            episode.episodeSlug,
          );
          return obj;
        },
        {
          en: urls("en").podcasts.episode(
            episode.podcastSlug,
            episode.episodeSlug,
          ),
        } as LocalizedUrlObject,
      ),
    },
  }));
}

async function getPageUrls(): Promise<MetadataRoute.Sitemap> {
  const pages = [
    (locale: Locale) => urls(locale).home,
    (locale: Locale) => urls(locale).about,
    (locale: Locale) => urls(locale).contact,
    (locale: Locale) => urls(locale).crashCourse,
    (locale: Locale) => urls(locale).donate.index,
    (locale: Locale) => urls(locale).events,
    (locale: Locale) => urls(locale).finney.index,
    (locale: Locale) => urls(locale).finney.rpow,
    (locale: Locale) => urls(locale).getInvolved,
    (locale: Locale) => urls(locale).library.index,
    (locale: Locale) => urls(locale).mempool.index,
    (locale: Locale) => urls(locale).mempool.seriesIndex,
    (locale: Locale) => urls(locale).podcasts.index,
    (locale: Locale) => urls(locale).skeptics,
  ];

  return pages.map((pathFunc) => ({
    url: pathFunc("en"),
    alternates: {
      languages: createLocalizedUrlObject(pathFunc),
    },
  }));
}

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const [
    pageUrls,
    authorUrls,
    libraryUrls,
    mempoolUrls,
    mempoolSeriesUrls,
    podcastsUrls,
    podcastEpisodesUrls,
  ] = await Promise.all([
    getPageUrls(),
    getAuthorUrls(),
    getLibraryUrls(),
    getMempoolUrls(),
    getMempoolSeriesUrls(),
    getPodcastsUrls(),
    getPodcastEpisodesUrls(),
  ]);

  return [
    ...pageUrls,
    ...authorUrls,
    ...libraryUrls,
    ...mempoolUrls,
    ...mempoolSeriesUrls,
    ...podcastsUrls,
    ...podcastEpisodesUrls,
  ];
}
