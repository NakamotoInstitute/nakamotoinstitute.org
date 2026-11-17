import { Metadata } from "next";
import { notFound } from "next/navigation";

import { openGraphImages } from "@/app/shared-metadata";
import { isLocale } from "@/i18n";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { APP_BASE_URL } from "@/lib/urls";
import { xHandle } from "@/lib/urls-client";

import { RootLayout } from "../components/RootLayout";

export async function generateMetadata(props: LocaleParams): Promise<Metadata> {
  const { locale } = await props.params;

  const { t } = await i18nTranslation(locale);
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
  if (!isLocale(locale)) notFound();

  return <RootLayout locale={locale}>{props.children}</RootLayout>;
}
