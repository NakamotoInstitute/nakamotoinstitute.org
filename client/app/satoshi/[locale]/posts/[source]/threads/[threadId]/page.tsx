import { PageLayout } from "@/app/components/PageLayout";
import { getForumThread, getForumThreads } from "@/lib/api/posts";
import { ForumPostSource, ForumPost } from "@/lib/api/schemas/posts";
import { getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatPostSource } from "@/utils/strings";
import clsx from "clsx";
import Link from "next/link";
import { notFound } from "next/navigation";

export const dynamicParams = false;

function ThreadPost({
  locale,
  post,
  odd,
  satoshiOnly,
}: {
  locale: Locale;
  post: ForumPost;
  odd: boolean;
  satoshiOnly: boolean;
}) {
  return (
    <article
      id={post.sourceId}
      className={clsx(
        "mb-3 border-2 border-night font-mono text-[13px] last:mb-0",
        odd ? "bg-gray" : "bg-white",
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
      <header className={clsx(post.satoshiId && "bg-flax")}>
        <div className="flex justify-between border-b-1 border-b-night p-2">
          <span className="font-bold">
            {post.posterUrl ? (
              <Link href={post.posterUrl}>{post.posterName}</Link>
            ) : (
              post.posterName
            )}
          </span>
          <Link href={{ hash: post.sourceId }}>#{post.sourceId}</Link>
        </div>
        <div className="border-b-1 border-b-night p-2">
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
          className="p-2 font-serif text-sm [&>.post>img]:inline"
          dangerouslySetInnerHTML={{
            __html: post.text,
          }}
        />
      </section>
      <footer className="flex justify-between border-t-1 border-t-night p-2">
        <Link href={post.url}>External link</Link>
        {post.satoshiId ? (
          <Link
            href={urls(locale).satoshi.posts.sourcePost(
              post.source,
              post.satoshiId.toString(),
            )}
          >
            Permalink
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

  const generateHref = (l: Locale) =>
    urls(l).satoshi.posts.sourceThreadsDetail(source, threadId);

  const { thread, posts } = threadData;

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <div className="text-center">
        <p>{formatPostSource(thread.source)}</p>
        <h1 className="text-2xl">{thread.title}</h1>
        {satoshiOnly ? (
          <Link href={generateHref(locale)}>View all posts</Link>
        ) : (
          <Link href={{ query: { view: "satoshi" } }}>View Satoshi only</Link>
        )}
      </div>
      {posts.map((p, index) => (
        <ThreadPost
          key={p.sourceId}
          locale={locale}
          post={p}
          odd={index % 2 !== 0}
          satoshiOnly={satoshiOnly}
        />
      ))}
    </PageLayout>
  );
}

export async function generateStaticParams() {
  const threads = await getForumThreads();
  return getLocaleParams((locale) =>
    threads.map((t) => ({
      locale,
      source: t.source,
      threadId: t.id.toString(),
    })),
  );
}
