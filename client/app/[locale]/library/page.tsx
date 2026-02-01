import { Metadata } from "next";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { DocumentIndex, api } from "@/lib/api";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

import { DocListing } from "./components/DocListing";

export const dynamicParams = false;

const generateHref = (l: Locale) => urls(l).library.index;

export async function generateMetadata(props: LocaleParams): Promise<Metadata> {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs(locales, generateHref);

  return {
    title: t("library"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function LibraryIndex(props: LocaleParams) {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const { data: docs = [] } = await api.library.getLibraryDocs({
    query: { locale },
  });

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref}>
      <PageHeader title={t("library")}>
        <p className="text-lg">{t("bitcoin_context")}</p>
      </PageHeader>
      <section>
        {docs.length > 0 ? (
          docs.map((doc: DocumentIndex) => (
            <DocListing key={doc.slug} doc={doc} locale={locale} t={t} />
          ))
        ) : (
          <p className="text-center">{t("empty_library_message")}</p>
        )}
      </section>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
