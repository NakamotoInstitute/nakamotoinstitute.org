import { Metadata } from "next";

import { urls } from "@/lib/urls";

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  return {
    alternates: {
      types: {
        "application/rss+xml": [
          {
            title: "The Crypto-Mises Podcast",
            url: urls(locale).podcast.rss,
          },
        ],
      },
    },
  };
}

export default function MempoolLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
