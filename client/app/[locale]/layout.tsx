import { Metadata } from "next";

import { openGraphImages } from "@/app/shared-metadata";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";

import { RootLayout } from "../components/RootLayout";

export async function generateMetadata(props: LocaleParams): Promise<Metadata> {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const siteTitle = t("sni_full");
  return {
    title: {
      template: `%s | ${siteTitle}`,
      default: siteTitle,
    },
    description: t("sni_mission_statement"),
    openGraph: { images: openGraphImages },
    twitter: { images: openGraphImages },
  };
}

export default async function MainLayout(
  props: LocaleParams & {
    children: React.ReactNode;
  },
) {
  const params = await props.params;

  const { locale } = params;

  const { children } = props;

  return <RootLayout locale={locale}>{children}</RootLayout>;
}
