import { Metadata } from "next";

import { RootLayout } from "@/app/components/RootLayout";
import { openGraphImages } from "@/app/shared-metadata";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const siteTitle = t("sni_full");
  return {
    title: {
      template: `%s | ${siteTitle}`,
      default: `${t("complete_satoshi")} | ${siteTitle}`,
    },
    description: t("sni_mission_statement"),
    openGraph: { images: openGraphImages },
    twitter: { images: openGraphImages },
  };
}

export default function SatoshiLayout({
  params: { locale },
  children,
}: LocaleParams & {
  children: React.ReactNode;
}) {
  return <RootLayout locale={locale}>{children}</RootLayout>;
}
