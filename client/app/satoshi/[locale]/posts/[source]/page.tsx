import { Metadata } from "next";

import { locales } from "@/i18n";
import { getSatoshiPostsBySource } from "@/lib/api/posts";
import { ForumPostSource, zForumPostSource } from "@/lib/api/schemas/posts";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatPostSource, otherForumPostSource } from "@/utils/strings";

import { ContentListing } from "@satoshi/components/ContentListing";
import { SourceLink } from "@satoshi/components/IndexHeader";
import { IndexPageLayout } from "@satoshi/components/IndexPageLayout";

export const dynamicParams = false;

const generateHref = (source: ForumPostSource) => (l: Locale) =>
  urls(l).satoshi.posts.sourceIndex(source);

export async function generateMetadata({
  params: { locale, source },
}: LocaleParams<{ source: ForumPostSource }>): Promise<Metadata> {
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

export default async function PostsSourceIndex({
  params: { source, locale },
}: LocaleParams<{ source: ForumPostSource }>) {
  const { t } = await i18nTranslation(locale);
  const posts = await getSatoshiPostsBySource(source);

  const otherSource = otherForumPostSource(source);

  const allLink: SourceLink = {
    name: t("all"),
    href: urls(locale).satoshi.posts.index,
  };
  const additionalLinks: SourceLink[] =
    source === "p2pfoundation"
      ? [
          { name: formatPostSource("p2pfoundation"), active: true },
          {
            name: formatPostSource("bitcointalk"),
            href: urls(locale).satoshi.posts.sourceIndex(otherSource),
          },
        ]
      : [
          {
            name: formatPostSource("p2pfoundation"),
            href: urls(locale).satoshi.posts.sourceIndex(otherSource),
          },
          { name: formatPostSource("bitcointalk"), active: true },
        ];
  const sourceLinks = [allLink, ...additionalLinks];

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
