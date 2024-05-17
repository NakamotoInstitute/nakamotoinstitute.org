import type { MetadataRoute } from "next";

import { getAuthorParams } from "@/lib/api/authors";
import { getLibraryDocs } from "@/lib/api/library";
import { getMempoolPosts, getMempoolSeriesParams } from "@/lib/api/mempool";
import { getEpisodes } from "@/lib/api/podcast";
import { urls } from "@/lib/urls";
import { Locale } from "@/types/i18n";
import {
  LocalizedUrlObject,
  createLocalizedUrlObject,
  translatedLocales,
} from "@/utils/sitemap";
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
      languages: langs.reduce((obj, lang) => {
        obj[formatLocale(lang)] = urls(lang).authors.detail(slug);
        return obj;
      }, {} as LocalizedUrlObject),
    },
  }));
}

async function getLibraryUrls(): Promise<MetadataRoute.Sitemap> {
  const libraryDocs = await getLibraryDocs("en");
  return libraryDocs.map((doc) => ({
    url: urls("en").library.doc(doc.slug),
    alternates: {
      languages: doc.translations.reduce((obj, translation) => {
        obj[formatLocale(translation.locale)] = urls(
          translation.locale,
        ).library.doc(translation.slug);
        return obj;
      }, {} as LocalizedUrlObject),
    },
  }));
}

async function getMempoolUrls(): Promise<MetadataRoute.Sitemap> {
  const mempoolPosts = await getMempoolPosts("en");
  return mempoolPosts.map((doc) => ({
    url: urls("en").mempool.post(doc.slug),
    alternates: {
      languages: doc.translations.reduce((obj, translation) => {
        obj[formatLocale(translation.locale)] = urls(
          translation.locale,
        ).mempool.post(translation.slug);
        return obj;
      }, {} as LocalizedUrlObject),
    },
  }));
}

async function getMempoolSeriesUrls(): Promise<MetadataRoute.Sitemap> {
  const mempoolSeries = await getMempoolSeriesParams();
  return mempoolSeries.map((series) => ({
    url: urls("en").mempool.seriesDetail(series.slug),
  }));
}

async function getPodcastUrls(): Promise<MetadataRoute.Sitemap> {
  const episodes = await getEpisodes();
  return episodes.map((episode) => ({
    url: urls("en").podcast.episode(episode.slug),
    alternates: {
      languages: translatedLocales.reduce((obj, locale) => {
        obj[formatLocale(locale)] = urls(locale).podcast.episode(episode.slug);
        return obj;
      }, {} as LocalizedUrlObject),
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
    (locale: Locale) => urls(locale).podcast.index,
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
    podcastUrls,
  ] = await Promise.all([
    getPageUrls(),
    getAuthorUrls(),
    getLibraryUrls(),
    getMempoolUrls(),
    getMempoolSeriesUrls(),
    getPodcastUrls(),
  ]);

  return [
    ...pageUrls,
    ...authorUrls,
    ...libraryUrls,
    ...mempoolUrls,
    ...mempoolSeriesUrls,
    ...podcastUrls,
  ];
}
