import { Metadata } from "next";
import Link from "next/link";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getAuthors } from "@/lib/api/authors";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

const generateHref = (l: Locale) => urls(l).authors.index;

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    title: t("authors"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function AuthorsIndex({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const authors = await getAuthors(locale);
  const generateHref = (l: Locale) => urls(l).authors.index;

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref}>
      <PageHeader title={t("authors")} />
      <ul>
        {authors.map((author) => (
          <li key={author.slug}>
            <Link href={urls(locale).authors.detail(author.slug)}>
              {author.name}
            </Link>
          </li>
        ))}
      </ul>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
