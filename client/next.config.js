const satoshiDestination =
  process.env.VERCEL_ENV === "development"
    ? `http://satoshi.localhost:${process.env.PORT ?? 3000}`
    : `https://${process.env.SATOSHI_HOST}`;

const cdnBaseUrl = new URL(process.env.CDN_BASE_URL);

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
    if (process.env.VERCEL_ENV !== "preview") {
      redirects.push({
        source: "/satoshi/:path*",
        destination: satoshiDestination,
        permanent: false,
      });
    }
    return redirects;
  },
};

module.exports = nextConfig;
