import { ToggleLinkProps } from "@/app/components/LanguageToggle";
import { locales } from "@/i18n";
import languages from "@/locales/languages.json";
import { domainToPathMapping } from "@/middleware";

const APP_BASE_URL = (() => {
  switch (process.env.VERCEL_ENV) {
    case "development":
      return "http://localhost:3000";
    case "production":
      return process.env.APP_BASE_URL as string;
    default:
      return `https://${process.env.VERCEL_URL as string}`;
  }
})();

const satoshiBase = "/satoshi";

const toFullUrl = (relativeUrl: string) => {
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
      locale === "en" && process.env.VERCEL_ENV !== "preview"
        ? `${satoshiBase}${path}`
        : `${satoshiBase}/${locale}${path}`;
    return toFullUrl(fullPath);
  };

  return {
    home: getUrl("/"),
    about: getUrl("/about"),
    authors: {
      index: getUrl("/authors"),
      detail: (slug: string) => getUrl(`/authors/${slug}`),
    },
    contact: getUrl("/contact"),
    crashCourse: getUrl("/crash-course"),
    donate: getUrl("/donate"),
    events: getUrl("/events"),
    finney: {
      index: getUrl("/finney"),
      rpow: getUrl("/finney/rpow"),
    },
    mempool: {
      index: getUrl("/mempool"),
      post: (slug: string) => getUrl(`/mempool/${slug}`),
      seriesIndex: getUrl("/mempool/series"),
      seriesDetail: (slug: string) => getUrl(`/mempool/series/${slug}`),
    },
    satoshi: {
      index: getSatoshiUrl("/"),
    },
    github: "https://github.com/NakamotoInstitute/nakamotoinstitute.org",
  };
};

export const generateLocaleToggleLinks = (
  locale: string,
  generateHref: (locale: Locale) => string,
): ToggleLinkProps => {
  return locales.reduce<ToggleLinkProps>(
    (acc, loc) => {
      const lang = languages.find((lang) => lang.code === loc);

      if (!lang) {
        return acc;
      }

      if (loc === locale) {
        acc.current = lang.name;
        return acc;
      }

      acc.links?.push({
        name: lang.name,
        href: generateHref(loc),
      });

      return acc;
    },
    { current: "", links: [] },
  );
};
