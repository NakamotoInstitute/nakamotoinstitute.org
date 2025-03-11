import { createJiti } from "jiti";
import { fileURLToPath } from "node:url";

const jiti = createJiti(fileURLToPath(import.meta.url), {
  alias: {
    "@": fileURLToPath(new URL("./", import.meta.url)),
  },
});
const { env } = await jiti.import("./env.ts");
const { externalUrls } = await jiti.import("./lib/urls.ts");

const satoshiDestination = `${
  env.VERCEL_ENV === "development" ? "http://" : "https://"
}${
  env.MAP_DOMAIN || env.VERCEL_ENV === "production"
    ? `satoshi.${env.VERCEL_URL}`
    : `${env.VERCEL_URL}/satoshi`
}`;

const cdnBaseUrl = new URL(env.CDN_BASE_URL);

/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
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
      redirects.push({
        source: "/satoshi/:path*",
        destination: `${satoshiDestination}/:path*`,
        permanent: false,
      });
    }
    return redirects;
  },
};

export default nextConfig;
