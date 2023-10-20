import { Metadata } from "next";
import { RootLayout } from "../components";
import { i18nTranslation } from "@/lib/i18n";

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const siteTitle = t("Satoshi Nakamoto Institute");
  return {
    title: {
      template: `%s | ${siteTitle}`,
      default: siteTitle,
    },
    description: t("Bitcoin scholarship"),
    robots: {
      index: false,
      follow: false,
      nocache: true,
    },
  };
}

export default function MainLayout({
  params: { locale },
  children,
}: LocaleParams & {
  children: React.ReactNode;
}) {
  return <RootLayout locale={locale}>{children}</RootLayout>;
}
