import { Metadata } from "next";

import { RootLayout } from "@/app/components/RootLayout";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { cdnUrl } from "@/lib/urls";

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
    openGraph: {
      images: [
        {
          url: cdnUrl("/img/sni_opengraph_1200.jpg"),
          width: 1200,
          height: 675,
        },
      ],
    },
    twitter: {
      images: [
        {
          url: cdnUrl("/img/sni_opengraph_1200.jpg"),
          width: 1200,
          height: 675,
        },
      ],
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
