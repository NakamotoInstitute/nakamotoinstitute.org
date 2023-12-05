import Link from "next/link";
import { PageLayout } from "@/app/components/PageLayout";
import { getAuthors } from "@/lib/api/authors";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { PageHeader } from "@/app/components/PageHeader";
import { Metadata } from "next";

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  return {
    title: t("Authors"),
  };
}

export default async function AuthorsIndex({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const authors = await getAuthors(locale);
  const generateHref = (l: Locale) => urls(l).authors.index;

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={t("Authors")} />
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
