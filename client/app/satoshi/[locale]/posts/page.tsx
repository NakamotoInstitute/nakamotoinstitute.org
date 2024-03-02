import { Metadata } from "next";
import Link from "next/link";

import { locales } from "@/i18n";
import { getSatoshiPosts } from "@/lib/api/posts";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatPostSource } from "@/utils/strings";

import { IndexPageLayout } from "@satoshi/components/IndexPageLayout";

export const dynamicParams = false;

const generateHref = (l: Locale) => urls(l).satoshi.posts.index;

export async function generateMetadata({
  params: { locale },
}: LocaleParams): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref);

  return {
    title: t("Forum Posts"),
    alternates: { languages },
  };
}

export default async function PostsIndex({ params: { locale } }: LocaleParams) {
  const posts = await getSatoshiPosts();

  const navLinks = {
    main: {
      text: "View threads",
      href: urls(locale).satoshi.posts.threadsIndex,
    },
    left: {
      text: formatPostSource("p2pfoundation"),
      href: urls(locale).satoshi.posts.sourceIndex("p2pfoundation"),
      sublink: {
        text: "Threads",
        href: urls(locale).satoshi.posts.sourceThreadsIndex("p2pfoundation"),
      },
    },
    right: {
      text: formatPostSource("bitcointalk"),
      href: urls(locale).satoshi.posts.sourceIndex("bitcointalk"),
      sublink: {
        text: "Threads",
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
