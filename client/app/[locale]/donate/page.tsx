import { Metadata } from "next";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

const generateHref = (l: Locale) => urls(l).donate;

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

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={t("Donate")} />
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
