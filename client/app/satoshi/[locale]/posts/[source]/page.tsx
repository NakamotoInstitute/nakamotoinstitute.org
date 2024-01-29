import { Metadata } from "next";
import Link from "next/link";

import { getSatoshiPostsBySource } from "@/lib/api/posts";
import { ForumPostSource, zForumPostSource } from "@/lib/api/schemas/posts";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatPostSource, otherForumPostSource } from "@/utils/strings";

import { IndexPageLayout } from "@satoshi/components/IndexPageLayout";

export const dynamicParams = false;

export async function generateMetadata({
  params: { locale, source },
}: LocaleParams<{ source: ForumPostSource }>): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  return {
    title: t("{{source}} Posts", { source: formatPostSource(source) }),
  };
}

export default async function PostsSourceIndex({
  params: { source, locale },
}: LocaleParams<{ source: ForumPostSource }>) {
  const posts = await getSatoshiPostsBySource(source);
  const generateHref = (l: Locale) => urls(l).satoshi.posts.sourceIndex(source);

  const otherSource = otherForumPostSource(source);

  const navLinks = {
    main: {
      label: "View threads",
      href: urls(locale).satoshi.posts.sourceThreadsIndex(source),
    },
    left: {
      label: "All posts",
      href: urls(locale).satoshi.posts.index,
      sublink: {
        label: "Threads",
        href: urls(locale).satoshi.posts.threadsIndex,
      },
    },
    right: {
      label: formatPostSource(otherSource),
      href: urls(locale).satoshi.posts.sourceIndex(otherSource),
      sublink: {
        label: "Threads",
        href: urls(locale).satoshi.posts.sourceThreadsIndex(otherSource),
      },
    },
  };
  return (
    <IndexPageLayout
      title={`${formatPostSource(source)} Posts`}
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
  return getLocaleParams((locale) =>
    zForumPostSource.options.map((source) => ({ locale, source })),
  );
}
