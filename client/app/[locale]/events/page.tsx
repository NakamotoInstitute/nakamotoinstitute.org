import { Metadata } from "next";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

const generateHref = (l: Locale) => urls(l).events;

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    title: t("events"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function EventsPage({ params: { locale } }: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const generateHref = (l: Locale) => urls(l).events;

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref}>
      <PageHeader title={t("events")} />
      <div className="text-center">
        <p>{t("no_events_message")}</p>
      </div>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
