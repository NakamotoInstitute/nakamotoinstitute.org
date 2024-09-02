import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "Satoshi Nakamoto Institute",
    short_name: "SNI",
    description: "Advancing and preserving bitcoin knowledge",
    start_url: "/",
    display: "standalone",
    background_color: "#f5f4ef",
    theme_color: "#c21324",
    icons: [
      {
        src: "/favicon.ico",
        sizes: "any",
        type: "image/x-icon",
      },
      {
        src: "/icon.png",
        sizes: "192x192",
        type: "image/png",
      },
      {
        src: "/apple-icon.png",
        sizes: "180x180",
        type: "image/png",
      },
    ],
  };
}
