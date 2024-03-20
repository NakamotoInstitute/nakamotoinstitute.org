import { Metadata } from "next";

import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { urls } from "@/lib/urls";

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);

  return {
    alternates: {
      types: {
        "application/rss+xml": [
          {
            title: t("The Crypto-Mises Podcast"),
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
