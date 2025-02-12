import { ToggleLinkProps } from "@/app/components/LanguageToggle";
import { env } from "@/env";
import { defaultLocale, languages, locales } from "@/i18n";

import { EmailSource } from "./api/schemas/emails";
import { ForumPostSource } from "./api/schemas/posts";

const prodDomainToPathMapping = [
  {
    domain: `satoshi.${env.VERCEL_PROJECT_PRODUCTION_URL}`,
    path: "/satoshi",
  },
];

const localDomainToPathMapping = [
  {
    domain: "satoshi.localhost",
    path: "/satoshi",
  },
];

export const domainToPathMapping =
  env.VERCEL_ENV === "development"
    ? env.MAP_DOMAIN
      ? localDomainToPathMapping
      : []
    : env.VERCEL_ENV === "production"
      ? prodDomainToPathMapping
      : [];

const APP_BASE_URL =
  env.VERCEL_ENV === "development"
    ? "http://localhost:3000"
    : env.VERCEL_ENV === "production"
      ? `https://${env.VERCEL_PROJECT_PRODUCTION_URL}`
      : `https://${env.VERCEL_URL}`;

export const toFullUrl = (relativeUrl: string) => {
  let baseUrl = APP_BASE_URL;
  // if the relativeURL matches a path mapped to a specific domain,
  // use that domain to build the full URL
  for (const { path, domain } of domainToPathMapping) {
    const regex = new RegExp(`^${path}(?=$|/|\\?)`);
    if (regex.test(relativeUrl)) {
      baseUrl = APP_BASE_URL.replace(/(:\/\/).*?(?=:|\/|$)/, `://${domain}`);
      relativeUrl = relativeUrl.replace(regex, "");
      break;
    }
  }
  return new URL(relativeUrl, baseUrl).href;
};

export const urls = (locale: Locale) => {
  const getUrl = (path: string) => {
    const fullPath = locale === "en" ? path : `/${locale}${path}`;
    return toFullUrl(fullPath);
  };

  const getSatoshiUrl = (path: string) => {
    const fullPath =
      locale === "en" ? `/satoshi${path}` : `/satoshi/${locale}${path}`;
    return toFullUrl(fullPath);
  };

  return {
    home: getUrl("/"),
    about: getUrl("/about/"),
    authors: {
      index: getUrl("/authors/"),
      detail: (slug: string) => getUrl(`/authors/${slug}/`),
    },
    contact: getUrl("/contact/"),
    crashCourse: getUrl("/crash-course/"),
    donate: {
      index: getUrl("/donate/"),
      zaprite: "https://pay.zaprite.com/pl_vNYDp4YBSd",
    },
    events: getUrl("/events/"),
    finney: {
      index: getUrl("/finney/"),
      rpow: getUrl("/finney/rpow/"),
    },
    getInvolved: getUrl("/get-involved/"),
    library: {
      index: getUrl("/library/"),
      doc: (slug: string) => getUrl(`/library/${slug}/`),
      docNode: (docSlug: string, nodeSlug: string) =>
        getUrl(`/library/${docSlug}/${nodeSlug}/`),
    },
    mempool: {
      index: getUrl("/mempool/"),
      post: (slug: string) => getUrl(`/mempool/${slug}/`),
      seriesIndex: getUrl("/mempool/series/"),
      seriesDetail: (slug: string) => getUrl(`/mempool/series/${slug}/`),
      rss: getUrl("/mempool/feed.xml"),
      atom: getUrl("/mempool/atom.xml"),
    },
    podcasts: {
      index: getUrl("/podcasts/"),
      show: (slug: string) => getUrl(`/podcasts/${slug}/`),
      episode: (slug: string, episodeSlug: string) =>
        getUrl(`/podcasts/${slug}/${episodeSlug}/`),
      episodeMp3: (slug: string, episodeSlug: string) =>
        cdnUrl(`/cryptomises/${slug}/${episodeSlug}.mp3`),
      rss: (slug: string) => getUrl(`/podcasts/${slug}/feed.xml`),
    },
    satoshi: {
      index: getSatoshiUrl("/"),
      code: getSatoshiUrl("/code/"),
      emails: {
        index: getSatoshiUrl("/emails/"),
        threadsIndex: getSatoshiUrl("/emails/threads/"),
        sourceIndex: (source: EmailSource) =>
          getSatoshiUrl(`/emails/${source}/`),
        sourceEmail: (source: EmailSource, id: string) =>
          getSatoshiUrl(`/emails/${source}/${id}/`),
        sourceThreadsIndex: (source: EmailSource) =>
          getSatoshiUrl(`/emails/${source}/threads/`),
        sourceThreadsDetail: (source: EmailSource, id: string) =>
          getSatoshiUrl(`/emails/${source}/threads/${id}/`),
      },
      posts: {
        index: getSatoshiUrl("/posts/"),
        threadsIndex: getSatoshiUrl("/posts/threads/"),
        sourceIndex: (source: ForumPostSource) =>
          getSatoshiUrl(`/posts/${source}/`),
        sourcePost: (source: ForumPostSource, id: string) =>
          getSatoshiUrl(`/posts/${source}/${id}/`),
        sourceThreadsIndex: (source: ForumPostSource) =>
          getSatoshiUrl(`/posts/${source}/threads/`),
        sourceThreadsDetail: (source: ForumPostSource, id: string) =>
          getSatoshiUrl(`/posts/${source}/threads/${id}/`),
      },
      quotesIndex: getSatoshiUrl("/quotes/"),
      quoteCategory: (slug: string) => getSatoshiUrl(`/quotes/${slug}/`),
    },
    skeptics: getUrl("/the-skeptics/"),
  };
};

export const externalUrls = {
  github: "https://github.com/NakamotoInstitute/nakamotoinstitute.org",
  nostr: "https://primal.net/sni",
  rumble: {
    channel: "https://rumble.com/c/c-7381366",
    link: (id: string) => `https://rumble.com/${id}.html`,
  },
  substack: "https://news.nakamotoinstitute.org",
  x: "https://x.com/NakamotoInst",
  youtube: {
    channel: "https://www.youtube.com/@SatoshiNakamotoInstitute",
    embed: (id: string) => `https://www.youtube.com/embed/${id}?rel=0`,
  },
};

export const cdnUrl = (path: string) => env.CDN_BASE_URL + path;

export const generateLocaleToggleLinks = (
  locale: string,
  generateHref: (locale: Locale) => string,
): ToggleLinkProps => {
  return locales.reduce<ToggleLinkProps>(
    (acc, loc) => {
      const name = languages[loc];

      if (loc === locale) {
        acc.current = locale;
        return acc;
      }

      acc.links?.push({
        text: name,
        href: generateHref(loc),
      });

      return acc;
    },
    { current: defaultLocale, links: [] },
  );
};
