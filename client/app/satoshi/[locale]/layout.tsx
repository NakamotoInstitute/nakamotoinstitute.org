import { Metadata } from "next";

import { RootLayout } from "@/app/components/RootLayout";
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
    robots: {
      index: false,
      follow: false,
      nocache: true,
    },
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
