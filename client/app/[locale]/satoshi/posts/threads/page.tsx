import { Metadata } from "next";

import { locales } from "@/i18n";
import { getForumThreads } from "@/lib/api/posts";
import {
  FORUM_POST_SOURCES,
  ForumPostSource,
  ForumThread,
} from "@/lib/api/schemas/posts";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatPostSource } from "@/utils/strings";

import { ContentListing } from "@satoshi/components/ContentListing";
import { IndexPageLayout } from "@satoshi/components/IndexPageLayout";

const generateHref = (l: Locale) => urls(l).satoshi.posts.threadsIndex;

export async function generateMetadata(props: LocaleParams): Promise<Metadata> {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs(locales, generateHref);

  return {
    title: t("forum_threads"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function PostThreadsIndex(props: LocaleParams) {
  const params = await props.params;

  const { locale } = params;

  const { t } = await i18nTranslation(locale);
  const threads = await getForumThreads();
  const sortedThreads = threads.reduce(
    (acc, thread) => {
      acc[thread.source].push(thread);
      return acc;
    },
    Object.fromEntries(
      FORUM_POST_SOURCES.map((source) => [source, [] as ForumThread[]]),
    ) as {
      [K in ForumPostSource]: ForumThread[];
    },
  );

  const sourceLinks = [
    {
      name: t("all"),
      href: urls(locale).satoshi.posts.threadsIndex,
      active: true,
    },
    ...FORUM_POST_SOURCES.map((s) => ({
      name: formatPostSource(s),
      href: urls(locale).satoshi.posts.sourceThreadsIndex(s),
    })),
  ];

  return (
    <IndexPageLayout
      t={t}
      type="posts"
      locale={locale}
      generateHref={generateHref}
      breadcrumbs={[
        { label: t("complete_satoshi"), href: urls(locale).satoshi.index },
        {
          label: t("forum_posts"),
          href: urls(locale).satoshi.posts.threadsIndex,
        },
      ]}
      sourceLinks={sourceLinks}
      toggleLinks={{
        active: "threads",
        href: urls(locale).satoshi.posts.index,
      }}
    >
      <section>
        {Object.entries(sortedThreads).map(([source, sourceThreads]) => {
          const typedSource = source as ForumPostSource;
          return (
            <div key={typedSource} className="pt-5">
              <h2 className="text-2xl font-bold">
                {formatPostSource(typedSource)}
              </h2>
              {sourceThreads.map((thread) => (
                <ContentListing
                  key={thread.id}
                  locale={locale}
                  label={thread.title}
                  href={urls(locale).satoshi.posts.sourceThreadsDetail(
                    thread.source,
                    thread.id.toString(),
                  )}
                  date={thread.date}
                />
              ))}
            </div>
          );
        })}
      </section>
    </IndexPageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
