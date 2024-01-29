import { Metadata } from "next";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  return {
    title: t("Events"),
  };
}

export default async function EventsPage({ params: { locale } }: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const generateHref = (l: Locale) => urls(l).events;

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={t("Events")} />
      <div className="text-center">
        <p>{t("There are no events currently scheduled.")}</p>
      </div>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
