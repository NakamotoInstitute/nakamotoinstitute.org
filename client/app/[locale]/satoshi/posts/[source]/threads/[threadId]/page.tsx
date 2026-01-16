import clsx from "clsx";
import { TFunction } from "i18next";
import { Metadata } from "next";
import { notFound } from "next/navigation";

import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { api, ForumPost, ForumPostSource } from "@/lib/api";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatPostSource } from "@/utils/strings";

import {
  ContentBox,
  ContentBoxBody,
  ContentBoxDisclaimer,
  ContentBoxFooter,
  ContentBoxHeader,
} from "@satoshi/components/ContentBox";
import { PostThreadNavigation } from "@satoshi/components/ContentNavigation";
import { ThreadPageHeader } from "@satoshi/components/ThreadPageHeader";

export const dynamicParams = false;

const generateHref =
  (source: ForumPostSource, threadId: string) => (l: Locale) =>
    urls(l).satoshi.posts.sourceThreadsDetail(source, threadId);

export async function generateMetadata(
  props: LocaleParams<{
    source: ForumPostSource;
    threadId: string;
  }>,
): Promise<Metadata> {
  const params = await props.params;

  const { locale, source, threadId } = params;

  const { data: threadData } = await api.satoshi.getForumThreadBySource({
    path: { source, thread_id: parseInt(threadId) },
  });
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs(locales, generateHref(source, threadId));

  return {
    title: t("title_thread", { title: threadData.thread.title }),
    alternates: {
      canonical: generateHref(source, threadId)(locale),
      languages,
    },
  };
}

type ThreadPostProps = {
  t: TFunction<string, string>;
  locale: Locale;
  post: ForumPost;
  odd: boolean;
  satoshiOnly: boolean;
};

async function ThreadPost({
  t,
  locale,
  post,
  odd,
  satoshiOnly,
}: ThreadPostProps) {
  return (
    <ContentBox
      id={post.sourceId}
      as="article"
      className={clsx(
        "mb-3 last:mb-0",
        !satoshiOnly &&
          post.source === "p2pfoundation" && [
            "relative",
            {
              "before:absolute before:-left-6 before:content-['↳']":
                (post.nestedLevel ?? 0) > 0,
              "ml-6": (post.nestedLevel ?? 0) === 1,
              "ml-12": (post.nestedLevel ?? 0) === 2,
              "ml-18": (post.nestedLevel ?? 0) === 3,
            },
          ],
      )}
      alternate={odd}
    >
      <ContentBoxHeader
        t={t}
        locale={locale}
        source={formatPostSource(post.source)}
        sourceId={post.sourceId}
        from={post.posterName}
        subject={post.subject}
        date={post.date}
        satoshi={!!post.satoshiId}
      />
      <ContentBoxBody>
        <div
          className="[&>.post>img]:inline"
          dangerouslySetInnerHTML={{
            __html: post.text,
          }}
        />
      </ContentBoxBody>
      {post.disclaimer && (
        <ContentBoxDisclaimer t={t} disclaimer={post.disclaimer} />
      )}
      <ContentBoxFooter
        t={t}
        hrefs={{
          original: post.url,
          permalink: post.satoshiId
            ? urls(locale).satoshi.posts.sourcePost(
                post.source,
                post.satoshiId.toString(),
              )
            : undefined,
        }}
      />
    </ContentBox>
  );
}

export default async function PostSourceThreadDetail(
  props: LocaleParams<
    { source: ForumPostSource; threadId: string },
    { searchParams: Promise<{ [key: string]: string | string[] | undefined }> }
  >,
) {
  const searchParams = await props.searchParams;

  const { view } = searchParams;

  const params = await props.params;

  const { source, threadId, locale } = params;

  const satoshiOnly = view === "satoshi";
  const { data: threadData } = await api.satoshi.getForumThreadBySource({
    path: { source, thread_id: parseInt(threadId) },
    query: satoshiOnly ? { satoshi: true } : undefined,
  });
  if (!threadData) {
    return notFound();
  }

  const { thread, posts, next, previous } = threadData;

  const { t } = await i18nTranslation(locale);

  return (
    <PageLayout
      t={t}
      locale={locale}
      generateHref={generateHref(source, threadId)}
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
    >
      <ThreadPageHeader
        t={t}
        sourceTitle={formatPostSource(thread.source)}
        title={thread.title}
        allLink={{
          href: generateHref(source, threadId)(locale),
          text: t("view_all_posts"),
        }}
        externalLink={thread.url}
        satoshiOnly={satoshiOnly}
      >
        <PostThreadNavigation
          t={t}
          locale={locale}
          id={thread.id}
          next={next}
          previous={previous}
          source={thread.source}
        />
      </ThreadPageHeader>
      {posts.map((p: ForumPost, index: number) => (
        <ThreadPost
          key={p.sourceId}
          t={t}
          locale={locale}
          post={p}
          odd={index % 2 !== 0}
          satoshiOnly={satoshiOnly}
        />
      ))}
    </PageLayout>
  );
}

// export async function generateStaticParams() {
//   const threads = await getForumThreads();
//   return getLocaleParams((locale) =>
//     threads.map((t) => ({
//       locale,
//       source: t.source,
//       threadId: t.id.toString(),
//     })),
//   );
// }
