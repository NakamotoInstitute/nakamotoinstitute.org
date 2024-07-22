import { Metadata } from "next";
import Link from "next/link";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getAllMempoolSeries } from "@/lib/api/mempool";
import { MempoolSeries } from "@/lib/api/schemas/mempool";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

const generateHref = (l: Locale) => urls(l).mempool.seriesIndex;

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    title: t("mempool_series"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

type SeriesListingProps = {
  locale: Locale;
  series: MempoolSeries;
};

function SeriesListing({ locale, series }: SeriesListingProps) {
  return (
    <article className="border-t border-dashed border-taupe-light py-4 last:border-b-0">
      <h2 className="font-bold md:text-xl">
        <Link
          className="text-cardinal hover:underline"
          href={urls(locale).mempool.seriesDetail(series.slug)}
        >
          <em>{series.title}</em>
        </Link>
      </h2>
    </article>
  );
}

export default async function SeriesIndex({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const allSeries = await getAllMempoolSeries(locale);

  return (
    <PageLayout
      t={t}
      locale={locale}
      generateHref={generateHref}
      breadcrumbs={[
        { label: t("mempool"), href: urls(locale).mempool.index },
        { label: t("mempool_series"), href: urls(locale).mempool.seriesIndex },
      ]}
    >
      <PageHeader title={t("mempool_series")}>
        <p>{t("mempool_series_description")}</p>
      </PageHeader>
      <section>
        {allSeries.map((series) => (
          <SeriesListing key={series.title} locale={locale} series={series} />
        ))}
      </section>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
