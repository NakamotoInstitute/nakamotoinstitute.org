import { Metadata } from "next";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

const generateHref = (l: Locale) => urls(l).contact;

export async function generateMetadata(props: LocaleParams): Promise<Metadata> {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    title: t("contact"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function ContactPage(props: LocaleParams) {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref}>
      <PageHeader title={t("contact")} />
      <p>contact (at) nakamotoinstitute (dot) org</p>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
