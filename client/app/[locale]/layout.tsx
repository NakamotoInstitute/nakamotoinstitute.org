import { Metadata } from "next";

import { openGraphImages } from "@/app/shared-metadata";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { xHandle } from "@/lib/urls-client";
import { APP_BASE_URL } from "@/lib/urls";

import { RootLayout } from "../components/RootLayout";

export async function generateMetadata(props: LocaleParams): Promise<Metadata> {
  const { locale } = await props.params;

  const { t } = await i18nTranslation(locale as Locale);
  const siteTitle = t("sni_full");
  return {
    metadataBase: new URL(APP_BASE_URL),
    title: {
      template: `%s | ${siteTitle}`,
      default: siteTitle,
    },
    description: t("sni_mission_statement"),
    openGraph: {
      type: "website",
      siteName: siteTitle,
      images: openGraphImages,
    },
    twitter: { site: `@${xHandle}`, images: openGraphImages },
  };
}

export default async function MainLayout(props: LayoutProps<"/[locale]">) {
  const { locale } = await props.params;

  return <RootLayout locale={locale as Locale}>{props.children}</RootLayout>;
}
