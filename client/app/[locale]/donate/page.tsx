import { Metadata } from "next";

import { ButtonLink } from "@/app/components/Button";
import { Markdown } from "@/app/components/Markdown";
import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getPage } from "@/lib/content";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

const generateHref = (l: Locale) => urls(l).donate.index;

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    title: t("donate"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function DonatePage({ params: { locale } }: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const content = await getPage("donate", locale);

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref}>
      <PageHeader title={t("donate")} />
      <Markdown className="page-content mb-4">{content}</Markdown>
      <ButtonLink href={urls(locale).donate.zaprite}>{t("donate")}</ButtonLink>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
