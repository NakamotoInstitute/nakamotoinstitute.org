import { Metadata } from "next";
import Link from "next/link";
import { PageLayout } from "@/app/components";
import { PageHeader } from "@/app/components/PageHeader";
import { getAllMempoolSeries } from "@/lib/api";
import { MempoolSeries } from "@/lib/api/schemas";
import { getLocaleParams, i18nTranslation } from "@/lib/i18n";
import { urls } from "@/lib/urls";

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  return {
    title: t("Mempool Series"),
  };
}

function SeriesListing({
  locale,
  series,
}: {
  locale: Locale;
  series: MempoolSeries;
}) {
  return (
    <article className="border-b border-solid border-night py-4 first:pt-0 last:border-b-0">
      <h2>
        <Link href={urls(locale).mempool.seriesDetail(series.slug)}>
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
  const generateHref = (l: Locale) => urls(l).mempool.seriesIndex;

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={t("Mempool Series")}>
        <p>{t("Extended blogchains for a deeper dive")}</p>
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
