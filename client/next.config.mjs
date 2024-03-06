import createJiti from "jiti";
import { fileURLToPath } from "node:url";

const jiti = createJiti(fileURLToPath(import.meta.url));
const { env } = jiti("./env");

const satoshiDestination =
  env.VERCEL_ENV === "development"
    ? `http://satoshi.localhost:${env.PORT}`
    : `https://${env.SATOSHI_HOST}`;

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
  async redirects() {
    const redirects = [
      {
        source: "/bitcoin.pdf",
        destination: `${cdnBaseUrl}/docs/bitcoin.pdf`,
        permanent: true,
      },
    ];
    if (env.VERCEL_ENV !== "preview") {
      redirects.push({
        source: "/satoshi/:path*",
        destination: satoshiDestination,
        permanent: false,
      });
    }
    return redirects;
  },
};

export default nextConfig;
