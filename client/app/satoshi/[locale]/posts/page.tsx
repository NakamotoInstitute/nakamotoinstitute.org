import Link from "next/link";
import { getSatoshiPosts } from "@/lib/api/posts";
import { getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatPostSource } from "@/utils/strings";
import { IndexPageLayout } from "@satoshi/components/IndexPageLayout";

export default async function PostsIndex({ params: { locale } }: LocaleParams) {
  const posts = await getSatoshiPosts();
  const generateHref = (l: Locale) => urls(l).satoshi.posts.index;

  const navLinks = {
    main: {
      label: "View threads",
      href: urls(locale).satoshi.posts.threadsIndex,
    },
    left: {
      label: formatPostSource("p2pfoundation"),
      href: urls(locale).satoshi.posts.sourceIndex("p2pfoundation"),
      sublink: {
        label: "Threads",
        href: urls(locale).satoshi.posts.sourceThreadsIndex("p2pfoundation"),
      },
    },
    right: {
      label: formatPostSource("bitcointalk"),
      href: urls(locale).satoshi.posts.sourceIndex("bitcointalk"),
      sublink: {
        label: "Threads",
        href: urls(locale).satoshi.posts.sourceThreadsIndex("bitcointalk"),
      },
    },
  };
  return (
    <IndexPageLayout
      title="Forum Posts"
      locale={locale}
      generateHref={generateHref}
      navLinks={navLinks}
    >
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
              (
              {formatDate(locale, p.date, {
                dateStyle: "medium",
                timeStyle: "long",
                hourCycle: "h24",
              })}
              )
            </em>
          </li>
        ))}
      </ul>
    </IndexPageLayout>
  );
}

export function generateStaticParams() {
  return getLocaleParams();
}
