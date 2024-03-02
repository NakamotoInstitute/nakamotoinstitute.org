import { Metadata } from "next";

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
    title: t("Donate"),
    alternates: { languages },
  };
}

export default async function DonatePage({ params: { locale } }: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const content = await getPage("donate", locale);

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={t("Donate")} />
      <Markdown className="prose mx-auto mb-4">{content}</Markdown>
      <div className="text-center">
        <a
          className="inline-block cursor-pointer select-none rounded border border-solid border-blue-600 bg-blue-600 px-3 py-1 text-white hover:border-blue-700 hover:bg-blue-700 hover:text-white focus:border-blue-700 focus:bg-blue-700 focus:text-white"
          href={urls(locale).donate.zaprite}
          role="button"
        >
          {t("Donate")}
        </a>
      </div>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
