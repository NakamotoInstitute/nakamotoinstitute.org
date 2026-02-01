import { Metadata } from "next";
import Link from "next/link";

import { Markdown } from "@/app/components/Markdown";
import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { DocumentIndex, api, getOrNotFound } from "@/lib/api";
import { getPage } from "@/lib/content";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate, formatDateRange } from "@/utils/dates";

const generateHref = (l: Locale) => urls(l).finney.index;

export async function generateMetadata(props: LocaleParams): Promise<Metadata> {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs(locales, generateHref);

  return {
    title: t("hal_finney"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function FinneyIndex(props: LocaleParams) {
  const params = await props.params;

  const { locale } = params;

  const [{ t }, content, { library }] = await Promise.all([
    i18nTranslation(locale),
    getPage("finney", locale),
    getOrNotFound(
      api.authors.getAuthor({
        path: { slug: "hal-finney" },
        query: { locale: "en" },
      }),
    ),
  ]);

  const birthDate = new Date(Date.UTC(1956, 4, 4));
  const deathDate = new Date(Date.UTC(2014, 7, 28));

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref}>
      <PageHeader title={t("hal_finney")}>
        <p className="text-xl text-gray-500">
          {formatDateRange(locale, birthDate, deathDate)}
        </p>
      </PageHeader>
      <Markdown>{content}</Markdown>
      <hr className="my-4" />
      <h2 className="mb-2 text-2xl font-medium">Library</h2>
      <ul className="mb-4">
        {library.map((doc: DocumentIndex) => (
          <li key={doc.slug} className="mb-2">
            <Link
              className="text-cardinal hover:underline"
              href={urls(locale).library.doc(doc.slug)}
            >
              {doc.title}
            </Link>{" "}
            ({formatDate(locale, doc.date)})
          </li>
        ))}
      </ul>
      <h2 className="mb-2 text-2xl font-medium">Code</h2>
      <ul>
        <li>
          <Link
            className="text-cardinal hover:underline"
            href={urls(locale).finney.rpow}
          >
            {t("rpow_title")}
          </Link>
        </li>
      </ul>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
