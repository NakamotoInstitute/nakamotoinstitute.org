const satoshiDestination =
  process.env.VERCEL_ENV === "development"
    ? `http://satoshi.localhost:${process.env.PORT ?? 3000}`
    : `https://${process.env.SATOSHI_HOST}`;

/** @type {import('next').NextConfig} */
const nextConfig = {
  async redirects() {
    return process.env.VERCEL_ENV !== "preview"
      ? [
          {
            source: "/satoshi/:path*",
            destination: satoshiDestination,
            permanent: false,
          },
        ]
      : [];
  },
};

module.exports = nextConfig;
