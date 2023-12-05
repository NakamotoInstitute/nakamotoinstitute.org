import { ReactNode } from "react";
import { Metadata, ResolvingMetadata } from "next";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";

export async function generateMetadata(
  { params: { locale } }: LocaleParams,
  parent: ResolvingMetadata,
): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const parentTitleTemplate = (await parent).title?.template;
  const sectionTitle = t("The Quotable Satoshi");
  return {
    title: {
      template: parentTitleTemplate
        ? `${sectionTitle} - ${parentTitleTemplate}`
        : `${sectionTitle} - %s`,
      default: sectionTitle,
    },
  };
}

export default function QuotesLayout({ children }: { children: ReactNode }) {
  return children;
}
