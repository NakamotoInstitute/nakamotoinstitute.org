import { Metadata } from "next";
import Link from "next/link";

import { Markdown } from "@/app/components/Markdown";
import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { getPage } from "@/lib/content";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

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
  const content = await getPage("rpow", locale);

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={t("RPOW - Reusable Proofs of Work")} />
      <div className="text-center">
        <p>
          <Link href="/finney/rpow/index.html">{t("Archived Website")}</Link>
        </p>
        <p>
          <Link href="https://github.com/NakamotoInstitute/RPOW">
            {t("GitHub")}
          </Link>
        </p>
        <p>
          <Link href="/library/rpow">{t("Original Announcement")}</Link>
        </p>
      </div>
      <hr className="my-4" />
      <Markdown className="page-content">{content}</Markdown>
      <hr className="my-4" />
      <div className="text-center">
        <Link href={urls(locale).finney.index}>{t("Back")}</Link>
      </div>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
