import { Metadata } from "next";

import { ButtonLink } from "@/app/components/Button";
import { Markdown } from "@/app/components/Markdown";
import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getPage } from "@/lib/content";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

const generateHref = (l: Locale) => urls(l).finney.rpow;

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    title: t("rpow_title"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function RPOWPage({ params: { locale } }: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const content = await getPage("rpow", locale);

  return (
    <PageLayout
      t={t}
      locale={locale}
      generateHref={generateHref}
      breadcrumbs={[
        { label: t("hal_finney"), href: urls(locale).finney.index },
        { label: t("RPOW"), href: urls(locale).finney.rpow },
      ]}
    >
      <PageHeader title={t("rpow_title")} />
      <div className="flex gap-3">
        <ButtonLink href="/finney/rpow/index.html">
          {t("archived_website")}
        </ButtonLink>
        <ButtonLink href="https://github.com/NakamotoInstitute/RPOW">
          {t("github")}
        </ButtonLink>
        <ButtonLink href="/library/rpow">
          {t("original_announcement")}
        </ButtonLink>
      </div>
      <hr className="my-4" />
      <Markdown className="page-content">{content}</Markdown>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
