import { getMempoolPosts } from "@/lib/api/mempool";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { getLocaleParams } from "@/lib/i18n/utils";
import { PageLayout } from "@/app/components/PageLayout";
import { PostListing } from "./components/PostListing";
import { urls } from "@/lib/urls";
import Link from "next/link";
import { PageHeader } from "@/app/components/PageHeader";
import { Metadata } from "next";

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  return {
    title: t("The Memory Pool"),
  };
}

export default async function MempoolIndex({
  params: { locale },
}: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const posts = await getMempoolPosts(locale);
  const generateHref = (l: Locale) => urls(l).mempool.index;

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={t("The Memory Pool")}>
        <p>
          Where ideas wait to be mined into the blockchain of the collective
          conscience
        </p>
        <p>
          <em>Some transactions may be invalid</em>
        </p>
        <p>
          <Link href="#">Feed</Link>
        </p>
      </PageHeader>
      <section>
        {posts.map((post) => (
          <PostListing key={post.slug} locale={locale} post={post} />
        ))}
      </section>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
