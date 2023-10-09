import { PageLayout, PageHeader } from "@/app/components";
import { ForumPostSource, ForumThread, getForumThreads } from "@/lib/api";
import { getLocaleParams } from "@/lib/i18n";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatPostSource } from "@/utils/strings";
import Link from "next/link";

export default async function PostThreadsIndex({
  params: { locale },
}: LocaleParams) {
  const threads = await getForumThreads();
  const generateHref = (l: Locale) => urls(l).satoshi.posts.threadsIndex;
  const sortedThreads = threads.reduce(
    (acc, thread) => {
      acc[thread.source].push(thread);
      return acc;
    },
    { p2pfoundation: [], bitcointalk: [] } as {
      [K in ForumPostSource]: ForumThread[];
    },
  );

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title="Forum Threads" />
      <section>
        {Object.entries(sortedThreads).map(([source, sourceThreads]) => {
          const typedSource = source as ForumPostSource;
          return (
            <div key={typedSource} className="pb-4 last:pb-0">
              <h2 className="pb-2 text-3xl">{formatPostSource(typedSource)}</h2>
              <ul>
                {sourceThreads.map((thread) => (
                  <li key={thread.id}>
                    <Link
                      href={urls(locale).satoshi.posts.sourceThreadsDetail(
                        thread.source,
                        thread.id.toString(),
                      )}
                    >
                      {thread.title}
                    </Link>{" "}
                    - <em>{formatDate(locale, thread.date)}</em>
                  </li>
                ))}
              </ul>
            </div>
          );
        })}
      </section>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
