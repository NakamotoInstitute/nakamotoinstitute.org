import { Metadata } from "next";

import { ListColumnLayout } from "@/app/components/ListColumnLayout";
import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getAuthors } from "@/lib/api/authors";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

const generateHref = (l: Locale) => urls(l).authors.index;

export async function generateMetadata(props: LocaleParams): Promise<Metadata> {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs(locales, generateHref);

  return {
    title: t("authors"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function AuthorsIndex(props: LocaleParams) {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const authors = await getAuthors(locale);
  const generateHref = (l: Locale) => urls(l).authors.index;

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref}>
      <PageHeader title={t("authors")} />
      <ListColumnLayout
        items={authors}
        hrefFunc={(slug: string) => urls(locale).authors.detail(slug)}
      />
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
