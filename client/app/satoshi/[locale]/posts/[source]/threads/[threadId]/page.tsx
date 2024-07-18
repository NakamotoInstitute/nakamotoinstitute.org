import clsx from "clsx";
import { TFunction } from "i18next";
import { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getForumThread } from "@/lib/api/posts";
import { ForumPost, ForumPostSource } from "@/lib/api/schemas/posts";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatPostSource } from "@/utils/strings";

import { PostThreadNavigation } from "@satoshi/components/ContentNavigation";
import { ThreadPageHeader } from "@satoshi/components/ThreadPageHeader";

export const dynamicParams = false;

const generateHref =
  (source: ForumPostSource, threadId: string) => (l: Locale) =>
    urls(l).satoshi.posts.sourceThreadsDetail(source, threadId);

export async function generateMetadata({
  params: { locale, source, threadId },
}: LocaleParams<{
  source: ForumPostSource;
  threadId: string;
}>): Promise<Metadata> {
  const threadData = await getForumThread(source, threadId);
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs(
    [...locales],
    generateHref(source, threadId),
  );

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
    <article
      id={post.sourceId}
      className={clsx(
        "mb-3 border-2 font-mono text-[13px] last:mb-0",
        odd ? "bg-neutral-100" : "bg-white",
        !satoshiOnly &&
          post.source === "p2pfoundation" && [
            "relative",
            {
              "before:absolute before:-left-6 before:content-['↳']":
                post.nestedLevel > 0,
              "ml-6": post.nestedLevel === 1,
              "ml-12": post.nestedLevel === 2,
              "ml-18": post.nestedLevel === 3,
            },
          ],
      )}
    >
      <header className={clsx(post.satoshiId && "bg-amber-200")}>
        <div className="flex justify-between border-b p-2">
          <span className="font-bold">
            {post.posterUrl ? (
              <Link href={post.posterUrl}>{post.posterName}</Link>
            ) : (
              post.posterName
            )}
          </span>
          <Link href={{ hash: post.sourceId }}>#{post.sourceId}</Link>
        </div>
        <div className="border-b p-2">
          <h2 className="text-lg font-bold">{post.subject}</h2>
          <time dateTime={post.date.toISOString()}>
            {formatDate(locale, post.date, {
              dateStyle: "long",
              timeStyle: "long",
            })}
          </time>
        </div>
      </header>
      <section>
        <div
          className="p-2 font-sans text-sm [&>.post>img]:inline"
          dangerouslySetInnerHTML={{
            __html: post.text,
          }}
        />
      </section>
      <footer className="flex justify-between border-t p-2">
        <Link href={post.url}>{t("external_link")}</Link>
        {post.satoshiId ? (
          <Link
            href={urls(locale).satoshi.posts.sourcePost(
              post.source,
              post.satoshiId.toString(),
            )}
          >
            {t("permalink")}
          </Link>
        ) : null}
      </footer>
    </article>
  );
}

export default async function PostSourceThreadDetail({
  params: { source, threadId, locale },
  searchParams: { view },
}: LocaleParams<
  { source: ForumPostSource; threadId: string },
  { searchParams: { [key: string]: string | string[] | undefined } }
>) {
  const satoshiOnly = view === "satoshi";
  const threadData = await getForumThread(source, threadId, view === "satoshi");
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
          className="mb-4"
          locale={locale}
          next={next}
          previous={previous}
          source={thread.source}
        />
      </ThreadPageHeader>
      {posts.map((p, index) => (
        <ThreadPost
          key={p.sourceId}
          t={t}
          locale={locale}
          post={p}
          odd={index % 2 !== 0}
          satoshiOnly={satoshiOnly}
        />
      ))}
      <PostThreadNavigation
        t={t}
        className="mt-4"
        locale={locale}
        next={next}
        previous={previous}
        source={thread.source}
        reverse
      />
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
