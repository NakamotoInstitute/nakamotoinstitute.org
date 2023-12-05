import Link from "next/link";
import { PageHeader } from "@/app/components/PageHeader";
import { PageLayout } from "@/app/components/PageLayout";
import { getSatoshiPostsBySource } from "@/lib/api/posts";
import { ForumPostSource, zForumPostSource } from "@/lib/api/schemas/posts";
import { formatPostSource } from "@/utils/strings";
import { getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";

export default async function PostsSourceIndex({
  params: { source, locale },
}: LocaleParams<{ source: ForumPostSource }>) {
  const posts = await getSatoshiPostsBySource(source);
  const generateHref = (l: Locale) => urls(l).satoshi.posts.sourceIndex(source);

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title={`${formatPostSource(source)} Posts`} />
      <ul>
        {posts.map((p) => (
          <li key={p.satoshiId}>
            <Link
              href={urls(locale).satoshi.posts.sourcePost(
                p.source,
                p.satoshiId.toString(),
              )}
            >
              {p.subject}
            </Link>{" "}
            <em>{p.date.toString()}</em>
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
