import { Metadata } from "next";
import Link from "next/link";

import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { api, MempoolPostIndex } from "@/lib/api";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

import { PostListing } from "./components/PostListing";

const generateHref = (l: Locale) => urls(l).mempool.index;

export async function generateMetadata(props: LocaleParams): Promise<Metadata> {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs(locales, generateHref);

  return {
    title: t("memory_pool"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function MempoolIndex(props: LocaleParams) {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const { data: posts } = await api.mempool.getMempoolPosts({ query: { locale } });

  return (
    <PageLayout t={t} locale={locale} generateHref={generateHref}>
      <PageHeader title={t("memory_pool")}>
        <p>{t("memory_pool_description")}</p>
        <p>
          <em>{t("mempool_invalid_transactions")}</em>
        </p>
        <p>
          <Link className="underline" href={urls(locale).mempool.rss}>
            {t("rss_feed")}
          </Link>
        </p>
      </PageHeader>
      <section>
        {posts.map((post: MempoolPostIndex) => (
          <PostListing key={post.slug} t={t} locale={locale} post={post} />
        ))}
      </section>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
