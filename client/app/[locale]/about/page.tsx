import { getPage } from "@/lib/content/pages";
import { getLocaleParams, i18nTranslation } from "@/lib/i18n";
import { Markdown, PageLayout } from "@/app/components";
import { urls } from "@/lib/urls";
import { PageHeader } from "@/app/components/PageHeader";
import { Metadata } from "next";

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  return {
    title: t("About"),
  };
}

export default async function AboutPage({ params: { locale } }: LocaleParams) {
  const content = await getPage("about", locale);
  const { t } = await i18nTranslation(locale);
  const generateHref = (l: Locale) => urls(l).about;

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={t("About")} />
      <Markdown>{content}</Markdown>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
