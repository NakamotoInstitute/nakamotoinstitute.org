import { Metadata } from "next";
import Link from "next/link";

import { locales } from "@/i18n";
import { getForumThreadsBySource } from "@/lib/api/posts";
import { ForumPostSource, zForumPostSource } from "@/lib/api/schemas/posts";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatPostSource, otherForumPostSource } from "@/utils/strings";

import { IndexPageLayout } from "@satoshi/components/IndexPageLayout";

export const dynamicParams = false;

const generateHref = (source: ForumPostSource) => (l: Locale) =>
  urls(l).satoshi.posts.sourceThreadsIndex(source);

export async function generateMetadata({
  params: { locale, source },
}: LocaleParams<{ source: ForumPostSource }>): Promise<Metadata> {
  const { t } = await i18nTranslation(locale);
  const languages = generateHrefLangs([...locales], generateHref(source));

  return {
    title: t("{{source}} Threads", { source: formatPostSource(source) }),
    alternates: { languages },
  };
}

export default async function PostSourceThreadsIndex({
  params: { source, locale },
}: LocaleParams<{ source: ForumPostSource }>) {
  const threads = await getForumThreadsBySource(source);

  const otherSource = otherForumPostSource(source);

  const navLinks = {
    main: {
      label: "View posts",
      href: urls(locale).satoshi.posts.sourceIndex(source),
    },
    left: {
      label: "All threads",
      href: urls(locale).satoshi.posts.threadsIndex,
      sublink: {
        label: "Posts",
        href: urls(locale).satoshi.posts.index,
      },
    },
    right: {
      label: formatPostSource(otherSource),
      href: urls(locale).satoshi.posts.sourceThreadsIndex(otherSource),
      sublink: {
        label: "Posts",
        href: urls(locale).satoshi.posts.sourceIndex(otherSource),
      },
    },
  };

  return (
    <IndexPageLayout
      title={`${formatPostSource(source)} Threads`}
      locale={locale}
      generateHref={generateHref(source)}
      navLinks={navLinks}
    >
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
            <em>({formatDate(locale, t.date)})</em>
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
