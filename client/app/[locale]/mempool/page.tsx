import { Metadata } from "next";
import Link from "next/link";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getMempoolPosts } from "@/lib/api/mempool";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

import { PostListing } from "./components/PostListing";

const generateHref = (l: Locale) => urls(l).mempool.index;

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    title: t("memory_pool"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function MempoolIndex({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const posts = await getMempoolPosts(locale);

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref}>
      <PageHeader title={t("memory_pool")}>
        <p>{t("memory_pool_description")}</p>
        <p>
          <em>{t("mempool_invalid_transactions")}</em>
        </p>
        <p>
          <Link href={urls(locale).mempool.rss}>{t("rss_feed")}</Link>
        </p>
      </PageHeader>
      <section>
        {posts.map((post) => (
          <PostListing key={post.slug} t={t} locale={locale} post={post} />
        ))}
      </section>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
