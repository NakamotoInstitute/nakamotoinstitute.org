import type { MetadataRoute } from "next";

import { locales } from "@/i18n";
import { getEmailThreads, getSatoshiEmails } from "@/lib/api/emails";
import { getForumThreads, getSatoshiPosts } from "@/lib/api/posts";
import { getQuoteCategories } from "@/lib/api/quotes";
import { EMAIL_SOURCES } from "@/lib/api/schemas/emails";
import { FORUM_POST_SOURCES } from "@/lib/api/schemas/posts";
import { urls } from "@/lib/urls";
import { LocalizedUrlObject, createLocalizedUrlObject } from "@/utils/sitemap";
import { formatLocale } from "@/utils/strings";

async function getEmailIndexUrls(): Promise<MetadataRoute.Sitemap> {
  const sourceIndexUrls = EMAIL_SOURCES.map((source) => ({
    url: urls("en").satoshi.emails.sourceIndex(source),
    alternates: {
      languages: createLocalizedUrlObject((locale: Locale) =>
        urls(locale).satoshi.emails.sourceIndex(source),
      ),
    },
  }));
  const sourceThreadIndexUrls = EMAIL_SOURCES.map((source) => ({
    url: urls("en").satoshi.emails.sourceThreadsIndex(source),
    alternates: {
      languages: createLocalizedUrlObject((locale: Locale) =>
        urls(locale).satoshi.emails.sourceThreadsIndex(source),
      ),
    },
  }));
  return [...sourceIndexUrls, ...sourceThreadIndexUrls];
}

async function getEmailUrls(): Promise<MetadataRoute.Sitemap> {
  const emails = await getSatoshiEmails();
  return emails.map(({ source, satoshiId }) => ({
    url: urls("en").satoshi.emails.sourceEmail(source, satoshiId.toString()),
    alternates: {
      languages: createLocalizedUrlObject((locale: Locale) =>
        urls(locale).satoshi.emails.sourceEmail(source, satoshiId.toString()),
      ),
    },
  }));
}

async function getEmailThreadUrls(): Promise<MetadataRoute.Sitemap> {
  const threads = await getEmailThreads();
  return threads.map(({ source, id }) => ({
    url: urls("en").satoshi.emails.sourceThreadsDetail(source, id.toString()),
    alternates: {
      languages: createLocalizedUrlObject((locale: Locale) =>
        urls(locale).satoshi.emails.sourceThreadsDetail(source, id.toString()),
      ),
    },
  }));
}

async function getPostIndexUrls(): Promise<MetadataRoute.Sitemap> {
  const sourceIndexUrls = FORUM_POST_SOURCES.map((source) => ({
    url: urls("en").satoshi.posts.sourceIndex(source),
    alternates: {
      languages: createLocalizedUrlObject((locale: Locale) =>
        urls(locale).satoshi.posts.sourceIndex(source),
      ),
    },
  }));
  const sourceThreadIndexUrls = FORUM_POST_SOURCES.map((source) => ({
    url: urls("en").satoshi.posts.sourceThreadsIndex(source),
    alternates: {
      languages: createLocalizedUrlObject((locale: Locale) =>
        urls(locale).satoshi.posts.sourceThreadsIndex(source),
      ),
    },
  }));
  return [...sourceIndexUrls, ...sourceThreadIndexUrls];
}

async function getPostUrls(): Promise<MetadataRoute.Sitemap> {
  const posts = await getSatoshiPosts();
  return posts.map(({ source, satoshiId }) => ({
    url: urls("en").satoshi.posts.sourcePost(source, satoshiId.toString()),
    alternates: {
      languages: createLocalizedUrlObject((locale: Locale) =>
        urls(locale).satoshi.posts.sourcePost(source, satoshiId.toString()),
      ),
    },
  }));
}

async function getPostThreadUrls(): Promise<MetadataRoute.Sitemap> {
  const threads = await getForumThreads();
  return threads.map(({ source, id }) => ({
    url: urls("en").satoshi.posts.sourceThreadsDetail(source, id.toString()),
    alternates: {
      languages: createLocalizedUrlObject((locale: Locale) =>
        urls(locale).satoshi.posts.sourceThreadsDetail(source, id.toString()),
      ),
    },
  }));
}

async function getQuoteCategoryUrls(): Promise<MetadataRoute.Sitemap> {
  const categories = await getQuoteCategories();
  return categories.map(({ slug }) => ({
    url: urls("en").satoshi.quoteCategory(slug),
    alternates: {
      languages: locales.reduce((obj, locale) => {
        obj[formatLocale(locale)] = urls(locale).satoshi.quoteCategory(slug);
        return obj;
      }, {} as LocalizedUrlObject),
    },
  }));
}

async function getPageUrls(): Promise<MetadataRoute.Sitemap> {
  const pages = [
    (locale: Locale) => urls(locale).satoshi.index,
    (locale: Locale) => urls(locale).satoshi.code,
    (locale: Locale) => urls(locale).satoshi.emails.index,
    (locale: Locale) => urls(locale).satoshi.emails.threadsIndex,
    (locale: Locale) => urls(locale).satoshi.posts.index,
    (locale: Locale) => urls(locale).satoshi.posts.threadsIndex,
    (locale: Locale) => urls(locale).satoshi.quotesIndex,
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
    emailIndexUrls,
    emailUrls,
    emailThreadUrls,
    postIndexUrls,
    postUrls,
    postThreadUrls,
    quoteCategoryUrls,
  ] = await Promise.all([
    getPageUrls(),
    getEmailIndexUrls(),
    getEmailUrls(),
    getEmailThreadUrls(),
    getPostIndexUrls(),
    getPostUrls(),
    getPostThreadUrls(),
    getQuoteCategoryUrls(),
  ]);

  return [
    ...pageUrls,
    ...emailIndexUrls,
    ...emailUrls,
    ...emailThreadUrls,
    ...postIndexUrls,
    ...postUrls,
    ...postThreadUrls,
    ...quoteCategoryUrls,
  ];
}
