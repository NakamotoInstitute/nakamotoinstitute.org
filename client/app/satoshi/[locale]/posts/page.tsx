import Link from "next/link";
import { PageLayout } from "@/app/components";
import { getSatoshiPosts } from "@/lib/api";
import { getLocaleParams } from "@/lib/i18n";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { PageHeader } from "@/app/components/PageHeader";

export default async function PostsIndex({ params: { locale } }: LocaleParams) {
  const posts = await getSatoshiPosts();
  const generateHref = (l: Locale) => urls(l).satoshi.posts.index;

  return (
    <PageLayout locale={locale} generateHref={generateHref}>
      <PageHeader title="Forum Posts" />
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
            <em>
              {formatDate(locale, p.date, {
                dateStyle: "long",
                timeStyle: "long",
                hourCycle: "h24",
              })}
            </em>
          </li>
        ))}
      </ul>
    </PageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
