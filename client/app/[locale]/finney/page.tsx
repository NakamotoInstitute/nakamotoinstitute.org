import { Metadata } from "next";
import Link from "next/link";

import { Markdown } from "@/app/components/Markdown";
import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getAuthor } from "@/lib/api/authors";
import { getPage } from "@/lib/content";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate, formatDateRange } from "@/utils/dates";

const generateHref = (l: Locale) => urls(l).finney.index;

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    title: t("Hal Finney"),
    alternates: { languages },
  };
}

export default async function FinneyIndex({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const content = await getPage("finney", locale);
  const { library } = await getAuthor("hal-finney", "en");

  const birthDate = new Date(Date.UTC(1956, 4, 4));
  const deathDate = new Date(Date.UTC(2014, 7, 28));

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={t("Hal Finney")}>
        <p className="text-xl text-gray-500">
          {formatDateRange(locale, birthDate, deathDate)}
        </p>
      </PageHeader>
      <Markdown>{content}</Markdown>
      <hr className="my-4" />
      <h2 className="mb-2 text-2xl font-medium">Library</h2>
      <ul className="mb-4">
        {library.map((doc) => (
          <li key={doc.slug} className="mb-2">
            <Link href={urls(locale).library.doc(doc.slug)}>{doc.title}</Link> (
            {formatDate(locale, doc.date)})
          </li>
        ))}
      </ul>
      <h2 className="mb-2 text-2xl font-medium">Code</h2>
      <ul>
        <li>
          <Link href={urls(locale).finney.rpow}>
            RPOW - Reusable Proofs of Work
          </Link>
        </li>
      </ul>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
