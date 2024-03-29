import { Metadata } from "next";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getLibraryDocs } from "@/lib/api/library";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

import { DocListing } from "./components/DocListing";

export const dynamicParams = false;

const generateHref = (l: Locale) => urls(l).library.index;

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    title: t("Library"),
    alternates: { languages },
  };
}

export default async function LibraryIndex({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const docs = await getLibraryDocs(locale);

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={t("Library")}>
        <p>
          {t(
            "Bitcoin was not forged in a vacuum. These works serve to contextualize bitcoin into the broader story of cryptography and freedom.",
          )}
        </p>
      </PageHeader>
      <section>
        {docs.length > 0 ? (
          docs.map((doc) => (
            <DocListing key={doc.slug} doc={doc} locale={locale} />
          ))
        ) : (
          <p className="text-center">
            {t("The library is empty for this language.")}
          </p>
        )}
      </section>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
