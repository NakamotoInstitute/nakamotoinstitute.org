import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        disallow: ["/*feed.xml", "/*atom.xml"],
      },
    ],
    sitemap: [
      "https://nakamotoinstitute.org/sitemap.xml",
      "https://satoshi.nakamotoinstitute.org/sitemap.xml",
    ],
  };
}
