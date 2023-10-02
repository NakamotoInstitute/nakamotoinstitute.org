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
    satoshi: {
      index: getSatoshiUrl("/"),
    },
    github: "https://github.com/NakamotoInstitute/nakamotoinstitute.org",
  };
};
