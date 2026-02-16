import { createJiti } from "jiti";

const jiti = createJiti(import.meta.url, {
  alias: {
    "@": new URL("./", import.meta.url),
  },
});
const { env } = await jiti.import("./env.ts");
const { externalUrls } = await jiti.import("./lib/urls.ts");
const { locales, defaultLocale } = await jiti.import("./i18n.ts");

const satoshiDestination = `${
  env.VERCEL_ENV === "development" ? "http://" : "https://"
}${
  env.MAP_DOMAIN || env.VERCEL_ENV === "production"
    ? `satoshi.${env.VERCEL_PROJECT_PRODUCTION_URL}`
    : `${env.VERCEL_URL}/satoshi`
}`;

const cdnBaseUrl = new URL(env.CDN_BASE_URL);

/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    dangerouslyAllowLocalIP: env.VERCEL_ENV === "development",
    remotePatterns: [
      {
        protocol: cdnBaseUrl.protocol.replace(/:$/, ""),
        hostname: cdnBaseUrl.hostname,
        port: cdnBaseUrl.port,
        pathname:
          cdnBaseUrl.pathname === "/" ? "/**" : `${cdnBaseUrl.pathname}/**`,
      },
    ],
  },
  trailingSlash: true,
  async redirects() {
    const redirects = [
      {
        source: "/bitcoin.pdf",
        destination: `${cdnBaseUrl}/docs/bitcoin.pdf`,
        permanent: true,
      },
      {
        source: "/donate/",
        destination: externalUrls.zaprite,
        permanent: false,
      },
    ];
    if (
      env.VERCEL_ENV === "production" ||
      (env.VERCEL_ENV === "development" && env.MAP_DOMAIN)
    ) {
      redirects.push(
        // No locale prefix - preserve path as-is
        {
          source: "/satoshi/:path*",
          destination: `${satoshiDestination}/:path*`,
          permanent: true,
        },
        // Default locale (en) - strip it from destination
        {
          source: "/en/satoshi/:path*",
          destination: `${satoshiDestination}/:path*`,
          permanent: true,
        },
        // Non-default locales - preserve locale in destination
        {
          source: `/:locale(${locales.filter((l) => l !== defaultLocale).join("|")})/satoshi/:path*`,
          destination: `${satoshiDestination}/:locale/:path*`,
          permanent: true,
        },
      );
    }
    return redirects;
  },
};

export default nextConfig;
