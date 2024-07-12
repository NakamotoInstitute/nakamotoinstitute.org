import { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { PageLayout } from "@/app/components/PageLayout";
import { locales } from "@/i18n";
import { getForumPost, getSatoshiPosts } from "@/lib/api/posts";
import { ForumPostSource } from "@/lib/api/schemas/posts";
import { i18nTranslation } from "@/lib/i18n/i18nTranslation";
import { generateHrefLangs, getLocaleParams } from "@/lib/i18n/utils";
import { urls } from "@/lib/urls";
import { formatDate } from "@/utils/dates";
import { formatPostSource } from "@/utils/strings";

import { PostNavigation } from "@satoshi/components/ContentNavigation";

export const dynamicParams = false;

const generateHref =
  (source: ForumPostSource, satoshiId: string) => (l: Locale) =>
    urls(l).satoshi.posts.sourcePost(source, satoshiId);

export async function generateMetadata({
  params: { locale, source, satoshiId },
}: LocaleParams<{
  source: ForumPostSource;
  satoshiId: string;
}>): Promise<Metadata> {
  const postData = await getForumPost(source, satoshiId);
  const languages = generateHrefLangs(
    [...locales],
    generateHref(source, satoshiId),
  );

  return {
    title: postData.post.subject,
    alternates: {
      canonical: generateHref(source, satoshiId)(locale),
      languages,
    },
  };
}

export default async function PostDetail({
  params: { source, satoshiId, locale },
}: LocaleParams<{ source: ForumPostSource; satoshiId: string }>) {
  const postData = await getForumPost(source, satoshiId);
  if (!postData) {
    return notFound();
  }

  const { t } = await i18nTranslation(locale);
  const { next, previous, post } = postData;

  return (
    <PageLayout
      t={t}
      locale={locale}
      generateHref={generateHref(source, satoshiId)}
      breadcrumbs={[
        { label: t("complete_satoshi"), href: urls(locale).satoshi.index },
        { label: t("forum_posts"), href: urls(locale).satoshi.emails.index },
      ]}
    >
      <PostNavigation
        t={t}
        className="mb-2"
        locale={locale}
        source={post.source}
        previous={previous}
        next={next}
      />
      <div>
        <h2 className="text-2xl">{formatPostSource(post.source)}</h2>
        <h1 className="text-4xl">{post.subject}</h1>
        <p className="text-xl">
          <time dateTime={post.date.toISOString()}>
            {formatDate(locale, post.date, {
              dateStyle: "long",
              timeStyle: "long",
              hourCycle: "h24",
            })}
          </time>
        </p>
        <div className="flex gap-2">
          <Link href={post.url}>{t("original_post")}</Link> •{" "}
          <Link
            href={{
              pathname: urls(locale).satoshi.posts.sourceThreadsDetail(
                post.source,
                post.threadId.toString(),
              ),
              hash: post.sourceId.toString(),
            }}
          >
            {t("view_in_thread")}
          </Link>
        </div>
      </div>
      <hr className="my-4" />
      <div
        dangerouslySetInnerHTML={{
          __html: post.text,
        }}
      />
      <PostNavigation
        t={t}
        className="mt-4"
        locale={locale}
        previous={previous}
        next={next}
        source={post.source}
        reverse
      />
    </PageLayout>
  );
}

// export async function generateStaticParams() {
//   const posts = await getSatoshiPosts();
//   return getLocaleParams((locale) =>
//     posts
//       .filter((p) => p.satoshiId)
//       .map((p) => ({
//         locale,
//         source: p.source,
//         satoshiId: p.satoshiId!.toString(),
//       })),
//   );
// }
