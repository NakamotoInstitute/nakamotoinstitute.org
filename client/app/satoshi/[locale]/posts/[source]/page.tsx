import { Metadata } from "next";
import Link from "next/link";

import { locales } from "@/i18n";
import { getSatoshiPostsBySource } from "@/lib/api/posts";
import { ForumPostSource, zForumPostSource } from "@/lib/api/schemas/posts";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatPostSource, otherForumPostSource } from "@/utils/strings";

import { IndexPageLayout } from "@satoshi/components/IndexPageLayout";

export const dynamicParams = false;

const generateHref = (source: ForumPostSource) => (l: Locale) =>
  urls(l).satoshi.posts.sourceIndex(source);

export async function generateMetadata({
  params: { locale, source },
}: LocaleParams<{ source: ForumPostSource }>): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref(source));

  return {
    title: t("{{source}} Posts", { source: formatPostSource(source) }),
    alternates: { languages },
  };
}

export default async function PostsSourceIndex({
  params: { source, locale },
}: LocaleParams<{ source: ForumPostSource }>) {
  const { t } = await i18nTranslation(locale);
  const posts = await getSatoshiPostsBySource(source);

  const otherSource = otherForumPostSource(source);

  const navLinks = {
    main: {
      text: t("View threads"),
      href: urls(locale).satoshi.posts.sourceThreadsIndex(source),
    },
    left: {
      text: t("All posts"),
      href: urls(locale).satoshi.posts.index,
      sublink: {
        text: t("Threads"),
        href: urls(locale).satoshi.posts.threadsIndex,
      },
    },
    right: {
      text: formatPostSource(otherSource),
      href: urls(locale).satoshi.posts.sourceIndex(otherSource),
      sublink: {
        text: t("Threads"),
        href: urls(locale).satoshi.posts.sourceThreadsIndex(otherSource),
      },
    },
  };
  return (
    <IndexPageLayout
      title={t("{{source}} Posts", { source: formatPostSource(source) })}
      locale={locale}
      generateHref={generateHref(source)}
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
