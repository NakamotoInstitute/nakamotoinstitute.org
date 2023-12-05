import Link from "next/link";
import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { getForumThreadsBySource } from "@/lib/api/posts";
import { ForumPostSource, zForumPostSource } from "@/lib/api/schemas/posts";
import { getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatPostSource } from "@/utils/strings";

export default async function PostSourceThreadsIndex({
  params: { source, locale },
}: LocaleParams<{ source: ForumPostSource }>) {
  const threads = await getForumThreadsBySource(source);
  const generateHref = (l: Locale) =>
    urls(l).satoshi.posts.sourceThreadsIndex(source);

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={`${formatPostSource(source)} Threads`} />
      <ul>
        {threads.map((t) => (
          <li key={t.id}>
            <Link
              href={urls(locale).satoshi.posts.sourceThreadsDetail(
                t.source,
                t.id.toString(),
              )}
            >
              {t.title}
            </Link>{" "}
            - <em>{formatDate(locale, t.date)}</em>
          </li>
        ))}
      </ul>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams((locale) =>
    zForumPostSource.options.map((source) => ({ locale, source })),
  );
}
