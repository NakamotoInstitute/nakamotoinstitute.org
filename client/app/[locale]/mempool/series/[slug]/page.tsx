import { Metadata } from "next";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import {
  api,
  Locale,
  MempoolPostIndex,
  TranslationSchema,
} from "@/lib/api";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { urls } from "@/lib/urls";

import { PostListing } from "@main/mempool/components/PostListing";

export const dynamicParams = false;

export async function generateMetadata(
  props: LocaleParams<{ slug: string }>,
): Promise<Metadata> {
  const params = await props.params;

  const { locale, slug } = params;

  const {
    data: { series },
  } = await api.mempool.getMempoolSeries({
    path: { slug },
    query: { locale },
  });
  const languages = series.translations.reduce(
    (acc: Record<Locale, string>, t: TranslationSchema) => {
      acc[t.locale] = urls(t.locale).mempool.seriesDetail(t.slug);
      return acc;
    },
    {} as Record<Locale, string>,
  );

  return {
    title: series.title,
    alternates: {
      canonical: urls(locale).mempool.seriesDetail(slug),
      languages,
    },
  };
}

export default async function SeriesDetail(
  props: LocaleParams<{ slug: string }>,
) {
  const params = await props.params;

  const { slug, locale } = params;

  const { t } = await i18nTranslation(locale);
  const {
    data: { series, posts },
  } = await api.mempool.getMempoolSeries({
    path: { slug },
    query: { locale },
  });

  const generateHref = (l: Locale) => {
    const translation = series.translations.find((t: TranslationSchema) => t.locale === l);
    if (translation) {
      return urls(l).mempool.seriesDetail(translation.slug);
    }
    return urls(l).mempool.seriesIndex;
  };

  return (
    <PageLayout
      t={t}
      locale={locale}
      generateHref={generateHref}
      breadcrumbs={[
        { label: t("mempool"), href: urls(locale).mempool.index },
        { label: t("mempool_series"), href: urls(locale).mempool.seriesIndex },
        {
          label: series.title,
          href: urls(locale).mempool.seriesDetail(series.slug),
        },
      ]}
    >
      <PageHeader title={series.title} />
      <section>
        {posts?.map((post: MempoolPostIndex) => (
          <PostListing key={post.slug} t={t} locale={locale} post={post} />
        ))}
      </section>
    </PageLayout>
  );
}

export async function generateStaticParams() {
  const { data } = await api.mempool.getMempoolSeriesParams();
  return data;
}
