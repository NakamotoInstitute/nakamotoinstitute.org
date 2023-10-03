import { PageLayout } from "@/app/components";
import { PageHeader } from "@/app/components/PageHeader";
import { getLocaleParams, i18nTranslation } from "@/lib/i18n";
import { urls } from "@/lib/urls";
import { formatDateRange } from "@/utils/dates";
import { Metadata } from "next";

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  return {
    title: t("Hal Finney"),
  };
}

export default async function FinneyIndex({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const generateHref = (l: Locale) => urls(l).finney.index;

  const birthDate = new Date(Date.UTC(1956, 4, 4));
  const deathDate = new Date(Date.UTC(2014, 7, 28));

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={t("Hal Finney")}>
        <p>{formatDateRange(locale, birthDate, deathDate)}</p>
      </PageHeader>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
