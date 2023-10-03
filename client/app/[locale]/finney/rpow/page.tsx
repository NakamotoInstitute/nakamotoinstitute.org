import { PageLayout } from "@/app/components";
import { PageHeader } from "@/app/components/PageHeader";
import { getLocaleParams, i18nTranslation } from "@/lib/i18n";
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
