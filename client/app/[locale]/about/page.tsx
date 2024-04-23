import { Metadata } from "next";

import { Markdown } from "@/app/components/Markdown";
import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getPage } from "@/lib/content";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

const generateHref = (l: Locale) => urls(l).about;

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    title: t("about"),
    alternates: { languages },
  };
}

export default async function AboutPage({ params: { locale } }: LocaleParams) {
  const content = await getPage("about", locale);
  const { t } = await i18nTranslation(locale);

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref}>
      <PageHeader title={t("about")} />
      <Markdown className="page-content">{content}</Markdown>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
