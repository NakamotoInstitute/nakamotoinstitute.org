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
    title: t("forum_posts"),
    alternates: {
      canonical: generateHref(locale),
      languages,
    },
  };
}

export default async function PostsIndex({ params: { locale } }: LocaleParams) {
  const { t } = await i18nTranslation(locale);
  const posts = await getSatoshiPosts();

  return (
    <IndexPageLayout
      t={t}
      title={t("forum_posts")}
      locale={locale}
      generateHref={generateHref}
      sourceLinks={[
        {
          name: t("all"),
          active: true,
        },
        {
          name: formatPostSource("p2pfoundation"),
          href: urls(locale).satoshi.posts.sourceIndex("p2pfoundation"),
        },
        {
          name: formatPostSource("bitcointalk"),
          href: urls(locale).satoshi.posts.sourceIndex("bitcointalk"),
        },
      ]}
      toggleLinks={{
        active: "individual",
        href: urls(locale).satoshi.posts.threadsIndex,
      }}
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
