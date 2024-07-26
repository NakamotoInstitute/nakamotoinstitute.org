import { Metadata } from "next";

import { locales } from "@/i18n";
import { getSatoshiPosts } from "@/lib/api/posts";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatPostSource } from "@/utils/strings";

import { ContentListing } from "@satoshi/components/ContentListing";
import { IndexPageLayout } from "@satoshi/components/IndexPageLayout";

export const dynamicParams = false;

const generateHref = (l: Locale) => urls(l).satoshi.posts.index;

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    title: t("forum_posts"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function PostsIndex({ params: { locale } }: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const posts = await getSatoshiPosts();

  return (
    <IndexPageLayout
      t={t}
      type="posts"
      locale={locale}
      generateHref={generateHref}
      breadcrumbs={[
        { label: t("complete_satoshi"), href: urls(locale).satoshi.index },
        { label: t("forum_posts"), href: urls(locale).satoshi.emails.index },
      ]}
      sourceLinks={[
        {
          name: t("all"),
          active: true,
        },
        {
          name: formatPostSource("p2pfoundation"),
          href: urls(locale).satoshi.posts.sourceIndex("p2pfoundation"),
        },
        {
          name: formatPostSource("bitcointalk"),
          href: urls(locale).satoshi.posts.sourceIndex("bitcointalk"),
        },
      ]}
      toggleLinks={{
        active: "individual",
        href: urls(locale).satoshi.posts.threadsIndex,
      }}
    >
      <section>
        {posts.map((p) => (
          <ContentListing
            key={p.satoshiId}
            locale={locale}
            label={p.subject}
            href={urls(locale).satoshi.posts.sourcePost(
              p.source,
              p.satoshiId.toString(),
            )}
            date={p.date}
          />
        ))}
      </section>
    </IndexPageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
