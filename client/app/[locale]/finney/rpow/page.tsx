import { PageLayout } from "@/app/components/PageLayout";
import { PageHeader } from "@/app/components/PageHeader";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { Metadata } from "next";

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  return {
    title: t("RPOW - Reusable Proofs of Work"),
  };
}

export default async function RPOWPage({ params: { locale } }: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const generateHref = (l: Locale) => urls(l).finney.rpow;

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={t("RPOW - Reusable Proofs of Work")} />
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
