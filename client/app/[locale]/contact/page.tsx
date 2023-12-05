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
    title: t("Contact"),
  };
}

export default async function ContactPage({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const generateHref = (l: Locale) => urls(l).contact;

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={t("Contact")} />
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
