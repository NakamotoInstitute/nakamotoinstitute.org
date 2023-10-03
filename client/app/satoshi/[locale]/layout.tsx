import { RootLayout } from "@/app/components";
import { i18nTranslation } from "@/lib/i18n";
import { Metadata } from "next";

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const siteTitle = t("Satoshi Nakamoto Institute");
  return {
    title: {
      template: `%s | ${siteTitle}`,
      default: `${t("The Complete Satoshi")} | ${siteTitle}`,
    },
    description: t("Bitcoin scholarship"),
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