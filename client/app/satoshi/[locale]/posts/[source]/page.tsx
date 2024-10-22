import { Metadata } from "next";

import { locales } from "@/i18n";
import { getSatoshiPostsBySource } from "@/lib/api/posts";
import {
  FORUM_POST_SOURCES,
  ForumPostSource,
  zForumPostSource,
} from "@/lib/api/schemas/posts";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatPostSource } from "@/utils/strings";

import { ContentListing } from "@satoshi/components/ContentListing";
import { IndexPageLayout } from "@satoshi/components/IndexPageLayout";

export const dynamicParams = false;

const generateHref = (source: ForumPostSource) => (l: Locale) =>
  urls(l).satoshi.posts.sourceIndex(source);

export async function generateMetadata(
  props: LocaleParams<{ source: ForumPostSource }>,
): Promise<Metadata> {
  const params = await props.params;

  const { locale, source } = params;

  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref(source));

  return {
    title: t("source_posts_title", { source: formatPostSource(source) }),
    alternates: {
      canonical: generateHref(source)(locale),
      languages,
    },
  };
}

export default async function PostsSourceIndex(
  props: LocaleParams<{ source: ForumPostSource }>,
) {
  const params = await props.params;

  const { source, locale } = params;

  const { t } = await i18nTranslation(locale);
  const posts = await getSatoshiPostsBySource(source);

  const sourceLinks = [
    { name: t("all"), href: urls(locale).satoshi.posts.index },
    ...FORUM_POST_SOURCES.map((s) => ({
      name: formatPostSource(s),
      href: urls(locale).satoshi.posts.sourceIndex(s),
      active: s === source,
    })),
  ];

  return (
    <IndexPageLayout
      t={t}
      type="posts"
      locale={locale}
      generateHref={generateHref(source)}
      breadcrumbs={[
        { label: t("complete_satoshi"), href: urls(locale).satoshi.index },
        { label: t("forum_posts"), href: urls(locale).satoshi.posts.index },
        {
          label: formatPostSource(source),
          href: urls(locale).satoshi.posts.sourceIndex(source),
        },
      ]}
      sourceLinks={sourceLinks}
      toggleLinks={{
        active: "individual",
        href: urls(locale).satoshi.posts.sourceThreadsIndex(source),
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
  return getLocaleParams((locale) =>
    zForumPostSource.options.map((source) => ({ locale, source })),
  );
}
