import { Metadata, ResolvingMetadata } from "next";

import { i18nTranslation } from "@/lib/i18n/i18nTranslation";

export async function generateMetadata(
  props: LocaleParams,
  parent: ResolvingMetadata,
): Promise<Metadata> {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const parentTitleTemplate = (await parent).title?.template;
  const sectionTitle = t("quotable_satoshi");
  return {
    title: {
      template: parentTitleTemplate
        ? `${sectionTitle} - ${parentTitleTemplate}`
        : `${sectionTitle} - %s`,
      default: sectionTitle,
    },
  };
}

type QuotesLayoutProps = {
  children: React.ReactNode;
};

export default function QuotesLayout({ children }: QuotesLayoutProps) {
  return children;
}
