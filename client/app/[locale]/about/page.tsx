import { Metadata } from "next";

import { Markdown } from "@/app/components/Markdown";
import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { getPage } from "@/lib/content";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  return {
    title: t("About"),
  };
}

export default async function AboutPage({ params: { locale } }: LocaleParams) {
  const content = await getPage("about", locale);
  const { t } = await i18nTranslation(locale);
  const generateHref = (l: Locale) => urls(l).about;

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={t("About")} />
      <Markdown className="page-content">{content}</Markdown>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
