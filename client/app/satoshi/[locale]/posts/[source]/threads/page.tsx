import { Metadata } from "next";

import { locales } from "@/i18n";
import { getForumThreadsBySource } from "@/lib/api/posts";
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
  urls(l).satoshi.posts.sourceThreadsIndex(source);

export async function generateMetadata({
  params: { locale, source },
}: LocaleParams<{ source: ForumPostSource }>): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref(source));

  return {
    title: t("source_threads", { source: formatPostSource(source) }),
    alternates: {
      canonical: generateHref(source)(locale),
      languages,
    },
  };
}

export default async function PostSourceThreadsIndex({
  params: { source, locale },
}: LocaleParams<{ source: ForumPostSource }>) {
  const { t } = await i18nTranslation(locale);
  const threads = await getForumThreadsBySource(source);

  const sourceLinks = [
    { name: t("all"), href: urls(locale).satoshi.posts.threadsIndex },
    ...FORUM_POST_SOURCES.map((s) => ({
      name: formatPostSource(s),
      href: urls(locale).satoshi.posts.sourceThreadsIndex(s),
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
        {
          label: t("forum_posts"),
          href: urls(locale).satoshi.posts.threadsIndex,
        },
        {
          label: formatPostSource(source),
          href: urls(locale).satoshi.posts.sourceThreadsIndex(source),
        },
      ]}
      sourceLinks={sourceLinks}
      toggleLinks={{
        active: "threads",
        href: urls(locale).satoshi.posts.sourceIndex(source),
      }}
    >
      <section>
        {threads.map((t) => (
          <ContentListing
            key={t.id}
            locale={locale}
            label={t.title}
            href={urls(locale).satoshi.posts.sourceThreadsDetail(
              t.source,
              t.id.toString(),
            )}
            date={t.date}
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
