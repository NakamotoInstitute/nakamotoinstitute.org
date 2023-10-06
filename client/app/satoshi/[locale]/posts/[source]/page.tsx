import Link from "next/link";
import { PageLayout, PageHeader } from "@/app/components";
import {
  ForumPostSource,
  getSatoshiPostsBySource,
  zForumPostSource,
} from "@/lib/api";
import { formatPostSource } from "@/utils/strings";
import { getLocaleParams } from "@/lib/i18n";
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
